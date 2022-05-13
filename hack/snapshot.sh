#!/bin/sh

((i=0))
while : ;
do
  read -p "Сделать снимок [y/n]" answer
  if [ "$answer" = "n" ];
  then
    break 
  fi
  if [ "$answer" = "y" ];
  then
    echo $i > index
    APPNAME=riseofcultures
    #APPNAME=nano
    APPPID=`sudo ps -A | grep ${APPNAME} | awk '{print $1}'`
    echo "${APPNAME} PID is ${APPPID}"
    sudo gdb -p ${APPPID} -q -x snapshot.py -ex="set confirm off" -ex="set pagination off" -ex quit
    ((i=i+1))
  fi
done
