AFCAT
###

actions 动作

    actionid

    esc_period  步骤持续时间，必须大于60秒

    eventsource 事件源，对应events的source类型

    name    动作名称

    def_longdata    问题信息文本

    def_shortdata   问题信息主题

    r_longdata  恢复消息文本

    r_shortdata 恢复消息主题

    recovery_msg    是否启用恢复消息
        0   不启用
        1   启用

    status  是否启用动作
        0   启用
        1   禁用


operations

    operationid

    operationtype   操作类型
            0   发送消息
            1   远程命令
            2   添加主机
            3   移除主机
            4   添加到主机组
            5   从主机组移除
            6   链接到模版
            7   取消链接模版
            8   启用主机
            9   禁用主机
            10  设置主机清单模式

    actionid    对应actionsID

    esc_period  是否启用持续时间，持续时间必须大于60，如果设置为0，那么动作的持续时间将会被使用
            0   使用，默认为0

    esc_step_from   默认1

    esc_step_to     默认1

    evaltype    操作条件评估方法
            0   AND/OR
            1   AND
            2   OR

    opcommand

    opcommand_grp

    opcommand_hst

    opconditions

    opgroup

    opmessage

    opmessage_grp

    opmessage_usr

    optemplate

    opinventory



groups  主机组

    groupid 组ID

    name    组名

    internal    是否为内部组，内部组不能删除
            0   不是内部组
            1   是内部组，默认只有Discovered hosts是内部组

    flags   标记组的来源
            0   普通组
            4   通过自动发现添加的组

hosts_groups    主机与主机组中间表
    hostgroupid
    hostid  外键关联主机表
    groupid 外键关联主机组表

interface
    interfaceid 主键ID，非自增

    hostid  外键关联主机ID

    main    是否设置默认接口
            0   不默认
            1   默认

    type    接口类型
            1   agent
            2   SNMP
            3   IPMI
            4   JMX

    useip   建立连接是否通过IP
            0   连接使用主机dns域名
            1   连接使用主机IP

    ip  主机IP地址

    dns dns名字即能解析主机的名称

    port    接口端口号。可以包含用户宏

    bulk    是否使用大量的snmp请求
            0   不使用
            1   使用，默认

hosts_templates 主机模版
    hosttemplateid

    hostid      关联到hosts

    templateid  关联到hosts


主机
hosts
    hostid  主机ID／模版ID   readonly

    proxy_hostid    代理主机ID，即这台主机通过该代理主机去监控

    host    主机名，监控agent端ID字段

    status  主机状态
            0   已启用，监视这台主机
            1   停用的，不监视这台主机
            3   模版
            5   主动模式    创建代理时使用
            6   被动模式    创建代理时使用

    available   客户端agent主机是否可用  readonly
            0   未知或模版
            1   可用
            2   不可用

    description 描述主机

    disable_until   下一次轮询一个不可用主机的时间，默认只读readonly

    ipmi_authtype   认证算法
            -1  默认
            0   无
            1   MD2
            2   MD5
            4   Straight
            5   OEM
            6   RMCP+

    ipmi_privilege  特权级别
            1   回调
            2   用户  默认
            3   操作者
            4   管理者
            5   OEM

    ipmi_available  可用的ipmiagent
            0   未知
            1   可用
            2   不可用

    ipmi_disable_until  ipmi不可用时下一次的轮询时间

    ipmi_error  ipmi不可用的错误信息

    ipmi_errors_from    ipmi不可用状态从什么时候开始

    ipmi_password   ipmi    密码

    ipmi_username   ipmi用户名

    jmx_available   可用的jmxagent
            0   未知
            1   可用
            2   不可用

    jmx_disable_until   当jmx不可用时下一次轮询当时间

    jmx_error   jmx不可用错误信息

    jmx_errors_from jmx 不可用状态开始时间

    maintenance_from    资产维护开始时间

    maintenance_status  生效当状态
            0   不维护
            1   维护生效

    maintenance_type    生效维护的类型
            0   通过数据收集维护    默认
            1   非数据收集维护

    maintenanceid   维护的ID，如果当前主机处于维护状态，否则为null

    snmp_available  snmp是否可用
            0   未知
            1   可用
            2   不可用

    snmp_disable_until  当snmp不可用时下一次轮询时间

    snmp_error  不可用时错误信息

    snmp_errors_from    错误开始时间

    error   当agent不可用时显示当错误信息

    error_from  故障时间    当agent不可用时开始的时间

    name    主机显示的名称，即可见名称，默认是用host字段是值填充

    flags   主机来源
            0   表示普通的主机
            4   表示自动发现的主机

    inventory_mode  主机资产类型
            -1   禁用
            0   手动，默认值
            1   自动

    tls_connect 连接主机类型
            1   非加密
            2   共享密钥（PSK）
            4   证书

监控项
items
    itemid  监控项ID

    type    监控项类型
            0   Zabbix 客户端,
            1   SNMPv1 客户端,
            2   Zabbix采集器,
            3   简单检查,
            4   SNMPv2 客户端,
            5   Zabbix内部,
            6   SNMPv3 客户端,
            7   Zabbix客户端(主动式),
            8   Zabbix整合,
            10  外部检查,
            11  数据库监控,
            12  IPMI客户端,
            13  SSH 客户端,
            14  TELNET客户端,
            15  可计算的,
            16  JMX agent代理程序,
            17  SNMP trap

    hostid  关联主机ID

    name    监控项名称

    key_    监控项key值

    delay   间隔／秒

    history 历史数据保留时间／天

    trends  趋势数据保留时间／天  默认365天

    status  监控项启用状态
            0   启用
            1   禁用

    value_type  数据类型，对应的存放历史数据表
            0   history表 numeric float
            1   history_str表 character
            2   history_log表 log
            3   history_uint表 numeric unsigned
            4   history_text表 text

    authtype    ssh认证方法，只有通过ssh代理方式时使用
            0   密码
            1   public key

    units   数据类型单位

    data_type   数据类型
            0   decimal 十进制
            1   octal   八进制
            2   hexadecimal 十六进制
            3   boolean 布尔

    delay_flex  自定义间隔

    delta   存储的值
            0   (default) as is
            1   Delta, speed per second
            2   Delta, simple change

    error   如果监控项有问题会自动更新这个错误信息 readonly

    history     监控项保持的历史数据时长，默认90天，单位天

    formula     公式，自定义乘数
            1   默认值

    lastclock   监控项最后一次更新时间

    logtimefmt  格式化日志时间

    templateid  监控项对应的父模版ID，该ID自关联，模版对应的为hostid相当于模版分组

    flags   监控项来源
            0   普通
            4   自动发现

    interfaceid 网卡IP，对应interface表interfaceid

    params  额外的参数类型取决于监控项
            针对ssh和telnet监控项 执行脚本
            数据库监控项  执行sql
            计算类型    执行公式

    port    针对snmp监控项，端口监控

    password    密码认证，针对简单检查，ssh,telnet，数据库监视，jmx监控项

    description 监控项描述信息

    state   该监控项是否适用
            0   支持
            1   不支持


functions

    functionid

    itemid  关联监控项items表ID

    triggerid   关联触发器trigger表ID

    function    与表达式相关，触发器通过什么方法执行，如diff,last。。。

    parameter

triggers

    triggerid

    description 触发器信息

    error   当触发器状态更新显示的错误信息，如果有任何问题

    status  触发器状态
            0   已启用
            1   停用的

    value   触发器是否触发
            0   未触发 ok
            1   已触发 problem

    priority    触发器优先级
            0   未分类
            1   信息
            2   警告
            3   一般严重
            4   严重
            5   灾难

    lastchange  触发器最后一次改变状态的时间

    templateid  父模版触发器ID

    type    触发器是否可以产生多个事件
            0   不能产生    默认
            1   可以产生多个事件

    url     触发器相关联的url

    flags   触发器来源
            0   普通
            4   自动发现

    comments    告警评论信息，触发器描述信息

    state   触发器是否正常
            0   正常
            1   未知
history

    itemid

    clock

    value

    ns

history_log

    id

    itemid      监控项ID

    clock       收到数据的时间

    timestamp

    source

    severity

    value

    logeventid

    ns      毫微秒

history_str
    itemid
    clock
    value
    ns

history_text
    id
    itemid
    clock
    value
    ns

history_uint
    itemid
    clock
    value
    ns

trends  趋势图 foat
    clock   时间戳
    itemid  监控项
    num     一小时内的值的次数
    value_min   最小值
    value_avg   平均值
    value_max   最大值

trends_uint integer
    clock
    itemid
    num
    value_min
    value_avg
    value_max

events

    eventid     事件ID

    source      事件类型
            0   事件通过触发器创建
            1   事件通过自动发现规则创建
            2   事件通过活动的agent自动注册
            3   内部事件

    object      事件相关联的对象类型
            0   触发器
            1   自动发现主机
            2   自动发现服务
            3   自动注册主机
            4   item
            5   LLD规则

    objectid    相关联的对象ID

    clock       事件创建时间

    value       相关联对象的状态
            触发器对象
            0   OK
            1   problem
            自动发现事件
            0   主机或服务up
            1   主机或服务down
            2   主机或服务自动发现
            3   主机或服务丢失

            内部事件
            0   正常
            1   未知或不支持

    acknowledged    事件是否已经确认

    ns

acknowledges

    acknowledgeid

    userid

    eventid

    clock

    message

graphs

    graphid 监控图ID

    name    图形名称

    width   图形宽度

    height  图形高度

    flags   图形来源
            0   普通
            4   自动发现

    templateid  父图形模版ID，自关联

    graphtype   图形类型
            0   正常
            1   堆叠
            2   饼图
            3   爆发的



graphs_items

    gitemid

    graphid     关联graph表

    itemid      关联items表

    drawtype

    sortorder

    yaxisside

    calc_fnc

    color

    type    图形类型
            0   简单
            2   计算图形，适用于饼图，和爆发式的图形


ids

    table_name

    field_name

    nextid