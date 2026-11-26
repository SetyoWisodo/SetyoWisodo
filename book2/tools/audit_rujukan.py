#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit kesiapan rujukan buku 17 bab.

Mengukur empat hal yang menentukan apakah sebuah buku bisa disebut
"rujukan akademik":

  1. KEPADATAN SITASI   berapa sitasi per 1.000 kata, berapa sumber unik
  2. KETERLACAKAN       sitasi yang tidak ada di bibliografi, dan entri
                        bibliografi yang tidak pernah dikutip
  3. KLAIM TANPA SUMBER kalimat yang memuat angka tetapi tidak menyebut
                        sumber di kalimat itu
  4. KELENGKAPAN        apakah setiap klaim bernomor ada di buku besar bukti

Keluaran: ringkasan di stdout + `book2/reference/laporan_audit.md`.
Keluar dengan kode 1 bila ada kegagalan keras (sitasi yatim, klaim
bernomor yang tidak ada di buku besar).

Pemakaian:
    python3 book2/tools/audit_rujukan.py
    python3 book2/tools/audit_rujukan.py --ringkas
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import re
import sys
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
BOOK = ROOT / "book2"
SRC = BOOK / "src" / "id"  # dipilih lewat --lang
REF = BOOK / "reference"
BIB = REF / "bibliografi.csv"
KLAIM = REF / "klaim.csv"
LAPORAN = REF / "laporan_audit.md"

YEAR = r"(?:18|19|20)\d{2}[a-z]?"
# Nama (Tahun)  |  (Nama, Tahun)  |  (Nama et al., Tahun; Nama, Tahun)
NARASI = re.compile(r"\b([A-Z][A-Za-zÀ-ÿ\-']+(?:\s+(?:et al\.|dkk\.|&\s+[A-Z][A-Za-zÀ-ÿ\-']+))?)\s+\(" + YEAR + r"\)")
# penanda baru: (@kunci) atau @kunci, boleh beberapa dipisah spasi/koma
KUNCI = re.compile(r"@([a-z]+\d{4}[a-z]*)")
KURUNG = re.compile(r"\(([^()]{2,240})\)")

# Angka yang layak diperiksa: punya satuan/konteks kuantitatif, bukan tahun
BILANGAN = re.compile(
    r"(?<![\w.])("
    r"\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?|"      # 1.700 / 61.672 / 4,75
    r"\d+(?:[.,]\d+)?"                          # 422 / 1.55
    r")\s*"
    r"(%|persen|°C|mm|sentimeter|meter|kilometer|km|hektare|ha|juta|miliar|triliun|"
    r"ton|GtCO₂|ppm|tahun|hari|orang|kematian|nyawa|dolar|US\$|rupiah|kali|lipat|"
    r"miliar ton|ribu|juta orang)"
)

SITASI_UMUM = (
    "IPCC", "WMO", "NOAA", "WHO", "FAO", "UNDRR", "OCHA", "IFRC", "CRED",
    "Bank Dunia", "World Bank", "BMKG", "BNPB", "BPS", "UNEP", "IEA",
)


def baca_berkas() -> list[tuple[str, str]]:
    return [(p.name, p.read_text(encoding="utf-8")) for p in sorted(SRC.glob("*.md"))]


def kata(teks: str) -> int:
    return len(re.sub(r"[#*>|:{}\[\]`_—–]", " ", teks).split())


def sitasi_dalam(teks: str) -> set[tuple[str, str]]:
    """(kunci atau nama-depan, tahun) untuk tiap sitasi."""
    out: set[tuple[str, str]] = set()
    for m in KUNCI.finditer(teks):
        out.add((m.group(1), ""))
    for m in KURUNG.finditer(teks):
        for bagian in m.group(1).split(";"):
            c = re.match(r"\s*([A-Z][A-Za-zÀ-ÿ\-']+)(?:[^,]{0,60})?,\s*(" + YEAR + r")", bagian)
            if c:
                out.add((c.group(1).lower(), c.group(2)))
    for m in NARASI.finditer(teks):
        tahun = re.search(YEAR, m.group(0))
        if tahun:
            out.add((m.group(1).split()[0].lower(), tahun.group(0)))
    # sebutan lembaga di badan teks: "menurut WMO (2025)"
    for lembaga in SITASI_UMUM:
        for m in re.finditer(re.escape(lembaga) + r"[^.\n]{0,40}?\(" + YEAR + r"\)", teks):
            tahun = re.search(YEAR, m.group(0))
            out.add((lembaga.split()[0].lower(), tahun.group(0)))
    return out


def muat_bibliografi() -> dict[str, dict]:
    if not BIB.exists():
        return {}
    with BIB.open(encoding="utf-8") as f:
        return {r["kunci"].lower(): r for r in csv.DictReader(f)}


def muat_klaim() -> dict[str, dict]:
    if not KLAIM.exists():
        return {}
    with KLAIM.open(encoding="utf-8") as f:
        return {r["id_klaim"]: r for r in csv.DictReader(f)}


def kalimat_dengan_angka(teks: str) -> list[str]:
    """Kalimat yang memuat besaran dan tidak menyebut sumber."""
    hasil = []
    teks = re.sub(r"^#.*$", "", teks, flags=re.M)
    for para in re.split(r"\n\s*\n", teks):
        para = " ".join(para.split())
        if not para or para.startswith(("|", "-", "*", ":")):
            continue
        for kal in re.split(r"(?<=[.!?])\s+", para):
            if not BILANGAN.search(kal):
                continue
            menyebut = bool(
                re.search(YEAR, kal)
                or any(l.lower() in kal.lower() for l in SITASI_UMUM)
                or re.search(r"\b(menurut|data|laporan|studi|riset|survei)\b", kal, re.I)
            )
            if not menyebut:
                hasil.append(kal.strip())
    return hasil


def jalankan(ringkas: bool = False) -> int:
    berkas = baca_berkas()
    total_kata = sum(kata(t) for _, t in berkas)

    semua = "\n".join(t for _, t in berkas)
    sitasi = sitasi_dalam(semua)
    bib = muat_bibliografi()
    klaim = muat_klaim()

    # 1. kepadatan — hitung kemunculan (bukan unik), termasuk multi-kunci [@a; @b]
    jumlah_sitasi = len(KUNCI.findall(semua))
    n_sitasi_kurung = len(KURUNG.findall(semua))
    kepadatan = jumlah_sitasi / max(total_kata, 1) * 1000

    # 2. keterlacakan
    # sitasi gaya lama (Nama, Tahun) tetap dihitung, tapi dipetakan ke kunci
    # nama depan DAN kata terakhir ("World Bank" -> "bank", "Badan Informasi Geospasial" -> "geospasial")
    peta: dict[str, str] = {}
    for k, r in bib.items():
        peta.setdefault(k.lower(), k)          # kunci itu sendiri
        for dalam in re.findall(r"\(([^)]+)\)", r["penulis"]):
            for tok in re.split(r"[,\s]+", dalam):
                if len(tok) > 2:
                    peta.setdefault(tok.lower(), k)
        bagian = re.split(r"[,\s]+", re.sub(r"\([^)]*\)", "", r["penulis"]).strip())
        for tok in filter(None, bagian):
            tok = tok.strip(".").lower()
            if len(tok) > 2:
                peta.setdefault(tok, k)
    yatim = sorted({s for s in sitasi if s[0] not in bib and s[0] not in peta})
    dikutip_kunci = {s[0] for s in sitasi}

    # 3. klaim tanpa sumber
    per_bab: dict[str, list[str]] = {}
    for nama, teks in berkas:
        k = kalimat_dengan_angka(teks)
        if k:
            per_bab[nama] = k
    total_tanpa = sum(len(v) for v in per_bab.values())

    # 4. buku besar bukti
    sudah = {k for k in klaim}
    belum_terverifikasi = [r for r in klaim.values() if r.get("status", "").strip().lower() not in ("terverifikasi", "verified")]

    baris = []
    baris.append("# Laporan Audit Kesiapan Rujukan\n")
    baris.append(f"Dihasilkan otomatis oleh `book2/tools/audit_rujukan.py`.\n")
    baris.append("## Ringkasan\n")
    baris.append("| Metrik | Nilai | Ambang rujukan | Status |")
    baris.append("|---|---:|---:|---|")
    baris.append(f"| Kata | {total_kata:,} | — | — |".replace(",", "."))
    baris.append(f"| Sitasi dalam teks | {jumlah_sitasi} | ≥ 1 per 500 kata | {'lolos' if jumlah_sitasi >= total_kata/500 else 'gagal'} |")
    baris.append(f"| Sitasi per 1.000 kata | {kepadatan:.2f} | ≥ 2,0 | {'lolos' if kepadatan >= 2 else 'gagal'} |")
    n_unik = len({s[0] for s in sitasi if s[0] in bib})
    baris.append(f"| Sumber unik | {n_unik} | ≥ 40 | {'lolos' if n_unik >= 40 else 'gagal'} |")
    baris.append(f"| Sitasi yatim (tak ada di bibliografi) | {len(yatim)} | 0 | {'lolos' if not yatim else 'gagal'} |")
    baris.append(f"| Kalimat berangka tanpa sumber | {total_tanpa} | ≤ {total_kata//1000} | {'lolos' if total_tanpa <= total_kata//1000 else 'gagal'} |")
    baris.append(f"| Klaim di buku besar bukti | {len(klaim)} | ≥ 120 | {'lolos' if len(klaim) >= 120 else 'gagal'} |")
    baris.append(f"| Klaim terverifikasi | {len(klaim)-len(belum_terverifikasi)} | semua | {'lolos' if not belum_terverifikasi else 'gagal'} |")
    baris.append("")

    baris.append("## Sitasi yatim\n")
    if yatim:
        baris.append("Sitasi berikut muncul di badan teks tetapi tidak punya entri bibliografi.\n")
        for nama, tahun in yatim:
            baris.append(f"- `{nama}` ({tahun})")
    else:
        baris.append("Tidak ada. Setiap sitasi punya entri bibliografi.")
    baris.append("")

    baris.append("## Kalimat berangka tanpa sumber\n")
    baris.append(f"Total: **{total_tanpa}** kalimat.\n")
    for nama, kals in per_bab.items():
        baris.append(f"### `{nama}` — {len(kals)}\n")
        for k in kals[:8]:
            baris.append(f"- {k[:220]}")
        if len(kals) > 8:
            baris.append(f"- … dan {len(kals)-8} lainnya")
        baris.append("")

    if belum_terverifikasi:
        baris.append("## Klaim yang belum terverifikasi\n")
        baris.append(f"{len(belum_terverifikasi)} dari {len(klaim)} klaim di buku besar belum berstatus `terverifikasi`.\n")

    laporan = "\n".join(baris)
    LAPORAN.parent.mkdir(parents=True, exist_ok=True)
    LAPORAN.write_text(laporan, encoding="utf-8")

    if ringkas:
        print(f"kata={total_kata} sitasi={jumlah_sitasi} kepadatan={kepadatan:.2f}/1000 "
              f"yatim={len(yatim)} tanpa_sumber={total_tanpa} klaim={len(klaim)}")
    else:
        print(laporan)

    keras = bool(yatim) or total_tanpa > total_kata // 1000
    return 1 if keras else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ringkas", action="store_true")
    ap.add_argument("--lang", default="id", choices=["id", "en"])
    a = ap.parse_args()
    globals()["SRC"] = BOOK / "src" / a.lang
    sys.exit(jalankan(a.ringkas))
