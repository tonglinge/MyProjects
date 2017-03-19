#!/usr/bin/env python
"""
该模块是cmdb中所有关于设备资产信息的处理方法
author: wangsong 2016-09-20
"""

import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from afcat.account.core.permission import operator_audit_decorator
from afcat.api.libs.public import Logger, response_format
from afcat.cmdb import models
from afcat.cmdb.libs import base, common

logger = Logger(__name__)


def get_asset_list(page_index, conditions, custid, perm_id_list=None, per_count=None):
    """
    获取设备资产的基础信息(首页显示的所有资产信息)
    :param conditions: str类型,查询过滤条件,目前仅支持: 按设备编号、资产编号、型号、管理IP模糊匹配
    :param page_index: 当前页码
    :param request: get
    :return: 所有资产信息的列表
    """
    _result_list = list()
    result = response_format()
    page_split_result = {"record": _result_list, "addperm": True}

    try:
        record_list = _load_equipment_list(conditions.strip(), custid, perm_id_list)
        # 获得分页结果
        page_split_result.update(common.page_split(record_list, page_index, per_count))
        # 获取分页后的记录
        equipment_obj_list = page_split_result.get("record")

        if record_list.count() > 0:
            for equipment_obj in equipment_obj_list:
                equipment_info = dict(id=equipment_obj.id, assetname=equipment_obj.assetname,
                                      assetno=equipment_obj.assetno,
                                      unitinfo=equipment_obj.slotindex,
                                      assettype=equipment_obj.assettype.name if equipment_obj.assettype else "",
                                      room=equipment_obj.room.name if equipment_obj.room else "",
                                      cabinet=equipment_obj.cabinet,
                                      model=equipment_obj.model,
                                      netarea=equipment_obj.netarea.name if equipment_obj.netarea else "",
                                      factory=equipment_obj.factory.name if equipment_obj.factory else "",
                                      manageip=equipment_obj.manageip,
                                      powertype=equipment_obj.powertype,
                                      usetype=equipment_obj.usetype,
                                      staffs=base.get_asset_staffs_str(equipment_obj),
                                      portmapcount=_get_portmapping_count(equipment_obj),
                                      changeperm=True,
                                      delperm=True)
                _result_list.append(equipment_info)
        page_split_result.update({"record": _result_list})
    except Exception as e:
        logger.error(e)
        page_split_result.update({"num_pages": 1, "curr_page": 1, "total_count": 0})

    finally:
        result["data"] = page_split_result
        return result


def _get_portmapping_count(equipment_obj):
    """
    获取网络设备的端口隐射数,删除设备时根据端口做判断,有端口隐射信息的无法删除
    :return:
    """
    map_count = 0
    try:
        if not equipment_obj:
            pass
        else:
            # 获取所有板卡对象
            e_card = equipment_obj.related_card.select_related()
            if e_card.count() > 0:
                card_id_list = [c.id for c in e_card]
                # 获取所有板卡的端口信息
                c_ports = models.PortList.objects.filter(flag=2, object_pk__in=card_id_list)
                # 获取该设备的板卡的端口隐射数
                map_count = models.PortMapping.objects.filter(
                    Q(localport__in=c_ports) | Q(targetport__in=c_ports)).count()
    except Exception as e:
        logger.error(e)

    return map_count


def _load_equipment_list(conditions, custid, perm_id_list=None):
    """
    根据条件获取所有设备信息列表
    :type perm_id_list: 允许访问的设备ID列表(权限控制)
    :param conditions: 条件
    :return:
    """
    record_list = list
    try:
        if not conditions and perm_id_list is None:
            # 如果未加条件或superuser
            record_list = models.Equipment.objects.filter(cust_id=custid)
        else:
            if perm_id_list is None:  # superuser
                record_list = models.Equipment.objects.filter(Q(model__contains=conditions) |
                                                              Q(sn__contains=conditions) |
                                                              Q(assetname__contains=conditions) |
                                                              Q(manageip__contains=conditions) |
                                                              Q(netarea__name__contains=conditions) |
                                                              Q(room__name__contains=conditions) |
                                                              Q(cabinet__contains=conditions) |
                                                              Q(assettype__name__contains=conditions),
                                                              cust_id=custid)
            else:
                # 获取指定权限下的设备信息
                record_list = models.Equipment.objects.filter(Q(model__contains=conditions) |
                                                              Q(sn__contains=conditions) |
                                                              Q(assetname__contains=conditions) |
                                                              Q(manageip__contains=conditions) |
                                                              Q(netarea__name__contains=conditions) |
                                                              Q(room__name__contains=conditions) |
                                                              Q(cabinet__contains=conditions) |
                                                              Q(assettype__name__contains=conditions),
                                                              cust_id=custid,
                                                              id__in=perm_id_list)
    except Exception as e:
        logger.error(e)

    return record_list


def get_asset_details(asset_id):
    """
    获取设备的详细信息
    :param asset_id:  设备ID
    :return: 字典格式数据
    """
    result = dict()
    data = response_format()
    try:
        equipment_obj = models.Equipment.objects.get(id=asset_id)
        equipment_info = _equipment_details(equipment_obj)
        equipment_exten_fields = _get_extend_field_values(equipment_obj)
        equipment_staffs = _equipments_staffs_details(equipment_obj)
        equipment_cards = _equipment_card_details(equipment_obj)
        result.update({"server": equipment_info, "staffs": equipment_staffs, "card": equipment_cards,
                       "extend": equipment_exten_fields})
        data["data"] = result
        # data = dict(data=result, status=True, error="")
    except ObjectDoesNotExist as e:
        data["info"] = "未找到指定的设备信息"
        data["status"] = False
        logger.error(e)
    return data


def _equipment_details(equipment_obj):
    """
    设备详情,页面展示列表详情时用
    :param equipment_obj: 设备对象
    :return:
    """
    try:
        _result = dict(id=equipment_obj.id, assetname=equipment_obj.assetname,
                       assetno=equipment_obj.assetno, sn=equipment_obj.sn,
                       assettype=equipment_obj.assettype.name if equipment_obj.assettype else "",
                       room=equipment_obj.room.name if equipment_obj.room else "",
                       roomaddr=equipment_obj.room.address if equipment_obj.room else "",
                       cabinet=equipment_obj.cabinet,
                       tradedate=datetime.strftime(equipment_obj.tradedate,
                                                   "%Y-%m-%d") if equipment_obj.tradedate else "",
                       expiredate=datetime.strftime(equipment_obj.expiredate,
                                                    "%Y-%m-%d") if equipment_obj.expiredate else "",
                       factory=equipment_obj.factory.name if equipment_obj.factory else "",
                       provider=equipment_obj.provider.name if equipment_obj.provider else "",
                       serviceprovider=equipment_obj.serviceprovider.name if equipment_obj.serviceprovider else "",
                       model=equipment_obj.model, powertype=equipment_obj.powertype,
                       usetype=equipment_obj.usetype,
                       netarea=equipment_obj.netarea.name if equipment_obj.netarea else "",
                       status=equipment_obj.status.status if equipment_obj.status else "",
                       manageip=equipment_obj.manageip, portcount=equipment_obj.portcount,
                       slotindex=equipment_obj.slotindex, remark=equipment_obj.remark
                       )
        return _result
    except Exception as e:
        logger.error(e)
        return None


def _get_extend_field_values(equipment_obj):
    """
    获取网络设备的扩展(自定义属性)信息
    :param equipment_obj: 设备对象
    :return: 扩展属性字典[{'label':'IOS版本','value':'v4.00.18,build0689b689,140731'},...]
    """
    _result = list()
    try:
        # 获取所有自定义字段信息
        customer_fields_obj = common.get_table_extend_fields(equipment_obj.cust_id, "Equipment")
        # 获取各字段的值
        if len(customer_fields_obj) > 0:
            for field in customer_fields_obj:
                field_label = field.get("label")
                field_value = getattr(equipment_obj, field.get("to_field"))
                _result.append({'label': field_label, 'value': field_value})
    except Exception as e:
        logger.error(e)
    return _result


def _equipments_staffs_details(equipment_obj):
    """
    获取设备资产的联系人信息
    :param equipment_obj: 资产对象
    :return:
    """
    _staffs_list = list()
    staffs_obj_List = equipment_obj.related_staffs.select_related()
    if staffs_obj_List.count() > 0:
        for staffs_obj in staffs_obj_List:
            _staff_dict = dict(id=staffs_obj.id,
                               staff_id=staffs_obj.staff_id,
                               name=staffs_obj.staff.name,
                               mobile=staffs_obj.staff.mobile,
                               tel=staffs_obj.staff.tel,
                               email=staffs_obj.staff.email,
                               role=staffs_obj.role.role_name if staffs_obj.role else "",
                               remark=staffs_obj.remark
                               )
            _staffs_list.append(_staff_dict)
    return _staffs_list


def _equipment_card_details(equipment_obj):
    """
    获取网络设备对应的板卡及端口映射关系
    :param equipment_obj: 所属板卡对象
    :return: 板卡信息[{"assetno":"4938493","sn":"sn0001","slot":1,"model":"xxx",
                    "port":[{"localport":"port0","targetport":"pppp","targettype":"host001:网卡(网卡0)}，{}，{} ]}, {}  ]
    """
    card_list = list()
    try:
        all_board_card = models.EquipmentBoardCard.objects.filter(equipment=equipment_obj)
        for card_obj in all_board_card:
            # 网络设备的板卡信息
            card_info = dict(id=card_obj.id, assetno=card_obj.assetno, sn=card_obj.sn, cardname=card_obj.cardname,
                             slot=card_obj.slot, model=card_obj.model, remark=card_obj.remark)
            card_ports = _equipment_port_list(card_obj)
            # print(card_ports)
            card_info.update({"portcount": len(card_ports.get("ports"))})
            card_info.update(card_ports)
            card_list.append(card_info)

        return card_list
    except Exception as e:
        logger.error(e)
        return ""


def _equipment_port_list(card_obj):
    """
    获取板卡对应的端口以及端口的映射信息
    :param card_obj:
    :return: 返回端口映射表
    """
    port_map_detail = dict(ports=list(), maps=list())
    try:
        # 获取该板卡下的所有端口信息
        ports_objs = models.PortList.objects.filter(flag=2, object_pk=card_obj.id).all()
        # 获取端口映射信息
        if ports_objs.count() > 0:
            port_maps = models.PortMapping.objects.filter(Q(localport__in=ports_objs) | Q(targetport__in=ports_objs))
            # 加载端口信息
            for port in ports_objs:
                if port.related_local.select_related().count() > 0 or port.related_target.select_related().count() > 0:
                    port_map_detail["ports"].append(dict(id=port.id, portname=port.portname, porttype=port.porttype,
                                                         vlan=port.vlan, remark=port.remark, hasmap=1))
                else:
                    port_map_detail["ports"].append(dict(id=port.id, portname=port.portname, porttype=port.porttype,
                                                         vlan=port.vlan, remark=port.remark, hasmap=0))

            if port_maps.count() > 0:
                for mapping in port_maps:
                    # 如果映射关系表的端口是本端
                    if mapping.localport in ports_objs:
                        target_port = mapping.targetport
                        local_port = mapping.localport
                    else:
                        target_port = mapping.localport
                        local_port = mapping.targetport
                    # 获取映射信息
                    if target_port:
                        # 获取对端设备的详细信息
                        target_card_info = _get_card_by_portid(target_port.id)
                        map_info = dict(targetportid=target_port.id, targetportname=target_port.portname,
                                        targetporttype=target_port.porttype, targetasset=target_card_info,
                                        remark=target_port.remark, mapid=mapping.id)
                    else:
                        map_info = dict(targetportid="", targetportname="", targetporttype="", targetasset="",
                                        mapid=mapping.id)

                    if local_port:
                        map_info.update(dict(localportname=local_port.portname))

                    port_map_detail["maps"].append(map_info)
        else:
            pass

    except Exception as e:
        logger.error(e)
    return port_map_detail


def _get_card_by_portid(port_id):
    """
    通过portlist表中的id获取所属的设备的信息
    :param port_id:  端口id
    :return: 返回设备的信息(str)
    """
    try:
        port_obj = models.PortList.objects.get(id=port_id)
        if port_obj.flag == 1:
            # 服务器资产的板卡端口
            card_obj = models.ServerBoardCard.objects.get(id=port_obj.object_pk)
            asset_info = "{0}:{1}".format(card_obj.server.hostname,
                                          "网卡" if card_obj.cardtype == 1 else "存储卡")

        if port_obj.flag == 2:
            # 设备资产的板卡端口
            card_obj = models.EquipmentBoardCard.objects.get(id=port_obj.object_pk)
            asset_info = "{0}:{1}({2})".format(card_obj.equipment.assetname, card_obj.equipment.model,
                                               card_obj.cardname)

        return asset_info
    except Exception as e:
        logger.error(e)
        return ""


def get_asset_base_info(sid):
    """
    获取设备资产的信息,对于关联关系的仅显示id，编辑时用
    :param sid: 设备资产id
    :return:
    """
    try:
        equipment_obj = models.Equipment.objects.get(id=sid)
        # 获取基础数据
        equipment_info = dict(id=equipment_obj.id,
                              assetname=equipment_obj.assetname,
                              assetno=equipment_obj.assetno, sn=equipment_obj.sn,
                              assettype=equipment_obj.assettype_id, room=equipment_obj.room_id,
                              cabinet=equipment_obj.cabinet, powertype=equipment_obj.powertype,
                              usetype=equipment_obj.usetype,
                              datacenter=equipment_obj.room.center_id if equipment_obj.room else "",
                              tradedate=datetime.strftime(equipment_obj.tradedate,
                                                          "%Y-%m-%d") if equipment_obj.tradedate else "",
                              expiredate=datetime.strftime(equipment_obj.expiredate,
                                                           "%Y-%m-%d") if equipment_obj.expiredate else "",
                              factory=equipment_obj.factory_id, model=equipment_obj.model,
                              provider=equipment_obj.provider_id, serviceprovider=equipment_obj.serviceprovider_id,
                              netarea=equipment_obj.netarea_id, status=equipment_obj.status_id,
                              manageip=equipment_obj.manageip, portcount=equipment_obj.portcount,
                              slotindex=equipment_obj.slotindex, remark=equipment_obj.remark
                              )
        # 获取用户自定义扩展字段的数据
        extend_fields = common.get_table_extend_fields(equipment_obj.cust_id, equipment_obj._meta.object_name)
        if len(extend_fields) > 0:
            for field in extend_fields:
                equipment_info.update({field.get("to_field"): getattr(equipment_obj, field.get("to_field"))})
        return equipment_info
    except ObjectDoesNotExist as e:
        logger.error("未找到指定ID的网络设备资产信息")
        return ""
    except Exception as e:
        logger.error(e)
        return ""


def load_related_base_configuration(custid):
    """
    获取编辑或添加时依赖的基表数据
    :return: 字典
    """
    related_tables = ["BaseDataCenter", "BaseMachineRoom", "BaseNetArea",
                      "BaseAssetCabinet", "BaseFactory", "BaseAssetStatus", "BaseEquipmentType"]
    related_data = base.get_base_data(custid, related_tables)
    # 获取自定义的扩展字段
    extend_field = common.get_table_extend_fields(custid, "Equipment")
    related_data.update({"extend": extend_field})
    return related_data


@operator_audit_decorator("Equipment")
def edit_asset(data):
    """
    添加 和 修改设备资产信息
    :param action: 要执行的动作 edit / add
    :param sid:  如果是edit, 资产id
    :param data: post的数据
    :return:
    """
    result = response_format()
    try:
        # print("e data:", data)
        asset_data = data.get("value", "")
        action = data.get("action")
        sid = asset_data.get("id", 0)
        user = data.get("user")
        custid = data.get("custid")

        if asset_data:
            asset_data = common.filter_dict(asset_data)
        # print(asset_data)
        if action == "edit":
            asset_data.update(dict(updateuser=user.username, updatedate=datetime.now()))
            asset_obj = models.Equipment.objects.filter(id=int(sid))
            if asset_obj.first().manageip != asset_data.get("manageip", ""):
                result = data_validate(asset_data.get("sn", ""), asset_data.get("manageip", ""), custid, sid)
                if result["status"]:
                    common.change_ip_status(custid, asset_obj.first().manageip, "ALLOCATED")
                    common.change_ip_status(custid, asset_data.get("manageip", ""), "USED", asset_obj.first().__str__())

                    asset_obj.update(**asset_data)
                    result["info"] = "修改成功"
            else:
                asset_obj.update(**asset_data)
                result["info"] = "修改成功"

        elif action == "new":
            # 检查sn是否重复
            result = data_validate(asset_data.get("sn", ""), asset_data.get("manageip", ""), custid)
            if result["status"]:
                asset_data.update(dict(id=base.nextid(models.Equipment._meta.db_table, custid),
                                       updateuser=user.username,
                                       createuser=user.username,
                                       cust_id=custid))
                asset_no = common.create_assno()
                asset_data.update({"assetno": asset_no})
                new_asset = models.Equipment.objects.create(**asset_data)
                # 修改IP地址的使用状态为已使用
                common.change_ip_status(custid, asset_data.get("manageip"), "USED", new_asset.__str__())
                result["data"] = dict(id=new_asset.id, equipmentname=new_asset.assetname)
                result["info"] = "添加成功"

        elif action == "delete":
            asset_obj = models.Equipment.objects.filter(id=sid)
            if not asset_obj:
                result["info"] = "未找到指定记录"
                result["status"] = False
                result["category"] = "error"
            else:
                # 获取该网络设备记录的所有依赖表记录
                related_data = load_asset_related_data(sid)
                # 保存历史数据
                base.save_del_history("Equipment", related_data, user, custid)
                # 删除板卡端口数据
                if len(json.loads(related_data).get("PortList", [])) > 0:
                    port_id_list = list()
                    for port in json.loads(related_data).get("PortList"):
                        port_id_list.append(port.get("id"))
                    # print(port_id_list)
                    models.PortList.objects.filter(id__in=port_id_list).delete()
                # 修改IP地址的使用状态为待回收
                common.change_ip_status(custid, asset_obj.first().manageip, "RECOVER")
                # 删除记录
                asset_obj.delete()
                result["info"] = "删除成功"
    except Exception as e:
        result["status"] = False
        result["category"] = "error"
        result["info"] = "系统错误!"
        logger.error(e)
    return result


def data_validate(sn, manageip, custid, obj_id=None):
    """
    验证提交的sn和ip地址的合法性
    :param sn:
    :param manageip:
    :param custid:
    :param obj_id:
    :return:
    """
    result = response_format()
    if _check_exists(sn, manageip, custid, obj_id):
        result["info"] = "SN或管理IP地址重复!"
        result["category"] = "warning"
        result["status"] = False
    else:
        if not common.ip_allocated(manageip, custid):
            result["info"] = "管理IP未分配或已被使用!"
            result["category"] = "error"
            result["status"] = False
        else:
            result["status"] = True
    return result


def _check_exists(sn, manageip, custid, obj_id=None):
    """
    添加和修改网络设备时检测时检测重复记录,主要检测sn、manageip
    :param sn: sn编号
    :param manageip: 管理IP
    :param custid: 客户编号,同一个客户下的不可以重复,不同客户的可以重复
    :param obj_id: 对象id，编辑的时候判断除自身之外的其它记录
    :return: 有重复记录True / 无重复记录False
    """
    exists_flag = False
    try:
        eq = models.Equipment.objects.filter(sn=sn, manageip=manageip, cust_id=custid)
        if obj_id:
            eq = eq.exclude(id=obj_id)
        if eq.count() > 0:
            exists_flag = True
    except Exception as e:
        logger.error(e)
    return exists_flag


def export_excel(custid, **kwargs):
    """
    导出设备excel功能
    :param kwargs:
    :return:
    """
    from afcat.cmdb.libs.excel import Excel
    conditions = kwargs.get("conditions", "")[0]
    e_obj_list = _load_equipment_list(conditions, custid)
    try:
        # create excel file object
        excel_obj = Excel()
        _excel_export_data(excel_obj, e_obj_list)
    except Exception as e:
        logger.error(e)
    finally:
        excel_obj.close()
        return excel_obj.file


# def _excel_export_main_info(excel_obj, record_obj_list):
#     """
#     导出网络设备的基本信息
#     :return:
#     """
#     excel_title = [
#         ("序号", 5), ("设备名称", 20), ("设备类型", 15), ("应用用途", 25), ("管理IP", 15), ("所属机房", 25), ("所在机柜", 10),
#         ("U位", 10), ("设备型号", 20), ("序列号", 25), ("电源数量", 10), ("联系人", 20), ("网络区域", 20), ("厂商", 25),
#         ("购买日期", 15), ("过保日期", 15), ("状态", 15), ("备注", 20)
#     ]
#     excel_rows = list()
#     row_index = 1
#     try:
#         sheet_obj = excel_obj.create_sheet(u"网络设备")
#         for e_obj in record_obj_list:
#             row = []
#             info = get_asset_details(e_obj.id)["data"]
#             asset_info = info.get("server", "")
#             asset_staff_info = info.get("staffs", "")
#             extend_field = common.list_to_dict(info.get("extend"), 'label', 'value')  # 扩展字段
#             print(extend_field)
#             # index
#             row.append(row_index)
#             # assetname
#             row.append(asset_info.get("assetname"))
#             # assettype
#             row.append(asset_info.get("assettype"))
#             # assetusetype
#             row.append(asset_info.get("usetype"))
#             # manageip
#             row.append(asset_info.get("manageip"))
#             # room
#             row.append(asset_info.get("room"))
#             # cabinet
#             row.append(asset_info.get("cabinet"))
#             # slotindex
#             row.append(asset_info.get("slotindex"))
#             # model
#             row.append(asset_info.get("model"))
#             # sn
#             row.append(asset_info.get("sn"))
#             # powercount
#             row.append(asset_info.get("powertype"))
#             # staffs
#             row.append(common.convert_dict_to_str(asset_staff_info, ["name", "role", "mobile"], "/"))
#             # netarea
#             row.append(asset_info.get("netarea"))
#             # factory
#             row.append(asset_info.get("factory"))
#             # tradedate
#             row.append(asset_info.get("tradedate"))
#             # expiredate
#             row.append(asset_info.get("expiredate"))
#             # status
#             row.append(asset_info["status"])
#             # remark
#             row.append(asset_info["remark"])
#
#             excel_rows.append(row)
#
#             row_index += 1
#
#         excel_obj.write_title(excel_title, sheet_obj)
#         excel_obj.write_row(excel_rows, sheet_obj)
#     except Exception as e:
#         logger.error(e)


def _excel_export_data(excel_obj, record_obj_list):
    """
    专门针对太原银行进行定制的excel导出
    :param excel_obj:
    :param record_obj_list:
    :return:
    """
    excel_title = [
        ("序号", 5), ("监控策略", 20), ("监控时间段", 15), ("设备管理IP", 15), ("团体字", 15), ("责任人", 20), ("逻辑区域", 15),
        ("机房位置", 20), ("设备类型", 10), ("管理组", 5), ("管理机构", 10), ("所属机构", 10), ("地域", 10), ("监控需求", 10),
        ("特殊需求", 10), ("别名", 10), ("用途", 8), ("房间位置", 20), ("机柜编号", 10), ("机内位置", 10), ("带内管理地址", 10),
        ("带外管理地址", 10), ("所属环境", 10), ("服务开始日期", 10), ("过保时间", 10), ("供应商", 5), ("服务提供商", 10),
        ("状态", 8), ("服务级别", 8), ("厂商", 10), ("设备型号", 8), ("设备序列号", 20), ("名称", 20), ("IOS版本", 20)
    ]
    excel_rows = list()
    row_index = 1
    try:
        sheet_obj = excel_obj.create_sheet(u"网络设备")
        for e_obj in record_obj_list:
            row = []
            info = get_asset_details(e_obj.id)["data"]
            print(info)
            asset_info = info.get("server", "")
            asset_staff_info = info.get("staffs", "")
            extend_field = common.list_to_dict(info.get("extend"), 'label', 'value')  # 扩展字段
            # index
            row.append(row_index)
            # 监控策略
            row.append(extend_field.get(excel_title[1][0]))
            # 监控时间段
            row.append(extend_field.get(excel_title[2][0]))
            # manageip
            row.append(asset_info.get("manageip"))
            # 团体字
            row.append(extend_field.get(excel_title[4][0]))
            # staffs
            row.append(common.convert_dict_to_str(asset_staff_info, ["name", "role", "mobile"], "/"))
            # 逻辑区域
            row.append(extend_field.get(excel_title[6][0]))
            # room
            row.append(asset_info.get("room"))
            # assettype
            row.append(asset_info.get("assettype"))
            # 管理组
            row.append(extend_field.get(excel_title[9][0]))
            # 管理机构
            row.append(extend_field.get(excel_title[10][0]))
            # 所属机构
            row.append(extend_field.get(excel_title[11][0]))
            # 地域
            row.append(extend_field.get(excel_title[12][0]))
            # 监控需求
            row.append(extend_field.get(excel_title[13][0]))
            # 特殊需求
            row.append(extend_field.get(excel_title[14][0]))
            # 别名
            row.append(extend_field.get(excel_title[15][0]))
            # assetusetype
            row.append(asset_info.get("usetype"))
            # roomaddress
            row.append(asset_info.get("roomaddr"))
            # cabinet
            row.append(asset_info.get("cabinet"))
            # slotindex
            row.append(asset_info.get("slotindex"))
            # 带内地址
            row.append(extend_field.get(excel_title[20][0]))
            # 带外地址
            row.append(extend_field.get(excel_title[21][0]))
            # netarea
            row.append(asset_info.get("netarea"))
            # tradedate
            row.append(asset_info.get("tradedate"))
            # expiredate
            row.append(asset_info.get("expiredate"))
            # provider
            row.append(asset_info.get("provider"))
            # service provider
            row.append(asset_info.get("serviceprovider"))
            # status
            row.append(asset_info["status"])
            # 服务级别
            row.append(extend_field.get(excel_title[28][0]))
            # factory
            row.append(asset_info.get("factory"))
            # model
            row.append(asset_info.get("model"))
            # sn
            row.append(asset_info.get("sn"))
            # assetname
            row.append(asset_info.get("assetname"))
            # remark
            row.append(extend_field.get(excel_title[33][0]))

            excel_rows.append(row)

            row_index += 1

        excel_obj.write_title(excel_title, sheet_obj)
        excel_obj.write_row(excel_rows, sheet_obj)
    except Exception as e:
        logger.error(e)


def load_asset_related_data(eid):
    """
    获得所有设备资产及关联数据的值
    :param eid: 资产设备id
    :return: json格式
    """
    all_data = dict()
    try:
        # 获取设备的记录数据
        asset_objs = models.Equipment.objects.get(id=eid)
        equipment_info = base.get_single_obj_record(asset_objs)
        all_data.update({"Equipment": equipment_info})

        # 获取g该记录关联的所有数据
        related_data = common.object_related_data("Equipment", eid)
        all_data.update(related_data)

        # 获取网络设备记录中关联板卡的端口信息
        # print(all_data)
        card_port_info = list()
        for card in asset_objs.related_card.select_related():
            portlist_obj = models.PortList.objects.filter(object_pk=card.id, flag=2)
            for port_obj in portlist_obj:
                card_port_info.append(base.get_single_obj_record(port_obj))

        all_data.update({"PortList": card_port_info})
    except Exception as e:
        logger.error(e)

    return json.dumps(all_data, cls=common.CJsonEncoder)


def get_id_list(type_obj_list, custid):
    """
    根据设备类型获取设备类型下的所有设备id
    :param type_obj_list: 设备类型对象列表
    :return: 设备id列表
    """
    id_list = list()
    equipments = models.Equipment.objects.filter(assettype__in=type_obj_list, cust_id=custid).values("id")
    for e in equipments:
        id_list.append(e.get("id", 0))
    return list(set(id_list))


@operator_audit_decorator("EquipmentBoardCard")
def post_boardcard(post_data, user):
    """
    添加,修改,删除网络设备板卡信息
    :param post_data:
    :return:
    """
    result = response_format()
    try:
        action = post_data.get("action")
        values = post_data.get("value")
        custid = post_data.get("custid")
        values = common.filter_dict(values)
        if action == "new":
            if "ports" in values.keys():
                ports = values.pop("ports")
            else:
                ports = ""
            # 更新id、assetno等信息
            values.update(dict(id=base.nextid(models.EquipmentBoardCard._meta.db_table, custid),
                               assetno=common.create_assno(),
                               createuser=user.username, updateuser=user.username))
            # 创建板卡信息
            boardcard = models.EquipmentBoardCard.objects.create(**values)
            # 插入端口到端口表
            if ports:
                portlist = ports.split(",")
                portlist.sort()
                for port in portlist:
                    if port:
                        port_obj = models.PortList.objects.create(
                            **dict(id=base.nextid(models.PortList._meta.db_table, custid),
                                   object_pk=boardcard.id,
                                   portname=port,
                                   flag=2))
            new_card_info = dict(id=boardcard.id, assetno=boardcard.assetno, sn=boardcard.sn, model=boardcard.model,
                                 cardname=boardcard.cardname, slot=boardcard.slot, remark=boardcard.remark)
            # 返回卡端口及映射信息
            new_card_info.update(_equipment_port_list(boardcard))
            result["info"] = "添加成功"
            result["data"] = new_card_info

        if action == "edit":
            cid = values.get("id", 0)
            if not cid:
                result["info"] = "参数错误"
                result["category"] = "error"
                result["status"] = False
                return result
            else:
                card_obj = models.EquipmentBoardCard.objects.filter(id=cid)
                card_obj.update(**values)
                result["info"] = "修改成功"

        if action == "delete":
            cid = values.get("id", 0)
            # 获取板卡对象
            card_obj = models.EquipmentBoardCard.objects.filter(id=cid).first()
            # 删除板卡对应的所有端口，同时关联的所有映射表也同时删除
            models.PortList.objects.filter(object_pk=card_obj.id, flag=2).delete()
            # 删除卡记录
            card_obj.delete()
            result["info"] = "删除成功"
    except Exception as e:
        logger.error(e)
        result["info"] = "系统错误"
        result["category"] = "error"
    return result


def get_port_map_info(request_data, custid):
    """
    根据请求的设备类型，返回端口信息,模糊搜索对应设备
    :param request_data: {"porttype":1, "condition":"xxxxxx"}
    :return:
    """
    target_port_list = list()
    try:
        card_dict_list = dict()
        porttype = int(request_data.get("porttype", 2))
        condition = request_data.get("condition", "")
        if porttype == 1:
            # 主机设备,获取模糊搜索条件的设备下的所有板卡信息
            servers_obj = models.Servers.objects.filter(hostname__contains=condition, cust_id=custid)
            for serv in servers_obj:
                serv_card_obj = serv.related_card.select_related()
                for card in serv_card_obj:
                    card_dict_list.update({card.id: "{0}:{1}".format(serv.hostname,
                                                                     "网卡" if card.cardtype == 1 else "存储卡")})
        if porttype == 2:
            # 网络设备端口
            equipment_obj = models.Equipment.objects.filter(
                Q(sn__contains=condition) | Q(assetname__contains=condition), cust_id=custid)
            for equipment in equipment_obj:
                ecard_obj = equipment.related_card.select_related()
                for card in ecard_obj:
                    card_dict_list.update({card.id: "{0}:{1}({2})".format(equipment.assetname,
                                                                          equipment.model,
                                                                          card.cardname)})
        # 获取已经建立匹配的端口ID
        mapped_id = list()
        all_map_rec = models.PortMapping.objects.all().values("localport_id", "targetport_id")
        for rec in all_map_rec:
            mapped_id.append(rec.get("localport_id"))
            mapped_id.append(rec.get("targetport_id"))

        # 获取端口信息
        port_list = models.PortList.objects.filter(flag=porttype, object_pk__in=list(card_dict_list.keys()),
                                                   ).exclude(id__in=mapped_id)
        for port in port_list:
            target_port_list.append(dict(id=port.id, portname=port.portname,
                                         portasset=card_dict_list.get(port.object_pk, ""),
                                         porttype=port.porttype))

    except Exception as e:
        logger.error(e)

    return target_port_list


@operator_audit_decorator("PortMapping")
def post_port_map_info(request_data):
    """
    添加、编辑、删除端口映射信息,提交的数据包括：板卡ID，端口名
    :param request_data: {"value":{"portname":"E1/0","card_id":10011,"targetport_id":10012,"remark":"xxx"},
                        "action":"edit/new/delete",
                        }
    :return:
    """
    result = response_format()
    try:
        # 获取端口对应的ID
        post_data = request_data.get("value", {})
        action = request_data.get("action", "")
        custid = request_data.get("custid")
        if not post_data or not action:
            result["info"] = "参数错误"
            result["category"] = "error"
            result["status"] = False
        else:
            if action == "delete":
                models.PortMapping.objects.filter(id=int(post_data.get("id"))).delete()
                result["info"] = "删除成功"
            else:
                # 获取端口ID
                local_port = models.PortList.objects.filter(object_pk=int(post_data.get("card_id", 0)),
                                                            portname=post_data.get("portname").strip(),
                                                            flag=2).first()
                if not local_port:
                    result["info"] = "未找到指定端口"
                    result["status"] = False
                else:
                    if action == "new":
                        # 查找本地端口或对端端口是否已经存在映射
                        check_port_id = [local_port.id, int(post_data.get("targetport_id", 0))]
                        mapped_obj = models.PortMapping.objects.filter(Q(localport_id__in=check_port_id) |
                                                                       Q(targetport_id__in=check_port_id),
                                                                       id__startswith=custid
                                                                       )
                        if mapped_obj.count() > 0:
                            # 本端或对端端口已经有映射关系
                            result["info"] = "指定端口已建立映射关系"
                            result["category"] = "warning"
                            result["status"] = True
                        else:
                            new_obj = models.PortMapping.objects.create(
                                **dict(id=base.nextid(models.PortMapping._meta.db_table, custid),
                                       localport_id=local_port.id,
                                       targetport_id=int(post_data.get("targetport_id", 0)),
                                       remark=post_data.get("remark", ""))
                            )
                            result["info"] = "添加成功"
                            result["data"] = dict(mapid=new_obj.id, id=new_obj.id, localport_id=new_obj.localport_id,
                                                  targetport_id=new_obj.targetport_id)

                    if action == "edit":
                        edit_data = dict(id=post_data.get("id"), localport_id=local_port.id,
                                         targetport_id=int(post_data.get("targetport_id", 0)),
                                         remark=post_data.get("remark", ""))
                        models.PortMapping.objects.filter(id=int(post_data.get("id"))).update(**edit_data)

                        result["info"] = "修改成功"

    except Exception as e:
        logger.error(e)
        result["info"] = "执行错误"
        result["status"] = False
    print(result)
    return result


# @operator_audit_decorator("Equipment")
# def import_excel(request_data, excel_data):
#     """
#     导入Excel文件到数据库
#     :param excel_data:
#     :param request_data:
#     :return:
#     """
#     save_record = list()
#     fail_record = list()
#     import_result = response_format()
#     custid = request_data.get("custid")
#     print(excel_data)
#     try:
#         base_table = [('BaseEquipmentType', ['name', 'id']), ('BaseDataCenter', ['name', 'id']),
#                       ('BaseMachineRoom', ['name', 'id']), ('Staffs', ['name', 'id']),
#                       ('BaseAssetStatus', ['status', 'id']), ('BaseNetArea', ['name', 'id']),
#                       ('BaseFactory', ['name', 'id'])
#                       ]
#         # 导入数据中的下拉框值对应的ID字典
#         base_table_id_dict = base.convert_table_field(base_table, 0, 1, custid)
#
#         # 获取当前asset表中的已存在所有sn与管理IP
#         list_asset_info = base.load_base_table_record("Equipment", ["sn", "manageip"], custid)
#         sn_list = list(set([obj.get('sn') for obj in list_asset_info.get("equipment")]))
#         if sn_list.count('') > 0:
#             sn_list.remove('')
#         ip_list = list(set([obj.get('manageip') for obj in list_asset_info.get("equipment")]))
#         if ip_list.count('') > 0:
#             ip_list.remove('')
#
#         # 开始导入数据
#         for obj in excel_data:
#             assets_obj_info = dict(assetname=obj[0], usetype=obj[1],
#                                    assettype_id=base_table_id_dict['baseequipmenttype'].get(obj[2], None),
#                                    room_id=base_table_id_dict['basemachineroom'].get(obj[4], None),
#                                    cabinet=int(obj[5]) if isinstance(obj[5], float) else obj[5],
#                                    manageip=obj[6],
#                                    slotindex=int(obj[7]) if isinstance(obj[7], float) else obj[7],
#                                    model=obj[8],
#                                    sn=int(obj[9]) if isinstance(obj[9], float) else obj[9],
#                                    powertype=obj[10],
#                                    factory_id=base_table_id_dict['basefactory'].get(obj[11], None),
#                                    netarea_id=base_table_id_dict['basenetarea'].get(obj[12], None),
#                                    tradedate=obj[13] if obj[13] else None,
#                                    expiredate=obj[14] if obj[14] else None,
#                                    status_id=base_table_id_dict["baseassetstatus"].get(obj[15], None),
#                                    remark=obj[16],
#                                    id=base.nextid(models.Equipment._meta.db_table, custid),
#                                    updateuser=request_data.get("user").username,
#                                    createuser=request_data.get("user").username,
#                                    # createuser='cmdb', updateuser='cmdb',
#                                    cust_id=custid, assetno=common.create_assno()
#                                    )
#             # 开始校验数据
#             # sn, manageip
#             err_msg = ""
#             if not assets_obj_info.get("assetname"):
#                 err_msg = "{0}| 设备名称不能为空 ".format(err_msg)
#
#             if assets_obj_info.get('sn') in sn_list:
#                 err_msg = "{0}| 序列号 {1} 已存在 ".format(err_msg, assets_obj_info.get("sn"))
#
#             if assets_obj_info.get('manageip') in ip_list:
#                 err_msg = "{0}| 管理IP {1} 已存在 ".format(err_msg, assets_obj_info.get("manageip"))
#             if not assets_obj_info.get('model'):
#                 err_msg = "{0}| 设备型号不能为空 ".format(err_msg)
#
#             if err_msg:
#                 fail_record.append({"row": excel_data.index(obj) + 1, "errmsg": err_msg.strip()[1:]})
#                 continue
#             else:
#                 if assets_obj_info.get('sn'):
#                     sn_list.append(assets_obj_info.get('sn'))
#                 if assets_obj_info.get('manageip'):
#                     ip_list.append(assets_obj_info.get('manageip'))
#
#             # 校验没问题就加入到要创建的列表中
#             # save_record.append(models.Equipment(**assets_obj_info))
#
#         # 将对象批量写入库
#         # models.Equipment.objects.bulk_create(save_record)
#         import_result["info"] = "导入完成!执行{0}条 成功{1}条, 失败{2}条.".format(len(excel_data), len(save_record),
#                                                                      len(fail_record))
#         import_result["data"] = fail_record
#         import_result["status"] = False if len(fail_record) > 0 else True
#
#     except Exception as e:
#         logger.error(e)
#         import_result["info"] = "导入错误!"
#
#     return import_result

def import_excel(request_data, excel_data):
    """
    针对太原银行导入Excel文件到数据库
    :param excel_data:
    :param request_data:
    :return:
    """
    save_record = list()
    fail_record = list()
    import_result = response_format()
    custid = request_data.get("custid")
    print(excel_data)
    try:
        base_table = [('BaseEquipmentType', ['name', 'id']), ('BaseDataCenter', ['name', 'id']),
                      ('BaseMachineRoom', ['name', 'id']), ('Staffs', ['name', 'id']),
                      ('BaseAssetStatus', ['status', 'id']), ('BaseNetArea', ['name', 'id']),
                      ('BaseFactory', ['name', 'id'])
                      ]
        # 导入数据中的下拉框值对应的ID字典
        base_table_id_dict = base.convert_table_field(base_table, 0, 1, custid)
        # 获取自定义扩展字段信息
        extend_field = common.list_to_dict(common.get_table_extend_fields(custid, "Equipment"), 'label', 'to_field')

        # 获取当前asset表中的已存在所有sn与管理IP
        list_asset_info = base.load_base_table_record("Equipment", ["sn", "manageip"], custid)
        sn_list = list(set([obj.get('sn') for obj in list_asset_info.get("equipment")]))
        if sn_list.count('') > 0:
            sn_list.remove('')
        ip_list = list(set([obj.get('manageip') for obj in list_asset_info.get("equipment")]))
        if ip_list.count('') > 0:
            ip_list.remove('')

        # 开始导入数据
        for obj in excel_data:
            assets_obj_info = dict(
                customer001=obj[1], customer002=obj[2], manageip=obj[3], customer003=obj[4],
                customer004=obj[6], room_id=base_table_id_dict['basemachineroom'].get(obj[7], None),
                assettype_id=base_table_id_dict['baseequipmenttype'].get(obj[8], None),
                customer005=obj[9], customer006=obj[10], customer007=obj[11],
                customer008=obj[12], customer009=obj[13], customer016=obj[14], customer010=obj[15],
                usetype=obj[16], cabinet=int(obj[17]) if isinstance(obj[17], float) else obj[17],
                slotindex=int(obj[18]) if isinstance(obj[18], float) else obj[18],
                customer011=obj[19], customer012=obj[20],
                netarea_id=base_table_id_dict['basenetarea'].get(obj[21], None),
                tradedate=obj[22] if obj[22] else None,
                expiredate=obj[23] if obj[23] else None,
                provider_id=base_table_id_dict['basefactory'].get(obj[24], None),
                serviceprovider_id=base_table_id_dict['basefactory'].get(obj[25], None),
                status_id=base_table_id_dict["baseassetstatus"].get(obj[26], None),
                customer013=obj[27],
                factory_id=base_table_id_dict['basefactory'].get(obj[28], None),
                model=obj[29],
                sn=int(obj[30]) if isinstance(obj[30], float) else obj[30],
                assetname=obj[31], customer015=obj[32],
                id=base.nextid(models.Equipment._meta.db_table, custid),
                updateuser=request_data.get("user").username,
                createuser=request_data.get("user").username,
                # createuser='cmdb', updateuser='cmdb',
                cust_id=custid, assetno=common.create_assno()
            )
            # 开始校验数据
            # sn, manageip
            err_msg = ""
            if not assets_obj_info.get("assetname"):
                err_msg = "{0}| 设备名称不能为空 ".format(err_msg)

            if assets_obj_info.get('sn') in sn_list:
                err_msg = "{0}| 序列号 {1} 已存在 ".format(err_msg, assets_obj_info.get("sn"))

            if assets_obj_info.get('manageip') in ip_list:
                err_msg = "{0}| 管理IP {1} 已存在 ".format(err_msg, assets_obj_info.get("manageip"))
            if not assets_obj_info.get('model'):
                err_msg = "{0}| 设备型号不能为空 ".format(err_msg)

            if err_msg:
                fail_record.append({"row": excel_data.index(obj) + 1, "errmsg": err_msg.strip()[1:]})
                continue
            else:
                if assets_obj_info.get('sn'):
                    sn_list.append(assets_obj_info.get('sn'))
                if assets_obj_info.get('manageip'):
                    ip_list.append(assets_obj_info.get('manageip'))

                # 校验没问题就加入到要创建的列表中
                save_record.append(models.Equipment(**assets_obj_info))

        # 将对象批量写入库
        models.Equipment.objects.bulk_create(save_record)
        import_result["info"] = "导入完成!执行{0}条 成功{1}条, 失败{2}条.".format(len(excel_data), len(save_record),
                                                                     len(fail_record))
        import_result["data"] = fail_record
        import_result["status"] = False if len(fail_record) > 0 else True

    except Exception as e:
        logger.error(e)
        import_result["info"] = "导入错误!"

    return import_result
