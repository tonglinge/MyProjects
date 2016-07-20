# coding:utf-8
from django.db import models

# Create your models here.

#主机组名信息表
class HostGroups(models.Model):
    GroupName = models.CharField(max_length=50,null=False)

#服务器主机信息表
class Host(models.Model):
    HostName = models.CharField(max_length=30,null=False)
    HostNetIpAddr = models.CharField(max_length=15)
    HostPriIpAddr = models.CharField(max_length=15)
    CpuCount = models.IntegerField(null=True)
    DiskCount = models.IntegerField(null=True)
    OSType = models.CharField(max_length=10,null=True)
    OSVerision = models.CharField(max_length=10,null=True)
    Producter = models.CharField(max_length=20,null=True)
    HostGroup = models.ForeignKey(HostGroups)


#监控模块名称表
class MonitorModels(models.Model):
    MonitorName = models.CharField(max_length=50,null=False)
    ModelPlubName = models.CharField(max_length=50, null=False)
    ModelName = models.CharField(max_length=50)

#主机及主机组关系表
'''
class Host_Group_Relation(models.Model):
    Gid = models.ForeignKey(HostGroups)
    Hid = models.ForeignKey(Host)
'''

#主机组及监控模块关系表
class Model_Group_Relation(models.Model):
    Gid = models.ForeignKey(HostGroups)
    Mid = models.ForeignKey(MonitorModels)
    Interval = models.IntegerField(null=False)

#用户组
class UserGroup(models.Model):
    GroupName = models.CharField(max_length=50)

#用户表
class Users(models.Model):
    Username = models.CharField(max_length=20,null=False)
    Password = models.CharField(max_length=50,null=False)
    Name = models.CharField(max_length=20)
    UserGroupID = models.ForeignKey(UserGroup)
    Email = models.EmailField()
    Tel = models.IntegerField()
    Mobile = models.IntegerField()

#用户组管理主机组对应关系表
class UserGroup_HostGroup_Relation(models.Model):
    UserGroupID = models.ForeignKey(UserGroup)
    HostGroupID = models.ForeignKey(HostGroups)


#主机监控项，包括CPU ,DISK,MEMORY,SWAP
# CPU:
class Host_CPU(models.Model):
    Hosts = models.ForeignKey(Host)
    CheckTime = models.DateTimeField()
    CPU_Idle = models.FloatField()
    CPU_User = models.FloatField()
    CPU_Sys = models.FloatField()

# DISK
class Host_Disk(models.Model):
    Hosts = models.ForeignKey(Host)
    CheckTime = models.DateTimeField()
    DISK_Mountpoint = models.CharField(max_length=50)
    DISK_TotalSize = models.FloatField()
    DISK_Used = models.FloatField()
    DISK_Free = models.FloatField()
    DISK_Precent = models.FloatField()

# Memory
class Host_Memory(models.Model):
    Hosts = models.ForeignKey(Host)
    CheckTime = models.DateTimeField()
    Mem_TotalSize = models.FloatField()
    Mem_Used = models.FloatField()
    Mem_Free = models.FloatField()
    Mem_Precent = models.FloatField()

# Swap
class Host_Swap(models.Model):
    Hosts = models.ForeignKey(Host)
    CheckTime = models.DateTimeField()
    Swap_TotalSize = models.FloatField()
    Swap_Used = models.FloatField()
    Swap_Free = models.FloatField()
    Swap_Precent = models.FloatField()








