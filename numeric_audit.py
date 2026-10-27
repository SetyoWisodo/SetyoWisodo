# -*- coding: utf-8 -*-
"""Daftar angka yang belum bertuan -- untuk diperiksa manusia sebelum terbit.

Menulis NUMERIC_CLAIMS.md: setiap paragraf yang memuat BESARAN (persen, juta,
miliar, hektare, korban, dolar, liter) tetapi tidak punya rujukan di paragraf
itu. Tahun ("pada 2023"), nomor bab ("x.1") dan nomor urut tidak dihitung --
itu bukan statistik, dan menghitungnya membuat angkanya membengkak jadi 22%.

Paragraf yang sumbernya disebut langsung di dalam kalimat ("Bank Dunia
memperkirakan ...", "Oxfam dan SEI ...") dicatat terpisah: itu atribusi dalam
prosa, sah menurut gaya buku ini.

Jalankan: python numeric_audit.py
"""
import re

import cite_numbers as C

# rujukan dalam tanda kurung: "(Nama, 2021)", "(de Waal, 1997)", "(A et al., 2020)"
CITE = re.compile(r"\([A-Za-z][^()]{0,80}?,\s*(?:19|20)\d{2}[a-z]?\)")
TARGETS = [("book.md", "EN", "Inggris"), ("book_id.md", "ID", "Indonesia")]

NUMWORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90,
    "satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6,
    "tujuh": 7, "delapan": 8, "sembilan": 9, "sepuluh": 10, "sebelas": 11,
}
UNITS = ("people", "person", "orang", "lives", "nyawa", "deaths", "kematian",
         "korban", "hectares", "hektar", "hektare", "kilometres", "kilometers",
         "kilometer", "metres", "meters", "meter", "litres", "liters", "liter",
         "percent", "per cent", "persen", "years", "tahun", "days", "hari",
         "homes", "rumah", "households", "buildings", "bangunan", "dollars",
         "dolar", "species", "spesies", "jobs", "pekerjaan", "cases", "kasus")


def deskrip(text):
    """Angka yang ditulis dengan kata diubah ke digit, dua bahasa."""
    words = ("hundred", "thousand", "seratus", "ribu", "puluh")
    def repl(m):
        total, cur = 0, 0
        for w in re.split(r"[\s-]+", m.group(0).lower()):
            if w in ("hundred", "seratus"):
                cur = (cur or 1) * 100
            elif w in ("thousand", "ribu"):
                total += (cur or 1) * 1000
                cur = 0
            elif w in NUMWORDS:
                cur += NUMWORDS[w]
        return str(total + cur)
    pat = (r"\b(?:(?:" + "|".join(sorted(list(NUMWORDS) + list(words),
                                          key=len, reverse=True)) +
           r")[\s-]+){1,5}(?=(?:" + "|".join(UNITS) + r")\b)")
    return re.sub(pat, repl, text, flags=re.I)


def figures(text):
    """[(angka, skala, satuan)] -- hanya besaran, bukan tahun."""
    out = []
    for m in C.FIG.finditer(deskrip(C.despell(text))):
        value = m.group(1).replace(",", "").replace(".", "")
        scale = (m.group(2) or "").lower()
        unit = (m.group(3) or "").strip()
        if not scale and not unit:
            continue
        if len(value) == 4 and 1900 <= int(value) <= 2099 and not scale:
            continue
        out.append((value, scale, unit))
    return out


def show(figs):
    seen, out = set(), []
    for v, scale, unit in figs:
        raw = re.sub(r"\s+", " ", f"{v} {scale} {unit}".replace("per cent", "%"))
        if raw not in seen:
            seen.add(raw)
            out.append(raw)
    return out


def main():
    lines = ["# Angka yang Belum Bertuan", "",
             "Daftar periksa, bukan tuduhan. Setiap paragraf di bawah memuat",
             "besaran tanpa rujukan di paragraf itu, dan sumbernya tidak disebut",
             "langsung di dalam kalimat. Tahun dan nomor bab tidak dihitung.",
             ""]
    summary, detail = [], []
    for path, code, name in TARGETS:
        text = open(path, encoding="utf-8").read()
        chap, paras, rows, prose = "?", 0, [], 0
        for b in re.split(r"\n\s*\n", text):
            if b.startswith(("# Chapter", "# Bab")):
                chap = b.lstrip("# ").split(":")[0]
                continue
            if not C.is_body(b):
                continue
            paras += 1
            figs = figures(b)
            if not figs:
                continue
            if CITE.search(b):
                continue
            if re.search(r"\b(?:World Bank|WHO|IPCC|WMO|FAO|UNEP|UNDRR|ILO|IEA|"
                         r"IRENA|Oxfam|UN-Habitat|OECD|IMF|Bank Dunia|PBB)\b", b):
                prose += 1
                continue
            rows.append((chap, show(figs), re.sub(r"\s+", " ", b)))
        summary.append((name, paras, len(rows), prose))
        detail.append((name, rows))

    head = ["| Edisi | Paragraf | Tanpa rujukan | Atribusi dalam prosa |",
            "|---|---|---|---|"]
    for name, tot, r, p_ in summary:
        head.append(f"| {name} | {tot} | {r} | {p_} |")
    lines[3:3] = head

    for name, rows in detail:
        lines += [f"## Edisi {name} ({len(rows)} paragraf)", ""]
        for chap, figs, body in rows:
            lines.append(f"- **{chap} · {', '.join(figs[:4])}** — {body[:170]}...")
        lines.append("")
    open("NUMERIC_CLAIMS.md", "w", encoding="utf-8").write("\n".join(lines))
    for name, tot, r, p_ in summary:
        print(f"{name}: paragraf {tot} | tanpa rujukan {r} | atribusi prosa {p_}")
    print("NUMERIC_CLAIMS.md ditulis")


if __name__ == "__main__":
    main()
