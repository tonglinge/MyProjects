#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun
@date 2016/10/19
"""
import re
from django.db import connection
from afcat.monitor.libs.monitor_hosts import acknowledged_type, issue_type, priority_type, available_type


class ExportFile(object):
    def __init__(self,
                 page=0,
                 group_id=None,
                 host_id=None,
                 host_status=None,
                 ip_address=None,
                 issue_level=None,
                 issue_status=None,
                 ack=None,
                 start_time=None,
                 end_time=None):
        self.page = page
        self.limit, self.offset = 25, 0  # 限制每页取多少数据，默认每次取25条数据，从第一条开始
        self.info = None
        self.group_id = "AND g.groupid='%s'" % group_id if group_id and group_id != "0" else ""
        self.host_id = "AND h.hostid='%s'" % host_id if host_id and host_id != "0" else ""
        self.host_status = "AND h.available='%s'" % host_status if host_status else ""
        self.ip_address = "AND net.ip LIKE '%{}%'".format(ip_address) if ip_address else ""
        self.issue_level = "AND t.priority='%s'" % issue_level if issue_level else ""
        self.issue_status = "AND t.value='%s'" % issue_status if issue_status else ""
        self.ack = "AND e.acknowledged='%s'" % ack if ack else ""
        self.start_time = "AND t.lastchange>=UNIX_TIMESTAMP('%s')" % start_time if start_time else ""
        self.end_time = "AND t.lastchange<=UNIX_TIMESTAMP('%s')" % end_time if end_time else ""

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
            # print(raw_sql)
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
        sql = "SELECT g.name groupname,h.name hostname,h.available,net.ip,t.priority,t.description,t.value status," \
              "FROM_UNIXTIME(t.lastchange) time,e.acknowledged,h.hostid " \
              "FROM hosts h,interface net,groups g,hosts_groups hg,items i,functions f,triggers t,events e " \
              "WHERE h.hostid = hg.hostid " \
              "AND h.hostid = net.hostid " \
              "AND h.status != 3 " \
              "AND h.hostid = i.hostid " \
              "AND hg.groupid = g.groupid " \
              "AND f.itemid = i.itemid " \
              "AND t.triggerid = f.triggerid " \
              "AND e.objectid = t.triggerid " \
              "AND e.clock = t.lastchange " \
              "%s %s %s %s %s %s %s %s %s" \
              "ORDER BY t.lastchange DESC , t.priority DESC LIMIT %s OFFSET %s"
        query_set = self.exec_raw_sql(sql,
                                   (self.group_id,
                                    self.host_id,
                                    self.host_status,
                                    self.ip_address,
                                    self.issue_level,
                                    self.issue_status,
                                    self.ack,
                                    self.start_time,
                                    self.end_time,
                                    limit,
                                    offset
                                    ))
        return query_set

    def filter_data(self, limit=20, offset=0):
        query_set = self.query_data(limit=limit, offset=offset)
        export_data = []
        for info in query_set:
            event_trigger = dict()
            event_trigger.update({'group_name': info[0]})
            event_trigger.update({'host_name': info[1]})
            event_trigger.update({'available': available_type.get(info[2])})
            event_trigger.update({'available_id': info[2]})
            event_trigger.update({'ip': info[3]})
            event_trigger.update({'priority': priority_type.get(info[4])})
            event_trigger.update({'priority_id': info[4]})
            event_trigger.update({'info': re.sub('\{.*\}', info[1], info[5])})
            event_trigger.update({'issue': issue_type.get(info[6])})
            event_trigger.update({'issue_id': info[6]})
            event_trigger.update({'date_time': str(info[7])})
            event_trigger.update({'ack': acknowledged_type.get(info[8])})
            event_trigger.update({'ack_id': info[8]})
            event_trigger.update({'host_id': info[9]})
            export_data.append(event_trigger)
        return export_data

    def object_list(self):
        return self

    @property
    def has_next(self):
        next_offset = self.offset + self.limit
        query_set = self.query_data(self.limit, next_offset)
        return bool(query_set)

