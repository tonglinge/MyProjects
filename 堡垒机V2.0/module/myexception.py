#!/usr/bin/env python

class MyException(Exception):
    __codelist__ = {
        '100': 'no error',
        '101': "用户名或密码错误",
    }
    
    def __init__(self, errcode):
        self.errcode = errcode
    
    def __str__(self):
        return self.__codelist__[self.errcode]
    