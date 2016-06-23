#!/usr/bin/env python
"""
对文件数据库进行操作的模块
"""
import os
import json
from conf import settings
from modules import common
import configparser

__user_config = os.path.join(settings.USER_INFO, "user.ini")


def read_section_all():
    """
    从user.ini文件中获取所有的 section,每个section就是一个用户名
    :return: 返回一个所有用户的用户名列表
    """
    f = configparser.ConfigParser()
    f.read(__user_config)
    userlist = f.sections()
    return userlist


def read_section_by_name(section_name):
    """
    根据传入的section，获取一个用户的信息，返回字典
    :param section_name: section 名，也就是用户名
    :return: 返回用户字典信息 {"username":"zhangsan", "password":"xxxx","isdel":0,"islock":0,"totalspace":29293832,
    "freespace":82822}
    """
    user_dict = dict()
    f = configparser.ConfigParser()
    f.read(__user_config)
    for k, v in f.items(section_name):
        user_dict[k] = v
    return user_dict


def add_option(section_name, **kwargs):
    """
    添加一个用户信息
    :param section_name: 节点名 也就是用户名
    :param kwargs: 用户信息字典 {"password":"xxxx","isdel":0,"islock":0,"totalspace":29293832“ "usedspace":82822}
    :return:
    """
    config = configparser.ConfigParser()
    with open(__user_config, "a+") as fa:
        config.add_section(section_name)
        config.set(section_name, "password", kwargs["password"])
        config.set(section_name, "islocked", kwargs["islocked"])
        config.set(section_name, "isdel", kwargs["isdel"])
        config.set(section_name, "totalspace", kwargs["totalspace"])
        config.set(section_name, "usedspace", kwargs["usedspace"])
        config.write(fa)


def modify_option(section_name, **kwargs):
    """
    修改配置文件,
    :param section_name:用户名 sectoin
    :param kwargs: 用户信息
    :return:
    """
    config = configparser.ConfigParser()
    config.read(__user_config)
    config.set(section_name, "password", kwargs["password"])
    config.set(section_name, "islocked", kwargs["islock"])
    config.set(section_name, "isdel", kwargs["isdel"])
    config.set(section_name, "totalspace", kwargs["totalspace"])
    config.set(section_name, "usedspace", kwargs["usedspace"])
    with open(__user_config, 'w+') as f:
        config.write(f)


def write_breakpoint(filemd5, filesize, recved_size, filepath, userobj):
    """
    写断点文件信息,每个用户的断点文件信息保存在各自用户的家目录下
    :param filesize: 文件总大小
    :param filemd5: 文件的MD5值
    :param recved_size: 已接收大小
    :param filepath: 文件存放路径,全名 ex: uploads/test/aaa.txt
    :param userobj: 客户端用户对象
    :return: 写文件，格式为{"filemd5":{"filepath":filepath,"recvsize":recved_size,"totalsize":totalsize}}
    """
    breadpoint_file = os.path.join(settings.BREAK_POINT_FOLDER, userobj.username)
    bfile = {filemd5: {"filepath": filepath, "totalsize": filesize, "recvsize": recved_size}}
    # 将信息写入文件
    with open(breadpoint_file, 'w+') as fw:
        fw.write(json.dumps(bfile))


def check_breakpoint(filemd5, userobj):
    """
    判断客户端上传的文件是否存在断点续传记录,返回结果，类型为列表
    :param filemd5: 文件md5
    :param userobj: 客户端用户对象
    :return:  存在: [已接收大小,文件存放路径] / 不存在: [0,用户当前路径]
    """
    try:
        breadpoint_file = os.path.join(settings.BREAK_POINT_FOLDER, userobj.username)
        # 存在断点记录文件吗
        if os.path.exists(breadpoint_file):
            with open(breadpoint_file, 'r') as fr:
                contant = fr.read()
                if len(contant) > 0:
                    bfile = json.loads(contant)
                    # 看要记录的文件是否已经存在
                    fmd5_list = list(bfile.keys())
                    # 存在
                    if filemd5 in fmd5_list:
                        # 获取已接收的大小
                        recved_size = [bfile[filemd5]["recvsize"], bfile[filemd5]["filepath"]]
                    else:
                        recved_size = [0, userobj.currpath]
                else:
                    recved_size = [0, userobj.currpath]
        else:
            # 文件都不存在肯定没有了
            recved_size = [0, userobj.currpath]
        return recved_size

    except Exception as e:
        common.write(e, "error")


def del_breakpoint(filemd5, userobj):
    """
    续传完成后，删除对应的记录
    :param filemd5: 文件md5值
    :param userobj: 客户端对象
    :return:
    """
    breadpoint_file = os.path.join(settings.BREAK_POINT_FOLDER, userobj.username)
    with open(breadpoint_file, 'r') as fr:
        bfile = json.load(fr)

    del bfile[filemd5]
    with open(breadpoint_file, 'w+') as fw:
        fw.write(json.dumps(bfile))



