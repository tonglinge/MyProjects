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
  connfilename="EMSCONN_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"
  
$TIB_HOME/ems/bin/tibemsadmin -server tcp://$ems_servip:$ems_servport -ignore -user $ems_user -password $ems_pwd -script $PROGRAM_HOME/cfg/emsconnection.cfg | awk '$2 ~ /[0-9]\.[0-9]\.[0-9]/' | awk '{ if(NF>10) print $0}'  > /tmp/emsconn.tmp

v_connstat=`cat /tmp/emsconn.tmp | wc -l`
if [ $v_connstat != "0" ]; then
#cat /tmp/emsconn.tmp0 | awk '$2 ~ /[0-9]\.[0-9]\.[0-9]/' | awk '{ if(NF>10) print $0}' > /tmp/emsconn.tmp
echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $WriteSql/$connfilename
  while read emsconn
   do
    domain=$DOMAIN
    ems_user=`echo $emsconn | awk '{print $9}' `
    ems_ip=`echo $emsconn | awk '{print $8}' `
    ems_host=` echo $emsconn | awk '{print $7}' `
    ems_uptime=` echo $emsconn | awk '{print $NF}' `
    ems_connid=` echo $emsconn | awk '{print $4}' `
 
   sql="INSERT INTO TAB_EMS_CONNECTIONS(CHECK_START_TIME,CHECK_FREQUENCY,DOMAIN_NAME,EMS_USER,IP_ADDRESS,HOST_NAME,UPTIME,HOST_ID,CONNECT_ID) VALUES('$check_start_time','$fre_ems min','$domain','$ems_user','$ems_ip','$ems_host','$ems_uptime',$HOST_ID,$ems_connid);"
   echo $sql >> $WriteSql/$connfilename

   done < /tmp/emsconn.tmp
mv $WriteSql/$connfilename $_OutputSqlPath
fi
rm /tmp/emsconn.tmp
}


#main
CreateSql
