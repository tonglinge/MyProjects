#!/bin/sh
. ../cfg/host.conf


# declare variable 
HostName=`hostname`
WriteSql=$WORKING
OutputSqlPath=$SQL_FOLDER
Check_start_time=$(date +%Y-%m-%d" "%H:%M":00")
FileName="EMSPRODUCE_"HostName"_"`date +%Y%m%d%H%M%S`".sql"

# Get script File for EMSProducers
ScriptFile=$PROGRAM_HOME/cfg/emsproducer.cfg

# Load EMS_Producers Info  into file /tmp/emsproducers.tmp by temp script
$TIB_HOME/ems/bin/tibemsadmin -server tcp://$ems_servip:$ems_servport -ignore -user $ems_user -password $ems_pwd -script $ScriptFile | awk '$NF ~ /[Kb|MB]/' > /tmp/emsproducers.tmp

# begin create SQL file by /tmp/emsproducers.tmp
echo "ALTER SESSION SET NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS';" > $WriteSql/$FileName

while read emsp_info
do
EMSUSER=`echo $emsp_info | awk '{print $1}' `
EMSCONNID=`echo $emsp_info | awk '{print $2}' `
EMSDEST=`echo $emsp_info | awk '{if(NF==10) print $4;else print "" }' `
TotalMsg=`echo $emsp_info | awk '{print $(NF-5)}'`
TotalSize=`echo $emsp_info | awk '{if($(NF-3)=="MB") print $(NF-4)*1024;else print $(NF-4)}' `
RateMsg=`echo $emsp_info | awk '{print $(NF-2)}' `
RateSize=`echo $emsp_info | awk '{if($NF=="MB") print $(NF-1)*1024;else print $(NF-1)}' `
EMSTYPE=`echo $emsp_info | awk '{print $3}'`
Sql="INSERT INTO TAB_EMS_PRODUCERS(check_start_time, ems_user, ems_connid, ems_dest, total_msg, total_size, rate_msg, rate_size, ems_type, domain_name, host_id) values('$Check_start_time','$EMSUSER','$EMSCONNID','$EMSDEST',$TotalMsg,$TotalSize,$RateMsg,$RateSize,'$EMSTYPE','$DOMAIN',$HOST_ID);"
echo $Sql >> $WriteSql/$FileName
done < /tmp/emsproducers.tmp

mv $WriteSql/$FileName $OutputSqlPath
# Delete temp file
rm /tmp/emsproducers.tmp

