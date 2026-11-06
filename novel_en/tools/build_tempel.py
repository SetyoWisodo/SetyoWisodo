#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_tempel.py — versi SIAP TEMPEL (tanpa sunting lagi) untuk Wattpad & Fizzo.

    python3 novel_en/tools/build_tempel.py          # rakit folder siap_tempel/
    python3 novel_en/tools/build_tempel.py --cek    # periksa saja

Keluaran (di novel_en/siap_tempel/):
  isi/ch_01.txt … ch_34.txt   isi bab saja, teks polos, siap tempel ke kolom cerita
  00_daftar_judul.txt         daftar judul berurutan, siap tempel ke kolom judul
  99_gabung_vol1.txt          seluruh bab dalam satu berkas (arsip/cadangan)
  CARA_TEMPEL.md              urutan tempel + catatan

Aturan pembersihan: markdown hilang, penekanan dijadikan teks biasa, pemisah scene
menjadi ***, kutipan/apostrof lengkung, satu baris kosong antarparagraf, tanpa spasi ekor.
"""
import glob, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "vol1")
OUT = os.path.join(ROOT, "siap_tempel")
PEMISAH = "***"
MAKS_KAR_WATTPAD = 50000


def kutip_lengkung(t):
    """' -> ’ , " -> “ ” (bergantian), tanpa menyentuh apostrof di dalam kata."""
    t = t.replace("\u2019", "'")
    t = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "\u2019", t)      # don't, mother's
    t = re.sub(r"(?<=[A-Za-z])'(?![A-Za-z])", "\u2019", t)      # akhir kata: engineers'
    untuk_buka = True
    keluaran = []
    for ch in t:
        if ch == '"':
            keluaran.append("\u201c" if untuk_buka else "\u201d")
            untuk_buka = not untuk_buka
        else:
            if ch == "\n":
                untuk_buka = True
            keluaran.append(ch)
    return "".join(keluaran)


def bersihkan(isi):
    t = isi.replace("\r\n", "\n").replace("\t", "    ")
    t = re.sub(r"\n+\*Next:[^\n]*\*\s*$", "", t.strip())
    t = re.sub(r"\n+-{3,}\s*$", "", t.strip())
    t = re.sub(r"(?m)^#{1,6}\s*", "", t)                 # judul markdown
    t = re.sub(r"(?m)^>\s?", "", t)                      # kutipan blok
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)               # tebal
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", t)  # miring
    t = re.sub(r"(?m)^-{3,}\s*$", PEMISAH, t)            # pemisah scene
    t = t.replace("`", "")
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", t)          # tautan -> teks
    t = kutip_lengkung(t)
    t = "\n".join(baris.rstrip() for baris in t.split("\n"))
    t = re.sub(r" {2,}", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"\n *\* \* \* *\n", "\n\n" + PEMISAH + "\n\n", t)
    return t.strip() + "\n"


def baca(path):
    mentah = open(path, encoding="utf-8").read().replace("\r\n", "\n").strip()
    baris = mentah.split("\n")
    judul_asli = baris[0].lstrip("# ").strip()
    bagian = [x.strip() for x in judul_asli.split("\u2014")]
    judul = bagian[-1] if len(bagian) > 1 else judul_asli
    isi = bersihkan("\n".join(baris[1:]))
    return judul, isi


def masalah_dalam(nama, isi):
    salah = []
    if re.search(r"(?<!\*)\*\*(?!\*)", isi):
        salah.append("%s: masih ada penekanan **" % nama)
    if re.search(r"(?<!\*)\*(?!\*)", isi):
        salah.append("%s: masih ada tanda bintang tunggal" % nama)
    if re.search(r"(?m)^#", isi):
        salah.append("%s: masih ada judul markdown" % nama)
    if re.search(r"(?m)^-{3,}$", isi):
        salah.append("%s: masih ada ---" % nama)
    if "]" in isi and "](" in isi:
        salah.append("%s: masih ada tautan markdown" % nama)
    if re.search(r"[ \t]+\n", isi):
        salah.append("%s: ada spasi ekor" % nama)
    if re.search(r"\n{3,}", isi):
        salah.append("%s: ada baris kosong berlebih" % nama)
    if '"' in isi or re.search(r"(?<=[A-Za-z])'(?=[A-Za-z])", isi):
        salah.append("%s: masih ada kutip lurus" % nama)
    if len(isi) > MAKS_KAR_WATTPAD:
        salah.append("%s: %d karakter (batas Wattpad %d)" % (nama, len(isi), MAKS_KAR_WATTPAD))
    return salah


def main():
    cek_saja = "--cek" in sys.argv
    berkas = {}
    for p in glob.glob(os.path.join(V, "ch_*.md")):
        m = re.search(r"ch_(\d{3})\.md$", p)
        if m:
            berkas[int(m.group(1))] = p
    if not berkas:
        sys.exit("Tidak ada bab di vol1/")

    bab, salah, total_kar = [], [], 0
    for n in sorted(berkas):
        judul, isi = baca(berkas[n])
        salah += masalah_dalam("ch_%03d" % n, isi)
        total_kar += len(isi)
        bab.append((n, judul, isi))

    print("bab: %d | karakter: %s | masalah: %d" % (len(bab), format(total_kar, ","), len(salah)))
    for s in salah:
        print("  -", s)
    if cek_saja:
        return 1 if salah else 0

    os.makedirs(os.path.join(OUT, "isi"), exist_ok=True)
    for lama in glob.glob(os.path.join(OUT, "isi", "*.txt")):
        os.remove(lama)

    for n, judul, isi in bab:
        open(os.path.join(OUT, "isi", "ch_%02d.txt" % n), "w", encoding="utf-8").write(isi)

    # daftar judul: satu baris per bab, siap salin ke kolom judul
    L = ["DAFTAR JUDUL — Volume I (tempel satu per satu ke kolom judul)", ""]
    for n, judul, isi in bab:
        L.append("%02d. %s  \u2014  %s kata \u00b7 %s karakter" % (n, judul, format(len(isi.split()), ","), format(len(isi), ",")))
    L += ["", "Kolom judul Wattpad/Fizzo: isi hanya judulnya (tanpa nomor).",
          "Contoh bab 1:  Buoy in Winter", ""]
    open(os.path.join(OUT, "00_daftar_judul.txt"), "w", encoding="utf-8").write("\n".join(L))

    # gabungan
    G = []
    for n, judul, isi in bab:
        G += ["CHAPTER %d" % n, judul.upper(), "", isi.strip(), "", "=" * 60, ""]
    open(os.path.join(OUT, "99_gabung_vol1.txt"), "w", encoding="utf-8").write("\n".join(G).strip() + "\n")

    cara = """# Cara tempel (tanpa sunting)

Berkas di folder `isi/` sudah bersih: tanpa markdown, tanpa tanda bintang penekanan,
kutipan lengkung, satu baris kosong antarparagraf, pemisah scene `***`.

## Wattpad
1. Cerita → **Add new part**.
2. Kolom **Part title**: salin satu baris judul dari `00_daftar_judul.txt`
   (contoh: `Buoy in Winter` — tanpa nomor `01.`).
3. Kolom **Story text**: buka `isi/ch_01.txt`, pilih semua (Ctrl+A), tempel (Ctrl+V).
4. **Publish** → ulangi untuk bab berikutnya dengan berkas `ch_02.txt` dst.
5. Jangan menekan Enter di akhir tempelan; berkas sudah diakhiri satu baris kosong.

## Fizzo Novel
1. Write → **New chapter**.
2. Judul dari `00_daftar_judul.txt`, isi dari `isi/ch_XX.txt`.
3. Fizzo menuntut minimal 1.000 kata per hari unggah; setiap bab sudah 1.500+ kata,
   jadi satu bab per hari aman.

## Kalau perlu arsip atau cetak
`99_gabung_vol1.txt` memuat seluruh bab berurutan dengan pembatas `====`.

## Catatan
- Penekanan huruf miring hilang saat ditempel (Wattpad/Fizzo tidak menerima format dari
  tempelan teks). Kalimatnya tetap utuh; yang hilang hanya kemiringan huruf.
- Semua bab 1.500–2.500 kata dan di bawah 50.000 karakter (batas satu part Wattpad).
- Setelah bab baru ditulis, jalankan ulang `python3 novel_en/tools/build_tempel.py`.
"""
    open(os.path.join(OUT, "CARA_TEMPEL.md"), "w", encoding="utf-8").write(cara)
    terbesar = max(len(i) for _, _, i in bab)
    print("siap_tempel/: %d berkas isi + daftar judul + gabungan + cara tempel" % len(bab))
    print("berkas terbesar: %s karakter (batas Wattpad %s)" % (format(terbesar, ","), format(MAKS_KAR_WATTPAD, ",")))
    return 1 if salah else 0


if __name__ == "__main__":
    sys.exit(main())
