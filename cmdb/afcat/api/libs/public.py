#! /usr/bin/env python
# encoding: utf8

"""
@author: zengchunyun
@date: 2016/12/11
"""

import collections
import importlib
import logging
import sys
from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import resolve_url
from django.utils import six
from django.utils.decorators import available_attrs
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.six.moves.urllib.parse import urlparse
from django.views.generic import View

__all__ = ['api', 'APIView', 'BaseView', 'BaseHandler', 'Logger', 'my_login_required', 'response_format', 'Paginator']


def response_format():
    """
    标准返回响应格式,
    status: 返回的请求状态结果
    data: 将要返回的数据封装到data里
    category: 如果有额外状态信息,需要在此指定信息类型,如error,high, info, debug
    info: 具体的信息存放在此处
    has_next: 对于分页时使用,用于判断是否还有剩余数据未返回
    has_previous: 用于判断是否可以取回上一页数据
    :return:
    """
    format_data = {
        'status': True,
        'data': [],
        'category': 'success',
        'info': '',
        'has_next': False,
        'has_previous': False,
    }
    return format_data


class Logger(object):
    """
    自定义日志记录形式，
    """

    def __init__(self, name=None):
        self.module = name
        self.logger = logging.getLogger(name)

    def format(self, request=None):
        extra = dict(
            method='-'.center(5),
            modules='-'.center(35),
            error_line='-'.center(7),
            user='-'.center(10),
            remote_user_ip='-'.center(15),
            url='-',
            remote_user_agent='-')
        try:
            extra['error_line'] = str(sys.exc_info()[2].tb_lineno).center(7)
        except AttributeError:
            pass
        extra['modules'] = self.module
        if hasattr(request, 'META'):
            extra['url'] = request.get_full_path()
            extra['user'] = str(request.user).center(10)
            extra['method'] = str(request.method).center(5)
            extra['remote_user_ip'] = str(request.META['REMOTE_ADDR']).center(15)
            extra['remote_user_agent'] = request.META['HTTP_USER_AGENT']
        return extra

    def debug(self, message=None, request=None):
        extra = self.format(request)
        self.logger.debug(message, extra=extra)

    def info(self, message=None, request=None):
        extra = self.format(request)
        self.logger.info(message, extra=extra)

    def warning(self, message=None, request=None):
        extra = self.format(request)
        self.logger.warning(message, extra=extra)

    def error(self, message=None, request=None):
        extra = self.format(request)
        self.logger.error(message, extra=extra)

    def critical(self, message=None, request=None):
        extra = self.format(request)
        self.logger.critical(message, extra=extra)


logger = Logger(__name__)


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    用户认证装饰器，认证失败则跳转到登录页面
    :param test_func:
    :param login_url: 登录URL名字
    :param redirect_field_name:
    :return:
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(self, request, *args, **kwargs):
            if test_func(request.user):
                return view_func(self, request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator


def my_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    只针对class view的http method方法使用的装饰器
    :param function:
    :param redirect_field_name:
    :param login_url:
    :return:
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def require_api(view_func):
    """
    规范的api url格式必须是[/api/api版本/app的名字/动作]
    规范的api模块命名必须是[app名字_api]方式命名，
    :param view_func:
    :return:
    """

    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        method = request.GET.get("method", None) if request.method == 'GET' else request.POST.get('method', None)
        request_method = str(method).split('.')
        if len(request_method) >= 2:
            app_name = request_method[0]
            try:
                libs = importlib.import_module("..libs", "afcat.api.libs")
                if hasattr(libs, "%s_api" % app_name):
                    app_api = getattr(libs, "%s_api" % app_name)
                    return view_func(request, api=app_api, method=request_method[1:], *args, **kwargs)
            except ImportError as e:
                logger.error(message=e, request=request)
            render_response = render(request, '500.html')
            render_response.status_code = 500
            logger.error('内部服务错误', request)
        else:
            render_response = render(request, '404.html')
            render_response.status_code = 404
            logger.warning(request=request)
        return render_response

    return _wrapped_view


class BaseView(View):
    """
    所有页面请求必须继承该view
    """

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, **kwargs):
        super(BaseView, self).__init__(**kwargs)
        self.ret = response_format()

    @method_decorator(login_required(login_url="login"))
    def dispatch(self, *args, **kwargs):
        """
        url匹配后，首先通过as_view方法，执行此方法，然后才会匹配http method
        :param args:
        :param kwargs:
        :return:
        """
        return super(BaseView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        pass

    def trace(self, request, *args, **kwargs):
        pass


class APIView(BaseView):
    """
    所有API接口必须继承该api view
    """

    @method_decorator([login_required(login_url='login'), require_api])
    def dispatch(self, *args, **kwargs):
        """
        url匹配后，首先通过as_view方法，执行此方法，然后才会匹配http method
        :param args:
        :param kwargs:
        :return:
        """
        return super(BaseView, self).dispatch(*args, **kwargs)


class BaseHandler(object):
    """所有的api服务必须继承该类"""

    def __init__(self, method=None, request=None):
        """
        self.ret 为api.libs.response 模块下response_format返回结果
        self.method 为请求的具体行为，如show.status,则method就是status
        self.sub_method 为扩展的具体行为，如果没有则为none,如，show.status.user 则self.sub_method就是['user'],切记，该对象为列表

        :param method: 通过API请求参数
        :param request: API请求对象
        """
        self.ret = response_format()
        self.sub_method = None
        if method:
            if len(method) == 2:
                self.method = method[1]
            elif len(method) > 2:
                self.method, self.sub_method = method[1], method[2:]
            else:
                self.method = None
        self.request = request
        self.page = request.GET.get("page", 1)
        self.per_page_count = request.GET.get("per_count", None)

    def execute(self):
        """
        所有继承该类的服务必须实现该方法，并通过该方法返回处理请求,如果有特殊参数传递的，可以重写
        :return:
        """
        try:
            func = getattr(self, str(self.method))
            if func:
                func()
            else:
                self.ret["info"] = "参数错误!"
                self.ret["category"] = "error"
                self.ret["status"] = False
            return self.ret
        except Exception as e:
            logger.error(e)
        # raise NotImplementedError("must be define execute function with subclass")


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class Paginator(object):
    def __init__(self, object_list, per_page=20):
        """

        :param object_list: 分页加载对象
        :param per_page: 每页多少条数据
        """
        self.object_list = object_list
        self.per_page = int(per_page)
        self.current_page = 1

    @staticmethod
    def validate_number(number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        self.current_page = int(number)
        start = (number - 1) * self.per_page
        end = start + self.per_page
        return self._get_page(self.object_list[start:end], number, self)

    @cached_property
    def num_pages(self):
        return self.per_page * self.current_page

    @cached_property
    def begin_pages(self):
        return self.num_pages - self.per_page

    @staticmethod
    def _get_page(*args, **kwargs):
        return Page(*args, **kwargs)


class Page(collections.Sequence):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.paginator.begin_pages, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (slice,) + six.integer_types):
            raise TypeError
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def has_next(self):
        return self.paginator.object_list.has_next

    def has_previous(self):
        return self.number > 1

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)


def api(request, *args, **kwargs):
    """
    api模块必须导入该方法处理API请求
    :param request: request对象
    :param args:
    :param kwargs: 默认包含一个api对象，通过kwargs.get('api')可以获取到对应的API模块
    :return:
    """
    ret = response_format()
    ret['status'] = False
    method = kwargs.pop("method", None)
    if method is not None:
        class_name = method[0].title()
        get_api = kwargs.get('api', None)
        if get_api is not None:
            class_methods = get_api.__all__
            if class_name in class_methods:
                handler = getattr(get_api, class_name, None)
                if handler is not None:
                    try:
                        request_handler = handler(request=request, method=method, *args, **kwargs)
                        return request_handler.execute()
                    except Exception as e:
                        ret['info'] = ' 内部请求错误'
                        ret['category'] = 'error'
                        logger.error(e, request)
            else:
                ret['info'] = 'API没有实现该方法'
                ret['category'] = 'error'
                logger.error("method: %s not implemented" % class_name, request=request)
        else:
            logger.error(message='request api module failed', request=request)
    else:
        ret['info'] = '请求方法不正确，格式{method: "方法.行为"}'
        ret['category'] = 'error'
        logger.warning(ret, request)
    return ret
