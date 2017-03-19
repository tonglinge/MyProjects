from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from afcat.account.core.auth_group import load_group_all_perms, load_groups, assign_groups_perms, groups_modify
from afcat.account.core.auth_user import load_user_list, user_modify
import json
from afcat.cmdb.libs.common import response_json, response_error, save_file_for_upload
from afcat.cmdb import models
from afcat.api.libs.public import Logger, response_format
logger = Logger(__name__)

# Create your views here.


def profile(request):
    return render(request, 'account/profile.html')


def profile_edit(request):
    return HttpResponse('ed')


def account_login(request):
    if request.method == "GET":
        return render(request, "layout/login.html")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, "account"):
                # default operate cust
                request.session["custid"] = int(str(user.account.cust_id).split(",")[0])
                request.session["custname"] = models.BaseCustomerInfo.objects.filter(
                    idcode=int(str(user.account.cust_id).split(",")[0])).first().custalias
            request.session.clear_expired()
            return redirect(request.GET.get('next') or "/cmdb/")
        else:
            errmsg = u'用户名或密码错误'
            return render(request, "layout/login.html", {"errmsg": errmsg})


def account_logout(request):
    logout(request)
    return redirect(request.GET.get('next') or "/account/login/")


@login_required(login_url="login")
def user_management(request):
    """
    用户管理
    :param request:
    :return:
    """
    if request.method == "GET":
        if request.is_ajax():
            user_list = load_user_list()
            return response_json(user_list)
        else:
            return render(request, 'account/user_management.html')

    if request.method == "POST":
        read_data = request.read()
        post_data = request.POST
        if not read_data:
            post_data = json.loads(post_data).get("data")
        else:
            post_data = json.loads(read_data.decode()).get("data")

        action = post_data.get("action", "")
        if not action:
            return response_error("操作异常!", request)
        else:
            result = user_modify(post_data)
            return response_json(result)


@login_required(login_url="login")
def group_management(request):
    if request.method == "GET":
        request_data = request.GET.get("data", "")
        gid = json.loads(request_data).get("gid", 0) if request_data else 0
        if not gid:
            gid = 0
        groups = load_groups()
        group_perm_list = load_group_all_perms(request.session.get("custid"), int(gid))
        respon_data = {"group_perm": group_perm_list, "groups": groups}
        if request.is_ajax():
            result = response_format()
            result["data"] = respon_data
            return response_json(result)
        else:
            return render(request, 'account/group_management.html', respon_data)

    if request.method == "POST":
        return_result = response_format()
        post_read = request.read()
        post_post = request.POST
        if not post_read:
            post_data = json.loads(post_post).get("data")
        else:
            post_data = json.loads(post_read.decode()).get("data")

        # print(post_data)
        group_id = post_data.get("group_id", 0)
        group_perms = post_data.get("perms", "")
        update_status = assign_groups_perms(group_id, group_perms)

        if not update_status:
            return_result["info"] = "权限更新失败"
            return_result["status"] = False
            return_result["category"] = "error"
        else:
            return_result["category"] = "success"
            return_result["info"] = "权限更新成功"

        return response_json(return_result)


def group_modify(request):
    """
    增加、删除、修改 权限组名
    :param request:
    :return:
    """
    if request.method == "POST":
        read_data = request.read()
        post_data = request.POST
        if not read_data:
            post_data = json.loads(post_data).get("data")
        else:
            post_data = json.loads(read_data.decode()).get("data")

        action = post_data.get("action", "")
        if not action:
            return response_error("操作异常!", request)
        else:
            result = groups_modify(post_data)
            # print("response_result:", result)
            return response_json(result)


def load_perm_groups(request):
    if request.method == "GET":
        result = response_format()
        groups = load_groups()
        result["data"] = groups
        return response_json(result)


def up_file(request):
    from django.conf import settings
    if request.method == "POST":
        file_obj = request.FILES['file']
        save_file_path = settings.BASE_DIR + "/static/img/account/"
        file_name = save_file_for_upload(save_file_path, file_obj)
        return HttpResponse(file_name)


def load_custs(request):
    """
    获取所有的客户信息
    :param request:
    :return:
    """
    if request.method == "GET":
        result = response_format()
        cust_objs = models.BaseCustomerInfo.objects.all().values("idcode", "custalias")
        if cust_objs.count() > 0:
            result["data"] = list(cust_objs)
        return response_json(result)