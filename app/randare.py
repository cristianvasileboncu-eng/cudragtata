# -*- coding: utf-8 -*-
"""Transformă un scenariu în video vertical MP4 (Pillow + FFmpeg)."""
import glob
import math
import os
import random
import shutil
import subprocess
import threading

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import continut as C
from .provizorii import inima, asigura
from .setari import ASSETS, FONT, FONT_BOLD, TEMP, log
from .voce import Voce, durata

NAVY = (31, 42, 68)
GOLD = (224, 165, 38)
ALB = (255, 255, 255)

PALETE = [
    ((255, 246, 228), (255, 214, 160)),   # crem – auriu
    ((226, 242, 255), (170, 210, 245)),   # cer
    ((232, 250, 238), (175, 225, 195)),   # mentă
    ((244, 236, 255), (205, 185, 240)),   # lavandă
    ((255, 238, 232), (250, 190, 170)),   # piersică
]

OPRIRE = threading.Event()   # setat de butonul „Oprește”


class Oprit(Exception):
    pass


_fonturi = {}


def font(m, bold=True):
    k = (m, bold)
    if k not in _fonturi:
        _fonturi[k] = ImageFont.truetype(FONT_BOLD if bold else FONT, m)
    return _fonturi[k]


def rupe(text, f, latime):
    cuv, linii, cur = text.split(), [], ""
    for c in cuv:
        t = (cur + " " + c).strip()
        if f.getlength(t) <= latime:
            cur = t
        else:
            if cur:
                linii.append(cur)
            cur = c
    if cur:
        linii.append(cur)
    return linii


def text_centrat(d, cy, linii, f, fill, spatiu=1.18):
    h = f.size * spatiu
    y = cy - h * len(linii) / 2
    for l in linii:
        w = f.getlength(l)
        d.text(((1080 - w) / 2, y), l, font=f, fill=fill)
        y += h


class Randare:
    def __init__(self, cfg):
        self.cfg = cfg
        v = cfg.get("video", {})
        self.W, self.H = v.get("latime", 1080), v.get("inaltime", 1920)
        self.fps = v.get("fps", 30)
        self.min_s = v.get("durata_min", 20)
        self.max_s = v.get("durata_max", 40)
        self.enc = self._encoder()
        asigura()
        self.logo = Image.open(os.path.join(ASSETS, "logo.png")).convert("RGBA")

    # ------------------------------------------------------------ utilitare
    def _encoder(self):
        out = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
        if " libx264 " in out:
            return ["-c:v", "libx264", "-preset", self.cfg.get("video", {}).get("preset", "veryfast"),
                    "-crf", "23", "-pix_fmt", "yuv420p"]
        if "h264_mediacodec" in out:
            return ["-c:v", "h264_mediacodec", "-b:v", "6M", "-pix_fmt", "yuv420p"]
        return ["-c:v", "mpeg4", "-q:v", "4", "-pix_fmt", "yuv420p"]

    def _ffmpeg(self, args):
        if OPRIRE.is_set():
            raise Oprit()
        p = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-hide_banner", "-v", "error"] + args,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            try:
                _, err = p.communicate(timeout=1)
                break
            except subprocess.TimeoutExpired:
                if OPRIRE.is_set():
                    p.kill()
                    raise Oprit()
        if p.returncode != 0:
            raise RuntimeError("FFmpeg a dat eroare: " + (err or "")[-800:])

    def _poza_personaj(self, rol, rng):
        fis = sorted(glob.glob(os.path.join(ASSETS, "personaje", rol, "*.png")))
        return rng.choice(fis) if fis else None

    # ------------------------------------------------------------ straturi
    def fundal(self, paleta, rng, cale):
        W, H = int(self.W * 1.1), int(self.H * 1.1)
        sus, jos = paleta
        im = Image.new("RGB", (W, H))
        d = ImageDraw.Draw(im)
        for y in range(H):
            t = y / H
            d.line([(0, y), (W, y)], fill=tuple(int(sus[i] + (jos[i] - sus[i]) * t) for i in range(3)))
        strat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ds = ImageDraw.Draw(strat)
        for _ in range(9):
            r = rng.randint(80, 260)
            x, y = rng.randint(0, W), rng.randint(0, H)
            ds.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, rng.randint(40, 90)))
        for _ in range(10):
            inima(ds, rng.randint(40, W - 40), rng.randint(40, H - 40), rng.randint(30, 70), (255, 255, 255, 110))
        strat = strat.filter(ImageFilter.GaussianBlur(3))
        im = Image.alpha_composite(im.convert("RGBA"), strat)
        im.convert("RGB").save(cale)

    def scena_statica(self, sc, scena, cale, rng, titlu_video):
        """Stratul transparent cu logo, eticheta și desenul scenei."""
        W, H = self.W, self.H
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        viz = scena["vizual"]
        tip = viz["tip"]
        # logo sus (sub zona de interfață a aplicațiilor)
        lw = 520
        lg = self.logo.resize((lw, int(self.logo.height * lw / self.logo.width)))
        if tip != "logo_mare":
            im.alpha_composite(lg, ((W - lw) // 2, 130))
        # eticheta (titlul scenei)
        et = scena.get("eticheta") or ""
        if et and tip != "logo_mare":
            f = font(56)
            w = f.getlength(et)
            x0, y0 = (W - w) / 2 - 40, 330
            d.rounded_rectangle([x0, y0, x0 + w + 80, y0 + 100], 50, fill=NAVY)
            d.text((x0 + 40, y0 + 18), et, font=f, fill=ALB)

        if tip == "text_mare":
            cx, cy, r = W // 2, 800, 230
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ALB, outline=GOLD, width=14)
            f = font(260 if len(viz["mare"]) <= 2 else 150)
            w = f.getlength(viz["mare"])
            d.text((cx - w / 2, cy - f.size * 0.62), viz["mare"], font=f, fill=NAVY)

        elif tip in ("forme",):
            self._forme(d, viz)

        elif tip == "mere":
            self._mere(d, viz)

        elif tip == "raspuns":
            poza = os.path.join(ASSETS, "animale", viz.get("animal", "") + ".png")
            if viz.get("animal") and os.path.exists(poza):
                a = Image.open(poza).convert("RGBA")
                a.thumbnail((640, 640))
                im.alpha_composite(a, ((W - a.width) // 2, 1050 - a.height))
                cy = 1180
            else:
                cy = 800
            f = font(130)
            linii = rupe(viz["mare"], f, 900)
            hh = len(linii) * 155 + 60
            d.rounded_rectangle([90, cy - hh / 2, W - 90, cy + hh / 2], 60, fill=ALB, outline=GOLD, width=12)
            text_centrat(d, cy, linii, f, NAVY)

        elif tip == "lista":
            f = font(200)
            d.text(((W - f.getlength(viz["mare"])) / 2, 470), viz["mare"], font=f, fill=GOLD,
                   stroke_width=6, stroke_fill=NAVY)
            f2 = font(90)
            y = 760
            for c in viz["cuvinte"]:
                w = f2.getlength(c)
                d.rounded_rectangle([(W - w) / 2 - 50, y - 10, (W + w) / 2 + 50, y + 120], 40, fill=ALB)
                d.text(((W - w) / 2, y), c, font=f2, fill=NAVY)
                y += 165

        elif tip == "logo_mare":
            lw2 = 900
            lg2 = self.logo.resize((lw2, int(self.logo.height * lw2 / self.logo.width)))
            im.alpha_composite(lg2, ((W - lw2) // 2, 640))
            f = font(54, bold=False)
            text_centrat(d, 1080, rupe(titlu_video, f, 900), f, NAVY)
        im.save(cale)

    def _forme(self, d, viz):
        rng = random.Random(viz["seed"])
        culoare = C.CULORI[viz["culoare"]]
        alte = [c for k, c in C.CULORI.items() if k != viz["culoare"]]
        n, nd = viz["n"], viz["distractori"]
        # grilă 4 x 4 în zona 480..1330
        celule = [(c, r) for r in range(4) for c in range(4)]
        rng.shuffle(celule)
        x0, y0, cw, ch = 120, 470, 210, 215
        d.rounded_rectangle([70, 440, 1010, 1340], 50, fill=(255, 255, 255, 210))
        obiecte = [(culoare, True)] * n + [(rng.choice(alte), False) for _ in range(nd)]
        nr = 0
        for (col, tinta), (c, r) in zip(obiecte, celule):
            cx = x0 + c * cw + cw / 2 + rng.randint(-15, 15)
            cy = y0 + r * ch + ch / 2 + rng.randint(-12, 12)
            s = 150
            self._forma(d, viz["forma"], cx, cy, s, col)
            if tinta and viz.get("numerotat"):
                nr += 1
                f = font(64)
                t = str(nr)
                d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=NAVY)
                d.text((cx - f.getlength(t) / 2, cy - 38), t, font=f, fill=ALB)

    def _forma(self, d, forma, cx, cy, s, col):
        r = s / 2
        if forma == "cerc":
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        elif forma == "patrat":
            d.rounded_rectangle([cx - r * 0.85, cy - r * 0.85, cx + r * 0.85, cy + r * 0.85], 18, fill=col)
        elif forma == "triunghi":
            d.polygon([(cx, cy - r), (cx + r, cy + r * 0.8), (cx - r, cy + r * 0.8)], fill=col)
        elif forma == "inima":
            inima(d, cx, cy, s * 0.95, col)
        else:  # stea
            pts = []
            for i in range(10):
                a = -math.pi / 2 + i * math.pi / 5
                rr = r if i % 2 == 0 else r * 0.45
                pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
            d.polygon(pts, fill=col)

    def _mere(self, d, viz):
        a, b, op = viz["a"], viz["b"], viz["op"]
        d.rounded_rectangle([70, 440, 1010, 1340], 50, fill=(255, 255, 255, 210))

        def mar(cx, cy, s, sters=False):
            col = (220, 50, 60) if op == "+" else (60, 140, 230)
            if op == "+":
                d.ellipse([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], fill=col)
                d.line([(cx, cy - s / 2), (cx + 8, cy - s / 2 - 28)], fill=(110, 70, 30), width=8)
                d.ellipse([cx + 8, cy - s / 2 - 30, cx + 44, cy - s / 2 - 10], fill=(70, 170, 80))
            else:
                d.ellipse([cx - s / 2.4, cy - s / 2, cx + s / 2.4, cy + s / 2], fill=col)
                d.line([(cx, cy + s / 2), (cx + 10, cy + s / 2 + 60)], fill=NAVY, width=4)
            if sters:
                d.line([(cx - s / 2, cy - s / 2), (cx + s / 2, cy + s / 2)], fill=NAVY, width=12)
                d.line([(cx + s / 2, cy - s / 2), (cx - s / 2, cy + s / 2)], fill=NAVY, width=12)

        def rand(nr, y, start_sters=None):
            s = 120
            per = min(nr, 5)
            tot = per * s + (per - 1) * 30
            for i in range(nr):
                rr, cc = divmod(i, 5)
                cx = (1080 - tot) / 2 + cc * (s + 30) + s / 2
                mar(cx, y + rr * 170, s, sters=start_sters is not None and i >= start_sters)

        f = font(120)
        if op == "+":
            rand(a, 560)
            d.text((540 - f.getlength("+") / 2, 760), "+", font=f, fill=NAVY)
            rand(b, 990)
        else:
            rand(a, 620, start_sters=a - b if "rezultat" in viz else None)
            d.text((540 - f.getlength(f"− {b}") / 2, 1000), f"− {b}", font=f, fill=NAVY)
        if "rezultat" in viz:
            t = f"= {viz['rezultat']}"
            f2 = font(150)
            w = f2.getlength(t)
            d.rounded_rectangle([540 - w / 2 - 50, 1170, 540 + w / 2 + 50, 1330], 50, fill=GOLD)
            d.text((540 - w / 2, 1172), t, font=f2, fill=NAVY)

    def subtitrare(self, text, cale):
        im = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        f = font(58)
        linii = rupe(text, f, 900)
        h = len(linii) * 70 + 50
        cy = 1500
        d.rounded_rectangle([60, cy - h / 2, self.W - 60, cy + h / 2], 36, fill=(255, 255, 255, 235),
                            outline=NAVY, width=5)
        text_centrat(d, cy, linii, f, NAVY, spatiu=1.2)
        im.save(cale)

    def cifra_mare(self, t, cale):
        im = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy, r = 540, 820, 260
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD, outline=NAVY, width=16)
        f = font(330)
        d.text((cx - f.getlength(t) / 2, cy - 210), t, font=f, fill=NAVY)
        im.save(cale)

    # ------------------------------------------------------------ bucăți text
    @staticmethod
    def bucati_subtitrare(text, max_car=64):
        """Împarte textul în bucăți scurte (max 2 rânduri pe ecran)."""
        propozitii, cur = [], ""
        for cuv in text.split():
            t = (cur + " " + cuv).strip()
            if len(t) > max_car and cur:
                propozitii.append(cur)
                cur = cuv
            else:
                cur = t
            if cur.endswith((".", "!", "?", "”")) and len(cur) > 25:
                propozitii.append(cur)
                cur = ""
        if cur:
            propozitii.append(cur)
        return propozitii

    # ------------------------------------------------------------ principal
    def randeaza(self, sc, iesire, progres=lambda p, m: None):
        OPRIRE.clear()
        rng = random.Random(sc["fingerprint"])
        lucru = os.path.join(TEMP, sc["fingerprint"])
        shutil.rmtree(lucru, ignore_errors=True)
        os.makedirs(lucru)
        try:
            return self._randeaza(sc, iesire, progres, rng, lucru)
        finally:
            shutil.rmtree(lucru, ignore_errors=True)

    def _randeaza(self, sc, iesire, progres, rng, lucru):
        voce = Voce(self.cfg)
        scene = sc["scene"]
        voce_cat = self.cfg.get("voce", {}).get("voci_pe_categorie", {}).get(sc["categorie"])
        # 1) voce pentru fiecare scenă
        audio, dur_a = [], []
        for i, s in enumerate(scene):
            progres(5 + 30 * i / len(scene), f"Voce {i + 1}/{len(scene)}")
            w = os.path.join(lucru, f"v{i}.wav")
            dur_a.append(voce.genereaza(s["text"], w, voce_cat))
            audio.append(w)
        # 2) durate și limite 20–40 s
        pauza = 0.45
        durate = [max(s["minim"], a + pauza) for s, a in zip(scene, dur_a)]
        total = sum(durate)
        if total > self.max_s:
            reducere = total - self.max_s + 0.5
            factor = min(1.25, sum(dur_a) / max(1.0, sum(dur_a) - reducere))
            log(f"Video prea lung ({total:.1f}s). Accelerez vocea x{factor:.2f}.", "WARN")
            for i, w in enumerate(audio):
                w2 = w + ".rapid.wav"
                subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", w, "-filter:a", f"atempo={factor:.3f}", w2], check=True)
                os.replace(w2, w)
                dur_a[i] = durata(w)
            durate = [max(s["minim"], a + pauza) for s, a in zip(scene, dur_a)]
            total = sum(durate)
            if total > self.max_s:
                raise RuntimeError(f"Scenariul e prea lung ({total:.1f}s) chiar și accelerat.")
        if total < self.min_s:
            durate[-1] += self.min_s - total + 0.3
        # 3) imagini
        paleta = rng.choice(PALETE)
        bg = os.path.join(lucru, "fundal.png")
        self.fundal(paleta, rng, bg)
        tata = self._poza_personaj("tata", rng)
        copil = self._poza_personaj("copil", rng)
        segmente = []
        for i, s in enumerate(scene):
            if OPRIRE.is_set():
                raise Oprit()
            progres(35 + 55 * i / len(scene), f"Scena {i + 1}/{len(scene)}")
            st = os.path.join(lucru, f"s{i}.png")
            self.scena_statica(sc, s, st, rng, sc["titlu"])
            seg = os.path.join(lucru, f"seg{i}.mp4")
            self._segment(i, s, durate[i], dur_a[i], audio[i], bg, st, tata, copil, lucru, seg)
            segmente.append(seg)
        # 4) lipire + muzică opțională
        progres(92, "Lipesc scenele")
        lista = os.path.join(lucru, "lista.txt")
        with open(lista, "w") as f:
            for sgm in segmente:
                f.write(f"file '{sgm}'\n")
        brut = os.path.join(lucru, "brut.mp4")
        self._ffmpeg(["-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", brut])
        muzica = sorted(glob.glob(os.path.join(ASSETS, "muzica", "*.mp3")))
        tmp_out = iesire + ".tmp.mp4"
        if muzica and self.cfg.get("video", {}).get("muzica", True):
            m = rng.choice(muzica)
            vol = self.cfg.get("video", {}).get("volum_muzica", 0.10)
            self._ffmpeg(["-i", brut, "-stream_loop", "-1", "-i", m, "-filter_complex",
                          f"[1:a]volume={vol}[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
                          "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                          "-movflags", "+faststart", tmp_out])
        else:
            self._ffmpeg(["-i", brut, "-c", "copy", "-movflags", "+faststart", tmp_out])
        os.replace(tmp_out, iesire)
        progres(100, "Gata")
        return durata(iesire), voce.motor_folosit

    def _segment(self, i, s, D, dur_voce, wav, bg, st, tata, copil, lucru, out):
        W, H, fps = self.W, self.H, self.fps
        viz = s["vizual"]
        intrari = ["-loop", "1", "-framerate", str(fps), "-i", bg,
                   "-loop", "1", "-framerate", str(fps), "-i", st]
        filtre = []
        mx, my = int(W * 0.05), int(H * 0.05)
        filtre.append(f"[0:v]crop={W}:{H}:x='{mx}+{mx}*sin(2*PI*t/9)':y='{my}+{my}*sin(2*PI*t/11+1)',setsar=1[b0]")
        filtre.append("[b0][1:v]overlay=0:0[b1]")
        ultim, idx = "b1", 2
        # personaje (cu mișcare simplă)
        pers = []
        if viz["tip"] == "personaje":
            if tata:
                pers.append((tata, 720, 130, -1))
            if copil:
                pers.append((copil, 520, 590, 1))
        elif viz["tip"] in ("text_mare", "numaratoare") and copil:
            pers.append((copil, 380, 40, -1))
        for k, (img, inalt, x0, sens) in enumerate(pers):
            intrari += ["-loop", "1", "-framerate", str(fps), "-i", img]
            faza = 0.7 * k
            y0 = 1330
            filtre.append(f"[{idx}:v]scale=-1:{inalt}[p{k}]")
            x = (f"if(lt(t,0.45),{x0}+{sens}*700*(1-t/0.45),{x0})+14*sin(2*PI*(t+{faza})/2.6)")
            y = f"{y0}-h+10*sin(2*PI*(t+{faza})*0.9)"
            filtre.append(f"[{ultim}][p{k}]overlay=x='{x}':y='{y}'[c{k}]")
            ultim, idx = f"c{k}", idx + 1
        # numărătoare 3-2-1
        if viz["tip"] == "numaratoare":
            pas = min(1.0, (D - 0.2) / 3)
            for k, t in enumerate(("3", "2", "1")):
                p = os.path.join(lucru, f"n{i}_{k}.png")
                self.cifra_mare(t, p)
                intrari += ["-loop", "1", "-framerate", str(fps), "-i", p]
                a, b = 0.1 + k * pas, 0.1 + (k + 1) * pas
                filtre.append(f"[{ultim}][{idx}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[n{k}]")
                ultim, idx = f"n{k}", idx + 1
        # subtitrări sincronizate (proporțional cu lungimea textului)
        bucati = self.bucati_subtitrare(s["text"])
        total_car = sum(len(b) for b in bucati) or 1
        t0 = 0.1
        for k, b in enumerate(bucati):
            p = os.path.join(lucru, f"t{i}_{k}.png")
            self.subtitrare(b, p)
            intrari += ["-loop", "1", "-framerate", str(fps), "-i", p]
            durb = max(0.8, dur_voce * len(b) / total_car)
            t1 = D if k == len(bucati) - 1 else t0 + durb
            filtre.append(f"[{ultim}][{idx}:v]overlay=0:0:enable='between(t,{t0:.2f},{t1:.2f})'[t{k}]")
            ultim, idx, t0 = f"t{k}", idx + 1, t1
        filtre.append(f"[{ultim}]fade=t=in:st=0:d=0.25,fade=t=out:st={D - 0.25:.2f}:d=0.25,format=yuv420p[v]")
        intrari += ["-i", wav]
        args = intrari + ["-filter_complex", ";".join(filtre), "-map", "[v]", "-map", f"{idx}:a",
                          "-af", "apad", "-t", f"{D:.2f}", "-r", str(fps)] + self.enc + \
               ["-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2", out]
        self._ffmpeg(args)
