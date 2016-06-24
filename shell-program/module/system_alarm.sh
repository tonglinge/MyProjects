#!/bin/sh
#set -x
#################################################################
## system_alarm.sh alarmtype alarmtime alarmID alarmThreshold  ##
#################################################################

. ../cfg/alarm.conf
. ../cfg/host.conf

_OutputSqlPath=$SQL_FOLDER
alarmfilename="ALARM_"`hostname`"_"$(date +%Y%m%d%H%M%S)".sql"

if [ $# -lt 3 ]; then
  echo "Error Argument! need three Argument "
  exit
fi

alarmtype=` echo $1 | tr "[:upper:]" "[:lower:]" `
currday=$2
currtime=$3
hostname=`hostname`

case $alarmtype in
cpu)
    armcpu=$alarm_cpu
    title=$CPU_ALARM_TITLE
    contant=`echo $CPU_ALARM_CONTANT | sed -e s/%alarmtime/$currday" "$currtime/g  | sed -e s/%alarmidle/$armcpu/g | sed -e s/%current/$5/g`
    alarmtype="cpu.cap Threshold"
    alarm_type_id=$CPU_ALARM_ID
#    echo $title,$contant,"alarmID "$4 >> testalarm_cpu.log
;;
disk)
   armdisk=$alarm_disk
   title=$DISK_ALARM_TITLE
   contant=`echo $DISK_ALARM_CONTANT | sed -e s/%alarmtime/$currday" "$currtime/g | sed -e "s/%alarmpoint/$armdisk/g" | sed -e "s/%current/$5/g" | sed -e "s/%mountpoint/\$6/g" `
   alarmtype="disk.cap Threshold"
   alarm_type_id=$DISK_ALARM_ID
#   echo $title,$contant,"alarmID"$4 >> testalarm_disk.log   
;;
net)
    armnet=$alarm_net
    title=$NET_ALARM_TITLE
    contant=`echo $NET_ALARM_CONTANT | sed -e s/%alarmtime/$currday" "$currtime/g  | sed -e s/%alarmpoint/$alarmnet/g | sed -e s/%current/$5/g`
    alarmtype="net.cap Threshold"
   alarm_type_id=$NET_ALARM_ID
#    echo $title,$contant,"alarmID "$4 >> testalarm_net.log
;;
memory)
   armmemory=$alarm_memory
   title=$MEMORY_ALARM_TITLE
   contant=`echo $MEMORY_ALARM_CONTANT | sed -e s/%alarmtime/$currday" "$currtime/g  | sed -e s/%alarmpoint/$armmemory/g | sed -e s/%current/$5/g`
   alarmtype="memory.cap Threshold"
   alarm_type_id=$MEMORY_ALARM_ID
#   echo $title,$contant,"alarmID: "$4 >> testalarm_memory.log
;;
swap)
   armswap=$alarm_swap
   title=$SWAP_ALARM_TITLE
   contant=`echo $SWAP_ALARM_CONTANT | sed -e s/%alarmtime/$currday" "$currtime/g  | sed -e s/%alarmpoint/$armswap/g | sed -e s/%current/$5/g`
   alarmtype="swap.cap Threshold"
   alarm_type_id=$SWAP_ALARM_ID
#   echo $title,$contant,"alarmID: "$4 >> testalarm_swap.log
;;
*)
   exit
;;

esac

echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $_OutputSqlPath/$alarmfilename 
sql="insert into tab_alarm(ALARM_ID,HOST_ID,ALARM_TITLE,ALARM_TEXT,ALARM_TYPE,ALARM_TIME,SEND_SMS_FLAG,MSG_RECERVER,PHONE_LIST,ALARM_TYPE_ID) values($4,$HOST_ID,'$title','$contant','$alarmtype','$currday $currtime',1,'$ALARM_RECEIVE','$ALARM_TEL','$alarm_type_id');"
#echo $sql >> $_OutputSqlPath/$alarmfilename

