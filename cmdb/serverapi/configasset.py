#!/usr/bin/env python
import json
import sys
from . import models
from .conf import collectmodule


class ConfigAsset(object):
    def __init__(self, request):
        self.request = self.__format_request_data(request)
        self.need_field = ['sn', 'asset_id', 'asset_type']
        self.sn = ""
        self.asset_id = -1
        self.asset_type = ""
        self.post_data = {}
        self.has_error = False
        self.error_msg = ""
        self.asset_obj = None
        self._anysis_para()

    def _anysis_para(self):
        """
        从传入的参数中获取必要的字段值
        :return:
        """
        for field in self.need_field:
            if field not in self.request:
                # 必须的字段在客户端提交的数据中没有，Error
                self.has_error = True
                self.error_msg = "Error:缺少必要参数,提交的数据必须包含[sn,asset_id,asset_type]"
                return self.has_error
        else:
            result = self.request
            self.post_data = result
            self.sn = result['sn']
            self.asset_id = result['asset_id']
            self.asset_type = result['asset_type']

    def insert_new_asset(self):
        """
        对没有资产id的请求，先在资产表中创建一个记录
        :return:
        """
        asset_id = self.__get_asset_id()
        if asset_id < 0:
            new_asset = {'sn': self.sn, 'asset_type': self.asset_type}
            other_key = {'name': 'new_' + self.asset_type}
            new_asset.update(other_key)
            models.Asset.objects.create(**new_asset)
        # 返回用户的id
        mod_asset = models.Asset.objects.filter(sn=self.sn).first()
        return mod_asset.id

    def __get_asset_id(self):
        """
        检查当前的资产ID是否存在，如果插入新资产Asset时该资产已经存在就返回ID,否则返回-1
        :return: -1 / id
        """
        asset_id = -1
        mod_asset = models.Asset.objects.filter(sn=self.sn).first()
        if mod_asset:
            asset_id = mod_asset.id
        return asset_id

    def __format_request_data(self, request_data):
        """
        test 查看收到的数据
        :return:
        """
        for k, v in request_data.items():
            result = json.loads(v[0])
            # for key, value in result.items():
            #     print("[ %s ]: %s" % (key, value))
            return result

    def accept_client_data(self):
        """
        对于客户端已经有资产ID的，提交过来的数据直接调用此方法进行操作
        :return:
        """
        # 获取资产对象
        if self.asset_id:
            self.asset_obj = models.Asset.objects.get(id=int(self.asset_id))
        else:
            self.asset_obj = models.Asset.objects.filter(sn=self.sn).first()

        # 从采集模块列表中获取信息，并执行相应模块
        # for module in collectmodule.CollectModule:
        #     module_name = 'insert_update_' + module
        #     print('begin exec function ', getattr(self, module_name))
        #
        #     if hasattr(self, module_name):
        #         print("**** find module ", module_name)
        #         module_obj = getattr(self, module_name)
        #         module_obj()
        #  执行各表操作
        self.__insert_update_server()
        self.__insert_update_cpu()
        self.__insert_update_ram()

    def __insert_update_server(self):
        """
        Server服务器表数据处理
        :return:
        """
        server_field = ['model', 'raid_type', 'os_type', 'os_distribution', 'os_release']
        # 判断是否存在当前asset_obj的对应server
        if hasattr(self.asset_obj, 'server'):
            # 已经存在Server记录，那就判断是否有更新字段信息,如果有就更新
            table_obj = getattr(self.asset_obj, 'server')
            self.__update_onetoone_table(table_obj, server_field, self.request)
            pass
        else:
            # 没有Server记录，新增一条记录
            self.__create_onetoone_record(models.Server, server_field)

    # def __create_server(self, column_list):
    #     """
    #     新增服务器Server信息
    #     :return:
    #     """
    #     tmp_dict = {}
    #     tmp_dict['asset_id'] = self.asset_obj.id
    #     for column in column_list:
    #         tmp_dict[column] = self.request.get(column)
    #     models.Server.objects.create(**tmp_dict)

    def __create_onetoone_record(self, table_obj, column_list):
        """
        创建资源数据表记录，该方法仅对于资产记录关联为OneToOne类型的记录，e.g: Server， CPU
        :param table_obj: 表对象
        :param column_list: 字段列表
        :return:
        """
        tmp_dict = {'asset_id': self.asset_obj.id}
        for column in column_list:
            tmp_dict[column] = self.request.get(column)
        table_obj.objects.create(**tmp_dict)

    def __insert_update_cpu(self):
        """
        CPU 信息数据处理
        :return:
        """
        cpu_field = ['cpu_core_count', 'cpu_count', 'cpu_model']
        if hasattr(self.asset_obj, 'cpu'):
            table_obj = getattr(self.asset_obj, 'cpu')
            self.__update_onetoone_table(table_obj, cpu_field, self.request)
        else:
            self.__create_onetoone_record(models.CPU, cpu_field)

    def __insert_update_ram(self):
        """
        RAM 数据信息更新或添加
        :return:
        """
        ram_field = ['sn', 'manufactory', 'model', 'capacity', 'slot']
        if getattr(self.asset_obj,'ram_set').select_related().count() > 0:
            # 有内存信息了，客户端发过来的数据与数据库对比可能有更换内存的、减少内存的、添加内存的,以下进行处理
            print('has ram')
            self.__update_foeignkey_table('ram', 'sn', self.request.get('ram'), ram_field)
        else:
            # 一条内存信息都没有,新添加所有内存信息
            print("no ram?? come here")
            self.__create_foreignkey_record(models.RAM, ram_field, 'ram')

    def __create_foreignkey_record(self, table_obj, column_list, data_key):
        """
        针对硬件资源数据表中的资产关联字段为 ForeignKey 类型的表添加新记录的公用模块
        :param table_obj: 表对象，此处的对象应该包含: DISK,NIC,RAM,
        :param column_list: 各表必须插入数据的字段列表
        :param data_key: 对应客户端提交过来的数据的key
        :return:
        """
        # 获取所有客户端提交过来的数据，结果为列表 e.g:
        # nic: [
        #     {'netmask': ['255.255.255.0', '64'], 'model': '[00000001] VMware Virtual Ethernet Adapter for VMnet1',
        #      'macaddress': '00:50:56:C0:00:01', 'ipaddress': '192.168.206.1', 'name': 1}，
        # {'netmask': ['255.255.254.0', '64'], 'model': '[00000002] Intel(R) Ethernet Connection I218-V',
        #  'macaddress': '68:F7:28:39:0B:8B', 'ipaddress': '10.34.32.105', 'name': 2},
        # {'netmask': ['255.255.255.0', '64'], 'model': '[00000003] VMware Virtual Ethernet Adapter for VMnet8',
        #  'macaddress': '00:50:56:C0:00:08', 'ipaddress': '192.168.2.1', 'name': 3},
        # {'netmask': '', 'model': '[00000004] Intel(R) Wireless-N 7260', 'macaddress': 'E8:B1:FC:C8:C0:53',
        #  'ipaddress': '', 'name': 4},
        # {'netmask': '','model': '[00000005] Microsoft Wi-Fi Direct Virtual Adapter', 'macaddress': 'E8:B1:FC:C8:C0:54'
        #  'ipaddress': '', 'name': 5},
        # {'netmask': '', 'model': '[00000006] Microsoft Hosted Network Virtual Adapter',
        #  'macaddress': 'EA:B1:FC:C8:C0:53', 'ipaddress': '', 'name': 6},
        # {'netmask': '', 'model': '[00000012] Bluetooth Device (Personal Area Network)',
        #  'macaddress': 'E8:B1:FC:C8:C0:57', 'ipaddress': '', 'name': 12}
        # ]
        request_data_list = self.request[data_key]
        for data in request_data_list:
            tmpdict = {'asset_id': self.asset_obj.id}
            for column in column_list:
                tmpdict[column] = data[column]
            table_obj.objects.create(**tmpdict)

    def __update_onetoone_table(self, db_table_obj, db_column_list, request_data):
        """
        当不是新添加数据时，检查提交的数据是否有更新的数据记录,只正对 Asset资产关联关系为OneToOne的
        :param db_table_obj:  要检查的数据表对象 e.g: Server, Disk
        :param db_column_list: 要检查的数据表字段列表
        :param request_data: 提交的数据
        :return:
        """
        for field in db_column_list:
            column_value_in_db = getattr(db_table_obj, field)
            column_value_for_response = request_data.get(field)
            # 由于提交的数据的值为str类型，而数据库中可能为 int 型 ，需要进行转换后判断
            if type(column_value_in_db) is int:
                column_value_for_response = int(column_value_for_response)
            if type(column_value_in_db) is float:
                column_value_for_response = float(column_value_for_response)
            if not column_value_for_response == column_value_in_db:
                # 数据库中的值和发送过来的数据不一致，修改字段的值
                db_column_obj = db_table_obj._meta.get_field(field)  # 获得字段对象
                db_column_obj.save_form_data(db_table_obj, column_value_for_response)  # 更新字段数据
                db_table_obj.save()  # 保存

    def __update_foeignkey_table(self, db_table_name, key, request_data_list, compare_column):
        """
        对关联资产Asset为Foreignkey的表，做更新处理，可能删除、添加或修改
        :param db_table_name: str类型，数据表name e.g: ram,nic,disk,
        :param key: 比较的关键字，用来提取db中的对象字段
        :param request_data_list: 客户端发送过来的所有数据列表，内容为字典
        :param compare_column: 判断是否有变化时比较的字段
        :return:
        """
        compare_key_in_db = []
        compare_key_in_client = []
        # 获取资产关联的数据库中的记录数,取出比较的key, 放入列表中
        db_record_obj_list = getattr(self.asset_obj, db_table_name + '_set').select_related()
        for record_obj in db_record_obj_list:
            # 获取单个记录的比较key的值
            compare_key_in_db.append(getattr(record_obj, key))

        # 获取客户端发送过来的数据中的记录，获取比较的key
        for record in request_data_list:
            compare_key_in_client.append(record.get(key))

        # 两个集合进行比较
        # 如果两个列表的数一样且元素都一样，则完全相同不做处理
        # 如果db中有client没有 表示资源已经移除，需要数据库中删除
        print('db table name:', db_table_name)
        print('key in db ', compare_key_in_db)
        print('key in client data', compare_key_in_client)
        # -- 比较db与client的差集,得到key的值的集合
        compare_difference_in_db = set(compare_key_in_db).difference(set(compare_key_in_client))
        if len(compare_difference_in_db) > 0:
            # -- db中有 但 客户端没有的数据key(字段)值
            for db_record_obj in db_record_obj_list:
                # -- 查找数据库中每条记录key字段的值是否与差集值相同，相同的这条记录就要删除
                if getattr(db_record_obj, key) in compare_difference_in_db:
                    db_record_obj.delete()

        # 如果client中有而db中没有表示新增加的，在数据库中添加
        compare_difference_in_client = set(compare_key_in_client).difference(set(compare_key_in_db))
        if len(compare_difference_in_client) > 0:
            for key_value in compare_difference_in_client:
                # 从比较的差集中将客户端提交的对应的这条的记录找出来，写入数据
                for record in request_data_list:
                    if key_value == record.get(key):
                        record['asset_id'] = self.asset_obj.id
                        db_record_obj_list.update_or_create(**record)

        # 如果两个都有的，比较其他的数据是否有变更，有则在数据库中修改记录
        # --取交集
        compare_intersetion = set(compare_key_in_db).intersection(set(compare_key_in_client))
        for compare_key_value in compare_intersetion:
            for db_record_obj in db_record_obj_list:
                column_value_changed = False
                if getattr(db_record_obj, key) == compare_key_value:  # 找到db记录对象
                    for column in compare_column:
                        record_dict = self.__value_in_data(key, compare_key_value, column, request_data_list)
                        if not getattr(db_record_obj, column) == record_dict.get(column, ""):
                            # 表示有变化
                            column_value_changed = True
                            break

                    if column_value_changed:
                        record_dict['asset_id'] = self.asset_obj.id
                        for column in compare_column:
                            column_obj = db_record_obj._meta.get_field(column)
                            column_obj.save_form_data(db_record_obj,record_dict.get(column))
                            db_record_obj.save()





    def __value_in_data(self,search_key,key_value,column,request_data):
        """
        从客户端发送过来的数据中的某一个信息中获取要查找的column名对应的值，
        通过在记录中(比如所有内存数据）根据search_key(sn),获取对应的值,与(key_value)匹配，一致表示要数据为要查找的一条记录
        在该记录中获取到 key=column的value，返回
        :param search_key: 查找的key
        :param key_value: 对比的值
        :param column: 与数据库进行对比的列对应的key
        :param request_data: 查找的数据列表
        :return: 返回找到的客户端发送过来的对应的那条记录
        """
        try:
            for record in request_data:
                compare_value = record.get(search_key)
                if compare_value == key_value:  # 找到记录
                    return record
                else:
                    continue
            else:
                return {}
        except Exception as e:
            return {}