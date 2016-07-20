# encoding:utf-8

from Web.models import Host_CPU, Host_Disk, Host_Memory, Host_Swap
from django.http.request import HttpRequest
import json


def SaveCpudata(request, hosts):
    try:
        checktime = request.POST.get("checktime")
        cpu_idle = request.POST.get("cpu_idle")
        cpu_sys = request.POST.get("cpu_sys")
        cpu_user = request.POST.get("cpu_user")
        Host_CPU.objects.create(Hosts=hosts,
                                CheckTime=checktime,
                                CPU_Idle=cpu_idle,
                                CPU_User=cpu_user,
                                CPU_Sys=cpu_sys)
        return True
    except Exception, e:
        return e.message


def SaveDiskdata(request, hosts):
    checktime = request.POST.get("checktime")
    mountlist = request.POST.get("partitions")
    mountlistdic = eval(mountlist)
    for points, values in mountlistdic.items():
        mountpoint = points
        totalsize = values["total"]
        usedsize = values["used"]
        freesize = values["free"]
        precent = values["precent"]
        Host_Disk.objects.create(Hosts=hosts,
                                 CheckTime=checktime,
                                 DISK_Mountpoint=mountpoint,
                                 DISK_TotalSize=totalsize,
                                 DISK_Used=usedsize,
                                 DISK_Free=freesize,
                                 DISK_Precent=precent)
        # Host_Disk.save()


def SaveMemoryData(request, hosts):
    checktime = request.POST.get("checktime")
    mem_total = request.POST.get("total")
    mem_used = request.POST.get("used")
    mem_free = request.POST.get("free")
    mem_precent = request.POST.get("precent")
    Host_Memory.objects.create(Hosts=hosts,
                               CheckTime=checktime,
                               Mem_TotalSize=mem_total,
                               Mem_Used=mem_used,
                               Mem_Free=mem_free,
                               Mem_Precent=mem_precent)
