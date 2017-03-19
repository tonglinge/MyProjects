#! /usr/bin/env python
# encoding: utf8
from afcat.api.libs.public import Logger, BaseHandler, response_format
logger = Logger(__name__)

__all__ = ['Show', 'Host', 'Groups']


def api(request, *args, **kwargs):
    ret = response_format()
    method = request.GET.get("method", None)
    if method is not None:
        method = str(method).split(".")
        handler = method[0].title()
        if handler in __all__:
            handler = globals().get(handler, None)
            if handler is not None:
                try:
                    request_handler = handler(request=request, method=method, *args, **kwargs)
                    return request_handler.execute()
                except Exception as e:
                    ret['info'] = ' 内部请求错误'
                    ret['category'] = 'error'
                    logger.error(e, request)
        else:
            ret['info'] = '请求非法'
            ret['category'] = 'error'
            logger.error("method: %s not implemented" % handler, request=request)
    else:
        ret['info'] = '请求方法不正确，格式{method: "方法.行为"}'
        ret['category'] = 'error'
        logger.warning(ret, request)
    return ret


class Show(BaseHandler):

    def __init__(self, method=None, request=None, *args, **kwargs):
        super(Show, self).__init__(method=method, request=request)
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        pass


class Host(BaseHandler):

    def __init__(self, method=None, request=None, *args, **kwargs):
        super(Host, self).__init__(method=method, request=request)
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        pass

    @staticmethod
    def get(host_id):
        host_info = {
            'host_id': host_id,
            'status': '0',
            'available': '0',
            'host_name': 'server',
            'description': 'description description',
            'proxy_hostid': '0'
        }
        return host_info

    def create(self):
        pass

    def delete(self):
        pass


class Groups(BaseHandler):

    def __init__(self, method=None, request=None, *args, **kwargs):
        super(Groups, self).__init__(method=method, request=request)
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        pass

    @staticmethod
    def get(group_id):
        group_info = {
            'group_id': group_id,
            'group_name': "数据库",
            'internal': "0",
        }

        return group_info

    def get_all(self):
        groups_info = []
        for group_id in range(start=10001, stop=10010):
            groups_info.append(self.get(group_id))
        return groups_info
