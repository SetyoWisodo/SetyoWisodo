#!/usr/bin/env python3
"""
Jalankan seluruh pipeline otomatis, berurutan, dengan laporan waktu.

Urutan penting: aset dulu, halaman turunan setelahnya, papan setelah data berubah,
periksa paling akhir (gerbang), lalu laporan.

    1. brandkit   label 70×100 mm, OG card, logo, halaman brand
    2. komersial  harga grosir 4 tier + penawaran B2B
    3. kreatif    5 video 9:16, carousel, story, feed, hub konten
    4. kampanye   landing kampanye dari katalog + manifest
    5. riset      outlier, pola, komentar, kata kunci → brief
    6. papan      dashboard harian + target divisi
    7. periksa    gerbang QA (berhenti bila ada temuan kritis)
    8. laporan    satu halaman ringkasan untuk dinilai

Pakai:
    python3 tools/jalankan.py                 # semua langkah
    python3 tools/jalankan.py --cepat         # lewati encode video (kreatif --cepat)
    python3 tools/jalankan.py --tanpa-brand   # lewati brandkit (lambat, aset jarang berubah)
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TGL = hari_ini().isoformat()


def langkah(nama, perintah, wajib=True):
    mulai = time.time()
    hasil = subprocess.run([sys.executable] + perintah, cwd=ROOT, capture_output=True, text=True)
    durasi = time.time() - mulai
    keluaran = (hasil.stdout or "").strip().splitlines()
    baris_akhir = next((b for b in reversed(keluaran) if b.strip()), "")
    ok = hasil.returncode == 0
    print(f"  {'OK ' if ok else 'XX '}{nama:<10} {durasi:5.1f}s  {baris_akhir[:88]}")
    if not ok and wajib:
        print("     → berhenti. keluaran terakhir:")
        for b in (hasil.stdout or hasil.stderr or "").strip().splitlines()[-8:]:
            print("       " + b)
        raise SystemExit(1)
    return ok, durasi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cepat", action="store_true", help="lewati encode video")
    ap.add_argument("--tanpa-brand", action="store_true", help="lewati brandkit")
    args = ap.parse_args()

    t0 = time.time()
    print(f"Pipeline Nocturne — {TGL}")
    print("─" * 78)

    langkah_list = []
    if not args.tanpa_brand:
        langkah_list.append(("brandkit", ["tools/brandkit.py", "--tanggal", TGL, "--batch", "A"]))
    langkah_list += [
        ("komersial", ["tools/komersial.py", "--tanggal", TGL]),
        ("kreatif", ["tools/kreatif.py"] + (["--cepat"] if args.cepat else [])),
        ("kampanye", ["tools/kampanye.py"]),
        ("riset", ["tools/riset.py"]),
        ("papan", ["tools/papan.py", "--tanggal", TGL]),
        ("periksa", ["tools/periksa.py"]),
        ("laporan", ["tools/laporan.py"]),
    ]

    total = 0.0
    for nama, cmd in langkah_list:
        _, d = langkah(nama, cmd)
        total += d

    print("─" * 78)
    print(f"Selesai dalam {time.time()-t0:.0f} detik ({len(langkah_list)} langkah).")
    print("Buka:")
    print("  laporan/index.html          ← ringkasan untuk dinilai")
    print("  dashboard/index.html        ← papan harian + target divisi")
    print("  index.html                  ← situs")
    print("  kampanye/index.html         ← landing kampanye konten")
    print("  konten/index.html           ← 15 aset + caption")
    print("  riset/index.html            ← riset konten & kata kunci")
    print("Jalankan server: python3 -m http.server 8080")


if __name__ == "__main__":
    main()
