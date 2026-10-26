# -*- coding: utf-8 -*-
"""Susun sampul depan dari seni mentah + tipografi (EN dan ID).

Seni mentah: book/cover/art_cover_v1.png (dibuat dengan prompt terkompilasi
dari skill Open Generative AI, lihat book/cover/SKILL_open_generative_ai.md).

Keluaran:
  book/publish/*_cover_front.jpg       2550 x 3608 px (rasio potong A4, 300 dpi)
                                       dipakai make_cover.py dan make_publish.py
  book/publish/*_cover_ebook.jpg       1600 x 2560 px (rasio 1:1,6 yang diminta
                                       toko ebook seperti KDP)

Jalankan: python make_cover_front.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "book/cover/art_cover_v1.png")
FONTS = os.path.join(HERE, "book/fonts")
PUB = os.path.join(HERE, "book/publish")
OUT_EN = os.path.join(PUB, "Surviving_the_Future_EN_cover_front.jpg")
OUT_ID = os.path.join(PUB, "Bertahan_Hidup_di_Masa_Depan_ID_cover_front.jpg")
EB_EN = os.path.join(PUB, "Surviving_the_Future_EN_cover_ebook.jpg")
EB_ID = os.path.join(PUB, "Bertahan_Hidup_di_Masa_Depan_ID_cover_ebook.jpg")

W, H = 2550, 3608                     # rasio potong A4 pada 300 dpi (8,5 x 12,03 in)
NAVY = (11, 22, 34)
NAVY_SOFT = (17, 31, 46)
IVORY = (246, 243, 235)
AMBER = (232, 163, 61)
MUTED = (176, 186, 199)

# tata letak dinyatakan sebagai pecahan, supaya rasio lain bisa memakai kode sama
F_KICKER = 0.050
F_TITLE = 0.089
F_IMAGE = 0.251
F_QUOTE = 0.848
F_AUTHOR = 0.928          # nama penulis di kaki sampul
F_YEAR = 0.966            # tahun di bawah nama
F_TITLE_WIDTH = 0.820


def tracked(draw, text, font, y, fill, tracking=0.0, center_x=None, width=None,
            max_w=None):
    """Tulis teks dengan jarak antarhuruf manual, rata tengah.

    `max_w` menjaga baris berjarak lebar tetap di dalam bidang potong: huruf
    diperkecil bertahap sampai muat, bukan dipotong.
    """
    if max_w:
        while max_w and font.size > 8:
            probe = sum(draw.textlength(ch, font=font) for ch in text) \
                    + tracking * (len(text) - 1)
            if probe <= max_w:
                break
            font = ImageFont.truetype(font.path, font.size - 1)
    cx = center_x if center_x is not None else width // 2
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking
    return total


def fit_to_width(draw, text, path, target_w, max_size, min_size=40):
    """Cari ukuran font terbesar yang muat pada lebar target."""
    size = max_size
    while size > min_size:
        f = ImageFont.truetype(path, size)
        if draw.textlength(text, font=f) <= target_w:
            return f
        size -= 2
    return ImageFont.truetype(path, min_size)


def build(cfg, out_path, w, h):
    s = w / 1800.0                     # skala semua ukuran huruf mengikuti lebar
    canvas = Image.new("RGB", (w, h), NAVY)

    # ---------- panel tipografi di atas ----------
    draw = ImageDraw.Draw(canvas)
    seam_h = int(h * 0.31)
    for y in range(seam_h):
        t = y / seam_h
        c = tuple(int(NAVY[i] + (NAVY_SOFT[i] - NAVY[i]) * (t ** 1.6)) for i in range(3))
        draw.line([(0, y), (w, y)], fill=c)

    # ---------- gambar di bawah, menyatu dengan panel ----------
    art = Image.open(ART).convert("RGB")
    img_top = int(h * F_IMAGE)
    box_h = h - img_top
    big = art.resize((w, int(art.height * w / art.width)), Image.LANCZOS)
    if big.height > box_h:                       # buang langit paling atas
        cut = int((big.height - box_h) * 0.40)
        big = big.crop((0, cut, w, cut + box_h))
    mask = Image.new("L", (w, box_h), 255)
    md = ImageDraw.Draw(mask)
    ramp = int(300 * s)
    for i in range(ramp):
        md.line([(0, i), (w, i)], fill=int(255 * (i / max(1, ramp - 1)) ** 1.5))
    canvas.paste(big, (0, img_top), mask)

    # ---------- pita bawah: cukup gelap agar kalimat penutup terbaca ----------
    band_h = int(h * 0.235)
    band = Image.new("L", (1, band_h))
    for i in range(band_h):
        t = i / (band_h - 1)
        band.putpixel((0, i), int(255 * min(1.0, (t ** 0.72) * 1.30)))
    band = band.resize((w, band_h), Image.BILINEAR)
    canvas.paste(Image.new("RGB", (w, band_h), NAVY), (0, h - band_h), band)

    draw = ImageDraw.Draw(canvas)

    # ---------- tipografi ----------
    def font(name, size):
        return ImageFont.truetype(os.path.join(FONTS, name), max(10, int(size * s)))

    black = os.path.join(FONTS, "SourceSans3-Black.otf")
    f_author = font("SourceSans3-Semibold.otf", 46)
    f_year = font("SourceSans3-Semibold.otf", 36)
    f_kick = font("SourceSans3-Semibold.otf", 42)
    f_sub = font("SourceSerif4-It.otf", 74)
    f_sub2 = font("SourceSerif4-It.otf", 46)

    tracked(draw, cfg["kicker"], f_kick, int(h * F_KICKER), AMBER, tracking=7 * s,
            width=w, max_w=int(w * 0.86))

    target = int(w * F_TITLE_WIDTH)
    max_size = int(276 * s)
    f1 = fit_to_width(draw, cfg["title1"], black, target, max_size)
    f2 = fit_to_width(draw, cfg["title2"], black, target, max_size)
    size = min(f1.size, f2.size)
    f1 = ImageFont.truetype(black, size)
    f2 = ImageFont.truetype(black, size)
    y_title = int(h * F_TITLE)
    tracked(draw, cfg["title1"], f1, y_title, IVORY, tracking=2 * s, width=w)
    tracked(draw, cfg["title2"], f2, y_title + int(size * 1.06), IVORY, tracking=2 * s, width=w)

    # aturan amber + subjudul
    rule_y = y_title + int(size * 1.06) + int(size * 1.12)
    half = int(90 * s)
    draw.line([(w // 2 - half, rule_y), (w // 2 + half, rule_y)], fill=AMBER, width=max(2, int(5 * s)))
    sub_w = draw.textlength(cfg["sub"], font=f_sub)
    draw.text(((w - sub_w) / 2, rule_y + int(40 * s)), cfg["sub"], font=f_sub, fill=AMBER)
    if cfg.get("sub2"):
        w2 = draw.textlength(cfg["sub2"], font=f_sub2)
        draw.text(((w - w2) / 2, rule_y + int(118 * s)), cfg["sub2"], font=f_sub2, fill=MUTED)

    # ---------- kalimat penutup di pita bawah ----------
    yq = int(h * F_QUOTE)
    for ln in cfg["quote"]:
        fq = fit_to_width(draw, ln, os.path.join(FONTS, "SourceSerif4-It.otf"),
                          int(w * 0.82), int(72 * s))
        wq = draw.textlength(ln, font=fq)
        # bayangan halus supaya tetap terbaca di atas gambar
        shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.text(((w - wq) / 2, yq), ln, font=fq, fill=(0, 0, 0, 205))
        shadow = shadow.filter(ImageFilter.GaussianBlur(int(11 * s)))
        canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB"), (0, 0))
        draw = ImageDraw.Draw(canvas)
        draw.text(((w - wq) / 2, yq), ln, font=fq, fill=IVORY)
        yq += int(fq.size * 1.26)

    # ---------- nama penulis dan tahun di kaki sampul ----------
    tracked(draw, cfg["author"], f_author, int(h * F_AUTHOR), IVORY, tracking=12 * s,
            width=w, max_w=int(w * 0.86))
    tracked(draw, cfg["year"], f_year, int(h * F_YEAR), AMBER, tracking=7 * s, width=w)

    canvas.save(out_path, quality=95, dpi=(300, 300), subsampling=0)
    print("  ->", os.path.relpath(out_path, HERE), canvas.size)


EN = dict(
    author="SETYO WISODO",
    year="2026",
    kicker="THE DEFINITIVE GUIDE TO THE CENTURY OF CRISES",
    title1="SURVIVING",
    title2="THE FUTURE",
    sub="Crisis, Climate, and Human Resilience",
    quote=["Survival is a decision, not a fate."],
)

ID = dict(
    author="SETYO WISODO",
    year="2026",
    kicker="PANDUAN LENGKAP MENUJU ABAD KRISIS",
    title1="BERTAHAN HIDUP",
    title2="DI MASA DEPAN",
    sub="Krisis, Iklim, dan Resiliensi Manusia",
    quote=["Bertahan hidup adalah keputusan, bukan takdir."],
)

if __name__ == "__main__":
    print("sampul depan:")
    build(EN, OUT_EN, W, H)
    build(ID, OUT_ID, W, H)
    print("sampul ebook (1:1,6):")
    build(EN, EB_EN, 1600, 2560)
    build(ID, EB_ID, 1600, 2560)
