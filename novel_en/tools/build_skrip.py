#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_skrip.py — SATU berkas skrip final dari seluruh bab yang sudah ditulis.

    python3 novel_en/tools/build_skrip.py            # tulis berkas
    python3 novel_en/tools/build_skrip.py --cek      # hanya periksa, tidak menulis

Masukan : novel_en/vol1/ch_*.md + novel_en/bible/struktur_100.py + bible/adegan.json
Keluaran: novel_en/SKRIP_FINAL.md   naskah bersih: halaman judul, daftar isi, arc, bab
          novel_en/SKRIP_FINAL.txt  teks polos untuk unggah Wattpad/Fizzo

Idempoten: jalankan kapan pun; bab baru ikut otomatis tanpa skrip ini disunting.
"""
import glob, json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "bible")
V = os.path.join(ROOT, "vol1")
sys.path.insert(0, B)
import struktur_100 as S

JUDUL_ID = "Sebelum Cahaya Sampai"
JUDUL_EN = "Before the Light Arrives"
MIN_KATA, MAKS_KATA = 1500, 2500
PEMISAH_TXT = "* * *"


def baca_bab(path):
    """(judul asli tanpa '#', isi) — penunjuk serial & pemisah ekor dibuang."""
    mentah = open(path, encoding="utf-8").read().replace("\r\n", "\n").strip()
    baris = mentah.split("\n")
    judul = baris[0].lstrip("# ").strip()
    isi = "\n".join(baris[1:]).strip()
    isi = re.sub(r"\n+\*Next:[^\n]*\*\s*$", "", isi).strip()
    isi = re.sub(r"\n+-{3,}\s*$", "", isi).strip()
    isi = re.sub(r"\n{3,}", "\n\n", isi)
    return judul, isi


def kata(t):
    return len(t.split())


_SATUAN = ("Zero One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Thirteen "
           "Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen").split()
_PULUHAN = ("- - Twenty Thirty Forty Fifty Sixty Seventy Eighty Ninety").split()


def kata_angka(n):
    """35 -> Thirty-Five (1..100)."""
    if n < 20:
        return _SATUAN[n]
    if n < 100:
        p, s = divmod(n, 10)
        return _PULUHAN[p] + (("-" + _SATUAN[s]) if s else "")
    return "One Hundred"


def main():
    cek_saja = "--cek" in sys.argv
    rows = {r[0]: dict(zip(S.FIELDS, r)) for r in S.ALL}
    arc = {r[0]: (k, j) for k, j, g in S.ARCS for r in g}
    ad = {}
    if os.path.exists(os.path.join(B, "adegan.json")):
        ad = {b["n"]: b for b in json.load(open(os.path.join(B, "adegan.json"), encoding="utf-8"))["bab"]}

    berkas = {}
    for p in glob.glob(os.path.join(V, "ch_*.md")):
        m = re.search(r"ch_(\d{3})\.md$", p)
        if m:
            berkas[int(m.group(1))] = p
    if not berkas:
        sys.exit("Tidak ada bab di novel_en/vol1/")

    urut = sorted(berkas)
    bab, masalah = [], []
    for n in urut:
        judul_asli, isi = baca_bab(berkas[n])
        j = kata(isi)
        c = rows.get(n, {})
        judul = c.get("t") or judul_asli.split("\u2014")[-1].strip()
        if j < MIN_KATA:
            masalah.append("bab %d: %d kata (min %d)" % (n, j, MIN_KATA))
        if j > MAKS_KATA:
            masalah.append("bab %d: %d kata (maks %d)" % (n, j, MAKS_KATA))
        for buruk in ("TODO", "TKTK", "lorem"):
            if buruk.lower() in isi.lower():
                masalah.append("bab %d: memuat \u201c%s\u201d" % (n, buruk))
        if re.search(r"\*Next:", isi):
            masalah.append("bab %d: penunjuk serial masih tersisa" % n)
        bab.append(dict(n=n, judul=judul, judul_asli=judul_asli, isi=isi, kata=j,
                        pov=c.get("pov", "\u2014"),
                        templat=ad.get(n, {}).get("templates", []),
                        arc=arc.get(n, ("Arc", "\u2014"))))

    total = sum(b["kata"] for b in bab)
    celah = [i for i in range(1, max(urut) + 1) if i not in berkas]
    berikut = max(urut) + 1
    judul_berikut = rows.get(berikut, {}).get("t", "")
    if cek_saja:
        print("cek: %d bab | %s kata badan | masalah: %d" % (len(bab), format(total, ","), len(masalah)))
        for m in masalah:
            print("  -", m)
        return 1 if masalah else 0

    # ---------- halaman judul + daftar isi ----------
    L = []
    L += ["# %s" % JUDUL_ID, "", "## %s" % JUDUL_EN, "",
          "**Volume I \u00b7 bab %d\u2013%d dari rencana 100 bab**" % (urut[0], urut[-1]), "",
          "Fiksi ilmiah + romance \u00b7 bahasa Inggris \u00b7 naskah siap unggah", "",
          "| | |", "|---|---|",
          "| Bab tertulis | **%d** dari 100 |" % len(bab),
          "| Total kata (badan naskah) | **%s** |" % format(total, ","),
          "| Rata-rata | **%d kata/bab** |" % (total // len(bab)),
          "| Rentang | %d\u2013%d kata |" % (min(b["kata"] for b in bab), max(b["kata"] for b in bab)),
          "| POV | Nara (utama), Vey, Kirana |",
          "| Dirakit | %s |" % datetime.date.today().isoformat()]
    if celah:
        L.append("| Celah | bab %s belum ditulis |" % ", ".join(str(x) for x in celah))
    L += ["", "> Berkas ini dirakit otomatis oleh `novel_en/tools/build_skrip.py`. "
              "Jangan disunting langsung: sunting `vol1/ch_XXX.md`, lalu jalankan ulang skripnya.", "",
          "---", "", "## Daftar Isi", "",
          "| # | Bab | POV | Templat | Kata |", "|---:|---|---|---|---:|"]
    for b in bab:
        L.append("| %d | %s | %s | %s | %s |" % (b["n"], b["judul"], b["pov"],
                                                " + ".join(b["templat"]) or "\u2014", format(b["kata"], ",")))
    L.append("")

    # ---------- badan naskah ----------
    arc_kini = None
    for b in bab:
        k, j = b["arc"]
        if k != arc_kini:
            arc_kini = k
            L += ["", "---", "", "# %s \u00b7 %s" % (k, j), ""]
        else:
            L += ["", "---", ""]
        L += ["## %s" % b["judul_asli"], ""]
        L.append(b["isi"])
    L += ["", "---", ""]
    if judul_berikut:
        L.append("*Bersambung: Chapter %s \u2014 %s, belum ditulis.*" % (kata_angka(berikut), judul_berikut))
    else:
        L.append("*Akhir Volume I.*")
    L.append("")

    md = re.sub(r"\n{3,}", "\n\n", "\n".join(L)).strip() + "\n"

    # ---------- teks polos ----------
    T = ["%s" % JUDUL_ID, "%s" % JUDUL_EN, "",
         "Volume I \u00b7 bab %d\u2013%d dari rencana 100 bab" % (urut[0], urut[-1]),
         "Fiksi ilmiah + romance \u00b7 bahasa Inggris", "",
         "%d bab \u00b7 %s kata" % (len(bab), format(total, ",")), "", "=" * 60, ""]
    for b in bab:
        bagian = [x.strip() for x in b["judul_asli"].split("\u2014")]
        T += [bagian[0].upper()]
        if len(bagian) > 1:
            T.append(bagian[-1].upper())
        T += ["", "-" * 60, ""]
        badan = re.sub(r"(?m)^#{1,6}\s*", "", b["isi"])
        badan = re.sub(r"\*\*(.+?)\*\*", r"\1", badan)
        badan = re.sub(r"\*(.+?)\*", r"\1", badan)
        badan = re.sub(r"(?m)^-{3,}\s*$", PEMISAH_TXT, badan)
        T += [badan.strip(), "", "=" * 60, ""]
    txt = re.sub(r"\n{3,}", "\n\n", "\n".join(T)).strip() + "\n"

    p_md = os.path.join(ROOT, "SKRIP_FINAL.md")
    p_txt = os.path.join(ROOT, "SKRIP_FINAL.txt")
    open(p_md, "w", encoding="utf-8").write(md)
    open(p_txt, "w", encoding="utf-8").write(txt)
    print("SKRIP_FINAL.md  : %d bab | %s kata | %d KB" % (len(bab), format(total, ","), len(md.encode()) // 1024))
    print("SKRIP_FINAL.txt : %d bab | %s kata | %d KB" % (len(bab), format(total, ","), len(txt.encode()) // 1024))
    print("masalah         : %d" % len(masalah))
    for m in masalah:
        print("  -", m)
    return 1 if masalah else 0


if __name__ == "__main__":
    sys.exit(main())
