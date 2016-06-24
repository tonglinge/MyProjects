#!/bin/sh
#set -x
. ../cfg/host.conf

_hostname=`hostname`
_osname=`uname`
WriteSql=$WORKING
_OutputSqlPath=$SQL_FOLDER

CreateSql()
{
  check_start_time=$(date +%Y-%m-%d" "%H:%M":00")
  msgfilename="EMSPENDMSG_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"

$TIB_HOME/ems/bin/tibemsadmin -server tcp://$ems_servip:$ems_servport -ignore -user $ems_user -password $ems_pwd -script $PROGRAM_HOME/cfg/emsqueuemsg.cfg > /tmp/ems_pendmsg.tmp

#Check Connection Status
v_connstat=`cat /tmp/ems_pendmsg.tmp | grep "Failed connect to" | awk '{print $1}' `
if [ "X"$v_connstat != "XFailed" ]; then
#Format columns for sql
#Format: queue_name  queue_type  connections  pending_msg  pending_msg_size
#Get "show queues" info,format columns for sql
cat /tmp/ems_pendmsg.tmp | awk '/\\*[+-][+-][+-][+-][+-][+-][+-][+-][+-]\\*/'| grep -v '$sys' | grep -v '>' | awk '$NF ~ /[Kb|MB]/' | awk '{if (NF==8) print $1$2"  QUEUE  "$(NF-3)"  "$(NF-2)"  "$(NF-1)"  "$NF;else print $1"  QUEUE  "$(NF-3)"  "$(NF-2)"  "$(NF-1)"  "$NF}' > /tmp/ems_pendmsg_sql.tmp
# Get "show durables" info,format columns for sql
cat /tmp/ems_pendmsg.tmp |awk '$NF ~ /[Kb|MB]/'| awk '$(NF-3) ~ /[A-Z|offline]/' | awk '{if (NF>=6) print $0}' | awk '{print $(NF-4)"  DURABLE  "$(NF-3)"  "$(NF-2)"  "$(NF-1)"  "$NF }'|awk '{ if ($3=="<offline>") print $1"  "$2"  0  "$4"  "$5;else print $1"  "$2"  1  "$4"  "$5}' >> /tmp/ems_pendmsg_sql.tmp

#Create Sql
echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $WriteSql/$msgfilename
while read pendmsg
do
check_fre=$fre_ems" min"
domain=$DOMAIN
queue_name=`echo $pendmsg | awk '{print $1}' `
queue_type=`echo $pendmsg | awk '{print $2}' `
queue_connections=`echo $pendmsg | awk '{print $3}' `
queue_pend_msg=`echo $pendmsg | awk '{print $4}'`
queue_pend_size=`echo $pendmsg | awk '{if ($NF=="MB") print $5*1024;else print $5}'`
host_id=$HOST_ID

sql="INSERT INTO TAB_PENDING_QUEUE(CHECK_START_TIME,CHECK_FREQUENCY,DOMAIN_NAME,QUEUE_NAME,QUEUE_TYPE,QUEUE_CONNECTIONS,PENDING_MSG,PENDING_MSG_SIZE,HOST_ID) values('$check_start_time','$check_fre','$domain','$queue_name','$queue_type','$queue_connections',$queue_pend_msg,$queue_pend_size,$host_id); "
echo $sql >> $WriteSql/$msgfilename

done < /tmp/ems_pendmsg_sql.tmp
#Exec Producer "sync_event_queue(v_domain varchar(12))"  
echo "exec sync_event_queue($DOMAIN);" >> $WriteSql/$msgfilename

mv $WriteSql/$msgfilename $_OutputSqlPath
rm -rf /tmp/ems_pendmsg_sql.tmp
else
echo $check_start_time"     "`cat /tmp/ems_pendmsg.tmp | grep "Failed connect to"` >> $PROGRAM_HOME/log/pendmsg_error.log 
fi
rm -rf /tmp/ems_pendmsg.tmp
}


CreateSql
