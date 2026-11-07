#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_sampul.py — pasang judul + nama penulis pada seni sampul, ekspor 3 ukuran.

    python3 novel_en/tools/build_sampul.py

Masukan : novel_en/pasar/sampul/seni_sampul.png   (seni tanpa teks)
Keluaran: sampul_wattpad_1024x1536.jpg
          sampul_kecil_512x800.jpg
          sampul_besar_1600x2400.jpg

Gaya huruf: serif tipis dengan jarak huruf lebar, warna gading hangat,
scrim gelap bergradasi di atas & bawah supaya teks terbaca tanpa menutup lukisan.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "pasar", "sampul")
SENI = os.path.join(DIR, "seni_sampul.png")
FONT = os.path.join(os.path.dirname(ROOT), "fonts", "Tinos-Regular.ttf")
FONT_IT = os.path.join(os.path.dirname(ROOT), "fonts", "Tinos-Italic.ttf")

JUDUL = ["BEFORE", "THE LIGHT", "ARRIVES"]
KICKER = "A  N O V E L"
PENULIS = "S E T Y O   W I S O D O"
TAGLINE = "Memory is currency. Love is the debt."
IVORY = (247, 243, 232)
AMBER = (226, 168, 92)
SHADOW = (8, 10, 14)


def scrim(im, atas=0.44, bawah=0.34):
    """Gradasi gelap: pekat di tepi atas/bawah, nol di tengah."""
    w, h = im.size
    lapis = Image.new("L", (1, h), 0)
    px = lapis.load()
    for y in range(h):
        t = y / max(1, h - 1)
        a = 0.0
        if t < atas:
            a = (1 - t / atas) ** 1.5
        elif t > 1 - bawah:
            a = ((t - (1 - bawah)) / bawah) ** 1.5
        px[0, y] = int(255 * a * 0.82)
    lapis = lapis.resize((w, h))
    gelap = Image.new("RGB", (w, h), SHADOW)
    return Image.composite(gelap, im, lapis)


def huruf(path, size):
    return ImageFont.truetype(path, size)


def jarak(d, teks, font, tracking):
    return sum(d.textlength(c, font=font) for c in teks) + tracking * (len(teks) - 1)


def tulis_jarak(d, teks, font, cx, y, isi, tracking, bayang=True):
    total = jarak(d, teks, font, tracking)
    x = cx - total / 2
    if bayang:
        dx = max(1, font.size // 26)
        for c in teks:
            d.text((x + dx, y + dx), c, font=font, fill=(0, 0, 0, 150))
            x += d.textlength(c, font=font) + tracking
        x = cx - total / 2
    for c in teks:
        d.text((x, y), c, font=font, fill=isi)
        x += d.textlength(c, font=font) + tracking
    return total


def buat(im_seni, W, H, keluar, judul_skala=1.0):
    im = im_seni.convert("RGB").resize((W, H), Image.LANCZOS)
    im = scrim(im)
    d = ImageDraw.Draw(im, "RGBA")

    s = W / 1024.0
    cx = W // 2

    # kicker
    f_kick = huruf(FONT, int(19 * s * judul_skala))
    tulis_jarak(d, "A   N O V E L", f_kick, cx, int(H * 0.055), AMBER, 2.0, bayang=False)

    # judul tiga baris
    f_judul = huruf(FONT, int(96 * s * judul_skala))
    y = int(H * 0.082)
    for baris in JUDUL:
        f = f_judul
        while jarak(d, baris, f, 8 * s) > W * 0.86 and f.size > 20:
            f = huruf(FONT, f.size - 1)
        tulis_jarak(d, baris, f, cx, y, IVORY, 8 * s)
        y += int(f.size * 1.18)



    # penulis di kaki
    f_pen = huruf(FONT, int(27 * s * judul_skala))
    tulis_jarak(d, "S E T Y O   W I S O D O", f_pen, cx, int(H * 0.898), IVORY, 3.0)

    # volume
    f_vol = huruf(FONT, int(15 * s * judul_skala))
    vol = "V O L U M E   I"
    vw = jarak(d, vol, f_vol, 2.0)
    d.text((cx - vw / 2, int(H * 0.940)), vol, font=f_vol, fill=AMBER + (230,))

    im.save(keluar, quality=92, subsampling=1, optimize=True)
    print("%-34s %dx%d  %d KB" % (os.path.basename(keluar), W, H, os.path.getsize(keluar) // 1024))


def main():
    if not os.path.exists(SENI):
        raise SystemExit("seni_sampul.png belum ada")
    seni = Image.open(SENI)
    buat(seni, 1024, 1536, os.path.join(DIR, "sampul_wattpad_1024x1536.jpg"))
    buat(seni, 512, 800, os.path.join(DIR, "sampul_kecil_512x800.jpg"), judul_skala=1.02)
    buat(seni, 1600, 2400, os.path.join(DIR, "sampul_besar_1600x2400.jpg"))


if __name__ == "__main__":
    main()
