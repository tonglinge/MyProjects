#! /usr/bin/env python
# encoding: utf8
from afcat.api.libs.public import Logger, BaseHandler, api
from django.contrib.auth.models import User
logger = Logger(__name__)

__all__ = ['api','Show', 'Host', 'Groups', 'Change']


# def api(request, *args, **kwargs):
#     ret = response_format()
#     method = request.GET.get("method", None) if request.method == 'GET' else request.POST.get('method', None)
#     if method is not None:
#         method = str(method).split(".")
#         handler = method[0].title()
#         if handler in __all__:
#             handler = globals().get(handler, None)
#             if handler is not None:
#                 try:
#                     request_handler = handler(request=request, method=method, *args, **kwargs)
#                     return request_handler.execute()
#                 except Exception as e:
#                     ret['info'] = ' 内部请求错误'
#                     ret['category'] = 'error'
#                     logger.error(e, request)
#         else:
#             ret['info'] = '请求非法'
#             ret['category'] = 'error'
#             logger.error("method: %s not implemented" % handler, request=request)
#     else:
#         ret['info'] = '请求方法不正确，格式{method: "方法.行为"}'
#         ret['category'] = 'error'
#         logger.warning(ret, request)
#     return ret


class Change(BaseHandler):

    def __init__(self, method=None, request=None, *args, **kwargs):
        super(Change, self).__init__(method=method, request=request)
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        logger.info('有新请求')
        if hasattr(self, str(self.method)):
            handler_method = getattr(self, str(self.method))
            handler_method()
        return self.ret

    def password(self):
        password1 = self.request.POST.get('password', None)
        password2 = self.request.POST.get('confirmpassword', None)
        user_id = self.request.POST.get('username', None)
        if password1 and password2 and password1 == password2:
            if user_id is None:
                user_id = self.request.user.id
            get_user = User.objects.filter(id=user_id).all()
            if get_user:
                get_user[0].set_password(password1)
                get_user[0].save()
                self.ret['info'] = '密码修改成功'
            else:
                self.ret['info'] = '用户不存在'
        else:
            self.ret['info'] = '两次输入不一致'
