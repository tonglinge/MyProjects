"""afcat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from afcat.tracker import views as tracker_views
from afcat.cmdb import views as cmdb_views

urlpatterns = [
    # url(r'^$', tracker_views.Index.as_view()),
    url(r'^$', cmdb_views.Index.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('afcat.account.urls')),
    url(r'^api/v1/', include('afcat.api.urls')),
    url(r'^tracker/', include('afcat.tracker.urls')),
    url(r'^monitor/', include('afcat.monitor.urls')),
    url(r'^cmdb/', include('afcat.cmdb.urls')),
    # url(r'^sysconfig/dbmanage/', cmdb_views.db_backup_manage, name='cmdb_sysconfig_dbmanage'),
]
