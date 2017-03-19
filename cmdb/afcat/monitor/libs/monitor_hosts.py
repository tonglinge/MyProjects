#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun 
@date 16/9/7
"""
import time
import re
from afcat.monitor import models
from django.db.models import Q, QuerySet
from django.db import connection, transaction
from django.db.utils import ProgrammingError
from collections import OrderedDict
from afcat.settings import MONITOR_SERVER

host_status = {
    0: "已启用",
    1: "停用的",
    3: "模版",
    5: "主动模式",
    6: "被动模式",
}

host_available = {
    0: "未知",
    1: "可用",
    2: "不可用",
}

host_ipmi_available = {
    0: "未知",
    1: "可用",
    2: "不可用",
}

host_jmx_available = {
    0: "未知",
    1: "可用",
    2: "不可用",
}

host_snmp_available = {
    0: "未知",
    1: "可用",
    2: "不可用",
}


# 触发器的事件等级
priority_type = {
    0: "未分类",
    1: "信息",
    2: "警告",
    3: "一般严重",
    4: "严重",
    5: "灾难",
}
# 触发器当前是否触发状态
issue_type = {
    0: "正常",
    1: "问题",
}

acknowledged_type = {
    0: "否",
    1: "是",
}

available_type = {
    0: "停用",
    1: "可用",
    2: "不可用",
}


def exec_raw_sql(raw_sql, param):
    """
    通过执行原生sql返回结果
    :param raw_sql: 原生sql语句
    :param param: sql参数
    :return:
    """
    try:
        raw_sql = raw_sql % param
        cursor = connection.cursor()
        cursor.execute(raw_sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(e)
    return []


class TimeFormat(object):
    @staticmethod
    def time_stamp_to_std(arg):
        time_format = '%Y-%m-%d %H:%M:%S'
        time_obj = time.localtime(arg)
        std_time = time.strftime(time_format, time_obj)
        return std_time

    @staticmethod
    def std_to_time_stamp(arg):
        time_format = '%Y-%m-%d %H:%M:%S'
        time_obj = time.strptime(arg, time_format)
        time_stamp = time.mktime(time_obj)
        return time_stamp


class ConfigHost(object):

    def __init__(self, filter_host=None, filter_dns=None, filter_ip=None, filter_port=None, filter_rst=1, filter_set=None):
        self.limit, self.offset = 25, 0  # 限制每页取多少数据，默认每次取25条数据，从第一条开始
        self.info = None
        self.filter_host = "AND h.name LIKE '%{}%'".format(filter_host) if filter_host else ""
        self.filter_dns = "AND net.dns LIKE '%{}%'".format(filter_dns) if filter_dns else ""
        self.filter_ip = "AND net.ip LIKE '%{}%'".format(filter_ip) if filter_ip else ""
        self.filter_port = "AND net.`port` = '%s'" % filter_port if filter_port else ""
        self.filter_rst = filter_rst
        self.filter_set = filter_set

    def exec_raw_sql(self, raw_sql, param=None, *args, **kwargs):
        """
        通过执行原生sql返回结果
        :param raw_sql: 原生sql语句
        :param param: sql参数
        :return:
        """
        try:
            if param is not None:
                raw_sql = raw_sql % param
            elif args:
                raw_sql = raw_sql % args
            cursor = connection.cursor()
            cursor.execute(raw_sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            self.info = e
        return []

    def __getitem__(self, limit):
        if isinstance(limit, slice):
            if limit.start is not None:
                start = int(limit.start)
            else:
                start = 0
            if limit.stop is not None:
                stop = int(limit.stop)
            else:
                stop = self.limit
            self.set_limits(start, stop)
            return self.filter_data(limit=self.limit, offset=self.offset)

    def set_limits(self, offset=None, end=None):
        if (offset and end) is not None:
            self.limit = end - offset
            self.offset = offset - 1 if offset > 0 else 0
        else:
            # 设置默认偏移量
            self.limit = 25
            self.offset = 0

    def query_data(self, limit=20, offset=0):
        sql = "SELECT DISTINCT h.hostid, h.`name`, h.`status`, h.available, h.snmp_available, h.jmx_available, " \
              "h.ipmi_available FROM `hosts` h, hosts_groups hg, interface net " \
              "WHERE h.hostid = net.hostid " \
              "AND h.hostid = hg.hostid AND h.flags IN(0 , 4) " \
              "%s %s %s %s ORDER BY h.`name` LIMIT %s OFFSET %s"

        query_set = self.exec_raw_sql(sql,
                                      (
                                          self.filter_host,
                                          self.filter_ip,
                                          self.filter_port,
                                          self.filter_dns,
                                          limit,
                                          offset
                                       )
                                      )
        return query_set

    def filter_data(self, limit=20, offset=0):
        query_applications = "SELECT * from applications WHERE hostid='%s'"
        query_items = "SELECT * FROM items WHERE hostid = '%s' AND flags IN(0 , 4) ORDER BY `name`"
        query_triggers = "SELECT t.* FROM `hosts` h , items i , `triggers` t , functions f " \
                         "WHERE h.hostid = i.hostid AND i.itemid = f.itemid " \
                         "AND t.triggerid = f.triggerid AND h.hostid = '%s' AND t.flags IN(0 , 4)"
        query_graphs = "SELECT DISTINCT g.graphid , g.`name` " \
                       "FROM `hosts` h , items i , graphs_items gi , graphs g " \
                       "WHERE h.hostid = i.hostid AND i.itemid = gi.itemid " \
                       "AND g.graphid = gi.graphid AND h.hostid = '%s' AND g.flags IN(0 , 4)"
        query_discovery = "SELECT i.* FROM `hosts` h , items i " \
                          "WHERE h.hostid = i.hostid AND h.hostid = '%s' AND i.flags = 1 ORDER BY i.itemid"
        query_interface = "SELECT net.ip , net.`port` " \
                          "FROM `hosts` h , interface net WHERE h.hostid = net.hostid AND h.hostid = '%s' LIMIT 1"
        query_set = self.query_data(limit=limit, offset=offset)
        data = []
        for item in query_set:
            host_detail = dict()
            host_id = item[0]
            host_detail['monitor_server'] = MONITOR_SERVER
            host_detail['host_id'] = host_id
            host_detail['host_name'] = item[1]
            query_applications_set = self.exec_raw_sql(query_applications, (host_id,))
            host_detail['applications_count'] = len(query_applications_set)
            query_items_set = self.exec_raw_sql(query_items, (host_id,))
            host_detail['items_count'] = len(query_items_set)
            query_triggers_set = self.exec_raw_sql(query_triggers, (host_id,))
            host_detail['triggers_count'] = len(query_triggers_set)
            query_graphs_set = self.exec_raw_sql(query_graphs, (host_id,))
            host_detail['graphs_count'] = len(query_graphs_set)
            query_discovery_set = self.exec_raw_sql(query_discovery, (host_id,))
            host_detail['discovery_count'] = len(query_discovery_set)
            query_interface_set = self.exec_raw_sql(query_interface, (host_id,))
            host_detail['interface'] = ":".join(query_interface_set[0])
            host_detail['status_id'] = item[2]
            host_detail['status'] = host_status.get(item[2])
            host_detail['available'] = item[3]
            host_detail['snmp_available'] = item[4]
            host_detail['jmx_available'] = item[5]
            host_detail['ipmi_available'] = item[6]
            data.append(host_detail)
        return data

    def object_list(self):
        return self

    @property
    def has_next(self):
        next_offset = self.offset + self.limit
        query_set = self.query_data(self.limit, next_offset)
        return bool(query_set)


class SearchHostInfo(object):
    """
    处理用户搜索主机组页面
    """

    def __init__(self, group_id=None, host_name=None, ip_address=None, status=None, issue_time=None, issue_level=None):
        self.group_id = group_id
        self.host_name = host_name
        self.ip_address = ip_address
        self.status = status
        self.issue_time = issue_time
        self.issue_level = issue_level
        self.search_info = []

    def filter_info(self):
        """
        通过搜索条件过滤主机，返回主机状态信息
        :return:
        """
        get_all_hosts = self.get_hosts_by_status_time()
        if get_all_hosts:
            for host in get_all_hosts:
                host_info = self.get_host_info(host)
                self.search_info.append(host_info)
            self.search_info.sort(key=lambda info: info['date'], reverse=True)
        return self.search_info

    def get_host_info(self, host):
        """
        通过主机对象获取主机信息
        :param host:
        :return:
        """
        host_info = dict()
        try:
            triggers = self.filter_has_triggered_events_by_host_id(host.hostid).order_by('-lastchange')
        except AttributeError:
            return host_info
        error_msg = ""
        if triggers.count():
            description = triggers.first().description
            error_msg = re.sub('\{.*\}', host.name, description)
            events = self.filter_event_by_trigger_id(triggers.first().triggerid).filter(source=0)
            repeat_count = events.filter(value=1).count()
            ack_count = events.filter(value=1, acknowledged=1).count()
            host_info['confirm'] = "是" if repeat_count == ack_count else "否"
        host_info['hostid'] = host.hostid
        host_info['group'] = self.get_group(host.hostid)
        host_info['hostname'] = host.name
        host_info['ip_address'] = self.get_ip_address(host.hostid)
        host_info['status'] = priority_type.get(triggers.first().priority) if triggers.count() else "正常"
        host_info['status_id'] = 1 if triggers.count() else 0
        host_info['date'] = TimeFormat.time_stamp_to_std(triggers.first().lastchange) if triggers.count() else ""
        host_info['detail'] = error_msg
        return host_info

    def get_host_info_by_host_id(self, host_id):
        """
        通过主机ID获取主机信息
        :param host_id:
        :return:
        """
        host = self.filter_host_by_host_id(host_id)
        host_info = self.get_host_info(host)
        return host_info

    def get_host_graphs_info(self, host_id):
        graphs = self.filter_graphs_by_host_id(host_id)
        graphs_info = []
        for graph_id in graphs:
            graph_info = dict()
            graph_data = self.format_history_data_by_host_id_graph_id(graph_id.graphid)
            graph_info['graph_name'] = graph_id.name
            graph_info['graph_id'] = graph_id.graphid
            graph_info['data'] = graph_data
            graphs_info.append(graph_info)
        return graphs_info

    def get_host_graphs_items(self, host_id):
        """获取主机所有的图形列表"""
        graphs = self.filter_graphs_by_host_id(host_id)
        graphs_info = []
        for graph_id in graphs:
            graph_info = dict()
            graph_info['graph_name'] = graph_id.name
            graph_info['graph_id'] = graph_id.graphid
            graphs_info.append(graph_info)
        return graphs_info

    @staticmethod
    def filter_host_by_host_id(host_id):
        """通过主机ID获取主机"""
        host = models.Hosts.objects.filter(hostid=host_id)
        return host.get() if host.all().count() else None

    def get_all_hosts(self):
        """获取所有的主机"""
        all_hosts = models.Hosts.objects.filter(Q(status__in=[0, 1]), ~Q(flags=2))
        if self.group_id:
            hosts_id = models.HostsGroups.objects.filter(groupid=self.group_id).values('hostid')
            all_hosts = models.Hosts.objects.filter(hostid__in=hosts_id)
        return all_hosts

    def get_hosts_by_host_name(self):
        """获取过滤条件主机名或主机别名的所有主机对象"""
        all_hosts = self.get_all_hosts()
        if self.host_name:
            all_hosts = all_hosts.filter(Q(name__contains=self.host_name) | Q(host__contains=self.host_name))
        return all_hosts

    @staticmethod
    def get_ip_address(host_id):
        """
        通过主机ID获取ip地址
        :param host_id:
        :return:
        """
        ip_obj = models.Interface.objects.filter(hostid=host_id).values('ip')
        return list(map(lambda get: get['ip'], ip_obj))

    @staticmethod
    def get_group(host_id):
        """
        通过主机id获取组名
        :param host_id:
        :return:
        """
        group_id = models.HostsGroups.objects.filter(hostid=host_id).values("groupid")
        groups_obj = models.Groups.objects.filter(groupid__in=group_id).values('name')
        return list(map(lambda get: get['name'], groups_obj))

    def get_hosts_by_interface(self):
        """获取过滤条件IP地址后的主机对象"""
        all_hosts = self.get_hosts_by_host_name()
        if all_hosts and self.ip_address:
            all_hosts = self.filter_hosts_with_ip_by_hosts_queryset(all_hosts)
        return all_hosts

    def get_hosts_by_status(self):
        """获取过滤条件主机状态是否可用的主机对象"""
        all_hosts = self.get_hosts_by_interface()
        if all_hosts and self.status:
            all_hosts = all_hosts.filter(available=self.status)
        return all_hosts

    def get_hosts_by_priority(self):
        """通过优先级过滤主机"""
        all_hosts = self.get_hosts_by_status()
        if all_hosts and self.issue_level and str(self.issue_level) != "0":
            all_hosts = self.filter_hosts_with_priority_by_hosts_queryset(all_hosts)
        return all_hosts

    def get_hosts_by_status_time(self):
        """通过故障时间过滤主机,如果主机无故障则也返回"""
        all_hosts = self.get_hosts_by_priority()
        if all_hosts and self.issue_time:
            self.issue_time = TimeFormat.std_to_time_stamp(self.issue_time)
            triggers = self.filter_hosts_triggers_by_hosts_id(all_hosts.values('hostid'))
            triggers = triggers.filter(Q(lastchange__gte=self.issue_time, value=1))
            all_hosts = self.filter_hosts_by_triggers_id(triggers.values('triggerid'))
        return all_hosts

    @staticmethod
    def filter_interface_by_hosts_queryset(hosts_queryset):
        """通过主机queryset获取IP"""
        hosts_ip = models.Interface.objects.filter(hostid__in=hosts_queryset.values('hostid'))
        return hosts_ip

    @staticmethod
    def filter_hosts_id_by_ip_address(ip_address):
        """通过主机IP获取主机ID"""
        hosts_id = models.Interface.objects.filter(ip__contains=ip_address).values('hostid')
        return hosts_id

    def filter_hosts_with_priority_by_hosts_queryset(self, hosts, value=1):
        """
        通过优先级过滤主机
        :param hosts:
        :param value: 1为已触发的，0为未触发,None表示去除value这个条件
        :return:
        """
        triggers = self.filter_hosts_triggers_by_hosts_id(hosts.values('hostid'))
        if value is None:
            filter_triggers_id = triggers.filter(priority=self.issue_level).values('triggerid')
        else:
            filter_triggers_id = triggers.filter(priority=self.issue_level, value=value).values('triggerid')
        hosts = self.filter_hosts_by_triggers_id(filter_triggers_id)
        return hosts

    def filter_hosts_with_ip_by_hosts_queryset(self, hosts):
        """通过IP地址条件过滤主机"""
        filter_hosts_ip = self.filter_interface_by_hosts_queryset(hosts)
        hosts_id = filter_hosts_ip.filter(ip__contains=self.ip_address).values('hostid_id')
        hosts = hosts.filter(hostid__in=hosts_id)
        return hosts

    @staticmethod
    def filter_host_items_by_host_id(host_id):
        """通过单台主机id获取主机对items对象"""
        items = models.Items.objects.filter(hostid=host_id)
        return items

    @staticmethod
    def filter_hosts_items_id_by_hosts_id(hosts_id):
        """通过主机列表id获取主机列表监控项"""
        items_id = models.Items.objects.filter(hostid__in=hosts_id).values('itemid')
        return items_id if items_id else []

    @staticmethod
    def filter_hosts_id_by_items_id(items_id):
        """通过主机items ID获取主机列表ID"""
        hosts_id = models.Items.objects.filter(itemid__in=items_id).values('hostid')
        return hosts_id if hosts_id else []

    @staticmethod
    def filter_hosts_triggers_id_by_items_id(items_id):
        """通过items id列表获取triggers id列表"""
        triggers_id = models.Functions.objects.filter(itemid__in=items_id).values('triggerid')
        return triggers_id if triggers_id else []

    @staticmethod
    def filter_hosts_items_id_by_triggers_id(triggers_id):
        """通过主机triggers ID获取主机items ID"""
        items_id = models.Functions.objects.filter(triggerid__in=triggers_id).values('itemid')
        return items_id if items_id else []

    @staticmethod
    def filter_host_item_id_by_trigger_id(trigger_id):
        """通过triggerID获取itemID"""
        item_id = models.Functions.objects.filter(triggerid=trigger_id).values('itemid')
        return item_id

    @staticmethod
    def filter_host_id_by_item_id(item_id):
        host_id = models.Items.objects.filter(itemid__in=item_id).values('hostid')
        return host_id

    def filter_host_by_trigger_id(self, trigger_id):
        """通过triggerID获取主机对象"""
        item_id = self.filter_host_item_id_by_trigger_id(trigger_id)
        host_id = self.filter_host_id_by_item_id(item_id)
        host = models.Hosts.objects.filter(hostid__in=host_id).distinct()
        return host

    @staticmethod
    def filter_hosts_triggers_by_triggers_id(triggers_id):
        """通过triggers_id获取triggers对象,排除触发器模版，类似网卡触发器模版和磁盘模版"""
        triggers = models.Triggers.objects.filter(triggerid__in=triggers_id).exclude(flags=2)
        return triggers

    def filter_hosts_triggers_by_items_id(self, items_id):
        """通过itemsID获取triggers对象"""
        triggers_id = self.filter_hosts_triggers_id_by_items_id(items_id)
        triggers = self.filter_hosts_triggers_by_triggers_id(triggers_id)
        return triggers

    def filter_hosts_id_by_triggers_id(self, triggers_id):
        """通过触发器ID列表获取主机ID列表"""
        items_id = self.filter_hosts_items_id_by_triggers_id(triggers_id)
        hosts_id = self.filter_hosts_id_by_items_id(items_id)
        return hosts_id

    def filter_hosts_by_triggers_id(self, triggers_id):
        """通过触发器ID列表获取主机列表对象"""
        hosts_id = self.filter_hosts_id_by_triggers_id(triggers_id)
        hosts = models.Hosts.objects.filter(hostid__in=hosts_id)
        return hosts

    def filter_host_triggers_by_host_id(self, host_id):
        """通过单台主机ID获取触发器对象"""
        items_id = self.filter_host_items_by_host_id(host_id).values('itemid')
        triggers = self.filter_hosts_triggers_by_items_id(items_id)
        return triggers

    def filter_hosts_triggers_by_hosts_id(self, hosts_id):
        """通过主机列表对象ID获取触发器"""
        items_id = self.filter_hosts_items_id_by_hosts_id(hosts_id)
        triggers = self.filter_hosts_triggers_by_items_id(items_id)
        return triggers

    def filter_has_triggered_events_by_host_id(self, host_id):
        """通过主机ID获取被触发的触发器对象"""
        triggers = self.filter_host_triggers_by_host_id(host_id).filter(value=1)
        return triggers

    @staticmethod
    def filter_events_by_triggers_id(triggers_id):
        """通过triggersID获取触发事件集合"""
        events = models.Events.objects.filter(objectid__in=triggers_id)
        return events

    @staticmethod
    def filter_event_by_trigger_id(trigger_id):
        """通过triggerID获取事件event对象"""
        events = models.Events.objects.filter(objectid=trigger_id)
        return events

    def filter_history_by_item_id(self, item_id):
        """通过itemID获取该item历史数据"""
        item = self.filter_item_by_item_id(item_id)
        value_type = item.first().value_type
        history_type = "filter_history_with_type_{}_by_item_id".format(value_type)
        if hasattr(self, history_type):
            history = getattr(self, history_type)
            return history(item_id).order_by('-clock')
        return {}

    @staticmethod
    def filter_history_with_type_0_by_item_id(item_id):
        """通过item ID获取valueType=0的数据"""
        history = models.History.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_history_with_type_1_by_item_id(item_id):
        """通过item ID获取valueType=1的数据"""
        history = models.HistoryStr.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_history_with_type_2_by_item_id(item_id):
        """通过item ID获取valueType=2的数据"""
        history = models.HistoryLog.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_history_with_type_3_by_item_id(item_id):
        """通过item ID获取valueType=3的数据"""
        history = models.HistoryUint.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_history_with_type_4_by_item_id(item_id):
        """通过item ID获取valueType=4的数据"""
        history = models.HistoryText.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_item_by_item_id(item_id):
        """通过item ID获取item对象"""
        item = models.Items.objects.filter(itemid=item_id)
        return item

    def format_item_name_by_item_id(self, item_id, name=None, key=None):
        """
        通过item ID获取对应的监控项名称
        :param item_id:
        :return: 格式化名称返回
        """
        if name is not None:
            item_name = name
            item_key = key
        else:
            item = self.filter_item_by_item_id(item_id)
            item_name = item.first().name
            item_key = item.first().key_field
        match_str = re.findall('\$\d', item_name)
        try:
            if match_str:
                for position in match_str:
                    index = str(position).lstrip('$')
                    key = re.search('\[.*\]', item_key)
                    key = str(key.group()).strip('[]').split(',') if key else []
                    item_name = re.sub('\$\d', key[int(index) - 1], item_name, count=match_str.index(position) + 1)
        except IndexError:
            pass
        return item_name

    def filter_history_by_items_id(self, items_id):
        """
        通过itemsID获取每个item对应的历史数据
        :param items_id: 需要是一个列表格式的字典元素数据
        :return:
        """
        history = []
        for item_id in items_id:
            if type(item_id) is dict:
                item_id = item_id.get('itemid')
            history.append(self.filter_history_by_item_id(item_id))
        return history

    def filter_host_history_by_host_id(self, host_id):
        """通过hostID获取主机监控项历史数据"""
        items_id = self.filter_host_items_by_host_id(host_id).values('itemid')
        history = self.filter_history_by_items_id(items_id)
        return history

    @staticmethod
    def filter_graphs_id_by_items_id(items_id):
        """通过itemsID获取所有相关的graphID"""
        graphs_id = models.GraphsItems.objects.filter(itemid__in=items_id).values('graphid').distinct()
        return graphs_id

    def filter_graphs_by_host_id(self, host_id):
        """通过主机ID获取该主机对应的所有图形"""
        items_id = self.filter_host_items_by_host_id(host_id).values('itemid')
        graphs_id = self.filter_graphs_id_by_items_id(items_id)
        graphs = self.filter_graphs_by_graphs_id(graphs_id)
        return graphs

    @staticmethod
    def filter_graphs_by_graphs_id(graphs_id):
        """通过graphID列表获取graph对象"""
        graphs = models.Graphs.objects.filter(Q(graphid__in=graphs_id) & ~Q(flags=2))
        return graphs

    @staticmethod
    def filter_graph_items_id_by_graph_id(graph_id):
        """通过graphID获取对应的itemsID列表"""
        items_id = models.GraphsItems.objects.filter(graphid=graph_id).values('itemid')
        return items_id

    def filter_graph_items_id_by_graphs_id(self, graphs_id):
        """通过graphsID获取列表形式的{graph_id：items}列表"""
        items_id = []
        for graph_id in graphs_id:
            if type(graph_id) is dict:
                graph_id = graph_id.get('graphid')
            item_id = self.filter_graph_items_id_by_graph_id(graph_id)
            items_id.append({graph_id: item_id})
        return items_id

    def format_history_data_by_host_id_graph_id(self, graph_id):
        """通过graphID获取该图形数据
        :return [{'date':[], 'values': []}]
        """
        graph_data = []
        if type(graph_id) is dict:
            graph_id = graph_id.get('graphid')
        items_id = self.filter_graph_items_id_by_graph_id(graph_id)
        for item_id in items_id:
            item_data = dict()
            if type(item_id) is dict:
                item_id = item_id.get('itemid')
            item_name = self.format_item_name_by_item_id(item_id)
            item_data['item_name'] = item_name
            history = list(self.filter_history_by_item_id(item_id)[1:60])
            history.sort(key=lambda get: get.clock)
            if history:
                date = list(map(lambda get: "'" + TimeFormat.time_stamp_to_std(get.clock) + "'", history))
                values = list(map(lambda get: str(get.value), history))
                item_data['date'] = date
                item_data['values'] = values
                graph_data.append(item_data)
        return graph_data


class SearchEventTrigger(SearchHostInfo):
    def __init__(self, group_id=None, host_id=None, ip_address=None, issue_level=None, ack=None, trigger_end_time=None,
                 start_time=None, end_time=None):
        """
        初始化触发器事件
        :param group_id: 主机组ID
        :param host_id: 主机ID
        :param ack: 是否确认
        :param trigger_end_time: 触发器截止时间
        :param start_time: 开始时间
        :param end_time: 结束时间
        """
        super().__init__(self, ip_address=ip_address, issue_level=issue_level)
        self.group_id = group_id
        self.host_id = host_id
        self.ack = ack
        self.start_time = start_time
        self.end_time = end_time
        self.trigger_end_time = trigger_end_time
        self.black_list = ['Templates', 'Linux servers', 'Zabbix servers', 'Discovered hosts', 'Virtual machines',
                           'Hypervisors']

    def get_groups(self, filter_null_group=True):
        """
        获取所有主机组
        :param filter_null_group: 是否过滤空组，即改组没有任何主机加入
        :return: 主机组query set
        """
        if filter_null_group:
            hosts_id = self.get_all_hosts().filter(~Q(status=1)).values('hostid')
            groups_id = self.filter_groups_id_by_hosts_id(hosts_id)
            groups = models.Groups.objects.filter(groupid__in=groups_id)
        else:
            groups = models.Groups.objects.all()
        return groups

    def filter_groups_by_group_id(self, group_id):
        """
        通过groupID获取主机组对象
        :param group_id:
        :return:
        """
        group = self.get_groups().filter(groupid=group_id)
        return group

    def filter_hosts_id_by_group_id(self, group_id):
        """
        通过groupID获取主机ID对象
        :param group_id:
        :return:
        """
        hosts_id = models.HostsGroups.objects.filter(groupid=group_id)
        if str(group_id) == "0":
            # groups_id = self.get_groups().values('groupid')
            # hosts_id = self.filter_hosts_id_by_groups_id(groups_id)
            hosts_id = self.get_all_hosts()
        return hosts_id

    @staticmethod
    def filter_hosts_id_by_groups_id(groups_id):
        """通过主机组ID获取主机ID"""
        hosts_id = models.HostsGroups.objects.filter(groupid__in=groups_id)
        return hosts_id

    @staticmethod
    def filter_groups_id_by_hosts_id(hosts_id):
        """通过主机ID获取主机组ID"""
        groups_id = models.HostsGroups.objects.filter(hostid__in=hosts_id).values('groupid').distinct()
        return groups_id

    @staticmethod
    def filter_hosts_by_hosts_id(hosts_id):
        """
        通过主机ID集合获取主机对象，排除停用的主机
        :param hosts_id:
        :return:
        """
        hosts = models.Hosts.objects.filter(hostid__in=hosts_id, status=0)
        return hosts

    def filter_hosts_by_group_id(self, group_id):
        """
        通过groupID获取主机对象
        :param group_id:
        :return:
        """
        hosts_id = self.filter_hosts_id_by_group_id(group_id)
        hosts = self.filter_hosts_by_hosts_id(hosts_id.values('hostid'))
        return hosts

    @staticmethod
    def format_host_objects(hosts):
        """
        将hosts集合对象格式化输出为{host_id: id,host_name: name}格式
        :param hosts: queryset集合
        :return:
        """
        hosts_list = []
        if type(hosts) is QuerySet:
            for host in hosts:
                hosts_list.append({'host_id': host.hostid, 'host_name': host.name})
        return hosts_list

    @staticmethod
    def format_group_objects(groups):
        """
        将groups集合对象格式化输出为{group_id: id, group_name: name}格式
        :param groups:queryset集合
        :return:
        """
        groups_list = []
        if type(groups) is QuerySet:
            for group in groups:
                groups_list.append({'group_id': group.groupid, 'group_name': group.name})
        return groups_list

    def get_group_info(self, filter_null_group=True):
        groups = self.get_groups(filter_null_group).all()
        groups = self.format_group_objects(groups)
        return groups

    def get_hosts_info(self, group_id):
        """
        通过groupID获取主机组下的主机列表
        :param group_id:
        :return:
        """
        hosts = self.filter_hosts_by_group_id(group_id)
        hosts = self.format_host_objects(hosts)
        return hosts

    def get_hosts_groups_rel(self):
        """
        获取主机组以及对应的主机
        [{"group_id":group_id, "group_name": group_name, hosts: [{"host_id": host_id, "host_name": host_name}]}]
        :return:
        """
        hosts_groups_rel = []
        groups = self.get_group_info(filter_null_group=False)
        for group in groups:
            if group.get("group_name") in self.black_list:
                continue
            context = dict()
            group_id = group.get('group_id')
            context['group_id'] = group_id
            context['group_name'] = group.get("group_name")
            context['hosts'] = []
            hosts = self.get_hosts_info(group_id)
            for host in hosts:
                context['hosts'].append({'host_id': host.get("host_id"), "host_name": host.get("host_name")})
            hosts_groups_rel.append(context)
        return hosts_groups_rel

    def get_groups_menu(self):
        """
        获取主机组菜单
        :return:
        """
        context = []
        groups = self.get_group_info()
        for group in groups:
            if group.get('group_name') in self.black_list:
                continue
            context.append(group)
        return context


class EventTriggers(object):
    def __init__(self,
                 page=0,
                 group_id=None,
                 host_id=None,
                 ip_address=None,
                 issue_level=None,
                 ack=None,
                 start_time=None,
                 end_time=None,
                 trigger_end_time=None):
        """
        初始化触发器事件
        :param page: 获取第几页数据
        :param group_id: 主机组ID
        :param host_id: 主机ID
        :param ack: 是否确认
        :param trigger_end_time: 触发器截止时间
        :param start_time: 开始时间
        :param end_time: 结束时间
        """
        self.page = page
        self.limit, self.offset = 25, 0  # 限制每页取多少数据，默认每次取25条数据，从第一条开始
        self.info = None
        self.group_id = "AND g.groupid='%s'" % group_id if group_id and group_id != "0" else ""
        self.host_id = "AND h.hostid='%s'" % host_id if host_id and host_id != "0" else ""
        self.ip_address = "AND net.ip LIKE '%{}%'".format(ip_address) if ip_address else ""
        self.issue_level = "AND t.priority='%s'" % issue_level if issue_level and issue_level != "0" else ""
        self.ack = "AND e.acknowledged='%s'" % ack if ack else ""
        self.start_time = "AND t.lastchange>=UNIX_TIMESTAMP('%s')" % start_time if start_time else ""
        self.end_time = "AND t.lastchange<=UNIX_TIMESTAMP('%s')" % end_time if end_time else ""
        self.trigger_end_time = "AND e.clock>=UNIX_TIMESTAMP('%s')" % trigger_end_time if trigger_end_time else ""

    def exec_raw_sql(self, raw_sql, param=None, *args, **kwargs):
        """
        通过执行原生sql返回结果
        :param raw_sql: 原生sql语句
        :param param: sql参数
        :return:
        """
        try:
            if param is not None:
                raw_sql = raw_sql % param
            elif args:
                raw_sql = raw_sql % args
            cursor = connection.cursor()
            cursor.execute(raw_sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            self.info = e
        return []

    def __getitem__(self, limit):
        if isinstance(limit, slice):
            if limit.start is not None:
                start = int(limit.start)
            else:
                start = 0
            if limit.stop is not None:
                stop = int(limit.stop)
            else:
                stop = self.limit
            self.set_limits(start, stop)
            return self.filter_data(limit=self.limit, offset=self.offset)

    def set_limits(self, offset=None, end=None):
        if (offset and end) is not None:
            self.limit = end - offset
            self.offset = offset - 1 if offset > 0 else 0
        else:
            # 设置默认偏移量
            self.limit = 25
            self.offset = 0

    def query_data(self, limit=20, offset=0):
        sql = "SELECT DISTINCT h.hostid , t.triggerid , t.priority , t.`value` , " \
              "FROM_UNIXTIME(t.lastchange) date_time , e.acknowledged , h.`name` , t.description, e.eventid " \
              "FROM " \
              "HOSTS h , hosts_groups hg , groups g , interface net , items i , functions f , TRIGGERS t , EVENTS e " \
              "WHERE h.hostid = hg.hostid " \
              "AND h.hostid = net.hostid " \
              "AND hg.groupid = g.groupid " \
              "AND h.hostid = i.hostid " \
              "AND h.hostid = i.hostid " \
              "AND i.itemid = f.itemid " \
              "AND t.triggerid = f.triggerid " \
              "AND e.objectid = t.triggerid " \
              "AND e.clock = t.lastchange " \
              "AND e.source = 0 AND h.`status` != 3 %s %s %s %s %s %s %s " \
              "ORDER BY date_time DESC , t.priority DESC , " \
              "h.hostid , t.priority , t.`value` , e.acknowledged , h.`name` , t.description LIMIT %s OFFSET %s"

        query_set = self.exec_raw_sql(sql,
                                      (self.group_id,
                                       self.host_id,
                                       self.ip_address,
                                       self.issue_level,
                                       self.ack,
                                       self.start_time,
                                       self.end_time,
                                       limit,
                                       offset
                                       )
                                      )
        return query_set

    def filter_data(self, limit=20, offset=0):
        event_sql = "SELECT e.eventid , e.objectid , FROM_UNIXTIME(e.clock) , e.`value` , e.acknowledged " \
                    "FROM `events` e WHERE e.objectid = %s %s ORDER BY e.clock DESC"
        query_set = self.query_data(limit=limit, offset=offset)
        export_data = []
        for info in query_set:
            event_trigger = dict()
            event_trigger.update({'host_id': info[0]})
            event_trigger.update({'data_switcherid': info[1]})
            event_trigger.update({'priority': priority_type.get(info[2])})
            event_trigger.update({'priority_id': info[2]})
            event_trigger.update({'issue': issue_type.get(info[3])})
            event_trigger.update({'issue_id': info[3]})
            event_trigger.update({'date_time': str(info[4])})
            event_trigger.update({'ack': acknowledged_type.get(info[5])})
            event_trigger.update({'ack_id': info[5]})
            event_trigger.update({'host_name': info[6]})
            event_trigger.update({'info': re.sub('\{.*\}', info[6], info[7])})
            event_trigger.update({'event_id': str(info[8])})
            export_data.append(event_trigger)
            if self.trigger_end_time:
                events_history = self.exec_raw_sql(event_sql, (info[1], self.trigger_end_time))
                if events_history:
                    export_data[-1]['parent'] = True
                for history_trigger in events_history:
                    event_history = dict()
                    event_history.update({'event_id': str(history_trigger[0])})
                    event_history.update({'data_parentid': history_trigger[1]})
                    event_history.update({'date_time': str(history_trigger[2])})
                    event_history.update({'issue': issue_type.get(history_trigger[3])})
                    event_history.update({'issue_id': history_trigger[3]})
                    event_history.update({'ack': acknowledged_type.get(history_trigger[4])})
                    event_history.update({'ack_id': history_trigger[4]})
                    export_data.append(event_history)
        return export_data

    def object_list(self):
        return self

    @property
    def has_next(self):
        next_offset = self.offset + self.limit
        query_set = self.query_data(self.limit, next_offset)
        return bool(query_set)

    def get_hosts(self, group_id):
        """
        获取所有主机，可以指定组名id获取组下的所有主机
        :param group_id:
        :return:
        """
        group_id = "AND g.groupid = %s AND h.hostid = hg.hostid" % group_id if group_id and str(group_id) != "0" else ""
        hosts_sql = "SELECT DISTINCT h.hostid , h.`name` " \
                    "FROM HOSTS h , hosts_groups hg , groups g " \
                    "WHERE h.`status` IN(0 , 1) AND h.flags != 2 " \
                    "AND hg.groupid = g.groupid " \
                    "%s ORDER BY h.`name`"

        hosts = self.exec_raw_sql(hosts_sql, (group_id,))
        hosts_list = []
        for host in hosts:
            hosts_list.append({'host_id': host[0], 'host_name': host[1]})
        return hosts_list


class ConfigHostsGroup(object):

    def __init__(self, hosts_id=None, group_name=None, group_id=None, modify=None, delete=None, response=None):
        self.hosts_id = hosts_id if type(hosts_id) is list else []
        self.group_name = group_name
        self.modify = modify
        self.group_id = group_id
        self.delete = delete
        if type(response) is not dict:
            response = dict()
        self.response = response
        self.black_list = ['Templates', 'Linux servers', 'Zabbix servers', 'Discovered hosts', 'Virtual machines', 'Hypervisors']

    @staticmethod
    def get_table_field_id(table_name, field_name):
        """
        获取表中对应字段的下一个值
        :param table_name: 表名
        :param field_name: 表字段名
        :return: 该字段的下一个值，如果为空则返回1
        """
        last_id = models.Ids.objects.filter(table_name=table_name, field_name=field_name).values('nextid').all()
        last_id = last_id[0].get('nextid') + 1 if last_id else 1
        return last_id

    @staticmethod
    def update_table_field_id(table_name, field_name, nextid):
        """
        更新该表中记录的字段信息
        :param table_name: 表名
        :param field_name: 需要更新的字段名
        :param nextid: 更新该字段的值为当前该字段的值
        :return: bool
        """
        try:
            update_rows = models.Ids.objects.filter(table_name=table_name, field_name=field_name).update(nextid=nextid)
        except Exception as e:
            print('字段更新错误：%s' % e)
            return False
        return update_rows

    def create_group(self, group_name):
        """
        创建,更新，删除 主机组
        :param group_name: 组名
        :return: bool
        """
        table_name = models.Groups._meta.db_table
        field_name = "groupid"

        if not models.Groups.objects.filter(name=group_name) and not self.modify:
            group_id = self.get_table_field_id(table_name=table_name, field_name=field_name)
            models.MonitorGroups.objects.create(group_id=group_id, group_name=group_name)
            models.Groups.objects.create(groupid=group_id, name=group_name)
            update_rows = self.update_table_field_id(table_name, field_name, group_id)
            return group_id if update_rows is not False else False
        else:
            if self.modify:
                models.Groups.objects.filter(groupid=self.group_id).update(name=self.group_name)
                models.MonitorGroups.objects.filter(group_id=self.group_id).update(group_name=self.group_name)
                # 判断更新的行数，如果行数为1则更新成功
                return self.group_id
            if self.delete:
                models.MonitorGroups.objects.filter(group_id=self.group_id).delete()
                models.HostsGroups.objects.filter(groupid=self.group_id).delete()
                models.Groups.objects.filter(groupid=self.group_id).delete()
                return self.group_id
            self.response["info"] = "已存在重名的组"
            self.response["category"] = "error"
        return False

    def create_hosts_groups(self, group, host):
        """
        关联主机与组的关系
        :param group:group对象
        :param host:主机对象
        :return:
        """
        monitor_group = models.MonitorGroups.objects.filter(group_id=group.groupid).all()[0]
        models.MonitorHostGroups.objects.create(group=monitor_group, host_id=host.hostid)
        table_name = models.HostsGroups._meta.db_table
        field_name = "hostgroupid"
        host_group_id = self.get_table_field_id(table_name=table_name, field_name=field_name)
        models.HostsGroups.objects.create(hostgroupid=host_group_id, hostid=host, groupid=group)
        update_rows = self.update_table_field_id(table_name, field_name, host_group_id)

        return host_group_id if update_rows is not False else False

    def create_hosts_group_rel(self):
        """
        建立主机与组之间的关系,更新或创建主机与组之间的关系
        :return:
        """
        context = dict()
        old_host_members = []  # 存放原来已有的组成员，主要用于更新操作
        if self.group_name:
            if self.group_name in self.black_list:
                self.response['info'] = "操作不允许"
                self.response["category"] = "error"
                return self.response
            try:
                get_group_id = self.create_group(self.group_name)
                if get_group_id:
                    if self.delete:
                        context['group_id'] = self.group_id
                        context['del_group'] = True
                        self.response['data'] = context
                        self.response["info"] = "删除【%s】成功" % self.group_name
                        return self.response
                    group = models.Groups.objects.filter(groupid=get_group_id)[0]
                    context['group_id'] = group.groupid
                    context['group_name'] = group.name
                    context['hosts'] = []
                    if self.modify:
                        old_host_members = models.HostsGroups.objects.filter(groupid=get_group_id).values('hostid')
                        old_host_members = list(map(lambda host_member: str(host_member.get("hostid")), old_host_members))
                    add_hosts = list(set(self.hosts_id).difference(old_host_members))
                    del_hosts = list(set(old_host_members).difference(self.hosts_id))
                    for host_id in add_hosts:
                        host = models.Hosts.objects.filter(hostid=host_id)[0]
                        context['hosts'].append({'host_id': host.hostid, "host_name": host.name})
                        get_host_group_id = self.create_hosts_groups(group, host)
                        if get_host_group_id is False:
                            self.response["info"] = "请求未完成"
                            self.response["category"] = "error"
                            return self.response
                    self.response["info"] = "创建【%s】成功" % self.group_name
                    if self.modify:
                        models.MonitorHostGroups.objects.filter(group__group_id=get_group_id, host_id__in=del_hosts).delete()
                        models.HostsGroups.objects.filter(groupid=get_group_id, hostid__in=del_hosts).delete()
                        context["del_hosts"] = del_hosts
                        self.response["info"] = "修改【%s】成功" % self.group_name
                    self.response['data'] = context
                    return self.response
            except ValueError as e:
                self.response['info'] = "请求未完成"
                self.response["category"] = "error"
        else:
            self.response['info'] = "组名不能为空"
            self.response["category"] = "warning"
        return self.response


class HostGroupsStatus(object):
    def __init__(self):
        self.info = None

    def exec_raw_sql(self, raw_sql, param):
        """
        通过执行原生sql返回结果
        :param raw_sql: 原生sql语句
        :param param: sql参数
        :return:
        """
        try:
            raw_sql = raw_sql % param
            cursor = connection.cursor()
            cursor.execute(raw_sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            self.info = e
        return []

    @staticmethod
    def list_to_dict(data_list):
        """将列表形式的字典元素转换为字典"""
        temp_dict = dict()
        for info in data_list:
            temp_dict.update(info)
        return temp_dict

    def get_all_groups_status(self):
        """
        获取所有主机组下对应的主机状态关系分类字典数据
        :return:
        """
        groups_status_info = []
        handler = SearchEventTrigger()
        groups = handler.get_groups_menu()
        max_count = 0
        groups_id = str(list(map(lambda group: group.get('group_id'), groups))).strip('[,]')
        str_sql = "SELECT group_id, status,count(id) as host_count " \
                  "FROM (SELECT g.groupid group_id,h.hostid as id,h.name, MAX(t.value) AS status " \
                  "FROM hosts h, groups g, hosts_groups hg, items i, triggers t, functions f " \
                  "WHERE hg.groupid = g.groupid " \
                  "AND hg.hostid = h.hostid " \
                  "AND i.hostid = h.hostid " \
                  "AND f.itemid = i.itemid " \
                  "AND f.triggerid = t.triggerid " \
                  "AND g.groupid in(%s) " \
                  "GROUP BY g.groupid,h.name, h.hostid) temp " \
                  "GROUP BY group_id,status"
        groups_status = self.exec_raw_sql(str_sql, groups_id)
        for group_info in groups:
            group_info_order = OrderedDict()
            group_info_order['group_id'] = group_info.get('group_id')
            group_info_order['group_name'] = "'%s'" % group_info.get('group_name')
            group_info_order["host_normal_count"] = 0
            group_info_order["host_issue_count"] = 0
            setp = 0
            max_number = 0
            for status in groups_status:
                if status[0] == group_info.get('group_id'):

                    if setp % 2:
                        max_number += status[2]
                        max_count = max_number if max_number > max_count else max_count
                    else:
                        max_number = status[2]
                        setp += 1
                    if status[1] == 0:
                        group_info_order['host_normal_count'] = status[2]
                    elif status[1] == 1:
                        group_info_order['host_issue_count'] = status[2]
            groups_status_info.append(group_info_order)
        groups_status_info = list(zip(*list(map(lambda info: list(info.values()), groups_status_info))))
        groups_status_info_key = ['group_id', 'group_name', 'host_normal_count', 'host_issue_count']
        groups_status_info = list(map(lambda key, value: {key: list(value)}, groups_status_info_key, groups_status_info))
        temp_info = dict()
        for info in groups_status_info:
            temp_info.update(info)
        total_issue_count = sum(temp_info.get('host_issue_count', [0]))
        total_normal_count = sum(temp_info.get('host_normal_count', [0]))
        groups_status_info = temp_info
        groups_status_info.update({'max_count': max_count})
        groups_status_info.update({'total_issue_count': total_issue_count})
        groups_status_info.update({'total_normal_count': total_normal_count})
        return groups_status_info

    def get_event_triggers_status(self, limit=20, offset=0):
        """
        获取最新20条告警信息
        :param limit: 限制20条
        :param offset:
        :return:
        """
        event_status_info_key = ['host_id', 'host_name', 'issue_id', 'datetime', 'description', 'ack_id']
        triggers_sql = "SELECT h.hostid,h.name,t.priority,FROM_UNIXTIME(t.lastchange),t.description,e.acknowledged " \
                       "FROM hosts h,items i,functions f,triggers t,events e " \
                       "WHERE h.hostid = i.hostid " \
                       "AND f.itemid = i.itemid " \
                       "AND f.triggerid = t.triggerid " \
                       "AND e.objectid = t.triggerid " \
                       "AND t.value = 1 " \
                       "AND e.clock = t.lastchange " \
                       "ORDER BY t.priority DESC , t.lastchange DESC LIMIT %s OFFSET %s"
        triggers = self.exec_raw_sql(triggers_sql, (limit, offset))
        event_triggers_status = []
        for event in triggers:
            error_msg = re.sub('\{.*\}', event[1], event[4])
            event = list(event)
            event[4] = error_msg
            event[3] = str(event[3])
            event_info = list(map(lambda key, value: {key: value}, event_status_info_key, event))
            event_info.append({'priority': priority_type.get(event[2])})
            event_info.append({'ack': acknowledged_type.get(event[5])})
            event_triggers_status.append(self.list_to_dict(event_info))
        return event_triggers_status

    @staticmethod
    def unit_convert(num, src_unit, dst_unit='mb'):
        """
        单位转换
        :param num:
        :param src_unit: 原来单位
        :param dst_unit: 目标单位
        :return:
        """
        src_unit = str(src_unit).lower()
        dst_unit = str(dst_unit).lower()
        rate = {
            'b': 1,
            'kb': 1024,
            'mb': 1024*1024,
            'gb': 1024*1024*1024,
            'tb': 1024*1024*1024*1024,
            'pb': 1024*1024*1024*1024*1024
        }
        if src_unit in rate:
            num *= rate.get(src_unit)
            num /= rate.get(dst_unit)
        return round(num, 2)

    def top_data_sql(self, key="", units='', limit=10, order_by='desc', **kwargs):
        """
        top10的sql语句，
        :param key: 不同类型的top数据值
        :param units: 单位
        :param limit: 限制多少条数据
        :param order_by: 排序，默认倒序
        :param kwargs: 其他参数
        :return: 返回查询结果
        """
        sql = "SELECT h.hostid,h.name,FROM_UNIXTIME(hm.clock),hm.value,i.name,i.key_,i.units " \
              "FROM hosts h,items i,monitor_monitorhistory hm " \
              "WHERE h.hostid = i.hostid " \
              "AND i.itemid = hm.itemid " \
              "AND i.units = '%s' " \
              "AND i.key_ LIKE '%s' " \
              "AND h.status = 0 ORDER BY hm.value %s LIMIT %s"

        result = self.exec_raw_sql(sql, (units, key, order_by, limit))
        return result

    @staticmethod
    def format_item_name(item_name, item_key):
        """格式化item key 字段
        :param item_name:
        :param item_key:
        :return:
        """
        match_str = re.findall('\$\d', item_name)
        try:
            if match_str:
                for position in match_str:
                    index = str(position).lstrip('$')
                    key = re.search('\[.*\]', item_key)
                    key = str(key.group()).strip('[]').split(',') if key else []
                    item_name = re.sub('\$\d', key[int(index) - 1], item_name, count=match_str.index(position) + 1)
        except IndexError:
            pass
        return item_name

    def get_top_data(self):
        """
        获取top 10数据
        :return:
        """
        host_info_key = ['host_id', 'host_name', 'datetime', 'value', 'description', 'unit']
        # 固定字典数据返回顺序，下面的排放顺序影响页面加载的顺序
        search_key = [
            {
                'id': 'cpu',
                'name': 'CPU使用率',
                'type': "graph",
                'args': {'key': 'system.cpu.util%idle%', 'units': '%', 'limit': 10, 'order_by': 'asc', 'dst_unit': '%'}
            },
            {
                'id': 'mem',
                'name': '内存可用大小',
                'type': "graph",
                'args': {'key': 'vm.memory.size%available%', 'units': 'B', 'limit': 10, 'order_by': 'desc', 'dst_unit': 'MB'}
            },
            {
                'id': 'net_out',
                'name': '网卡出口流量',
                'type': "table",
                'args': {'key': 'net.if.out%', 'units': 'bps', 'limit': 10, 'order_by': 'desc', 'dst_unit': 'MB'}
            },
            {
                'id': 'net_in',
                'name': '网卡入口流量',
                'type': "table",
                'args': {'key': 'net.if.in%', 'units': 'bps', 'limit': 10, 'order_by': 'desc', 'dst_unit': 'MB'}
            },
            {
                'id': 'disk',
                'name': '磁盘可用大小',
                'type': "table",
                'args': {'key': 'vfs.fs.size%free%', 'units': 'B', 'limit': 10, 'order_by': 'desc', 'dst_unit': 'GB'}
            }
        ]
        all_item_data = []
        for item in search_key:
            item_name = item.get('name')
            item_value = item.get('args')
            item_id = item.get('id')
            item_type = item.get('type')
            item_unit = item_value.get('dst_unit')
            result = self.top_data_sql(**item_value)
            item_data = []
            for host in result:
                host = list(host)
                if item_type != "table":
                    host[1] = "'%s'" % host[1]
                host[2] = str(host[2])
                host[3] = self.unit_convert(host[3], host[6], item_value.get('dst_unit'))
                host[4] = self.format_item_name(host[4], host[5])
                host.pop(5)
                host_info = list(map(lambda key, value: {key: value}, host_info_key, host))
                host_info = self.list_to_dict(host_info)
                item_data.append(host_info)
            all_item_data.append({'name': item_name, 'value': item_data, 'id': item_id, 'type': item_type, 'unit': item_unit})
        return all_item_data

