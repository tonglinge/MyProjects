#!/usr/bin/env python

import os
import time
from conf import settings
from modules import common
from modules.users import Users
from dbhelper import dbapi


def auth(client_socket, args):
    """
    客户端用户登录认证模块
    :param client_socket: 客户端socket对象
    :param args: 用户发送过来的数据 ex: "auth|test|a7470858e79c282bc2f6adfd831b132672dfd1224c1e78cbf5bcd057"
    :return: 3状态结果:  0: 认证成功 ， 1:用户不存在 , 2:用户被锁 3:用户名或密码错误
    """
    recv_data_list = args.split("|")
    username = recv_data_list[1]
    passwd = recv_data_list[2]
    # 将传入的用户对象实例化
    client_user = Users(username)
    # 若用户存在
    if client_user.exists:
        # 验证成功
        if client_user.user_auth(passwd):
            auth_status = "0"
            # 加载用户的磁盘配额信息
            user_space = "{0}|{1}".format(client_user.totalspace, client_user.usedspace)
        # 验证失败
        elif client_user.isdel == 1:
            # 用户已经删除,不存在
            auth_status = "1"
        elif client_user.islocked == 1:
            # 用户被锁了
            auth_status = "2"
        else:
            # 密码错误
            auth_status = "3"
    else:
        auth_status = "1"

    # 认证结果发送给客户端
    client_socket.send(bytes(auth_status, encoding='utf8'))

    # 认证成功则将用户空间信息发送到客户端
    if auth_status == "0":
        client_socket.send(bytes(user_space, 'utf8'))
    return client_user


def show(client_socket, client_user, recv_data):
    """
    执行用户的show命令，将当前文件夹(用户对象的当前路径属性 self.currpath)下的文件显示出来
    :param client_socket:  客户端socket对象
    :param client_user:  客户端 用户 对象
    :param recv_data: 用户发送过来的数据 show|
    :return: 返回用户对象的 self.currpath 目录下的所有文件及文件夹串
    """
    _check_folder = client_user.currpath
    # 获取所有文件名 或 文件夹名的 列表
    file_list = os.listdir(_check_folder)
    # 目录下的文件数
    file_count = len(file_list)

    # 如果有文件
    if file_count > 0:
        return_list = "{filecount}|".format(filecount=file_count)

        for i in file_list:
            f = os.path.join(_check_folder, i)
            stat = os.stat(f)
            create_time = time.strftime('%Y:%m-%d %X', time.localtime(stat.st_mtime))
            file_size = stat.st_size
            if os.path.isfile(f):
                return_list += "{ctime}        {fsize}    {fname}\n".format(ctime=create_time,
                                                                            fsize=str(file_size).rjust(10, " "),
                                                                            fname=i)
            if os.path.isdir(f):
                return_list += "{ctime}  <DIR> {fsize}    {fname}\n".format(ctime=create_time,
                                                                            fsize=str(file_size).rjust(10, " "),
                                                                            fname=i)
    else:
        return_list = "0|"

    try:
        # 开始发送信息到客户端
        # 1 先把结果串的大小发过去
        str_len = len(return_list.encode("utf-8"))
        client_socket.send(bytes(str(str_len), encoding='utf8'))
        # 2 接收客户端 read 标识，防止连包
        read_stat = client_socket.recv(100).decode()
        if read_stat == "ready":
            client_socket.sendall(return_list.encode('utf-8'))
           # client_socket.sendall(bytes(return_list, encoding='utf8'))
        else:
            common.writelog("client send show command，send 'ready' status fail", "info")
    except Exception as e:
        common.writelog(e, "error")


def cd(client_socket, client_user, recv_data):
    """
    对用户的cd命令进行操作，如果合法则修改用户对象self.currpath 为指定路径
    结果状态：0： 已经是家目录，1： 进入成功 2： 传入的文件夹名不是文件夹
    如果是 ..： 表示返回上一级菜单，如果当前目录已经是家目录则返回结果状态0，否则返回 1
    如果是非..： 如果 目录名为非目录，返回2， 否则返回1
    :param client_socket: 客户端socket对象
    :param client_user: 客户端用户对象
    :param recv_data: 接收的命令 "cd|[folder]" -> [folder]= .. or foldername
    :return: {结果状态(0,1,2)|目录名}
    """
    # 获取用户进入的目录
    cd_folder = recv_data.split("|")[1]
    # 返回上一级?
    try:
        if cd_folder == "..":
            # 如果当前已经是家目录了
            if client_user.currpath == client_user.homepath:
                send_data = "0|{0}".format(os.path.basename(client_user.currpath))
            else:
                client_user.currpath = os.path.dirname(client_user.currpath)
                send_data = "1|{0}".format(os.path.basename(client_user.currpath))
        else:
            # 组合路径
            tmp_path = os.path.join(client_user.currpath, cd_folder)
            # 是文件夹吗?
            if os.path.isdir(tmp_path):
                client_user.currpath = tmp_path
                send_data = "1|{0}".format(os.path.basename(client_user.currpath))
            else:
                # 不是文件夹
                send_data = "2|{0}".format(cd_folder)
        # 开始发送结果
        client_socket.sendall(bytes(send_data, 'utf8'))
    except Exception as e:
        common.writelog(e, "error")


def put(client_socket, client_user, recv_data):
    """
    用户上传文件,服务端接收模块，先发送一个准备接收状态
    如果不是断点续传文件，直接发送"4000|recved_size(0)"

    :param client_socket: 客户端socket对象
    :param client_user: 客户端用户对象
    :param recv_data: 发送过来的信息 "put|filename|filesize|filemd5"
    :return:
    """
    # 初始化上传文件的基本信息
    filename = recv_data.split("|")[1]
    filesize = int(recv_data.split("|")[2])
    filemd5 = recv_data.split("|")[3]

    # 检查文件是否以前上传过但未传完,用filemd5匹配,返回
    check_result = dbapi.check_breakpoint(filemd5, client_user)
    if check_result[0] == 0:
        # 不存在断点
        break_status = "0"
        recv_size = 0
        # 没有断点的话路径为用户对象当前路径
        save_path = os.path.join(client_user.currpath, filename)
        # 全新的文件的话,更新用户使用空间大小
        client_user.update_quota(filesize)
    else:
        break_status = "1"
        recv_size = check_result[0]
        # 有断点的话,文件路径为上次的文件路径
        save_path = check_result[1]

    # 将状态发送给客户端
    ready_status = "{0}|{1}".format(break_status, str(recv_size))
    client_socket.send(bytes(ready_status, 'utf8'))

    try:
        # 开始接收数据了,每次接收2048
        with open(save_path, 'a+b') as fa:
            fa.seek(recv_size)
            while filesize - recv_size > 2048:
                recv_data = client_socket.recv(2048)
                fa.write(recv_data)
                recv_size += len(recv_data)

                # 客户端突然断开了?
                if recv_data == b'':
                    # 写入文件,为以后断点续传准备
                    dbapi.write_breakpoint(filemd5, filesize, recv_size, save_path, client_user)
                    break
            # 剩下的不足2048了
            else:
                # 将剩下的全部收了
                recv_data = client_socket.recv(filesize - recv_size)
                # 客户端突然断开了?
                if recv_data == b'':
                    # 写入文件,为以后断点续传准备
                    dbapi.write_breakpoint(filemd5, filesize, recv_size, save_path, client_user)
                    common.writelog("Client upload file connected closed", "error")
                fa.write(recv_data)

                # 全部收完了,如果存在断点记录，完成后删除
                if break_status == "1":
                    dbapi.del_breakpoint(filemd5, client_user)

    except Exception as e:
        if recv_size < filesize:
            dbapi.write_breakpoint(filemd5, filesize, recv_size, save_path, client_user)
        common.writelog(str(e), "error")


def get(client_socket, client_user, recv_data):
    # 获取文件名
    filename = recv_data.split("|")[1]
    # 文件存在吗
    file = os.path.join(client_user.currpath, filename)
    if os.path.exists(file):
        # 先告诉客户端文件存在标识
        client_socket.send(bytes("1", 'utf8'))
        # 得到客户端回应
        client_socket.recv(100)
        # 发送文件的基本信息 "filesize|file_name|file_md5"
        filesize = os.stat(file).st_size
        file_md5 = common.encry_md5(file)
        sent_data = "{fsize}|{fname}|{fmd5}".format(fsize=str(filesize),
                                                    fname=filename,
                                                    fmd5=file_md5)
        client_socket.sendall(bytes(sent_data, 'utf8'))

        # 客户端收到了吗? 收到ready
        if str(client_socket.recv(100), 'utf-8') == "ready":
            # 开始发送数据了
            sended_size = 0
            with open(file, 'rb') as fr:
                while filesize - sended_size > 2048:
                    s_data = fr.read(2048)
                    client_socket.send(s_data)
                    sended_size += len(s_data)
                else:
                    s_data = fr.read(filesize - sended_size)
                    client_socket.send(s_data)
    else:
        # 文件不存在，下毛线啊
        client_socket.send(bytes("0", 'utf8'))
