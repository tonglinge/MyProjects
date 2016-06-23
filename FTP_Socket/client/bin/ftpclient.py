#!/usr/bin/env python
"""
__author : wangsong
主接口文件,通过本文件去调用命令模块
"""
from module.client import Client
from conf import template
from conf import settings
from conf import codes
from module import common

def start():
    server_ip = settings.FTP_SERVER_IP
    server_port = settings.FTP_SERVER_PORT

    common.show_message(template.START_MENU, "INFO")
    common.show_message("正在连接FTP服务器 {0}:{1} ......".format(server_ip, server_port), "INFO")

    # 创建一个client对象
    client = Client(server_ip, server_port)
    # 连接服务器，返回结果
    conn_result = client.connect()
    # 连接成功
    if conn_result == codes.CONN_SUCC:
        common.show_message("连接成功!", "NOTICE")

        # 客户端登录
        client_login(client)

        # 登录成功
        if client.login_status:
            # 退出系统
            exit_flag = False
            while not exit_flag:
                # 显示登录后的菜单
                show_menu = template.LOGINED_MENU.format(client.username,
                                                         str(int(client.totalspace / 1024 / 1024)),
                                                         str(int(client.usedspace / 1024 / 1024)))
                common.show_message(show_menu, "NOTICE")
                # 输入命令串
                input_command = common.input_command("[ 输入命令 ] : ")
                if input_command == "quit":
                    exit_flag = True
                else:
                    # 获取命令的的command
                    cmd_func = input_command.split("|")[0]
                    try:
                        # 通过反射调用Client类的对应command方法,并返回执行结果
                        if hasattr(Client, cmd_func):
                            func = getattr(Client, cmd_func)
                            exec_result = func(client, input_command)
                            print(exec_result)
                        else:
                            common.writelog("Client {0} 未找到".format(input_command), "error")
                    except Exception as e:
                        common.writelog(e, "error")

    else:
        common.show_message("连接失败", "ERROR")


def client_login(userobj):
    """
    客户端前台登录操作
    :param userobj: 当前客户端对象
    :return: 登录结果
    """
    tmp_flag = False
    while not tmp_flag:
        # 开始登录
        username = common.input_msg("Input username: ")
        password = common.input_msg("Input password: ")
        # sha224加密结果
        password = common.encry_sha(password)
        # 开始登录认证
        auth_status = userobj.login(username, password)

        if auth_status == codes.AUTH_SUCC:
            common.show_message("登录成功", "NOTICE")
            tmp_flag = True
        elif auth_status == codes.AUTH_FAIL:
            common.show_message("用户名或密码错误", "ERROR")
        elif auth_status == codes.AUTH_LOCKED:
            common.show_message("账户已被锁定,联系管理员!", "ERROR")
        else:
            common.show_message("用户不存在", "ERROR")
