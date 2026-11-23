# -*- coding: utf-8 -*-
"""Voce românească gratuită.

1. edge-tts (vocile Microsoft ro-RO-EmilNeural / ro-RO-AlinaNeural) – sună natural,
   are nevoie de internet. ATENȚIE: nu e un serviciu oficial; poate înceta oricând.
2. espeak-ng – merge fără internet, dar sună robotic.
3. fără voce – doar subtitrări (durata se calculează după lungimea textului).
"""
import asyncio
import json
import os
import shutil
import subprocess
import time

from .setari import log


def durata(cale):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "json", cale], capture_output=True, text=True)
    try:
        return float(json.loads(out.stdout)["format"]["duration"])
    except Exception:
        return 0.0


def _edge(text, cale_mp3, voce, viteza, ton="+0Hz"):
    import edge_tts  # noqa

    async def run():
        c = edge_tts.Communicate(text, voce, rate=viteza, pitch=ton)
        await asyncio.wait_for(c.save(cale_mp3), timeout=60)

    asyncio.run(run())
    return os.path.exists(cale_mp3) and os.path.getsize(cale_mp3) > 1000


def _espeak(text, cale_wav, inaltime=45):
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    if not exe:
        return False
    subprocess.run([exe, "-v", "ro", "-s", "150", "-p", str(inaltime), "-w", cale_wav, text],
                   check=True, capture_output=True, timeout=60)
    return os.path.exists(cale_wav) and os.path.getsize(cale_wav) > 1000


def _liniste(cale_wav, secunde):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "lavfi", "-i",
                    "anullsrc=r=44100:cl=stereo", "-t", f"{secunde:.2f}", cale_wav], check=True)


def _normalizeaza(src, dst):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", src, "-ar", "44100", "-ac", "2", dst], check=True)


class Voce:
    def __init__(self, cfg):
        self.cfg = cfg.get("voce", {})
        self.motor_folosit = None
        self._edge_ok = self.cfg.get("motor", "auto") in ("auto", "edge")
        self._espeak_ok = self.cfg.get("motor", "auto") in ("auto", "espeak")
        self.reusite_edge = 0

    VORBITORI = {
        # vorbitor: (voce edge, viteză, ton, înălțime espeak)
        "tata": ("ro-RO-EmilNeural", "+4%", "+0Hz", 40),
        "copil": ("ro-RO-AlinaNeural", "+8%", "+45Hz", 80),
        "narator": ("ro-RO-EmilNeural", "-4%", "-2Hz", 35),
    }

    def genereaza(self, text, cale_wav, voce=None, vorbitor=None):
        """Creează cale_wav (44.1 kHz stereo). Întoarce durata în secunde."""
        tmp = cale_wav + ".src"
        viteza, ton, inalt = self.cfg.get("viteza", "+0%"), "+0Hz", 45
        if vorbitor:
            v = self.cfg.get("vorbitori", {}).get(vorbitor) or self.VORBITORI.get(vorbitor)
            if v:
                voce, viteza, ton, inalt = v
        if self._edge_ok:
            mp3 = tmp + ".mp3"
            nume_voce = voce or self.cfg.get("voce_edge", "ro-RO-EmilNeural")
            # încercăm de mai multe ori: serviciul gratuit mai „sughite” uneori
            variante = [(viteza, ton)] * 3 + [("+0%", "+0Hz")] * 2
            ultima = None
            for k, (vit, tn) in enumerate(variante):
                try:
                    time.sleep(0.4 if k == 0 else 2.0 * k)
                    if _edge(text, mp3, nume_voce, vit, tn):
                        _normalizeaza(mp3, cale_wav)
                        os.remove(mp3)
                        self.motor_folosit = "edge-tts"
                        self.reusite_edge += 1
                        return durata(cale_wav)
                except Exception as e:
                    ultima = e
            if self.reusite_edge:
                # nu amestecăm vocea naturală cu cea robotică în același video
                raise RuntimeError(f"Vocea naturală nu a răspuns după 5 încercări ({ultima}). "
                                   "Video-ul se reface mai târziu.")
            log(f"edge-tts nu merge ({type(ultima).__name__}: {ultima}). Folosesc vocea de rezervă.", "WARN")
            self._edge_ok = False
        if self._espeak_ok:
            try:
                w = tmp + ".wav"
                if _espeak(text, w, inalt):
                    _normalizeaza(w, cale_wav)
                    os.remove(w)
                    self.motor_folosit = self.motor_folosit or "espeak"
                    return durata(cale_wav)
            except Exception as e:
                log(f"espeak nu merge ({e}).", "WARN")
                self._espeak_ok = False
        sec = max(1.5, len(text) / 14.0)
        _liniste(cale_wav, sec)
        self.motor_folosit = self.motor_folosit or "fără voce"
        return sec
