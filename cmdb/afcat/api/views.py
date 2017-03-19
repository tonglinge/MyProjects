#! /usr/bin/env python
# encoding: utf8
from django.shortcuts import render
from django.http import JsonResponse

from afcat.api.libs.public import APIView, Logger, api
logger = Logger(__name__)


class API(APIView):

    def get(self, request, *args, **kwargs):
        logger.info(request=request)
        get_api = kwargs.get('api', None)
        if get_api:
            api_ret = api(request, *args, **kwargs)
            if type(api_ret) == dict:
                self.ret.update(api_ret)
            else:
                self.ret['data'] = []
        else:
            self.ret['info'] = "未获取到对应的API处理方法！！"
            self.ret['category'] = "error"
            logger.warning(self.ret, request)
        return JsonResponse(self.ret)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


def bad_request_view(request):
    logger.warning(message="bad_request", request=request)
    return render(request, '400.html')


def permission_denied_view(request):
    logger.warning(message="permission_denied", request=request)
    return render(request, '403.html')


def page_not_found_view(request):
    logger.warning(message="page_not_found", request=request)
    return render(request, '404.html')


def error_view(request):
    logger.error(message="error_request", request=request)
    return render(request, '500.html')
