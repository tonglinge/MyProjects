#! /usr/bin/env python
# encoding: utf8


from django.conf.urls import url
from afcat.api import views as api_views
from afcat.api import cmdb_views

urlpatterns = [
    url(r'^afcat/$', api_views.API.as_view()),
    url(r'^cmdb/$', cmdb_views.AdminIndex.as_view()),
    url(r'', view=api_views.page_not_found_view),

    # url(r'^cmdb/report/index/$', cmdb_views.SysConfig.as_view())
]
