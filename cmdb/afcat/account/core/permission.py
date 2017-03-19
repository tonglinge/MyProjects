#!/usr/bin/env python
"""
所有的权限操作方法
"""

import json

from django.contrib.auth.models import ContentType
from django.http.response import HttpResponse
from guardian.shortcuts import get_objects_for_user

from afcat.account import models as account_models
from afcat.api.libs.public import Logger
from afcat.cmdb import models as cmdb_models
from afcat.cmdb.libs.common import response_error
from afcat.cmdb.settings import PERMISSION_REQUIRE

logger = Logger(__name__)


def get_user_menus(user):
    """
    获取当前登录用户可以访问的菜单列表
    :param user: 当前登录用户
    :return: 可以访问的菜单列表['m_001_0','m_005_0' ....]
    """
    can_view_menu = []
    try:
        if user.is_superuser:
            menus = account_models.Menus.objects.filter(is_avaible=1)
        else:
            menus = get_objects_for_user(user, "account.view_menus")
        for menu in menus:
            can_view_menu.append(menu.menu_code)
    except Exception as e:
        logger.error(e)
    return can_view_menu


def permission_require(perms_check_type):
    """
    权限控制模块,对返回的数据进行权限的更新
    :param perms_check_type: 检测类型：view_list:查看资产列表信息; view_details: 查看详情
    :param func:views中的函数
    :return:  重新封装后的结果
    """

    def outer(func):
        def inner(request):
            if request.method == "POST":
                return func(request)

            get_param = json.loads(request.GET.get("data"))
            perm_model = get_param.get("model")
            # 当前操作的客户
            custid = request.session.get("custid")
            # print("Request Model:", perm_model)
            # 获取操作的类参数
            perm_data = models_perm_table(perm_model)

            if not perm_data:
                return response_error("您无权进行此操作,联系管理员开通权限!", request)
            else:
                if not perm_data.get("permission_require") or request.user.is_superuser:
                    # 不进行权限认证
                    return func(request)
                else:
                    # 实例化权限类
                    perm_obj = Perms(request.user, custid, **perm_data)
                    if perms_check_type == "view_list":
                        # 查看资产列表 asset_info 信息
                        perms_list = perm_obj.load_perms()
                        # print("Perms_List:", perms_list)
                        response = permission_response_for_view_list(func, request, perms_list)

                    if perms_check_type == "view_detail":
                        # 查看资产详情信息,如果用户不能编辑此资产,则无法操作所有的关联资产信息,只能查看
                        perms_list = perm_obj.load_perms()
                        response = permission_response_for_view_detail(func, request, perms_list)

                    if perms_check_type == "change_get":
                        response_data = func(request)
                        # print("In permissions:", response_data.content)
                        if request.method == "GET":
                            response = perm_obj.clear_request_data(response_data)
                    return response

        return inner

    return outer


def permission_response_for_view_list(func, request, perms_list):
    """
    查看资产列表信息时,对权限的控制
    将返回的数据进行权限判断后再处理并返回., 对每个对象添加 编辑和删除权限
    :param perms_list: 可以查看的所有的资产设备ID 列表
    :param func: 被装饰的函数（views中的函数)
    :return:
    """
    # 获取可以查看的id列表
    perm_id_list = perms_list.get("view")
    response = func(request, perm_id_list)

    # 获得返回数据的字典格式
    return_data = json.loads(response.content.decode())

    # 是否是成功返回的数据
    if return_data.get("status"):
        if request.user.is_superuser or perms_list.get("add"):
            return_data["data"]["addperm"] = True
        else:
            return_data["data"]["addperm"] = False

        # 获取所有的数据记录
        record_data = return_data["data"]["record"]
        # 允许编辑的资产ID
        change_id_list = perms_list.get("change")
        # 允许删除的资产ID
        delete_id_list = perms_list.get("delete")
        # 遍历所有返回数据,对于允许编辑或删除的数据修改权限值
        for record in record_data:
            if request.user.is_superuser or record.get("id") in change_id_list or change_id_list is None:
                record["changeperm"] = True
            else:
                record["changeperm"] = False
            if request.user.is_superuser or record.get("id") in delete_id_list or delete_id_list is None:
                record["delperm"] = True
            else:
                record["delperm"] = False
        response = HttpResponse(json.dumps(return_data))
    return response


def permission_response_for_view_detail(func, request, perm_list):
    """
    查看资产详细信息页面时的权限模块,当server信息中的changeperm为True时,才可以编辑所有的关联设备信息
    :param func:  view中请求的方法
    :param request:  httprequest对象
    :param perm_list: 资产的权限信息:增删改查的id列表
    :return:
    """
    response = func(request)
    return_data = json.loads(response.content.decode())
    # 获取允许编辑的资产 id 列表
    change_perm_id_list = perm_list.get("change", [])
    # 获取资产详细信息
    server_detail_info = return_data.get("data").get("server")
    if request.user.is_superuser or server_detail_info.get("id", 0) in change_perm_id_list:
        # 资产允许编辑
        server_detail_info["changeperm"] = True
    else:
        server_detail_info["changeperm"] = False
    response = HttpResponse(json.dumps(return_data))
    return response


def models_perm_table(model_name):
    """
    根据要请求的model名，获取执行权限的类
    :param model_name: request中请求的model名(server/equipment)
    :return:
    """
    from afcat.cmdb.libs import server, equipment, assets
    model_table = {
        "server": {"app_label": "cmdb", "related_model": "projects", "id_model": server,
                   "permission_require": PERMISSION_REQUIRE.get("server")},
        "assets": {"app_label": "cmdb", "related_model": None, "id_model": assets,
                   "permission_require": PERMISSION_REQUIRE.get("assets")},
        "equipment": {"app_label": "cmdb", "related_model": "baseequipmenttype", "id_model": equipment,
                      "permission_require": PERMISSION_REQUIRE.get("equipment")},
        "projects": {"app_label": "cmdb", "permission_require": PERMISSION_REQUIRE.get("projects")}
    }
    if model_name in model_table.keys():
        return model_table.get(model_name)
    else:
        return ""


def operator_audit_decorator(audit_model_name):
    """
    操作审计,主要对服务器资产，网络设备,主机设备及相关附属表的操作(增、删、改)的操作记录
    2017-01-23 增加对excel导入功能审计
    2017-02-15 增加对IP管理的增删改的审计
    :param audit_model_name: 操作的model名,主机下面的子表（关联表）是通用接口，用relatedmodel进行判断,都会传入asset(关联的model名）
    :return:
    """

    def outer(func):
        def inner(*args, **kwargs):
            try:
                # 获取请求数据信息,对于普通方法第一个参数request(取args[0]),对于类方法中的第一个为self(取args[1])
                # print("parameters...", args, kwargs)
                request_info = args[0] if isinstance(args[0], dict) else args[1]
                # print("请求数据",request_info)
                ret = ""  # 保存被装饰函数func执行结果
                op_object_id = 0  # 操作的对象的id
                op_object = None  # 根据id获取的对象
                op_object_info = ""  # 操作的具体数据
                model_object = None  # models中的model对象
                action = request_info.get("action")  # 动作
                op_user = request_info.get("user").username  # 操作人

                # 通过基表接口POST数据的,会传入一个table名(与models一致)
                if audit_model_name == "BaseData":
                    model_name = request_info.get("table")
                # 主机关联表的提交走通用接口,都会传入一个asset名(与models一致)
                elif audit_model_name == "ServerRelated":
                    model_name = request_info.get("asset")
                else:
                    model_name = audit_model_name
                # print(request_info, model_name)
                # 获取操作的model的名
                if hasattr(cmdb_models, model_name):
                    model_object = getattr(cmdb_models, model_name)
                    model_verbose_name = model_object._meta.verbose_name
                else:
                    model_verbose_name = ""

                if action in ["del", "delete"]:
                    # 删除操作从提交的数据中获取操作对象id
                    op_object_id = request_info.get("value", {"id": 0}).get("id", 0)
                    # 删除的先获取要操作对象的数据
                    op_object = model_object.objects.filter(id=op_object_id).first()
                    # 执行对应方法
                    ret = func(*args, **kwargs)

                if action == "edit":
                    op_object_id = request_info.get("value", {"id": 0}).get("id", 0)
                    ret = func(*args, **kwargs)
                    op_object = model_object.objects.filter(id=op_object_id).first()

                if action == "new":
                    ret = func(*args, **kwargs)
                    if ret:
                        op_object_id = ret["data"].get("id", 0) if ret.get("data") else 0
                        op_object = model_object.objects.filter(id=op_object_id).first()

                if action == "import":  # 导入数据的记录
                    ret = func(*args, **kwargs)
                    # print(ret)
                    op_object_id = ""
                    op_object_info = ret.get("info", "") if isinstance(ret, dict) else ""

                # print("[返回结果数据]:", ret)
                # if op_object:
                op_object_info = op_object.__str__() if op_object and not op_object_info else op_object_info

                # print("Audit Message: 动作:{0}, 操作人:{1}, 操作Models: {2}, "
                #       "操作类型:{3}, 操作对象ID：{4}, 操作对象:{5}".format(action,
                #                                               op_user,
                #                                               model_object._meta.object_name,
                #                                               model_verbose_name,
                #                                               op_object_id,
                #                                               op_object_info))
                if op_object_id:
                    cmdb_models.OperateAudit.audit.log_action(op_user, action, model_verbose_name, op_object_info,
                                                              op_object_id, request_info.get("custid", None))
                return ret
            except Exception as e:
                logger.error(e)
                return func(*args, **kwargs)

        return inner

    return outer


def get_user_managed_customer(user):
    """
    获取用户可以管理的客户信息,用户登录之后再渲染时中间件调用此方法(menu.py)
    :param user: 当前登录用户
    :return: {"custid":1001, "custalias":"xxxx"}
    """
    custinfo = []
    if not user.username == "":
        if hasattr(user, 'account'):
            managed_cust_id_list = user.account.cust_id.split(',')
            cust_obj_list = cmdb_models.BaseCustomerInfo.objects.filter(idcode__in=managed_cust_id_list)
            if cust_obj_list.count() > 0:
                custinfo = [{"custid": obj.idcode, "custalias": obj.custalias} for obj in cust_obj_list]
    return custinfo


class Perms(object):
    """
    权限管理类
    """

    def __init__(self, user, custid, app_label, related_model, id_model, permission_require=True):
        """
        构造函数，主要针对 CMDB 的主机和设备资产管理
        :param user: 当前登录的用户
        :param app_label:  "cmdb"
        :param related_model: 权限依赖表,Server:projects ,Equipment: baseequipmenttype
        :param id_model:  获取资产id的model： servers,euquipment
        """
        self.app_label = app_label
        self.check_user = user
        self.curr_custid = custid
        self.perm_table = related_model
        self.id_model = id_model
        self.permission_require = permission_require

    def get_model_permission_objects(self):
        """
        获取指定 app.mocdel 的所有权限的对象字典
        :return: 所有权限的对象
        e.g:
        user = User.objects.get(username='monitor')
        get_model_permission_objects("cmdb", "projects", user)
           return
           {
            'add_projects': {'table_perm': False, 'object_perm': True, 'data': [<Projects: 助学贷款系统>]},
            'delete_projects': {'table_perm': False, 'object_perm': False, 'data': []},
            'change_projects': {'table_perm': False, 'object_perm': False, 'data': []},
            'view_projects': {'table_perm': False, 'object_perm': True, 'data': [<Projects: 资金系 统(一期)>, <Projects: 核心系统>]}
            }
        """
        all_perms = dict()
        try:
            content_type = ContentType.objects.get(app_label=self.app_label, model=self.perm_table)
            perms = content_type.permission_set.all()
            for perm in perms:
                content_perms = dict()
                perm_label = "%s.%s" % (self.app_label, perm.codename)
                # print("perm_label: ---", perm_label)
                # 获取指定的所有的权限对象 get_objects_for_user(user,"cmdb.view_servers")
                # print(perm_label)
                perm_objects = get_objects_for_user(self.check_user, perm_label)
                content_perms.update({"data": list(perm_objects)})
                content_perms.update({"table_perm": self.check_user.has_perm(perm_label)})
                if perm_objects.count() > 0:
                    content_perms.update({"object_perm": True})
                else:
                    content_perms.update({"object_perm": False})
                perm_objects_list = {perm.codename: content_perms}
                all_perms.update(perm_objects_list)
        except Exception as e:
            logger.error(e)

        return all_perms

    def action_perm(self, action, perm_table):
        """
        根据要获取的权限动作返回一个 permission的codename
        :param action: 要获取的权限的动作: view, new, edit, delete
        :param perm_table: 要操作的model表名
        """
        action_perm_table = {
            "view": "view_%s" % perm_table,
            "new": "add_%s" % perm_table,
            "edit": "change_%s" % perm_table,
            "delete": "delete_%s" % perm_table
        }
        return action_perm_table.get(action, "")

    def load_perms(self):
        """
        获取当前用户能操作的资产的权限,对于查看、删除、编辑的权限则返回能操作的资产 ID 列表
        :return: 返回权限及id_list {"add":True/False,"view":[1,2,3],"change":[2,3,4],"delete":[3]}
                    None表示不限制
        """
        perm_dict = dict()
        try:
            if not self.check_user.is_superuser:
                # 如果用户没有权限的依赖表(服务器设备暂时未指定依赖关系表),则默认普通用户只能查看不能编辑
                # view:None 表示不限制
                if not self.perm_table:
                    perm_dict = {"add": False, "change": [], "view": None, "delete": []}
                else:
                    # 1 获取用户可以查看的资产关联的类型的所有权限信息(server关联projects, 设备关联类型baseequipmenttype)
                    user_projects_perm = self.get_model_permission_objects()

                    for perm_codename, perm_values in user_projects_perm.items():
                        perm_action = perm_codename.split("_")[0]
                        if perm_action == "add":
                            perm_status = perm_values.get("object_perm", False)
                        else:
                            # 获取所有权限能访问的具体对象的id列表
                            perm_status = self.id_model.get_id_list(perm_values.get("data", []), self.curr_custid)
                        perm_dict.update({perm_action: perm_status})
                        # print("Current User's Perms:", perm_dict)
            else:
                perm_dict = {"add": True, "change": None, "view": None, "delete": None}
                # print("perm_dict:", perm_dict)
        except Exception as e:
            logger.error(e)
        return perm_dict

    def clear_request_data(self, response_data):
        """
        添加或编辑服务器信息时,加载的"所属业务线"下拉框(projects)只能显示用户允许查看的系统名称,对此数进行清洗

        :param response_data: GET 请求的基表数据
        :return: 对请求的数据进行过滤后的数据
        """
        try:
            if not self.check_user.is_superuser:
                allow_change_projece_id = list()
                # 获取返回的所有projects 信息
                source_data = json.loads(response_data.content.decode())
                projects_data = source_data["data"].get(self.perm_table)
                # 获取所有的允许修改的 peojects 的ID列表
                project_perm_data = self.get_model_permission_objects()
                # print("Project_Perms", project_perm_data)

                for projects_obj in project_perm_data.get("add_{0}".format(self.perm_table)).get("data"):
                    allow_change_projece_id.append(projects_obj.id)
                # print("Allow Change PID:", allow_change_projece_id)
                # 开始过滤
                tmp_data = projects_data.copy()
                for project_info in tmp_data:
                    if project_info.get("id", 0) not in allow_change_projece_id:
                        projects_data.remove(project_info)
                response = HttpResponse(json.dumps(source_data))
            else:
                response = response_data
        except Exception as e:
            logger.error(e)
            response = response_data
        return response
