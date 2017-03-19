#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun 
@date 16/9/7
"""
import time
import re


class TimeConvert:
    @staticmethod
    def unix_time_conv(arg):
        """
        unit_time时间转换成标准时间
        :return:
        """
        time_format = '%Y-%m-%d %H:%M:%S'
        time_obj = time.localtime(arg)
        time_std = time.strftime(time_format, time_obj)
        return time_std

    @staticmethod
    def std_time_conv(arg):
        """
        标准时间转换成unix_time
        :param arg:
        :return:
        """
        time_format = '%Y-%m-%d %H:%M:%S'
        time_obj = time.strptime(arg, time_format)
        time_unix = time.mktime(time_obj)
        return time_unix
print(TimeConvert.unix_time_conv(1473271761))
print(TimeConvert.unix_time_conv(585434788))


class HostInfo(object):
    """
    通过hostid获取主机相关状态
    """

    def __init__(self, host_id):
        self.host_id = host_id

    def get_host_name(self):
        """
        通过host_id获取主机名
        :return:
        """
        host = models.Hosts.objects.get(hostid=self.host_id)
        host_name = host.name
        return host_name

    def get_host_gid(self):
        """
        通过host_id获取主机组id，如果主机从属多个组，则只获取一个所属组id
        :return:
        """
        host_grp = models.HostsGroups.objects.filter(hostid=self.host_id).order_by("groupid").all()
        list_host_grp = []
        for item in host_grp:
            list_host_grp.append(item.groupid_id)
        return list_host_grp

    def get_host_gname(self):
        """
        通过host_gid获取主机组名，由于get_host_gid()方法只获取一个组id
        所以获取的组名也只有一个
        :return:
        """
        host_gid = self.get_host_gid()
        host_gname = models.Groups.objects.filter(groupid__in=host_gid).order_by("name").all()
        list_host_gname = []
        for item in host_gname:
            list_host_gname.append(item.name)
        return list_host_gname

    def get_host_ip(self):
        """
        通过host_id获取主机ip地址
        :return:
        """
        host_ip = models.Interface.objects.get(hostid=self.host_id)
        host_ip = host_ip.ip
        return host_ip

    def get_host_item_id(self):
        """
        通过host_id获取主机所有的监控项目items_id
        :return:
        """
        hst_itm = models.Items.objects.filter(hostid=self.host_id).all()
        list_items_id = []
        for item in hst_itm:
            list_items_id.append(item.itemid)
        host_items_id = list_items_id
        return host_items_id

    def get_host_trigger_id(self):
        """
        通过items_id获取主机所有监控项目已经被定义的triggers_id
        :return:
        """
        host_items_id = self.get_host_item_id()
        hst_tid = models.Functions.objects.filter(itemid__in=host_items_id).all()
        list_trigger_id = []
        for item in hst_tid:
            list_trigger_id.append(item.triggerid_id)
        return list_trigger_id

    def get_host_total_cnt(self):
        """
        通过triggers_id获取主机所有已被触发的triggers的总数
        :return:
        """
        host_triggers_id = self.get_host_trigger_id()
        host_total_cnt = models.Triggers.objects.filter(triggerid__in=host_triggers_id, status=0, value=1).count()
        return host_total_cnt

    def get_host_status(self):
        """
        通过主机被触发的triggers的总数来判断主机是否正常
        :return:
        """
        host_total_cnt = self.get_host_total_cnt()
        if host_total_cnt:
            host_status = '故障'
        else:
            host_status = '正常'
        return host_status

    def get_host_triggers_lastcheck(self):
        """
        获取主机所有已被触发triggers的最新时间，告警级别，告警详细
        :return:
        """
        host_name = self.get_host_name()
        host_triggers_id = self.get_host_trigger_id()
        hst_lastcheck = models.Triggers.objects.filter(triggerid__in=host_triggers_id, status=0, value=1).all()
        list_triggers_lastcheck = []
        dict_level = {1: "灾难", 2: "严重", 3: "一般严重", 4: "警告", 5: "信息"}
        for item in hst_lastcheck:
            if not dict_level.get(item.priority):
                lastcheck_level = "未分类"
            else:
                lastcheck_level = dict_level.get(item.priority)
            description = re.sub(r'\{HOST\.NAME\}', host_name, item.description)
            lastcheck_time = TimeConvert.unix_time_conv(item.lastchange)
            list_triggers_lastcheck.append([description, lastcheck_level, lastcheck_time])
        return list_triggers_lastcheck

    def get_host_ack(self):
        """
        获取主机所有被触发监控的信息是否已被确认，及确认的详细信息
        :return:
        """
        list_trigger_id = self.get_host_trigger_id()
        if list_trigger_id:
            ack_event = models.Events.objects.filter(objectid__in=list_trigger_id, source=0)\
                .order_by("-clock").all()
        list_ack_event = []
        if ack_event:
            for item in ack_event:
                change_time = TimeConvert.unix_time_conv(item.clock)
                ack_status = item.acknowledged
                if item.acknowledged:
                    ack_obj = models.Acknowledges.objects.get(eventid=item.eventid)
                    ack_time = TimeConvert.unix_time_conv(ack_obj.clock)
                    ack_msg = ack_obj.message
                else:
                    ack_time = ''
                    ack_msg = ''
                list_ack_event.append([item.eventid, change_time, ack_status, ack_time, ack_msg])
        return list_ack_event



class SearchHost(object):
    def __init__(self, arg):
        self.host_name = arg.get('host-name', None)
        self.host_ip = arg.get('ip', None)
        self.host_status = arg.get('status', None)
        self.last_change = arg.get('issue-time', None)
        self.warn_level = arg.get('issue-level', None)

    @staticmethod
    def all_host():
        set_all_hosts = set()
        type_host = [1, 2]
        all_hosts_obj = models.Hosts.objects.filter(available__in=type_host).all()
        for item in all_hosts_obj:
            set_all_hosts.add(item.hostid)
        return set_all_hosts

    def search_by_hostname(self):
        """
        通过主机名查询，返回符合条件的hostid列表
        :return:
        """
        li_search_hostname = []
        if self.host_name is not None:
            filter_hostname = models.Hosts.objects.filter(available__in=[1, 2], host__contains=self.host_name).all()
            for item in filter_hostname:
                li_search_hostname.append(item.hostid)
        else:
            filter_hostname = models.Hosts.objects.all()
            for item in filter_hostname:
                li_search_hostname.append(item.hostid)
        return set(li_search_hostname)

    def search_by_ipaddr(self):
        """
        通过主机IP地址查询，返回符合条件的hostid列表
        :return:
        """
        search_ip = []
        if self.host_ip is not None:
            filter_ip = models.Interface.objects.filter(ip__contains=self.host_ip).all()
            for item in filter_ip:
                search_ip.append(item.hostid_id)
        else:
            filter_ip = models.Interface.objects.all()
            for item in filter_ip:
                search_ip.append(item.hostid_id)
        return set(search_ip)

    def search_by_host_status(self):
        """
        通过主机状态查询，返回符合条件的主机列表
        :return:
        """
        normal_host = []
        abnormal_host = []
        all_hosts = SearchHost.all_host()
        if all_hosts:
            for host_id in all_hosts:
                host_obj = HostInfo(host_id)
                if host_obj.get_host_total_cnt():
                    abnormal_host.append(host_id)
                else:
                    normal_host.append(host_id)
        else:
            return None
        if self.host_status == '0':
            return set(normal_host)
        elif self.host_status == '1':
            return set(abnormal_host)
        else:
            return all_hosts
        # active_triggers = []
        # active_items = []
        # res_hosts = set()
        #
        # def filter_host_status(arg):
        #     """
        #     查询主机状态正常的主机
        #     :return:
        #     """
        #     filter_status_triggers = models.Triggers.objects.filter(value=arg).all()
        #     for item_triggers in filter_status_triggers:
        #         active_triggers.append(item_triggers.triggerid)
        #     if active_triggers:
        #         filter_status_items = models.Functions.objects.filter(
        #             triggerid__in=active_triggers).all()
        #         for item_items in filter_status_items:
        #             active_items.append(item_items.itemid_id)
        #         filter_hosts = models.Items.objects.filter(itemid__in=active_items).all()
        #         for item_hosts in filter_hosts:
        #             print(item_hosts.hostid)
        #             query_hosts = res_hosts.add(item_hosts.hostid_id)
        #             print(query_hosts)
        #         valid_hosts = query_hosts.intersection_update(SearchHost.all_host())
        #         return valid_hosts
        # if self.host_status == '1':
        #     # 返回故障主机集合
        #     if filter_host_status(1):
        #         set_hosts = filter_host_status(1)
        # else:
        #     if self.host_status == '0':
        #         # 返回正常主机集合
        #         if filter_host_status(0):
        #             set_hosts = filter_host_status(0)
        #     else:
        #         # 返回所有主机集合
        #         set_hosts = SearchHost.all_host()
        # return set_hosts

    def search_by_last_change(self):
        """
        通过主机故障发生时间查询，返回符合条件的hostid列表
        :return:
        """
        if self.last_change:
            li_trigger = []
            li_items = []
            set_hosts = set()
            self.last_change = TimeConvert.std_time_conv(self.last_change)
            filter_lastchange_triggers = models.Triggers.objects.filter(
                lastchange__gte=self.last_change).all()
            print(len(filter_lastchange_triggers))
            if filter_lastchange_triggers:
                for item in filter_lastchange_triggers:
                    li_trigger.append(item.triggerid)
                filter_lastchange_items = models.Functions.objects.filter(
                    triggerid__in=li_trigger
                ).all()
                for item in filter_lastchange_items:
                    li_items.append(item.itemid_id)
                filter_lastchange_host = models.Items.objects.filter(
                    itemid__in=li_items
                ).all()
                for item in filter_lastchange_host:
                    set_hosts.add(item.hostid_id)
                return set_hosts
        else:
            return None

    def search_by_status_priority(self):
        """
        通过主机状态级别
        :return:
        """
        host_triggers = []
        host_items = []
        set_hosts = set()
        if self.host_status:
            if self.warn_level:
                filter_status_triggers = models.Triggers.objects.filter(value=1)\
                    .filter(priority=self.warn_level).all()
                for item in filter_status_triggers:
                    host_triggers.append(item.triggerid)
                filter_status_items = models.Functions.objects.filter(triggerid__in=host_triggers).all()
                for item in filter_status_items:
                    host_items.append(item.itemid_id)
                filter_status_hosts = models.Items.objects.filter(itemid__in=host_items).all()
                for item in filter_status_hosts:
                    set_hosts.add(item.hostid_id)
                if set_hosts:
                    return set_hosts
                else:
                    return None
            else:
                return self.search_by_host_status
        else:
            return None


class HostGraph(object):
    def __init__(self, arg):
        self.user_id = arg.get('user_id', None)
        self.host_id = arg.get('host_id', None)
        self.display_type = arg.get('display_type', None)
        self.start_time = arg.get('start_time', None)
        self.end_time = arg.get('end_time', None)

    def query_graphs_show(self, graph_id):
        """
        根据主机graph_id查询是否显示，0不显示， 1显示
        :param graph_id:
        :return:
        """
        graph_show_obj = models.HostsGraphs.objects.get(host_id=self.host_id, graph_type=self.display_type,
                                                        graph_id=graph_id)
        return graph_show_obj.graph_show

    def host_graphs_info(self):
        """
        根据hostid查询主机所有可选的图形信息
        :return:
        """
        host_items = set()
        graphs_items = set()
        graph_list = {}
        host_obj = models.Items.objects.filter(hostid=self.host_id).all()
        if host_obj:
            for item in host_obj:
                host_items.add(item.itemid)
            graphs_items_obj = models.GraphsItems.objects.filter(itemid__in=list(host_items)).all()
            if graphs_items_obj:
                for item in graphs_items_obj:
                    graphs_items.add(item.graphid_id)
                graphs_obj = models.Graphs.objects.filter(graphid__in=list(graphs_items)).all()
                for item in graphs_obj:
                    graph_list['graph_id'] = item.graphid
                    graph_list['graph_name'] = item.name
                    graph_list['graph_show'] = 0
                # for item in graphs_items_obj:
                #     graphs_items.add(item.itemid_id)
                # host_items.intersection_update(graphs_items)
                # item_id = list(host_items)
                # graphs_obj = models.GraphsItems.objects.filter(itemid__in=item_id).all()
                # for item in graphs_obj:
                #     graph_info[item.i] = item.
            else:
                return None
        else:
            return None
        # if graph_id:
        #     graphs_info = {}
        #     ret_graphs_items = []
        #     ret_graphs_obj = models.GraphsItems.objects.filter(graphid__in=graph_id).all()
        #     for graphs_items in ret_graphs_obj:
        #         graphs_name_obj = models.Graphs.objects.filter(graphid=graphs_items.graphid).all()
        #         for items_name in graphs_name_obj:
        #             graphs_info['graphsid'] = graphs_items.graphid_id
        #             graphs_info['graphs_name'] = items_name.name
        #             graphs_info['hostid'] = self.host_id
        #             ret_graphs_items.append(graphs_info)
        #     return ret_graphs_items
        # else:
        #     return None

    def graph_data_src(self):
        """
        根据用户选择的item和起始时间确定数据来源和数据范围
        :return:
        """
        start_unix_time = None
        end_unix_time = None
        data_src = None
        if self.start_time is None and self.end_time is None:
            start_unix_time = time.time() - 3600
            end_unix_time = time.time()
            data_src = 'History'
        elif self.start_time is None and self.end_time is not None:
            point_time = time.time() - 86400
            if self.start_time < point_time:
                start_unix_time = -28799
                data_src = 'Trends'
            else:
                start_unix_time = time.time() - 86400
                data_src = 'History'
            end_unix_time = self.end_time
        elif self.start_time is not None and self.end_time is not None:
            time_width = self.end_time - self.start_time
            if time_width > 86400:
                data_src = 'Trends'
            else:
                data_src = 'History'
            start_unix_time = self.start_time
            end_unix_time = self.end_time
        data_src_info = [start_unix_time, end_unix_time, data_src]
        return data_src_info

    @staticmethod
    def graph_data_type(data_item, data_src, data_type):
        """
        通过item，数据来源，数据类型，确定发送数据的内容
        :param data_item:
        :param data_src:
        :param data_type:
        :return:
        """
        value_obj = None
        graphs_data = []
        if data_src == 'Trends':
            if data_type == '0':
                value_obj = models.Trends.objects.filter(itemid=data_item.itemid).\
                    order_by("clock").all()
            elif data_type == '3':
                value_obj = models.TrendsUint.objects.filter(itemid=data_item.itemid).\
                    order_by("clock").all()
            for data_item in value_obj:
                graphs_data.append([data_item.value_min,
                                    data_item.value_avg,
                                    data_item.value_max]
                                   )
        elif data_src == 'History':
            if data_type == '0':
                value_obj = models.History.objects.filter(itemid=data_item.itemid).\
                    order_by("clock").all()
                for data_item in value_obj:
                    graphs_data.append([data_item.value_min,
                                        data_item.value_avg,
                                        data_item.value_max]
                                       )
            elif data_type == '1':
                value_obj = models.HistoryStr.objects.filter(itemid=data_item.itemid).\
                    order_by("clock").all()
                for data_item in value_obj:
                    graphs_data.append(data_item.value)
            elif data_type == '2':
                value_obj = models.HistoryLog.objects.filter(itemid=data_item.itemid).\
                    order_by("clock").all()
                for data_item in value_obj:
                    graphs_data.append(data_item.value)
            elif data_type == '3':
                value_obj = models.HistoryUint.objects.filter(itemid=data_item.itemid).\
                    order_by("clock").all()
                for data_item in value_obj:
                    graphs_data.append([data_item.value_min,
                                        data_item.value_avg,
                                        data_item.value_max]
                                       )
            elif data_type == '4':
                value_obj = models.HistoryText.objects.filter(itemid=data_item.itemid).\
                    order_by("clock").all()
                for data_item in value_obj:
                    graphs_data.append(data_item.value)
        return graphs_data

    def graph_info(self):
        """
        根据hostid查询主机的有关数据信息
        :return:
        """
        host_graph_items = []
        host_graph_id = []
        host_graph_obj = models.UsersGraphs.objects.filter(userid=self.user_id).\
            filter(hostid=self.host_id).filter(graphtype=self.display_type).all()
        if host_graph_obj:
            for host_item in host_graph_obj:
                host_graph_items.append(host_item.itemid)
                graph_type_obj = models.Items.objects.get(itemid=host_item.itemid)
                graph_id_obj = models.GraphsItems.objects.get(itemid=host_item.itemid)
                host_graph_id.append(graph_id_obj.graphid)


                graph_type = graph_type_obj.value_type
        else:
            return None


def get_host_groups(request):
    print(request.GET)
    ret = response_format()
    request_list = ['host-name', 'ip', 'status', 'issue-time', 'issue-level']
    request_search = {}
    var = request.GET.get('data')
    if var:
        var = json.loads(var)
    else:
        ret['data'] = None
        return HttpResponse(json.dumps(ret))
    for item in request_list:
        if var.get(item):
            request_search[item] = var.get(item)
    print('3.', request_search)
    obj = SearchHost(request_search)
    request_method = list(request_search.keys())
    res_hosts_id = []
    if len(request_method):
        for item in request_method:
            if item == 'host-name':
                search_hostname = getattr(obj, 'search_by_hostname')
                run_res = search_hostname()
                if run_res:
                    res_hosts_id.append(str(run_res))
                else:
                    ret['data'] = None
                    return HttpResponse(json.dumps(ret))
            elif item == 'ip':
                search_ip = getattr(obj, 'search_by_ipaddr')
                run_res = search_ip()
                if run_res:
                    res_hosts_id.append(str(run_res))
                else:
                    ret['data'] = None
                    return HttpResponse(json.dumps(ret))
            elif item == 'status':
                search_status = getattr(obj, 'search_by_host_status')
                run_res = search_status()
                if run_res:
                    res_hosts_id.append(str(run_res))
                else:
                    ret['data'] = None
                    return HttpResponse(json.dumps(ret))
            elif item == 'issue-time':
                search_last_change = getattr(obj, 'search_by_last_change')
                run_res = search_last_change()
                if run_res:
                    res_hosts_id.append(str(run_res))
                else:
                    ret['data'] = None
                    return HttpResponse(json.dumps(ret))
            elif item == 'issue-level':
                search_priority = getattr(obj, 'search_by_status_priority')
                run_res = search_priority()
                if run_res:
                    res_hosts_id.append(str(run_res))
                else:
                    ret['data'] = None
                    return HttpResponse(json.dumps(ret))
        result_request = list(set(res_hosts_id))
        len_res = len(result_request)
        if len_res  == 1:
            handle_res = eval(result_request[0])
        else:
            print('4.', result_request[0])
            handle_res_first = eval(result_request[0])
            result_request.pop(0)
            for item in result_request:
                handle_item = eval(item)
                handle_res_first.intersection_update(handle_item)
            handle_res = handle_res_first
    else:
        search_status = getattr(obj, 'all_host')
        if search_status():
            handle_res = list(search_status())
        else:
            ret['data'] = None
            return HttpResponse(json.dumps(ret))
    result_view = []
    for hostid in handle_res:
        host_obj = HostInfo(hostid)
        result_host_name = host_obj.get_host_name()
        result_host_ip = host_obj.get_host_ip()
        result_host_gname = host_obj.get_host_gname()
        result_host_status = host_obj.get_host_status()
        try:
            result_host_last_check = host_obj.get_host_triggers_lastcheck()[0][2]
        except Exception:
            result_host_last_check = None
        try:
            result_host_msg = host_obj.get_host_triggers_lastcheck()[0][0]
        except Exception:
            result_host_msg = None
        for host_grp in result_host_gname:
            tmp = {}
            tmp['hostid'] = hostid
            tmp['group'] = host_grp
            tmp['ip_address'] = result_host_ip
            tmp['hostname'] = result_host_name
            tmp['status'] = result_host_status
            tmp['date'] = result_host_last_check
            tmp['detail'] = result_host_msg
            result_view.append(tmp)
    print(result_view)
    ret['data'] = result_view
    print('ret', ret)

    return HttpResponse(json.dumps(ret))
