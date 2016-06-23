#!/usr/bin/env python
"""
__author: wangsong
用户相关操作类，包括：
创建用户、用户验证、获取用户的磁盘配额信息、断点续传文件信息、创建用户文档
"""
import os
from conf import settings
from modules import common
from dbhelper import dbapi


class Users(object):
    def __init__(self, username):
        self.username = username
        self.password = ""
        self.exists = False
        self.islocked = 0
        self.isdel = 0
        self.totalspace = 0
        self.usedspace = 0
        self.homepath = os.path.join(settings.USER_HOME_FOLDER, self.username)  # 用户家目录
        self.currpath = self.homepath  # 用户当前目录
        self.__check_users()

    def __check_users(self):
        """
        检测用户是否存在，如果存在则exists标识True,并加载用户信息
        当用户从客户端登录时，先实例化用户后判断用户exists标识是否为True，如为False直接返回不存在，否则进行认证
        :return: 修改用户存在标识self.exists值
        """
        user_list = dbapi.read_section_all()
        if self.username in user_list:
            self.exists = True
            self.currpath = self.homepath
            self.__load_user_info()

    def __load_user_info(self):
        """
        从配置文件中加载用户的信息，填充对象属性
        :return:
        """
        user_info = dbapi.read_section_by_name(self.username)
        self.password = user_info["password"]
        self.islocked = int(user_info["islocked"])
        self.isdel = int(user_info["isdel"])
        self.totalspace = int(user_info["totalspace"])
        self.usedspace = int(user_info["usedspace"])

    def user_auth(self, password):
        """
        用户登录验证模块，主要是密码验证，密码用sha224算法加密
        :param password: 密码明文
        :return: 密码校验成功True / 失败 False
        """
        # 密码正确了
        if password == self.password:
            if self.islocked == 1 or self.isdel == 1:
                return False
            else:
                return True
        else:
            return False

    def create_user(self):
        """
        创建一个新用户
        :return:
        """
        try:
            kwargs = dict(password=self.password, islocked=str(self.islocked), isdel=str(self.isdel),
                          totalspace=str(self.totalspace), usedspace=str(self.usedspace))
            dbapi.add_option(self.username, **kwargs)
            self.__create_folder()
        except Exception as e:
            common.writelog(e, "error")

    def __create_folder(self):
        """
        创建用户后再upload目录下创建一个该用户的家目录
        :return:
        """
        _folder = self.homepath
        os.mkdir(_folder)

    def update_quota(self, filesize):
        """
        更新用户的磁盘空间配额信息
        :param filesize: 新上传文件的大小
        :return:
        """
        self.usedspace += filesize
        # 组合参数为字典
        kwargs = dict(password=self.password, islock=str(self.islocked), isdel=str(self.isdel),
                      totalspace=str(self.totalspace),
                      usedspace=str(self.usedspace))
        dbapi.modify_option(self.username, **kwargs)
