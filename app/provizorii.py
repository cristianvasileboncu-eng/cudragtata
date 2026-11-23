# -*- coding: utf-8 -*-
"""Imagini PROVIZORII (logo + personaje simple), folosite doar până pui
imaginile reale de pe cudragtata.ro în folderul assets/."""
import os

from PIL import Image, ImageDraw, ImageFont

from .setari import ASSETS, FONT_BOLD, FONT

NAVY = (31, 42, 68)
GOLD = (224, 165, 38)
RED = (214, 69, 80)


def inima(d, cx, cy, s, fill):
    r = s * 0.27
    d.ellipse([cx - 2 * r, cy - r * 1.6, cx, cy + r * 0.4], fill=fill)
    d.ellipse([cx, cy - r * 1.6, cx + 2 * r, cy + r * 0.4], fill=fill)
    d.polygon([(cx - 2 * r + 2, cy - r * 0.25), (cx + 2 * r - 2, cy - r * 0.25), (cx, cy + s * 0.62)], fill=fill)


def logo(cale):
    W, H = 1000, 300
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W - 1, H - 1], 60, fill=(255, 250, 240, 235))
    # fir care unește cele două inimi
    d.line([(70, 200), (120, 150), (170, 190), (215, 160)], fill=GOLD, width=7)
    inima(d, 105, 130, 120, RED)
    inima(d, 225, 160, 70, GOLD)
    f1 = ImageFont.truetype(FONT_BOLD, 84)
    f2 = ImageFont.truetype(FONT, 40)
    d.text((300, 55), "Cu drag, tata", font=f1, fill=NAVY)
    d.text((305, 175), "pentru tații de departe", font=f2, fill=GOLD)
    im.save(cale)


def personaj(cale, mare=True, culoare=NAVY, par=(70, 45, 30), barba=False):
    W, H = (520, 900) if mare else (400, 640)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = W // 2
    cap = int(W * 0.30)
    piele = (246, 206, 170)
    top = 20
    # corp
    d.rounded_rectangle([cx - W * 0.36, top + cap * 2 - 10, cx + W * 0.36, H - 60], 90, fill=culoare)
    # picioare
    d.rounded_rectangle([cx - W * 0.28, H - 110, cx - W * 0.06, H - 5], 30, fill=(60, 70, 90))
    d.rounded_rectangle([cx + W * 0.06, H - 110, cx + W * 0.28, H - 5], 30, fill=(60, 70, 90))
    # inimioară pe piept
    inima(d, cx, top + cap * 2 + H * 0.16, W * 0.16, GOLD if culoare == NAVY else RED)
    # cap
    d.ellipse([cx - cap, top, cx + cap, top + cap * 2], fill=piele)
    d.pieslice([cx - cap, top - 6, cx + cap, top + cap * 1.3], 180, 360, fill=par)
    # ochi + zâmbet
    ox = cap * 0.38
    for sx in (-1, 1):
        d.ellipse([cx + sx * ox - 12, top + cap * 1.0 - 12, cx + sx * ox + 12, top + cap * 1.0 + 12], fill=NAVY)
    d.arc([cx - cap * 0.4, top + cap * 1.05, cx + cap * 0.4, top + cap * 1.6], 15, 165, fill=RED, width=8)
    if barba:
        d.chord([cx - cap * 0.75, top + cap * 1.2, cx + cap * 0.75, top + cap * 2.05], 0, 180, fill=par)
        d.arc([cx - cap * 0.35, top + cap * 1.12, cx + cap * 0.35, top + cap * 1.55], 15, 165, fill=(250, 240, 230), width=8)
    # obraji
    for sx in (-1, 1):
        d.ellipse([cx + sx * cap * 0.62 - 16, top + cap * 1.25 - 10, cx + sx * cap * 0.62 + 16, top + cap * 1.25 + 10],
                  fill=(240, 160, 150))
    im.save(cale)


def asigura():
    """Creează imaginile provizorii doar dacă lipsesc."""
    os.makedirs(os.path.join(ASSETS, "personaje", "tata"), exist_ok=True)
    os.makedirs(os.path.join(ASSETS, "personaje", "copil"), exist_ok=True)
    os.makedirs(os.path.join(ASSETS, "animale"), exist_ok=True)
    os.makedirs(os.path.join(ASSETS, "muzica"), exist_ok=True)
    lg = os.path.join(ASSETS, "logo.png")
    if not os.path.exists(lg):
        logo(lg)
    t = os.path.join(ASSETS, "personaje", "tata")
    if not any(f.lower().endswith(".png") for f in os.listdir(t)):
        personaj(os.path.join(t, "tata_provizoriu.png"), True, NAVY, barba=True)
    c = os.path.join(ASSETS, "personaje", "copil")
    if not any(f.lower().endswith(".png") for f in os.listdir(c)):
        personaj(os.path.join(c, "copil_provizoriu.png"), False, GOLD, par=(150, 90, 40))
