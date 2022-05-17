#!/bin/bash

rm -f ./mem.dump

APPNAME=riseofcultures
APPPID=`sudo ps -A | grep ${APPNAME} | awk '{print $1}'`
echo "${APPNAME} PID is ${APPPID}"
sudo gdb -p ${APPPID} -ex="set confirm off" -ex="set pagination off" -q -x hack_gdb.py -ex quit

while : ;
do
  echo "Разверните окно игры и перезайдите в переговоры."
  read -p "Сделать снимок [y/n]" answer
  if [ "$answer" = "n" ];
  then
    break 
  fi
  if [ "$answer" = "y" ];
  then
    sudo gdb -p ${APPPID} -ex="set confirm off" -ex="set pagination off" -q -x hack_gdb.py -ex quit
  fi
done
