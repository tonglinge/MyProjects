#!/bin/sh
#set -x
. ../cfg/host.conf
scripts="system_cpu_check.sh system_net_check.sh system_disk_check.sh system_memory_check.sh system_ems_check.sh  system_ssh_check.sh system_downlog_check.sh"

if [ $# -eq 0 ]; then
  echo "need argument : start [scripts]| stop [scripts] | startall | stopall | check "
  exit
fi

getInstance()
{
   if [ $# -eq 0 ]; then
     echo ""
     exit     
   else
     case $1 in
       cpu)
          echo "system_cpu_check.sh"
          ;;
       net)
          echo "system_net_check.sh"
          ;;
       disk)
         echo "system_disk_check.sh"
         ;;
      memory)
         echo "system_memory_check.sh"
        ;;
      ems)  
        echo "system_ems_check.sh"
        ;;
      coredata)
       echo "system_core_check.sh"
        ;;
       ssh)
       echo "system_ssh_check.sh"
       ;;
       downlog)
       echo "system_downlog_check.sh"
       ;;
       *)
         echo ""
         ;;
      esac
  fi
}

startAll()
{
  cat ../cfg/module.cfg | grep -v "#" > /tmp/startmodule.tmp
  while read module
  do
   start $module
  done < /tmp/startmodule.tmp
 rm -rf /tmp/startmodule.tmp 
}

stopAll()
{
 cat ../cfg/module.cfg | grep -v "#" > /tmp/startmodule.tmp
  while read module
  do
   x=`getInstance $module`
    xstatus=`checkstatus $x`
    if [ $xstatus = "running" ]; then
     sid=`ps -ef | grep $PROGRAM_HOME/module/$x | grep -v grep | awk '{print $2}' `
     kid=` ps -ef | grep $sid | grep -v grep | awk '{ if ($3=='$sid' || $2=='$sid') print $2}' `
     kill $kid
     echo " $x stopped successful..."
    fi
  done < /tmp/startmodule.tmp

rm -rf /tmp/startmodule.tmp 
}

checkstatus()
{
  if [ $# -eq 0 ]; then
    for x in $scripts
      do
        ps -ef | grep $PROGRAM_HOME/module/$x | grep -v grep >/dev/null
        if [ $? = 0 ]; then
           echo $x " is running...."
         else
           echo  $x "is stopped..... "
        fi
     done
  else
    ps -ef | grep $1 | grep -v grep > /dev/null
    if [ $? = 0 ]; then
       echo "running"
    else
       echo  "stopped"
    fi 
  fi
}

start()
{
   script=` echo $1 | tr "[:upper:]" "[:lower:]" `
   instance=` getInstance $script`  
   if [ "x"$instance = "x" ]; then
      echo "Error argument:  start [cpu | net | disk | memory | ems | ssh | downlog] "
      exit
   else
   status=`checkstatus $instance` 
       #echo $status
   if [ $status = "running" ]; then
      echo  $script "monitor script start Failed! The Script is aready in running...."
   else
     allowRun=`cat $PROGRAM_HOME/cfg/module.cfg | grep -v "#" | grep $script`
     if [ "X"$allowRun = "X" ]; then
       echo " ERROR: this module ia not allowed to run on this Host! "
       exit
     else
       $PROGRAM_HOME/module/$instance & >/dev/null
       echo $script" monitor start successful ..."
     fi
  fi
  fi
}

stops()
{
  script=` echo $1  | tr "[:upper:]" "[:lower:]" `
  instance=`getInstance $script	`
  if [ "x"$instance = "x" ]; then
      echo "Error argument:  stop [cpu | net | disk | memory | memprocess | cpuprocess] "
      exit
  else
  status=` checkstatus $instance `
    if [ $status = "running" ]; then
        sid=`ps -ef | grep $instance | grep -v grep | awk '{print $2}' `
        pid=`ps -ef | grep $sid | grep -v grep | awk '{if ($3=='$sid' || $2=='$sid') print $2}' `
        kill $pid
        echo " $1 monitor stop successful.."
    else
       echo " $1 monitor doesn't running..."
       exit
    fi
  fi
}


  argume1=`echo $1 | tr "[:upper:]" "[:lower:]" `
  case $argume1 in
   startall)
         startAll
         ;;
   stopall)
         stopAll
         ;;
   check)
         checkstatus $2
         ;;
   start)
         if [ $# -ne 2 ]; then
          echo " argument Error!"
          echo " monitor.sh start [net|cpu|disk|memory|cpuprocess|memprocess|ems]"
          exit
         fi
         argume2=`echo $2 | tr "[:upper:]" "[:lower:]" `
         start $argume2
         ;;
   stop)
         argume2=`echo $2 | tr "[:upper:]" "[:lower:]" `
         stops $argume2
         ;;
   help)
         help
        ;;
   *)
        echo "need argument : start [scripts]| stop [scripts] | startall | stopall | check "
        exit
       ;;
  esac

