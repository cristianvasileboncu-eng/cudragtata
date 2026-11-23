# -*- coding: utf-8 -*-
"""Postări foto (1080x1350): citatul zilei, sfatul zilei, jocul zilei.
Opțional: poza devine un clip de 12 s cu melodie (dacă ai pus muzică în assets/muzica)."""
import glob
import hashlib
import os
import random
import subprocess

from PIL import Image, ImageDraw, ImageFilter

from . import baza
from . import continut as C
from .provizorii import asigura, inima
from .randare import GOLD, NAVY, ALB, PALETE, Randare, font, rupe
from .setari import ASSETS, VIDEO, config, log
from .texte import legenda

W, H = 1080, 1350


def _fp(*parti):
    return hashlib.sha1("|".join(parti).encode()).hexdigest()[:16]


def _alege(categorie, rng):
    """Întoarce (fingerprint, date) pentru tipul de poză cerut."""
    if categorie == "poza_citat":
        surse = [(f"{t}:{k}", fr) for t, v in C.POVESTI.items() for k, fr in enumerate(v["m4"]) if not fr.startswith("„")]
        cheie, text = rng.choice(surse)
        return _fp("citat", cheie), {"tip": "citat", "titlu": "Gândul zilei", "text": text,
                                      "descriere": "Un gând mic pentru tații care vor să fie aproape."}
    if categorie == "poza_sfat":
        tema = rng.choice(list(C.SFATURI))
        k = rng.randrange(len(C.SFATURI[tema]["idei"]))
        return _fp("sfat", tema, str(k)), {"tip": "sfat", "titlu": "Sfatul zilei",
                                            "subtitlu": C.SFATURI[tema]["titlu"],
                                            "text": C.SFATURI[tema]["idei"][k],
                                            "descriere": "Încearcă azi. Durează doar câteva minute."}
    # poza_joc
    if rng.random() < 0.5:
        animal = rng.choice(list(C.ANIMALE))
        return _fp("ghicitoare", animal), {
            "tip": "ghicitoare", "titlu": "Ghicește animalul!", "indicii": C.ANIMALE[animal],
            "descriere": "Citiți indiciile împreună. Cine ghicește primul?",
            "raspuns": f"Ai ghicit? Scrie răspunsul în comentarii!\n.\n.\n.\nRăspuns: {animal} 🐾"}
    obiect = rng.choice(list(C.OBIECTE)); culoare = rng.choice(list(C.CULORI))
    n = rng.randint(4, 9); d = rng.randint(1, 4)
    return _fp("numarat", obiect, culoare, str(n), str(d)), {
        "tip": "numarat", "titlu": "Joc de numărat", "text": f"Câte {obiect} {culoare} vezi?",
        "forma": C.OBIECTE[obiect], "culoare": culoare, "n": n, "distractori": d, "seed": rng.randint(1, 10**6),
        "descriere": "Numărați cu voce tare, împreună!",
        "raspuns": f"Scrie răspunsul în comentarii!\n.\n.\n.\nRăspuns: {n} {obiect} {culoare} ⭐"}


def _fundal(rng):
    sus, jos = rng.choice(PALETE)
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(sus[i] + (jos[i] - sus[i]) * t) for i in range(3)))
    st = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(st)
    for _ in range(8):
        inima(ds, rng.randint(40, W - 40), rng.randint(40, H - 40), rng.randint(30, 70), (255, 255, 255, 110))
    return Image.alpha_composite(im.convert("RGBA"), st.filter(ImageFilter.GaussianBlur(2)))


def deseneaza(date, cale, rng):
    asigura()
    im = _fundal(rng)
    d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(ASSETS, "logo.png")).convert("RGBA")
    lw = 560
    logo = logo.resize((lw, int(logo.height * lw / logo.width)))
    im.alpha_composite(logo, ((W - lw) // 2, 50))
    # eticheta
    f = font(60)
    t = date["titlu"]
    w = f.getlength(t)
    d.rounded_rectangle([(W - w) / 2 - 45, 260, (W + w) / 2 + 45, 368], 54, fill=NAVY)
    d.text(((W - w) / 2, 278), t, font=f, fill=ALB)
    # card alb
    d.rounded_rectangle([60, 410, W - 60, 1150], 50, fill=(255, 255, 255, 235), outline=GOLD, width=10)
    tip = date["tip"]
    if tip in ("citat", "sfat"):
        if tip == "citat":
            d.text((100, 400), "“", font=font(220), fill=GOLD)
        else:
            fs = font(44, bold=False)
            d.text(((W - fs.getlength(date["subtitlu"])) / 2, 450), date["subtitlu"], font=fs, fill=GOLD)
        for marime in (76, 68, 60, 54):
            fl = font(marime)
            linii = rupe(date["text"], fl, 860)
            if len(linii) * marime * 1.25 < 560:
                break
        y = 800 - len(linii) * marime * 1.25 / 2
        for l in linii:
            d.text(((W - fl.getlength(l)) / 2, y), l, font=fl, fill=NAVY)
            y += marime * 1.25
    elif tip == "ghicitoare":
        fi = font(52)
        y = 470
        for k, ind in enumerate(date["indicii"], 1):
            linii = rupe(f"{k}. {ind}", fi, 860)
            for l in linii:
                d.text((110, y), l, font=fi, fill=NAVY)
                y += 66
            y += 40
        fq = font(80)
        q = "Ce animal sunt?"
        d.text(((W - fq.getlength(q)) / 2, 1020), q, font=fq, fill=GOLD, stroke_width=3, stroke_fill=NAVY)
    else:  # numărat
        fq = font(60)
        d.text(((W - fq.getlength(date["text"])) / 2, 440), date["text"], font=fq, fill=NAVY)
        prng = random.Random(date["seed"])
        culoare = C.CULORI[date["culoare"]]
        alte = [c for k, c in C.CULORI.items() if k != date["culoare"]]
        cel = [(c, r) for r in range(3) for c in range(4)]
        prng.shuffle(cel)
        ob = [culoare] * date["n"] + [prng.choice(alte) for _ in range(date["distractori"])]
        for col, (c, r) in zip(ob, cel):
            Randare._forma(None, d, date["forma"], 170 + c * 247, 640 + r * 175, 140, col)
    # subsol
    fs = font(46)
    s = "cudragtata.ro"
    d.text(((W - fs.getlength(s)) / 2, 1200), s, font=fs, fill=NAVY)
    im.convert("RGB").save(cale, quality=92)


def genereaza_poza(categorie, slot=None, zi=None):
    zi = zi or baza.azi()
    rng = random.Random()
    for _ in range(300):
        fp, date = _alege(categorie, rng)
        if not baza.exista_fp(fp):
            break
    else:
        raise RuntimeError(f"Nu mai sunt combinații noi pentru {categorie}.")
    nume = f"{zi}_{'s%d' % slot if slot is not None else 'manual'}_{categorie}_{fp}.jpg"
    cale = os.path.join(VIDEO, nume)
    deseneaza(date, cale, rng)
    sc = {"categorie": categorie, "tema": date["tip"], "fingerprint": fp, "componente": [f"{categorie}:{fp}"],
          "titlu": date["titlu"], "descriere": date["descriere"] + ("\n\n" + date["raspuns"] if date.get("raspuns") else "")}
    cfg = config()
    fisier = cale
    if cfg.get("poze", {}).get("ca_video_cu_muzica"):
        muzica = sorted(glob.glob(os.path.join(ASSETS, "muzica", "*.mp3")))
        if muzica:
            fisier = cale[:-4] + ".mp4"
            poza_in_video(cale, fisier, rng.choice(muzica))
        else:
            log("Nu există muzică în assets/muzica – postez poza simplă.", "WARN")
    vid = baza.adauga_video(sc, fisier, 0, "", slot, zi)
    log(f"Poză #{vid} gata: {os.path.basename(fisier)}")
    return vid


def poza_in_video(jpg, mp4, muzica, sec=12):
    """Poză 4:5 pe fundal vertical estompat, zoom lent, melodie, 12 secunde."""
    f = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];"
         f"[0:v]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2,"
         f"scale=1188:2112,crop=1080:1920:x='54*t/{sec}':y='96*t/{sec}',"
         f"fade=t=in:st=0:d=0.5,fade=t=out:st={sec - 0.6}:d=0.6,format=yuv420p[v];"
         f"[1:a]volume=0.8,afade=t=in:st=0:d=1,afade=t=out:st={sec - 1.5}:d=1.5[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-loop", "1", "-framerate", "30", "-i", jpg,
                    "-stream_loop", "-1", "-i", muzica, "-filter_complex", f, "-map", "[v]", "-map", "[a]",
                    "-t", str(sec)] + Randare(config()).enc + [
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", mp4], check=True)
