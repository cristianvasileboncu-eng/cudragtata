# -*- coding: utf-8 -*-
"""Comenzi din terminal:

  python -m app.cli demo [poveste|sfat|joc]   – generează un video de test
  python -m app.cli verifica                  – verifică instalarea
  python -m app.cli conturi                   – arată canalele din Buffer
  python -m app.cli zi                        – o rulare zilnică completă (pentru GitHub)
  python -m app.cli auto                      – rulează publicarea automată (fără interfață)
  python -m app.cli scenarii                  – arată 3 scenarii exemplu (fără video)
"""
import json
import shutil
import subprocess
import sys

from .setari import config, log, secrete


def verifica():
    ok = True
    for exe in ("ffmpeg", "ffprobe"):
        p = shutil.which(exe)
        print(f"{'✔' if p else '✘'} {exe}: {p or 'LIPSEȘTE – rulează: pkg install ffmpeg'}")
        ok &= bool(p)
    try:
        import PIL
        print(f"✔ Pillow {PIL.__version__}")
    except ImportError:
        print("✘ Pillow lipsește – rulează: pkg install python-pillow")
        ok = False
    try:
        import edge_tts  # noqa
        print("✔ edge-tts instalat (voce naturală, cere internet)")
    except ImportError:
        print("• edge-tts nu e instalat (se folosește espeak sau fără voce)")
    e = shutil.which("espeak-ng") or shutil.which("espeak")
    print(f"{'✔' if e else '•'} espeak: {e or 'nu e instalat (opțional)'}")
    enc = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
    print(f"{'✔' if ' libx264 ' in enc else '•'} encoder H.264 (libx264): {'da' if ' libx264 ' in enc else 'nu, folosesc alternativă'}")
    s = secrete()
    print(f"{'✔' if s.get('BUFFER_API_KEY') else '•'} Buffer: {'configurat' if s.get('BUFFER_API_KEY') else 'neconfigurat (încă nu e nevoie)'}")
    print(f"{'✔' if s.get('CLOUDINARY_CLOUD_NAME') else '•'} Cloudinary: {'configurat' if s.get('CLOUDINARY_CLOUD_NAME') else 'neconfigurat (încă nu e nevoie)'}")
    print(f"Mod publicare: {'REAL' if config()['publicare']['publicare_reala'] else 'SIMULARE (nu se postează nimic)'}")
    return ok


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "ajutor"
    if cmd == "verifica":
        sys.exit(0 if verifica() else 1)
    elif cmd == "demo":
        from .generator import genereaza
        from . import baza
        cat = argv[2] if len(argv) > 2 else "poveste"
        ultim = [-1]

        def progres(p, m):
            if int(p) // 10 != ultim[0]:
                ultim[0] = int(p) // 10
                print(f"  {int(p):3d}%  {m}", flush=True)
        vid = genereaza(cat, progres=progres)
        v = baza.video(vid)
        print(f"\nGATA! Video salvat în:\n  {v['fisier']}\nDurată: {v['durata']:.1f} s, voce: {v['voce']}")
    elif cmd == "scenarii":
        from .scenarii import construieste
        for cat in ("poveste", "sfat", "joc"):
            sc = construieste(cat, lambda fp: False)
            print(f"\n=== {cat.upper()}: {sc['titlu']} ===")
            for s in sc["scene"]:
                print(" -", s["text"])
    elif cmd == "conturi":
        from .publicare import Buffer
        b = Buffer()
        for c in b.canale(reimprospatare=True):
            print(f"{c['service']:10s} {c.get('displayName') or c.get('name')}  id={c['id']}")
    elif cmd == "zi":
        from .automat import Automat
        from . import baza
        n = baza.marcheaza_intrerupte()
        if n:
            log(f"{n} postări rămase „în curs” de la o rulare întreruptă → verifică în Buffer.", "WARN")
        a = Automat()
        for _ in range(30):
            if not a.un_pas():
                break
        rez = baza.video_zi(baza.azi())
        log(f"Rulare terminată: {len(rez)} materiale pentru {baza.azi()}.")
        for v in rez:
            for p in baza.postari_video(v["id"]):
                print(f"  #{v['id']} {v['titlu']} → {p['platforma']}: {p['status']} {p['programat_la'] or ''} {p['mesaj'] or ''}")
        if any(p["status"] == "eroare" for v in rez for p in baza.postari_video(v["id"])):
            sys.exit(2)
    elif cmd == "auto":
        from .automat import Automat
        Automat().ruleaza_blocant()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
