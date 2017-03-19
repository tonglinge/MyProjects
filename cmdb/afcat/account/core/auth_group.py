#!/usr/bin/env python
"""
权限认证中组的管理模块
"""
from django.contrib.auth.models import Group, ContentType
from guardian.shortcuts import assign_perm, remove_perm, get_objects_for_group
from afcat.account.models import Menus
from afcat.cmdb.models import Projects, BaseEquipmentType
from afcat.api.libs.public import Logger, response_format
logger = Logger(__name__)


def load_group_all_perms(custid, gid=0):
    """
    获取一个组拥有的所有权限信息
    :param custid: 当前选择的客户
    :param gid: 组ID
    :return: 所有权限信息的字典
    """
    perm_list = dict()
    group_obj = Group.objects.filter(id=gid).first()
    if group_obj:
        perm_list.update({"menu": load_group_menu_perms(group_obj)})
        perm_list.update({"projects": load_group_projects_perms(group_obj, custid)})
        perm_list.update({"equipmenttype": load_group_assettype_perms(group_obj, custid)})
    return perm_list


def load_groups_perms(group_obj, app_label, model, custid=None):
    """
    获取组在某个模块的所有权限对象
    :param group_obj: 权限组对象
    :param app_label: app名
    :param model:models名
    :return: 组包含的所有对象权限
    """
    project_perm_obj = dict()
    content_type = ContentType.objects.get(app_label=app_label, model=model)
    check_perm_list = content_type.permission_set.all()
    # 获取权限组对象拥有的所有project列表
    for check_perm in check_perm_list:
        perm_type = check_perm.codename.split("_")[0]
        if not group_obj:
            perm_projects = []
        else:
            perm_projects = get_objects_for_group(group_obj, "{0}.{1}".format(check_perm.content_type.app_label,
                                                                              check_perm.codename))
        # 对于分客户的处理,将单个组的所有权限对象进行客户过滤
        if custid:
            perm_projects.filter(object_pk__startswith=custid)
        project_perm_obj.update({perm_type: perm_projects})
    return project_perm_obj


def load_group_menu_perms(group_obj):
    """
    获取权限组的所有菜单权限
    :param group_obj: 组对象
    :return:
    """
    check_perm = "account.view_menus"
    menu_perm_info = list()
    all_menus_obj = Menus.objects.filter(is_avaible=1).order_by("menu_code")
    # 获取组所能访问的菜单
    if not group_obj:
        # 组不存在,则所有权限认为为空
        group_menu_obj = list()
    else:
        group_menu_obj = get_objects_for_group(group_obj, check_perm)

    for menu_obj in all_menus_obj:
        has_perm = 1 if menu_obj in group_menu_obj else 0
        menu_perm = dict(id=menu_obj.id, name=menu_obj.menu_name, view=has_perm)
        menu_perm_info.append(menu_perm)

    return menu_perm_info


def load_group_projects_perms(group_obj, custid):
    """
    获取权限组的所有 projects 权限
    :param group_obj: 权限组对象
    :return: 所有projects的权限列表
    """
    all_projects_obj = list()
    project_perm_obj = load_groups_perms(group_obj,"cmdb","projects")

    # 所有projects列表及权限信息
    # projects = Projects.objects.all().order_by("id")
    projects = Projects.objects.filter(id__startswith=str(custid))
    for project in projects:
        view_perm = 1 if project in project_perm_obj.get("view") else 0
        add_perm = 1 if project in project_perm_obj.get("add") else 0
        delete_perm = 1 if project in project_perm_obj.get("delete") else 0
        change_perm = 1 if project in project_perm_obj.get("change") else 0
        all_projects_obj.append(
            dict(name=project.sysname, id=project.id, view=view_perm, add=add_perm, deleted=delete_perm,
                 change=change_perm))

    return all_projects_obj


def load_group_assettype_perms(group_obj, custid):
    """
    获取权限组包含设备资产的类型权限信息
    :param group_obj:
    :return:
    """
    all_assettype_obj = list()
    basetype_perm_obj = load_groups_perms(group_obj, "cmdb", "baseequipmenttype")

    # 获取所有设备分类子类的对象,并获取各对象权限
    # assettype_obj_list = BaseEquipmentType.objects.all().order_by("id")
    assettype_obj_list = BaseEquipmentType.objects.filter(id__startswith=str(custid))
    for type_obj in assettype_obj_list:
        view_perm = 1 if type_obj in basetype_perm_obj.get("view") else 0
        add_perm = 1 if type_obj in basetype_perm_obj.get("add") else 0
        change_perm = 1 if type_obj in basetype_perm_obj.get("change") else 0
        delete_perm = 1 if type_obj in basetype_perm_obj.get("delete") else 0
        all_assettype_obj.append(
            dict(name=type_obj.name, id=type_obj.id, view=view_perm, add=add_perm, deleted=delete_perm,
                 change=change_perm))

    return all_assettype_obj


def load_groups():
    """
    获取所有组信息
    :return:
    """
    group_list = list()
    groups = Group.objects.all().order_by("id")
    for group in groups:
        group_list.append(dict(id=group.id, name=group.name))
    return group_list


def get_group_perms_model(perm):
    """
    获取权限组中权限对应的操作的表名(model)
    :param perm: 要查找的权限名
    :return: model名
    """
    perm_mapping_table = {
        "account.view_menus": Menus,
        "cmdb.view_projects": Projects,
        "cmdb.change_projects": Projects,
        "cmdb.add_projects": Projects,
        "cmdb.delete_projects": Projects,
        "cmdb.view_baseequipmenttype": BaseEquipmentType,
        "cmdb.add_baseequipmenttype": BaseEquipmentType,
        "cmdb.change_baseequipmenttype": BaseEquipmentType,
        "cmdb.delete_baseequipmenttype": BaseEquipmentType,
    }
    return perm_mapping_table.get(perm)


def assign_groups_perms(gid, group_perms):
    """
    更新权限组的权限方法
    :param gid: 权限组id
    :param group_perms:所有的权限字典信息
    :return:
    """
    if gid == 0 or not group_perms:
        update_status = False
    else:
        try:
            group_obj = Group.objects.get(id=gid)
            for perms_name, perms_id in group_perms.items():
                # 获取当前组在表中的已有权限并全部移除
                old_perms = get_objects_for_group(group_obj, perms_name)
                remove_perm(perms_name, group_obj, old_perms)
                # 添加新的权限
                model_obj = get_group_perms_model(perms_name)
                # print(perms_name, model_obj)
                new_perms = model_obj.objects.filter(id__in=perms_id)
                assign_perm(perms_name, group_obj, new_perms)
            update_status = True
        except Exception as e:
            logger.error(e)
            update_status = False
    return update_status


def groups_modify(request_data):
    """
    增删改查组名
    :param resquest_data:POST提交数据
    :return: 成功失败信息
    """

    action = request_data.get("action")
    result = response_format()
    result["category"] = "success"
    try:
        if action == "add":
            group_name = request_data.get('group_name')
            new_group = Group.objects.create(name=group_name)
            result["info"] = "添加成功"
            result["data"] = dict(id=new_group.id, name=new_group.name)
            return result
        if action == "change":
            group_name = request_data.get("group_name")
            group_id = request_data.get("id")
            Group.objects.filter(id=group_id).update(name=group_name)
            result["info"] = "更新成功"
        if action == "delete":
            group_id = request_data.get("id")
            # if this group contains users, delete will cancel
            group_obj = Group.objects.filter(id=group_id).first()
            if group_obj.user_set.count() > 0:
                result["info"] = u"该组包含 {0} 个用户,无法删除!".format(str(group_obj.user_set.count()))
                result["category"] = "warning"
                result["status"] = False
            else:
                group_obj.delete()
                result["info"] = "删除成功"
    except Exception as e:
        logger.error(e)
        result["info"] = "操作异常"
        result["status"] = False
        result["catagory"] = "error"
    return result
