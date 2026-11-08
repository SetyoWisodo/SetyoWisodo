#!/usr/bin/env python3
"""Satu berkas HTML untuk halaman katalog (dibuka tanpa server).

Isi disatukan: CSS, data, skrip, dan **foto diperkecil** (JPEG data URI). Foto
asli 2000 px tidak disisipkan — sembilan SKU × tiga sudut akan jadi 12 MB dan
halaman luring jadi tidak terpakai. Yang disisipkan: sudut 0° (760 px) + sudut
18° (520 px) per SKU, dan hero 1200 px untuk lot unggulan. Batas 2,5 MB.

Pakai:
    python3 tools/katalog-luring.py           # tulis katalog/katalog-luring.html
    python3 tools/katalog-luring.py --cek     # periksa hasilnya
"""

from __future__ import annotations

import base64
import io
import json
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMBER = os.path.join(ROOT, "katalog", "index.html")
CSS = os.path.join(ROOT, "katalog", "katalog.css")
JS = os.path.join(ROOT, "katalog", "katalog.js")
DATA = os.path.join(ROOT, "data", "katalog.js")
FAVICON = os.path.join(ROOT, "brand", "favicon.svg")
KELUAR = os.path.join(ROOT, "katalog", "katalog-luring.html")
HURUF = [("Fraunces", "fraunces.woff2", "300 700", "normal"),
         ("Fraunces", "fraunces-italic.woff2", "300 400", "italic"),
         ("Inter Tight", "intertight.woff2", "400 600", "normal")]
FOTO = {"0": 760, "18": 520}
HERO_LEBAR = 1200
KUALITAS = 74
BATAS = 2_500_000


def baca(p: str) -> str:
    with open(p, encoding="utf-8") as f:
        return f.read()


def data_uri(jalur: str, lebar: int) -> str:
    with Image.open(jalur) as im:
        im = im.convert("RGB")
        if im.width > lebar:
            im = im.resize((lebar, round(im.height * lebar / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=KUALITAS, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def data_tertanam() -> str:
    """data/katalog.js dengan jalur gambar diganti data URI (yang disisipkan saja)."""
    teks = baca(DATA)
    obj = json.loads(teks[teks.index("{"):teks.rindex("}") + 1])
    for s in obj["sku"]:
        for kunci, lebar in FOTO.items():
            jalur = os.path.join(ROOT, s["foto"][kunci])
            if os.path.exists(jalur):
                s["foto"][kunci] = data_uri(jalur, lebar)
        # sudut 40° tidak disisipkan: tombolnya tetap ada, jatuh ke sudut 0°
        s["foto"]["40"] = s["foto"]["0"]
        jh = os.path.join(ROOT, s["foto"]["hero"])
        if os.path.exists(jh):
            s["foto"]["hero"] = data_uri(jh, HERO_LEBAR)
    return ("/* Foto disisipkan sebagai data URI (diperkecil) — versi luring. */\n"
            "window.KATALOG = " + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + ";\n")


def huruf_css() -> str:
    bagian = ["/* Huruf disisipkan — versi luring tidak boleh memanggil berkas luar. */"]
    for keluarga, berkas, bobot, gaya in HURUF:
        with open(os.path.join(ROOT, "assets", "fonts", berkas), "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        bagian.append('@font-face{font-family:"%s";src:url("data:font/woff2;base64,%s") format("woff2");'
                      "font-weight:%s;font-style:%s;font-display:swap}" % (keluarga, b64, bobot, gaya))
    return "\n".join(bagian)


def bangun() -> str:
    html = baca(SUMBER)
    css = baca(CSS)
    html = html.replace('<link rel="stylesheet" href="../assets/css/fonts.css" />',
                        "<style>\n" + huruf_css() + "\n</style>")
    html = html.replace('<link rel="stylesheet" href="katalog.css" />', "<style>\n" + css + "\n</style>")
    html = html.replace('<script src="../data/katalog.js"></script>',
                        "<script>\n" + data_tertanam() + "\n</script>")
    html = html.replace('<script src="katalog.js"></script>', "<script>\n" + baca(JS) + "\n</script>")
    with open(FAVICON, "rb") as f:
        fav = base64.b64encode(f.read()).decode("ascii")
    html = html.replace('<link rel="icon" href="../brand/favicon.svg" type="image/svg+xml" />',
                        '<link rel="icon" href="data:image/svg+xml;base64,%s" />' % fav)
    html = html.replace('<link rel="preload" href="../assets/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin />', "")
    html = html.replace('<a class="lbl box" href="../index.html">Kembali / Back</a>',
                        '<a class="lbl box" href="#katalog">Nocturne Koffie</a>')
    return html


def cek() -> list[str]:
    m = []
    if not os.path.exists(KELUAR):
        return ["katalog/katalog-luring.html belum ada — jalankan tools/katalog-luring.py"]
    teks = baca(KELUAR)
    ukuran = os.path.getsize(KELUAR)
    if ukuran > BATAS:
        m.append(f"{ukuran/1024:.0f} KB lebih dari batas {BATAS//1024} KB")
    luar = re.findall(r'(?:src|href)="(\.\./[^"]+)"', teks)
    if luar:
        m.append("masih menaut berkas luar: " + ", ".join(sorted(set(luar))[:3]))
    for wajib in ("window.KATALOG", "data:image/jpeg;base64,", "@font-face", 'id="grid"'):
        if wajib not in teks:
            m.append(f"tidak memuat {wajib}")
    if '<script src=' in teks or '<link rel="stylesheet"' in teks:
        m.append('masih ada <script src> atau <link rel="stylesheet">')
    if teks.count("data:image/jpeg;base64,") < 10:
        m.append("foto yang disisipkan kurang dari 10")
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
    print(f"  katalog/katalog-luring.html · {os.path.getsize(KELUAR)/1024:.0f} KB · "
          f"{len(isi):,} karakter")
    for x in cek():
        print("  ✗", x)
