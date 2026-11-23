# -*- coding: utf-8 -*-
"""Publicare: Cloudinary Free (link public) + Buffer API (GraphQL, cheie personală).

Doar biblioteca standard Python (fără pachete extra).
"""
import datetime
import hashlib
import json
import mimetypes
import os
import time
import urllib.error
import urllib.request
import uuid

from . import baza
from .setari import DATE, config, log, secrete
from .texte import legenda, titlu_youtube

BUFFER_URL = "https://api.buffer.com"
CANALE = os.path.join(DATE, "canale.json")


class EroarePublicare(Exception):
    pass


class EroareRetea(EroarePublicare):
    """Conexiunea s-a rupt: nu știm sigur dacă cererea a ajuns."""


def _http(url, data=None, headers=None, timeout=120):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        corp = e.read().decode("utf-8", "replace")[:500]
        if e.code == 429:
            raise EroarePublicare(f"Limită de cereri atinsă (429). Reîncerc mai târziu. {corp}")
        raise EroarePublicare(f"HTTP {e.code}: {corp}")
    except urllib.error.URLError as e:
        raise EroareRetea(f"Fără conexiune: {e.reason}")
    except (TimeoutError, OSError) as e:
        raise EroareRetea(f"Conexiune întreruptă: {e}")


# ------------------------------------------------------------------ Cloudinary
class Cloudinary:
    def __init__(self):
        s = secrete()
        self.cloud = s.get("CLOUDINARY_CLOUD_NAME")
        self.key = s.get("CLOUDINARY_API_KEY")
        self.secret = s.get("CLOUDINARY_API_SECRET")
        if not (self.cloud and self.key and self.secret):
            raise EroarePublicare("Cloudinary nu e configurat în secrete.env")

    def _semnatura(self, params):
        s = "&".join(f"{k}={params[k]}" for k in sorted(params))
        return hashlib.sha1((s + self.secret).encode()).hexdigest()

    def incarca(self, cale, public_id):
        tip = "video" if cale.endswith(".mp4") else "image"
        params = {"folder": "cudragtata", "public_id": public_id, "timestamp": str(int(time.time()))}
        params["signature"] = self._semnatura(params)
        params["api_key"] = self.key
        granita = uuid.uuid4().hex
        corp = []
        for k, v in params.items():
            corp.append(f'--{granita}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
        mime = mimetypes.guess_type(cale)[0] or "application/octet-stream"
        corp.append(f'--{granita}\r\nContent-Disposition: form-data; name="file"; filename="{os.path.basename(cale)}"\r\n'
                    f"Content-Type: {mime}\r\n\r\n".encode())
        with open(cale, "rb") as f:
            corp.append(f.read())
        corp.append(f"\r\n--{granita}--\r\n".encode())
        r = _http(f"https://api.cloudinary.com/v1_1/{self.cloud}/{tip}/upload", b"".join(corp),
                  {"Content-Type": f"multipart/form-data; boundary={granita}"}, timeout=300)
        if "secure_url" not in r:
            raise EroarePublicare(f"Cloudinary nu a returnat link: {r}")
        return r["secure_url"], r["public_id"], tip

    def sterge(self, public_id, tip):
        params = {"public_id": public_id, "timestamp": str(int(time.time()))}
        params["signature"] = self._semnatura(params)
        params["api_key"] = self.key
        data = "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in params.items()).encode()
        return _http(f"https://api.cloudinary.com/v1_1/{self.cloud}/{tip}/destroy", data,
                     {"Content-Type": "application/x-www-form-urlencoded"})


# ------------------------------------------------------------------ Buffer
class Enum(str):
    """Valoare GraphQL scrisă fără ghilimele (ex.: customScheduled)."""


def _gql(v):
    if isinstance(v, Enum):
        return str(v)
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return "[" + ", ".join(_gql(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{k}: {_gql(x)}" for k, x in v.items()) + "}"
    raise TypeError(type(v))


class Buffer:
    def __init__(self):
        self.cheie = secrete().get("BUFFER_API_KEY")
        if not self.cheie:
            raise EroarePublicare("Buffer nu e configurat în secrete.env")

    def cerere(self, query):
        r = _http(BUFFER_URL, json.dumps({"query": query}).encode(),
                  {"Content-Type": "application/json", "Authorization": f"Bearer {self.cheie}"})
        if r.get("errors"):
            raise EroarePublicare("Buffer: " + "; ".join(e.get("message", "") for e in r["errors"]))
        return r["data"]

    def canale(self, reimprospatare=False):
        if not reimprospatare and os.path.exists(CANALE):
            with open(CANALE, encoding="utf-8") as f:
                return json.load(f)
        orgs = self.cerere("query { account { organizations { id name } } }")["account"]["organizations"]
        toate = []
        for o in orgs:
            q = 'query { channels(input: {organizationId: %s}) { id name displayName service isQueuePaused } }' % json.dumps(o["id"])
            toate += self.cerere(q)["channels"]
        with open(CANALE, "w", encoding="utf-8") as f:
            json.dump(toate, f, ensure_ascii=False, indent=1)
        return toate

    def canal_pentru(self, platforma):
        for c in self.canale():
            if platforma in (c.get("service") or "").lower():
                return c
        return None

    def posteaza(self, canal, platforma, text, url, este_video, cand_utc, titlu, categorie=""):
        cfg = config()["publicare"]
        asset = {"video": {"url": url}} if este_video else {"image": {"url": url}}
        inp = {"text": text, "channelId": canal["id"], "schedulingType": Enum("automatic"),
               "mode": Enum("customScheduled"), "dueAt": cand_utc, "assets": [asset]}
        meta = None
        if platforma == "youtube":
            yt = cfg.get("youtube", {})
            meta = {"youtube": {"title": titlu_youtube(titlu), "categoryId": str(yt.get("categorie", "22")),
                                "privacy": Enum(yt.get("confidentialitate", "public")),
                                "madeForKids": categorie in yt.get("pentru_copii_categorii", []),
                                "isAiGenerated": bool(cfg.get("marcheaza_ai", True))}}
        elif platforma == "instagram":
            meta = {"instagram": {"type": Enum("reel" if este_video else "post"), "shouldShareToFeed": True,
                                  "isAiGenerated": bool(cfg.get("marcheaza_ai", True))}}
        elif platforma == "tiktok":
            m = {"isAiGenerated": bool(cfg.get("marcheaza_ai", True))} if este_video else {"title": titlu[:90]}
            meta = {"tiktok": m}
        if meta:
            inp["metadata"] = meta
        q = ("mutation { createPost(input: %s) { ... on PostActionSuccess { post { id dueAt } } "
             "... on MutationError { message } } }") % _gql(inp)
        r = self.cerere(q)["createPost"]
        if "post" not in r or not r.get("post"):
            raise EroarePublicare("Buffer a refuzat: " + str(r.get("message")))
        return r["post"]["id"]


# ------------------------------------------------------------------ flux complet
PLATFORME = ("tiktok", "instagram", "youtube")


def ora_la_utc(local_dt):
    ts = time.mktime(local_dt.timetuple())
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def publica_element(vid, cand_local):
    """Programează un video/o poză pe platformele permise, fără dubluri.
    cand_local: datetime local la care să apară postarea."""
    cfg = config()
    pub = cfg["publicare"]
    real = pub.get("publicare_reala", False)
    v = baza.video(vid)
    if not v or not v["fisier"] or not os.path.exists(v["fisier"]):
        raise EroarePublicare(f"Fișierul pentru #{vid} lipsește.")
    este_video = v["fisier"].endswith(".mp4")
    zi = cand_local.date().isoformat()
    text = legenda(v["categorie"], v["titlu"], v["descriere"], cfg.get("site", "cudragtata.ro"), seed=v["fingerprint"])
    platforme = [p for p in PLATFORME if este_video or p != "youtube"]   # YouTube nu primește poze
    buf = Buffer() if real else None
    url = v["cloud_url"]
    rezultate = {}
    for p in platforme:
        ex = baza.postare(vid, p)
        if ex and ex["status"] in ("programat", "in_curs", "verifica"):
            continue
        if ex and ex["status"] == "simulat" and not real:
            continue
        limita = pub.get("limite_pe_zi", {}).get(p, 3)
        if baza.postari_in_zi(p, zi, reale=real) >= limita:
            rezultate[p] = "limită zilnică atinsă"
            continue
        canal = buf.canal_pentru(p) if real else {"id": "simulare"}
        if canal is None:
            rezultate[p] = "canal neconectat în Buffer"
            continue
        if not real:
            baza.rezerva_postare(vid, p, "simulare", cand_local.isoformat(timespec="minutes"), status="simulat")
            log(f"[SIMULARE] #{vid} → {p} la {cand_local:%H:%M}: {v['titlu']}")
            rezultate[p] = "simulat"
            continue
        if not url:
            c = Cloudinary()
            url, pid, tip = c.incarca(v["fisier"], f"{v['zi']}_{v['fingerprint']}")
            baza.actualizeaza_video(vid, cloud_url=url, cloud_id=f"{tip}:{pid}")
            log(f"#{vid} încărcat în Cloudinary.")
        if not baza.rezerva_postare(vid, p, canal["id"], cand_local.isoformat(timespec="minutes")):
            continue   # altcineva a rezervat deja → fără dublură
        try:
            bid = buf.posteaza(canal, p, text, url, este_video, ora_la_utc(cand_local), v["titlu"], v["categorie"])
            baza.actualizeaza_postare(vid, p, status="programat", buffer_id=bid, mesaj="")
            log(f"#{vid} programat pe {p} la {cand_local:%H:%M} (Buffer {bid}).")
            rezultate[p] = "programat"
        except EroareRetea as e:
            # nu știm dacă Buffer a primit cererea → NU reîncercăm automat (evităm dublura)
            baza.actualizeaza_postare(vid, p, status="verifica", mesaj=str(e)[:300])
            log(f"#{vid} pe {p}: conexiune întreruptă, verifică manual în Buffer.", "WARN")
            rezultate[p] = "verifica"
        except EroarePublicare as e:
            # răspuns clar de eroare de la Buffer → postarea NU s-a creat; se poate reîncerca
            baza.actualizeaza_postare(vid, p, status="eroare", mesaj=str(e)[:300])
            log(f"#{vid} eroare pe {p}: {e}", "ERROR")
            rezultate[p] = "eroare"
    return rezultate


def curata_cloudinary():
    cfg = config()
    zile = cfg["publicare"].get("sterge_din_cloudinary_dupa_zile", 3)
    limita = (datetime.date.today() - datetime.timedelta(days=zile)).isoformat()
    with baza.conectare() as c:
        rows = c.execute("SELECT id, cloud_id FROM video WHERE cloud_id IS NOT NULL AND cloud_sters=0 AND zi<?",
                         (limita,)).fetchall()
    if not rows:
        return
    cl = Cloudinary()
    for r in rows:
        tip, pid = r["cloud_id"].split(":", 1)
        try:
            cl.sterge(pid, tip)
            baza.actualizeaza_video(r["id"], cloud_sters=1)
            log(f"#{r['id']} șters din Cloudinary (economisim spațiul gratuit).")
        except EroarePublicare as e:
            log(f"Nu am putut șterge #{r['id']} din Cloudinary: {e}", "WARN")
