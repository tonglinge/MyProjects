#!/bin/sh
#set -x
. ../cfg/command.conf
. ../cfg/host.conf

_hostname=`hostname`
_osname=`uname`
_OutputSqlPath=$SQL_FOLDER
check_start_time=""

random()
{
retnum=`echo | awk 'BEGIN{srand()}; {printf "%ld\n",rand()*1000000000}'`
echo $retnum
}

writeSql()
{
     writefile=$WORKING/$1
     hostid=$HOST_ID
     checktime=$check_start_time
     mountpoint=$2
     disksize=$3
     diskfree=$4
     diskused=$5
     diskcap=$6
     checkfre=$7

#  result=`echo $diskcap $alarm_disk | awk '{if($1>$2){printf"Alarm"}else{printf"NoAlarm"}}'`
#  if [ $result = "Alarm" ]; then
#     sleep 1
#     alarmID=`random`
#     alarmMountpoint=`echo $mountpoint | sed -e 's/\//\\\\\//g' `
#     $PROGRAM_HOME/module/system_alarm.sh disk $check_start_time $alarmID $diskcap $alarmMountpoint &
#  else
     alarmID=""
#  fi 
  if [ ! -f $writefile ]; then
     echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $writefile
  fi

  echo "insert into tab_system_disk(HOST_ID,CHECK_START_TIME,MOUNT_POINT,DISK_SIZE,DISK_FREE,DISK_USED,DISK_CAP,ALARM_ID,CHECK_FREQUENCY) values($hostid,'$checktime','$mountpoint',$disksize,$diskfree,$diskused,$diskcap,'$alarmID','$checkfre'); " >> $writefile
}


CreateSql()
{
  check_start_time=$(date +%Y-%m-%d" "%H:%M":00")
  diskfile="DISK_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"

  case $_osname in
  Linux)
           $RHEL_DISK | awk '{if (NF>2) print ;}' | grep -v Filesystem | grep -v /dev/shm > /tmp/disk.tmp
       #    echo "-------"`date +%H%M%S`"---------------" >> /tmp/disk_`date +%Y%m%d`.tmp
       #     cat /tmp/disk.tmp >> /tmp/disk_`date +%Y%m%d`.tmp
       #    echo "" >> /tmp/disk_`date +%Y%m%d`.tmp

            while read diskinfo
            do
		mountpoint=` echo $diskinfo | awk '{print $NF}' `
                disksize=` echo $diskinfo | awk '{print $(NF-4)}' `
                diskfree=` echo $diskinfo | awk '{print $(NF-2)}' `
                diskused=` echo $diskinfo | awk '{print $(NF-3)}' `
                diskcap=` echo $diskinfo | awk '{print $(NF-1)}' | awk -F['%'] '{print $1}'`
                diskcap=`echo "scale=2;$diskcap/100" | bc `
                checkfre=$fre_disk"min"
            writeSql $diskfile $mountpoint $disksize $diskfree $diskused $diskcap $checkfre 
            done < /tmp/disk.tmp
     mv $WORKING/$diskfile $SQL_FOLDER/    
   ;;
  HP-UX)
       $HPUX_DISK | awk '{if (NF>2) print ;}' | grep -v Filesyste > /tmp/disk.tmp 
       while read diskinfo
            do
                mountpoint=` echo $diskinfo | awk '{print $NF}' `
                disksize=` echo $diskinfo | awk '{print $(NF-4)}' `
                diskfree=` echo $diskinfo | awk '{print $(NF-2)}' `
                diskused=` echo $diskinfo | awk '{print $(NF-3)}' `
                diskcap=` echo $diskinfo | awk '{print $(NF-1)}' | awk -F['%'] '{print $1}'`
                diskcap=`echo "scale=2;$diskcap/100" | bc `
                checkfre=$fre_disk"min"
            writeSql $diskfile $mountpoint $disksize $diskfree $diskused $diskcap $checkfre
            done < /tmp/disk.tmp
   mv $WORKING/$diskfile $SQL_FOLDER/
   ;;
   AIX)
       $AIX_DISK | awk '{if (NF>2) print ;}' | grep -v Filesystem | grep -v /proc | grep -v /dev/odm > /tmp/disk.tmp 
       while read diskinfo
            do
                mountpoint=` echo $diskinfo | awk '{print $NF}' `
                disksize=` echo $diskinfo | awk '{print $(NF-5)}' `
                diskfree=` echo $diskinfo | awk '{print $(NF-4)}' `
                diskused=` echo $diskinfo | awk '{print $(NF-5)-$(NF-4)}' `
                diskcap=` echo $diskinfo | awk '{print $(NF-3)}' | awk -F['%'] '{print $1}'`
                diskcap=`echo "scale=2;$diskcap/100" | bc `
                checkfre=$fre_disk"min"
            writeSql $diskfile $mountpoint $disksize $diskfree $diskused $diskcap $checkfre
            done < /tmp/disk.tmp
    mv $WORKING/$diskfile $SQL_FOLDER/
   ;;
   *)
      exit
   ;;    
  esac

 ##--Clear temp file ----#
   rm /tmp/disk.tmp
}

main()
{
while true
do
 current=$(date +%H:%M:%S)
 min=`echo $current | awk -F[':'] '{print $2}'`
 sec=`echo $current | awk -F[':'] '{print $3}'`
let cursec=10#$min%$fre_disk*60+10#$sec
let slptime=$fre_disk*60-10#$cursec
#echo $slptime
sleep $slptime
CreateSql
done

}
main
