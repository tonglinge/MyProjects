#!/usr/bin/env python
"""
系统错误代码表
"""
NO_ERROR = 99999               # 系统正常返回
USER_NOT_EXISTS = 10000        # 用户名不存在
CARD_NOT_BINDED = 10001        # 用户未绑定信用卡
BALANCE_NOT_ENOUGHT = 10002    # 信用卡余额不足
CARD_OWNER_ERROR = 10003       # 绑定卡时输入的卡号与卡的所有人不一致
CARD_PASS_ERROR = 10004        # 信用卡密码错误
