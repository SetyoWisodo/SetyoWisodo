#!/usr/bin/env python3
"""Bangun satu berkas HTML mandiri untuk halaman biji sangrai.

Kenapa ada berkas ini: kalau `biji-sangrai/index.html` dibuka langsung dari
folder unduhan (file:///…/ssddw.html), CSS, JS, dan gambar tidak ikut karena
semuanya ditautkan relatif. Hasilnya halaman tampil sebagai HTML mentah —
tanpa gaya, tanpa gerak, tanpa gambar.

Berkas ini menyatukan semuanya ke dalam satu .html:

    · <link rel="stylesheet"> → <style> (isi toko.css)
    · @font-face url(ttf)     → data:font/ttf;base64,…
    · <script src="toko.js">  → <script> (isi toko.js)
    · <img src="../assets/…"> → data:image/jpeg;base64,… (diperkecil 420 px)
    · favicon                 → data:image/svg+xml;base64,…

Situs sesungguhnya tetap memakai berkas terpisah — versi tunggal ini hanya
untuk pratinjau/berbagi. Semua isi diambil dari halaman yang sudah lulus
gerbang, jadi tidak ada teks atau angka yang ditulis ulang di sini.

Pakai:
    python3 tools/luring.py           # tulis biji-sangrai/biji-sangrai-luring.html
    python3 tools/luring.py --cek     # periksa berkas tunggalnya, tanpa menulis
"""

from __future__ import annotations

import argparse
import base64
import io
import os
import re
import sys

from fontTools import subset
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMBER = os.path.join(ROOT, "biji-sangrai", "index.html")
CSS = os.path.join(ROOT, "biji-sangrai", "toko.css")
JS = os.path.join(ROOT, "biji-sangrai", "toko.js")
FAVICON = os.path.join(ROOT, "brand", "favicon.svg")
KELUAR = os.path.join(ROOT, "biji-sangrai", "biji-sangrai-luring.html")

LEBAR_GAMBAR = 340      # tajam sampai ±170 px tampil, cukup untuk pratinjau
KUALITAS = 68
BATAS_BYTE = 2_000_000  # batas ukuran berkas tunggal
SUBSET = True           # huruf dipangkas ke karakter yang benar-benar dipakai


def baca(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def data_uri_gambar(path: str) -> str:
    """Kecilkan gambar lalu jadikan data URI (JPEG)."""
    with Image.open(path) as im:
        im = im.convert("RGB")
        if im.width > LEBAR_GAMBAR:
            tinggi = int(round(im.height * LEBAR_GAMBAR / im.width))
            im = im.resize((LEBAR_GAMBAR, tinggi), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def karakter_terpakai(html: str, css: str) -> str:
    """Semua karakter yang muncul di teks halaman + CSS (tanpa tag)."""
    teks = re.sub(r"<[^>]+>", " ", html)
    teks += " " + re.sub(r"[{};:]", " ", css)
    huruf = {c for c in teks if c.isprintable()}
    # karakter kontrol dasar + tanda baca umum yang mungkin dipakai lewat CSS
    huruf |= set("0123456789.,:;!?()[]{}%–—-·×→←↗“”‘’…€$@/\\|+*&\"'# ")

    import string
    huruf |= set(string.ascii_letters + string.digits)
    return "".join(sorted(huruf))


def data_uri_font(path: str, karakter: str | None = None) -> str:
    if SUBSET and karakter:
        buf = io.BytesIO()
        subset.main([
            str(path),
            f"--text={karakter}",
            "--layout-features=*",
            "--no-hinting",
            f"--output-file={os.devnull}",
        ]) if False else None
        opsi = subset.Options()
        opsi.layout_features = ["kern", "liga"]
        opsi.hinting = False
        opsi.desubroutinize = True
        font = subset.load_font(str(path), opsi)
        subsetter = subset.Subsetter(options=opsi)
        subsetter.populate(text=karakter)
        subsetter.subset(font)
        subset.save_font(font, buf, opsi)
        return "data:font/ttf;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    with open(path, "rb") as f:
        return "data:font/ttf;base64," + base64.b64encode(f.read()).decode("ascii")


def data_uri_svg(path: str) -> str:
    with open(path, "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode("ascii")


def sisip_css(css: str, karakter: str | None = None) -> str:
    def ganti(m):
        rel = m.group(1)
        path = os.path.normpath(os.path.join(ROOT, "biji-sangrai", rel))
        return f'url("{data_uri_font(path, karakter)}") format("truetype")'

    return re.sub(r'url\("([^"]+\.ttf)"\)\s*format\("truetype"\)', ganti, css)


def sisip_gambar(html: str) -> tuple[str, int]:
    cache: dict[str, str] = {}
    jumlah = 0

    def ganti(m):
        nonlocal jumlah
        rel = m.group(1)
        path = os.path.normpath(os.path.join(ROOT, "biji-sangrai", rel))
        if not os.path.exists(path):
            return m.group(0)
        if path not in cache:
            cache[path] = data_uri_gambar(path)
            jumlah += 1
        return f'src="{cache[path]}"'

    return re.sub(r'src="(\.\./assets/[^"]+)"', ganti, html), jumlah


def bangun() -> tuple[str, dict]:
    html = baca(SUMBER)
    karakter = karakter_terpakai(html, baca(CSS))
    css = sisip_css(baca(CSS), karakter)
    js = baca(JS)

    html = html.replace('<link rel="stylesheet" href="toko.css">', f"<style>\n{css}\n</style>")
    html = html.replace('<script src="toko.js" defer></script>', f"<script>\n{js}\n</script>")

    # ikon: sisipkan favicon, buang tautan apple-touch-icon (berkas raster besar)
    html = html.replace('<link rel="apple-touch-icon" href="../brand/apple-touch-icon.png">', "")
    html = html.replace(
        '<link rel="icon" href="../brand/favicon.svg" type="image/svg+xml">',
        f'<link rel="icon" type="image/svg+xml" href="{data_uri_svg(FAVICON)}">',
    )

    html, jumlah_gambar = sisip_gambar(html)

    # tautan antar-halaman diarahkan ke alamat situs, supaya tetap bisa diklik
    # meski berkas ini tergeletak sendirian di folder unduhan
    for lokal, daring in (
        ("../index.html", "https://nocturnekoffie.id/"),
        ("../kampanye/index.html", "https://nocturnekoffie.id/kampanye/"),
        ("../komersial/penawaran-b2b.html", "https://nocturnekoffie.id/komersial/penawaran-b2b.html"),
    ):
        html = html.replace(f'href="{lokal}"', f'href="{daring}"')

    # tanda jujur di kepala berkas: ini salinan pratinjau, bukan berkas utama
    html = html.replace(
        "<title>",
        "<title>[pratinjau luring] ",
        1,
    )

    # aset tidak boleh tertinggal relatif; tautan halaman sudah jadi URL penuh
    sisa = re.findall(r'src="(\.\.?/[^"]+)"', html)
    sisa += re.findall(r'href="(\.\.?/[^"]+\.(?:css|js))"', html)
    return html, {"gambar": jumlah_gambar, "sisa": sisa, "css": len(css), "js": len(js)}


def periksa() -> int:
    if not os.path.exists(KELUAR):
        print("XX biji-sangrai/biji-sangrai-luring.html belum dibuat")
        return 1
    teks = baca(KELUAR)
    masalah = []

    if re.search(r'src="\.\.?/', teks):
        masalah.append("masih ada aset bertautan relatif — berkas tidak mandiri")
    if 'href="toko.css"' in teks or 'src="toko.js"' in teks:
        masalah.append("CSS/JS masih ditautkan, belum disisipkan")
    if "@font-face" not in teks:
        masalah.append("tidak ada @font-face — huruf akan jatuh ke font sistem")
    if "prefers-reduced-motion" not in teks:
        masalah.append("aturan reduced-motion hilang")
    if "https://wa.me/" not in teks:
        masalah.append("tautan WhatsApp hilang")
    besar = os.path.getsize(KELUAR)
    if besar > BATAS_BYTE:
        masalah.append(f"berkas {besar/1024/1024:.2f} MB melewati batas {BATAS_BYTE/1024/1024:.0f} MB")

    # semua biji harus tetap ada setelah penggabungan
    import json
    katalog = json.loads(baca(os.path.join(ROOT, "data", "catalog.json")))
    for p in katalog["products"]:
        if p["name"] not in teks:
            masalah.append(f"biji {p['name']} hilang")

    for m in masalah:
        print("XX", m)
    print(f"{'OK' if not masalah else 'GAGAL'} · {besar/1024:.0f} KB · "
          f"{teks.count('data:image/jpeg')} gambar tersisip · {teks.count('data:font/ttf')} huruf tersisip · "
          f"{len(masalah)} masalah")
    return 0 if not masalah else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true")
    a = ap.parse_args()

    if a.cek:
        return periksa()

    html, info = bangun()
    if info["sisa"]:
        for s in info["sisa"]:
            print("XX tautan relatif tertinggal:", s)
        return 1
    with open(KELUAR, "w", encoding="utf-8") as f:
        f.write(html)
    besar = os.path.getsize(KELUAR)
    print(f"biji-sangrai/biji-sangrai-luring.html · {besar/1024:.0f} KB · "
          f"{info['gambar']} gambar · CSS {info['css']/1024:.0f} KB · JS {info['js']/1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
