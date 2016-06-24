#!/usr/bin/env python
"""
公共函数模块
"""
import logging
import getpass
from hashlib import sha1
from conf import settings


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
    elif msgtype == "INFORMATION":
        show_msg = "\n\033[1;32m{0}\033[0m\n".format(msg)
    else:
        show_msg = "\n{0}\n".format(msg)
    print(show_msg)


def input_msg(message, limit_value=tuple(), password=False, int=False):
    """
    判断input输入的信息是否为空的公共检测函数,为空继续输入,不为空返回输入的信息
    :param int: 输入是否要求是数字
    :param password: 输入是否密码,如果是密码用getpass方法获取
    :param limit_value: 对输入的值有限制,必须为limit_value的值;ex:("admin","user")
    :param message: input()函数的提示信息
    :return: 返回输入的信息
    """
    is_null_flag = True
    while is_null_flag:
        if not password:
            input_value = input(message).strip().lower()
        else:
            input_value = getpass.getpass(message)

        # 输入必须数字
        if int:
            if not input_value.isdigit():
                show_message("输入类型错误,必须为数字!", "ERROR")
                continue
            else:
                break

        # 输入为空
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


def encry(string):
    """
    对密码进行加密
    :param string: 输入字符串
    :return: 加密后的字符串
    """
    md = sha1()
    md.update(string.encode())
    result = md.hexdigest()
    return result


def write_log(msg, msgtype="info"):
    log = logging.Logger("syslog")
    log.setLevel(logging.INFO)
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    filehandle = logging.FileHandler(settings.LOG_FILE)
    filehandle.setLevel(logging.INFO)
    log.addHandler(filehandle)
    filehandle.setFormatter(log_format)

    if msgtype == "info" or msgtype == "INFO":
        log.info(msg)
    if msgtype == "error" or msgtype == "ERROR":
        log.error(msg)
    if msgtype == "debug" or msgtype == "DEBUG":
        log.debug(msg)

    log.removeHandler(filehandle)
