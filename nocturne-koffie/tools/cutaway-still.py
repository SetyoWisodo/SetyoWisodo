#!/usr/bin/env python3
"""Lembar still potong-buka — gambar SKEMA, bukan tangkapan layar peramban.

Sama seperti tools/pratinjau.py: Chromium tidak ada di sandbox ini, jadi tidak
ada satu pun piksel halaman yang bisa diambil. Yang bisa: menyusun ulang
geometri yang SAMA dengan `cutaway/data.js` (posisi, jarak buka, sudut kamera)
secara ortografis-perspektif dengan PIL, lalu menaruhnya berdampingan.

Gunanya tepat seperti putaran still pada metode Cutaway: sebelum percaya pada
filmnya, periksa siluet, urutan buka, dan apakah ada bidang yang saling
menembus. Gambar ini tidak membuktikan rupa halaman — huruf, bayangan, dan
gradasi di peramban bisa berbeda.

Keluaran: cutaway/still/lembar-still.png (3 frame) + satu PNG per frame.

    python3 tools/cutaway-still.py
"""
from __future__ import annotations

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "cutaway", "data.js")
KELUAR = os.path.join(ROOT, "cutaway", "still")

PAPER = (237, 235, 230)
SHEET = (244, 242, 237)
INK = (20, 20, 20)
MUTED = (109, 106, 99)
ACCENT = (31, 63, 176)
BRAND = (245, 239, 228)
ORANGE = (225, 84, 43)
BJII = (74, 44, 26)

LEBAR, TINGGI = 720, 900          # satu frame
FOKUS = 1600.0                    # jarak kamera, piksel


def baca_data() -> dict:
    teks = open(DATA, encoding="utf-8").read()
    return json.loads(teks[teks.index("{"):teks.rindex("}") + 1])


def halus(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * x * (x * (x * 6 - 15) + 10)


def bukaan(t: float, bid: str, D: dict) -> float:
    hasil = 0.0
    for k in D["KETUKAN"]:
        ikut = k["bagian"] == bid or bid in k.get("bukaLagi", [])
        if not ikut:
            continue
        a, b, c, d = k["mulai"] + 0.12, k["mulai"] + 1.12, k["selesai"] - 0.55, k["selesai"]
        p = 0.0
        if a < t < d:
            p = halus((t - a) / 1.0) if t < b else (1.0 if t < c else 1 - halus((t - c) / 0.55))
        hasil = max(hasil, p)
    return hasil


def kamera(t: float, D: dict) -> dict:
    i = 0
    for j, k in enumerate(D["KETUKAN"]):
        if t >= k["mulai"]:
            i = j
    k = D["KAMERA"][D["KETUKAN"][i]["id"]]
    s = D["KAMERA"][D["KETUKAN"][max(0, i - 1)]["id"]]
    p = 1.0 if i == 0 else halus((t - D["KETUKAN"][i]["mulai"]) / 0.9)
    return {
        "ry": s["ry"] + (k["ry"] - s["ry"]) * p + math.sin(t * 0.44) * 1.5,
        "rx": s["rx"] + (k["rx"] - s["rx"]) * p + math.sin(t * 0.31 + 1.1) * 0.9,
        "zoom": s["zoom"] + (k["zoom"] - s["zoom"]) * p + math.sin(t * 0.6) * 0.004,
        "ty": s["ty"] + (k["ty"] - s["ty"]) * p,
    }


def putar(v, ry, rx, rz=0.0):
    x, y, z = v
    a = math.radians(ry)
    x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
    a = math.radians(rx)
    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
    if rz:
        a = math.radians(rz)
        x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
    return (x, y, z)


def proyeksi(v, kam, skala):
    """Kamera di +z, sama seperti `perspective` di CSS: z besar = lebih dekat."""
    x, y, z = putar(v, kam["ry"], kam["rx"])
    jarak = max(FOKUS / skala - z, 1.0)
    f = FOKUS / jarak
    return (LEBAR / 2 + x * f, TINGGI / 2 + y * f + kam["ty"] * 0.1 * skala, -jarak)


def warna(bid: str) -> tuple:
    return {"label": BRAND, "kertas": SHEET, "sisi": PAPER, "segel": (60, 60, 60),
            "katup": MUTED, "biji": BJII, "stiker": INK}[bid]


def sudut_bagian(b: dict, p: float, cermin: bool) -> list:
    m = -1 if cermin else 1
    n = math.sqrt(sum(a * a for a in b["arah"])) or 1
    dx = (b["pos"][0] + b["arah"][0] / n * b["jarak"] * p) * m
    dy = b["pos"][1] + b["arah"][1] / n * b["jarak"] * p
    dz = b["pos"][2] + b["arah"][2] / n * b["jarak"] * p
    ry = (b["muka_ry"] + b["putar"] * p) * m
    rx = b["muka_rx"] * (1 - 0.6 * p)
    hw, hh = b["w"] / 2, b["h"] / 2
    keluar = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        v = putar((sx * hw, sy * hh, 0.0), ry, rx)
        keluar.append((v[0] + dx, v[1] + dy, v[2] + dz))
    return keluar


def frame(D: dict, t: float, judul: str) -> Image.Image:
    kam = kamera(t, D)
    skala = min(TINGGI * 0.60 / (100 / D["UKUR"]["rasio"]), LEBAR * 0.44 / 100) * kam["zoom"]
    im = Image.new("RGB", (LEBAR, TINGGI), PAPER)
    d = ImageDraw.Draw(im, "RGBA")
    try:
        f_judul = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-600-normal.ttf"), 20)
        f_kecil = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-400-normal.ttf"), 15)
    except OSError:
        f_judul = f_kecil = ImageFont.load_default()

    # kisi lantai: membantu menilai kemiringan kamera
    for i in range(-6, 7):
        a = proyeksi((i * 40, 90, 0), kam, skala)
        b = proyeksi((i * 40, 90, -260), kam, skala)
        d.line([a[:2], b[:2]], fill=(20, 20, 20, 16), width=1)

    bidang = []
    for b in D["BAGIAN"]:
        p = bukaan(t, b["id"], D)
        for cermin in ([False, True] if b.get("kembar") else [False]):
            pts = [proyeksi(v, kam, skala) for v in sudut_bagian(b, p, cermin)]
            z = sum(q[2] for q in pts) / 4   # = -jarak kamera
            bidang.append((z, b, pts, p))
    bidang.sort(key=lambda x: x[0])        # z kecil = jauh, digambar dulu

    for z, b, pts, p in bidang:
        xy = [(q[0], q[1]) for q in pts]
        dasar = warna(b["wajah"])
        sorot = bool(p > 0.5)
        if b["id"] != "biji":                 # isi tidak punya bidang: hanya bijinya
            d.polygon(xy, fill=dasar)
        if b["id"] != "biji":
            d.line(xy + [xy[0]], fill=ACCENT if sorot else (20, 20, 20, 170),
                   width=3 if sorot else 1)
        if b["id"] == "biji":
            for k in range(7):
                bx = 0.26 + (k % 3) * 0.23
                by = 0.16 + (k // 3) * 0.33
                px = xy[0][0] + (xy[1][0] - xy[0][0]) * bx + (xy[3][0] - xy[0][0]) * by
                py = xy[0][1] + (xy[1][1] - xy[0][1]) * bx + (xy[3][1] - xy[0][1]) * by
                r = 0.05 * math.hypot(xy[1][0] - xy[0][0], xy[1][1] - xy[0][1]) + 3
                d.ellipse([px - r * 0.6, py - r, px + r * 0.6, py + r], fill=(92, 58, 34))
        if b["id"] == "label" or b["wajah"] == "label":
            d.line([xy[0], xy[1]], fill=ORANGE, width=4)
        if b["id"] == "katup":
            d.ellipse([min(x for x, _ in xy), min(y for _, y in xy),
                       max(x for x, _ in xy), max(y for _, y in xy)],
                      outline=(250, 250, 250), width=2)

    d.text((28, 26), judul, font=f_judul, fill=INK)
    d.text((28, 54), f'{t:.2f} s · kamera ry {kam["ry"]:.0f}° rx {kam["rx"]:.0f}° zoom {kam["zoom"]:.2f}',
           font=f_kecil, fill=MUTED)
    d.text((28, TINGGI - 34), "skema geometri dari cutaway/data.js — bukan tangkapan layar peramban",
           font=f_kecil, fill=MUTED)
    return im


def main() -> None:
    os.makedirs(KELUAR, exist_ok=True)
    D = baca_data()
    pilihan = [(0.0, "Sampul · frame 0"), (3.6, "Badan terbuka"), (18.6, "Isi sangrai")]
    lembar = Image.new("RGB", (LEBAR * len(pilihan), TINGGI), PAPER)
    for i, (t, judul) in enumerate(pilihan):
        im = frame(D, t, judul)
        im.save(os.path.join(KELUAR, f"{i:02d}-{int(t*10):03d}.png"))
        lembar.paste(im, (LEBAR * i, 0))
    keluar = os.path.join(KELUAR, "lembar-still.png")
    lembar.save(keluar, optimize=True)
    print(f"  cutaway/still/lembar-still.png · {os.path.getsize(keluar)/1024:.0f} KB · "
          f"{LEBAR*len(pilihan)}×{TINGGI} · {len(pilihan)} frame")


if __name__ == "__main__":
    main()
