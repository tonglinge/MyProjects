#!/usr/bin/env python
"""
用户模块类，提供用户登录
"""
import os
from conf import settings
from modules import common
from dbhelper import dbapi
from modules.myexception import MyException

class Users(object):

    __userdb = settings.DB_USERS

    def __init__(self, uname):
        self.username = uname
        self.name = ""
        self.passwd = ""
        self.role = "user"
        self.inputcmd = ""
        self.groups = ""
        self.exists = True
        self.manage_ip = []

        self.__load_user_info()

    def __load_user_info(self):
        """
        从users.xml文件获取用户信息，如果不存在则exists标识为False，否则load所用信息
        :return:
        """
        user = dbapi.load_users(self.username)
        if not user:
            self.exists = False
        else:
            # 获取用户信息数据
            self.name = user["name"]
            self.passwd = user["password"]
            self.role = user["role"]
            self.groups = user["groups"]
            self.exists = True
            self.__load_manage_ip()

    def __load_manage_ip(self):
        """
        根据用户管理的组ID号，获取所有可以管理的主机IP列表，去重后返回唯一IP
        :return:
        """
        ip_list = []
        for gid in self.groups.split(","):
            hosts_in_gid = dbapi.load_host_by_gid(gid)
            for host in hosts_in_gid:
                ip_list.append(host["ip"])
        # 通过set转换一下，去重
        self.manage_ip = list(set(ip_list))

    def user_auth(self, password):
        """
        登录验证
        :param password: 用户输入密码
        :return:
        """
        try:
            if not self.exists:
                auth_status = False
            else:
                encry_passwd = common.encry_sha(password)
                if self.passwd == encry_passwd:
                    auth_status = True
                else:
                    auth_status = False
            return auth_status

        except Exception as e:
            common.write_log(e, "error")

    @staticmethod
    def auth_ip(func):
        def inner(userobj, input_command_list):
            try:
                # 用户输入即无 -h ，也无 -g 语法错误
                if input_command_list.count("-h") == 0 and input_command_list.count("-g") == 0:
                    raise MyException("103")

                # 用户输入 -h e.g: cmd -h 192.168.1.1,192.168.1.2,存在未授权IP
                if input_command_list.count("-h") > 0:
                    input_ip_list = input_command_list[input_command_list.index("-h") + 1].split(",")
                    for ip in input_ip_list:
                        if ip not in userobj.manage_ip:
                            raise MyException("104")

                # 用户输入 -g e.g: cmd -g gid 存在未授权 组，
                if input_command_list.count("-g") > 0:
                    # 获取组信息
                    input_gid_list = input_command_list[input_command_list.index("-g") + 1].split(",")
                    for gid in input_gid_list:
                        # 如果gid不在用户管理的gid内，报异常
                        if gid not in userobj.groups:
                            raise MyException("104")

                return func(userobj, input_command_list)

            except MyException as e:
                common.write_log(e, "warning")
            except Exception as e:
                common.write_log(e, "error")
        return inner

    def load_host_by_ip(self, ip):
        for gid in self.groups.split(","):
            host_info_list = dbapi.load_host_by_gid(gid)
            for host in host_info_list:
                if host["ip"] == ip:
                    return host

