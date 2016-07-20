# coding=utf-8
import json
import Common

"""
@主机类
"""


class host(object):
    def __init__(self, ipaddr):
        self.host_ipaddr = ipaddr
        # self.host_name = hostname

    @property
    def ReturnJsonData(self):
        pass


"""
服务器CPU信息子类
 @returnjsondata以json格式返回所有信息
"""


class cpu(host):
    def __init__(self, ipaddr, checktime):
        super(cpu, self).__init__(ipaddr)
        self.model_name = "Model_CPU"
        self.cpu_sys = 0
        self.cpu_user = 0
        self.cpu_idle = 0
        self.check_time = checktime

    @property
    def ReturnJsonData(self):
        """
        返回序列化结果，字典类型：{'model_name':'Model_CPU','host_ipaddr':'192.168.1.10','cpu_sys':23.1}
        """
        dic_cpuinfo = {'modelname': self.model_name, 'checktime': self.check_time, 'host_ipaddr': self.host_ipaddr,
                       'cpu_sys': self.cpu_sys, 'cpu_user': self.cpu_user, 'cpu_idle': self.cpu_idle}
        # dic_cpuinfo['host_name'] = self.host_name

        return json.dumps(dic_cpuinfo)
        # return  dic_cpuinfo


"""
服务器disk类
"""


class disk(host):
    def __init__(self, ipaddr, checktime):
        super(disk, self).__init__(ipaddr)
        self.model_name = "Model_DISK"
        self.checktime = checktime
        self.mountpoint = ''
        self.partition_total = 0
        self.partition_used = 0
        self.partition_free = 0
        self.partition_precent = 0.0
        self.partitions = {}

    @property
    def AddPartition(self):
        """
        将分区信息添加到字典表，组合成一个完成的所有分区的信息表,分区使用信息结果为MB：
        {'/root':{'total':1234,'used':21212,'free':2323,'precent':12.2}}
        """
        self.partitions[self.mountpoint] = {'total': Common.BytetoMb(self.partition_total),
                                            'used': Common.BytetoMb(self.partition_used),
                                            'free': Common.BytetoMb(self.partition_free),
                                            'precent': self.partition_precent}
        return self.partitions

    @property
    def ReturnJsonData(self):
        dic_diskinfo = {'modelname': self.model_name, 'checktime': self.checktime, 'host_ipaddr': self.host_ipaddr,
                        'partitions': self.partitions}
        return json.dumps(dic_diskinfo)


"""
内存类
"""


class memory(host):
    def __init__(self, ipaddr, checktime):
        super(memory, self).__init__(ipaddr)
        self.model_name = "Model_MEMORY"
        self.checktime = checktime
        self.memory_total = 0
        self.memory_used = 0
        self.memory_free = 0
        self.precent = 0.0

    @property
    def ReturnJsonData(self):
        dic_memory = {'modelname': self.model_name, 'checktime': self.checktime, 'host_ipaddr': self.host_ipaddr,
                      'total': Common.BytetoMb(self.memory_total), 'used': Common.BytetoMb(self.memory_used),
                      'free': Common.BytetoMb(self.memory_free), 'precent': self.precent}
        # dic_memory['host_name'] = self.host_name
        return json.dumps(dic_memory)


"""
SWAP类
"""


class swap(host):
    def __init__(self, ipaddr, checktime):
        super(swap, self).__init__(ipaddr)
        self.model_name = "Model_SWAP"
        self.checktime = checktime
        self.swap_total = 0
        self.swap_used = 0
        self.swap_free = 0
        self.swap_precent = 0.0

    @property
    def ReturnJsonData(self):
        dic_swap = {'modelname': self.model_name, 'checktime': self.checktime, 'host_ipaddr': self.host_ipaddr,
                    'total': self.swap_total, 'used': self.swap_used, 'free': self.swap_free,
                    'precent': self.swap_precent}
        # dic_swap['host_name'] = self.host_name
        return json.dumps(dic_swap)
