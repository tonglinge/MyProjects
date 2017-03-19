from django.db import models

from afcat.cmdb.packages import cmdbmanger
from afcat.cmdb.settings import APP_NAME


# Create your models here.

class BaseCustomerInfo(models.Model):
    """
    客户信息基表
    """
    id = models.BigIntegerField(primary_key=True)
    idcode = models.IntegerField(unique=True, verbose_name=u"唯一序号")
    custalias = models.CharField(max_length=100, verbose_name=u"客户简称")
    custname = models.CharField(max_length=200, verbose_name=u"客户名称")
    custCode = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"客户编号")

    def __str__(self):
        return "{0}:{1}".format(self.idcode, self.custalias)

    @staticmethod
    def is_public():
        """
        定义该model是公共model,不用区分客户,仅判断用不做任何处理
        :return:
        """
        return True

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_basecustomerinfo", "can view BaseCustomerInfo"),
        )
        verbose_name = u"客户信息表"
        verbose_name_plural = u"客户信息表"
        ordering = ["-idcode"]


class IDS(models.Model):
    """
    所有表的id值的库
    """
    tablename = models.CharField(max_length=100)
    nextid = models.BigIntegerField()

    class Meta:
        app_label = APP_NAME
        # unique_together = ["tablename", "nextid"]
        permissions = (
            ("view_ids", "can view ids"),
        )


class BaseCompany(models.Model):
    """
    公司名称表
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=u"公司名称")

    def __str__(self):
        return self.name

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_basecompany", "can view BaseCompany"),
        )
        verbose_name_plural = u"公司基表"
        verbose_name = u"公司基表"
        ordering = ["-name"]


class BaseDepartment(models.Model):
    """
    基表-部门表
    """
    id = models.BigIntegerField(primary_key=True)
    company = models.ForeignKey("BaseCompany", related_name='my_department', verbose_name=u"公司名称")
    name = models.CharField(max_length=100)
    up_department = models.ForeignKey('self', blank=True, null=True, related_name='updepart')
    top_department = models.ForeignKey('self', blank=True, null=True, related_name='topdepart')

    def __str__(self):
        return "{0}-{1}".format(self.company, self.name)

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_basedepartment", "can view BaseDepartment"),
        )
        verbose_name_plural = u"部门基表"
        verbose_name = u"部门基表"
        ordering = ["-id"]


class BaseRole(models.Model):
    """
    基表-人员角色表
    """
    id = models.BigIntegerField(primary_key=True)
    role_name = models.CharField(max_length=100, verbose_name=u"角色名称")

    def __str__(self):
        return self.role_name

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_baserole", "can view BaseRole"),
        )
        verbose_name_plural = u"角色表"
        verbose_name = u"角色表"
        ordering = ["-role_name"]


class BaseSoftType(models.Model):
    """
    基表-软件分类表 e.g: 操作系统,数据库,中间件..
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=u"软件类型")

    def __str__(self):
        return self.name

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_basesofttype", "can view BaseSoftType"),
        )
        verbose_name_plural = u"软件分类"
        verbose_name = u"软件分类"
        ordering = ["name", "-id"]


class BaseSoft(models.Model):
    """
    软件列表
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=u"软件名称")
    type = models.ForeignKey("BaseSoftType", related_name="softlist", verbose_name=u"软件类型")
    version = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"软件版本")

    def __str__(self):
        return "{0}:{1}".format(self.name, self.version)

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_basesoft", "can view BaseSoft"),
        )
        verbose_name_plural = u"软件列表"
        verbose_name = u"软件列表"
        ordering = ["name", "type", "version"]


class SoftLisence(models.Model):
    """
    软件序列号
    """
    id = models.BigIntegerField(primary_key=True)
    soft = models.ForeignKey('BaseSoft', related_name='softlisence', verbose_name=u"软件名称")
    lisence = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"Lisene号")
    tradedate = models.DateField(null=True, blank=True, verbose_name=u"购买日期")
    expiredate = models.DateField(null=True, blank=True, verbose_name=u"过期日期")
    remark = models.CharField(max_length=300, null=True, blank=True, verbose_name=u"备注")

    def __str__(self):
        return "{0}:{1}".format(self.soft.name, self.lisence)

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_softlisence", "can view SoftLisence"),
        )
        verbose_name_plural = u"软件Lisence"
        verbose_name = u"软件Lisence"
        ordering = ["soft", "tradedate"]


class BaseAssetType(models.Model):
    """
    资产分类 e.g:物理机、虚拟机、网络设备、办公设备
    """
    flag_choice = (
        (1, u"是"), (0, u"否")
    )
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=u"类型名称")
    flag = models.IntegerField(choices=flag_choice, default=0, verbose_name=u"是否虚机类型")

    def __str__(self):
        return self.name

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_baseassettype", "can view BaseAssetType"),
        )
        verbose_name_plural = u"服务器用途"
        verbose_name = u"服务器用途"
        ordering = ["name", "flag"]


class BaseAssetSubtype(models.Model):
    """
    资产分类子类, e.g: 物理机:PCServer,小机,刀片
    """
    id = models.BigIntegerField(primary_key=True)
    type = models.ForeignKey('BaseAssetType', on_delete=models.CASCADE, verbose_name=u"所属分类")
    name = models.CharField(max_length=200, verbose_name=u"主机类型")

    def __str__(self):
        return "{0}:{1}".format(self.type.name, self.name)

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_baseassetsubtype", "can view BaseAssetSubtype"),
        )
        verbose_name_plural = u"服务器分类"
        verbose_name = u"服务器分类"
        ordering = ["-type", "name"]


class BaseFactory(models.Model):
    """
    资产、设备厂商,集成厂商
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name=u"厂商名称")
    contact = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"联系方式")

    def __str__(self):
        return self.name

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_basefactory", "can view BaseFactory"),
        )
        verbose_name_plural = u"设备厂商"
        verbose_name = u"设备厂商"
        ordering = ["name", "contact"]


class BaseDataCenter(models.Model):
    """
    数据中心
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=u"数据中心")

    def __str__(self):
        return self.name

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_basedatacenter", "can view BaseDataCenter"),
        )
        verbose_name_plural = u"数据中心"
        verbose_name = u"数据中心"
        ordering = ["name"]


class BaseMachineRoom(models.Model):
    """
    机房表
    """
    id = models.BigIntegerField(primary_key=True)
    center = models.ForeignKey('BaseDataCenter', related_name="related_rooms",
                               on_delete=models.SET_NULL, null=True, verbose_name=u"所属中心")
    name = models.CharField(max_length=100, verbose_name=u"机房名称")
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"机房地址")

    def __str__(self):
        return "{0}:{1}".format(self.center.name, self.name)

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_basemachineroom", "can view BaseMachineRoom"),
        )
        verbose_name_plural = u"机房"
        verbose_name = u"机房"
        ordering = ["center", "name", "address"]


class R_MachineRoom_Staff(models.Model):
    """
    机房联系人表
    """
    id = models.BigIntegerField(primary_key=True)
    room = models.ForeignKey('BaseMachineRoom', on_delete=models.CASCADE, related_name="related_staffs",
                             verbose_name=u"机房")
    staff = models.ForeignKey('Staffs', verbose_name=u"联系人")
    role = models.ForeignKey('BaseRole', verbose_name=u"角色")
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"备注")

    def __str__(self):
        return "{0}:{1}".format(self.staff.name, self.role.role_name)

    class Meta:
        app_label = APP_NAME


class BaseAssetCabinet(models.Model):
    """
    资产机柜表
    """
    id = models.BigIntegerField(primary_key=True)
    room = models.ForeignKey('BaseMachineRoom', on_delete=models.SET_NULL, null=True, verbose_name=u"所属机房")
    numbers = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"机柜号")
    slotcount = models.IntegerField(null=True, blank=True, verbose_name=u"槽位数(U)")

    def __str__(self):
        return self.numbers

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_baseassetcabinet", "can view BaseAssetCabinet"),
        )
        verbose_name_plural = u"机柜"
        verbose_name = u"机柜"
        ordering = ["room", "numbers", "slotcount"]


class BaseNetArea(models.Model):
    """
    资产网络分区:测试区,生产区,外联区...
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=u"网络区域名称")

    def __str__(self):
        return self.name

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_basenetarea", "can view BaseNetArea"),
        )
        verbose_name_plural = u"网络区域"
        verbose_name = u"网络区域"
        ordering = ["name", "-id"]


class BaseAssetStatus(models.Model):
    """
    资产状态
    """
    id = models.BigIntegerField(primary_key=True)
    status = models.CharField(max_length=100, verbose_name=u"状态")
    flag = models.IntegerField(default=0, verbose_name=u"销毁标识")

    def __str__(self):
        return self.status

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_baseassetstatus", "can view BaseAssetStatus"),
        )
        verbose_name_plural = u"设备状态"
        verbose_name = u"设备状态"
        ordering = ["status", "-id"]


class BaseRunningStatus(models.Model):
    """
    服务器运行状态
    """
    id = models.BigIntegerField(primary_key=True)
    status = models.CharField(max_length=100, verbose_name=u"运行状态")

    def __str__(self):
        return self.status

    class Meta:
        app_label = APP_NAME
        verbose_name = u"运行状态"
        verbose_name_plural = u"运行状态"
        permissions = (
            ("view baserunningstatus", "can view RunningStatus"),
        )
        ordering = ["-id"]


class BaseBalanceType(models.Model):
    """
    F5负载策略
    """
    id = models.BigIntegerField(primary_key=True)
    typename = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"F5策略")

    def __str__(self):
        return self.typename

    class Meta:
        app_label = APP_NAME
        verbose_name = u"F5负载策略"
        verbose_name_plural = u"F5负载策略"
        permissions = (
            ("view balancetype", "can view BalanceType"),
        )
        ordering = ["id"]


class IPDesign(models.Model):
    """
    IP地址规划表
    """
    id = models.BigIntegerField(primary_key=True)
    ipaddr = models.GenericIPAddressField(verbose_name=u"IP地址")
    maskbits = models.IntegerField(verbose_name=u"子网掩码位")
    parentip = models.ForeignKey('IPDesign', null=True, blank=True, related_name='submask', verbose_name=u"子网归属")
    counts = models.IntegerField(null=True, verbose_name=u"子网/IP数量")
    datacenter = models.ForeignKey('BaseDataCenter', null=True, verbose_name=u"数据中心")
    netarea = models.ForeignKey('BaseNetArea', null=True, blank=True, verbose_name=u"网络区域")
    vlan = models.TextField(max_length=100, null=True, blank=True, verbose_name=u"VLAN范围")
    usefor = models.TextField(max_length=100, null=True, blank=True, verbose_name=u"用途")
    cust = models.ForeignKey('BaseCustomerInfo', to_field='idcode', null=True, verbose_name=u"所属客户")
    createuser = models.TextField(max_length=100, null=True, blank=True, verbose_name=u"创建人")
    createdate = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name=u"创建日期")
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"备注")

    def __str__(self):
        return "{0}/{1}".format(self.ipaddr, str(self.maskbits))

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_ipdesign", "Can View IPDesign"),
        )
        verbose_name = u"IP地址规划"
        verbose_name_plural = u"IP地址规划"


class IPManage(models.Model):
    """
    IP分配表关联表
    """
    status_choices = (('1', '未分配'), ('2', '已分配'), ('3', '已使用'), ('4', '待回收'))
    id = models.BigIntegerField(primary_key=True)
    ipaddr = models.GenericIPAddressField(verbose_name=u"IP地址")
    ipmask = models.ForeignKey('IPDesign', related_name='allocated', verbose_name=u"IP地址段")
    status = models.TextField(max_length=5, choices=status_choices, verbose_name=u"IP状态")
    vlan = models.TextField(max_length=50, null=True, blank=True, verbose_name=u"VLAN编号")
    allocateuser = models.TextField(max_length=20, null=True, blank=True, verbose_name=u"分配人")
    allocatedate = models.DateField(auto_now_add=True, verbose_name=u"分配日期")
    allocateto = models.TextField(max_length=200, null=True, blank=True, verbose_name=u"分配系统或设备")
    binded = models.TextField(max_length=200, null=True, blank=True, verbose_name=u"绑定设备")
    cust = models.ForeignKey('BaseCustomerInfo', to_field='idcode', null=True, verbose_name=u"所属客户")
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"备注")

    def __str__(self):
        return "{0}:状态({1})".format(self.ipaddr, self.get_status_display())

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_ipallocation", "Can View IPAllocation"),
        )
        verbose_name = u"IP分配管理"
        verbose_name_plural = u"IP分配管理"


class BaseRaidType(models.Model):
    """
    RAID类型表
    """
    id = models.BigIntegerField(primary_key=True)
    typename = models.CharField(max_length=50, verbose_name=u"RAID类型")

    def __str__(self):
        return self.typename

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_baseraidtype", "can view BaseRaidType"),
        )
        verbose_name_plural = u"RAID类型"
        verbose_name = u"RAID类型"
        ordering = ["typename"]


class BaseEquipmentType(models.Model):
    """
    设备资产类型表
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"类型名称")

    def __str__(self):
        return self.name

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_baseequipmenttype", "Can View BaseEquipmentType"),
        )
        verbose_name_plural = u"网络设备类型"
        verbose_name = u"网络设备类型"
        ordering = ["name"]


class Staffs(models.Model):
    """
    人员信息表
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=u"姓名")
    alias = models.CharField(max_length=50, verbose_name=u"简称")
    mobile = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"手机")
    tel = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"座机")
    company = models.ForeignKey('BaseCompany', on_delete=models.SET_NULL, related_name='company_staffs',
                                null=True, blank=True, verbose_name=u"所属公司")
    email = models.EmailField(null=True, blank=True, verbose_name=u"邮箱")
    remark = models.CharField(max_length=300, null=True, blank=True, verbose_name=u"备注")

    def __str__(self):
        return self.name

    class Meta:
        app_label = APP_NAME
        ordering = ['name', "alias", "mobile"]
        permissions = (
            ("view_staffs", "Can View Staffs"),
        )
        verbose_name_plural = u"联系人"
        verbose_name = u"联系人"


class ItemsSet(models.Model):
    """
    项目集
    """
    id = models.BigIntegerField(primary_key=True)
    itemname = models.CharField(max_length=200, verbose_name=u"项目集名称")
    staffs = models.ForeignKey("Staffs", null=True, blank=True, verbose_name=u"联系人")
    cust = models.ForeignKey("BaseCustomerInfo", on_delete=models.SET_NULL, null=True, to_field="idcode",
                             verbose_name=u"所属客户")

    def __str__(self):
        return self.itemname

    class Meta:
        app_label = APP_NAME
        verbose_name_plural = u"项目集"
        verbose_name = u"项目集"
        permissions = (
            ("view_itemsset", "Can View ItemsSet"),
        )


class Projects(models.Model):
    """
    项目(系统)信息表
    """
    syslevel_choice = (
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")
    )
    id = models.BigIntegerField(primary_key=True)
    sysname = models.CharField(max_length=100, verbose_name=u"项目名称")
    sysalias = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"项目简称")
    company = models.ForeignKey('BaseCompany', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u"所属公司")
    syslevel = models.CharField(max_length=10, null=True, blank=True, choices=syslevel_choice, verbose_name=u"系统等级")
    disasterlevel = models.CharField(max_length=10, null=True, blank=True, choices=syslevel_choice,
                                     verbose_name=u"灾备等级")
    # cust = models.ForeignKey('BaseCustomerInfo', to_field="idcode", null=True, blank=True, verbose_name=u"所属客户")
    itemsset = models.ForeignKey("ItemsSet", null=True, blank=True, verbose_name=u"所属项目集")

    def __str__(self):
        return self.sysname

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_projects", "Can View Projects"),
        )
        verbose_name_plural = u"项目信息"
        verbose_name = u"项目信息"
        ordering = ["sysname", "sysalias", "company", "syslevel"]


class R_Project_Staff(models.Model):
    """
    项目联系人信息表
    """
    id = models.BigIntegerField(primary_key=True)
    project = models.ForeignKey("Projects", related_name="related_staffs", on_delete=models.CASCADE)
    staff = models.ForeignKey("Staffs")
    role = models.ForeignKey("BaseRole", null=True)

    def __str__(self):
        return "{0}:{1}".format(self.staff.name, self.role.role_name)

    class Meta:
        app_label = APP_NAME
        ordering = ['project']


class Business(models.Model):
    """
    业务线模块
    """
    id = models.BigIntegerField(primary_key=True)
    bussname = models.CharField(max_length=200, verbose_name=u"模块名称")
    project = models.ForeignKey('Projects', related_name="project_business", on_delete=models.CASCADE,
                                verbose_name=u"所属项目")

    def __str__(self):
        return "{0}:{1}".format(self.project, self.bussname)

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_business", "Can View Business"),
        )
        verbose_name_plural = u"业务模块"
        verbose_name = u"业务模块"
        ordering = ["project", "bussname"]


class Assets(models.Model):
    """
    服务器资产表
    """
    id = models.BigIntegerField(primary_key=True)
    assetno = models.CharField(max_length=50, unique=True)
    sn = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"序列号(SN)")
    model = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"型号")
    usetype = models.ForeignKey("BaseAssetType", related_name="asset_type", on_delete=models.SET_NULL, null=True,
                                verbose_name=u"用途属性")
    assettype = models.ForeignKey('BaseAssetSubtype', null=True, on_delete=models.SET_NULL, verbose_name=u"设备类型")
    room = models.ForeignKey('BaseMachineRoom', related_name='asset_room', on_delete=models.SET_NULL, null=True,
                             verbose_name=u"机房")
    cabinet = models.CharField(max_length=100, null=True, verbose_name=u"机柜")
    unitinfo = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"单元信息")
    cpu = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"CPU")
    memory = models.CharField(max_length=100, null=True, verbose_name=u"内存")
    manageip = models.GenericIPAddressField(max_length=100, null=True, verbose_name=u"管理IP")
    clusterinfo = models.CharField(max_length=200, null=True, verbose_name=u"集群信息")
    factory = models.ForeignKey('BaseFactory', related_name='asset_factory', on_delete=models.SET_NULL, null=True,
                                verbose_name=u"厂商")
    integrator = models.ForeignKey('BaseFactory', related_name='asset_integrator', on_delete=models.SET_NULL, null=True,
                                   verbose_name=u"集成商")
    tradedate = models.DateField(null=True, blank=True, verbose_name=u"购买日期")
    startdate = models.DateField(null=True, blank=True, verbose_name=u"开始保修期")
    expiredate = models.DateField(null=True, blank=True, verbose_name=u"过保日期")
    netarea = models.ForeignKey('BaseNetArea', related_name='asset_area', on_delete=models.SET_NULL, null=True,
                                verbose_name=u"网络区域")
    assetstatus = models.ForeignKey('BaseAssetStatus', related_name='asset_status', on_delete=models.SET_NULL,
                                    null=True, verbose_name=u"设备状态")
    cust = models.ForeignKey('BaseCustomerInfo', to_field='idcode', related_name='asset_cust',
                             on_delete=models.SET_NULL, null=True, verbose_name=u"所属客户")
    contact = models.CharField(max_length=200, null=True, verbose_name=u"硬件负责人")
    createuser = models.CharField(max_length=100, null=True, verbose_name=u"创建人")
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100, null=True, verbose_name=u"最近更新人")
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=200, null=True, blank=True)
    objects = models.Manager()
    report = cmdbmanger.AssetsManage()

    def __str__(self):
        if not self.usetype:
            return self.sn
        else:
            return "{0}:{1}".format(self.usetype.name if self.usetype else "", self.sn)

    class Meta:
        app_label = APP_NAME
        ordering = ['-createdate']
        permissions = (
            ("view_assets", "Can View Assets"),
        )
        verbose_name = u"服务器资产"
        verbose_name_plural = u"服务器资产"


class Servers(models.Model):
    """
    主机表
    """
    id = models.BigIntegerField(primary_key=True)
    hostname = models.CharField(max_length=200)
    type = models.ForeignKey("BaseAssetType", related_name='server', on_delete=models.SET_NULL, null=True)
    ownserver = models.ForeignKey('Assets', related_name='related_asset', on_delete=models.SET_NULL, null=True,
                                  blank=True)
    tradedate = models.DateField(null=True, blank=True)
    expiredate = models.DateField(null=True, blank=True)
    model = models.CharField(max_length=100, null=True)
    partition = models.CharField(max_length=100, null=True, verbose_name=u"分区名")
    netarea = models.ForeignKey('BaseNetArea', related_name='area_server', on_delete=models.SET_NULL, null=True)
    runningstatus = models.ForeignKey('BaseRunningStatus', related_name='run_status', on_delete=models.SET_NULL,
                                      null=True)
    balancetype = models.ForeignKey('BaseBalanceType', related_name='related_balance', on_delete=models.SET_NULL,
                                    null=True)
    cust = models.ForeignKey('BaseCustomerInfo', to_field='idcode', related_name='cust_server',
                             on_delete=models.SET_NULL,
                             null=True)
    createuser = models.CharField(max_length=100)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=200, null=True, blank=True)
    objects = models.Manager()
    report = cmdbmanger.HostManage()

    def __str__(self):
        if not self.type:
            return self.hostname
        else:
            return "{0}:{1}".format(self.type.name if self.type else "", self.hostname)

    class Meta:
        app_label = APP_NAME
        ordering = ['-createdate']
        permissions = (
            ("view_servers", "Can View Servers"),
        )
        verbose_name = u"主机"
        verbose_name_plural = u"主机"


class R_Server_Business(models.Model):
    id = models.BigIntegerField(primary_key=True)
    server = models.ForeignKey('Servers', related_name="related_business", on_delete=models.CASCADE)
    business = models.ForeignKey('Business', related_name="related_servers", on_delete=models.CASCADE)
    createuser = models.CharField(max_length=100)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100)
    updatedate = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = APP_NAME
        verbose_name = u"主机业务"
        verbose_name_plural = u"主机业务"


class R_Server_Staff(models.Model):
    """
    服务器联系人关联关系表
    """
    id = models.BigIntegerField(primary_key=True)
    server = models.ForeignKey('Servers', related_name="related_staffs", on_delete=models.CASCADE)
    staff = models.ForeignKey('Staffs')
    role = models.ForeignKey('BaseRole')
    createuser = models.CharField(max_length=100)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=200)

    def __str__(self):
        return "%s:%s" % (self.server.hostname, self.staff.name)

    class Meta:
        app_label = APP_NAME
        verbose_name = u"主机联系人"
        verbose_name_plural = u"主机联系人"


class IPConfiguration(models.Model):
    """
    IP配置表
    """
    id = models.BigIntegerField(primary_key=True)
    server = models.ForeignKey('Servers', related_name='server_ip', on_delete=models.CASCADE)
    ipaddress = models.GenericIPAddressField(null=True)
    gatway = models.GenericIPAddressField(null=True)
    iptype = models.CharField(max_length=100, null=True, blank=True)
    domain = models.CharField(max_length=100, null=True, blank=True)
    vlan = models.CharField(max_length=100, null=True, blank=True)
    createuser = models.CharField(max_length=100, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100, null=True)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return "{0}:{1}({2})".format(self.server.hostname, self.ipaddress, self.iptype)

    class Meta:
        app_label = APP_NAME
        verbose_name = u"主机IP配置"
        verbose_name_plural = u"主机IP配置"


class ServerBoardCard(models.Model):
    """
    服务器的板卡信息，包括网卡和存储卡
    """
    card_type = (
        (1, "网卡"), (2, "存储卡")
    )
    id = models.BigIntegerField(primary_key=True)
    assetno = models.CharField(max_length=100, unique=True)
    sn = models.CharField(max_length=100, unique=True, null=True, verbose_name=u"设备编号(SN)")
    server = models.ForeignKey("Servers", related_name="related_card", on_delete=models.CASCADE, verbose_name=u"所属主机")
    factory = models.ForeignKey("BaseFactory", on_delete=models.SET_NULL, null=True, verbose_name="厂商")
    model = models.CharField(max_length=100, null=True, verbose_name=u"型号")
    cardtype = models.IntegerField(choices=card_type, default=1, verbose_name=u"卡类型")
    mac = models.CharField(max_length=100, null=True, verbose_name=u"MAC/WWW")
    slot = models.CharField(max_length=50, null=True, verbose_name=u"槽位号")
    createuser = models.CharField(max_length=50, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100, null=True)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=200, null=True, verbose_name=u"备注")

    def __str__(self):
        return "{0}:{1}".format(self.server.hostname, self.get_cardtype_display())

    class Meta:
        app_label = APP_NAME
        verbose_name = u"主机板卡"
        verbose_name_plural = u"主机板卡"


class StorageVG(models.Model):
    """
    存储VG
    """
    id = models.BigIntegerField(primary_key=True)
    server = models.ForeignKey("Servers", related_name="related_vg", on_delete=models.CASCADE, verbose_name=u"所属主机")
    raidtype = models.ForeignKey("BaseRaidType", null=True, on_delete=models.SET_NULL, verbose_name=u"RAID类型")
    vgname = models.CharField(max_length=200, verbose_name=u"VG/Pool名称")
    vgsize = models.CharField(max_length=100, verbose_name=u"VG大小")
    createuser = models.CharField(max_length=100, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100, null=True)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=200, null=True, verbose_name=u"备注")

    def __str__(self):
        return "{0}:{1}".format(self.server.hostname, self.vgname)

    class Meta:
        app_label = APP_NAME
        verbose_name = u"主机存储"
        verbose_name_plural = u"主机存储"


class StoragePV(models.Model):
    """
    存储PV
    """
    id = models.BigIntegerField(primary_key=True)
    vg = models.ForeignKey("StorageVG", related_name="related_pv", on_delete=models.CASCADE, null=True,
                           verbose_name=u"所属VG")
    pvname = models.CharField(max_length=100, verbose_name=u"PV名称")
    pvsize = models.CharField(max_length=50, verbose_name=u"pv大小")
    createuser = models.CharField(max_length=100, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100, null=True)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=200, null=True, verbose_name=u"备注")

    def __str__(self):
        return "{0}:{1}".format(self.vg.vgname, self.pvname)

    class Meta:
        app_label = APP_NAME
        verbose_name = u"存储PV"
        verbose_name_plural = u"存储PV"


class StorageLV(models.Model):
    """
    存储LV
    """
    id = models.BigIntegerField(primary_key=True)
    vg = models.ForeignKey("StorageVG", related_name="related_lv", on_delete=models.CASCADE, verbose_name=u"所属VG")
    lvname = models.CharField(max_length=100, verbose_name=u"LV/LUN名称")
    lvsize = models.CharField(max_length=100, verbose_name=u"LV/LUN大小")
    filesystem = models.CharField(max_length=200, null=True, verbose_name=u"主机PV/FS")
    createuser = models.CharField(max_length=100)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=200, null=True, verbose_name=u"备注")

    def __str__(self):
        return "{0}:{1}".format(self.vg.vgname, self.lvname)

    class Meta:
        app_label = APP_NAME
        verbose_name = u"存储LV"
        verbose_name_plural = u"存储LV"


class CpuMemory(models.Model):
    """
    cpu和内存信息
    """
    id = models.BigIntegerField(primary_key=True)
    server = models.ForeignKey('Servers', related_name='server_cpu', on_delete=models.CASCADE, verbose_name=u"所属主机")
    model = models.CharField(max_length=50, null=True, verbose_name=u"型号")
    cpucount = models.CharField(max_length=10, null=True, verbose_name=u"CPU数")
    corecount = models.CharField(max_length=10, null=True, verbose_name=u"CPU核数")
    frequency = models.CharField(max_length=50, null=True, verbose_name=u"频率")
    memory = models.IntegerField(null=True, verbose_name=u"内存")
    createuser = models.CharField(max_length=100)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=300, null=True)

    def __str__(self):
        return "{0}:{1}C,{2}G".format(self.server.hostname, str(self.cpucount), str(self.memory))

    class Meta:
        app_label = APP_NAME
        verbose_name = u"CPU内存"
        verbose_name_plural = u"CPU内存"


class InstalledSoftList(models.Model):
    """
    安装软件信息
    """
    id = models.BigIntegerField(primary_key=True)
    server = models.ForeignKey('Servers', related_name='server_soft', on_delete=models.CASCADE)
    soft = models.ForeignKey('BaseSoft', on_delete=models.SET_NULL, null=True, blank=True)
    lisence = models.ForeignKey('SoftLisence', on_delete=models.SET_NULL, null=True, blank=True)
    port = models.CharField(max_length=200, null=True, blank=True)
    createuser = models.CharField(max_length=100, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100, null=True)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return "{0}:{1}".format(self.server.hostname, self.soft.name)

    class Meta:
        app_label = APP_NAME
        verbose_name = u"安装软件"
        verbose_name_plural = u"安装软件"


class Equipment(models.Model):
    """
    设备资产
    """
    id = models.BigIntegerField(primary_key=True)
    assetno = models.CharField(max_length=100, verbose_name='资产编号')
    sn = models.CharField(max_length=100, null=True, verbose_name='序列号')
    assetname = models.CharField(max_length=200, null=True, verbose_name='设备名称')
    assettype = models.ForeignKey('BaseEquipmentType', related_name='assettype_equipment', on_delete=models.SET_NULL,
                                  null=True, verbose_name='设备类型')
    room = models.ForeignKey('BaseMachineRoom', related_name='room_equipment', on_delete=models.SET_NULL, null=True, verbose_name='机房')
    cabinet = models.CharField(max_length=100, null=True, verbose_name=u"机柜")
    tradedate = models.DateField(null=True, verbose_name='购买日期')
    expiredate = models.DateField(null=True, verbose_name='过保日期')
    factory = models.ForeignKey('BaseFactory', related_name='equipment_factory',null=True, verbose_name='厂商')
    provider = models.ForeignKey('BaseFactory', related_name='equipment_provider', null=True, blank=True, verbose_name='供应商')
    serviceprovider = models.ForeignKey('BaseFactory', related_name='equipment_service',null=True, blank=True, verbose_name='服务提供商')
    model = models.CharField(max_length=100, null=True, verbose_name='型号')
    netarea = models.ForeignKey('BaseNetArea', on_delete=models.SET_NULL, null=True, verbose_name='网络区域')
    status = models.ForeignKey('BaseAssetStatus', on_delete=models.SET_NULL, null=True, verbose_name='设备状态')
    manageip = models.GenericIPAddressField(null=True, verbose_name='管理IP')
    portcount = models.IntegerField(null=True, verbose_name='端口数')
    slotindex = models.CharField(max_length=100, null=True, verbose_name='U位')
    powertype = models.CharField(max_length=100, null=True, verbose_name=u"电源数量")
    usetype = models.CharField(max_length=100, null=True, verbose_name=u"应用用途")
    cust = models.ForeignKey('BaseCustomerInfo', related_name='cust_equipment', to_field="idcode", null=True,
                             on_delete=models.SET_NULL, verbose_name='所属客户')
    createuser = models.CharField(max_length=100, verbose_name='创建人')
    createdate = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    updateuser = models.CharField(max_length=100, verbose_name='更新人')
    updatedate = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    remark = models.CharField(max_length=300, null=True, verbose_name='备注')
    customer001 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段1')
    customer002 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段2')
    customer003 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段3')
    customer004 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段4')
    customer005 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段5')
    customer006 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段6')
    customer007 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段7')
    customer008 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段8')
    customer009 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段9')
    customer010 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段10')
    customer011 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段11')
    customer012 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段12')
    customer013 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段13')
    customer014 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段14')
    customer015 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段15')
    customer016 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段16')
    customer017 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段17')
    customer018 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段18')
    customer019 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段19')
    customer020 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段20')
    customer021 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段21')
    customer022 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段22')
    customer023 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段23')
    customer024 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段24')
    customer025 = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'自定义字段25')
    objects = models.Manager()
    report = cmdbmanger.EquipmentManage()

    def __str__(self):
        return "{0} {1}".format(self.assettype.name if self.assettype else "", self.assetname)

    class Meta:
        app_label = APP_NAME
        ordering = ['-createdate']
        permissions = (
            ("view_equipment", "Can View Equipment"),
        )
        verbose_name = u"网络设备"
        verbose_name_plural = u"网络设备"


class PortList(models.Model):
    """
    所有的板卡端口列表,包括服务器资产的网卡/存储卡，网络设备的板卡，跳线架 端口
    """
    ptype = (
        (1, "服务器板卡"),
        (2, "网络设备板卡")
    )
    id = models.BigIntegerField(primary_key=True)
    object_pk = models.BigIntegerField(verbose_name=u"设备板卡ID")
    portname = models.CharField(max_length=100,verbose_name=u"端口名")
    porttype = models.CharField(max_length=100, null=True, verbose_name=u"端口类型")
    flag = models.IntegerField(choices=ptype, default=2, verbose_name=u"设备类型")
    vlan = models.CharField(max_length=20, null=True, verbose_name=u"VLAN")
    remark = models.CharField(max_length=200, null=True, verbose_name=u"备注")

    def __str__(self):
        if self.flag == 2:
            card_name = EquipmentBoardCard.objects.filter(id=self.object_pk).first().__str__()
        else:
            card_name = ServerBoardCard.objects.filter(id=self.object_pk).first().__str__()

        return "{0}({1})".format(self.portname, card_name)

    class Meta:
        app_label = APP_NAME
        ordering = ['portname']
        verbose_name = u"端口列表"
        verbose_name_plural = u"端口列表"


class EquipmentBoardCard(models.Model):
    """
    网络设备板卡信息表1
    """
    id = models.BigIntegerField(primary_key=True)
    assetno = models.CharField(max_length=100)
    sn = models.CharField( max_length=100, null=True, verbose_name=u"设备编号")
    equipment = models.ForeignKey("Equipment", related_name="related_card", on_delete=models.CASCADE,
                                  verbose_name=u"关联设备")
    cardname = models.CharField(max_length=100, verbose_name=u"板卡名")
    slot = models.CharField(max_length=100, null=True, verbose_name=u"槽位号")
    model = models.CharField( max_length=100, null=True, verbose_name=u"型号")
    createuser = models.CharField(max_length=100, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    updateuser = models.CharField(max_length=100, null=True)
    updatedate = models.DateTimeField(auto_now=True)
    remark = models.CharField( max_length=200, null=True, verbose_name=u"备注")

    def __str__(self):
        return "{0}:{1}".format(self.equipment.assetname if self.equipment else "", self.cardname)

    class Meta:
        app_label = APP_NAME
        verbose_name = u"网络设备板卡"
        verbose_name_plural = u"网络设备板卡"


class PortMapping(models.Model):
    """
    端口映射表,用来记录本地端口与对端端口的端口信息
    """
    id = models.BigIntegerField(primary_key=True)
    localport = models.ForeignKey("PortList", on_delete=models.CASCADE, related_name="related_local",
                                  verbose_name=u"本地端口")
    targetport = models.ForeignKey("PortList", on_delete=models.CASCADE, related_name="related_target",
                                   null=True, verbose_name=u"对端端口")
    remark = models.CharField(max_length=200, null=True, verbose_name=u'备注')

    def __str__(self):
        return self.localport

    class Meta:
        app_label = APP_NAME
        ordering = ['localport__portname']
        verbose_name = u"端口映射"
        verbose_name_plural = u"端口映射"


class R_Equipment_Staff(models.Model):
    """
    设备资产联系人
    """
    id = models.BigIntegerField(primary_key=True)
    equipment = models.ForeignKey('Equipment', related_name="related_staffs", on_delete=models.CASCADE, verbose_name=u"所属设备")
    staff = models.ForeignKey('Staffs', verbose_name='联系人')
    role = models.ForeignKey('BaseRole', verbose_name='角色')
    createuser = models.CharField(max_length=100, verbose_name='创建人')
    createdate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateuser = models.CharField(max_length=100, verbose_name='更新人')
    updatedate = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    remark = models.CharField(max_length=100, null=True, verbose_name='备注')

    def __str__(self):
        return self.staff.name

    class Meta:
        app_label = APP_NAME
        verbose_name = u"网络设备联系人"
        verbose_name_plural = u"网络设备联系人"


class AssetHistory(models.Model):
    """
    资产设备删除备份历史表
    """

    id = models.BigIntegerField(primary_key=True)
    model_name = models.CharField(max_length=100)
    data = models.TextField(null=True)
    op_date = models.DateTimeField(auto_now=True)
    op_user = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = APP_NAME
        permissions = (
            ("view_assethistory", "can view AssetHistory Record"),
        )


class OperateAudit(models.Model):
    """
    操作审计表
    """
    operate_time = models.DateTimeField(u"操作时间", auto_now_add=True)
    operater = models.CharField(u"操作人", max_length=100, null=True)
    action = models.CharField(u"动作", max_length=100, null=True)
    model_name = models.CharField(u"操作表", max_length=100, null=True)
    operate_data = models.CharField(u"操作数据", max_length=300, null=True)
    cust = models.ForeignKey('BaseCustomerInfo', to_field="idcode", null=True, on_delete=models.SET_NULL)
    object_pk = models.CharField(max_length=50, null=True)
    objects = models.Manager()
    audit = cmdbmanger.AuditManage()

    def __str__(self):
        return "{0}:{1}-{2}".format(self.operater, self.action, self.operate_data)

    class Meta:
        app_label = APP_NAME
        verbose_name_plural = u"审计"
        verbose_name = u"审计"
        permissions = (
            ("view_operateaudit", "can view OperateAudit"),
        )


class BackupRecord(models.Model):
    """
    数据库备份记录表
    """
    filename = models.CharField(max_length=200, verbose_name=u'文件名称')
    backupdate = models.DateTimeField(auto_now=True)
    backupuser = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=300, null=True, blank=True)

    @staticmethod
    def is_public():
        """
        此表为公共表,不区分客户
        :return:
        """
        return True

    def __str__(self):
        return "备份集 {0}".format(self.filename)

    class Meta:
        app_label = APP_NAME
        ordering = ["-backupdate"]
        verbose_name = u"数据备份"
        verbose_name_plural = u"数据备份"


class TemplsteVerification(models.Model):
    """
    对上传要导入的数据的模板文件进行验证
    """
    template_name = models.CharField(max_length=100, verbose_name=u"模板名称")
    md5_value = models.CharField(max_length=100, verbose_name=u"校验码")

    def __str__(self):
        return "{0}:{1}".format(self.template_name, self.md5_value)

    @staticmethod
    def is_public():
        """
        此表为公共表,不区分客户
        :return:
        """
        return True

    class Meta:
        app_label = APP_NAME
        verbose_name = u"模板校验"
        verbose_name_plural = u"模板校验"


class BalanceMapping(models.Model):
    """
    负载均衡F5映射管理
    """
    id = models.BigIntegerField(primary_key=True)
    equipment = models.ForeignKey("Equipment", verbose_name=u"所属设备")
    vsname = models.TextField(max_length=150, verbose_name=u"vs名称")
    vsaddr = models.GenericIPAddressField(null=True, blank=True, verbose_name=u"vs地址")
    port = models.IntegerField(null=True, blank=True, verbose_name=u"服务端口")
    dnsdomain = models.TextField(max_length=100, null=True, blank=True, verbose_name=u"DNS域名")
    snataddr = models.TextField(max_length=300, null=True, blank=True, verbose_name=u"SNAT地址")
    pooladdr = models.TextField(max_length=300, null=True, blank=True, verbose_name=u"地址池")
    ploy = models.ForeignKey("BaseBalanceType", null=True, blank=True, verbose_name=u"策略")
    vlan = models.TextField(null=True, blank=True, verbose_name=u"VLAN")
    datacenter = models.ForeignKey("BaseDataCenter", null=True, blank=True, verbose_name=u"数据中心")
    netarea = models.ForeignKey("BaseNetArea", verbose_name=u"所属区域")
    project = models.ForeignKey("Projects", null=True, blank=True, verbose_name=u"所属系统")
    business = models.TextField(max_length=100, null=True, blank=True, verbose_name=u"所属业务")
    hosttype = models.TextField(max_length=50, null=True, blank=True, verbose_name=u"主机类型")
    hostname = models.TextField(max_length=300, null=True, blank=True, verbose_name=u"主机名称")
    remark = models.TextField(max_length=200, null=True, blank=True)
    createdate = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.vsname

    class Meta:
        app_label = APP_NAME
        verbose_name_plural = "F5映射"
        verbose_name = "F5映射"
        permissions = (
            ("view_balancemapping", "can view F5 Mapping"),
        )
        ordering = ['-createdate']


class TableFieldPropertyClassify(models.Model):
    """
    数据表中每个字段的自定义字段名称表
    """
    propertykey = models.CharField(max_length=255, null=True, blank=True, verbose_name='属性key')
    propertyname = models.CharField(max_length=255, null=True, blank=True, verbose_name='显示名称')
    tablename = models.CharField(max_length=255, null=True, blank=True, verbose_name='表名称')
    tablefield = models.CharField(max_length=255, null=True, blank=True, verbose_name='字段名称')
    ordered = models.IntegerField(default=1, verbose_name='显示顺序')
    cust = models.ForeignKey('BaseCustomerInfo', related_name='cust_field_alias', to_field="idcode", null=True,
                             on_delete=models.SET_NULL, verbose_name='所属客户')
    createtime = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        app_label = APP_NAME
        verbose_name_plural = '表字段别名'
        verbose_name = '表字段别名'


class CustomerTableProperty(models.Model):
    """
    用户自定义扩展属性表
    """
    propertykey = models.CharField(max_length=255, null=True, blank=True, verbose_name='自定义key')
    propertyname = models.CharField(max_length=255, null=True, blank=True, verbose_name='显示名称')
    tablename = models.CharField(max_length=255, null=True, blank=True, verbose_name='表名称')
    tablefield = models.CharField(max_length=255, null=True, blank=True, verbose_name='扩展字段名称')
    cust = models.ForeignKey('BaseCustomerInfo', related_name='cust_field_customer', to_field="idcode", null=True,
                             on_delete=models.SET_NULL, verbose_name='所属客户')
    createtime = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        app_label = APP_NAME
        verbose_name_plural = '扩展字段表'
        verbose_name = '扩展字段表'