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
import re
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

# Hanya edisi Inggris yang dijual. Edisi Indonesia tetap dirender sebagai alat
# koreksi internal, tetapi tidak ditampilkan di halaman ini.
EDITIONS = [
    ("EN", "Surviving_the_Future_EN"),
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


def build_html(host=""):
    parts = []

    base = f"https://{host}" if host else ""
    parts.insert(0, f'''<div class="hero">
      <a class="btn" href="/copy/en" target="_blank">Buka teks deskripsi EN &nbsp;→</a>
      <p class="lede" style="margin:14px 0 0">Lalu <b>Ctrl+A</b>, <b>Ctrl+C</b>, dan tempel ke kotak
      Description di Gumroad. Alamat halaman itu:
      <code>{base}/copy/en</code> — bisa juga diketik langsung di bilah alamat,
      atau dibuka dari kartu di bawah.</p></div>''')

    parts.append('<h2>Teks deskripsi siap tempel</h2><div class="grid">')
    for slug, t in [("en-plain", "EN — teks polos (paling gampang)"),
                    ("en", "EN — berformat"), ("sample", "Sampel gratis"),
                    ("pesan", "Teks pesan penjualan — pesan pribadi, surel dosen, pitch afiliasi")]:
        parts.append(f'<a class="card" href="/copy/{slug}" target="_blank">'
                     f'<div class="meta"><b>{html.escape(t)}</b>'
                     f'<span>{"salin semua teks di halaman ini" if slug == "en-plain" else "buka → Ctrl+A → Ctrl+C → tempel di Description"}</span></div></a>')
    parts.append("</div>")

    parts.append('<h2>Foto marketplace — Inggris</h2><div class="grid">')
    for key, title, note in MKT:
        ext = "png" if key == "hero" and "transparan" in title else "jpg"
        parts.append(card("marketplace", f"Surviving_the_Future_EN_mkt_{key}.{ext}",
                          title, note))
    parts.append("</div>")

    parts.append('<h2>Sampul Gumroad</h2><div class="grid">')
    for root, f, t in [
        ("gumroad", "cover_en_1_hero.png", "EN — sampul 1"),
        ("gumroad", "cover_en_2_inside.png", "EN — sampul 2, halaman asli"),
        ("gumroad", "cover_en_3_quote.png", "EN — sampul 3, kutipan"),
        ("gumroad", "cover_sample_1_hero.png", "Sampel — sampul 1"),
        ("gumroad", "thumb_en.png", "Thumbnail EN"),
        ("gumroad", "thumb_sample.png", "Thumbnail sampel"),
        ("gumroad", "profile_avatar.png", "Avatar profil"),
    ]:
        parts.append(card(root, f, t))
    parts.append("</div>")

    parts.append('<h2>Buku — edisi Inggris (satu-satunya yang dijual)</h2><div class="grid">')
    for tag, slug in EDITIONS:
        for f, t in [
            (f"{slug}_ebook.pdf", f"{tag} — PDF lengkap (sampul + isi)"),
            (f"{slug}_interior.pdf", f"{tag} — PDF interior (untuk cetak)"),
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
.hero{{background:#132538;border:1px solid #2a4056;border-radius:14px;padding:26px 26px 24px;margin:0 0 8px}}
.btn{{display:inline-block;background:var(--amber);color:#151006;font-weight:700;
 font-size:16px;padding:13px 22px;border-radius:9px;text-decoration:none}}
.btn:hover{{filter:brightness(1.08)}}
code{{background:#0d1b2a;border:1px solid var(--line);border-radius:5px;
 padding:2px 6px;font-size:12.5px;color:#f0d9b0;word-break:break-all}}
.meta{{padding:11px 13px 13px;display:flex;flex-direction:column;gap:3px}}
.meta b{{font-size:14px;font-weight:600}}
.meta span{{font-size:11.5px;color:var(--muted);word-break:break-all}}
.meta .sub{{color:var(--amber);opacity:.85}}
</style></head><body>
<h1>Unduhan</h1>
<p class="lede">Klik kartu mana pun untuk mengunduh. Foto marketplace berukuran
3000 × 3000 px, siap diunggah ke Gumroad, Amazon, atau Etsy.</p>
{''.join(parts)}
<h2>Edisi Indonesia</h2>
<p class="lede">Edisi Indonesia tidak dijual. Berkasnya tetap dirender sebagai pembanding
saat menyunting — tidak ditautkan di sini, tidak diunggah ke Gumroad, dan tidak
dipromosikan.</p>
<h2>Cadangan permanen</h2>
<p class="lede">Kalau tautan preview ini berhenti bekerja (sandbox sesi berakhir),
semua berkas yang sama tersedia di repositori:
<a href="https://github.com/SetyoWisodo/SetyoWisodo/tree/arena/3b1aa1ad-setyowisodo/book/publish"
   style="color:var(--amber)">book/publish di GitHub</a>.</p>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.unquote(self.path.split("?")[0])

        if path in ("/", "/index.html"):
            body = build_html(self.headers.get("Host", "")).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path.startswith("/copy/"):
            name = path[len("/copy/"):].strip("/").lower()
            fname = {"en": "listing_en.html", "sample": "listing_sample.html",
                     "en-plain": "listing_en_plain.txt",
                     "pesan": "outreach.html"}.get(name)
            full = os.path.join(PUB, "gumroad", "copy", fname or "")
            if fname and os.path.isfile(full):
                body = open(full, "rb").read()
                # judul H1 dibuang: judul produk sudah ada di kolom Name Gumroad
                body = re.sub(rb"<h1>.*?</h1>", b"", body, count=1, flags=re.S)
                # kotak petunjuk ikut terbuang supaya tidak tersalin saat Ctrl+A
                body = re.sub(rb"<div class=\"hint\">.*?</div>", b"", body, count=1, flags=re.S)
                self.send_response(200)
                ctype = ("text/plain; charset=utf-8" if fname.endswith(".txt")
                         else "text/html; charset=utf-8")
                self.send_header("Content-Type", ctype)
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
