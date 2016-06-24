#!/bin/sh
#set -x
. ../cfg/host.conf


DOWNLOG=/shared/esb/applogs/core/downlog/log
hostname=`hostname`
str_today=$(date +%Y-%m-%d)
workfolder=$WORKING
sqlfolder=$SQL_FOLDER
FileName="DOWNLOG_"$hostname"_"`date +%Y%m%d%H%M%S`".sql"
check_start_time=$(date +%Y-%m-%d" "%H:%M":00")

#Format Date yyyy-mm-dd to yyyymmdd
Fun_FormatDate()
{
  yy=`expr substr $1 1 4`
  mm=`expr substr $1 6 2`
  dd=`expr substr $1 9 2`
  echo $yy$mm$dd
}
# 1 Delete the num-record file for yesterday 
Fun_DelReclogForYesterday()
{
tmp_today=`Fun_FormatDate $str_today`
yesterday=`$PROGRAM_HOME/module/FunctionDate.sh $tmp_today` 
yesterday=`Fun_FormatDate $yesterday`
if [ -f ../log/downlog_$yesterday.rec ]; then
   rm ../log/downlog_$yesterday.rec
fi
}
# if  have downlog file  
Fun_CreateRecLog()
{
if [ -d $DOWNLOG/$str_today ]; then
TotalRecNum=`cat $DOWNLOG/$str_today/Info.log | wc -l`
 if [ -f ../log/downlog_$tmp_today.rec ]; then
  LastRecNum=`cat ../log/downlog_$tmp_today.rec`
let  NewRecNum=10#$TotalRecNum-10#$LastRecNum
   if [ "X"$NewRecNum != "X0" ]; then
     cat $DOWNLOG/$str_today/Info.log | tail -$NewRecNum > /tmp/CoreDownlog.tmp
   fi
 else
  cat $DOWNLOG/$str_today/Info.log > /tmp/CoreDownlog.tmp
 fi
echo $TotalRecNum > ../log/downlog_$tmp_today.rec
fi
}

#Create SQL file for DB
Fun_CreateSql()
{
if [ -f /tmp/CoreDownlog.tmp ]; then
echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $workfolder/$FileName
while read downlog
do
log_date=`echo $downlog | awk '{print $1}' | awk '{print substr($0,length($0)-9)}' `
log_time=`echo $downlog | awk '{print $2}' | awk '{print substr($0,1,5)}' `
down_date=$log_date" "$log_time
down_upsys=`echo $downlog | awk -F['>'] '{print $2}' | awk -F[','] '{print $1}' `
down_downsys=`echo $downlog | awk -F['>'] '{print $2}' | awk -F[','] '{print $2}'`
down_cid=`echo $downlog |  awk -F['>'] '{print $2}' | awk -F[','] '{print $5}' `
down_msgid=`echo $downlog | awk '{print $1}' | awk '{print substr($0,2,length($0)-13)}' `
Sql="INSERT INTO TAB_DOWNLOG(CHECK_START_TIME,DOWNLOG_DATE,MSGID,UP_SYSTEM,DOWN_SYSTEM,CORRELATION_ID,HOST_ID) VALUES('$check_start_time','$down_date','$down_msgid','$down_upsys','$down_downsys','$down_cid',$HOST_ID);"
echo $Sql >> $workfolder/$FileName

done < /tmp/CoreDownlog.tmp
rm /tmp/CoreDownlog.tmp
fi
}

Main()
{
 while true
do
 current=$(date +%H:%M:%S)
 min=`echo $current | awk -F[':'] '{print $2}'`
 sec=`echo $current | awk -F[':'] '{print $3}'`
let cursec=10#$min%$fre_downlog*60+10#$sec
let slptime=$fre_downlog*60-10#$cursec
 sleep $slptime
 Fun_DelReclogForYesterday
 Fun_CreateRecLog
 Fun_CreateSql
done
}


Main
