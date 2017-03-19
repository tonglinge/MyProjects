#!/usr/bin/env python
"""
该模块用来处理其它所有模块中涉及到的公共方法
author: wangsong  2016-09-13
"""

import copy
import hashlib
import importlib
import json
import os
import re
from datetime import datetime, date

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse
from django.shortcuts import render

from afcat.api.libs.public import Logger, response_format
from afcat.cmdb import models
from afcat.cmdb import settings

logger = Logger(__name__)


def create_assno():
    """
    生成一个唯一的资产ID号,12位,用时间戳
    :return:
    """
    assetno = int(datetime.timestamp(datetime.now()) * 10000)
    return str(assetno)


def page_split(objlist, page_index, per_count=None):
    """
    分页模块,每页显示的记录数保存在 settings 配置中
    :param objlist:  要显示的记录列表集
    :param page_index: 当前页
    :param per_count: 煤业显示多少条记录数
    :return:  显示的记录结果集,总页码,当前页码 e.g: {"record":result, "num_pages":10, "curr_page":1}
    """
    record_list = objlist  # 数据源
    if not per_count:
        per_count = settings.PER_PAGE_COUNT
    page_obj = Paginator(record_list, per_count)

    try:
        result_list = page_obj.page(page_index)
    except PageNotAnInteger:
        page_index = 1
        result_list = page_obj.page(1)
    except EmptyPage:
        page_index = page_obj.num_pages
        result_list = page_obj.page(page_obj.num_pages)
    return {"record": result_list, "num_pages": page_obj.num_pages, "curr_page": page_index,
            "total_count": len(objlist)}


def writelog(msg):
    """
    记录错误日志信息
    :param msg: 日志信息
    :return:
    """
    logger.error(msg)
    # log = logging.getLogger("cmdb")
    # log.setLevel(logging.INFO)
    # filelog = logging.FileHandler(settings.LOG_FILE)
    # filelog.setLevel(logging.ERROR)
    # log_format = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(module)s - %(message)s")
    # filelog.setFormatter(log_format)
    # log.addHandler(filelog)
    # log.error(msg)


def response_json(data):
    """
    对HttpResponse重新进行封装一下,返回一个json的数据格式
    :param data: 要返回的数据
    :return: 重新封装过的对象
    """
    import json
    try:
        json_data = json.dumps(data, cls=CJsonEncoder)
        response = HttpResponse(json_data)
    except Exception as e:
        logger.error(e)
        response = HttpResponse("")
    # 跨域问题
    response["Access-Control-Allow-Origin"] = "*"
    return response


def response_error(error_msg, request):
    """
    错误返回信息
    :param error_msg:错误消息
    :param request:
    :return:
    """
    result = response_format()
    result["status"] = False
    result["category"] = "error"
    result["info"] = error_msg

    if request.is_ajax():
        return response_json(result)
    else:
        return render(request, "cmdb/notfound.html", {"param": None})


def get_model(model_name):
    """
    反射获取cmdb.libs下的模块名, server,equipment
    :param model_name: str类型, 模块名: server, equipment
    :return:  返回一个model对象
    """
    try:
        # cmdb_obj = __import__("afcat.cmdb")
        libs_obj = importlib.import_module("..libs", "afcat.cmdb.libs")
        # libs_obj = getattr(cmdb_obj, "libs")
        asset_obj = getattr(libs_obj, model_name)
        return asset_obj
    except Exception as e:
        logger.error(e)
        return ""


def filter_dict(dic):
    """
    清洗字典列表,将为值为空的元素del掉
    :param dic:
    :return:
    """
    new_dic = dic.copy()
    for key in new_dic.keys():
        if not new_dic[key]:
            del dic[key]
    return dic


def convert_dict_to_str(dic_list, key_list, mark):
    """
    将字典数据按照指定key转换成一个字符串
    :param mark: 连接的符号
    :param key_list: 提取的内容key
    :param dic: 字典列表
    :return:
    """
    result = []
    try:
        for dic in dic_list:
            tmpdic = []
            for key in key_list:
                value = str(dic.get(key))
                if value:
                    tmpdic.append(value)
            result.append(mark.join(tmpdic))
        return "\n".join(result)
    except Exception as e:
        logger.error(e)
        return result


def get_related_tables_name(model_name):
    """
    获取指定model关联的所有表名
    :param model_name: model表名
    :return: 所有与该表有关联的表名
    """
    related_tables = []
    try:
        model_obj = getattr(models, model_name)
        for related_obj in model_obj._meta.related_objects:
            table_name = related_obj.related_model._meta.object_name
            related_tables.append(table_name)
    except Exception as e:
        logger.error(e)

    return related_tables


def object_related_data(models_name, object_id):
    """
    获取指定id的对象的所有关联表数据(保留历史的时候用)
    :param models_name: modes 名
    :param object_id: 要查找的models的id号
    :return: json格式数据
    """
    all_data = dict()
    try:
        # 获取所删除 id的对象
        model = getattr(models, models_name)
        related_tables = get_related_tables_name(models_name)
        # 遍历所有依赖的关系表,获取所有的依赖关系表数据(字段及值)
        for table_name in related_tables:
            table_obj, table_fields = get_table_fields_name(table_name)

            for field_obj in table_obj._meta.fields:
                if field_obj.many_to_one and field_obj.related_model._meta.model_name == models_name.lower():
                    check_field = field_obj.column
                    break
            related_data = table_obj.objects.filter(**{check_field: object_id}).values(*table_fields)
            all_data.update({table_name: list(related_data)})
    except Exception as e:
        logger.error(e)

    return all_data


def get_table_fields_name(model_name):
    """
    根据表名，获取表的所有字段名
    :param model_name: 表名
    :return: 所有字段列表
    """
    field_list = list()
    model_obj = getattr(models, model_name)
    for field_obj in model_obj._meta.fields:
        field_list.append(field_obj.column)
    return model_obj, field_list


def get_request_data(request):
    """
    获取ajax请求的提交的数据
    :param request: request请求
    :return:
    """
    print(request.GET)
    if request.method == "GET":
        data = json.loads(request.GET.get("data", ""))

    if request.method == "POST":
        read_data = request.read()
        post_data = request.POST
        if post_data:
            data = json.loads(post_data.get("data"))
        else:
            data = json.loads(read_data.decode()).get("data")

    custid = request.session.get("custid", "")
    if not custid:
        # 未获取到客户ID,可能未给当前用户分配客户或从数据库获取客户ID失败
        result = response_format()
        result["info"] = "请选择要操作的客户"
        result["status"] = False
        result["category"] = "warning"
        return response_json(result)
    else:
        # 将当前操作用户加入请求数据中
        data.update({"user": request.user, "custid": custid})
        return data


def get_record_all_fields(model_obj):
    """
    获取一条model对象的所有字段及字段值
    :param model_obj:
    :return:
    """
    return_data = dict()
    for f in model_obj._meta.fields:
        file_name = f.column
        file_value = getattr(model_obj, file_name)
        return_data.update({file_name: file_value})
    return return_data


def save_file_for_upload(file_path, fileobj):
    """
    保存文件到服务器
    :param file_path: 要保存的文件路径
    :param fileobj: 发送的文件对象
    :return:
    """
    try:
        file_name = create_assno() + "." + fileobj.name.split('.')[1]
        save_file = os.path.join(file_path, file_name)
        recv_size = 0
        with open(save_file, 'wb+') as f:
            for trunc in fileobj.chunks(1024):
                f.write(trunc)
                recv_size += len(trunc)

        return file_name
    except Exception as e:
        logger.error(e)
        return ""


class CJsonEncoder(json.JSONEncoder):
    """
    解决json序列化日期格式问题
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def md5_encry(str):
    """
    获取指定的字符串的MD5值
    :param str:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(str.encode())
    result = md5.hexdigest()
    return result


def get_file_md5():
    """
    从数据库中获取所有模板文件的title的MD5值
    :return: 模板名称及title值的键值
    """
    data = dict()
    try:
        md5_values = models.TemplsteVerification.objects.all()
        for obj in md5_values:
            data.update({obj.template_name: obj.md5_value})
    except Exception as e:
        logger.error(e)

    return data


def ip_check(ipaddr):
    """
    验证IP地址合法性
    :param ipaddr: ip地址(V4)
    :return: True/False
    """
    ip_reg = "^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\." \
             "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$"
    pattern = re.compile(ip_reg)
    flag = pattern.match(ipaddr)
    if not flag:
        return False
    else:
        return True


def ip_allocated(manageip, custid):
    """
    检测管理IP是否是分配的IP,如果未分配不能使用
    :param ipaddr: 管理IP地址
    :param custid: 客户ID
    :return: 可以使用 True / 不可以使用 False
    """
    flag = True
    try:
        if manageip:
            allocate_qset = models.IPManage.objects.filter(cust=custid, ipaddr=manageip)
            if allocate_qset.count() > 0:
                # 已分配的数据,要检测是否已经被使用 ('1', '已预留'), ('2', '已分配'), ('3', '已使用'), ('4', '待回收')
                if allocate_qset.first().status in ('3', '4'):
                    flag = False
            else:
                flag = False

    except Exception as e:
        logger.error(e)

    return flag


def change_ip_status(custid, ipaddr, status, memo=""):
    """
    修改分配IP地址表中的 IP 状态
    :param custid: 客户ID
    :param ipaddr: IP地址
    :param status: 修改的状态
    :param memo: 备注信息
    :return:
    """
    status_info = {"RESERED": 1, "ALLOCATED": 2, "USED": 3, "RECOVER": 4}
    try:
        if ipaddr:
            ip_obj = models.IPManage.objects.filter(ipaddr=ipaddr, cust=custid).first()
            if ip_obj:
                ip_obj.status = status_info.get(status)
                if ip_obj.status == 2:
                    ip_obj.binded = ""
                if ip_obj.status == 3:
                    ip_obj.binded = memo
                ip_obj.save()
    except Exception as e:
        logger.error(e)


def get_value_by_ids(models_name, show_field, ids):
    """
    通过id号返回某个表中指定的一个字段的值, business或host主机名
    :param models_name: models名 e.g: Business
    :param show_field: 要显示的某个字段值
    :param ids:  id列表  10011,10012
    :return: 逗号分隔的字段值 e.g:  业务系统,数据库
    """
    value = ""
    try:
        id_list = ids.split(',')
        model_obj = getattr(models, models_name)
        if id_list:
            record = model_obj.objects.filter(id__in=id_list).values(show_field)
            for r in record:
                field_value = r.get(show_field, "")
                value = "{0},{1}".format(field_value, value) if field_value else value
    except Exception as e:
        logger.error(e)

    return value[:-1]


def get_field_verbose_name(models_obj, custid):
    """
    获取数据表中各字段的verbose_name, 如果有自定义的显示自定名称,没有自定义显示默认verbose_name
    对于有扩展字段(自定义),显示自定义扩展名称
    :param models_name: 模块(表)名
    :param custid:  所属客户ID
    :return: {”default":{'field_name':'verbose_name'....},"extend":[{"to_field":"","verbose_name":"自定义名“}]
    """
    field_info = dict()
    try:
        model_obj = models_obj
        models_name = models_obj._meta.object_name
        model_fields = model_obj._meta.fields
        field_verbose_name = {field.column: field.verbose_name for field in model_fields}
        # 去掉自定义字段
        _tmp_fields = copy.deepcopy(field_verbose_name)
        for k, v in _tmp_fields.items():
            if re.match('customer\d{3}', k):
                del field_verbose_name[k]
        del _tmp_fields

        # 获取自定义字段名称
        customer_verbose_objs = models.TableFieldPropertyClassify.objects.filter(cust_id=custid,
                                                                                 tablename=models_name).order_by(
            "ordered")
        if customer_verbose_objs.count() > 0:
            customer_verbose_name = {obj.tablefield: obj.propertyname for obj in customer_verbose_objs}
            field_verbose_name.update(customer_verbose_name)
        field_info.update({models_name: field_verbose_name})

        # 获取扩展字段名称
        # customer_field_info = get_table_extend_fields(custid, models_name)
        # if len(customer_field_info) > 0:
        #     field_info.update({"extend": {models_name: customer_field_info}})
    except Exception as e:
        logger.error(e)

    return field_info


def get_table_extend_fields(custid, table_name):
    """
    获取指定表的扩展字段信息
    :param custid: 客户ID
    :param table_name: 表名
    :return:
    """
    _result = list()
    try:
        customer_field_objs = models.CustomerTableProperty.objects.filter(cust_id=custid,
                                                                          tablename=table_name).order_by('id')
        if customer_field_objs.count() > 0:
            for obj in customer_field_objs:
                _result.append({'label': obj.propertyname, 'to_field': obj.tablefield})
    except Exception as e:
        logger.error(e)

    return _result


def list_to_dict(list_objs, field_key, field_value):
    """
    转换列表中的字典元素为字典类型
    :param list_objs: e.g:[{'label':'AAA','value':'111'},{'label':'bbb','value':'222'}]
    :param field_key:  'label'
    :param field_value: 'value'
    :return: e.g:{'AAA':'111','bbb':'222}
    """
    _result = dict()
    try:
        for field in list_objs:
            key = field.get(field_key)
            value = field.get(field_value)
            _result.update({key: value})

    except Exception as e:
        logger.error(e)

    return _result
