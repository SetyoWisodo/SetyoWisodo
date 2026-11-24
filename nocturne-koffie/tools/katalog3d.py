#!/usr/bin/env python3
"""Katalog produk 3D untuk landing page — satu rig, lima sudut per lot.

Kenapa berkas ini ada
---------------------
`tools/foto.py` sudah bisa merender kemasan dengan shading per piksel, tetapi
hasilnya:
  · 2000 × 2000 px, 150–920 KB per berkas — terlalu berat untuk kartu 4:5 di
    landing page (sembilan kartu = belasan MB);
  · latar kertas studio dengan bayangan kontak, bukan latar kartu produk;
  · hanya tiga sudut tetap, tidak bisa dipakai untuk pemutar 360°.

Yang ditulis di sini: satu rig kecil yang memakai **renderer `foto.py` yang
sudah terbukti** (permukaan, cahaya, tekstur), lalu menghasilkan dua hal:

  1. `assets/img/katalog-3d/<id>-<sudut>.webp`  — lima sudut untuk kartu
     (0°, −18°, 28°, 55°, 90°) + satu hero 16:9, latar transparan (WebP alpha);
  2. `assets/img/katalog-3d/<id>-putar/<nn>.webp` — 16 langkah untuk pemutar
     360° di halaman detail. Ke-16 langkah ini dipakai juga oleh kartu saat
     hover: jadi tidak ada render ganda dan tidak ada gambar "karangan".

Kenapa transparan, bukan latar kertas
-------------------------------------
Kartu produk di `index.html` memakai `background:var(--paper-2)` dan rasio 4:5.
Kalau render membawa latarnya sendiri, kertas render (putih kehangatan) akan
bertabrakan dengan kertas halaman. Dengan alpha, satu berkas bisa dipakai di
kartu, di lembar detail, dan di latar gelap — tanpa render ulang.

Batas (jujur)
-------------
· Ini render dari label + geometri sendiri, **bukan pemotretan** kemasan fisik.
· Sudut pandang kamera turun 4°; kemiringan itu dibuat tetap supaya seluruh
  katalog terasa satu sesi foto.
· 16 langkah untuk 360° = 22,5° per langkah. Saat diseret cepat, mata membaca
  sebagai putaran; saat berhenti, gambarnya tajam. Bukan video 60 fps.
· Hanya 500 g (satu-satunya ukuran yang spek fisiknya dikonfirmasi pemilik).

Pakai
-----
    python3 tools/katalog3d.py                 # 9 lot, semua keluaran
    python3 tools/katalog3d.py --satu gayo     # satu lot untuk menilai
    python3 tools/katalog3d.py --cek           # periksa keluaran + berat
"""

from __future__ import annotations

import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import foto as F                                     # noqa: E402
import katalog as K                                  # noqa: E402

ROOT = K.ROOT
KELUAR = os.path.join(ROOT, "assets", "img", "katalog-3d")
DATA = os.path.join(ROOT, "data", "katalog-3d.json")
JS = os.path.join(ROOT, "data", "katalog3d.js")

# Lima sudut kartu. 0° label tegak (paling terbaca), 90° gusset penuh (paling
# "bentuk"), dan tiga di antaranya membuat hover terasa berputar.
SUDUT_KARTU = (0, -18, 28, 55, 90)
# Putaran penuh: 16 langkah, mulai dari 0° (bukan −18°) supaya langkah 0 bisa
# dipakai sebagai gambar diam tanpa render tambahan.
LANGKAH = 16
KARTU_PX = 640          # tinggi objek; kartu 4:5 @2× = 1200 tinggi, objek 86%
PUTAR_PX = 440          # pemutar di halaman detail lebih kecil
KUALITAS = 82


def potong_transparan(im: Image.Image) -> Image.Image:
    """Buang tepi kosong, sisakan margin 2% supaya tepi tidak mentok."""
    bb = im.split()[3].getbbox()
    if not bb:
        return im
    im = im.crop(bb)
    pad_x = max(1, round(im.width * 0.02))
    pad_y = max(1, round(im.height * 0.02))
    kanvas = Image.new("RGBA", (im.width + 2 * pad_x, im.height + 2 * pad_y), (0, 0, 0, 0))
    kanvas.paste(im, (pad_x, pad_y), im)
    return kanvas


def simpan(im: Image.Image, jalur: str) -> int:
    os.makedirs(os.path.dirname(jalur), exist_ok=True)
    im.save(jalur, "WEBP", quality=KUALITAS, method=6, alpha_quality=90)
    return os.path.getsize(jalur)


def render_lot(p: dict, sp: dict) -> dict:
    g = F.spek(sp)
    lbl = K.label(p["id"])
    if lbl is None:
        return {"id": p["id"], "status": "tanpa label"}

    kartu = {}
    for sudut in SUDUT_KARTU:
        im = potong_transparan(F.render(g, lbl, KARTU_PX, sudut))
        nama = f'{p["id"]}-{abs(sudut)}.webp'
        kb = simpan(im, os.path.join(KELUAR, nama))
        kartu[str(sudut)] = {"berkas": f"assets/img/katalog-3d/{nama}",
                             "kb": round(kb / 1024, 1),
                             "ukuran": list(im.size)}

    folder_putar = os.path.join(KELUAR, f'{p["id"]}-putar')
    putar = {}
    for i in range(LANGKAH):
        sudut = round(360 * i / LANGKAH)
        im = potong_transparan(F.render(g, lbl, PUTAR_PX, sudut if sudut < 180 else sudut - 360))
        nama = f"{i:02d}.webp"
        kb = simpan(im, os.path.join(folder_putar, nama))
        putar[f"{i:02d}"] = {"berkas": f'assets/img/katalog-3d/{p["id"]}-putar/{nama}',
                             "kb": round(kb / 1024, 1),
                             "derajat": sudut}

    kb_kartu = sum(v["kb"] for v in kartu.values())
    kb_putar = sum(v["kb"] for v in putar.values())
    return {
        "id": p["id"], "no": p["no"], "nama": p["name"], "status": "siap",
        "ukuran_kemasan": sp["aktif"].get("berat", sp["aktif"]["kunci"]),
        "kartu": kartu, "putar": putar,
        "kb_kartu": round(kb_kartu, 1), "kb_putar": round(kb_putar, 1),
        "berkas": len(kartu) + len(putar),
    }


def tulis_data(hasil: list[dict]) -> None:
    siap = [h for h in hasil if h.get("status", "siap") == "siap"]
    isi = {
        "_keterangan": (
            "Katalog produk 3D untuk landing page. Dibangun tools/katalog3d.py "
            "dari data/catalog.json + data/kemasan-katalog.json. Render sendiri "
            "(bukan pemotretan), latar transparan, 500 g saja."
        ),
        "sudut_kartu": list(SUDUT_KARTU),
        "langkah_putar": LANGKAH,
        "kartu_px": KARTU_PX,
        "putar_px": PUTAR_PX,
        "sku": [{
            "id": h["id"], "no": h["no"], "nama": h["nama"],
            "ukuran": h["ukuran_kemasan"],
            "kartu": h["kartu"], "putar": h["putar"],
            "kb_kartu": h["kb_kartu"], "kb_putar": h["kb_putar"],
        } for h in siap],
    }
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(isi, f, ensure_ascii=False, indent=1)
        f.write("\n")


def tulis_js(hasil: list[dict]) -> None:
    """Data untuk halaman: kartu + langkah putar. Ringkas, tanpa komentar.

    Ditulis sebagai `window.KATALOG3D` (bukan JSON yang di-fetch) supaya kartu
    bisa memakai jalur gambar tanpa menunggu permintaan jaringan kedua; isinya
    hanya jalur berkas, jadi beratnya beberapa KB.
    """
    siap = [h for h in hasil if h.get("status", "siap") == "siap"]
    isi = {
        "sudut_kartu": list(SUDUT_KARTU),
        "langkah": LANGKAH,
        "sku": [{
            "id": h["id"], "no": h["no"], "nama": h["nama"],
            "kartu": {k: v["berkas"] for k, v in h["kartu"].items()},
            "putar": [h["putar"][f"{i:02d}"]["berkas"] for i in range(LANGKAH)],
        } for h in siap],
    }
    with open(JS, "w", encoding="utf-8") as f:
        f.write("/* Katalog 3D Nocturne — dibangun tools/katalog3d.py. Jangan sunting tangan. */\n")
        f.write("window.KATALOG3D = ")
        json.dump(isi, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")


LEMBAR = os.path.join(ROOT, "laporan", "katalog-3d.png")


def lembar(hasil: list[dict]) -> None:
    """Satu lembar bukti: sembilan kartu, latar kertas brand, ukuran 1:1.

    Gunanya untuk menilai konsistensi cahaya dan siluet tanpa membuka
    peramban — bukan gambar halaman.
    """
    from PIL import ImageDraw, ImageFont
    siap = [h for h in hasil if h.get("status", "siap") == "siap"]
    if not siap:
        return
    kol, sel = 5, (300, 375)
    baris = (len(siap) + kol - 1) // kol
    sheet = Image.new("RGB", (kol * sel[0] + 40, baris * (sel[1] + 30) + 40), (245, 239, 228))
    dr = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-500-normal.ttf"), 16)
    except OSError:
        f = ImageFont.load_default()
    for n, h in enumerate(siap):
        im = Image.open(os.path.join(ROOT, h["kartu"]["0"]["berkas"])).convert("RGBA")
        im.thumbnail((sel[0] - 40, sel[1] - 40), Image.LANCZOS)
        x = 20 + (n % kol) * sel[0]
        y = 20 + (n // kol) * (sel[1] + 30)
        dr.rounded_rectangle([x, y, x + sel[0] - 20, y + sel[1]], 8, fill=(239, 230, 214))
        sheet.paste(im, (x + (sel[0] - 20 - im.width) // 2, y + (sel[1] - im.height) // 2), im)
        dr.text((x + 12, y + sel[1] - 24), f'{h["no"]}  {h["nama"]}', fill=(22, 17, 13), font=f)
    os.makedirs(os.path.dirname(LEMBAR), exist_ok=True)
    sheet.save(LEMBAR, optimize=True)


def cek() -> list[str]:
    masalah = []
    if not os.path.exists(DATA):
        return ["data/katalog-3d.json belum ada — jalankan tools/katalog3d.py"]
    with open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    if len(d["sku"]) != 9:
        masalah.append(f'sku di data {len(d["sku"])}, seharusnya 9')
    for s in d["sku"]:
        for kunci, jalur in s["kartu"].items():
            p = os.path.join(ROOT, jalur["berkas"])
            if not os.path.exists(p):
                masalah.append(f'{s["id"]} kartu {kunci}: {jalur["berkas"]} hilang')
            elif os.path.getsize(p) / 1024 > 260:
                masalah.append(f'{s["id"]} kartu {kunci}: {os.path.getsize(p)/1024:.0f} KB > 260 KB')
        if len(s["putar"]) != LANGKAH:
            masalah.append(f'{s["id"]}: {len(s["putar"])} langkah putar, seharusnya {LANGKAH}')
        for kunci, jalur in list(s["putar"].items())[:1]:
            if not os.path.exists(os.path.join(ROOT, jalur["berkas"])):
                masalah.append(f'{s["id"]} putar {kunci}: {jalur["berkas"]} hilang')
    # tidak boleh ada PNG/JPEG besar yang ikut masuk folder ini
    total = 0
    for akar, _, berkas in os.walk(KELUAR):
        for b in berkas:
            total += os.path.getsize(os.path.join(akar, b))
    if total / 1024 / 1024 > 24:
        masalah.append(f'berat folder katalog 3D {total/1024/1024:.1f} MB > 24 MB')
    return masalah


if __name__ == "__main__":
    if "--cek" in sys.argv:
        mm = cek()
        for x in mm:
            print("  ✗", x)
        print("  kesimpulan:", "OK · katalog 3D lengkap" if not mm else f"{len(mm)} masalah")
        sys.exit(0 if not mm else 1)

    sp = K.spek()
    produk = K.baca_catalog()
    if "--satu" in sys.argv:
        kriteria = sys.argv[sys.argv.index("--satu") + 1]
        produk = [p for p in produk if p["id"] == kriteria]

    hasil = []
    for p in produk:
        h = render_lot(p, sp)
        hasil.append(h)
        if h["status"] == "siap":
            print(f'  {h["no"]} {h["nama"]:<16} {h["berkas"]:>2} berkas · '
                  f'kartu {h["kb_kartu"]:>5.0f} KB · putar {h["kb_putar"]:>5.0f} KB')
    if "--satu" not in sys.argv:
        tulis_data(hasil)
        tulis_js(hasil)
        lembar(hasil)
        siap = [h for h in hasil if h["status"] == "siap"]
        print(f'  total      {len(siap)} lot · '
              f'{sum(h["berkas"] for h in siap)} berkas · '
              f'kartu {sum(h["kb_kartu"] for h in siap)/1024:.1f} MB · '
              f'putar {sum(h["kb_putar"] for h in siap)/1024:.1f} MB')
        print(f'  lembar     laporan/katalog-3d.png · '
              f'{os.path.getsize(LEMBAR)/1024:.0f} KB' if os.path.exists(LEMBAR) else "")
        for x in cek():
            print("  ✗", x)
