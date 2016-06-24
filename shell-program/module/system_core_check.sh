#!/bin/bash
#set -x
. ../cfg/host.conf

_hostname=`hostname`
WriteSql=$WORKING
_OutputSqlPath=$SQL_FOLDER


CreateCoreFile()
{
LOGS=/shared/esb/applogs/core
checkdate=`sh FunctionDate.sh $(date +%Y%m%d)`
echo $checkdate
for x in up-teller1 up-teller2 up-teller3 up-teller4 down-rb down-cl down-dp down-gl down-cd down-fm down-data up-data down-mm down-fx up-nv down-ft down-pi down-tf \
up-tf down-pg up-pg down-cdbcls up-cdbcls down-cdbwf up-wf up-summit up-dbank down-cdbibpinfo down-cdbsilinfo up-cdbibp up-cdbrt up-cdbsil downlog 
do
if [ -d $LOGS/$x/log/$checkdate ]; then
	echo  "$checkdate $x Send and Rece is `cat $LOGS/$x/log/$1/Info.log |grep "MsgSend" |wc -l` \
`cat $LOGS/$x/log/$1/Info.log |grep "MsgRevd" |wc -l`" >> /tmp/emscoreinfo.tmp 
	else
	echo "$checkdate $x Send and Rece is" "     0        0" >> /tmp/emscoreinfo.tmp
fi
done
}

CreateSql()
{
  CreateCoreFile
  corefilename="CORE_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"
  let i=1
  echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD';" > $WriteSql/$corefilename

  while read corefile
  do
    bname=`echo $corefile | awk '{print "CORE_"$2}'`
    bname=`echo $bname | tr "[:lower:]" "[:upper:]"`
    starttime=`echo $corefile | awk '{print $1}'`
    receive=`echo $corefile | awk '{print $8}'`
    send=`echo $corefile | awk '{print $7}'`
    let err=$send-$receive
    sql="insert into tab_core_bussiness(BUSSINESS_UNIQUE_ID,BUSSINESS_UNIQUE_NAME,START_TIME,CORE_RECVS,CORE_SENDS,CORE_ERRS) \
         values($i,'$bname','$starttime',$receive,$send,$err);"    
    echo $sql >> $WriteSql/$corefilename
    let i=$i+1
  done < /tmp/emscoreinfo.tmp
rm -rf /tmp/emscoreinfo.tmp
mv $WriteSql/$corefilename  $_OutputSqlPath
}

main()
{
while true
do
time=$fre_coreat
hour1=`echo $time|awk -F[:] '{print $1}'`
min1=`echo $time | awk -F[':'] '{print $2}' `
sec1=`echo $time | awk -F[':'] '{print $3}' `
let totalsec=(10#$hour1*60+10#$min1)*60+$sec1

currtime=$(date +%H:%M:%S)
hour2=`echo $currtime|awk -F[:] '{print $1}'`
min2=`echo $currtime | awk -F[':'] '{print $2}' `
sec2=`echo $currtime | awk -F[':'] '{print $3}' `
let currsec=(10#$hour2*60+10#$min2)*60+$sec2

let sleepsec=10#$totalsec-10#$currsec
if [ $sleepsec -lt 0 ]; then
let sleepsec=86400+$sleepsec
fi

#echo $time
#echo $currtime
#echo $sleepsec
sleep $sleepsec
CreateSql
done
}

main
