#!/usr/bin/env python
from copy import copy
from datetime import datetime

from django.db import connections
from django.db.models import Manager


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
        :param result_data: [obj1,obj2]
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
            SELECT
                *
            FROM
                (SELECT
                    CONCAT(t.name, '-', e.model) e_name, COUNT(*) type_count
                FROM
                    cmdb.cmdb_equipment e, cmdb.cmdb_baseequipmenttype t, cmdb.cmdb_basefactory f
                WHERE
                    t.id = e.assettype_id
                        AND e.factory_id = f.id
                        AND e.cust_id = '{0}'
                GROUP BY e.factory_id , e.assettype_id , e.model UNION SELECT
                    CONCAT(t.name, '-', e.model) e_name, COUNT(*) AS type_count
                FROM
                    cmdb.cmdb_equipment e, cmdb.cmdb_baseequipmenttype t
                WHERE
                    t.id = e.assettype_id
                        AND e.cust_id = '{0}'
                        AND e.factory_id IS NULL
                GROUP BY e.factory_id , e.assettype_id , e.model UNION SELECT
                    '其它' e_name, COUNT(*) type_count
                FROM
                    cmdb.cmdb_equipment e
                WHERE
                    e.cust_id = '{0}'
                        AND e.assettype_id IS NULL) _tmp
            ORDER BY e_name;
            """.format(custid)
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
                AND cust_id = '{0}'
                GROUP BY mon ORDER BY createdate
                """.format(custid)
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
            SELECT
                CONCAT(bat.name,'-',bast.name) r_name,
                COUNT(a.assettype_id) r_count
            FROM
                cmdb.cmdb_assets a,
                cmdb.cmdb_baseassettype bat,
                cmdb.cmdb_baseassetsubtype bast
            WHERE
                a.usetype_id = bat.id
                    AND a.assettype_id = bast.id
                    AND a.cust_id = {0}
            GROUP BY a.assettype_id , a.usetype_id
            ORDER BY a.usetype_id
        """.format(custid)

        result_list = self.fetch_report_data(sql)
        return result_list

    def month_group_count(self, month_value_dict, custid=0):
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
                    AND cust_id = '{0}'
                    GROUP BY mon ORDER BY createdate
                    """.format(custid)
            result_list = self.fetch_report_data(sql)
            month_value_dict = self.difference_update(result_list, month_value_dict)
        except Exception as e:
            pass
        return month_value_dict


class HostManage(BaseCustomManage):
    def os_group_count(self, custid=""):
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
              AND si.id like '{0}%'
              GROUP BY si.soft_id) tmpdb GROUP BY name
              """.format(custid)

        result_list = self.fetch_report_data(sql)
        return result_list

    def month_group_count(self, month_value_dict, custid=""):
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
            AND cust_id = '{0}'
            GROUP BY mon ORDER BY createdate
        """.format(custid)
        result_list = self.fetch_report_data(sql)
        asset_result = month_value_dict

        month_value_dict = self.difference_update(result_list, asset_result)
        return month_value_dict

    def item_group_count(self, custid=""):
        """
        按项目集进行分组,获取每个项目集下的所有主机数,会有重叠
        :param custid: 当前选中的客户idcode
        :return:
        """
        sql = """
        SELECT
            item.itemname, COUNT(ser.hostname)
        FROM
            cmdb.cmdb_servers ser,
            cmdb.cmdb_r_server_business ser_bu,
            cmdb.cmdb_business bu,
            cmdb.cmdb_projects pro,
            cmdb.cmdb_itemsset item
        WHERE
            ser.id = ser_bu.server_id
                AND bu.id = ser_bu.business_id
                AND bu.project_id = pro.id
                AND pro.itemsset_id = item.id
                AND ser.cust_id = '{0}'
        GROUP BY itemname
        UNION SELECT
            '未划分' itemname, COUNT(ser.hostname)
        FROM
            cmdb.cmdb_servers ser
        WHERE
            ser.id NOT IN (SELECT
                    ser_bu.server_id
                FROM
                    cmdb.cmdb_r_server_business ser_bu)
                AND ser.cust_id = '{0}'
        GROUP BY itemname
        """.format(custid)
        result_list = self.fetch_report_data(sql)
        return result_list


class AuditManage(Manager):
    """
    审计的自定义Manage
    """

    def log_action(self, operater, action, model_name, operate_data, object_pk, cust=None):
        self.model.objects.create(
            operater=operater,
            action=self.action_repr(action),
            model_name=model_name,
            operate_data=operate_data,
            object_pk=object_pk,
            cust_id=cust
        )

    def action_repr(self, action):
        """
        根据action动作返回中文
        :param action:
        :return:
        """
        action_dict = {"del": u"删除", "delete": u"删除", "new": u"新增", "edit": u"编辑", "change": u"编辑",
                       "restore": u"恢复数据", "import": u"导入"}
        result_repr = action_dict.get(action, "")

        return result_repr

    def last_record(self, cust_id,start_index=0, end_index=10):
        """
        获取指定返回的审计记录, 默认按时间倒序排序最近10条
        :param start_index:开始记录
        :param end_index:结束记录
        :return:
        """
        try:
            result_record = self.model.objects.filter(cust_id=cust_id).order_by("-operate_time")[start_index: end_index]
            record_list = self.record_details(result_record)
        except Exception as e:
            print(e)
            record_list = []
        return record_list

    def record_details(self, record_objs):
        """
        获取对象的详细信息
        :param record_objs: 对象集
        :return: 详细信息 列表
        """
        try:
            result_list = [dict(operater=obj.operater, action=obj.action, model_name=obj.model_name,
                                operate_time=datetime.strftime(obj.operate_time, "%Y-%m-%d %H:%M"),
                                operate_data=obj.operate_data)
                           for obj in record_objs]
            return result_list
        except Exception as e:
            return []
