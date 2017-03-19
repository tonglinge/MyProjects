#!/usr/bin/env python
"""
excel 对象生成模块,返回文件流格式
主要使用xlswriter创建excel对象,调用方法
1 实例化excel对象 excel_obj = Excel()
2 写excel的标题  excel_obj.write_title()
3 关闭excel对象  excel_obj.close()
4 返回的结果为对象的file属性  excel_obj.file,应用使用时也用这个
document: https://xlsxwriter.readthedocs.io/
"""
import io
import os
from datetime import datetime

import xlrd
import xlsxwriter


class Excel(object):
    def __init__(self, in_memory=True, file_name=None):
        """
        Constructor
        """
        self.in_memory = in_memory
        if in_memory:
            self.output = io.BytesIO()
            self.file_obj = xlsxwriter.Workbook(self.output, {"in_memory": True})
        else:
            self.file_obj = xlsxwriter.Workbook(file_name)
        self.title_format = self.file_obj.add_format({
            'font_name': '微软雅黑',
            'font_size': '9',
            'text_wrap': True,
            'valign': 'vcenter',
            'align': 'center',
            'bold': True,
            'bg_color': '#c7bcba',
            'border': 1,
            'border_color': '#434141'
        })
        self.row_format = self.file_obj.add_format({
            'font_name': '微软雅黑',
            'font_size': '9',
            'text_wrap': True,
            'valign': 'vcenter',
            'border': 1,
            'border_color': 'black'
        })
        self.row_height = 25
        self.file = None

    def close(self):
        """
        关闭对象
        :return:
        """
        self.file_obj.close()
        if self.in_memory:
            self.output.seek(0)
            self.file = self.output.read()

    def write_title(self, title_list, sheet_obj):
        """
        写excel的title 第一行
        :param sheet_obj: 要操作的sheet页对象
        :param title_list: 标题列表,包含列名和列宽  e.g: [('列0',5),('列1',10)..]
        :return:
        """
        sheet_obj.set_row(0, self.row_height)
        column_index = 0
        for column in title_list:
            sheet_obj.set_column(column_index, column_index, column[1])
            sheet_obj.write(0, column_index, column[0], self.title_format)
            column_index += 1

    def write_row(self, row_list, sheet_obj):
        """
        写excel中数据的行
        :param sheet_obj: 要操作的sheet页对象
        :param row_list:结果集的数据,列表,显示数据须与 title 顺序对应  e.g: [['1','host001',.....],['2','host002',....]]
        :return:
        """
        row_index = 1
        for record in row_list:
            sheet_obj.set_row(row_index, self.row_height)
            column_index = 0
            for column in record:
                sheet_obj.write(row_index, column_index, column, self.row_format)
                column_index += 1
            row_index += 1

    def create_sheet(self, sheet_name):
        """
        创建一个新的sheet页
        :param sheet_name: sheet名
        :return:
        """
        sheet_obj = self.file_obj.add_worksheet(sheet_name)
        return sheet_obj


class DownTemplate(object):
    """
    下载excel模板文件
    """

    def __init__(self, **kwargs):
        """
        构造方法
        :param isbase: 是否是基表数据导入,默认False,基表数据需要传入表名base_table
        :param kwargs: 传入包括操作表类型
                    template_name(assets,equipment,server),
                    file_type: 0: 样例文件, 1: 模板文件
        """
        self.template_type = kwargs.get("template_type")
        self.file_type = kwargs.get("file_type")
        self.base_table = kwargs.get("base_table")
        self.user = kwargs.get("user")
        self.cust = kwargs.get("custid")
        self.tmp_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exceltemplate")
        self.filename = "t_{0}.xlsx".format(self.template_type)
        self.xls_obj = None

    def get_template(self):
        """
        下载模板调用的唯一方法, 根据传入的参数获取要执行的方法并执行
        :return:
        """
        _file_IO = None
        if int(self.file_type):
            self.xls_obj = Excel(in_memory=True)
            # 模板文件
            func = self.__template_func()
            if func:
                func()
                self.xls_obj.close()
                _file_IO = self.xls_obj.file
            else:
                self.xls_obj.file = None

        else:
            # 样例文件
            _file_IO = self.__example_template
        # 关闭
        return _file_IO

    def __template_func(self):
        """
        模板类型及其对应的处理方法
        :return:
        """
        template_dict = {
            "assets": self.__asset_template,
            "server": self.__host_template,
            "equipment": self.__equipment_template,
            "serverstorage": self.__host_storage_template,
            "base": self.__base_template
        }
        func = template_dict.get(self.template_type, None)
        return func

    def __load_list_data(self, base_tables):
        """
        模板中下拉框选择的基表数据
        :param base_tables: 基表名及对应字段 [('BaseAssetType', ['name']), ('BaseAssetSubtype', ['name'])]
        :return: 字典格式的数据
        """

        from afcat.cmdb.libs import base
        tmp_dict = dict()
        for obj in base_tables:
            tmp_dict.update(base.load_base_table_record(obj[0], obj[1], self.cust))
            if len(obj[1]) == 1:
                tmp_dict.update({obj[0].lower(): [v.get(obj[1][0]) for v in tmp_dict.get(obj[0].lower())]})
            else:
                tmp_dict.update(
                    {obj[0].lower(): ["-".join(str(v.get(k)) for k in obj[1]) for v in tmp_dict.get(obj[0].lower())]})

        return tmp_dict

    def __asset_template(self):
        """
        服务器设备资产导入模板
        :return:
        """
        try:
            row_title = [("序列号(sn)", 15), ("服务器用途", 10), ("服务器分类", 10), ("生产厂商", 10), ("集成商", 10),
                         ("型号", 10), ("数据中心", 15), ("机房", 15), ("机柜", 10), ("管理IP", 10), ("集群信息", 15),
                         ("单元信息", 15), ("CPU数量", 10), ("内存(GB)", 10), ("硬件负责人", 20), ("购买日期", 15),
                         ("保修日期", 15), ("过保日期", 15), ("服务器状态", 15), ("所属环境", 15), ("备注", 20)]
            data_validate_table = [('BaseAssetType', ['name']), ('BaseAssetSubtype', ['name']),
                                   ('BaseFactory', ['name']),
                                   ('BaseDataCenter', ['name']), ('BaseMachineRoom', ['name']),
                                   ('BaseAssetStatus', ['status']), ('BaseNetArea', ['name'])]

            data_validate_dict = self.__load_list_data(data_validate_table)
            # 主sheet页
            sheet = self.xls_obj.create_sheet(u"assets")

            # 写title
            self.xls_obj.write_title(row_title, sheet)
            # 服务器用途序列
            sheet.data_validation(1, 1, 65535, 1, {'validate': 'list',
                                                   'source': data_validate_dict["baseassettype"]})
            # 服务器分类序列
            sheet.data_validation(1, 2, 65535, 2, {'validate': 'list',
                                                   'source': data_validate_dict["baseassetsubtype"]})
            # 生产厂商、集成商
            sheet.data_validation(1, 3, 65535, 3, {'validate': 'list',
                                                   'source': data_validate_dict["basefactory"]})
            sheet.data_validation(1, 4, 65535, 4, {'validate': 'list',
                                                   'source': data_validate_dict["basefactory"]})
            # 型号
            sheet.data_validation(1, 5, 65535, 5, {'validate': 'length',
                                                   'criteria': '>=',
                                                   'minimum': 1,
                                                   'error_type': 'stop',
                                                   'ignore_blank': False,
                                                   'input_message': '型号为必填项',
                                                   'error_message': '型号不能为空'
                                                   })
            # 数据中心
            sheet.data_validation(1, 6, 65535, 6, {'validate': 'list',
                                                   'source': data_validate_dict["basedatacenter"],
                                                   'input_message': '数据中心为必填项',
                                                   'error_message': '数据中心不能为空'
                                                   })
            # 机房
            sheet.data_validation(1, 7, 65535, 7, {'validate': 'list',
                                                   'source': data_validate_dict["basemachineroom"],
                                                   'input_message': '机房为必填项',
                                                   'error_message': '机房不能为空'
                                                   })
            # IP 限制不能重复
            sheet.data_validation(1, 9, 65535, 9, {'validate': 'custom',
                                                   'value': '=COUNTIF($1:$65535,J2)=1',
                                                   'input_message': 'IP唯一不可重复',
                                                   })
            # 服务器状态
            sheet.data_validation(1, 18, 65535, 18, {'validate': 'list',
                                                     'source': data_validate_dict["baseassetstatus"]})
            # 网络区域
            sheet.data_validation(1, 19, 65535, 19, {'validate': 'list',
                                                     'source': data_validate_dict["basenetarea"]})

        except Exception as e:
            print(e)

    def __equipment_template(self):
        """
        太原银行定制的导入数据模板
        :return:
        """
        row_title = [
            ("序号", 5), ("监控策略", 20), ("监控时间段", 15), ("设备管理IP", 15), ("团体字", 15), ("责任人", 20), ("逻辑区域", 15),
            ("机房位置", 20), ("设备类型", 10), ("管理组", 15), ("管理机构", 15), ("所属机构", 15), ("地域", 10), ("监控需求", 10),
            ("特殊需求", 10), ("别名", 10), ("用途", 8), ("机柜编号", 10), ("机内位置", 10), ("带内管理地址", 10),
            ("带外管理地址", 10), ("所属环境", 10), ("服务开始日期", 10), ("过保时间", 10), ("供应商", 15), ("服务提供商", 15),
            ("状态", 8), ("服务级别", 8), ("厂商", 15), ("设备型号", 8), ("设备序列号", 20), ("名称", 20), ("IOS版本", 20)
        ]
        try:
            data_validate_table = [('BaseEquipmentType', ['name']), ('BaseDataCenter', ['name']),
                                   ('BaseMachineRoom', ['name']), ('Staffs', ['name']),
                                   ('BaseAssetStatus', ['status']), ('BaseNetArea', ['name']),
                                   ('BaseFactory', ['name'])]

            data_validate_dict = self.__load_list_data(data_validate_table)
            # 主sheet页
            sheet = self.xls_obj.create_sheet(u"equipment")

            # 写title
            self.xls_obj.write_title(row_title, sheet)
            # IP 限制不能重复
            sheet.data_validation(1, 3, 65535, 3, {'validate': 'custom',
                                                   'value': '=COUNTIF($1:$65535,J2)=1',
                                                   'input_message': 'IP唯一不可重复',
                                                   })
            # 责任人
            sheet.data_validation(1, 5, 65535, 5, {'validate': 'list',
                                                   'source': data_validate_dict["staffs"]})
            # 机房
            sheet.data_validation(1, 7, 65535, 7, {'validate': 'list',
                                                   'source': data_validate_dict["basemachineroom"],
                                                   'input_message': '机房为必填项',
                                                   'error_message': '机房不能为空'
                                                   })
            # 设备分类 8
            sheet.data_validation(1, 8, 65535, 8, {'validate': 'list',
                                                   'source': data_validate_dict["baseequipmenttype"],
                                                   'input_message': '必填项'})
            # 生产厂商、供应商、服务商
            sheet.data_validation(1, 24, 65535, 24, {'validate': 'list',
                                                     'source': data_validate_dict["basefactory"]})
            sheet.data_validation(1, 25, 65535, 25, {'validate': 'list',
                                                     'source': data_validate_dict["basefactory"]})
            sheet.data_validation(1, 28, 65535, 28, {'validate': 'list',
                                                     'source': data_validate_dict["basefactory"]})

            # 设备状态
            sheet.data_validation(1, 26, 65535, 26, {'validate': 'list',
                                                     'source': data_validate_dict["baseassetstatus"]})
            # 网络区域 15
            sheet.data_validation(1, 21, 65535, 21, {'validate': 'list',
                                                     'source': data_validate_dict["basenetarea"],
                                                     'input_message': '必填项'})

            # SN、设备名称不能为空
            sheet.data_validation(1, 30, 65535, 30, {'validate': 'length',
                                                     'criteria': '>=',
                                                     'minimum': 1,
                                                     'error_type': 'stop',
                                                     'input_message': '必填项',
                                                     'ignore_blank': False,
                                                     'error_message': '序列号不能为空'
                                                     })
            sheet.data_validation(1, 1, 65535, 31, {'validate': 'length',
                                                     'criteria': '>=',
                                                     'minimum': 1,
                                                     'error_type': 'stop',
                                                     'input_message': '必填项',
                                                     'ignore_blank': False,
                                                     'error_message': '设备名称不能为空'
                                                     })
            #
            # # 数据中心
            # sheet.data_validation(1, 3, 65535, 3, {'validate': 'list',
            #                                        'source': data_validate_dict["basedatacenter"],
            #                                        'input_message': '必填项'})
            #
            # # U位 型号均必填
            # sheet.data_validation(1, 7, 65535, 7, {'validate': 'length',
            #                                        'criteria': '>=',
            #                                        'minimum': 1,
            #                                        'error_type': 'stop',
            #                                        'ignore_blank': False,
            #                                        'input_message': '必填项',
            #                                        'error_message': 'U位不能为空'
            #                                        })
            # sheet.data_validation(1, 8, 65535, 8, {'validate': 'length',
            #                                        'criteria': '>=',
            #                                        'minimum': 1,
            #                                        'error_type': 'stop',
            #                                        'ignore_blank': False,
            #                                        'input_message': '必填项',
            #                                        'error_message': '型号不能为空'
            #                                        })
            #

        except Exception as e:
            print(e)

    # def __equipment_template(self):
    #     """
    #     网络设备模板数据
    #     :return:
    #     """
    #     try:
    #         row_title = [("设备名称", 20), ("应用用途", 10), ("设备分类", 15), ("数据中心", 15), ("机房", 15), ("机柜", 15),
    #                      ("管理IP", 15), ("U位", 10), ("型号", 15), ("序列号", 20), ("电源数量", 10), ("厂商", 15),
    #                      ("网络区域", 15), ("购买日期", 15), ("过保日期", 15), ("设备状态", 15), ("备注", 20)]
    #         data_validate_table = [('BaseEquipmentType', ['name']), ('BaseDataCenter', ['name']),
    #                                ('BaseMachineRoom', ['name']),
    #                                ('BaseAssetStatus', ['status']), ('BaseNetArea', ['name']), ('BaseFactory', ['name'])
    #                                ]
    #
    #         data_validate_dict = self.__load_list_data(data_validate_table)
    #
    #         # 主sheet页
    #         sheet = self.xls_obj.create_sheet(u"equipment")
    #
    #         # 写title
    #         self.xls_obj.write_title(row_title, sheet)
    #         # 设备名称不能为空
    #         sheet.data_validation(1, 0, 65535, 0, {'validate': 'length',
    #                                                'criteria': '>=',
    #                                                'minimum': 1,
    #                                                'error_type': 'stop',
    #                                                'input_message': '必填项',
    #                                                'ignore_blank': False,
    #                                                'error_message': '设备名称不能为空'
    #                                                })
    #         # 设备分类
    #         sheet.data_validation(1, 2, 65535, 2, {'validate': 'list',
    #                                                'source': data_validate_dict["baseequipmenttype"],
    #                                                'input_message': '必填项'})
    #         # 数据中心
    #         sheet.data_validation(1, 3, 65535, 3, {'validate': 'list',
    #                                                'source': data_validate_dict["basedatacenter"],
    #                                                'input_message': '必填项'})
    #         # 机房
    #         sheet.data_validation(1, 4, 65535, 4, {'validate': 'list',
    #                                                'source': data_validate_dict["basemachineroom"],
    #                                                'input_message': '必填项'})
    #         # 管理IP不可重复
    #         sheet.data_validation(1, 6, 65535, 6, {'validate': 'custom',
    #                                                'value': '=COUNTIF($1:$65535,G2)=1',
    #                                                'input_message': 'IP唯一不可重复',
    #                                                })
    #         # U位 型号均必填
    #         sheet.data_validation(1, 7, 65535, 7, {'validate': 'length',
    #                                                'criteria': '>=',
    #                                                'minimum': 1,
    #                                                'error_type': 'stop',
    #                                                'ignore_blank': False,
    #                                                'input_message': '必填项',
    #                                                'error_message': 'U位不能为空'
    #                                                })
    #         sheet.data_validation(1, 8, 65535, 8, {'validate': 'length',
    #                                                'criteria': '>=',
    #                                                'minimum': 1,
    #                                                'error_type': 'stop',
    #                                                'ignore_blank': False,
    #                                                'input_message': '必填项',
    #                                                'error_message': '型号不能为空'
    #                                                })
    #         # 生产厂商
    #         sheet.data_validation(1, 11, 65535, 11, {'validate': 'list',
    #                                                  'source': data_validate_dict["basefactory"]})
    #         # 网络区域
    #         sheet.data_validation(1, 12, 65535, 12, {'validate': 'list',
    #                                                  'source': data_validate_dict["basenetarea"],
    #                                                  'input_message': '必填项'})
    #         # 设备状态
    #         sheet.data_validation(1, 15, 65535, 15, {'validate': 'list',
    #                                                  'source': data_validate_dict["baseassetstatus"]})
    #
    #     except Exception as e:
    #         print(e)

    def __host_template(self):
        """
        主机模板
        :return:
        """
        try:
            row_title = [("序号", 8), ("主机名(*)", 15), ("主机类型", 15), ("宿主机", 25), ("型号", 15), ("分区", 10),
                         ("CPU(数)", 8), ("内存(GB)", 8), ("网络区域", 10), ("F5策略", 10), ("购买日期", 10), ("过保日期", 10),
                         ("运行状态", 10), ("所属业务线", 25), ("IP地址", 15), ("网关地址", 15), ("IP类型", 10), ("域名", 20),
                         ("VLAN编号", 10), ("IP备注", 20), ("安装软件", 20), ("联系人", 15), ("联系人角色", 10)]
            data_validate_table = [('BaseAssetType', ['name']), ('Assets', ['model', 'sn']),
                                   ('BaseNetArea', ['name']), ('BaseBalanceType', ['typename']),
                                   ('BaseRunningStatus', ['status']), ('Business', ['project__sysname', 'bussname']),
                                   ('BaseSoft', ['type__name', 'name', 'version']), ('Staffs', ['name']),
                                   ('BaseRole', ['role_name'])]

            data_validate_dict = self.__load_list_data(data_validate_table)
            # 生成excel文件对象
            sheet = self.xls_obj.create_sheet(u"server")
            # 生成一个基表数据sheet页保存一些比较大的基表数据
            base_sheet = self.xls_obj.create_sheet(u"basedata")
            base_sheet.hide()

            # 写基表数据到另一个sheet页保留
            basesoft_list = data_validate_dict.get('basesoft')  # 软件信息
            business_list = data_validate_dict.get('business')  # 业务信息
            ownserver_list = data_validate_dict.get('assets')  # 宿主机
            for i in range(0, len(basesoft_list)):
                base_sheet.write(i, 0, basesoft_list[i])
            for i in range(0, len(business_list)):
                base_sheet.write(i, 1, business_list[i])
            for i in range(0, len(ownserver_list)):
                base_sheet.write(i, 2, ownserver_list[i])

            # 写title
            self.xls_obj.write_title(row_title, sheet)
            # 主机名不能为空
            sheet.data_validation(1, 1, 65535, 1, {'validate': 'length',
                                                   'criteria': '>=',
                                                   'minimum': 1,
                                                   'error_type': 'stop',
                                                   'ignore_blank': False,
                                                   'input_message': '必填项',
                                                   'error_message': '主机名不能为空'
                                                   })
            # 主机类型
            sheet.data_validation(1, 2, 65535, 2, {'validate': 'list',
                                                   'source': data_validate_dict.get('baseassettype')})
            # 宿主机
            sheet.data_validation(1, 3, 65535, 3, {'validate': 'list',
                                                   'source': '=basedata!$C$1:$C${0}'.format(len(ownserver_list))})
            # 网络区域
            sheet.data_validation(1, 8, 65535, 8, {'validate': 'list',
                                                   'source': data_validate_dict.get('basenetarea')})
            # F5策略
            sheet.data_validation(1, 9, 65535, 9, {'validate': 'list',
                                                   'source': data_validate_dict.get('basebalancetype')})
            # 运行状态
            sheet.data_validation(1, 12, 65535, 12, {'validate': 'list',
                                                     'source': data_validate_dict.get('baserunningstatus')})
            # 所属业务线
            sheet.data_validation(1, 13, 65535, 13, {'validate': 'list',
                                                     'source': '=basedata!$B$1:$B${0}'.format(len(business_list))})
            # IP地址不能重复
            sheet.data_validation(1, 14, 65535, 14, {'validate': 'custom',
                                                     'value': '=COUNTIF($1:$65535,O2)=1',
                                                     'input_message': 'IP唯一不可重复',
                                                     })
            # IP类型
            sheet.data_validation(1, 16, 65535, 16, {'validate': 'list', 'source': ['物理IP', '服务IP']})
            # 安装软件
            sheet.data_validation(1, 20, 65535, 20, {'validate': 'list',
                                                     'source': '=basedata!$A$1:$A${0}'.format(len(basesoft_list))})
            # 联系人
            sheet.data_validation(1, 21, 65535, 21, {'validate': 'list',
                                                     'source': data_validate_dict.get('staffs')})
            # 角色
            sheet.data_validation(1, 22, 65535, 22, {'validate': 'list',
                                                     'source': data_validate_dict.get('baserole')
                                                     })

        except Exception as e:
            print(e)

    def __host_storage_template(self):
        """
        主机的存储模板
        :return:
        """
        pass

    def __base_template(self):
        """
        基表数据模板
        :return:
        """
        pass

    @property
    def __example_template(self):
        """
        样例模板文件
        :return:
        """
        self.filename = "example_{0}.xlsx".format(self.template_type)
        self.tmp_file = os.path.join(self.tmp_path, self.filename)
        if os.path.isfile(self.tmp_file):
            with open(self.tmp_file, 'rb') as f:
                file = f.read()
        else:
            file = None
        return file


class ImportData(object):
    """
    导入数据模块
    构造方法参数:
    file_name: 上传到tmp文件下的要导入的文件的文件名
    cust_id: 客户编号
    """

    def __init__(self, **kwargs):
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exceltemplate")
        self.template_name = ""  # 验证文件时用
        self.file_name = ""
        self.cust_id = 0
        self.user = ""
        self.avaible = self.__parse_args(**kwargs)

    def __parse_args(self, **kwargs):
        """
        解析参数,对提交的数据进行参数分析,检查是否合法,如果不合法则返回False
        :param kwargs:
        :return:
        """
        template_name = kwargs.get("template_name")
        self.cust_id = kwargs.get("cust_id")
        self.file_name = os.path.join(self.file_path, kwargs.get("file_name"))
        if not os.path.isfile(self.file_name):
            return False
        if not template_name:
            return False

        self.template_name = template_name
        return True

    @property
    def file_titles(self):
        """
        获取文件的title字段,返回一个字符串
        :return: 返回一个字符串
        """
        with xlrd.open_workbook(self.file_name) as xls:
            sheet_book = xls.sheet_by_index(0)
            title_row = sheet_book.row_values(0)
        return "".join(title_row)

    def file_verification(self):
        """
        验证要导入的文件和模板类型是否一致,
        :return:
        """
        return True

    def read_xls_data(self, sheet_name=None):
        """
        读取上传的excel文件内容,保存在列表中
        :param sheet_name: 要读取的excel文件的sheet名,默认为模板名,对于server包含多个模板的需要指定sheet名
        :return:
        """
        data = list()
        data_sheet_name = self.template_name if not sheet_name else sheet_name
        try:
            with xlrd.open_workbook(self.file_name) as xls:
                # sheet_book = xls.sheet_by_index(0)
                sheet_book = xls.sheet_by_name(data_sheet_name)
                for row in range(1, sheet_book.nrows):
                    row_list = list()
                    for col in range(0, sheet_book.ncols):
                        if sheet_book.cell(row, col).ctype == 3:
                            # 如果是日期格式
                            py_data = xlrd.xldate.xldate_as_datetime(sheet_book.cell(row, col).value, xls.datemode)
                            row_list.append(datetime.strftime(py_data, "%Y-%m-%d"))
                            continue
                        if sheet_book.cell(row, col).ctype == 2:
                            # number类型
                            row_list.append(int(sheet_book.cell(row, col).value))
                            continue
                        row_list.append(sheet_book.cell(row, col).value)

                    data.append(row_list)
        except Exception as e:
            self.avaible = False
        return data
