#!/usr/bin/env python
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from afcat.account.core.permission import operator_audit_decorator
from afcat.api.libs.public import Logger, response_format
from afcat.cmdb.libs import common, base
from afcat.cmdb.models import Assets, IPManage

logger = Logger(__name__)


def get_asset_list(page_index, conditions, custid, perm_id_list=None, per_count=None):
    """
    获取服务器设备资产信息
    :param page_index:页码
    :param conditions: 搜索条件 {"type":10012, "content":"xxxx"}
    :param perm_id_list: 允许访问的权限的id列表
    :return:
    """
    result = response_format()
    asset_result_list = list()
    page_split_result = {"record": asset_result_list, "addperm": True}

    try:
        all_assets_obj = _get_record_by_condition(conditions, perm_id_list, custid)
        # 获取分页数据
        page_split_result.update(common.page_split(all_assets_obj, page_index,per_count))
        show_asset_obj = page_split_result.get("record")

        if len(all_assets_obj) > 0:
            for asset_obj in show_asset_obj:
                asset_info = dict(id=asset_obj.id, sn=asset_obj.sn,
                                  model=asset_obj.model, unitinfo=asset_obj.unitinfo, cpu=asset_obj.cpu,
                                  memory=asset_obj.memory, manageip=asset_obj.manageip,
                                  contact=asset_obj.contact, remark=asset_obj.remark,
                                  assetstatus=asset_obj.assetstatus.status if asset_obj.assetstatus else "",
                                  assettype=asset_obj.assettype.name if asset_obj.assettype else "",
                                  cabinet=asset_obj.cabinet,
                                  room=asset_obj.room.name if asset_obj.room else "",
                                  netarea=asset_obj.netarea.name if asset_obj.netarea else "",
                                  factory=asset_obj.factory.name if asset_obj.factory else "",
                                  integrator=asset_obj.integrator.name if asset_obj.integrator else "",
                                  startdate=asset_obj.startdate, expiredate=asset_obj.expiredate,
                                  hostcount=asset_obj.related_asset.select_related().count(),
                                  changeperm=True,
                                  delperm=True
                                  )
                asset_result_list.append(asset_info)

        page_split_result.update({"record": asset_result_list})
        # 将搜索的基表数据返回给前端 下拉框
        base_type = base.get_base_data(custid, ["BaseAssetType"])
        page_split_result.update(base_type)

    except Exception as e:
        logger.error(e)
        result["info"] = "无数据记录"
        page_split_result.update({"num_pages": 1, "curr_page": 1, "total_count": 0})

    finally:
        result["data"] = page_split_result
        return result


def _get_record_by_condition(conditions, perm_id_list, custid):
    """
    根据查询条件获取所有数据
    :param condition: 查询条件
    :return:
    """
    search_condition = dict(cust_id=custid)
    all_assets_obj = list()
    try:
        if perm_id_list:
            search_condition.update({"id__in": perm_id_list})

        # 查询条件
        if conditions:
            # if int(conditions.get("type", 0)) > 0:
            #     search_condition.update({"usetype_id": conditions.get("type")})
            # if conditions.get("content"):
            #     search_condition.update({"sn__contains": conditions.get("content")})
            content = conditions.get("content")
            all_assets_obj = Assets.objects.filter(Q(sn__contains=content) |
                                                   Q(model__contains=content) |
                                                   Q(usetype__name__contains=content)|
                                                   Q(assettype__name__contains=content) |
                                                   Q(manageip__contains=content) |
                                                   Q(netarea__name__contains=content) |
                                                   Q(assetstatus__status__contains=content),
                                                   **search_condition).all()
        else:
            # 获取所有数据
            all_assets_obj = Assets.objects.filter(**search_condition).all()
    except Exception as e:
        logger.error(e)

    return all_assets_obj


def load_related_base_configuration(custid):
    """
    获取编辑或添加时依赖的基表数据
    :return: 字典
    """
    related_tables = ["BaseAssetType", "BaseAssetSubtype", "BaseMachineRoom", "BaseDataCenter",
                      "BaseAssetCabinet", "BaseFactory", "BaseAssetStatus", "BaseNetArea"]
    related_data = base.get_base_data(custid, related_tables)
    return related_data


def get_asset_base_info(asset_id):
    """
    编辑时获取资产的详细信息(get)
    :param asset_id: 资产ID
    :return:
    """
    try:
        asset_obj = Assets.objects.get(id=asset_id)
        asset_info = common.get_record_all_fields(asset_obj)
        # 追加数据中心
        asset_info.update({"basedatacenter": asset_obj.room.center_id if asset_obj.room else ""})
        related_hosts_count = asset_obj.related_asset.select_related().count()
        asset_info.update({"host_count": related_hosts_count})
        return asset_info
    except ObjectDoesNotExist as e:
        logger.error(e)
        return ""
    except Exception as e:
        logger.error(e)
        return ""


@operator_audit_decorator("Assets")
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
            asset_obj = Assets.objects.filter(id=sid)
            if asset_obj.first().manageip != asset_data.get("manageip", ""):
                result = data_validate(asset_data.get("sn", ""), asset_data.get("manageip", ""), custid, sid)
                if result["status"]:
                    # 修改IP使用状态
                    common.change_ip_status(custid, asset_obj.first().manageip,"ALLOCATED")
                    common.change_ip_status(custid,asset_data.get("manageip", ""),"USED",asset_obj.first().__str__())
                    asset_obj.update(**asset_data)
                    result["info"] = "修改成功"
            else:
                asset_obj.update(**asset_data)
                result["info"] = "修改成功"

        elif action == "new":
            result = data_validate(asset_data.get("sn", ""), asset_data.get("manageip", ""), custid)
            if result["status"]:
                asset_data.update(dict(id=base.nextid(Assets._meta.db_table, custid),
                                       updateuser=user.username,
                                       createuser=user.username,
                                       cust_id=custid,
                                       assetno=common.create_assno()))
                # print("post new data:", asset_data)
                asset_obj = Assets.objects.create(**asset_data)
                # 修改IP地址的使用状态为已使用
                common.change_ip_status(custid, asset_data.get("manageip"),"USED", asset_obj.__str__())
                result["info"] = "添加成功"
                result["data"] = dict(id=asset_obj.id)

        elif action == "delete":
            asset_obj = Assets.objects.filter(id=sid)
            if not asset_obj:
                result["info"] = "未找到指定记录"
                result["status"] = False
                result["category"] = "error"
            else:
                # 查看要删除的记录是是否有关联的主机
                related_server = asset_obj[0].related_asset.select_related()
                if related_server.count() > 0:
                    # 还有关联主机,不能删除
                    result["info"] = "此设备关联主机,请先迁移主机"
                    result["category"] = "warning"
                    # print(result)
                else:
                    related_data = get_asset_base_info(sid)
                    # 保存历史数据
                    base.save_del_history("Assets", related_data, user, custid)
                    # 修改IP地址的使用状态为待回收
                    common.change_ip_status(custid, asset_obj.first().manageip,"RECOVER")
                    # 删除记录
                    asset_obj.delete()
                    result["info"] = "删除成功"
    except Exception as e:
        logger.error(e)
        result["status"] = False
        result["category"] = "error"
        result["info"] = "内部错误!"

    return result


def get_asset_details(sid):
    """
    获取详细信息
    :return:
    """

    try:
        asset_obj = Assets.objects.get(id=sid)
        asset_info = dict(id=asset_obj.id, sn=asset_obj.sn,
                          model=asset_obj.model, usetype=asset_obj.usetype.name if asset_obj.usetype else "",
                          assettype=asset_obj.assettype.name if asset_obj.assettype else "",
                          room=asset_obj.room.name if asset_obj.room else "",
                          cabinet=asset_obj.cabinet,
                          unitinfo=asset_obj.unitinfo, cpu=asset_obj.cpu,
                          memory=asset_obj.memory, manageip=asset_obj.manageip,
                          clusterinfo=asset_obj.clusterinfo,
                          factory=asset_obj.factory.name if asset_obj.factory else "",
                          integrator=asset_obj.integrator.name if asset_obj.integrator else "",
                          tradedate=datetime.strftime(asset_obj.tradedate,
                                                      "%Y-%m-%d") if asset_obj.tradedate else "",
                          startdate=datetime.strftime(asset_obj.startdate,
                                                      "%Y-%m-%d") if asset_obj.startdate else "",
                          expiredate=datetime.strftime(asset_obj.expiredate,
                                                       "%Y-%m-%d") if asset_obj.expiredate else "",
                          netarea=asset_obj.netarea.name if asset_obj.netarea else "",
                          assetstatus=asset_obj.assetstatus.status if asset_obj.assetstatus else "",
                          contact=asset_obj.contact, createuser=asset_obj.createuser, remark=asset_obj.remark,
                          hostcount=asset_obj.related_asset.select_related().count()
                          )
    except Exception as e:
        logger.error(e)
        asset_info = dict()

    return asset_info


def export_excel(custid, **kwargs):
    """
    导出服务器资产信息数据
    :param kwargs:
    :return:
    """
    from afcat.cmdb.libs.excel import Excel
    try:
        excel_obj = Excel()

        condition = {"content": kwargs.get("content")[0]}

        sheet_title = [
            ("序号", 5), ("SN", 20), ("型号", 15), ("用途", 20), ("设备类型", 15), ("网络区域", 15), ("机房", 15),
            ("机柜", 10), ("单元信息", 10), ("CPU", 5), ("内存", 5), ("管理IP", 10), ("集群信息", 10),
            ("厂商", 10), ("集成商", 10), ("购买日期", 10), ("开始保修期", 10), ("过保日期", 10),
            ("设备状态", 10), ("联系人", 15), ("备注", 25)
        ]

        asset_obj_list = _get_record_by_condition(condition, None, custid)

        row_index = 1
        sheet_rows = list()
        for asset_obj in asset_obj_list:
            rec_row = list()
            asset_info = get_asset_details(asset_obj.id)
            # index
            rec_row.append(row_index)
            # sn
            rec_row.append(asset_info.get("sn", ""))
            # model
            rec_row.append(asset_info.get("model", ""))
            # usetype
            rec_row.append(asset_info.get("usetype", ""))
            # assettype
            rec_row.append(asset_info.get("assettype", ""))
            # netarea
            rec_row.append(asset_info.get("netarea", ""))
            # room
            rec_row.append(asset_info.get("room", ""))
            # cabinet
            rec_row.append(asset_info.get("cabinet", ""))
            # unitinfo
            rec_row.append(asset_info.get("unitinfo", ""))
            # CPU
            rec_row.append(asset_info.get("cpu", ""))
            # memory
            rec_row.append(asset_info.get("memory", ""))
            # ip
            rec_row.append(asset_info.get("manageip", ""))
            # clusterinfo
            rec_row.append(asset_info.get("clusterinfo", ""))
            # factory
            rec_row.append(asset_info.get("factory", ""))
            # integer
            rec_row.append(asset_info.get("integrator", ""))
            # tradedate
            rec_row.append(asset_info.get("tradedate", ""))
            # startdate
            rec_row.append(asset_info.get("startdate", ""))
            # expiredate
            rec_row.append(asset_info.get("expiredate", ""))
            # assetstatus
            rec_row.append(asset_info.get("assetstatus", ""))
            # contact
            rec_row.append(asset_info.get("contact", ""))
            # remark
            rec_row.append(asset_info.get("remark", ""))

            # save
            sheet_rows.append(rec_row)

            row_index += 1
        # start to save excel
        sheet_obj = excel_obj.create_sheet(u"服务器资产")
        excel_obj.write_title(sheet_title, sheet_obj)
        excel_obj.write_row(sheet_rows, sheet_obj)
    except Exception as e:
        logger.error(e)
    finally:
        excel_obj.close()

    return excel_obj.file


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
    if not _check_exists(sn, manageip, custid, obj_id):
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
    :return: 有重复记录False / 无重复记录True
    """
    flag = True
    try:
        qset = Assets.objects.filter(Q(sn=sn) | Q(manageip=manageip), cust_id=custid)
        if obj_id:
            qset = qset.exclude(id=obj_id)
        if qset.count() > 0:
            flag = False
    except Exception as e:
        logger.error(e)
    return flag


@operator_audit_decorator("Assets")
def import_excel(request_data, excel_data):
    """
    从Excel文件导入数据
    :param request_data:  提交数据
    :param excel_data:  导入的有序数据列表,按照模板顺序进行排序的
    :return: 返回导入的结果
    """
    import_result = response_format()
    fail_record = list()
    succ_record = list()
    custid = request_data.get("custid")
    try:
        data_validate_table = [('BaseAssetType', ['name', 'id']), ('BaseAssetSubtype', ['name', 'id']),
                               ('BaseFactory', ['name', 'id']),
                               ('BaseDataCenter', ['name', 'id']), ('BaseMachineRoom', ['name', 'id']),
                               ('BaseAssetStatus', ['status', 'id']), ('BaseNetArea', ['name', 'id'])]

        # 获取所有表格中涉及序列的基表数据
        list_validate_data = base.convert_table_field(data_validate_table, 0, 1, custid)
        # 获取当前asset表中的已存在所有sn与管理IP
        list_asset_info = base.load_base_table_record("Assets", ["sn", "manageip"], custid)
        sn_list = list(set([obj.get('sn') for obj in list_asset_info.get("assets")]))
        if sn_list.count('') > 0:
            sn_list.remove('')
        ip_list = list(set([obj.get('manageip') for obj in list_asset_info.get("assets")]))
        if ip_list.count('') > 0:
            ip_list.remove('')
        # 开始遍历data数据,生成models对象
        for obj in excel_data:
            assets_obj_info = dict(sn=int(obj[0]) if isinstance(obj[0], float) else obj[0],
                                   usetype_id=list_validate_data["baseassettype"].get(obj[1], None),
                                   assettype_id=list_validate_data["baseassetsubtype"].get(obj[2], None),
                                   factory_id=list_validate_data["basefactory"].get(obj[3], None),
                                   integrator_id=list_validate_data["basefactory"].get(obj[4], None),
                                   model=int(obj[5]) if isinstance(obj[5], float) else obj[5],
                                   room_id=list_validate_data["basemachineroom"].get(obj[7], None),
                                   cabinet=int(obj[8]) if isinstance(obj[8], float) else obj[8],
                                   manageip=obj[9], clusterinfo=obj[10], unitinfo=obj[11],
                                   cpu=int(obj[12]) if isinstance(obj[12], float) else obj[12],
                                   memory=int(obj[13]) if isinstance(obj[13], float) else obj[13],
                                   contact=obj[14],
                                   tradedate=obj[15] if obj[15] else None,
                                   startdate=obj[16] if obj[16] else None,
                                   expiredate=obj[17] if obj[17] else None,
                                   assetstatus_id=list_validate_data["baseassetstatus"].get(obj[18], None),
                                   netarea_id=list_validate_data["basenetarea"].get(obj[19], None),
                                   remark=obj[20],
                                   updateuser=request_data.get("user").username if request_data.get("user") else "",
                                   createuser=request_data.get("user").username if request_data.get("user") else "",
                                   # createuser='cmdb', updateuser='cmdb',
                                   cust_id=custid, assetno=common.create_assno()
                                   )
            # 开始校验数据
            # sn, manageip
            err_msg = ""
            if assets_obj_info.get("sn") in sn_list:
                err_msg = "{0}, 序列号 {1} 已存在".format(err_msg, assets_obj_info.get("sn"))

            if assets_obj_info.get('manageip') in ip_list:
                err_msg = "{0}, 管理IP {1} 已存在".format(err_msg, assets_obj_info.get("manageip"))

            if not assets_obj_info.get("model"):
                err_msg = "{0}, 设备型号不能为空".format(err_msg)

            if err_msg:
                fail_record.append({"row": excel_data.index(obj) + 1, "errmsg": err_msg[1:]})
                continue
            else:
                # 校验没问题就加入到要创建的列表中
                assets_obj_info.update(dict(id=base.nextid(Assets._meta.db_table, custid)))
                succ_record.append(Assets(**assets_obj_info))
                if obj[0]:
                    sn_list.append(obj[0])
                if obj[9]:
                    ip_list.append(obj[9])
        # 批量创建到数据库表中
        Assets.objects.bulk_create(succ_record)
        import_result["info"] = "导入完成! 执行{0}条 成功{1}条, 失败{2}条.".format(len(excel_data), len(succ_record),
                                                                      len(fail_record))
        import_result["data"] = fail_record
        import_result["status"] = False if len(fail_record) > 0 else True

    except Exception as e:
        logger.error(e)
        import_result["info"] = "导入错误!"

    return import_result
