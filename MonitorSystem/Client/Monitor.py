# coding:utf-8

from datetime import datetime
from multiprocessing import process
import Common


def doprogress(model, ipaddr, strCurrtime, postdataUrl):
    try:
        result = Common.ExecuteModel(model, ipaddr, strCurrtime)
        Common.CommitResultToServer(result, postdataUrl)
    except Exception, e:
        Common.WriteLog(e.message, "Error")


if __name__ == "__main__":
    ClientIpaddr = "192.168.3.1"
    GetConfigUrl = "http://192.168.3.100/getpara/" + ClientIpaddr + "/"
    Post_data_Url = "http://192.168.3.100/postdata/"
    try:
        # 获取服务器参数配置,配置中的模块执行时间为执行平率，单位分钟
        Config = Common.GetConfigPara(GetConfigUrl)
        if len(Config) > 0:
            Currt_ime = datetime.now()
            # 获取各模块最近一次要执行的具体时间
            ExecuteInfo = Common.FormatModelExecTime(Currt_ime, Config)
            while True:
                Currt_ime = datetime.now()
                strCurrtime = Currt_ime.strftime("%Y-%m-%d %H:%M:%S")
                print(Currt_ime)
                for model in ExecuteInfo.keys():
                    # 如果到了某个模块的执行时间
                    if strCurrtime >= ExecuteInfo[model]:
                        # 获取所有模块的新的执行时间
                        UpdateModelExecTime = Common.FormatModelExecTime(Currt_ime, Config)
                        # '更新字典表中当前模块的执行时间为下次执行时间
                        ExecuteInfo[model] = UpdateModelExecTime[model]
                        try:
                            # doProgress(model,"192.168.1.1",strCurrtime)
                            # 新建子进程执行信息采集
                            p = process.Process(target=doprogress,
                                                args=(model, ClientIpaddr, strCurrtime, Post_data_Url))
                            p.start()
                        except Exception, e:
                            Common.WriteLog(e.message, "Error")
                # 10分钟1次获取服务器监控配置参数，并按新的参数执行
                if (int(Currt_ime.strftime("%M")) % 10) == 0:
                    Config = Common.GetConfigPara(GetConfigUrl)
                    ExecuteInfo = Common.FormatModelExecTime(Currt_ime, Config)
        else:
            Common.WriteLog('get configuration from server failed! load config model para null.', 'error')
    except Exception, e:
        Common.WriteLog(e.message, 'Error')