#!/usr/bin/env python
"""
该模块用来处理cmdb中所有服务器资产相关信息
author: wangsong   2016-09-06
"""
import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.signals import post_save

from afcat.account.core.permission import operator_audit_decorator
from afcat.api.libs.public import Logger, response_format
from afcat.cmdb import models
from afcat.cmdb.libs import base, common

logger = Logger(__name__)


def get_asset_list(page_index, conditions, custid, perm_id_list=None, per_count=None):
    """
    显示主机资产列表信息,
    :param perm_id_list: 允许查看的主机列表
    :type conditions: 搜索条件: e.g: {"key":"hostname/ip/sys","value":"host001"} or ""
    :return: 返回分页后的主机信息,总页数,当前页码, 返回给前端首页
    """
    result = response_format()
    _hosts_list = list()
    page_split_result = {"record": _hosts_list, "addperm": True}

    try:
        # 获取允许查看的资产id列表
        if perm_id_list is None:
            # super user
            pass
        else:
            # if perm_id_list:
            if not conditions:
                conditions = {"perm_id_list": perm_id_list}
            else:
                conditions.update({"perm_id_list": perm_id_list})

        all_hosts = _load_serverobj_list_by_condition(conditions, custid)
        # 获取分页数据
        page_split_result.update(common.page_split(all_hosts, page_index, per_count))
        servers_obj_list = page_split_result["record"]

        if all_hosts.count() > 0:
            for server_obj in servers_obj_list:
                business_info = _business_in_server(server_obj.related_business.select_related())
                _server_info = dict(id=server_obj.id, hostname=server_obj.hostname,
                                    type=server_obj.type.name if server_obj.type else "",
                                    model=server_obj.model,
                                    partition=server_obj.partition,
                                    business=business_info[0],
                                    projects=business_info[1],
                                    probusiness=business_info[2],
                                    balancetype=server_obj.balancetype.typename if server_obj.balancetype else "",
                                    netarea=server_obj.netarea.name if server_obj.netarea else "",
                                    cabinet=server_obj.ownserver.cabinet if server_obj.ownserver else "",
                                    unitinfo=server_obj.ownserver.unitinfo if server_obj.ownserver else "",
                                    staffs=_staff_server_str(server_obj),
                                    cpu=server_obj.server_cpu.first().cpucount if server_obj.server_cpu.first() else 0,
                                    memory=server_obj.server_cpu.first().memory if server_obj.server_cpu.first() else 0,
                                    remark=server_obj.remark,
                                    delperm=True,
                                    changeperm=True
                                    )
                _hosts_list.append(_server_info)
        page_split_result.update({"record": _hosts_list})

    except Exception as e:
        logger.error(e)
        page_split_result.update({"num_pages": 1, "curr_page": 1, "total_count": 0})

    result['data'] = page_split_result
    return result


def _load_serverobj_list_by_condition(conditions, custid):
    """
    根据查询条件返回所有的主机对象结果集
    :param conditions: 查询条件
    :return:
    """
    if not conditions:
        all_hosts = models.Servers.objects.filter(cust_id=custid)
    else:
        try:
            # 搜索条件
            # search_key = conditions.get("key", "")
            search_value = conditions.get("value", "")
            # 获取能访问的主机id
            search_filter = dict(cust_id=custid)
            if conditions.get("perm_id_list") is not None:
                search_filter.update({"id__in": conditions.get("perm_id_list")})

            if search_value:
                # if search_key == "hostname":
                #     search_filter.update({"hostname__contains": search_value})
                #
                # elif search_key == "ip":
                #     search_filter.update({"server_ip__ipaddress__contains": search_value})
                #
                # elif search_key == "sys":
                #     id_list = list()
                #     buss_list = models.Business.objects.filter(project__sysname__contains=search_value)
                #     server_list = models.R_Server_Business.objects.filter(business__in=buss_list).values("server_id")
                #     for server in list(server_list):
                #         id_list.append(server.get("server_id"))
                #     search_filter.update({"id__in": id_list})
                # elif search_key == "ownserver":
                #     search_filter.update({"ownserver__sn__contains": search_value})
                # else:
                #     pass
                all_hosts = models.Servers.objects.filter(Q(hostname__contains=search_value) |
                                                          Q(server_ip__ipaddress__contains=search_value) |
                                                          Q(ownserver__sn__contains=search_value) |
                                                          Q(id__in=[obj.get("server_id") for obj in list(
                                                              models.R_Server_Business.objects.filter(
                                                                  business__project__sysname__contains=search_value).values(
                                                                  "server_id"))]),
                                                          **search_filter
                                                          ).all().distinct()
            else:
                # 获得结果
                all_hosts = models.Servers.objects.filter(**search_filter).all().distinct()
        except KeyError:
            all_hosts = models.Servers.objects.all()
    return all_hosts


def _business_in_server(business_obj_list):
    """
    获取服务器资产所属业务线的字符串结果
    :param business_obj_list:所有资产关联的业务线对象(r_server_bussiness) queryset
    :return:业务线的名字串 e.g: 资金数据库,资金业务系统
    """
    business = list()
    projects = list()
    union_str = list()
    try:
        if business_obj_list.count() > 0:
            for r_buss_obj in business_obj_list:
                buss_obj = r_buss_obj.business
                projects.append(buss_obj.project.sysname if buss_obj.project else "")
                business.append(buss_obj.bussname)
                union_str.append("%s - %s" % (buss_obj.project.sysname if buss_obj.project else "",
                                              buss_obj.bussname))
                # business = ",".join(return_str)
    except Exception as e:
        logger.error(e)
    return union_str, list(set(projects)), business


def _staff_server_str(server_obj):
    """
    获取服务器资产的所有联系人信息
    :param server_obj:服务器资产对象
    :return: 首页显示的联系人信息字符串格式(仅姓名,用逗号分隔)
    """
    return base.get_asset_staffs_str(server_obj)


def get_asset_details(server_id):
    """
    获取服务器的所有详细信息
    :param server_id: 服务器资产ID
    :return: 所有资产信息的一个的字典
    """
    result = dict()
    data = response_format()
    try:
        server_obj = models.Servers.objects.get(id=server_id)
        result.update({"server": _server_base_info(server_obj)})
        result.update({"cpu": _server_cpu_info(server_obj)})
        result.update({"ip": _server_ip_info(server_obj)})
        result.update({"vg": _server_vg_info(server_obj)})
        result.update({"card": _server_card_info(server_obj)})
        result.update({"software": _server_software_info(server_obj)})
        result.update({"staffs": _server_staff_info(server_obj)})
        # data = {"data": result, "status": True}
        data["data"] = result
    except (ObjectDoesNotExist, Exception) as e:
        data["info"] = "未找到指定的设备信息"
        data["status"] = False
        logger.error(e)
    return data


def _server_base_info(server_obj):
    """
    获取主机的基本信息(主机表的信息)
    :param server_obj: 主机对象
    :return:  主机字典信息
    """
    buss_info = _business_in_server(server_obj.related_business.select_related())
    server = dict(id=server_obj.id, hostname=server_obj.hostname, model=server_obj.model,
                  type=server_obj.type.name if server_obj.type else "",
                  ownserver="{0}:{1}".format(server_obj.ownserver.model,
                                             server_obj.ownserver.sn) if server_obj.ownserver else "",
                  partition=server_obj.partition,
                  tradedate=datetime.strftime(server_obj.tradedate, "%Y-%m-%d") if server_obj.tradedate else "",
                  expiredate=datetime.strftime(server_obj.expiredate, "%Y-%m-%d") if server_obj.expiredate else "",
                  netarea=server_obj.netarea.name if server_obj.netarea else "",
                  balancetype=server_obj.balancetype.typename if server_obj.balancetype else "",
                  runningstatus=server_obj.runningstatus.status if server_obj.runningstatus else "",
                  business=buss_info[0], projects=buss_info[1], probussiness=buss_info[2],
                  remark=server_obj.remark)
    return server


def _server_cpu_info(server_obj):
    """
    获取指定server的CPU及内存信息
    :param server_id: 服务器id
    :return: cpu数据字典 {'cpucount':1,'cputype':'intel','cpucore':3.....}
    """
    result = list()
    try:
        cpu_objs = server_obj.server_cpu.select_related().all()
        if cpu_objs:
            for cpu_obj in cpu_objs:
                cpuinfo = dict(id=cpu_obj.id, model=cpu_obj.model, cpucount=cpu_obj.cpucount,
                               corecount=cpu_obj.corecount,
                               frequenct=cpu_obj.frequency, memory=cpu_obj.memory, remark=cpu_obj.remark)
                result.append(cpuinfo)
    except Exception as e:
        logger.error(e)
    finally:
        return result


def _server_ip_info(server_obj):
    """
    获取指定server的 IP 配置信息
    :param server_obj:
    :return:[{"ipaddress":"","iptype":"","gatway":""...},{}]
    """
    ipinfo = []
    ip_obj_list = server_obj.server_ip.select_related()
    try:
        if ip_obj_list.count() > 0:
            for ip_obj in ip_obj_list:
                ip = dict(id=ip_obj.id, ipaddress=ip_obj.ipaddress, gatway=ip_obj.gatway,
                          iptype=ip_obj.iptype, domain=ip_obj.domain, vlan=ip_obj.vlan,
                          remark=ip_obj.remark)
                ipinfo.append(ip)
    except Exception as e:
        logger.error(e)
    return ipinfo


def _server_card_info(server_obj):
    """
    主机详细信息页面显示所有板卡(网卡/存储卡)信息
    :param server_obj: 主机对象
    :return: 所有板卡信息的字典列表
    """
    card_list = list()
    try:
        all_card_obj = models.ServerBoardCard.objects.filter(server=server_obj)
        for card_obj in all_card_obj:
            card_info = _server_card_details(card_obj)
            card_list.append(card_info)
    except Exception as e:
        logger.error(e)
    return card_list


def _server_card_details(card_obj):
    """
    获取主机单块板卡(网卡/存储卡)的详细信息
    :param card_obj: 卡对象
    :return: 返回卡信息的字典形式
    """
    try:
        card_info = dict(id=card_obj.id, assetno=card_obj.assetno, sn=card_obj.sn,
                         model=card_obj.model,
                         typevalue=card_obj.cardtype, typename="网卡" if card_obj.cardtype == 1 else "存储卡",
                         mac=card_obj.mac, slot=card_obj.slot,
                         factoryid=card_obj.factory_id, factory=card_obj.factory.name if card_obj.factory else "",
                         serverid=card_obj.server_id,
                         remark=card_obj.remark,
                         portcount=models.PortList.objects.filter(object_pk=card_obj.id, flag=1).count())
        return card_info
    except Exception as e:
        logger.error(e)
        return dict()


def _server_card_port(card_obj):
    """
    获取主机设备某一块板卡下的所有端口信息
    :param card_obj: 板卡对象
    :return: 端口的列表
    """
    port_list = list()
    try:
        all_port_obj = models.PortList.objects.filter(object_pk=card_obj.id, flag=1)
        for port_obj in all_port_obj:
            port_info = dict(id=port_obj.id, portname=port_obj.portname, porttype=port_obj.porttype, vlan=port_obj.vlan,
                             targetport="", targettype="", targetasset="")

            # 获取端口映射表中的本端口映射记录(作为对端target端口存在)
            map_obj_list = port_obj.related_target.select_related().all()
            for map_obj in map_obj_list:
                if map_obj.localport.flag == 2:
                    # 获取对端(网络设备)的端口信息
                    obj_id = map_obj.localport.object_pk
                    card_obj = models.EquipmentBoardCard.objects.filter(id=obj_id).first()
                    if card_obj:
                        port_info.update(dict(targetport=map_obj.localport.portname if map_obj.localport else "",
                                              targettype=map_obj.localport.porttype if map_obj.localport else "",
                                              targetasset="{0}:{1}({2})".format(
                                                  card_obj.equipment.assetname if card_obj.equipment else "",
                                                  card_obj.equipment.model if card_obj.equipment else "",
                                                  card_obj.cardname)))
                        # port_info.update(map_info)
            port_list.append(port_info)

    except Exception as e:
        logger.error(e)
    return port_list


def _server_vg_info(server_obj):
    """
    加载服务器资产的VG信息
    :param server_obj:服务器资产对象
    :return: vg信息字典列表
    """
    vg_list = list()
    try:
        vg_obj_list = models.StorageVG.objects.filter(server=server_obj)
        if vg_obj_list.count() > 0:
            for vg_obj in vg_obj_list:
                vg_info = dict(id=vg_obj.id, vgname=vg_obj.vgname, vgsize=vg_obj.vgsize,
                               raidtype=vg_obj.raidtype.typename if vg_obj.raidtype else "",
                               remark=vg_obj.remark)
                vg_info.update(load_vg_related_lv_pv(vg_obj))
                vg_list.append(vg_info)

    except Exception as e:
        logger.error(e)
    return vg_list


def _server_software_info(server_obj):
    """
    获取指定 server 下面的所有安装软件信息
    :param server_id:
    :return:
    """
    software_info = []
    software_obj_list = server_obj.server_soft.select_related()
    try:
        if software_obj_list.count() > 0:
            for soft_obj in software_obj_list:
                soft = dict(id=soft_obj.id,
                            soft_id=soft_obj.soft_id,
                            softname=soft_obj.soft.name,
                            softtype=soft_obj.soft.type.name,
                            version=soft_obj.soft.version if soft_obj.soft.version else "",
                            lisence=soft_obj.lisence.lisence if soft_obj.lisence else "",
                            port=soft_obj.port,
                            remark=soft_obj.remark)
                software_info.append(soft)
    except Exception as e:
        logger.error(e)
    return software_info


def _server_staff_info(server_obj):
    """
    获取指定 server 上的联系人信息
    :type server_obj: 服务器对象
    :return: 人员信息
    """
    staffs_info = []
    try:
        staffs_obj_list = server_obj.related_staffs.select_related()
        if staffs_obj_list.count() > 0:
            for staffs_obj in staffs_obj_list:
                staff = dict(id=staffs_obj.id,
                             staff_id=staffs_obj.staff_id,
                             role_id=staffs_obj.role_id,
                             name=staffs_obj.staff.name,
                             mobile=staffs_obj.staff.mobile,
                             tel=staffs_obj.staff.tel,
                             email=staffs_obj.staff.email,
                             role=staffs_obj.role.role_name if staffs_obj.role else "",
                             remark=staffs_obj.remark)
                staffs_info.append(staff)
    except Exception as e:
        logger.error(e)
    return staffs_info


def _serv_business_info(serv_obj, field_list=None):
    """
    获取服务器业务线
    :param serv_obj: 服务器对象
    :param field_list: 需要的字段名,如果为空返回对象的列表
    :return: 指定字段名的对象列表
    """
    result = list()
    try:
        r_business = serv_obj.related_business.select_related()
        for r_obj in r_business:
            buss_obj = r_obj.business
            if not field_list:
                result.append(buss_obj)
            else:
                field_value_dic = dict()
                for field_name in field_list:
                    field_value = getattr(buss_obj, field_name)
                    field_value_dic.update({field_name: field_value})
                result.append(field_value_dic)
    except Exception as e:
        logger.error(e)
    return result


def load_related_base_configuration(custid):
    """
    前端对服务器修改或新增加时，获取页面所需要的基表数据信息
    :return: 返回所有信息的数据信息，字典
    """
    base_config = dict()
    try:

        base_config.update(base.load_base_table_record("BaseAssetType", ["id", "name", "flag"], custid))
        base_config.update(base.load_base_table_record("BaseNetArea", ["id", "name"], custid))
        base_config.update(base.load_base_table_record("BaseBalanceType", ["id", "typename"], custid))
        base_config.update(base.load_base_table_record("BaseRunningStatus", ["id", "status"], custid))
        base_config.update(base.load_base_table_record("Projects", ["id", "sysname"], custid))
        base_config.update(base.load_base_table_record("Business", ["id", "bussname", "project"], custid))
        base_config.update(_get_own_server(custid))

    except Exception as e:
        logger.error(e)
    return base_config


def _get_own_server(custid):
    """
    获取服务器主机信息中的宿主主机
    :return:
    """
    server_list = list()
    try:
        assets_obj = models.Assets.objects.filter(cust_id=custid)
        for asset in assets_obj:
            subtype = asset.assettype.name if asset.assettype else ""
            server_list.append(dict(id=asset.id, server="{0} {1}[{2}]".format(subtype, asset.model, asset.sn)))
    except Exception as e:
        logger.error(e)
    return {"ownserver": server_list}


def get_vg_related_detail(vg_id):
    """
    点击vg详情后,显示所有vg下的pv, lv信息
    :param vg_id: vg的id
    :return: {"vg":{}, "pv":[{},{}],"lv":[{},{}]}
    """
    result = response_format()
    vg_detail = dict(vg=dict(pv=list(), lv=list()), )
    try:
        vg_obj = models.StorageVG.objects.get(id=vg_id)
        vg_detail["vg"].update(dict(id=vg_obj.id, vgname=vg_obj.vgname, vgsize=vg_obj.vgsize,
                                    raidtype=vg_obj.raidtype.typename if vg_obj.raidtype else ""))
        # 获取所有pv信息
        pv_obj_list = vg_obj.related_pv.select_related().all()
        for pv_obj in pv_obj_list:
            vg_detail["vg"]["pv"].append(dict(id=pv_obj.id, pvname=pv_obj.pvname, pvsize=pv_obj.pvsize,
                                              remark=pv_obj.remark))
        # 获取所有lv信息
        lv_obj_list = vg_obj.related_lv.select_related().all()
        for lv_obj in lv_obj_list:
            vg_detail["vg"]["lv"].append(dict(id=lv_obj.id, lvname=lv_obj.lvname, lvsize=lv_obj.lvsize,
                                              filesystem=lv_obj.filesystem, remark=lv_obj.remark))
    except Exception as e:
        logger.error(e)

    result["data"] = vg_detail
    return result


def load_vg_related_lv_pv(vg_obj):
    """
    获取vg下面的所有lv,pv的信息,加载主机详情后将vg下的lv,Pv信息一起显示出来
    :param vg_obj:
    :return:
    """
    vg_detail = dict(pv=list(), lv=list())
    try:
        # 获取所有pv信息
        pv_obj_list = vg_obj.related_pv.select_related().all()
        for pv_obj in pv_obj_list:
            vg_detail["pv"].append(dict(id=pv_obj.id, pvname=pv_obj.pvname, pvsize=pv_obj.pvsize,
                                        remark=pv_obj.remark))
        # 获取所有lv信息
        lv_obj_list = vg_obj.related_lv.select_related().all()
        for lv_obj in lv_obj_list:
            vg_detail["lv"].append(dict(id=lv_obj.id, lvname=lv_obj.lvname, lvsize=lv_obj.lvsize,
                                        filesystem=lv_obj.filesystem, remark=lv_obj.remark))
    except Exception as e:
        logger.error(e)

    return vg_detail


def get_asset_base_info(sid):
    """
    获取单个服务器的基本信息(服务器资产表中的信息)
    :param sid:
    :return:
    """
    try:
        buss_info = list()
        server_obj = models.Servers.objects.get(id=sid)
        server_info = common.get_record_all_fields(server_obj)
        related_buss = server_obj.related_business.select_related()
        for buss in related_buss:
            buss_info.append({"id": buss.business_id, "bussname": buss.business.bussname})
        server_info.update({"business": buss_info})

        return server_info
    except Exception as e:
        logger.error(e)
        return ""


@operator_audit_decorator("Servers")
def edit_asset(data):
    """
    增加或编辑主机信息时，保存提交过来的数据
    :param data: 数据,{"server":{},"business":[1,2]} server主机产基本信息,business为关联的多对多业务编号
    :return: 成功返回True，否则返回False
    """
    try:
        buss_data = list()
        server_obj = None
        result = response_format()
        # 对于传过来的值data,如果有空的就去掉

        server_data = data.get("value", "")
        action = data.get("action")
        sid = server_data.get("id", 0)
        user = data.get("user")
        custid = data.get("custid")
        if server_data:
            server_data = common.filter_dict(server_data)
            buss_data = data.get("business", [])  # 所属业务线id 列表

        if action == "edit":
            if not _check_exists(server_data.get("hostname", ""), custid, sid):
                # print(sid)
                server_qset = models.Servers.objects.filter(id=sid)
                # print(server_qset)
                server_data.update(dict(updateuser=user.username, updatedate=datetime.now()))
                server_qset.update(**server_data)
                server_obj = server_qset.first()
                result["info"] = "修改成功"
            else:
                result["info"] = "主机名重复"
                result["category"] = "warning"
                result["status"] = False

        elif action == "delete":
            server_obj = models.Servers.objects.filter(id=sid).first()
            if server_obj:
                del_history_data = load_servers_related_data(sid)
                # 写入历史数据
                base.save_del_history("Servers", del_history_data, user, custid)
                # 删除所有服务器板卡的端口数据
                port_id_list = list()
                for port in json.loads(del_history_data).get("PortList", []):
                    port_id_list.append(port.get("id"))
                models.PortList.objects.filter(id__in=port_id_list).delete()
                # 删除Server记录
                server_obj.delete()
                result["info"] = "删除成功!"
            else:
                result["status"] = False
                result["info"] = "未找到指定的记录"
                result["category"] = "error"
        else:
            if not _check_exists(server_data.get("hostname", ""), custid):
                # 新增的添加一个资产编号
                server_data.update(dict(id=base.nextid(models.Servers._meta.db_table, custid),
                                        cust_id=custid,
                                        createuser=user.username, updateuser=user.username))
                # print(server_data)
                server_obj = models.Servers.objects.create(**server_data)
                result["info"] = "添加成功"
                result["data"] = dict(id=server_obj.id)
            else:
                result["info"] = "主机名重复"
                result["category"] = "warning"
                result["status"] = False
        if server_obj:
            server_obj.related_business.select_related().delete()
            if buss_data:
                for ids in buss_data:
                    server_obj.related_business.select_related().create(
                        id=base.nextid(models.R_Server_Business._meta.db_table, custid),
                        server=server_obj,
                        business_id=int(ids))

    except Exception as e:
        logger.error(e)
        result["info"] = "操作失败,联系管理员!"
        result["category"] = "error"
        result["status"] = False
    return result


def _check_exists(hostname, custid, obj_id=None):
    """
    检查主机名是否存在
    :param hostname: 主机名
    :param custid: 客户编号
    :param obj_id: 编辑时的主机ID
    :return: 存在Ture / 不存在 False
    """
    exists_flag = False
    try:
        sc = models.Servers.objects.filter(cust_id=custid, hostname=hostname)
        if obj_id:
            sc.exclude(id=obj_id)

        if sc.count() > 0:
            exists_flag = True
    except Exception as e:
        logger.error(e)

    return exists_flag


@operator_audit_decorator("ServerRelated")
def save_servers_related_asset(data):
    """
    服务器资产中子资产信息的添加,修改公共方法
    :param action: 新增 or 编辑 or 删除  (new/edit/del)
    :param data: data: {"asset":"CpuMemroy", "value":{"id":1, "server_id":2, "model":"intel","cpucount":2,"corecount":2,
                            "frequency":"3.4","memory":6,"remark":""}
    :return: 成功True 失败False
    """
    from afcat.cmdb.packages.cmdbsignals import check_signal

    tablename = data.get("asset")
    value_data = data.get("value")
    action = data.get("action")
    user = data.get("user")
    custid = data.get("custid")
    result = response_format()
    try:
        table_obj = getattr(models, tablename)
        # value_data = common.filter_dict(value_data)
        if action == "new":
            # 追加自定义ID
            value_data.update(dict(id=base.nextid(table_obj._meta.db_table, custid),
                                   createuser=user.username,
                                   updateuser=user.username))
            # 检查是否有assetno资产编号字段,如有添加一个资产编号
            for field in table_obj._meta.fields:
                if field.column == "assetno":
                    value_data.update({"assetno": common.create_assno()})
                    break
            # print(value_data)
            # 对于配置IP地址信息时,IP重复验证,调用信号
            check_result = check_signal.send(sender=table_obj, instance=value_data)
            exists_flag = check_result[0][1].get("status") if check_result else True

            if not exists_flag:
                result["info"] = check_result[0][1].get("err")
                result["category"] = "error"
            else:
                newobj = table_obj.objects.create(**value_data)
                result["data"] = base.get_single_obj_record(newobj)
                result["info"] = "添加成功"
                result["category"] = "success"

        elif action == "edit":  # edit
            value_data.update(dict(updateuser=user.username, updatedate=datetime.now()))
            # IP重复验证
            check_result = check_signal.send(sender=table_obj, instance=value_data)
            exists_flag = check_result[0][1].get("status") if check_result else True

            if not exists_flag:
                result["info"] = check_result[0][1].get("err")
                result["category"] = "error"
            else:
                qset = table_obj.objects.filter(id=value_data["id"])
                # 针对IPConfiguration进行提交后IP状态更改
                post_save.send(sender=table_obj, instance=qset.first(),
                               **{"update": True, "ipaddress": value_data.get("ipaddress", "")})
                qset.update(**value_data)
                # 返回新的对象信息
                newobj = table_obj.objects.get(id=value_data["id"])
                result["data"] = base.get_single_obj_record(newobj)
                result["info"] = "修改成功"
                result["category"] = "success"
        else:  # del
            del_obj = table_obj.objects.filter(id=value_data["id"]).delete()
            result["info"] = "删除成功"
            result["category"] = "success"
        return result
    except Exception as e:
        logger.error(e)
        result["info"] = "执行错误"
        result["category"] = "error"
    return result


def export_excel(custid, **kwargs):
    """
    根据前端的过滤条件生成excel文件
    :param kwargs: 查询条件 {"key":"ip", "value":""}
    :return:
    """
    from afcat.cmdb.libs import excel
    try:
        conditions = {"value": kwargs.get("value")[0]}
        all_hosts = _load_serverobj_list_by_condition(conditions, custid)

        host_details_list = list()
        excel_obj = excel.Excel()
        for host in all_hosts:
            host_detail = get_asset_details(host.id)
            host_details_list.append(host_detail.get("data"))

        # 生成主机主要信息的sheet页
        _excel_write_host_sheet(excel_obj, host_details_list)
        # 生成IP 页
        _excel_write_ip_sheet(excel_obj, host_details_list)

        excel_obj.close()
        return excel_obj.file
    except Exception as e:
        logger.error(e)
        return excel_obj.file


def _excel_write_host_sheet(excel_obj, hosts_record):
    """
    导出所有主机信息到一个sheet页
    :return:
    """
    host_sheet = excel_obj.create_sheet(u"主机")
    host_title = [("序号", 5), ("业务系统", 15), ("应用模块", 15), ("主机名", 15), ("主机类型", 10), ("网络域", 20),
                  ("F5策略", 10), ("型号", 15), ("分区号", 15), ("安装软件", 25), ("CPU", 5), ("内存(G)", 10),
                  ("购买日期", 10), ("过保日期", 10), ("运行状态", 10), ("联系人", 40), ("备注", 20)
                  ]
    host_rows = []
    row_index = 1
    try:
        # print(hosts_record)
        for host in hosts_record:
            row = []
            info = host.get("server")
            # index
            row.append(row_index)
            # projectname
            row.append("\n".join(info["projects"]))
            # business
            row.append("\n".join(info["probussiness"]))
            # hostname
            row.append(info["hostname"])
            # server type
            row.append(info["type"])
            # netarea
            row.append(info["netarea"])
            # F5
            row.append(info["balancetype"])
            # server model
            row.append(info["model"])
            # partition
            row.append(info["partition"])
            # installed software
            if host.get("software", ""):
                row.append(common.convert_dict_to_str(host["software"], ["softname", "version"], " "))
            else:
                row.append("")
            # cpu
            if host.get("cpu", ""):
                row.append(
                    common.convert_dict_to_str(host["cpu"], ["cpucount"], "/")
                )
                # # memory
                row.append(
                    common.convert_dict_to_str(host["cpu"], ["memory"], "/")
                )
                # row.append(info["cpu"]["memory"])
            else:
                row.append("")
                row.append("")
            # tradedate
            row.append(info["tradedate"])
            # expiredate
            row.append(info["expiredate"])
            # status
            row.append(info["runningstatus"])
            # staffs
            if host.get("staffs", ""):
                row.append(common.convert_dict_to_str(host["staffs"], ["name", "role", "mobile", "remark"], "/"))
            else:
                row.append("")
            # remark
            row.append(info["remark"])

            row_index += 1
            host_rows.append(row)

        excel_obj.write_title(host_title, host_sheet)
        excel_obj.write_row(host_rows, host_sheet)
    except Exception as e:
        logger.error(e)


def _excel_write_ip_sheet(excel_obj, hosts_record):
    """
    写入所有主机的IP信息
    :param excel_obj: Excel文件对象
    :param hosts_record: 主机记录信息
    :return:
    """
    try:
        ip_sheet = excel_obj.create_sheet(u"IP配置")
        ip_title = [
            ("序号", 5), ("IP地址", 15), ("网关", 15), ("IP类型", 15), ("域名", 15), ("VLAN", 5), ("所属主机", 10), ("备注", 20)
        ]
        row_index = 1
        ip_rows = list()
        for host in hosts_record:
            ip_record = host.get("ip")
            for info in ip_record:
                row = list()
                # index
                row.append(row_index)
                # ip addr
                row.append(info.get("ipaddress", ""))
                # gatway
                row.append(info.get("gatway", ""))
                # type
                row.append(info.get("iptype", ""))
                # domain
                row.append(info.get("domain", ""))
                # vlan
                row.append(info.get("vlan", ""))
                # host
                row.append(host["server"]["hostname"])
                # remark
                row.append(info.get("remark", ""))

                ip_rows.append(row)
                row_index += 1

        excel_obj.write_title(ip_title, ip_sheet)
        excel_obj.write_row(ip_rows, ip_sheet)

    except Exception as e:
        logger.error(e)


def load_servers_related_data(sid):
    """
    获取要删除的服务器数据及所关联的所有信息
    :param sid: 服务器id
    :return: json格式数据
    """
    try:
        history_data = dict()  # 保存服务器数据信息
        # 获取要删除的server的数据
        server_obj = models.Servers.objects.get(id=sid)
        server_record = common.get_record_all_fields(server_obj)
        # 获取 server 的依赖表数据
        server_related_data = common.object_related_data("Servers", sid)

        history_data.update({"Servers": server_record})
        history_data.update(server_related_data)

        # 服务器的板卡端口PortList信息(非直接关联server,关联ServerBoardCard)
        card_port_info = list()
        for card in server_obj.related_card.select_related():
            portlist_obj = models.PortList.objects.filter(object_pk=card.id, flag=1)
            for port_obj in portlist_obj:
                card_port_info.append(base.get_single_obj_record(port_obj))
        history_data.update({"PortList": card_port_info})
        #
        # 服务器的lv,pv信息(关联StorageVG)
        server_vg = history_data.get("StorageVG", "")
        if len(server_vg) > 0:
            for vg in server_vg:
                vg_id = vg.get("id")
                vg_related_data = common.object_related_data("StorageVG", vg_id)
                print(vg_id)
                if "StorageLV" in history_data.keys():
                    history_data["StorageLV"].append(vg_related_data.get("StorageLV"))
                else:
                    history_data.update({"StorageLV": vg_related_data.get("StorageLV")})

                if "StoragePV" in history_data.keys():
                    history_data["StoragePV"].append(vg_related_data.get("StoragePV"))
                else:
                    history_data.update({"StoragePV": vg_related_data.get("StoragePV")})

        return json.dumps(history_data, cls=common.CJsonEncoder)
    except Exception as e:
        logger.error(e)
        return ""


def get_id_list(project_obj_list, custid):
    """
    根据项目对象列表Projects获取项目列表对象中下的所有服务器id
    :param project_obj_list: 项目Projects对象列表[projects1,projects2...]
    :return: 返回服务器的id列表[1,2,3,4....]
    """
    # 获取指定系统列表中下的所有服务器id列表
    project_business_list = models.Business.objects.filter(project__in=project_obj_list)
    servers = models.R_Server_Business.objects.filter(business__in=project_business_list, server__cust_id=custid)
    server_id_list = [obj.server_id for obj in servers]

    # 对于未设置所属系统的主机也能看到
    has_business_server_list = [obj.get("server_id") for obj in
                                models.R_Server_Business.objects.all().values("server_id")]
    no_business_servers = models.Servers.objects.exclude(id__in=has_business_server_list, cust_id=custid)
    server_id_list.extend([obj.id for obj in no_business_servers])

    return list(set(server_id_list))


@operator_audit_decorator("ServerBoardCard")
def post_server_card(request_data):
    """
    添加、编辑、删除 主机的板卡信息
    :param user: 当前登录的用户
    :param request_data: POST 提交板卡信息
    :return: 返回成功、失败结果
    """
    result = response_format()
    try:
        # print(request_data)
        values = request_data.get("value")
        action = request_data.get("action")
        user = request_data.get("user")
        port_list = list()
        if "ports" in values.keys():
            ports = values.pop("ports")
        else:
            ports = ""
        # 过滤无效的空数据
        values = common.filter_dict(values)

        if action == "new":
            values.update(dict(id=base.nextid(models.ServerBoardCard._meta.db_table, request_data.get("custid")),
                               assetno=common.create_assno(),
                               createuser=user.username, updateuser=user.username))

            card_obj = models.ServerBoardCard.objects.create(**values)
            # 添加端口信息
            if ports:
                port_list = ports.split(",")
                for port in port_list:
                    models.PortList.objects.create(**dict(id=base.nextid(models.PortList._meta.db_table,
                                                                         request_data.get("custid")),
                                                          portname=port,
                                                          object_pk=card_obj.id,
                                                          flag=1))
            result["info"] = "添加成功"
            result["data"] = dict(id=card_obj.id, sn=card_obj.sn,
                                  model=card_obj.model, mac=card_obj.mac, slot=card_obj.slot,
                                  factory=card_obj.factory.name if card_obj.factory else "")
            print("in server.py ...", result)

        if action == "edit":
            cid = values.get("id", 0)
            # 追加更新信息的人和时间
            values.update(dict(updateuser=user.username, updatedate=datetime.now()))
            # 1 更新板卡信息
            models.ServerBoardCard.objects.filter(id=cid).update(**values)

            result["info"] = "更新成功"

        if action == "del":
            del_id = values.get("id", 0)
            # 删除所有端口信息
            models.PortList.objects.filter(object_pk=del_id, porttype=1).delete()
            # 要删除的对象
            models.ServerBoardCard.objects.filter(id=del_id).delete()
            result["info"] = "删除成功"
    except Exception as e:
        logger.error(e)
        result["info"] = "执行错误"
    return result


def host_card_ports_detail(card_id):
    """
    主机详情页面点击板卡详情时,返回板卡的详细信息及板卡对应的所有端口信息
    :param card_id: 要查询的板卡id
    :return:
    """
    result = response_format()
    try:
        host_card_obj = models.ServerBoardCard.objects.get(id=card_id)
        card_info = _server_card_details(host_card_obj)
        ports_info = _server_card_port(host_card_obj)
        result["data"] = dict(card=card_info, ports=ports_info)

    except ObjectDoesNotExist as e:
        result["info"] = "未获取到指定板卡"
        result["category"] = "error"
    except Exception as e:
        logger.error(e)
        result["info"] = "无指定板卡信息"
        result["category"] = "error"

    return result


@operator_audit_decorator("Servers")
def import_excel(request_data, excel_data):
    """
    导入server主机数据
    :param excel_data: excel文件中的数据
    :param request_data:
    :return:
    """
    result_info = response_format()
    custid = request_data.get("custid")
    # 保存主机信息
    server_info = dict()
    # 保存主机关联表信息
    server_related_info = dict(cpu=list(), ip=list(), soft=list(), staffs=list(), business=list())
    # 保存失败的记录信息
    fail_record_info = list()
    try:
        data_type = request_data.get("template_type")
        if data_type == "server":
            data_validate_table = [('BaseAssetType', ['name', 'id']), ('Assets', [['model', 'sn', 'id'], 'id']),
                                   ('BaseNetArea', ['name', 'id']), ('BaseBalanceType', ['typename', 'id']),
                                   ('BaseRunningStatus', ['status', 'id']),
                                   ('Business', [['project__sysname', 'bussname', 'id'], 'id']),
                                   ('BaseSoft', [['type__name', 'name', 'version', 'id'], 'id']),
                                   ('Staffs', ['name', 'id']),
                                   ('BaseRole', ['role_name', 'id'])]
            # 获取所有表格中涉及序列的基表数据对应的ID号
            list_validate_data = base.convert_table_field(data_validate_table, 0, 1, custid)
            # 获取需要验证的主机名
            exists_host_name = base.load_base_table_record("Servers", ["hostname"], custid)
            hostname_list = list(set([obj.get('hostname') for obj in exists_host_name.get("servers")]))
            if hostname_list.count('') > 0:
                hostname_list.remove('')
            # 主机基础数据
            print("import server base info.....")
            for row_data in excel_data:
                err_msg = ""
                host_name = row_data[1].strip()
                # 生成主机表信息
                if not host_name in server_info.keys():
                    servers = dict(hostname=host_name,
                                   type_id=list_validate_data['baseassettype'].get(row_data[2], None),
                                   ownserver_id=list_validate_data['assets'].get(row_data[3], None),
                                   model=str(row_data[4]),
                                   partition=row_data[5],
                                   netarea_id=list_validate_data['basenetarea'].get(row_data[8], None),
                                   balancetype_id=list_validate_data['basebalancetype'].get(row_data[9], None),
                                   tradedate=row_data[10] if row_data[10] else None,
                                   expiredate=row_data[11] if row_data[11] else None,
                                   runningstatus_id=list_validate_data['baserunningstatus'].get(row_data[12], None),
                                   cust_id=custid,
                                   updateuser=request_data.get("user").username if request_data.get("user") else "",
                                   createuser=request_data.get("user").username if request_data.get("user") else ""
                                   )
                    # 验证主机名是否存在
                    if not host_name:
                        err_msg = "{0}, 主机名不能为空".format(err_msg)
                    if host_name in hostname_list:
                        err_msg = "{0}, 主机名 {1} 重复".format(err_msg, host_name)
                    if err_msg:
                        fail_record_info.append({"row": excel_data.index(row_data) + 1, "errmsg": err_msg[1:]})
                        continue
                    # 可以导入,保存主机对象
                    servers.update(dict(id=base.nextid(models.Servers._meta.db_table, custid)))
                    # hostname_list.append(host_name)
                    server_info.update({host_name: models.Servers(**servers)})

                # 记录CPU\内存信息
                if row_data[6]:
                    server_related_info["cpu"].append(dict(
                        id=base.nextid(models.CpuMemory._meta.db_table, custid),
                        cpucount=int(row_data[6]) if row_data and isinstance(row_data[6], float) else None,
                        memory=int(row_data[7]) if row_data and isinstance(row_data[7], float) else None,
                        server_id=server_info[host_name].id,
                        updateuser=request_data.get("user").username if request_data.get("user") else "",
                        createuser=request_data.get("user").username if request_data.get("user") else ""
                    ))

                # business
                if row_data[13]:
                    if not list_validate_data['business'].get(row_data[13], None):
                        err_msg = "{0}, 业务线{1}不存在".format(err_msg, row_data[13])
                    else:
                        server_related_info["business"].append(dict(
                            id=base.nextid(models.R_Server_Business._meta.db_table, custid),
                            business_id=list_validate_data['business'].get(row_data[13], None),
                            server_id=server_info[host_name].id,
                            updateuser=request_data.get("user").username if request_data.get("user") else "",
                            createuser=request_data.get("user").username if request_data.get("user") else ""
                        ))

                # 记录IP信息
                if row_data[14]:
                    server_related_info["ip"].append(dict(
                        id=base.nextid(models.IPConfiguration._meta.db_table, custid),
                        ipaddress=row_data[14] if row_data[14] else None,
                        gatway=row_data[15] if row_data[15] else None,
                        iptype=row_data[16],
                        domain=row_data[17] if row_data[17] else None,
                        vlan=int(row_data[18]) if row_data[18] and isinstance(row_data[18], float) else None,
                        remark=row_data[19],
                        updateuser=request_data.get("user").username if request_data.get("user") else "",
                        createuser=request_data.get("user").username if request_data.get("user") else "",
                        server_id=server_info[host_name].id
                    ))

                # software
                if row_data[20]:
                    if not list_validate_data['basesoft'].get(row_data[20], None):
                        err_msg = "{0}, 软件{1}不存在".format(err_msg, row_data[13])
                    else:
                        server_related_info["soft"].append(dict(
                            id=base.nextid(models.InstalledSoftList._meta.db_table, custid),
                            soft_id=list_validate_data['basesoft'].get(row_data[20], None),
                            server_id=server_info[host_name].id,
                            updateuser=request_data.get("user").username if request_data.get("user") else "",
                            createuser=request_data.get("user").username if request_data.get("user") else ""
                        ))

                # staffs
                if row_data[21]:
                    print(list_validate_data, row_data[21], row_data[22])

                    if not list_validate_data['staffs'].get(row_data[21], None):
                        # 指定的联系人不存在
                        err_msg = "{0}, 联系人{1}不存在".format(err_msg, row_data[21])
                    elif not list_validate_data['baserole'].get(row_data[22], None):
                        err_msg = "{0}, 角色{1}不存在".format(err_msg, row_data[22])
                    else:
                        server_related_info["staffs"].append(dict(
                            id=base.nextid(models.R_Server_Staff._meta.db_table, custid),
                            staff_id=list_validate_data['staffs'].get(row_data[21], None),
                            role_id=list_validate_data['baserole'].get(row_data[22], None),
                            server_id=server_info[host_name].id,
                            updateuser=request_data.get("user").username if request_data.get("user") else "",
                            createuser=request_data.get("user").username if request_data.get("user") else ""
                        ))
                if err_msg.strip():
                    # 更新失败记录
                    fail_record_info.append({"row": excel_data.index(row_data) + 1, "errmsg": err_msg[1:]})

            # 开始批量写入数据库
            models.Servers.objects.bulk_create([v for k, v in server_info.items()])
            models.CpuMemory.objects.bulk_create([models.CpuMemory(**obj) for obj in server_related_info["cpu"]])
            models.R_Server_Business.objects.bulk_create(
                [models.R_Server_Business(**obj) for obj in server_related_info["business"]])
            models.IPConfiguration.objects.bulk_create(
                [models.IPConfiguration(**obj) for obj in server_related_info["ip"]])
            models.InstalledSoftList.objects.bulk_create(
                [models.InstalledSoftList(**obj) for obj in server_related_info["soft"]])
            models.R_Server_Staff.objects.bulk_create(
                [models.R_Server_Staff(**obj) for obj in server_related_info["staffs"]])
            result_info["info"] = "导入完成! 执行{0}条,成功{1}条,失败{2}条!".format(len(excel_data),
                                                                       len(excel_data) - len(fail_record_info),
                                                                       len(fail_record_info))
            result_info["data"] = fail_record_info
            result_info["status"] = False if len(fail_record_info) > 0 else True

        if data_type == "serverstorage":
            # 主机存储数据
            pass
    except Exception as e:
        logger.error(e)
        result_info["info"] = "执行写入失败!"
    print("related_info: ", server_related_info)
    return result_info
