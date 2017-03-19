use cmdb;

-- Dumping data for table `auth_user`
INSERT INTO `auth_user` VALUES (2,'pbkdf2_sha256$30000$n0QCHIl5LccG$HpUSOs+Ul9Y2T9vmkHnRea3d74EtAnMdlXVus9kj9Ek=',NULL,1,'afcat','','','',1,1,'2016-12-05 16:57:58.908701');
-- Dumping data for table `account_menus`
INSERT INTO `account_menus`(id,menu_code, menu_name,is_avaible) VALUES (10011,'m_001_0','计算',0),(10012,'m_002_0','网络',0),(10013,'m_003_0','存储',0),(10014,'m_004_0','安全',0),(10015,'m_005_0','容器',0),(10016,'m_006_0','监控',1),(10017,'m_007_0','CMDB',1),(10018,'m_008_0','自动化运维',0),(10019,'m_009_0','服务编排',0),(100110,'m_010_0','高可用',0),(100111,'m_011_0','业务性能分析',0),(100112,'m_012_0','微服务',0),(100113,'m_013_0','大数据',0),(100114,'m_014_0','日志',0),(100115,'m_015_0','邮件',0),(100116,'m_016_0','知识库',1),(100117,'m_017_0','应用市场',0),(100118,'m_018_0','帐号管理',1);

-- Dumping data for table `cmdb_basecustomerinfo`
INSERT INTO `cmdb_basecustomerinfo`(id,idcode,custalias,custname,custcode) VALUES (10011,1001,'包商银行','包商银行','C000002'),(10015,1002,'中民投','中国民生投资股份有限公司','C000037');

-- Dumping data for table `cmdb_basedatacenter`
INSERT INTO `cmdb_basedatacenter`(id,name) VALUES (10015,'马连道灾备数据中心'),(10017,'亦庄数据中心'),(10018,'西红门数据中心');

-- Dumping data for table `cmdb_basemachineroom`
INSERT INTO `cmdb_basemachineroom`(id,name,address,center_id) VALUES (10016,'中民投','北京市经济技术开发区东环北路11号',10017),(100110,'包商数据中心','北京市大兴区西红门北兴路东段2号，星光影视园 世纪互联星光机房',10018),(100111,'包商数字银行','北京市大兴区西红门北兴路东段2号，星光影视园 世纪互联星光机房',10018),(100112,'哈尔滨数据中心','北京市经济技术开发区东环北路11号',10017),(100113,'模型银行','北京市经济技术开发区东环北路11号',10017),(100114,'包商测试网','北京市大兴区西红门北兴路东段2号，星光影视园 世纪互联星光机房',10018),(100116,'包商银行灾备数据中心','马连道北京通信管理局2层机房',10015);

-- Dumping data for table `cmdb_baseassetcabinet`
INSERT INTO `cmdb_baseassetcabinet`(id, numbers, slotcount, room_id) VALUES (10011,'1-A01',NULL,100111),(10013,'1-B01',NULL,100113),(10014,'1-B02',NULL,100113),(10015,'A-20-23',43,100113),(100119,'167',NULL,100111),(100120,'177',NULL,100111),(100122,'183',NULL,100111),(100123,'173',NULL,100111),(100124,'166',176,100111),(100126,'185',NULL,100111),(100127,'175',NULL,100111),(100128,'168',NULL,100111),(100129,'178',NULL,100111),(100130,'H02',42,100116);

-- Dumping data for table `cmdb_baseassetstatus`
INSERT INTO `cmdb_baseassetstatus`(id, status, flag) VALUES (10012,'销毁',1),(10013,'闲置',0),(10014,'维护',0),(10015,'使用',0);

-- Dumping data for table `cmdb_baseassettype`
INSERT INTO `cmdb_baseassettype`(id, name,flag) VALUES (10011,'服务器设备',0),(10012,'虚拟主机',1),(10013,'存储设备',0),(10014,'备份设备',0),(10015,'特殊设备',0),(10016,'小机分区',1),(100111,'刀箱服务器',0),(100112,'工控机',0),(100117,'刀片服务器',0);

-- Dumping data for table `cmdb_baseassetsubtype`
INSERT INTO `cmdb_baseassetsubtype`(id,name,type_id) VALUES (10011,'HMC',100112),(10014,'HP小机',10011),(10015,'VMWARE虚拟机',10012),(10016,'青云虚拟机',10012),(10017,'OpenStack虚机',10012),(10018,'IBM小机分区',10012),(10019,'EMC存储',10013),(100110,'P750',10011),(100111,'P780',10011),(100112,'PC',10011),(100113,'TAPE',10011),(100114,'other',10011),(100130,'pureflex',100117);

-- Dumping data for table `cmdb_basebalancetype`
INSERT INTO `cmdb_basebalancetype`(id,typename) VALUES (10011,'负载'),(10012,'NAT'),(10013,'无调用关系'),(10014,'不过'),(10015,'优先级');


-- Dumping data for table `cmdb_basecompany`
INSERT INTO `cmdb_basecompany`(id,name) VALUES (10011,'其它'),(10012,'包商银行'),(10013,'亚联信息'),(10014,'中民投');


-- Dumping data for table `cmdb_basedepartment`
INSERT INTO `cmdb_basedepartment`(id,name,company_id,top_department_id,up_department_id) VALUES (10011,'科技处',10012,NULL,NULL);

-- Dumping data for table `cmdb_baseequipmenttype`
INSERT INTO `cmdb_baseequipmenttype`(id,name) VALUES (10011,'交换机'),(10012,'路由器'),(10013,'防火墙'),(10015,'负载设备F5');

-- Dumping data for table `cmdb_basefactory`
INSERT INTO `cmdb_basefactory`(id, name,contact) VALUES (10011,'IBM',''),(10012,'EMC',''),(10013,'DELL',''),(10014,'惠普',''),(10015,'联想',''),(10016,'思科',''),(10017,'F5',''),(10018,'H3','');

-- Dumping data for table `cmdb_basenetarea`
INSERT INTO `cmdb_basenetarea`(id, name) VALUES (10011,'生产后台'),(10012,'办公后台'),(10013,'电话银行'),(10014,'管理区'),(10015,'互联网隔离区'),(10017,'互联网后台'),(10018,'外联隔离');

-- Dumping data for table `cmdb_baseraidtype`
INSERT INTO `cmdb_baseraidtype`(id,typename) VALUES (10011,'RAID0'),(10012,'RAID1'),(10013,'RAID2'),(10014,'RAID4'),(10015,'RAID5'),(10016,'RAID6'),(10017,'RAID7'),(10018,'RAID0+1');

-- Dumping data for table `cmdb_baserole`
INSERT INTO `cmdb_baserole`(id, role_name) VALUES (10011,'甲方(银行)负责人'),(10015,'外包项目经理'),(10017,'外包运维人员'),(10018,'硬件负责人'),(10019,'应用负责人'),(100111,'负责人');

-- Dumping data for table `cmdb_baserunningstatus`
INSERT INTO `cmdb_baserunningstatus`(id,status) VALUES (10011,'使用'),(10012,'关闭'),(10013,'销毁'),(10014,'未使用');

-- Dumping data for table `cmdb_basesofttype`
INSERT INTO `cmdb_basesofttype`(id,name) VALUES (10011,'操作系统'),(10012,'数据库软件'),(10013,'中间件系统'),(10014,'应用系统');

-- Dumping data for table `cmdb_basesoft`
INSERT INTO `cmdb_basesoft`(id,name,version,type_id) VALUES (10011,'RHEL','7.0',10011),(10012,'RHEL','6.4',10011),(10013,'CentOS','7.0',10011),(10014,'HPUX','11.11',10011),(10015,'HPUX','11.23',10011),(10016,'AIX','6.3',10011),(10017,'ORACLE','10.0.2.4',10012),(10018,'ORACLE','11G',10012),(10019,'ORACLE','12C',10012),(100110,'weblogic','10.3.5',10013),(100114,'SUSE','11 sp3',10011),(100115,'linux','',10011),(100116,'WIN 2008 R2','WIN 2008 R2',10011),(100118,'AIX 6108-02-1316','AIX 6108-02-1316',10011),(100119,'Solaris 10 update 9','Solaris 10 update 9',10011),(100121,'WAS ND 7.1','',10013),(100122,'IHS 7','',10013),(100123,'WEBLOGIC','10.3.5',10013),(100124,'JDK 1.6','JDK 1.6',10013),(100125,'WAS 7.0.0.25','WAS 7.0.0.25',10013),(100126,'TOMCAT 6.0','TOMCAT 6.0',10013),(100131,'DB2','10.1.0.3',10012),(100132,'AIX','6108-05-1415',10011);

-- Dumping data for table `cmdb_softlisence`
INSERT INTO `cmdb_softlisence`(id,lisence,tradedate,expiredate,remark,soft_id) VALUES (10017,'8293-1928-3928-49','2016-01-01','2020-01-01','',10017);

-- Dumping data for table `cmdb_projects`
INSERT INTO `cmdb_projects`(id,sysname,sysalias,syslevel,company_id,cust_id,disasterlevel) VALUES (10011,'资金系统','SUMMIT','1',10011,1001,'1'),(10012,'助贷系统','ZXDK','3',10011,1001,'3'),(10013,'亚联柜面通','MBIS','2',10011,1001,'2'),(10014,'统一报价平台/路透','','1',10011,1001,'1'),(10015,'外汇清算','FEX','1',10011,1001,'1'),(10016,'深证通前置','','2',10011,1001,'2'),(10017,'资金托管','ACS','1',10011,1001,'1'),(10018,'影像平台','BDS','3',10011,1001,'3'),(10019,'电子银行业务监控','TMS','3',10011,1001,'3'),(100110,'人力资源管理系统','HR','4',10011,1001,'4'),(100111,'客户风险管理','FXGL','3',10011,1001,'3'),(100112,'手机银行贴膜版','MBFR','4',10011,1001,'4'),(100113,'二代支付','','2',10011,1001,'2'),(100114,'现金管理','CMP','2',10012,1001,'2'),(100115,'存款','DM','1',10012,1001,'1'),(100117,'BPP','BPP','1',10012,1001,'1'),(100118,'SAP PI','SAP PI','3',10012,1001,'2'),(100119,'Solution Manager/SMD','SMD','3',10012,1001,'2'),(100120,'贷款核算/CML','CML','2',10012,1001,'2'),(100121,'SAP PORTAL门户','PORTAL','3',10012,1001,'2'),(100122,'信贷管理系统','CMIS','2',10012,1001,'2');

-- Dumping data for table `cmdb_business`
INSERT INTO `cmdb_business`(id,bussname,project_id) VALUES (10011,'资金业务系统',10011),(10012,'资金数据库',10011),(10013,'高校助学贷款',10012),(10014,'生源地助学贷款',10012),(10015,'亚联柜面通-前置',10013),(10016,'统一报价平台-前置',10014),(10017,'外汇清算-SWIFT',10015),(10018,'深证通前置',10016),(10019,'应用服务器',10017),(100110,'数据库服务器',10017),(100111,'文档服务器',10017),(100112,'应用',100114),(100113,'数据库',100114),(100115,'应用服务器',100117),(100116,'数据库服务器（HADR）',100117),(100117,'消息服务器（主备）',100117),(100119,'PI(主备)',100118),(100120,'SOLMAN(单机)',100119),(100121,'应用(F5)',100120),(100122,'数据库(主备)-消息',100120),(100123,'应用(F5)',100121),(100124,'数据库(主备)',100121),(100126,'WEB服务器(F5) web服务器02(VM)',100122),(100127,'数据库(主备)',100122),(100128,'应用系统',100110);

-- Dumping data for table `cmdb_staffs`
INSERT INTO `cmdb_staffs`(id,name,alias,mobile,tel,email,remark,company_id) VALUES (10015,'郑明清','zhengmingqing','','','','',10012),(10016,'程海先','程海先','','','','',10012),(10017,'杨文举','杨文举','','','','',10012),(10018,'李铸','李铸','','','','',10012),(10019,'王丽','王丽','','','','',10013),(100110,'闫建军','闫建军','','','','',10013),(100112,'毛国鹏','毛国鹏','','','','',10013),(100113,'周立涛','周立涛','','','','',10013),(100114,'张锰','张锰','','','','',10013),(100115,'李想','李想','','','','',10013),(100116,'杨瑞','杨瑞','','','','',10013),(100117,'于璠','于璠','','','','',10013),(100118,'王源','王源','','','','',10013),(100119,'李乾坤','李乾坤','','','','',10013),(100120,'朱孔亮','朱孔亮','','','','',10013);

-- Dumping data for table `cmdb_ids`
INSERT INTO `cmdb_ids` VALUES (1,'account_menus',100119),(2,'cmdb_assethistory',10011),(3,'cmdb_assets',10011),(4,'cmdb_baseassetcabinet',100131),(5,'cmdb_baseassetstatus',10016),(6,'cmdb_baseassetsubtype',100131),(7,'cmdb_baseassettype',100118),(8,'cmdb_basebalancetype',10016),(9,'cmdb_basecompany',10015),(10,'cmdb_basecustomerinfo',10016),(11,'cmdb_basedatacenter',10019),(12,'cmdb_basedepartment',10012),(13,'cmdb_baseequipmenttype',10016),(14,'cmdb_basefactory',10019),(15,'cmdb_basemachineroom',100117),(16,'cmdb_basenetarea',10019),(17,'cmdb_baseraidtype',10019),(18,'cmdb_baserole',100112),(19,'cmdb_baserunningstatus',10015),(20,'cmdb_basesoft',100133),(21,'cmdb_basesofttype',10015),(22,'cmdb_business',100129),(23,'cmdb_cpumemory',10012),(24,'cmdb_equipment',10011),(25,'cmdb_equipmentboardcard',10011),(26,'cmdb_ids',10011),(27,'cmdb_installedsoftlist',10011),(28,'cmdb_ipallocation',10011),(29,'cmdb_ipconfiguration',10012),(30,'cmdb_ipsource',10011),(31,'cmdb_operateaudit',10011),(32,'cmdb_portlist',10011),(33,'cmdb_portmapping',10011),(34,'cmdb_projects',100123),(35,'cmdb_r_equipment_staff',10011),(36,'cmdb_r_machineroom_staff',10011),(37,'cmdb_r_project_staff',10011),(38,'cmdb_r_server_business',10016),(39,'cmdb_r_server_staff',10011),(40,'cmdb_serverboardcard',10011),(41,'cmdb_servers',10015),(42,'cmdb_softlisence',10018),(43,'cmdb_staffs',100121),(44,'cmdb_storagelv',10011),(45,'cmdb_storagepv',10011),(46,'cmdb_storagevg',10011);


