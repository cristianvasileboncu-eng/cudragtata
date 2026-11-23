# -*- coding: utf-8 -*-
"""Biblioteca de scenarii originale „Cu drag, tata”.

Fiecare video se compune automat din bucăți (fraze) alese din aceste liste.
Combinațiile sunt multe, iar sistemul ține minte ce a folosit, ca să nu repete.

Poți adăuga oricând fraze noi: respectă forma listelor de mai jos.
"""

FINAL = "Cu drag, tata."

# ---------------------------------------------------------------------------
# POVEȘTI: fiecare temă are 4 momente; din fiecare moment se alege o frază.
# Toate frazele dintr-o temă se potrivesc între ele în orice combinație.
# ---------------------------------------------------------------------------
POVESTI = {
    "clatite": {
        "titluri": ["Clătitele cu surprize", "Bucătarul cel mic"],
        "m1": [
            "Duminică dimineață, tata și cel mic au hotărât să facă clătite.",
            "Într-o dimineață cu soare, cel mic a anunțat: „Azi gătesc eu, tata!”",
            "Tata a scos castronul cel mare, iar cel mic și-a pus șorțul de bucătar.",
        ],
        "m2": [
            "Cel mic a spart primul ou. Jumătate a ajuns în castron, jumătate pe masă.",
            "Făina a zburat peste tot, iar tata avea acum o mustață albă.",
            "Au amestecat împreună, numărând fiecare învârtire până la douăzeci.",
        ],
        "m3": [
            "Prima clătită s-a lipit de tigaie, dar tata a râs: „Prima e pentru noroc!”",
            "Cel mic a desenat câte un zâmbet cu gem pe fiecare clătită.",
            "Când tata a întors clătita în aer, cel mic a aplaudat ca la circ.",
        ],
        "m4": [
            "Nu au ieșit perfecte, dar au fost cele mai bune clătite din lume.",
            "Bucătăria era plină de făină, dar și de râsete.",
            "De atunci, duminica are un nume nou: ziua clătitelor cu tata.",
        ],
    },
    "zmeu": {
        "titluri": ["Zmeul care nu voia să zboare", "O zi cu vânt"],
        "m1": [
            "Vântul bătea tare, așa că tata și cel mic au luat zmeul și au plecat în parc.",
            "Cel mic a găsit în debara un zmeu vechi, cu o coadă lungă și colorată.",
            "„Tata, azi zburăm ceva?” a întrebat cel mic, cu un zmeu roșu în mână.",
        ],
        "m2": [
            "Prima încercare a fost un dezastru: zmeul a căzut direct în iarbă.",
            "Tata a alergat până a rămas fără suflu, dar zmeul tot nu se ridica.",
            "S-au uitat împreună la copaci, ca să afle din ce parte bate vântul.",
        ],
        "m3": [
            "Apoi, o pală de vânt a ridicat zmeul sus, tot mai sus, peste copaci.",
            "Cel mic a ținut sfoara singur, iar tata doar l-a ajutat cu o mână.",
            "Zmeul a dansat pe cer ca un pește colorat într-un ocean albastru.",
        ],
        "m4": [
            "Uneori ai nevoie de mai multe încercări. Și de cineva care aleargă cu tine.",
            "Au plecat acasă obosiți, cu obrajii roșii și cu o poveste nouă.",
            "Zmeul a zburat sus, dar cel mai frumos a fost că au fost împreună.",
        ],
    },
    "departe": {
        "titluri": ["Ora șapte, ora noastră", "Aproape, de departe"],
        "m1": [
            "Tata lucra departe, dar în fiecare seară, la ora șapte, telefonul suna.",
            "Între tata și cel mic erau multe orașe, dar aveau un plan secret.",
            "Cel mic aștepta lângă telefon, cu o cutie de jucării pregătită.",
        ],
        "m2": [
            "„Azi construim un castel”, a zis tata, și fiecare și-a luat cuburile.",
            "Au citit aceeași poveste în același timp, fiecare din cartea lui.",
            "Tata a ascuns o jucărie în cameră, iar cel mic a ghicit unde, după indicii.",
        ],
        "m3": [
            "Castelul lui tata a căzut primul, și au râs amândoi până la lacrimi.",
            "Cel mic a ghicit din prima și a făcut un dans al victoriei în fața camerei.",
            "La final, și-au pus amândoi palma pe ecran, palmă în palmă.",
        ],
        "m4": [
            "Distanța se măsoară în kilometri. Dragostea, în timpul petrecut împreună.",
            "Nu erau în aceeași cameră, dar erau în aceeași poveste.",
            "„Mâine la aceeași oră?” „Mâine la aceeași oră, tata!”",
        ],
    },
    "ploaie": {
        "titluri": ["Fortăreața de pături", "Aventura din sufragerie"],
        "m1": [
            "Afară ploua de dimineață, iar planul de joacă în parc a căzut.",
            "Ploaia bătea în geam, iar cel mic se plictisea de moarte.",
            "„Nu putem ieși”, a oftat cel mic. Tata a zâmbit misterios.",
        ],
        "m2": [
            "Tata a adus toate păturile și pernele din casă.",
            "Au construit o fortăreață din scaune, pături și o lanternă.",
            "Fiecare a desenat pe o foaie harta fortăreței secrete.",
        ],
        "m3": [
            "Înăuntru, cu lanterna aprinsă, tata a spus povești cu dragoni.",
            "Au ascultat ploaia din fortăreață, ca doi exploratori în cort.",
            "Cel mic a devenit regele fortăreței, iar tata, paznicul lui credincios.",
        ],
        "m4": [
            "Ziua ploioasă a devenit cea mai frumoasă aventură a săptămânii.",
            "Nu ai nevoie de soare ca să ai o zi bună. Ai nevoie de imaginație.",
            "Pătura veche a devenit castel, iar ploaia a devenit muzică.",
        ],
    },
    "stele": {
        "titluri": ["Steaua noastră", "Câte stele sunt pe cer?"],
        "m1": [
            "Era seară, iar cel mic nu voia deloc să doarmă.",
            "Tata și cel mic au ieșit pe balcon, înainte de culcare.",
            "„Câte stele sunt pe cer, tata?” a întrebat cel mic.",
        ],
        "m2": [
            "Au început să numere stelele, dar s-au încurcat la treizeci și șapte.",
            "Tata i-a arătat o stea strălucitoare și a numit-o „steaua noastră”.",
            "Au inventat constelații noi: un dinozaur, o pizza și o mașinuță.",
        ],
        "m3": [
            "Cel mic a căscat o dată, apoi încă o dată.",
            "„Steaua noastră ne vede și când suntem departe”, a zis tata.",
            "Au promis că în fiecare seară se vor uita la aceeași stea.",
        ],
        "m4": [
            "Unele lucruri nu au nevoie de multe cuvinte. Doar de cineva lângă tine.",
            "Și așa, cu ochii la stele, cel mic a adormit liniștit.",
            "Noapte bună, steluță. Mâine numărăm din nou.",
        ],
    },
    "atelier": {
        "titluri": ["Căsuța pentru păsări", "Micul tâmplar"],
        "m1": [
            "Tata a găsit în atelier câteva scânduri și a avut o idee.",
            "„Construim o căsuță pentru păsări?” a întrebat tata. Cel mic a sărit în sus.",
            "Cu un ciocan mic în mână, cel mic era gata de lucru.",
        ],
        "m2": [
            "Tata ținea scândura, iar cel mic măsura cu metrul, foarte serios.",
            "Au ales culorile: acoperiș roșu și pereți galbeni.",
            "Primul cui a ieșit strâmb, dar tata a zis că așa are personalitate.",
        ],
        "m3": [
            "Când au terminat, căsuța nu era perfectă, dar era a lor.",
            "Au agățat căsuța în copac și au așteptat cu sufletul la gură.",
            "A doua zi dimineață, o vrabie s-a uitat curioasă înăuntru.",
        ],
        "m4": [
            "Cele mai frumoase lucruri sunt cele făcute cu mâinile noastre, împreună.",
            "Răbdarea, un ciocan și un tată lângă tine pot construi orice.",
            "Acum, de fiecare dată când trece o pasăre, cel mic zâmbește.",
        ],
    },
}

# ---------------------------------------------------------------------------
# SFATURI pentru părinți: o introducere + 3 idei + o încheiere.
# ---------------------------------------------------------------------------
SFATURI = {
    "zece_minute": {
        "titlu": "Zece minute care contează",
        "intro": [
            "Ai doar zece minute? E suficient. Uite trei idei.",
            "Trei gesturi mici pentru tații ocupați.",
        ],
        "idei": [
            "Lasă telefonul în altă cameră și lasă copilul să aleagă jocul.",
            "Întreabă „Ce a fost cel mai amuzant azi?”, nu „Cum a fost la școală?”",
            "Transformă strânsul jucăriilor într-o întrecere.",
            "Citește o poveste și lasă-l pe el să inventeze finalul.",
            "Pune-i în ghiozdan un bilețel desenat de tine.",
            "Ascultă povestea cu dinozauri până la capăt, chiar și a zecea oară.",
            "Alege o zi pe săptămână care să fie doar a voastră.",
            "Spune-i concret ce ți-a plăcut azi la el.",
        ],
    },
    "distanta": {
        "titlu": "Pentru tații de departe",
        "intro": [
            "Ești departe de copilul tău? Trei idei pentru apelul de azi.",
            "Un apel video poate fi o aventură. Uite cum.",
        ],
        "idei": [
            "Stabiliți o oră fixă pentru apel, ca să aibă ce aștepta.",
            "Pregătește un joc înainte de apel: o ghicitoare sau o poveste.",
            "Citiți aceeași carte, fiecare cu exemplarul lui.",
            "Lasă-l să-ți arate camera și jucăriile. Tu doar întreabă.",
            "Trimite-i o poză cu ceva care ți-a amintit de el.",
            "Încheiați apelul cu un salut secret, doar al vostru.",
            "Un apel scurt e în regulă. Contează să fie constant.",
            "Desenați același lucru în același timp și comparați la final.",
        ],
    },
    "bucatarie": {
        "titlu": "Gătim împreună",
        "intro": [
            "Bucătăria e cel mai bun loc de joacă. Trei idei.",
            "Vrei să gătești cu copilul? Începe așa.",
        ],
        "idei": [
            "Dă-i o sarcină doar a lui: spălatul legumelor sau amestecatul.",
            "Lasă-l să guste și să-ți spună ce lipsește.",
            "Faceți forme amuzante: sandvișuri cu fețe, clătite cu zâmbet.",
            "Acceptă mizeria de la început. Face parte din distracție.",
            "Numărați împreună ingredientele. E și matematică, și joacă.",
            "Puneți nume rețetelor voastre, de exemplu „Supa supereroilor”.",
            "Lasă-l să decoreze farfuria, chiar dacă nu iese perfect.",
            "La final, strângeți împreună. Și asta poate fi un joc.",
        ],
    },
    "emotii": {
        "titlu": "Când e supărat",
        "intro": [
            "Copilul e supărat? Trei lucruri simple care ajută.",
            "Emoțiile mari au nevoie de un tată calm. Trei idei.",
        ],
        "idei": [
            "Spune cu voce tare ce vezi: „Văd că ești supărat.”",
            "Întreabă „Ce te-ar ajuta acum?” înainte să dai soluții.",
            "Spune-i și tu cum te simți, simplu, pe înțelesul lui.",
            "Suflați împreună, ca peste lumânările de ziua lui.",
            "Laudă efortul, nu doar rezultatul.",
            "Când greșești, spune „Îmi pare rău”. Copilul învață din exemplu.",
            "Faceți o îmbrățișare de zece secunde și numărați împreună.",
            "Seara, întreabă: „Care a fost partea ta preferată din zi?”",
        ],
    },
    "seara": {
        "titlu": "Rutina de seară",
        "intro": [
            "Seara poate fi cel mai frumos moment al zilei. Trei idei.",
            "Pentru o culcare mai liniștită, încearcă asta.",
        ],
        "idei": [
            "Aceeași rutină în fiecare seară îl ajută să se liniștească.",
            "Opriți ecranele cu o jumătate de oră înainte de culcare.",
            "Inventați o poveste împreună, câte o propoziție fiecare.",
            "Spuneți fiecare trei lucruri frumoase din ziua care a trecut.",
            "Lasă-l să aleagă pijamaua sau cartea de seară.",
            "Un cântec de noapte bună poate deveni amintirea lui de o viață.",
            "Vorbește mai încet și mai rar. Liniștea se transmite.",
            "Spune-i „Te iubesc”, chiar dacă pare că a adormit deja.",
        ],
    },
    "joaca": {
        "titlu": "Joacă fără jucării scumpe",
        "intro": [
            "Nu ai nevoie de jucării scumpe. Ai nevoie de idei ca acestea.",
            "Trei jocuri de făcut azi, fără să cumperi nimic.",
        ],
        "idei": [
            "Lasă-l pe el să conducă jocul. Tu ești doar ajutorul.",
            "Un cearșaf și două scaune devin un castel.",
            "Pierde din când în când, dar nu de fiecare dată.",
            "Jucați-vă de-a oglinda: el face o mișcare, tu o copiezi.",
            "Ascunde o jucărie și dă-i indicii: „cald” sau „rece”.",
            "Transformă plimbarea într-o vânătoare de culori.",
            "Dansați pe melodia lui preferată, chiar dacă nu știi pașii.",
            "Construiți ceva din cutii goale. Imaginația face restul.",
        ],
    },
}

INCHEIERI_SFAT = [
    "Alege o singură idee pentru azi. E destul.",
    "Salvează clipul pentru seara asta.",
    "Trimite-l unui tată care are nevoie de o idee azi.",
    "Care idee o încerci azi? Scrie în comentarii.",
]

# ---------------------------------------------------------------------------
# JOCURI EDUCATIVE (se generează automat, cu multe variante)
# ---------------------------------------------------------------------------
ANIMALE = {
    # nume (cum se spune la final), indicii
    "pisica": ["Am mustăți lungi și torc când sunt fericită.", "Îmi place să mă joc cu ghemul.", "Spun „miau”."],
    "câinele": ["Dau din coadă când sunt bucuros.", "Sunt cel mai bun prieten al omului.", "Spun „ham-ham”."],
    "vaca": ["Trăiesc la fermă și mănânc iarbă.", "Din laptele meu se face brânză.", "Spun „muuu”."],
    "leul": ["Am o coamă mare și sunt regele animalelor.", "Răcnetul meu se aude de departe.", "Trăiesc în savană."],
    "elefantul": ["Sunt foarte mare și am urechi uriașe.", "Am o trompă lungă.", "Îmi place să mă stropesc cu apă."],
    "girafa": ["Am cel mai lung gât dintre toate animalele.", "Mănânc frunze din vârful copacilor.", "Am pete maro pe blană."],
    "iepurele": ["Am urechi lungi și sar foarte repede.", "Îmi plac morcovii.", "Am o codiță pufoasă."],
    "broasca": ["Sar și trăiesc lângă baltă.", "Prind muște cu limba.", "Spun „oac-oac”."],
    "rața": ["Înot pe lac și am pene.", "Am un cioc lat și galben.", "Spun „mac-mac”."],
    "ursul": ["Sunt mare, blănos și iubesc mierea.", "Iarna dorm foarte mult.", "Trăiesc în pădure."],
    "vulpea": ["Am blana roșcată și coada stufoasă.", "În povești sunt foarte isteață.", "Locuiesc într-o vizuină, în pădure."],
    "bufnița": ["Stau trează noaptea și dorm ziua.", "Am ochi mari și rotunzi.", "Spun „hu-hu”."],
    "pinguinul": ["Am pene, dar nu zbor.", "Trăiesc unde e foarte frig.", "Merg legănat și înot excelent."],
    "delfinul": ["Trăiesc în mare, dar nu sunt pește.", "Îmi place să sar din apă.", "Vorbesc prin fluierături."],
    "albina": ["Sunt mică și zbor din floare în floare.", "Fac miere.", "Spun „bzzz”."],
    "melcul": ["Îmi port casa în spinare.", "Merg foarte, foarte încet.", "Ies afară după ploaie."],
    "calul": ["Alerg foarte repede și am coamă.", "Oamenii mă călăresc.", "Mănânc fân și ovăz."],
    "oaia": ["Am lână moale și creață.", "Trăiesc în turmă.", "Spun „behehe”."],
    "porcul": ["Am un nas rotund, numit rât.", "Îmi place să mă tăvălesc în noroi.", "Spun „guiț-guiț”."],
    "cocoșul": ["Am o creastă roșie.", "Cânt dimineața devreme.", "Spun „cucurigu”."],
    "maimuța": ["Mă cațăr în copaci.", "Îmi plac bananele.", "Fac multe năzbâtii."],
    "crocodilul": ["Am mulți dinți ascuțiți.", "Stau în râu și par un buștean.", "Am pielea solzoasă."],
    "fluturele": ["Cândva am fost omidă.", "Am aripi colorate.", "Zbor din floare în floare."],
    "veverița": ["Am o coadă mare și pufoasă.", "Strâng alune pentru iarnă.", "Sar din creangă în creangă."],
    "ariciul": ["Am țepi pe spate.", "Când mă sperii, mă fac ghem.", "Ies noaptea să caut gâze."],
}

# obiecte pentru jocul de numărat (substantiv plural, formă)
OBIECTE = {
    "steluțe": "stea",
    "inimioare": "inima",
    "cerculețe": "cerc",
    "pătrățele": "patrat",
    "triunghiuri": "triunghi",
}
CULORI = {
    # nume la plural: culoare RGB
    "roșii": (226, 60, 60),
    "albastre": (52, 120, 230),
    "galbene": (245, 200, 40),
    "verzi": (60, 180, 90),
    "mov": (150, 80, 200),
    "portocalii": (245, 140, 40),
}
NUMERE = {1: "unu", 2: "două", 3: "trei", 4: "patru", 5: "cinci", 6: "șase",
          7: "șapte", 8: "opt", 9: "nouă", 10: "zece"}

LITERE = {
    "A": ["albină", "avion", "ardei"], "B": ["barcă", "banană", "bunică"],
    "C": ["casă", "cățel", "creion"], "D": ["delfin", "dovleac", "dulap"],
    "E": ["elefant", "elicopter", "ecran"], "F": ["fluture", "floare", "furculiță"],
    "G": ["girafă", "gutuie", "ghiozdan"], "I": ["iepure", "iarbă", "insulă"],
    "L": ["leu", "lămâie", "lună"], "M": ["măr", "mașină", "munte"],
    "N": ["nor", "nas", "nucă"], "O": ["ou", "oaie", "ochelari"],
    "P": ["pisică", "pâine", "pom"], "R": ["rață", "roată", "rachetă"],
    "S": ["soare", "sanie", "scaun"], "T": ["tren", "tobă", "tată"],
    "U": ["urs", "umbrelă", "unghie"], "V": ["vulpe", "vapor", "vioară"],
    "Z": ["zebră", "zmeu", "zăpadă"],
}

INCHEIERI_JOC = [
    "Spune-i lui tata răspunsul tău!",
    "Jucați-vă din nou diseară, la apel!",
    "Ai ghicit? Bate palma cu tata!",
]

HASHTAGURI = {
    "poveste": "#cudragtata #tata #copii #povesti #povestipentrucopii #parinti",
    "sfat": "#cudragtata #tata #parinti #sfaturiparinti #copii #tatadedeparte",
    "joc": "#cudragtata #jocuricopii #jocuri #copii #educatie #tata",
}
