#!/usr/bin/env python
import os
from datetime import datetime
from conf import settings, errorcode, template
from modules.users import Users
from modules.creditcard import CreditCard
from modules import common
from dbhelper import dbapi


class Shopping(object):
    # 购物商城界面
    __welcome_title = template.shopping_index_menu
    # 购物商城商品数据库
    __database = "{0}.db".format(os.path.join(settings.DATABASE['dbpath'], settings.DATABASE["tables"]["shopping"]))
    # 购物记录报表存放文件
    __shop_report_file = os.path.join(settings.REPORT_PATH, "shopping_history")

    def __init__(self):
        # 存放购物车列表
        self.shopping_cart = []
        # 购物总费用
        self.shopping_cost = 0
        # 用户选择的商品分类 key
        self.goods_classify_id = ""
        # 数据表中所有商品信息
        self.shop_market = dict()
        # 购物商城欢迎菜单
        self.welcome_menu = ""

        self._get_shop_market()  # 获取数据表数据
        self._construct_title_menu()  # 购物商城欢迎菜单

    def _get_shop_market(self):
        """
        获取购物商城所有商品信息,存入类字段(shop_market)
        :return:  self.shop_market
        """
        self.shop_market = dbapi.load_data_from_db(self.__database)

    def _construct_title_menu(self):
        """
        构建欢迎菜单,存入类字段(welcome_menu)
        :return: self.welcome_menu
        """
        _menu = []
        keys = list(self.shop_market.keys())
        # 按类型编号排序
        keys.sort()
        for goods_type_id in keys:
            goods_type_name = self.shop_market[goods_type_id]['typename']
            _menu.append("[{0}] {1}   ".format(goods_type_id, goods_type_name))
        _menu.append("[{0}] {1}   ".format("4", "查看购物车"))
        _menu.append("[{0}] {1}   ".format("5", "购物结算"))
        _menu.append("[{0}] {1}   ".format("0", "退出商城"))
        self.welcome_menu = self.__welcome_title.format(menu="".join(_menu))

    def get_goods_list_by_typeid(self):
        """
        根据用户选择的商品分类编号,获取该分类下所有商品,返回结果为tuple
        :return:  返回tuple类型: 指定分类商品下的所有商品信息
        """
        if self.goods_classify_id not in list(self.shop_market.keys()):
            return None
        else:
            return self.shop_market[self.goods_classify_id]['product']

    @staticmethod
    def print_goods_list(goods_list):
        """
        将goods_list列表中的商品信息输出到屏幕,商品列表或购物车商品列表
        :param goods_list: 要打印的商品信息，类型为tuple
        :return: 输出到屏幕
        """
        _goodlist = goods_list
        print("|{0}|{1}|{2}|".format('商品编号'.center(11), '商品名称'.center(50), '商品价格(RMB)'.center(10)))
        print('%s' % '-' * 95)

        for goods in _goodlist:
            chinese_num = common.get_chinese_num(goods['name'])
            len_name = len(goods['name'])
            space_str = (55 - len_name - chinese_num) * " "
            print('| %-12s | %s |%15s|' % (goods['no'], goods['name'] + space_str, str(goods['price'])))

    def add_shopping_card(self, goodsid):
        """
        根据用户输入的商品编号，将商品编号加入购物车，如果商品编号不存在返回False,添加成功返回True
        :param goodsid: 商品编号
        :return: 成功 True / 失败 False
        """
        exist_flag = False
        # 从商品列表中获取指定类型的所有商品信息(tuple)
        _goods_tuple = self.shop_market[self.goods_classify_id]['product']

        # 开始查找输入的商品编号
        for goods in _goods_tuple:
            if goods['no'] == goodsid:
                self.shopping_cart.append(goods)
                self.shopping_cost += goods['price']
                exist_flag = True
                break
        return exist_flag

    @Users.user_auth
    def payfor_shopcart(self, userobj):
        """
        购物车结算模块,功能包括：购物车付款、购物记录写入文件、
        :param kwargs: 字典参数 {cost=购物车金额, userobj=用户对象}
        :return:
        """
        # 判断用户有没有绑定信用卡
        if not userobj.bindcard:
            # 用户没有绑定信用卡,直接返回错误，在外层绑卡
            return errorcode.CARD_NOT_BINDED
        else:
            # 用户绑定了信用卡了, 获取信用卡信息(实例化对象)
            cardobj = CreditCard(userobj.bindcard)
            # 卡余额够吗
            if cardobj.credit_balance < self.shopping_cost:
                common.show_message("您的信用卡本月额度不够! ", "NOTICE")
                return errorcode.BALANCE_NOT_ENOUGHT
            else:
                # 生成一个流水号
                serno = common.create_serialno()
                # 调用卡的支付模块进行支付
                cardobj.card_pay(self.shopping_cost, 1, serno)
                # 记录购物流水
                shopping_record = {userobj.username: {"time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                                      "cost": self.shopping_cost,
                                                      "serno": serno,
                                                      "detail": self.shopping_cart}}
                # 写入报表记录文件
                dbapi.append_db_json(shopping_record, self.__shop_report_file)

                # 购物结算完成后将对象的购物车清空, 购物车商品总价清0 ,待下次购物
                self.shopping_cart.clear()
                self.shopping_cost = 0
                return errorcode.NO_ERROR

