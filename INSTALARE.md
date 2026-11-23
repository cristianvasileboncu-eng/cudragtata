# Cu drag, tata – Auto Video Farm
## Ghid de instalare pe Infinix NOTE 40 Pro (Android 14), fără calculator

Lucrăm în ordine. **Nu treci la partea următoare până nu merge cea de acum.**

---

## PARTEA A – Primul video demonstrativ

### Pasul 1. Instalează Termux și Termux:Boot (gratuite)
1. În Chrome, deschide **f-droid.org** și instalează aplicația **F-Droid**.
2. Din F-Droid, instalează **Termux** și **Termux:Boot**.
   - Amândouă trebuie să vină din același loc (F-Droid). Nu amesteca cu Google Play.
3. Deschide **Termux:Boot** o singură dată, apoi închide-l (așa se activează).

### Pasul 2. Pune programul în telefon
1. Descarcă `cudragtata-autovideo.zip` (ajunge în **Descărcări / Download**).
2. Deschide **Termux** și scrie (apasă Enter după fiecare rând):
```
termux-setup-storage
```
   Apasă **Permite** când te întreabă telefonul.
```
pkg install -y unzip
cp ~/storage/downloads/cudragtata-autovideo.zip ~
cd ~ && unzip -o cudragtata-autovideo.zip
cd cudragtata-autovideo
```

### Pasul 3. Instalează (o singură dată, 5–15 minute)
```
bash instaleaza.sh
```
Dacă te întreabă ceva cu `[Y/n]`, scrie `y` și Enter.
La final trebuie să vezi bife ✔ la **ffmpeg** și **Pillow**.

### Pasul 4. Generează video-ul demonstrativ
```
bash demo.sh
```
După 1–3 minute scrie **GATA!**. Video-ul îl găsești în **Galerie → Movies → CuDragTata**.
Alte variante: `bash demo.sh sfat` sau `bash demo.sh joc`.

---

## VERSIUNEA 2 – Emoție + reclame (după ce ai instalat)
```
bash descarca_imagini.sh
bash demo.sh emotie
bash demo.sh reclama
```
- `descarca_imagini.sh` ia imaginile de pe cudragtata.ro și le pune ca fundal.
- Clipurile tale (de ex. din Google Flow) le poți pune în `assets/clipuri/` (MP4). Dacă numele începe ca o imagine (ex. `joc-garaj_1.mp4`), se folosesc la scenele potrivite.
- Imaginile tale (ChatGPT / Gemini): citește `PROMPTURI_IMAGINI.md`, pune imaginile în `povesti/<id>/1.jpg, 2.jpg…`.
- Scenariile noi sunt în `app/continut_v2.py` (12 povești emoționante + 10 reclame pentru jocuri).

---

## PARTEA B – Interfața cu butoane

```
bash porneste.sh
```
Se deschide în Chrome adresa `http://127.0.0.1:8765` cu butoanele:
**Generează · Previzualizează · Publicare automată · Istoric · Oprește**.

- Interfața merge doar pe telefonul tău (nu e publică pe internet).
- Ca să oprești tot: în Termux scrie `bash opreste.sh`.

---

## PARTEA C – Imaginile tale de pe cudragtata.ro

Acum programul folosește imagini **provizorii**. Pune-le pe ale tale (PNG cu fundal transparent):

| Ce | Unde pui fișierul |
|---|---|
| Logo | `assets/logo.png` (îl înlocuiești pe cel existent) |
| Personajul tata | `assets/personaje/tata/` (șterge `tata_provizoriu.png`) |
| Personajul copil | `assets/personaje/copil/` (șterge `copil_provizoriu.png`) |
| Animale (opțional) | `assets/animale/leul.png`, `pisica.png` etc. (numele ca în joc) |
| Muzică (opțional) | `assets/muzica/*.mp3` |

Muzică: pune **doar melodii a căror licență permite folosirea pe rețele sociale**.
Melodiile „la modă” din TikTok/Instagram nu pot fi puse automat; ele se adaugă doar manual, din aplicație.

---

## PARTEA D – Publicarea (DOAR după ce partea A merge)

Programul pornește în **modul SIMULARE**: generează tot și scrie în Istoric, dar **nu postează nimic**.

1. Cont **Buffer** gratuit (buffer.com). Conectează maximum 3 canale:
   - TikTok: cont **Business**
   - Instagram: cont **Creator** sau **Business**
   - YouTube
2. Cheia API Buffer: `publish.buffer.com/settings/api` → creează cheia.
3. Cont **Cloudinary** gratuit (fără card). Din **Settings → API Keys** iei: Cloud name, API Key, API Secret.
4. Scrie cheile în fișierul de secrete:
```
nano secrete.env
```
   Salvezi cu **Ctrl+O**, Enter, apoi ieși cu **Ctrl+X**.
5. Verifică conturile:
```
python -m app.cli conturi
```
6. Abia când totul arată bine: în `config.json` schimbi `"publicare_reala": false` în `true`.

### Ce se publică pe zi (se poate schimba în `config.json`)
- **3 video-uri**: poveste, sfat, joc. Merg pe TikTok, Instagram Reels și YouTube Shorts (YouTube primește maximum 2 pe zi).
- **3 poze**: gândul zilei, sfatul zilei, jocul zilei. Merg pe Instagram și TikTok (YouTube nu primește poze).
- Orele sunt în `config.json` → `zilnic`. Fiecare postare primește o descriere cu invitație spre cudragtata.ro și hashtaguri.
- `"poze": {"ca_video_cu_muzica": true}` transformă pozele în clipuri de 12 secunde cu melodie (doar dacă ai pus muzică).

### Cum evită programul postările duble
- Fiecare combinație de conținut are o „amprentă”. Nu se generează niciodată de două ori.
- Fiecare postare se notează în Istoric **înainte** de trimitere. Dacă telefonul se oprește exact atunci, postarea apare ca **„verifică”** și **nu** se retrimite automat. Te uiți tu în Buffer.
- După 3 zile, fișierele se șterg din Cloudinary, ca să rămâi în planul gratuit.

---

## PARTEA E – Ca să meargă singur, zilnic (Infinix / XOS)

Infinix închide agresiv aplicațiile din fundal. Fă toate setările de mai jos (denumirile pot diferi puțin):
1. **Setări → Baterie** → gestionarea bateriei pentru aplicații → **Termux** → permite rularea în fundal (fără restricții). La fel pentru **Termux:Boot**.
2. **Setări → Aplicații → Pornire automată** → activează **Termux** și **Termux:Boot**.
3. În lista de aplicații recente, ține apăsat pe Termux → **Blochează** (lacătul).
4. Opțiuni dezvoltator (Setări → Despre telefon → apasă de 7 ori pe „Număr versiune”) → activează **„Dezactivează restricțiile proceselor copil”**, dacă există pe telefonul tău.
5. Ține telefonul la încărcat și pe Wi-Fi, mai ales dimineața, când se generează.

După o repornire, Termux:Boot pornește singur serverul. Dacă publicarea automată era pornită, continuă de unde a rămas.

---

## Probleme frecvente
- **Vocea e robotică**: vocea naturală (edge-tts) cere internet și nu e un serviciu oficial; când nu merge, programul folosește espeak.
- **„Se generează deja”**: așteaptă să termine sau apasă **Oprește**.
- Orice eroare: deschide **Jurnal tehnic** în interfață și trimite-mi o captură.
