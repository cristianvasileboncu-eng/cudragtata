#!/data/data/com.termux/files/usr/bin/bash
# Descarcă imaginile de pe cudragtata.ro (site-ul tău) ca fundaluri pentru video-uri.
cd "$(dirname "$0")" || exit 1
mkdir -p assets/fundaluri
T="${TMPDIR:-$HOME}"
for n in familia-in-aventura joc-garaj eroii-pe-pajiste cat-familie cat-masinute cat-educative cat-ghicit joc-usi; do
  if curl -fsSL -m 60 -o "$T/$n.webp" "https://cudragtata.ro/imagini/$n.webp"; then
    ffmpeg -y -v error -i "$T/$n.webp" -q:v 2 "assets/fundaluri/$n.jpg" && echo "✔ $n" || echo "✘ $n (nu am putut converti)"
    rm -f "$T/$n.webp"
  else
    echo "✘ $n (nu s-a descărcat)"
  fi
done
echo "Gata. Imaginile sunt în assets/fundaluri"
