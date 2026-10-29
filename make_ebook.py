# -*- coding: utf-8 -*-
"""Edisi digital: sampul berwarna sebagai halaman pertama, halaman judul tetap.

Halaman 1 file interior adalah halaman judul tipografis (teks saja). Pembeli
yang membukanya melihat teks polos lebih dulu, jadi kesannya naskah, bukan buku.

Skrip ini **menyisipkan** satu halaman sampul di depan, sehingga:

  * halaman 1 = sampul berwarna (A4 penuh, tanpa margin, tanpa folio),
  * halaman 2 = halaman judul seperti aslinya,
  * total halaman menjadi 458 (EN) dan 474 (ID),

Nomor folio yang tercetak tidak berubah, jadi Daftar Isi dan Indeks tetap
menunjuk halaman yang benar. Bookmark digeser satu halaman agar tetap mendarat
di halaman yang sama seperti sebelumnya.

File `*_interior.pdf` **tidak diubah** — itu yang dikirim ke percetakan.

Jalankan: python make_ebook.py
"""
import os

import pymupdf
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
    # selisih 0,04 persen sehingga tidak terlihat melar.
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

    doc = pymupdf.open(interior)
    n_src = doc.page_count
    toc_before = doc.get_toc(simple=True)

    cover = pymupdf.open(tmp)
    doc.insert_pdf(cover, start_at=0)          # halaman judul tetap, hanya bergeser
    cover.close()

    # Bookmark: pymupdf membiarkan nomor halaman apa adanya, sehingga seluruh
    # tujuan harus digeser satu halaman agar mendarat di tempat yang sama.
    doc.set_toc([[lvl, title, page + 1] for lvl, title, page in toc_before])

    doc.set_metadata(dict(doc.metadata, producer="fpdf2 + PyMuPDF"))
    doc.save(ebook, garbage=4, deflate=True)
    doc.close()
    os.remove(tmp)

    # ---- verifikasi ----
    out = pymupdf.open(ebook)
    n_out = out.page_count
    assert n_out == n_src + 1, (n_out, n_src)
    assert len(out.get_toc()) == len(toc_before), (len(out.get_toc()), len(toc_before))
    first = out[0]
    assert not first.get_text().strip(), "halaman sampul masih berisi teks"
    assert first.get_images(full=True), "halaman sampul tidak memuat gambar"

    # setiap bookmark bab harus mendarat di halaman yang memuat judulnya.
    # Teks judul dicetak dengan jarak antarhuruf ("C H A P T E R 1"),
    # jadi perbandingan dilakukan tanpa spasi sama sekali.
    def squash(x):
        return "".join(x.lower().split())

    checked = 0
    for _lvl, title, page in out.get_toc():
        if not title.lower().startswith(("chapter ", "bab ")):
            continue
        head, _, rest = title.partition(":")
        assert squash(head) in squash(out[page - 1].get_text()), (title, page)
        assert squash(rest.strip().split(":")[0]) in squash(out[page - 1].get_text()), (title, page)
        checked += 1
    assert checked >= 20, checked

    size = os.path.getsize(ebook) / 1048576
    print(f"  {label}")
    print(f"    {slug}_ebook.pdf  {n_out} hlm  {size:.2f} MB  "
          f"halaman 1: sampul {first.rect.width:.0f}x{first.rect.height:.0f} pt  "
          f"halaman 2: {out[1].get_text().strip().splitlines()[0][:32]}")
    out.close()
    return n_out


def main():
    print("edisi digital (sampul + halaman judul + isi):")
    for label, slug in EDITIONS:
        build(slug, label)
    print("selesai")


if __name__ == "__main__":
    main()
