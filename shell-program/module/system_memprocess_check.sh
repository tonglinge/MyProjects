#!/bin/sh
#set -x
. ../cfg/command.conf
. ../cfg/host.conf

_hostname=`hostname`
_osname=`uname`
writesql=$WORKING
_OutputSqlPath=$SQL_FOLDER

writesql()
{
  filename=$1
  hostid=$HOST_ID
  checkstarttime=$2" "$3
  checkfre=$fre_memprocess" min"
  topno=$4
  processcmd=$5
  pid=$6
  user=$7
  pcpu=$8
  vsz=$9
  if [ ! -f $filename ];then
    echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $filename
  fi
sql="insert into tab_mem_process(HOST_ID,CHECK_START_TIME,CHECK_FREQUENCY,TOP_NO,PROCESS_CMD,PRO_PID,PRO_USER,PCPU,VSZ) values($hostid,'$checkstarttime','$checkfre',$topno,'$processcmd',$pid,'$user',$pcpu,$vsz);"
 echo $sql >> $filename
}

CreateSql()
{
  check_start_time=$(date +%Y-%m-%d" "%H:%M":00")
  memprocessfilename="MEMPROCESS_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"
let top=1

  case $_osname in
  Linux)
    eval $RHEL_MEMPROCESS >> /tmp/memprocess.tmp
#    echo "---------"$check_start_time"-------------" >> /tmp/memprocess_`date +%Y%m%d`.tmp
#    cat /tmp/memprocess.tmp >> /tmp/memprocess_`date +%Y%m%d`.tmp
#    echo "" >> /tmp/memprocess_`date +%Y%m%d`.tmp
  ;;
  HP-UX)
   eval $HPUX_MEMPROCESS > /tmp/memprocess.tmp
   ;;
  AIX)
   eval $AIX_MEMPROCESS > /tmp/memprocess.tmp   
  ;;
  *)
    exit
  ;;
  esac


    while read line
    do
    let  _icmd=5 
    let _col=`echo $line | awk '{print NF}'`
    _pcmd=""
     while (($_col>=$_icmd))
     do
        _pcmd=$_pcmd`echo $line | awk '{print $'$_icmd}''`
     let _icmd=$_icmd+1 
    done
     _pid=`echo $line | awk '{print $4}'`
     _user=`echo $line | awk '{print $3}'`
     _pcpu=`echo $line | awk '{print $2}'`
     _vsz=`echo $line | awk '{print $1}'`
writesql $writesql/$memprocessfilename $check_start_time $top $_pcmd $_pid $_user $_pcpu $_vsz
let top=$top+1
    done < /tmp/memprocess.tmp
rm /tmp/memprocess.tmp
mv $writesql/$memprocessfilename $_OutputSqlPath
}


#main()
#{
#while true
#do
# current=$(date +%H:%M:%S)
# min=`echo $current | awk -F[':'] '{print $2}'`
# sec=`echo $current | awk -F[':'] '{print $3}'`
#let cursec=10#$min%$fre_memprocess*60+10#$sec
#let slptime=$fre_memprocess*60-10#$cursec
# echo $slptime
# sleep $slptime
# CreateSql
#done
#}

#main
CreateSql
