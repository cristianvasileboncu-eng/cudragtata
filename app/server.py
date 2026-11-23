# -*- coding: utf-8 -*-
"""Interfața din telefon: http://127.0.0.1:8765 (doar pe telefonul tău)."""
import json
import os
import re
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from . import baza
from .automat import Automat
from .setari import DATE, RADACINA, VIDEO, config, log, salveaza_stare, secrete, stare, ultimele_linii

AUTOMAT = Automat()
JOB = {"activ": False, "procent": 0, "mesaj": "", "ultim_id": None, "eroare": ""}
TIPURI = ("text", "emotie", "reclama", "poveste", "sfat", "joc", "poza_citat", "poza_sfat", "poza_joc")


def _genereaza(tip):
    JOB.update(activ=True, procent=0, mesaj="Pornesc...", eroare="")
    try:
        if tip.startswith("poza_"):
            from .poze import genereaza_poza
            vid = genereaza_poza(tip)
        else:
            from .generator import genereaza
            vid = genereaza(tip, progres=lambda p, m: JOB.update(procent=int(p), mesaj=m))
        JOB.update(ultim_id=vid, mesaj="Gata! Apasă „Previzualizează”.", procent=100)
    except Exception as e:
        from .randare import Oprit
        JOB.update(eroare="Oprit." if isinstance(e, Oprit) else str(e), mesaj="")
        if not isinstance(e, Oprit):
            log(f"Eroare la generare: {e}\n{traceback.format_exc()[-600:]}", "ERROR")
    finally:
        JOB["activ"] = False


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, obj, cod=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(cod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            with open(os.path.join(os.path.dirname(__file__), "ui.html"), "rb") as f:
                b = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
        elif u.path == "/api/stare":
            cfg, s = config(), secrete()
            st = stare()
            self._json({
                "job": JOB, "automat": AUTOMAT.activ(), "lucru_automat": st.get("lucru", ""),
                "ultima_verificare": st.get("ultima_verificare"),
                "real": cfg["publicare"].get("publicare_reala", False),
                "buffer": bool(s.get("BUFFER_API_KEY")), "cloudinary": bool(s.get("CLOUDINARY_CLOUD_NAME")),
                "jurnal": ultimele_linii(25)})
        elif u.path == "/api/istoric":
            rows = baza.istoric(60)
            for r in rows:
                r["nume_fisier"] = os.path.basename(r["fisier"] or "")
                r["exista"] = bool(r["fisier"]) and os.path.exists(r["fisier"])
            self._json(rows)
        elif u.path.startswith("/media/"):
            self._media(u.path[len("/media/"):])
        else:
            self._json({"eroare": "nu există"}, 404)

    def _media(self, nume):
        if not re.fullmatch(r"[\w\-.]+\.(mp4|jpg)", nume):
            return self._json({"eroare": "nume invalid"}, 400)
        cale = os.path.join(VIDEO, nume)
        if not os.path.exists(cale):
            return self._json({"eroare": "lipsește"}, 404)
        marime = os.path.getsize(cale)
        tip = "video/mp4" if nume.endswith(".mp4") else "image/jpeg"
        rng = self.headers.get("Range")
        start, end = 0, marime - 1
        if rng and rng.startswith("bytes="):
            a, _, b = rng[6:].partition("-")
            start = int(a) if a else 0
            end = int(b) if b else marime - 1
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {start}-{end}/{marime}")
        else:
            self.send_response(200)
        self.send_header("Content-Type", tip)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        with open(cale, "rb") as f:
            f.seek(start)
            rest = end - start + 1
            while rest > 0:
                bucata = f.read(min(65536, rest))
                if not bucata:
                    break
                try:
                    self.wfile.write(bucata)
                except (BrokenPipeError, ConnectionResetError):
                    return
                rest -= len(bucata)

    def do_POST(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/api/genereaza":
            tip = (q.get("tip") or ["poveste"])[0]
            if tip not in TIPURI:
                return self._json({"eroare": "tip necunoscut"}, 400)
            if JOB["activ"]:
                return self._json({"eroare": "Se generează deja ceva."}, 409)
            threading.Thread(target=_genereaza, args=(tip,), daemon=True).start()
            self._json({"ok": True})
        elif u.path == "/api/auto/porneste":
            salveaza_stare(automat=True)
            AUTOMAT.porneste_fir()
            self._json({"ok": True})
        elif u.path == "/api/opreste":
            salveaza_stare(automat=False)
            AUTOMAT.opreste()
            from .randare import OPRIRE
            OPRIRE.set()
            log("Oprit din interfață.")
            self._json({"ok": True})
        else:
            self._json({"eroare": "nu există"}, 404)


def main():
    port = config().get("port", 8765)
    with open(os.path.join(DATE, "server.pid"), "w") as f:
        f.write(str(os.getpid()))
    if stare().get("automat"):
        log("Publicarea automată era pornită → o reiau.")
        AUTOMAT.porneste_fir()
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    log(f"Interfața rulează: http://127.0.0.1:{port}")
    srv.serve_forever()


if __name__ == "__main__":
    main()
