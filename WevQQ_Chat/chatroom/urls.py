#!/usr/bin/env python

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="chat_main"),
    url(r'^sendmsg/$', views.send_msg, name="send_msg"),
    url(r'^getmsg/$', views.get_msg, name="get_msg"),
    url(r'^friendstat/$', views.updata_status, name="updata_stat"),
    url(r'^fileprocess/$', views.get_upload_size, name="get_filesize"),
    url(r'^loadusers/$', views.load_all_user, name='load_user'),
    url(r'^addfriend/$', views.add_friend, name='add_friend'),
    url(r'^loadmembers/', views.load_group_members, name='load_memebers')
]
