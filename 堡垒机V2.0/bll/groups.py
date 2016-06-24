#!/usr/bin/env python3

from module.tables import Groups
from module import common

class BLL_Host_Group(object):

    def __init__(self, sqlhelper):
        self.mysql = sqlhelper
        self.groupname = ""


    def insert(self):
        """
        插入一条组记录
        :return:
        """

        try:
            # 链接数据库
            self.mysql.connect()

            group = Groups(self.groupname)
            self.mysql.session.add(group)
            self.mysql.session.commit()
            # close
            self.mysql.close()

        except Exception as e:
            common.write_log("[bll.groups.insert] {0}".format(e), "ERROR")

    def load_group_by_name(self):
        """
        通过组名返回一个组对象，用来获取组信息或检测组是否存在
        :return: 组对象
        """
        try:
            self.mysql.connect()
            group = self.mysql.session.query(Groups).filter(Groups.groupname==self.groupname).first()
            self.mysql.close()
            return group
        except Exception as e:
            common.write_log("[bll.groups.load_group_by_name] {0}".format(e), "ERROR")

    def load_group_all(self):
        try:
            self.mysql.connect()
            grouplist = self.mysql.session.query(Groups).all()
            self.mysql.close()
            return grouplist
        except Exception as e:
            common.write_log("[bll.groups.load_group_all {0}".format(e))