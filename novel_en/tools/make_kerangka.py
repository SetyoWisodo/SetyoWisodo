#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_kerangka.py — render bible/KERANGKA_PER_BAB.md (kontrak penulisan per bab)."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "bible"); V = os.path.join(ROOT, "vol1"); sys.path.insert(0, B)
import struktur_100 as S

ATURAN = """# Kerangka Berpikir per Bab — Volume I

*Before the Light Arrives* — 100 bab, 10 arc, ±160.000 kata.

Berkas ini **kontrak penulisan**. Penulis bab berikutnya membaca kartu babnya,
tiga kartu sebelumnya, dan aturan ini.

## Aturan yang tidak boleh dilanggar

1. **POV.** Nara orang pertama past tense (mayoritas). Bab Vey (11, 57, 60, 73, 85, 86, 96)
   present tense, tanpa menamai emosi. Bab Kirana (36, 55, 56, 74, 88) past tense, kalimat pendek.
2. **Panjang.** 1.500–2.500 kata.
3. **Dialog.** 20–60% kata berada di dalam kutipan. Bab tanpa percakapan gagal audit.
4. **Scene.** 3–6 scene per bab, dipisah `---`.
5. **Kalimat.** Rata-rata 8–17 kata.
6. **Hook.** Dua kalimat terakhir persis seperti kartu.
7. **Setiap bab memuat satu keputusan**, bukan hanya satu penemuan.
8. **Sains.** Tidak ada informasi lebih cepat dari cahaya, tidak ada kloning isi paket,
   tidak ada penghapusan gratis. Landauer, Shannon, no-cloning, delayed choice disebut
   dengan nama dan tahun aslinya (lihat research/KUTIPAN_SAINS.md).
9. **Nama.** Ejaan resmi dari tokoh.json; ejaan terlarang tidak boleh muncul.
"""

def main():
    tokoh = json.load(open(os.path.join(B, "tokoh.json"), encoding="utf-8"))
    sains = json.load(open(os.path.join(B, "sains.json"), encoding="utf-8"))
    twist = json.load(open(os.path.join(B, "twist.json"), encoding="utf-8"))["twists"]
    pet = json.load(open(os.path.join(B, "petunjuk.json"), encoding="utf-8"))
    ada = set(int(m.group(1)) for m in (re.match(r"ch_(\d{3})\.md$", f) for f in os.listdir(V)) if m)
    o = [ATURAN, "\n## Peta arc\n"]
    for k, j, g in S.ARCS:
        n = [r[0] for r in g]
        o.append("- **%s — %s** (bab %d–%d)" % (k, j, min(n), max(n)))
    o.append("\nTertulis: **%d / 100**\n\n---\n" % len(ada))
    for k, j, g in S.ARCS:
        n = [r[0] for r in g]
        o.append("\n## %s — %s (bab %d–%d)\n" % (k, j, min(n), max(n)))
        for r in g:
            d = dict(zip(S.FIELDS, r)); nn = d["n"]
            o.append("\n### Bab %d — %s  \n`%s` · %s · POV %s\n" % (nn, d["t"], "selesai" if nn in ada else "belum", d["d"], d["pov"]))
            o.append("- **Beat:** %s" % d["beat"])
            o.append("- **Hook:** %s" % d["hook"])
            o.append("- **Yang berubah:** %s" % d["sets"])
            for f, lab in (("plant", "Tanam"), ("pay", "Bayar")):
                if d[f] != "-":
                    for p in [x.strip() for x in d[f].split(",")]:
                        o.append("- **%s %s:** %s" % (lab, p, pet.get(p, {}).get("object", "—")))
            if d["sci"] != "-":
                for s in [x.strip() for x in d["sci"].split(",")]:
                    x = sains.get(s, {})
                    o.append("- **Sains %s:** %s (%s, %s) — %s" % (s, x.get("claim"), x.get("who"), x.get("year"), x.get("use")))
            o.append("- **Hadir:** %s" % d["cast"])
    o.append("\n---\n\n## Enam twist dan buktinya\n")
    for t in twist:
        o.append("\n**%s** — %s  \nDibayar bab %s · bukti: %s" % (t["id"], t["claim"], t["paid"], ", ".join(str(c) for c in t["clues"])))
    o.append("\n\n## Tokoh\n")
    for nama, d in tokoh.items():
        o.append("\n**%s** (%s) — %s  \nKanon: %s  \nEjaan terlarang: %s" % (nama, d["age"], d["role"], "; ".join(d["facts"]), ", ".join(d["forbidden"]) or "—"))
    open(os.path.join(B, "KERANGKA_PER_BAB.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")
    print("KERANGKA_PER_BAB.md |", len(ada), "bab tertulis")

if __name__ == "__main__":
    main()
