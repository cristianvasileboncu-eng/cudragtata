#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")" || exit 1
touch date/oprit_manual
[ -f date/paznic.pid ] && kill "$(cat date/paznic.pid)" 2>/dev/null
[ -f date/server.pid ] && kill "$(cat date/server.pid)" 2>/dev/null
termux-wake-unlock 2>/dev/null
echo "Oprit. (Publicarea automată pornește din nou doar când apeși butonul sau rulezi porneste.sh)"
