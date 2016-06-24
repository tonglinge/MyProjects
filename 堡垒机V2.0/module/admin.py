#!/usr/bin/env python
import copy
from datetime import datetime, timedelta
from bll.groups import BLL_Host_Group
from bll.hosts import BLL_Hosts
from bll.ssh_user import BLL_SSH_User
from bll.login_user import BLL_Login_User
from module import common


def load_host_groups(sqlhelper):
    """
    显示所有主机组，用户选择返回一个选择的主机组列表
    :param sqlhelper: 数据库访问对象
    :return: 返回选择的主机组
    """
    tmpi = 0
    tmpflag = False

    # 获取所有组信息
    print("\n\033[1;30m <-- 选择所属主机组编号 -->\033[0m")
    groupobj = BLL_Host_Group(sqlhelper)
    grouplist = groupobj.load_group_all()
    while tmpi < len(grouplist):
        print("  [{0}]  {1}".format(str(tmpi + 1), grouplist[tmpi].groupname))
        tmpi += 1

    # 选择主机组
    while not tmpflag:
        choose_group = []
        gidlist = common.input_msg("选择组编号(多个组用逗号分割): ")
        for gid in gidlist.split(","):
            if not gid.isdigit():
                common.show_message("输入错误!", "ERROR")
                tmpflag = False
                break
            elif int(gid)  > len(grouplist):
                common.show_message("组编号不存在,请重新选择!", "ERROR")
                tmpflag = False
                break
            else:
                # 将选择的主机组对象放入选择列表中
                choose_group.append(grouplist[int(gid) - 1])
                tmpflag = True
    return choose_group


def add_group(sqlhelper):
    """
    添加主机组
    :param sqlhelper: 数据库连接对象
    :return:
    """
    try:
        groupname = common.input_msg("请输入主机组名称: ")
        groupobj = BLL_Host_Group(sqlhelper)
        groupobj.groupname = groupname
        if not groupobj.load_group_by_name():
            groupobj.insert()
            common.show_message("主机组添加成功", "INFORMATION")
        else:
            common.show_message("该组已经存在!", "NOTICE")
    except Exception as e:
        common.write_log("[module.admin.add_group] {0}".format(e))


def add_host(sqlhelper):
    """
    添加主机信息
    :param sqlhelper:
    :return:
    """
    try:
        hostname = common.input_msg("  请输入主机名: ")
        hostip = common.input_msg("  请输入IP地址: ")
        sshport = common.input_msg("  请输入SSH端口(default:22): ", int=True)
        choose_group = load_host_groups(sqlhelper)

        # 生成主机对象并执行sql写入
        hostobj = BLL_Hosts(sqlhelper)
        hostobj.hostname = hostname
        hostobj.ipaddr = hostip
        hostobj.sshport = sshport
        hostobj.insert(choose_group)
        common.show_message("主机添加成功!", "INFORMATION")
    except Exception as e:
        common.write_log("[module.admin.add_host] {0}".format(e))


def add_host_user(sqlhelper):
    """
    添加主机用户信息
    :param sqlhelper:
    :return:
    """
    try:
        group_list = load_host_groups(sqlhelper)
        while len(group_list) > 1:
            print("添加主机用户时一次只能选择一台主机,请选择一个主机组!")
            group_list = load_host_groups(sqlhelper)

        # 显示选择组下的所有主机信息
        tmpi = 0
        #print(choose_group,type(choose_group))
        choose_group = group_list[0]
        hostobj = BLL_Hosts(sqlhelper)
        host_list = hostobj.load_hosts_by_group(choose_group)
        print("\n\033[1;30m <--- 主机组 [{0}] 包含如下主机,请选择主机编号 --->\033[0m".format(choose_group.groupname))
        while tmpi < len(host_list):
            print("  [{0}]  主机名:{1}   IP:{2}".format(tmpi+1,
                                                     host_list[tmpi].hostname.ljust(10, " "),
                                                     host_list[tmpi].ipaddr)
                  )
            tmpi += 1

        # 选择主机编号
        while True:
            host_id = common.input_msg("选择主机编号(q 返回): ")
            if host_id == "q":
                break
            else:
                host_id = int(host_id)

            # 判断选择的组编号是否越界
            if host_id > len(host_list):
                common.show_message("选择编号错误,请重新选择!", "ERROR")
                continue
            else:
                break
        choose_host = host_list[host_id-1]

        # 对选择的主机添加用户
        choose_flag = False
        ssh_user = BLL_SSH_User(sqlhelper, choose_host)
        while not choose_flag:
            auth_user = common.input_msg("登录用户名: ")
            auth_type = common.input_msg("登录验证类型[1:密码 / 2:密钥]: ", limit_value=('1','2'))
            auth_key = common.input_msg("登录密码/密钥文件: ")

            # 新增用户
            ssh_user.auth_key = auth_key
            ssh_user.auth_name = auth_user
            ssh_user.auth_type = int(auth_type)
            ssh_user.insert()
            # 继续添加
            common.show_message("添加成功!", "INFORMATION")
            goon = common.input_msg("是否继续添加用户(y/n)? :", limit_value=('y','n'))
            if goon == "y":
                continue
            else:
                choose_flag = True
    except Exception as e:
        common.write_log("[module.admin.add_host_user] {0}".format(e))


def add_login_user(sqlhelper):
    """
    添加登录堡垒及的账户信息
    :param sqlhelper:
    :return:
    """
    try:
        back_flag = False
        while not back_flag:
            # 初始化输入
            login_user = BLL_Login_User(sqlhelper)
            while True:
                username = common.input_msg("用户名(q 返回): ")
                if username == "q":
                    back_flag = True
                    break
                # 判断用户是否存在
                login_user.username = username
                if login_user.user_exists:
                    common.show_message("该用户名已经存在,请重新输入!", "ERROR")
                    continue
                else:
                    break

            if not back_flag:
                password = common.input_msg("密  码: ", password=True)
                name = common.input_msg("姓  名: ")
                role = common.input_msg("权限(1:普通用户 / 2:管理员): ", limit_value=('1','2'))
                expired_days = common.input_msg("有效期(天): ", int=True)
                expired = datetime.now() + timedelta(days=int(expired_days))
                if role == "1":
                    role = "user"
                else:
                    role = "admin"

                # 给用户划分组
                group_list = load_host_groups(sqlhelper)
                # group_list对象在数据库操作中关闭链接后就没了，不知到为什么，copy一份
                group_list_bak = copy.deepcopy(group_list)

                # 开始新建一个用户
                login_user.password = common.encry(password)
                login_user.name = name
                login_user.role = role
                login_user.expired = expired
                login_user.insert(group_list)

                common.show_message("用户[{0}]创建成功!".format(username), "INFORMATION")

                # 给用户分配所属组下的主机登录用户,主机包含多个登录用户,给用户分配一个用户
                choose = common.input_msg("需要现在给[{0}]分配各主机的管理用户吗?(y/n)".format(username), limit_value=('y','n'))
                if choose == "y":
                    hostobj = BLL_Hosts(sqlhelper)
                    sshuserobj = BLL_SSH_User(sqlhelper, hostobj)

                    # 保存所有主机登录用户的id，用于去重
                    ssh_user_set = []

                    for usergroup in group_list_bak:
                        # 根据用户的所属组获取各组下的所有主机
                        hostobj_list = hostobj.load_hosts_by_group(usergroup)
                        # 从主机列表遍历获取所有ssh用户信息
                        for host in hostobj_list:
                            sshuserobj.host = host
                            # 获取主机下的所有用户信息
                            sshuser_list = sshuserobj.load_users_by_host()
                            # 将这些信息添加到集合中，单条记录为字典格式
                            for sshuser in sshuser_list:
                                sshuser_info = dict(sid=sshuser.id,
                                                    username=sshuser.auth_user,
                                                    host=host.hostname,
                                                    group=usergroup.groupname)
                                ssh_user_set.append(sshuser_info)


                    # 全部遍历完成后的集合中存放的就是该用户可以使用的登录主机用户信息，下面用来选择
                    common.show_message("<--可以使用的用户列表-->", "INFORMATION")
                    for user in ssh_user_set:
                        print("用户ID: {0}  用户名: {1}  所属主机: {2}  所属组: {3}".format(
                            str(user['sid']).ljust(3, ' '),
                            user['username'].ljust(10, ' '),
                            user['host'].ljust(8, ' '),
                            user['group'].ljust(8, ' '))
                        )
                    ssh_user_id_list = common.input_msg("请选择SSH用户ID(多个用,分隔): ")
                    # 当前处理的登录用户对象
                    curr_user = BLL_Login_User(sqlhelper)
                    curr_user.username = login_user.username
                    curr_user.insert_ssh_user(ssh_user_id_list)
                    common.show_message("分配成功!".format(username), "INFORMATION")

                else:
                    pass
    except Exception as e:
        common.write_log("[module.admin.add_login_user] {0}".format(e), "ERROR")






