#!/usr/bin/env python3
"""Foto 3D kemasan untuk e-commerce — permukaan 3D sungguhan, shading per piksel.

Kenapa ditulis ulang
--------------------
Versi sebelumnya mengisi tiap muka dengan satu gradien lurus, jadi hasilnya
terbaca sebagai kotak hitam berlabel. Foto produk yang meyakinkan butuh:
lengkung panel yang menangkap lampu, tepi yang menggelap, kilau kain, dan
bayangan yang masuk akal.

Cara kerjanya
-------------
1. **Permukaan, bukan bidang.** Tiap muka punya fungsi 3D (u, v) → titik di
   ruang objek: panel menggembung, gusset berlekuk dua lobus, pita segel
   bergelombang. Normal dihitung dari turunan fungsi itu (bukan dari gradien
   gambar), lalu diputar ke ruang kamera.
2. **Material.** Ambient studio + diffuse key + fill + rim + sheen kain + kilau
   dua lapis (pita softbox + titik sempit) + oklusi sudut. Semua numpy.
3. **Komposisi.** Latar putih murni untuk marketplace (tanpa bayangan — syarat
   Tokopedia/Shopee) atau kertas studio dengan bayangan kontak + pantulan lantai
   untuk halaman brand.

Batas (jujur, jangan diklaim lebih)
-----------------------------------
· Render dari label + geometri sendiri, **bukan pemotretan** kemasan fisik.
· Ukuran 135 × 260 mm dan stiker 120 × 170 mm dari pemilik (9 Nov 2026);
  ketebalan sisi, chamfer, dan warna bahan masih asumsi — lihat
  data/kemasan-katalog.json.
· Lipatan kertas tajam, jahitan, foil/spot-UV, dan jendela transparan tidak
  dimodelkan.

Pakai
-----
    python3 tools/foto.py                 # semua SKU
    python3 tools/foto.py --satu gayo     # satu SKU untuk menilai cahaya
    python3 tools/foto.py --cek           # periksa keluaran
"""

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import katalog as K                                    # noqa: E402

ROOT = K.ROOT
KELUAR = K.KELUAR
PASAR = K.PASAR
DATA = K.DATA
POUCH = os.path.join(ROOT, "assets", "img", "pouch")
STUDIO = os.path.join(ROOT, "assets", "img", "studio")
LEMBAR = K.LEMBAR

KATALOG = K.KATALOG
HERO = K.HERO
KUALITAS = K.KUALITAS
SUDUT = (0, -18, 40)
PITCH = -4.0
OBJEK = 0.76
S = 2


# ------------------------------------------------------------------ cahaya ---
def satuan(v):
    v = np.asarray(v, dtype=np.float64)
    return v / np.linalg.norm(v)


L_KEY = satuan((-0.40, -0.62, 0.67))       # softbox besar: kiri, atas, depan
L_FILL = satuan((0.74, 0.06, 0.67))        # pemantul kanan
L_WRAP = satuan((-0.95, 0.10, 0.30))       # lampu samping kiri, menyapu gusset
L_RIM = satuan((-0.30, 0.55, -0.78))       # rim dari belakang: memisahkan siluet
V = np.array([0.0, 0.0, 1.0])              # arah kamera


def lembut(rgb):
    """Bahu lembut di atas 0,84 — kertas putih jangan pecah jadi bidang rata."""
    x = np.clip(rgb, 0, None)
    return np.where(x < 0.84, x, 0.84 + 0.16 * (1.0 - np.exp(-(x - 0.84) / 0.16)))


def shade(n, albedo, oklusi, kekasaran=1.0, sheen=0.12):
    """Warna RGB float 0..1 dari normal kamera `n` (H, W, 3).

    Kalibrasi: permukaan yang menghadap kamera dengan albedo putih keluar
    ±0,84 (kertas studio), bukan 1,0 — supaya label tidak pecah putih rata.
    """
    n = n / np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-9)
    kunci = np.clip((n * L_KEY).sum(-1), 0, None)[..., None]
    isi = np.clip((n * L_FILL).sum(-1), 0, None)[..., None] * 0.18
    samping = np.clip((n * L_WRAP).sum(-1), 0, None)[..., None] ** 3.0 * 0.38
    rim = np.clip((n * L_RIM).sum(-1), 0, None)[..., None] ** 2.5 * 0.14
    atas = (n[..., 1] * -0.5 + 0.5)[..., None]
    ambient = 0.20 + 0.26 * atas
    rgb = albedo * (ambient + kunci * 0.60 + isi + samping + rim)

    # sheen kain: tepi yang memutar menjauh dari kamera menangkap cahaya
    cos_v = np.clip((n * V).sum(-1), 0, 1)
    tepi = (1.0 - cos_v) ** 4.0
    rgb = rgb + sheen * tepi[..., None] * np.array([1.0, 0.99, 0.96])

    # kilau: pita softbox lebar (dominan di bahan matte) + titik sempit
    h = satuan(L_KEY + V)
    d = np.clip((n * h).sum(-1), 0, None)
    # bahan matte: kilau lemah dan menyempit, jangan sampai hitam jadi kelabu
    kilau = (d ** (5.0 / kekasaran) * 0.10 + d ** (48.0 / kekasaran) * 0.10)[..., None]
    rgb = rgb + kilau * np.array([1.0, 0.995, 0.98])

    return lembut(rgb * oklusi[..., None])


# ---------------------------------------------------------------- geometri ---
def spek(g: dict | None = None) -> dict:
    sp = K.spek()
    u = sp["aktif"]
    W, H = float(u["lebar"]), float(u["tinggi"])
    D = float(u["gusset"])
    return {
        "sp": sp, "W": W, "H": H, "D": D,
        "sisi": float(u.get("sisi") or D / 2),
        "c": float(u.get("chamfer") or 10.0),
        "segel": float(u["segel"]),
        "zipper": float(u["zipper"]),
        "stiker": sp.get("stiker") or {},
        "valve": sp.get("valve") or {},
        "bahan": sp.get("bahan") or {},
    }


def permukaan(g: dict, muka: str):
    """Fungsi 3D (u, v) → titik ruang objek, **vektor** (bisa menerima array).

    Lengkung panel dan lekuk gusset dikerjakan di sini, jadi normal yang
    dihitung dari fungsi ini benar-benar melengkung — bukan gradien gambar.
    """
    W, H, c = g["W"], g["H"], g["c"]

    def titik(u, v):
        u = np.asarray(u, dtype=np.float64)
        v = np.asarray(v, dtype=np.float64)
        y = v * H
        a = np.clip((y - g["segel"]) / (H * 0.30), 0.0, 1.0)
        halus = a * a * (3 - 2 * a)
        # flat-bottom: lebar & kedalaman hampir tetap; hanya 6–14% menyempit
        # di bawah zipper. Penyempitan besar membuat pouch terbaca limas.
        hw = W / 2 * (0.94 + 0.06 * halus) * (1.0 + 0.02 * np.clip((y - H * 0.88) / (H * 0.12), 0, 1))
        hw = hw * np.where(y < g["segel"], 0.975, 1.0)
        d = g["D"] / 2 * (0.86 + 0.14 * halus)

        if muka in ("depan", "belakang"):
            x = (u - 0.5) * 2 * hw
            gembung = (1.0 - np.clip(np.abs(2 * u - 1), 0, 1) ** 2.2) ** 0.45
            isi = 0.78 + 0.22 * np.clip((v - 0.03) / 0.26, 0, 1)
            z = d + 0.105 * W * gembung * isi
            if muka == "belakang":
                z = -z
            return np.stack([x, y, z], axis=-1)
        if muka in ("sisi_kiri", "sisi_kanan"):
            tanda = -1.0 if muka == "sisi_kiri" else 1.0
            z = d - 2 * d * u
            # dinding samping nyaris rata; hanya menggembung 3 mm di lipatan
            lobus = np.abs(np.sin(np.pi * u)) ** 1.2
            x = tanda * (hw + 0.022 * W * lobus)
            return np.stack([x, y, z], axis=-1)
        if muka in ("chamfer_depan_kiri", "chamfer_depan_kanan"):
            tanda = -1.0 if muka.endswith("kiri") else 1.0
            x = tanda * (hw - c * (1 - u))
            z = d - c * u
            return np.stack([x, y, z], axis=-1)
        if muka in ("chamfer_belakang_kiri", "chamfer_belakang_kanan"):
            tanda = -1.0 if muka.endswith("kiri") else 1.0
            x = tanda * (hw - c * u)
            z = -d + c * (1 - u)
            return np.stack([x, y, z], axis=-1)
        if muka == "segel":
            # Flens atas: bidang y≈0, melengkung 1,6 mm. Di sini u = kedalaman
            # dan v = lebar, jadi lebar/kedalaman harus dihitung ulang dari
            # y=0 (v*H bukan tinggi — itu sebabnya flens sempat melebar keliru).
            hw0 = W / 2 * 0.94 * 0.975
            d0 = g["D"] / 2 * 0.86
            y0 = -0.012 * W * np.sin(np.pi * u) * np.sin(np.pi * v)
            return np.stack([(v - 0.5) * 2 * hw0, y0, d0 - 2 * d0 * u], axis=-1)
        raise ValueError(muka)

    return titik


# Chamfer tidak digambar: saat muka hampir sejajar kamera, segi empatnya
# menyilang dan topengnya melebar jadi baji hitam (terlihat di uji 62°).
# Siluet panel + dua sisi sudah membaca sebagai pouch; sudut chamfer tetap ada
# di geometri (dipakai menghitung lebar), hanya tidak jadi muka terpisah.
MUKA_URUT = ["belakang", "chamfer_belakang_kiri", "chamfer_belakang_kanan",
             "sisi_kiri", "sisi_kanan",
             "chamfer_depan_kiri", "chamfer_depan_kanan", "depan", "segel"]


def normal_piksel(titik, u: np.ndarray, v: np.ndarray,
                  keluar: np.ndarray) -> np.ndarray:
    """Normal per piksel dari turunan fungsi permukaan, dijamin menghadap keluar."""
    e = 1e-3
    P = titik(u, v)
    du = (titik(np.minimum(u + e, 1.0), v) - titik(np.maximum(u - e, 0.0), v))
    dv = (titik(u, np.minimum(v + e, 1.0)) - titik(u, np.maximum(v - e, 0.0)))
    n = np.cross(du, dv)
    panjang = np.linalg.norm(n, axis=-1, keepdims=True)
    n = n / np.maximum(panjang, 1e-12)
    arah = np.sum(n * keluar, axis=-1, keepdims=True)
    n = np.where(arah < 0, -n, n)
    return n


def rotasi(yaw: float, pitch: float):
    """Putar vektor ruang objek ke ruang kamera (kamera di +z), bisa vektor."""
    a, b = math.radians(yaw), math.radians(pitch)
    ca, sa, cb, sb = math.cos(a), math.sin(a), math.cos(b), math.sin(b)
    # x'=x·ca + z·sa ; y'=y·cb + x·sa·sb − z·ca·sb ; z'=−x·sa·cb + y·sb + z·ca·cb
    M = np.array([[ca, 0.0, sa],
                  [sa * sb, cb, -ca * sb],
                  [-sa * cb, sb, ca * cb]])

    def f(v):
        return np.asarray(v, dtype=np.float64) @ M.T

    return f


def kamera(yaw: float, pitch: float, tinggi_mm: float, tinggi_px: float):
    """Proyeksi perspektif: mm → piksel, jarak kamera 3,4 × tinggi objek."""
    f = rotasi(yaw, pitch)
    jarak = tinggi_mm * 3.4
    skala = tinggi_px / tinggi_mm

    def p(v3):
        q = f(v3)
        k = jarak / np.maximum(1.0, jarak - q[..., 2])
        return np.stack([q[..., 0] * k * skala, q[..., 1] * k * skala], axis=-1)

    return f, p


# ------------------------------------------------------------------ tekstur ---
def warna_bahan(g: dict) -> np.ndarray:
    return np.array(K.hex_rgb((g["bahan"] or {}).get("warna") or "#1B1A18"),
                    dtype=np.float64) / 255.0


def tenun(w: int, h: int, kekuatan: float = 0.045) -> np.ndarray:
    """Derau kain halus — garis berjarak tetap terbaca sebagai karung."""
    rng = np.random.default_rng(7)
    b = rng.normal(0, 1, (h, w))
    b = np.asarray(Image.fromarray(((b * 0.5 + 0.5) * 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(0.7)), dtype=np.float64) / 255.0
    return 1.0 + (b - 0.5) * kekuatan


def valve(albedo: np.ndarray, g: dict, w: int, h: int) -> np.ndarray:
    """Valve satu arah: lubang gelap, kubah silikon, bayangan kontak.

    Kubah dibuat radial (terang di tengah, gelap di tepi) supaya tetap terbaca
    tiga dimensi dari sisi mana pun — tekstur muka belakang tercermin saat
    kamera di 180°, jadi arah terang mutlak tidak bisa dipaku di sini.
    """
    v = g["valve"]
    if not v.get("ada"):
        return albedo
    cx = float(v.get("x", 0.5)) * w
    cy = float(v.get("y_dari_atas", 52)) / g["H"] * h
    r = max(6.0, w * float(v.get("diameter", 15)) / g["W"] / 2)

    yy, xx = np.mgrid[0:h, 0:w]
    dx, dy = (xx - cx) / r, (yy - cy) / r
    d = np.sqrt(dx ** 2 + dy ** 2)

    # bayangan kontak: valve menonjol, jadi ada cincin gelap di sekelilingnya
    kontak = np.exp(-((d - 1.02) / 0.22) ** 2)
    albedo *= (1.0 - 0.42 * kontak)[..., None]

    # dudukan (flange) gelap: plastik hitam rata dengan bahan
    dudukan = (d >= 0.92) & (d < 1.06)
    albedo[dudukan] = albedo[dudukan] * 0.55

    # kubah silikon: terang di tengah, gelap di tepi, dipotong bayangan bawah
    dalam = d < 0.92
    kubah = np.sqrt(np.clip(1 - (np.clip(d, 0, 1) / 0.92) ** 2, 0, 1))
    terang = 0.52 + 0.40 * kubah - 0.10 * np.clip(dy, 0, 1)
    warna = terang[..., None] * np.array([1.0, 0.995, 0.985])
    # celah tipis di tepi kubah (bayangan dudukan)
    celah = (d >= 0.84) & (d < 0.92)
    warna[celah] *= 0.55
    albedo[dalam] = warna[dalam]
    return albedo


def tekstur_panel(g: dict, lbl: Image.Image | None, w: int, h: int,
                  stiker: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Albedo + oklusi + peta kertas untuk satu panel (stiker atau muka valve)."""
    albedo = np.zeros((h, w, 3)) + warna_bahan(g)
    albedo *= tenun(w, h)[..., None]
    kertas = np.zeros((h, w))

    if stiker and lbl is not None:
        st = g["stiker"]
        sw, sh = float(st.get("lebar", 120)), float(st.get("tinggi", 170))
        cx, cy = float(st.get("x", 0.5)) * g["W"], float(st.get("y", 0.5)) * g["H"]
        x0 = int(round((cx - sw / 2) / g["W"] * w))
        x1 = int(round((cx + sw / 2) / g["W"] * w))
        y0 = int(round((cy - sh / 2) / g["H"] * h))
        y1 = int(round((cy + sh / 2) / g["H"] * h))
        x0, x1 = max(0, x0), min(w, x1)
        y0, y1 = max(0, y0), min(h, y1)
        if x1 - x0 > 6 and y1 - y0 > 6:
            teks = np.asarray(lbl.convert("RGB").resize(
                (x1 - x0, y1 - y0), Image.LANCZOS), dtype=np.float64) / 255.0
            albedo[y0:y1, x0:x1] = teks
            kertas[y0:y1, x0:x1] = 1.0
            # tepi kertas: sisi atas/kiri menangkap cahaya, bawah/kanan gelap
            albedo[y0:y0 + 2, x0:x1] = np.clip(albedo[y0:y0 + 2, x0:x1] * 1.06, 0, 1)
            albedo[y0:y1, x0:x0 + 2] = np.clip(albedo[y0:y1, x0:x0 + 2] * 1.04, 0, 1)
            albedo[y1 - 2:y1, x0:x1] *= 0.80
            albedo[y0:y1, x1 - 2:x1] *= 0.84

            # bayangan tempelan: stiker setebal ±0,2 mm memblokir cahaya dari
            # kiri-atas, jadi bayangan jatuh ke kanan-bawah lalu mengabur
            topeng = np.zeros((h, w))
            topeng[y0:y1, x0:x1] = 1.0
            geser = np.roll(np.roll(topeng, max(1, round(h * 0.0028)), axis=0),
                            max(1, round(w * 0.0022)), axis=1)
            bayang = Image.fromarray((geser * 255).astype(np.uint8)).filter(
                ImageFilter.GaussianBlur(max(1.2, h / 520)))
            bayang = np.asarray(bayang, dtype=np.float64) / 255.0
            albedo *= (1.0 - 0.42 * bayang * (1.0 - topeng))[..., None]
    elif not stiker:
        albedo = valve(albedo, g, w, h)

    u = (np.arange(w) + 0.5) / w
    v = (np.arange(h) + 0.5) / h

    # pita segel atas: crimp bergerigi, tepi atas menangkap cahaya, dan
    # garis gelap di bawahnya — inilah yang membaca "pouch kopi", bukan folder
    v_segel = g["segel"] / g["H"]
    pita = (v < v_segel * 0.92)[:, None, None]
    jarak = max(2.0, g["segel"] * 0.45)
    gerigi = (0.5 + 0.5 * np.cos(2 * math.pi * u * (g["W"] / jarak)))[None, :, None]
    albedo = np.where(pita, np.clip(albedo * (0.72 + 0.62 * gerigi), 0, 1), albedo)
    tepi_atas = np.exp(-((v - v_segel * 0.06) / (v_segel * 0.10)) ** 2)[:, None, None]
    albedo = np.clip(albedo + 0.35 * tepi_atas, 0, 1)
    garis_segel = np.exp(-((v - v_segel * 0.97) / 0.006) ** 2)[:, None, None]
    albedo *= (1.0 - 0.60 * garis_segel)

    # dasar: jahitan bawah (flat-bottom) — garis terang di atas, gelap di bawah
    dasar = np.exp(-((v - 0.905) / 0.008) ** 2)[:, None, None]
    albedo = np.clip(albedo * (1.0 + 0.30 * dasar), 0, 1)
    lipat_dasar = np.exp(-((v - 0.930) / 0.006) ** 2)[:, None, None]
    albedo *= (1.0 - 0.45 * lipat_dasar)

    # jahitan bahu: garis gelap tipis tepat di bawah pita segel, melintang penuh
    bahu = (g["segel"] * 1.25 + g["zipper"] * 0.55) / g["H"]
    garis = np.exp(-((v - bahu) / 0.010) ** 2)[:, None, None]
    albedo *= (1.0 - 0.30 * garis)
    # lipatan dasar: garis terang tipis di atas dasar panel
    dasar_garis = np.exp(-((v - 0.935) / 0.010) ** 2)[:, None, None]
    albedo *= (1.0 + 0.22 * dasar_garis)
    tepi = np.clip((np.abs(2 * u - 1) - 0.94) / 0.06, 0, 1)[None, :] ** 1.5
    bawah = np.clip((v - 0.80) / 0.20, 0, 1)[:, None] ** 1.6
    okl = (1.0 - 0.34 * tepi) * (1.0 - 0.24 * bawah)
    okl = np.broadcast_to(okl, (h, w)).copy()
    for x in (0, 1, w - 2, w - 1):
        albedo[:, x] *= 0.74
    return albedo, okl, kertas


def tekstur_segel(g: dict, w: int, h: int) -> tuple[np.ndarray, np.ndarray]:
    """Flens segel: x = lebar, y = kedalaman. Gerigi berjalan dari depan ke
    belakang, menangkap key light karena muka ini menghadap ke atas."""
    albedo = np.zeros((h, w, 3)) + warna_bahan(g) * 1.45
    u = (np.arange(w) + 0.5) / w
    jarak = max(2.0, float((g["sp"].get("segel") or {}).get("gerigi", 7)))
    gerigi = 0.5 + 0.5 * np.cos(2 * math.pi * u * (g["W"] / jarak))
    albedo *= (0.86 + 0.30 * gerigi)[None, :, None]
    albedo *= tenun(w, h, 0.03)[..., None]
    v = (np.arange(h) + 0.5) / h
    okl = np.broadcast_to((1.02 - 0.22 * np.abs(v - 0.5) * 2)[:, None], (h, w)).copy()
    return albedo, okl


def tekstur_sisi(g: dict, w: int, h: int, kiri: bool,
                 lekuk: float = 0.40) -> tuple[np.ndarray, np.ndarray]:
    albedo = np.zeros((h, w, 3)) + warna_bahan(g)
    albedo *= tenun(w, h, 0.05)[..., None]
    u = (np.arange(w) + 0.5) / w
    lipat = np.exp(-((u - 0.5) / 0.06) ** 2)[None, :]
    tepi = (np.clip((np.abs(2 * u - 1) - 0.88) / 0.12, 0, 1) ** 1.4)[None, :]
    okl = (1.0 - lekuk * lipat) * (1.0 - 0.20 * tepi)
    okl = np.broadcast_to(okl, (h, w)).copy()
    okl *= (1.0 - 0.20 * np.clip((np.arange(h) / h - 0.75) / 0.25, 0, 1))[:, None]
    if not kiri:
        albedo *= 0.92
    return albedo, okl


def render(g: dict, lbl: Image.Image | None, tinggi_px: int, yaw: float,
           pitch: float = PITCH) -> Image.Image:
    """Render pouch ke kanvas RGBA transparan; tinggi objek = tinggi_px."""
    h_px = tinggi_px * S
    w_px = round(h_px * g["W"] / g["H"])
    f, p = kamera(yaw, pitch, g["H"], h_px)

    # siluet semua muka → kotak kanvas
    sil = []
    for nama in MUKA_URUT:
        titik = permukaan(g, nama)
        for u in (0.0, 0.5, 1.0):
            for v in (0.0, 0.5, 1.0):
                sil.append(p(titik(u, v)))
    xs = [q[0] for q in sil]
    ys = [q[1] for q in sil]
    pad = 5 * S
    x0, x1 = min(xs) - pad, max(xs) + pad
    y0, y1 = min(ys) - pad, max(ys) + pad
    W, H = int(math.ceil(x1 - x0)), int(math.ceil(y1 - y0))
    kanvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    def tempel(rgb: np.ndarray, quad):
        """Tempel tekstur ke segi empat hasil proyeksi.

        Ring geometri bisa berlawanan arah (muka kiri: u membesar ke kiri),
        jadi topeng digambar dari titik yang diurutkan mengelilingi pusat —
        bukan dari urutan homografi. Kalau tidak, poligon menyilang sendiri
        dan PIL mengisinya sebagai dua baji (bug "segitiga hitam").
        """
        img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
        lt, rt, rb, lb = [(q[0] - x0, q[1] - y0) for q in quad]
        koef = K.homografi([(0, 0), (img.width, 0), (img.width, img.height),
                            (0, img.height)], [lt, rt, rb, lb])
        lapis = img.transform((W, H), Image.PERSPECTIVE, koef, Image.BICUBIC)

        cx = sum(q[0] for q in (lt, rt, rb, lb)) / 4
        cy = sum(q[1] for q in (lt, rt, rb, lb)) / 4
        ring = sorted((lt, rt, rb, lb), key=lambda q: math.atan2(q[1] - cy, q[0] - cx))
        S2 = 4
        besar = Image.new("L", (W * S2, H * S2), 0)
        ImageDraw.Draw(besar).polygon([(q[0] * S2, q[1] * S2) for q in ring], fill=255)
        topeng = besar.resize((W, H), Image.LANCZOS)
        kanvas.paste(lapis.convert("RGBA"), (0, 0), topeng)

    muka = []
    for nama in MUKA_URUT:
        titik = permukaan(g, nama)
        n_rata = normal_piksel(titik, np.array(0.5), np.array(0.5),
                               np.array([0.0, 0.0, 1.0 if "depan" in nama else -1.0
                                         if "belakang" in nama else
                                         0.0])) if False else None
        # uji tampak: normal di tengah muka, diputar ke kamera
        titik0 = permukaan(g, nama)
        keluar = keluar_muka(nama)
        n3 = normal_piksel(titik0, np.array(0.5), np.array(0.5), np.array(keluar))
        if float(f(n3)[2]) <= 0.015:
            continue
        zc = float(f(titik0(0.5, 0.5))[2])
        muka.append((zc, nama, titik0, keluar))

    for _, nama, titik, keluar in sorted(muka):
        if nama == "segel":
            tw = max(16, round(w_px * 1.1))
            th = max(12, round(w_px * 1.1 * g["D"] / g["W"]))
            albedo, okl = tekstur_segel(g, tw, th)
            uu = (np.arange(tw) + 0.5) / tw
            vv = (np.arange(th) + 0.5) / th
            UU, VV = np.meshgrid(uu, vv)
            # tekstur x = lebar (v), y = kedalaman (u)
            n3 = normal_piksel(titik, VV, UU, np.array(keluar))
            f_rot = f(n3)
            rgb = shade(f_rot, albedo, okl, kekasaran=1.6)
            quad = [p(titik(0.0, 0.0)), p(titik(0.0, 1.0)),
                    p(titik(1.0, 1.0)), p(titik(1.0, 0.0))]
            tempel(rgb, quad)
            continue
        if nama in ("depan", "belakang"):
            tw = round(w_px * 1.1)
            th = round(tw * g["H"] / g["W"])
            albedo, okl, _ = tekstur_panel(g, lbl, tw, th, nama == "depan")
        elif nama.startswith("sisi"):
            tw = max(12, round(w_px * 1.1 * g["D"] / g["W"]))
            th = round(tw * g["H"] / g["D"])
            albedo, okl = tekstur_sisi(g, tw, th, nama.endswith("kiri"))
        else:
            # chamfer: strip sempit, hanya bahan + lekuk membulat di tengah
            tw = max(10, round(w_px * 1.1 * min(g["c"], 6.0) / g["W"]))
            th = round(tw * g["H"] / min(g["c"], 6.0))
            albedo, okl = tekstur_sisi(g, tw, th, nama.endswith("kiri"), lekuk=0.10)
            albedo *= 0.80

        uu = (np.arange(tw) + 0.5) / tw
        vv = (np.arange(th) + 0.5) / th
        UU, VV = np.meshgrid(uu, vv)
        n3 = normal_piksel(titik, UU, VV, np.array(keluar))
        f_rot = f(n3)
        rgb = shade(f_rot, albedo, okl, kekasaran=1.2)
        quad = [p(titik(0.0, 0.0)), p(titik(1.0, 0.0)),
                p(titik(1.0, 1.0)), p(titik(0.0, 1.0))]
        tempel(rgb, quad)

    kanvas = kanvas.resize((max(1, W // S), max(1, H // S)), Image.LANCZOS)
    return kanvas


def keluar_muka(nama: str) -> tuple[float, float, float]:
    """Arah "keluar" tiap muka, dipakai untuk memastikan normal tidak terbalik."""
    if nama == "depan":
        return (0.0, 0.0, 1.0)
    if nama == "belakang":
        return (0.0, 0.0, -1.0)
    if nama == "segel":
        return (0.0, -1.0, 0.0)
    if nama == "sisi_kanan":
        return (1.0, 0.0, 0.0)
    if nama == "sisi_kiri":
        return (-1.0, 0.0, 0.0)
    if nama == "chamfer_depan_kanan":
        return (0.62, 0.0, 0.78)
    if nama == "chamfer_depan_kiri":
        return (-0.62, 0.0, 0.78)
    if nama == "chamfer_belakang_kanan":
        return (0.62, 0.0, -0.78)
    return (-0.62, 0.0, -0.78)


def potong(im: Image.Image) -> Image.Image:
    bb = im.split()[3].getbbox()
    return im.crop(bb) if bb else im


# ---------------------------------------------------------------- komposisi ---
def latar_kertas(ukuran: tuple[int, int]) -> np.ndarray:
    W, H = ukuran
    y, x = np.mgrid[0:H, 0:W]
    u, v = x / W, y / H
    dasar = 0.975 - 0.030 * ((u - 0.5) * 2) ** 2 - 0.045 * v ** 2.0
    rgb = np.stack([dasar, dasar * 0.998, dasar * 0.990], -1)
    return np.clip(rgb, 0, 1)


def tempatkan(latar, obj: Image.Image, skala: float, cx: float, dasar_y: float,
              bayangan: bool = True, pantulan: bool = False):
    H, W = latar.shape[:2]
    th = round(H * skala)
    tw = round(obj.width * th / obj.height)
    o = obj.resize((tw, th), Image.LANCZOS)
    x = round(W * cx - tw / 2)
    y = round(H * dasar_y - th)
    kanvas = latar.copy()

    if bayangan:
        def topeng(ellipse, blur, isi):
            sh = Image.new("L", (W, H), 0)
            ImageDraw.Draw(sh).ellipse(ellipse, fill=isi)
            return np.asarray(sh.filter(ImageFilter.GaussianBlur(blur)),
                              dtype=np.float64) / 255.0

        kontak = topeng([x - tw * 0.08, y + th - th * 0.015,
                         x + tw * 1.10, y + th + th * 0.055],
                        max(5, th // 34), 220)
        lebar = topeng([x - tw * 0.30, y + th - th * 0.02,
                        x + tw * 1.36, y + th + th * 0.16],
                       max(10, th // 12), 80)
        kanvas *= (1.0 - 0.55 * kontak[..., None])
        kanvas *= (1.0 - 0.26 * lebar[..., None])

    if pantulan:
        refl = o.transpose(Image.FLIP_TOP_BOTTOM).copy()
        fade = Image.new("L", (tw, th))
        dr = ImageDraw.Draw(fade)
        for i in range(th):
            dr.line([(0, i), (tw, i)], fill=int(56 * max(0.0, 1 - i / (th * 0.5))))
        refl.putalpha(Image.composite(fade, Image.new("L", (tw, th), 0), refl.split()[3]))
        lapis = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lapis.paste(refl, (x, y + th))
        arr = np.asarray(lapis, dtype=np.float64) / 255.0
        a = arr[..., 3:4]
        kanvas = kanvas * (1 - a) + arr[..., :3] * a

    lapis = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lapis.paste(o, (x, y), o)
    arr = np.asarray(lapis, dtype=np.float64) / 255.0
    a = arr[..., 3:4]
    return np.clip(kanvas * (1 - a) + arr[..., :3] * a, 0, 1), (x, y, x + tw, y + th)


def foto(g: dict, lbl: Image.Image | None, yaw: float, ukuran: tuple[int, int],
         skala: float, latar: str, cx: float = 0.5,
         dasar: float = 0.90) -> tuple[Image.Image, list[int]]:
    """Satu foto + kotak objek (x0, y0, x1, y1) untuk penempatan di halaman."""
    obj = potong(render(g, lbl, round(ukuran[1] * skala * 1.15), yaw))
    if latar == "putih":
        kanvas = np.ones((ukuran[1], ukuran[0], 3))
        rgb, kotak = tempatkan(kanvas, obj, skala, cx, dasar, bayangan=False)
    else:
        rgb, kotak = tempatkan(latar_kertas(ukuran), obj, skala, cx, dasar,
                               bayangan=True, pantulan=True)
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)), list(kotak)


# ------------------------------------------------------------------ keluaran ---
def render_sku(p: dict, sp: dict) -> dict:
    g = spek(sp)
    lbl = K.label(p["id"])
    if lbl is None:
        return {"id": p["id"], "status": "tanpa label"}
    for folder in (KELUAR, PASAR, POUCH, STUDIO):
        os.makedirs(folder, exist_ok=True)

    keluaran = {}
    tinggi_px = 0
    for sudut in SUDUT:
        im, kotak = foto(g, lbl, sudut, (KATALOG, KATALOG), OBJEK, "studio")
        nama = f'{p["id"]}-{abs(sudut)}.jpg'
        im.save(os.path.join(KELUAR, nama), "JPEG", quality=KUALITAS,
                optimize=True, progressive=True)
        tinggi_px = max(tinggi_px, kotak[3] - kotak[1])
        keluaran[abs(sudut)] = {"berkas": f"assets/img/katalog/{nama}",
                                "kb": round(os.path.getsize(os.path.join(KELUAR, nama)) / 1024, 1),
                                "kotak": kotak}

    im, kotak = foto(g, lbl, -14, HERO, 0.80, "studio", cx=0.68, dasar=0.92)
    nama_hero = f'{p["id"]}-hero.jpg'
    im.save(os.path.join(KELUAR, nama_hero), "JPEG", quality=KUALITAS,
            optimize=True, progressive=True)
    keluaran["hero"] = {"berkas": f"assets/img/katalog/{nama_hero}",
                        "kb": round(os.path.getsize(os.path.join(KELUAR, nama_hero)) / 1024, 1),
                        "kotak": kotak}

    pasar_keluar = {}
    for kunci, uk, skala in (("1x1", (1000, 1000), 0.80), ("4x5", (1080, 1350), 0.72)):
        im, kotak = foto(g, lbl, 0, uk, skala, "putih", dasar=0.90)
        nama = f'{p["id"]}-{kunci}.jpg'
        im.save(os.path.join(PASAR, nama), "JPEG", quality=KUALITAS,
                optimize=True, progressive=True)
        pasar_keluar[kunci] = {"berkas": f"assets/img/katalog/pasar/{nama}",
                               "kb": round(os.path.getsize(os.path.join(PASAR, nama)) / 1024, 1),
                               "ukuran": list(uk), "kotak": kotak}

    studio_keluar = {}
    for nama, yaw, skala, latar in (("depan", 0, 0.84, "putih"),
                                    ("tiga-perempat", -25, 0.82, "studio"),
                                    ("valve", 180, 0.84, "putih"),
                                    ("sisi", 45, 0.80, "putih")):
        im, _ = foto(g, lbl, yaw, (2000, 2000), skala, latar)
        nama_f = f'{p["id"]}-{nama}.jpg'
        im.save(os.path.join(STUDIO, nama_f), "JPEG", quality=KUALITAS,
                optimize=True, progressive=True)
        studio_keluar[nama] = {"berkas": f"assets/img/studio/{nama_f}",
                               "kb": round(os.path.getsize(os.path.join(STUDIO, nama_f)) / 1024, 1)}

    muka_rak(g, lbl, p["id"], "muka").save(os.path.join(POUCH, f'{p["id"]}-muka.png'),
                                           optimize=True)
    muka_rak(g, lbl, p["id"], "sisi").save(os.path.join(POUCH, f'{p["id"]}-sisi.png'),
                                           optimize=True)

    u = sp["aktif"]
    return {"id": p["id"], "nama": p["name"], "status": "siap",
            "ukuran": u["kunci"], "bentuk": u.get("bentuk", "flat-bottom"),
            "geometri": {k: u[k] for k in ("lebar", "tinggi", "gusset", "segel", "zipper")},
            "sisi": u.get("sisi"), "bahan": (sp.get("bahan") or {}).get("nama"),
            "stiker": sp.get("stiker"), "valve": sp.get("valve"),
            "tinggi_objek_px": tinggi_px,
            "keluaran": keluaran, "pasar": pasar_keluar, "studio": studio_keluar,
            "pouch": {"muka": {"berkas": f'assets/img/pouch/{p["id"]}-muka.png'},
                      "sisi": {"berkas": f'assets/img/pouch/{p["id"]}-sisi.png'},
                      "valve": {"berkas": f"assets/img/studio/{p['id']}-valve.jpg"}}}


def muka_rak(g: dict, lbl: Image.Image | None, id_: str, jenis: str) -> Image.Image:
    """Muka datar transparan untuk rak (CSS): panel stiker atau dinding sisi.

    Normal dipakai apa adanya (kamera hadap depan) — gambar ini ditempel di
    DOM, bukan diproyeksikan, jadi tidak perlu rotasi kamera.
    """
    if jenis == "muka":
        w = 900
        h = round(w * g["H"] / g["W"])
        albedo, okl, _ = tekstur_panel(g, lbl, w, h, True)
        titik, keluar = permukaan(g, "depan"), np.array([0.0, 0.0, 1.0])
    else:
        w = 320
        h = round(w * g["H"] / g["D"])
        albedo, okl = tekstur_sisi(g, w, h, False)
        titik, keluar = permukaan(g, "sisi_kanan"), np.array([1.0, 0.0, 0.0])
    uu = (np.arange(w) + 0.5) / w
    vv = (np.arange(h) + 0.5) / h
    UU, VV = np.meshgrid(uu, vv)
    n3 = normal_piksel(titik, UU, VV, keluar)
    rgb = shade(n3, albedo, okl)
    return Image.fromarray((rgb * 255).astype(np.uint8)).convert("RGBA")


def banding(hasil: list[dict]) -> None:
    ikon, kepala, kaki = 300, 58, 26
    baris = [h for h in hasil if h["status"] == "siap"]
    W = ikon * 4 + 40
    H = kepala + (ikon + kaki) * len(baris) + 20
    lembar = Image.new("RGB", (W, H), (237, 235, 230))
    d = ImageDraw.Draw(lembar)
    try:
        from PIL import ImageFont
        f_k = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-600-normal.ttf"), 15)
        f_j = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-500-normal.ttf"), 13)
    except OSError:
        f_k = f_j = ImageFont.load_default()
    d.text((20, 20), "FOTO 3D E-COMMERCE — DEPAN · TIGA PEREMPAT · VALVE · SISI",
           font=f_k, fill=(20, 20, 20))
    d.text((W - 200, 22), "tools/foto.py", font=f_j, fill=(109, 106, 99))
    for i, h in enumerate(baris):
        y = kepala + i * (ikon + kaki)
        d.text((20, y + 4), h["nama"].upper(), font=f_k, fill=(20, 20, 20))
        for j, kunci in enumerate(("depan", "tiga-perempat", "valve", "sisi")):
            e = h["studio"][kunci]
            im = Image.open(os.path.join(ROOT, e["berkas"]))
            im.thumbnail((ikon - 14, ikon - 14), Image.LANCZOS)
            x = 20 + j * ikon
            lembar.paste(im, (x, y + kaki))
            d.rectangle([x, y + kaki, x + ikon - 8, y + kaki + ikon - 8],
                        outline=(222, 218, 210))
        d.line([20, y + ikon + kaki + 6, W - 20, y + ikon + kaki + 6], fill=(222, 218, 210))
    lembar.save(LEMBAR, optimize=True)


def cek() -> list[str]:
    m: list[str] = []
    if not os.path.exists(DATA):
        return ["data/katalog-render.json belum ada — jalankan python3 tools/foto.py"]
    with open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    siap = [s for s in d["sku"] if s["status"] == "siap"]
    if len(siap) != 9:
        m.append(f"{len(siap)} SKU dirender, seharusnya 9")
    sp = K.spek()
    u = sp["aktif"]
    for s in siap:
        g_ = s.get("geometri") or {}
        if g_.get("lebar") != u["lebar"] or g_.get("tinggi") != u["tinggi"]:
            m.append(f'{s["id"]}: geometri {g_} ≠ spesifikasi {u["lebar"]}×{u["tinggi"]}')
        for bagian in ("keluaran", "pasar", "studio"):
            for kunci, e in (s.get(bagian) or {}).items():
                jalur = os.path.join(ROOT, e["berkas"])
                if not os.path.exists(jalur):
                    m.append(f'{s["id"]} {bagian}/{kunci}: berkas tidak ada')
                    continue
                with Image.open(jalur) as im:
                    if bagian == "keluaran" and kunci != "hero" and im.size != (KATALOG, KATALOG):
                        m.append(f'{s["id"]} {kunci}: ukuran {im.size}')
                    if bagian == "pasar" and kunci == "1x1" and im.size != (1000, 1000):
                        m.append(f'{s["id"]} pasar 1x1: ukuran {im.size}')
                    if bagian == "studio" and im.size != (2000, 2000):
                        m.append(f'{s["id"]} studio {kunci}: ukuran {im.size}')
                    # hanya foto yang memang berlatar putih murni yang diuji
                    putih = bagian == "pasar" or (bagian == "studio"
                                                 and kunci != "tiga-perempat")
                    if putih:
                        for titik in ((0, 0), (im.width - 1, 0), (0, im.height - 1),
                                      (im.width - 1, im.height - 1)):
                            if min(im.convert("RGB").getpixel(titik)) < 248:
                                m.append(f'{s["id"]} {bagian}/{kunci}: sudut bukan putih bersih')
                                break
                if os.path.getsize(jalur) > 900_000:
                    m.append(f'{s["id"]} {bagian}/{kunci}: {os.path.getsize(jalur)/1024:.0f} KB berat')
        for jenis in ("muka", "sisi"):
            if not os.path.exists(os.path.join(POUCH, f'{s["id"]}-{jenis}.png')):
                m.append(f'{s["id"]}: muka rak {jenis} tidak ada')
    if not os.path.exists(LEMBAR):
        m.append("laporan/katalog-render.png belum ada")
    return m


if __name__ == "__main__":
    if "--cek" in sys.argv:
        mm = cek()
        for x in mm:
            print("  ✗", x)
        print("  kesimpulan:", "OK · 9 SKU foto e-commerce 2000 px"
              if not mm else f"{len(mm)} masalah")
        sys.exit(0 if not mm else 1)

    sp = K.spek()
    u = sp["aktif"]
    print(f'  kemasan  {u.get("berat")} · {u["lebar"]}×{u["tinggi"]} mm · '
          f'sisi {u.get("sisi")} · segel {u["segel"]} · zipper {u["zipper"]} · '
          f'stiker {(sp.get("stiker") or {}).get("lebar")}×'
          f'{(sp.get("stiker") or {}).get("tinggi")} mm')
    produk = K.baca_catalog()
    if "--satu" in sys.argv:
        kriteria = sys.argv[sys.argv.index("--satu") + 1]
        produk = [p for p in produk if p["id"] == kriteria]
    hasil = [render_sku(p, sp) for p in produk]
    K.tulis_data(hasil)
    K.tulis_js(hasil)
    banding(hasil)
    total = sum(e["kb"] for s in hasil if s["status"] == "siap"
                for bagian in ("keluaran", "pasar", "studio")
                for e in (s.get(bagian) or {}).values())
    print(f'  foto     {len([h for h in hasil if h["status"] == "siap"])} SKU · '
          f'3 sudut + hero + 2 pasar + 4 studio · {total/1024:.1f} MB')
    for x in cek():
        print("  ✗", x)
