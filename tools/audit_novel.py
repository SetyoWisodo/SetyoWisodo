#!/usr/bin/env python3
"""audit_novel.py — pemeriksaan otomatis naskah novel berbasis Markdown.

Dipakai untuk proyek novel romance; diadaptasi dari final_audit.py yang dipakai
pada buku non-fiksi 457 halaman. Setiap pemeriksaan menghasilkan FAIL / WARN /
OK, dan skrip keluar dengan kode 1 kalau ada FAIL, sehingga bisa dipakai di
pre-commit atau CI.

Struktur yang diharapkan:

    manuscript/bab_01.md ... bab_24.md
    bible/tokoh.json      {"Alya": ["Alia", "Alliya"], "Bima": ["Bimma"]}
    bible/timeline.json   [{"bab": 1, "tanggal": "2026-03-02"}, ...]

Jalankan:  python3 tools/audit_novel.py
"""
import glob
import json
import os
import re
import sys
from collections import Counter

BAB_GLOB = "manuscript/bab_*.md"
MIN_KATA, MAX_KATA = 1500, 5000
MAKS_PANJANG_BAB = 1.25          # bab terpanjang maksimal 1,25x median

# Frasa klise romance yang paling sering muncul tanpa disadari penulis.
KLISE = [
    "a breath she didn't know she was holding",
    "a breath he didn't know he was holding",
    "shiver down her spine",
    "shiver ran down",
    "butterflies in her stomach",
    "their eyes locked",
    "electricity shot through",
    "he smirked",
    "she rolled her eyes",
    "little did they know",
    "only time would tell",
    "and then everything changed",
]

HASIL = []


def ok(kat, pesan):
    HASIL.append(("OK", kat, pesan))


def warn(kat, pesan):
    HASIL.append(("WARN", kat, pesan))


def fail(kat, pesan):
    HASIL.append(("FAIL", kat, pesan))


def baca(path):
    return open(path, encoding="utf-8").read()


def isi_bab(teks):
    """Buang judul bab dan penanda markdown lain sebelum menghitung kata."""
    baris = [b for b in teks.splitlines() if not b.strip().startswith("#")]
    return " ".join(baris)


def main():
    berkas = sorted(glob.glob(BAB_GLOB))
    if not berkas:
        fail("struktur", "tidak ada berkas %s" % BAB_GLOB)
        lapor()
        return 1

    # 1. struktur: jumlah bab & panjang
    if len(berkas) != 24:
        warn("struktur", "%d bab (target 24)" % len(berkas))
    else:
        ok("struktur", "24 bab")

    kata = {}
    pendek, panjang = [], []
    for b in berkas:
        n = len(isi_bab(baca(b)).split())
        kata[b] = n
        nama = os.path.basename(b)
        if n < MIN_KATA:
            pendek.append((nama, n))
        elif n > MAX_KATA:
            panjang.append((nama, n))
    for nama, n in pendek[:6]:
        fail("panjang", "%s hanya %d kata (minimum %d)" % (nama, n, MIN_KATA))
    if len(pendek) > 6:
        fail("panjang", "dan %d bab lain di bawah %d kata" % (len(pendek) - 6, MIN_KATA))
    for nama, n in panjang[:6]:
        fail("panjang", "%s %d kata (maksimum %d)" % (nama, n, MAX_KATA))
    if len(panjang) > 6:
        fail("panjang", "dan %d bab lain di atas %d kata" % (len(panjang) - 6, MAX_KATA))
    if kata:
        urut = sorted(kata.values())
        median = urut[len(urut) // 2]
        for b, n in kata.items():
            if n > median * MAKS_PANJANG_BAB:
                warn("panjang", "%s %.2fx median — periksa apakah ada adegan berlebih"
                     % (os.path.basename(b), n / median))
        if not any(h[0] == "FAIL" and h[1] == "panjang" for h in HASIL):
            ok("panjang", "semua bab dalam rentang %d–%d kata (median %d)"
               % (min(kata.values()), max(kata.values()), median))

    teks_semua = "\n\n".join(isi_bab(baca(b)) for b in berkas)

    # 2. frasa klise
    temuan = {k: teks_semua.lower().count(k) for k in KLISE}
    temuan = {k: v for k, v in temuan.items() if v}
    if temuan:
        rinci = ", ".join("%s (%d)" % (k, v) for k, v in
                          sorted(temuan.items(), key=lambda x: -x[1])[:5])
        (fail if sum(temuan.values()) > 8 else warn)("klise", rinci)
    else:
        ok("klise", "nol frasa klise dari daftar pantau")

    # 3. ejaan nama tokoh
    if os.path.exists("bible/tokoh.json"):
        tokoh = json.load(open("bible/tokoh.json", encoding="utf-8"))
        salah = []
        for benar, varian in tokoh.items():
            for v in varian:
                n = len(re.findall(r"\b%s\b" % re.escape(v), teks_semua))
                if n:
                    salah.append("%s seharusnya %s (%d)" % (v, benar, n))
        if salah:
            fail("nama", "; ".join(salah))
        else:
            ok("nama", "ejaan %d tokoh konsisten" % len(tokoh))

    # 4. tipografi
    if "  " in teks_semua:
        warn("tipografi", "ada spasi ganda")
    if "..." in teks_semua:
        warn("tipografi", "elipsis tiga titik; pakai karakter … (U+2026)")
    if not any(h[0] != "OK" and h[1] == "tipografi" for h in HASIL):
        ok("tipografi", "spasi dan elipsis bersih")

    # 5. pembuka bab tidak boleh saling meniru
    pembuka = {}
    for b in berkas:
        par = [p for p in isi_bab(baca(b)).split("\n\n") if p.strip()]
        if par:
            pembuka[b] = set(re.findall(r"\w+", par[0].lower()))
    mirip = []
    kunci = list(pembuka)
    for i in range(len(kunci)):
        for j in range(i + 1, len(kunci)):
            a, c = pembuka[kunci[i]], pembuka[kunci[j]]
            if a and c and len(a & c) / len(a | c) > 0.45:
                mirip.append("%s ~ %s" % (os.path.basename(kunci[i]),
                                          os.path.basename(kunci[j])))
    if mirip:
        contoh = ", ".join(mirip[:4])
        sisa = (" dan %d pasangan lain" % (len(mirip) - 4)) if len(mirip) > 4 else ""
        warn("variasi", "pembuka bab terlalu mirip: %s%s" % (contoh, sisa))
    else:
        ok("variasi", "pembuka 24 bab berbeda")

    # 6. timeline
    if os.path.exists("bible/timeline.json"):
        peristiwa = json.load(open("bible/timeline.json", encoding="utf-8"))
        salah = []
        sebelumnya = None
        for p in sorted(peristiwa, key=lambda x: x["bab"]):
            if sebelumnya and p["tanggal"] < sebelumnya["tanggal"]:
                salah.append("bab %d (%s) mendahului bab %d (%s)"
                             % (p["bab"], p["tanggal"],
                                sebelumnya["bab"], sebelumnya["tanggal"]))
            sebelumnya = p
        if salah:
            fail("timeline", "; ".join(salah))
        else:
            ok("timeline", "%d titik waktu berurutan" % len(peristiwa))

    # 7. POV — satu bab satu sudut pandang
    pov = {}
    for b in berkas:
        t = isi_bab(baca(b))
        nama = re.findall(r"\b(Alya|Bima)\b", t)
        if nama:
            pov[os.path.basename(b)] = Counter(nama).most_common(1)[0][0]
    ganti = [b for i, b in enumerate(pov) if i and pov[b] != pov[list(pov)[i - 1]]]
    if len(ganti) > len(pov) // 2:
        warn("pov", "sudut pandang berganti %d kali — pastikan disengaja" % len(ganti))
    elif pov:
        ok("pov", "sudut pandang tiap bab terdeteksi (%d bab)" % len(pov))

    return lapor()


def lapor():
    urutan = {"FAIL": 0, "WARN": 1, "OK": 2}
    for tingkat, kat, pesan in sorted(HASIL, key=lambda h: (urutan[h[0]], h[1])):
        print("%-4s %-10s %s" % (tingkat, kat, pesan))
    n_fail = sum(1 for h in HASIL if h[0] == "FAIL")
    n_warn = sum(1 for h in HASIL if h[0] == "WARN")
    n_ok = sum(1 for h in HASIL if h[0] == "OK")
    print("\nFAIL %d | WARN %d | OK %d" % (n_fail, n_warn, n_ok))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
