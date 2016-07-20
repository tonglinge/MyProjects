import datetime
from django.shortcuts import render,render_to_response
from django.http.request import HttpRequest
from django.http.response import HttpResponse,HttpResponseRedirect
from Common import common


def Default(request, Method=None, **kwargs):
    method = Method
    if method == "":
        return HttpResponseRedirect("/Login")
        #return HttpResponseRedirect("404.html")
    else:
        try:
            classobj = __import__('Web.views')
            ViewObj = getattr(classobj,'views')
            FuncObj = getattr(ViewObj, method)
            return FuncObj(request)
        except ImportError, e:
            common.WriteLog("Import Model"+ method + "Error")
        except Exception, e:
            common.WriteLog(e.message)
        return HttpResponseRedirect("/Login")