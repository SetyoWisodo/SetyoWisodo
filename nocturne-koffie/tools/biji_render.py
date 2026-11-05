#!/usr/bin/env python3
"""Pasang render biji kopi 3D ke halaman.

Sejak 5 Nov 2026 bentuk biji bukan lagi mesh parametrik yang digambar sendiri,
melainkan **render hiper-realistis** (satu biji Arabika medium roast). Alasannya
jujur: mesh 640×800 hasil `tools/biji.py` terbaca seperti gumpalan cokelat
mengilap — pemilik menyebutnya "sangat aneh". Render ini menggantikannya.

Yang dikerjakan skrip ini (bukan generator gambar — gambarnya dibuat di luar):

   1. menyamakan warna latar render dengan kertas brief (#F5EFE4), supaya
      gambar menyatu dengan halaman dan tidak tampak sebagai kotak;
   2. memotong ke rasio 4:5 lalu mengecilkan ke 640×800;
   3. memeriksa bahwa keenam titik zona benar-benar jatuh di atas biji
      (pikselnya bukan latar) dan tidak saling menumpuk;
   4. meratakan derau latar ke warna kertas, supaya gambar tidak tampak
      sebagai kotak di atas halaman;
   5. menulis `assets/img/biji-3d-poster.webp` + `laporan/biji-render.json`.

Sumber render: `assets/img/biji-render-02.png` (928×1152).
Titik zona disimpan di `data/biji3d.json` pada kunci `titik_foto` (persen).

Pakai:
    python3 tools/biji_render.py          # tulis poster + laporan
    python3 tools/biji_render.py --cek    # periksa saja
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from PIL import Image, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMBER = os.path.join(ROOT, "assets", "img", "biji-render-02.png")
POSTER = os.path.join(ROOT, "assets", "img", "biji-3d-poster.webp")
DATA = os.path.join(ROOT, "data", "biji3d.json")
LAPORAN = os.path.join(ROOT, "laporan", "biji-render.json")

KERTAS = (245, 239, 228)   # --paper #F5EFE4 dari data/design-system.json
LEBAR, TINGGI = 640, 800
KUALITAS = 82          # WebP: foto + alfa, 66 KB (PNG 640×800 = 600 KB lebih)
TOLERANSI_DERAU = 6    # piksel sedekat ini ke warna kertas dianggap latar bersih


def baca_data() -> dict:
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def warna_latar(im: Image.Image) -> tuple[int, int, int]:
    """Median warna di bingkai 12 px terluar — di situlah latar polos."""
    w, h = im.size
    potong = 12
    bagian = [
        im.crop((0, 0, w, potong)),
        im.crop((0, h - potong, w, h)),
        im.crop((0, 0, potong, h)),
        im.crop((w - potong, 0, w, h)),
    ]
    total = [0, 0, 0]
    n = 0
    for b in bagian:
        st = ImageStat.Stat(b)
        for i in range(3):
            total[i] += st.median[i] * (b.width * b.height)
        n += b.width * b.height
    return tuple(int(round(t / n)) for t in total)  # type: ignore[return-value]


def samakan_latar(im: Image.Image) -> tuple[Image.Image, dict]:
    """Geser tiap kanal supaya latar tepat sama dengan warna kertas."""
    asal = warna_latar(im)
    selisih = [KERTAS[i] - asal[i] for i in range(3)]

    kanal = list(im.split())
    for i in range(3):
        if selisih[i]:
            kanal[i] = kanal[i].point(lambda v, d=selisih[i]: max(0, min(255, v + d)))
    hasil = Image.merge("RGB", kanal)
    return hasil, {"latar_asal": asal, "selisih": selisih, "latar_akhir": warna_latar(hasil)}


def potong_4_5(im: Image.Image) -> Image.Image:
    w, h = im.size
    target = w / (LEBAR / TINGGI)     # tinggi ideal untuk lebar ini
    if target <= h:
        atas = int(round((h - target) / 2))
        im = im.crop((0, atas, w, atas + int(round(target))))
    else:
        lebar = h * (LEBAR / TINGGI)
        kiri = int(round((w - lebar) / 2))
        im = im.crop((kiri, 0, kiri + int(round(lebar)), h))
    return im.resize((LEBAR, TINGGI), Image.LANCZOS)


def rapikan_latar(im: Image.Image) -> Image.Image:
    """Ratakan vignette latar studio ke warna kertas, tanpa menyentuh biji.

    Render punya latar bergradasi halus (sudut ±235, tengah ±245). Satu
    pergeseran global tidak cukup; memotong latar jadi transparan menyisakan
    pita derau; dan mengoreksi semua piksel membuat biji ikut pucat. Jadi:

      1. latar diperkirakan dengan bidang kuadratik yang dipasang hanya pada
         sel-sel terang (sel yang isinya biji tidak dipakai);
      2. koreksi diterapkan hanya pada piksel yang dekat dengan bidang itu —
         biji yang jauh lebih gelap tidak tersentuh;
      3. sisa derau di dekat warna kertas disetel tepat ke kertas.
    """
    import numpy as np

    a = np.asarray(im.convert("RGB")).astype("float32")
    h, w = a.shape[:2]
    kertas = np.array(KERTAS, dtype="float32")
    luma = a[:, :, 0] * 0.299 + a[:, :, 1] * 0.587 + a[:, :, 2] * 0.114

    # 1 · sampel latar: sel 20 px yang mayoritas terang
    sel = 20
    xs, ys, vals = [], [], []
    for y0 in range(0, h - sel + 1, sel):
        for x0 in range(0, w - sel + 1, sel):
            blok = luma[y0:y0 + sel, x0:x0 + sel]
            if float(np.percentile(blok, 50)) < 215:
                continue                      # sel ini berisi biji — lewati
            piksel = a[y0:y0 + sel, x0:x0 + sel].reshape(-1, 3)
            xs.append(x0 + sel / 2)
            ys.append(y0 + sel / 2)
            vals.append(np.percentile(piksel, 85, axis=0))
    if len(xs) < 8:
        return im                              # latar tidak terbaca: biarkan apa adanya

    xs = np.array(xs) / w
    ys = np.array(ys) / h
    vals = np.array(vals)
    A = np.column_stack([np.ones_like(xs), xs, ys, xs * xs, xs * ys, ys * ys])

    bidang = np.zeros((h, w, 3), dtype="float32")
    yy, xx = np.mgrid[0:h, 0:w]
    xx = xx / w
    yy = yy / h
    M = np.stack([np.ones_like(xx), xx, yy, xx * xx, xx * yy, yy * yy], axis=-1)
    for c in range(3):
        koef, *_ = np.linalg.lstsq(A, vals[:, c], rcond=None)
        bidang[:, :, c] = M @ koef

    # 2 · koreksi hanya di dekat latar
    defisit = kertas - bidang
    jarak = np.abs(a - bidang).max(axis=2)
    bobot = np.clip(1.0 - (jarak - 8.0) / 16.0, 0.0, 1.0)[:, :, None]
    hasil = np.clip(a + defisit * bobot, 0, 255)

    # 3 · derau halus di sekitar kertas
    dekat = np.abs(hasil - kertas).max(axis=2) <= TOLERANSI_DERAU
    hasil[dekat] = kertas

    # 4 · cincin terluar 2 px dipaksa tepat ke kertas, supaya tepi gambar
    #     tidak pernah terlihat sebagai garis saat object-fit: cover
    tepi = 2
    hasil[:tepi, :] = kertas
    hasil[-tepi:, :] = kertas
    hasil[:, :tepi] = kertas
    hasil[:, -tepi:] = kertas
    return Image.fromarray(hasil.astype("uint8"), "RGB")


def apakah_biji(px: tuple[int, int, int], ambang: int = 60) -> bool:
    """Piksel dianggap biji kalau jauh lebih gelap daripada kertas."""
    return (KERTAS[0] - px[0]) > ambang and (KERTAS[1] - px[1]) > ambang


def periksa(im: Image.Image, data: dict) -> list[str]:
    masalah = []
    titik: list[tuple[str, int, int]] = []
    for z in data["zona"]:
        t = z.get("titik_foto")
        if not t or len(t) != 2:
            masalah.append(f"zona {z['id']} belum punya titik_foto")
            continue
        x = int(round(im.width * t[0] / 100))
        y = int(round(im.height * t[1] / 100))
        if not (0 <= x < im.width and 0 <= y < im.height):
            masalah.append(f"titik {z['id']} di luar gambar ({t[0]}%, {t[1]}%)")
            continue
        px = im.getpixel((x, y))
        if not apakah_biji(px):
            masalah.append(f"titik {z['id']} jatuh di latar, bukan di biji "
                           f"({t[0]}%, {t[1]}% → rgb{px})")
        titik.append((z["id"], x, y))

    # titik tidak boleh saling menumpuk (jarak < 8% lebar gambar)
    for i in range(len(titik)):
        for j in range(i + 1, len(titik)):
            dx = abs(titik[i][1] - titik[j][1])
            dy = abs(titik[i][2] - titik[j][2])
            if (dx * dx + dy * dy) ** 0.5 < im.width * 0.08:
                masalah.append(f"titik {titik[i][0]} dan {titik[j][0]} terlalu berdekatan")
    return masalah


def laporan(im: Image.Image, data: dict, catatan: dict) -> dict:
    return {
        "sumber": os.path.relpath(SUMBER, ROOT),
        "poster": os.path.relpath(POSTER, ROOT),
        "ukuran": [im.width, im.height],
        "rasio": round(im.width / im.height, 3),
        "tepi": "derau latar diratakan ke #F5EFE4 (latar tidak dipotong)",
        "latar": catatan,
        "titik": {z["id"]: z["titik_foto"] for z in data["zona"]},
        "catatan": "Gambar dihasilkan generator gambar, bukan hasil pindai biji "
                   "Nocturne dan bukan model parametrik. Agtron 55–60 = perkiraan visual.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true")
    a = ap.parse_args()

    data = baca_data()
    if not os.path.exists(SUMBER):
        print("XX sumber render tidak ada:", os.path.relpath(SUMBER, ROOT))
        return 1

    with Image.open(SUMBER) as src:
        im = src.convert("RGB")
    catatan = {"latar_awal": warna_latar(im)}
    im = potong_4_5(im)
    im = rapikan_latar(im)
    catatan["latar_akhir"] = warna_latar(im)
    masalah = periksa(im, data)
    for xy in ((2, 2), (im.width - 3, 2), (2, im.height - 3), (im.width - 3, im.height - 3)):
        if max(abs(im.getpixel(xy)[i] - KERTAS[i]) for i in range(3)) > 3:
            masalah.append(f"sudut {xy} tidak menyatu dengan kertas: {im.getpixel(xy)}")
    im_rapi = im

    if a.cek:
        for m in masalah:
            print("XX", m)
        print(f"{'OK' if not masalah else 'GAGAL'} · {im.width}×{im.height} · "
              f"{len(data['zona'])} titik · latar rgb{catatan['latar_akhir']} · "
              f"{len(masalah)} masalah")
        return 0 if not masalah else 1

    if masalah:
        for m in masalah:
            print("XX", m)
        print("poster tidak ditulis")
        return 1

    im_rapi.save(POSTER, "WEBP", quality=KUALITAS, method=6)
    with open(LAPORAN, "w", encoding="utf-8") as f:
        json.dump(laporan(im_rapi, data, catatan), f, indent=2, ensure_ascii=False)
        f.write("\n")

    kb = os.path.getsize(POSTER) / 1024
    print(f"{os.path.relpath(POSTER, ROOT)} · {im.width}×{im.height} · {kb:.0f} KB · "
          f"latar rgb{catatan['latar_akhir']} (asal rgb{catatan['latar_awal']}) · "
          f"{len(data['zona'])} titik di atas biji")
    return 0


if __name__ == "__main__":
    sys.exit(main())
