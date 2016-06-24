#!/bin/sh
getuptime()
{
 systemUptime=`uptime | awk -F[','] '{print $1}' | awk '{print $NF}' `
 case  $systemUptime in
    day|days)
 systemUptime=`uptime | awk -F[','] '{print $1" "$2}'  | awk '{print $3" "$4" "$5}' | awk -F[':'] '{if ($2 != "") {print $1" hours "$2" mins"} else {print $1" mins" } }'`
       ;;
    min)
       systemUptime=`uptime | awk -F[','] '{print $1}' | awk '{print $3$4}'`
       ;;
    *)
       systemUptime=`uptime | awk -F[','] '{print $1}' | awk '{print $3$4}' |  awk -F[':'] '{print $1" hours "$2" mins"}' `
       ;;
  esac
 echo $systemUptime
}

getprocess()
{
 process=` ps -fu $1 | grep -v grep | wc -l`
  echo $process
}

gethostid()
{
 hostid=` cat /home/tibco/shell-program/cfg/host.conf | grep "HOST_ID" | awk -F['='] '{print $2}' `
 echo $hostid
}
process=`getprocess $1 `
uptimes=`getuptime`
hostid=`gethostid`


echo $process","$uptimes","$hostid
