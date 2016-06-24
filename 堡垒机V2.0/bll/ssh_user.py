
from module.tables import SSH_User
from module.tables import Hosts
from module.common import write_log


class BLL_SSH_User(object):

    def __init__(self, sqlhelper, hostobj):
        self.mysql = sqlhelper
        self.auth_type = ""
        self.auth_name = ""
        self.auth_key = 1
        self.host = hostobj

    def insert(self):
        try:
            self.mysql.connect()
            ssh_user = SSH_User(auth_key = self.auth_key,
                                auth_type = self.auth_type,
                                auth_user = self.auth_name)
            ssh_user.hid = self.host.id
            self.mysql.session.add(ssh_user)
            self.mysql.session.commit()

            self.mysql.close()
        except Exception as e:
            write_log("[bll.ssh_user.insert] {0}".format(e))

    def load_users_by_host(self):
        """
        通过主机获取该主机下的所有ssh用户信息,是多对一的关系查询
        :return:
        """
        try:
            self.mysql.connect()
            # 根据关联关系从主机得到主机下的所有用户
            ssh_user_list = self.mysql.session.query(SSH_User).filter(SSH_User.hid == self.host.id).all()
            self.mysql.close()
            return ssh_user_list
        except Exception as e:
            write_log("[bll.ssh_user.load_user_by_host] {0}".format(e), "ERROR")