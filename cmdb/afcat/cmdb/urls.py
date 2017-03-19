#!/usr/bin/env python
from django.conf.urls import url
from afcat.cmdb import views

urlpatterns = [
    url('^$', views.Index.as_view(), name='cmdb_index'),
    url("^(?P<template_name>\w+)/list/$", views.get_page_templates, name="cmdb_templates"),
    url(r'^admin/index/$', views.AdminIndex.as_view(), name='admin_index'),
    url('^assetinfo/', views.get_asset_list, name='cmdb_asset_list'),
    url('^assetdetail/', views.get_asset_detail, name='cmdb_asset_detail'),
    url('^assetmodify/', views.asset_modify, name='cmdb_assetmodify'),
    url('^eboardcard/', views.post_equipment_boardcard, name='cmdb_equipmentcard'),
    url('^servboardcard/', views.server_boardcard, name='cmdb_servercard'),
    url('^loadportmap', views.get_port_map, name='cmdb_portmap'),
    url('^modifyportmap', views.post_port_map, name='cmdb_port_portmap'),
    url('^vgdetail/', views.get_vg_detail, name='cmdb_host_vgdetail'),
    url('^staffs/', views.staffs_list, name='cmdb_staffslist'),
    url('^basedata/', views.load_base_data, name='cmdb_basedata'),
    url('^relatedasset/', views.post_servers_related_asset, name='cmdb_server_asset'),
    url(r'^sysconfig/dbmanage/', views.db_backup_manage, name='cmdb_sysconfig_dbmanage'),
    url('^exportexcel/', views.report_excel, name='cmdb_export_excel'),
    url('^dataimport/', views.import_excel_data, name='cmdb_import_ddata'),
    url('^downtemplate/', views.down_excel_templates, name='cmdb_down_template'),

]