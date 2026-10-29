# -*- coding: utf-8 -*-
"""Edisi digital: sampul berwarna sebagai halaman pertama.

Halaman 1 file interior adalah halaman judul tipografis (teks saja, tanpa
gambar). Pembeli yang mengunduh PDF melihat halaman teks sebagai halaman
pertama, dan kesannya seperti naskah yang belum selesai — bukan buku.

Skrip ini membuat edisi digital yang **menukar** halaman judul itu dengan
sampul berwarna penuh (A4, tanpa margin). Karena yang ditukar, bukan
disisipkan:

  * jumlah halaman tetap sama (457 / 473),
  * nomor folio yang tercetak di kaki halaman tidak bergeser,
  * Daftar Isi, Indeks, dan bookmark tetap menunjuk halaman yang benar.

File `*_interior.pdf` **tidak diubah** — itu yang dikirim ke percetakan.

Jalankan: python make_ebook.py
"""
import os

import pypdf
from fpdf import FPDF

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "book", "publish")

EDITIONS = [
    ("Surviving the Future — EN", "Surviving_the_Future_EN"),
    ("Bertahan Hidup di Masa Depan — ID", "Bertahan_Hidup_di_Masa_Depan_ID"),
]


def build_cover(jpg, out):
    """Satu halaman A4 penuh dari berkas sampul depan."""
    pdf = FPDF(unit="pt", format="A4")
    pdf.set_auto_page_break(False)
    pdf.set_margins(0, 0, 0)
    pdf.add_page()
    # w+h sekaligus = skala penuh; rasio sampul 0,7068 vs A4 0,7071,
    # selisihnya 0,04 persen sehingga tidak terlihat melar.
    pdf.image(jpg, x=0, y=0, w=pdf.w, h=pdf.h)
    pdf.output(out)


def build(slug, label):
    interior = os.path.join(PUB, slug + "_interior.pdf")
    jpg = os.path.join(PUB, slug + "_cover_front.jpg")
    ebook = os.path.join(PUB, slug + "_ebook.pdf")
    tmp = os.path.join(PUB, ".cover_tmp.pdf")

    for f in (interior, jpg):
        if not os.path.exists(f):
            raise SystemExit("berkas hilang: " + f)

    build_cover(jpg, tmp)

    src = pypdf.PdfReader(interior)
    n_src = len(src.pages)
    cover = pypdf.PdfReader(tmp)

    writer = pypdf.PdfWriter(clone_from=src)
    writer.remove_page(0)                      # buang halaman judul teks
    writer.insert_page(cover.pages[0], 0)      # ganti dengan sampul
    with open(ebook, "wb") as fh:
        writer.write(fh)

    os.remove(tmp)

    out = pypdf.PdfReader(ebook)
    n_out = len(out.pages)
    assert n_out == n_src, (n_out, n_src)
    first = out.pages[0]
    print(f"  {label}")
    print(f"    {slug}_ebook.pdf  {n_out} hlm  "
          f"{os.path.getsize(ebook)/1048576:.2f} MB  "
          f"halaman 1: {first.mediabox.width:.0f}x{first.mediabox.height:.0f} pt")
    return n_out


def main():
    print("edisi digital (sampul + isi):")
    total = 0
    for label, slug in EDITIONS:
        total = build(slug, label)
    print(f"selesai — {total} halaman per edisi")


if __name__ == "__main__":
    main()
