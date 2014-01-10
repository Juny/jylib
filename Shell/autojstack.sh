#!/bin/bash
# file:autojstack.sh
# 当线程数超过给定数量时,自动抓取堆栈
# 参数1 进程名字
# 参数2 最大线程数

proc=$1
maxThreadCount=$2
declare -i count=1
threadCount=0
 
while true
do
    sleep 5s
    pid=`ps -ef | grep $proc | grep -v 'grep'|grep -v 'autojstack' | awk '{print $2}'`
    threadCount=`ps -Tfp $pid| wc -l`
    if (($threadCount >= $maxThreadCount))
    then
        echo `jstack $pid>/tmp/"jstack_"$proc"_"$count`
        echo "jstack_"$proc"_"$count" threadCount:"$threadCount" OK"
        count=$count+1
        if(($count > 3))
        then
            exit 0
        fi
    fi
done