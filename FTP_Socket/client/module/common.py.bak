#!/usr/bin/env python
"""
author: wangsong
系统公共模块
"""
from datetime import datetime
import io
import sys
import hashlib
from conf import settings


def writelog(content, types):
    """
    自定义写错误日志
    :param types: 日志显示类型 : info  error
    :param content: 日志信息
    :return: 无返回，写入文件 error.log
    """
    _content = "\n{0} - {1} -  {2} ".format(datetime.now().strftime("%Y-%m-%d %X"), types, content)
    with open(settings.LOGS, "a+") as fa:
        fa.write(_content)


def encry_md5(file):
    """
    获取文件的MD5值，用于MD5校验
    :param file: 文件名
    :return: MD5值
    """
    fmd = hashlib.md5()
    file = io.FileIO(file, 'r')
    byte = file.read(2048)
    while byte != b'':
        fmd.update(byte)
        byte = file.read(2048)
    file.close()
    md5value = fmd.hexdigest()
    return md5value


def show_message(msg, msgtype):
    """
    对print函数进行封装，根据不同类型显示不同颜色
    :param msg:  显示的消息体
    :param msgtype:  消息类型
    :return: 返回格式化过的内容
    """
    if msgtype == "NOTICE":
        show_msg = "\n\033[1;33m{0}\033[0m\n".format(msg)
    elif msgtype == "ERROR":
        show_msg = "\n\033[1;31m{0}\033[0m\n".format(msg)
    elif msgtype == "INFO":
        show_msg = "\n\033[1;32m{0}\033[0m\n".format(msg)
    else:
        show_msg = "\n{0}\n".format(msg)
    print(show_msg)


def input_msg(message, limit_value=tuple()):
    """
    判断input输入的信息是否为空的公共检测函数,为空继续输入,不为空返回输入的信息
    :param limit_value: 对输入的值有限制,必须为limit_value的值;ex:("admin","user")
    :param message: input()函数的提示信息
    :return: 返回输入的信息
    """
    is_null_flag = True
    while is_null_flag:
        input_value = input(message).strip().lower()
        if not input_value:
            show_message("输入不能为空!", "ERROR")
            continue
        elif len(limit_value) > 0:
            if input_value not in limit_value:
                show_message("输入的值不正确,请重新输入!", "ERROR")
                continue
            else:
                is_null_flag = False
        else:
            is_null_flag = False
            continue
    return input_value


def encry_sha(string):
    """
    用户密码加密函数 sha224加密
    :param string: 明文字符串
    :return: 加密字符串
    """
    sha = hashlib.sha224()
    sha.update(string.encode())
    sha_value = sha.hexdigest()
    return sha_value

def input_command(message):
    """
    用户输入命令模块，用来检测用户输入命令是否合法，对输入命令去空格等处理
    :param message: 提示消息
    :return: 返回格式化过的命令 "show|","cd|args","put|args","get|args"
    """
    flag = False
    while not flag:
        command_list = ["show", "put", "get", "cd", "quit"]
        command_input = input(message).strip()

        if command_input == "show":
            return_command = "{0}|".format(command_input)
            flag = True
        elif command_input == "quit":
            return_command = command_input
            flag = True
        else:
            # 不是show命令都必须符合 command|args格式
            if command_input.count("|") != 1:
                print("\033[1;30m输入命令不合法\033[0m")
            else:
                cmd = command_input.split("|")[0].strip().lower()
                args = command_input.split("|")[1].strip()
                if cmd not in command_list:
                    print("\033[1;30m输入命令不合法\033[0m")
                else:
                    return_command = "{0}|{1}".format(cmd, args)
                    flag = True
    return return_command

def print_process(totalsize, curr_size):
    """
    打印进度条，打印66个#
    :param totalsize:
    :param curr_size:
    :return:
    """
    c = int((curr_size / totalsize) * 66)
    p = int((curr_size / totalsize) * 100)
    j = "#" * c
    sys.stdout.write("[ {0}% ] || {1}#\r".format(str(p), j))
    sys.stdout.flush()


