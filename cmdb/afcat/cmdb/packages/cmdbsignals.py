#!/usr/bin/env python
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from django.db.models.signals import post_save, pre_save, ModelSignal, post_delete
from django.dispatch import receiver

from afcat.api.libs.public import Logger
from afcat.cmdb import models
from afcat.cmdb.libs import common

logger = Logger(__name__)

# 自定义审计操作信号,需要传入action=(new/delete/restore/backup)
operate_audit = ModelSignal(providing_args=["instance", "using", "user"], use_caching=True)
check_signal = ModelSignal(providing_args=["instance", "using"], use_caching=True)


@receiver(pre_save, sender=models.BaseCustomerInfo)
def auto_create_idcode(sender, instance, **kwargs):
    """
    在新生成一个客户信息之前，将客户的唯一编号idcode自动增加,在现有表中增加1
    :param sender: BaseCustomerInfo 对象
    :param instance: 当前操作的实例
    :param kwargs:
    :return:
    """
    try:
        # 获取IDS表中最后的记录客户id, 初始从1001开始
        try:
            sql = "select id,max(substr(nextid,1,4)) curr_max_custid from cmdb.cmdb_ids"
            curr_idcode = models.IDS.objects.raw(sql)[0]
            new_idcode = int(curr_idcode.curr_max_custid) + 1
        except ObjectDoesNotExist:
            new_idcode = 1001
        instance.idcode = new_idcode

    except Exception as e:
        logger.error(e)
    return instance


@receiver(post_save, sender=models.BaseCustomerInfo)
def init_ids_tables(sender, instance, **kwargs):
    """
    新创建一个客户,则在IDS资源表中初始化所有表的ID
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    try:
        ids_obj_list = list()
        if kwargs.get("created"):
            custid = instance.idcode
            startid = int("{0}{1}".format(custid, '1'))
            # 是否已经存在改客户的ids记录,有就不操作了
            check_result = models.IDS.objects.filter(nextid__startswith=custid).count()
            if check_result == 0:
                cursor = connections["cmdb"].cursor()
                # 初始化IDS表
                cursor.execute("SELECT app_label, model FROM django_content_type "
                               "WHERE app_label in('account','cmdb') "
                               "and model not in ('account')")
                for rec in cursor.fetchall():
                    app_label, model = rec
                    ids_obj_list.append(models.IDS(tablename="{0}_{1}".format(app_label, model), nextid=startid))
                    # models.IDS.objects.create(tablename="{0}_{1}".format(app_label, model), nextid=startid)
                models.IDS.objects.bulk_create(ids_obj_list)
                # 插入基表数据
                init_basedata(custid)
    except Exception as e:
        logger.error(e)


@receiver(operate_audit, sender=models.BaseCustomerInfo)
@receiver(operate_audit, sender=models.BackupRecord)
def operate_audit_signal(sender, instance, **kwargs):
    """
    删除客户时记录到操作日志,基表的删除日志, 暂只针对客户信息做了审计、删除备份集
    在cmdb_api中删除记录时发送此信号
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    try:
        models.OperateAudit.audit.log_action(operater=kwargs["user"].username,
                                             action=kwargs.get("action", "delete"),
                                             cust=kwargs.get("custid"),
                                             model_name=instance._meta.verbose_name,
                                             operate_data=instance.__str__(), object_pk=instance.id)
    except Exception as e:
        logger.error(e)
        # pass


@receiver(operate_audit, sender=models.IPManage)
def allocate_ip_audit(sender, instance, **kwargs):
    """
    单独正对IP地址分配的审计,由于分配是地址段,批量添加bulk_create()无法调用信号。
    审计是记录一个分配信息就可以了
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    try:
        audit_info = dict(operater=kwargs["user"].username,
                          action=kwargs.get("action", "delete"),
                          model_name=instance._meta.verbose_name,
                          operate_data=kwargs.get("data"),
                          cust=kwargs.get("cust_id"),
                          object_pk=None)
        models.OperateAudit.audit.log_action(**audit_info)
        print("allocate ip .....", audit_info)
    except Exception as e:
        logger.error(e)


@receiver(check_signal, sender=models.IPConfiguration)
def check_ip_exists(sender, instance, **kwargs):
    """
    主机添加IP地址时判断IP是否重复,在Server中的关联表数据操作时发送信号
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    flag = True
    err = ""
    old_ip = ""
    try:
        obj_ips = models.IPConfiguration.objects.filter(id=instance.get("id")).values("ipaddress")
        if obj_ips.count() > 0:
            print(obj_ips)
            old_ip = obj_ips[0].get("ipaddress")

        if old_ip != instance.get("ipaddress"):
            # ip一样表示没有修改IP，不用判断
            ip_queryset = models.IPConfiguration.objects.filter(id__startswith=str(instance.get("id"))[:4],
                                                                ipaddress=instance.get("ipaddress")).exclude(
                id=instance.get("id"))
            if ip_queryset.count() > 0:
                flag = False
                err = "IP地址重复"
            elif not common.ip_allocated(instance.get("ipaddress", ""), str(instance.get("id"))[:4]):
                flag = False
                err = "IP地址未分配或已使用"
    except Exception as e:
        logger.error(e)
    return {"status": flag, "err": err}


@receiver(post_save, sender=models.IPConfiguration)
def update_ip_status(sender, instance, **kwargs):
    """
    对于主机附属表记录中的IPConfiguration表在进行添加和编辑时,修改IPManage表的状态信息
    :param sender: 信号发送对象，这里只时接收IPConfiguration对象信号
    :param instance: 对象实例
    :param kwargs: 发送的数据字典
    :return:
    """
    try:
        custid = str(instance.id)[:4]
        if kwargs.get("created"):  # new
            ipaddr = instance.ipaddress
            common.change_ip_status(custid, ipaddr, "USED", instance.__str__())

        if kwargs.get("update"):
            old_ip = instance.ipaddress
            ipaddr = kwargs.get("ipaddress")
            if old_ip != ipaddr:
                common.change_ip_status(custid, old_ip, "ALLOCATED")
                common.change_ip_status(custid, ipaddr, "USED", instance.__str__())
    except Exception as e:
        logger.error(e)


@receiver(post_delete, sender=models.IPConfiguration)
def on_dele(sender, instance, **kwargs):
    """
    删除主机的IP配置时,修改IP的状态
    :param sender: IPConfiguration
    :param instance:
    :param kwargs:
    :return:
    """
    try:
        custid = str(instance.id)[:4]
        common.change_ip_status(custid, instance.ipaddress, "RECOVER")
    except Exception as e:
        logger.error(e)


def init_basedata(custid):
    """
    初始化基表数据
    :param custid: 客户ID
    :return:
    """
    # from afcat.cmdb import models as cmdb_models

    init_data = [
        {"model": "BaseRole",
         "data": [{"id": int("{0}1".format(custid)), "role_name": "运维人员"},
                  {"id": int("{0}2".format(custid)), "role_name": "开发人员"},
                  {"id": int("{0}3".format(custid)), "role_name": "项目经理"},
                  {"id": int("{0}4".format(custid)), "role_name": "行方负责人"}]},
        {"model": "BaseSoftType",
         "data": [{"id": int("{0}1".format(custid)), "name": "操作系统"},
                  {"id": int("{0}2".format(custid)), "name": "数据库软件"},
                  {"id": int("{0}3".format(custid)), "name": "中间件软件"},
                  {"id": int("{0}4".format(custid)), "name": "应用软件"}]},
        {"model": "BaseSoft",
         "data": [
             {"id": int("{0}1".format(custid)), "name": "AIX", "version": "7.1", "type_id": int("{0}1".format(custid))},
             {"id": int("{0}2".format(custid)), "name": "AIX", "version": "6.1", "type_id": int("{0}1".format(custid))},
             {"id": int("{0}3".format(custid)), "name": "AIX", "version": "5.3", "type_id": int("{0}1".format(custid))},
             {"id": int("{0}4".format(custid)), "name": "HPUX", "version": "11.23",
              "type_id": int("{0}1".format(custid))},
             {"id": int("{0}5".format(custid)), "name": "HPUX", "version": "11.11",
              "type_id": int("{0}1".format(custid))},
             {"id": int("{0}6".format(custid)), "name": "RHEL", "version": "7.0",
              "type_id": int("{0}1".format(custid))},
             {"id": int("{0}7".format(custid)), "name": "RHEL", "version": "6.5",
              "type_id": int("{0}1".format(custid))},
             {"id": int("{0}8".format(custid)), "name": "RHEL", "version": "6.4",
              "type_id": int("{0}1".format(custid))},
             {"id": int("{0}9".format(custid)), "name": "Solaris", "version": "10.9",
              "type_id": int("{0}1".format(custid))},
             {"id": int("{0}10".format(custid)), "name": "Solaris", "version": "11.2",
              "type_id": int("{0}1".format(custid))},
             {"id": int("{0}11".format(custid)), "name": "CentOS", "version": "7.0",
              "type_id": int("{0}1".format(custid))},
             {"id": int("{0}12".format(custid)), "name": "SUSE", "version": "11 SP3",
              "type_id": int("{0}1".format(custid))},
             {"id": int("{0}13".format(custid)), "name": "ORACLE", "version": "10.2.0.4",
              "type_id": int("{0}2".format(custid))},
             {"id": int("{0}14".format(custid)), "name": "ORACLE", "version": "11.2.0.1",
              "type_id": int("{0}2".format(custid))},
             {"id": int("{0}15".format(custid)), "name": "ORACLE", "version": "12.1.0.3",
              "type_id": int("{0}2".format(custid))},
             {"id": int("{0}16".format(custid)), "name": "WAS", "version": "ND 7.1",
              "type_id": int("{0}3".format(custid))},
             {"id": int("{0}17".format(custid)), "name": "WAS", "version": "7.0.0.25",
              "type_id": int("{0}3".format(custid))},
             {"id": int("{0}18".format(custid)), "name": "IHS", "version": "7", "type_id": int("{0}3".format(custid))}
         ]},
        {"model": "BaseAssetType",
         "data": [
             {"id": int("{0}1".format(custid)), "name": u"小型机", "flag": 0},
             {"id": int("{0}2".format(custid)), "name": u"PC服务器", "flag": 0},
             {"id": int("{0}3".format(custid)), "name": u"存储设备", "flag": 0},
             {"id": int("{0}4".format(custid)), "name": u"刀箱服务器", "flag": 0},
             {"id": int("{0}5".format(custid)), "name": u"刀片服务器", "flag": 0},
             {"id": int("{0}6".format(custid)), "name": u"工控机", "flag": 0},
             {"id": int("{0}7".format(custid)), "name": u"LPAR分区", "flag": 1},
             {"id": int("{0}8".format(custid)), "name": u"虚拟主机", "flag": 1}
         ]},
        {"model": "BaseAssetSubtype",
         "data": [
             {"id": int("{0}1".format(custid)), "name": u"IBM P780", "type_id": int("{0}1".format(custid))},
             {"id": int("{0}2".format(custid)), "name": u"IBM P750", "type_id": int("{0}1".format(custid))},
             {"id": int("{0}3".format(custid)), "name": u"PC机", "type_id": int("{0}2".format(custid))},
             {"id": int("{0}4".format(custid)), "name": u"EMC存储", "type_id": int("{0}3".format(custid))},
             {"id": int("{0}5".format(custid)), "name": u"HMC", "type_id": int("{0}6".format(custid))},
             {"id": int("{0}6".format(custid)), "name": u"PureFlex", "type_id": int("{0}5".format(custid))},
         ]},
        {"model": "BaseFactory",
         "data": [
             {"id": int("{0}1".format(custid)), "name": u"IBM"},
             {"id": int("{0}2".format(custid)), "name": u"F5"},
             {"id": int("{0}3".format(custid)), "name": u"EMC"},
             {"id": int("{0}4".format(custid)), "name": u"惠普(HP)"},
             {"id": int("{0}5".format(custid)), "name": u"戴尔(DELL)"},
             {"id": int("{0}6".format(custid)), "name": u"思科(CISCO)"},
             {"id": int("{0}7".format(custid)), "name": u"联想(LENOVO)"},
             {"id": int("{0}8".format(custid)), "name": u"华三(H3C)"},
             {"id": int("{0}9".format(custid)), "name": u"华为(HUAWEI)"},
             {"id": int("{0}10".format(custid)), "name": u"飞塔(FORTINET)"},
             {"id": int("{0}11".format(custid)), "name": u"山石(HILLSTONE)"},

         ]},
        {"model": "BaseNetArea",
         "data": [
             {"id": int("{0}1".format(custid)), "name": u"生产后台"},
             {"id": int("{0}2".format(custid)), "name": u"办公后台"},
             {"id": int("{0}3".format(custid)), "name": u"互联网隔离区"},
             {"id": int("{0}4".format(custid)), "name": u"管理区"},
             {"id": int("{0}5".format(custid)), "name": u"互联网后台"},
             {"id": int("{0}6".format(custid)), "name": u"外联隔离"},
             {"id": int("{0}7".format(custid)), "name": u"电话银行"}
         ]},
        {"model": "BaseAssetStatus",
         "data": [
             {"id": int("{0}1".format(custid)), "status": u"销毁", "flag": 1},
             {"id": int("{0}2".format(custid)), "status": u"闲置", "flag": 0},
             {"id": int("{0}3".format(custid)), "status": u"维护", "flag": 0},
             {"id": int("{0}4".format(custid)), "status": u"使用", "flag": 0},
         ]},
        {"model": "BaseRunningStatus",
         "data": [
             {"id": int("{0}1".format(custid)), "status": u"使用"},
             {"id": int("{0}2".format(custid)), "status": u"关闭"},
             {"id": int("{0}3".format(custid)), "status": u"销毁"},
             {"id": int("{0}4".format(custid)), "status": u"未使用"},
         ]},
        {"model": "BaseBalanceType",
         "data": [
             {"id": int("{0}1".format(custid)), "typename": u"负载"},
             {"id": int("{0}2".format(custid)), "typename": u"NAT"},
             {"id": int("{0}3".format(custid)), "typename": u"优先级"},
             {"id": int("{0}4".format(custid)), "typename": u"无调用关系"},
             {"id": int("{0}5".format(custid)), "typename": u"不过"}
         ]},
        {"model": "BaseRaidType",
         "data": [
             {"id": int("{0}1".format(custid)), "typename": u"RAID0"},
             {"id": int("{0}2".format(custid)), "typename": u"RAID1"},
             {"id": int("{0}3".format(custid)), "typename": u"RAID2"},
             {"id": int("{0}4".format(custid)), "typename": u"RAID3"},
             {"id": int("{0}5".format(custid)), "typename": u"RAID4"},
             {"id": int("{0}6".format(custid)), "typename": u"RAID5"},
             {"id": int("{0}7".format(custid)), "typename": u"RAID6"},
             {"id": int("{0}8".format(custid)), "typename": u"RAID7"},
             {"id": int("{0}9".format(custid)), "typename": u"RAID0+1"},
         ]},
        {"model": "BaseEquipmentType",
         "data": [
             {"id": int("{0}1".format(custid)), "name": u"交换机"},
             {"id": int("{0}2".format(custid)), "name": u"路由器"},
             {"id": int("{0}3".format(custid)), "name": u"防火墙"},
             {"id": int("{0}4".format(custid)), "name": u"加密机"},
             {"id": int("{0}5".format(custid)), "name": u"负载设备"}
         ]}
    ]
    try:
        # 开始初始化基础表
        for init_item in init_data:
            models_list = list()
            exec_models = getattr(models, init_item.get("model"))
            for data in init_item.get("data"):
                models_list.append(exec_models(**data))
            # exec_models.objects.create(**data)
            exec_models.objects.bulk_create(models_list)

        # 执行完成后重新更新ids表中基表的nextid值
        table_name_list = dict()
        # 获取当前要添加的基表的记录数{"cmdb_baserole":4, ...}
        for obj in init_data:
            table_name_list.update(
                {"{0}_{1}".format(getattr(models, obj.get("model"))._meta.app_label,
                                  obj.get("model").lower()): len(obj.get("data"))})

        # 获取当前IDS表中当前custid客户的要更新的数据记录
        update_record = models.IDS.objects.filter(nextid__startswith=custid, tablename__in=table_name_list.keys())
        for rec in update_record:
            rec_count = table_name_list.get(rec.tablename)
            new_id = str(int(rec_count) + 1)
            rec.nextid = int("{0}{1}".format(custid, new_id))
            rec.save()
    except Exception as e:
        logger.error(e)
