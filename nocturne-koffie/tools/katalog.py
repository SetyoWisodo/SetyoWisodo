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
    lapis = lapis.filter(ImageFilter.GaussianBlur(max(3, (y1 - y0) // 3)))
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


def kotak(muka: Image.Image, tinggi: int, yaw: float, pitch: float = -5.0) -> Image.Image:
    """Bangun kotak kemasan bervolume dengan proyeksi sungguhan, lalu miringkan `yaw`.

    Tiga muka: depan (label, dipetakan ke segi empat hasil proyeksi), sisi
    (warna tepi label, digelapkan), atas (pita tipis lebih terang). Muka yang
    menghadap kamera digambar terakhir. Dua kali render (supersample) supaya
    tepinya tidak bergerigi.
    """
    S = 2                                     # supersample
    rasio = muka.height / muka.width
    h = tinggi * S
    w = max(2, round(h / rasio))
    d = max(3, round(w * KETEBALAN))

    a, b = math.radians(yaw), math.radians(pitch)
    ca, sa, cb, sb = math.cos(a), math.sin(a), math.cos(b), math.sin(b)
    f = max(w, h) * 2.6                       # panjang fokus (proyeksi lemah)

    def proyeksi(x: float, y: float, z: float) -> tuple[float, float]:
        # putar Y lalu X
        x1 = x * ca + z * sa
        z1 = -x * sa + z * ca
        y2 = y * cb - z1 * sb
        z2 = y * sb + z1 * cb
        k = f / (f + z2)
        return x1 * k, y2 * k

    def muka_kotak(z: float) -> list:
        return [((-w / 2, -h / 2, z), (w / 2, -h / 2, z), (w / 2, h / 2, z), (-w / 2, h / 2, z))]

    depan_q = [proyeksi(*v) for v in muka_kotak(d / 2)[0]]
    # sisi kanan (x = +w/2) dan kiri (x = −w/2)
    sisi_kanan = [proyeksi(w / 2, -h / 2, d / 2), proyeksi(w / 2, -h / 2, -d / 2),
                  proyeksi(w / 2, h / 2, -d / 2), proyeksi(w / 2, h / 2, d / 2)]
    sisi_kiri = [proyeksi(-w / 2, -h / 2, -d / 2), proyeksi(-w / 2, -h / 2, d / 2),
                 proyeksi(-w / 2, h / 2, d / 2), proyeksi(-w / 2, h / 2, -d / 2)]
    atas = [proyeksi(-w / 2, -h / 2, -d / 2), proyeksi(w / 2, -h / 2, -d / 2),
            proyeksi(w / 2, -h / 2, d / 2), proyeksi(-w / 2, -h / 2, d / 2)]

    semua = depan_q + sisi_kanan + sisi_kiri + atas
    xs = [q[0] for q in semua]
    ys = [q[1] for q in semua]
    pad = 4 * S
    x0, x1 = min(xs) - pad, max(xs) + pad
    y0, y1 = min(ys) - pad, max(ys) + pad
    W, H = math.ceil(x1 - x0), math.ceil(y1 - y0)

    def tembak(tekstur: Image.Image, quad: list) -> tuple[Image.Image, Image.Image]:
        """Petakan tekstur ke segi empat (kiri-atas, kanan-atas, kanan-bawah, kiri-bawah)."""
        lt, rt, rb, lb = [(q[0] - x0, q[1] - y0) for q in quad]
        koef = homografi([(0, 0), (tekstur.width, 0), (tekstur.width, tekstur.height),
                          (0, tekstur.height)], [lt, rt, rb, lb])
        lapis = tekstur.transform((W, H), Image.PERSPECTIVE, koef, Image.BICUBIC)
        # topeng digambar 4× lalu diperkecil: tepi polygon jadi halus, bukan bergerigi
        S2 = 4
        besar = Image.new("L", (W * S2, H * S2), 0)
        ImageDraw.Draw(besar).polygon(
            [(x * S2, y * S2) for x, y in (lt, rt, rb, lb)], fill=255)
        topeng = besar.resize((W, H), Image.LANCZOS)
        return lapis, topeng

    # --- tekstur tiga muka
    depan_tex = cahaya(muka.resize((w, h), Image.LANCZOS), yaw)

    # sisi & atas = papan karton tanpa cetak. Warnanya diambil dari kertas label
    # (median 4 sudut), lalu digelapkan dengan gradien ke arah jauh dari cahaya.
    def kertas_papan() -> tuple[int, int, int]:
        px = [muka.getpixel((x, y)) for x in (3, muka.width - 4)
              for y in (3, muka.height - 4)]
        return tuple(int(sum(p[i] for p in px) / len(px) * 0.92) for i in range(3))

    papan = kertas_papan()
    tw = max(3, int(d))
    th_sisi = h
    sisi_tex = Image.new("RGB", (tw, th_sisi), papan)
    grad = Image.new("L", (tw, 1))
    for x in range(tw):
        q = x / max(1, tw - 1)                      # 0 = tepi depan
        if yaw >= 0:                                # sisi kanan: jauh dari cahaya
            v = 255 * (0.62 - 0.30 * q)
        else:                                       # sisi kiri: kena key light
            v = 255 * (0.96 - 0.34 * q)
        grad.putpixel((x, 0), max(0, min(255, round(v))))
    grad = grad.resize((tw, th_sisi), Image.BILINEAR)
    sisi_tex = ImageChops.multiply(sisi_tex, Image.merge("RGB", (grad, grad, grad)))

    atas_tex = Image.new("RGB", (w, tw), papan)
    ga = Image.new("L", (w, 1))
    for x in range(w):
        q = x / max(1, w - 1)
        ga.putpixel((x, 0), max(0, min(255, round(255 * (1.02 - 0.20 * q)))))
    ga = ga.resize((w, tw), Image.BILINEAR)
    atas_tex = ImageChops.multiply(atas_tex, Image.merge("RGB", (ga, ga, ga)))

    # --- gambar dari yang paling jauh
    urut = []
    if yaw > 0.5:
        urut.append((sisi_kanan, sisi_tex))
    elif yaw < -0.5:
        urut.append((sisi_kiri, sisi_tex))
    urut.append((atas, atas_tex))
    urut.append((depan_q, depan_tex))

    # cermin tekstur sisi bila yang terlihat sisi kiri
    kanvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for quad, tex in urut:
        if quad is sisi_kiri:
            tex = tex.transpose(Image.FLIP_LEFT_RIGHT)
        lapis, topeng = tembak(tex, quad)
        kanvas.paste(lapis, (0, 0), topeng)

    # hanya sambungan depan↔sisi yang digambar: garis tipis di tepi muka depan.
    # (menggambar semua sisi membuat garis melintang menembus label)
    if abs(yaw) > 0.5:
        dg = ImageDraw.Draw(kanvas)
        tepi = (depan_q[1], depan_q[2]) if yaw > 0 else (depan_q[0], depan_q[3])
        dg.line([(q[0] - x0, q[1] - y0) for q in tepi], fill=(150, 142, 128), width=1)

    # pangkas tepat ke batas geometri (bukan menebak dari warna latar — gradasi
    # kertas hampir sewarna, jadi ambang warna bisa salah)
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
    lx0, lx1 = x0 - tw // 7, x0 + tw + tw // 4
    ly0, ly1 = bawah - max(8, th // 30), bawah + max(16, th // 9)
    sh = bayangan((W, H), (lx0, ly0, lx1, ly1), 96)
    gelap = Image.new("RGB", (W, H), (58, 46, 36))
    latar = Image.composite(gelap, latar, sh.point(lambda v: int(v * 0.62)))
    # bayangan kontak: elips sempit tepat di bawah objek, lebih pekat
    kx = Image.new("L", (W, H), 0)
    ImageDraw.Draw(kx).ellipse([x0 - tw // 12, bawah - max(3, th // 70),
                                x0 + tw + tw // 12, bawah + max(5, th // 34)], fill=210)
    kx = kx.filter(ImageFilter.GaussianBlur(max(2, th // 90)))
    latar = Image.composite(Image.new("RGB", (W, H), (44, 34, 26)), latar, kx)
    latar.paste(o, (x0, y0), o.split()[3] if o.mode == "RGBA" else None)
    return latar, (x0, y0, x0 + tw, y0 + th)


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
def render_sku(p: dict) -> dict:
    muka = label(p["id"])
    if muka is None:
        return {"id": p["id"], "status": "tanpa label"}
    os.makedirs(KELUAR, exist_ok=True)
    keluaran = {}
    tinggi_obj = 0
    for sudut in SUDUT:
        # tinggi objek di ruang render: sedikit lebih besar dari tinggi akhir
        o = kotak(muka, 1100, sudut)
        im, kk = bingkai((KATALOG, KATALOG), o, OBJEK_KATALOG, 0.5, 0.82)
        nama = f'{p["id"]}-{abs(sudut)}.jpg'
        jalur = os.path.join(KELUAR, nama)
        im.save(jalur, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
        tinggi_obj = max(tinggi_obj, kk[3] - kk[1])
        keluaran[abs(sudut)] = {"berkas": f"assets/img/katalog/{nama}",
                                "kotak": list(kk),
                                "kb": round(os.path.getsize(jalur) / 1024, 1)}
    o = kotak(muka, 1150, -16)
    hero, kh = bingkai(HERO, o, OBJEK_HERO, 0.68, 0.84)
    nama_hero = f'{p["id"]}-hero.jpg'
    jalur = os.path.join(KELUAR, nama_hero)
    hero.save(jalur, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
    keluaran["hero"] = {"berkas": f"assets/img/katalog/{nama_hero}", "kotak": list(kh),
                        "kb": round(os.path.getsize(jalur) / 1024, 1)}
    return {"id": p["id"], "nama": p["name"], "status": "siap",
            "tinggi_objek_px": tinggi_obj, "keluaran": keluaran}


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
        })
    isi = {
        "keterangan": "Dibangun tools/katalog.py dari data/catalog.json + assets/img/katalog. "
                      "Harga = varian terkecil; jangan diketik di JS.",
        "rig": {"sudut": list(SUDUT), "katalog_px": KATALOG, "hero_px": list(HERO)},
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
    if tinggi:
        sebar = (max(tinggi) - min(tinggi)) / max(tinggi)
        if sebar > 0.08:
            m.append(f"tinggi objek antar SKU berbeda {sebar:.0%} — satu rig harus konsisten (≤ 8%)")
    if not os.path.exists(LEMBAR):
        m.append("laporan/katalog-render.png belum ada")
    return m


if __name__ == "__main__":
    if "--cek" in sys.argv:
        mm = cek()
        for x in mm:
            print("  ✗", x)
        print("  kesimpulan:", "OK · 9 SKU × 3 sudut + hero, satu rig" if not mm else f"{len(mm)} masalah")
        sys.exit(0 if not mm else 1)
    produk = baca_catalog()
    if "--satu" in sys.argv:
        kriteria = sys.argv[sys.argv.index("--satu") + 1]
        produk = [p for p in produk if p["id"] == kriteria]
    hasil = [render_sku(p) for p in produk]
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
