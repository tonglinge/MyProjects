from django.test import TestCase
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render_to_response

import urllib2,json,urllib
# Create your tests here.

def test(request):
    return HttpResponse("<HTML>Index Page</HTML>")

def CommitResultToServer(request):
    data = {"checktime": "2015-12-09 12:30:00", "modelname": "Model_CPU", "cpu_idle": 42.7, "cpu_user": 42.2, "cpu_sys": 15.2, "host_ipaddr": "192.168.3.1"}
    #result = json.dumps(data)
    commitdata = urllib.urlencode(data)
    url = urllib2.urlopen("http://192.168.3.100/postdata/",commitdata).read()
    if(url == "ok"):
        pass
    else:
       print("No")
     #return True
    #return True


def test_page_function(request):
    return render_to_response("test.html")