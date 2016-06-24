#!/usr/bin/env python
import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from dalhelper.mysqlhelper import MySqlHelper
from module import tables, common
from conf import settings


def init_run():
    """
    数据库初始化模块，检测数据库是否已经创建，如果未创建数据库就生成表
    """
    if os.path.exists(settings.DB_INIT_LCK):
        pass
    else:
        confirm = common.input_msg("尚未创建数据表，是否现在初始化数据表?(y/n): ", ("y", "n"))
        # 开始创建数据表
        if confirm == "y":
            try:
                common.show_message("开始创建数据表......", "INFORMATION")
                base = tables.Base
                mysql = MySqlHelper()
                base.metadata.create_all(mysql.engine)
                common.show_message("数据表创建完成！", "INFORMATION")

                # 创建完成数据表后生成标识文件
                fb = open(settings.DB_INIT_LCK, 'wb')
                fb.close()

                # 创建一个管理员
                common.show_message("开始初始化用户........", "INFORMATION")
                user_admin = tables.Login_User(username='admin',
                                               password=common.encry('admin'),
                                               name='管理员',
                                               role='admin',
                                               isdel=0,
                                               expired=datetime.now() + timedelta(days=+999)
                                               )
                mysql.connect()
                mysql.session.add(user_admin)
                mysql.session.commit()
                common.show_message("初始化用户完成，请用admin / admin 登录", "INFORMATION")
                # 关闭连接
                mysql.close()
            except Exception as e:
                common.write_log(e, "error")
                sys.exit(-1)
