# -*- coding: utf-8 -*-
"""Combină bucățile din continut.py în scenarii complete (fără duplicate)."""
import hashlib
import json
import random

from . import continut as C


def _fp(categorie, componente):
    s = categorie + "|" + "|".join(componente)
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:16]


def _scena(text, vizual, eticheta="", minim=2.5):
    return {"text": text, "vizual": vizual, "eticheta": eticheta, "minim": minim}


# ---------------------------------------------------------------- POVEȘTI
def _poveste(rng):
    tema = rng.choice(list(C.POVESTI))
    t = C.POVESTI[tema]
    idx = [rng.randrange(len(t[m])) for m in ("m1", "m2", "m3", "m4")]
    ti = rng.randrange(len(t["titluri"]))
    titlu = t["titluri"][ti]
    comp = [f"poveste:{tema}:t{ti}"] + [f"poveste:{tema}:m{i+1}:{k}" for i, k in enumerate(idx)]
    fraze = [t[f"m{i+1}"][k] for i, k in enumerate(idx)]
    scene = [_scena(fraze[0], {"tip": "personaje", "poza": "start"}, titlu)]
    scene += [_scena(f, {"tip": "personaje", "poza": p}) for f, p in zip(fraze[1:], ("mijloc", "mijloc", "final"))]
    scene.append(_scena(C.FINAL, {"tip": "logo_mare"}, minim=2.5))
    return {"categorie": "poveste", "titlu": titlu, "tema": tema,
            "componente": comp, "scene": scene,
            "descriere": f"{titlu} – o poveste scurtă despre tata și cel mic."}


# ---------------------------------------------------------------- SFATURI
def _sfat(rng):
    tema = rng.choice(list(C.SFATURI))
    t = C.SFATURI[tema]
    ii = rng.randrange(len(t["intro"]))
    idei = sorted(rng.sample(range(len(t["idei"])), 3))
    rng.shuffle(idei)
    ie = rng.randrange(len(C.INCHEIERI_SFAT))
    comp = [f"sfat:{tema}:i{ii}"] + [f"sfat:{tema}:x{k}" for k in sorted(idei)] + [f"sfat:inc{ie}"]
    scene = [_scena(t["intro"][ii], {"tip": "personaje", "poza": "start"}, t["titlu"])]
    for n, k in enumerate(idei, 1):
        scene.append(_scena(t["idei"][k], {"tip": "text_mare", "mare": str(n)}, f"Ideea {n}"))
    scene.append(_scena(C.INCHEIERI_SFAT[ie] + " " + C.FINAL, {"tip": "logo_mare"}, minim=3))
    return {"categorie": "sfat", "titlu": t["titlu"], "tema": tema,
            "componente": comp, "scene": scene,
            "descriere": f"{t['titlu']}: trei idei simple pentru tați."}


# ---------------------------------------------------------------- JOCURI
def _ghicitoare(rng):
    animal = rng.choice(list(C.ANIMALE))
    indicii = C.ANIMALE[animal][:]
    ordine = list(range(3))
    rng.shuffle(ordine)
    ie = rng.randrange(len(C.INCHEIERI_JOC))
    comp = [f"joc:ghicitoare:{animal}", "ord" + "".join(map(str, ordine)), f"joc:inc{ie}"]
    scene = [_scena("Ghicitoarea zilei! Ascultă indiciile și ghicește cine sunt.",
                    {"tip": "personaje", "poza": "start"}, "Ghicește animalul!")]
    for n, k in enumerate(ordine, 1):
        scene.append(_scena(indicii[k], {"tip": "text_mare", "mare": "?"}, f"Indiciul {n}"))
    scene.append(_scena("Te-ai gândit? Trei, doi, unu!", {"tip": "numaratoare"}, minim=3.2))
    nume = animal[0].upper() + animal[1:]
    scene.append(_scena(f"Este {animal}! " + C.INCHEIERI_JOC[ie] + " " + C.FINAL,
                        {"tip": "raspuns", "mare": nume, "animal": animal}, "Răspunsul"))
    return {"categorie": "joc", "titlu": "Ghicește animalul!", "tema": "ghicitoare",
            "componente": comp, "scene": scene,
            "descriere": "Ghicitoare cu animale pentru copii. Jucați-vă împreună!"}


def _numarat(rng):
    obiect = rng.choice(list(C.OBIECTE))
    culoare = rng.choice(list(C.CULORI))
    n = rng.randint(3, 9)
    distr = rng.randint(0, 4)
    seed = rng.randint(1, 10**6)
    comp = [f"joc:numarat:{obiect}:{culoare}:{n}:{distr}"]
    viz = {"tip": "forme", "forma": C.OBIECTE[obiect], "culoare": culoare,
           "n": n, "distractori": distr, "seed": seed}
    intro = f"Joc de numărat! Câte {obiect} {culoare} vezi?"
    scene = [_scena(intro, dict(viz), "Joc de numărat", minim=3)]
    scene.append(_scena("Numără cu voce tare, împreună cu tata!", dict(viz), "Numără!", minim=5))
    scene.append(_scena("Gata? Trei, doi, unu!", {"tip": "numaratoare"}, minim=3.2))
    v2 = dict(viz); v2["numerotat"] = True
    scene.append(_scena(f"Sunt {C.NUMERE[n]} {obiect} {culoare}! Bravo! " + C.FINAL, v2, f"Răspuns: {n}"))
    return {"categorie": "joc", "titlu": "Joc de numărat", "tema": "numarat",
            "componente": comp, "scene": scene,
            "descriere": "Joc de numărat pentru cei mici. Numărați împreună!"}


def _socoteala(rng):
    if rng.random() < 0.6:
        a = rng.randint(1, 5)
        b = rng.randint(1, min(5, 10 - a))
        intrebare = (f"Tata are {C.NUMERE[a] if a > 1 else 'un'} {'mere' if a > 1 else 'măr'}. "
                     f"Mai primește {C.NUMERE[b] if b > 1 else 'unul'}. Câte mere are acum?")
        rez = a + b
        viz1 = {"tip": "mere", "a": a, "b": b, "op": "+"}
    else:
        a = rng.randint(3, 9); b = rng.randint(1, a - 1)
        intrebare = (f"Tata avea {C.NUMERE[a]} baloane. "
                     f"{'Unul a zburat' if b == 1 else C.NUMERE[b].capitalize() + ' au zburat'}. Câte au rămas?")
        rez = a - b
        viz1 = {"tip": "mere", "a": a, "b": b, "op": "-"}
    comp = [f"joc:socoteala:{viz1['op']}:{a}:{b}"]
    rez_txt = C.NUMERE[rez] if rez > 1 else "unul"
    scene = [_scena("Socoteala zilei! Ascultă cu atenție.", {"tip": "personaje", "poza": "start"}, "Socoteala zilei")]
    scene.append(_scena(intrebare, viz1, "Gândește!", minim=4))
    scene.append(_scena("Trei, doi, unu!", {"tip": "numaratoare"}, minim=3.2))
    v2 = dict(viz1); v2["rezultat"] = rez
    scene.append(_scena(f"Răspunsul este {rez_txt}! Bravo! " + C.FINAL, v2, f"Răspuns: {rez}"))
    return {"categorie": "joc", "titlu": "Socoteala zilei", "tema": "socoteala",
            "componente": comp, "scene": scene,
            "descriere": "Mică problemă de matematică pentru copii. Rezolvați împreună!"}


def _litera(rng):
    lit = rng.choice(list(C.LITERE))
    cuv = C.LITERE[lit]
    ie = rng.randrange(len(C.INCHEIERI_JOC))
    comp = [f"joc:litera:{lit}", f"joc:inc{ie}"]
    scene = [_scena(f"Litera zilei este {lit}!", {"tip": "text_mare", "mare": lit}, "Litera zilei")]
    scene.append(_scena(f"Câte cuvinte care încep cu {lit} știi tu? Spune-le cu voce tare!",
                        {"tip": "text_mare", "mare": lit}, "Gândește!", minim=5))
    scene.append(_scena("Iată câteva: " + ", ".join(cuv) + ".",
                        {"tip": "lista", "mare": lit, "cuvinte": cuv}, f"Cuvinte cu {lit}"))
    scene.append(_scena("Mai găsiți împreună încă trei cuvinte. " + C.FINAL, {"tip": "logo_mare"}))
    return {"categorie": "joc", "titlu": f"Litera zilei: {lit}", "tema": "litera",
            "componente": comp, "scene": scene,
            "descriere": f"Litera zilei: {lit}. Joc de vocabular pentru copii."}


JOCURI = [_ghicitoare, _numarat, _socoteala, _litera]
CATEGORII = {"poveste": _poveste, "sfat": _sfat}


def construieste(categorie, exista_fp, folosite_recent=(), teme_recente=(), seed=None, incercari=300):
    """Alege cea mai „proaspătă” combinație care nu a mai fost folosită.

    exista_fp(fp) -> True dacă video-ul a mai fost făcut.
    folosite_recent: componente folosite în ultimele video-uri (se evită).
    teme_recente: teme folosite recent (se evită dacă se poate).
    """
    rng = random.Random(seed)
    folosite = set(folosite_recent)
    teme = list(teme_recente)
    best, best_scor = None, None
    for _ in range(incercari):
        if categorie == "joc":
            f = rng.choice(JOCURI)
        else:
            f = CATEGORII[categorie]
        sc = f(rng)
        sc["fingerprint"] = _fp(sc["categorie"], sc["componente"])
        if exista_fp(sc["fingerprint"]):
            continue
        scor = sum(1 for c in sc["componente"] if c in folosite)
        if sc["tema"] in teme[:2]:
            scor += 5
        if sc.get("stil") == "v2" and sc["tema"] in teme[:12]:
            scor += 20
        if best is None or scor < best_scor:
            best, best_scor = sc, scor
            if scor == 0:
                break
    if best is None:
        raise RuntimeError("Nu mai există combinații noi pentru „%s”. Adaugă fraze noi în continut.py." % categorie)
    return best


if __name__ == "__main__":
    for cat in ("poveste", "sfat", "joc"):
        s = construieste(cat, lambda fp: False)
        print(json.dumps(s, ensure_ascii=False, indent=1)[:1500])


# ---------------------------------------------------------------- V2: emoție + reclame
def _v2(categorie):
    from . import continut_v2 as V

    def build(rng):
        lista = V.EMOTIE if categorie == "emotie" else V.RECLAME
        s = rng.choice(lista)
        hi = rng.randrange(len(s["hooks"]))
        ci = rng.randrange(len(V.CTA[categorie]))
        imagini = s["imagini"][:]
        rng.shuffle(imagini)
        scene = []
        for k, (cine, text) in enumerate(s["replici"]):
            sc = _scena(text, {"tip": "dinamic", "imagine": imagini[k % len(imagini)], "focus": k,
                                     "poveste": s["id"], "index": k},
                        minim=1.8)
            sc["vorbitor"] = cine
            if k == 0:
                sc["hook"] = s["hooks"][hi]
            scene.append(sc)
        final = _scena(V.CTA[categorie][ci], {"tip": "final_cta", "imagine": imagini[0],
                                              "slogan": rng.choice(V.SLOGANURI)}, minim=2.6)
        final["vorbitor"] = "narator"
        scene.append(final)
        return {"categorie": categorie, "titlu": s["titlu"], "tema": s["id"],
                "componente": [f"{categorie}:{s['id']}", f"{categorie}:{s['id']}:h{hi}", f"cta{categorie}{ci}"],
                "scene": scene, "hook": s["hooks"][hi], "stil": "v2",
                "descriere": s["hooks"][hi] + " " + V.SLOGANURI[0]}
    return build


CATEGORII["emotie"] = _v2("emotie")
CATEGORII["reclama"] = _v2("reclama")


# ---------------------------------------------------------------- V3: doar text + muzică
def _text(rng):
    from . import continut_text as T
    s = rng.choice(T.TEXTE)
    ci = rng.randrange(len(T.CTA_TEXT))
    imagini = s["imagini"][:]
    rng.shuffle(imagini)
    scene = [_scena(s["hook"], {"tip": "dinamic", "imagine": imagini[0], "focus": 0,
                                "poveste": s["id"], "index": 0}, minim=2.4)]
    scene[0]["stil_text"] = "hook"
    for k, linie in enumerate(s["linii"], 1):
        scene.append(_scena(linie, {"tip": "dinamic", "imagine": imagini[k % len(imagini)], "focus": k,
                                    "poveste": s["id"], "index": k}, minim=2.4))
    scene.append(_scena(T.CTA_TEXT[ci], {"tip": "final_cta", "imagine": imagini[0],
                                         "slogan": T.CTA_TEXT[ci]}, minim=3.2))
    return {"categorie": "text", "titlu": s["titlu"], "tema": s["id"],
            "componente": [f"text:{s['id']}", f"text:{s['id']}:c{ci}"],
            "scene": scene, "hook": s["hook"], "stil": "v2", "fara_voce": True,
            "descriere": s["hook"] + " " + " ".join(s["linii"][:2])}


CATEGORII["text"] = _text
