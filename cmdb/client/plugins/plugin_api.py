from .linux import sysinfo


def LinuxSysInfo():
    return sysinfo.collect()

def WindowsSysInfo():
    from .windows import sysinfo as win_sysinfo
    return win_sysinfo.collect()
