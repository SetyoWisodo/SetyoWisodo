#!/usr/bin/env python3
"""Rakit gambar buku: potong, perbaiki, dan bakar kredit + lisensi ke dalam gambar.

Kredit tidak pernah dipisahkan dari berkasnya. Alasannya praktis: begitu gambar
dipindahkan ke Word, EPUB, atau presentasi, keterangan di halaman lain hilang,
dan gambar yatim tanpa kredit adalah gambar yang tidak boleh dipakai.

Pemakaian:
    python3 tools/siapkan_gambar.py            # rakit semua
    python3 tools/siapkan_gambar.py pakistan   # satu set saja
"""
import json
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUMBER = ROOT / "gambar" / "sumber"
KELUAR = ROOT / "gambar"
MANIFES = ROOT / "gambar" / "manifes.json"

LEBAR = 1800          # lebar cetak ~13 cm pada 350 dpi
BAR = 96              # tinggi pita kredit bawah
MUTIARA = (250, 249, 246)
TINTA = (32, 34, 38)
ABU = (108, 112, 120)


def font(ukuran: int, tebal: bool = False):
    kandidat = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if tebal
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if tebal
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for k in kandidat:
        if pathlib.Path(k).exists():
            return ImageFont.truetype(k, ukuran)
    return ImageFont.load_default()


def bungkus(draw, teks: str, f, lebar: int) -> list[str]:
    """Pecah teks jadi baris yang muat, tanpa memotong kata."""
    kata, baris, kini = teks.split(), [], ""
    for k in kata:
        coba = (kini + " " + k).strip()
        if draw.textlength(coba, font=f) <= lebar:
            kini = coba
        else:
            if kini:
                baris.append(kini)
            kini = k
    if kini:
        baris.append(kini)
    return baris


def rakit(item: dict) -> pathlib.Path:
    asal = SUMBER / item["berkas_sumber"]
    im = Image.open(asal).convert("RGB")
    if item.get("potong"):
        kiri, atas, kanan, bawah = item["potong"]
        w, h = im.size
        im = im.crop((int(kiri * w), int(atas * h), int(kanan * w), int(bawah * h)))
    if item.get("putar"):
        im = im.rotate(item["putar"], expand=True, resample=Image.BICUBIC)
    # skala ke lebar target
    if im.width != LEBAR:
        tinggi = round(im.height * LEBAR / im.width)
        im = im.resize((LEBAR, tinggi), Image.LANCZOS)
    f_kredit = font(20)
    f_judul = font(20, tebal=True)
    kanvas = Image.new("RGB", (LEBAR, im.height + BAR), MUTIARA)
    kanvas.paste(im, (0, 0))
    d = ImageDraw.Draw(kanvas)
    d.line([(0, im.height), (LEBAR, im.height)], fill=(214, 211, 204), width=2)
    d.text((28, im.height + 20), item["sumber"], font=f_judul, fill=TINTA)
    baris = bungkus(d, item["lisensi"], f_kredit, LEBAR - 56)
    for i, b in enumerate(baris[:2]):
        d.text((28, im.height + 48 + i * 24), b, font=f_kredit, fill=ABU)
    tujuan = KELUAR / item["berkas"]
    tujuan.parent.mkdir(parents=True, exist_ok=True)
    kanvas.save(tujuan, "JPEG", quality=90, optimize=True, progressive=True)
    return tujuan


def main(pilih: list[str]) -> None:
    data = json.loads(MANIFES.read_text(encoding="utf-8"))
    for item in data:
        if pilih and item["kunci"] not in pilih:
            continue
        asal = SUMBER / item["berkas_sumber"]
        if not asal.exists():
            print(f"LEWAT {item['kunci']}: sumber belum ada ({asal.name})")
            continue
        p = rakit(item)
        print(f"OK    {item['kunci']:<22} {p.relative_to(ROOT)}  {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
