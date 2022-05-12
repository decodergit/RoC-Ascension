#!/bin/sh

APPNAME=riseofcultures
#APPNAME=nano
APPPID=`sudo ps -A | grep ${APPNAME} | awk '{print $1}'`
echo "${APPNAME} PID is ${APPPID}"
sudo gdb -p ${APPPID} -q -x first.py -ex="set confirm off" -ex="set pagination off" -ex quit
