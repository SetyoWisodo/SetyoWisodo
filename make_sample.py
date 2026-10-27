# -*- coding: utf-8 -*-
"""Buat versi SAMPLE (gratis, beberapa lembar) dari PDF interior.

Strategi sampel — bukan sekadar "potong 10 halaman pertama":
  1. halaman depan lengkap (judul, hak cipta, DAFTAR ISI penuh)  -> menunjukkan skala
  2. Prakata                                                     -> membangun kredibilitas
  3. Bab 1 utuh                                                  -> membuktikan mutu tulisan
  4. sepasang halaman Bab 2 yang memuat gambar data              -> membuktikan klaim "data"
  5. halaman penutup: apa yang ada di balik sampel + ajakan

Tiap halaman sampel diberi catatan kaki kecil "Free sample", supaya kalau
berkas ini tersebar, ia menyebar bersama alamat pembeliannya.

Keluaran: book/publish/*_sample.pdf
Jalankan: python make_sample.py
"""
import os

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "book/publish")
FONTS = os.path.join(HERE, "book/fonts")

NAVY = (0.043, 0.086, 0.133)
AMBER = (0.910, 0.639, 0.239)
IVORY = (0.965, 0.953, 0.922)
MUTED = (0.62, 0.68, 0.75)

ED = [
    dict(
        src=os.path.join(HERE, "Surviving_the_Future.pdf"),
        out=os.path.join(PUB, "Surviving_the_Future_EN_sample.pdf"),
        pages=[*range(1, 33)],        # 1-based, inklusif; halaman gambar dicari otomatis
        lang="en",
        title="SURVIVING THE FUTURE",
        sub="Crisis, Climate, and Human Resilience",
        total=None,   # diisi dari jumlah halaman PDF asli
        sample_note="This is a free sample of the complete edition.",
        end_head="END OF THE FREE SAMPLE",
        read_line="You have just read {n} of the {total} pages in this edition.",
        inside_head="WHAT THE COMPLETE EDITION CONTAINS",
        inside=[
            ("24 chapters", "from the physics of warming to action plans for a single street"),
            ("25 data tables and 11 figures", "every number traceable to a named source"),
            ("24 case studies", "Bhola, Amphan, Chicago 1995, the Ahr valley, Cape Town, Chennai"),
            ("Worklists and worksheets", "an emergency checklist and a local risk profile you can fill in"),
            ("Glossary, analytical caveats, index", "and 172 sources, with notes on every event figure"),
        ],
        cta_head="GET THE COMPLETE EDITION",
        cta_body="The full PDF, EPUB and print editions are available from the publisher.",
        cta_url="[ isi alamat toko Anda di sini ]",
        foot_tpl="FREE SAMPLE  \u00b7  Surviving the Future  \u00b7  full edition: {total} pages",
        legal="This sample may be shared freely. The complete edition is licensed to the "
              "individual who bought it and may not be redistributed.",
    ),
    dict(
        src=os.path.join(HERE, "Surviving_the_Future_ID.pdf"),
        out=os.path.join(PUB, "Bertahan_Hidup_di_Masa_Depan_ID_sample.pdf"),
        pages=[*range(1, 35)],
        lang="id",
        title="BERTAHAN HIDUP DI MASA DEPAN",
        sub="Krisis, Iklim, dan Ketahanan Manusia",
        total=None,   # diisi dari jumlah halaman PDF asli
        sample_note="Ini adalah sampel gratis dari edisi lengkap.",
        end_head="AKHIR SAMPEL GRATIS",
        read_line="Anda baru membaca {n} dari {total} halaman edisi ini.",
        inside_head="ISI EDISI LENGKAP",
        inside=[
            ("24 bab", "dari fisika pemanasan sampai rencana aksi untuk satu jalan"),
            ("25 tabel data dan 11 gambar", "setiap angka dapat ditelusuri ke sumbernya"),
            ("24 studi kasus", "Bhola, Amphan, Chicago 1995, Lembah Ahr, Cape Town, Chennai"),
            ("Ceklis dan lembar kerja", "daftar periksa darurat dan profil risiko lokal yang bisa Anda isi"),
            ("Glosarium, catatan analitis, indeks", "dan 172 sumber, dengan catatan untuk setiap angka peristiwa"),
        ],
        cta_head="DAPATKAN EDISI LENGKAP",
        cta_body="PDF lengkap, EPUB, dan edisi cetak tersedia dari penerbit.",
        cta_url="[ isi alamat toko Anda di sini ]",
        foot_tpl="SAMPEL GRATIS  \u00b7  Bertahan Hidup di Masa Depan  \u00b7  edisi lengkap: {total} halaman",
        legal="Sampel ini boleh dibagikan. Edisi lengkap dilisensikan kepada pembeli "
              "dan tidak boleh disebarluaskan.",
    ),
]


def closing_page(doc, cfg, page_w, page_h):
    """Halaman penutup sampel: apa yang dibaca, apa yang belum, dan cara membeli."""
    page = doc.new_page(width=page_w, height=page_h)
    page.draw_rect(pymupdf.Rect(0, 0, page_w, page_h), color=None, fill=NAVY)

    serif_b = os.path.join(FONTS, "SourceSerif4-Semibold.otf")
    serif_r = os.path.join(FONTS, "SourceSerif4-Regular.otf")
    serif_i = os.path.join(FONTS, "SourceSerif4-It.otf")
    sans_b = os.path.join(FONTS, "SourceSans3-Semibold.otf")
    sans_r = os.path.join(FONTS, "SourceSans3-Regular.otf")

    m = 62.0
    w = page_w - 2 * m
    y = 96.0

    page.insert_font(fontname="sb", fontfile=serif_b)
    page.insert_font(fontname="sr", fontfile=serif_r)
    page.insert_font(fontname="si", fontfile=serif_i)
    page.insert_font(fontname="nb", fontfile=sans_b)
    page.insert_font(fontname="nr", fontfile=sans_r)

    # kepala amber
    page.insert_text((m, y), cfg["end_head"], fontname="nb", fontsize=11.5,
                     color=AMBER, render_mode=0)
    y += 13
    page.draw_line(pymupdf.Point(m, y), pymupdf.Point(m + 54, y), color=AMBER, width=2.2)
    y += 40

    # judul buku
    page.insert_text((m, y), cfg["title"], fontname="sb", fontsize=27, color=IVORY)
    y += 26
    page.insert_text((m, y), cfg["sub"], fontname="si", fontsize=14, color=AMBER)
    y += 34

    # kalimat "berapa yang sudah dibaca"
    page.insert_text((m, y), cfg["read_line"].format(n=len(cfg["pages"]), total=cfg["total"]),
                     fontname="si", fontsize=13.5, color=IVORY)
    y += 40

    # daftar isi edisi lengkap
    page.insert_text((m, y), cfg["inside_head"], fontname="nb", fontsize=10.5, color=AMBER)
    y += 24
    for lead, body in cfg["inside"]:
        page.insert_text((m, y), lead, fontname="sb", fontsize=11.5, color=IVORY)
        y += 15
        page.insert_text((m + 14, y), body, fontname="nr", fontsize=10.5, color=MUTED)
        y += 24

    # kotak ajakan
    y += 10
    box_h = 96
    page.draw_rect(pymupdf.Rect(m, y, m + w, y + box_h),
                   color=AMBER, fill=(0.075, 0.125, 0.19), width=1.6)
    page.insert_text((m + 22, y + 30), cfg["cta_head"], fontname="nb",
                     fontsize=12, color=AMBER)
    page.insert_text((m + 22, y + 50), cfg["cta_body"], fontname="nr",
                     fontsize=10.5, color=IVORY)
    page.insert_text((m + 22, y + 72), cfg["cta_url"], fontname="nb",
                     fontsize=11, color=AMBER)

    # catatan lisensi di kaki
    page.insert_textbox(pymupdf.Rect(m, page_h - 92, m + w, page_h - 52),
                        cfg["legal"], fontname="nr", fontsize=8.5, color=MUTED,
                        align=pymupdf.TEXT_ALIGN_LEFT)
    return page


def sample_footer(page, cfg, page_w):
    """Catatan kaki kecil di setiap halaman sampel."""
    text = cfg["foot_tpl"].format(total=cfg["total"])
    page.insert_text((page_w / 2 - 150, page.rect.height - 22), text,
                     fontname="helv", fontsize=6.6, color=(0.55, 0.58, 0.63))


def figure_pages(src, start):
    """Dua halaman bergambar pertama sesudah halaman `start` -- bukti bahwa
    klaim "data" di dalam buku benar-benar berisi gambar, bukan hanya teks."""
    for i in range(start, min(start + 80, src.page_count)):
        if src[i].get_images(full=True):
            return [i + 1, i + 2] if i + 2 <= src.page_count else [i + 1]
    return []


def build(cfg):
    src = pymupdf.open(cfg["src"])
    cfg["total"] = src.page_count          # jumlah halaman edisi lengkap, bukan angka tetap
    cfg["pages"] = cfg["pages"] + figure_pages(src, len(cfg["pages"]) + 1)
    out = pymupdf.open()
    pw, ph = src[0].rect.width, src[0].rect.height

    for pno in cfg["pages"]:
        out.insert_pdf(src, from_page=pno - 1, to_page=pno - 1)

    for page in out:
        sample_footer(page, cfg, pw)

    closing_page(out, cfg, pw, ph)

    out.set_metadata({
        "title": f"{cfg['title']} \u2014 free sample",
        "author": "Setyo Wisodo",
        "subject": cfg["sample_note"],
        "keywords": "sample, preview, climate, resilience",
        "creator": "Setyo Wisodo",
        "producer": "fpdf2",
    })
    out.set_toc([])                     # sampel tanpa bookmark penuh
    out.save(cfg["out"], garbage=3, deflate=True)
    out.close()
    src.close()
    n = len(cfg["pages"]) + 1
    print("  -> %s  (%d halaman)" % (os.path.relpath(cfg["out"], HERE), n))


if __name__ == "__main__":
    print("membuat sampel:")
    for c in ED:
        build(c)
