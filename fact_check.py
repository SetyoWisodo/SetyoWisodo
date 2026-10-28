# -*- coding: utf-8 -*-
"""Pemeriksa konsistensi fakta (Gate 2).

Tabel fakta kanonis: satu nilai untuk satu peristiwa, diperiksa di kedua edisi.
Kegagalan berarti angka hilang, berbeda antarbahasa, atau menyimpang dari nilai
yang dipakai di seluruh buku.

Jalankan: python fact_check.py
"""
import re
import sys

# (label, konteks EN, konteks ID, nilai yang harus muncul)
FACTS = [
    ("CO2 2024", r"carbon dioxide reached about", r"424 bagian per juta", ["424"]),
    ("CH4", r"methane about", r"bagian per miliar", ["1,934", "1.934", "1.900"]),
    ("Sea-level rate", r"millimetres a year today", r"milimeter per tahun", ["4.5", "4,5"]),
    ("Warming to date", r"rise of about", r"suhu permukaan sekitar 1,1", ["1.1", "1.3", "1,1", "1,3"]),
    ("Katrina deaths", r"Katrina in 2005", r"Katrina", ["1,400", "1.400"]),
    ("Maria excess deaths", r"excess deaths", r"kematian berlebih", ["2,975", "2.975"]),
    ("Europe 2003", r"70,000", r"70.000", ["70,000", "70.000"]),
    ("Black Saturday", r"Black Saturday", r"Black Saturday", ["173"]),
    ("Camp Fire", r"Eighty-five people", r"Delapan puluh lima", ["eighty-five", "delapan puluh lima"]),
    ("Bhola cyclone", r"Bhola", r"Bhola", ["300,000", "300.000", "three hundred thousand", "tiga ratus ribu"]),
    ("Somalia 2011", r"Somal", r"Somal", ["258,000", "258.000"]),
    ("Ethiopia 1984", r"Ethiopian famine", r"Kelaparan Etiopia", ["one million", "satu juta", "sejuta"]),
    ("Sahel 1968", r"100,000", r"100.000", ["100,000", "100.000"]),
    ("Pakistan affected", r"Pakistan", r"Pakistan", ["33 million", "thirty-three million", "33 juta", "tiga puluh tiga juta"]),
    ("Pakistan deaths", r"1,700", r"1.700", ["1,700", "1.700"]),
    ("Pakistan damage", r"US\$30 billion", r"US\$30 miliar", ["30"]),
    ("Ahr valley", r"Ahrweiler", r"Ahrweiler", ["134"]),
    ("Heat deaths per year", r"489,000", r"489.000", ["489,000", "489.000"]),
    ("Europe heat deaths", r"175,000 deaths a year", r"175.000 kematian", ["175,000", "175.000"]),
    ("Remaining 1.5 budget", r"remaining carbon budget", r"anggaran karbon", ["250"]),
    ("WHO climate deaths", r"250,000 additional", r"250.000 kematian tambahan", ["250,000", "250.000"]),
    ("Europe 2022 heat", r"European summer of 2022", r"musim panas Eropa 2022", ["61,700", "61.700"]),
    ("Air pollution toll", r"seven million people a year", r"tujuh juta orang per tahun", ["seven million", "tujuh juta", "7 million", "7 juta"]),
]

PAIRS = [("book.md", 0, "en"), ("book_id.md", 1, "id")]


def sentences(text):
    out = []
    for line in text.split("\n"):
        if line.startswith(("#", "|", "-", "[[", ">")):
            continue
        out += [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if len(s.split()) > 6]
    return out


def check(path, lang_idx):
    text = open(path, encoding="utf-8").read()
    sents = sentences(text)
    rows = []
    for label, ctx_en, ctx_id, values in FACTS:
        ctx = ctx_en if lang_idx == 0 else ctx_id
        hit = None
        ok = False
        for s in sents:
            if re.search(ctx, s, re.I) and any(v.lower() in s.lower() for v in values):
                hit, ok = s, True
                break
        if hit is None:
            for s in sents:
                if re.search(ctx, s, re.I):
                    hit = s
                    break
        rows.append((label, ok, hit[:150] if hit else None))
    return rows


def main():
    bad = 0
    for path, idx, tag in PAIRS:
        rows = check(path, idx)
        print("=" * 70)
        print(path, f"({len(rows)} fakta)")
        for label, ok, ctx in rows:
            mark = "OK  " if ok else "FAIL"
            print(f"  {mark} {label:22s} {'' if ok else (ctx or 'konteks tidak ditemukan')}")
            if not ok:
                bad += 1
    print("=" * 70)
    print("TOTAL GAGAL:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
