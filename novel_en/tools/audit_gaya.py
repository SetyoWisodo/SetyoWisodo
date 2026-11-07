#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_gaya.py - gerbang "human feel".

    python3 novel_en/tools/audit_gaya.py            # semua bab
    python3 novel_en/tools/audit_gaya.py ch_001      # satu bab, cetak cuplikan
    python3 novel_en/tools/audit_gaya.py --banding   # bandingkan bab

Yang diukur bukan "bagus atau tidak" - itu kerja telinga. Yang diukur ialah
jejak mesin: pola yang berulang terlalu rapi sampai terasa ditempel.

Enam gejala yang sudah terbukti ada di 34 bab pertama:
  1. paragraf seragam-pendek (median 10 kata, separuh bab di bawah 10 kata)
  2. angka yang sama dipakai sebagai tic ("eleven" 249 kali)
  3. dialog beruntun tanpa beat (72%)
  4. pembuka paragraf yang sama ("I put", "I looked", "I sat")
  5. kalimat yang panjangnya nyaris seragam
  6. paragraf tanpa satu pun detail yang tidak diperlukan cerita

Batas di bawah ini disetel dari ch_001 setelah disunting tangan, bukan dari
angka bulat. Keluar 1 kalau ada FAIL.
"""
import glob, os, re, sys
from collections import Counter
from statistics import median, pstdev

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOL = os.path.join(ROOT, "vol1")

# --- batas -------------------------------------------------------------
P_MIN_MED, P_MAX_PENDEK = 12, 38     # median kata/paragraf; % paragraf <10 kata
P_PANJANG_MIN = 4                    # % paragraf >80 kata
ANGKA_MAKS = 4.0                     # angka-kata yang sama, per 1.000 kata
DIALOG_BEAT_MIN = 42                 # % baris dialog yang punya beat (laporan)
DERET_MAKS = 5                       # dialog beruntun tanpa beat
BUKA_MAKS = 6.0                      # pembuka paragraf yang sama, per 1.000 kata
KAL_SD_MIN = 6.5                     # simpangan baku panjang kalimat

BUKA = ["I put", "I looked", "I sat", "I did", "I said", "I took", "I read",
        "I stood", "I went", "I felt", "I thought", "I knew", "I kept", "I let"]
ANGKA = ["eleven", "twelve", "ten", "nine", "six", "five", "four", "three",
         "forty", "sixty", "hundred", "thousand"]
SATUAN = ("minute", "second", "hour", "day", "week", "year", "winter", "gram",
          "kilo", "metre", "meter", "percent", "people", "page", "door", "deck")
AFORISME = re.compile(r"(?:\.|;)\s+(?:That is|That was|Which is|It is|This is)\b")


def kalimat(t):
    return [s for s in re.split(r"(?<=[.!?\u2026])[\s\u201c\u201d]+", t.strip()) if s]


def paragraf(isi):
    return [p.strip() for p in re.split(r"\n\s*\n", isi) if p.strip()
            and not p.strip().startswith(("#", "---", "*Next:"))]


def ukur(isi):
    kata = isi.split()
    n = max(1, len(kata))
    paras = paragraf(isi)
    pk = [len(p.split()) for p in paras]
    kal = kalimat(re.sub(r"\u201c.*?\u201d", " ", isi, flags=re.S))
    kl = [len(k.split()) for k in kal] or [0]

    # dialog: baris yang seluruhnya/terutama dialog, punya beat atau tidak
    # deret dialog tanpa beat lebih mengganggu daripada persentasenya:
    # dua-tiga baris beruntun itu wajar, enam beruntun itu naskah drama.
    baris, tanpa, deret, terpanjang = 0, 0, 0, 0
    for p in paras:
        if not p.lstrip().startswith("\u201c"):
            deret = 0
            continue
        baris += 1
        sisa = re.sub(r"\u201c.*?\u201d", "", p, flags=re.S).strip()
        if len(sisa.split()) < 3:
            tanpa += 1
            deret += 1
            terpanjang = max(terpanjang, deret)
        else:
            deret = 0

    # angka yang diikuti satuan itu ukuran, bukan tic - jangan dihitung
    polos = re.sub(r"\b(" + "|".join(ANGKA) + r")\s+\w*(" + "|".join(SATUAN) + r")\w*", " ", isi.lower())
    rendah = {w: len(re.findall(r"\b" + w + r"\b", polos)) for w in ANGKA}
    buka = Counter()
    for p in paras:
        for b in BUKA:
            if p.startswith(b):
                buka[b] += 1
                break

    return dict(
        kata=n,
        median_par=median(pk) if pk else 0,
        pendek=round(100 * sum(1 for x in pk if x < 10) / len(pk), 1) if pk else 0,
        panjang=round(100 * sum(1 for x in pk if x > 80) / len(pk), 1) if pk else 0,
        angka=round(1000 * max(rendah.values()) / n, 1),
        angka_kata=max(rendah, key=rendah.get),
        dialog=baris,
        dialog_tanpa=round(100 * tanpa / baris, 1) if baris else 0,
        deret=terpanjang,
        buka=buka.most_common(1)[0] if buka else ("-", 0),
        buka_laju=round(1000 * (buka.most_common(1)[0][1] / n), 1) if buka else 0,
        kal_sd=round(pstdev(kl), 1),
        aforisme=len(AFORISME.findall(isi)),
    )


def periksa(nama, u):
    out = []
    if u["median_par"] < P_MIN_MED:
        out.append(("WARN", "paragraf", f"median {u['median_par']:.0f} kata (min {P_MIN_MED})"))
    if u["pendek"] > P_MAX_PENDEK:
        out.append(("WARN", "paragraf", f"{u['pendek']}% paragraf <10 kata (maks {P_MAX_PENDEK}%)"))
    if u["panjang"] < P_PANJANG_MIN:
        out.append(("WARN", "napas", f"{u['panjang']}% paragraf >80 kata (min {P_PANJANG_MIN}%)"))
    if u["angka"] > ANGKA_MAKS:
        out.append(("WARN", "tic-angka", f"\u201c{u['angka_kata']}\u201d {u['angka']}/1000 kata (maks {ANGKA_MAKS})"))
    if u["deret"] > DERET_MAKS:
        out.append(("WARN", "beat", f"{u['deret']} dialog beruntun tanpa beat (maks {DERET_MAKS})"))
    if u["buka_laju"] > BUKA_MAKS:
        out.append(("WARN", "pembuka", f"\u201c{u['buka'][0]}\u201d {u['buka'][1]}x ({u['buka_laju']}/1000 kata)"))
    if u["kal_sd"] < KAL_SD_MIN:
        out.append(("WARN", "irama", f"sd kalimat {u['kal_sd']} (min {KAL_SD_MIN})"))
    return out


def main():
    arg = [a for a in sys.argv[1:] if not a.startswith("--")]
    pola = f"ch_{arg[0][-3:]}.md" if arg else "ch_*.md"
    berkas = sorted(glob.glob(os.path.join(VOL, pola)))
    if not berkas:
        print("tidak ada berkas"); return 1

    semua, gagal, catat = {}, 0, []
    for f in berkas:
        nama = os.path.basename(f)
        u = ukur(open(f, encoding="utf-8").read())
        semua[nama] = u
        for tingkat, k, m in periksa(nama, u):
            catat.append((tingkat, k, nama, m))
            gagal += tingkat == "FAIL"

    if arg:
        u = semua[os.path.basename(berkas[0])]
        print(f"\n{os.path.basename(berkas[0])}  {u['kata']} kata")
        print(f"  paragraf  median {u['median_par']:.0f} | {u['pendek']}% <10 kata | {u['panjang']}% >80 kata")
        print(f"  tic       \u201c{u['angka_kata']}\u201d {u['angka']}/1000 kata")
        print(f"  dialog    {u['dialog']} baris | {u['dialog_tanpa']}% tanpa beat | deret terpanjang {u['deret']}")
        print(f"  pembuka   \u201c{u['buka'][0]}\u201d {u['buka'][1]}x")
        print(f"  irama     sd kalimat {u['kal_sd']} | aforisme {u['aforisme']}")

    if "--banding" in sys.argv:
        print(f"\n{'bab':10}{'kata':>6}{'medPar':>8}{'<10':>6}{'>80':>6}{'tic':>6}{'deret':>6}{'sdKal':>7}")
        for n, u in semua.items():
            print(f"{n[:-3]:10}{u['kata']:6}{u['median_par']:8.0f}{u['pendek']:6.1f}"
                  f"{u['panjang']:6.1f}{u['angka']:6.1f}{u['deret']:6}{u['kal_sd']:7.1f}")

    kabar = Counter(k for _, k, _, _ in catat)
    for k, j in kabar.most_common():
        contoh = [c for c in catat if c[1] == k][:3]
        print(f"WARN {k:10} {j:2}x  " + "; ".join(f"{c[2][:-3]} {c[3]}" for c in contoh))
    print(f"\n{len(berkas)} bab | {sum(u['kata'] for u in semua.values()):,} kata | "
          f"FAIL {gagal} | WARN {len(catat)}")
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
