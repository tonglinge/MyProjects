#!/usr/bin/env python

from afcat.cmdb.libs.common import page_split, writelog, create_assno
from afcat.account.models import Account
from afcat.cmdb.models import BaseCustomerInfo
from datetime import datetime
from afcat.api.libs.public import response_format
from django.contrib.auth.models import User, Group


def load_user_list():
    """
    显示所有账户
    :param curr_page:当前页码
    :return: 所有用户的详细信息
    """
    return_data = []
    result = response_format()
    try:
        account_user = Account.objects.all()

        for user in account_user:
            # print(user, user.username.username, user.username.groups.select_related())
            user_info = dict(id=user.username_id, nickname=user.nickname, avatar=str(user.avatar),
                             username=user.username.username,
                             email=user.username.email,
                             groupname=user.username.groups.select_related()[0].name if user.username.groups else "",
                             is_superuser=user.username.is_superuser, is_active=user.username.is_active,
                             cust_id=user.cust_id,
                             usercust=",".join([obj.get('custalias') for obj in
                                 BaseCustomerInfo.objects.filter(idcode__in=user.cust_id.split(',')).values("custalias")]),
                             last_login=datetime.strftime(user.username.last_login,
                                                          "%Y-%m-%d %H:%M") if user.username.last_login else "",
                             date_joined=datetime.strftime(user.username.date_joined,
                                                           "%Y-%m-%d") if user.username.date_joined else "",
                             )
            return_data.append(user_info)
        result["data"] = return_data
    except AttributeError as e:
        writelog("[account.auth_user.load_user_list] {0}".format(str(e)))
        result["status"] = False
        result["category"] = "error"
        result["info"] = "未获取用户信息"
    return result


def user_modify(request_data):
    """
    用户管理操作，包括添加、修改、删除
    :param request_data: {'avatar': '1.jpg', 'last_login': '2016-10-28', 'date_joined': '2016-10-08', 'username': 'monitor',
                        'nickname': 'wangsong', 'is_active': True, 'is_superuser': False}
    :return:
    """
    action = request_data.get("action")
    if action == "add":
        result = add_user(request_data)
    if action == "change":
        result = change_user(request_data)
    if action == "delete":
        result = delete_user(request_data.get("id"))
    if action == "resetpass":
        uid = request_data.get("id")
        password = request_data.get("new_pass")
        result = reset_password(uid, password)
    return result


def add_user(request_data):
    """
    创建新用户
    :param request_data: 提交数据
    :return:
    """
    result = response_format()
    username = request_data.get("username")
    password = request_data.get("password")
    is_superuser = int(request_data.get("is_superuser"))
    is_active = int(request_data.get("is_active"))
    user_group_id = int(request_data.get("groups"))
    nickname = request_data.get("nickname")
    head_img = request_data.get("navatar")[1:-1]
    email = request_data.get("email")
    cust_id = request_data.get("cust_id")
    try:
        # 判断用户是否存在
        chk_user = User.objects.filter(username=username)
        if chk_user.count() > 0:
            result["info"] = "用户已经存在"
            result["category"] = "error"
            return result

        # 创建user
        auth_user = User.objects.create_user(username=username,
                                             password=password,
                                             is_superuser=is_superuser,
                                             is_active=is_active,
                                             email=email
                                             )
        User.objects.select_for_update()
        # 分配组
        g = Group.objects.get(id=user_group_id)
        auth_user.groups.add(g)

        # 创建account
        if cust_id.split(",").count('0') > 0:
            cust_id_list = cust_id.split(',')
            cust_id_list.remove('0')
            cust_id = ",".join(cust_id_list)
        Account.objects.create(username=auth_user,
                               nickname=nickname,
                               avatar=head_img if head_img else "default.jpg",
                               cust_id=cust_id)

        result["info"] = "添加成功"
        result["category"] = "success"

    except Exception as e:
        writelog("[account.auth_user.add_user] {0}".format(str(e)))
        result["category"] = "error"
        result["info"] = "添加失败"
    return result


def delete_user(uid):
    """
    删除用户信息
    :param uid:auth_user中的user ID
    :return:
    """
    result = response_format()
    try:
        user_obj = User.objects.get(id=int(uid))
        user_obj.delete()
        result["info"] = "删除成功!"
        result["category"] = "success"
    except Exception as e:
        writelog("[account.auth_user.delete_user] {0}".format(str(e)))
        result["category"] = "error"
        result["info"] = "删除失败!"
    return result


def change_user(request_data):
    """
    修改联系人信息
    :param request_data:
    :return:
    """
    result = response_format()
    print("change_user:", request_data)
    try:
        username = request_data.get("username", "")
        nickname = request_data.get("nickname", "")
        groupid = request_data.get("groups")
        email = request_data.get("email")
        active = request_data.get("is_active")
        superuser = request_data.get("is_superuser")
        headimg = request_data.get("navatar", "")
        custid = request_data.get("cust_id")

        user_obj = User.objects.get(username=username)
        # 更新组
        user_obj.groups.clear()
        user_obj.groups.add(Group.objects.get(id=int(groupid)))
        # 更新auth用户信息
        user_obj.email = email
        user_obj.is_active = int(active)
        user_obj.is_superuser = int(superuser)
        user_obj.save()
        # 更新account用户信息
        user_obj.account.nickname = nickname
        user_obj.account.cust_id = custid
        if headimg:
            user_obj.account.avatar = headimg
        user_obj.account.save()

        result["info"] = "更新成功!"
        result["category"] = "success"
    except Exception as e:
        writelog("[account.auth_user.change_user] {0}".format(str(e)))
        result["info"] = "更新失败!"
        result["category"] = "error"
    return result


def reset_password(uid, new_password):
    """
    重置密码
    :param uid: 用户ID
    :param new_password: 新密码
    :return:
    """
    result = response_format()
    try:
        change_user = User.objects.get(id=int(uid))
        print(change_user, new_password)
        change_user.set_password(new_password)
        change_user.save()
        result["info"] = "密码重置成功!"
        result["category"] = "success"
    except Exception as e:
        writelog("[account.auth_user.reset_password] {0}".format(str(e)))
        result["category"] = "error"
        result["info"] = "更新失败!"
    return result

