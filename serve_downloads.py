# -*- coding: utf-8 -*-
"""Halaman unduhan: semua berkas buku + foto marketplace, bisa diklik.

Jalankan:  PORT=8080 python serve_downloads.py
Lalu buka: http://127.0.0.1:8080/
Berkas dilayani di /f/<path relatif terhadap book/publish/>.

Skrip ini sengaja disimpan di repo, bukan di /tmp — sebelumnya hilang setiap
kali lingkungan kerja dijalankan ulang.
"""
import html
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "book", "publish")
PORT = int(os.environ.get("PORT", "8080"))

MKT = [
    ("hero", "Gambar utama", "22° — depan, punggung, tebal buku"),
    ("front", "Depan lurus", "0° — untuk thumbnail dan iklan"),
    ("angle", "Sudut 3/4", "38° — memperlihatkan ketebalan"),
    ("fore", "Tepi kertas", "−28° — membuktikan jumlah halaman"),
    ("back", "Sampul belakang", "205° — untuk gambar kedua atau ketiga"),
    ("spine", "Punggung", "52° — untuk rak dan katalog"),
    ("hero", "Hero transparan", "PNG, latar kosong untuk banner"),
]

EDITIONS = [
    ("EN", "Surviving_the_Future_EN"),
    ("ID", "Bertahan_Hidup_di_Masa_Depan_ID"),
]


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def card(root, fname, title, note="", preview=True):
    path = os.path.join(PUB, root, fname)
    if not os.path.exists(path):
        return ""
    size = human(os.path.getsize(path))
    url = "/f/" + urllib.parse.quote("/".join(x for x in (root, fname) if x))
    img = (f'<img loading="lazy" src="{url}" alt="{html.escape(title)}">'
           if preview else '')
    return f'''<a class="card" href="{url}" download>
      <div class="thumb">{img}</div>
      <div class="meta"><b>{html.escape(title)}</b>
        <span>{html.escape(fname)}</span>
        <span class="sub">{html.escape(note)} · {size}</span></div></a>'''


def build_html():
    parts = []

    parts.append('<h2>Foto marketplace — Inggris</h2><div class="grid">')
    for key, title, note in MKT:
        ext = "png" if key == "hero" and "transparan" in title else "jpg"
        parts.append(card("marketplace", f"Surviving_the_Future_EN_mkt_{key}.{ext}",
                          title, note))
    parts.append("</div>")

    parts.append('<h2>Foto marketplace — Indonesia</h2><div class="grid">')
    for key, title, note in MKT:
        ext = "png" if key == "hero" and "transparan" in title else "jpg"
        parts.append(card("marketplace", f"Bertahan_Hidup_di_Masa_Depan_ID_mkt_{key}.{ext}",
                          title, note))
    parts.append("</div>")

    parts.append('<h2>Kedua edisi</h2><div class="grid">')
    parts.append(card("marketplace", "pair_mkt_lineup.jpg", "Lineup dua edisi",
                      "3600 × 2400 — untuk produk bundle"))
    parts.append("</div>")

    parts.append('<h2>Sampul Gumroad</h2><div class="grid">')
    for root, f, t in [
        ("gumroad", "cover_en_1_hero.png", "EN — sampul 1"),
        ("gumroad", "cover_en_2_inside.png", "EN — sampul 2, halaman asli"),
        ("gumroad", "cover_en_3_quote.png", "EN — sampul 3, kutipan"),
        ("gumroad", "cover_id_1_hero.png", "ID — sampul 1"),
        ("gumroad", "cover_id_2_inside.png", "ID — sampul 2"),
        ("gumroad", "cover_id_3_quote.png", "ID — sampul 3"),
        ("gumroad", "cover_bundle_1_hero.png", "Bundle — sampul 1"),
        ("gumroad", "cover_sample_1_hero.png", "Sampel — sampul 1"),
        ("gumroad", "thumb_en.png", "Thumbnail EN"),
        ("gumroad", "thumb_id.png", "Thumbnail ID"),
        ("gumroad", "profile_avatar.png", "Avatar profil"),
    ]:
        parts.append(card(root, f, t))
    parts.append("</div>")

    parts.append('<h2>Buku</h2><div class="grid">')
    for tag, slug in EDITIONS:
        for f, t in [
            (f"{slug}_interior.pdf", f"{tag} — PDF isi"),
            (f"{slug}_sample.pdf", f"{tag} — sampel gratis"),
            (f"{slug}.epub", f"{tag} — EPUB"),
            (f"{slug}.docx", f"{tag} — DOCX"),
            (f"{slug}_figures.zip", f"{tag} — paket gambar"),
            (f"{slug}_cover_print.pdf", f"{tag} — bungkus cetak"),
        ]:
            parts.append(card("", f, t, preview=False))
    parts.append("</div>")

    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Unduhan — Surviving the Future</title><style>
:root{{--navy:#0b1624;--ink:#e9eef5;--muted:#8ea3b8;--amber:#e8a33d;--line:#20334a}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--navy);color:var(--ink);
 font-family:system-ui,-apple-system,"Segoe UI",sans-serif;padding:40px 26px 70px}}
h1{{font-family:Georgia,serif;font-size:34px;margin:0 0 6px;letter-spacing:-.01em}}
.lede{{color:var(--muted);margin:0 0 40px;max-width:640px;line-height:1.55}}
h2{{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--amber);
 margin:44px 0 16px;padding-top:20px;border-top:1px solid var(--line)}}
.grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}}
.card{{display:block;text-decoration:none;color:inherit;background:#111f31;
 border:1px solid var(--line);border-radius:10px;overflow:hidden;transition:.15s}}
.card:hover{{border-color:var(--amber);transform:translateY(-2px)}}
.thumb{{background:#fff;aspect-ratio:1;display:flex;align-items:center;justify-content:center}}
.thumb img{{width:100%;height:100%;object-fit:contain}}
.card:has(.thumb:empty) .thumb{{display:none}}
.meta{{padding:11px 13px 13px;display:flex;flex-direction:column;gap:3px}}
.meta b{{font-size:14px;font-weight:600}}
.meta span{{font-size:11.5px;color:var(--muted);word-break:break-all}}
.meta .sub{{color:var(--amber);opacity:.85}}
</style></head><body>
<h1>Unduhan</h1>
<p class="lede">Klik kartu mana pun untuk mengunduh. Foto marketplace berukuran
3000 × 3000 px, siap diunggah ke Gumroad, Amazon, atau Etsy.</p>
{''.join(parts)}
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.unquote(self.path.split("?")[0])

        if path in ("/", "/index.html"):
            body = build_html().encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path.startswith("/f/"):
            rel = path[3:].lstrip("/")
            full = os.path.normpath(os.path.join(PUB, rel))
            if full.startswith(PUB) and os.path.isfile(full):
                size = os.path.getsize(full)
                self.send_response(200)
                ctype = "application/octet-stream"
                for ext, ct in ((".pdf", "application/pdf"), (".jpg", "image/jpeg"),
                                (".jpeg", "image/jpeg"), (".png", "image/png"),
                                (".zip", "application/zip"),
                                (".epub", "application/epub+zip")):
                    if full.lower().endswith(ext):
                        ctype = ct
                        break
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(size))
                self.send_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(full)}"')
                self.end_headers()
                with open(full, "rb") as fh:
                    while chunk := fh.read(262144):
                        self.wfile.write(chunk)
                return

        self.send_error(404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"unduhan siap di 0.0.0.0:{PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
