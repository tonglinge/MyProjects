# coding:utf-8

from django.db import models
from django.shortcuts import render_to_response
import Web.models
import Common.common


def CheckLogin(request, user, pwd):
    # Common.common.WriteLog("CheckLogin Function begin" )
    try:
        usermodle = Web.models.Users.objects.filter(Username=user, Password=pwd)
        # Common.common.WriteLog("CheckLogin Function count=" + str(count))
        if usermodle.count() > 0:
            request.session["user_id"] = usermodle[0].id
            request.session["user_name"] = usermodle[0].Name
            return "1"
        else:
            return "0"
    except Exception, e:
        Common.common.WriteLog(e.message)


# 获取所有主机信息列表
def GetHostListAll(PageNum, PageperCount):
    """
    获取主机列表，返回主机列表对象
    :param PageNum: 当前页数，默认为1
    :param PageperCount: 每页显示记录数
    :return:
    """
    RecordStart = (int(PageNum) - 1) * int(PageperCount)
    RecordEnd = int(PageNum) * int(PageperCount)
    HostList = Web.models.Host.objects.all()[RecordStart:RecordEnd]
    return HostList


# 根据主机ID号获取主机实例
def GetHostByID(hid):
    HostGroupList = Web.models.HostGroups.objects.all()
    HostModel = Web.models.Host.objects.get(id=hid)
    return (HostModel, HostGroupList)


def login_auth(func):
    """
    登陆验证装饰器，所有非登陆模块均需要引用
    :param func: 加载装饰器的函数
    :return: 返回函数执行结果
    """
    def warper(request):
        if request.session.get("user_id", None) is not None:
            response = func(request)
        else:
            return render_to_response("Login.html")
        return response
    return warper
