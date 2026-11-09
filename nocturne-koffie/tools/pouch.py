#!/usr/bin/env python3
"""Foto studio kemasan 500 g flat-bottom — stiker 12 × 17 cm di tengah muka belakang.

Kenapa berkas ini terpisah dari `katalog.py`
--------------------------------------------
`katalog.py` memodelkan kemasan sebagai **kotak berlabel penuh**. Kemasan yang
benar (dikirim pemilik 9 Nov 2026) berbeda: **flat-bottom pouch 13,5 × 26 cm**,
bahan gelap, **valve di muka depan**, dan desain dicetak sebagai **stiker
12 × 17 cm yang ditempel di tengah muka belakang**. Karena itu bentuknya bukan
kotak, dan muka yang dipakai untuk jualan adalah muka **belakang** (sisi stiker).

Yang dibuat di sini
-------------------
1. Geometri pouch: 8 titik penampang melintang (panel + chamfer + sisi gusset),
   menyempit ke atas karena zipper menarik kedua panel. Muka dihitung normalnya,
   yang membelakangi kamera dibuang, sisanya digambar dari yang terjauh.
2. Tekstur: bahan (tenun halus + gradien), stiker (label yang sudah ada, ditempel
   dengan bayangan tipis), valve (cincin + kubah + bayangan), sisi gusset
   (lipatan tengah), dan pita segel atas (crimp + zipper).
3. Keluaran foto: 3 sudut + hero + 2 rasio marketplace (kontrak sama dengan
   `katalog.py`, jadi halaman `katalog/` dan versi luringnya ikut memakai foto
   ini tanpa diubah), plus muka datar transparan untuk `rak/`.

Batas (jangan diklaim lebih)
----------------------------
· Ini render dari geometri + label sendiri, **bukan pemotretan** kemasan fisik.
· Ketebalan (sisi 45 mm, chamfer 10 mm) **asumsi**; ukuran 13,5 × 26 cm dan stiker
  12 × 17 cm berasal dari pemilik.
· Lipatan kertas di sudut bawah, tekstur foil, dan jahitan tidak dimodelkan.

Pakai
-----
    python3 tools/pouch.py              # semua SKU
    python3 tools/pouch.py --satu gayo  # satu SKU, untuk mencoba sudut/cahaya
    python3 tools/pouch.py --cek        # periksa keluaran
"""

from __future__ import annotations

import json
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import katalog as K                                    # noqa: E402  (pustaka rig, bukan skrip)

ROOT = K.ROOT
SPEC = K.SPEC
KELUAR = K.KELUAR
PASAR = K.PASAR
DATA = K.DATA
JS = K.JS
LEMBAR = K.LEMBAR
POUCH = os.path.join(ROOT, "assets", "img", "pouch")
SPESIMEN = os.path.join(ROOT, "laporan", "pouch-spesimen.png")

SUDUT = (0, -18, 40)
KATALOG = K.KATALOG
HERO = K.HERO
OBJEK = K.OBJEK_KATALOG
OBJEK_HERO = K.OBJEK_HERO
KUALITAS = K.KUALITAS
PITCH = -5.0
SUPERSAMPLE = 2


# ------------------------------------------------------------------ bentuk ---
def geometri(sp: dict) -> dict:
    """Ukuran pouch dalam mm, plus turunan yang dipakai renderer."""
    u = sp["aktif"]
    if u.get("bentuk", "flat-bottom") != "flat-bottom":
        raise SystemExit("pouch.py hanya untuk bentuk flat-bottom "
                         f"(sekarang: {u.get('bentuk')})")
    W, H = float(u["lebar"]), float(u["tinggi"])
    D = float(u["gusset"])                     # kedalaman dasar (≈ 2 × sisi)
    sisi = float(u.get("sisi") or D / 2)
    c = float(u.get("chamfer") or 0)
    return {
        "W": W, "H": H, "D": D, "sisi": sisi, "chamfer": min(c, W / 6, D / 6),
        "segel": float(u["segel"]), "zipper": float(u["zipper"]),
        "kt": 0.72,                            # penyempitan atas (zipper menarik panel)
        "stiker": sp.get("stiker", {}),
        "valve": sp.get("valve", {}),
        "bahan": sp.get("bahan", {}),
    }


def penampang(g: dict) -> list[tuple[float, float]]:
    """Delapan titik penampang (x, z) berurutan searah jarum jam dilihat dari atas."""
    W, D, c = g["W"], g["D"], g["chamfer"]
    hw, hd = W / 2, D / 2
    return [(hw - c, hd), (hw, hd - c), (hw, -(hd - c)), (hw - c, -hd),
            (-(hw - c), -hd), (-hw, -(hd - c)), (-hw, hd - c), (-(hw - c), hd)]


# ditulis sebagai (indeks titik awal, akhir, nama muka, arah normal di ruang objek)
MUKA = [
    (7, 0, "stiker", (0.0, 0.0, 1.0)),         # panel dengan stiker — muka untuk jualan
    (3, 4, "depan", (0.0, 0.0, -1.0)),         # panel dengan valve
    (1, 2, "sisi_kanan", (1.0, 0.0, 0.0)),
    (5, 6, "sisi_kiri", (-1.0, 0.0, 0.0)),
    (0, 1, "chamfer_kanan", (0.7, 0.0, 0.7)),
    (2, 3, "chamfer_kanan", (0.7, 0.0, -0.7)),
    (4, 5, "chamfer_kiri", (-0.7, 0.0, -0.7)),
    (6, 7, "chamfer_kiri", (-0.7, 0.0, 0.7)),
]


def proyeksi_kamera(yaw: float, pitch: float, f_panjang: float):
    a, b = math.radians(yaw), math.radians(pitch)
    ca, sa, cb, sb = math.cos(a), math.sin(a), math.cos(b), math.sin(b)

    def putar(x: float, y: float, z: float) -> tuple[float, float, float]:
        x1 = x * ca + z * sa
        z1 = -x * sa + z * ca
        y2 = y * cb - z1 * sb
        z2 = y * sb + z1 * cb
        return x1, y2, z2

    def proyeksi(x: float, y: float, z: float) -> tuple[float, float]:
        x1, y2, z2 = putar(x, y, z)
        k = f_panjang / max(1.0, f_panjang - z2)
        return x1 * k, y2 * k

    return putar, proyeksi


# ----------------------------------------------------------------- tekstur ---
def bahan_dasar(ukuran: tuple[int, int], warna: tuple[int, int, int],
                kilap: float, langkah: int = 0) -> Image.Image:
    """Warna bahan + tenun halus supaya tidak terlihat cat datar.

    `langkah` = jarak garis dalam piksel tekstur. Dulu dihitung dari ukuran
    tekstur, sehingga muka sempit (chamfer 10 mm) jadi penuh garis vertikal
    dan terbaca seperti anyaman karung.
    """
    w, h = ukuran
    langkah = langkah or max(7, round(min(w, h) / 26))   # tenun selalu sama rapatnya
    im = Image.new("RGB", ukuran, warna)
    lapis = Image.new("L", ukuran, 0)
    d = ImageDraw.Draw(lapis)
    langkah = max(5, langkah)
    for y in range(0, h, langkah):
        d.line([(0, y), (w, y)], fill=5, width=1)
    for x in range(0, w, langkah):
        d.line([(x, 0), (x, h)], fill=4, width=1)
    lapis = lapis.filter(ImageFilter.GaussianBlur(0.6))
    im = ImageChops.subtract(im, Image.merge("RGB", (lapis, lapis, lapis)))
    if kilap > 0.02:
        im = K.kilau(im, kilap)
    return im


def gradien_vertikal(w: int, h: int, atas: float, bawah: float) -> Image.Image:
    jalur = Image.new("L", (1, h))
    for y in range(h):
        p = y / max(1, h - 1)
        jalur.putpixel((0, y), max(0, min(255, round(255 * (atas + (bawah - atas) * p)))))
    return jalur.resize((w, h), Image.BILINEAR)


def tempel_stiker(panel: Image.Image, lbl: Image.Image, g: dict) -> Image.Image:
    """Tempel label sebagai stiker 12 × 17 cm di tengah muka belakang.

    Detail yang membuatnya terbaca sebagai stiker, bukan cetakan langsung:
    tepi terang 1 px, bayangan tipis di bawah-tepi (lem menahan kertas),
    dan sedikit kilau di sisi yang kena lampu.
    """
    W, H = g["W"], g["H"]
    st = g["stiker"] or {}
    sw_mm = float(st.get("lebar", 120))
    sh_mm = float(st.get("tinggi", 170))
    cx = float(st.get("x", 0.5)) * W
    cy = float(st.get("y", 0.5)) * H

    pw, ph = panel.size
    sw = max(8, round(pw * sw_mm / W))
    sh = max(8, round(ph * sh_mm / H))
    x = round(pw * cx / W - sw / 2)
    y = round(ph * cy / H - sh / 2)

    stiker = lbl.resize((sw, sh), Image.LANCZOS)

    # bayangan stiker: lebih pekat di bawah & kanan (lampu dari kiri-atas)
    bayang = Image.new("L", (pw, ph), 0)
    db = ImageDraw.Draw(bayang)
    db.rectangle([x + 2, y + 3, x + sw + 3, y + sh + 4], fill=120)
    bayang = bayang.filter(ImageFilter.GaussianBlur(max(2, sw // 44)))
    gelap = Image.new("RGB", (pw, ph), (0, 0, 0))
    panel = Image.composite(gelap, panel, bayang.point(lambda v: int(v * 0.55)))
    panel.paste(stiker, (x, y))

    d = ImageDraw.Draw(panel, "RGBA")
    # tepi stiker: gelap tipis (kertas menempel di kain), plus kilau di sisi lampu
    d.rectangle([x, y, x + sw - 1, y + sh - 1], outline=(0, 0, 0, 90), width=1)
    d.line([(x, y), (x, y + sh - 1)], fill=(255, 255, 255, 40), width=1)
    d.line([(x, y), (x + sw - 1, y)], fill=(255, 255, 255, 30), width=1)
    d.line([(x + 1, y + sh - 1), (x + sw - 2, y + sh - 1)], fill=(0, 0, 0, 60), width=1)
    return panel


def gambar_valve(panel: Image.Image, g: dict) -> Image.Image:
    """Valve satu arah di muka depan: dasar gelap, cincin logam tipis, kubah + pantulan.

    Versi pertama menggambar tiga lingkaran penuh bertumpuk sehingga tampak
    seperti lubang bola. Yang benar: cincin sempit, kubah kecil di tengah,
    satu busur pantulan di sisi lampu, dan bayangan lembut di bawahnya.
    """
    W, H = g["W"], g["H"]
    v = g["valve"] or {}
    if not v.get("ada"):
        return panel
    pw, ph = panel.size
    S = 4                                          # gambar 4× lalu diperkecil: tepi halus
    r = max(6, round(pw * float(v.get("diameter", 15)) / W / 2))
    cx = round(pw * float(v.get("x", 0.5)))
    cy = round(ph * float(v.get("y_dari_atas", 52)) / H)

    def lingkaran_kanvas() -> Image.Image:
        return Image.new("RGBA", (w4, h4), (0, 0, 0, 0))

    w4, h4 = pw * S, ph * S
    lapis = lingkaran_kanvas()
    d = ImageDraw.Draw(lapis, "RGBA")
    R, X, Y = r * S, cx * S, cy * S

    # bayangan di bawah-kanan (lampu dari kiri-atas)
    d.ellipse([X - R * 1.06 + R * 0.10, Y - R * 1.06 + R * 0.16,
               X + R * 1.06 + R * 0.10, Y + R * 1.06 + R * 0.16], fill=(0, 0, 0, 70))
    # dasar valve: sedikit lebih gelap dari bahan, dengan tepi luar
    d.ellipse([X - R, Y - R, X + R, Y + R], fill=(46, 45, 42, 255))
    d.ellipse([X - R, Y - R, X + R, Y + R], outline=(10, 10, 10, 190),
              width=max(1, R // 7))
    # cincin
    d.ellipse([X - R * 0.82, Y - R * 0.82, X + R * 0.82, Y + R * 0.82],
              outline=(96, 93, 88, 230), width=max(1, R // 6))
    d.arc([X - R * 0.82, Y - R * 0.82, X + R * 0.82, Y + R * 0.82], 200, 330,
          fill=(190, 186, 178, 190), width=max(1, R // 5))
    # kubah tengah
    d.ellipse([X - R * 0.52, Y - R * 0.56, X + R * 0.50, Y + R * 0.46],
              fill=(68, 66, 62, 255))
    d.ellipse([X - R * 0.40, Y - R * 0.46, X + R * 0.10, Y - R * 0.02],
              fill=(120, 116, 109, 200))
    # batang tengah
    d.ellipse([X - R * 0.14, Y - R * 0.14, X + R * 0.14, Y + R * 0.14],
              fill=(28, 28, 26, 255))

    lapis = lapis.resize((pw, ph), Image.LANCZOS)
    kanvas = panel.convert("RGBA")
    kanvas.alpha_composite(lapis)
    return kanvas.convert("RGB")


def garis_zipper(panel: Image.Image, g: dict) -> Image.Image:
    """Jejak zipper 32 mm di bawah segel; hanya di area bahan (tidak menimpa stiker)."""
    W, H = g["W"], g["H"]
    pw, ph = panel.size
    y = round(ph * (g["segel"] + g["zipper"] * 0.55) / H)
    d = ImageDraw.Draw(panel, "RGBA")
    d.line([(0, y), (pw, y)], fill=(0, 0, 0, 46), width=max(1, ph // 700))
    d.line([(0, y + max(1, ph // 620)), (pw, y + max(1, ph // 620))],
           fill=(255, 255, 255, 34), width=max(1, ph // 800))
    return panel


def teks_panel(g: dict, lbl: Image.Image | None, jenis: str,
               px_lebar: int) -> Image.Image:
    """Tekstur satu muka panel selebar `px_lebar` piksel."""
    W, H = g["W"], g["H"]
    pw = max(4, px_lebar)
    ph = max(4, round(pw * H / W))
    warna = K.hex_rgb((g["bahan"] or {}).get("warna") or "#1B1A18")
    kilap = float((g["bahan"] or {}).get("kilap", 0.16))
    panel = bahan_dasar((pw, ph), warna, kilap)

    if jenis == "stiker" and lbl is not None:
        panel = tempel_stiker(panel, lbl, g)
    elif jenis == "depan":
        panel = gambar_valve(panel, g)

    panel = garis_zipper(panel, g)
    # pita segel di tepi atas: crimp halus, sedikit lebih gelap
    segel = max(2, round(ph * g["segel"] / H))
    d = ImageDraw.Draw(panel, "RGBA")
    d.rectangle([0, 0, pw, segel], fill=(255, 255, 255, 7))
    langkah = max(3, round(pw / 90))
    for x in range(0, pw, langkah):
        d.line([(x, 0), (x, segel)], fill=(255, 255, 255, 16), width=1)
    d.line([(0, segel), (pw, segel)], fill=(0, 0, 0, 90), width=max(1, ph // 700))
    d.line([(0, segel + max(1, ph // 700)), (pw, segel + max(1, ph // 700))],
           fill=(255, 255, 255, 30), width=max(1, ph // 900))

    # gradien: kiri dekat lampu lebih terang, dan bagian bawah sedikit lebih gelap
    gx = Image.new("L", (pw, 1))
    for x in range(pw):
        p = x / max(1, pw - 1)
        # sorot dari kiri-atas: puncak ±0,30 lebar, turun ke tepi kanan
        sorot = 0.80 + 0.24 * math.exp(-((p - 0.30) / 0.34) ** 2) - 0.10 * max(0.0, p - 0.62)
        gx.putpixel((x, 0), max(0, min(255, round(255 * sorot))))
    gx = gx.resize((pw, ph), Image.BILINEAR)
    gy = gradien_vertikal(pw, ph, 1.0, 0.93)
    topeng = ImageChops.multiply(gx, gy)
    return ImageChops.multiply(panel, Image.merge("RGB", (topeng, topeng, topeng)))


def teks_sisi(g: dict, px_lebar: int, cahaya: float = 1.0,
              lipat: bool = True, langkah: int = 8) -> Image.Image:
    """Tekstur muka samping: bahan + lipatan gusset di tengah + gelap ke belakang."""
    W, H, D = g["W"], g["H"], g["D"]
    sisi_mm = g["sisi"]
    pw = max(3, px_lebar)
    ph = max(4, round(pw * H / sisi_mm))
    warna = K.hex_rgb((g["bahan"] or {}).get("warna") or "#1B1A18")
    im = bahan_dasar((pw, ph), warna, float((g["bahan"] or {}).get("kilap", 0.16)),
                     langkah=langkah)
    d = ImageDraw.Draw(im, "RGBA")
    if lipat and pw >= 26:
        # lipatan gusset: satu garis terang + satu gelap di tengah sisi
        d.line([(pw * 0.5, 0), (pw * 0.5, ph)], fill=(255, 255, 255, 34),
               width=max(1, pw // 26))
        d.line([(pw * 0.5 + max(1, pw // 34), 0), (pw * 0.5 + max(1, pw // 34), ph)],
               fill=(0, 0, 0, 52), width=max(1, pw // 34))
    # tepi muka: sedikit gelap (sudut terlipat), proporsional terhadap lebar muka
    tepi = max(2, min(pw // 5, 18))
    for i in range(tepi):
        alfa = int(86 * (1 - i / tepi))
        d.line([(i, 0), (i, ph)], fill=(0, 0, 0, alfa), width=1)
        d.line([(pw - 1 - i, 0), (pw - 1 - i, ph)], fill=(0, 0, 0, alfa), width=1)
    # segel atas
    segel = max(2, round(ph * g["segel"] / H))
    d.rectangle([0, 0, pw, segel], fill=(0, 0, 0, 30))
    if abs(cahaya - 1.0) > 0.01:
        skala = Image.new("L", im.size, max(0, min(255, round(255 * cahaya))))
        im = ImageChops.multiply(im, Image.merge("RGB", (skala, skala, skala)))
    return im


# ------------------------------------------------------------------- render ---
def render(g: dict, lbl: Image.Image | None, tinggi_px: int, yaw: float,
           pitch: float = PITCH) -> Image.Image:
    """Render pouch ke kanvas RGBA transparan, sisi terpanjang = tinggi_px."""
    S = SUPERSAMPLE
    h = tinggi_px * S
    w = round(h * g["W"] / g["H"])
    f_mm = max(g["W"], g["H"]) * 3.4           # jarak kamera dalam mm
    skala = h / g["H"]                          # mm → piksel
    putar, proyeksi_mm = proyeksi_kamera(yaw, pitch, f_mm)

    def proyeksi(x: float, y: float, z: float) -> tuple[float, float]:
        px_, py_ = proyeksi_mm(x, y, z)
        return px_ * skala, py_ * skala
    pts = penampang(g)
    H2, kt = g["H"] / 2, g["kt"]

    teks: dict[str, Image.Image] = {
        "depan": teks_panel(g, lbl, "depan", round(w * 1.4)),
        "stiker": teks_panel(g, lbl, "stiker", round(w * 1.4)),
        "sisi_kanan": teks_sisi(g, max(10, round(w * 1.4 * g["sisi"] / g["W"])), 0.74),
        "sisi_kiri": teks_sisi(g, max(10, round(w * 1.4 * g["sisi"] / g["W"])), 1.0),
        "chamfer_kanan": teks_sisi(g, max(8, round(w * 1.4 * g["chamfer"] / g["W"])), 0.62,
                                   lipat=False, langkah=14),
        "chamfer_kiri": teks_sisi(g, max(8, round(w * 1.4 * g["chamfer"] / g["W"])), 1.08,
                                  lipat=False, langkah=14),
    }

    muka = []
    for i, j, nama, normal in MUKA:
        (xi, zi), (xj, zj) = pts[i], pts[j]
        quad3 = [(xi, -H2, zi * kt), (xj, -H2, zj * kt),
                 (xj, H2, zj), (xi, H2, zi)]
        nx, ny, nz = putar(*normal)
        if nz <= 1e-6:                                    # membelakangi kamera
            continue
        z_rata = sum(putar(*p)[2] for p in quad3) / 4
        muka.append((z_rata, nama, [proyeksi(*p) for p in quad3]))

    semua = [p for _, _, q in muka for p in q]
    pad = 3 * S
    x0 = min(p[0] for p in semua) - pad
    x1 = max(p[0] for p in semua) + pad
    y0 = min(p[1] for p in semua) - pad
    y1 = max(p[1] for p in semua) + pad
    W, H = math.ceil(x1 - x0), math.ceil(y1 - y0)
    kanvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    for _, nama, quad in sorted(muka, key=lambda t: t[0]):
        tex = teks[nama]
        lt, rt, rb, lb = [(p[0] - x0, p[1] - y0) for p in quad]
        # muka belakang terlihat dari luar: urutan tekstur harus dicerminkan
        luas = ((rt[0] - lt[0]) * (lb[1] - lt[1]) - (lb[0] - lt[0]) * (rt[1] - lt[1]))
        if luas < 0:
            tex = tex.transpose(Image.FLIP_LEFT_RIGHT)
        koef = K.homografi([(0, 0), (tex.width, 0), (tex.width, tex.height),
                            (0, tex.height)], [lt, rt, rb, lb])
        lapis = tex.transform((W, H), Image.PERSPECTIVE, koef, Image.BICUBIC)
        S2 = 4
        besar = Image.new("L", (W * S2, H * S2), 0)
        ImageDraw.Draw(besar).polygon([(p[0] * S2, p[1] * S2) for p in (lt, rt, rb, lb)],
                                      fill=255)
        topeng = besar.resize((W, H), Image.LANCZOS)
        kanvas.paste(lapis, (0, 0), topeng)

    kanvas = kanvas.resize((max(1, W // S), max(1, H // S)), Image.LANCZOS)
    return kanvas


def bidang(g: dict, lbl: Image.Image | None, jenis: str, tinggi: int) -> Image.Image:
    """Muka datar untuk `rak/`: tanpa perspektif, transparan di luar bentuk."""
    if jenis == "muka":
        return teks_panel(g, lbl, "stiker", round(tinggi * g["W"] / g["H"])).convert("RGBA")
    lebar = round(tinggi * g["sisi"] / g["H"])
    tex = teks_sisi(g, lebar, 0.8)
    topeng = Image.new("L", tex.size, 255)
    img = tex.convert("RGBA")
    img.putalpha(topeng)
    return img


# ------------------------------------------------------------------ keluaran ---
def render_sku(p: dict, sp: dict) -> dict:
    g = geometri(sp)
    lbl = K.label(p["id"])
    if lbl is None:
        return {"id": p["id"], "status": "tanpa label"}
    os.makedirs(KELUAR, exist_ok=True)
    os.makedirs(PASAR, exist_ok=True)
    os.makedirs(POUCH, exist_ok=True)

    keluaran, tinggi_obj = {}, 0
    for sudut in SUDUT:
        obj = render(g, lbl, 1150, sudut)
        im, kk = K.bingkai((KATALOG, KATALOG), obj, OBJEK, 0.5, 0.82)
        nama = f'{p["id"]}-{abs(sudut)}.jpg'
        jalur = os.path.join(KELUAR, nama)
        im.save(jalur, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
        tinggi_obj = max(tinggi_obj, kk[3] - kk[1])
        keluaran[abs(sudut)] = {"berkas": f"assets/img/katalog/{nama}",
                                "kotak": list(kk),
                                "kb": round(os.path.getsize(jalur) / 1024, 1)}

    obj = render(g, lbl, 1150, -16)
    hero, kh = K.bingkai(HERO, obj, OBJEK_HERO, 0.68, 0.84)
    jalur = os.path.join(KELUAR, f'{p["id"]}-hero.jpg')
    hero.save(jalur, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
    keluaran["hero"] = {"berkas": f'assets/img/katalog/{p["id"]}-hero.jpg',
                        "kotak": list(kh), "kb": round(os.path.getsize(jalur) / 1024, 1)}

    pasar_keluar = {}
    for kunci, ukuran, skala in (("1x1", (1000, 1000), 0.82), ("4x5", (1080, 1350), 0.74)):
        obj_p = render(g, lbl, 1100, 0)
        im_p = K.pasar(ukuran, obj_p, skala, 0.5, 0.88)
        nama_p = f'{p["id"]}-{kunci}.jpg'
        jalur_p = os.path.join(PASAR, nama_p)
        im_p.save(jalur_p, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
        pasar_keluar[kunci] = {"berkas": f"assets/img/katalog/pasar/{nama_p}",
                               "kb": round(os.path.getsize(jalur_p) / 1024, 1),
                               "ukuran": list(ukuran)}

    # muka pemakaian lain: valve (muka depan) dan dua muka datar untuk rak
    other = {}
    obj_v = render(g, lbl, 2000, 180)
    im_v, kv = K.bingkai((KATALOG, KATALOG), obj_v, 0.70, 0.5, 0.84)
    jalur_v = os.path.join(POUCH, f'{p["id"]}-valve.jpg')
    im_v.save(jalur_v, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
    other["valve"] = {"berkas": f'assets/img/pouch/{p["id"]}-valve.jpg',
                      "kotak": list(kv), "kb": round(os.path.getsize(jalur_v) / 1024, 1)}

    for jenis in ("muka", "sisi"):
        im_f = bidang(g, lbl, jenis, 1200)
        jalur_f = os.path.join(POUCH, f'{p["id"]}-{jenis}.png')
        im_f.save(jalur_f, optimize=True)
        other[jenis] = {"berkas": f'assets/img/pouch/{p["id"]}-{jenis}.png',
                        "kb": round(os.path.getsize(jalur_f) / 1024, 1),
                        "ukuran": list(im_f.size)}

    u = sp["aktif"]
    return {
        "id": p["id"], "nama": p["name"], "status": "siap",
        "ukuran": u["kunci"],
        "geometri": {k: u[k] for k in ("lebar", "tinggi", "gusset", "segel", "zipper")},
        "sisi": u.get("sisi"), "bentuk": u.get("bentuk", "flat-bottom"),
        "bahan": (sp.get("bahan") or {}).get("nama", "—"),
        "stiker": sp.get("stiker"), "valve": sp.get("valve"),
        "tinggi_objek_px": tinggi_obj, "keluaran": keluaran, "pasar": pasar_keluar,
        "pouch": other,
    }


def lembar(hasil: list[dict]) -> None:
    ikon, kepala, kaki = 300, 58, 26
    baris = [h for h in hasil if h["status"] == "siap"]
    W = ikon * len(SUDUT) + 40
    H = kepala + (ikon + kaki) * len(baris) + 20
    lembar_im = Image.new("RGB", (W, H), K.PAPER)
    d = ImageDraw.Draw(lembar_im)
    try:
        from PIL import ImageFont
        f_k = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-600-normal.ttf"), 15)
        f_j = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-500-normal.ttf"), 13)
    except OSError:
        f_k = f_j = ImageFont.load_default()
    d.text((20, 20), "KEMASAN 500 g FLAT-BOTTOM — STIKER 12 × 17 cm DI TENGAH BELAKANG",
           font=f_k, fill=K.TINTA)
    d.text((W - 190, 22), "tools/pouch.py", font=f_j, fill=(109, 106, 99))
    for i, h in enumerate(baris):
        y = kepala + i * (ikon + kaki)
        d.text((20, y + 4), h["nama"].upper(), font=f_k, fill=K.TINTA)
        for j, sudut in enumerate(SUDUT):
            k = h["keluaran"][abs(sudut)]
            im = Image.open(os.path.join(ROOT, k["berkas"]))
            im.thumbnail((ikon - 16, ikon - 16), Image.LANCZOS)
            x = 20 + j * ikon
            lembar_im.paste(im, (x, y + kaki))
            d.rectangle([x, y + kaki, x + ikon - 8, y + kaki + ikon - 8],
                        outline=(220, 216, 208))
            d.text((x + 2, y + kaki + ikon - 6), f'{sudut}°', font=f_j, fill=(109, 106, 99))
        d.line([20, y + ikon + kaki + 6, W - 20, y + ikon + kaki + 6], fill=(222, 218, 210))
    lembar_im.save(LEMBAR, optimize=True)


def spesimen(sp: dict) -> None:
    """Satu lembar: muka stiker, muka valve, 3/4 — supaya bisa dicocokkan ke kemasan asli."""
    g = geometri(sp)
    lbl = K.label("gayo")
    f_k = f_j = None
    try:
        from PIL import ImageFont
        f_k = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-600-normal.ttf"), 20)
        f_j = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-400-normal.ttf"), 17)
    except OSError:
        f_k = f_j = ImageFont.load_default()
    ubin = [("muka stiker (belakang)", 0), ("muka valve (depan)", 180), ("3/4", -18)]
    kanvas = Image.new("RGB", (1560, 1240), K.PAPER_TERANG)
    x = 40
    for judul, yaw in ubin:
        obj = render(g, lbl, 900, yaw)
        dasar = 1000
        sh = Image.new("L", kanvas.size, 0)
        ox = x + (400 - obj.width) // 2
        ImageDraw.Draw(sh).ellipse([ox - obj.width // 6, dasar - 12,
                                    ox + obj.width + obj.width // 5, dasar + 42], fill=110)
        sh = sh.filter(ImageFilter.GaussianBlur(20))
        kanvas = Image.composite(Image.new("RGB", kanvas.size, (58, 46, 36)), kanvas,
                                 sh.point(lambda v: int(v * 0.55)))
        kanvas.paste(obj, (ox, dasar - obj.height), obj)
        d = ImageDraw.Draw(kanvas)
        d.text((x, 1050), judul, font=f_k, fill=K.TINTA)
        d.text((x, 1082), f"{uy if False else ''}", font=f_j, fill=K.PAPER)
        x += 500
    d = ImageDraw.Draw(kanvas)
    u = sp["aktif"]
    d.text((40, 34), "SPESIMEN KEMASAN 500 g — FLAT-BOTTOM, VALVE DEPAN, STIKER BELAKANG",
           font=f_k, fill=K.TINTA)
    d.text((40, 68), f"{u['lebar']} × {u['tinggi']} mm · sisi {u.get('sisi', '—')} mm · "
                     f"stiker {(sp.get('stiker') or {}).get('lebar')} × "
                     f"{(sp.get('stiker') or {}).get('tinggi')} mm di tengah · "
                     f"bahan {(sp.get('bahan') or {}).get('warna')} "
                     f"{(sp.get('bahan') or {}).get('nama', '')}", font=f_j, fill=(109, 106, 99))
    d.text((40, 1120), "Ukuran & stiker dari pemilik. Ketebalan sisi/chamfer masih asumsi — "
                       "ganti di data/kemasan-katalog.json bila sudah diukur.", font=f_j,
           fill=(109, 106, 99))
    kanvas.save(SPESIMEN, optimize=True)
    print(f"  spesimen   laporan/pouch-spesimen.png · {os.path.getsize(SPESIMEN)/1024:.0f} KB")


def cek() -> list[str]:
    m: list[str] = []
    if not os.path.exists(DATA):
        return ["data/katalog-render.json belum ada — jalankan python3 tools/pouch.py"]
    with open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    siap = [s for s in d["sku"] if s["status"] == "siap"]
    if len(siap) != 9:
        m.append(f"{len(siap)} SKU dirender, seharusnya 9")
    sp = K.spek()
    u = sp["aktif"]
    for s in siap:
        if s.get("bentuk") != "flat-bottom":
            m.append(f'{s["id"]}: bukan flat-bottom')
        g_ = s.get("geometri") or {}
        if g_.get("lebar") != u["lebar"] or g_.get("tinggi") != u["tinggi"]:
            m.append(f'{s["id"]}: geometri foto {g_} ≠ spesifikasi '
                     f'{u["lebar"]}×{u["tinggi"]}')
        for kunci, e in (s.get("pouch") or {}).items():
            if not os.path.exists(os.path.join(ROOT, e["berkas"])):
                m.append(f'{s["id"]}: {e["berkas"]} tidak ada')
        for kunci, e in (s.get("pasar") or {}).items():
            jalur = os.path.join(ROOT, e["berkas"])
            if not os.path.exists(jalur):
                m.append(f'{s["id"]} pasar/{kunci}: tidak ada')
                continue
            with Image.open(jalur) as im:
                for titik in ((0, 0), (im.width - 1, 0)):
                    if min(im.convert("RGB").getpixel(titik)) < 250:
                        m.append(f'{s["id"]} pasar/{kunci}: latar bukan putih murni')
                        break
    if not os.path.exists(LEMBAR):
        m.append("laporan/katalog-render.png belum ada")
    if not os.path.exists(SPESIMEN):
        m.append("laporan/pouch-spesimen.png belum ada")
    return m


if __name__ == "__main__":
    if "--cek" in sys.argv:
        mm = cek()
        for x in mm:
            print("  ✗", x)
        print("  kesimpulan:", "OK · 9 SKU kemasan 500 g flat-bottom, stiker belakang"
              if not mm else f"{len(mm)} masalah")
        sys.exit(0 if not mm else 1)

    sp = K.spek()
    u = sp["aktif"]
    print(f'  kemasan    {u.get("berat", u["kunci"])} · {u["lebar"]}×{u["tinggi"]} mm · '
          f'sisi {u.get("sisi")} mm · segel {u["segel"]} · zipper {u["zipper"]}')
    print(f'  bahan      {(sp.get("bahan") or {}).get("warna")} '
          f'({(sp.get("bahan") or {}).get("nama")})')
    print(f'  stiker     {(sp.get("stiker") or {}).get("lebar")} × '
          f'{(sp.get("stiker") or {}).get("tinggi")} mm di tengah muka belakang · '
          f'valve {"ada" if (sp.get("valve") or {}).get("ada") else "tidak"} di muka depan')

    produk = K.baca_catalog()
    if "--satu" in sys.argv:
        kriteria = sys.argv[sys.argv.index("--satu") + 1]
        produk = [p for p in produk if p["id"] == kriteria]
    hasil = [render_sku(p, sp) for p in produk]
    K.tulis_data(hasil)
    K.tulis_js(hasil)
    lembar(hasil)
    spesimen(sp)
    total = sum(e["kb"] for s in hasil if s["status"] == "siap"
                for e in {**s["keluaran"], **s.get("pouch", {})}.values())
    print(f'  SKU        {len([h for h in hasil if h["status"] == "siap"])} · '
          f'{len(SUDUT)} sudut + hero + valve + 2 muka rak · {total/1024:.1f} MB')
    print(f'  lembar     laporan/katalog-render.png · {os.path.getsize(LEMBAR)/1024:.0f} KB')
    for x in cek():
        print("  ✗", x)
