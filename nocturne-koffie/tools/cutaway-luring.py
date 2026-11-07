#!/usr/bin/env python3
"""Bangun satu berkas HTML mandiri untuk halaman potong-buka (cutaway/).

Alasannya sama dengan tools/luring.py: kalau `cutaway/index.html` dibuka dari
folder unduhan (file:///…), CSS, skrip, huruf, dan label tidak ikut karena
ditautkan relatif. Berkas tunggal ini menyatukan semuanya:

    · cutaway.css        → <style>, url(label.png) → data:image/jpeg;base64
    · assets/css/fonts.css → <style>, hanya huruf yang dipakai halaman ini
    · data.js + cutaway.js → <script> sebaris
    · favicon            → data:image/svg+xml;base64

Bukan salinan kedua: semua isi dibaca dari berkas yang lulus gerbang, jadi tidak
ada satu angka pun yang ditulis ulang di sini.

Pakai:
    python3 tools/cutaway-luring.py          # tulis cutaway/cutaway-luring.html
    python3 tools/cutaway-luring.py --cek    # periksa berkas tunggalnya
"""

from __future__ import annotations

import base64
import io
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMBER = os.path.join(ROOT, "cutaway", "index.html")
CSS = os.path.join(ROOT, "cutaway", "cutaway.css")
DATA = os.path.join(ROOT, "cutaway", "data.js")
JS = os.path.join(ROOT, "cutaway", "cutaway.js")
LABEL = os.path.join(ROOT, "brand", "label-blue-mount-ijen.png")
FAVICON = os.path.join(ROOT, "brand", "favicon.svg")
KELUAR = os.path.join(ROOT, "cutaway", "cutaway-luring.html")

HURUF = [("Inter Tight", "intertight.woff2", "400 600", "normal", "woff2"),
         ("Newsreader", "newsreader.woff2", "400", "normal", "woff2"),
         ("Newsreader", "newsreader-italic.woff2", "400", "italic", "woff2")]
LEBAR_LABEL = 620
KUALITAS = 76
BATAS_BYTE = 1_500_000


def baca(p: str) -> str:
    with open(p, encoding="utf-8") as f:
        return f.read()


def b64(p: str) -> str:
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def label_uri() -> str:
    with Image.open(LABEL) as im:
        im = im.convert("RGB")
        if im.width > LEBAR_LABEL:
            im = im.resize((LEBAR_LABEL, round(im.height * LEBAR_LABEL / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def huruf_css() -> str:
    keluar = ["/* Huruf disisipkan — halaman ini tidak boleh memanggil berkas luar. */"]
    for keluarga, berkas, bobot, gaya, fmt in HURUF:
        keluar.append(
            '@font-face{font-family:"%s";src:url("data:font/%s;base64,%s") format("%s");'
            "font-weight:%s;font-style:%s;font-display:swap}" %
            (keluarga, fmt, b64(os.path.join(ROOT, "assets", "fonts", berkas)), fmt, bobot, gaya))
    return "\n".join(keluar)


def bangun() -> str:
    html = baca(SUMBER)
    css = baca(CSS).replace('url("../brand/label-blue-mount-ijen.png")', 'url("%s")' % label_uri())

    html = html.replace('<link rel="stylesheet" href="../assets/css/fonts.css" />',
                        "<style>\n%s\n</style>" % huruf_css())
    html = html.replace('<link rel="stylesheet" href="cutaway.css" />',
                        "<style>\n%s\n</style>" % css)
    html = html.replace('<script src="data.js"></script>',
                        "<script>\n%s\n</script>" % baca(DATA))
    html = html.replace('<script src="cutaway.js"></script>',
                        "<script>\n%s\n</script>" % baca(JS))
    html = html.replace('<link rel="icon" href="../brand/favicon.svg" type="image/svg+xml" />',
                        '<link rel="icon" href="data:image/svg+xml;base64,%s" />' % b64(FAVICON))
    # tautan antanhalaman: di berkas tunggal tidak ada halaman lain
    html = html.replace('<a class="lbl box" href="../index.html">Kembali / Back</a>',
                        '<a class="lbl box" href="#kendali">Nocturne Koffie</a>')
    html = html.replace('<a class="lbl box" href="../rak/index.html">Rak sangrai</a>', "")
    html = html.replace('<a href="../laporan/cutaway-checklist.md">ceklis 12 baris</a>',
                        "<span>ceklis 12 baris, lihat laporan/cutaway-checklist.md</span>")
    html = html.replace("<main class=\"panggung\">", "<main class=\"panggung\" id=\"panggung\">")
    html = html.replace("<footer class=\"kendali\">", "<footer class=\"kendali\" id=\"kendali\">")
    html = html.replace('<link rel="preload" href="../assets/fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin />', "")
    return html


def cek() -> list[str]:
    m = []
    if not os.path.exists(KELUAR):
        return ["cutaway/cutaway-luring.html belum ada — jalankan tools/cutaway-luring.py"]
    teks = baca(KELUAR)
    ukuran = os.path.getsize(KELUAR)
    if ukuran > BATAS_BYTE:
        m.append(f"{ukuran/1024:.0f} KB lebih dari batas {BATAS_BYTE//1024} KB")
    luar = re.findall(r'(?:src|href)="(\.\./[^"]+)"', teks)
    if luar:
        m.append("masih menaut berkas luar: " + ", ".join(sorted(set(luar))[:3]))
    for wajib in ("window.CUTAWAY", 'id="kamera"', "@font-face", "data:image/jpeg;base64,"):
        if wajib not in teks:
            m.append(f"tidak memuat {wajib}")
    if teks.count('<script src=') or teks.count('<link rel="stylesheet"'):
        m.append("masih ada <script src> atau <link rel=\"stylesheet\">")
    if baca(SUMBER) == teks:
        m.append("berkas tunggal identik dengan sumber — tidak disisipi apa pun")
    return m


if __name__ == "__main__":
    if "--cek" in sys.argv:
        mm = cek()
        for x in mm:
            print("  ✗", x)
        print("  kesimpulan:", "OK · satu berkas, tanpa tautan luar" if not mm else f"{len(mm)} masalah")
        sys.exit(0 if not mm else 1)
    isi = bangun()
    with open(KELUAR, "w", encoding="utf-8") as f:
        f.write(isi)
    print(f"  cutaway/cutaway-luring.html · {os.path.getsize(KELUAR)/1024:.0f} KB · "
          f"{len(isi):,} karakter")
    for x in cek():
        print("  ✗", x)
