# -*- coding: utf-8 -*-
"""Lucrul zilnic, fără intervenția ta:
generează video-urile și pozele zilei, le programează în Buffer la orele
stabilite, curăță fișierele vechi. Poate fi oprit oricând și reia singur
de unde a rămas (după repornire, totul e salvat în istoric)."""
import datetime
import fcntl
import glob
import os
import shutil
import threading
import time
import traceback

from . import baza
from .setari import DATE, TEMP, VIDEO, config, log, salveaza_stare, stare

LACAT = os.path.join(DATE, "automat.lacat")


def _ora(s, zi):
    h, m = map(int, s.split(":"))
    return datetime.datetime.combine(zi, datetime.time(h, m))


class Automat:
    def __init__(self):
        self.stop = threading.Event()
        self.fir = None
        self._lacat = None
        self.esecuri = {}

    # ------------------------------------------------------------ pornire/oprire
    def porneste_fir(self):
        if self.fir and self.fir.is_alive():
            return False
        self.stop.clear()
        self.fir = threading.Thread(target=self._bucla_sigura, daemon=True)
        self.fir.start()
        return True

    def opreste(self):
        self.stop.set()
        from .randare import OPRIRE
        OPRIRE.set()

    def activ(self):
        return bool(self.fir and self.fir.is_alive())

    def ruleaza_blocant(self):
        salveaza_stare(automat=True)
        try:
            self._bucla_sigura()
        except KeyboardInterrupt:
            log("Oprit din tastatură.")

    # ------------------------------------------------------------ bucla
    def _bucla_sigura(self):
        self._lacat = open(LACAT, "w")
        try:
            fcntl.flock(self._lacat, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            log("Publicarea automată rulează deja în alt proces. Nu pornesc a doua oară.", "WARN")
            return
        n = baza.marcheaza_intrerupte()
        if n:
            log(f"{n} postări întrerupte la ultima oprire → marcate „verifică în Buffer”.", "WARN")
        shutil.rmtree(TEMP, ignore_errors=True)
        os.makedirs(TEMP, exist_ok=True)
        log("Publicarea automată a pornit.")
        try:
            while not self.stop.is_set():
                try:
                    lucrat = self.un_pas()
                except Exception as e:
                    log(f"Eroare în ciclu: {e}\n{traceback.format_exc()[-800:]}", "ERROR")
                    lucrat = False
                salveaza_stare(ultima_verificare=baza.acum())
                if not lucrat:
                    self.stop.wait(300)   # verifică la 5 minute
        finally:
            fcntl.flock(self._lacat, fcntl.LOCK_UN)
            self._lacat.close()
            log("Publicarea automată s-a oprit.")

    def un_pas(self):
        """Face un singur lucru și întoarce True dacă a mai rămas de lucru imediat."""
        cfg = config()
        z = cfg["zilnic"]
        acum = datetime.datetime.now()
        azi = acum.date()
        if acum < _ora(z.get("ora_generare", "07:00"), azi):
            return False
        existente = {v["slot"]: v for v in baza.video_zi(azi.isoformat())}
        # 1) generează ce lipsește azi (un element pe pas)
        plan = [(i, c) for i, c in enumerate(z.get("categorii", []))] + \
               [(10 + i, c) for i, c in enumerate(z.get("poze", []))]
        for slot, cat in plan:
            if slot in existente:
                continue
            cheie = (azi, slot)
            if self.esecuri.get(cheie, 0) >= 3:
                continue
            try:
                salveaza_stare(lucru=f"Generez {cat} (slot {slot})")
                if cat.startswith("poza_"):
                    from .poze import genereaza_poza
                    genereaza_poza(cat, slot, azi.isoformat())
                else:
                    from .generator import genereaza
                    genereaza(cat, slot, azi.isoformat(),
                              progres=lambda p, m: salveaza_stare(lucru=f"{cat}: {m} ({int(p)}%)"))
            except Exception as e:
                self.esecuri[cheie] = self.esecuri.get(cheie, 0) + 1
                log(f"Nu am putut genera {cat}: {e}", "ERROR")
            finally:
                salveaza_stare(lucru="")
            return not self.stop.is_set()
        # 2) programează în Buffer
        from .publicare import publica_element, curata_cloudinary
        ore_v = z.get("ore_publicare", [])
        ore_p = z.get("ore_poze", [])
        for slot, v in sorted(existente.items()):
            if not (v["fisier"] and os.path.exists(v["fisier"])):
                stari = [p["status"] for p in baza.postari_video(v["id"])]
                if not any(st in ("programat", "in_curs", "verifica") for st in stari):
                    log(f"Fișierul pentru #{v['id']} lipsește și nu e publicat – îl refac.", "WARN")
                    baza.sterge_video(v["id"])
                    return True
        decalaj = 0
        for slot, v in sorted(existente.items()):
            ore = ore_p if slot >= 10 else ore_v
            k = slot - 10 if slot >= 10 else slot
            if k >= len(ore):
                continue
            cand = _ora(ore[k], azi)
            minim = acum + datetime.timedelta(minutes=15 + decalaj)
            if cand < minim:
                if acum.hour >= 23:
                    continue   # prea târziu pentru azi
                cand = minim
                decalaj += 25   # ora a trecut: le eșalonăm, nu toate odată
            if not (v["fisier"] and os.path.exists(v["fisier"])):
                continue   # deja programat într-o rulare anterioară
            try:
                publica_element(v["id"], cand)
            except Exception as e:
                log(f"Publicare #{v['id']}: {e}", "ERROR")
        # 3) curățenie o dată pe zi
        s = stare()
        if s.get("ultima_curatenie") != azi.isoformat():
            self.curatenie(cfg)
            if cfg["publicare"].get("publicare_reala"):
                try:
                    curata_cloudinary()
                except Exception as e:
                    log(f"Curățenie Cloudinary: {e}", "WARN")
            salveaza_stare(ultima_curatenie=azi.isoformat())
        return False

    @staticmethod
    def curatenie(cfg):
        zile = cfg.get("pastreaza_video_local_zile", 14)
        limita = time.time() - zile * 86400
        n = 0
        for f in glob.glob(os.path.join(VIDEO, "*")):
            if os.path.getmtime(f) < limita:
                os.remove(f)
                n += 1
        if n:
            log(f"Am șters {n} fișiere mai vechi de {zile} zile (istoricul rămâne).")
