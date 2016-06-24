#!/bin/sh
#set -x
. ../cfg/host.conf

_hostname=`hostname`
_osname=`uname`
_OutputSqlPath=$SQL_FOLDER

CreateSql()
{
  check_start_time=$(date +%Y-%m-%d" "%H:%M":00")
  cpufilename="EMS_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"
  
$TIB_HOME/ems/bin/tibemsadmin -server tcp://$ems_servip:$ems_servport -ignore -user $ems_user -password $ems_pwd -script $PROGRAM_HOME/cfg/emsscript.cfg > /tmp/emsinfo.tmp

  v_connstat=` cat /tmp/emsinfo.tmp | grep "Failed connect to" | awk '{print NF}' `
 if [ "X"$v_connstat = "X" ]; then
  conn=`cat /tmp/emsinfo.tmp | grep "Connections:" | awk '{print $2}' `
  pendmsg=`cat /tmp/emsinfo.tmp | grep "Pending Messages:" | awk '{print $3}'`
  pendsize=` cat /tmp/emsinfo.tmp | grep "Pending Message Size:" | awk '{if ($5=="MB") print $4*1024;else print $4}'`
  pendtype=` cat /tmp/emsinfo.tmp | grep "Pending Message Size:" | awk '{print $5}'`
  produce=`cat /tmp/emsinfo.tmp | grep Producers: | awk '{print $2}' `
  consumer=`cat /tmp/emsinfo.tmp | grep Consumers: | awk '{print $2}'`
  memuse=` cat /tmp/emsinfo.tmp | grep "Message Memory Usage:" |  awk '{if ($5=="MB") print $4*1024;else print $4}' `
  queues=` cat /tmp/emsinfo.tmp | grep Queues:  | awk '{print $2}' `
  activestat=1
else
  conn=0
  pendmsg=0
  pendsize="0.0"
  produce=0
  consumer=0
  memuse="0.0"
  queues=0
  activestat=0
 fi
echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $_OutputSqlPath/$cpufilename
sql=" INSERT INTO TAB_EMS_INFO (CHECK_START_TIME,CHECK_FREQUENCY,DOMAIN_NAME,EMS_CONNECTIONS,EMS_PENDING_MSG,EMS_PENDING_MSG_SIZE,EMS_PRODUCERS,EMS_CONSUMERS,EMS_MEMORY_USAGE,EMS_QUEUES,host_id,ACTIVE_STATUS) values('$check_start_time','$fre_ems min','$DOMAIN',$conn,$pendmsg,'$pendsize',$produce,$consumer,'$memuse',$queues,$HOST_ID,$activestat); "
echo $sql >> $_OutputSqlPath/$cpufilename
#echo $sql >> /home/tibco/shell-program/working/$cpufilename


rm /tmp/emsinfo.tmp
}


main()
{
 while true
do
 current=$(date +%H:%M:%S)
 min=`echo $current | awk -F[':'] '{print $2}'`
 sec=`echo $current | awk -F[':'] '{print $3}'`
let cursec=10#$min%$fre_ems*60+10#$sec
let slptime=$fre_ems*60-10#$cursec
# echo $slptime
 sleep $slptime
# check emsinfo
 CreateSql
# check emsconn info
sh $PROGRAM_HOME/module/system_emsconnection_check.sh 
# check ems pending_msg info
sh $PROGRAM_HOME/module/system_pendingmsg_check.sh
# check ems producers info
sh $PROGRAM_HOME/module/system_emsproducers_check.sh
done
}
main
