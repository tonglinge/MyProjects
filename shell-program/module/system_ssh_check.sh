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
  connfilename="SSH_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"

cd $PROGRAM_HOME/bin/
./startssh.sh >> /tmp/sshlogin.tmp

echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $WriteSql/$connfilename
  while read sshlogin 
   do
    HOST_IP=`echo $sshlogin | awk -F[,] '{print $1}' | awk -F['='] '{print $2}'| awk '{print $1}'`
    Errflag=`echo $sshlogin | awk '{print $2}' | grep "ERROR"`
    if [ "X"$Errflag = "X" ]; then
IS_LOGIN=1
PS_NUM=`echo $sshlogin | awk '{print $2}' | awk -F[','] '{print $1}' `
UPTIME=`echo $sshlogin |awk -F[','] '{print $2}'`
HOSTID=`echo $sshlogin | awk -F[','] '{print $3}'`
    else
     IS_LOGIN=0
PS_NUM=0
UPTIME=""
HOSTID=0
    fi
    CHKMACHINE=$_hostname
  sql="INSERT INTO TAB_SSH_LOGIN(CHECK_START_TIME,CHECK_FREQUENCY,HOST_IP,IS_LOGIN,PS_NUM,UPTIME,CHECK_MACHINE,HOST_ID) values('$check_start_time',$fre_ssh,'$HOST_IP',$IS_LOGIN,$PS_NUM,'$UPTIME','$CHKMACHINE',$HOSTID);"
   echo $sql >> $WriteSql/$connfilename

   done < /tmp/sshlogin.tmp

rm /tmp/sshlogin.tmp
mv $WriteSql/$connfilename $_OutputSqlPath
}


main()
{
while true
do
 current=$(date +%H:%M:%S)
 min=`echo $current | awk -F[':'] '{print $2}'`
 sec=`echo $current | awk -F[':'] '{print $3}'`
let cursec=10#$min%$fre_ssh*60+10#$sec
let slptime=$fre_ssh*60-10#$cursec
# echo $slptime
 sleep $slptime
 CreateSql
done

}

main
