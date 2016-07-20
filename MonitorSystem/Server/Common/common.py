# coding:utf-8

import os
import hashlib, types
from datetime import date, datetime


def WriteLog(Msg):
    LogPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Logs/"
    LogFile = LogPath + "Error.log"
    with open(LogFile, "a+") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%W") + " " + Msg + "\n")


def GetMd5String(CodeString):
    if type(CodeString) is types.UnicodeType:  # 传入的待加密字符串必须是字符串类型
        x = hashlib.md5()
        x.update(CodeString)
        result = x.hexdigest()

    else:
        result = CodeString
    # WriteLog(result)
    return result
