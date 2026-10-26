# -*- coding: utf-8 -*-
"""Render 3D buku (sampul + tebal punggung) untuk tampilan marketplace.

Geometri memakai ukuran nyata dari build_report.json: potong 8,27 x 11,69 inci,
tebal punggung 1,075 inci (EN) / 1,113 inci (ID). Kotak buku punya enam sisi,
jadi buku bisa diputar sampai sisi belakang tanpa gambar palsu:

  depan   -> sampul depan
  belakang-> panel belakang dari file bungkus cetak (diekstrak ulang tiap jalan)
  punggung-> judul + nama penulis, digambar skrip (bukan dari sampul datar)
  tiga lainnya -> tumpukan kertas

Keluaran di book/publish/3d/:
  *_3d_square.png        latar putih, gambar utama marketplace
  *_3d_transparent.png   latar transparan, untuk banner
  *_3d_front.png         tampak depan, sudut ringan
  *_3d_back.png          tampak belakang (belakang + punggung)
  *_3d_front_back.png    depan dan belakang dalam satu bingkai
  pair_3d_square.png     kedua edisi berdampingan

Jalankan: python make_3d.py
"""
import json
import os
import tempfile

import numpy as np
import pymupdf
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

SS = 2.0                      # supersampling

BOOKS = {
    "en": dict(
        cover=os.path.join(PUB, "Surviving_the_Future_EN_cover_front.jpg"),
        wrap=os.path.join(PUB, "Surviving_the_Future_EN_cover_print.pdf"),
        slug="Surviving_the_Future_EN",
        spine_title="SURVIVING THE FUTURE",
        author="SETYO WISODO",
    ),
    "id": dict(
        cover=os.path.join(PUB, "Bertahan_Hidup_di_Masa_Depan_ID_cover_front.jpg"),
        wrap=os.path.join(PUB, "Bertahan_Hidup_di_Masa_Depan_ID_cover_print.pdf"),
        slug="Bertahan_Hidup_di_Masa_Depan_ID",
        spine_title="BERTAHAN HIDUP DI MASA DEPAN",
        author="SETYO WISODO",
    ),
}


# ------------------------------------------------------------------ panel belakang
def back_panel(cfg, spacer, report):
    """Ambil panel belakang dari PDF bungkus cetak, tanpa kotak barcode kosong."""
    cache = os.path.join(tempfile.gettempdir(), "book3d")
    os.makedirs(cache, exist_ok=True)
    out = os.path.join(cache, os.path.basename(cfg["wrap"]).replace(".pdf", "_back.png"))
    if os.path.exists(out):
        return Image.open(out).convert("RGB")

    bleed = report["bleed_in"]
    trim_w, trim_h = report["trim_in"]
    bar = report["barcode_area_in"]
    dpi = 200                                   # cukup untuk tekstur 3D
    clip = pymupdf.Rect(bleed * 72, bleed * 72,
                        (bleed + trim_w) * 72, (bleed + trim_h) * 72)
    page = pymupdf.open(cfg["wrap"])[0]
    pix = page.get_pixmap(dpi=dpi, clip=clip)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    # tutup kotak barcode putih dengan warna latar sekitarnya
    px = dpi
    x0 = (trim_w - bar["from_right_trim"] - bar["width"]) * px
    y0 = (trim_h - bar["from_bottom_trim"] - bar["height"]) * px
    x1 = x0 + bar["width"] * px
    y1 = y0 + bar["height"] * px
    patch = img.crop((int(x0) - 60, int(y1) + 24, int(x0) + 40, int(y1) + 64))
    bg = tuple(int(v) for v in np.asarray(patch).reshape(-1, 3).mean(0))
    ImageDraw.Draw(img).rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], fill=bg)

    img.save(out)
    return img


# ------------------------------------------------------------------ tekstur
def spine_texture(cfg, spine_in, trim_h_in, px_per_in):
    """Punggung: navy, gradasi melintang, judul vertikal, nama penulis."""
    w = max(24, int(round(spine_in * px_per_in)))
    h = int(round(trim_h_in * px_per_in))
    img = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(img)

    for x in range(w):
        t = x / max(1, w - 1)
        k = 0.72 + 0.42 * (1 - abs(t - 0.42) / 0.62) ** 1.4
        d.line([(x, 0), (x, h)], fill=tuple(min(255, int(c * k)) for c in NAVY))

    m = max(3, int(w * 0.33))
    bar = max(2, int(px_per_in * 0.018))
    d.rectangle([m, int(h * 0.052), w - m, int(h * 0.052) + bar], fill=AMBER)
    d.line([(m, int(h * 0.735)), (w - m, int(h * 0.735))],
           fill=(74, 92, 112), width=max(1, bar // 2))

    def vertical(text, font, fill, cy_frac, max_h_frac, tracking=0):
        f = font
        probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        tw = probe.textlength(text, font=f)
        while tw > h * max_h_frac and f.size > 12:
            f = ImageFont.truetype(f.path, f.size - 1)
            tw = probe.textlength(text, font=f)
        strip = Image.new("RGBA", (int(tw) + 12, int(f.size * 1.7)), (0, 0, 0, 0))
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


def pages_texture(w_in, h_in, px_per_in, vertical=False):
    """Tumpukan kertas; `vertical` untuk sisi depan buku (tepi halaman)."""
    w = max(8, int(round(w_in * px_per_in)))
    h = max(8, int(round(h_in * px_per_in)))
    if vertical:
        w, h = h, w
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    step = max(2, int(h / 90))
    for y in range(0, h, step):
        tone = 226 + (y * 7) % 18
        d.line([(0, y), (w, y)], fill=(tone, tone - 5, tone - 22))
    if vertical:
        img = img.rotate(90, expand=True)
    return img


# ------------------------------------------------------------------ geometri
def find_coeffs(dst, src):
    m = []
    for (x, y), (X, Y) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -X * x, -X * y])
        m.append([0, 0, 0, x, y, 1, -Y * x, -Y * y])
    A = np.array(m, dtype=np.float64)
    B = np.array([c for p in src for c in p], dtype=np.float64)
    return np.linalg.lstsq(A, B, rcond=None)[0]


def project(points, yaw, pitch, cam, f, cx, cy):
    """Putar titik (x kanan, y atas, z ke kamera) lalu proyeksikan."""
    out, depth = [], []
    ca, sa = np.cos(yaw), np.sin(yaw)
    cb, sb = np.cos(pitch), np.sin(pitch)
    for x, y, z in points:
        x1 = x * ca + z * sa
        z1 = -x * sa + z * ca
        y2 = y * cb - z1 * sb
        z2 = y * sb + z1 * cb
        k = f / (cam - z2)
        out.append((cx + x1 * k, cy - y2 * k))
        depth.append(z2)
    return out, depth


def expand(quad, px):
    cx = sum(p[0] for p in quad) / len(quad)
    cy = sum(p[1] for p in quad) / len(quad)
    out = []
    for x, y in quad:
        dx, dy = x - cx, y - cy
        d = max(1e-6, (dx * dx + dy * dy) ** 0.5)
        out.append((x + dx / d * px, y + dy / d * px))
    return out


def quad_face(texture, quad, size, shade=None):
    w, h = texture.size
    coeffs = find_coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    warped = texture.transform(size, Image.PERSPECTIVE, tuple(coeffs),
                               resample=Image.BICUBIC)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(quad, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.9))
    warped.putalpha(mask)
    if shade is not None:
        warped = apply_shade(warped, shade)
    return warped


def apply_shade(layer, shade):
    w, h = layer.size
    xs = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :]
    ys = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
    k = np.asarray(shade(xs, ys), dtype=np.float32)
    arr = np.asarray(layer, dtype=np.float32)
    arr[..., :3] *= k[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


# ------------------------------------------------------------------ render
def render(cfg, report, yaw_deg=28.0, pitch_deg=13.0, canvas=2000,
           bg=(255, 255, 255, 255), shadow=True):
    size = int(canvas * SS)
    cover = Image.open(cfg["cover"]).convert("RGB")
    back = back_panel(cfg, None, report)
    ppi = cover.width / report["trim_in"][0]
    tw, th = report["trim_in"]
    spine_in = float(report["spine_in"])

    spine_tex = spine_texture(cfg, spine_in, th, ppi * 2.0)
    pages_top = pages_texture(tw, spine_in, 220)
    pages_fore = pages_texture(spine_in, th, 220, vertical=True)

    W, H, D = tw, th, spine_in
    hw, hh, hd = W / 2, H / 2, D / 2

    # tiap sisi: [kiri-atas, kanan-atas, kanan-bawah, kiri-bawah]
    faces = {
        "front": ([(-hw, hh, hd), (hw, hh, hd), (hw, -hh, hd), (-hw, -hh, hd)], cover,
                  lambda x, y: 0.955 + 0.055 * np.clip((x - 0.18) / 0.55, 0, 1)),
        "back": ([(hw, hh, -hd), (-hw, hh, -hd), (-hw, -hh, -hd), (hw, -hh, -hd)], back,
                 lambda x, y: 0.925 + 0.045 * np.clip((0.9 - x) / 0.6, 0, 1)),
        "spine": ([(-hw, hh, hd), (-hw, hh, -hd), (-hw, -hh, -hd), (-hw, -hh, hd)], spine_tex,
                  lambda x, y: 0.80 + 0.22 * np.clip((np.abs(x - 0.5) * 2 - 0.2) / 0.6, 0, 1)),
        "fore": ([(hw, hh, -hd), (hw, hh, hd), (hw, -hh, hd), (hw, -hh, -hd)], pages_fore,
                 lambda x, y: 0.82 + 0.14 * np.clip((x - 0.1) / 0.8, 0, 1)),
        "top": ([(-hw, hh, -hd), (hw, hh, -hd), (hw, hh, hd), (-hw, hh, hd)], pages_top,
                lambda x, y: 0.99 + 0.02 * y),
        "bottom": ([(-hw, -hh, hd), (hw, -hh, hd), (hw, -hh, -hd), (-hw, -hh, -hd)], pages_fore,
                   lambda x, y: 0.70 + 0.10 * x),
    }

    normals = {
        "front": (0, 0, 1), "back": (0, 0, -1),
        "spine": (-1, 0, 0), "fore": (1, 0, 0),
        "top": (0, 1, 0), "bottom": (0, -1, 0),
    }

    def facing(key, yaw, pitch):
        """Benar bila sisi menghadap kamera setelah diputar."""
        nx, ny, nz = normals[key]
        ca, sa = np.cos(yaw), np.sin(yaw)
        cb, sb = np.cos(pitch), np.sin(pitch)
        x1 = nx * ca + nz * sa
        z1 = -nx * sa + nz * ca
        z2 = ny * sb + z1 * cb
        return z2 > 0.02

    visible = {k: v for k, v in faces.items()
               if facing(k, np.radians(yaw_deg), np.radians(pitch_deg))}

    all_pts = [p for f in visible.values() for p in f[0]]
    proj_flat, depth_flat = project(all_pts, np.radians(yaw_deg), np.radians(pitch_deg),
                                    46.0, 34.0 * (size / 2000.0), 0, 0)
    xs, ys = [p[0] for p in proj_flat], [p[1] for p in proj_flat]
    bw, bh = max(xs) - min(xs), max(ys) - min(ys)
    margin = 0.115 if shadow else 0.075
    scale = min(size * (1 - margin * 2) / bw, size * (1 - margin * 2) / bh)
    ox = size / 2 - (max(xs) + min(xs)) / 2 * scale
    oy = size / 2 - (max(ys) + min(ys)) / 2 * scale
    proj_flat = [(x * scale + ox, y * scale + oy) for x, y in proj_flat]

    ordered = []
    for i, (key, (quad, tex, shade)) in enumerate(visible.items()):
        pts = proj_flat[i * 4:(i + 1) * 4]
        ordered.append((float(np.mean(depth_flat[i * 4:(i + 1) * 4])), key, pts, tex, shade))
    ordered.sort(key=lambda t: t[0])            # jauh dulu, dekat belakangan

    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    if shadow:
        # bayangan di bawah seluruh buku, dihitung dari semua sisi yang terlihat
        bottom = max(p[1] for f in visible.values() for p in f[0])
        left = min(x for _d, _k, pts, _t, _s in ordered for x, _y in pts)
        right = max(x for _d, _k, pts, _t, _s in ordered for x, _y in pts)
        sy = bottom * scale + oy - size * 0.004 if bottom < 1e6 else size * 0.8
        sx = (left + right) / 2
        sw = (right - left) * 0.90
        sh = size * 0.040
        sh_img = Image.new("L", (size, size), 0)
        ImageDraw.Draw(sh_img).ellipse([sx - sw / 2, sy - sh / 2, sx + sw / 2, sy + sh / 2],
                                       fill=105)
        sh_img = sh_img.filter(ImageFilter.GaussianBlur(size * 0.015))
        layer = Image.alpha_composite(
            layer, Image.composite(Image.new("RGBA", (size, size), (17, 26, 38, 255)),
                                   Image.new("RGBA", (size, size), (0, 0, 0, 0)), sh_img))

    for _d, key, pts, tex, shade in ordered:
        layer = Image.alpha_composite(
            layer, quad_face(tex, expand(pts, 1.4), (size, size), shade=shade))

    # engsel tipis di pertemuan punggung dan sampul depan
    if "front" in visible and "spine" in visible:
        front_pts = [p for _d, k, p, _t, _s in ordered if k == "front"][0]
        dd = ImageDraw.Draw(layer)
        dd.line([front_pts[0], front_pts[3]], fill=(0, 0, 0, 70),
                width=max(2, int(size * 0.0016)))

    out = Image.new("RGBA", (size, size), bg)
    out = Image.alpha_composite(out, layer)
    return out.resize((canvas, canvas), Image.LANCZOS)


# ------------------------------------------------------------------ keluaran
def save(img, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    img.save(path)
    print("  ->", os.path.relpath(path, HERE), img.size)


def content_bbox(img):
    a = img.split()[-1].point(lambda v: 255 if v > 8 else 0)
    return a.getbbox() or (0, 0, img.width, img.height)


def compose(builds, canvas=2000, gap_frac=0.045, fill=0.94):
    """Susun beberapa render berdampingan dalam satu bingkai persegi.

    Masukan harus render transparan tanpa bayangan: crop memakai alfa, jadi
    bayangan akan ikut terpotong menjadi bercak kelabu di bawah buku.
    """
    imgs = []
    for im in builds:
        im = im.convert("RGBA")
        imgs.append(im.crop(content_bbox(im)))
    gap = int(canvas * gap_frac)
    board = Image.new("RGBA", (canvas, canvas), (255, 255, 255, 255))
    total_w = sum(i.width for i in imgs)
    k = min((canvas * fill) / max(i.height for i in imgs),
            (canvas - gap * (len(imgs) + 1)) / total_w)
    x = gap
    for im in imgs:
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        board.alpha_composite(im, (x, (canvas - im.height) // 2))
        x += im.width + gap
    return board


def main():
    rep = json.load(open(os.path.join(PUB, "build_report.json")))
    print("render 3d:")
    front_view, back_view, clear = {}, {}, {}

    for key, cfg in BOOKS.items():
        r = rep[key]
        slug = cfg["slug"]
        main_img = render(cfg, r, canvas=2000)
        save(main_img, f"{slug}_3d_square.png")

        c = render(cfg, r, canvas=2000, bg=(255, 255, 255, 0))
        save(c, f"{slug}_3d_transparent.png")
        clear[key] = c

        f = render(cfg, r, yaw_deg=13, pitch_deg=8, canvas=2000)
        save(f, f"{slug}_3d_front.png")
        front_view[key] = render(cfg, r, yaw_deg=13, pitch_deg=8, canvas=2000,
                                 bg=(255, 255, 255, 0), shadow=False)

        b = render(cfg, r, yaw_deg=208, pitch_deg=8, canvas=2000)
        save(b, f"{slug}_3d_back.png")
        back_clear = render(cfg, r, yaw_deg=208, pitch_deg=8, canvas=2000,
                            bg=(255, 255, 255, 0), shadow=False)

        save(compose([front_view[key], back_clear]), f"{slug}_3d_front_back.png")

    save(compose([front_view["en"], front_view["id"]], fill=0.80), "pair_3d_square.png")


if __name__ == "__main__":
    main()
