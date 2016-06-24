#!/usr/bin/env python
"""
账单生成模块：
1 从report_bill中便利所有流水记录，获取所有卡号
2 将卡号存放到列表中
3 对列表进行集合类型转换
4 根据集合中的唯一的卡号信息，每个卡号生成一个文件 cardno_startdate_enddate报表文件,文件中存放字典信息对账单
5 将对账的费用统计信息接入一个统计文件 ,包括字段：卡号、对应详单文件名、账单日期、还款日期、应还款金额、已还款金额、
{"detail":{[],[]}
 "
"""
import calendar
import os
from datetime import datetime, timedelta
from datetime import date
from dbhelper import dbapi
from conf import template
from conf import settings
from modules import common
from modules.shopping import Shopping


def get_date():
    """
    用户输入一个时间段,如果显示报表是要提供开始、结束日期,返回开始，结束时间
    :return: 字典格式,{"start":startdate, "end": enddate}
    """
    startdate = common.input_date("输入查询开始日期(yyyy-mm-dd)[default:2016-01-01]: ", "2016-01-01")
    enddate = common.input_date("输入查询结束日期(yyyy-mm-dd)[default: today]: ", date.today().strftime("%Y-%m-%d"))
    return {"start": startdate, "end": enddate}


def print_shopping_history(userobj):
    """
    个人中心 - 购物历史记录打印模块
    :param userobj:    用户对象
    :return:  显示指定时间段的购物历史记录
    """
    date_between = get_date()
    start = date_between["start"]
    end = date_between["end"]
    # 通过dbapi获得要查询的记录列表,结果为dict_list类型
    history_list = dbapi.load_shop_history(userobj.username, start, end)
    # 获取模板文件样式
    _template = template.shopping_history
    common.show_message(_template.format(username=userobj.username,
                                         startdate=start,
                                         enddate=end), "NOTICE")

    if not history_list:
        common.show_message("无购物记录!", "NOTICE")
    else:
        for record in history_list:
            # 获取消费信息
            _tmprec = list(record.values())[0]
            common.show_message("\n流水号:{0}       时间:{1}     消费金额：{2}\n".format(_tmprec["serno"],
                                                                               _tmprec["time"],
                                                                               _tmprec["cost"]), "NOTICE")
            # 调用Shopping的类方法打印详单
            Shopping.print_goods_list(_tmprec["detail"])


def print_bill_history(userobj):
    """
    个人中心-账单明细 打印模块
    :param userobj: 用户对象
    :return:
    """
    dates = get_date()
    startdate = dates["start"]
    enddate = dates["end"]
    # 保存所有账单流水的记录列表,数据为一个字符串
    msglist = list()
    # 获取显示模板
    _template = template.report_bill
    # 获取符合条件的账单明细记录(dict_list 类型)
    _recordlist = dbapi.load_bill_report(userobj.bindcard, startdate, enddate)
    for record in _recordlist:
        tmpmsg = "{time}      {costtype}  {cost}     {crdno}".format(time=record["starttime"],
                                                                     costtype=record["payfor"].ljust(10),
                                                                     cost=str(record["cost"]).ljust(6),
                                                                     crdno=record["serialno"])
        msglist.append(tmpmsg)
    # 填充模板并打印
    common.show_message(_template.format(cardno=userobj.bindcard,
                                         startdate=startdate,
                                         enddate=enddate,
                                         billdetail="\n".join(msglist)
                                         ), "NOTICE")


def create_card_statement(cardno):
    """
    生成信用卡对账单
    :param cardno:卡号
    :return:
    """
    # 获得当前时间
    currday = datetime.now().strftime("%Y-%m-%d")
    today = date.today().day
    # 如果是账单日22号 开始生成账单
    if today == settings.STATEMENT_DAY:
        # 生成对账单数据库中存放对账单数据的字典 key
        startday = (datetime.now() + timedelta(days=-30)).strftime("%Y%m{0}".format(settings.STATEMENT_DAY))
        endday = datetime.now().strftime("%Y%m%d")
        statement_key = "{start}{end}".format(start=startday, end=endday)

        # 从对账单流水中计算出要还款的金额
        startdate = (datetime.now() + timedelta(days=-30)).strftime("%Y-%m-{0} 00:00:00".format(settings.STATEMENT_DAY))
        enddate = datetime.now().strftime("%Y-%m-%d 00:00:00")
        # 获取卡号对应的消费流水记录列表
        bill_list = dbapi.load_bill_report(cardno, startdate, enddate)

        statement_total = 0.00
        # 如果有消费记录,生成对账单
        if len(bill_list) > 0:
            for bill in bill_list:
                # 获取一个对账单日期的消费总费用
                statement_total += bill["cost"]

            # 获取还款日期 下个月10号
            statement_pdate = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-10")

            # 生成对账单的统计数据字典{"2016012220160222":{"账单日":currday,
            #                                             "账单范围":startdate至enddate,
            #                                             "账单金额":statement_bill,
            #                                             "已还款":0,
            #                                             "还款日":pdate
            #                                             "已还完":0}}

            statement_dict = {statement_key: {"billdate": currday,
                                              "startdate": startdate,
                                              "enddate": enddate,
                                              "total": statement_total,
                                              "payed": 0,
                                              "pdate": statement_pdate,
                                              "interest": 0,
                                              "isfinished": 0}}
            # 对账单文件名
            file_name = os.path.join(settings.REPORT_PATH, "statement_{0}".format(cardno))
            # 写入文件
            dbapi.append_db_json(statement_dict, file_name)


def create_statement_main():
    """
    卡对账单初始化模块,从卡数据库文件中加载所有卡号，对所有卡调用生成对账单模块
    :return:
    """
    _database = "{0}.db".format(os.path.join(settings.DATABASE['dbpath'], settings.DATABASE["tables"]["creditcard"]))
    card_list = dbapi.load_data_from_db(_database)
    cards = list(card_list.keys())
    for cardno in cards:
        create_card_statement(cardno)


def print_statement_list(cardno, list_info):
    """
    将卡号对应的未还款记录显示出来，
    :param cardno: 卡号
    :param list_info: 信用卡对账单信息
    :return: 无返回
    """
    # 获取显示模板
    show_template = template.report_statement_list
    tmpstrlist = list()

    # 如果获取到了对账单数据
    if len(list_info) > 0:
        for record in list_info:
            for k, v in record.items():
                # 如果还未全部还完款
                if v["isfinished"] == 0:
                    tmpmsg = "{sno}{pdate}{spay}{payed}".format(sno=k.ljust(20),
                                                                pdate=v["pdate"].ljust(13),
                                                                spay=str(v["total"]).ljust(13),
                                                                payed=str(v["payed"]))
                    tmpstrlist.append(tmpmsg)
        tmpstrlist.append("您目前共有 {0} 个账单".format(len(tmpstrlist)))
        # 填充模板,将填充后的魔板信息返回
        result = show_template.format(cardno=cardno, show_msg="\n".join(tmpstrlist))
        return result
    else:
        return ""


def print_statement_detail(cardno, serino, details):
    """
    还款模块 - 用户选择还款的单号后，显示详细的还款对账单及流水信息
    :param cardno: 信用卡卡号
    :param serino: 对账单编号
    :param statement_list: 对账单列表
    :return: 返回填充后的模板信息
    """
    # 获取显示模板
    show_template = template.report_statement_detail
    # 获取指定编号的详细信息
    _billdate = details["billdate"]  # 账单日
    _sdate = details["startdate"]  # 账单开始日期
    _edate = details["enddate"]  # 账单结束日期
    _total = details["total"]  # 费用总额
    _payed = details["payed"]  # 已还款金额
    _pdate = details["pdate"]  # 还款日
    _interest = details["interest"]  # 利息

    # 获取详细的流水清单
    _flows = list()
    _recordlist = dbapi.load_bill_report(cardno, _sdate, _edate)
    for info in _recordlist:
        tmpmsg = "{time}      {costtype}  {cost}     {crdno}".format(time=info["starttime"],
                                                                     costtype=info["payfor"].ljust(10),
                                                                     cost=str(info["cost"]).ljust(6),
                                                                     crdno=info["serialno"])
        _flows.append(tmpmsg)

    # 填充模板
    result_message = show_template.format(cardno=cardno,
                                          serino=serino,
                                          billdate=_billdate,
                                          sdate=_sdate[0:10],
                                          edate=_edate[0:10],
                                          pdate=_pdate,
                                          total=_total,
                                          payed=_payed,
                                          interest=_interest,
                                          details="\n".join(_flows))
    return result_message
