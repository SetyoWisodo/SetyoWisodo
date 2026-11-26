#!/usr/bin/env python3
"""Cari DOI untuk entri bibliografi lewat Crossref, dengan verifikasi judul.

Pemakaian:
    python3 tools/cari_doi.py            # laporan saja (tidak mengubah apa pun)
    python3 tools/cari_doi.py --tulis    # tulis DOI yang lolos verifikasi ke CSV

Aturan verifikasi (ketat, supaya tidak menebak):
  - kemiripan judul (token-set ratio) >= 0.86
  - tahun terbit selisih <= 1 tahun
  - nama belakang penulis pertama cocok (bila Crossref memberi penulis)

Entri yang tidak lolos dilaporkan sebagai "BELUM", bukan dipaksakan.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BIB = ROOT / "reference" / "bibliografi.csv"
CACHE = ROOT / ".gen" / "crossref_cache.json"
UA = "UnderstandingCrisis/1.0 (bibliography verification; mailto:none@example.org)"


def norm(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = s.replace("’", "'").replace("–", "-").replace("—", "-")
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    return " ".join(s.split())


def mirip(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def muat_cache() -> dict:
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def simpan_cache(c: dict) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")


def tanya_crossref(judul: str, penulis: str, tahun: str, cache: dict) -> dict | None:
    kunci = f"{norm(judul)}|{tahun}"
    if kunci in cache:
        return cache[kunci]
    q = urllib.parse.urlencode(
        {
            "query.bibliographic": f"{judul} {penulis} {tahun}",
            "rows": "5",
            "select": "DOI,title,container-title,volume,page,issued,author,type",
        }
    )
    url = f"https://api.crossref.org/works?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as fh:
            data = json.load(fh)
    except Exception as exc:  # noqa: BLE001
        print(f"    ! gagal kueri: {exc}", file=sys.stderr)
        return None
    items = data.get("message", {}).get("items", [])
    cache[kunci] = {"items": items}
    time.sleep(0.35)  # sopan ke API
    return cache[kunci]


def pilih_terbaik(items: list[dict], judul: str, penulis: str, tahun: str) -> tuple[dict | None, float]:
    terbaik, skor_terbaik = None, 0.0
    for it in items:
        t = (it.get("title") or [""])[0]
        s = mirip(judul, t)
        th = it.get("issued", {}).get("date-parts", [[None]])[0][0]
        if th and tahun:
            try:
                if abs(int(str(th)[:4]) - int(str(tahun)[:4])) > 1:
                    s -= 0.25
            except ValueError:
                pass
        fam = ""
        au = it.get("author") or []
        if au:
            fam = (au[0].get("family") or "").lower()
        if fam and penulis:
            fam_csv = norm(penulis).split(",")[0].split()[0]
            if fam_csv and fam_csv[:5] not in fam and fam[:5] not in fam_csv:
                s -= 0.2
        if s > skor_terbaik:
            terbaik, skor_terbaik = it, s
    return terbaik, skor_terbaik


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tulis", action="store_true")
    ap.add_argument("--ambang", type=float, default=0.86)
    a = ap.parse_args()

    with BIB.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    bidang = list(rows[0].keys())
    cache = muat_cache()

    belum, dapat = [], 0
    for r in rows:
        if r["identifier"].strip() and "doi" in r["identifier"].lower():
            continue
        judul, penulis, tahun = r["judul"], r["penulis"], r["tahun"]
        # tahun bisa berakhiran a/b (mis. 2022a)
        tahun_bersih = re.sub(r"[a-z]$", "", tahun)
        res = tanya_crossref(judul, penulis, tahun_bersih, cache)
        if res is None:
            belum.append((r["kunci"], "--", "kueri gagal"))
            continue
        it, skor = pilih_terbaik(res["items"], judul, penulis, tahun_bersih)
        if it and skor >= a.ambang:
            doi = it["DOI"]
            cont = (it.get("container-title") or [""])[0]
            print(f"OK   {r['kunci']:16} {skor:.2f}  {doi:38} {cont[:40]}")
            r["identifier"] = f"doi:{doi}"
            dapat += 1
        else:
            kandidat = ""
            if it:
                kandidat = f"{it.get('DOI')} | {(it.get('title') or [''])[0][:50]} | {skor:.2f}"
            print(f"BELUM {r['kunci']:16} ---- {kandidat}")
            belum.append((r["kunci"], kandidat, "di bawah ambang"))

    simpan_cache(cache)
    print(f"\nDOI baru: {dapat} | belum: {len(belum)}")

    if a.tulis and dapat:
        with BIB.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=bidang)
            w.writeheader()
            w.writerows(rows)
        print(f"Ditulis ke {BIB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
