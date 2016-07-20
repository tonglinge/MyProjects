# coding:utf-8

from datetime import datetime, timedelta
import sys, os
import ModelClass
import urllib2, urllib
import json


def BytetoMb(bytevalue):
    return bytevalue / 1024 / 1024


def WriteLog(Msg, FileType):
    """
    写日志文件
    :param Msg: log message
    :param FileType: Filetype：Error , Info
    :return:
    """
    LogPath = os.path.dirname(os.path.abspath(__file__)) + "/logs/"
    LogFile = LogPath + FileType + ".log"
    with open(LogFile, "a+") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + Msg + "\n")


def GetConfigPara(GetConfigurl):
    """
    从服务器获取监控配置信息，监控模块:执行频率(单位分钟）
    :return:字典配置文件  {"Load_CPU_Info":2,"Load_DISK_Info":10,"Load_MEMORY_Info":5}
    """
    ConfigParameters = {}
    try:
        html = urllib2.urlopen(GetConfigurl)
        result = html.read()
        ConfigParameters = json.loads(result)
        # ConfigParameters = {"Load_CPU_Info":2,"Load_DISK_Info":10,"Load_MEMORY_Info":5}

    except Exception, e:
        WriteLog('[exception]function GetConfigPara : ' + e.message, 'Error')
    return ConfigParameters


def FormatModelExecTime(currtime, configpara):
    """
    将配置信息中的模块执行频率值转换为执行的时间
    :param currtime: 当前时间:datatime.now()
    :param configpara: 服务器配置信息，字典表
    :return: 各模块执行时间，返回字典，如{"Load_CPU_Info":"10:05:00"}
    """
    result = {}
    strtimes = currtime.strftime("%H:%M:%S")
    strtime_min = strtimes.split(":")[1]
    strtime_sec = strtimes.split(":")[2]
    for model in configpara.keys():
        interval = int(configpara[model])  # 获取模块的执行频率
        intsec = (int(strtime_min) % interval) * 60 + int(strtime_sec)  # 获得取整的秒数
        next_execute_sec = interval * 60 - intsec  # 根据执行频率获取下一次执行的时间间隔
        next_execute_time = currtime + timedelta(seconds=next_execute_sec)
        result[model] = next_execute_time.strftime("%Y-%m-%d %H:%M:%S")
    return result



def CommitResultToServer(result, postdataurl):
    # WriteLog(result, "Info")
    try:
        commitdata = urllib.urlencode(json.loads(result))
        url = urllib2.urlopen(postdataurl, commitdata).read()
        if url == "ok":
            pass
        else:
            WriteLog(result, 'Error')
            # return True
    except Exception, e:
        WriteLog(e.message, "Error")
        # pass


def ExecuteModel(modelname, ipaddr, CheckTime):
    """
    通过反射调用ModelClass模块下的对应监控模块，并返回执行结果
    :param modelname: 要执行的模块名称
    :param ipaddr: 参数IP地址
    :return: 返回json序列化的结果
    """
    try:
        FuncObj = getattr(ModelClass, modelname)
        Result = FuncObj(ipaddr, CheckTime)  # 执行的结果
        return Result

    except Exception, e:
        WriteLog(e.message, "Error")
