#!/data/data/com.termux/files/usr/bin/bash
# Generează UN video demonstrativ, direct pe telefon.
cd "$(dirname "$0")" || exit 1
termux-wake-lock 2>/dev/null
python -m app.cli demo "${1:-poveste}"
termux-wake-unlock 2>/dev/null
