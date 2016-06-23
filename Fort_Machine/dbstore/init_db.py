#!/usr/bin/env python
"""
初始化数据表文件：
groups.xml:  服务器主机组文件，包括：
                                GID：组编号
                                GNAME：组名称
hosts.xml: 主机文件，包括：
                        GID: 所属主机组编号
                        HIP: 主机IP
                        HNAME：主机名
                        HUSER：登录名
                        HKEY: 登录密码 (AUTH_TYPE=1则为密码，AUTH_TYPE=2则为私钥文件)
                        AUTH_TYPE：验证类型(1:用户名密码登录，2：密钥登录)
users.xml: 用户文件，包括：
                        UID：用户ID
                        UNAME: 用户名
                        UPASS: 用户密码 (加密)
                        UROLE: 用户权限 (user:普通用户， admin: 管理员)
                        GID: 管理服务器组ID (1,2)
"""
import os
import sys
from xml.etree import ElementTree

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modules import common

groups = {
    "G01": "新闻组",
    "G02": "视频组",
    "G03": "开发组",
    "G04": "文件组"
}
hosts = {
    "G01": [{"HIP": "192.168.2.128", "HNAME": "agent", "HUSER": "root", "PORT": "22", "AUTH_TYPE": 1, "HKEY": "redhat"},
            {"HIP": "192.168.2.129", "HNAME": "ubuntu", "HUSER": "super", "PORT": "22", "AUTH_TYPE": 1,
             "HKEY": "super"}, ],
    "G02": [{"HIP": "192.168.1.128", "HNAME": "agent", "HUSER": "root", "PORT": "22", "AUTH_TYPE": 2,
             "HKEY": "private_test03.rsa"}, ],
    "G03": [
        {"HIP": "192.168.2.129", "HNAME": "ubuntu", "HUSER": "super", "PORT": "22", "AUTH_TYPE": 1, "HKEY": "test"}, ],
    "G04": [{"HIP": "192.168.2.128", "HNAME": "agent", "HUSER": "root", "PORT": "22", "AUTH_TYPE": 1, "HKEY": "redhat"}, ]
}
users = {
    "admin": {"UPASS": "12345", "GID": "G01,G02,G03,G04", "UROLE": "admin", "NAME": "administrator"},
    "test": {"UPASS": "12345", "GID": "G01,G02", "UROLE": "user", "NAME": "zhangsan"}
}


def init_groups():
    root = ElementTree.Element("GROUPS")

    for k, v in groups.items():
        gid = ElementTree.SubElement(root, "GROUP", attrib={"GID": k})
        gname = ElementTree.SubElement(gid, "GNAME")
        gname.text = v

    xmlfile = ElementTree.ElementTree(root)
    xmlfile.write("groups.xml", encoding="utf-8", xml_declaration=True)


def init_hosts():
    root = ElementTree.Element("HOSTS")

    for k, hlist in hosts.items():
        gid = ElementTree.SubElement(root, "GROUP", attrib={"GID": k})
        for host in hlist:
            h = ElementTree.SubElement(gid, "HOST")

            hip = ElementTree.SubElement(h, "HIP")
            hname = ElementTree.SubElement(h, "HNAME")
            huser = ElementTree.SubElement(h, "HUSER")
            auth_type = ElementTree.SubElement(h, "AUTH_TYPE")
            hkey = ElementTree.SubElement(h, "HKEY")
            hport = ElementTree.SubElement(h, "PORT")

            hip.text = host["HIP"]
            hname.text = host["HNAME"]
            huser.text = host["HUSER"]
            auth_type.text = str(host["AUTH_TYPE"])
            hkey.text = host["HKEY"]
            hport.text = host["PORT"]

    xmlfile = ElementTree.ElementTree(root)
    xmlfile.write("hosts.xml", encoding="utf-8", xml_declaration=True)


def init_users():
    root = ElementTree.Element("USERS")

    for k, info in users.items():
        u = ElementTree.SubElement(root, "USER", attrib={"UNAME": k})

        upass = ElementTree.SubElement(u, "UPASS")
        ugid = ElementTree.SubElement(u, "GID")
        urole = ElementTree.SubElement(u, "UROLE")
        uname = ElementTree.SubElement(u, "NAME")

        upass.text = common.encry_sha(info["UPASS"])
        ugid.text = info["GID"]
        urole.text = info["UROLE"]
        uname.text = info["NAME"]

    xmlfile = ElementTree.ElementTree(root)
    xmlfile.write("users.xml", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    init_users()
