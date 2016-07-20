# coding:utf-8
import psutil
import HostClass


def Load_CPU_Info(ipaddr, CheckTime):
    CpuInfo = HostClass.cpu(ipaddr, CheckTime)
    CheckObj = psutil.cpu_times_percent(3, False)
    CpuInfo.cpu_sys = CheckObj.system
    CpuInfo.cpu_user = CheckObj.user
    CpuInfo.cpu_idle = CheckObj.idle
    return CpuInfo.ReturnJsonData


def Load_DISK_Info(ipaddr, CheckTime):
    DiskInfo = HostClass.disk(ipaddr, CheckTime)
    DiskPartitions = psutil.disk_partitions(all=False)
    for _partition in DiskPartitions:
        if _partition.fstype != "ISO9660" and _partition.opts != "cdrom":
            _PartitionInfo = psutil.disk_usage(_partition.mountpoint)
            DiskInfo.mountpoint = _partition.mountpoint
            DiskInfo.partition_total = _PartitionInfo.total
            DiskInfo.partition_used = _PartitionInfo.used
            DiskInfo.partition_free = _PartitionInfo.free
            DiskInfo.partition_precent = _PartitionInfo.percent
            DiskInfo.AddPartition
    return DiskInfo.ReturnJsonData


def Load_MEMORY_Info(ipaddr, CheckTime):
    MemInfo = HostClass.memory(ipaddr, CheckTime)
    CurrMem = psutil.phymem_usage()
    MemInfo.memory_total = CurrMem.total
    MemInfo.memory_used = CurrMem.used
    MemInfo.memory_free = CurrMem.free
    MemInfo.precent = CurrMem.percent
    return MemInfo.ReturnJsonData


def Load_SWAP_Info(ipaddr, CheckTime):
    SwapInfo = HostClass.swap(ipaddr, CheckTime)
    CurrSwap = psutil.swap_memory()
    SwapInfo.swap_total = CurrSwap.total
    SwapInfo.swap_used = CurrSwap.used
    SwapInfo.swap_free = CurrSwap.free
    SwapInfo.swap_precent = CurrSwap.percent
    return SwapInfo.ReturnJsonData


def execute_task(ipaddr, CheckTime):
    # 1 从服务器获取任务 get_task()
    # 2 查看是否到了要执行任务的时间
    # 3 如果到了就执行 并提交结果 commit_task_result()
    pass
