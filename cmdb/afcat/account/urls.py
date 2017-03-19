#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun 
@date 16/8/25
"""

from django.conf.urls import url
from afcat.account import views

urlpatterns = [
    url(r'^login/', views.account_login, name='login'),
    url(r'^logout/', views.account_logout, name='logout'),
    url(r'^user_management/', views.user_management, name='user_management'),
    url(r'^upfile/', views.up_file, name='user_upfile'),
    url(r'^load_groups/', views.load_perm_groups, name='load_group'),
    url(r'^load_custs/', views.load_custs, name='load_custs'),
    url(r'^group_management/', views.group_management, name='group_management'),
    url(r'^group_modify', views.group_modify, name='group_modify'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'profile_edit/', views.profile_edit, name='profile_edit')
]
