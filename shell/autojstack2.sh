#!/bin/bash
# file:autojstack2.sh
# 检查本地日志,如果发现指定字符,自动抓取堆栈
# 参数1 进程名字

cat /dev/null > /tmp/autojstack.log
proc=$1
declare -i count=1
limitCount=0
busyCount=0
h=0
while true
do
    pid=`ps -ef | grep $proc | grep -v 'grep'|grep -v 'autojstack' | awk '{print $2}'`
    h=`date +%Y%m%d_%H`
    echo "grep limit /data/log/LOG_$h.log | wc -l"
    limitCount=`grep limit /data/log/LOG_$h.log | wc -l`
    busyCount=`grep busy /data/log/LOG_$h.log | wc -l`
    echo "limit="$limitCount
    echo "busy="$busyCount
    if (($limitCount > 0 | $busyCount > 0 ))
    then
        t=`date +%Y%m%d_%H%M%S`
        echo `jstack $pid > /tmp/jstack_$t.stack`
        echo "jstack $pid > /tmp/jstack_$t.stack OK"
        count=$count+1
        if(($count > 5))
        then
            exit 0
        fi
        echo `cat /dev/null > /data/log/LOG_$h.log`
    fi
    sleep 5s
done