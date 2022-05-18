#!/bin/bash

rm -f asm.log
APPNAME=riseofcultures
APPPID=`sudo ps -A | grep ${APPNAME} | awk '{print $1}'`
echo "${APPNAME} PID is ${APPPID}"
for ((n=0;n<10;n++))
do
    echo "---------------------------------------------------" >> asm.log
    message="Запуск $n ($(date))"
    echo $message
    echo $message >> asm.log
    echo "---------------------------------------------------" >> asm.log
    sudo gdb -q -p ${APPPID} < test.gdb >> asm.log 2>&1
    echo "---------------------------------------------------" >> asm.log
    echo "" >> asm.log
    sleep 0.1
done

