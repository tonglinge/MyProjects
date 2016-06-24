#!/usr/bin/env python
from django import template
from django.conf import settings
from django.utils.html import format_html


register = template.Library()

@register.simple_tag
def website_title():
    return settings.WEBSITE_TITLE


def split_page(result_obj):
    """
    分页模块，后台传入一个分页结果集就可以
    :param result_obj:
    :return:
    """
    return_str = "<nav>"
    return_str += "<ul class='pagination  pull-right'>"
    if result_obj.has_previous():
        return_str += "<li>"
        return_str += "<a href='?page=" + str(result_obj.previous_page_number()) + "' aria-label='Previous'>"
        return_str += "<span aria-hidden='true'>&laquo;</span>"
        return_str += "</a></li>"

    for i in result_obj.paginator.page_range:
        # print(i,result_obj.paginator.page_range,result_obj.number)
        hide_page_num = abs(result_obj.number - i)
        if hide_page_num <= 3:  # 3为当前页前后显示多少个
            return_str += "<li "
            if i == result_obj.number:
                return_str += "class='active'><a href='?page=" + str(i) + "'>" + str(i) + "</a></li>"
            else:
                return_str += "><a href='?page=" + str(i) + "'>" + str(i) + "</a></li>"

    if result_obj.has_next():
        return_str += "<li><a href='?page=" + str(result_obj.next_page_number()) + "' aria-label='Next'>"
        return_str += "<span aria-hidden='true'>&raquo;</span></a></li></ul></nav>"

    #return format_html(return_str)
    return return_str


@register.simple_tag
def test(string):
    return string
