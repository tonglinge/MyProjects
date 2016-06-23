#!/usr/bin/env python

class MyException(Exception):

    __errcodes = {
        "100": "无异常",
        "102": "未找到该组对应的主机信息",
        "103": "无效的命令",
        "104": "存在未授权的IP地址",
        "105": "存在未授权的组ID",
        "106": "无效的命令参数",
        "107": "源文件不存在",
        "108": "命令语法错误,-u与-d不能同时存在",
        "109": "命令语法错误,未指定文件传送方式(-u/-d)",
        "110": "命令语法错误,必须指定源和目的文件(-s -d)",
    }

    def __init__(self, errcode):
        self._errcode = errcode

    def __str__(self):
        return self.__errcodes[self._errcode]
