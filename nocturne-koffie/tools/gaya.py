#!/usr/bin/env python3
"""Empat perlakuan gaya untuk render biji — semuanya deterministik (Pillow/NumPy).

Dipakai untuk memilih arah visual tanpa menebak: satu render yang sama
(`assets/img/biji-render-02.png`) diolah menjadi empat gaya, lalu disusun jadi
satu lembar perbandingan `laporan/gaya-biji.png`.

    python3 tools/gaya.py            # tulis laporan/gaya-biji.png
    python3 tools/gaya.py --pasang A # pasang gaya terpilih ke beranda
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMBER = os.path.join(ROOT, "assets", "img", "biji-render-02.png")
KELUAR = os.path.join(ROOT, "laporan", "gaya-biji.png")
POSTER = os.path.join(ROOT, "assets", "img", "biji-3d-poster.webp")
DATA = os.path.join(ROOT, "data", "biji3d.json")
FONT = os.path.join(ROOT, "assets", "fonts", "inter-latin-600-normal.ttf")
FONTD = os.path.join(ROOT, "assets", "fonts", "bricolage-grotesque-latin-800-normal.ttf")

PAPER = np.array([245, 239, 228], dtype="float32")
INK = np.array([22, 17, 13], dtype="float32")
ORANGE = np.array([225, 84, 43], dtype="float32")
ESPRESSO = np.array([74, 44, 26], dtype="float32")
GOLD = np.array([217, 164, 65], dtype="float32")
W, H = 640, 800


def bayangan_bulat(alfa: np.ndarray) -> np.ndarray:
    """Bayangan elips lembut di bawah biji (0–1)."""
    h, w = alfa.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w * 0.50, h * 0.776
    rx, ry = w * 0.150, h * 0.022
    d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
    elips = np.clip(1.0 - d, 0, 1) ** 0.7
    return np.asarray(
        Image.fromarray((elips * 255).astype("uint8"), "L").filter(ImageFilter.GaussianBlur(6))
    ).astype("float32")[:, :, None] / 255.0


def muat() -> tuple[np.ndarray, np.ndarray]:
    """Kembalikan (rgb 0–255, alfa biji 0–1)."""
    im = Image.open(SUMBER).convert("RGB")
    im = im.crop((0, 0, im.width, int(im.width * H / W))) if im.width / im.height < W / H else im
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype("float32")
    luma = a[:, :, 0] * 0.299 + a[:, :, 1] * 0.587 + a[:, :, 2] * 0.114
    alfa = np.clip((205.0 - luma) / 42.0, 0.0, 1.0)
    alfa = np.asarray(
        Image.fromarray((alfa * 255).astype("uint8"), "L").filter(ImageFilter.GaussianBlur(1.4))
    ).astype("float32") / 255.0
    # isi lubang kecil (pori terang di dalam biji)
    alfa = np.maximum(alfa, np.asarray(
        Image.fromarray(((alfa > 0.35) * 255).astype("uint8"), "L")
        .filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    ).astype("float32") / 255.0)
    alfa[:, :, None]
    alfa3 = alfa[:, :, None]
    # bayangan asli (luma 180–235) ikut terekam: buang dengan ambang tegas,
    # lalu erosi 1 px supaya sisa kabut di tepi tidak ikut jadi "biji"
    alfa3 = np.clip((alfa3 - 0.66) / 0.24, 0, 1)
    alfa3 = np.asarray(
        Image.fromarray((alfa3[:, :, 0] * 255).astype("uint8"), "L")
        .filter(ImageFilter.MinFilter(3))
    ).astype("float32")[:, :, None] / 255.0
    return a, alfa3


def grain( bentuk: tuple[int, int], kuat: float = 9.0, benih: int = 7) -> np.ndarray:
    rng = np.random.default_rng(benih)
    n = rng.normal(0, kuat, bentuk[:2])[:, :, None]
    return n


def relight(a: np.ndarray, alfa: np.ndarray, latar: np.ndarray,
            bayangan: float = 0.5) -> np.ndarray:
    """Taruh biji di atas latar baru, dengan cahaya tepi hangat."""
    h, w = alfa.shape[:2]
    yy = np.linspace(0, 1, h)[:, None, None]
    dasar = latar * (1 - yy * 0.25)

    # cahaya tepi: gradien horizontal & vertikal, hanya mengenai biji
    kx = np.linspace(-1, 1, w)[None, :, None]
    ky = np.linspace(-1, 1, h)[:, None, None]
    tepi = np.clip(1.0 - np.abs(kx * 1.15), 0, 1) ** 2.2
    tepi = tepi * np.clip(1.0 - np.abs(ky + 0.1) * 1.1, 0, 1) ** 0.6
    sinar = (ORANGE * 0.55 + GOLD * 0.45) * tepi * 0.85

    isi = a * 1.06 + 6.0
    dasar = dasar * (1 - bayangan * bayangan_bulat(alfa))
    keluar = isi * alfa + dasar * (1 - alfa) + sinar * alfa
    return np.clip(keluar, 0, 255)


def s_kurva(a: np.ndarray, kontras: float = 1.16, tengah: float = 118.0) -> np.ndarray:
    return np.clip((a - tengah) * kontras + tengah, 0, 255)


# ── gaya ────────────────────────────────────────────────────────────────────
def gaya_a_film(a, alfa):
    """Film gelap: latar near-black, biji disorot hangat, grain halus."""
    latar = np.zeros_like(a) + np.array([16, 12, 10], dtype="float32")
    x = np.linspace(0, 1, a.shape[1])[None, :, None]
    y = np.linspace(0, 1, a.shape[0])[:, None, None]
    pendar = np.clip(1 - ((x - 0.80) ** 2 / 0.16 + (y - 0.16) ** 2 / 0.34), 0, 1) ** 1.6
    latar = latar + (ORANGE * 0.30 + GOLD * 0.10) * pendar
    hasil = relight(a, alfa, latar, bayangan=0.0)   # di latar hitam, bayangan tak terlihat
    hasil = s_kurva(hasil, 1.2, 96)
    hasil = hasil + grain(a.shape, 7.5)
    return np.clip(hasil, 0, 255)


def gaya_b_polos(a, alfa):
    """Warna polos: render apa adanya di latar kertas, bayangan elips lembut.

    Inilah yang dipakai sekarang, tapi dengan bayangan studio yang lebih rapi.
    """
    latar = np.zeros_like(a) + PAPER
    latar = latar * (1 - 0.30 * bayangan_bulat(alfa))
    return np.clip(a * alfa + latar * (1 - alfa), 0, 255)


def gaya_c_mono(a, alfa):
    """Monokrom kertas: hitam-putih kontras tinggi, latar kertas brief."""
    luma = np.asarray(Image.fromarray(a.astype("uint8"), "RGB").convert("L")).astype("float32")
    luma = np.clip((luma - 30) * 1.28, 0, 255)
    isi = np.dstack([luma] * 3)
    latar = np.zeros_like(a) + PAPER
    latar = latar * (1 - 0.28 * bayangan_bulat(alfa))
    return np.clip(isi * alfa + latar * (1 - alfa), 0, 255)


def gaya_d_arsir(a, alfa):
    """Arsir cetak: dua warna (espresso + orange), garis arsir diagonal, latar kertas."""
    luma = np.asarray(Image.fromarray(a.astype("uint8"), "RGB").convert("L")).astype("float32") / 255.0
    h, w = luma.shape
    yy, xx = np.mgrid[0:h, 0:w]
    # garis diagonal miring 45° untuk bayangan sedang, silang untuk yang paling gelap
    satu = ((xx + yy) % 8) < 2
    dua = ((xx - yy) % 8) < 2
    gelap = luma < 0.34
    sedang = (luma >= 0.34) & (luma < 0.56)
    terang = (luma >= 0.56) & (luma < 0.78)

    isi = np.zeros_like(a)
    isi[:] = PAPER
    isi[terang] = ORANGE * 0.55 + PAPER * 0.45
    isi[sedang] = ORANGE
    isi[gelap] = ESPRESSO
    isi[terang & satu] = ORANGE * 0.85 + ESPRESSO * 0.15
    isi[sedang & satu] = ESPRESSO
    isi[gelap & dua] = INK

    hasil = np.where(alfa > 0.45, isi, PAPER)
    bayang = bayangan_bulat(alfa) * (1 - (alfa > 0.45))
    hasil = hasil * (1 - 0.20 * bayang) + ESPRESSO * 0.20 * bayang
    return np.clip(hasil, 0, 255)


def semua_gaya(a, alfa) -> dict:
    return {
        "A": ("Film gelap · grain", gaya_a_film(a, alfa)),
        "B": ("Warna polos di kertas", gaya_b_polos(a, alfa)),
        "C": ("Monokrom kertas", gaya_c_mono(a, alfa)),
        "D": ("Arsir cetak · 2 warna", gaya_d_arsir(a, alfa)),
    }


def lembar(hasil: dict) -> Image.Image:
    """Susun 2×2 dengan label, untuk satu gambar perbandingan."""
    sel_w, sel_h = 320, 400
    pad, kepala = 26, 96
    lebar = pad * 2 + sel_w * 2 + 18
    tinggi = kepala + pad + (sel_h + 46) * 2
    sheet = Image.new("RGB", (lebar, tinggi), tuple(int(v) for v in PAPER))
    d = ImageDraw.Draw(sheet)

    d.text((pad, 26), "SATU RENDER · EMPAT GAYA", font=ImageFont.truetype(FONTD, 26),
           fill=tuple(int(v) for v in INK))
    d.text((pad, 62), "pilih satu, saya pasang ke beranda", font=ImageFont.truetype(FONT, 13),
           fill=(120, 110, 100))

    urut = list(hasil.items())
    for i, (kunci, (nama, arr)) in enumerate(urut):
        baris, kolom = divmod(i, 2)
        x = pad + kolom * (sel_w + 18)
        y = kepala + pad + baris * (sel_h + 46)
        im = Image.fromarray(arr.astype("uint8"), "RGB").resize((sel_w, sel_h), Image.LANCZOS)
        sheet.paste(im, (x, y))
        d.rectangle((x, y, x + sel_w - 1, y + sel_h - 1), outline=(22, 17, 13), width=1)
        d.text((x, y + sel_h + 8), f"{kunci} · {nama}", font=ImageFont.truetype(FONT, 14),
               fill=tuple(int(v) for v in INK))
    return sheet


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasang", choices=["A", "B", "C", "D"], help="pasang gaya ke poster beranda")
    a = ap.parse_args()

    rgb, alfa = muat()
    hasil = semua_gaya(rgb, alfa)

    if a.pasang:
        nama, arr = hasil[a.pasang]
        im = Image.fromarray(arr.astype("uint8"), "RGB")
        im.save(POSTER, "WEBP", quality=84, method=6)
        with open(os.path.join(ROOT, "laporan", "gaya-terpilih.json"), "w", encoding="utf-8") as f:
            json.dump({"gaya": a.pasang, "nama": nama}, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"gaya {a.pasang} ({nama}) dipasang → {os.path.relpath(POSTER, ROOT)} · "
              f"{os.path.getsize(POSTER)/1024:.0f} KB")
        return 0

    sheet = lembar(hasil)
    sheet.save(KELUAR, optimize=True)
    for k, (nama, _) in hasil.items():
        print(f"  {k} · {nama}")
    print(f"→ {os.path.relpath(KELUAR, ROOT)} · {os.path.getsize(KELUAR)/1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
