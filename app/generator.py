# -*- coding: utf-8 -*-
"""Alege un scenariu nou (fără duplicate), îl randează și îl salvează în istoric."""
import datetime
import os
import shutil
import threading

from . import baza
from .randare import Randare
from .scenarii import construieste
from .setari import VIDEO, config, log

_blocare = threading.Lock()   # un singur video se generează odată


def genereaza(categorie, slot=None, zi=None, progres=lambda p, m: None):
    if not _blocare.acquire(blocking=False):
        raise RuntimeError("Se generează deja un video. Așteaptă să termine.")
    try:
        cfg = config()
        comp, teme = baza.componente_recente(30)
        sc = construieste(categorie, baza.exista_fp, comp, teme)
        zi = zi or baza.azi()
        nume = f"{zi}_{'s%d' % slot if slot is not None else 'manual'}_{categorie}_{sc['fingerprint']}.mp4"
        cale = os.path.join(VIDEO, nume)
        log(f"Generez: {sc['titlu']} ({categorie}, {sc['fingerprint']})")
        t0 = datetime.datetime.now()
        if sc.get("stil") == "v2":
            from .randare_v2 import RandareV2 as R
        else:
            R = Randare
        dur, voce = R(cfg).randeaza(sc, cale, progres)
        sec = (datetime.datetime.now() - t0).total_seconds()
        vid = baza.adauga_video(sc, cale, dur, voce, slot, zi)
        log(f"Video #{vid} gata: {nume} ({dur:.1f}s, voce: {voce}, {sec:.0f}s de lucru)")
        galerie = os.path.expanduser(cfg.get("copie_in_galerie", ""))
        if galerie and os.path.isdir(os.path.dirname(galerie.rstrip("/"))):
            try:
                os.makedirs(galerie, exist_ok=True)
                shutil.copy2(cale, os.path.join(galerie, nume))
            except Exception as e:
                log(f"Nu am putut copia în galerie: {e}", "WARN")
        return vid
    finally:
        _blocare.release()
