#!/bin/sh
#set -x
. ../cfg/host.conf
. ../cfg/command.conf

_hostname=`hostname`
_osname=`uname`
_OutputSqlPath=$SQL_FOLDER
_OutputDataPath=$PROGRAM_HOME"/data"
_OutputSqllogPath=$PROGRAM_HOME"/log"
tmpfile="/tmp/net.tmp"

net_dist=$HOST_GATEWAY

random()
{
retnum=`echo | awk 'BEGIN{srand()}; {printf "%ld\n",rand()*1000000000}'`
echo $retnum
}

writedata()
{
  datafile=$_OutputDataPath"/NET_"$_hostname"_"`date +%Y%m%d`
  if [ ! -f $datafile ]; then
    echo "HECK_START_TIME        HOST_ID CHECK_FREQUENCY NET_DEST        MAX_NET_TRIP    AVG_NET_TRIP    PACKET_LOSS     ALARM_ID">$datafile
  fi
  
 echo $1" "$2"	"$3"	"$4"	"$5"	"$6"	"$7"	"$8"	"$9 >> $datafile	
}


CreateSql()
{
check_start_time=`date +%Y-%m-%d" "%H:%M:%S`
netfilename="NET_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"

case $_osname in
HP-UX)
  $HPUX_NET $HOST_GATEWAY -n $NETPING_COUNT | tail -2 > $tmpfile
  max_net_trip=`cat $tmpfile | tail -1 | awk -F['='] '{print $2}' | awk -F['/'] '{print $3}'`
  avg_net_trip=`cat $tmpfile | tail -1 | awk -F['='] '{print $2}' | awk -F['/'] '{print $2}'`
  packet_loss=`cat $tmpfile | grep "packet loss" | awk -F[','] '{print $3}' | awk '{print $1}' | awk -F['%'] '{print $1}'`
;;
AIX)
  $AIX_NET -c $NETPING_COUNT $HOST_GATEWAY  | tail -2 > $tmpfile
  max_net_trip=` cat $tmpfile | tail -1 | awk -F['='] '{print $2}' | awk -F['/'] '{print $3}' | awk '{print $1}' `
  avg_net_trip=` cat $tmpfile | tail -1 | awk -F['='] '{print $2}' | awk -F['/'] '{print $2}' `
  packet_loss=` cat $tmpfile | grep "packet loss" | awk -F[','] '{print $3}' | awk '{print $1}' | awk -F['%'] '{print $1}'`
;;
Linux)
   $RHEL_NET -c $NETPING_COUNT $HOST_GATEWAY | tail -2 > $tmpfile
   max_net_trip=`cat $tmpfile | tail -1 | awk -F['='] '{print $2}' | awk -F['/'] '{print $3}'`
   avg_net_trip=`cat $tmpfile | tail -1 | awk -F['='] '{print $2}' | awk -F['/'] '{print $2}'`
   packet_loss=` cat $tmpfile | grep "packet loss" | awk -F[','] '{print $3}' | awk '{print $1}' | awk -F['%'] '{print $1}'`
;;
*)
 exit 
;;
esac

rm $tmpfile
## check alarm status ####
     result=`echo $packet_loss $alarm_net | awk '{if($1>$2){printf"Alarm"}else{printf"NoAlarm"}}'`
     if [ $result = "Alarm" ]; then
        alarmID=` random`
       $PROGRAM_HOME/module/system_alarm.sh net $check_start_time $alarmID $packet_loss &
     else
        alarmID=""
     fi

## write sqlfile ###

echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';" > $_OutputSqlPath/$netfilename
sql="insert into tab_system_net(HOST_ID,CHECK_START_TIME,NET_DEST,MAX_NET_TRIP,AVG_NET_TRIP,PACKET_LOSS,ALARM_ID,CHECK_FREQUENCY)\
 values($HOST_ID,'$check_start_time','$net_dist',$max_net_trip,$avg_net_trip,$packet_loss,'$alarmID','1min'); "

echo $sql  >> $_OutputSqlPath/$netfilename

## write datafile ####
#writedata $check_start_time	$HOST_ID	$fre_net"min"	$net_dist	$max_net_trip	$avg_net_trip	$packet_loss	'null' 

}

main()
{
while true
do
 current=$(date +%H:%M:%S)
 min=`echo $current | awk -F[':'] '{print $2}'`
 sec=`echo $current | awk -F[':'] '{print $3}'`
let cursec=10#$min%$fre_net*60+10#$sec
let slptime=$fre_net*60-10#$cursec
# echo $slptime
 sleep $slptime
 CreateSql
done  

}

main  

