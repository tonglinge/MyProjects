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
  check_start_time=$(date +%Y-%m-%d" "%H:%M":00")
  cpufilename="CPU_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"

  case $_osname in
   Linux)
   	systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1}' | awk '{print $NF}' `
        case  $systemUptime in
           days)
               systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1" "$2}'  | awk '{print $3" "$4" "$5}' | awk -F[':'] '{print $1" hours "$2" mins"}'`
               ;;
           min)
               systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1}' | awk '{print $3$4}'`
               ;;
           *)
               systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1}' | awk '{print $3$4}' |  awk -F[':'] '{print $1" hours "$2" mins"}'`
               ;;
          esac
   	tinfo=`$RHEL_CPU  | tail -1 `
        col=`echo $tinfo | awk '{print NF}' `
  #---RHEL5 has 17 cols,but RHEL4 has 16 cols,no 'st' cols ----#
        if [ $col = 17 ]; then
         tmp=` echo $tinfo | awk '{print $(NF-2)" "$(NF-3)" "$(NF-4)}' `
        else
         tmp=` echo $info | awk '{print $(NF-1)" "$(NF-2)" "$(NF-3)}' `
        fi
   	cpuIDLE=`echo $tmp | awk '{print $1}' `
   	cpuSystem=` echo $tmp | awk '{print $2}' `
   	cpuUser=`echo $tmp | awk '{print $3}' `
   	cpuIDLE=` echo "scale=3;$cpuIDLE/100" | bc `
   	cpuSystem=` echo "scale=3;$cpuSystem/100" | bc `
   	cpuUser=` echo "scale=3;$cpuUser/100" | bc `
       ;;
   HP-UX)
   	systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1}' | awk '{print $NF}' `
         case  $systemUptime in
           days)
               systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1" "$2}'  | awk '{print $3" "$4" "$5}' | awk -F[':'] '{print $1" hours "$2" mins"}'`
               ;;
           min)
               systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1}' | awk '{print $3$4}'`
               ;;
           *)
               systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1}' | awk '{print $3$4}' |  awk -F[':'] '{print $1" hours "$2" mins"}'`
               ;;
          esac
        tmp=` $HPUX_CPU  | tail -1 | awk '{print $NF" "$(NF-1)" "$(NF-2)}' `
   	cpuIDLE=`echo $tmp | awk '{print $1}' `
   	cpuSystem=` echo $tmp | awk '{print $2}' `
   	cpuUser=`echo $tmp | awk '{print $3}' `
   	cpuIDLE=` echo "scale=2;$cpuIDLE/100" | bc `
   	cpuSystem=` echo "scale=2;$cpuSystem/100" | bc `
   	cpuUser=` echo "scale=2;$cpuUser/100" | bc `
       ;;
   AIX)
   	systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1}' | awk '{print $NF}' `
        case  $systemUptime in
           days)
               systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1" "$2}'  | awk '{print $3" "$4" "$5}' | awk -F[':'] '{print $1" hours "$2" mins"}'`
               ;;
           min)
               systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1}' | awk '{print $3$4}'`
               ;;
           *)
               systemUptime=`$RHEL_UPTIME | awk -F[','] '{print $1}' | awk '{print $3$4}' |  awk -F[':'] '{print $1" hours "$2" mins"}'`
               ;;
          esac
        tmp=`$AIX_CPU  | tail -1 | awk '{print $(NF-1)" "$(NF-2)" "$(NF-3)}' ` cpuIDLE=`echo $tmp | awk '{print $1}' `
  	cpuSystem=` echo $tmp | awk '{print $2}' `
  	cpuUser=`echo $tmp | awk '{print $3}' `
	cpuIDLE=` echo "scale=3;$cpuIDLE/100" | bc `
   	cpuSystem=` echo "scale=3;$cpuSystem/100" | bc `
   	cpuUser=` echo "scale=3;$cpuUser/100" | bc `
      ;;
     *)
       echo " This Script doesn't support by this OS"
       exit
      ;; 
  esac
   
  ## check alarm #####
#     result=`echo $cpuIDLE $alarm_cpu | awk '{if($1>$2){printf"NoAlarm"}else{printf"Alarm"}}'`
 #    if [ $result = "Alarm" ]; then
 #       alarmID=` random`
 #      $PROGRAM_HOME/module/system_alarm.sh cpu $check_start_time $alarmID $cpuIDLE &
 #    else
        alarmID=""
 #    fi

 ##  write to sqlfile ##
 echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $_OutputSqlPath/$cpufilename
sql="insert into tab_system_cpu(HOST_ID,CHECK_START_TIME,SYSTEM_UPTIME,CPU_SYSTEM,CPU_USER,CPU_IDLE,ALARM_ID,CHECK_FREQUENCY)\
 values($HOST_ID,'$check_start_time','$systemUptime',$cpuSystem,$cpuUser,$cpuIDLE,'$alarmID','$fre_cpu min'); "

echo $sql >> $_OutputSqlPath/$cpufilename

}


main()
{
while true
do
 current=$(date +%H:%M:%S)
 min=`echo $current | awk -F[':'] '{print $2}'`
 sec=`echo $current | awk -F[':'] '{print $3}'`
let cursec=10#$min%$fre_cpu*60+10#$sec
let slptime=$fre_cpu*60-10#$cursec
# echo $slptime
 sleep $slptime
 CreateSql

# check cpuprocesses
sh $PROGRAM_HOME/module/system_cpuprocess_check.sh 
done

}

main
