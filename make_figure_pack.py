# -*- coding: utf-8 -*-
"""Paket gambar untuk pembeli: 11 gambar 300 dpi + indeks + lisensi pakai.

Harga jual yang tinggi menuntut isi yang benar-benar dipakai pembeli. Pembaca
profesional (dosen, perencana, jurnalis) membutuhkan gambarnya lepas dari buku
untuk slide dan laporan — itulah yang dijual paket ini, bukan file tambahan
yang sekadar menambah jumlah.

Jalankan: python make_figure_pack.py
Keluaran: book/publish/*_figures.zip
"""
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "book/publish")
FIGS = os.path.join(HERE, "figures")

PACKS = [
    dict(src="book.md", suffix="", out="Surviving_the_Future_EN_figures.zip",
         lang="en", title="Surviving the Future"),
    dict(src="book_id.md", suffix="_id", out="Bertahan_Hidup_di_Masa_Depan_ID_figures.zip",
         lang="id", title="Bertahan Hidup di Masa Depan"),
]


def parse(md_path, lang):
    s = open(md_path, encoding="utf-8").read()
    pat = r"!\[((?:Figure|Gambar) \d+\.\d+ [^\]]*)\]\(figures/([^)]+)\)\|\|(.*)"
    rows = re.findall(pat, s)
    return [(cap.strip(), fn.strip(), src.strip()) for cap, fn, src in rows]


def readme(cfg, rows):
    if cfg["lang"] == "en":
        head = f"""FIGURE PACK - {cfg['title']}
==============================================

Eleven figures from the book, 300 dpi PNG, with the caption and source line
for each. Sized for slides, reports and teaching material.

WHAT YOU MAY DO
  Use these figures in your own presentations, lectures, reports and
  publications. No permission needed, no fee, no attribution required --
  though citing the book is good practice and helps the argument travel.

WHAT YOU MAY NOT DO
  Resell the figures, or redistribute the pack itself as a standalone product.

Each figure in the book carries its own source line. Reproduce that line when
you use the figure, because the data belongs to the original source, not to
this book. The footnote below each figure tells you where the numbers came from.
"""
    else:
        head = f"""PAKET GAMBAR - {cfg['title']}
==============================================

Sebelas gambar dari buku, PNG 300 dpi, lengkap dengan keterangan dan baris
sumbernya. Ukurannya siap untuk slide, laporan, dan bahan ajar.

YANG BOLEH ANDA LAKUKAN
  Memakai gambar ini di presentasi, kuliah, laporan, dan publikasi Anda
  sendiri. Tanpa izin, tanpa biaya, tanpa wajib menyebutkan sumber --
  meski mengutip bukunya adalah kebiasaan baik dan membantu argumennya
  menyebar.

YANG TIDAK BOLEH
  Menjual kembali gambarnya, atau menyebarkan paket ini sebagai produk
  tersendiri.

Setiap gambar membawa baris sumbernya sendiri. Sertakan baris itu saat Anda
memakainya, karena datanya milik sumber aslinya, bukan milik buku ini.
"""
    body = ["", "DAFTAR GAMBAR" if cfg["lang"] == "id" else "INDEX", "-" * 60, ""]
    for cap, fn, src in rows:
        body.append(f"  {fn}")
        body.append(f"    {cap}")
        body.append(f"    {src}")
        body.append("")
    return head + "\n".join(body)


def build(cfg):
    rows = parse(os.path.join(HERE, cfg["src"]), cfg["lang"])
    out = os.path.join(PUB, cfg["out"])
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("README.txt", readme(cfg, rows))
        for cap, fn, _ in rows:
            path = os.path.join(FIGS, fn)
            z.write(path, arcname=f"figures/{fn}")
    print("  -> %-52s %2d gambar  %d KB"
          % (cfg["out"], len(rows), os.path.getsize(out) // 1024))
    return out


if __name__ == "__main__":
    print("paket gambar:")
    for c in PACKS:
        build(c)
