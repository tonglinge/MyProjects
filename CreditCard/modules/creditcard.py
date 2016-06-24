#!/usr/bin/env python
import os
from datetime import datetime, date, timedelta
from conf import settings, errorcode
from modules import common
from dbhelper import dbapi


class CreditCard(object):
    __database = "{0}.db".format(os.path.join(settings.DATABASE['dbpath'], settings.DATABASE["tables"]["creditcard"]))

    def __init__(self, cardno):
        # 信用卡卡号
        self.cardno = cardno
        # 信用卡密码
        self.password = ""
        # 卡所有者
        self.owner = ""
        # 信用卡额度
        self.credit_total = settings.CREDIT_TOTAL
        # 信用卡透支余额
        self.credit_balance = settings.CREDIT_TOTAL
        # 信用卡日息
        self.dayrate = settings.EXPIRE_DAY_RATE
        # 提现手续费率
        self.feerate = settings.FETCH_MONEY_RATE
        # 所有信用卡数据
        self.credit_card = {}
        # 信用卡是否存在标识
        self.card_is_exists = True
        # 信用卡状态(是否冻结)
        self.frozenstatus = 0

        # 获取卡的信息
        self._load_card_info()

    def _load_card_info(self):
        """
        根据用户输入的卡号获取信用卡信息,如果卡号不存在就返回False
        :return: 信用卡对象
        """
        exists_flag = False
        self.credit_card = dbapi.load_data_from_db(self.__database)
        for key, items in self.credit_card.items():
            if key == self.cardno:
                self.password = self.credit_card[self.cardno]['password']
                self.credit_total = self.credit_card[self.cardno]['credit_total']
                self.credit_balance = self.credit_card[self.cardno]['credit_balance']
                self.owner = self.credit_card[self.cardno]['owner']
                self.frozenstatus = self.credit_card[self.cardno]['frozenstatus']

                exists_flag = True
                break
        self.card_is_exists = exists_flag

    """
    @property
    def card_is_exists(self):
        if self.cardno in list(self.credit_card.keys()):
            return True
        else:
            return False
    """

    def card_pay(self, cost, paytype, sereialno):
        """
        信用卡支付,从信用卡可透支余额中扣费
        :param sereialno: 流水号
        :param cost: 消费金额 float类型
        :param paytype: 消费类型 int类型  ( 1:消费、2:转账、3:提现、4:手续费 ) 对于2,3类型的支付要扣手续费,单记录一条流水单
        :return:
        """
        if paytype == 1:
            payfor = "消费"
        elif paytype == 2:
            payfor = "转账"
        elif paytype == 3:
            payfor = "提现"
        elif paytype == 4:
            payfor = "手续费"
        else:
            payfor = "未知"

        # 支付扣款
        self.credit_balance -= cost

        # 记录消费流水对账单,将发生了费用还没有还款的账单信息写入文件 report_bill 中
        _tmp_bill_record = dict(cardno="{0}".format(self.cardno),
                                starttime=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
                                payfor=payfor,
                                cost=cost,
                                serialno=sereialno)
        dbapi.append_db_json(_tmp_bill_record, os.path.join(settings.REPORT_PATH, "report_bill"))

        # 更新信用卡可透支余额信息到数据库 creditcard.db
        self.credit_card[self.cardno]["credit_balance"] = self.credit_balance
        dbapi.write_db_json(self.credit_card, self.__database)

    def create_card(self):
        """
        新发行一张行用卡
        :return:
        """
        password = common.encrypt(self.password)
        self.credit_card[self.cardno] = dict(password=password,
                                             credit_total=self.credit_total,
                                             credit_balance=self.credit_balance,
                                             owner=self.owner,
                                             frozenstatus=self.frozenstatus)
        # 保存到数据库
        dbapi.write_db_json(self.credit_card, self.__database)

    def update_card(self):
        password = common.encrypt(self.password)
        self.credit_card[self.cardno]["password"] = password
        self.credit_card[self.cardno]["owner"] = self.owner
        self.credit_card[self.cardno]["credit_total"] = self.credit_total
        self.credit_card[self.cardno]["credit_balance"] = self.credit_balance
        self.credit_card[self.cardno]["frozenstatus"] = self.frozenstatus
        # 写入数据库
        dbapi.write_db_json(self.credit_card, self.__database)

    def _pay_check(self, cost, password):
        """
        转账、提现时验证操作，判断卡的余额与支付密码是否正确。并返回错误类型码
        :param cost:  转账、提现金额（包含手续费）
        :param password: 支付密码
        :return: 错误码
        """
        totalfee = cost
        # 提现金额及手续费和大于余额,
        if totalfee > self.credit_balance:
            return errorcode.BALANCE_NOT_ENOUGHT
        elif common.encrypt(password) != self.password:
            return errorcode.CARD_PASS_ERROR
        else:
            return errorcode.NO_ERROR

    def fetch_money(self, count, passwd):
        """
        提现
        :param count: 提现金额
        :param passwd:信用卡提现密码
        :return: 返回错误类型码
        """
        totalfee = count + count * self.feerate
        check_result = self._pay_check(totalfee, passwd)
        if check_result == errorcode.NO_ERROR:
            # 扣取提现金额并写入数据库，生成账单
            self.card_pay(count, 3, common.create_serialno())
            # 扣取手续费并写入数据库, 生成账单
            self.card_pay(count * self.feerate, 4, common.create_serialno())
            return errorcode.NO_ERROR
        else:
            return check_result

    def translate_money(self, trans_count, passwd, trans_cardobj):
        """
        信用卡转账模块
        :param trans_count: 要转账的金额
        :param passwd: 信用卡密码
        :param trans_cardobj: 对方卡号对应的卡对象
        :return: 转账结果
        """
        totalfee = trans_count + trans_count * self.feerate
        check_result = self._pay_check(totalfee, passwd)
        if check_result == errorcode.NO_ERROR:
            # 先扣款，生成消费流水账单
            self.card_pay(trans_count, 2, common.create_serialno())
            # 扣手续费, 生成消费流水账单
            self.card_pay(trans_count * self.feerate, 4, common.create_serialno())
            # 给对方卡充值,并写入数据库文件
            trans_cardobj.credit_balance += totalfee
            trans_cardobj.update_card()
            return errorcode.NO_ERROR
        else:
            return check_result

    def load_statement_list(self):
        """
        获取要还款的对账单列表数据，仅包含对账单号、还款日、应还款额、已还款额
        :return: 对账单列表
        """
        # 获取要显示的信息
        list_info = dbapi.load_statement_list(self.cardno)
        return list_info

    def recreate_statement(self):
        """
        根据今天的日期将当前卡的对账单重新生成,主要对过了还款日的账单重新生成利息信息
        :return:
        """
        # 获取当前日期
        today = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        # 获取所有卡的对账单信息
        card_statement = dbapi.load_statement_list(self.cardno)
        tmp_list = list()
        # 如果有记录
        if len(card_statement) > 0:
            for record in card_statement:
                for k, v in record.items():
                    # 如果已经还款了,将对账单放入临时列表中
                    if v["isfinished"] == 1:
                        tmp_list.append(record)
                    else:
                        # 还未还款? 获取还款日期
                        pay_day = datetime.strptime(v["pdate"], "%Y-%m-%d")
                        # 如果还款日大于当前日期,无利息
                        day_delta = (today - pay_day).days
                        if day_delta > 0:
                            # 过了还款日了，计算利息 = 总费用 * 日息 * 超过天数
                            interest = v["total"] * settings.EXPIRE_DAY_RATE * day_delta
                            # 更新利息信息记录
                            record[k]["interest"] = interest
                            # 将更新过的记录写入临时列表
                            tmp_list.append(record)
                        else:
                            # 没有过还款日直接写入临时列表
                            tmp_list.append(record)
            # 都处理完了，将更新过的列表写入文件，替换原有信息
            dbapi.write_statement_list(self.cardno, tmp_list)
        else:
            # 此卡没有对账单记录
            pass


