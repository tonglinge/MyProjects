#!/usr/bin/env python

from template import templates
from module import common
from bll.op_log import BLL_Op_Logs
from bll.login_user import BLL_Login_User
from dalhelper.mysqlhelper import MySqlHelper
from module import admin, interactive


def login(sqlhelper):
    while True:
        username = common.input_msg("登录名: ")
        passwd = common.input_msg("密码: ", password=True)

        # 实例化一个用户对象
        user = BLL_Login_User(sqlhelper)
        user.username = username
        user.password = common.encry(passwd)
        # 执行登录操作
        user.login()
        if user.exists:
            # 登录成功,如果是管理员进入管理员模块
            if user.role == "admin":
                admin_run(user, sqlhelper)

            else:
                # 普通用户进入普通用户模块
                user_run(user, sqlhelper)
                # print("name:", user.name, user.role)
        else:
            common.show_message("用户名或密码错误!", "ERROR")

        del user


def title_menu(userobj):
    # 填充菜单
    title = templates.LOGIN_MENU.format(user=userobj.username,
                                        role='管理员' if userobj.role == 'admin' else '普通用户',
                                        date=str(userobj.last_login_date)[0:19],
                                        )
    return title


def user_run(user, sqlhelper):
    """
    普通用户登录操作模块
    :param user:
    :return:
    """
    try:
        op_log = BLL_Op_Logs(user, sqlhelper)
        exit_flag = False
        while not exit_flag:
            tmpi = 0
            tmpflag = False
            # 打印标题
            print(title_menu(user))
            common.show_message("<-- 请选择要操作的主机 -->", "INFORMATION")
            # 获取用户所属组列表
            host_list = user.load_hosts_by_uid()
            # 打印主机列表
            for host in host_list:
                print("\033[1;32m  [{0}]   主机名:{1}  IP:{2}  所属组:{3}\033[0m".format(str(tmpi + 1),
                                                                                   host['hostname'],
                                                                                   host['ipaddr'],
                                                                                   host['groupname']
                                                                                   ))
                tmpi += 1
            # 选择一个要登录的主机
            while not tmpflag:
                exit_flag = False
                choose_id = common.input_msg("\n请选择要登录的主机编号(exit 退出): ")
                if choose_id == "exit":
                    exit_flag = True
                    break
                if int(choose_id) > len(host_list):
                    common.show_message("主机编号不存在!", "ERROR")
                    continue
                else:
                    choose_host = host_list[int(choose_id) - 1]
                    break
            # 是否要退出
            if exit_flag == True:
                continue

            # 要登录的主机IP
            ssh_host_ip = choose_host['ipaddr']
            ssh_host_port = choose_host['port']
            ssh_host_hostname = choose_host['hostname']
            # 获取选择的主机中用户可以使用的ssh用户列表
            ssh_users = user.load_sshusers(choose_host['hostid'])

            if len(ssh_users) == 0:  # 未找到可以使用的账户
                common.show_message("\n未配置登录用户,请联系系统管理员!", "ERROR")
                continue
            elif len(ssh_users) == 1:  # 如果当前主机只有一个用户可以操作
                ssh_user = ssh_users[0]
            else:  # 有多个用户,需要选择一个
                tmpi = 0
                for sshuser in ssh_users:
                    print(" [{0}] {1}".format(str(tmpi + 1), sshuser['username']))
                    tmpi += 1
                choose = common.input_msg("请选择要使用的SSH用户编号:", int=True)
                ssh_user = ssh_users[int(choose) - 1]

            # 记录一条op日志
            op_log.save_log(("用户[{0}]使用SSH用户[{1}]登录主机[{2}](IP:{3}).".format(user.username,
                                                                           ssh_user['username'],
                                                                           ssh_host_hostname,
                                                                           ssh_host_ip),), "ssh")
            # 调用paramiko进行登录
            # print(ssh_host_ip, ssh_host_port, ssh_user['username'], ssh_user['auth_type'], ssh_user['passwd'])
            interactive.run(user,
                            sqlhelper,
                            ssh_host_ip,
                            ssh_host_port,
                            ssh_user['username'],
                            ssh_user['auth_type'],
                            ssh_user['passwd'])
            op_log.save_log(("用户[{0}]使用SSH用户[{1}]登出主机[{2}](IP:{3}).".format(user.username,
                                                                           ssh_user['username'],
                                                                           ssh_host_hostname,
                                                                           ssh_host_ip),), "ssh")
            # 释放对象
            del op_log
    except Exception as e:
        common.write_log("[bin.main.user_run] {0}".format(e), "error")


def admin_run(userobj, sqlhelper):
    """
    管理员登录后的操作模块
    :param user：当前登录的用户对象
    """
    func_module_list = []
    while True:
        print(title_menu(userobj))

        # 打印功能菜单
        for menu in templates.ADMIN_MENU:
            mid = list(menu.keys())[0]
            mcontant = list(menu.values())[0]["showmsg"]
            module = list(menu.values())[0]["module"]
            print("[{0}] {1}".format(mid, mcontant))
            func_module_list.append(module)

        choose = common.input_msg("\n请选择功能(quit)：", ('1', '2', '3', '4', 'quit'))
        if choose == "quit":
            break
        else:
            # 根据setting中的菜单配置调用相关模块（admin.py)中
            choosed_module = func_module_list[int(choose) - 1]
            func = getattr(admin, choosed_module)
            func(sqlhelper)


def run():
    sqlhelper = MySqlHelper()
    login(sqlhelper)
