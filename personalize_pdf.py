# -*- coding: utf-8 -*-
"""Beri tanda pemilik pada salinan yang dibeli (personal watermark).

Yang dilakukan untuk setiap pembeli:
  1. stempel samar di kaki setiap halaman berisi nomor lisensi + nama pembeli
  2. halaman "Salinan ini milik ..." di depan, dengan nomor lisensi
  3. nomor lisensi yang sama ditulis ke metadata PDF

Ini bukan pengaman teknis — PDF tetap bisa disalin. Yang dicapai: salinan yang
bocor bisa dilacak ke pembeli asalnya, dan pembeli tahu bahwa salinannya
bertanda namanya. Itu yang membuat orang berpikir dua kali sebelum menyebarkan.

Pemakaian:
    python personalize_pdf.py --edition en --name "Budi Santoso" --order INV-2026-0142
    python personalize_pdf.py --edition id --name "Budi Santoso" --order INV-2026-0142

Keluaran: book/publish/sold/Surviving_the_Future_EN_Budi_Santoso.pdf
"""
import argparse
import datetime as dt
import os
import re

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "book/publish")
OUTDIR = os.path.join(PUB, "sold")
FONTS = os.path.join(HERE, "book/fonts")

ED = {
    "en": dict(src=os.path.join(HERE, "Surviving_the_Future.pdf"),
               title="SURVIVING THE FUTURE",
               lang="en"),
    "id": dict(src=os.path.join(HERE, "Surviving_the_Future_ID.pdf"),
               title="BERTAHAN HIDUP DI MASA DEPAN",
               lang="id"),
}

TXT = {
    "en": dict(
        stamp="Licensed copy  \u00b7  {order}  \u00b7  {name}",
        head="THIS COPY IS LICENSED TO",
        body=("This file was issued to the purchaser named below. It carries a licence "
              "number on every page. If you received it from anyone else, it was shared "
              "without permission \u2014 please buy your own copy."),
        order="Licence", date="Issued", pages="Pages",
    ),
    "id": dict(
        stamp="Salinan berlisensi  \u00b7  {order}  \u00b7  {name}",
        head="SALINAN INI DILISENSIKAN KEPADA",
        body=("Berkas ini diterbitkan untuk pembeli yang namanya tercantum di bawah. "
              "Nomor lisensinya tercetak di setiap halaman. Jika Anda menerima berkas ini "
              "dari orang lain, berarti berkas itu dibagikan tanpa izin \u2014 silakan beli "
              "salinan Anda sendiri."),
        order="Lisensi", date="Diterbitkan", pages="Halaman",
    ),
}

NAVY = (0.043, 0.086, 0.133)
AMBER = (0.910, 0.639, 0.239)
IVORY = (0.965, 0.953, 0.922)
MUTED = (0.62, 0.68, 0.75)
STAMP = (0.47, 0.50, 0.55)


def slug(text):
    s = re.sub(r"[^A-Za-z0-9]+", "_", text.strip()).strip("_")
    return s or "pembeli"


def license_page(doc, cfg, txt, name, order, issued, total):
    """Halaman depan: pernyataan lisensi dengan nama pembeli."""
    page = doc.new_page(pno=-1, width=595, height=842)     # A4, ditambahkan di akhir
    page.draw_rect(pymupdf.Rect(0, 0, 595, 842), color=None, fill=NAVY)

    page.insert_font(fontname="sb", fontfile=os.path.join(FONTS, "SourceSerif4-Semibold.otf"))
    page.insert_font(fontname="sr", fontfile=os.path.join(FONTS, "SourceSerif4-Regular.otf"))
    page.insert_font(fontname="si", fontfile=os.path.join(FONTS, "SourceSerif4-It.otf"))
    page.insert_font(fontname="nb", fontfile=os.path.join(FONTS, "SourceSans3-Semibold.otf"))

    m, y = 72.0, 190.0
    page.insert_text((m, y), txt["head"], fontname="nb", fontsize=11, color=AMBER)
    y += 12
    page.draw_line(pymupdf.Point(m, y), pymupdf.Point(m + 52, y), color=AMBER, width=2)
    y += 46

    # nama pembeli, dibungkus bila panjang
    box = pymupdf.Rect(m, y, 595 - m, y + 90)
    page.insert_textbox(box, name, fontname="sb", fontsize=23, color=IVORY, lineheight=1.25)
    y += 74

    page.insert_text((m, y), cfg["title"], fontname="si", fontsize=13, color=AMBER)
    y += 46

    page.insert_text((m, y), f"{txt['order']}:  {order}", fontname="nb", fontsize=11, color=IVORY)
    y += 20
    page.insert_text((m, y), f"{txt['date']}:  {issued}", fontname="nr"
                     if False else "sr", fontsize=11, color=MUTED)
    y += 20
    page.insert_text((m, y), f"{txt['pages']}:  {total}", fontname="sr", fontsize=11, color=MUTED)
    y += 44

    page.insert_textbox(pymupdf.Rect(m, y, 595 - m, y + 140), txt["body"],
                        fontname="sr", fontsize=10.5, color=MUTED, lineheight=1.45)
    # pindahkan halaman lisensi ke paling depan
    doc.move_page(doc.page_count - 1, 0)
    return doc[0]


def build(edition, name, order, protect=False, owner_pw=None):
    cfg = ED[edition]
    txt = TXT[cfg["lang"]]
    issued = dt.date.today().isoformat()

    doc = pymupdf.open(cfg["src"])
    total = doc.page_count

    licensed = license_page(doc, cfg, txt, name, order, issued, total)

    # stempel samar di setiap halaman isi (mulai halaman 2)
    stamp = txt["stamp"].format(order=order, name=name)
    for i in range(1, doc.page_count):
        page = doc[i]
        r = page.rect
        page.insert_text((r.width / 2 - 118, r.height - 13), stamp,
                         fontname="helv", fontsize=5.6, color=STAMP,
                         render_mode=0)

    doc.set_metadata({
        "title": cfg["title"],
        "author": "Setyo Wisodo",
        "subject": f"Licensed to {name}  \u00b7  {order}",
        "keywords": f"licence {order}; buyer {name}",
        "creator": "Setyo Wisodo",
        "producer": "fpdf2",
    })

    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, f"{os.path.basename(cfg['src'])[:-4]}_{slug(name)}.pdf")
    if protect:
        # cetak dan salin teks tetap boleh (aksesibilitas); ubah dan anotasi tidak.
        # Ini tidak menghentikan pembajak, tetapi menghentikan penyalinan iseng.
        perm = int(pymupdf.PDF_PERM_PRINT | pymupdf.PDF_PERM_COPY
                   | pymupdf.PDF_PERM_ACCESSIBILITY)
        doc.save(out, encryption=pymupdf.PDF_ENCRYPT_AES_256,
                 owner_pw=owner_pw or f"owner-{order}", user_pw="",
                 permissions=perm, garbage=3, deflate=True)
    else:
        doc.save(out, garbage=3, deflate=True)
    doc.close()
    mode = "berproteksi" if protect else "tanpa proteksi"
    print(f"  -> {os.path.relpath(out, HERE)}  ({total + 1} halaman, lisensi {order}, {mode})")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Tandai salinan yang dibeli dengan nama pembeli.")
    ap.add_argument("--edition", choices=["en", "id"], required=True)
    ap.add_argument("--name", required=True, help="nama pembeli")
    ap.add_argument("--order", required=True, help="nomor pesanan / nomor lisensi")
    ap.add_argument("--protect", action="store_true",
                    help="kunci izin: boleh cetak & salin teks, tidak boleh ubah/anotasi")
    ap.add_argument("--owner-pw", default=None,
                    help="kata sandi pemilik (default: owner-<nomor lisensi>)")
    a = ap.parse_args()
    build(a.edition, a.name, a.order, protect=a.protect, owner_pw=a.owner_pw)
