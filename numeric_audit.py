# -*- coding: utf-8 -*-
"""Daftar angka yang belum bertuan -- untuk diperiksa manusia sebelum terbit.

Menulis NUMERIC_CLAIMS.md: setiap paragraf yang memuat kuantitas (persen,
juta, miliar, hektare, korban, dolar) tetapi tidak punya rujukan di paragraf
itu, dikelompokkan per bab, lengkap dengan angkanya.

Kenapa dipisah dari audit_plagiarism.py: pemeriksa lama menghitung SETIAP
digit, termasuk tahun ("pada 2023") dan nomor bab ("x.1"), sehingga angkanya
membengkak jadi 22% dan menyesatkan. Tahun bukan statistik; yang perlu
rujukan adalah besaran.

Jalankan: python numeric_audit.py
"""
import re

import cite_numbers as C

CITE_STRICT = __import__("re").compile(r"\([A-Z][^()]{0,80}?(?:19|20)\d{2}[a-z]?\)")

TARGETS = [("book.md", "EN", "Inggris"), ("book_id.md", "ID", "Indonesia")]


def collect(path):
    text = open(path, encoding="utf-8").read()
    chap, out = "?", []
    for b in re.split(r"\n\s*\n", text):
        if b.startswith("# Chapter") or b.startswith("# Bab"):
            chap = b.lstrip("# ").split(":")[0]
            continue
        if not C.is_body(b) or not re.search(r"\d", b):
            continue
        if not C.QUANTITY.search(b) or CITE_STRICT.search(b):
            continue
        out.append((chap, show_figs(b), b))
    return out


def show_figs(text):
    seen, out = set(), []
    for m in C.FIG.finditer(C.despell(text)):
        raw = f"{m.group(1)} {(m.group(2) or '')} {m.group(3)}"
        raw = re.sub(r"\s+", " ", raw.replace("per cent", "%")).strip()
        if raw not in seen:
            seen.add(raw)
            out.append(raw)
    return out


def short(v):
    if v >= 10**9:
        return f"{v/10**9:g} miliar"
    if v >= 10**6:
        return f"{v/10**6:g} juta"
    if v >= 1000:
        return f"{v:,}".replace(",", ".")
    return str(v)


def main():
    lines = ["# Angka yang Belum Bertuan",
             "",
             "Setiap paragraf di bawah ini menyebut sebuah besaran tanpa rujukan di",
             "paragraf itu, dan besarannya tidak saya temukan terpasang pada sumber",
             "mana pun di Daftar Pustaka. Daftar ini bukan tuduhan plagiasi -- ini",
             "daftar periksa. Angka yang tercantum di sini berasal dari laporan",
             "peristiwa dan basis data yang belum masuk Daftar Pustaka.",
             "",
             "Cara memakainya: buka babnya, cek angkanya ke sumber resmi, lalu",
             "tambahkan entri Daftar Pustaka bila perlu. Kalau angkanya ternyata",
             "tidak bisa dipertanggungjawabkan, hapus atau ubah menjadi rentang.",
             ""]
    total = 0
    for path, code, name in TARGETS:
        rows = collect(path)
        total += len(rows)
        per = {}
        for chap, vals, b in rows:
            per.setdefault(chap, []).append((vals, b))
        lines.append(f"## Edisi {name} ({len(rows)} paragraf)")
        lines.append("")
        for chap in sorted(per, key=lambda c: int(re.sub(r"\D", "", c) or 0)):
            lines.append(f"### {chap}")
            lines.append("")
            for vals, b in per[chap]:
                figure = ", ".join(vals[:4]) if vals else "-"
                body = re.sub(r"\s+", " ", b)
                lines.append(f"- **{figure}** — {body[:170]}...")
            lines.append("")
    lines.insert(1, "")
    lines.insert(2, f"**Total: {total} paragraf.** ")
    open("NUMERIC_CLAIMS.md", "w", encoding="utf-8").write("\n".join(lines))
    print(f"NUMERIC_CLAIMS.md ditulis: {total} paragraf tanpa rujukan")


if __name__ == "__main__":
    main()
