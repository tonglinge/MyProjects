from plugins import plugin_api
import json,platform,sys


class InfoCollection(object):
    """
    收集服务器资源信息类
    """
    def __init__(self):
        pass

    def get_platform(self):
        """
        获取当前服务器操作系统类型
        :return:
        """
        os_platform = platform.system()
        return os_platform

    def collect(self):
        """
        开始获取服务器资源信息
        :return:
        """
        os_platform = self.get_platform()
        try:
            # 调用类中对应操作系统的资源收集方法
            func = getattr(self, os_platform)
            info_data = func()   # 收集信息
            formatted_data = self.build_report_data(info_data)
            return formatted_data
        except AttributeError as e:
            sys.exit("Error:MadKing doens't support os [%s]! " % os_platform)

    def Linux(self):
        sys_info = plugin_api.LinuxSysInfo()
        return sys_info

    def Windows(self):
        sys_info = plugin_api.WindowsSysInfo()
        #print(sys_info)
        return sys_info

    def build_report_data(self, data):
        #add token info in here before send
        return data
