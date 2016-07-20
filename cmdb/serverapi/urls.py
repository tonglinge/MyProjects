#!/usr/bin/env python
from django.conf.urls import url
from django.contrib import admin
from serverapi import views

urlpatterns = [
    url(r'asset_with_no_asset_id/', views.asset_with_no_id),
    url(r'^$', views.asset_with_id)
]