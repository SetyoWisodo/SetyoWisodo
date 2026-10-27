# -*- coding: utf-8 -*-
"""Foto marketplace final: enam sudut per edisi, 3000 px, putih + transparan.

Bedanya dengan make_3d.py (yang menyiapkan tampilan cepat untuk halaman
penjualan): di sini resolusinya 3000 px supaya tajam saat pembeli memperbesar,
latar putih bersih untuk Amazon/Etsy, dan versi transparan untuk banner.

Sudut dipilih menurut pekerjaannya di halaman marketplace:
  hero    depan + punggung + tepi atas -- foto utama, paling meyakinkan
  front   nyaris lurus -- untuk thumbnail kecil, distorsi paling sedikit
  angle   3/4 tajam -- memperlihatkan ketebalan buku
  fore    memperlihatkan tepi kertas -- membuktikan 451 halaman
  back    sampul belakang -- dipakai di gambar kedua atau ketiga
  spine   punggung terbaca -- untuk daftar rak dan katalog

Jalankan: python make_marketplace.py
Keluaran: book/publish/marketplace/
"""
import json
import os

from PIL import Image, ImageDraw, ImageFilter

import make_3d as m3

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "book/publish")
OUT = os.path.join(PUB, "marketplace")

PX = 3000                 # sisi gambar final
SS = 1.7                  # internal 5100 px, cukup untuk tepi tajam
WHITE = (255, 255, 255)
QUALITY = 92              # JPG

SHOTS = [
    ("hero", dict(yaw_deg=22, pitch_deg=11)),
    ("front", dict(yaw_deg=0, pitch_deg=7)),
    ("angle", dict(yaw_deg=38, pitch_deg=16)),
    ("fore", dict(yaw_deg=-28, pitch_deg=10)),
    ("back", dict(yaw_deg=205, pitch_deg=9)),
    # punggung ada di sisi yaw positif; 52 derajat membuat teksnya membelok
    # sampai bisa dibaca tanpa menutupi seluruh sampul depan
    ("spine", dict(yaw_deg=52, pitch_deg=9)),
]


def save(img, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    if name.endswith(".jpg"):
        bg = Image.new("RGB", img.size, WHITE)
        if img.mode == "RGBA":
            bg.paste(img, (0, 0), img)
            img = bg
        img.save(path, quality=QUALITY, optimize=True, subsampling=0)
    else:
        img.save(path)
    print("  %-46s %5dx%-5d %4d KB"
          % (name, img.width, img.height, os.path.getsize(path) // 1024))


def lineup(clears, canvas=(3600, 2400), gap_frac=0.06):
    """Kedua edisi berdampingan, tinggi sama, dengan bayangan kontak lembut."""
    W, H = canvas
    board = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    ims = [im.crop(im.split()[-1].getbbox()) for im in clears]
    target_h = int(H * 0.80)
    ims = [im.resize((int(im.width * target_h / im.height), target_h), Image.LANCZOS)
           for im in ims]

    gap = int(W * gap_frac)
    total = sum(i.width for i in ims) + gap * (len(ims) - 1)
    x = (W - total) // 2
    base = (H + target_h) // 2 - int(H * 0.03)

    for im in ims:
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).ellipse(
            [x + im.width * 0.04, base - int(H * 0.028),
             x + im.width * 0.96, base + int(H * 0.030)], fill=120)
        sh = sh.filter(ImageFilter.GaussianBlur(int(H * 0.020)))
        dark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dark.paste(Image.new("RGBA", (W, H), (18, 26, 38, 255)), (0, 0), sh)
        board = Image.alpha_composite(board, dark)
        board.alpha_composite(im, (x, base - im.height))
        x += im.width + gap
    return board


def main():
    m3.SS = SS
    rep = json.load(open(os.path.join(PUB, "build_report.json")))
    print("foto marketplace (%d px):" % PX)

    clears = {}
    for key, cfg in m3.BOOKS.items():
        r = rep[key]
        slug = cfg["slug"]
        for name, kw in SHOTS:
            img = m3.render(cfg, r, canvas=PX, **kw)
            save(img, f"{slug}_mkt_{name}.jpg")

        hero_clear = m3.render(cfg, r, canvas=PX, bg=(255, 255, 255, 0),
                               **dict(SHOTS[0][1]))
        save(hero_clear, f"{slug}_mkt_hero.png")
        clears[key] = hero_clear

    board = lineup([clears["en"], clears["id"]])
    save(board, "pair_mkt_lineup.png")
    save(board, "pair_mkt_lineup.jpg")


if __name__ == "__main__":
    main()
