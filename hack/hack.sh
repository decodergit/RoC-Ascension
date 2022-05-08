#!/bin/sh

rm -rf output-dir
#apktool d -o output-dir com.innogames.riseofcultures.apk
#python3 makeDebuggable.py xml ./output-dir/AndroidManifest.xml ./output-dir/AndroidManifest.xml
#apktool b -o com.innogames.riseofcultures_debuggable.apk output-dir
#keytool -genkey -v -keystore resign.keystore -alias "InnoGames GmbH" -keyalg RSA -keysize 2048 -validity 10000
#jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore resign.keystore com.innogames.riseofcultures_debuggable.apk alias_name

# Нужен zipalign из android-sdk-build-tools
#python3 makeDebuggable.py apk com.innogames.riseofcultures.apk com.innogames.riseofcultures.debuggable.apk resign.keystore "InnoGames GmbH"


Native heap dump not available. To enable, run these commands (requires root):
# adb shell stop
# adb shell setprop libc.debug.malloc.options backtrace
# adb shell start


adb connect 192.168.1.69
adb root
adb -s 192.168.1.69:5555 shell am dumpheap -n com.innogames.riseofcultures data/local/tmp/roc_1.dump
adb pull /data/local/tmp/roc_1.dump
/opt/android-sdk/platform-tools/hprof-conv ./1/roc_1.dump ./1/roc_1.hprof


#java -jar ./android-keystore-password-recover/build/akpr.jar -m 3 -k ./BNDLTOOL.RSA -d ./words_000.txt
