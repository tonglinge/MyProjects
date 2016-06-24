#!/usr/bin/env python
import os
from conf import settings, errorcode, template
from modules import common
from modules.creditcard import CreditCard
from dbhelper import dbapi


class Users(object):
    # 用户数据库
    __database = "{0}.db".format(os.path.join(settings.DATABASE['dbpath'], settings.DATABASE["tables"]["users"]))

    def __init__(self):
        self.username = ""  # 登录名
        self.password = ""  # 登录密码
        self.bindcard = ""  # 绑定卡
        self.islogin = False  # 登录状态
        self.name = ""  # 姓名
        self.mobile = ""  # 手机
        self.islocked = 0  # 是否锁定
        self.role = "user"  # 账户权限
        self.trycount = 0  # 登录尝试次数
        self.isdel = 0  # 用户删除标识
        self.dict_user = {}
        self.db_load()

    def db_load(self):
        self.dict_user = dbapi.load_data_from_db(self.__database)

    def _user_login(self, password):
        """
        用户登录验证模块,对用户对象进行判断,登录成功后返回一个新的用户对象
        :return:
        """
        # 对输入的密码加密
        _password = common.encrypt(password)

        for user, details in self.dict_user.items():
            # 找到用户名
            if user == self.username and not details["isdel"]:
                # 是否被锁定
                if details["islocked"] == 0:
                    # 账户未锁定,验证密码
                    if details["password"] == _password:
                        self.islogin = True
                        self.bindcard = details["bindcard"]
                        self.name = details["name"]
                        self.mobile = details["mobile"]
                        self.role = details["role"]
                        self.isdel = details["isdel"]
                        self.islocked = details["islocked"]
                        self.password = password
                        break
                    else:
                        # 密码错误,失败1次
                        self.trycount += 1
                else:
                    # 账户锁定了
                    self.islocked = 1

    def login(self):
        """
        用户登录过程函数，输入用户名和密码后调用内部方法 _user_login进行登录验证
        :return:
        """
        while self.trycount < settings.ERROR_MAX_COUNT:
            self.username = input("用户名: ")
            password = input("密  码: ")

            if not self.user_exists:
                common.show_message("用户名不存在！", "ERROR")
                continue

            # 调用用户登录方法进行登录
            self._user_login(password)

            # 用户锁定就直接退出
            if self.islocked:
                common.show_message("该用户已被锁定,请联系系统管理员！", "ERROR")
                self.trycount = 0

                break

            # 登录成功 退出登录
            if self.islogin:
                break
            else:
                common.show_message("用户名密码错误", "NOTICE")
        else:
            # 失败3次了还输? 锁了你
            self.islocked = 1

            # 更新用户信息
            self.dict_user[self.username]["islocked"] = self.islocked
            self.update_user()
            common.show_message("输入错误次数过多,请联系系统管理员!", "ERROR")

        # 将用户的登录尝试次数恢复初始值 0
        self.trycount = 0

    def update_user(self):
        """
        用户数据更新方法,用户修改信息、用户账户锁定、解锁等操作之后更新数据库文件
        :return:
        """
        try:
            '''
            _password = common.encrypt(self.password)
            self.dict_user[self.username]["password"] = _password
            self.dict_user[self.username]["islocked"] = self.islocked
            self.dict_user[self.username]["name"] = self.name
            self.dict_user[self.username]["mobile"] = self.mobile
            self.dict_user[self.username]["bindcard"] = self.bindcard
            self.dict_user[self.username]["isdel"] = self.isdel
            self.dict_user[self.username]["role"] = self.role
            '''
            # 写入数据库文件
            dbapi.write_db_json(self.dict_user, self.__database)
            return True
        except Exception as e:
            common.write_log(e)
            return False

    @property
    def user_exists(self):
        """
        判断用户名是否存在,用户注册时判断，存在返回True, 否则返回False
        :return: True / False
        """
        if self.username in list(self.dict_user.keys()):
            return True
        else:
            return False

    def create_user(self):
        """
        新创建一个用户,将用户数据同步写入到数据库文件
        :return:
        """
        self.dict_user[self.username] = dict(password=common.encrypt(self.password),
                                             name=self.name,
                                             mobile=self.mobile,
                                             bindcard=self.bindcard,
                                             role=self.role,
                                             islocked=0,
                                             isdel=0,
                                             )
        dbapi.write_db_json(self.dict_user, self.__database)

    def del_user(self):
        """
        删除用户,逻辑删除
        :return:
        """
        self.dict_user[self.username]["isdel"] = 1
        self.update_user()

    def unlock_user(self):
        self.dict_user[self.username]["islocked"] = 0
        self.update_user()

    def init_user_info(self):
        """
        创建用户，完善用户资料信息
        :return:
        """
        is_null_flag = True
        while is_null_flag:
            self.username = input("登录用户名(小写字母）:").strip().lower()
            if not self.username:
                common.show_message("用户名不能为空", "ERROR")
                continue
            elif self.user_exists:
                common.show_message("该用户名已存在", "ERROR")
                continue
            else:
                is_null_flag = False
                continue

        self.name = common.input_msg("姓名:")
        self.password = common.input_msg("密码:")
        self.mobile = common.input_msg("手机:")
        self.role = common.input_msg("用户权限(user/admin):", ("admin", "user"))
        self.create_user()
        common.show_message("用户创建成功!", "NOTICE")

    @staticmethod
    def user_auth(func):
        """
        用户登录验证装饰器, userobj 为登录用户对象,未登录时可以传入一个空对象
        :param func: 被装饰的函数
        :return:
        """

        def login_check(self, userobj):
            # 用户还未登录
            if not userobj.islogin:
                common.show_message("用户未登录,请先登录系统！", "NOTICE")

                # 开始用户登录
                userobj.login()
                # 登录成功了吗
                if userobj.islogin:
                    return func(self, userobj)
                else:
                    common.show_message("登录失败,请联系系统管理员!", "ERROR")

            else:
                return func(self, userobj)

        return login_check

    def bind_card(self, cardobj):
        """
        用户绑定信用卡,调用该方法绑定卡时,先实例化卡对象,再判断卡是否有效(卡是否存在、卡密码是否正确)
        :param cardobj: 信用卡对象
        :return: 成功 99999 / 失败 错误码
        """
        # 判断用户输入的卡号和实际卡号所有人是不是一致的
        if self.username == cardobj.owner:
            self.bindcard = cardobj.cardno
            self.update_user()
            return errorcode.NO_ERROR
        else:
            return errorcode.CARD_OWNER_ERROR

    def logout(self):
        """
        注销当前用户,将系统属性置空
        :return:
        """
        self.islogin = False
        self.bindcard = ""
        self.mobile = ""
        self.name = ""
        self.password = ""
        self.username = ""
        common.show_message("注销成功", "NOTICE")

    def modify_password(self):
        """
        个人中心 - 修改密码
        :return:
        """
        _not_null_flag = False
        try:
            while not _not_null_flag:
                _new_password = input("输入新密码: ").strip()
                _confirm_password = input("再次输入确认密码:").strip()
                if not _new_password or not _confirm_password:
                    common.show_message("密码不能为空,请重新输入!", "ERROR")
                    continue
                if _new_password != _confirm_password:
                    common.show_message("两次输入密码不一致,请重新输入!", "NOTICE")
                    continue
                _not_null_flag = True
            self.password = _new_password
            _password = common.encrypt(self.password)
            self.dict_user[self.username]["password"] = _password
            self.update_user()
            common.show_message("密码修改成功!", "INFORMATIOM")
            return True
        except Exception as e:
            common.write_log(e)
            return False

    def modify_user_info(self):
        """
        打印用户信息
        :return: 用户信息字符串
        """
        if self.islocked == 1:
            currstatus = "账户锁定"
        else:
            currstatus = "账户正常"
        frmuser = template.user_info.format(
            username=self.username,
            name=self.name,
            mobile=self.mobile,
            bindcard=self.bindcard,
            role=self.role,
            islocked="是" if self.islocked == 1 else "否",
            isdel="是" if self.isdel == 1 else "否"
        )
        # 打印用户信息
        common.show_message(frmuser, "NOTICE")

        # 开始修改
        common.show_message("请输入新的资料,若不更新直接回车：", "NOTICE")
        new_name = input("姓名({0}); ".format(self.name))
        new_mobile = input("手机({0}): ".format(self.mobile))
        self.name = self.name if len(new_name) == 0 else new_name
        self.mobile = self.mobile if len(new_mobile) == 0 else new_mobile
        # 输入信用卡卡号
        _card_noerror = False
        while not _card_noerror:
            new_bindcard = input("绑定卡({0}): ".format(self.bindcard))
            if len(new_bindcard) > 0:
                # 创建一个卡对象
                cardobj = CreditCard(new_bindcard)
                if not cardobj.card_is_exists:
                    common.show_message("您输入的卡号不存在!", "ERROR")

                elif cardobj.owner != self.username:
                    common.show_message("您输入的卡号非法,请联系系统管理员!", "ERROR")
                else:
                    # 都正确了
                    self.bindcard = new_bindcard
                    _card_noerror = True
            else:
                _card_noerror = True
        # 更新用户资料库变量
        self.dict_user[self.username]["name"] = self.name
        self.dict_user[self.username]["mobile"] = self.mobile
        self.dict_user[self.username]["bindcard"] = self.bindcard
        if self.update_user():
            common.show_message("信息更新成功!", "NOTICE")
        else:
            common.show_message("更新失败,查看日志!", "ERROR")

    def load_user_info(self):
        """
        根据用户名获取用户信息
        :return: 用户对象
        """
        if self.user_exists:
            user_detail = self.dict_user[self.username]
            self.name = user_detail["name"]
            self.bindcard = user_detail["bindcard"]
            self.islocked = user_detail["islocked"]
            self.role = user_detail["role"]
            self.isdel = user_detail["isdel"]
            self.mobile = user_detail["mobile"]
            return True
        else:
            return False
