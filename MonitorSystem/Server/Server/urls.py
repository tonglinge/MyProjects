"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import os
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from Web.service import GetParaService , ReceiveClientData
import Web.Router
import Web.tests

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^img/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.IMG_STATIC_DIRS}),
    #url(r'^css/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.CSS_STATIC_DIRS}),
    #url(r'^java/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.JS_STATIC_DIRS}),
    url(r'^getpara/(?P<ipaddrs>(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}))', GetParaService),
    url(r'^postdata', ReceiveClientData),
    url(r'^test', Web.tests.test_page_function),
    url(r'^(?P<Method>(\w*)$)', Web.Router.Default)

]
