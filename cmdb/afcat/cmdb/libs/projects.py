#!/usr/bin/env python
"""
项目信息相关方法
author: wngsong   2016-09-22
"""

from django.db.models import Q
from collections import OrderedDict
from afcat.cmdb import models
from afcat.cmdb.libs import common
from afcat.api.libs.public import response_format


def get_asset_list(page_index, condition, perm_id_list=""):
    """
    获取项目信息
    :param pageindex:页码{"page":1,"model":"projects","condition":{"key":"sys","value":""}}
    :param condition: 搜索条件
    :return:
    """
    try:
        data = dict()
        result = response_format()
        # 获取所有联系人的信息
        if not condition:
            all_projects = models.R_Project_Staff.objects.all()
        else:
            condition_key = condition.get("key", "")
            condition_value = condition.get("value", "")
            if condition_key == "sys":
                all_projects = models.R_Project_Staff.objects.filter(
                    Q(project__sysname__contains=condition_value) | Q(
                        project__sysalias__contains=condition_value))
            elif condition_key == "staff":
                all_projects = models.R_Project_Staff.objects.filter(
                    Q(staff__alias__contains=condition_value) | Q(staff__name__contains=condition_value)
                )
            else:
                all_projects = models.R_Project_Staff.objects.all()
                # 分页
        print(all_projects)
        if all_projects.count() > 0:
            staff_list = list()  # 联系人列表
            project_idlist = list()  # 联系人所属项目id
            record_info = list()  # 所有的记录结果
            page_split_result = common.page_split(all_projects, page_index)
            record_obj_list = page_split_result.get("record")
            print("split_count", record_obj_list)
            for project_obj in record_obj_list:
                if project_obj.project_id not in project_idlist:
                    project_idlist.append(project_obj.project_id)
                    staff_list = []
                project_info = dict(name=project_obj.staff.name,
                                    department=project_obj.staff.department.name if project_obj.staff.department else "",
                                    mobile=project_obj.staff.mobile,
                                    tel=project_obj.staff.tel,
                                    email=project_obj.staff.email,
                                    role=project_obj.role.role_name if project_obj.role else ""
                                    )
                staff_list.append(project_info)
                record_info.append({"project": project_obj.project.sysname,
                                    "project_id": project_obj.project_id,
                                    "staffs": staff_list
                                    })
            data.update(OrderedDict({"record": record_info, "num_pages": page_split_result["num_pages"],
                                     "curr_page": page_split_result["curr_page"]}))
    except Exception as e:
        common.writelog("[cmdb.projects.get_asset_list] " + str(e))
        result["info"] = "未找到记录信息"
        data.update({"record": "", "num_pages": 1, "curr_page": 1})
    finally:
        result["data"] = data
        print(data)
        return result
