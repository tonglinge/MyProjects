#!/usr/bin/env python
"""
数据库访问层，定义数据库访问接口
"""
from conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MySqlHelper(object):
    __server__ = settings.DBSERVER
    __engine__ = settings.PYTHON_API
    __user__ = settings.USER
    __password__ = settings.PASSWORD
    __port__ = settings.PORT
    __dbname__ = settings.DATABASE

    def __init__(self):
        self.engine = create_engine(
            "mysql+{engine}://{user}:{passwd}@{server}:{port}/{dbname}?charset=utf8".format(engine=self.__engine__,
                                                                                            user=self.__user__,
                                                                                            passwd=self.__password__,
                                                                                            server=self.__server__,
                                                                                            port=self.__port__,
                                                                                            dbname=self.__dbname__),
            echo=False)
        self.Session = sessionmaker(self.engine)
        self.session = None

    def connect(self):
        self.session = self.Session()

    def close(self):
        self.session.close()
