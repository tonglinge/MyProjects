#!/usr/bin/env python
from django.db.models import Manager
from django.db import connections
from copy import copy
from datetime import datetime


class BaseCustomManage(Manager):
    """
    自定义Manage基类,首页图表所需要数据时用,只返回两列数据
    """

    def fetch_report_data(self, sql):
        result_list = []
        with connections["cmdb"].cursor() as cursor:
            cursor.execute(sql)
        for row in cursor.fetchall():
            record = self.model()
            record.name = row[0]
            record.value = row[1]

            result_list.append(record)
        return result_list

    def difference_update(self, result_data, show_data):
        """
        获取每月数据时对比结果与需要显示的月份数据,进行合并
        :param result_data: [obj1,obj2}
        :param show_data: {'2016-12':0,'2016-11':0....}
        :return: {'2016-12':11,'2016-11':0...}
        """
        # 对于没有在月记录列表值为0
        # print(result_data, show_data)
        return_data = copy(show_data)
        if len(result_data) > 0:
            for month_data in result_data:
                if month_data.name in show_data.keys():
                    return_data.update({month_data.name: month_data.value})
        return return_data


class EquipmentManage(BaseCustomManage):
    def equipment_type_group_count(self, custid=None):
        """
        统计网络设备数量,按设备类型分类统计
        :return:
        """
        sql = """
            SELECT t.name,count(*) type_count FROM
              cmdb.cmdb_equipment e,
              cmdb.cmdb_baseequipmenttype t
            WHERE t.id = e.assettype_id"""
        if custid:
            sql = "{0} AND e.cust_id='{1}' ".format(sql, custid)
        sql = "{0} GROUP BY e.assettype_id".format(sql)
        result_list = self.fetch_report_data(sql)
        return result_list

    def month_group_count(self, month_value_dict, custid=None):
        """
        获取当前月份以及之前12月内所有设备数量统计
        :param custid: 客户ID
        :return:
        """
        sql = """
                SELECT DATE_FORMAT(createdate, '%Y-%m') mon, COUNT(*)
                FROM cmdb.cmdb_equipment
                WHERE createdate >= date_add(sysdate(), interval -12 month)
                """
        if custid:
            sql = "{0} AND id LIKE '{1}%' ".format(sql, custid)
        sql = "{0} GROUP BY mon ORDER BY createdate".format(sql)
        result_list = self.fetch_report_data(sql)
        month_value_dict = self.difference_update(result_list, month_value_dict)
        return month_value_dict


class AssetsManage(BaseCustomManage):
    def asset_type_group_count(self, custid=None):
        """
        统计服务器设备数量,按设备类型统计
        :param custid:
        :return:
        """
        sql = """
            SELECT t.name, COUNT(*) FROM
              cmdb.cmdb_assets a,
              cmdb.cmdb_baseassettype t
            WHERE
              t.id = a.usetype_id"""
        if custid:
            sql = "{0} AND a.cust_id='{1}' ".format(sql, custid)
        sql = "{0} GROUP BY a.usetype_id".format(sql)

        result_list = self.fetch_report_data(sql)
        return result_list

    def month_group_count(self, month_value_dict,custid=None):
        """
        获取当前月份以及之前12月内所有设备数量统计
        :param custid: 客户ID
        :return:
        """
        try:
            sql = """
                    SELECT DATE_FORMAT(createdate, '%Y-%m') mon, COUNT(*)
                    FROM cmdb.cmdb_assets
                    WHERE createdate >= date_add(sysdate(), interval -12 month)
                    """
            if custid:
                sql = "{0} AND id LIKE '{1}%' ".format(sql, custid)
            sql = "{0} GROUP BY mon ORDER BY createdate".format(sql)
            result_list = self.fetch_report_data(sql)
            month_value_dict = self.difference_update(result_list, month_value_dict)
        except Exception as e:
            pass
        return month_value_dict


class HostManage(BaseCustomManage):
    def os_group_count(self, custid=None):
        """
        获取主机的报表数据,通过操作系统进行分类
        :param custid: 客户id
        :return:
        """
        sql = """
            SELECT name, SUM(scount) FROM
              (SELECT sf.name, COUNT(si.server_id) scount  FROM
                cmdb.cmdb_installedsoftlist si, cmdb.cmdb_basesofttype st, cmdb.cmdb_basesoft sf
              WHERE  si.soft_id = sf.id  AND sf.type_id = st.id AND st.name in ('操作系统','OS')
              """
        if custid:
            sql = "{0} AND si.id like '{1}%' ".format(sql, custid)
        sql = "{0} GROUP BY si.soft_id) tmpdb GROUP BY name".format(sql)

        result_list = self.fetch_report_data(sql)
        return result_list

    def month_group_count(self, month_value_dict, custid=None):
        """
        获取当前月份以及之前12月内所有设备数量统计
        :param custid:客户id
        :param month_value_dict: 要显示的所有月记录初始列表[{'2016-12':0},{'2016-11':0},.....]
        :return:
        """
        sql = """
            SELECT DATE_FORMAT(createdate, '%Y-%m') mon, COUNT(*)
            FROM cmdb.cmdb_servers
            WHERE createdate  >= date_add(sysdate(), interval -12 month)
        """
        if custid:
            sql = "{0} AND id LIKE '{1}%' ".format(sql, custid)
        sql = "{0} GROUP BY mon ORDER BY createdate".format(sql)
        result_list = self.fetch_report_data(sql)
        asset_result = month_value_dict
        month_value_dict = self.difference_update(result_list, asset_result)
        return month_value_dict


class AuditManage(Manager):
    def log_action(self, operater, action, model_name, operate_data, object_pk):
        self.model.objects.create(
            operater=operater,
            action=self.action_repr(action),
            model_name=model_name,
            operate_data=operate_data,
            object_pk=object_pk
        )

    def action_repr(self, action):
        """
        根据action动作返回中文
        :param action:
        :return:
        """
        result_repr = ""
        if action in ['del', 'delete']:
            result_repr = u"删除"
        if action in ['new']:
            result_repr = u"添加"
        if action in ['edit', 'change']:
            result_repr = u"编辑"
        return result_repr

    def last_record(self, start_index=0, end_index=10):
        """
        获取指定返回的审计记录, 默认按时间倒序排序最近10条
        :param start_index:开始记录
        :param end_index:结束记录
        :return:
        """
        try:
            result_record = self.model.objects.all().order_by("-operate_time")[start_index: end_index]
            record_list = [dict(operater=obj.operater, action=obj.action, model_name=obj.model_name,
                                operate_time=datetime.strftime(obj.operate_time, "%Y-%m-%d %H:%M"), operate_data=obj.operate_data)
                           for obj in result_record]
        except Exception as e:
            record_list = []
        return record_list
