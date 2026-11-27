#!/usr/bin/env python3
"""Audit atribusi: tandai kalimat yang kata kuncinya tidak cocok dengan judul sumber.

Bukan penentu salah/benar — hanya menyaring 250 kalimat menjadi puluhan yang
perlu dibaca manusia. Skor rendah = ketidakcocokan leksikal antara kalimat dan
judul/penerbit entri bibliografi.
"""
import csv
import json
import pathlib
import re

REF = pathlib.Path("reference/bibliografi.csv")
STOP = set("""the of and to in a is that for on with as by at from be this it are was
were an or which their its has have had not but they we you can if when than then
there these those such more most less least very much many also only just about
into over under between during after before while because how what who whom whose
per cent percent million billion thousand one two three four five six seven eight
nine ten first second third chapter book figure table box source data year years
people world global country countries city cities""".split())


def toks(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]{4,}", s.lower()) if w not in STOP}


def main() -> None:
    bib = {r["kunci"]: r for r in csv.DictReader(REF.open(encoding="utf-8"))}
    rows = []
    for lang, pat in (("en", "[01][0-9]-*.md"),):
        for p in sorted(pathlib.Path(f"src/{lang}").glob(pat)):
            if p.name.startswith(("00-", "99-")):
                continue
            t = p.read_text(encoding="utf-8")
            for para in re.split(r"\n\s*\n", t):
                if para.lstrip().startswith(("#", ":::")):
                    continue
                for kal in re.split(r"(?<=[.!?])\s+", " ".join(para.split())):
                    ks = re.findall(r"@([a-z]+\d{4}[a-z]*)", kal)
                    if not ks:
                        continue
                    kt = toks(kal)
                    best = 0.0
                    for k in ks:
                        r = bib.get(k)
                        if not r:
                            continue
                        st = toks(r["judul"] + " " + r["penerbit"] + " " + r["penulis"])
                        if not kt or not st:
                            continue
                        best = max(best, len(kt & st) / len(kt))
                    rows.append({"bab": p.name[:2], "skor": round(best, 2),
                                 "kunci": ks, "kalimat": kal})
    rows.sort(key=lambda x: x["skor"])
    json.dump(rows, open("reference/audit_atribusi.json", "w"), ensure_ascii=False, indent=1)
    n = len(rows)
    for amb in (0.0, 0.05, 0.1):
        print(f"skor <= {amb}: {sum(1 for r in rows if r['skor'] <= amb)} dari {n}")
    print("\n20 terendah:")
    for r in rows[:20]:
        print(f"  {r['skor']:.2f} [{r['bab']}] {r['kalimat'][:120]}")
        print(f"        kunci={r['kunci']}")


if __name__ == "__main__":
    main()
