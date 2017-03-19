#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun
@date 2016/10/10
"""
from afcat import settings
from afcat.account.core.permission import get_user_menus, get_user_managed_customer


def common_processor(request):
    context = dict()
    # 获取用户可以访问的菜单权限
    left_menu_permission = get_user_menus(request.user)
    # 获取用户可以管理的客户信息
    manage_cust_info = get_user_managed_customer(request.user)
    context.update({'main_menu': left_menu_permission, 'manage_cust': manage_cust_info})
    if str(request.path).startswith('/monitor'):
        context.update({
            'monitor_server': settings.MONITOR_SERVER,
            'monitor': 'active',
        })
    if str(request.path).startswith('/cmdb'):
        context.update({
            'monitor_server': settings.MONITOR_SERVER,
            'cmdb': 'active',
        })
        if str(request.path).startswith('/cmdb/sysconfig') or str(request.path).startswith('/cmdb/sysconfig_import'):
            context.update({
                'sysconfig': 'active',
            })
        if str(request.path).startswith('/cmdb/cmdb_ipconfig'):
            context.update({
                'ipconfig': 'active',
            })

    if str(request.path).startswith('/account'):
        context.update({
            'monitor_server': settings.MONITOR_SERVER,
            'account': 'active',
        })
    if str(request.path).startswith('/tracker'):
        context.update({
            'monitor_server': settings.MONITOR_SERVER,
            'tracker': 'active',
        })
        if str(request.path).startswith('/tracker/management'):
            context.update({
                'tracker_management': 'active',
            })
    return context

