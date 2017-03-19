#! /usr/bin/env python
# encoding: utf8


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
        'category': 'info',
        'info': '',
        'has_next': False,
        'has_previous': False,
    }
    return format_data
