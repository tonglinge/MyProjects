#!/bin/sh
#set -x
. ../cfg/command.conf
. ../cfg/host.conf

_hostname=`hostname`
_osname=`uname`
_OutputSqlPath=$SQL_FOLDER

random()
{
retnum=`echo | awk 'BEGIN{srand()}; {printf "%ld\n",rand()*1000000000}'`
echo $retnum
}

CreateSql()
{
  check_start_time=$(date +%Y-%m-%d" "%H:%M:%S)
  memfilename="MEMORY_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"

  case $_osname in
   Linux)
        tmp=`$RHEL_MEMORY | grep Mem | awk '{print $2" "$3" "$4}' `
        tmpswap=`$RHEL_MEMORY | grep Swap | awk '{print $2" "$3" "$4}' `
       memphy=` echo $tmp | awk '{print $1}' `
       memfree=` echo $tmp | awk '{print $3}' `
       memcap=` echo "scale=2;($memphy-$memfree)/$memphy" | bc `
       swapinfo=`echo $tmpswap | awk '{print $1}' `
       swapused=` echo $tmpswap | awk '{print $2}' `
       swapcap=` echo "scale=2;$swapused/$swapinfo" | bc `
       ;;
   HP-UX)
       memphy=`$HPUX_MEMORY | tail -1 | awk '{print $7}'`
       memfree=`$HPUX_CPU | tail -1 | awk '{print $5}' `
let memfree=$memfree*4
       memcap=`echo "scale=2;($memphy-$memfree)/$memphy" | bc `
       tmpswap=`$HPUX_SWAP | grep dev | awk '{print $2" "$3" "$4}' `
       swapinfo=` echo $tmpswap | awk '{print $1}' `
       swapused=` echo $tmpswap | awk '{print $2}' `
       swapcap=`echo "scale=2;$swapused/$swapinfo" | bc `
       ;;
   AIX)
      memphy=`$AIX_MEMORY | tail -1 | awk '{print $2}'`
let memphy=$memphy*1024
      memfree=`$AIX_CPU| tail -1 | awk '{print $4}' `
let memfree=$memfree*4/1024
      memcap=` echo "scale=2;($memphy-$memfree)/$memphy" | bc`
      swaptmp=`$AIX_SWAP | tail -1 | awk '{print $4" "$5}' `
      swapinfo=`echo $swaptmp | awk '{print $1}' | awk -F['M'] '{print $1}' `
let swapinfo=$swapinfo*1024
      swapcap=`echo $swaptmp | awk '{print $2}' `
      swapused=`echo "scale=0;$swapinfo*$swapcap/100" | bc ` 
      swapcap=` echo "scale=2;$swapcap/100" | bc `
      ;;
  esac

##--- check memory alarm -----##
#  memresult=`echo $memcap $alarm_memory | awk '{if($1>$2){printf"Alarm"}else{printf"NoAlarm"}}'`
#     if [ $memresult = "Alarm" ]; then
#        alarmID=` random`
#       $PROGRAM_HOME/module/system_alarm.sh memory $check_start_time $alarmID $memcap &
#     else
        alarmID=""
#     fi
#  swapresult=`echo $swapcap $alarm_swap | awk '{if($1>$2){printf"Alarm"}else{printf"NoAlarm"}}'`
#     if [ $swapresult = "Alarm" ]; then
#        if [ "X"$alarmID = "X" ]; then        
#           alarmID=` random`
#        fi
#       $PROGRAM_HOME/module/system_alarm.sh swap $check_start_time $alarmID $swapcap &
#     fi
#---  write sql file ----#
echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $_OutputSqlPath/$memfilename
sql="insert into tab_system_memory(HOST_ID,CHECK_START_TIME,MEM_PHY,MEM_PHY_FREE,SWAP_INFO,SWAP_USED,MEM_CAP,SWAP_CAP,ALARM_ID,CHECK_FREQUENCY) values($HOST_ID,'$check_start_time',$memphy,$memfree,$swapinfo,$swapused,$memcap,$swapcap,'$alarmID','$fre_memory min');"
echo $sql >> $_OutputSqlPath/$memfilename
}


main()
{
while true
do
 current=$(date +%H:%M:%S)
 min=`echo $current | awk -F[':'] '{print $2}'`
 sec=`echo $current | awk -F[':'] '{print $3}'`
let cursec=10#$min%$fre_memory*60+10#$sec
let slptime=$fre_memory*60-10#$cursec
# echo $slptime
 sleep $slptime
 CreateSql

# check memprocess
sh $PROGRAM_HOME/module/system_memprocess_check.sh
done
}

main
