#!/data/data/com.termux/files/usr/bin/sh
# Rulat de Termux:Boot după repornirea telefonului.
termux-wake-lock
cd ~/cudragtata-autovideo || exit 1
[ -f date/oprit_manual ] && exit 0
nohup bash paznic.sh > /dev/null 2>&1 &
