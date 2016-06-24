#!/usr/bin/env python
"""
__author: super
数据库访问层：
1 提供从数据文件、报表文件中读取数据的接口
2 将数据写入到数据文件的接口
"""
import os
import json
from conf import settings
from modules.common import write_log


def append_db_json(contant, filename):
    """
    将信息以 json 格式写入数据表文件(追加)
    :param contant: 要写入的 json 格式内容
    :param filename: 要写入的数据表文件名
    :return: 无返回
    """
    try:
        with open(filename, 'a+') as fa:
            fa.write(json.dumps(contant))
            fa.write("\n")
    except Exception as e:
        write_log(e)


def write_db_json(contant, filename):
    """
    将信息以 json 格式写入数据表文件（覆盖）
    :param contant: 写入的json数据内容
    :param filename: 要写入的文件名
    :return: 无返回结果
    """
    try:
        with open(filename, 'w+') as fw:
            fw.write(json.dumps(contant))
    except Exception as e:
        write_log(e)


def load_data_from_db(tabename):
    """
    从指定的数据表中获取所有数据,通过 json 方式将数据返回
    :param tabename: 数据文件名
    :return: 返回所有结果
    """
    try:
        with open(tabename, 'r+') as f:
            return json.load(f)
    except Exception as e:
        write_log(e)


def load_bill_report(cardno, startdate, enddate):
    """
    从信用卡对账单中获取指定卡的对账信息数据, 获取某一个时间段内的数据
    :param enddate: 查询记录的结束日期
    :param startdate: 查询记录的开始日期
    :param cardno: 信用卡卡号
    :return: 信用卡对账单数据 ,返回结果为 list 数据类型
    """
    r_file = os.path.join(settings.REPORT_PATH, "report_bill")
    result = []
    try:
        with open(r_file, "r+") as f:
            for line in f:
                _record = json.loads(line)
                if _record["cardno"] == cardno:
                    if startdate <= _record["starttime"] <= enddate:
                        result.append(_record)
        return result
    except Exception as e:
        write_log(e)


def load_shop_history(user, startdate, enddate):
    """
    查找报表记录中的指定用户的购物历史记录,将结果存入到列表中
    :param user:  用户名
    :param startdate: 开始日期
    :param enddate: 结束日期
    :return: 结果 dict_list
    """
    _file = os.path.join(settings.REPORT_PATH, "shopping_history")
    result = list()
    try:
        with open(_file, "r") as f:
            for line in f:
                _record = json.loads(line)
                # 如果找到指定用户记录
                if list(_record.keys())[0] == user:
                    if list(_record.values())[0]["time"] >= startdate <= enddate:
                        result.append(_record)
        return result
    except Exception as e:
        write_log("dbapi > load_shop_history > {0}".format(e))


def load_statement_list(cardno):
    """
    从对账单中获取记录,
    :param cardno: 对账单文件
    :return: 返回一个列表
    """
    file = os.path.join(settings.REPORT_PATH, "statement_{0}".format(cardno))
    result_list = list()
    try:
        if os.path.isfile(file):
            with open(file, 'r+') as f:
                for line in f:
                    statement = json.loads(line)
                    result_list.append(statement)
        return result_list
    except Exception as e:
        write_log("dbapi > load_statement_list > {0}".format(e))


def write_statement_list(cardno, db_list):
    """
    将对账单记录写入对账单文件，更新
    :param cardno: 对账单的卡号
    :param db_list: 新的对账信息列表
    :return:
    """
    file = os.path.join(settings.REPORT_PATH, "statement_{0}".format(cardno))
    with open(file, 'w+') as f:
        for newrecord in db_list:
            f.write(json.dumps(newrecord))
            f.write("\n")

