# -*- coding: utf-8 -*-
"""Descrieri (mesajele postărilor), profesionale și legate de site."""
import random

from . import continut as C

DESCHIDERI = {
    "emotie": [
        "Pentru toți tații care poartă dorul în buzunar. 💛",
        "Departe, dar tot tata.",
        "Uneori, cele mai mari lucruri sunt cele mai mici momente.",
    ],
    "reclama": [
        "Un apel video devine o aventură. 🎮",
        "Jocuri gratuite pentru tați și copii, chiar și de la distanță.",
        "Fiecare pe telefonul lui, împreună în aceeași aventură.",
    ],
    "poveste": [
        "O poveste de 30 de secunde, de citit împreună în seara asta. 💛",
        "Povești mici, amintiri mari. Ascultați-o împreună.",
        "Pentru tații care vor să fie aproape, chiar și de departe.",
    ],
    "sfat": [
        "Idei simple, pentru zile aglomerate. 💛",
        "Nu ai nevoie de mult timp. Ai nevoie de puțin timp, bine folosit.",
        "Pentru tați care vor să fie prezenți, nu perfecți.",
    ],
    "joc": [
        "Jocul zilei: 30 de secunde de joacă împreună. 🎲",
        "Puneți-l pe ecran și jucați-vă împreună, acasă sau la apel video.",
        "Un mic joc pentru minți curioase. Câte puncte faceți azi?",
    ],
}
INVITATII = [
    "Mai multe povești și jocuri pentru tați și copii găsești pe {site}.",
    "Pe {site} găsești jocuri pe care le puteți juca împreună, chiar și de la distanță.",
    "Urmărește pagina pentru o idee nouă în fiecare zi. Mai multe pe {site}.",
]


def legenda(categorie, titlu, descriere, site="cudragtata.ro", seed=None, extra=""):
    rng = random.Random(seed)
    baza = categorie.replace("poza_", "")
    baza = {"text": "emotie", "citat": "poveste", "ghicitoare": "joc", "numarat": "joc"}.get(baza, baza)
    desch = rng.choice(DESCHIDERI.get(baza, DESCHIDERI["poveste"]))
    inv = rng.choice(INVITATII).format(site=site)
    from .continut_v2 import HASHTAGURI_V2
    tags = HASHTAGURI_V2.get(baza) or C.HASHTAGURI.get(baza, C.HASHTAGURI["poveste"])
    corp = f"{titlu}\n\n{desch}\n{descriere}"
    if extra:
        corp += "\n\n" + extra
    return f"{corp}\n\n{inv}\n\nCu drag, tata. 💛\n\n{tags}"


def titlu_youtube(titlu):
    t = f"{titlu} | Cu drag, tata #Shorts"
    return t[:100]
