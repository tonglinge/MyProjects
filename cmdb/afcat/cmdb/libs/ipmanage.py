#!/usr/bin/env python
"""
IP管理部分的导出excel,包括F5映射管理,IP规划管理及分配管理
"""
import sys

from django.db.models import Q

from afcat.api.libs.public import Logger
from afcat.cmdb import models
from afcat.cmdb.libs import common
from afcat.cmdb.libs.excel import Excel

logger = Logger(__name__)


def export_excel(custid, **kwargs):
    """
    导出Excel功能,
    :param custid:
    :param kwargs: {file_type:"balancemapping / ipdesign / ipallocate", condition: }
    :return:
    """
    try:
        file_type = kwargs.get("file_type", "")[0]
        condition = kwargs.get("conditions", "")[0]
        if not file_type:
            return None
        else:
            func = getattr(sys.modules[__name__], "{0}_excel".format(file_type))
            file_obj = func(custid, condition)
            return file_obj
    except Exception as e:
        logger.error(e)
        return None


def balancemapping_excel(custid, condition):
    """
    F5地址映射导出Excel
    :param custid: 客户ID
    :param condition: 搜索条件
    :return: excel文件对象
    """
    export_data = list()
    try:
        excel = Excel()
        sheet_obj = excel.create_sheet(u"F5地址映射")
        excel_title = [
            ("序号", 5), ("vs名称", 20), ("vs地址", 15), ("DNS域名", 25), ("SNAT地址", 15), ("地址池", 15), ("VLAN", 10),
            ("所属系统", 10), ("所属业务", 20), ("所属设备", 25), ("数据中心", 20), ("网络区域", 20), ("负载策略", 10), ("主机类型", 10),
            ("主机名称", 30), ("备注", 20)
        ]
        excel_row = list()
        all_data = get_balance_mapping_data(custid, condition)

        row_index = 1
        for obj in all_data:
            row = []
            obj_detail = get_balance_mapping_detail_info(obj)
            # index
            row.append(row_index)
            # vsname
            row.append(obj_detail.get("vsname"))
            # vsaddr:port
            row.append("{0}:{1}".format(obj_detail.get("vsaddr"), obj_detail.get("port")))
            # dnsdomain
            row.append(obj_detail.get("dnsdomain"))
            # snataddr
            row.append(obj_detail.get("snataddr").replace(",", "\n"))
            # pooladdr
            row.append(obj_detail.get("pooladdr").replace(",", "\n"))
            # vlan
            row.append(obj_detail.get("vlan"))
            # project
            row.append(obj_detail.get("project"))
            # business
            row.append(obj_detail.get("business"))
            # equipment
            row.append(obj_detail.get("equipment"))
            # datacenter
            row.append(obj_detail.get("datacenter"))
            # netarea
            row.append(obj_detail.get("netarea"))
            # ploy
            row.append(obj_detail.get("ploy"))
            # hosttype
            row.append(obj_detail.get("hosttype"))
            # hostname
            row.append(obj_detail.get("hostname"))
            # remark
            row.append(obj_detail.get("remark"))

            excel_row.append(row)
            row_index += 1
        excel.write_title(excel_title, sheet_obj)
        excel.write_row(excel_row, sheet_obj)

        excel.close()
        return excel.file

    except Exception as e:
        logger.error(e)
        return None


def ipdesign_excel(custid, condition):
    pass


def ipallocate_excel(custid, condition):
    """
    IP 地址分配管理的excel导出功能
    :param custid:
    :param condition:
    :return:
    """
    try:
        excel = Excel()
        sheet_obj = excel.create_sheet(u"IP分配管理")
        excel_title = [
            ("序号", 5), ("IP地址", 20), ("所属子网", 15), ("分配状态", 25), ("VLAN编号", 15), ("分配日期", 15), ("分配系统", 10),
            ("绑定设备", 10), ("分配人", 20), ("数据中心", 20), ("网络区域", 20), ("备注", 25)]
        excel_row = list()
        show_index = 1
        # 获取所有导出数据
        ip_qset = models.IPManage.objects.filter(cust_id=custid, ipaddr__contains=condition).order_by("ipaddr")
        for ip_obj in ip_qset:
            row = []
            ip_info = get_ipmanage_detail_info(ip_obj)
            # index
            row.append(show_index)
            # ipaddr
            row.append(ip_info.get("ipaddr"))
            # netmask
            row.append(ip_info.get("ipmask"))
            # status
            row.append(ip_info.get("status"))
            # vlan
            row.append(ip_info.get("vlan"))
            # allocate date
            row.append(ip_info.get("allocatedate"))
            # project
            row.append(ip_info.get("allocateto"))
            # binded
            row.append(ip_info.get("binded"))
            # allocate user
            row.append(ip_info.get("allocateuser"))
            # datacenter
            row.append(ip_info.get("datacenter"))
            # netarea
            row.append(ip_info.get("netarea"))
            # remark
            row.append(ip_info.get("remark"))

            excel_row.append(row)
            show_index += 1

        # 写excel文件
        excel.write_title(excel_title, sheet_obj)
        excel.write_row(excel_row, sheet_obj)

        excel.close()
        return excel.file

    except Exception as e:
        logger.error(e)
        return None


def get_balance_mapping_data(custid, search_condition):
    """
    获取所有地址映射数据
    :param custid: 客户ID
    :param condition: 条件
    :return:
    """
    try:
        data = models.BalanceMapping.objects.filter(Q(vsname__contains=search_condition) |
                                                    Q(vsaddr__contains=search_condition) |
                                                    Q(dnsdomain__contains=search_condition) |
                                                    Q(snataddr__contains=search_condition) |
                                                    Q(pooladdr__contains=search_condition),
                                                    id__startswith=custid)
        return data
    except Exception as e:
        logger.error(e)
        return []


def get_balance_mapping_detail_info(map_obj):
    try:
        info = dict(id=map_obj.id, vsname=map_obj.vsname, vsaddr=map_obj.vsaddr, port=map_obj.port,
                    dnsdomain=map_obj.dnsdomain, snataddr=map_obj.snataddr, pooladdr=map_obj.pooladdr,
                    vlan=map_obj.vlan,
                    netarea_id=map_obj.netarea_id,
                    datacenter_id=map_obj.datacenter_id,
                    datacenter=map_obj.datacenter.name if map_obj.datacenter else "",
                    netarea=map_obj.netarea.name if map_obj.netarea else "",
                    project=map_obj.project.sysname if map_obj.project else "",
                    project_id=map_obj.project_id,
                    ploy=map_obj.ploy.typename if map_obj.ploy else "",
                    business=common.get_value_by_ids("Business", "bussname", map_obj.business),
                    business_id=map_obj.business,
                    equipment=map_obj.equipment.assetname if map_obj.equipment else "",
                    equipment_id=map_obj.equipment_id,
                    hostname=map_obj.hostname,
                    hosttype=map_obj.hosttype,
                    remark=map_obj.remark
                    )
        return info
    except Exception as e:
        logger.error(e)
        return ""


def get_ipmanage_detail_info(ip_obj):
    """
    获取ip分配的详细信息
    :param ip_obj: ip对象
    :return:
    """
    try:
        detail_info = dict(id=ip_obj.id, ipaddr=ip_obj.ipaddr, ipmask=ip_obj.ipmask.__str__(),
                           status=ip_obj.get_status_display(),
                           allocateuser=ip_obj.allocateuser, allocatedate=ip_obj.allocatedate,
                           allocateto=ip_obj.allocateto, binded=ip_obj.binded,
                           vlan=ip_obj.vlan,
                           datacenter=ip_obj.ipmask.datacenter.name if ip_obj.ipmask and ip_obj.ipmask.datacenter else "",
                           netarea=ip_obj.ipmask.netarea.name if ip_obj.ipmask and ip_obj.ipmask.netarea else "",
                           remark=ip_obj.remark)
        return detail_info
    except Exception as e:
        logger.error(e)
        return ""
