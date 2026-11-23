# -*- coding: utf-8 -*-
"""Scenarii v2 – „Cu drag, tata”.

Reguli după care sunt scrise (tiparele video-urilor scurte de succes):
- primele 1–2 secunde: o replică sau o imagine care oprește degetul (hook);
- 20–35 de secunde, fără pauze moarte;
- dialog tata–copil (două voci), emoție reală, fără dramă exagerată;
- final care se leagă de început (buclă) + invitație scurtă spre site.

Reguli de proiect: fără promisiuni că dorul dispare, fără discurs împotriva
mamelor, fără detalii despre copii reali. Personajele sunt „tata” și „copilul”.

Vorbitori: "tata" (Emil), "copil" (Alina, voce mai subțire), "narator" (Emil, calm).
"imagini": ce fundaluri de pe site se potrivesc (nume de fișier fără extensie).
"""

SLOGANURI = [
    "Departe, dar tot tata.",
    "Aproape, chiar și departe.",
    "Un apel video devine o aventură.",
    "Din dor, s-a născut o idee. Din iubire, o lume de aventuri.",
]

CTA = {
    "emotie": [
        "Pentru tații de departe: cudragtata.ro.",
        "Jocuri pentru apelul de diseară, pe cudragtata.ro.",
        "Trimite-l unui tată care are nevoie azi.",
    ],
    "reclama": [
        "Joacă gratuit pe cudragtata.ro.",
        "Intră pe cudragtata.ro și jucați-vă diseară.",
        "Link în profil. Cu drag, tata.",
    ],
}

# ---------------------------------------------------------------- EMOȚIE
EMOTIE = [
    {
        "id": "valiza", "tema": "plecare", "titlu": "Valiza din hol",
        "imagini": ["familia-in-aventura", "cat-familie"],
        "hooks": ["Cea mai grea dimineață", "Valiza din hol…"],
        "replici": [
            ("copil", "Tata, de ce e valiza ta în hol?"),
            ("tata", "Plec la muncă departe, puiule. Dar am un plan."),
            ("copil", "Ce plan?"),
            ("tata", "În fiecare seară, la ora șapte, ne vedem pe telefon. Și ne jucăm."),
            ("copil", "Promiți?"),
            ("tata", "Promit. Plecarea e o zi. Iubirea e în fiecare zi."),
        ],
    },
    {
        "id": "ora_sapte", "tema": "distanta", "titlu": "Ora șapte",
        "imagini": ["familia-in-aventura", "cat-familie", "joc-garaj"],
        "hooks": ["Ora 19:00. Telefonul sună.", "Cel mai așteptat apel"],
        "replici": [
            ("narator", "Ora șapte. Un telefon sună, la o mie de kilometri distanță."),
            ("copil", "Tata! Azi am construit o mașină din cutii!"),
            ("tata", "Arată-mi! Wow, are și aripi?"),
            ("copil", "E mașină zburătoare. Ca să vin la tine."),
            ("narator", "Distanța se măsoară în kilometri. Dragostea, în minutele petrecute împreună."),
        ],
    },
    {
        "id": "dor_seara", "tema": "dor", "titlu": "Dorul de seară",
        "imagini": ["cat-familie", "familia-in-aventura"],
        "hooks": ["Pentru tații cu dor", "Dacă ți-e dor, ascultă"],
        "replici": [
            ("narator", "Sunt tați care adorm cu telefonul în mână."),
            ("narator", "Care ascultă de zece ori același mesaj vocal: „Noapte bună, tati.”"),
            ("narator", "Dorul nu înseamnă că ai fost un tată mai puțin bun."),
            ("narator", "Înseamnă că iubești. Și că mâine poți fi din nou acolo, chiar și pe un ecran."),
        ],
    },
    {
        "id": "zece_minute", "tema": "timp", "titlu": "Zece minute",
        "imagini": ["cat-familie", "joc-usi", "familia-in-aventura"],
        "hooks": ["Ai doar 10 minute?", "Copilul nu ține minte cadoul…"],
        "replici": [
            ("narator", "Copilul tău nu va ține minte cât a costat jucăria."),
            ("narator", "Va ține minte cine s-a așezat pe jos lângă el."),
            ("copil", "Tata, te joci cu mine?"),
            ("tata", "Zece minute. Fără telefon. Doar noi doi."),
            ("narator", "Zece minute azi pot fi o amintire pentru toată viața."),
        ],
    },
    {
        "id": "intrebarea", "tema": "apropiere", "titlu": "Întrebarea potrivită",
        "imagini": ["familia-in-aventura", "cat-familie"],
        "hooks": ["Nu-l mai întreba asta", "O întrebare schimbă tot"],
        "replici": [
            ("tata", "Cum a fost la școală?"),
            ("copil", "Bine."),
            ("narator", "Și conversația se oprește. Încearcă altfel."),
            ("tata", "Care a fost cel mai amuzant lucru azi?"),
            ("copil", "Un porumbel a intrat în clasă și a stat pe catedră!"),
            ("narator", "Întrebarea potrivită deschide o poveste."),
        ],
    },
    {
        "id": "stea", "tema": "distanta", "titlu": "Steaua noastră",
        "imagini": ["eroii-pe-pajiste", "familia-in-aventura"],
        "hooks": ["Un secret între tată și copil", "Steaua noastră"],
        "replici": [
            ("copil", "Tata, tu vezi aceeași lună ca mine?"),
            ("tata", "Aceeași. Uite, ți-o arăt pe geam."),
            ("copil", "Atunci hai să alegem o stea. Doar a noastră."),
            ("tata", "Când ți-e dor, te uiți la ea. Și eu mă uit în același timp."),
            ("narator", "Unele promisiuni se fac pe cer."),
        ],
    },
    {
        "id": "bucurie", "tema": "bucurie", "titlu": "Râsul lui",
        "imagini": ["joc-garaj", "cat-masinute", "familia-in-aventura"],
        "hooks": ["Cel mai frumos sunet din lume", "Ce sunet te face fericit?"],
        "replici": [
            ("narator", "Cel mai frumos sunet din lume?"),
            ("copil", "Tata, ai pierdut! Mașina mea e mai rapidă!"),
            ("tata", "Nu se poate! Revanșa!"),
            ("narator", "Râsul copilului tău, când câștigă împotriva ta."),
            ("narator", "Pierde din când în când. Merită de fiecare dată."),
        ],
    },
    {
        "id": "nu_perfect", "tema": "apropiere", "titlu": "Nu trebuie să fii perfect",
        "imagini": ["cat-familie", "familia-in-aventura"],
        "hooks": ["Tată, ascultă asta", "Nu trebuie să fii perfect"],
        "replici": [
            ("narator", "Nu trebuie să fii un tată perfect."),
            ("narator", "Trebuie doar să fii acolo. Să asculți. Să râzi. Să-i spui „te iubesc”."),
            ("copil", "Tata, și eu te iubesc. Până la lună și înapoi."),
            ("tata", "Iar eu până la lună, de o mie de ori."),
        ],
    },
    {
        "id": "intoarcere", "tema": "apropiere", "titlu": "Ziua întoarcerii",
        "imagini": ["familia-in-aventura", "eroii-pe-pajiste"],
        "hooks": ["Mai sunt 3 zile…", "Numără zilele"],
        "replici": [
            ("copil", "Mai sunt trei zile până vii acasă!"),
            ("tata", "Trei zile. Ce facem prima dată?"),
            ("copil", "Clătite! Și construim un castel din pături!"),
            ("tata", "S-a făcut. Pregătește harta castelului."),
            ("narator", "Uneori, așteptarea e și ea o aventură."),
        ],
    },
    {
        "id": "timp_pretios", "tema": "timp", "titlu": "Timpul prețios",
        "imagini": ["cat-familie", "familia-in-aventura"],
        "hooks": ["Ai făcut socoteala?", "Câte veri mai sunt?"],
        "replici": [
            ("narator", "Până la 18 ani, un copil are doar 18 veri."),
            ("narator", "Unele le-ai trăit deja. Altele te așteaptă."),
            ("copil", "Tata, vara asta mergem la mare?"),
            ("tata", "Mergem. Și construim cel mai mare castel de nisip."),
            ("narator", "Timpul nu se întoarce. Dar se poate umple de amintiri."),
        ],
    },
    {
        "id": "desenul", "tema": "dor", "titlu": "Desenul",
        "imagini": ["cat-educative", "cat-familie"],
        "hooks": ["Ce a desenat copilul…", "Un desen care doare frumos"],
        "replici": [
            ("copil", "Tata, ți-am făcut un desen. Ești tu, în avion."),
            ("tata", "Și cine e lângă avion?"),
            ("copil", "Sunt eu. Zbor lângă tine, ca să nu-ți fie singur."),
            ("narator", "Copiii simt dorul la fel ca noi. Doar că îl desenează."),
        ],
    },
    {
        "id": "rutina", "tema": "apropiere", "titlu": "Ritualul nostru",
        "imagini": ["joc-usi", "familia-in-aventura"],
        "hooks": ["Un ritual de 30 de secunde", "Salutul nostru secret"],
        "replici": [
            ("tata", "Gata salutul secret?"),
            ("copil", "Gata! Palmă, pumn, inimioară!"),
            ("tata", "Palmă, pumn, inimioară! Noapte bună, campionule."),
            ("narator", "Un ritual mic îi spune copilului: suntem o echipă, oriunde am fi."),
        ],
    },
]

# ---------------------------------------------------------------- RECLAME (jocurile de pe site)
RECLAME = [
    {
        "id": "garaj_1", "tema": "garaj", "titlu": "Garajul Trăsnit",
        "imagini": ["joc-garaj", "cat-masinute"],
        "hooks": ["Cea mai trăsnită mașină?", "Copilul a construit ASTA"],
        "replici": [
            ("copil", "Tata, mașina mea are roți de pizza și motor de rachetă!"),
            ("tata", "Atunci a mea are aripi de dragon! Pe locuri…"),
            ("narator", "Garajul Trăsnit: nouă niveluri, piese nebune și Marea Cursă."),
            ("narator", "Fiecare pe telefonul lui, împreună în aceeași aventură."),
        ],
    },
    {
        "id": "garaj_2", "tema": "garaj", "titlu": "Marea Cursă",
        "imagini": ["cat-masinute", "joc-garaj"],
        "hooks": ["Tată vs. copil. Cine câștigă?", "Revanșa de diseară"],
        "replici": [
            ("narator", "Tată contra copil. Marea Cursă."),
            ("copil", "Trei, doi, unu… start!"),
            ("tata", "Hei! De unde ai turbo?"),
            ("copil", "L-am construit în Garajul Trăsnit!"),
            ("narator", "Un apel video devine o aventură."),
        ],
    },
    {
        "id": "eroi_1", "tema": "eroi", "titlu": "Cei trei eroi",
        "imagini": ["eroii-pe-pajiste", "familia-in-aventura"],
        "hooks": ["Pădurea are nevoie de ajutor!", "Copilul tău, erou?"],
        "replici": [
            ("narator", "Pădurea fermecată a rămas fără lumină."),
            ("copil", "Tata, doar noi o putem salva!"),
            ("tata", "Atunci la drum, eroule. Eu țin harta, tu deschizi porțile."),
            ("narator", "Cei trei eroi și pădurea fermecată. Patru niveluri de aventură împreună."),
        ],
    },
    {
        "id": "eroi_2", "tema": "eroi", "titlu": "Eroii de diseară",
        "imagini": ["eroii-pe-pajiste", "joc-usi"],
        "hooks": ["Seara asta salvăm o pădure", "Misiune pentru tată și copil"],
        "replici": [
            ("tata", "Misiune nouă: o pădure întreagă așteaptă eroii."),
            ("copil", "Eu sunt eroul cu pelerină!"),
            ("tata", "Și eu sunt cel care te urmează."),
            ("narator", "Un joc în care copilul conduce, iar tata îl ajută. Chiar și de departe."),
        ],
    },
    {
        "id": "pod_1", "tema": "pod", "titlu": "Podul Curcubeului",
        "imagini": ["cat-masinute", "familia-in-aventura"],
        "hooks": ["Un pod făcut din curcubeu", "Drum spre castel!"],
        "replici": [
            ("copil", "Tata, podul e din curcubeu! Pe ce culoare mergem?"),
            ("tata", "Pe galben! Și tu ții volanul."),
            ("narator", "Podul Curcubeului: trei niveluri cu mașinuțe, până la Castelul Curcubeului."),
            ("narator", "Perfect pentru cei mici, la apelul de seară."),
        ],
    },
    {
        "id": "comoara_1", "tema": "comoara", "titlu": "Comoara din Pădurea Fermecată",
        "imagini": ["eroii-pe-pajiste", "cat-ghicit"],
        "hooks": ["Am găsit o hartă secretă!", "Unde e comoara?"],
        "replici": [
            ("copil", "Tata, am găsit o hartă! Are un X roșu!"),
            ("tata", "Și eu am jumătatea cealaltă. Împreună găsim comoara."),
            ("narator", "Comoara din Pădurea Fermecată: fiecare are o parte din hartă. Doar împreună ajungeți la final."),
        ],
    },
    {
        "id": "site_1", "tema": "site", "titlu": "Departe, dar tot tata",
        "imagini": ["familia-in-aventura", "cat-familie"],
        "hooks": ["Pentru tații de departe", "Ești departe de copilul tău?"],
        "replici": [
            ("narator", "Ești departe de copilul tău? Nu ești singurul."),
            ("narator", "Pe cudragtata.ro, un apel video devine o aventură."),
            ("narator", "Porniți apelul, deschideți același joc, fiecare pe telefonul lui."),
            ("copil", "Tata, mai jucăm o dată?"),
            ("narator", "Departe, dar tot tata."),
        ],
    },
    {
        "id": "site_2", "tema": "site", "titlu": "Din dor, s-a născut o idee",
        "imagini": ["cat-familie", "familia-in-aventura", "eroii-pe-pajiste"],
        "hooks": ["Cum s-a născut ideea asta", "Din dor, o idee"],
        "replici": [
            ("narator", "Din dor, s-a născut o idee."),
            ("narator", "Din iubire, o lume de aventuri pentru tați și copii."),
            ("narator", "Jocuri, povești și provocări pe care le jucați împreună, chiar dacă sunteți departe."),
            ("copil", "Tata, mâine ne jucăm iar?"),
            ("tata", "Mâine. Și poimâine. Cu drag."),
        ],
    },
    {
        "id": "provocare", "tema": "provocare", "titlu": "Provocarea săptămânii",
        "imagini": ["cat-familie", "cat-educative"],
        "hooks": ["Provocare pentru tați!", "Poți construi asta în 15 minute?"],
        "replici": [
            ("narator", "Provocarea săptămânii: construiți ceva împreună din cutii și hârtie."),
            ("copil", "Eu fac un garaj! Tata, tu faci mașina!"),
            ("tata", "Accept provocarea!"),
            ("narator", "Provocări noi în fiecare săptămână, pe cudragtata.ro."),
        ],
    },
    {
        "id": "ghicit", "tema": "ghicit", "titlu": "Ghicește ce e!",
        "imagini": ["cat-ghicit", "cat-educative"],
        "hooks": ["Ghicești din 3 indicii?", "Joc rapid pentru apel"],
        "replici": [
            ("tata", "Ghicitoare: am urechi lungi și sar foarte repede."),
            ("copil", "Iepurele! Prea ușor! Încă una!"),
            ("tata", "Bine… Îmi port casa în spinare."),
            ("copil", "Melcul!"),
            ("narator", "Jocuri de ghicit pentru apelul de diseară. Pe cudragtata.ro."),
        ],
    },
]

HASHTAGURI_V2 = {
    "emotie": "#cudragtata #tata #tati #dordecopii #tatadedeparte #parinti #iubire #familie #copii #emotii",
    "reclama": "#cudragtata #jocuricopii #tata #copii #apelvideo #jocurieducative #parinti #familie #aventura #tatadedeparte",
}
