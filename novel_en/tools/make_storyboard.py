#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_storyboard.py — papan cerita + ukuran struktural -> bible/STORYBOARD.md"""
import glob, hashlib, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "bible"); V = os.path.join(ROOT, "vol1"); sys.path.insert(0, B)
import struktur_100 as S

def kal(t): return [s for s in re.split(r"(?<=[.!?\u2026])[\s\u201c\u201d]+", t.strip()) if s]

def metrik(t):
    kata = t.split(); dg = " ".join(re.findall(r"\u201c(.*?)\u201d", t, flags=re.S))
    kal_ = kal(re.sub(r"\u201c.*?\u201d", " ", t, flags=re.S))
    sc = [b for b in re.split(r"\n-{3,}\n", t) if b.strip() and not b.strip().startswith("*Next")]
    return dict(kata=len(kata), scene=len(sc), dialog=round(100*len(dg.split())/max(1,len(kata))),
                kal=round(sum(len(k.split()) for k in kal_)/max(1,len(kal_)),1))

def main():
    rows = {r[0]: dict(zip(S.FIELDS, r)) for r in S.ALL}
    arc = {r[0]: (k, j) for k, j, g in S.ARCS for r in g}
    berkas = {}
    for p in glob.glob(os.path.join(V, "ch_*.md")):
        m = re.search(r"ch_(\d{3})\.md$", p)
        if m: berkas[int(m.group(1))] = p
    o = ["# Storyboard & Ukuran Struktural — Volume I\n",
         "*Dibuat `tools/make_storyboard.py` · versi bible `%s`*" % hashlib.sha1(open(os.path.join(B,"struktur_100.py"),"rb").read()).hexdigest()[:8],
         "\nPapan ini turunan naskah, bukan sumber fakta baru.\n", "\n## Status\n"]
    total = sum(len(open(p, encoding="utf-8").read().split()) for p in berkas.values())
    o.append("- Bab tertulis: **%d / 100**" % len(berkas))
    o.append("- Total kata: **%s**" % format(total, ","))
    o.append("- Rata-rata: **%d kata/bab**\n" % (total // max(1, len(berkas))))
    o += ["\n## Papan ringkas\n",
          "| Bab | Judul | POV | Tanggal | Kata | Scene | Dialog% | Kalimat |",
          "|---:|---|---|---|---:|---:|---:|---:|"]
    pola = []
    for n in sorted(berkas):
        judul, isi = open(berkas[n], encoding="utf-8").read().split("\n", 1)
        judul = judul.lstrip("# ").split("\u2014")[-1].strip(); m = metrik(isi); c = rows[n]
        o.append("| %d | %s | %s | %s | %d | %d | %d | %.1f |" % (n, judul, c["pov"], c["d"], m["kata"], m["scene"], m["dialog"], m["kal"]))
        if m["kata"] < 1500: pola.append("bab %d: %d kata" % (n, m["kata"]))
        if m["dialog"] < 20: pola.append("bab %d: dialog %d%%" % (n, m["dialog"]))
    belum = [n for n in range(1, 101) if n not in berkas]
    o.append("\n## Pola dan lubang\n")
    o += ["- " + x for x in pola] or []
    if belum: o.append("- belum ditulis: %d bab, mulai bab %d" % (len(belum), belum[0]))
    o.append("\n## Papan per bab\n")
    for n in sorted(berkas):
        judul, isi = open(berkas[n], encoding="utf-8").read().split("\n", 1)
        c = rows[n]; k, j = arc[n]; m = metrik(isi)
        kode = "V1-%s-C%03d" % (k.replace("Arc ", "A").zfill(3), n)
        o.append("\n### %s — %s" % (kode, judul.lstrip("# ").split("\u2014")[-1].strip()))
        o.append("`%s` · POV %s · %s · %d kata · hadir: %s" % (j, c["pov"], c["d"], m["kata"], c["cast"]))
        o.append("- **Beat:** %s" % c["beat"]); o.append("- **Hook:** %s" % c["hook"])
        for i, b in enumerate([x for x in re.split(r"\n-{3,}\n", isi) if x.strip() and not x.strip().startswith("*Next")], 1):
            baris = [y for y in b.split("\n") if y.strip()]
            o.append("  - `%s-S%02d` · %d kata · %s" % (kode, i, len(b.split()), baris[0][:100] if baris else ""))
    open(os.path.join(B, "STORYBOARD.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")
    print("STORYBOARD.md |", len(berkas), "bab |", len(pola), "pola")

if __name__ == "__main__":
    main()
