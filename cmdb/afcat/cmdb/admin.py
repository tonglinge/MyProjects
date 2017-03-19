from django.contrib import admin
from afcat.cmdb import models
from afcat.cmdb.models import Equipment

# Register your models here.
admin.site.register(models.BaseCustomerInfo)
admin.site.register(models.BaseAssetCabinet)
admin.site.register(models.BaseAssetStatus)
admin.site.register(models.BaseAssetSubtype)
admin.site.register(models.BaseAssetType)
admin.site.register(models.BaseCompany)
admin.site.register(models.BaseFactory)
admin.site.register(models.BaseRole)
admin.site.register(models.BaseDepartment)
admin.site.register(models.BaseSoftType)
admin.site.register(models.BaseSoft)
admin.site.register(models.R_Server_Staff)
admin.site.register(models.Projects)
admin.site.register(models.Business)
admin.site.register(models.Staffs)
admin.site.register(models.Servers)
admin.site.register(models.IPConfiguration)
admin.site.register(models.CpuMemory)
admin.site.register(Equipment)
admin.site.register(models.BaseMachineRoom)
admin.site.register(models.BaseDataCenter)
admin.site.register(models.BaseNetArea)
admin.site.register(models.BaseRaidType)
admin.site.register(models.InstalledSoftList)
admin.site.register(models.SoftLisence)
admin.site.register(models.R_Equipment_Staff)
admin.site.register(models.R_Project_Staff)
admin.site.register(models.BaseEquipmentType)