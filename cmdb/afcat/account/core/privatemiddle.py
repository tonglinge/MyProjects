#!/usr/bin/env python
"""
自定义中间件
"""

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect


class PromissionMiddle(MiddlewareMixin):

    def process_request(self, request):
        if request.path == "/account/login/":
            if not request.user.is_anonymous():
                return HttpResponseRedirect(redirect_to=request.path)
            else:
                pass
        elif request.user.is_anonymous():
            # print("go back to login")
            return HttpResponseRedirect(redirect_to="/account/login/")

