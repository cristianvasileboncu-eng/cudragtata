# -*- coding: utf-8 -*-
"""Randare v2 – stil dinamic pentru TikTok / Reels / Shorts.

- fundal: imaginile tale de pe cudragtata.ro (assets/fundaluri) sau clipuri
  proprii (assets/clipuri), cu zoom de impact la fiecare replică și mișcare lentă;
- hook mare în prima secundă;
- subtitrări mari, câte 2–3 cuvinte, centrate (stil TikTok);
- eticheta vorbitorului (TATA / COPILUL);
- final cu logo, site și slogan.
"""
import glob
import os
import random

from PIL import Image, ImageDraw, ImageFilter

from .provizorii import asigura
from .randare import GOLD, NAVY, ALB, PALETE, Oprit, OPRIRE, Randare, font, rupe
from .setari import ASSETS, log
from .voce import Voce

GALBEN = (255, 210, 63)
CULORI_VORBITOR = {"tata": (224, 165, 38), "copil": (90, 190, 255)}
NUME_VORBITOR = {"tata": "TATA", "copil": "COPILUL"}
FOCUS = [(0.5, 0.45), (0.3, 0.5), (0.7, 0.5), (0.5, 0.6), (0.4, 0.35), (0.6, 0.4)]


def imagine_fundal(cheie, rng):
    d = os.path.join(ASSETS, "fundaluri")
    fis = sorted(glob.glob(os.path.join(d, f"{cheie}.*")))
    if not fis:
        fis = sorted(f for f in glob.glob(os.path.join(d, "*")) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
    return rng.choice(fis) if fis else None


def imagine_poveste(poveste, index):
    """Imaginile tale pentru o poveste: povesti/<id>/1.jpg, 2.jpg ... (în ordine)."""
    from .setari import RADACINA
    d = os.path.join(RADACINA, "povesti", poveste or "")
    if not poveste or not os.path.isdir(d):
        return None
    fis = sorted((f for f in os.listdir(d) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))),
                 key=lambda f: (len(f), f))
    return os.path.join(d, fis[index % len(fis)]) if fis else None


def clip_fundal(cheie, rng):
    d = os.path.join(ASSETS, "clipuri")
    fis = sorted(glob.glob(os.path.join(d, f"{cheie}*.mp4"))) or sorted(glob.glob(os.path.join(d, "*.mp4")))
    return rng.choice(fis) if fis else None


class RandareV2(Randare):
    SCALA = 1.5   # imaginea de fundal e pregătită mai mare, pentru zoom fin

    def pregateste_fundal(self, sursa, cale, rng, intunecat=False):
        W, H = int(self.W * self.SCALA), int(self.H * self.SCALA)
        if sursa:
            im = Image.open(sursa).convert("RGB")
        else:   # fără imagini de pe site: degrade cu personajele provizorii
            tmp = cale + ".tmp.png"
            self.fundal(rng.choice(PALETE), rng, tmp)
            im = Image.open(tmp).convert("RGB")
            os.remove(tmp)
        # fundal estompat care umple tot ecranul
        r = max(W / im.width, H / im.height)
        bg = im.resize((int(im.width * r) + 1, int(im.height * r) + 1))
        bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
        bg = bg.filter(ImageFilter.GaussianBlur(30))
        bg = Image.blend(bg, Image.new("RGB", bg.size, (15, 20, 35)), 0.35)
        # imaginea clară, cât mai mare, în centru (zona 1620 x 1950)
        zw, zh = W, int(H * 0.68)
        r2 = max(zw / im.width, zh / im.height)
        fg = im.resize((int(im.width * r2) + 1, int(im.height * r2) + 1))
        fg = fg.crop(((fg.width - zw) // 2, (fg.height - zh) // 2, (fg.width - zw) // 2 + zw, (fg.height - zh) // 2 + zh))
        bg.paste(fg, (0, int(H * 0.16)))
        if not sursa:
            tata = self._poza_personaj("tata", rng)
            copil = self._poza_personaj("copil", rng)
            for p, x, h in ((tata, 0.18, 1100), (copil, 0.55, 800)):
                if p:
                    c = Image.open(p).convert("RGBA")
                    c = c.resize((int(c.width * h / c.height), h))
                    bg.paste(c, (int(W * x), int(H * 0.80) - h), c)
        if intunecat:
            bg = Image.blend(bg.filter(ImageFilter.GaussianBlur(12)), Image.new("RGB", bg.size, (12, 18, 32)), 0.55)
        bg.save(cale, quality=90)

    # ------------------------------------------------------------ straturi
    def strat_fix(self, scena, cale):
        """Umbre pentru lizibilitate + logo mic + eticheta vorbitorului + hook."""
        W, H = self.W, self.H
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        g = Image.new("L", (1, H))
        for y in range(H):
            a = 0
            if y < 520:
                a = int(150 * (1 - y / 520))
            elif y > 980:
                a = int(190 * min(1, (y - 980) / 600))
            g.putpixel((0, y), a)
        umbra = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        umbra.putalpha(g.resize((W, H)))
        im.alpha_composite(umbra)
        d = ImageDraw.Draw(im)
        viz = scena["vizual"]
        if viz["tip"] == "final_cta":
            lw = 860
            lg = self.logo.resize((lw, int(self.logo.height * lw / self.logo.width)))
            im.alpha_composite(lg, ((W - lw) // 2, 560))
            f = font(96)
            t = "cudragtata.ro"
            w = f.getlength(t)
            d.rounded_rectangle([(W - w) / 2 - 50, 900, (W + w) / 2 + 50, 1050], 75, fill=GOLD)
            d.text(((W - w) / 2, 918), t, font=f, fill=NAVY)
            fs = font(54)
            y = 1110
            for l in rupe(viz.get("slogan", ""), fs, 900):
                d.text(((W - fs.getlength(l)) / 2, y), l, font=fs, fill=ALB, stroke_width=4, stroke_fill=(0, 0, 0))
                y += 70
            im.save(cale)
            return
        # logo mic sus
        lw = 380
        lg = self.logo.resize((lw, int(self.logo.height * lw / self.logo.width)))
        im.alpha_composite(lg, ((W - lw) // 2, 140))
        # hook mare (prima replică)
        if scena.get("hook"):
            fh = font(92)
            y = 330
            for l in rupe(scena["hook"], fh, 960)[:3]:
                d.text(((W - fh.getlength(l)) / 2, y), l, font=fh, fill=GALBEN, stroke_width=9, stroke_fill=(0, 0, 0))
                y += 112
        # cine vorbește
        cine = scena.get("vorbitor")
        if cine in NUME_VORBITOR:
            f = font(46)
            t = NUME_VORBITOR[cine]
            w = f.getlength(t)
            x0, y0 = (W - w) / 2 - 30, 1125
            d.rounded_rectangle([x0, y0, x0 + w + 60, y0 + 72], 36, fill=CULORI_VORBITOR[cine])
            d.text((x0 + 30, y0 + 9), t, font=f, fill=NAVY)
        im.save(cale)

    def bucata_text(self, text, cale, culoare=ALB):
        im = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        f = font(88)
        linii = rupe(text, f, 960)
        y = 1300 - len(linii) * 108 / 2
        for l in linii:
            d.text(((self.W - f.getlength(l)) / 2, y), l, font=f, fill=culoare, stroke_width=10, stroke_fill=(0, 0, 0))
            y += 108
        im.save(cale)

    def text_intreg(self, text, cale, hook=False):
        im = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        marime = 104 if hook else 84
        f = font(marime)
        linii = rupe(text, f, 940)
        h = marime * 1.25
        y = (1080 if not hook else 960) - len(linii) * h / 2
        for l in linii:
            d.text(((self.W - f.getlength(l)) / 2, y), l, font=f, fill=GALBEN if hook else ALB,
                   stroke_width=10 if hook else 8, stroke_fill=(0, 0, 0))
            y += h
        im.save(cale)

    @staticmethod
    def grupuri_cuvinte(text, max_car=16):
        grupuri, cur = [], []
        for c in text.split():
            t = " ".join(cur + [c])
            if cur and (len(t) > max_car or len(cur) >= 3):
                grupuri.append(" ".join(cur))
                cur = [c]
            else:
                cur.append(c)
            if c.endswith((".", "!", "?", ",", "…", ":")) and len(" ".join(cur)) > 6:
                grupuri.append(" ".join(cur))
                cur = []
        if cur:
            grupuri.append(" ".join(cur))
        return grupuri

    # ------------------------------------------------------------ principal
    def _randeaza(self, sc, iesire, progres, rng, lucru):
        voce = Voce(self.cfg)
        scene = sc["scene"]
        self.fara_voce = bool(sc.get("fara_voce")) or self.cfg.get("voce", {}).get("motor") == "niciuna"
        audio, dur_a = [], []
        for i, s in enumerate(scene):
            progres(5 + 30 * i / len(scene), f"Voce {i + 1}/{len(scene)}")
            w = os.path.join(lucru, f"v{i}.wav")
            if self.fara_voce:
                sec = 0.9 + 0.36 * len(s["text"].split())   # timp de citit
                from .voce import _liniste
                _liniste(w, sec)
                dur_a.append(sec)
                voce.motor_folosit = "fără voce (text + muzică)"
            else:
                dur_a.append(voce.genereaza(s["text"], w, vorbitor=s.get("vorbitor", "narator")))
            audio.append(w)
        pauza = 0.25
        durate = [max(s["minim"], a + pauza) for s, a in zip(scene, dur_a)]
        total = sum(durate)
        if total > self.max_s:
            raise RuntimeError(f"Scenariul e prea lung ({total:.1f}s). Scurtează replicile din continut_v2.py.")
        if total < self.min_s:
            durate[-1] += self.min_s - total + 0.3
        segmente = []
        for i, s in enumerate(scene):
            if OPRIRE.is_set():
                raise Oprit()
            progres(35 + 55 * i / len(scene), f"Scena {i + 1}/{len(scene)}")
            seg = os.path.join(lucru, f"seg{i}.mp4")
            self._segment_v2(i, s, durate[i], dur_a[i], audio[i], rng, lucru, seg)
            segmente.append(seg)
        return self._lipeste(segmente, iesire, rng, lucru, progres, voce)

    def _lipeste(self, segmente, iesire, rng, lucru, progres, voce):
        from .voce import durata
        progres(92, "Lipesc scenele")
        lista = os.path.join(lucru, "lista.txt")
        with open(lista, "w") as f:
            for sgm in segmente:
                f.write(f"file '{sgm}'\n")
        brut = os.path.join(lucru, "brut.mp4")
        self._ffmpeg(["-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", brut])
        muzica = sorted(glob.glob(os.path.join(ASSETS, "muzica", "*.mp3")))
        tmp_out = iesire + ".tmp.mp4"
        if getattr(self, "fara_voce", False) and not muzica:
            log("Nu ai muzică în assets/muzica – video-ul text va fi fără sunet!", "WARN")
        if muzica and self.cfg.get("video", {}).get("muzica", True):
            vol = self.cfg.get("video", {}).get("volum_muzica", 0.10)
            if getattr(self, "fara_voce", False):
                vol = self.cfg.get("video", {}).get("volum_muzica_fara_voce", 0.9)
            from .voce import durata as _d
            dtot = _d(brut)
            self._ffmpeg(["-i", brut, "-stream_loop", "-1", "-i", rng.choice(muzica), "-filter_complex",
                          f"[1:a]volume={vol},afade=t=in:st=0:d=1,afade=t=out:st={max(0, dtot - 1.8):.2f}:d=1.8[m];"
                          f"[0:a][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]",
                          "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                          "-movflags", "+faststart", tmp_out])
        else:
            self._ffmpeg(["-i", brut, "-c", "copy", "-movflags", "+faststart", tmp_out])
        os.replace(tmp_out, iesire)
        progres(100, "Gata")
        return durata(iesire), voce.motor_folosit

    def _segment_v2(self, i, s, D, dur_voce, wav, rng, lucru, out):
        W, H, fps = self.W, self.H, self.fps
        viz = s["vizual"]
        final = viz["tip"] == "final_cta"
        clip = None if final else clip_fundal(viz.get("imagine", ""), rng)
        intrari, filtre = [], []
        if clip:
            intrari += ["-stream_loop", "-1", "-i", clip]
            filtre.append(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                          f"fps={fps},setsar=1[b0]")
        else:
            bg = os.path.join(lucru, f"bg{i}.jpg")
            sursa = imagine_poveste(viz.get("poveste"), viz.get("index", 0)) or \
                imagine_fundal(viz.get("imagine", ""), rng)
            self.pregateste_fundal(sursa, bg, rng, intunecat=final)
            fx, fy = FOCUS[viz.get("focus", i) % len(FOCUS)]
            n = max(1, int(D * fps))
            # zoom de impact în primele 0,3 s + apropiere lentă
            z = f"1.04+0.10*max(0,1-on/9)+{0.06 / n:.6f}*on"
            intrari += ["-loop", "1", "-framerate", str(fps), "-i", bg]
            filtre.append(f"[0:v]zoompan=z='{z}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d=1:"
                          f"s={W}x{H}:fps={fps},setsar=1[b0]")
        st = os.path.join(lucru, f"s{i}.png")
        self.strat_fix(s, st)
        intrari += ["-loop", "1", "-framerate", str(fps), "-i", st]
        filtre.append("[b0][1:v]overlay=0:0[b1]")
        ultim, idx = "b1", 2
        if not final and getattr(self, "fara_voce", False):
            p = os.path.join(lucru, f"t{i}.png")
            self.text_intreg(s["text"], p, hook=s.get("stil_text") == "hook")
            intrari += ["-loop", "1", "-framerate", str(fps), "-i", p]
            filtre.append(f"[{idx}:v]format=rgba,fade=t=in:st=0.15:d=0.6:alpha=1[tf]")
            filtre.append(f"[{ultim}][tf]overlay=0:0[tx]")
            ultim, idx = "tx", idx + 1
        elif not final:
            grupuri = self.grupuri_cuvinte(s["text"])
            total_car = sum(len(g) + 1 for g in grupuri) or 1
            t0 = 0.05
            for k, g in enumerate(grupuri):
                p = os.path.join(lucru, f"t{i}_{k}.png")
                self.bucata_text(g, p, GALBEN if k % 2 else ALB)
                intrari += ["-loop", "1", "-framerate", str(fps), "-i", p]
                t1 = D if k == len(grupuri) - 1 else t0 + max(0.35, dur_voce * (len(g) + 1) / total_car)
                filtre.append(f"[{ultim}][{idx}:v]overlay=0:0:enable='between(t,{t0:.2f},{t1:.2f})'[t{k}]")
                ultim, idx, t0 = f"t{k}", idx + 1, t1
        filtre.append(f"[{ultim}]fade=t=in:st=0:d=0.12,fade=t=out:st={D - 0.12:.2f}:d=0.12,format=yuv420p[v]")
        intrari += ["-i", wav]
        args = intrari + ["-filter_complex", ";".join(filtre), "-map", "[v]", "-map", f"{idx}:a",
                          "-af", "apad", "-t", f"{D:.2f}", "-r", str(fps)] + self.enc + \
               ["-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2", out]
        self._ffmpeg(args)
