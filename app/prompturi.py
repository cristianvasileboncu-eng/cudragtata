# -*- coding: utf-8 -*-
"""Generează PROMPTURI_IMAGINI.md: cereri gata scrise pentru ChatGPT / Gemini,
câte o imagine pentru fiecare replică din fiecare poveste (continut_v2.py).

Rulează:  python -m app.prompturi
"""
import os

from . import continut_v2 as V
from .setari import RADACINA

STIL = ("Ilustrație 3D caldă, în stilul unui film de animație pentru familie, lumină aurie, "
        "culori calde cu accente bleumarin și auriu, format VERTICAL 9:16, fără niciun text sau literă în imagine. "
        "Personaje (la fel în toate imaginile): TATA – bărbat de aproximativ 40 de ani, barbă scurtă castanie, "
        "pulover bleumarin; COPILUL – băiețel de 6 ani, păr castaniu ciufulit, tricou galben. "
        "Personaje inventate, nu persoane reale.")

SCENE = {
    "valiza": ["copilul în pijama privește o valiză mare în holul casei, dimineața", "tata îngenunchează și îi vorbește copilului, ținându-l de umeri",
               "copilul curios, cu ochii mari", "tata îi arată pe telefon un ceas care indică ora 19:00", "copilul îi întinde degetul mic pentru o promisiune",
               "tata și copilul fac promisiunea cu degetele mici, la ușă"],
    "ora_sapte": ["un telefon care sună pe o masă, seara, ceasul arată 19:00", "copilul arată spre camera telefonului o mașină din cutii de carton",
                  "tata râde, privind telefonul într-o cameră de hotel", "copilul ține mașina de carton cu aripi, ca și cum ar zbura",
                  "tata și copilul, fiecare pe ecranul lui, zâmbind"],
    "dor_seara": ["tata stă pe marginea patului, seara, cu telefonul în mână", "tata ascultă un mesaj vocal, cu un zâmbet trist",
                  "tata se uită pe fereastră la luminile orașului", "dimineață: tata zâmbește la un apel video cu copilul"],
    "zece_minute": ["o cutie de jucărie scumpă, uitată într-un colț", "tata stă pe covor lângă copil, construind cu cuburi",
                    "copilul întinde o jucărie spre tata", "telefonul tatei pus deoparte, cu ecranul în jos", "tata și copilul râzând pe covor"],
    "intrebarea": ["tata la masă îl întreabă ceva pe copil", "copilul ridică din umeri, plictisit", "tata pe gânduri, cu mâna la bărbie",
                   "tata se apleacă spre copil, curios", "copilul povestește entuziasmat, gesticulând", "tata și copilul râd la masă"],
    "stea": ["copilul la fereastră, noaptea, privind luna", "tata la altă fereastră, în alt oraș, privind aceeași lună",
             "copilul arată cu degetul o stea strălucitoare", "tata și copilul, fiecare la fereastra lui, privind aceeași stea", "cerul înstelat cu o stea mai strălucitoare"],
    "bucurie": ["copilul râzând cu gura până la urechi", "copilul ridică brațele în semn de victorie lângă o pistă de mașinuțe",
                "tata se preface supărat, amuzant", "tata și copilul râzând împreună pe covor", "tata ciufulindu-i părul copilului"],
    "nu_perfect": ["tata obosit, dar zâmbitor, cu copilul în brațe", "tata ascultă atent ce spune copilul", "copilul își desface brațele larg",
                   "tata și copilul îmbrățișați, privind spre lună"],
    "intoarcere": ["copilul arată un calendar cu zile tăiate cu roșu", "tata pe apel video, zâmbind", "copilul cu o tigaie de jucărie și o pătură pe umeri",
                   "tata salută cu degetul mare în sus", "copilul desenând o hartă a unui castel din pături"],
    "timp_pretios": ["un castel de nisip pe plajă, la apus", "o clepsidră cu nisip auriu", "copilul cu o găletușă trage de mâna tatălui",
                     "tata și copilul construind un castel de nisip uriaș", "tata și copilul pe plajă, la apus, de mână"],
    "desenul": ["copilul ține un desen colorat cu un avion", "tata privește desenul pe telefon, emoționat", "desenul: un copil zburând lângă un avion",
                "tata ține desenul printat lângă inimă"],
    "rutina": ["tata și copilul față în față, gata de salutul secret", "palmă în palmă", "pumn în pumn, apoi o inimioară făcută din degete",
               "copilul adormit, tata îl învelește"],
    "garaj_1": ["copilul arată o mașină trăsnită cu roți de pizza", "tata cu o mașină cu aripi de dragon", "un garaj colorat plin de piese ciudate",
                "tata și copilul, fiecare cu telefonul lui, jucându-se"],
    "garaj_2": ["două mașini de curse colorate la linia de start", "steagul de start fluturat", "mașina tatei rămasă în urmă, tata surprins",
                "copilul câștigă cursa, mașina cu turbo", "tata și copilul pe un apel video, bucuroși"],
    "eroi_1": ["o pădure fermecată întunecată, cu licurici stinși", "copilul cu pelerină de erou, hotărât", "tata cu o hartă veche, copilul deschide o poartă",
               "pădurea luminată din nou, colorată"],
    "eroi_2": ["o hartă a unei păduri magice", "copilul cu pelerină bleumarin", "tata zâmbind, urmându-l pe copil", "tata și copilul pe două telefoane, în aceeași aventură"],
    "pod_1": ["un pod din curcubeu peste nori", "o mașinuță galbenă pe podul curcubeu", "un castel din curcubeu la capătul podului", "copilul la apel video, entuziasmat"],
    "comoara_1": ["copilul ține jumătate de hartă cu un X roșu", "tata ține cealaltă jumătate de hartă", "un cufăr cu comoară strălucitor în pădure"],
    "site_1": ["tata singur, privind telefonul, seara", "un apel video vesel între tata și copil", "două telefoane cu același joc colorat",
               "copilul întreabă ceva, zâmbind", "tata și copilul, fiecare pe ecranul lui, cu inimioare între ele"],
    "site_2": ["o inimă mare și una mică unite printr-un fir auriu", "o lume de aventuri: păduri, mașinuțe, castele", "tata și copilul jucându-se pe telefoane",
               "copilul la apel video", "tata zâmbind cald la telefon"],
    "provocare": ["cutii de carton, foarfece și hârtie colorată pe masă", "copilul construiește un garaj din cutie", "tata ridică o mașină de carton, mândru",
                  "garajul și mașina de carton terminate"],
    "ghicit": ["tata cu un semn de întrebare deasupra capului", "un iepure care sare", "tata gândindu-se, amuzat", "un melc cu căsuța în spinare",
               "copilul ridicând mâna bucuros"],
}


def scrie():
    linii = ["# Prompturi pentru imagini – „Cu drag, tata”", "",
             "Cum le folosești:",
             "1. Copiază un prompt în ChatGPT sau Gemini și cere imaginea.",
             "2. Salvează imaginile cu numele 1.jpg, 2.jpg, 3.jpg… (în ordinea de mai jos).",
             "3. Pune-le în folderul `povesti/<id>/` din program (ex.: `povesti/valiza/1.jpg`).",
             "4. Programul le folosește automat când alege povestea respectivă. Dacă lipsesc, folosește imaginile de pe site.",
             "", "**Stil (scrie-l la începutul fiecărei cereri):**", "", "> " + STIL, ""]
    for grup, lista in (("POVEȘTI CU EMOȚIE", V.EMOTIE), ("RECLAME", V.RECLAME)):
        linii += ["", f"## {grup}", ""]
        for s in lista:
            sc = SCENE.get(s["id"], [])
            linii += [f"### {s['titlu']}  → folder `povesti/{s['id']}/`", ""]
            for k, (cine, text) in enumerate(s["replici"]):
                desc = sc[k] if k < len(sc) else (sc[-1] if sc else "tata și copilul împreună")
                linii.append(f"{k + 1}. ({cine}: „{text}”)  \n   **Prompt:** {STIL} Scena: {desc}.")
            linii.append("")
    cale = os.path.join(RADACINA, "PROMPTURI_IMAGINI.md")
    with open(cale, "w", encoding="utf-8") as f:
        f.write("\n".join(linii))
    return cale


if __name__ == "__main__":
    print(scrie())
