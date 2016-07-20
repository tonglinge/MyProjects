# -*- coding:utf-8 -*-

"""
这个文件可以用来作为html模板文件的函数集合文件，在这里面定义的函数可以直接在html模板中调用，必须满足以下几点：
1 文件所在目录路径必须在应用目录下(如Web下)
2 目录文件名必须为： templatetags
3 需要在html模板中应用的函数名必须加上 @注册变量名.simple_tag属性(如：@register.simple_tag)
4 在模板中应用文件 {% load 文件名  %}
5 模板调用 {% function args %}
"""

from django import template

register = template.Library()


@register.simple_tag
def page_function_test(args):
    msg = 'templates tags function: ' + __func(args)
    return msg


def __func(arg):
    msg = arg + " haha"
    return msg
