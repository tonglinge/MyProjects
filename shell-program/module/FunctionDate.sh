#!/bin/sh  
#output: "true" "fase"   
check_leap()   
{  
    Y=`expr substr $1 1 4`  
  
    r1=`expr $Y % 4`  
    r2=`expr $Y % 100`  
    r3=`expr $Y % 400`  
  
    if [ "$r1" = "0" -a "$r2" = "0" -o "$r3" = "0" ];then  
        FRUN="true"  
    else  
        FRUN="false"  
    fi  
    echo $FRUN  
}  
#-----------------------------------------------------------------  
 
# Get max day in the month
get_mon_days()  
{  
    Y=`expr substr $1 1 4`  
    M=`expr substr $1 5 2`  
  
    case "$M" in  
         01|03|05|07|08|10|12) days=31;;  
         04|06|09|11) days=30;;  
         02)  
        _tmpStr=`check_leap "$Y"`  #if is yunnian
        if [ "$_tmpStr" = "true" ] ; then  
            #yun nian
            days=29  
        else  
            days=28  
        fi  
        ;;  
         *)  
        days=0  
        ;;  
    esac  
    echo $days  
}  
#-----------------------------------------------------------------  
 
#Return Yesterday   
get_before_date()  
{  
    Y=`expr substr $1 1 4`  
    M=`expr substr $1 5 2`  
    D=`expr substr $1 7 2`  
 
       
    if [ "$D" -eq 01 ]  
    then  
        if [ "$M" -eq 01 ]  
        then              
            YY=`expr $Y - 1`  
            be_date="${YY}-12-31"  
        else            
            MM=`expr $M - 1`  
            MM=`printf "%02d" $MM`  
            dad=`get_mon_days "$Y$MM"`  
            be_date="$Y-$MM-$dad"  
        fi  
    else 
        DD=`expr $D - 1`  
        DD=`printf "%02d" $DD`  
        be_date="$Y-$M-$DD"  
    fi  
    echo $be_date  
}

#-----------------------------------------------------------------  
get_next_date()  
{  
    Y=`expr substr $1 1 4`  
    M=`expr substr $1 5 2`  
    D=`expr substr $1 7 2`  
  
    dad=`get_mon_days "$Y$M"`  #days Count in current month
  
    if [ "$D" = "$dad" ];then           
        if [ "$M$D" = "1231" ];then              
            YY=`expr $Y + 1`  
            next_date="${YY}-01-01"  
        else  
            MM=`expr $M + 1`  
            MM=`printf "%02d" $MM`  
            next_date="$Y-${MM}-01"  
        fi  
    else        
        DD=`expr $D + 1`  
        DD=`printf "%02d" $DD`  
        next_date="$Y-$M-$DD"  
    fi  
  
    echo $next_date  
}  
if [ $# = 0 ]; then
echo "need date argument ,format: yyyymmdd"
exit
else
splicstr=`expr substr $1 5 1`
if [ $splicstr = "-" ]; then
echo "Date argument Error,Format: yyyymmdd"
exit
else
get_before_date $1 
fi
fi
