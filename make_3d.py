# -*- coding: utf-8 -*-
"""Render 3D buku (sampul + tebal punggung) untuk tampilan marketplace.

Geometri memakai ukuran nyata dari build_report.json:
potong 8,27 x 11,69 inci, tebal punggung 1,075 inci (EN) / 1,113 inci (ID).
Jadi punggung pada gambar bukan hiasan — skalanya sama dengan file cetak.

Keluaran di book/publish/3d/:
  *_3d_square.png        2000 x 2000, latar putih  (gambar utama marketplace)
  *_3d_transparent.png   2000 x 2000, latar transparan (untuk banner toko)
  *_3d_front.png         2000 x 2000, tampak depan + punggung tipis
  pair_3d_square.png     2000 x 2000, kedua edisi berdampingan

Jalankan: python make_3d.py
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "book/publish")
OUT = os.path.join(PUB, "3d")
FONTS = os.path.join(HERE, "book/fonts")

NAVY = (10, 19, 32)
AMBER = (232, 163, 61)
IVORY = (246, 243, 235)
PAPER = (238, 232, 214)

SERIF_B = os.path.join(FONTS, "SourceSerif4-Semibold.otf")
SANS = os.path.join(FONTS, "SourceSans3-Semibold.otf")
SANS_R = os.path.join(FONTS, "SourceSans3-Regular.otf")

SS = 2.0          # supersampling

BOOKS = {
    "en": dict(
        cover=os.path.join(PUB, "Surviving_the_Future_EN_cover_front.jpg"),
        slug="Surviving_the_Future_EN",
        spine_title="SURVIVING THE FUTURE",
        spine_sub="Crisis, Climate, and Human Resilience",
        author="SETYO WISODO",
    ),
    "id": dict(
        cover=os.path.join(PUB, "Bertahan_Hidup_di_Masa_Depan_ID_cover_front.jpg"),
        slug="Bertahan_Hidup_di_Masa_Depan_ID",
        spine_title="BERTAHAN HIDUP DI MASA DEPAN",
        spine_sub="Krisis, Iklim, dan Resiliensi Manusia",
        author="SETYO WISODO",
    ),
}


# ---------------------------------------------------------------- geometri 3d
def find_coeffs(dst, src):
    """Koefisien PIL PERSPECTIVE: memetakan piksel keluaran (dst) ke sumber (src)."""
    m = []
    for (x, y), (X, Y) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -X * x, -X * y])
        m.append([0, 0, 0, x, y, 1, -Y * x, -Y * y])
    A = np.array(m, dtype=np.float64)
    B = np.array([c for p in src for c in p], dtype=np.float64)
    return np.linalg.lstsq(A, B, rcond=None)[0]


def project(points, yaw, pitch, cam, f, cx, cy):
    """Putar titik 3D (x kanan, y atas, z ke arah kamera) lalu proyeksikan."""
    out = []
    ca, sa = np.cos(yaw), np.sin(yaw)
    cb, sb = np.cos(pitch), np.sin(pitch)
    for x, y, z in points:
        x1 = x * ca + z * sa
        z1 = -x * sa + z * ca
        y2 = y * cb - z1 * sb
        z2 = y * sb + z1 * cb
        k = f / (cam - z2)
        out.append((cx + x1 * k, cy - y2 * k))
    return out


def quad_face(texture, quad, size, shade=None):
    """Tempel tekstur ke satu bidang segi empat pada kanvas seukuran `size`."""
    w, h = texture.size
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    coeffs = find_coeffs(quad, src)
    warped = texture.transform(size, Image.PERSPECTIVE, tuple(coeffs),
                                resample=Image.BICUBIC)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(quad, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    warped.putalpha(mask)
    if shade is not None:
        warped = apply_shade(warped, shade)
    return warped


def expand(quad, px):
    """Lebarkan segi empat dari titik pusatnya, untuk menutup celah antarbidang."""
    cx = sum(p[0] for p in quad) / len(quad)
    cy = sum(p[1] for p in quad) / len(quad)
    out = []
    for x, y in quad:
        dx, dy = x - cx, y - cy
        d = max(1e-6, (dx * dx + dy * dy) ** 0.5)
        out.append((x + dx / d * px, y + dy / d * px))
    return out


def apply_shade(layer, shade):
    """shade(x_frac, y_frac) -> faktor kecerahan 0..1+ pada kanvas."""
    w, h = layer.size
    xs = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :]
    ys = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
    k = shade(xs, ys).astype(np.float32)
    arr = np.asarray(layer, dtype=np.float32)
    arr[..., :3] *= k[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


# ---------------------------------------------------------------- tekstur
def spine_texture(cfg, spine_in, trim_w_in, trim_h_in, px_per_in):
    """Punggung buku: navy, judul serif vertikal, aksen amber, nama penulis."""
    w = max(24, int(round(spine_in * px_per_in)))
    h = int(round(trim_h_in * px_per_in))
    img = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(img)

    # gradien melintang: buku bulat, tepi lebih gelap
    for x in range(w):
        t = x / max(1, w - 1)
        k = 0.72 + 0.42 * (1 - abs(t - 0.42) / 0.62) ** 1.4
        row = tuple(min(255, int(c * k)) for c in NAVY)
        d.line([(x, 0), (x, h)], fill=row)

    # garis aksen: satu di kepala punggung, satu di atas nama penulis
    m = max(3, int(w * 0.33))
    bar = max(2, int(px_per_in * 0.018))
    d.rectangle([m, int(h * 0.052), w - m, int(h * 0.052) + bar], fill=AMBER)
    d.line([(m, int(h * 0.735)), (w - m, int(h * 0.735))],
           fill=(74, 92, 112), width=max(1, bar // 2))

    def vertical(text, font, fill, cy_frac, max_h_frac, tracking=0):
        f = font
        tmp = Image.new("RGBA", (10, 10))
        dd = ImageDraw.Draw(tmp)
        tw = dd.textlength(text, font=f)
        limit = h * max_h_frac
        while tw > limit and f.size > 12:
            f = ImageFont.truetype(f.path, f.size - 1)
            tw = dd.textlength(text, font=f)
        cap = int(f.size * 1.7)
        strip = Image.new("RGBA", (int(tw) + 12, cap), (0, 0, 0, 0))
        sd = ImageDraw.Draw(strip)
        if tracking:
            x = 6
            for ch in text:
                sd.text((x, 0), ch, font=f, fill=fill)
                x += sd.textlength(ch, font=f) + tracking
        else:
            sd.text((6, 0), text, font=f, fill=fill)
        strip = strip.rotate(-90, expand=True)
        img.paste(strip, ((w - strip.width) // 2, int(h * cy_frac) - strip.height // 2), strip)

    vertical(cfg["spine_title"], ImageFont.truetype(SERIF_B, int(w * 0.265)),
             IVORY, 0.335, 0.46)
    vertical(cfg["author"], ImageFont.truetype(SANS, int(w * 0.175)),
             (208, 216, 226), 0.795, 0.17, tracking=2)

    return img


def pages_texture(trim_w_in, spine_in, px_per_in):
    """Blok kertas: krem dengan garis halus tumpukan halaman."""
    w = int(round(trim_w_in * px_per_in))
    h = max(20, int(round(spine_in * px_per_in)))
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    step = max(2, int(h / 90))
    for y in range(0, h, step):
        tone = 226 + (y * 7) % 18
        d.line([(0, y), (w, y)], fill=(tone, tone - 5, tone - 22))
    # sisi dekat punggung sedikit lebih gelap
    for x in range(min(w // 3, 90)):
        k = int(14 * (1 - x / max(1, min(w // 3, 90))))
        d.line([(x, 0), (x, h)], fill=(238 - k, 232 - k, 214 - k))
    return img


# ---------------------------------------------------------------- render
def render(cfg, spine_in, trim_w=8.27, trim_h=11.69,
           yaw_deg=28.0, pitch_deg=13.0, canvas=2000, bg=(255, 255, 255, 255),
           shadow=True):
    """Satu bingkai 3D: muka depan + punggung + blok kertas atas."""
    size = int(canvas * SS)
    cover = Image.open(cfg["cover"]).convert("RGB")
    ppi = cover.width / trim_w
    spine_in = float(spine_in)
    spine_tex = spine_texture(cfg, spine_in, trim_w, trim_h, ppi * 2.2)
    pages_tex = pages_texture(trim_w, spine_in, ppi * 2.2)

    W, H, D = trim_w, trim_h, spine_in
    yaw, pitch = np.radians(yaw_deg), np.radians(pitch_deg)

    # sudut kotak buku (y ke atas, z ke kamera)
    f_tl = (-W / 2, +H / 2, +D / 2)
    f_tr = (+W / 2, +H / 2, +D / 2)
    f_br = (+W / 2, -H / 2, +D / 2)
    f_bl = (-W / 2, -H / 2, +D / 2)
    s_tf = (-W / 2, +H / 2, +D / 2)
    s_tb = (-W / 2, +H / 2, -D / 2)
    s_bb = (-W / 2, -H / 2, -D / 2)
    s_bf = (-W / 2, -H / 2, +D / 2)
    t_fl = (-W / 2, +H / 2, +D / 2)
    t_fr = (+W / 2, +H / 2, +D / 2)
    t_br = (+W / 2, +H / 2, -D / 2)
    t_bl = (-W / 2, +H / 2, -D / 2)

    cam, f = 46.0, 34.0 * (size / 2000.0)
    pts = [f_tl, f_tr, f_br, f_bl, s_tf, s_tb, s_bb, s_bf,
           t_fl, t_fr, t_br, t_bl]
    proj = project(pts, yaw, pitch, cam, f, 0, 0)
    xs = [p[0] for p in proj]
    ys = [p[1] for p in proj]
    bw, bh = max(xs) - min(xs), max(ys) - min(ys)
    margin = 0.115 if shadow else 0.075
    scale = min(size * (1 - margin * 2) / bw, size * (1 - margin * 2) / bh)
    ox = size / 2 - (max(xs) + min(xs)) / 2 * scale
    oy = size / 2 - (max(ys) + min(ys)) / 2 * scale
    proj = [(x * scale + ox, y * scale + oy) for x, y in proj]
    q_front = proj[0:4]
    # punggung: balik urutan supaya tekstur tidak tercetak cermin
    q_spine = [proj[5], proj[4], proj[7], proj[6]]
    q_top = proj[8:12]

    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    if shadow:
        # bayangan kontak + ambient lembut di bawah buku
        sy = max(p[1] for p in q_front) - size * 0.004
        sx = (min(p[0] for p in q_front) + max(p[0] for p in q_front)) / 2
        sw = (max(p[0] for p in q_front) - min(p[0] for p in q_front)) * 0.90
        sh = size * 0.040
        sh_img = Image.new("L", (size, size), 0)
        ImageDraw.Draw(sh_img).ellipse(
            [sx - sw / 2, sy - sh / 2, sx + sw / 2, sy + sh / 2], fill=110)
        sh_img = sh_img.filter(ImageFilter.GaussianBlur(size * 0.015))
        shadow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        shadow_layer.putalpha(sh_img)
        shadow_layer = Image.composite(
            Image.new("RGBA", (size, size), (17, 26, 38, 255)),
            Image.new("RGBA", (size, size), (0, 0, 0, 0)), sh_img)
        layer = Image.alpha_composite(layer, shadow_layer)

    # bidang atas (kertas) — paling belakang
    top = quad_face(pages_tex, expand(q_top, 1.6), (size, size),
                    shade=lambda x, y: 0.97 + 0.05 * y)
    layer = Image.alpha_composite(layer, top)

    # punggung — muka kiri, sedikit lebih gelap dari depan
    spine = quad_face(spine_tex, expand(q_spine, 1.6), (size, size),
                      shade=lambda x, y: 0.80 + 0.22 * np.clip(
                          (x - 0.06) / 0.30, 0, 1))
    layer = Image.alpha_composite(layer, spine)

    # muka depan
    front = quad_face(cover, expand(q_front, 1.2), (size, size),
                      shade=lambda x, y: 0.955 + 0.055 * np.clip(
                          (x - 0.18) / 0.55, 0, 1))
    layer = Image.alpha_composite(layer, front)

    # engsel: garis gelap tipis di pertemuan punggung dan muka depan
    hinge = ImageDraw.Draw(layer)
    hinge.line([q_front[0], q_front[3]], fill=(0, 0, 0, 70),
               width=max(2, int(size * 0.0016)))
    # kilau di sepanjang engsel
    hinge.line([q_front[0], q_front[3]], fill=(255, 255, 255, 26),
               width=max(1, int(size * 0.0007)))

    out = Image.new("RGBA", (size, size), bg)
    out = Image.alpha_composite(out, layer)
    return out.resize((canvas, canvas), Image.LANCZOS)


def save(img, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    img.save(path)
    print("  ->", os.path.relpath(path, HERE), img.size)


def main():
    rep = json.load(open(os.path.join(PUB, "build_report.json")))
    print("render 3d:")
    singles, transparent = {}, {}
    for key, cfg in BOOKS.items():
        spine = rep[key]["spine_in"]
        main_img = render(cfg, spine, canvas=2000)
        singles[key] = main_img
        save(main_img, f"{cfg['slug']}_3d_square.png")
        clear = render(cfg, spine, canvas=2000, bg=(255, 255, 255, 0))
        save(clear, f"{cfg['slug']}_3d_transparent.png")
        transparent[key] = clear
        save(render(cfg, spine, yaw_deg=13, pitch_deg=8, canvas=2000),
             f"{cfg['slug']}_3d_front.png")

    # kedua edisi berdampingan
    size = 2000
    pair = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    books = []
    for key in ("en", "id"):
        im = transparent[key]
        bbox = im.split()[-1].point(lambda v: 255 if v > 8 else 0).getbbox()
        books.append(im.crop(bbox) if bbox else im)

    gap = int(size * 0.03)
    slot_w = (size - gap * 3) // 2
    slot_h = int(size * 0.86)
    # skala bersama: kedua buku seukuran sama dan utuh di dalam bingkai
    total_w = sum(b.width for b in books)
    k = min((size * 0.80) / max(b.height for b in books),
            (size - gap * 3) / total_w)
    for i, im in enumerate(books):
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        x = gap + i * (slot_w + gap) + (slot_w - im.width) // 2
        y = (size - im.height) // 2
        pair.alpha_composite(im, (x, y))
    save(pair, "pair_3d_square.png")


if __name__ == "__main__":
    main()
