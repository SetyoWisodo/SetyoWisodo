#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_adegan.py — render bible/ADEGAN.md: papan visual per bab & per scene.

    python3 novel_en/tools/make_adegan.py

Membaca adegan.json + struktur_100 + naskah, menulis papan yang bisa dipakai
untuk storyboard, pitch, atau adaptasi.
"""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "bible"); V = os.path.join(ROOT, "vol1"); sys.path.insert(0, B)
import struktur_100 as S

def main():
    ad = json.load(open(os.path.join(B, "adegan.json"), encoding="utf-8"))
    T = ad["templates"]; peta = {b["n"]: b for b in ad["bab"]}
    rows = {r[0]: dict(zip(S.FIELDS, r)) for r in S.ALL}
    arc = {r[0]: k for k, j, g in S.ARCS for r in g}
    ada = {}
    for p in glob.glob(os.path.join(V, "ch_*.md")):
        m = re.search(r"ch_(\d{3})\.md$", p)
        if m: ada[int(m.group(1))] = p

    o = ["# Papan Adegan — Volume I\n",
         "*Dirender dari `bible/adegan.json` + `bible/FILM_GRAMMAR.md`.*\n",
         "Setiap bab memakai maksimal dua templat. Templat menjelaskan **cara** "
         "adegan disusun, bukan isinya; isinya tetap dari `struktur_100.py`.\n",
         "\n## Templat\n"]
    for k, v in T.items():
        o.append("\n**%s — %s**  \nAsal: %s  \nShot: %s" % (k, v["nama"], v["asal"], " → ".join(v["shot"])))
    o.append("\n\n## Ringkasan pemakaian\n")
    o.append("| Bab | Judul | Templat | Lensa | Cahaya | Warna |")
    o.append("|---:|---|---|---|---|---|")
    for n in range(1, 101):
        b = peta[n]; c = rows[n]
        o.append("| %d | %s | %s | %s | %s | %s |" % (n, c["t"], " + ".join(b["templates"]),
                                                     b["lensa"], b["cahaya"], b["warna"]))
    for n in sorted(ada):
        b = peta[n]; c = rows[n]
        isi = open(ada[n], encoding="utf-8").read().split("\n", 1)[1]
        sc = [x for x in re.split(r"\n-{3,}\n", isi) if x.strip() and not x.strip().startswith("*Next")]
        o.append("\n---\n\n## Bab %d — %s\n" % (n, c["t"]))
        o.append("`%s` · %s · %s · %s" % (arc[n], b["lensa"], b["cahaya"], b["warna"]))
        for i, s in enumerate(sc, 1):
            baris = [y for y in s.split("\n") if y.strip()]
            t = b["templates"][0] if i % 2 else b["templates"][-1]
            o.append("\n**%02d · %s — %s**" % (i, t, T[t]["nama"]))
            o.append("Shot: %s" % " → ".join(T[t]["shot"]))
            o.append("Aksen: %d kata · %s" % (len(s.split()), baris[0][:90] if baris else ""))
    p = os.path.join(B, "ADEGAN.md")
    open(p, "w", encoding="utf-8").write("\n".join(o) + "\n")
    print("ADEGAN.md:", len(ada), "bab tertulis |", len(T), "templat")

if __name__ == "__main__":
    main()
