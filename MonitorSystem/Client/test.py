# coding:utf-8

# 'from datetime import date, time, datetime, timedelta'
def outer(func):
    def warper():
        print("hello warper")
        func()
        #return result
    return warper


@outer
def fun_1():
    print("functions")

fun_1()