#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")" || exit 1
mkdir -p date; rm -f date/oprit_manual
termux-wake-lock 2>/dev/null
if [ -f date/paznic.pid ] && kill -0 "$(cat date/paznic.pid)" 2>/dev/null; then
  echo "Serverul rulează deja."
else
  nohup bash paznic.sh > /dev/null 2>&1 &
  sleep 3
fi
termux-open-url http://127.0.0.1:8765 2>/dev/null || echo "Deschide în Chrome: http://127.0.0.1:8765"
