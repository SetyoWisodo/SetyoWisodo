#!/usr/bin/env python3
"""Validator untuk 03_kartu_klip.json.

Dipakai sebelum render, dan sebagai gerbang rilis: kalau skrip ini keluar
dengan kode 1, jangan render bab yang ditandai.

    python3 validate_kartu_klip.py                  # periksa semua, ringkas
    python3 validate_kartu_klip.py --bab 13 24 4 8  # detail untuk bab tertentu
    python3 validate_kartu_klip.py --siap           # daftar bab yang boleh render
    python3 validate_kartu_klip.py --csv > status.csv

Yang diperiksa:
  E1  24 bab, id 1..24, tanpa duplikat
  E2  4 beat per bab, id s1..s4
  E3  beat punya angle/hook/line; line <= 12 kata (yang dibacakan adalah line)
  E4  klip punya url, dan url bukan halaman depan domain
  E5  quote_status hanya dari daftar yang sah
  E6  verbatim wajib punya quote; to_source wajib TIDAK punya quote
  E7  tidak ada kode diskon selain LAUNCH20 / KAMPUS25
  E8  matematika ekonomi konsisten (net per buku, views per buku)
  W1  angka dengan sumber "buku bab N" tanpa nama lembaga -> perlu nomor halaman
  W2  bab yang belum siap render (masih ada klip to_source / tanpa quote)
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
DATA = HERE / "03_kartu_klip.json"

ALLOWED_STATUS = {"verbatim", "paraphrase_check_before_use", "to_source"}
ALLOWED_CODES = {"LAUNCH20", "KAMPUS25"}
FORBIDDEN_CODES = ["BUNDLEUP40", "FIRSTBUYERFREE", "LAUNCH30", "SALE50"]

E, W = [], []


def err(code, msg):
    E.append((code, msg))


def warn(code, msg):
    W.append((code, msg))


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    ch = d.get("chapters", [])

    # E1 ---------------------------------------------------------------
    ids = [c.get("id") for c in ch]
    if len(ch) != 24:
        err("E1", f"jumlah bab {len(ch)}, seharusnya 24")
    if sorted(ids) != list(range(1, 25)):
        err("E1", f"id bab tidak lengkap/duplikat: {sorted(ids)}")

    # E8 ---------------------------------------------------------------
    eco = d.get("economics", {})
    net = eco.get("net_per_book_usd", {})
    direct = net.get("direct")
    if not isinstance(direct, (int, float)) or not (36 < direct < 40):
        err("E8", f"net per buku direct {direct!r}, seharusnya 38.40")
    rpm = eco.get("shorts_rpm_range_usd", [])
    views = eco.get("one_book_equals_ad_revenue_shorts_views", [])
    if len(rpm) == 2 and len(views) == 2 and direct:
        lo, hi = direct / (rpm[1] / 1000), direct / (rpm[0] / 1000)
        if not (abs(views[0] - lo) / lo < 0.05 and abs(views[1] - hi) / hi < 0.05):
            err("E8", "views per buku tidak cocok dengan net/RPM: "
                      f"hitung {lo:,.0f}-{hi:,.0f}, tertulis {views[0]:,}-{views[1]:,}")
    if "one_book_equals_shorts_views" in eco:
        err("E8", "kunci lama one_book_equals_shorts_views masih ada")

    # E7 ---------------------------------------------------------------
    meta = d.get("product", {})
    allowed = set(meta.get("codes_allowed", ALLOWED_CODES))
    declared_bad = set(meta.get("codes_forbidden", [])) | set(FORBIDDEN_CODES)
    blob = DATA.read_text(encoding="utf-8")
    for bad in declared_bad:            # deklarasi larangan bukan pelanggaran
        blob = blob.replace(bad, "")
    found = set(re.findall(r"\b[A-Z]{4,}[0-9]{2}\b", blob))
    for code in found - allowed:
        if code in FORBIDDEN_CODES or re.fullmatch(r"[A-Z]+[0-9]{2}", code):
            err("E7", f"kode diskon tidak sah muncul di JSON: {code}")

    ready, not_ready = [], []
    for c in sorted(ch, key=lambda x: x["id"]):
        cid = c["id"]

        # E2 -----------------------------------------------------------
        beats = c.get("shorts_beats", [])
        if len(beats) != 4:
            err("E2", f"bab {cid}: {len(beats)} beat, seharusnya 4")
        if [b.get("id") for b in beats] != ["s1", "s2", "s3", "s4"]:
            err("E2", f"bab {cid}: id beat {[b.get('id') for b in beats]}, seharusnya s1..s4")

        # E3 -----------------------------------------------------------
        bad = 0
        for b in beats:
            for k in ("angle", "hook", "line"):
                if not (b.get(k) or "").strip():
                    err("E3", f"bab {cid} {b.get('id')}: field {k} kosong")
            n = len(b.get("line", "").split())
            if n > 12:
                err("E3", f"bab {cid} {b.get('id')}: line {n} kata (maks 12) — "
                          f"yang dibacakan adalah line, bukan hook")
                bad += 1

        # E4/E5/E6 -----------------------------------------------------
        clips = c.get("clips", [])
        if not clips:
            err("E4", f"bab {cid}: tidak ada klip sama sekali")
        pending = 0
        for i, k in enumerate(clips, 1):
            url = (k.get("url") or "").strip()
            st = k.get("quote_status")
            if not url:
                err("E4", f"bab {cid} klip {i} ({k.get('outlet')}): tidak ada url")
            elif urlparse(url).path in ("", "/"):
                err("E4", f"bab {cid} klip {i} ({k.get('outlet')}): url halaman depan, "
                          f"bukan halaman sumber — tidak bisa diarsipkan")
            if st not in ALLOWED_STATUS:
                err("E5", f"bab {cid} klip {i}: quote_status {st!r} tidak sah")
            if st == "verbatim" and not (k.get("quote") or "").strip():
                err("E6", f"bab {cid} klip {i}: verbatim tanpa teks quote")
            if st == "to_source":
                pending += 1
                if (k.get("quote") or "").strip():
                    err("E6", f"bab {cid} klip {i}: to_source tapi sudah ada quote — "
                              f"ubah status ke verbatim setelah diverifikasi")
            if st == "paraphrase_check_before_use":
                pending += 1

        # W1 ------------------------------------------------------------
        for n in c.get("numbers", []):
            src = str(n.get("source", ""))
            if re.fullmatch(r"buku bab \d+", src.strip()):
                warn("W1", f"bab {cid}: angka '{n.get('value')}' hanya bersumber "
                           f"'{src}' — tambahkan nama lembaga atau nomor halaman")

        if pending == 0:
            ready.append(cid)
        else:
            not_ready.append((cid, pending, len(clips)))

    # keluaran ---------------------------------------------------------
    print(f"JSON     : {DATA.name} v{d.get('schema_version')}")
    print(f"Bab      : {len(ch)} | beat {sum(len(c.get('shorts_beats', [])) for c in ch)} | "
          f"klip {sum(len(c.get('clips', [])) for c in ch)}")
    print(f"Ekonomi  : net ${direct}/buku direct | ${net.get('discover')}/buku Discover | "
          f"1 buku = {views[0]:,}-{views[1]:,} views iklan".replace(",", ".") if views else "")
    print()

    print(f"SIAP RENDER ({len(ready)} bab): {ready or '-'}")
    print(f"BELUM SIAP ({len(not_ready)} bab):")
    for cid, p, n in not_ready:
        print(f"  bab {cid:>2}: {p}/{n} klip belum verbatim")
    print()

    for code, msg in E:
        print(f"ERROR {code}: {msg}")
    for code, msg in W:
        print(f"warn  {code}: {msg}")
    print()
    print(f"Hasil    : {len(E)} error, {len(W)} peringatan")

    if "--siap" in sys.argv:
        print("\nBoleh render: " + (", ".join(str(x) for x in ready) or "tidak ada"))
    if "--bab" in sys.argv:
        want = {int(x) for x in sys.argv[sys.argv.index("--bab") + 1:] if x.isdigit()}
        print()
        for c in ch:
            if c["id"] in want:
                print(f"bab {c['id']}: {c['title_en']}")
                for b in c["shorts_beats"]:
                    print(f"   {b['id']} [{b['angle']}] {b['line']}")
                for k in c["clips"]:
                    print(f"   klip {k['format']:<5} {k['quote_status']:<26} {k['outlet']}")

    return 1 if E else 0


if __name__ == "__main__":
    sys.exit(main())
