#!/usr/bin/env python
"""
__author: super
数据库访问层用来对数据库文件(xml)进行读写操作
"""
import os
from xml.etree import ElementTree as ET
from modules.common import write_log
from conf import settings

from modules.myexception import MyException


def load_host_by_gid(gid):
    """
    根据组ID返回组下所有的服务器字典列表
    :param gid: 组ID e.g: G01
    :return: 服务器字典[ {"HIP":"192.168.1.2","HUSER":"root", "HKEY":"123","AUTH_TYPE":"1","HNAME":"MACH01"} ]
    """
    try:
        host_list = list()
        xml_file = ET.parse(settings.DB_HOSTS)
        root = xml_file.getroot()
        for groups in root:
            # 如果找到指定gid的节点
            if groups.attrib["GID"] == gid:
                # 开始获取服务器IP 并返回
                for child in groups:
                    h_dict = {}
                    for hosts in child:
                        if hosts.tag == "HIP": h_dict["ip"] = hosts.text
                        if hosts.tag == "HNAME": h_dict["hostname"] = hosts.text
                        if hosts.tag == "HUSER": h_dict["user"] = hosts.text
                        if hosts.tag == "AUTH_TYPE": h_dict["auth_type"] = hosts.text
                        if hosts.tag == "HKEY": h_dict["hostkey"] = hosts.text
                        if hosts.tag == "PORT": h_dict["port"] = hosts.text

                    host_list.append(h_dict)
        if len(host_list) > 0:
            return host_list
        else:
            # 未找到指定组或该组无服务器信息
            raise MyException("102")
    except MyException as e:
        write_log(e, "info")
    except Exception as e:
        write_log(e, "error")

def load_users(username):
    return_dict = dict()
    try:
        xml_file = ET.parse(settings.DB_USERS)
        root = xml_file.getroot()
        for child in root:
            if child.attrib["UNAME"] == username:
                for protertys in child:
                    if protertys.tag == "NAME":
                        return_dict["name"] = protertys.text
                    if protertys.tag == "UPASS":
                        return_dict["password"] = protertys.text
                    if protertys.tag == "GID":
                        return_dict["groups"] = protertys.text
                    if protertys.tag == "UROLE":
                        return_dict["role"] = protertys.text
                break
        if len(return_dict) > 0:
            return return_dict
        else:
            return False
    except Exception as e:
        write_log(e, "error")

def load_group_info():
    """
    返回所有组列表
    :return:
    """
    g_dict = {}

    xmlfile = ET.parse(settings.DB_GROUPS)
    root = xmlfile.getroot()
    for group in root:
        for name in group:
            g_dict[group.attrib["GID"]] = name.text

    return g_dict


