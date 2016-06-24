#!/usr/bin/env python3
"""
主机逻辑层,用来实现对主机表操作
"""

from module.tables import Hosts, Groups
from module.common import write_log


class BLL_Hosts(object):

    def __init__(self, sqlhelper):
        self.mysql = sqlhelper
        self.hostname = ""
        self.ipaddr = ""
        self.sshport = ""

    def insert(self,groupsobj_list):
        """
        添加主机信息表，并同时添加关联表
        :param groups: 用户选择的主机所属主机组对象列表
        :return:
        """
        try:
            self.mysql.connect()
            host = Hosts(self.hostname,
                         self.ipaddr,
                         self.sshport)
            host.groups = groupsobj_list

            self.mysql.session.add(host)
            self.mysql.session.commit()
            # 关闭连接
            self.mysql.close()
        except Exception as e:
            write_log("[bll.hosts.insert] {0}".format(e), "error")

    def load_hosts_by_group(self, groupobj):
        """
        通过选择的主机组获取该组下所有的主机信息
        :param groupobj: 主机组对象
        :return:
        """
        try:
            self.mysql.connect()
            group = self.mysql.session.query(Groups).filter(Groups.id==groupobj.id).first()
            print(group)
            host_list = group.hostlist
            print(host_list)
            self.mysql.close()
            return host_list
        except Exception as e:
            write_log("[bll.hosts.load_hosts_by_group] {0}".format(e), "error")
