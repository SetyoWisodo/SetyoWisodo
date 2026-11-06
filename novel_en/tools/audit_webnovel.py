#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_webnovel.py — gerbang mutu naskah serial.

    python3 novel_en/tools/audit_webnovel.py

Menerapkan skill storyboard: panjang, scene, rasio dialog, panjang kalimat,
hook, ejaan tokoh, tipografi, sains ber-DOI, timeline, neraca petunjuk.
Keluar 1 kalau ada FAIL.
"""
import glob, json, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIBLE = os.path.join(ROOT, "bible"); VOL = os.path.join(ROOT, "vol1")
sys.path.insert(0, BIBLE)
import struktur_100 as S

MIN_W, MAX_W = 1500, 2500
MIN_D, MAX_D = 20, 60      # rasio dialog %
MIN_S, MAX_S = 3, 6        # scene per bab
KAL_MIN, KAL_MAX = 8, 17   # rata-rata kata/kalimat
HOOK_MAX = 2
KLISE = ["shiver down her spine", "butterflies in her stomach", "their eyes locked",
         "little did they know", "only time would tell", "her heart skipped a beat"]
H = []

def ok(k, m): H.append(("OK", k, m))
def warn(k, m): H.append(("WARN", k, m))
def fail(k, m): H.append(("FAIL", k, m))
def load(n, d=None):
    p = os.path.join(BIBLE, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else (d or {})

def kalimat(t):
    return [s for s in re.split(r"(?<=[.!?\u2026])[\s\u201c\u201d]+", t.strip()) if s]

def metrik(isi):
    kata = isi.split()
    paras = [p.strip() for p in isi.split("\n\n") if p.strip()]
    dialog = " ".join(re.findall(r"\u201c(.*?)\u201d", isi, flags=re.S))
    kal = kalimat(re.sub(r"\u201c.*?\u201d", " ", isi, flags=re.S))
    return dict(kata=len(kata), par=len(paras),
                dialog=round(100 * len(dialog.split()) / max(1, len(kata))),
                kal=round(sum(len(k.split()) for k in kal) / max(1, len(kal)), 1),
                scene=len([b for b in re.split(r"\n-{3,}\n", isi) if b.strip() and not b.strip().startswith("*Next")]))

def main():
    rows = {r[0]: dict(zip(S.FIELDS, r)) for r in S.ALL}
    tokoh = load("tokoh.json"); sains = load("sains.json"); petunjuk = load("petunjuk.json")
    berkas = {}
    for p in glob.glob(os.path.join(VOL, "ch_*.md")):
        m = re.search(r"ch_(\d{3})\.md$", p)
        if m: berkas[int(m.group(1))] = p

    if not berkas:
        fail("struktur", "tidak ada naskah di novel_en/vol1/")
        return lapor()
    nomor = sorted(berkas)
    celah = [n for n in range(1, max(nomor) + 1) if n not in berkas]
    if celah: fail("struktur", "bab hilang: %s" % celah)
    ok("struktur", "%d dari 100 bab (%.0f%%)" % (len(nomor), len(nomor)))

    alias = {}
    for resmi, d in tokoh.items():
        for v in d.get("canon", []):
            alias.setdefault(v.lower(), set()).update(d.get("canon", [resmi]))

    teks, tanggal, metrik_semua = {}, [], {}
    for n in nomor:
        c = rows.get(n)
        judul, isi = open(berkas[n], encoding="utf-8").read().split("\n", 1)
        judul = judul.lstrip("# ").strip()
        teks[n] = isi; m = metrik(isi); metrik_semua[n] = m
        nama = "ch_%03d.md" % n
        if c:
            harap = c["t"]
            if judul.split("\u2014")[-1].strip().lower() != harap.lower():
                fail("judul", "%s: \u201c%s\u201d != \u201c%s\u201d" % (nama, judul, harap))
            tanggal.append((n, c["d"]))
        if m["kata"] < MIN_W: fail("panjang", "%s: %d kata (min %d)" % (nama, m["kata"], MIN_W))
        elif m["kata"] > MAX_W: warn("panjang", "%s: %d kata (maks %d)" % (nama, m["kata"], MAX_W))
        if m["dialog"] < MIN_D: fail("dialog", "%s: %d%% (min %d%%, skill storyboard)" % (nama, m["dialog"], MIN_D))
        elif m["dialog"] > MAX_D: warn("dialog", "%s: %d%% (maks %d%%)" % (nama, m["dialog"], MAX_D))
        if not (MIN_S <= m["scene"] <= MAX_S):
            warn("scene", "%s: %d scene (target %d\u2013%d)" % (nama, m["scene"], MIN_S, MAX_S))
        if not (KAL_MIN <= m["kal"] <= KAL_MAX):
            warn("kalimat", "%s: rata-rata %.1f kata (target %d\u2013%d)" % (nama, m["kal"], KAL_MIN, KAL_MAX))
        paras = [p for p in isi.split("\n\n") if p.strip() and not p.strip().startswith("*Next")]
        if paras and len(kalimat(paras[-1])) > HOOK_MAX:
            warn("hook", "%s: paragraf akhir %d kalimat" % (nama, len(kalimat(paras[-1]))))
        for resmi, d in tokoh.items():
            for salah in d.get("forbidden", []):
                if re.search(r"\b%s\b" % re.escape(salah), isi):
                    fail("nama", "%s: \u201c%s\u201d seharusnya \u201c%s\u201d" % (nama, salah, resmi))
        if '"' in isi: fail("tipografi", "%s: kutip lurus" % nama)
        if "  " in isi: warn("tipografi", "%s: spasi ganda" % nama)
        if "..." in isi: warn("tipografi", "%s: elipsis tiga titik" % nama)
        if c:
            for tok in [t.strip() for t in c["cast"].split(",")]:
                tok = re.sub(r"\s*\(.*?\)", "", tok).strip()
                if not tok or tok == c["pov"]: continue
                if not any(v.lower() in isi.lower() for v in alias.get(tok.lower(), [tok])):
                    warn("cast", "%s: \u201c%s\u201d tidak muncul" % (nama, tok))
            if c["sci"] != "-":
                for sid in [s.strip() for s in c["sci"].split(",")]:
                    a = sains.get(sid, {}).get("anchor", "")
                    if a and a.lower() not in isi.lower():
                        warn("sains", "%s: penambat %s tidak disebut" % (nama, sid))
        rendah = isi.lower()
        hit = [k for k in KLISE if k in rendah]
        if hit: warn("klise", "%s: %s" % (nama, "; ".join(hit)))
        for bad in ("TODO", "TKTK", "lorem"):
            if bad.lower() in rendah: fail("kebersihan", "%s: \u201c%s\u201d" % (nama, bad))

    for i in range(1, len(tanggal)):
        if tanggal[i][1] < tanggal[i - 1][1]:
            fail("timeline", "bab %d mendahului bab %d" % (tanggal[i][0], tanggal[i - 1][0]))
    if tanggal and not any(h[1] == "timeline" and h[0] == "FAIL" for h in H):
        ok("timeline", "%d tanggal berurutan" % len(tanggal))

    # petunjuk
    tanam, bayar = {}, {}
    for n in nomor:
        c = rows.get(n)
        if not c: continue
        if c["plant"] != "-":
            for p in [x.strip() for x in c["plant"].split(",")]: tanam.setdefault(p, []).append(n)
        if c["pay"] != "-":
            for p in [x.strip() for x in c["pay"].split(",")]: bayar.setdefault(p, []).append(n)
    salah = [(p, tanam[p], bayar[p]) for p in bayar if p in tanam and min(bayar[p]) < min(tanam[p])]
    if salah: fail("petunjuk", "dibayar sebelum ditanam: %s" % salah)
    else: ok("petunjuk", "%d tanam, %d bayar" % (len(tanam), len(bayar)))

    # pengulangan
    if len(teks) > 1:
        def sh(t):
            w = re.findall(r"[a-z']+", t.lower())
            return set(tuple(w[i:i+9]) for i in range(max(0, len(w) - 8)))
        k = sorted(teks); mirip = []
        for i in range(len(k)):
            a = sh(teks[k[i]])
            for j in range(i + 1, len(k)):
                b = sh(teks[k[j]])
                if a and b and len(a & b) / max(1, min(len(a), len(b))) > 0.02:
                    mirip.append((k[i], k[j]))
        if mirip: warn("pengulangan", "paragraf kembar: %s" % mirip[:4])
        else: ok("pengulangan", "tidak ada paragraf kembar")

    # riset
    try:
        kartu = {k["id"]: k for k in json.load(open(os.path.join(ROOT, "research", "kutipan.json"), encoding="utf-8"))["kartu"]}
    except Exception:
        kartu = {}
    if not kartu: fail("riset", "research/kutipan.json tidak terbaca")
    else:
        salah = []
        for sid, d in sains.items():
            kk = kartu.get(sid)
            if not kk: salah.append("%s tanpa kartu" % sid)
            elif int(d.get("year", 0)) != int(kk.get("tahun", -1)): salah.append("%s tahun beda" % sid)
            elif not kk.get("doi"): salah.append("%s tanpa DOI" % sid)
        if salah: fail("riset", "; ".join(salah))
        else: ok("riset", "%d penambat sinkron dengan DOI" % len(sains))
    return lapor()

def lapor():
    for t, k, m in sorted(H, key=lambda h: ({"FAIL":0,"WARN":1,"OK":2}[h[0]], h[1])):
        print("%-4s %-12s %s" % (t, k, m))
    nf = sum(1 for h in H if h[0]=="FAIL"); nw = sum(1 for h in H if h[0]=="WARN"); no = sum(1 for h in H if h[0]=="OK")
    print("\nFAIL %d | WARN %d | OK %d" % (nf, nw, no))
    return 1 if nf else 0

if __name__ == "__main__":
    sys.exit(main())
