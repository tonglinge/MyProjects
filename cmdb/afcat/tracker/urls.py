#! /usr/bin/env python
# encoding: utf8


from django.conf.urls import url
from afcat.tracker import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='tracker_index'),
    url(r'^application/view/$', view=views.ApplicationView.as_view(), name="tracker_application_view"),
    url(r'^application/database/(?P<host_id>\d+)/$', view=views.ApplicationDatabase.as_view(), name="tracker_application_database"),
    url(r'^host/view/$', view=views.HostView.as_view(), name="tracker_host_view"),
    url(r'^host/(?P<host_id>\d+)/detail/$', view=views.HostDetail.as_view(), name="tracker_host_detail"),
    url(r'^host/events/$', view=views.HostEvents.as_view(), name='tracker_host_events'),
    url(r'^network/view/$', view=views.NetworkView.as_view(), name="tracker_network_view"),
    url(r'^network/port/(?P<item_id>\d+)/$', view=views.NetworkPort.as_view(), name="tracker_network_port"),
    url(r'^report/view/$', view=views.ReportView.as_view(), name="tracker_report_view"),
    url(r'^management/groups/$', view=views.ManagementGroups.as_view(), name="tracker_management_groups"),
    url(r'^management/hosts/$', view=views.ManagementHosts.as_view(), name="tracker_management_hosts"),
    url(r'^management/templates/$', view=views.ManagementTemplates.as_view(), name="tracker_management_templates"),
    url(r'^management/settings/$', view=views.ManagementSettings.as_view(), name="tracker_management_settings"),
    url(r'^login/$', view=views.Login.as_view(), name="tracker_login"),
]
