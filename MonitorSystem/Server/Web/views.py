# coding:utf-8

from django.shortcuts import render, render_to_response
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.backends.db import SessionStore
from Common import common, views, pageclass
from Common.views import login_auth
import Web.models


# 登陆验证模块

def Login(request, **kwargs):
    if request.method == "POST":
        username = request.POST.get('username')
        password = common.GetMd5String(request.POST.get('pwd'))
        check_result = views.CheckLogin(request, username, password)
        if check_result == "1":
            return HttpResponseRedirect("/Index")
        else:
            return render_to_response("Login.html", {"ErrorMessage": "用户名或密码不正确"})
    else:
        return render_to_response("Login.html")


def logout(request):
    if request.method == "GET":
        try:
            del request.session['user_name']
            del request.session['user_id']
        except KeyError, e:
            common.WriteLog(e.message)
        return HttpResponseRedirect("/Login")
    else:
        pass


@login_auth
def Index(request):
    if request.method == "GET":
        try:
            login_name = request.session.get('user_name')
            return render_to_response("index.html", {"LoginName": login_name})
        except Exception, e:
            common.WriteLog(e.message)


# 主机列表信息展示、修改、删除、新增 功能
@login_auth
def Hostlist(request, **kwargs):
    if request.method == "POST":  # 修改或新增时POST方式提交表单
        hid = request.POST.get("hostid", "0")
        hostname = request.POST.get("hostname")
        hostnetipaddr = request.POST.get("netipaddr")
        hostproipaddr = request.POST.get("priipaddr")
        cpucount = request.POST.get("cpucount")
        diskcount = request.POST.get("diskcount")
        ostype = request.POST.get("ostype")
        groups = Web.models.HostGroups.objects.get(id=request.POST.get("groups"))
        if hid == "":  # 无主机ID，认为就是添加新主机
            newhost = Web.models.Host.objects.create(HostName=hostname,
                                                     HostNetIpAddr=hostnetipaddr,
                                                     HostPriIpAddr=hostproipaddr,
                                                     CpuCount=cpucount,
                                                     DiskCount=diskcount,
                                                     OSType=ostype,
                                                     HostGroup=groups)
        else:  # 修改主机信息
            newhost = Web.models.Host.objects.get(id=int(hid))
            newhost.HostName = hostname
            newhost.HostNetIpAddr = hostnetipaddr
            newhost.HostPriIpAddr = hostproipaddr
            newhost.CpuCount = cpucount
            newhost.DiskCount = diskcount
            newhost.OSType = ostype
            newhost.HostGroup = groups
        newhost.save()
        return HttpResponseRedirect("/Hostlist")
    else:  # 显示列表信息，GET方式获取表单
        action = request.GET.get('a', "")
        pagenum = int(request.GET.get('pagenum', "1"))
        reccount = Web.models.Host.objects.count()

    pi = pageclass.PageInfo(reccount, pagenum)
    pi.Count()

    # 提交页面中有a=edit，则修改信息，
    if action == "edit":  # 加载显示修改页面
        hid = request.GET.get("hid")  # 待修改主机ID号
        host_groups = views.GetHostByID(int(hid))
        return render_to_response("Hostedit.html", {"HostModel": host_groups[0], "HostGroupList": host_groups[1]})
    # a=new ,新增记录
    elif action == "new":  # 加载显示新增页面
        host_groups = Web.models.HostGroups.objects.all()
        return render_to_response("Hostedit.html", {"HostGroupList": host_groups})
    elif action == "del":  # 删除记录并返回修改完后的结果集
        hid = request.GET.get("id")
        Web.models.Host.objects.get(id=hid).delete()
        return HttpResponseRedirect("/Hostlist")

    elif action == "":  # 什么参数都没有?那就 是默认的显示全部，
        host_list = views.GetHostListAll(pi.Pagenum, pi.PerCount)
        return render_to_response("Hosts.html", {"Hostlist": host_list, "PageInfo": pi})


@login_auth
def person(request):
    if request.method == "GET":
        try:
            uid = request.session.get('user_id',0)
            user = Web.models.Users.objects.get(id=uid)
            if user is not None:
                return render_to_response("person.html", {'user': user})
            else:
                return render_to_response("person.html")
        except Exception, e:
            common.WriteLog(e.message)
    else:
        try:
            new_password = request.POST.get('newpasswd')
            if new_password == "":
                return HttpResponse("failed")
            else:
                new_passwd_md5 = common.GetMd5String(new_password)
                Web.models.Users.objects.update(Password=new_passwd_md5)
                # Web.models.Users.save()
                return HttpResponse("success")
        except Exception, e:
            common.WriteLog('person model posted modify password failed!' + e.message)
