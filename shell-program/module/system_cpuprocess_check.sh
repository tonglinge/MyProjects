#!/bin/sh
#set -x
. ../cfg/command.conf
. ../cfg/host.conf

_hostname=`hostname`
_osname=`uname`
WriteSql=$WORKING
_OutputSqlPath=$SQL_FOLDER

writesql()
{
  filename=$1
  hostid=$HOST_ID
  checkstarttime=$2" "$3
  checkfre=$fre_cpuprocess" min"
  topno=$4
  processcmd=$5
  pid=$6
  user=$7
  pcpu=$8
  cputime=$9
  if [ ! -f $filename ];then
    echo "alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'; " > $filename
  fi
sql="insert into tab_cpu_process(HOST_ID,CHECK_START_TIME,CHECK_FREQUENCY,TOP_NO,PROCESS_CMD,PRO_PID,PRO_USER,PCPU,CPU_TIME) values($hostid,'$checkstarttime','$checkfre',$topno,'$processcmd',$pid,'$user',$pcpu,'$cputime');"
 echo $sql >> $filename
}

CreateSql()
{
  check_start_time=$(date +%Y-%m-%d" "%H:%M":00")
  cpuprocessfilename="CPUPROCESS_"$_hostname"_"`date +%Y%m%d%H%M%S`".sql"
let top=1

  case $_osname in
  Linux)
    eval $RHEL_CPUPROCESS > /tmp/cpuprocess.tmp
  ;;
  HP-UX)
   eval $HPUX_CPUPROCESS > /tmp/cpuprocess.tmp
   ;;
  AIX)
   eval $AIX_CPUPROCESS > /tmp/cpuprocess.tmp   
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
     _pcpu=`echo $line | awk '{print $1}'`
     _cputime=`echo $line | awk '{print $2}'`
writesql $WriteSql/$cpuprocessfilename $check_start_time $top $_pcmd $_pid $_user $_pcpu $_cputime
let top=$top+1
    done < /tmp/cpuprocess.tmp
rm /tmp/cpuprocess.tmp
mv  $WriteSql/$cpuprocessfilename   $_OutputSqlPath
}


#main()
#{
#while true
#do
# current=$(date +%H:%M:%S)
# min=`echo $current | awk -F[':'] '{print $2}'`
# sec=`echo $current | awk -F[':'] '{print $3}'`
#let cursec=10#$min%$fre_cpuprocess*60+10#$sec
#let slptime=$fre_memprocess*60-10#$cursec
# echo $slptime
# sleep $slptime
# CreateSql
#done
#}

#main
CreateSql
