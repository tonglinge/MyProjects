#!/usr/bin/env python

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 服务端地址
FTP_SERVER_IP = "127.0.0.1"
FTP_SERVER_PORT = 9999
# 文件下载保存路径
DOWNLOAD_FILE_PATH = os.path.join(BASE_DIR, "uploads")

# 日志文件存放路径
LOGS = os.path.join(BASE_DIR, "logs/ftpserver.log")

# 用户信息文件保存路径
USER_INFO = os.path.join(BASE_DIR, "database")

# 用户家目录文件夹
USER_HOME_FOLDER = os.path.join(BASE_DIR, "uploads")

# 客户端家目录最大上传文件大小（默认配置),单位MB
HOME_QUOTA = 500

# 用户断点续传文件保存目录
BREAK_POINT_FOLDER = os.path.join(os.path.join(BASE_DIR, "database"), "breakpoint")
