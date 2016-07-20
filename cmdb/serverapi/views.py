from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .configasset import ConfigAsset
# Create your views here.


@csrf_exempt
def asset_with_id(request):
    """
    客户端提交的数据包含资产ID时走这里,增加、删除或更新资产表
    :param request:
    :return:
    """
    print(request.method)
    if request.method == "POST":
        print("has asset id.....")
        request_data = dict(request.POST)
        # print(request_data)
        config = ConfigAsset(request_data)
        if config.has_error:
            return HttpResponse(json.dumps(config.error_msg))
        config.accept_client_data()
    return HttpResponse(json.dumps("okokok"))


@csrf_exempt
def asset_with_no_id(request):
    """
    当客户端没有获取到自己的资产ID时走这里，先根据提交的sn创建一个资产ID，再提交数据
    :param request:
    :return:
    """
    request_data = dict(request.POST)
    config = ConfigAsset(request_data)
    asset_id = config.insert_new_asset()
    return HttpResponse(json.dumps({'asset_id': asset_id}))
