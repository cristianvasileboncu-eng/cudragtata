#!/data/data/com.termux/files/usr/bin/bash
# Instalare „Cu drag, tata – Auto Video Farm” în Termux (Android ARM64)
cd "$(dirname "$0")" || exit 1
echo "== 1/5 Actualizez Termux (poate dura câteva minute) =="
pkg update -y && pkg upgrade -y -o Dpkg::Options::="--force-confnew"
echo "== 2/5 Instalez Python, FFmpeg, Pillow și espeak =="
pkg install -y python ffmpeg python-pillow espeak || { echo "EROARE la pkg install. Trimite o captură de ecran."; exit 1; }
echo "== 3/5 Instalez vocea naturală (edge-tts) =="
export AIOHTTP_NO_EXTENSIONS=1 FROZENLIST_NO_EXTENSIONS=1 MULTIDICT_NO_EXTENSIONS=1 YARL_NO_EXTENSIONS=1 PROPCACHE_NO_EXTENSIONS=1
pip install edge-tts || echo "ATENȚIE: edge-tts nu s-a instalat. Programul merge, dar cu vocea espeak (robotică)."
echo "== 4/5 Pregătesc pornirea automată după restart (Termux:Boot) =="
mkdir -p ~/.termux/boot
cp boot/porneste-cudragtata.sh ~/.termux/boot/
chmod +x ~/.termux/boot/porneste-cudragtata.sh porneste.sh opreste.sh demo.sh paznic.sh
[ -f secrete.env ] || cp secrete.env.exemplu secrete.env
echo "== 5/5 Verific instalarea =="
python -m app.cli verifica
echo
echo "GATA. Următorul pas: bash demo.sh"
