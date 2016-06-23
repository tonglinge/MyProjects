#!/usr/bin/env python

import sys
from conf import settings
from bin import ftpserver
from conf import template
from modules.users import Users
from modules import common

if __name__ == "__main__":
    # Server 端启停标识
    SERVER_RUNNING_STATUS = False
    # 程序退出标识
    SYS_EXIT_FLAG = False
    # 服务端进程
    P_SERVER = None

    while not SYS_EXIT_FLAG:
        # 打印开始菜单
        if not SERVER_RUNNING_STATUS:
            menu = template.MENU_START.format(menu1="[1] 启动服务",
                                              menu2="[2] 添加用户",
                                              menu3="[3] 结束程序")
        else:
            menu = template.MENU_START.format(menu1="[1] 停止服务",
                                              menu2="[2] 添加用户",
                                              menu3="[3] 结束程序")
        print(menu)
        command = input("请选择功能编号:")
        if command not in("1", "2", "3"):
            print("请输入正确的功能编号!")
            continue

        if command == "3":
            if SERVER_RUNNING_STATUS:
                confirm = input("FTP 服务端正在运行中,确认要退出系统吗?(y/n)").strip().lower()
                if confirm == "y":
                    # 结束进程
                    P_SERVER.terminate()
                    SYS_EXIT_FLAG = True
                elif confirm == "n":
                    continue
                else:
                    if confirm not in ("y", "n"):
                        print("输入错误!")
                        continue
            else:
                SYS_EXIT_FLAG = True

        if command == "1":
            if SERVER_RUNNING_STATUS:
                # 服务端已经启动了,1则结束服务
                P_SERVER.terminate()
                SERVER_RUNNING_STATUS = False
                print("\033[1;31mFTP 服务端已停止!\033[0m;")
            else:
                # 服务端未启动,则启动服务端
                #P_SERVER = ftpserver.start()
                ftpserver.doprocess()
                SERVER_RUNNING_STATUS = True
                print("\033[1;30mFTP 服务端已启动!\033[0m;")

        if command == "2":
            try:
                tmpflag = False
                while not tmpflag:
                    username = common.input_msg("输入用户名[q返回]: ")
                    if username == "q":
                        tmpflag = True
                        continue
                    # 创建用户对象
                    new_user = Users(username)
                    if not new_user.exists:
                        userpasswd = common.input_msg("设置初始密码[默认12345]: ", default="12345")
                        totalspace = common.input_msg("设置磁盘配额[默认500M]: ", default=str(settings.HOME_QUOTA))
                        print("\n 正在初始化用户，请稍等.........\n")

                        new_user.password = common.encry_sha(userpasswd)
                        new_user.islocked = 0
                        new_user.isdel = 0
                        new_user.totalspace = int(totalspace) * 1024 * 1024
                        new_user.usedspace = 0
                        new_user.create_user()

                        print("初始化成功!")
                    else:
                        print("\033[1;30m用户已经存在!\033[0m;\n")
                        continue
            except Exception as e:
                common.writelog("start - main - type2 - {0}".format(e), "error")




