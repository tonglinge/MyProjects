import json
from django.shortcuts import HttpResponse
from afcat.api.libs.public import APIView, Logger, response_format
logger = Logger(__name__)
# Create your views here.


class TrackerIndex(APIView):

    def get(self, request, *args, **kwargs):
        ret = response_format()
        get_api = kwargs.get('api', None)
        if get_api:
            api_ret = get_api.api(request, *args, **kwargs)
            if type(api_ret) == dict:
                ret.update(api_ret)
            else:
                ret['data'] = []
        else:
            ret['info'] = "请求非法！"
            ret['category'] = "error"
            logger.warning(ret, request)
        return HttpResponse(json.dumps(ret))


class TrackerApplication(APIView):

    def get(self, request, *args, **kwargs):
        ret = response_format()
        get_api = kwargs.get('api', None)
        if get_api:
            api_ret = get_api.api(request, *args, **kwargs)
            if type(api_ret) == dict:
                ret.update(api_ret)
            else:
                ret['data'] = []
        else:
            ret['info'] = "请求非法！"
            ret['category'] = "error"
            logger.warning(ret, request)
        return HttpResponse(json.dumps(ret))


class TrackerNetwork(APIView):
    def get(self, request, *args, **kwargs):
        ret = response_format()
        get_api = kwargs.get('api', None)
        if get_api:
            api_ret = get_api.api(request, *args, **kwargs)
            if type(api_ret) == dict:
                ret.update(api_ret)
            else:
                ret['data'] = []
        else:
            ret['info'] = "请求非法！"
            ret['category'] = "error"
            logger.warning(ret, request)
        return HttpResponse(json.dumps(ret))


class TrackerEvents(APIView):

    def get(self, request, *args, **kwargs):
        ret = response_format()
        get_api = kwargs.get('api', None)
        if get_api:
            api_ret = get_api.api(request, *args, **kwargs)
            if type(api_ret) == dict:
                ret.update(api_ret)
            else:
                ret['data'] = []
        else:
            ret['info'] = "请求非法！"
            ret['category'] = "error"
            logger.warning(ret, request)
        return HttpResponse(json.dumps(ret))


class TrackerHost(APIView):

    def get(self, request, *args, **kwargs):
        ret = response_format()
        get_api = kwargs.get('api', None)
        if get_api:
            api_ret = get_api.api(request, *args, **kwargs)
            if type(api_ret) == dict:
                ret.update(api_ret)
            else:
                ret['data'] = []
        else:
            ret['info'] = "请求非法！"
            ret['category'] = "error"
            logger.warning(ret, request)
        return HttpResponse(json.dumps(ret))


class TrackerHostConfig(APIView):

    def get(self, request, *args, **kwargs):
        ret = response_format()
        get_api = kwargs.get('api', None)
        if get_api:
            api_ret = get_api.api(request, *args, **kwargs)
            if type(api_ret) == dict:
                ret.update(api_ret)
            else:
                ret['data'] = []
        else:
            ret['info'] = "请求非法！"
            ret['category'] = "error"
            logger.warning(ret, request)
        return HttpResponse(json.dumps(ret))


class TrackerSettings(APIView):

    def get(self, request, *args, **kwargs):
        ret = response_format()
        get_api = kwargs.get('api', None)
        if get_api:
            api_ret = get_api.api(request, *args, **kwargs)
            if type(api_ret) == dict:
                ret.update(api_ret)
            else:
                ret['data'] = []
        else:
            ret['info'] = "请求非法！"
            ret['category'] = "error"
            logger.warning(ret, request)
        return HttpResponse(json.dumps(ret))
