from django.contrib import admin

# Register your models here.

from afcat.monitor.models import MonitorGroups, MonitorHostGroups


admin.site.register(MonitorGroups)
admin.site.register(MonitorHostGroups)