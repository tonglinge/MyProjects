#!/usr/bin/env python
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db.models import Q

from afcat.account.core.permission import operator_audit_decorator
from afcat.api.libs.public import Logger, response_format
from afcat.cmdb import models
from afcat.cmdb.libs.common import page_split

logger = Logger(__name__)


def load_base_table_record(table_name, fields, custid):
    """
    前端页面需要的基表数据的获取方法,指定显示的字段,返回字典格式数据 e.g:
    {"baseassettype":[{"id":1,"name":"物理机"],["id":2,"name":"虚拟机"],["id":3,"name":"网络设备"]]}
    :param fields: 其它需要显示的字段，列表
    :param table_name:  要获取数据的数据基表名 与 models中定义表名一直，必选
    :return: 字典 {"table_name":[{id:value}.....],}
    """
    result = dict()
    record_list = list()
    try:
        table_obj = getattr(models, table_name)
        # all_record = table_obj.objects.all().values(*fields)
        all_record = table_obj.objects.filter(id__startswith=custid).values(*fields)
        for record in all_record:
            record_list.append(record)
        result = {table_name.lower(): record_list}
    except (AttributeError, FieldError) as e:
        # 找不到指定的表
        logger.error(e)
    return result


def get_base_data(custid, tablelist):
    """
    获取指定的所有基础数据表的数据公共方法
    :param tablelist: 数据表列表, 表名需和models定义的一致e.g: ["BaseAssetType","BaseNetArea"]
    :return: 返回所有表结果的字典,返回所有的字段名
    """
    result = dict()
    table_fields = list()
    for tablename in tablelist:
        table_fields.clear()
        try:
            table_obj = getattr(models, tablename)
            # get all columns in table
            for field_obj in table_obj._meta.fields:
                table_fields.append(field_obj.column)
            # all_data = table_obj.objects.all().values(*table_fields)
            all_data = table_obj.objects.filter(id__startswith=custid).values(*table_fields)
            result.update({tablename.lower(): list(all_data)})
        except (AttributeError, FieldError) as e:
            logger.error(e)
    return result


@operator_audit_decorator("BaseData")
def post_base_data(post_data):
    """
    添加、修改、删除单个基表数据
    :param table: 表名
    :return:
    """
    result = response_format()
    try:
        post_value = post_data.get("value", "")
        table_obj = getattr(models, post_data.get("table"))
        if post_data.get("action") == "edit":
            record_id = post_value.get("id")
            record_obj = table_obj.objects.filter(id=int(record_id))
            record_obj.update(**post_value)
            result["info"] = "修改成功"

        if post_data.get("action") == "new":
            post_value.update(dict(id=nextid(table_obj._meta.db_table, post_data.get("custid"))))
            new_obj = table_obj.objects.create(**post_value)
            new_record_info = get_single_obj_record(new_obj)
            result["data"] = new_record_info
            result["info"] = "添加成功"

        if post_data.get("action") in ("del", "delete"):
            table_obj.objects.filter(id=post_value.get("id")).delete()
            result["info"] = "删除成功"

    except Exception as e:
        logger.error(e)
        result["info"] = "更新失败"
        result["category"] = "error"
    return result


def get_asset_staffs_str(asset_obj):
    """
    返回资产(服务器,设备等)关联的人员信息的名字
    :param obj: 关联的资产对象
    :return:  名字字符串 e.g: 张三,李四,王五
    """
    staff_name_list = ""
    staff_obj_list = asset_obj.related_staffs.select_related()
    if staff_obj_list.count() > 0:
        staff_list = []
        for staff in staff_obj_list:
            staff_list.append(staff.staff.name)
        staff_name_list = ",".join(staff_list)
    return staff_name_list


def get_staffs_list(request_data):
    """
    获取所有联系人信息
    :param request_data:
    :return:
    """
    result = response_format()
    staff_info_list = list()
    try:
        request_page = request_data.get("page", 1)
        condition = request_data.get("condition", "")
        if not condition:
            all_staffs = models.Staffs.objects.all()
        else:
            all_staffs = models.Staffs.objects.filter(Q(name=condition) | Q(alias=condition) | Q(mobile=condition)
                                                      | Q(tel=condition))

        if all_staffs.count() > 0:
            return_data = page_split(all_staffs, request_page)
            for staff_obj in return_data.get("record"):
                staff_info = dict(id=staff_obj.id, name=staff_obj.name,
                                  mobile=staff_obj.mobile, tel=staff_obj.tel,
                                  email=staff_obj.email,
                                  company=staff_obj.company.name if staff_obj.company else "",
                                  department=staff_obj.department.name)
                staff_info_list.append(staff_info)
            result["data"] = staff_info_list
        else:
            result["info"] = "未查找到记录"
            result["category"] = True
    except Exception as e:
        logger.error(e)
        result["info"] = "未查找到记录"
        result["category"] = False
    return result


def nextid(tablename, custid=""):
    """
    获取指定表的id值
    :param tablename: models.TABLE._meta.db_table
    :return:id值
    """
    try:

        id_obj = models.IDS.objects.get(tablename=tablename, nextid__startswith=custid)
        next_id = id_obj.nextid
        custcode = str(next_id)[:4]
        record_id = str(next_id)[4:]
        # print("tb:{2},custid:{0}, curr_id:{1}".format(custcode, record_id, tablename))
        new_id = int("{0}{1}".format(custcode, int(record_id) + 1))
        id_obj.nextid = new_id
        id_obj.save()
        return next_id
    except ObjectDoesNotExist:
        # 表中数据未找到对应的表,返回对应表的第一个ID，并添加到表记录中
        # print("ID Does not exiest")
        init_id = int("{0}1".format(custid))
        models.IDS.objects.create(**dict(tablename=tablename, nextid=init_id + 1))
        return init_id
        # pass
    except Exception as e:
        logger.error(e)
        return 0


def save_del_history(modelname, op_data, user, custid):
    """
    删除设备信息时保留历史记录
    :return:
    """
    try:
        models.AssetHistory.objects.create(id=nextid(models.AssetHistory._meta.db_table, custid=custid),
                                           model_name=modelname, data=op_data, op_user=user.username)
    except Exception as e:
        logger.error(e)


def get_single_obj_record(obj):
    """
    获取单个对象的所有字段及字段值
    :param obj: model对象
    :return:
    """
    obj_info = dict()
    try:
        for field in obj._meta.fields:
            obj_info.update({field.column: getattr(obj, field.column)})

        # 对于特殊的几个表（R开头的关系表)返回关联表信息,公共方法,添加新记录后要返回记录信息
        if obj._meta.object_name in ['R_Equipment_Staff', 'R_Server_Staff']:
            obj_info.update(dict(name=obj.staff.name, mobile=obj.staff.mobile,
                                 email=obj.staff.email, tel=obj.staff.tel,
                                 role=obj.role.role_name if obj.role else ""))
    except Exception as e:
        logger.error(e)
    return obj_info


def import_excel(excel_data, request_data):
    pass


def convert_table_field(table_field_list, key_index, value_index, custid):
    """
    将字符串字典形式转换为值的key:value形式
    :param value_index: 字段列表中作为key的index下标
    :param key_index:   字段列表中作为value的index下标
    :param table_field_list:表及字段的列表 e.g: [(table_name1, [field1, field2]),(table_name2, [field1, field2])]
                也可以是组合的列作为key值: e.g: [(table_name1,[(field1,field2),field3])
    :param custid: 客户ID
    :return:返回表及字段字典的字典集 {table_name:{field1.value:field2.value,field1.value:field2.value}, ...} or
                                {table_name:{field1.value-field2.value: field3}}
    """
    data_dict = dict()
    try:
        for obj in table_field_list:
            if isinstance(obj[1][key_index], tuple) or isinstance(obj[1][key_index], list):
                data_dict.update(load_base_table_record(obj[0], obj[1][key_index], custid))
                obj[1][key_index].remove(obj[1][value_index])
                data_dict[obj[0].lower()] = {
                '-'.join([str(v.get(k)) for k in obj[1][key_index]]): v.get(obj[1][value_index])
                for v in data_dict.get(obj[0].lower())}
            else:
                data_dict.update(load_base_table_record(obj[0], obj[1], custid))
                # 将id与值value进行转换为字典形式
                data_dict[obj[0].lower()] = {v.get(obj[1][key_index]): v.get(obj[1][value_index])
                                             for v in data_dict.get(obj[0].lower())}
    except Exception as e:
        logger.error(e)
    return data_dict
