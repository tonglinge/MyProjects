use zabbix;
drop trigger if exists tri_monitorhistoryhistory;
DELIMITER $
create trigger tri_monitorhistoryhistory after insert
on history for each row
begin
declare host_exist int;
set host_exist=(select count(*) from monitor_monitorhistory where itemid=new.itemid);
if host_exist >0  then
    update `zabbix`.`monitor_monitorhistory` set clock=new.clock,value=new.value,ns=new.ns where itemid=new.itemid;
else
INSERT INTO `zabbix`.`monitor_monitorhistory`
(
`itemid`,
`clock`,
`value`,
`ns`)
VALUES
(
new.itemid,
new.clock,
new.value,
new.ns);

end if;
end$
DELIMITER ;

drop trigger if exists tri_monitorhistoryhistory_uint;
DELIMITER $
create trigger tri_monitorhistoryhistory_uint after insert
on history_uint for each row
begin
declare host_exist int;
set host_exist=(select count(*) from monitor_monitorhistory where itemid=new.itemid);
if host_exist >0  then
    update `zabbix`.`monitor_monitorhistory` set clock=new.clock,value=new.value,ns=new.ns where itemid=new.itemid;
else
INSERT INTO `zabbix`.`monitor_monitorhistory`
(
`itemid`,
`clock`,
`value`,
`ns`)
VALUES
(
new.itemid,
new.clock,
new.value,
new.ns);

end if;
end$
DELIMITER ;



-- 查询top 10 cpu
use zabbix;
SELECT h.hostid,h.name,FROM_UNIXTIME(hm.clock),hm.value,i.name,i.key_,i.units FROM hosts h,items i,monitor_monitorhistory hm WHERE h.hostid = i.hostid AND i.itemid = hm.itemid AND i.units = '%' AND i.key_ LIKE 'system.cpu.util%idle%' AND h.status = 0 ORDER BY hm.value DESC LIMIT 10

-- 查询内存
use zabbix;
SELECT h.hostid,h.name,FROM_UNIXTIME(hm.clock),hm.value,i.name,i.key_,i.units
FROM hosts h,items i,monitor_monitorhistory hm
WHERE h.hostid = i.hostid AND i.itemid = hm.itemid AND i.units = 'B' AND i.key_ LIKE 'vm.memory.size%available%' AND h.status = 0
ORDER BY hm.value DESC
LIMIT 10

-- 查询磁盘空闲

use zabbix;
SELECT h.hostid,h.name,FROM_UNIXTIME(hm.clock),hm.value,i.name,i.key_,i.units
FROM hosts h,items i,monitor_monitorhistory hm
WHERE h.hostid = i.hostid AND i.itemid = hm.itemid AND i.units = 'B' AND i.key_ LIKE 'vfs.fs.size%free%' AND h.status = 0
ORDER BY hm.value DESC
LIMIT 10

-- 查询网卡出口流量
use zabbix;
SELECT h.hostid,h.name,FROM_UNIXTIME(hm.clock),hm.value,i.name,i.key_,i.units
FROM hosts h,items i,monitor_monitorhistory hm
WHERE h.hostid = i.hostid AND i.itemid = hm.itemid AND i.units = 'bps' AND i.key_ LIKE 'net.if.out%' AND h.status = 0
ORDER BY hm.value DESC
LIMIT 10

-- 查询网络入口流量
use zabbix;
SELECT h.hostid,h.name,FROM_UNIXTIME(hm.clock),hm.value,i.name,i.key_,i.units
FROM hosts h,items i,monitor_monitorhistory hm
WHERE h.hostid = i.hostid AND i.itemid = hm.itemid AND i.units = 'bps' AND i.key_ LIKE 'net.if.in%' AND h.status = 0
ORDER BY hm.value DESC
LIMIT 10

-- 插入新主机
INSERT INTO `hosts`( `hostid` , `proxy_hostid` , `host` , `status` , `ipmi_authtype` , `ipmi_privilege` , `ipmi_username` , `ipmi_password` , `name` , `flags` , `templateid` , `description` , `tls_connect` , `tls_accept` , `tls_issuer` , `tls_subject` , `tls_psk_identity` , `tls_psk`) SELECT nextid + 1 id , NULL , 'Zabbix server' , '1' , '-1' , '2' , '' , '' , 'Zabbix server' , '0' , NULL , '' , '1' , '1' , '' , '' , '' , '' FROM ids WHERE table_name = 'hosts' AND field_name = 'hostid';

SELECT nextid + 1 id , FROM ids WHERE table_name = 'hosts' AND field_name = 'hostid';

INSERT INTO `hosts`( `hostid` , `proxy_hostid` , `host` , `status` , `ipmi_authtype` , `ipmi_privilege` , `ipmi_username` , `ipmi_password` , `name` , `flags` , `templateid` , `description` , `tls_connect` , `tls_accept` , `tls_issuer` , `tls_subject` , `tls_psk_identity` , `tls_psk`) values( '10084' , NULL , 'Zabbix server' , '1' , '-1' , '2' , '' , '' , 'Zabbix server' , '0' , NULL , '' , '1' , '1' , '' , '' , '' , '');

UPDATE ids SET nextid = '1001' WHERE table_name = 'hosts' AND field_name = 'hostid';

-- 查询所有主机的状态
SELECT DISTINCT h.hostid, h.`name`, h.`status`, h.available, h.snmp_available, h.jmx_available, h.ipmi_available FROM `hosts` h, hosts_groups hg, interface net WHERE h.hostid = net.hostid AND h.hostid = hg.hostid AND h.flags IN(0 , 4) AND net.dns LIKE "%s" AND h.`name` LIKE "%s" AND net.ip LIKE "%s" AND net.`port` = "%s" ORDER BY h.`name` LIMIT 50 OFFSET 0
-- 查询指定主机ID的应用集
-- SELECT * from applications WHERE hostid='10084'
-- 查询指定主机的监控项
-- SELECT * FROM items WHERE hostid = '10084' AND flags IN(0 , 4) ORDER BY `name`
-- 查询指定主机的触发器
-- SELECT t.* FROM `hosts` h , items i , `triggers` t , functions f WHERE h.hostid = i.hostid AND i.itemid = f.itemid AND t.triggerid = f.triggerid AND h.hostid = '10084' AND t.flags IN(0 , 4)
-- 查询指定主机的图形
-- SELECT DISTINCT g.graphid , g.`name` FROM `hosts` h , items i , graphs_items gi , graphs g WHERE h.hostid = i.hostid AND i.itemid = gi.itemid AND g.graphid = gi.graphid AND h.hostid = '10084' AND g.flags IN(0 , 4)
-- 查询指定主机的自动发现数
-- SELECT i.* FROM `hosts` h , items i WHERE h.hostid = i.hostid AND h.hostid = '10084' AND i.flags = 1 ORDER BY i.itemid
-- 查询所有主机
-- SELECT hostid , `host` , available , `name` FROM `hosts` WHERE flags IN(0 , 4) AND `status` = 0 ORDER BY `name`
-- 查询当前默认的接口
-- SELECT net.hostid , net.ip , net.`port` FROM `hosts` h , interface net WHERE h.hostid = net.hostid AND h.hostid = '10084' LIMIT 1
-- 查询指定主机的关联模版
-- SELECT * from `hosts` h, hosts_templates ht WHERE ht.hostid=10084 and h.hostid=ht.templateid
-- 查询指定主机的关联及链接模版
-- SELECT ht.hostid , ht.templateid , 1 FROM hosts_templates ht WHERE ht.hostid = 10084 UNION SELECT ht2.hostid , ht2.templateid , 2 FROM hosts_templates ht2 ,( SELECT ht.templateid FROM hosts_templates ht WHERE ht.hostid = 10084) b WHERE ht2.hostid = b.templateid

