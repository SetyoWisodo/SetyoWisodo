# -*- coding: utf-8 -*-
"""Peta paragraf -> modul sumber, untuk kerja deduplikasi paragraf.

Mencetak, untuk setiap paragraf yang terlibat dalam pasangan duplikat
(skor >= ambang), modul sumber dan nomor barisnya.
"""
import glob
import io
import re
import sys

sys.path.insert(0, ".")
import audit_redundancy as ar


def sources_snapshot():
    """{(file, line): teks literal} untuk semua modul konten."""
    out = {}
    for f in sorted(glob.glob("content/*.py") + glob.glob("content_id/*.py") + ["gen_book.py", "gen_book_id.py"]):
        for n, ln in enumerate(io.open(f, encoding="utf-8"), 1):
            s = ln.strip()
            if s.startswith('"') and len(s) > 80:
                out[(f, n)] = s.strip(",")
    return out


def key(text, n=9):
    words = re.findall(r"[A-Za-zÀ-ÿ'’]+", text)
    return " ".join(w.lower() for w in words[:n])


def locate(text, snap):
    k = key(text)
    hits = []
    for (f, n), lit in snap.items():
        lk = key(lit)
        if lk and (lk == k or (k.startswith(lk[:40]) and len(lk) > 40) or k[:40] in lk):
            hits.append((f, n, len(lit)))
    return hits


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "book.md"
    thr = 6.0
    for a in sys.argv[2:]:
        if a.startswith("--thr="):
            thr = float(a.split("=")[-1])
    lang = "id" if "id" in path.replace("book_id", "id").replace("book.md", "en") else "en"
    sig, hits = ar.scan(path, lang, top=500)
    paras = {}
    for score, jr, nums, names, a, b in hits:
        if score >= thr:
            paras.setdefault(a, []).append((score, b))
            paras.setdefault(b, []).append((score, a))
    snap = sources_snapshot()
    print("%s: %d paragraf unik pada ambang %.1f" % (path, len(paras), thr))
    for i, (idx, partners) in enumerate(sorted(paras.items())):
        p = sig[idx]
        loc = locate(p["text"], snap)
        print("\n[%02d] §%s  (skor maks %.1f, %d pasangan)" % (i, p["head"], max(s for s, _ in partners), len(partners)))
        print("     lokasi:", loc if loc else "TIDAK DITEMUKAN")
        print("     teks  :", p["text"][:180])


if __name__ == "__main__":
    main()
