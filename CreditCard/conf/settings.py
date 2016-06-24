#!/usr/bin/env python

import os
import sys

# 程序文件主目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加环境变量
sys.path.append(BASE_DIR)

# 数据库信息
DATABASE = dict(engineer="file", dbpath=os.path.join(BASE_DIR, "database"), tables={"users": "users",
                                                                                    "shopping": "shoppingmark",
                                                                                    "creditcard": "creditcard"
                                                                                    })

# 日志文件存放路径
LOG_PATH = os.path.join(BASE_DIR, "logs")
# 账单报表文件路径
REPORT_PATH = os.path.join(BASE_DIR, "report")
# 用户登录失败最大次数
ERROR_MAX_COUNT = 3
# 日息费率
EXPIRE_DAY_RATE = 0.0005
# 转账、提现手续费
FETCH_MONEY_RATE = 0.05
# 信用额度
CREDIT_TOTAL = 10000
# 每月账单日期(默认每月22日为账单日)
STATEMENT_DAY = 22
