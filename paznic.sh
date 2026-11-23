#!/data/data/com.termux/files/usr/bin/bash
# Ține serverul pornit: dacă se oprește din eroare, îl repornește după 30 s.
cd "$(dirname "$0")" || exit 1
echo $$ > date/paznic.pid
while true; do
  python -m app.server >> date/server.log 2>&1
  [ -f date/oprit_manual ] && break
  sleep 30
done
