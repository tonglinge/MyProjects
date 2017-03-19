#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun 
@date 16/8/22
"""

from django.conf.urls import url
from afcat.monitor import views

urlpatterns = [
    url(r'^$', views.index, name='monitor_index'),
    url(r'^host/groups/$', view=views.host_groups, name='host_groups'),
    url(r'^host/groups/(?P<group_id>\d+)', view=views.host_groups_detail, name="host_groups_detail"),
    url(r'^host/(?P<host_id>\d+)/(?P<display_type>\w+)/', views.host_info, name="host_info"),
    url(r'^event/trigger/', view=views.event_trigger, name="event_trigger"),
    url(r'^report/custom/', view=views.report_custom, name="monitor_report_custom"),
    url(r'^report/default/', view=views.report_default, name="monitor_report_default"),
    url(r'^config/host/groups/', view=views.config_host_groups, name="monitor_config_host_groups"),
    url(r'^config/template/', view=views.config_template, name="monitor_config_template"),
    url(r'^config/host/management/', view=views.config_host_management, name="monitor_config_host_management"),
    url(r'^config/host/$', view=views.config_host, name="monitor_config_host"),
    url(r'^config/host/detail/$', view=views.config_host_detail, name="monitor_config_host_detail"),
    url(r'^config/host/add/$', view=views.config_host_add, name="monitor_config_host_add"),
    url(r'^config/host/edit/(P<host_id>\d+)/$', view=views.config_host_edit, name="monitor_config_host_edit"),
    url(r'^config/action/media/', view=views.config_media, name="monitor_config_media"),
    url(r'^config/action/behaviour/', view=views.config_behaviour, name="monitor_config_behaviour"),
    url(r'^lasted/data/', view=views.lasted_data, name="monitor_lasted_data"),
    url(r'^queue/', view=views.queue_status, name="monitor_queue"),
    url(r'^get_host_groups_status/', views.get_host_groups_status, name="get_host_groups_status"),
    url(r'^get_host_graph_detail/', views.host_graph_detail, name="host_graph_detail"),
    url(r'^get_host_groups/', views.get_host_groups, name="get_host_groups"),
    url(r'^get_event_trigger/', views.get_event_trigger, name="get_event_trigger"),
    url(r'^create_new_group/', views.create_new_group, name="create_new_group"),
    url(r'^export_data_to_file/', views.export_data_to_file, name="export_data_to_file"),
]
