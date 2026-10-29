#!/usr/bin/env python3
"""
D4 · Kreatif & Media — generator aset konten (tanpa kamera).

Menulis ke folder konten/:
  reel-*.mp4        video vertikal 9:16 (1080×1920, 24 fps) untuk Reels/TikTok
  reel-*.jpg        poster (cover) tiap video
  carousel-*.jpg    slide 4:5 (1080×1350) untuk carousel Instagram
  story-*.jpg       frame 9:16 statis untuk Instagram Story
  post-*.jpg        feed 1:1 (1080×1080)
  index.html        hub konten: pratinjau + caption + jadwal

Juga menulis data/kreatif.json (manifest) yang dibaca situs & papan harian.

Pakai:
    python3 tools/kreatif.py                # semua aset
    python3 tools/kreatif.py --cepat        # tanpa encode video (hanya gambar)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import shutil
import subprocess
import tempfile
from datetime import date

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "konten")
FONTS = os.path.join(os.path.dirname(ROOT), "book", "fonts")
PRODUK = os.path.join(ROOT, "assets", "img", "produk")

SANS_BLACK = os.path.join(FONTS, "SourceSans3-Black.otf")
SANS_BOLD = os.path.join(FONTS, "SourceSans3-Bold.otf")
SANS_SEMI = os.path.join(FONTS, "SourceSans3-Semibold.otf")
SANS = os.path.join(FONTS, "SourceSans3-Regular.otf")
SERIF_IT = os.path.join(FONTS, "SourceSerif4-It.otf")
SERIF = os.path.join(FONTS, "SourceSerif4-Regular.otf")

PAPER = (245, 239, 228)
PAPER2 = (239, 230, 214)
INK = (22, 17, 13)
ESPRESSO = (74, 44, 26)
ORANGE = (225, 84, 43)
GOLD = (217, 164, 65)

F = lambda p, s: ImageFont.truetype(p, int(s))
FPS = 24

KATALOG = json.load(open(os.path.join(ROOT, "data", "catalog.json"), encoding="utf-8"))


def rp(n):
    return "Rp" + f"{int(n):,}".replace(",", ".")


def harga(id_produk, gram=100):
    for p in KATALOG["products"]:
        if p["id"] == id_produk:
            for v in p["variants"]:
                if v["grams"] == gram:
                    return v["price"]
    for b in KATALOG["bundles"]:
        if b["id"] == id_produk:
            return b["price"]
    return None


# ────────────────────────────── utilitas gambar ────────────────────────────
def kertas(w, h, base=PAPER, seed=1):
    img = Image.new("RGB", (w, h), base)
    random.seed(seed)
    n = Image.new("L", (max(1, w // 4), max(1, h // 4)))
    px = n.load()
    for y in range(n.height):
        for x in range(n.width):
            px[x, y] = random.randint(120, 136)
    n = n.resize((w, h), Image.BILINEAR).convert("RGB")
    return Image.blend(img, n, 0.03)


def ease_out(p):
    return 1 - (1 - max(0.0, min(1.0, p))) ** 3


def seg(t, a, b):
    """progress 0..1 di dalam rentang waktu a..b"""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return max(0.0, min(1.0, (t - a) / (b - a)))


def teks_bungkus(draw, text, font, max_w):
    kata, baris, cur = text.split(), [], ""
    for k in kata:
        coba = (cur + " " + k).strip()
        if draw.textlength(coba, font=font) <= max_w:
            cur = coba
        else:
            if cur:
                baris.append(cur)
            cur = k
    if cur:
        baris.append(cur)
    return baris


def tempel_lembut(base, layer, xy):
    base.alpha_composite(layer, (int(xy[0]), int(xy[1])))


def panel(gambar, warna, radius=0):
    lay = Image.new("RGBA", gambar.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, gambar.size[0] - 1, gambar.size[1] - 1], radius=radius, fill=warna)
    return lay


def _trim(im, toleransi=18):
    """Buang margin polos (putih/krem) di tepi gambar produk."""
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    def tepi_polos(vals):
        return max(vals) - min(vals) < 6 and sum(vals) / len(vals) > 235

    def kolom(x):
        return tepi_polos([px[x, y] for y in range(0, h, max(1, h // 120))])

    def baris(y):
        return tepi_polos([px[x, y] for x in range(0, w, max(1, w // 120))])

    x0 = 0
    while x0 < w - 2 and kolom(x0):
        x0 += 1
    x1 = w - 1
    while x1 > x0 + 2 and kolom(x1):
        x1 -= 1
    y0 = 0
    while y0 < h - 2 and baris(y0):
        y0 += 1
    y1 = h - 1
    while y1 > y0 + 2 and baris(y1):
        y1 -= 1
    if x1 - x0 < w * 0.35 or y1 - y0 < h * 0.35:
        return im
    return im.crop((x0, y0, x1 + 1, y1 + 1))


def foto_produk(nama, target_w, trim=True):
    p = os.path.join(PRODUK, nama)
    im = Image.open(p).convert("RGB")
    if trim:
        im = _trim(im)
    r = target_w / im.width
    return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)


def bayangan(im, blur=26, alpha=90):
    pad = blur * 2
    canvas = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (10, 8, 6, alpha))
    canvas.paste(sh, (pad, pad))
    canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(im.convert("RGBA"), (pad, pad))
    return canvas


def marker(d, cx, cy, r, warna=INK, bg=PAPER, gap=0.095):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=warna)
    g = max(2, int(r * 2 * gap))
    d.rectangle([cx - g / 2, cy - r - 2, cx + g / 2, cy + r + 2], fill=bg)


def titik_roast(d, x, y, r, gap, level, warna=INK):
    for i in range(5):
        cx = x + i * (r * 2 + gap)
        box = [cx - r, y - r, cx + r, y + r]
        if i < level:
            d.ellipse(box, fill=warna)
        else:
            d.ellipse(box, outline=warna, width=max(2, int(r / 3)))


def stempel(img, teks1, teks2, r=120, sudut=-9, warna=ORANGE, pos=None):
    size = r * 2 + 12
    lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = size // 2
    d.ellipse([c - r, c - r, c + r, c + r], outline=(*warna, 235), width=6)
    d.ellipse([c - r + 14, c - r + 14, c + r - 14, c + r - 14], outline=(*warna, 150), width=2)
    f1 = F(SANS_BLACK, r * 0.62)
    f2 = F(SANS_SEMI, r * 0.2)
    w1 = d.textlength(teks1, font=f1)
    d.text((c - w1 / 2, c - r * 0.52), teks1, font=f1, fill=(*warna, 245))
    w2 = d.textlength(teks2, font=f2)
    d.text((c - w2 / 2, c + r * 0.02), teks2, font=f2, fill=(*warna, 240))
    lay = lay.rotate(sudut, resample=Image.BICUBIC, expand=False)
    img.alpha_composite(lay, (int(pos[0]), int(pos[1])))


def lockup(img, d, x, y, skala=1.0, warna=INK, sub=True):
    r = 13 * skala
    marker(d, x + r, y + r, r, warna, bg=(PAPER if warna == INK else INK))
    d.text((x + r * 2 + 12 * skala, y - 2 * skala), "Nocturne", font=F(SANS_BLACK, 27 * skala), fill=warna)
    if sub:
        d.text((x + r * 2 + 14 * skala, y + 28 * skala), "K O F F I E   B R A N D",
               font=F(SANS_SEMI, 8.5 * skala), fill=(*warna, 160) if warna == INK else warna)


# ────────────────────────────── bingkai video ──────────────────────────────
def frame_dasar(w, h, base=PAPER):
    return kertas(w, h, base, seed=w + h).convert("RGBA")


def lapisan_teks(w, h, baris, warna=INK, ukuran=96, atas=None, x=None, font=SANS_BLACK,
                 alpha=255, max_w=None, tinggi_baris=1.03):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = 80 if x is None else x
    y = atas if atas is not None else h * 0.28
    max_w = max_w if max_w else w - x * 2
    for teks, gaya in baris:
        f = F(font if gaya.get("font") is None else gaya["font"], ukuran * gaya.get("skala", 1))
        warna_t = gaya.get("warna", warna)
        for ln in teks_bungkus(d, teks, f, max_w):
            d.text((x, y), ln, font=f, fill=(*warna_t, alpha))
            y += ukuran * gaya.get("skala", 1) * tinggi_baris
        y += ukuran * 0.12
    return lay


TEXT_TOP = 300
TEXT_BOT = 940
IMG_TOP, IMG_BOT = 986, 1452
CTA_TOP, CTA_BOT = 1504, 1712


_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def tinggi_baris(baris, ukuran, max_w):
    total = 0.0
    for teks, gaya in baris:
        f = F(gaya.get("font") or SANS_BLACK, ukuran * gaya.get("skala", 1))
        n = len(teks_bungkus(_MEASURE, teks, f, max_w))
        total += n * ukuran * gaya.get("skala", 1) * 1.03 + ukuran * 0.12
    return total


def render_reel(judul, adegan, path_mp4, path_poster, durasi=7.0, produk="ijen.jpg",
                warna_panel=None, meta="", cta="Pesan via WhatsApp", handle="@nocturnekoffie"):
    """Zona tetap: judul 300–940, foto 986–1452, kartu CTA 1504–1712. Teks berganti per beat."""
    W, H = 1080, 1920
    dasar = frame_dasar(W, H)
    d0 = ImageDraw.Draw(dasar)

    d0.rectangle([40, 40, W - 40, H - 40], outline=(198, 186, 168), width=2)
    lockup(dasar, d0, 74, 78, 1.05)
    kicker = "NOCTURNEKOFFIE.ID · BANYUWANGI"
    d0.text((W - 74 - d0.textlength(kicker, font=F(SANS_SEMI, 18)), 92), kicker,
            font=F(SANS_SEMI, 18), fill=(150, 138, 122))

    # foto produk: masuk tepat di zona
    f = foto_produk(produk, 900)
    gerbang = IMG_BOT - IMG_TOP - 76
    if f.height > gerbang:
        r = gerbang / f.height
        f = f.resize((max(1, int(f.width * r)), max(1, int(f.height * r))), Image.LANCZOS)
    f = f.resize((int(f.width * 1.10), int(f.height * 1.10)), Image.LANCZOS)
    if warna_panel:
        f = Image.blend(f, Image.new("RGB", f.size, warna_panel), 0.5)
    fsh = bayangan(f, 26, 70)

    # teks dipusatkan vertikal di zona judul
    zona_teks = TEXT_BOT - 150 - TEXT_TOP
    for ad in adegan:
        t_ad = tinggi_baris(ad["baris"], ad.get("ukuran", 100), W - 160)
        ad["_atas"] = TEXT_TOP + max(0.0, (zona_teks - t_ad) / 2)

    total = int(durasi * FPS)
    tmp = tempfile.mkdtemp(prefix="nk-reel-")

    for i in range(total):
        t = i / FPS
        p = t / durasi
        img = dasar.copy()

        # foto: naik pelan + zoom halus, tetap di dalam zona
        masuk = ease_out(seg(t, 0.05, 0.85))
        zr = 1.0 + 0.04 * p
        fw, fh = int(fsh.width * zr), int(fsh.height * zr)
        fz = fsh.resize((fw, fh), Image.LANCZOS)
        al = int(255 * masuk)
        if al > 0:
            layer = fz.copy()
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * al / 255)))
            fx = int(W / 2 - fw / 2)
            fy = int(IMG_TOP + (IMG_BOT - IMG_TOP - fh) / 2 + (1 - masuk) * 40)
            img.alpha_composite(layer, (fx, max(60, fy)))

        # teks per beat (dibatasi zona judul)
        for ad in adegan:
            a = ease_out(seg(t, ad["t0"], ad["t0"] + 0.4))
            bb = 1 - ease_out(seg(t, ad["t1"] - 0.28, ad["t1"])) if ad.get("t1") else 1
            alpha = int(255 * min(a, bb))
            if alpha <= 3:
                continue
            lay = lapisan_teks(W, H, ad["baris"], ukuran=ad.get("ukuran", 100),
                               atas=ad["_atas"] - (1 - a) * 24, x=80, alpha=alpha,
                               max_w=W - 160)
            img.alpha_composite(lay)

        # garis aksen + meta produk
        gp = ease_out(seg(t, 0.6, 1.6))
        if gp > 0:
            d = ImageDraw.Draw(img)
            d.rectangle([80, TEXT_BOT - 78, 80 + int(190 * gp), TEXT_BOT - 71], fill=ORANGE)
            if meta:
                d.text((80, TEXT_BOT - 40), meta.upper(), font=F(SANS_SEMI, 21), fill=(140, 128, 112))

        # kartu penutup (solid)
        cp = ease_out(seg(t, durasi - 1.4, durasi - 0.5))
        if cp > 0:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            a = int(255 * cp)
            d.rounded_rectangle([80, CTA_TOP, W - 80, CTA_BOT], radius=8, fill=(*INK, a))
            d.text((116, CTA_TOP + 30), cta, font=F(SANS_BOLD, 40), fill=(*PAPER, a))
            d.text((116, CTA_TOP + 86), "nocturnekoffie.id  ·  " + handle,
                   font=F(SANS, 26), fill=(230, 222, 210, int(a * 0.72)))
            d.text((116, CTA_TOP + 128), "Tanggal sangrai dicetak di tiap kantong",
                   font=F(SANS_SEMI, 22), fill=(*GOLD, a))
            img.alpha_composite(lay)

        img.convert("RGB").save(os.path.join(tmp, f"{i:04d}.png"), compress_level=1)

    poster_frame = max(0, min(total - 1, int((durasi - 0.55) * FPS)))
    Image.open(os.path.join(tmp, f"{poster_frame:04d}.png")).convert("RGB").save(
        path_poster, quality=90, optimize=True)

    ff = None
    try:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        if shutil.which("ffmpeg"):
            ff = shutil.which("ffmpeg")

    if ff:
        subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", os.path.join(tmp, "%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "25",
                        "-preset", "medium", "-movflags", "+faststart", path_mp4], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return bool(ff)


# ───────────────────────────── slide & statis ──────────────────────────────
def slide_teks(path, judul, baris, label, ukuran=92, rasio=(1080, 1350), foto=None,
               footer="nocturnekoffie.id", nomor=None):
    """Slide editorial: judul di atas, foto di tengah, body menempel di bawah."""
    W, H = rasio
    img = frame_dasar(W, H)
    d = ImageDraw.Draw(img)
    d.rectangle([36, 36, W - 36, H - 36], outline=(198, 186, 168), width=2)
    lockup(img, d, 66, 66, 0.85)
    d.text((66, 140), label.upper(), font=F(SANS_SEMI, 21), fill=(140, 128, 112))
    d.line([66, 178, W - 66, 178], fill=INK, width=3)

    # judul
    y = 226
    f = F(SANS_BLACK, ukuran)
    for ln in teks_bungkus(d, judul, f, W - 132):
        d.text((66, y), ln, font=f, fill=INK)
        y += ukuran * 1.02
    judul_bawah = y
    d.rectangle([66, y + 26, 66 + 150, y + 33], fill=ORANGE)

    # body menempel di atas footer
    fb = F(SERIF_IT, 40)
    blok = []
    for ln in baris:
        blok += teks_bungkus(d, ln, fb, W - 132)
    tinggi = len(blok) * 50 + (len(baris) - 1) * 12
    body_bawah = H - 216
    body_atas = body_bawah - tinggi
    if tinggi and body_atas < judul_bawah + 60:
        body_atas = judul_bawah + 60

    # foto di ruang tengah
    if foto:
        im = foto_produk(foto, W - 132)
        sh = bayangan(im, 22, 70)
        ruang = (body_atas if tinggi else H - 190) - (judul_bawah + 46) - 24
        max_h = min(int(H * 0.44), max(180, ruang))
        if sh.height > max_h:
            r = max_h / sh.height
            sh = sh.resize((int(sh.width * r), int(sh.height * r)), Image.LANCZOS)
        fy = int(judul_bawah + 46 + (max_h - sh.height) / 2)
        img.alpha_composite(sh, (int(W / 2 - sh.width / 2), fy))

    # ornamen tengah bila tanpa foto: angka slide hantu
    if not foto and nomor:
        ang = nomor.split("/")[0]
        ruang = (body_atas if tinggi else H - 190) - (judul_bawah + 56)
        if ruang > 300:
            size = min(360.0, ruang - 96)
            fg = F(SANS_BLACK, size)
            bb = d.textbbox((0, 0), ang, font=fg)
            gh = bb[3] - bb[1]
            while gh > ruang - 96 and size > 120:
                size *= 0.94
                fg = F(SANS_BLACK, size)
                bb = d.textbbox((0, 0), ang, font=fg)
                gh = bb[3] - bb[1]
            bawah = (body_atas if tinggi else H - 200) - 54
            atas_g = bawah - gh
            d.text((66 - bb[0], atas_g - bb[1]), ang, font=fg, fill=(228, 217, 199))
            d.text((66, atas_g - 40), "N O C T U R N E   ·   B U K T I",
                   font=F(SANS_SEMI, 17), fill=(186, 174, 154))

    yy = body_atas
    for i, ln in enumerate(blok):
        d.text((66, yy), ln, font=fb, fill=(70, 60, 52))
        yy += 50

    # footer
    d.line([66, H - 178, W - 66, H - 178], fill=(198, 186, 168), width=2)
    d.text((66, H - 140), footer, font=F(SANS_SEMI, 22), fill=(140, 128, 112))
    kanan = "Nocturne Koffie" if nomor is None else f"Nocturne Koffie · {nomor}"
    d.text((W - 66 - d.textlength(kanan, font=F(SANS_SEMI, 22)), H - 140), kanan,
           font=F(SANS_SEMI, 22), fill=INK)
    img.convert("RGB").save(path, quality=93, optimize=True)
    return path


def slide_stempel(path, judul, baris, label, skor="81.5", ukuran=96):
    """Slide gelap: batch ditolak. Kartu catatan QC di tengah + stempel."""
    W, H = 1080, 1350
    img = frame_dasar(W, H, INK)
    d = ImageDraw.Draw(img)
    d.rectangle([36, 36, W - 36, H - 36], outline=(70, 60, 52), width=2)
    marker(d, 66 + 12, 66 + 12, 12, PAPER, bg=INK)
    d.text((104, 62), "Nocturne", font=F(SANS_BLACK, 27), fill=PAPER)
    d.text((106, 92), "K O F F I E   B R A N D", font=F(SANS_SEMI, 9), fill=(150, 138, 122))
    d.text((66, 146), label.upper(), font=F(SANS_SEMI, 21), fill=GOLD)

    y = 220
    f = F(SANS_BLACK, ukuran)
    for ln in teks_bungkus(d, judul, f, W - 132):
        d.text((66, y), ln, font=f, fill=PAPER)
        y += ukuran * 1.02

    y += 34
    fb = F(SERIF_IT, 40)
    for ln in baris:
        for l2 in teks_bungkus(d, ln, fb, W - 132):
            d.text((66, y), l2, font=fb, fill=(214, 205, 192))
            y += 50
        y += 8

    # kartu catatan QC
    ky = min(y + 64, H - 430)
    d.rounded_rectangle([66, ky, W - 96, ky + 268], radius=6, fill=(44, 35, 28))
    d.text((98, ky + 30), "CATATAN CUP · BATCH NK-RNG-2610-A", font=F(SANS_SEMI, 16), fill=(150, 138, 122))
    d.line([98, ky + 66, W - 128, ky + 66], fill=(70, 60, 52), width=2)
    baris_qc = [("Skor cup", skor), ("Ambang kami", "83,0"), ("Keputusan", "disangrai ulang"),
                ("Dikirim", "tidak")]
    yy = ky + 88
    for k, v in baris_qc:
        d.text((98, yy), k, font=F(SANS, 24), fill=(160, 150, 136))
        wv = d.textlength(v, font=F(SANS_BOLD, 24))
        warna_v = ORANGE if k in ("Keputusan", "Dikirim") else PAPER
        d.text((W - 128 - wv, yy), v, font=F(SANS_BOLD, 24), fill=warna_v)
        yy += 44

    stempel(img, skor, "DITOLAK · QC", 112, -11, ORANGE, (W - 322, H - 356))
    d.text((66, H - 108), "Setiap batch dicicipi. Yang tidak lolos tidak dikirim.",
           font=F(SANS_SEMI, 22), fill=(150, 138, 122))
    img.convert("RGB").save(path, quality=93, optimize=True)
    return path


def story_frame(path, judul, isi, jenis="teks"):
    W, H = 1080, 1920
    img = frame_dasar(W, H)
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, W - 40, H - 40], outline=(198, 186, 168), width=2)
    lockup(img, d, 74, 74, 0.95)
    d.text((74, 300), "STORY · " + ("JAJAK PENDAHULUAN" if jenis == "poll" else "EDUKASI"),
           font=F(SANS_SEMI, 22), fill=(140, 128, 112))

    y = 360
    f = F(SANS_BLACK, 96)
    for ln in teks_bungkus(d, judul, f, W - 148):
        d.text((74, y), ln, font=f, fill=INK)
        y += 98
    d.rectangle([74, y + 20, 74 + 160, y + 27], fill=ORANGE)
    y += 78

    fb = F(SERIF_IT, 44)
    for ln in isi:
        for l2 in teks_bungkus(d, ln, fb, W - 148):
            d.text((74, y), l2, font=fb, fill=(70, 60, 52))
            y += 56
        y += 10

    # ornamen tengah: cincin + siluet angka/tanda
    bawah = (H - 470) if jenis == "poll" else (H - 200)
    ruang = bawah - y - 40
    if ruang > 300:
        cy = int(y + 40 + ruang / 2)
        r = int(min(ruang * 0.34, 190))
        d.ellipse([W // 2 - r, cy - r, W // 2 + r, cy + r], outline=(220, 209, 190), width=3)
        d.ellipse([W // 2 - r + 18, cy - r + 18, W // 2 + r - 18, cy + r - 18],
                  outline=(228, 217, 199), width=2)
        glif = "?" if jenis == "poll" else "3"
        fg = F(SERIF_IT, r * 1.15)
        bb = d.textbbox((0, 0), glif, font=fg)
        d.text((W // 2 - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]),
               glif, font=fg, fill=(214, 203, 184))

    if jenis == "poll":
        for i, opsi in enumerate(["< 2 minggu", "> 1 bulan"]):
            yy = H - 460 + i * 116
            d.rounded_rectangle([74, yy, W - 74, yy + 92], radius=10, outline=INK, width=3)
            d.text((108, yy + 30), opsi, font=F(SANS_SEMI, 34), fill=INK)

    d.text((74, H - 128), "nocturnekoffie.id", font=F(SANS_SEMI, 24), fill=(140, 128, 112))
    img.convert("RGB").save(path, quality=93, optimize=True)
    return path


def post_peta_rasa(path):
    W, H = 1080, 1080
    img = frame_dasar(W, H)
    d = ImageDraw.Draw(img)
    d.rectangle([32, 32, W - 32, H - 32], outline=(198, 186, 168), width=2)
    lockup(img, d, 60, 58, 0.8)
    d.text((60, 128), "PAKET · 3 × 100 g", font=F(SANS_SEMI, 19), fill=(140, 128, 112))
    f = F(SANS_BLACK, 78)
    d.text((60, 158), "Peta Rasa", font=f, fill=INK)
    d.text((60, 162), "", font=f, fill=INK)
    d.text((60, 246), "Tiga keluarga kopi. Satu kotak.", font=F(SERIF_IT, 34), fill=(70, 60, 52))

    trio = ["ijen.jpg", "raung.jpg", "excelsa.jpg"]
    x = 62
    for i, nm in enumerate(trio):
        im = foto_produk(nm, 290)
        ang = 4 if i == 1 else -3
        im = im.rotate(ang, expand=True, resample=Image.BICUBIC)
        sh = bayangan(im, 16, 60)
        img.alpha_composite(sh, (x, 340))
        x += 300

    d.text((60, H - 190), rp(harga("peta-rasa")), font=F(SANS_BLACK, 62), fill=INK)
    d.text((60, H - 118), "biasanya " + rp(88000), font=F(SANS, 28), fill=(140, 128, 112))
    d.rounded_rectangle([W - 380, H - 178, W - 60, H - 96], radius=999, fill=INK)
    d.text((W - 340, H - 156), "Pesan via WA →", font=F(SANS_SEMI, 30), fill=PAPER)
    img.convert("RGB").save(path, quality=93, optimize=True)
    return path


# ────────────────────────────── hub konten ────────────────────────────────
def hub_html(items, tgl):
    kartu = ""
    for it in items:
        if it["format"] == "video":
            media = (f'<video src="{it["file"]}" poster="{it["poster"]}" controls muted loop playsinline '
                     f'preload="metadata"></video>')
        else:
            media = f'<img src="{it["file"]}" alt="{it["judul"]}" loading="lazy">'
        kartu += f"""<article class="kartu">
      <div class="media {it['format']}">{media}</div>
      <div class="isi">
        <p class="meta">{it['platform']} · {it['rasio']}{' · ' + str(it.get('durasi','')) + 's' if it.get('durasi') else ''}</p>
        <h3>{it['judul']}</h3>
        <p class="cap">{it['caption_ringkas']}</p>
        <p class="jadwal">Jadwal: {it['jadwal']} · status: <b>{it['status']}</b></p>
        <details><summary>Caption lengkap</summary><pre>{it['caption']}</pre></details>
      </div>
    </article>"""

    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hub Konten — Nocturne Koffie</title>
<meta name="robots" content="noindex">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--paper:#F5EFE4;--ink:#16110D;--muted:#6b6156;--orange:#E1542B;--gold:#D9A441;--line:1px solid rgba(22,17,13,.14)}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 Inter,system-ui,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:42px clamp(16px,4vw,40px) 80px}}
h1{{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(30px,5vw,46px);line-height:1;letter-spacing:-.03em;margin:6px 0 10px}}
.kicker{{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}}
.lede{{max-width:64ch;color:var(--muted)}}
.bar{{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 30px}}
.bar a{{font-size:13px;padding:8px 14px;border-radius:99px;border:var(--line);text-decoration:none;color:inherit}}
.bar a:hover{{border-color:var(--ink)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:22px}}
.kartu{{border:var(--line);border-radius:8px;overflow:hidden;background:#fff8;display:flex;flex-direction:column}}
.media{{background:var(--ink);display:grid;place-items:center;overflow:hidden}}
.media.video{{aspect-ratio:9/16}}
.media img{{width:100%;display:block}}
.media video{{width:100%;height:100%;object-fit:cover;display:block}}
.isi{{padding:14px 16px 18px}}
.meta{{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}}
h3{{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:19px;margin:0 0 6px;line-height:1.15}}
.cap{{font-size:13.5px;color:var(--muted);margin:0 0 10px}}
.jadwal{{font-size:12px;margin:0 0 10px;color:var(--muted)}}
details{{font-size:12.5px}}
summary{{cursor:pointer;color:var(--orange);font-weight:600}}
pre{{white-space:pre-wrap;font:12.5px/1.55 Inter,sans-serif;background:#fff;padding:10px;border-radius:6px;border:var(--line);max-height:260px;overflow:auto}}
footer{{margin-top:40px;border-top:1px solid rgba(22,17,13,.18);padding-top:14px;font-size:12px;color:var(--muted);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}}
</style></head><body><div class="wrap">
<p class="kicker">D4 Kreatif &amp; Media · dibuat {tgl.strftime('%d %B %Y')} · tools/kreatif.py</p>
<h1>Hub Konten</h1>
<p class="lede">Semua aset video &amp; gambar siap tayang. Video sudah 9:16 (1080×1920, 24 fps) — tinggal unggah
sebagai Reels/TikTok, atau pakai posternya untuk carousel. Caption diambil dari
<code>marketing/08-konten-siap-pakai.md</code>. Setelah tayang, ubah status di
<code>data/kreatif.json</code> lalu jalankan <code>python3 tools/papan.py</code>.</p>
<div class="bar">
  <a href="../index.html">← Situs</a>
  <a href="../dashboard/index.html">Papan harian</a>
  <a href="../kampanye/index.html">Landing kampanye</a>
  <a href="../brand/index.html">Brand kit</a>
  <a href="../marketing/08-konten-siap-pakai.md">Naskah konten</a>
  <a href="../marketing/09-media-kreator.md">Playbook kreator</a>
</div>
<div class="grid">{kartu}</div>
<footer><span>Dihasilkan otomatis — jangan edit berkas ini.</span><span>{len(items)} aset</span></footer>
</div></body></html>"""


# ──────────────────────────────── main ────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cepat", action="store_true", help="lewati encode video")
    ap.add_argument("--tanggal", default=None)
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    tgl = date.fromisoformat(args.tanggal) if args.tanggal else date.today()
    items = []
    video_ok = False

    # ── 1. Video vertikal
    reels = [
        dict(
            id="reel-menit-terakhir", judul="12 menit terakhir sebelum kopi dikemas",
            file="reel-01-menit-terakhir.mp4", poster="reel-01-poster.jpg", produk="ijen.jpg",
            meta="Blue Mount Ijen · Arabika · 1.700–1.800 mdpl",
            adegan=[
                dict(t0=0.15, t1=2.5, baris=[("12 menit terakhir", {})], ukuran=118),
                dict(t0=2.3, t1=4.6, baris=[("sebelum kopi ini", {}), ("dikemas.", {"warna": ESPRESSO})], ukuran=104),
                dict(t0=4.4, t1=6.7, baris=[("20 detik lebih lama,", {"skala": 0.86}),
                                            ("rasanya berubah.", {"warna": ORANGE, "skala": 0.86})], ukuran=96),
            ],
            jadwal="3 Nov 2026", platform="IG Reels", rasio="9:16",
            caption_ringkas="Proses sangrai: berhenti berdasarkan catatan, bukan perasaan.",
        ),
        dict(
            id="reel-tanggal-sangrai", judul="Tanggal sangrai, bukan tanggal kedaluwarsa",
            file="reel-02-tanggal-sangrai.mp4", poster="reel-02-poster.jpg", produk="raung.jpg",
            meta="Raung · Robusta · 422–443 mdpl",
            adegan=[
                dict(t0=0.15, t1=2.4, baris=[("Kami tidak mencetak", {}), ("tanggal kedaluwarsa.", {"warna": ESPRESSO})], ukuran=100),
                dict(t0=2.2, t1=4.3, baris=[("Kami mencetak", {}), ("tanggal sangrai.", {"warna": ORANGE})], ukuran=104),
                dict(t0=4.1, t1=6.7, baris=[("Puncak rasa:", {"skala": 0.6}), ("7–21 hari", {"skala": 1.3}),
                                            ("setelah sangrai.", {"skala": 0.6})], ukuran=100),
            ],
            jadwal="4 Nov 2026", platform="IG Carousel (penutup) + Reels", rasio="9:16",
            caption_ringkas="Bukti kesegaran yang bisa dihitung sendiri oleh pembeli.",
        ),
        dict(
            id="reel-first-crack", judul="Suara first crack",
            file="reel-03-first-crack.mp4", poster="reel-03-poster.jpg", produk="gayo.jpg",
            meta="Gayo · Arabika · 1.346 mdpl · Natural",
            adegan=[
                dict(t0=0.15, t1=2.5, baris=[("Dengar ini sekali.", {})], ukuran=112),
                dict(t0=2.3, t1=4.6, baris=[("Biji pecah.", {"warna": ORANGE}), ("Rasanya mulai terbentuk.", {"skala": 0.72})], ukuran=104),
                dict(t0=4.4, t1=6.7, baris=[("Kami berhenti", {}), ("di titik itu,", {"warna": ESPRESSO}), ("tiap batch.", {"skala": 0.72})], ukuran=100),
            ],
            jadwal="5 Nov 2026", platform="TikTok", rasio="9:16",
            caption_ringkas="Audio asli first crack — hook tanpa perlu bicara.",
        ),
        dict(
            id="reel-batch-ditolak", judul="Minggu ini satu batch tidak lolos",
            file="reel-04-batch-ditolak.mp4", poster="reel-04-poster.jpg", produk="blend-7030.jpg",
            warna_panel=INK, meta="Batch NK-RNG-2610-A · skor cup 81,5",
            adegan=[
                dict(t0=0.15, t1=2.4, baris=[("Minggu ini", {}), ("satu batch", {"warna": ESPRESSO}), ("tidak lolos.", {})], ukuran=104),
                dict(t0=2.2, t1=4.4, baris=[("Skornya 81,5.", {}), ("Ambang kami 83.", {"skala": 0.74, "warna": ORANGE})], ukuran=98),
                dict(t0=4.2, t1=6.7, baris=[("Kami tidak", {}), ("mengirimnya.", {"warna": ORANGE})], ukuran=112),
            ],
            jadwal="7 Nov 2026", platform="IG Reels", rasio="9:16",
            caption_ringkas="Kepercayaan dibangun dari hal yang berani ditolak.",
        ),
        dict(
            id="reel-kirim-hari-ini", judul="Order hari ini, dikirim hari ini",
            file="reel-05-kirim-hari-ini.mp4", poster="reel-05-poster.jpg", produk="semeru.jpg",
            meta="Pesan sebelum 15.00 WIB · Senin–Sabtu",
            adegan=[
                dict(t0=0.15, t1=2.4, baris=[("Order hari ini,", {}), ("dikirim hari ini.", {"warna": ORANGE})], ukuran=104),
                dict(t0=2.2, t1=4.4, baris=[("Sebelum jam 15.00 WIB,", {"skala": 0.78}), ("Senin–Sabtu.", {})], ukuran=98),
                dict(t0=4.2, t1=6.7, baris=[("Resi dikirim", {}), ("hari itu juga,", {"warna": ESPRESSO}), ("bukan besok.", {"skala": 0.72})], ukuran=100),
            ],
            jadwal="13 Nov 2026", platform="IG Reels", rasio="9:16",
            caption_ringkas="Janji operasional yang bisa dicek: cut-off 15.00, resi hari itu.",
        ),
    ]

    for r in reels:
        if not args.cepat:
            ok = render_reel(r["judul"], r["adegan"], os.path.join(OUT, r["file"]),
                             os.path.join(OUT, r["poster"]), durasi=7.0, produk=r["produk"],
                             warna_panel=r.get("warna_panel"), meta=r.get("meta", ""))
            video_ok = video_ok or ok
        else:
            # tanpa encode: pakai gambar produk sebagai poster sementara
            shutil.copy(os.path.join(PRODUK, r["produk"]), os.path.join(OUT, r["poster"]))
        items.append(dict(
            id=r["id"], judul=r["judul"], platform=r["platform"], format="video", rasio=r["rasio"],
            file=r["file"] if not args.cepat else r["poster"], poster=r["poster"], durasi=7,
            jadwal=r["jadwal"], status="siap", caption_ringkas=r["caption_ringkas"],
            caption=CAPTION.get(r["id"], ""),
        ))

    # ── 2. Carousel 4:5
    car = [
        ("carousel-01a.jpg", "Kenapa kami mencetak tanggal sangrai, bukan kedaluwarsa",
         ["Kata \u201cfresh\u201d tidak bisa diperiksa. Tanggal bisa.",
          "Jadi tanggal sangrai yang kami cetak \u2014 bukan tanggal kedaluwarsa yang mengarang batas."],
         "Bukti \u00b7 slide 1 dari 3", 88, None, "1/3"),
        ("carousel-01b.jpg", "Rasa terbaiknya 7\u201321 hari setelah sangrai",
         ["Setelah itu masih enak \u2014 hanya kehilangan bagian paling menariknya.",
          "Karena itu kami sangrai mingguan, bukan menyetok banyak sekaligus."],
         "Bukti \u00b7 slide 2 dari 3", 74, "raung.jpg", "2/3"),
        ("carousel-01c.jpg", "Di tiap kantong ada tiga hal",
         ["tanggal sangrai \u00b7 kode batch \u00b7 level roast",
          "Sebutkan kode batch kalau rasanya tidak sesuai \u2014 kami bisa cek catatan QC, bukan menebak."],
         "Bukti \u00b7 slide 3 dari 3", 82, None, "3/3"),
        ("carousel-02a.jpg", "Biji utuh atau digiling?",
         ["Biji utuh bertahan 3\u20134\u00d7 lebih lama.",
          "Tapi butuh grinder. Kalau belum punya, kami giling sesuai metode seduh Anda."],
         "Edukasi \u00b7 slide 1 dari 2", 88, "ijen.jpg", "1/2"),
        ("carousel-02b.jpg", "Kalau kami giling, sebutkan alatnya",
         ["V60 butuh gilingan lebih kasar daripada moka pot.",
          "Satu pertanyaan di WhatsApp, dan kami kirim ukuran yang tepat."],
         "Edukasi \u00b7 slide 2 dari 2", 72, None, "2/2"),
        ("carousel-03a.jpg", "Belum punya grinder? Mulai dari sini",
         ["Night Drip: 10 sachet, cukup air panas.",
          "Rp45.000 untuk 10 cangkir \u2014 cara termurah mencoba kopi Banyuwangi tanpa alat."],
         "Jualan \u00b7 slide 1 dari 2", 78, "excelsa.jpg", "1/2"),
    ]
    for nama, judul, baris, label, uk, foto, nomor in car:
        p = slide_teks(os.path.join(OUT, nama), judul, baris, label, uk, foto=foto, nomor=nomor)
        items.append(dict(
            id=nama.replace(".jpg", ""), judul=judul, platform="Instagram (carousel)", format="gambar",
            rasio="4:5", file=nama, poster=nama, jadwal="4–11 Nov 2026", status="siap",
            caption_ringkas=label, caption=CAPTION.get("carousel", ""),
        ))

    # slide gelap (batch ditolak)
    p = slide_stempel(os.path.join(OUT, "carousel-04a.jpg"),
                      "Batch yang tidak lolos tidak dikirim",
                      ["Aftertaste pahit, manisnya tidak muncul.",
                       "Disangrai ulang, dicicipi lagi, baru masuk kemasan."],
                      "Bukti · slide 1 dari 2", skor="81,5")
    items.append(dict(id="carousel-04a", judul="Batch yang tidak lolos tidak dikirim",
                      platform="Instagram (carousel)", format="gambar", rasio="4:5",
                      file="carousel-04a.jpg", poster="carousel-04a.jpg", jadwal="7 Nov 2026",
                      status="siap", caption_ringkas="Slide gelap dengan stempel QC.",
                      caption=CAPTION.get("batch", "")))

    # ── 3. Story
    for nama, judul, isi, jenis in [
        ("story-01.jpg", "Tiga tanda kopi masih segar", ["Aroma keluar saat dibuka.", "Biji masih mengkilap, tidak berminyak berlebih.", "Mengembang (bloom) saat diseduh."], "teks"),
        ("story-02.jpg", "Kopi di rumah Anda berapa lama?", ["Jawaban Anda menentukan kapan kami tawarkan restock."], "poll"),
    ]:
        story_frame(os.path.join(OUT, nama), judul, isi, jenis)
        items.append(dict(id=nama.replace(".jpg", ""), judul=judul, platform="Instagram Story",
                          format="gambar", rasio="9:16", file=nama, poster=nama,
                          jadwal="6 Nov 2026", status="siap", caption_ringkas="Story " + jenis,
                          caption="Teks di layar: " + " / ".join(isi)))

    # ── 4. Feed 1:1
    post_peta_rasa(os.path.join(OUT, "post-01-peta-rasa.jpg"))
    items.append(dict(id="post-01-peta-rasa", judul="Peta Rasa — tiga keluarga kopi",
                      platform="Instagram (feed)", format="gambar", rasio="1:1",
                      file="post-01-peta-rasa.jpg", poster="post-01-peta-rasa.jpg",
                      jadwal="10 Nov 2026", status="siap",
                      caption_ringkas="Post jualan utama: paket termurah sebagai pintu masuk.",
                      caption=CAPTION.get("peta", "")))

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_html(items, tgl))

    manifest = {
        "_catatan": "Manifest aset kreatif. Dibaca situs (strip 'Di balik sangrai') dan papan harian. "
                    "Ubah status jadi 'tayang' setelah diposting.",
        "dibuat": tgl.isoformat(),
        "video_terencode": video_ok,
        "items": items,
    }
    with open(os.path.join(ROOT, "data", "kreatif.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    vid = sum(1 for i in items if i["format"] == "video")
    img = sum(1 for i in items if i["format"] == "gambar")
    print(f"Aset kreatif dibuat: {vid} video · {img} gambar · {len(items)} total")
    print("  video terencode:", "ya" if video_ok else "TIDAK (ffmpeg tidak ditemukan)")
    print("  hub:", os.path.relpath(os.path.join(OUT, 'index.html'), ROOT))
    print("  manifest:", os.path.relpath(os.path.join(ROOT, 'data', 'kreatif.json'), ROOT))
    for i in items:
        print(f"   - {i['file']:<30} {i['rasio']:>5}  {i['judul'][:52]}")


CAPTION = {
    "reel-menit-terakhir": """Dua belas menit terakhir sebelum kopi ini bisa dikirim.

Suhu turun, first crack lewat, dan kami berhenti di titik development yang
sudah ditentukan untuk batch ini. Kalau berhenti 20 detik lebih lama, rasanya
berubah — jadi kami berhenti berdasarkan catatan, bukan perasaan.

Setelah itu kopi masih harus menunggu: dicicipi besok, dicicipi lagi hari ke-7,
baru dikemas dengan tanggal sangrai & kode batch.

Kopi batch minggu ini: [produk] · [tanggal sangrai]
Pesan lewat tautan di bio.

#kopibanyuwangi #proseskopi #specialtycoffeeindonesia #nocturnekoffie""",
    "reel-tanggal-sangrai": """Kami tidak mencetak tanggal kedaluwarsa. Kami mencetak tanggal sangrai.

Kopi bukan makanan yang "rusak" di satu tanggal. Rasa terbaiknya ada di jendela
7–21 hari setelah disangrai. Setelah itu masih enak, hanya kehilangan bagian
paling menariknya.

Di tiap kantong: tanggal sangrai · kode batch · level roast 1–5.
Kalau rasanya tidak sesuai, sebutkan kode batch-nya — kami bisa cek catatan QC,
bukan menebak.

#kopisegar #kopibanyuwangi #nocturnekoffie""",
    "reel-batch-ditolak": """Minggu ini satu batch tidak lolos.

Skornya 81,5 — ambang kami 83. Aftertaste-nya pahit dan manisnya tidak muncul.
Batch itu tidak dikirim. Biji disangrai ulang, dicicipi lagi, baru masuk kemasan.

Kerugiannya nyata untuk kami, tapi lebih baik kami menanggungnya daripada Anda
menerima kopi yang "agak beda" dari yang Anda beli sebelumnya.

Bukan cerita bagus — ini bagian dari pekerjaannya: menolak hasil sendiri kalau
tidak memenuhi standar.

#qualitycontrol #kopibanyuwangi #nocturnekoffie""",
    "carousel": """Simpan untuk dibaca lagi.

Kami mencetak tanggal sangrai karena itu satu-satunya bukti kesegaran yang
bisa Anda periksa sendiri. Kata "fresh" tidak bisa diperiksa.

Batch terbaru ada di tautan bio.""",
    "batch": """Setiap batch dicicipi sebelum dijual. Yang tidak lolos tidak dikirim.

Kami tidak menjualnya dengan diskon, dan tidak mengirimnya dengan label berbeda.
Disangrai ulang.

Skor dan catatan tiap batch kami simpan. Kalau mau tahu batch kopi Anda,
sebutkan kode batch di kemasan.""",
    "peta": """Belum tahu mau mulai dari mana?

Peta Rasa: tiga keluarga kopi dalam satu kotak.
— Blue Mount Ijen (arabika, 1.700–1.800 mdpl)
— Raung (robusta, 422–443 mdpl)
— Ijen Excelsa (excelsa, 434–442 mdpl)

Tiga-tiganya dari Banyuwangi, tiga profil rasa yang betul-betul berbeda.

Rp79.000 untuk 3 × 100 g (biasanya Rp88.000 kalau dibeli terpisah).
Pesan lewat tautan di bio — sebut saja "PETA RASA".""",
}


if __name__ == "__main__":
    main()
