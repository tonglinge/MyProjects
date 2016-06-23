#!/usr/bin/env python
"""
__author: super
公共函数模块
"""
import sys
import logging
import hashlib
from conf import settings

def get_log_level():
    level = settings.LOG_LEVEL
    result = logging.INFO
    if level == "debug":
        result = logging.DEBUG
    if level == "warning":
        result = logging.WARNING
    if level == "error":
        result = logging.ERROR
    return result


def write_log(msg, msgtype, log_type="sys"):
    log = logging.getLogger("SSHLOG")
    log.setLevel(get_log_level())

    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # 记录到文件
    if log_type == "sys":
        filehandle = logging.FileHandler(settings.SYSLOG_FILE)
    else:
        filehandle = logging.FileHandler(settings.OPLOG_FILE)
    filehandle.setLevel(logging.INFO)
    log.addHandler(filehandle)
    filehandle.setFormatter(log_format)

    # 打印屏幕,只打印错误日志
    if settings.LOG_PRING:
        screenhandle = logging.StreamHandler()
        screenhandle.setLevel(logging.INFO)
        log.addHandler(screenhandle)
        screenhandle.setFormatter(log_format)

    if msgtype == "info":
        log.info(msg)
    if msgtype == "error":
        log.error(msg)
    if msgtype == "debug":
        log.debug(msg)

    log.removeHandler(filehandle)
    if settings.LOG_PRING:
        log.removeHandler(screenhandle)

def encry_sha(string):
    """
    用户登录密码加密
    :param string: 明文密码字符串
    :return: sha1加密的字符串
    """
    m = hashlib.sha1()
    m.update(string.encode())
    result = m.hexdigest()
    return result

def inputs(message, limit_value=tuple(), trycount=3):
    """
    判断input输入的信息是否为空的公共检测函数,为空继续输入,不为空返回输入的信息
    :param trycount: 操作失败次数
    :param limit_value: 对输入的值有限制,必须为limit_value的值;ex:("admin","user")
    :param message: input()函数的提示信息
    :return: 返回输入的信息
    """
    is_null_flag = True
    count = 0
    while is_null_flag:
        if count < trycount:
            input_value = input(message).strip()
            if not input_value:
                print("\033[1;30m 输入不能为空!\033[0m;")
                count += 1
                continue
            # 验证限制条件
            elif len(limit_value) > 0:
                if input_value not in limit_value:
                    print("\033[1;30m 输入的值不正确,请重新输入!\033[0m;")
                    count += 1
                    continue
                else:
                    is_null_flag = False
            else:
                is_null_flag = False
                continue

        else:
            print("尝试次数过多！")
            sys.exit(0)

    return input_value
