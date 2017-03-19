#! /usr/bin/env python
# encoding: utf8
import copy
import ipaddress
import os
import re
from collections import OrderedDict
from datetime import datetime, date, timedelta

from django import forms
from django.core.management import call_command
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.base import ModelBase
from django.shortcuts import render, HttpResponse

from afcat import settings
from afcat.api.libs.public import Logger, BaseHandler
from afcat.cmdb import models as cmdb_models
from afcat.cmdb.libs import common, ipmanage
from afcat.cmdb.libs.base import nextid

logger = Logger(__name__)

__all__ = ["Configure", "Reportindex", "Ipmanagement", "Balancemapping", "Tableproperty"]


def get_tables(request):
    """获取所有基表名称"""
    models_list = [
        'BaseAssetType',
        'BaseAssetSubtype',
        'BaseEquipmentType',
        'BaseDataCenter',
        'BaseMachineRoom',
        'BaseNetArea',
        'ItemsSet',
        'Projects',
        'Business',
        'BaseAssetStatus',
        'BaseRunningStatus',
        'BaseSoftType',
        'BaseSoft',
        'SoftLisence',
        'BaseFactory',
        'BaseCompany',
        'BaseRole',
        'BaseRaidType',
        'BaseBalanceType',
        'BaseCustomerInfo',
        'Staffs',
    ]
    models = []
    app_name = cmdb_models.__package__.split(".")[1]  # 获取当前app的名字
    if type(models_list) is not list:
        models_list = dir(cmdb_models)
    for model in models_list:
        register_model = dict()

        if hasattr(cmdb_models, str(model)):
            model_obj = getattr(cmdb_models, str(model))
            if isinstance(model_obj, ModelBase):
                if model_obj._meta.app_label == app_name:
                    register_model['object_name'] = model_obj._meta.object_name
                    register_model['verbose_name'] = model_obj._meta.verbose_name
                    models.append(register_model)
    return models


def get_model(model_name):
    """
    通过model_name反射model_name对象
    :param model_name: 表名
    :return: 表对象
    """
    model_obj = model_name
    if isinstance(model_name, str):
        if hasattr(cmdb_models, model_name):
            model_obj = getattr(cmdb_models, model_name)
    return model_obj


def gel_all_fields_name(model_name):
    """

    :param model_name:
    :return:
    """
    fields_name = []
    model_obj = get_model(model_name)
    try:
        get_fields = model_obj._meta.concrete_fields
        for field in get_fields:
            fields_name.append({field.name: field.verbose_name})
    except AttributeError as e:
        logger.error(e)
        pass
    return fields_name


def get_model_data(request, model_name):
    """
    获取表中所有的数据
    :param model_name:
    :return:
    """
    model_obj = get_model(model_name)
    try:
        if hasattr(model_obj, "is_public"):
            model_data = model_obj.objects.all()
        else:
            model_data = model_obj.objects.filter(id__startswith=request.session.get("custid"))
        return model_data
    except AttributeError as e:
        logger.error(e)
        pass
    return []  # 如果没有数据,则返回空列表,注意!这里返回对象的必须是可迭代对象,防止页面渲染异常!


def set_paginator(request, model_data):
    """为数据设置分页"""
    per_records = request.GET.get('per_records')  # 获取每页显示多少条数据
    try:
        if per_records:
            per_records = int(per_records)
        else:
            per_records = 20  # 默认显示10条数据
    except ValueError as e:
        logger.error(e)
        per_records = 20
    paginator = Paginator(model_data, per_records)
    page = request.GET.get('page')
    try:
        model_data = paginator.page(page)  # 获取第几页数据
    except PageNotAnInteger:
        model_data = paginator.page(1)  # 默认显示第一页数据
    except EmptyPage:
        model_data = paginator.page(paginator.num_pages)  # 如果获取的分页数据不存在,则显示最后一页数据
    return model_data


def get_tables_data(request, table_name):
    model_data = get_model_data(request, table_name)  # 获取该表所有数据
    model_data = set_paginator(request, model_data)  # 设置分页
    records = []
    for record in model_data:
        record_data = []
        for field in record._meta.get_fields():
            if not hasattr(record, field.name):
                continue
            field_data = getattr(record, field.name)
            if field.is_relation:
                if field.one_to_many:
                    pass
                elif field.many_to_one:
                    pass
                elif field.many_to_many:
                    many_to_many_records = []
                    for other_record in field_data.select_related():
                        many_to_many_records.append(other_record)
                    field_data = ",".join(many_to_many_records)
                if not field.concrete:
                    remote_name = field.related_model._meta.model_name
                    local_name = record._meta.model_name
                    if remote_name == local_name:
                        continue
            if hasattr(field, 'choices'):
                if hasattr(record, "get_%s_display" % field.name):
                    get_choice_func = getattr(record, "get_%s_display" % field.name)
                    field_data = get_choice_func()
            else:
                continue
            # 对于datetime类型进行转换
            if isinstance(field_data, datetime):
                field_data = field_data.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(field_data, date):
                field_data = field_data.strftime('%Y-%m-%d')
            record_data.append({field.name: str(field_data)})
        records.append(record_data)
    fields_name = gel_all_fields_name(table_name)  # 获取表字段
    return {
        'fields_name': fields_name,
        'records': records,
        'has_next': model_data.has_next(),
        'has_previous': model_data.has_previous()
    }


def delete_records(request, table_name, records_id):
    """
    删除指定表中对应id数据
    :param table_name: 表名
    :param records_id: ID列表
    :return:
    """
    ret = {'status': True, 'info': '删除成功', 'category': 'warning'}
    delete_records_success = []
    model_obj = get_model(table_name)
    try:
        from afcat.cmdb.packages.cmdbsignals import operate_audit
        for pk in records_id:
            del_models_qs = model_obj.objects.filter(id=pk)
            # 删除基表数据审计(发送审计信号)
            operate_audit.send(sender=model_obj, instance=del_models_qs[0], user=request.user, action="delete",
                               cust=request.session.get("custid"))
            del_models_qs.delete()
            delete_records_success.append(pk)
        ret['data'] = delete_records_success
    except Exception as e:
        logger.error(e)
        ret['status'] = False
        ret['info'] = "删除失败"
        ret['category'] = 'error'
    return ret


def get_model_form(table_name, get_id, custid):
    """
    通过model表名获取model form对象
    """
    from django.forms.models import ModelChoiceField

    class Form(forms.ModelForm):
        class Meta:
            model = get_model(table_name)
            exclude = ["idcode"]  # 针对客户信息表BaseCustomerInfo, 不显示指定字段

        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                field = cls.base_fields[field_name]
                #  区分不同客户下的基表显示数据不一样,对queryset重新过滤
                if isinstance(field, ModelChoiceField):
                    if field.queryset.count() > 0:
                        if not hasattr(field.queryset[0], "is_public"):
                            field.queryset = field.queryset.filter(id__startswith=str(custid))
                field.widget.attrs.update({'class': 'form-control'})
                field.error_messages = {'required': '{0} 不能为空'.format(field.label)}

            return forms.ModelForm.__new__(cls)

    return Form


def handler404(request):
    """访问页面不存在,处理"""
    render_respond = render(request, '404.html')
    render_respond.status_code = 404
    return render_respond


def edit_record(request):
    """添加,修改数据页面
    request: 封装的请求对象
    table_name: 操作的表名
    """
    table_name = request.GET.get("table_name", "") if request.method == 'GET' else request.POST.get("table_name", "")
    get_id = request.GET.get("id", None) if request.method == 'GET' else request.POST.get("id", "")
    context = {}
    instance = None  # 初始化实例属性为空
    btn_type = "添加"
    model_form = get_model_form(table_name, get_id, request.session.get("custid"))  # 尝试获取model form对象

    if model_form is None:  # 如果获取不到form对象,请求可能非法,直接返回404错误页面
        return handler404(request)
    if hasattr(cmdb_models, table_name):
        model_obj = getattr(cmdb_models, table_name)
        table_verbose_name = model_obj._meta.verbose_name
        model_form.base_fields['id'].widget.attrs.update({'readonly': 'true'})
        model_form.base_fields['id'].label = "序号"
        if get_id:
            instance = model_obj.objects.filter(pk=get_id).all()
            instance = instance[0] if len(instance) == 1 else None
        else:
            # 添加记录自动追加ID
            if request.method == "GET":
                # 对于不区分客户的表（e.g: BaseCustomerInfo) ID 自增长
                if not hasattr(model_obj, 'is_public'):
                    from afcat.cmdb.libs import base
                    model_form.base_fields['id'].widget.attrs.update({'value': base.nextid(model_obj._meta.db_table,
                                                                                           request.session.get(
                                                                                               "custid")),
                                                                      })
                else:
                    model_form.base_fields['id'].widget.attrs.update({'value': model_obj.objects.latest("id").id + 1,
                                                                      })
        form_data = model_form(instance=instance)  # 实例化form表单
    if instance is not None:
        btn_type = "修改"

    if request.method == 'POST':
        post_data = request.POST.copy()
        if post_data.get("table_name"):
            post_data.pop('table_name')
        if post_data.get("method"):
            post_data.pop('method')
        form_data = model_form(post_data, instance=instance)  # 如果是POST请求,则进行校验数据
        if form_data.is_valid():
            form_data.save()
            message = "添加成功"
            btn_type = "修改"
            if instance:
                message = "修改成功"
            context["message"] = message
        else:
            error_message = "添加失败"
            if instance:
                error_message = "修改失败"
            context["error_message"] = error_message
    context['btn_type'] = btn_type
    context["model_form"] = form_data  # 返回model form 对象
    context["table_name"] = table_verbose_name  # 返回表名
    return HttpResponse(render(request, 'cmdb/model_form.html', context))


class Configure(BaseHandler):
    """
    method: configure.dbbackup , configure.dbrestore
    """

    def __init__(self, method=None, request=None, *args, **kwargs):
        super(Configure, self).__init__(method=method, request=request)
        self.args = args
        self.kwargs = kwargs

    def db_backup(self):
        """
        备份数据
        :return:
        """
        try:
            from afcat.cmdb.packages.cmdbsignals import operate_audit
            remark = self.request.GET.get("remark", "")
            backup_path = os.path.join(settings.BASE_DIR, "fixtures")
            filename = "cmdb_{0}".format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
            backup_file = os.path.join(backup_path, "{0}.json".format(filename))
            new_rec = cmdb_models.BackupRecord.objects.create(filename=filename, backupuser=self.request.user.username,
                                                              remark=remark)
            # 添加审计,将当前备份写入操作记录
            operate_audit.send(sender=cmdb_models.BackupRecord, instance=new_rec, user=self.request.user,
                               action="new", cust=self.request.session.get("custid"))

            if new_rec:  # 写数据库成功
                with open(backup_file, 'a+') as f:
                    call_command("dumpdata", "--database", "cmdb", "--indent", "2",
                                 "--exclude", "auth.permission",
                                 "--exclude", "contenttypes.contenttype",
                                 stdout=f)
                self.ret["info"] = "备份完成"
                self.ret["category"] = "success"
                self.ret["data"] = dict(id=new_rec.id, filename=new_rec.filename, backupdate=new_rec.backupdate,
                                        backupuser=new_rec.backupuser, remark=new_rec.remark)

            else:
                self.ret["info"] = "备份失败"
                self.ret["category"] = "error"
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "备份失败,检查磁盘空间或目录权限!"
            self.ret["category"] = "error"

    def db_restore(self):
        """
        还原数据
        :return:
        """
        try:
            from afcat.cmdb.packages.cmdbsignals import operate_audit
            rec_id = self.request.GET.get("id", 0)
            if int(rec_id) <= 0:
                self.ret["info"] = "未选择还原的备份"
            else:
                db_obj = cmdb_models.BackupRecord.objects.get(id=int(rec_id))
                filename = db_obj.filename

                # 查看文件是否存在
                file = os.path.join(settings.BASE_DIR, "fixtures", "{0}.json".format(filename))
                if os.path.isfile(file):
                    # 先删除所有数据
                    call_command("flush", "--database", "cmdb", "--noinput")
                    # 开始导入备份数据
                    call_command("loaddata", "--database", "cmdb", "{0}.json".format(filename))
                    self.ret["info"] = "还原成功"
                    # 写入审计
                    operate_audit.send(sender=cmdb_models.BackupRecord, instance=db_obj, user=self.request.user,
                                       action="restore", cust=self.request.session.get("custid"))
                else:
                    self.ret["info"] = "数据文件被删除或文件名错误!"
                    self.ret["category"] = "error"
        except Exception as e:
            logger.error(e)

    def db_record(self):
        """
        获取所有备份的结果集
        :return:
        """
        try:
            record_data = list()
            result_rec = get_tables_data(self.request, "BackupRecord")
            record_list = result_rec.get("records")
            if len(record_list) > 0:
                for field_record_list in record_list:
                    rec_info = dict()
                    for fields in field_record_list:
                        rec_info.update(fields)
                    record_data.append(rec_info)
            self.ret["data"] = record_data
            self.ret["has_next"] = result_rec.get("has_next", False)
            self.ret["has_previous"] = result_rec.get("has_previous", False)
        except Exception as e:
            logger.error(e)

    def db_remove(self):
        """
        删除数据备份
        :return:
        """
        from afcat.cmdb.packages.cmdbsignals import operate_audit
        try:
            sid = self.request.GET.get("id", 0)
            if int(sid) > 0:
                record = cmdb_models.BackupRecord.objects.filter(id=int(sid))
                if record.count() > 0:
                    filename = record[0].filename
                    file = os.path.join(settings.BASE_DIR, "fixtures", "{0}.json".format(filename))
                    if os.path.isfile(file):
                        # 删除文件
                        os.remove(file)
                        # 添加审计
                        operate_audit.send(sender=cmdb_models.BackupRecord, instance=record[0], user=self.request.user,
                                           action="delete", cust=self.request.session.get("custid"))
                    # 删除记录
                    record.delete()
                    self.ret["info"] = "删除成功"
                    self.ret["category"] = "success"
                else:
                    self.ret["info"] = "未找到指定记录"
                    self.ret["category"] = "warning"
            else:
                self.ret["info"] = "参数错误"
                self.ret["category"] = "error"
        except Exception as e:
            logger.error(e)

    def change_cust(self):
        """
        前端改变当前选中的客户ID,修改session的值
        :return:
        """
        try:
            choose_custid = self.request.GET.get("custid")
            choose_cust_obj = cmdb_models.BaseCustomerInfo.objects.filter(idcode=choose_custid).first()
            if choose_cust_obj:
                self.request.session["custid"] = choose_cust_obj.idcode
                self.request.session["custname"] = choose_cust_obj.custalias
                self.ret["data"] = {"custalias": choose_cust_obj.custalias}
                self.ret["info"] = "当前客户: {0}".format(choose_cust_obj.custalias)
                self.ret["category"] = "success"
        except Exception as e:
            logger.error(e)


class Reportindex(BaseHandler):
    """
    cmdb首页所需要的数据的展示api接口
    """

    def __init__(self, method=None, request=None, *args, **kwargs):
        super(Reportindex, self).__init__(method=method, request=request)
        self.args = args
        self.kwargs = kwargs
        self.custid = self.request.session.get("custid")

    def get_previous_month(self, d, index, result_dict):
        """
        获取指定日期前12个月前的日期(yyyy-mm)
        :param d: datetime类型日期
        :param index: 循环到第几次
        :param result_list: 结果数据
        :return: ['2016-11','2016-10'...]
        """
        while index > 1:
            day_count = timedelta(days=d.day)
            last_month_last_day = d - day_count
            result_dict.update({datetime.strftime(last_month_last_day, '%Y-%m'): 0})
            index -= 1
            self.get_previous_month(last_month_last_day, index, result_dict)
            return result_dict

    def iterate_sum(self, count_list):
        """
        将列表中的值迭代相加
        :param count_list:[1,2,3]
        :return: [1,3,6]
        """
        sum_value = 0
        new_list = list()
        count_list.reverse()
        for i in count_list:
            sum_value += i
            new_list.append(sum_value)
        return new_list

    def get_record(self):
        """
        获取首页展示所需要的数据
        :return:
        """
        return_data = list()
        try:
            cust_id = self.request.session.get("custid", None)
            total_count = dict(name="totalcount", values=dict())
            # 获取网络设备的详细统计数据
            equipment_data = cmdb_models.Equipment.report.equipment_type_group_count(cust_id)
            return_data.append(
                {"name": "equipment",
                 "series": [{"value": obj.value, "name": "{0}:{1}台".format(obj.name if obj.name else '其它', obj.value)}
                            for obj in equipment_data],
                 "title": u"网络设备详细统计",
                 "legend": ["{0}:{1}台".format(obj.name if obj.name else '其它', obj.value) for obj in equipment_data]})
            # 获取网络设备的分类总数
            return_data.append(
                {"name": "equipment_count", "series": self._get_total_count(equipment_data), "title": "网络设备分类统计"})
            # 获取总的设备数
            total_count["values"].update({"equipment": sum([int(obj.value) for obj in equipment_data])})

            #  获取服务器设备的统计数量
            asset_data = cmdb_models.Assets.report.asset_type_group_count(cust_id)
            return_data.append(
                {"name": "asset",
                 "series": [{"value": obj.value, "name": "{0}:{1}台".format(obj.name if obj.name else '其它', obj.value)}
                            for obj in asset_data],
                 "title": "服务器详细统计",
                 "legend": ["{0}:{1}台".format(obj.name if obj.name else '其它', obj.value) for obj in asset_data]})
            # 获取服务器设备的分类总数
            return_data.append({"name": "asset_count", "series": self._get_total_count(asset_data), "title": "服务器分类统计"})
            # 服务器设备的总数
            total_count["values"].update({"assets": sum([int(obj.value) for obj in asset_data])})

            # 获取主机统计数量(按操作系统分)
            host_data = cmdb_models.Servers.report.os_group_count(cust_id)
            return_data.append(
                {"name": "host",
                 "series": [{"value": obj.value, "name": "{0}:{1}台".format(obj.name if obj.name else '其它', obj.value)}
                            for obj in host_data],
                 "title": "主机(操作系统)",
                 "legend": ["{0}:{1}台".format(obj.name, obj.value) for obj in host_data]})
            # 主机总数
            total_count["values"].update({"server": sum([int(obj.value) for obj in host_data])})

            # 获取主机的统计数量(按项目集划分)
            host_itemset_data = cmdb_models.Servers.report.item_group_count(cust_id)
            return_data.append(
                {
                    "name": "itemset", "series": [
                    {"value": obj.value, "name": "{0}:{1}台".format(obj.name if obj.name else '其它', obj.value)}
                    for obj in host_itemset_data],
                    "title": "主机(项目集)",
                    "legend": ["{0}:{1}台".format(obj.name, obj.value) for obj in host_itemset_data]
                })

            return_data.append(total_count)
            # 获取最近10条操作记录
            operate_audit = cmdb_models.OperateAudit.audit.last_record(cust_id)
            return_data.append({"name": "audit", "data": operate_audit})

            # 获取要显示的折线图的数据
            # show_date = OrderedDict({datetime.strftime(datetime.now(), '%Y-%m'): 0})
            # init_data = self.get_previous_month(datetime.now(), 12, show_date)
            # # 主机的每月数量折线图数据
            # host_month_count = cmdb_models.Servers.report.month_group_count(init_data, cust_id)
            # asset_month_count = cmdb_models.Assets.report.month_group_count(init_data, cust_id)
            # equipment_month_count = cmdb_models.Equipment.report.month_group_count(init_data, cust_id)
            # xaxis = list(map(lambda x: "'{0}'".format(x), init_data.keys()))
            # xaxis.reverse()
            # asset_series = list(asset_month_count.values())
            # equipment_series = list(equipment_month_count.values())
            # host_series = list(host_month_count.values())
            #
            # month_count = {
            #     "xAxis": xaxis,
            #     "name": "monthcount",
            #     "legend": ['"服务器设备"', '"网络设备"', '"主机"'],
            #     "series": [
            #         {"name": u"服务器设备", "value": self.iterate_sum(asset_series)},
            #         {"name": u"网络设备", "value": self.iterate_sum(equipment_series)},
            #         {"name": "主机", "value": self.iterate_sum(host_series)}
            #     ]}
            # return_data.append(month_count)
            # return_data.reverse()
            self.ret["data"] = return_data
        except Exception as e:
            logger.error(e)

    def _get_total_count(self, obj_list):
        """
        获取服务器、网络设备的分类统计数据
        :param obj_list: 所有的对象
        :return: 返回统计后的结果 e.g: [{'name':'交换机','value':3},{'name':'路由器','value':10}]
        """
        try:
            tmp_count = dict()
            for obj in obj_list:
                if not obj.name:
                    obj.name = '其它'
                if obj.name.split('-')[0] in tmp_count.keys():
                    tmp_count[obj.name.split('-')[0]] += obj.value
                else:
                    tmp_count[obj.name.split('-')[0]] = obj.value
            result = [{"name": "{0}: {1}台".format(k, v), "value": v} for k, v in tmp_count.items()]
            return result
        except Exception as e:
            logger.error(e)
            return []

    def audit(self):
        """
        获取所有的审计信息
        :return:
        """
        try:
            condition = self.request.GET.get("condition")
            if condition:
                all_audit_objs = cmdb_models.OperateAudit.objects.filter(Q(operater__contains=condition) |
                                                                         Q(model_name__contains=condition) |
                                                                         Q(operate_data__contains=condition),
                                                                         cust_id=self.custid).order_by("-operate_time")
            else:
                all_audit_objs = cmdb_models.OperateAudit.objects.filter(cust_id=self.custid).order_by("-operate_time")
            if all_audit_objs.count() > 0:
                page_objs = common.page_split(all_audit_objs, self.page, self.per_page_count)
                detail_info = cmdb_models.OperateAudit.audit.record_details(page_objs.get("record"))
                page_objs.update({"record": detail_info})
                self.ret["data"] = page_objs
                self.ret["status"] = True
        except Exception as e:
            logger.error(e)


class Ipmanagement(BaseHandler):
    """
    IP配置管理API接口
    """
    from afcat.account.core.permission import operator_audit_decorator

    def __init__(self, method=None, request=None, *args, **kwargs):
        super(Ipmanagement, self).__init__(method=method, request=request)
        self.args = args
        self.kwargs = kwargs
        self.custid = self.request.session.get("custid", None)
        self.ret["category"] = "error"
        self.ret["status"] = False

    def info(self):
        """
        获取 IP 地址信息
        :return:
        """
        result_data = {"ip_tree": list(), "ip_design": dict(), "ip_allocate": dict()}
        ip_id = self.request.GET.get("ip_id", None)
        datacenter_id = self.request.GET.get("datacenter_id", None)
        try:
            ip_design = self.__ip_design_info(ip_id, datacenter_id)
            ip_tree = self.__tree_list(ip_design.get('record'), ip_id)
            ip_allocate = self.__ip_allocate_info(mask_id=ip_id, datacenter_id=datacenter_id)
            result_data["ip_tree"].extend(ip_tree)
            result_data["ip_design"].update(ip_design)
            result_data["ip_allocate"].update(ip_allocate)
        except Exception as e:
            logger.error(e)
        self.ret["data"] = result_data

    def allocation(self):
        """
        划分子网或IP地址
        :return:
        """
        try:
            post_data = common.get_request_data(self.request)
            _action = post_data.get("action", None)
            # 请求的类型： 子网：subnet   IP: ip, 用来反射调用
            _type = post_data.get("type", None)

            if not _action or not hasattr(self, "_{0}_{1}".format(_type, _action)):
                self.ret["info"] = "提交参数错误!"
            else:
                func = getattr(self, "_{0}_{1}".format(_type, _action))
                func(post_data)

        except Exception as e:
            logger.error(e)

    def __ip_design_info(self, ip_id=None, datacenter_id=None):
        """
        获取选中IP的所有子网段IP的详细信息,渲染到右侧的table中,显示所有字段信息
        :param ip_id: 要获取信息的ip id
        :return:
        """
        show_list = OrderedDict()
        try:
            ip_info = list()
            if not ip_id:
                condition = dict(cust_id=self.custid, parentip_id__isnull=True)
                if datacenter_id:
                    # 显示顶级的IP列表,父ID为空的记录,第一次加载页面的时候会触发
                    condition.update(dict(datacenter_id=int(datacenter_id)))
                ip_list = cmdb_models.IPDesign.objects.filter(**condition).extra(
                    select={"ip": "inet_aton('ipaddr')"}).order_by("ip")
            else:
                ip_list = cmdb_models.IPDesign.objects.filter(parentip_id=ip_id, cust_id=self.custid).extra(
                    select={"ip": "inet_aton('ipaddr')"}).order_by("ip")
            show_list = self.__ip_design_details(ip_list)
        except Exception as e:
            logger.error(e)

        return show_list

    def __ip_design_details(self, iplist):
        """
        获取所有记录的详细信息
        :param iplist:  记录对象列表
        :return:
        """
        ip_info = list()
        page_split_record = dict()
        try:
            if iplist.count() > 0:
                page_split_record = common.page_split(iplist, self.page, self.per_page_count)
                for ip_obj in page_split_record.get("record"):
                    ip_info.append(dict(id=ip_obj.id, ipaddr=ip_obj.__str__(), counts=ip_obj.counts,
                                        allocatecount=ip_obj.submask.select_related().count()
                                        if ip_obj.submask.select_related().count() > 0 else ip_obj.allocated.select_related().count(),
                                        datacenter_id=ip_obj.datacenter_id, netarea_id=ip_obj.netarea_id,
                                        datacenter=ip_obj.datacenter.name if ip_obj.datacenter else "",
                                        netarea=ip_obj.netarea.name if ip_obj.netarea else "",
                                        vlan=ip_obj.vlan, usefor=ip_obj.usefor,
                                        remark=ip_obj.remark))
                page_split_record["record"] = ip_info

        except Exception as e:
            logger.error(e)
        return page_split_record

    def __tree_list(self, ip_list, id):
        """
        获取选中的左侧tree菜单(IP)下的所有子网段IP地址信息
        :param obj_list: 要获取的IP信息下的所有子网obj
        :param id: 指定的IP的ID,如果没有ID 表示第一次加载数据,需要显示数据中心信息
        :return: list列表 [{"ip":"40.1.0.0/16","id":10011}, {...}]
        """
        tree_info = list()
        try:
            if ip_list:
                if not id:
                    # 无参数ID,按数据中心分组加载信息
                    _tmp_dict = dict()
                    for ip_obj in ip_list:
                        datacenter = ip_obj.get("datacenter")
                        if datacenter and datacenter in _tmp_dict.keys():
                            _tmp_dict[datacenter].append({"ip": ip_obj.get("ipaddr"), "id": ip_obj.get("id"),
                                                          "allocate": ip_obj.get("allocatecount", 0),
                                                          "datacenter_id": ip_obj.get("datacenter_id"),
                                                          "datacenter": ip_obj.get("datacenter", "")})
                        else:
                            _tmp_dict.update({datacenter: [{"ip": ip_obj.get("ipaddr"), "id": ip_obj.get("id"),
                                                            "allocate": ip_obj.get("allocatecount", 0),
                                                            "datacenter_id": ip_obj.get("datacenter_id"),
                                                            "datacenter": ip_obj.get("datacenter", "")}]})
                    tree_info.extend([{"datacenter": k, "ip": _tmp_dict.get(k),
                                       "datacenter_id": _tmp_dict.get(k)[0].get("datacenter_id") if _tmp_dict else "",
                                       "datacenter": _tmp_dict.get(k)[0].get("datacenter") if _tmp_dict else "", }
                                      for k in _tmp_dict.keys()])
                else:
                    # 仅加载IP信息
                    for ip_obj in ip_list:
                        if not (ip_obj.get("id") == int(id)):
                            tree_info.extend([{"ip": ip_obj.get("ipaddr"), "id": ip_obj.get("id"),
                                               "allocate": ip_obj.get("allocatecount", 0),
                                               "datacenter_id": ip_obj.get("datacenter_id"),
                                               "datacenter": ip_obj.get("datacenter", "")}])
        except Exception as e:
            logger.error(e)
        return tree_info

    def __ip_allocate_info(self, mask_id=None, ipaddr=None, datacenter_id=None, **kwargs):
        """
        获取选中IP的所有分配的IP信息
        :param mask_id:指定网段的id (C类网ID)
        :param ipaddr: 要搜索IP地址(模糊匹配),字典类型
        :param datacenter_id: 数据中心ID
        :return:
        """
        result_info = dict()
        try:
            allocate_info = list()
            _condition = dict(cust=self.custid)
            if mask_id:
                _condition.update({"ipmask__id": mask_id})
            if datacenter_id:
                _condition.update({"ipmask__datacenter_id": datacenter_id})
            if ipaddr:
                _condition.update({"ipaddr__contains": ipaddr})
            if kwargs:
                _condition.update(**kwargs)
            # if ip_id:
            ip_details_list = cmdb_models.IPManage.objects.filter(**_condition).extra(
                select={"ip": "inet_aton('ipaddr')"}).order_by("ip")

            if ip_details_list.count() > 0:
                result_info.update(common.page_split(ip_details_list, self.page, self.per_page_count))
                for ip_obj in result_info.get('record'):
                    details_info = ipmanage.get_ipmanage_detail_info(ip_obj)
                    if details_info:
                        allocate_info.append(details_info)
                result_info.update({'record': allocate_info})
        except Exception as e:
            logger.error(e)
        return result_info

    def __ip_subnet_validate(self, ipaddr, maskbits, parentip_id):
        """
        判断新建子网时输入的子网IP及掩码是否合法,判断是否超过允许划分子网的最大数
        :param ipaddr:  子网IP
        :param mask:    子网掩码位
        :param parentip_id: 父网段ip的记录id
        :return:  result结果
        """
        try:
            check_status = True

            # 获取子网父ID对应的对象
            parent_subnet_obj = cmdb_models.IPDesign.objects.filter(id=int(parentip_id)).first()

            if parent_subnet_obj:
                parent_subnet = "{0}/{1}".format(parent_subnet_obj.ipaddr, parent_subnet_obj.maskbits)

                subnet_obj = parent_subnet_obj.submask.select_related()
                # 判断子网数是否已经达到允许划分的最大值
                if subnet_obj.count() >= parent_subnet_obj.counts:
                    self.ret["info"] = "已达到允许划分的最大上限!"
                    self.ret["category"] = "error"
                    self.ret["status"] = False
                    check_status = False
                    return check_status

                # 判断当前要添加的IP子网的IP地址是否已经包含在已分配的子网内
                if subnet_obj.count() > 0:
                    for obj in subnet_obj:
                        if ipaddress.ip_address(ipaddr) in ipaddress.ip_network(
                                "{0}/{1}".format(obj.ipaddr, obj.maskbits)):
                            self.ret["info"] = "已存在包含此IP的子网网段!"
                            self.ret["category"] = "error"
                            self.ret["status"] = False
                            check_status = False
                            break
                    if not check_status:
                        return check_status

                # 判断ip是否在划分的子网内
                if not (ipaddress.ip_address(ipaddr) in ipaddress.ip_network(parent_subnet)):
                    self.ret["info"] = "IP地址不合法,非子网IP!"
                    self.ret["category"] = "error"
                    self.ret["status"] = False
                    check_status = False
                    return check_status

                # 判断掩码位是否合法
                if int(maskbits) <= int(parent_subnet_obj.maskbits):
                    self.ret["info"] = "掩码位不合法!"
                    self.ret["category"] = "error"
                    self.ret["status"] = False
                    check_status = False
                    return check_status
        except Exception as e:
            logger.error(e)
        return check_status

    def __check_ip_subnet_exists(self, ipaddr, maskbits, objid=None):
        """
        检测是否存在已经划分的IP子网
        :param ipaddr: ipd地址
        :param maskbits:  ip子网掩码位
        :param objid: 对象id
        :return:
        """
        try:
            exists_flag = False
            sql_condition = {'cust_id': self.custid, 'ipaddr': ipaddr, 'maskbits': maskbits}
            qset = cmdb_models.IPDesign.objects.filter(**sql_condition)
            if objid:
                qset = qset.exclude(id=int(objid))
            if qset.count() > 0:
                self.ret["info"] = "已存在此子网"
                self.ret["category"] = "error"
                self.ret["status"] = False
                exists_flag = True
        except Exception as e:
            logger.error(e)

        return exists_flag

    @operator_audit_decorator("IPDesign")
    def _subnet_delete(self, request_data):
        """
        删除子网,如果要删除的记录已经有分配记录,则不允许删除
        :param request_data: POST提交的数据{"value":{"id":10011},"action":"delete"}
        :return:
        """
        try:
            post_value = request_data.get("value")
            if post_value:
                obj_id = post_value.get("id", 0)
                obj = cmdb_models.IPDesign.objects.filter(id=int(obj_id))
                if obj.count() == 0:
                    self.ret["info"] = "未找到删除记录"
                else:
                    if obj[0].submask.select_related().count() > 0 or obj[0].allocated.select_related().count() > 0:
                        self.ret["info"] = "此网段包含子网或已分配IP,无法删除!"
                        self.ret["status"] = False
                        self.ret["category"] = "error"
                    else:
                        obj.delete()
                        self.ret["info"] = "删除成功!"
                        self.ret["category"] = "success"
                        self.ret["status"] = True
            else:
                self.ret["info"] = "参数错误,未找到删除记录"
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "系统内部错误!"

    @operator_audit_decorator("IPDesign")
    def _subnet_new(self, request_data):
        """
        新添加子网或在某个网络上新划分子网
        :param request_data: POST提交的数据{"value":{...}, "action":"new"}
        :return:
        """
        try:
            post_value = request_data.get("value")
            post_value = common.filter_dict(post_value)

            if post_value.get("parentip_id", None):
                # 父ID不为空,表示划分子网,为空则添加新的网段, 划分子网需要检测新的子网是否是父IP的子网
                check_result = self.__ip_subnet_validate(post_value.get("ipaddr", None), post_value.get("maskbits", 0),
                                                         post_value.get("parentip_id"))
                if not check_result:
                    return
            # 判断IP子网是否已经存在
            if self.__check_ip_subnet_exists(post_value.get("ipaddr", None), post_value.get("maskbits", 0)):
                return

            post_value.update(dict(id=nextid(cmdb_models.IPDesign._meta.db_table, self.custid),
                                   cust_id=request_data.get("custid"),
                                   createuser=request_data.get("user").username,
                                   ))
            if post_value:
                new_obj = cmdb_models.IPDesign.objects.create(**post_value)

                self.ret["info"] = "添加成功"
                self.ret["category"] = "success"
                self.ret["status"] = True
                self.ret["data"] = dict(id=new_obj.id, ipaddr=new_obj.__str__(), ipcounts=new_obj.counts,
                                        allocatecount=0,
                                        datacenter=new_obj.datacenter.name if new_obj.datacenter_id and new_obj.datacenter else "",
                                        netarea=new_obj.netarea.name if new_obj.netarea_id and new_obj.netarea else "",
                                        remark=new_obj.remark)
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "系统错误!"
        # 此处可以不用ret,为了审计需要加了return
        return self.ret

    @operator_audit_decorator("IPDesign")
    def _subnet_edit(self, request_data):
        """
        编辑子网
        :param request_data: POST提交的数据,{"value":{...},"action":"edit"}
        :return:
        """
        try:
            post_value = request_data.get("value")
            obj = cmdb_models.IPDesign.objects.filter(id=post_value.get("id", 0))
            if obj.count() == 0:
                # 未找到记录
                self.ret["info"] = "参数错误,未找到记录!"
            else:
                # 检测IP是否是有效子网
                check_result = self.__ip_subnet_validate(post_value.get("ipaddr"), post_value.get("maskbits"),
                                                         obj.first().parentip_id)
                if not check_result:
                    return

                # 判断IP子网是否已经存在
                if self.__check_ip_subnet_exists(post_value.get("ipaddr", None), post_value.get("maskbits", 0),
                                                 int(post_value.get("id", 0))):
                    return

                obj.update(**post_value)
                self.ret["info"] = "修改成功"
                self.ret["category"] = "success"
                self.ret["status"] = True
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "系统错误"

    def _ip_new(self, request_data):
        """
        IP规划页面对C类地址分配IP地址段
        :param request_data:
        :return:
        """
        from afcat.cmdb.packages.cmdbsignals import operate_audit
        try:
            ip_obj_list = list()
            post_value = request_data.get("value")
            start_ip = post_value.get("startip", 0)
            end_ip = post_value.get("endip", 0)
            # 检测IP地址合法性
            if self.__ip_is_validate(start_ip, end_ip):
                net_part = ".".join(start_ip.split('.')[:-1])
                s_ip_part = int("".join(start_ip.split('.')[-1:]))
                e_ip_part = int("".join(end_ip.split('.')[-1:])) + 1
                # 判断其实IP是否小于结束IP
                if s_ip_part > e_ip_part:
                    self.ret["info"] = "IP填写错误,起始IP地址大于结束IP!"
                    self.ret["category"] = "error"
                    self.ret["status"] = False
                else:
                    # 检测IP是否是指定IP的子网IP
                    if post_value.get("ipmask_id", None):
                        # 检测要分配的IP子网的IP
                        parent_subnet_obj = cmdb_models.IPDesign.objects.filter(
                            id=int(post_value.get("ipmask_id"))).first()
                        if parent_subnet_obj:
                            parent_subnet = "{0}/{1}".format(parent_subnet_obj.ipaddr, parent_subnet_obj.maskbits)
                            start_ip_in_subnet = ipaddress.ip_address(start_ip) in ipaddress.ip_network(parent_subnet)
                            end_ip_in_subnet = ipaddress.ip_address(end_ip) in ipaddress.ip_network(parent_subnet)
                            if start_ip_in_subnet and end_ip_in_subnet:
                                for i in range(s_ip_part, e_ip_part):
                                    ipaddr = "{0}.{1}".format(net_part, str(i))
                                    ip_obj = cmdb_models.IPManage(
                                        id=nextid(cmdb_models.IPManage._meta.db_table, self.custid),
                                        ipaddr=ipaddr,
                                        ipmask_id=post_value.get("ipmask_id"),
                                        status=post_value.get("status"),
                                        vlan=post_value.get("vlan"),
                                        allocateuser=request_data.get("user").username,
                                        allocateto=post_value.get("allocateto"),
                                        cust_id=request_data.get("custid"),
                                        remark=post_value.get("remark")
                                    )
                                    ip_obj_list.append(ip_obj)
                                # 批量写入
                                cmdb_models.IPManage.objects.bulk_create(ip_obj_list)
                                # 审计日志(此处由于不是单条记录创建,是批量创建无法调用信号,之前通用审计接口也无法使用,未想到更好办法,写死了)
                                operate_audit.send(sender=cmdb_models.IPManage,
                                                   data="分配{0}-{1}({2}）".format(start_ip, end_ip,
                                                                                post_value.get("allocateto")),
                                                   instance=cmdb_models.IPManage,
                                                   user=request_data.get("user"), action="new", cust_id=self.custid)
                                self.ret["info"] = "创建成功"
                                self.ret["category"] = "success"
                                self.ret["status"] = True
                            else:
                                self.ret["info"] = "IP地址不合法,非子网IP!"
                                self.ret["category"] = "error"
                                self.ret["status"] = False

        except Exception as e:
            logger.error(e)
            self.ret["info"] = u"内部错误"

    @operator_audit_decorator("IPManage")
    def _ip_edit(self, request_data):
        """
        编辑IP管理地址信息
        :param request_data:
        :return:
        """
        try:
            post_value = request_data.get("value")
            if not post_value:
                self.ret["info"] = "参数错误!"
            else:
                qset = cmdb_models.IPManage.objects.filter(id=int(post_value.get("id", 0)))
                if qset.count() > 0:
                    qset.update(**dict(id=post_value.get("id"), allocateto=post_value.get("allocateto"),
                                       vlan=post_value.get("vlan"), remark=post_value.get("remark")))
                    self.ret["info"] = "修改成功!"
                    self.ret["category"] = "success"
                    self.ret["status"] = True
                else:
                    self.ret["info"] = "未找到指定的记录!"
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "系统错误"

    @operator_audit_decorator("IPManage")
    def _ip_delete(self, request_data):
        """
        删除IP分配管理信息
        :param request_data:{"value":{”id":10011}, "action":"delete",“type":"ip"}
        :return:
        """
        try:
            post_data = request_data.get("value")

            if not post_data or not post_data.get("id", 0):
                self.ret["info"] = "参数错误,未找到删除记录"
            else:
                qset = cmdb_models.IPManage.objects.filter(id=post_data.get("id"))
                if qset.count() > 0:
                    qset.delete()
                    self.ret["info"] = "删除成功!"
                    self.ret["status"] = True
                    self.ret["category"] = "success"
                else:
                    self.ret["info"] = "参数错误,未找到删除记录"
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "系统错误!"

    def __ip_is_validate(self, start_ip, end_ip):
        """
        对两个IP进行有效性验证
        :param startip: 起始IP
        :param endip:  结束IP
        :return: True/False
        """
        check_flag = False
        if not (start_ip and end_ip):
            self.ret["info"] = "IP范围不能为空!"
        elif not (common.ip_check(start_ip) and common.ip_check(end_ip)):
            self.ret["info"] = "IP地址不合法!"
        elif ".".join(start_ip.split('.')[:-1]) != ".".join(end_ip.split('.')[:-1]):
            self.ret["info"] = "起始IP与结束IP非同一网段!"
        else:
            qset_sql = "SELECT * FROM cmdb.cmdb_ipmanage WHERE inet_aton(ipaddr) BETWEEN inet_aton('{0}') AND inet_aton('{1}')".format(
                start_ip, end_ip)
            qset = cmdb_models.IPManage.objects.raw(qset_sql)
            if len(list(qset)) == 0:
                check_flag = True
            else:
                self.ret["info"] = "存在已分配的IP地址!"

        return check_flag

    def ipinfo(self):
        """
        按条件搜索显示所有分配IP的信息
        :return:
        """
        kwargs = dict()
        try:
            ipaddr = self.request.GET.get("condition", "")
            status = self.request.GET.get("status", None)
            if status:
                kwargs.update({"status": status})
            result = self.__ip_allocate_info(mask_id=None, ipaddr=ipaddr, **kwargs)
            self.ret["data"] = result
            self.ret["category"] = "info"
            self.ret["status"] = True
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "内部错误!"
            self.ret["category"] = "error"
            self.ret["status"] = False

    def subnet_info(self):
        """
        按条件搜索显示所有子网信息
        :return:
        """
        try:
            condition = self.request.GET.get("condition", "")
            iplist = cmdb_models.IPDesign.objects.filter(cust_id=self.custid, ipaddr__contains=condition)
            result = self.__ip_design_details(iplist)
            self.ret["data"] = result
            self.ret["category"] = "info"
            self.ret["status"] = True
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "内部错误!"
            self.ret["category"] = "error"
            self.ret["status"] = False


class Balancemapping(BaseHandler):
    """
    F5映射信息接口
    """
    from afcat.account.core.permission import operator_audit_decorator

    def __init__(self, method=None, request=None, *args, **kwargs):
        super(Balancemapping, self).__init__(method=method, request=request)
        self.args = args
        self.kwargs = kwargs
        self.custid = self.request.session.get("custid", None)

    def info(self):
        """
        获取所有映射信息
        :return:
        """
        data = list()
        try:
            search_condition = self.request.GET.get("condition", "")
            if self.custid:
                objs = self._get_all_data(search_condition)

                show_record = common.page_split(objs, self.page, self.per_page_count)
                obj_list = show_record.get("record")
                if show_record.get("total_count", 0) > 0:
                    for obj in obj_list:
                        data.append(self._get_details(obj))
                    show_record["record"] = data
                else:
                    show_record["record"] = []
                self.ret["data"] = show_record
        except Exception as e:
            logger.error(e)
            self.ret["info"] = u"内部错误"
            self.ret["category"] = u"error"

    def _get_all_data(self, search_condition):
        """
        根据条件获取所有记录
        :param condition:查询条件
        :return:
        """
        try:
            data = ipmanage.get_balance_mapping_data(self.custid, search_condition)
            return data
        except Exception as e:
            logger.error(e)
            return []

    def operate(self):
        try:
            post_data = common.get_request_data(self.request)
            action = post_data.get("action")
            if hasattr(self, action):
                func = getattr(self, action)
                func(post_data)
            else:
                self.ret["info"] = "请求参数错误,未找到指定方法!"
                self.ret["category"] = "error"
                self.ret["status"] = False
        except Exception as e:
            logger.error(e)

    @operator_audit_decorator("BalanceMapping")
    def new(self, post_data):
        """
        新增映射记录
        :param post_data:  提交的数据
        :return:
        """
        try:
            post_value = post_data.get("value")
            if post_value:
                exist_flag = self._check_vsname_exists(post_value.get("vsname"), post_value.get("vsaddr"),
                                                       post_value.get("port"))
                if exist_flag:
                    self.ret["info"] = "已存在此名称或IP的配置信息!"
                    self.ret["category"] = "warning"
                    self.ret["status"] = False
                    self.ret["data"] = {}
                else:
                    post_value.update(dict(id=nextid(cmdb_models.BalanceMapping._meta.db_table, custid=self.custid)))
                    # post_value.update(dict(business=",".join(post_value.get("business"))))
                    new_obj = cmdb_models.BalanceMapping.objects.create(**post_value)
                    if new_obj:
                        self.ret["info"] = "添加成功"
                        self.ret["data"] = common.get_record_all_fields(new_obj)
            else:
                self.ret["info"] = "添加失败,参数错误!"
                self.ret["category"] = "error"
                self.ret["status"] = False
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "内部错误"
            self.ret["category"] = "error"

        return self.ret

    @operator_audit_decorator("BalanceMapping")
    def edit(self, post_data):
        """
        编辑记录
        :param post_data: POST提交的数据
       :return:
        """
        try:

            post_value = post_data.get("value")
            if post_value:
                obj_id = post_value.get("id", None)
                if obj_id:
                    cmdb_models.BalanceMapping.objects.filter(id=int(obj_id)).update(**post_value)
                    self.ret["info"] = u"更新成功!"
                    self.ret["catetory"] = "success"
                    self.ret["status"] = True

                else:
                    self.ret["info"] = u"参数错误,未找到记录!"
                    self.ret["category"] = "error"
        except Exception as e:
            logger.error(e)

    @operator_audit_decorator("BalanceMapping")
    def delete(self, post_data):
        """
        删除指定的数据记录
        :param post_data:{"id":10011,"action":delete"}
        :return:
        """
        try:
            post_value = post_data.get("value", "")
            if not post_value:
                self.ret["info"] = "参数错误"
                self.ret["category"] = "error"
            else:
                cmdb_models.BalanceMapping.objects.filter(id=int(post_value.get("id"))).delete()
                self.ret["info"] = "删除成功"
                self.ret["category"] = "success"
        except Exception as e:
            logger.error(e)
            self.ret["info"] = "系统错误"
            self.ret["category"] = "error"

    def loadequipment(self, post_data):
        """
        获取指定区域的网络设备信息
        :param post_data: {action:"loadequipment", value:{netarea_id:10012}}
        :return:
        """
        result_list = list()
        try:
            post_value = post_data.get("value", "")
            if not post_value:
                self.ret["info"] = "请求参数错误,未指定值"
                self.ret["category"] = "error"
            else:
                equipment_list = cmdb_models.Equipment.objects.filter(cust_id=self.custid,
                                                                      netarea_id=post_value.get("netarea_id"))
                if equipment_list.count() > 0:
                    for equipment in equipment_list:
                        result_list.append(dict(id=equipment.id, name=equipment.__str__()))
                self.ret["data"] = result_list
        except Exception as e:
            logger.error(e)

    def _get_details(self, map_obj):
        """
        获取负载映射表中记录对象的详细信息,返回前端渲染
        :param map_obj: 数据对象
        :return:
        """
        try:
            info = ipmanage.get_balance_mapping_detail_info(map_obj)
            return info
        except Exception as e:
            logger.error(e)
            return ""

    def _check_vsname_exists(self, vsname, vsaddr, port):
        """
        检测添加的映射记录是否已经存在，主要检测vsname 和 vsaddr:port 是否已经添加
        :param vsname:
        :return:
        """
        exist_flag = False
        try:
            qset_count = cmdb_models.BalanceMapping.objects.filter(
                Q(vsname=vsname) | Q(vsaddr=vsaddr, port=port)).count()
            if qset_count > 0:
                exist_flag = True
        except Exception as e:
            logger.error(e)
        return exist_flag


class Tableproperty(BaseHandler):
    """
    扩展表属性及自定义表字段处理接口
    """

    def __init__(self, method=None, request=None, *args, **kwargs):
        super(Tableproperty, self).__init__(method=method, request=request)
        self.args = args
        self.kwargs = kwargs
        self.custid = self.request.session.get("custid", None)

    def load_filed_alias(self):
        """
        获取表的自定义显示别名, 必须指定表的models名称 e.g: Equipment
        :return: 各列的自定义显示名称
        """
        field_info = dict(default=None, extend=None)
        try:
            post_data = common.get_request_data(self.request)
            # post_data = self.request.GET
            model_name = post_data.get("models", None)
            if not model_name or not hasattr(cmdb_models, model_name):
                self.ret["info"] = "参数错误,模块名称不存在!"
                self.ret["category"] = "error"
                self.ret["status"] = False
            else:
                model_obj = getattr(cmdb_models, model_name)
                # 获取主表的自定义显示名称
                field_info = common.get_field_verbose_name(model_obj, self.custid)
                # 获取所有关联关系的表中的自定义名称
                for related_obj in model_obj._meta.related_objects:
                    field_info.update(common.get_field_verbose_name(related_obj.related_model, self.custid))

                self.ret["data"] = field_info
                self.ret["status"] = True
        except Exception as e:
            logger.error(e)

    def createfield(self):
        """
        创建自定义扩展字段,
        参数：
        :return:
        """
        model_customer_fields = list()
        try:
            post_data = common.get_request_data(self.request)
            # post_data = self.request.GET
            model_name = post_data.get("models", None)
            verbose_name = post_data.get("label", None)

            if not (model_name and verbose_name and hasattr(cmdb_models, model_name)):
                self.ret["info"] = "参数错误,需指定标签及模块名称"
                self.ret["category"] = "error"
                self.ret["status"] = False
            else:
                model_obj = getattr(cmdb_models, model_name)

                # 获取主表所有可扩展的自定义列
                model_all_fields = [field.column for field in model_obj._meta.fields]
                for field in model_all_fields:
                    if re.search('customer\d{3}', field):
                        model_customer_fields.append(field)
                # 获取当前已经占用的自定义列
                defined_field_objs = cmdb_models.CustomerTableProperty.objects.filter(cust_id=self.custid,
                                                                                      tablename=model_name)

                if defined_field_objs.count() > 0:
                    defined_fields = [obj.tablefield for obj in defined_field_objs]
                    # 获取可以使用的自定义列
                    set_all_fields = set(model_customer_fields)
                    set_defined_fields = set(defined_fields)
                    source_result = list(set_all_fields.difference(set_defined_fields))
                    if len(source_result) > 0:
                        source_result.sort()
                        tablefield = source_result[0]  # 可以用的自定义列
                    else:
                        tablefield = None
                else:
                    # 还没有自定义过,取第一个
                    tablefield = 'customer001'

                if not tablefield:
                    self.ret["info"] = "超过自定义最大值"
                    self.ret["category"] = "error"
                    self.ret["result"] = False
                else:
                    cmdb_models.CustomerTableProperty.objects.create(propertykey=verbose_name,
                                                                     propertyname=verbose_name,
                                                                     tablename=model_name,
                                                                     tablefield=tablefield,
                                                                     cust_id=self.custid)
                    self.ret["info"] = "创建成功"
                    self.ret["category"] = "success"
                    self.ret["result"] = True
                    self.ret["data"] = {"verbose_name": verbose_name, "to_field": tablefield}

        except Exception as e:
            logger.error(e)
            self.ret["info"] = "系统错误,创建失败!"
            self.ret["category"] = "error"
            self.ret["result"] = False
