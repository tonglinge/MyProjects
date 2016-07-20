# coding:utf-8
from django.http.request import HttpRequest
from django.http.response import HttpResponse
import models
import json
from Common import common, monitor


# 客户端获取参数模块
def GetParaService(request, ipaddrs):
    result = {}
    ipaddrstr = ipaddrs
    host = models.Host.objects.get(HostNetIpAddr=ipaddrstr)  # 根据IP获取服务器信息
    # group = models.Host_Group_Relation.objects.get(Hid = host)
    model_id_list = models.Model_Group_Relation.objects.filter(Gid_id=host.HostGroup_id)
    if model_id_list.count() > 0:
        for model_id in model_id_list:
            interval = model_id.Interval
            modelname = models.MonitorModels.objects.get(id=model_id.Mid_id)
            result[modelname.ModelName] = interval
    return HttpResponse(json.dumps(result))


def ReceiveClientData(request):
    modelname = request.POST.get("modelname")
    ipaddr = request.POST.get("host_ipaddr")
    try:
        hostmodel = models.Host.objects.get(HostNetIpAddr=ipaddr)
        if hostmodel is not None:  # 找到记录
            if modelname == "Model_CPU":
                monitor.SaveCpudata(request, hostmodel)  # CPU模块数据保存
            if modelname == "Model_DISK":
                monitor.SaveDiskdata(request, hostmodel)  # DISK模块数据保存
            if modelname == "Model_MEMORY":
                monitor.SaveMemoryData(request, hostmodel)  # Memory模块数据保存

            return HttpResponse("ok")
        else:  # 未找到记录
            common.WriteLog(modelname + " not found hosts for ip " + ipaddr)
    except Exception, e:
        common.WriteLog(e.message)
