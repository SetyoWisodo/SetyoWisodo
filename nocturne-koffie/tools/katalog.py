#!/usr/bin/env python3
"""Foto katalog & hero landing page — dirender deterministik dari label sendiri.

Kenapa ada berkas ini
---------------------
Foto katalog dan gambar hero biasanya datang dari render 3D (Blender + GPU) atau
dari generator gambar. Di sandbox ini tidak ada keduanya, dan sejak 5 Nov pemilik
menolak hasil generator gambar. Yang bisa dilakukan tanpa keduanya: menyusun
**rig studio** yang sama untuk semua SKU dan merendernya dari label vektor yang
sudah ada — sudut, arah cahaya, bayangan, dan latar identik, sehingga 9 foto
terlihat seperti satu sesi pemotretan, bukan sembilan gambar berbeda.

Resepnya (aturan yang sama dipakai skill `katalog-render`):

    · rig tetap: key light kiri-atas 45°, fill kanan 25%, rim kanan-atas tipis
    · latar kertas brand, gradasi vertikal, tanpa tekstur yang menipu
    · objek berdiri di lantai dengan bayangan kontak + bayangan jatuh
    · tiga sudut per SKU: 0° (depan), −18° (3/4 kiri), +40° (sisi)
    · katalog 1:1 2000 px, objek 70% tinggi bidang
    · hero 16:9 2400×1350, objek di sepertiga kanan, kiri dikosongkan untuk judul

Keluaran
--------
    assets/img/katalog/<id>-0.jpg       depan
    assets/img/katalog/<id>-18.jpg      3/4
    assets/img/katalog/<id>-40.jpg      sisi
    assets/img/katalog/<id>-hero.jpg    16:9 untuk hero
    laporan/katalog-render.png          lembar kontak 9 SKU × 3 sudut
    data/katalog-render.json            ukuran, berat, tinggi objek terukur

Pakai
-----
    python3 tools/katalog.py            # render semua SKU
    python3 tools/katalog.py --cek      # periksa keluaran (bentuk, ukuran, konsistensi)
    python3 tools/katalog.py --satu gayo
"""

from __future__ import annotations

import json
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "data", "catalog.json")
KELUAR = os.path.join(ROOT, "assets", "img", "katalog")
DATA = os.path.join(ROOT, "data", "katalog-render.json")
JS = os.path.join(ROOT, "data", "katalog.js")
LEMBAR = os.path.join(ROOT, "laporan", "katalog-render.png")
SPEC = os.path.join(ROOT, "data", "kemasan-katalog.json")
SPESIMEN = os.path.join(ROOT, "laporan", "kemasan-spesimen.png")
PASAR = os.path.join(ROOT, "assets", "img", "katalog", "pasar")

PAPER = (237, 235, 230)       # #EDEBE6
PAPER_TERANG = (246, 243, 236)
TINTA = (20, 20, 20)          # #141414
AKSEN = (225, 84, 43)         # #E1542B — hanya untuk pelat identitas di lembar kontak

# --- rig studio: satu resep untuk semua SKU ------------------------------------
KEY = (-0.62, -0.78)          # arah cahaya utama (kiri-atas)
FILL = 0.26                   # pengisi dari kanan
RIM = 0.34                    # garis cahaya di tepi kanan
SISI_GELAP = 0.46             # muka samping terhadap muka depan
ATAS_TERANG = 1.06
SUDUT = (0, -18, 40)
KATALOG = 2000                # px, 1:1
HERO = (2400, 1350)           # px, 16:9
OBJEK_KATALOG = 0.70          # tinggi objek / tinggi bidang
OBJEK_HERO = 0.72
KETEBALAN = 0.065             # tebal kemasan / lebar depan (karton terisi 200–250 g)
LEBAR_SISI = 0.085
LEBAR_ATAS = 0.022
KUALITAS = 88


# ------------------------------------------------------------------ bantuan ---
# ------------------------------------------------------- spesifikasi kemasan ---
BAWAAN = {
    "status": "sementara",
    "satuan": "mm",
    "bentuk": "stand-up pouch",
    "ukuran_aktif": "250",
    "ukuran": {
        "100": {"lebar": 100, "tinggi": 160, "gusset": 30, "segel": 12, "zipper": 26},
        "250": {"lebar": 120, "tinggi": 200, "gusset": 35, "segel": 13, "zipper": 28},
        "500": {"lebar": 150, "tinggi": 250, "gusset": 40, "segel": 14, "zipper": 30},
    },
    "bahan": {"warna": "#F0EBE0", "kilap": 0.22, "nama": "kraft matte"},
    "depan": {"cetak_penuh": True, "margin": 0},
    "valve": {"ada": False, "x": 0.5, "y_dari_atas": 60, "diameter": 15},
    "segel": {"gerigi": 7},
}


def hex_rgb(kode: str) -> tuple[int, int, int]:
    kode = kode.strip().lstrip("#")
    return tuple(int(kode[i:i + 2], 16) for i in (0, 2, 4))       # type: ignore[return-value]


def spek(ukuran: str | None = None) -> dict:
    """Baca data/kemasan-katalog.json lalu pilih satu ukuran pouch.

    Semua angka geometri foto berasal dari sini: rasio tinggi/lebar, tebal
    (gusset), lebar pita segel, posisi zipper, posisi valve, warna bahan, kilap.
    Ganti berkasnya, jalankan ulang, sembilan foto ikut berubah.
    """
    data = {}
    if os.path.exists(SPEC):
        with open(SPEC, encoding="utf-8") as f:
            data = json.load(f)
    sp = {**BAWAAN, **{k: v for k, v in data.items() if not k.startswith("_")}}
    for k, v in BAWAAN.items():                       # isi anak kunci yang belum ada
        if isinstance(v, dict):
            sp[k] = {**v, **sp.get(k, {})}
    kunci = str(ukuran or sp.get("ukuran_aktif") or "250")
    if kunci not in sp["ukuran"]:
        raise SystemExit(f"ukuran '{kunci}' tidak ada di data/kemasan-katalog.json "
                         f"(ada: {', '.join(sp['ukuran'])})")
    u = dict(sp["ukuran"][kunci])
    for wajib in ("lebar", "tinggi", "gusset", "segel", "zipper"):
        if not u.get(wajib):
            raise SystemExit(f"ukuran {kunci}: '{wajib}' belum diisi di data/kemasan-katalog.json")
    if u["zipper"] + u["segel"] > u["tinggi"] * 0.4:
        raise SystemExit(f"ukuran {kunci}: zipper+segel terlalu besar untuk tinggi pouch")
    u["kunci"] = kunci
    sp["aktif"] = u
    return sp


def muka_kemasan(lbl: Image.Image, w: int, h: int, sp: dict) -> Image.Image:
    """Muka depan kemasan: desain label + bahan, pita segel, zipper, valve.

    Bedanya dengan `lbl.resize((w, h))` yang lama: tinggi kemasan datang dari
    ukuran mm (bukan dari rasio berkas label), jadi ada area bahan di atas
    desain — persis tempat segel dan zipper berada di pouch sungguhan.
    """
    u = sp["aktif"]
    bahan = sp.get("bahan", {})
    warna = hex_rgb(bahan.get("warna") or "#F0EBE0")
    depan = sp.get("depan", {})
    cetak_penuh = depan.get("cetak_penuh", True)
    band = max(2, round(h * u["zipper"] / u["tinggi"]))       # area bahan di atas desain
    margin = max(0, round(w * float(depan.get("margin") or 0) / u["lebar"]))

    if cetak_penuh:
        art_w, art_h, art_x, art_y = w, h - band, 0, band
    else:
        art_w, art_h = max(8, w - 2 * margin), max(8, h - band - margin)
        art_x, art_y = margin, band

    kanvas = Image.new("RGB", (w, h), warna)
    kanvas.paste(lbl.resize((art_w, art_h), Image.LANCZOS), (art_x, art_y))

    d = ImageDraw.Draw(kanvas, "RGBA")
    # pita segel atas: crimp halus (garis vertikal) + bayangan tipis di bawahnya
    segel = max(3, round(h * u["segel"] / u["tinggi"]))
    gerigi_px = max(2, round(w * float(sp.get("segel", {}).get("gerigi", 7)) / u["lebar"]))
    for x in range(0, w, gerigi_px):
        d.line([(x, 0), (x, segel)], fill=(0, 0, 0, 13), width=1)
    d.line([(0, segel), (w, segel)], fill=(0, 0, 0, 30), width=max(1, w // 1100))
    d.line([(0, segel + max(1, h // 500)), (w, segel + max(1, h // 500))],
           fill=(255, 255, 255, 46), width=max(1, h // 700))

    # zipper: dua garis (bayangan + kilau) tepat di bawah pita segel
    zy = segel + max(2, round(band * 0.34))
    if zy < band - 2:
        d.line([(0, zy), (w, zy)], fill=(0, 0, 0, 40), width=max(1, h // 600))
        d.line([(0, zy + max(1, h // 520)), (w, zy + max(1, h // 520))],
               fill=(255, 255, 255, 60), width=max(1, h // 700))

    # valve satu arah: cincin + cekungan, hanya bila spesifikasi menyebut ada
    v = sp.get("valve", {})
    if v.get("ada"):
        r = max(4, round(w * float(v.get("diameter", 15)) / u["lebar"] / 2))
        vx = round(w * float(v.get("x", 0.5)))
        vy = round(h * float(v.get("y_dari_atas", 60)) / u["tinggi"])
        d.ellipse([vx - r, vy - r, vx + r, vy + r], fill=(0, 0, 0, 20))
        d.ellipse([vx - r, vy - r, vx + r, vy + r], outline=(0, 0, 0, 70),
                  width=max(1, r // 5))
        d.ellipse([vx - r * 0.62, vy - r * 0.62, vx + r * 0.62, vy + r * 0.62],
                  fill=(255, 255, 255, 34))
        d.arc([vx - r, vy - r, vx + r, vy + r], 200, 320, fill=(255, 255, 255, 120),
              width=max(1, r // 4))

    # oklusi bawah: kain mendekat lantai jadi sedikit lebih gelap
    bawah = Image.new("L", (1, h))
    for y in range(h):
        p_ = y / max(1, h - 1)
        nilai = 255 if p_ < 0.9 else round(255 * (1 - 0.10 * (p_ - 0.9) / 0.1))
        bawah.putpixel((0, y), nilai)
    bawah = bawah.resize((w, h), Image.BILINEAR)
    kanvas = ImageChops.multiply(kanvas, Image.merge("RGB", (bawah, bawah, bawah)))
    return kanvas


def kilau(muka: Image.Image, kekuatan: float) -> Image.Image:
    """Kilau bahan: pita vertikal lembut dari arah key light (0 = matte)."""
    if kekuatan <= 0.01:
        return muka
    w, h = muka.size
    pita = Image.new("L", (w, 1), 0)
    cx = w * (0.5 + KEY[0] * 0.30)
    lebar = max(2, round(w * 0.16))
    for x in range(w):
        j = max(0.0, 1.0 - abs(x - cx) / lebar)
        pita.putpixel((x, 0), round(255 * (j ** 2)))
    topeng = pita.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(2, w // 30)))
    tambah = topeng.point(lambda v: round(v * 0.34 * kekuatan))
    return ImageChops.screen(muka, Image.merge("RGB", (tambah, tambah, tambah)))


def baca_catalog() -> list[dict]:
    with open(CATALOG, encoding="utf-8") as f:
        return json.load(f)["products"]


def label(id_: str) -> Image.Image | None:
    jalur = os.path.join(ROOT, "brand", f"label-{id_}.png")
    if not os.path.exists(jalur):
        return None
    return Image.open(jalur).convert("RGB")


def gradasi(ukuran: tuple[int, int], atas: tuple, bawah: tuple) -> Image.Image:
    """Gradasi vertikal halus — latar kertas, bukan putih mati."""
    w, h = ukuran
    kecil = Image.new("RGB", (1, h))
    for y in range(h):
        p = y / max(1, h - 1)
        kecil.putpixel((0, y), tuple(round(a + (b - a) * p) for a, b in zip(atas, bawah)))
    return kecil.resize((w, h), Image.BILINEAR)


def bayangan(ukuran: tuple[int, int], kotak: tuple[int, int, int, int],
             kekuatan: int = 96) -> Image.Image:
    """Bayangan kontak: elips kabur di bawah objek + jatuh ke kanan."""
    lapis = Image.new("L", ukuran, 0)
    d = ImageDraw.Draw(lapis)
    x0, y0, x1, y1 = kotak
    d.ellipse([x0, y0, x1, y1], fill=kekuatan)
    # kabur menurut LEBAR elips, bukan tingginya: elips bayangan sangat pipih,
    # kalau diblur menurut tinggi hasilnya bertepi keras seperti papan
    lapis = lapis.filter(ImageFilter.GaussianBlur(max(6, (x1 - x0) // 12)))
    return lapis


def cahaya(muka: Image.Image, sudut: float) -> Image.Image:
    """Terapkan key + fill + rim ke satu muka datar (gradien horizontal + radial)."""
    w, h = muka.size
    # gradien horizontal: terang di kiri (dekat key light), gelap di kanan
    pita = Image.new("L", (w, 1))
    for x in range(w):
        p = x / max(1, w - 1)
        nilai = 255 * (1.0 - 0.22 * p)          # sisi kanan turun 22%
        pita.putpixel((x, 0), max(0, min(255, round(nilai))))
    topeng = pita.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2))
    muka = ImageChops.multiply(muka, Image.merge("RGB", (topeng, topeng, topeng)))

    # sorot radial dari arah key (kiri-atas), menambah terang tanpa mengubah warna
    sorot = Image.new("L", (w, h), 0)
    ds = ImageDraw.Draw(sorot)
    cx = w * (0.5 + KEY[0] * 0.32)
    cy = h * (0.5 + KEY[1] * 0.32)
    r = int(max(w, h) * 0.62)
    for i in range(10, 0, -1):
        rr = r * i / 10
        ds.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                   fill=int(18 * (1 - i / 10) ** 1.6 * 6))
    sorot = sorot.filter(ImageFilter.GaussianBlur(r // 6))
    sorot3 = Image.merge("RGB", (sorot, sorot, sorot))
    return ImageChops.screen(muka, sorot3)



def _selesaikan(A: list[list[float]], b: list[float]) -> list[float]:
    """Eliminasi Gauss sederhana untuk 8×8 (dipakai menyusun homografi)."""
    n = len(A)
    M = [linha[:] + [b[i]] for i, linha in enumerate(A)]
    for kol in range(n):
        piv = max(range(kol, n), key=lambda r: abs(M[r][kol]))
        if abs(M[piv][kol]) < 1e-12:
            raise ValueError("matriks singular")
        M[kol], M[piv] = M[piv], M[kol]
        for r in range(kol + 1, n):
            f = M[r][kol] / M[kol][kol]
            for c in range(kol, n + 1):
                M[r][c] -= f * M[kol][c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        v = M[r][n] - sum(M[r][c] * x[c] for c in range(r + 1, n))
        x[r] = v / M[r][r]
    return x


def homografi(sumber: list[tuple[float, float]],
              tujuan: list[tuple[float, float]]) -> list[float]:
    """Homografi sumber→tujuan (4 titik), lalu dibalik supaya bisa dipakai PIL.

    PIL `Image.PERSPECTIVE` memetakan piksel KELUARAN ke piksel MASUKAN, jadi yang
    dibutuhkan inversnya. Inilah yang membuat muka kotak benar-benar mengecil ke
    jauh (perspektif sungguhan), bukan sekadar gambar ditempel miring.
    """
    A, b = [], []
    for (x, y), (u, v) in zip(sumber, tujuan):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    h = _selesaikan(A, b)
    H = [[h[0], h[1], h[2]], [h[3], h[4], h[5]], [h[6], h[7], 1.0]]
    # invers 3×3 (adjoin / determinan)
    a, b_, c = H[0]
    d, e, f = H[1]
    g, i, j = H[2]
    det = a * (e * j - f * i) - b_ * (d * j - f * g) + c * (d * i - e * g)
    if abs(det) < 1e-12:
        raise ValueError("homografi tidak bisa dibalik")
    inv = [[(e * j - f * i) / det, (c * i - b_ * j) / det, (b_ * f - c * e) / det],
           [(f * g - d * j) / det, (a * j - c * g) / det, (c * d - a * f) / det],
           [(d * i - e * g) / det, (b_ * g - a * i) / det, (a * e - b_ * d) / det]]
    if abs(inv[2][2]) < 1e-12:
        raise ValueError("homografi terbalik singular")
    inv = [[v / inv[2][2] for v in linha] for linha in inv]
    return [inv[0][0], inv[0][1], inv[0][2], inv[1][0], inv[1][1], inv[1][2], inv[2][0], inv[2][1]]


def kotak(muka: Image.Image, tinggi: int, yaw: float, pitch: float = -5.0,
          sp: dict | None = None) -> Image.Image:
    """Bangun kemasan bervolume dengan proyeksi perspektif sungguhan.

    Beda dengan versi lama: geometri ditulis sebagai **delapan titik + empat
    muka**, tiap muka punya normal sendiri, dan muka yang menghadap menjauh
    dibuang (back-face culling) lalu digambar dari yang terjauh. Versi lama
    menebak urutan gambar dengan `if yaw > 0`, memakai tanda kedalaman yang
    terbalik (muka depan justru dikecilkan), dan menambal bentuk dengan titik
    kelima yang membuat topengnya menusuk keluar.

    Bentuknya pouch berdiri: muka depan rata (label), gusset membuka penuh di
    bawah, dan di bawah pita segel kedua panel terjepit — jadi muka atas hanya
    selebar tepi segel, bukan kedalaman gusset.
    """
    sp = sp or spek()
    u = sp["aktif"]
    S = 2                                           # supersample
    rasio = u["tinggi"] / u["lebar"]                # dari ukuran mm, bukan dari label
    h = tinggi * S
    w = max(2, round(h / rasio))
    d = max(3, round(w * u["gusset"] / u["lebar"]))  # kedalaman gusset (bawah)
    d_atas = d * 0.12                                # di bawah segel panel terjepit

    a, b = math.radians(yaw), math.radians(pitch)
    ca, sa, cb, sb = math.cos(a), math.sin(a), math.cos(b), math.sin(b)
    f = max(w, h) * 3.4                              # jarak kamera (proyeksi lembut)

    def putar(x: float, y: float, z: float) -> tuple[float, float, float]:
        x1 = x * ca + z * sa
        z1 = -x * sa + z * ca
        y2 = y * cb - z1 * sb
        z2 = y * sb + z1 * cb
        return x1, y2, z2

    def proyeksi(x: float, y: float, z: float) -> tuple[float, float]:
        x1, y2, z2 = putar(x, y, z)
        # kamera di sumbu +z: titik dengan z lebih besar lebih dekat → lebih besar
        k = f / max(1.0, f - z2)
        return x1 * k, y2 * k

    # delapan titik: depan (z=+d/2), belakang bawah (−d), belakang atas (−d_atas)
    depan = {"lt": (-w / 2, -h / 2, d / 2), "rt": (w / 2, -h / 2, d / 2),
             "rb": (w / 2, h / 2, d / 2), "lb": (-w / 2, h / 2, d / 2)}
    belakang = {"lt": (-w / 2, -h / 2, -d_atas), "rt": (w / 2, -h / 2, -d_atas),
                "rb": (w / 2, h / 2, -d), "lb": (-w / 2, h / 2, -d)}
    p3 = {**depan, **{f"b_{k}": v for k, v in belakang.items()}}

    muka_kotak = {
        # nama: (empat titik CCW dari luar, normal di ruang objek)
        "depan": (["lt", "rt", "rb", "lb"], (0.0, 0.0, 1.0)),
        "kanan": (["rt", "b_rt", "b_rb", "rb"], (1.0, 0.0, 0.0)),
        "kiri": (["b_lt", "lt", "lb", "b_lb"], (-1.0, 0.0, 0.0)),
        "atas": (["b_lt", "b_rt", "rt", "lt"], (0.0, -1.0, 0.0)),
    }

    semua_q, tampak = [], []
    for nama, (kunci, n) in muka_kotak.items():
        q = [proyeksi(*p3[k]) for k in kunci]
        semua_q += q
        nx, ny, nz = putar(*n)
        if nz > 1e-6:                               # hanya muka yang menghadap kamera
            z_rata = sum(putar(*p3[k])[2] for k in kunci) / 4
            tampak.append((z_rata, nama, q))

    xs = [q[0] for q in semua_q]
    ys = [q[1] for q in semua_q]
    pad = 4 * S
    x0, x1 = min(xs) - pad, max(xs) + pad
    y0, y1 = min(ys) - pad, max(ys) + pad
    W, H = math.ceil(x1 - x0), math.ceil(y1 - y0)

    def tembak(tekstur: Image.Image, quad: list) -> tuple[Image.Image, Image.Image]:
        """Petakan tekstur ke segi empat; topeng poligon digambar 4× lalu diperkecil."""
        lt, rt, rb, lb = [(q[0] - x0, q[1] - y0) for q in quad]
        koef = homografi([(0, 0), (tekstur.width, 0), (tekstur.width, tekstur.height),
                          (0, tekstur.height)], [lt, rt, rb, lb])
        lapis = tekstur.transform((W, H), Image.PERSPECTIVE, koef, Image.BICUBIC)
        S2 = 4
        besar = Image.new("L", (W * S2, H * S2), 0)
        ImageDraw.Draw(besar).polygon([(x * S2, y * S2) for x, y in (lt, rt, rb, lb)], fill=255)
        return lapis, besar.resize((W, H), Image.LANCZOS)

    # --- tekstur
    depan_tex = kilau(cahaya(muka_kemasan(muka, w, h, sp), yaw),
                      float(sp.get("bahan", {}).get("kilap") or 0.0))

    def kertas_papan() -> tuple[int, int, int]:
        kode = sp.get("bahan", {}).get("warna")
        if kode:
            return hex_rgb(kode)
        px = [muka.getpixel((x, y)) for x in (3, muka.width - 4)
              for y in (3, muka.height - 4)]
        return tuple(int(sum(p[i] for p in px) / len(px) * 0.92) for i in range(3))

    papan = kertas_papan()
    tw = max(4, d)

    def gradien_1d(n: int, awal: float, akhir: float) -> Image.Image:
        jalur = Image.new("L", (n, 1))
        for i in range(n):
            q = i / max(1, n - 1)
            jalur.putpixel((i, 0), max(0, min(255, round(255 * (awal + (akhir - awal) * q)))))
        return jalur

    # sisi: x=0 di tepi depan (dekat cahaya), x=tw di belakang (jauh)
    sisi_awal = 0.74 if yaw >= 0 else 0.96
    sisi_tex = Image.new("RGB", (tw, h), papan)
    gs = gradien_1d(tw, sisi_awal, sisi_awal - 0.30).resize((tw, h), Image.BILINEAR)
    lipat = Image.new("L", (1, h))
    for y in range(h):
        q = y / max(1, h - 1)
        lipat.putpixel((0, y), 255 if q < 0.55 else round(255 * (1 - 0.16 * (q - 0.55) / 0.45)))
    lipat = lipat.resize((tw, h), Image.BILINEAR)
    gs = ImageChops.multiply(gs, lipat)
    sisi_tex = ImageChops.multiply(sisi_tex, Image.merge("RGB", (gs, gs, gs)))

    # atas: x=0 di tepi depan (terang), x=tw di belakang (bayangan segel)
    atas_tex = Image.new("RGB", (w, tw), papan)
    ga = gradien_1d(w, 1.02, 0.82)
    ga = ga.resize((w, tw), Image.BILINEAR)
    gb = Image.new("L", (1, tw))
    for y in range(tw):
        q = y / max(1, tw - 1)
        gb.putpixel((0, y), round(255 * (0.98 - 0.34 * q)))
    gb = gb.resize((w, tw), Image.BILINEAR)
    ga = ImageChops.multiply(ga, gb)
    atas_tex = ImageChops.multiply(atas_tex, Image.merge("RGB", (ga, ga, ga)))

    tekstur = {"depan": depan_tex, "kanan": sisi_tex, "kiri": sisi_tex, "atas": atas_tex}

    # --- gambar dari yang paling jauh; muka depan selalu terakhir (paling dekat)
    kanvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for _, nama, quad in sorted(tampak, key=lambda t: t[0]):
        if nama == "depan":
            continue
        lapis, topeng = tembak(tekstur[nama], quad)
        kanvas.paste(lapis, (0, 0), topeng)
    depan_q = next((q for _, n, q in tampak if n == "depan"), None)
    if depan_q:
        lapis, topeng = tembak(depan_tex, depan_q)
        kanvas.paste(lapis, (0, 0), topeng)

    # garis sambungan hanya di tepi depan↔sisi (menggambar semua sisi membuat
    # garis melintang menembus label)
    if depan_q and abs(yaw) > 0.5:
        dg = ImageDraw.Draw(kanvas)
        tepi = (depan_q[1], depan_q[2]) if yaw > 0 else (depan_q[0], depan_q[3])
        dg.line([(q[0] - x0, q[1] - y0) for q in tepi], fill=(150, 142, 128, 255), width=1)

    # pangkas tepat ke batas geometri (ambang warna tidak bisa dipakai: kertas
    # latar dan kertas kemasan hanya beda beberapa satuan)
    kanvas = kanvas.resize((W // S, H // S), Image.LANCZOS)
    p = pad // S
    return kanvas.crop((p, p, kanvas.width - p, kanvas.height - p))


def potong_konten(im: Image.Image) -> Image.Image:
    """Pangkas latar kertas (putih hangat) supaya objek terukur, bukan ditebak."""
    abu = im.convert("L")
    beda = ImageChops.difference(abu, Image.new("L", im.size, 232))
    kotak_k = beda.point(lambda v: 255 if v > 12 else 0).getbbox()
    if not kotak_k:
        return im
    return im.crop(kotak_k)


def tempatkan(latar: Image.Image, objek: Image.Image, skala_tinggi: float,
              kanan: float = 0.5, dasar: float = 0.80) -> tuple[Image.Image, tuple]:
    """Tempel objek + bayangan kontak di lantai; kembalikan gambar dan kotak objek."""
    W, H = latar.size
    th = round(H * skala_tinggi)
    tw = round(objek.width * th / objek.height)
    o = objek.resize((tw, th), Image.LANCZOS)
    cx = round(W * kanan)
    bawah = round(H * dasar)
    x0, y0 = cx - tw // 2, bawah - th
    # bayangan: elips di bawah, digeser sedikit ke kanan (cahaya dari kiri)
    lx0, lx1 = x0 - tw // 9, x0 + tw + tw // 5
    ly0, ly1 = bawah - max(6, th // 44), bawah + max(10, th // 20)
    sh = bayangan((W, H), (lx0, ly0, lx1, ly1), 96)
    gelap = Image.new("RGB", (W, H), (58, 46, 36))
    latar = Image.composite(gelap, latar, sh.point(lambda v: int(v * 0.52)))
    # bayangan kontak: elips sempit tepat di bawah objek, lebih pekat
    kx = Image.new("L", (W, H), 0)
    ImageDraw.Draw(kx).ellipse([x0 - tw // 12, bawah - max(3, th // 70),
                                x0 + tw + tw // 12, bawah + max(5, th // 34)], fill=210)
    kx = kx.filter(ImageFilter.GaussianBlur(max(2, th // 90)))
    latar = Image.composite(Image.new("RGB", (W, H), (44, 34, 26)), latar, kx)
    latar.paste(o, (x0, y0), o.split()[3] if o.mode == "RGBA" else None)
    return latar, (x0, y0, x0 + tw, y0 + th)


def pasar(ukuran: tuple[int, int], objek: Image.Image, skala: float,
          kanan: float = 0.5, dasar: float = 0.86) -> Image.Image:
    """Foto untuk marketplace: latar PUTIH MURNI, tanpa bayangan, objek di tengah.

    Aturan Tokopedia/Shopee minta latar putih bersih tanpa properti; bayangan dan
    latar kertas justru bisa ditolak atau dipotong sistem. Karena itu foto ini
    dibuat terpisah, bukan sekadar versi kecil dari foto katalog.
    """
    W, H = ukuran
    latar = Image.new("RGB", ukuran, (255, 255, 255))
    th = round(H * skala)
    tw = round(objek.width * th / objek.height)
    o = objek.resize((tw, th), Image.LANCZOS)
    x = round(W * kanan) - tw // 2
    y = round(H * dasar) - th
    if o.mode == "RGBA":
        latar.paste(o, (x, y), o.split()[3])
    else:
        latar.paste(o, (x, y))
    return latar


def bingkai(ukuran: tuple[int, int], objek: Image.Image, skala: float,
            kanan: float, dasar: float) -> tuple[Image.Image, tuple]:
    latar = gradasi(ukuran, PAPER_TERANG, PAPER)
    # vignette halus: tepi sedikit lebih gelap, seperti kertas di bawah lampu
    vg = Image.new("L", ukuran, 0)
    dv = ImageDraw.Draw(vg)
    dv.ellipse([-ukuran[0] * 0.18, -ukuran[1] * 0.28, ukuran[0] * 1.18, ukuran[1] * 1.28], fill=255)
    vg = vg.filter(ImageFilter.GaussianBlur(min(ukuran) // 16))
    latar = Image.composite(latar, Image.new("RGB", ukuran, PAPER), vg)
    return tempatkan(latar, objek, skala, kanan, dasar)


# -------------------------------------------------------------------- render ---
def render_sku(p: dict, sp: dict | None = None, ukuran: str | None = None) -> dict:
    sp = sp or spek(ukuran)
    muka = label(p["id"])
    if muka is None:
        return {"id": p["id"], "status": "tanpa label"}
    if ukuran:
        # ukuran yang diminta pemilik: pakai berkas label untuk berat itu bila ada
        # (mis. label-gayo-500.png), kalau tidak label dasar dipakai apa adanya.
        varian = label(f'{p["id"]}-{ukuran}')
        if varian is not None:
            muka = varian
    os.makedirs(KELUAR, exist_ok=True)
    keluaran = {}
    tinggi_obj = 0
    for sudut in SUDUT:
        # tinggi objek di ruang render: sedikit lebih besar dari tinggi akhir
        o = kotak(muka, 1100, sudut, sp=sp)
        im, kk = bingkai((KATALOG, KATALOG), o, OBJEK_KATALOG, 0.5, 0.82)
        nama = f'{p["id"]}-{abs(sudut)}.jpg'
        jalur = os.path.join(KELUAR, nama)
        im.save(jalur, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
        tinggi_obj = max(tinggi_obj, kk[3] - kk[1])
        keluaran[abs(sudut)] = {"berkas": f"assets/img/katalog/{nama}",
                                "kotak": list(kk),
                                "kb": round(os.path.getsize(jalur) / 1024, 1)}
    o = kotak(muka, 1150, -16, sp=sp)
    hero, kh = bingkai(HERO, o, OBJEK_HERO, 0.68, 0.84)
    nama_hero = f'{p["id"]}-hero.jpg'
    jalur = os.path.join(KELUAR, nama_hero)
    hero.save(jalur, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
    keluaran["hero"] = {"berkas": f"assets/img/katalog/{nama_hero}", "kotak": list(kh),
                        "kb": round(os.path.getsize(jalur) / 1024, 1)}

    # foto marketplace: putih murni, dua rasio yang dipakai e-commerce & feed
    os.makedirs(PASAR, exist_ok=True)
    pasar_keluar = {}
    for kunci, ukuran, skala in (("1x1", (1000, 1000), 0.80), ("4x5", (1080, 1350), 0.72)):
        obyek_p = kotak(muka, 900, 0, sp=sp)
        im_p = pasar(ukuran, obyek_p, skala, 0.5, 0.88)
        nama_p = f'{p["id"]}-{kunci}.jpg'
        jalur_p = os.path.join(PASAR, nama_p)
        im_p.save(jalur_p, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
        pasar_keluar[kunci] = {"berkas": f"assets/img/katalog/pasar/{nama_p}",
                               "kb": round(os.path.getsize(jalur_p) / 1024, 1),
                               "ukuran": list(ukuran)}
    u = sp["aktif"]
    return {"id": p["id"], "nama": p["name"], "status": "siap",
            "ukuran": u["kunci"],
            "geometri": {k: u[k] for k in ("lebar", "tinggi", "gusset", "segel", "zipper")},
            "bahan": sp.get("bahan", {}).get("nama", "—"),
            "tinggi_objek_px": tinggi_obj, "keluaran": keluaran,
            "pasar": pasar_keluar}


def lembar_hasil(hasil: list[dict]) -> None:
    """Lembar kontak: 9 SKU × 3 sudut, dengan label kecil di bawah tiap baris."""
    ikon = 300
    kepala = 58
    kaki = 26
    baris = [h for h in hasil if h["status"] == "siap"]
    W = ikon * len(SUDUT) + 40
    H = kepala + (ikon + kaki) * len(baris) + 20
    lembar = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(lembar)
    try:
        from PIL import ImageFont
        f_kecil = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-600-normal.ttf"), 15)
        f_judul = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-500-normal.ttf"), 13)
    except OSError:
        f_kecil = f_judul = ImageFont.load_default()
    d.text((20, 20), "FOTO KATALOG — 3 SUDUT, SATU RIG", font=f_kecil, fill=TINTA)
    d.text((W - 210, 22), "tools/katalog.py", font=f_judul, fill=(109, 106, 99))
    for i, h in enumerate(baris):
        y = kepala + i * (ikon + kaki)
        d.text((20, y + 4), h["nama"].upper(), font=f_kecil, fill=TINTA)
        for j, sudut in enumerate(SUDUT):
            k = h["keluaran"][abs(sudut)]
            im = Image.open(os.path.join(ROOT, k["berkas"]))
            im.thumbnail((ikon - 16, ikon - 16), Image.LANCZOS)
            x = 20 + j * ikon
            lembar.paste(im, (x, y + kaki))
            d.rectangle([x, y + kaki, x + ikon - 8, y + kaki + ikon - 8], outline=(220, 216, 208))
            d.text((x + 2, y + kaki + ikon - 6), f'{sudut}°', font=f_judul, fill=(109, 106, 99))
        d.line([20, y + ikon + kaki + 6, W - 20, y + ikon + kaki + 6], fill=(222, 218, 210))
    lembar.save(LEMBAR, optimize=True)


def tulis_js(hasil: list[dict]) -> None:
    """Data untuk halaman katalog: isi SKU + jalur gambar. Harga dari catalog.json."""
    produk = {p["id"]: p for p in baca_catalog()}
    sku = []
    for h in hasil:
        if h["status"] != "siap":
            continue
        p = produk[h["id"]]
        v = sorted(p["variants"], key=lambda x: x["grams"])
        sku.append({
            "id": p["id"], "no": p["no"], "nama": p["name"],
            "asal": p["origin_line"], "notes": p["notes"],
            "proses": p["process"], "roast": p["roast_level"],
            "harga": v[0]["price"], "harga_teks": "Rp{:,.0f}".format(v[0]["price"]).replace(",", "."),
            "ukuran": [{"label": x["weight"], "harga": x["price"]} for x in v],
            "sku": v[0]["sku"], "status": p["status"],
            "foto": {str(k): e["berkas"] for k, e in h["keluaran"].items()},
            "pasar": {k: e["berkas"] for k, e in (h.get("pasar") or {}).items()},
        })
    sp = spek()
    u = sp["aktif"]
    isi = {
        "keterangan": "Dibangun tools/katalog.py dari data/catalog.json + data/kemasan-katalog.json "
                      "+ assets/img/katalog. Harga = varian terkecil; jangan diketik di JS.",
        "rig": {"sudut": list(SUDUT), "katalog_px": KATALOG, "hero_px": list(HERO)},
        "kemasan": {"status": sp.get("status"), "bentuk": u.get("bentuk", sp.get("bentuk")),
                    "stiker": sp.get("stiker"),
                    "ukuran": u["kunci"], "lebar": u["lebar"], "tinggi": u["tinggi"],
                    "gusset": u["gusset"], "segel": u["segel"], "zipper": u["zipper"],
                    "berat": u.get("berat"), "bahan": sp.get("bahan", {}).get("nama"),
                    "warna": sp.get("bahan", {}).get("warna"),
                    "kilap": sp.get("bahan", {}).get("kilap"),
                    "valve": bool(sp.get("valve", {}).get("ada"))},
        "sku": sku,
    }
    with open(JS, "w", encoding="utf-8") as f:
        f.write("/* Foto katalog Nocturne — dibangun tools/katalog.py. Jangan sunting tangan. */\n")
        f.write("window.KATALOG = ")
        json.dump(isi, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")


def tulis_data(hasil: list[dict]) -> None:
    p = {
        "keterangan": "Dirender tools/katalog.py dari label brand — bukan foto asli dan bukan "
                      "generator gambar. Satu rig studio untuk semua SKU.",
        "rig": {"key": KEY, "fill": FILL, "rim": RIM, "sisi_gelap": SISI_GELAP,
                "sudut": list(SUDUT), "katalog_px": KATALOG, "hero_px": list(HERO),
                "objek_katalog": OBJEK_KATALOG, "objek_hero": OBJEK_HERO},
        "sku": hasil,
    }
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ----------------------------------------------------------------------- cek ---
def spesimen() -> None:
    """Lembar tiga ukuran (100 / 250 / 500 g) bersebelahan pada satu garis lantai.

    Dipakai untuk mencocokkan render dengan kemasan di tangan: kalau proporsi
    atau warna bahan tidak sama, yang salah adalah data/kemasan-katalog.json — bukan
    halamannya. Skala antar ukuran benar (mm), jadi 100 g tampak lebih kecil.
    """
    semua = spek()
    p = baca_catalog()[0]
    muka = label(p["id"])
    if muka is None:
        raise SystemExit("label contoh tidak ada")
    u_all = semua["ukuran"]
    urut = sorted(u_all, key=lambda k: u_all[k]["tinggi"])
    tinggi_acuan = max(u_all[k]["tinggi"] for k in urut)
    tinggi_kanvas = 1400
    pad = 80
    ubin: list[tuple[str, Image.Image, dict]] = []
    for k in urut:
        sp_k = spek(k)
        o = kotak(muka, round(950 * u_all[k]["tinggi"] / tinggi_acuan), 0, sp=sp_k)
        ubin.append((k, o, sp_k))
    W = sum(o.width for _, o, _ in ubin) + pad * (len(ubin) + 1)
    H = tinggi_kanvas
    latar = gradasi((W, H), PAPER_TERANG, PAPER)
    dasar = round(H * 0.80)
    x = pad
    d0 = ImageDraw.Draw(latar)
    for k, o, sp_k in ubin:
        skala = 950 * u_all[k]["tinggi"] / tinggi_acuan / o.height * 0.92
        oo = o.resize((round(o.width * skala), round(o.height * skala)), Image.LANCZOS)
        y = dasar - oo.height
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).ellipse([x - oo.width // 8, dasar - 10,
                                    x + oo.width + oo.width // 5, dasar + oo.height // 9], fill=110)
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        latar = Image.composite(Image.new("RGB", (W, H), (58, 46, 36)), latar, sh.point(lambda v: int(v * 0.6)))
        latar.paste(oo, (x, y), oo.split()[3] if oo.mode == "RGBA" else None)
        x += oo.width + pad
    d = ImageDraw.Draw(latar)
    try:
        from PIL import ImageFont
        f_k = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-600-normal.ttf"), 22)
        f_t = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-400-normal.ttf"), 19)
    except OSError:
        f_k = f_t = ImageFont.load_default()
    d.text((40, 34), "SPESIMEN KEMASAN — TIGA UKURAN, SKALA mm", font=f_k, fill=TINTA)
    d.text((40, 66), "Cocokkan dengan kemasan di tangan; kalau beda, perbaiki data/kemasan-katalog.json",
           font=f_t, fill=(109, 106, 99))
    x = pad
    for k, o, sp_k in ubin:
        skala = 950 * u_all[k]["tinggi"] / tinggi_acuan / o.height * 0.92
        ww = round(o.width * skala)
        u = sp_k["aktif"]
        d.text((x, dasar + 26), f"{u.get('berat', k + ' g')}  ·  {u['lebar']}×{u['tinggi']} mm",
               font=f_k, fill=TINTA)
        d.text((x, dasar + 56), f"gusset {u['gusset']} · segel {u['segel']} · zipper {u['zipper']}",
               font=f_t, fill=(109, 106, 99))
        d.text((x, dasar + 82), f"bahan {sp_k.get('bahan', {}).get('warna', '—')} · "
               f"kilap {sp_k.get('bahan', {}).get('kilap', 0)}",
               font=f_t, fill=(109, 106, 99))
        x += ww + pad
    latar.save(SPESIMEN, optimize=True)
    print(f"  spesimen   laporan/kemasan-spesimen.png · {os.path.getsize(SPESIMEN)/1024:.0f} KB")


def cek() -> list[str]:
    m: list[str] = []
    if not os.path.exists(DATA):
        return ["data/katalog-render.json belum ada — jalankan python3 tools/katalog.py"]
    with open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    siap = [s for s in d["sku"] if s["status"] == "siap"]
    if len(siap) != 9:
        m.append(f'{len(siap)} SKU dirender, seharusnya 9')
    tinggi = []
    for s in siap:
        for kunci, e in s["keluaran"].items():
            jalur = os.path.join(ROOT, e["berkas"])
            if not os.path.exists(jalur):
                m.append(f'{s["id"]}: {e["berkas"]} tidak ada')
                continue
            with Image.open(jalur) as im:
                w, h = im.size
            harap = HERO if kunci == "hero" else (KATALOG, KATALOG)
            if (w, h) != harap:
                m.append(f'{s["id"]} {kunci}: {w}×{h}, seharusnya {harap[0]}×{harap[1]}')
            if os.path.getsize(jalur) > 520_000:
                m.append(f'{s["id"]} {kunci}: {os.path.getsize(jalur)/1024:.0f} KB terlalu berat')
            x0, y0, x1, y1 = e["kotak"]
            if kunci != "hero":
                tinggi.append(y1 - y0)
                if not (0.62 * KATALOG <= (y1 - y0) <= 0.78 * KATALOG):
                    m.append(f'{s["id"]} {kunci}: objek {(y1-y0)/KATALOG:.0%} tinggi bidang, target 70%')
                if x0 < 0 or x1 > KATALOG or y1 > KATALOG:
                    m.append(f'{s["id"]} {kunci}: objek keluar bidang')
            else:
                if x1 > HERO[0]:
                    m.append(f'{s["id"]} hero: objek melewati kanan bidang')
                if x0 < HERO[0] * 0.45:
                    m.append(f'{s["id"]} hero: objek terlalu ke tengah — kiri harus kosong untuk judul')
    for s in siap:
        for kunci, e in (s.get("pasar") or {}).items():
            jalur = os.path.join(ROOT, e["berkas"])
            if not os.path.exists(jalur):
                m.append(f'{s["id"]} pasar/{kunci}: berkas tidak ada')
                continue
            with Image.open(jalur) as im:
                if list(im.size) != e["ukuran"]:
                    m.append(f'{s["id"]} pasar/{kunci}: ukuran tidak sesuai')
                # empat sudut harus putih murni — syarat foto marketplace
                for titik in ((0, 0), (im.width - 1, 0), (0, im.height - 1),
                              (im.width - 1, im.height - 1)):
                    if min(im.convert("RGB").getpixel(titik)) < 250:
                        m.append(f'{s["id"]} pasar/{kunci}: latar bukan putih murni')
                        break
    if tinggi:
        sebar = (max(tinggi) - min(tinggi)) / max(tinggi)
        if sebar > 0.08:
            m.append(f"tinggi objek antar SKU berbeda {sebar:.0%} — satu rig harus konsisten (≤ 8%)")
    if not os.path.exists(LEMBAR):
        m.append("laporan/katalog-render.png belum ada")
    if not os.path.exists(SPESIMEN):
        m.append("laporan/kemasan-spesimen.png belum ada — jalankan --spesimen")
    # geometri yang dipakai foto harus sama dengan data/kemasan-katalog.json sekarang
    try:
        sp = spek()
    except SystemExit as e:
        m.append(str(e))
        return m
    u = sp["aktif"]
    dipakai = {s.get("ukuran") for s in siap}
    if dipakai != {u["kunci"]}:
        m.append(f"foto memakai ukuran {sorted(x for x in dipakai if x)} tapi "
                 f"data/kemasan-katalog.json memilih {u['kunci']} — render ulang")
    for s in siap:
        g = s.get("geometri") or {}
        if g and any(g.get(k) != u.get(k) for k in ("lebar", "tinggi", "gusset", "segel", "zipper")):
            m.append(f'{s["id"]}: geometri foto beda dengan spesifikasi — render ulang')
            break
    return m


if __name__ == "__main__":
    if "--cek" in sys.argv:
        mm = cek()
        for x in mm:
            print("  ✗", x)
        print("  kesimpulan:", "OK · 9 SKU × 3 sudut + hero, satu rig" if not mm else f"{len(mm)} masalah")
        sys.exit(0 if not mm else 1)
    spesimen()
    ukuran = sys.argv[sys.argv.index("--ukuran") + 1] if "--ukuran" in sys.argv else None
    if "--spesimen" in sys.argv:
        sys.exit(0)
    sp = spek(ukuran)
    u = sp["aktif"]
    print(f'  kemasan    {u.get("berat", u["kunci"] + " g")} · {u["lebar"]}×{u["tinggi"]} mm · '
          f'gusset {u["gusset"]} · bahan {sp.get("bahan", {}).get("warna")} '
          f'({sp.get("bahan", {}).get("nama", "—")}) · status {sp.get("status", "—")}')
    produk = baca_catalog()
    if "--satu" in sys.argv:
        kriteria = sys.argv[sys.argv.index("--satu") + 1]
        produk = [p for p in produk if p["id"] == kriteria]
    hasil = [render_sku(p, sp=sp) for p in produk]
    tulis_data(hasil)
    tulis_js(hasil)
    lembar_hasil(hasil)
    total = sum(e["kb"] for s in hasil if s["status"] == "siap" for e in s["keluaran"].values())
    print(f'  SKU        {len([h for h in hasil if h["status"] == "siap"])} · '
          f'{len(SUDUT)} sudut + hero · {total/1024:.1f} MB')
    print(f'  lembar     laporan/katalog-render.png · {os.path.getsize(LEMBAR)/1024:.0f} KB')
    print(f'  data       data/katalog-render.json')
    for x in cek():
        print("  ✗", x)
