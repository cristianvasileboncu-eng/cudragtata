# -*- coding: utf-8 -*-
"""Căi, setări, secrete și jurnal."""
import datetime
import json
import os
import threading

RADACINA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = os.path.join(RADACINA, "date")
VIDEO = os.path.join(RADACINA, "video")
TEMP = os.path.join(DATE, "temp")
ASSETS = os.path.join(RADACINA, "assets")
FONT_BOLD = os.path.join(ASSETS, "fonturi", "DejaVuSans-Bold.ttf")
FONT = os.path.join(ASSETS, "fonturi", "DejaVuSans.ttf")
JURNAL = os.path.join(DATE, "jurnal.log")
CONFIG = os.path.join(RADACINA, "config.json")
SECRETE = os.path.join(RADACINA, "secrete.env")
STARE = os.path.join(DATE, "stare.json")

for _d in (DATE, VIDEO, TEMP):
    os.makedirs(_d, exist_ok=True)

_lock = threading.Lock()


def config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def secrete():
    """Citește secrete.env (CHEIE=valoare). Nu se afișează nicăieri."""
    rez = {}
    for k in ("BUFFER_API_KEY", "CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET"):
        if os.environ.get(k):
            rez[k] = os.environ[k].strip()
    if os.path.exists(SECRETE):
        with open(SECRETE, encoding="utf-8") as f:
            for linie in f:
                linie = linie.strip()
                if not linie or linie.startswith("#") or "=" not in linie:
                    continue
                k, v = linie.split("=", 1)
                v = v.strip().strip('"').strip("'")
                if v and not rez.get(k.strip()):
                    rez[k.strip()] = v
    return rez


def stare():
    try:
        with open(STARE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def salveaza_stare(**kw):
    with _lock:
        s = stare()
        s.update(kw)
        tmp = STARE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=1)
        os.replace(tmp, STARE)


def log(mesaj, nivel="INFO"):
    linie = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} [{nivel}] {mesaj}"
    print(linie, flush=True)
    with _lock:
        try:
            if os.path.exists(JURNAL) and os.path.getsize(JURNAL) > 2_000_000:
                os.replace(JURNAL, JURNAL + ".vechi")
            with open(JURNAL, "a", encoding="utf-8") as f:
                f.write(linie + "\n")
        except Exception:
            pass


def ultimele_linii(n=40):
    try:
        with open(JURNAL, encoding="utf-8") as f:
            return f.readlines()[-n:]
    except Exception:
        return []
