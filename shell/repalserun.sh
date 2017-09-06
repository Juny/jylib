#!/bin/sh
# file:repalserun.sh
# 替换run文件
for folder in `ls /service/faeserver/worker/appbean/`
do
  echo '/service/faeserver/worker/appbean/'$folder
  cp -f /home/gjy/run '/service/faeserver/worker/appbean/'$folder
done
exit 0