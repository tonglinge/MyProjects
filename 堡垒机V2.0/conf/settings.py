#!/usr/bin/env python

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 数据库连接地址
DBSERVER = "localhost"
PORT = 3306
USER = "python"
PASSWORD = "12345"
PYTHON_API = "pymysql"
DATABASE = "baolei"

# 数据库初始化标识文件
DB_INIT_LCK = os.path.join(BASE_DIR, "conf/.dblck")
# 系统错误日志目录
LOG_FILE = os.path.join(BASE_DIR, "logs/sys.log")
# 密钥存放地址
RSAKEY_PATH = os.path.join(BASE_DIR, "raskey")
