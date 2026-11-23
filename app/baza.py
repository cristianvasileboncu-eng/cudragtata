# -*- coding: utf-8 -*-
"""Istoric în SQLite: video-uri generate și postări (împiedică duplicatele)."""
import datetime
import json
import os
import sqlite3

from .setari import DATE

CALE = os.path.join(DATE, "istoric.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS video (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  creat TEXT NOT NULL,
  zi TEXT NOT NULL,
  slot INTEGER,               -- 0,1,2 pentru video-urile zilnice; NULL = manual
  categorie TEXT, tema TEXT,
  fingerprint TEXT UNIQUE NOT NULL,
  componente TEXT, titlu TEXT, descriere TEXT,
  fisier TEXT, durata REAL, voce TEXT,
  cloud_url TEXT, cloud_id TEXT, cloud_sters INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS postare (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  video_id INTEGER NOT NULL,
  platforma TEXT NOT NULL,
  canal_id TEXT, buffer_id TEXT,
  status TEXT NOT NULL,       -- in_curs | programat | simulat | eroare | verifica
  programat_la TEXT,          -- ora locală ISO
  mesaj TEXT, creat TEXT,
  incercari INTEGER DEFAULT 0,
  UNIQUE(video_id, platforma)
);
"""


def conectare():
    c = sqlite3.connect(CALE, timeout=30)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    return c


def acum():
    return datetime.datetime.now().isoformat(timespec="seconds")


def azi():
    return datetime.date.today().isoformat()


def exista_fp(fp):
    with conectare() as c:
        return c.execute("SELECT 1 FROM video WHERE fingerprint=?", (fp,)).fetchone() is not None


def componente_recente(n=30):
    with conectare() as c:
        rows = c.execute("SELECT componente, tema FROM video ORDER BY id DESC LIMIT ?", (n,)).fetchall()
    comp, teme = set(), []
    for r in rows:
        comp.update(json.loads(r["componente"] or "[]"))
        teme.append(r["tema"])
    return comp, teme


def adauga_video(sc, fisier, durata, voce, slot=None, zi=None):
    with conectare() as c:
        cur = c.execute(
            "INSERT INTO video(creat, zi, slot, categorie, tema, fingerprint, componente, titlu, descriere, fisier, durata, voce)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (acum(), zi or azi(), slot, sc["categorie"], sc["tema"], sc["fingerprint"],
             json.dumps(sc["componente"], ensure_ascii=False), sc["titlu"], sc["descriere"],
             fisier, durata, voce))
        return cur.lastrowid


def video_zi(zi):
    with conectare() as c:
        return c.execute("SELECT * FROM video WHERE zi=? AND slot IS NOT NULL ORDER BY slot", (zi,)).fetchall()


def video(vid):
    with conectare() as c:
        return c.execute("SELECT * FROM video WHERE id=?", (vid,)).fetchone()


def ultimele_video(n=30):
    with conectare() as c:
        return c.execute("SELECT * FROM video ORDER BY id DESC LIMIT ?", (n,)).fetchall()


def postari_video(vid):
    with conectare() as c:
        return c.execute("SELECT * FROM postare WHERE video_id=?", (vid,)).fetchall()


def postare(vid, platforma):
    with conectare() as c:
        return c.execute("SELECT * FROM postare WHERE video_id=? AND platforma=?", (vid, platforma)).fetchone()


def postari_in_zi(platforma, zi, reale=True):
    st = ("in_curs", "programat", "verifica") if reale else ("simulat",)
    with conectare() as c:
        q = "SELECT COUNT(*) FROM postare WHERE platforma=? AND substr(programat_la,1,10)=? AND status IN (%s)" % ",".join("?" * len(st))
        return c.execute(q, (platforma, zi, *st)).fetchone()[0]


def rezerva_postare(vid, platforma, canal_id, programat_la, status="in_curs"):
    """Scrie postarea ÎNAINTE de apelul către Buffer. Dacă există deja, refuză."""
    with conectare() as c:
        ex = c.execute("SELECT status, incercari FROM postare WHERE video_id=? AND platforma=?", (vid, platforma)).fetchone()
        incercari = 0
        if ex:
            if ex["status"] == "eroare" and status != "simulat" and (ex["incercari"] or 0) < 3:
                incercari = (ex["incercari"] or 0) + 1
                c.execute("DELETE FROM postare WHERE video_id=? AND platforma=?", (vid, platforma))
            elif ex["status"] == "simulat" and status != "simulat":
                c.execute("DELETE FROM postare WHERE video_id=? AND platforma=?", (vid, platforma))
            else:
                return False
        c.execute("INSERT INTO postare(video_id, platforma, canal_id, status, programat_la, creat, incercari) VALUES (?,?,?,?,?,?,?)",
                  (vid, platforma, canal_id, status, programat_la, acum(), incercari))
        return True


def actualizeaza_postare(vid, platforma, **kw):
    if not kw:
        return
    campuri = ", ".join(f"{k}=?" for k in kw)
    with conectare() as c:
        c.execute(f"UPDATE postare SET {campuri} WHERE video_id=? AND platforma=?", (*kw.values(), vid, platforma))


def actualizeaza_video(vid, **kw):
    campuri = ", ".join(f"{k}=?" for k in kw)
    with conectare() as c:
        c.execute(f"UPDATE video SET {campuri} WHERE id=?", (*kw.values(), vid))


def marcheaza_intrerupte():
    """După o repornire: postările rămase „in_curs” NU se reîncearcă automat
    (s-ar putea să fi ajuns deja în Buffer). Le marcăm pentru verificare manuală."""
    with conectare() as c:
        n = c.execute("UPDATE postare SET status='verifica', mesaj='Întrerupt în timpul trimiterii – verifică în Buffer' WHERE status='in_curs'").rowcount
    return n


def istoric(n=60):
    with conectare() as c:
        vs = c.execute("SELECT * FROM video ORDER BY id DESC LIMIT ?", (n,)).fetchall()
        rez = []
        for v in vs:
            ps = c.execute("SELECT platforma, status, programat_la, mesaj FROM postare WHERE video_id=?", (v["id"],)).fetchall()
            d = dict(v)
            d["postari"] = [dict(p) for p in ps]
            rez.append(d)
        return rez


def sterge_video(vid):
    with conectare() as c:
        c.execute("DELETE FROM postare WHERE video_id=?", (vid,))
        c.execute("DELETE FROM video WHERE id=?", (vid,))
