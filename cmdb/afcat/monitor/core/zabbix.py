#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun 
@date 16/9/1
"""

import datetime
from urllib.request import build_opener, HTTPCookieProcessor, HTTPError, Request
from urllib.parse import urlencode


class API(object):
    def __init__(self, url, name, password):
        self.url = url
        self.name = name
        self.password = password
        url_opener = build_opener(HTTPCookieProcessor())
        params = {"name": self.name, 'password': self.password, 'autologin': 1, "enter": 'Sign in'}
        encode_data = urlencode(params)
        request = Request(url, bytes(encode_data, "utf-8"))
        for i in dir(request):
            if hasattr(request, i):
                print(i)
                print(getattr(request, i))
        try:
            response = url_opener.open(request, timeout=10)
            print(response)
            print(response.__dict__.get('headers'))
            print(response.getheaders())
            print(dir(response))
            for i in dir(response):
                print(i)
                print(getattr(response, i))
            self.url_opener = url_opener
            # print(dir(self.url_opener))

        except HTTPError as e:
            print(e)

    def get_graph(self, url, params, image_dir):
        if params.get("graphid", None) is None:
            exit(1)
        if params.get("period", None) is None:
            params["period"] = 86400
        if params.get('stime', None) is None:
            params["stime"] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if params.get("width", None) is None:
            params["width"] = 800
        if params.get("height", None) is None:
            params["height"] = 200
        encode_data = urlencode(params)
        request = Request(url, bytes(encode_data, "utf-8"))
        # print(dir(request))
        # for i in dir(request):
        #     if hasattr(request, i):
        #         func = getattr(request, i)
        #         if hasattr(func, "__call__"):
        #             try:
        #                 print(func())
        #             except Exception as e:
        #                 print(e)
        #         else:
        #             print(getattr(request, i))
        url = self.url_opener.open(request)
        image = url.read()
        image_name = "%s/%s.html" % (image_dir, params["graphid"])
        f = open(image_name, 'wb')
        f.write(image)


# graph_url = "http://192.168.101.251/zabbix/tr_events.php?triggerid=13560&eventid=155"
# login_url = "http://192.168.101.251/zabbix/index.php"
# username = "Admin"
# password = "zabbix"
# save_dir = "/Users/zengchunyun/tmp"
# data = {"graphid": "tr_events", "period": 86400, "stime": 2016090100000, "width": 900, "height": 200}
# auth = API(login_url, username, password)
# auth.get_graph(graph_url, data, save_dir)
# print(auth)