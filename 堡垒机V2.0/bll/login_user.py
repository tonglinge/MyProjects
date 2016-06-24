#!/usr/bin/env python
from datetime import datetime
from module.tables import Login_User, SSH_User
from module import common
from bll.op_log import BLL_Op_Logs


class BLL_Login_User(object):
    def __init__(self, sqlhelper):
        self.mysql = sqlhelper
        self.id = 0
        self.username = ""
        self.password = ""
        self.name = ""
        self.role = "user"
        self.last_login_date = datetime.now()
        self.expired = None
        self.exists = False

    def login(self):
        try:
            # 建立连接
            self.mysql.connect()
            search_result = self.mysql.session.query(Login_User).filter(Login_User.username == self.username). \
                filter(Login_User.password == self.password). \
                filter(Login_User.expired > datetime.now()). \
                filter(Login_User.isdel == False).first()
            # 执行完关闭连接
            self.mysql.close()
            # 登录失败
            if not search_result:
                self.exists = False
            else:
                # 登录成功
                self.id = search_result.id
                self.exists = True
                self.name = search_result.name
                self.role = search_result.role
                self.username = search_result.username
                self.expired = search_result.expired
                # print(search_result)
            # 写操作日志记录
            self.__write_login_log()

        except Exception as e:
            common.write_log("[bll.login_user.login] {0}".format(e), "ERROR")

    def __write_login_log(self):
        try:
            if not self.exists:
                op_msg = ("用户{user}登录系统失败!".format(user=self.username),)
            else:
                op_msg = ("用户{user}登录系统成功!".format(user=self.username),)

            op_type = "login"
            op_log = BLL_Op_Logs(self, self.mysql)
            # 获取当前上次登录的时间
            op_date = op_log.last_login_date()
            if op_date:
                self.last_login_date = op_date

            # 写日志
            op_log.save_log(op_msg, op_type)

            # 执行完在内存中删除此对象
            del op_log
        except Exception as e:
            common.write_log("[bll.login_user.__write_log_log] {0}".format(e), "ERROR")

    def insert(self, grouplist):
        """
        信添加一个登录账户
        :return:
        """
        try:
            self.mysql.connect()
            new_user = Login_User(self.username,
                                  self.name,
                                  self.role,
                                  0,
                                  self.expired,
                                  self.password)
            new_user.groups = grouplist
            self.mysql.session.add(new_user)
            self.mysql.session.commit()
            self.mysql.close()
            return new_user
        except Exception as e:
            common.write_log("[bll.login_user.insert] {0}".format(e), "error")

    @property
    def user_exists(self):
        """
        检测用户是否已经存在
        :return:
        """
        try:
            self.mysql.connect()
            user = self.mysql.session.query(Login_User).filter(Login_User.username == self.username).first()
            if not user:
                self.exists = False
            else:
                self.exists = True
            self.mysql.close()
            return self.exists
        except Exception as e:
            common.write_log("[bll.login_user.user_exists] {0}".format(e), "error")

    def insert_ssh_user(self, id_list):
        """
        给添加的登录用户分配ssh登录用户
        :param id_list:
        :return:
        """
        try:
            self.mysql.connect()
            ssh_user_obj_list = self.mysql.session.query(SSH_User).filter(SSH_User.id.in_(id_list)).all()
            login_user_obj = self.mysql.session.query(Login_User).filter(Login_User.username == self.username).first()
            login_user_obj.sshusers = ssh_user_obj_list
            self.mysql.session.commit()
            self.mysql.close()
        except Exception as e:
            common.write_log("[bll.login_user.insert_ssh_user] {0}".format(e), "error")

    def load_hosts_by_uid(self):
        """
        获取登录用户管理的所有主机列表
        :return:
        """
        try:
            host_list = []
            self.mysql.connect()
            # 获取登录用户所属组列表
            userobj = self.mysql.session.query(Login_User).filter(Login_User.username == self.username).first()
            groups = userobj.groups
            # 获取所有组下的主机信息
            for group in groups:
                hosts = group.hostlist
                # 遍历主机下的所有用户
                for host in hosts:
                    host_info = dict(hostid=host.id,
                                     hostname=host.hostname,
                                     ipaddr= host.ipaddr,
                                     port=host.sshport,
                                     groupname=group.groupname)
                    host_list.append(host_info)

            self.mysql.close()
            return host_list
        except Exception as e:
            common.write_log("[bll.login_user.load_hosts_by_uid] {0}".format(e), "error")

    def load_sshusers(self, hid):
        """
        获取当前登录用户选择的主机对象下的ssh用户信息
        :param hid:
        :return:
        """
        try:
            ssh_user_list = []
            self.mysql.connect()
            # 获取主机对应的所有SSH用户e.g:ssh_user1, ssh_user2
            sshuser_all_host = self.mysql.session.query(SSH_User).filter(SSH_User.hid == hid).all()
            # 获取当前用户可以使用的所有SSH用户 e.g:ssh_user1, ssh_user3
            curr_userobj = self.mysql.session.query(Login_User).filter(Login_User.username == self.username).first()
            sshuser_all_user = curr_userobj.sshusers
            # 获取当前选择的主机中用户可以使用的用户， 过滤后得到e.g :ssh_user1
            tmplist = []
            for obj in sshuser_all_user:
                if obj in sshuser_all_host:
                    tmplist.append(obj)
            # 返回一个选择的用户对象字典列表
            for _tmpuser in tmplist:
                sshuser = dict(username=_tmpuser.auth_user,
                               auth_type=_tmpuser.auth_type,
                               passwd=_tmpuser.auth_key)
                ssh_user_list.append(sshuser)
            self.mysql.close()
            return ssh_user_list
        except Exception as e:
            common.write_log("[bll.login_user.load_sshsers] {0}".format(e), "error")


