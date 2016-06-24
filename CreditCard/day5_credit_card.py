#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys
from datetime import date, datetime
from conf import template, errorcode
from conf import settings
from modules import shopping, common
from dbhelper import dbapi
from modules.users import Users
from modules.creditcard import CreditCard
from modules import report


def doshopping(userobj):
    """
    购物商城模块,进行购物部分的所有处理
    :param userobj:  一个用户对象,如果用户未登录，在支付模块会通过装饰器来登录
    :return:
    """
    # 实例化商城
    shoppobj = shopping.Shopping()
    # 选择商品类型
    exitflag = False
    while not exitflag:
        # 开始菜单
        print(shoppobj.welcome_menu)
        shop_cassify_id = input("请选择商品分类编号[1-3]: ").strip().lower()
        if not shop_cassify_id: continue
        if shop_cassify_id == "0":
            exitflag = True
            continue
        if int(shop_cassify_id) not in range(1, 6):
            common.show_message("请选择正确的商品类型编号!", "ERROR")
            continue
        elif shop_cassify_id == "4":
            # 查看购物车
            shopping.Shopping.print_goods_list(shoppobj.shopping_cart)
            common.show_message("当前购物车共有 {0} 件商品,合计 {1} 元 !".format(len(shoppobj.shopping_cart),
                                                                    shoppobj.shopping_cost), "INFORMATION")
            continue
        elif shop_cassify_id == "5":
            # 购物结算
            dealresult = shoppobj.payfor_shopcart(userobj)
            if dealresult == errorcode.NO_ERROR:
                common.show_message("支付完成!", "INFORMATION")
        else:
            # 获取用户选择的商品类型编号
            shoppobj.goods_classify_id = shop_cassify_id
            # 获得商品类型编号对应的商品列表
            goods_list = shoppobj.get_goods_list_by_typeid()
            if not goods_list:
                common.show_message("未找到商品信息！", "NOTICE")
                continue

            # 开始选择商品，添加到购物车
            choose_goods_flag = True
            while choose_goods_flag:
                # 显示指定商品分类下的所有商品列表(Shopping类静态方法)
                shopping.Shopping.print_goods_list(goods_list)
                goods_id = input("选择商品编号,加入购物车(q返回上一级): ").strip().lower()
                if not goods_id: continue
                # 返回上一级
                if goods_id == "q":
                    choose_goods_flag = False
                    continue
                else:
                    # 将选择商品加入购物车
                    result = shoppobj.add_shopping_card(goods_id)
                    if result:
                        # 添加成功,显示购物车所有商品信息
                        shopping.Shopping.print_goods_list(shoppobj.shopping_cart)
                        common.show_message("已将商品加入购物车!", "INFORMATION")
                        # 是否继续添加
                        nextflag = False
                        while not nextflag:
                            donext = input("继续购物(y) or 返回上一级(q):").strip().lower()
                            if donext == "y":
                                break
                            elif donext == "q":
                                choose_goods_flag = False
                                break
                            else:
                                continue
                    else:
                        # 添加购物车失败
                        common.show_message("添加购物车失败,请检查输入商品编号是否正确!", "ERROR")
                        continue


def user_login(userobj, today, weekoftoday):
    """
    主菜单的2号菜单登录系统模块
    :param userobj: 当前用户对象
    :param today: 菜单显示的日期
    :param weekoftoday: 菜单显示的星期
    :return:
    """
    quitflag = False
    while not quitflag:
        if userobj.islogin:
            # 如果用户已经登录,菜单功能2为个人中心,调用另一个菜单模板 index_user_center
            print(template.index_user_center.format(userobj.name, today, common.numtochr(weekoftoday)))
            _chooseflag = False
            while not _chooseflag:
                _choose = input("选择功能：")
                if _choose not in ("1", "2", "3", "4", "5", "6"):
                    common.show_message("选择正确的功能编号!", "ERROR")
                    continue
                else:
                    _chooseflag = True

            # 返回上级菜单
            if _choose == "6":
                quitflag = True
            else:
                # 根据用户按键开始处理,从 template 模块查找各按键对应的模块,通过反射来执行
                func_dict = template.user_center_func
                modulepy = __import__(func_dict[_choose]["module"])
                # 1,2,5号键为users类方法，
                if _choose in ('1', '2', '5'):
                    modulesobj = getattr(modulepy, "users")
                    classobj = getattr(modulesobj, "Users")
                    func = getattr(classobj, func_dict[_choose]["func"])
                else:
                    # 3,4为 report 模块的方法
                    modulesobj = getattr(modulepy, "report")
                    func = getattr(modulesobj, func_dict[_choose]["func"])
                func(userobj)
        else:
            # 用户未登录,调用 Users类的登录模块
            userobj.login()
            quitflag = True


def card_center(userobj):
    if userobj.islogin:
        # 重新load一下数据
        userobj.db_load()
        cardno = userobj.bindcard
        # 获得信用卡对象
        card = CreditCard(cardno)
    else:
        # 未登录信用卡
        input_flag = False
        while not input_flag:
            cardno = input("请输入信用卡卡号: ").strip().lower()
            if cardno.isnumeric():
                card = CreditCard(cardno)
                if card.card_is_exists:
                    pwd = input("请输入密码:")
                    if common.encrypt(pwd) == card.password:
                        common.show_message("登录成功", "NOTICE")
                        input_flag = True
                        continue
                else:
                    common.show_message("卡号不存在,请重新输入!", "ERROR")
                    continue
            else:
                common.show_message("卡号无效!", "ERROR")
                continue

    show_template = template.index_ATM
    quitflag = False
    while not quitflag:
        print(show_template.format(cardno=card.cardno))
        _choose = common.input_msg("请选择功能: ", ("1", "2", "3", "4", "5"))
        # 返回
        if _choose == "5":
            quitflag = True
            continue

        # 查看信用卡信息
        if _choose == "1":
            common.show_message(template.card_info.format(cardno=card.cardno,
                                                          owner=card.owner,
                                                          total=card.credit_total,
                                                          balance=card.credit_balance,
                                                          status="正常" if card.frozenstatus == 0 else "冻结"
                                                          ), "NOTICE")
        # 提现
        if _choose == "2":
            if card.frozenstatus == 1:
                common.show_message("卡已冻结,请联系客服!", "ERROR")
            else:
                common.show_message("信用卡提现将收取 {0}% 的手续费!".format(settings.FETCH_MONEY_RATE * 100), "NOTICE")
                quitflag = False
                while not quitflag:
                    cost = common.input_msg("请输入要提现的金额(q返回):")
                    if cost.isnumeric():
                        cardpasswd = common.input_msg("请输入信用卡密码:")
                        # 执行提现操作
                        exe_result = card.fetch_money(float(cost), cardpasswd)
                        if exe_result == errorcode.NO_ERROR:
                            common.show_message("已完成提现！", "NOTICE")
                        if exe_result == errorcode.BALANCE_NOT_ENOUGHT:
                            common.show_message("信用卡可透支余额不足!", "ERROR")
                        if exe_result == errorcode.CARD_PASS_ERROR:
                            common.show_message("信用卡密码错误!", "ERROR")
                    elif cost == "q":
                        quitflag = True
                        continue
                    else:
                        common.show_message("输入错误!", "ERROR")
        # 转账
        if _choose == "3":
            if card.frozenstatus == 1:
                common.show_message("此卡已冻结,请联系客服!", "ERROR")
            else:
                common.show_message("信用卡转账将收取 {0}% 的手续费!".format(settings.FETCH_MONEY_RATE * 100), "NOTICE")
                quitflag = False
                while not quitflag:
                    trans_cardno = common.input_msg("请输入要转账的卡号(q返回):")
                    if trans_cardno.isnumeric():
                        # 生成一个卡对象, 验证卡号是否存在
                        trans_cardobj = CreditCard(trans_cardno)

                        # 卡号不存在返回主菜单
                        if not trans_cardobj.card_is_exists:
                            common.show_message("卡号不存在,请确认!", "ERROR")
                            quitflag = True
                            continue
                        else:
                            # 卡号存在
                            trans_cost = common.input_msg("请输入要转账的金额: ")

                            # 如果输入的均为数字
                            if trans_cost.isnumeric():
                                comfirm = common.input_msg("确定要给卡号 {0} 转入人民币 {1} 元吗(y/n)?".format(trans_cardobj.cardno,
                                                                                                  trans_cost),
                                                           ("y", "n"))
                                if comfirm == "y":
                                    cardpasswd = common.input_msg("请输入信用卡密码:")

                                    # 执行转账操作
                                    exe_result = card.translate_money(float(trans_cost), cardpasswd, trans_cardobj)

                                    if exe_result == errorcode.NO_ERROR:
                                        common.show_message("转账完成！", "NOTICE")
                                    if exe_result == errorcode.BALANCE_NOT_ENOUGHT:
                                        common.show_message("信用卡可透支余额不足!", "ERROR")
                                    if exe_result == errorcode.CARD_PASS_ERROR:
                                        common.show_message("信用卡密码错误!", "ERROR")
                            else:
                                common.show_message("输入错误!", "ERROR")

                    elif trans_cardno == "q":
                        quitflag = True
                        continue
                    else:
                        common.show_message("输入错误!", "ERROR")

        # 还款
        if _choose == "4":
            # 更新一下对账单信息
            card.recreate_statement()

            quitflag = False
            while not quitflag:
                # 获取对账单所有列表
                interest_list = card.load_statement_list()
                # 获取还未还款的记录并显示
                message_info = report.print_statement_list(card.cardno, interest_list)

                # 如果有要还款的记录
                if len(message_info) > 0:
                    common.show_message(message_info, "NOTICE")
                    # 输入要还款的单号
                    serino_list = list()
                    for order in interest_list:
                        serino_list.append(list(order.keys())[0])
                    serino_list.append("q")
                    pay_serno = common.input_msg("请选择还款的16位账单号(q退出)：", tuple(serino_list))

                    if pay_serno == "q":
                        quitflag = True
                        continue
                    else:
                        for i in range(len(interest_list)):
                            for k, details in interest_list[i].items():
                                if k == pay_serno:
                                    # 显示指定单号的相信对账单信息
                                    common.show_message(report.print_statement_detail(card.cardno,
                                                                                      pay_serno,
                                                                                      details),
                                                        "NOTICE")
                                    pay_fee = common.input_msg("请输入还款金额:")
                                    if pay_fee.isnumeric():
                                        # 更新已还款金额 = 现在还的金额 + 已经还的金额
                                        total_payed = details["payed"] + float(pay_fee)
                                        interest_list[i][pay_serno]["payed"] = total_payed

                                        # 全还了吗？需要还款数 = 消费总费用 + 利息
                                        need_pay = details["total"] + details["interest"]
                                        if total_payed >= need_pay:
                                            # 还款数大于等于需要还款数，则更新已还款字段信息
                                            interest_list[i][pay_serno]["isfinished"] = 1
                                        else:
                                            # 没全部还款
                                            common.show_message("您尚未全部还款,请在还款日前尽快还款!", "NOTICE")
                                        # 将还款后的信息写入数据库更新
                                        dbapi.write_statement_list(card.cardno, interest_list)

                                        # 还款成功
                                        common.show_message("还款成功", "NOTICE")
                                        # 是否继续
                                        iscontinue = common.input_msg("继续还款吗(y/n)?", ("y", "n"))
                                        if iscontinue == "n":
                                            quitflag = True

                                    else:
                                        common.show_message("输入数据不正确，请重新输入!", "ERROR")
                else:
                    common.show_message("无账单信息！", "NOTICE")
                    quitflag = True


def get_users():
    """
    显示用户的信息,用户新建、删除、解锁用户时显示用户基本信息
    :return:
    """
    username = common.input_msg("请输入用户名:")
    # 创建一个用户实例
    _deluser = Users()
    _deluser.username = username
    # 如果用户名存在,load用户信息成功
    if _deluser.load_user_info():
        # 先显示一下用户的信息
        common.show_message(template.user_info.format(username=_deluser.username,
                                                      name=_deluser.name,
                                                      mobile=_deluser.mobile,
                                                      role=_deluser.role,
                                                      isdel="否" if _deluser.isdel == 0 else "是",
                                                      islocked="否" if _deluser.islocked == 0 else "是",
                                                      bindcard=_deluser.bindcard)
                            , "NOTICE")
        return _deluser
    else:
        common.show_message("用户名不存在!", "ERROR")
        return False


def fill_card_info():
    """
    填充信用卡资料信息
    :return: 返回一个信用卡对象
    """
    retry_flag = False
    while not retry_flag:
        cardno = common.input_msg("请输入卡号:")
        cardobj = CreditCard(cardno)
        if cardobj.card_is_exists:
            common.show_message("卡号已存在,请重新输入卡号", "ERROR")
            continue
        else:
            retry_flag = True
            continue

    cardobj.password = common.input_msg("请输入密码:")
    cardobj.credit_total = common.input_msg("信用额度(default:{0}):".format(cardobj.credit_total))
    cardobj.credit_balance = cardobj.credit_total
    cardobj.owner = common.input_msg("所有者:")
    return cardobj


def manager(userobj):
    """
    主菜单后台管理模块
    :param userobj: 当前登录用户对象
    :return:
    """
    if userobj.islogin:
        if userobj.role == "admin":
            quit_flag = False
            while not quit_flag:
                _show_template = template.index_admin
                print(_show_template.format(username=userobj.name))
                _choose = input("选择操作功能: ").strip().lower()
                # 创建新用户
                if _choose == "1":
                    _newuser = Users()
                    # 调用初始化用户函数创建新用户
                    _newuser.init_user_info()
                # 删除用户
                if _choose == "2":
                    _user = get_users()
                    if _user:
                        confirm = common.input_msg("确定要删除此用户吗(y/n)?", ("y", "n"))
                        if confirm == "y":
                            _user.del_user()
                            common.show_message("用户删除成功!", "NOTICE")
                # 解锁用户
                if _choose == "3":
                    _user = get_users()
                    if _user:
                        confirm = common.input_msg("确认解锁吗(y/n)?", ("y", "n"))
                        if confirm == "y":
                            _user.unlock_user()
                            common.show_message("用户解锁成功!", "NOTICE")
                # 发行信用卡
                if _choose == "4":
                    newcard = fill_card_info()
                    newcard.create_card()
                    common.show_message("发卡成功!", "NOTICE")

                # 冻结信用卡
                if _choose == "5":
                    cardno = common.input_msg("输入卡号:")
                    card = CreditCard(cardno)
                    if not card.card_is_exists:
                        common.show_message("卡号不存在", "ERROR")
                    else:
                        # 调用模板显示卡信息
                        common.show_message(template.card_info.format(cardno=card.cardno,
                                                                      owner=card.owner,
                                                                      total=card.credit_total,
                                                                      balance=card.credit_balance,
                                                                      status="正常" if card.frozenstatus == 0 else "冻结"
                                                                      ), "INFORMATION")
                        confirm = common.input_msg("确认要冻结此卡吗(y/n)?", ("y", "n"))
                        if confirm == "y":
                            card.frozenstatus = 1
                            card.update_card()
                            common.show_message("此卡已冻结!", "NOTICE")
                # 退出
                if _choose == "0":
                    quit_flag = True
        else:
            # 不是 admin 角色无权限
            common.show_message("权限不够!", "ERROR")
    else:
        common.show_message("请先登录系统!", "NOTICE")
        userobj.login()


if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    weekoftoday = date.weekday(datetime.now())
    curruser = Users()

    # 初始化对账单
    report.create_statement_main()

    # --------    开始主程序   -------------------
    exitflag = False
    while not exitflag:
        # 如果用户登录了，显示登录的界面; 未登录显示未登录的界面
        if not curruser.islogin:
            print(template.index_default_menu.format("", today, common.numtochr(weekoftoday)))
        else:
            print(template.index_logined_menu.format("欢迎您: {0}".format(curruser.name), today,
                                                     common.numtochr(weekoftoday)))

        choose = common.input_msg("选择功能编号[1-5]: ", ("1", "2", "3", "4", "5")).strip()
        if choose == "5":
            exitflag = True
            continue

        # 1 购物商城
        if choose == "1":
            curruser.db_load()
            doshopping(curruser)

        # 2 用户登录
        if choose == "2":
            curruser.db_load()
            user_login(curruser, today, weekoftoday)

        # 3 信用卡管理
        if choose == "3":
            card_center(curruser)

        # 4 后台管理
        if choose == "4":
            manager(curruser)
