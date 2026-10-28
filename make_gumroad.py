# -*- coding: utf-8 -*-
"""Rakit materi listing Gumroad: sampul 16:9, thumbnail, dan teks siap tempel.

Spesifikasi resmi Gumroad (help/article/60):
  cover      minimal 1280 x 720 px, < 50 MB, PNG/JPEG; di sini dirender
             2560 x 1440 supaya tajam di layar retina (Gumroad turunkan ke 4096 max)
  thumbnail  minimal 600 x 600 px; di sini 1600 x 1600

Jalankan: python make_gumroad.py
Keluaran: book/publish/gumroad/
"""
import os
import textwrap

import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "book/publish")
D3 = os.path.join(PUB, "3d")
OUT = os.path.join(PUB, "gumroad")
FONTS = os.path.join(HERE, "book/fonts")

W, H = 2560, 1440                 # 16:9
SQ = 1600                         # thumbnail persegi

NAVY = (11, 22, 36)
NAVY_LO = (18, 34, 52)
AMBER = (232, 163, 61)
IVORY = (246, 243, 235)
MUTED = (150, 165, 182)


def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


SER_B = "SourceSerif4-Semibold.otf"
SER_I = "SourceSerif4-It.otf"
SER_R = "SourceSerif4-Regular.otf"
SAN_B = "SourceSans3-Semibold.otf"
SAN_R = "SourceSans3-Regular.otf"
SAN_L = "SourceSans3-Light.otf"


def background(w, h, glow=(0.72, 0.34)):
    """Latar navy bergradasi + cahaya hangat di belakang buku."""
    img = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        c = tuple(int(NAVY[i] + (NAVY_LO[i] - NAVY[i]) * t * 0.9) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)

    # cahaya lembut
    g = Image.new("L", (w, h), 0)
    gd = ImageDraw.Draw(g)
    cx, cy, r = int(w * glow[0]), int(h * glow[1]), int(h * 0.62)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=90)
    g = g.filter(ImageFilter.GaussianBlur(int(h * 0.14)))
    warm = Image.new("RGB", (w, h), (58, 46, 30))
    img = Image.composite(warm, img, g.point(lambda v: int(v * 1.15)))

    # garis vertikal halus
    d = ImageDraw.Draw(img)
    d.rectangle([int(w * 0.545), 0, int(w * 0.545) + 2, h], fill=(30, 44, 62))
    return img


def place_book(canvas, path, box, shadow=True):
    """Tempel render 3D RGBA ke dalam kotak (x, y, w, h), jaga rasio."""
    bk = Image.open(path).convert("RGBA")
    bb = bk.getchannel("A").getbbox()
    bk = bk.crop(bb)
    x, y, bw, bh = box
    s = min(bw / bk.width, bh / bk.height)
    bk = bk.resize((int(bk.width * s), int(bk.height * s)), Image.LANCZOS)
    px = x + (bw - bk.width) // 2
    py = y + (bh - bk.height) // 2

    if shadow:
        sh = Image.new("L", canvas.size, 0)
        ImageDraw.Draw(sh).rectangle([px, py + bk.height - 30, px + bk.width, py + bk.height + 16],
                                     fill=120)
        sh = sh.filter(ImageFilter.GaussianBlur(38))
        dark = Image.new("RGB", canvas.size, (3, 6, 10))
        canvas.paste(dark, (0, 0), sh)

    canvas.paste(bk, (px, py), bk)
    return px, py, bk.width, bk.height


def book_size(path, box):
    """Ukuran buku (w, h) setelah dipaskan ke kotak (x, y, bw, bh)."""
    bk = Image.open(path).convert("RGBA")
    bk = bk.crop(bk.getchannel("A").getbbox())
    _, _, bw, bh = box
    s = min(bw / bk.width, bh / bk.height)
    return int(bk.width * s), int(bk.height * s)


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(draw, xy, text, font, width, color, line_h):
    x, y = xy
    for ln in wrap(draw, text, font, width):
        draw.text((x, y), ln, font=font, fill=color)
        y += line_h
    return y


def kicker(draw, xy, text, size=40):
    x, y = xy
    f = F(SAN_B, size)
    # huruf renggang
    cx = x
    for ch in text.upper():
        draw.text((cx, y), ch, font=f, fill=AMBER)
        cx += draw.textlength(ch, font=f) + size * 0.17
    draw.line([x, y + size + 18, x + 96, y + size + 18], fill=AMBER, width=5)
    return y + size + 40


# --------------------------------------------------------------------------
def cover_hero(cfg, out):
    """Sampul utama: buku 3D di kiri, judul dan angka di kanan."""
    img = background(W, H)
    d = ImageDraw.Draw(img)

    if "render2" in cfg:
        room = int(W * 0.545) - 60
        p1 = os.path.join(D3, cfg["render"])
        p2 = os.path.join(D3, cfg["render2"])
        w1, h1 = book_size(p1, (0, 0, room, 1200))
        w2, h2 = book_size(p2, (0, 0, room, 1080))
        gap = 46
        total = w1 + w2 + gap
        x0 = (room - total) // 2 + 30
        place_book(img, p1, (x0, 160, w1, 1200))
        place_book(img, p2, (x0 + w1 + gap, 250, w2, 1080))
    else:
        place_book(img, os.path.join(D3, cfg["render"]), (-140, 90, 1500, 1290))
    d = ImageDraw.Draw(img)

    x = int(W * 0.585)
    y = 236
    y = kicker(d, (x, y), cfg["kicker"])

    tw = W - x - 120
    f = F(SER_B, 118)
    for ln in wrap(d, cfg["title"], f, tw):
        d.text((x, y), ln, font=f, fill=IVORY)
        y += 128
    y += 6
    f = F(SER_I, 52)
    for ln in wrap(d, cfg["sub"], f, tw):
        d.text((x, y), ln, font=f, fill=AMBER)
        y += 64
    y += 40

    y = block(d, (x, y), cfg["blurb"], F(SAN_R, 34), tw, MUTED, 48)

    y += 30
    d.line([x, y, x + tw * 0.9, y], fill=(45, 62, 82), width=2)
    y += 34

    # tiga angka penting
    colw = tw / 3
    for i, (num, lab) in enumerate(cfg["stats"]):
        cx = x + i * colw
        d.text((cx, y), num, font=F(SER_B, 66), fill=IVORY)
        ly = y + 84
        for ln in wrap(d, lab, F(SAN_L, 25), colw - 26):
            d.text((cx, ly), ln, font=F(SAN_L, 25), fill=MUTED)
            ly += 32
    return img


def cover_inside(cfg, out):
    """Sampul kedua: deretan halaman asli buku, membuktikan isinya nyata."""
    img = background(W, H, glow=(0.30, 0.45))
    d = ImageDraw.Draw(img)

    doc = pymupdf.open(cfg["pdf"])
    picks = cfg["pages"]
    thumbs = []
    for p in picks:
        pix = doc[p - 1].get_pixmap(dpi=110)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        thumbs.append(im)
    doc.close()

    # halaman ditumpuk miring pada lapisan terpisah, lalu dipotong ke lebar yang diizinkan
    ph = int(H * 0.78)
    base_y = int(H * 0.11)
    xs = [90, 440, 790]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, im in enumerate(thumbs):
        s = ph / im.height
        im = im.resize((int(im.width * s), ph), Image.LANCZOS).convert("RGBA")
        rot = [-7, 0, 7][i]
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))

        sh = Image.new("L", im.size, 0)
        ImageDraw.Draw(sh).rectangle([0, 0, im.width, im.height], fill=150)
        sh = sh.filter(ImageFilter.GaussianBlur(26))
        sh = Image.composite(sh, Image.new("L", im.size, 0), im.getchannel("A"))
        dark = Image.new("RGBA", im.size, (2, 5, 9, 255))
        layer.paste(dark, (xs[i] - 6, base_y + 22), sh)
        layer.paste(im, (xs[i], base_y), im)

    bb = layer.getbbox()
    stack = layer.crop(bb)
    room = int(W * 0.50) - 70           # ruang yang tersedia sebelum kolom teks
    if stack.width > room:
        k = room / stack.width
        stack = stack.resize((int(stack.width * k), int(stack.height * k)), Image.LANCZOS)
    img.paste(stack, (70, (H - stack.height) // 2 + 20), stack)
    d = ImageDraw.Draw(img)

    x = int(W * 0.60)
    y = 250
    y = kicker(d, (x, y), cfg["inside_kicker"])
    tw = W - x - 110
    f = F(SER_B, 76)
    for ln in wrap(d, cfg["inside_title"], f, tw):
        d.text((x, y), ln, font=f, fill=IVORY)
        y += 86
    y += 26
    y = block(d, (x, y), cfg["inside_body"], F(SAN_R, 33), tw, MUTED, 47)

    y += 36
    # susutkan ukuran poin bila daftar tidak muat sampai bawah halaman
    for fs, lead in ((31, 42), (29, 39), (27, 36), (25, 34), (23, 32)):
        probe = y
        for item in cfg["inside_list"]:
            probe = block(d, (x + 34, probe), item, F(SAN_R, fs), tw - 34, IVORY, lead) + 12
        if probe <= H - 70:
            break
    for item in cfg["inside_list"]:
        d.ellipse([x, y + int(fs * 0.38), x + 11, y + int(fs * 0.38) + 11], fill=AMBER)
        y = block(d, (x + 34, y), item, F(SAN_R, fs), tw - 34, IVORY, lead) + 12
    return img


def cover_quote(cfg, out):
    """Sampul ketiga: satu kalimat besar dari sampul belakang."""
    img = background(W, H, glow=(0.5, 0.5))
    d = ImageDraw.Draw(img)

    place_book(img, os.path.join(D3, cfg["render"]), (W - 1060, 120, 900, 1200))
    d = ImageDraw.Draw(img)

    x = 170
    tw = int(W * 0.50) - x
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    y = 0
    dl.text((x, y), "\u201c", font=F(SER_B, 260), fill=AMBER)
    y += 215

    f = F(SER_I, 86)
    for ln in wrap(dl, cfg["quote"], f, tw):
        dl.text((x, y), ln, font=f, fill=IVORY)
        y += 112

    y += 40
    dl.line([x, y, x + 120, y], fill=AMBER, width=6)
    y += 46
    for ln in wrap(dl, cfg["quote_src"], F(SAN_B, 34), tw):
        dl.text((x, y), ln, font=F(SAN_B, 34), fill=MUTED)
        y += 44

    bb = layer.getbbox()
    text = layer.crop(bb)
    img.paste(text, (x, (H - text.height) // 2), text)
    return img


def thumb(cfg):
    """Thumbnail 1600x1600 untuk Discover, perpustakaan pembeli, dan profil."""
    img = Image.new("RGB", (SQ, SQ), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(SQ):
        t = y / SQ
        d.line([(0, y), (SQ, y)],
               fill=tuple(int(NAVY[i] + (NAVY_LO[i] - NAVY[i]) * t) for i in range(3)))

    place_book(img, os.path.join(D3, cfg["render"]), (-60, 120, SQ + 120, 1120))
    d = ImageDraw.Draw(img)

    y = 1290
    f = F(SER_B, 104)
    for ln in wrap(d, cfg["thumb_title"], f, SQ - 160):
        d.text((80, y), ln, font=f, fill=IVORY)
        y += 112
    d.text((80, SQ - 104), cfg["thumb_foot"], font=F(SAN_B, 40), fill=AMBER)
    return img


# --------------------------------------------------------------------------
EN = dict(
    render="Surviving_the_Future_EN_3d_transparent.png",
    pdf=os.path.join(HERE, "Surviving_the_Future.pdf"),
    kicker="The evidence edition",
    title="Surviving the Future",
    sub="Crisis, Climate, and Human Resilience",
    blurb="Twenty-four chapters on heat, flood, drought, fire, food, water, migration "
          "and conflict \u2014 written for readers who want the evidence, not the slogan.",
    stats=[("24", "chapters"), ("152", "sources"), ("457", "pages")],
    pages=[20, 34, 50],
    inside_kicker="Look inside",
    inside_title="Real pages, real data",
    inside_body="No stock imagery and no filler. Every chapter carries its own case study, "
                "its own table, and the observation that would prove it wrong.",
    inside_list=[
        "25 data tables and 11 figures, each traceable to a named source",
        "24 case studies: Bhola 1970, Amphan 2020, Chicago 1995, the Ahr valley 2021",
        "Emergency checklists and a local risk profile you can fill in for your street",
        "Glossary, analytical caveats and a full index",
    ],
    quote="A prepared world is not a world without disasters. It is a world where disasters "
          "stop being surprises.",
    quote_src="From the back cover",
    thumb_title="Surviving the Future",
    thumb_foot="457 pages  \u00b7  English",
)

ID = dict(
    render="Bertahan_Hidup_di_Masa_Depan_ID_3d_transparent.png",
    pdf=os.path.join(HERE, "Surviving_the_Future_ID.pdf"),
    kicker="Edisi bukti",
    title="Bertahan Hidup di Masa Depan",
    sub="Krisis, Iklim, dan Ketahanan Manusia",
    blurb="Dua puluh empat bab tentang panas, banjir, kekeringan, kebakaran, pangan, air, "
          "migrasi, dan konflik \u2014 untuk pembaca yang ingin bukti, bukan slogan.",
    stats=[("24", "bab"), ("152", "sumber"), ("473", "halaman")],
    pages=[21, 35, 51],
    inside_kicker="Lihat isinya",
    inside_title="Halaman asli, data asli",
    inside_body="Tanpa gambar stok dan tanpa isi tambahan. Setiap bab membawa studi kasusnya "
                "sendiri, tabelnya sendiri, dan pengamatan yang akan membuktikannya salah.",
    inside_list=[
        "25 tabel data dan 11 gambar, semuanya dapat ditelusuri ke sumber bernama",
        "24 studi kasus: Bhola 1970, Amphan 2020, Chicago 1995, Lembah Ahr 2021",
        "Ceklis darurat dan profil risiko lokal yang bisa Anda isi sendiri di jalan Anda",
        "Glosarium, catatan analitis, dan indeks lengkap",
    ],
    quote="Dunia yang siap bukan dunia tanpa bencana. Dunia yang siap adalah dunia ketika "
          "bencana berhenti menjadi kejutan.",
    quote_src="Dari sampul belakang",
    thumb_title="Bertahan Hidup di Masa Depan",
    thumb_foot="473 halaman  \u00b7  Indonesia",
)

BUNDLE = dict(
    render="Surviving_the_Future_EN_3d_transparent.png",
    kicker="Bilingual bundle",
    title="Two languages, one argument",
    sub="Surviving the Future + Bertahan Hidup di Masa Depan",
    blurb="Both editions in one purchase: 930 pages, 304 sources and citations, "
          "the same 24 chapters written separately for each readership.",
    render2="Bertahan_Hidup_di_Masa_Depan_ID_3d_transparent.png",
    stats=[("2", "editions"), ("930", "pages"), ("24", "chapters")],
    quote="Two editions, one argument: the hazard is not the disaster. The decision is.",
    quote_src="Buy both, read either",
    thumb_title="Both editions",
    thumb_foot="930 pages  \u00b7  EN + ID",
)

SAMPLE = dict(
    render="Surviving_the_Future_EN_3d_transparent.png",
    kicker="Free sample",
    title="Read the first chapter",
    sub="35 of 457 pages, free",
    blurb="Full table of contents, the preface, all of Chapter 1, and one data spread. "
          "No email wall on the download itself.",
    stats=[("35", "pages"), ("1", "chapter"), ("0", "cost")],
    thumb_title="Free sample",
    thumb_foot="35 pages  \u00b7  free",
)


def avatar(initials="SW", sub="Setyo Wisodo"):
    """Foto profil 800x800: monogram, bukan sampul buku.

    Memakai sampul akan mengikat akun ke satu judul; monogram tetap dipakai
    saat buku berikutnya terbit."""
    N = 800
    img = Image.new("RGB", (N, N), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(N):
        t = y / N
        d.line([(0, y), (N, y)],
               fill=tuple(int(NAVY[i] + (NAVY_LO[i] - NAVY[i]) * t * 1.15) for i in range(3)))

    # bingkai tipis
    d.rectangle([36, 36, N - 36, N - 36], outline=(38, 54, 74), width=2)

    f = F(SER_B, 250)
    tw = d.textlength(initials, font=f)
    d.text(((N - tw) / 2, 232), initials, font=f, fill=IVORY)

    d.line([(N / 2 - 52, 545), (N / 2 + 52, 545)], fill=AMBER, width=5)

    f2 = F(SAN_B, 34)
    tw2 = d.textlength(sub, font=f2)
    d.text(((N - tw2) / 2, 590), sub, font=f2, fill=MUTED)
    return img


def save(img, name, note):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    img.save(p, optimize=True)
    print("  %-42s %sx%s  %s" % (note, img.width, img.height,
                                 "%d KB" % (os.path.getsize(p) // 1024)))


if __name__ == "__main__":
    print("materi Gumroad:")
    save(cover_hero(EN, None), "cover_en_1_hero.png", "EN cover 1 hero")
    save(cover_inside(EN, None), "cover_en_2_inside.png", "EN cover 2 inside")
    save(cover_quote(EN, None), "cover_en_3_quote.png", "EN cover 3 quote")
    save(cover_hero(ID, None), "cover_id_1_hero.png", "ID cover 1 hero")
    save(cover_inside(ID, None), "cover_id_2_inside.png", "ID cover 2 inside")
    save(cover_quote(ID, None), "cover_id_3_quote.png", "ID cover 3 quote")
    save(cover_hero(BUNDLE, None), "cover_bundle_1_hero.png", "Bundle cover 1 hero")
    save(cover_quote(BUNDLE, None), "cover_bundle_2_quote.png", "Bundle cover 2 quote")
    save(cover_hero(SAMPLE, None), "cover_sample_1_hero.png", "Sample cover 1 hero")

    save(thumb(EN), "thumb_en.png", "EN thumbnail")
    save(thumb(ID), "thumb_id.png", "ID thumbnail")
    save(thumb(BUNDLE), "thumb_bundle.png", "Bundle thumbnail")
    save(thumb(SAMPLE), "thumb_sample.png", "Sample thumbnail")
    save(avatar(), "profile_avatar.png", "Profile avatar")
