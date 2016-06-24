#!/usr/bin/env python
import hashlib
import random
import os
import time
from datetime import datetime, date
from conf import settings


def verification_code():
    """
    生成一个4位的验证码
    :return:  返回验证码
    """
    _code = list()
    for i in range(4):
        ra = random.randrange(4)
        if i == ra:
            _code.append(chr(random.randrange(97, 122)))
        else:
            _code.append(str(i))
    result = ''.join(_code)
    return result


def encrypt(string):
    """
    字符串加密函数
    :param string: 待加密的字符串
    :return:  返回加密过的字符串
    """
    ha = hashlib.md5(b'oldboy')
    ha.update(string.encode('utf-8'))
    result = ha.hexdigest()
    return result


def write_log(content):
    """
    写错误日志
    :param content: 日志信息
    :return: 无返回，写入文件 error.log
    """
    _content = "\n{0} : {1} ".format(datetime.now().strftime("%Y-%m-%d %X"), content)
    _filename = os.path.join(settings.LOG_PATH, "errlog.log")
    with open(_filename, "a+") as fa:
        fa.write(_content)


# 获取汉字个数
def get_chinese_num(uchar):
    i = 0
    for utext in uchar:
        if u'\u4e00' <= utext <= u'\u9fa5':
            i += 1
    return i


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


def create_serialno():
    """
    生成一个消费、转账、提款时的流水号，不重复
    :return: 流水号
    """
    serno = "{0}{1}".format(datetime.now().strftime("%Y%m%d%H%M%S"), str(int(time.time())))
    return serno


def numtochr(num_of_weekday):
    """
    将数字星期转换为中文数字
    :param num_of_weekday: 星期几的数字字符( 0,1,2,3,4,5,6)
    :return: 中文 星期几
    """
    chrtuple = ('日', '一', '二', '三', '四', '五', '六')
    num = int(num_of_weekday)
    return chrtuple[num]


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

def input_date(msg, default_date):
    """
    对输入的日期进行判断是否正确 yyyy-mm-dd or yyyy-m-d
    :param msg:输入提示信息
    :param default_date: 默认日期
    :return:返回日期 str类型
    """
    check_flag = False
    while not check_flag:
        strdate = input(msg).strip()
        if not strdate:
            strdate = default_date

        try:
            date_list = strdate.split("-")
            result = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
            check_flag = True
        except ValueError:
            show_message("输入日期不合法,请重新输入!", "ERROR")
            continue
    return result.strftime("%Y-%m-%d")
