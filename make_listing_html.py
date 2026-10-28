# -*- coding: utf-8 -*-
"""Ubah teks listing menjadi HTML berformat, untuk ditempel ke editor Gumroad.

Kalau teks polos ditempel ke kotak Description, Gumroad membuang semua judul dan
daftar — hasilnya satu dinding paragraf. Membuka HTML ini di browser, menekan
Ctrl+A lalu Ctrl+C, kemudian menempel ke editor Gumroad akan membawa serta
heading, tebal-miring, dan poin-poinnya.

Buka berkas .html di browser -> Ctrl+A -> Ctrl+C -> tempel di Description.

Jalankan: python make_listing_html.py
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
COPY = os.path.join(HERE, "book/publish/gumroad/copy")

FILES = ["listing_en.txt", "listing_id.txt", "listing_bundle.txt", "listing_sample.txt"]

CSS = """
body{font-family:Georgia,'Times New Roman',serif;font-size:17px;line-height:1.62;
     color:#1b1b1b;max-width:720px;margin:48px auto;padding:0 26px;background:#fff}
h1{font-size:30px;line-height:1.2;margin:0 0 6px;letter-spacing:-.01em}
.sub{font-style:italic;color:#8a5a12;font-size:19px;margin:0 0 30px}
h2{font-size:15px;letter-spacing:.13em;text-transform:uppercase;color:#8a5a12;
   margin:38px 0 12px;padding-top:16px;border-top:1px solid #e3e0d8}
p{margin:0 0 15px}
ul{margin:0 0 16px;padding-left:22px}
li{margin-bottom:7px}
em{color:#333}
.hint{font-family:system-ui,sans-serif;font-size:13px;color:#7a7a7a;
      border-left:3px solid #e8a33d;padding:10px 14px;margin-bottom:34px;background:#faf7ef;
      user-select:none;-webkit-user-select:none}
"""


def convert(text):
    lines = text.replace("\r\n", "\n").split("\n")

    # buang baris judul dan garis "===="
    while lines and not lines[0].strip():
        lines.pop(0)
    title = lines.pop(0).strip() if lines else ""
    subtitle = ""
    if lines and lines[0].strip() and not lines[0].startswith("="):
        subtitle = lines.pop(0).strip()
    while lines and (not lines[0].strip() or set(lines[0].strip()) <= {"="}):
        lines.pop(0)

    out = [f"<h1>{html.escape(title)}</h1>"]
    if subtitle:
        out.append(f'<p class="sub">{html.escape(subtitle)}</p>')

    para, items = [], []

    def flush_para():
        if para:
            out.append("<p>" + html.escape(" ".join(para)) + "</p>")
            para.clear()

    def flush_list():
        if items:
            out.append("<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>")
            items.clear()

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        # lanjutan poin: baris menjorok setelah sebuah butir
        if raw.startswith("  ") and line and items:
            items[-1] += " " + line
            i += 1
            continue

        # heading: baris teks diikuti baris garis "-" atau "="
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if line and nxt and set(nxt) <= {"-", "="} and len(nxt) >= 3:
            flush_para()
            flush_list()
            out.append(f"<h2>{html.escape(line)}</h2>")
            i += 2
            continue

        if not line or set(line) <= {"=", "-"}:
            flush_para()
            flush_list()
            i += 1
            continue

        if line.startswith("* "):
            flush_para()
            items.append(line[2:].strip())
            i += 1
            continue

        flush_list()
        para.append(line)
        i += 1

    flush_para()
    flush_list()
    return "\n".join(out)


def build(name):
    src = os.path.join(COPY, name)
    text = open(src, encoding="utf-8").read()
    body = convert(text)

    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(name)}</title><style>{CSS}</style></head><body>
<div class="hint">Tekan <b>Ctrl+A</b> lalu <b>Ctrl+C</b>, kemudian tempel ke kotak
Description di Gumroad. Judul, poin, dan tebal-miring akan ikut terbawa.</div>
{body}
</body></html>"""

    out = os.path.join(COPY, name.replace(".txt", ".html"))
    open(out, "w", encoding="utf-8").write(page)
    print("  %-28s -> %s" % (name, os.path.basename(out)))


if __name__ == "__main__":
    print("HTML siap tempel:")
    for f in FILES:
        build(f)
