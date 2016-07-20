#!/usr/bin/env python

# 定义目前采集的信息模块
# 在serverapi的 configasset模块的accept_client_data方法中会从以下定义的模块中动态加载采集信息
CollectModule = ['server', 'cpu', 'disk', 'nic', 'ram']
