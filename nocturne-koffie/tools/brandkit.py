#!/usr/bin/env python3
"""
Brand kit Nocturne Koffie — generator aset cetak & digital.

Menulis ke folder brand/:
  logo-mark.svg · logo-lockup.svg · favicon.svg
  og-1200x630.jpg
  label-<produk>.png        (label kantong 70 × 100 mm, 300 dpi)
  label-sheet-a4.png        (8 label siap cetak di A4)
  colophon.md               (aturan pakai + isi setiap berkas)

Pakai:
    python3 tools/brandkit.py
    python3 tools/brandkit.py --tanggal 2026-11-02 --batch A

Hanya butuh Pillow. Font memakai Source Sans 3 / Source Serif 4 yang ada di repo.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from datetime import date

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "brand")
FONTS = os.path.join(os.path.dirname(ROOT), "book", "fonts")

SANS_BLACK = os.path.join(FONTS, "SourceSans3-Black.otf")
SANS_BOLD = os.path.join(FONTS, "SourceSans3-Bold.otf")
SANS_SEMI = os.path.join(FONTS, "SourceSans3-Semibold.otf")
SANS = os.path.join(FONTS, "SourceSans3-Regular.otf")
SANS_IT = os.path.join(FONTS, "SourceSans3-It.otf")
SERIF = os.path.join(FONTS, "SourceSerif4-Regular.otf")
SERIF_IT = os.path.join(FONTS, "SourceSerif4-It.otf")
SERIF_BOLD = os.path.join(FONTS, "SourceSerif4-Bold.otf")

PAPER = (245, 239, 228)
PAPER2 = (239, 230, 214)
INK = (22, 17, 13)
ESPRESSO = (74, 44, 26)
ORANGE = (225, 84, 43)
GOLD = (217, 164, 65)

F = lambda path, size: ImageFont.truetype(path, size)


def rupiah(n):
    return "Rp" + f"{int(n):,}".replace(",", ".")


# ───────────────────────────── tekstur & alat ─────────────────────────────
def paper_canvas(w, h, base=PAPER):
    """Latar kertas dengan grain halus — tanpa aset eksternal."""
    img = Image.new("RGB", (w, h), base)
    random.seed(w * 7 + h)
    noise = Image.new("L", (w // 3, h // 3))
    px = noise.load()
    for y in range(noise.height):
        for x in range(noise.width):
            px[x, y] = random.randint(118, 138)
    noise = noise.resize((w, h), Image.BILINEAR).convert("RGB")
    img = Image.blend(img, noise, 0.035)
    return img


def fit_font(draw, text, path, max_w, start, min_size=10):
    size = start
    while size > min_size:
        f = F(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return F(path, min_size)


def tracked(draw, xy, text, font, fill, tracking=0, anchor_center=False):
    """Teks dengan letter-spacing (PIL belum mendukung tracking)."""
    if tracking == 0:
        draw.text(xy, text, font=font, fill=fill, anchor="mm" if anchor_center else "la")
        return
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor_center:
        x -= total / 2
    for c, cw in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += cw + tracking


def mark(draw, cx, cy, r, color=INK, gap_ratio=0.095):
    """Simbol brand: bulatan dengan celah tipis (motif yang sama dengan logo)."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    gap = max(2, int(r * 2 * gap_ratio))
    draw.rectangle([cx - gap / 2, cy - r - 2, cx + gap / 2, cy + r + 2], fill=PAPER if color != PAPER else INK)


def roast_dots(draw, x, y, r, gap, level, color=INK, total=5):
    for i in range(total):
        cx = x + i * (r * 2 + gap)
        box = [cx - r, y - r, cx + r, y + r]
        if i < level:
            draw.ellipse(box, fill=color)
        else:
            draw.ellipse(box, outline=color, width=max(2, r // 4))


# ───────────────────────────────── logo (SVG) ─────────────────────────────
def svg_logo_mark():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-label="Nocturne Koffie">
  <title>Nocturne Koffie — simbol</title>
  <circle cx="60" cy="60" r="56" fill="#16110D"/>
  <rect x="54.7" y="0" width="10.6" height="120" fill="#F5EFE4"/>
  <circle cx="60" cy="60" r="56" fill="none" stroke="#16110D" stroke-width="0"/>
</svg>
"""


def svg_logo_lockup(dark=False):
    bg = "#F5EFE4" if not dark else "#16110D"
    fg = "#16110D" if not dark else "#F5EFE4"
    sub = "#16110D" if not dark else "#F5EFE4"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 120" role="img" aria-label="Nocturne Koffie Brand">
  <title>Nocturne Koffie — lockup</title>
  <rect width="420" height="120" fill="{bg}"/>
  <g transform="translate(16,26)">
    <circle cx="34" cy="34" r="34" fill="{fg}"/>
    <rect x="30.5" y="0" width="7" height="68" fill="{bg}"/>
  </g>
  <text x="104" y="62" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="40"
        font-weight="800" letter-spacing="-1.2" fill="{fg}">Nocturne</text>
  <text x="106" y="86" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="10.5"
        font-weight="600" letter-spacing="5.2" fill="{sub}" opacity=".62">KOFFIE BRAND</text>
</svg>
"""


def svg_favicon():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="12" fill="#16110D"/>
  <circle cx="32" cy="32" r="20" fill="#F5EFE4"/>
  <rect x="29.2" y="12" width="5.6" height="40" fill="#16110D"/>
</svg>
"""


# ─────────────────────────────── OG image ─────────────────────────────────
def buat_og(path):
    W, H = 1200, 630
    img = paper_canvas(W, H)
    d = ImageDraw.Draw(img)

    # garis tepi tipis
    d.rectangle([24, 24, W - 24, H - 24], outline=(*INK, 255), width=1)

    # lockup kiri atas
    mark(d, 62, 66, 15, INK)
    d.text((90, 52), "Nocturne", font=F(SANS_BLACK, 26), fill=INK)
    tracked(d, (91, 82), "KOFFIE BRAND", F(SANS_SEMI, 9), (110, 100, 92), tracking=3.4)

    # headline
    f1 = F(SANS_BLACK, 86)
    f2 = F(SANS_BLACK, 86)
    d.text((58, 176), "Kopi dari petani.", font=f1, fill=INK)
    d.text((58, 268), "Diseduh untukmu.", font=f2, fill=ESPRESSO)

    # paragraf
    body = F(SANS, 21)
    d.multiline_text((60, 388),
                     "Sembilan kopi. Nama petani, desa, dan ketinggian\n"
                     "kebunnya tercantum di setiap kemasan.\n"
                     "Disangrai mingguan di Banyuwangi.",
                     font=body, fill=(60, 50, 44), spacing=8)

    # blok kanan: tanggal sangrai + kontak
    d.rectangle([862, 170, 1140, 462], fill=INK)
    d.text((892, 196), "SETIAP KEMASAN", font=F(SANS_SEMI, 12), fill=GOLD)
    for i, t in enumerate(["tanggal sangrai", "kode batch", "nama petani", "elevasi kebun"]):
        d.text((892, 226 + i * 38), "— " + t, font=F(SANS, 19), fill=(245, 239, 228))
    d.line([892, 392, 1110, 392], fill=(110, 100, 92), width=1)
    d.text((892, 406), "nocturnekoffie.id", font=F(SANS_SEMI, 17), fill=(245, 239, 228))

    # garis aksen
    d.rectangle([58, 500, 260, 506], fill=ORANGE)

    # kaki
    d.text((58, 530), "Brand kopi · Banyuwangi, Jawa Timur", font=F(SANS, 17), fill=(110, 100, 92))
    d.text((W - 58 - d.textlength("+62 898-8188-800", font=F(SANS_SEMI, 17)), 530),
           "+62 898-8188-800", font=F(SANS_SEMI, 17), fill=INK)

    img.save(path, quality=92, optimize=True, progressive=True)
    return path


# ─────────────────────────────── label kantong ────────────────────────────
def _stempel(img, xy, teks1, teks2, r=86, sudut=-9):
    """Stempel QC bulat — dibuat di layer terpisah lalu diputar."""
    size = r * 2 + 8
    lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = size // 2
    d.ellipse([c - r, c - r, c + r, c + r], outline=(*ORANGE, 235), width=4)
    d.ellipse([c - r + 10, c - r + 10, c + r - 10, c + r - 10], outline=(*ORANGE, 150), width=1)
    f1 = F(SANS_BLACK, 22)
    f2 = F(SANS_SEMI, 10)
    w1 = d.textlength(teks1, font=f1)
    d.text((c - w1 / 2, c - 26), teks1, font=f1, fill=(*ORANGE, 240))
    w2 = d.textlength(teks2, font=f2)
    d.text((c - w2 / 2, c + 4), teks2, font=f2, fill=(*ORANGE, 235))
    lay = lay.rotate(sudut, resample=Image.BICUBIC, expand=False)
    img.paste(lay, xy, lay)


def buat_label(produk, batch, tanggal, path, w=827, h=1181, skor=None):
    """Label 70 × 100 mm @300 dpi."""
    img = paper_canvas(w, h).convert("RGBA")
    d = ImageDraw.Draw(img)
    M = 58

    d.rectangle([M * 0.5, M * 0.5, w - M * 0.5, h - M * 0.5], outline=(198, 186, 168), width=1)

    # ── kepala
    mark(d, M + 12, M + 10, 10, INK)
    tracked(d, (M + 32, M + 3), "NOCTURNE KOFFIE", F(SANS_BOLD, 11), INK, tracking=2.2)
    tracked(d, (M + 32, M + 20), "KOFFIE BRAND", F(SANS_SEMI, 7), (120, 108, 96), tracking=2.6)

    d.text((M, M + 54), f"{produk['kind'].upper()} · {produk['process'].upper()}",
           font=F(SANS_SEMI, 11), fill=(120, 108, 96))
    d.line([M, M + 76, w - M, M + 76], fill=INK, width=2)

    # ── nama produk (maks 2 baris)
    name = produk["name"].upper()
    size = 66
    while size > 26:
        f = F(SANS_BLACK, size)
        words = name.split()
        if len(words) > 1:
            mid = (len(words) + 1) // 2
            l1, l2 = " ".join(words[:mid]), " ".join(words[mid:])
            widest = max(d.textlength(l1, font=f), d.textlength(l2, font=f))
        else:
            l1, l2, widest = name, "", d.textlength(name, font=f)
        if widest <= w - M * 2:
            break
        size -= 2
    f_name = F(SANS_BLACK, size)
    y = M + 96
    d.text((M, y), l1, font=f_name, fill=INK)
    if l2:
        d.text((M, y + size * 0.98), l2, font=f_name, fill=INK)
    y += size * 0.98 * (2 if l2 else 1) + 30
    d.line([M, y, w - M, y], fill=(198, 186, 168), width=1)

    # ── petani / komposisi
    y += 24
    d.text((M, y), "DITANAM OLEH" if produk.get("farmer_type") != "blend" else "SIGNATURE BLEND",
           font=F(SANS_SEMI, 9), fill=ORANGE)
    y += 21
    if produk.get("farmer_type") == "blend":
        f_farmer = fit_font(d, produk.get("composition", ""), SERIF_IT, w - M * 2, 24)
        lines = produk.get("composition", "").replace(" · ", "\n").split("\n")
        for ln in lines:
            d.text((M, y), ln, font=fit_font(d, ln, SERIF_IT, w - M * 2, 24), fill=INK)
            y += 30
        y += 8
        varietas = produk.get("variety", "")
    else:
        f_farmer = fit_font(d, produk["farmer"], SERIF_BOLD, w - M * 2, 32)
        d.text((M, y), produk["farmer"], font=f_farmer, fill=INK)
        y += 46
        wilayah = ", ".join([x for x in (produk.get("village"), produk.get("district"), produk.get("region")) if x])
        d.text((M, y), wilayah, font=fit_font(d, wilayah, SANS, w - M * 2, 16), fill=(70, 60, 52))
        y += 26
        f_key, f_val = F(SANS, 14), F(SANS_SEMI, 14)
        d.text((M, y), "Ketinggian", font=f_key, fill=(132, 120, 106))
        d.text((M + 112, y), produk.get("elevation", "—"), font=f_val, fill=INK)
        y += 22
        d.text((M, y), "Varietas", font=f_key, fill=(132, 120, 106))
        d.text((M + 112, y), produk.get("variety", "—"),
               font=fit_font(d, produk.get("variety", "—"), SANS_SEMI, w - M - 112, 14), fill=INK)
        y += 30
        varietas = produk.get("variety", "")

    # ── catatan rasa
    y += 8
    d.line([M, y, w - M, y], fill=(198, 186, 168), width=1)
    y += 22
    d.text((M, y), "CATATAN RASA", font=F(SANS_SEMI, 9), fill=(132, 120, 106))
    y += 20
    rasa = " · ".join(produk.get("notes", []))
    d.text((M, y), rasa, font=fit_font(d, rasa, SERIF_IT, w - M * 2, 26), fill=ESPRESSO)
    y += 40

    # ── rekomendasi seduh
    seduh = " · ".join(produk.get("brew", []))
    d.text((M, y), "SEDUH", font=F(SANS_SEMI, 9), fill=(132, 120, 106))
    d.text((M + 58, y - 1), seduh, font=fit_font(d, seduh, SANS, w - M - 58, 14), fill=(70, 60, 52))

    # ── zona editorial bawah: nomor seri (kiri) + elevasi/komposisi (kanan)
    zona_y = h - 560
    seri = f"{int(produk.get('no', '0') or 0):02d}"
    d.text((M - 6, zona_y), seri, font=F(SANS_BLACK, 132), fill=PAPER2)
    d.text((M, zona_y + 142), f"SERI {seri} / 09 · {produk.get('category', '').upper()}",
           font=F(SANS_SEMI, 9), fill=(176, 164, 148))

    if produk.get("farmer_type") == "blend":
        komp = produk.get("variety", "")
        komp_short = "70/30" if "70%" in komp else ("60/40" if "60%" in komp else "—")
        f_big = F(SANS_BLACK, 96)
        lebar = d.textlength(komp_short, font=f_big)
        d.text((w - M - lebar, zona_y - 6), komp_short, font=f_big, fill=PAPER2)
        d.text((w - M - d.textlength("KOMPOSISI", font=F(SANS_SEMI, 9)), zona_y + 102), "KOMPOSISI",
               font=F(SANS_SEMI, 9), fill=(176, 164, 148))
    else:
        angka = (produk.get("elevation") or "").split("–")[0].replace(".", "").strip()
        if angka.isdigit():
            f_big = F(SANS_BLACK, 96)
            lebar = d.textlength(angka, font=f_big)
            d.text((w - M - lebar, zona_y - 6), angka, font=f_big, fill=PAPER2)
            d.text((w - M - d.textlength("mdpl", font=F(SANS_SEMI, 11)), zona_y + 100), "mdpl",
                   font=F(SANS_SEMI, 11), fill=(176, 164, 148))

    # ── stempel QC (opsional, hanya bila skor tersedia)
    if skor:
        _stempel(img, (w - M - 168, h - 742), f"{skor:g}", "DIPERIKSA · QC", r=66)

    # ── blok gelap: tanggal, batch, level roast
    by = h - 300
    d.rectangle([M, by, w - M, by + 178], fill=INK)
    d.text((M + 26, by + 22), "TANGGAL SANGRAI", font=F(SANS_SEMI, 9), fill=GOLD)
    d.text((M + 26, by + 40), tanggal.strftime("%d.%m.%Y"), font=F(SANS_BLACK, 40), fill=PAPER)
    d.text((M + 26, by + 98), "KODE BATCH", font=F(SANS_SEMI, 9), fill=GOLD)
    d.text((M + 26, by + 114), batch, font=F(SANS_SEMI, 21), fill=PAPER)

    d.text((w - M - 26 - 132, by + 22), "LEVEL ROAST", font=F(SANS_SEMI, 9), fill=GOLD)
    roast_dots(d, w - M - 26 - 126, by + 76, 9, 11, produk.get("roast_level", 3), color=PAPER)
    d.text((w - M - 26 - 132, by + 100), f"{produk.get('roast_level', 3)}/5", font=F(SANS_SEMI, 13), fill=PAPER)

    # ── kaki
    fy = h - 96
    d.line([M, fy - 18, w - M, fy - 18], fill=(198, 186, 168), width=1)
    d.text((M, fy), "Disangrai mingguan oleh Ais Coffee Roastery,", font=F(SANS, 12), fill=(120, 108, 96))
    d.text((M, fy + 20), "dikemas dan dikirim dari Banyuwangi.", font=F(SANS, 12), fill=(120, 108, 96))
    d.text((w - M - d.textlength("nocturnekoffie.id", font=F(SANS_SEMI, 12)), fy),
           "nocturnekoffie.id", font=F(SANS_SEMI, 12), fill=INK)

    img.convert("RGB").save(path, quality=94, optimize=True)
    return path


def buat_sheet(produk_list, paths, path):
    """A4 (2480 × 3508 @300dpi) berisi 8 label 70×100 mm + garis potong."""
    W, H = 2480, 3508
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    lw, lh = 827, 1181
    cols, rows = 2, 3
    gapx = (W - cols * lw) // (cols + 1)
    gapy = (H - rows * lh) // (rows + 1)
    i = 0
    for r in range(rows):
        for c in range(cols):
            if i >= len(paths):
                break
            x = gapx + c * (lw + gapx)
            y = gapy + r * (lh + gapy)
            lab = Image.open(paths[i]).convert("RGB")
            sheet.paste(lab, (x, y))
            # tanda potong
            for cx in (x, x + lw):
                d.line([cx, y - 14, cx, y - 4], fill=(160, 160, 160), width=1)
                d.line([cx, y + lh + 4, cx, y + lh + 14], fill=(160, 160, 160), width=1)
            for cy in (y, y + lh):
                d.line([x - 14, cy, x - 4, cy], fill=(160, 160, 160), width=1)
                d.line([x + lw + 4, cy, x + lw + 14, cy], fill=(160, 160, 160), width=1)
            i += 1
    d.text((gapx, 60), "NOCTURNE KOFFIE — LEMBAR LABEL (A4 · 8 label 70 × 100 mm)",
           font=F(SANS_SEMI, 26), fill=(90, 90, 90))
    sheet.save(path, quality=92, optimize=True)


def buat_halaman_brand():
    """Halaman brand kit: semua aset dalam satu tampilan, siap dibagikan ke desainer/cetak."""
    import glob
    labels = sorted(glob.glob(os.path.join(OUT, "label-*.png")))
    labels = [os.path.basename(x) for x in labels if "sheet" not in x]
    kartu = "".join(
        f'<figure><img src="{os.path.basename(l)}" alt="Label {os.path.basename(l)}" loading="lazy">'
        f'<figcaption>{os.path.basename(l).replace("label-", "").replace(".png", "").replace("-", " ")}</figcaption></figure>'
        for l in labels)
    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brand Kit — Nocturne Koffie</title>
<style>
:root{{--paper:#F5EFE4;--ink:#16110D;--muted:#6b6156;--gold:#D9A441;--orange:#E1542B;--line:1px solid rgba(22,17,13,.16)}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 Inter,system-ui,sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:44px clamp(16px,4vw,40px) 80px}}
h1{{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(30px,5vw,46px);line-height:1;letter-spacing:-.03em;margin:8px 0 10px}}
.kicker{{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}}
.lede{{max-width:60ch;color:var(--muted)}}
h2{{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:12px;letter-spacing:.18em;text-transform:uppercase;
   color:var(--muted);border-top:2px solid var(--ink);padding-top:12px;margin:44px 0 16px}}
.row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}}
.sw{{border-radius:6px;height:96px;border:var(--line)}}
.sw span{{display:block;padding:8px 10px;font-size:11px;letter-spacing:.06em}}
figure{{margin:0;border:var(--line);background:#fff;border-radius:4px;overflow:hidden}}
figure img{{width:100%;display:block}}
figcaption{{padding:8px 10px;font-size:12px;color:var(--muted);text-transform:capitalize;border-top:var(--line)}}
.logos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}
.logos img{{width:100%;display:block;border:var(--line);border-radius:4px;background:#fff}}
.og{{width:100%;border:var(--line);border-radius:4px}}
a{{color:inherit}}
.note{{font-size:12.5px;color:var(--muted);border-left:2px solid var(--gold);padding-left:12px;margin-top:14px}}
</style></head><body><div class="wrap">
<p class="kicker">Brand kit · dihasilkan oleh tools/brandkit.py</p>
<h1>Nocturne Koffie</h1>
<p class="lede">Semua aset cetak & digital dalam satu tempat. Label memakai ukuran 70 × 100 mm @300 dpi,
siap ditempel ke kantong black matte 250 g. Tanggal sangrai, kode batch, dan level roast
diisi otomatis dari <code>data/catalog.json</code> + <code>data/batch-qc.csv</code>.</p>

<h2>Logo</h2>
<div class="logos">
  <img src="logo-mark.svg" alt="Simbol Nocturne">
  <img src="logo-lockup.svg" alt="Lockup Nocturne gelap di atas kertas">
  <img src="logo-lockup-dark.svg" alt="Lockup Nocturne terang di atas tinta">
</div>
<p class="note">Simbol = bulatan dengan celah 9,5% — motif yang sama dipakai sebagai penanda level roast
dan peluru daftar di situs. Jangan memberi warna lain, gradien, atau bayangan.</p>

<h2>Palet</h2>
<div class="row">
  <div class="sw" style="background:#F5EFE4"><span>Paper · #F5EFE4</span></div>
  <div class="sw" style="background:#16110D;color:#F5EFE4"><span>Ink · #16110D</span></div>
  <div class="sw" style="background:#E1542B;color:#fff"><span>Burnt Orange · #E1542B</span></div>
  <div class="sw" style="background:#4A2C1A;color:#F5EFE4"><span>Espresso · #4A2C1A</span></div>
  <div class="sw" style="background:#D9A441"><span>Roast Gold · #D9A441</span></div>
</div>

<h2>Kartu berbagi (Open Graph)</h2>
<img class="og" src="og-1200x630.jpg" alt="Kartu OG Nocturne 1200 × 630">
<p class="note">Dipakai saat tautan dibagikan di WhatsApp, Instagram, X, dan Facebook. Ukuran 1200 × 630 px.</p>

<h2>Label kantong — 9 SKU</h2>
<div class="row">{kartu}</div>
<p class="note">Cetak: <b>label-sheet-a4.png</b> (8 label per lembar A4, ada tanda potong) atau
label per produk untuk cetak stiker roll. Ganti tanggal & batch lewat
<code>python3 tools/brandkit.py --tanggal YYYY-MM-DD --batch A</code>.</p>

<h2>Ikon aplikasi</h2>
<div class="logos" style="grid-template-columns:120px 1fr">
  <img src="apple-touch-icon.png" alt="Ikon 180 px" style="border-radius:24px">
  <img src="favicon.svg" alt="Favicon" style="max-width:120px">
</div>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tanggal", default=None, help="YYYY-MM-DD tanggal sangrai (default: hari ini)")
    ap.add_argument("--batch", default="A", help="suffix kode batch (A/B/C)")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(ROOT, "data", "catalog.json"), encoding="utf-8") as f:
        catalog = json.load(f)

    tgl = date.fromisoformat(args.tanggal) if args.tanggal else date.today()

    # skor cupping terakhir yang lolos, per produk (untuk stempel QC)
    skor = {}
    qc_path = os.path.join(ROOT, "data", "batch-qc.csv")
    if os.path.exists(qc_path):
        import csv as _csv
        with open(qc_path, encoding="utf-8-sig") as fq:
            for row in _csv.DictReader(fq):
                if (row.get("status") or "").lower() != "lolos":
                    continue
                try:
                    skor[row["produk"].strip()] = float(row["skor_cupping"])
                except (KeyError, ValueError):
                    continue

    open(os.path.join(OUT, "logo-mark.svg"), "w", encoding="utf-8").write(svg_logo_mark())
    open(os.path.join(OUT, "logo-lockup.svg"), "w", encoding="utf-8").write(svg_logo_lockup())
    open(os.path.join(OUT, "logo-lockup-dark.svg"), "w", encoding="utf-8").write(svg_logo_lockup(dark=True))
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(svg_favicon())

    buat_og(os.path.join(OUT, "og-1200x630.jpg"))

    # label per produk (9 SKU)
    paths = []
    kode = {"gayo": "GYO", "kintamani": "KTM", "blue-mount-ijen": "IJN", "semeru": "SMR",
            "arjuno": "ARJ", "raung": "RNG", "ijen-excelsa": "EXC",
            "blend-7030": "B70", "blend-6040": "B60"}
    for p in catalog["products"]:
        b = f"NK-{kode.get(p['id'], p['id'][:3].upper())}-{tgl.strftime('%y%m')}-{args.batch}"
        path = os.path.join(OUT, f"label-{p['id']}.png")
        buat_label(p, b, tgl, path, skor=skor.get(p['id']))
        paths.append(path)

    buat_sheet(catalog["products"], paths[:6], os.path.join(OUT, "label-sheet-a4.png"))

    # favicon raster
    icon = Image.new("RGB", (180, 180), INK)
    d = ImageDraw.Draw(icon)
    d.rounded_rectangle([0, 0, 180, 180], radius=34, fill=INK)
    d.ellipse([34, 34, 146, 146], fill=PAPER)
    d.rectangle([82, 20, 98, 160], fill=INK)
    icon.save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(buat_halaman_brand())

    print("Brand kit dibuat di", OUT)
    for f in sorted(os.listdir(OUT)):
        print("  -", f, f"{os.path.getsize(os.path.join(OUT, f))//1024} KB")


if __name__ == "__main__":
    main()
