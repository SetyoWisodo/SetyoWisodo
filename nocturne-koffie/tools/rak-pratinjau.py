"""
Pratinjau komposisi hero rak — PNG, bukan tangkapan peramban.

Kenapa ada berkas ini
---------------------
`rak/index.html` adalah halaman dengan perspektif 3D, kursor kustom, dan tirai
kertas. Tidak ada peramban di sandbox ini, jadi saya tidak bisa memberi tangkapan
layar sungguhan. Yang bisa saya berikan: **perkiraan komposisi** yang dihitung
dengan rumus yang sama dengan `rak/rak.js` (jarak punggung, posisi judul, letak
tab), digambar dengan Pillow memakai potongan atlas yang sama.

Bedanya dengan peramban, dan ini harus disebut kalau gambar ini ditunjukkan:
  · tidak ada perspektif sungguhan — kotak aktif hanya diputar 2D sekitar 4,5°;
  · tidak ada bayangan jatuh, butir kertas, atau kursor;
  · teks digambar dengan Fraunces/Inter versi TTF, bukan woff2 yang dipakai web.

Pakai:
    python3 tools/rak-pratinjau.py         # tulis laporan/rak-pratinjau.png
"""

from __future__ import annotations

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "laporan", "rak-pratinjau.png")
FONT = os.path.join(ROOT, "assets", "fonts")

PAPER = (245, 239, 228)
SHEET = (250, 246, 238)
INK = (22, 17, 13)
MUTED = (109, 101, 88)
ACCENT = (225, 84, 43)
RULE = (22, 17, 13)

W, Hh = 1600, 1000
H = min(0.46 * Hh, 0.31 * W)          # rumus --H: min(46vh, 31vw)
WS = H * 142 / 840
D = H * 474 / 900
GAP = H * 0.03


def font(nama: str, ukuran: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONT, nama), ukuran)


def spasi(d, xy, teks, f, isi=INK, jarak=0.0, anchor="mm"):
    if not jarak:
        d.text(xy, teks, font=f, fill=isi, anchor=anchor)
        return
    lebar = sum(d.textlength(c, font=f) + jarak for c in teks) - jarak
    x = xy[0] - lebar / 2
    for c in teks:
        d.text((x, xy[1]), c, font=f, fill=isi, anchor="lm")
        x += d.textlength(c, font=f) + jarak


def potong(atlas: Image.Image, kotak, ukuran):
    x, y, w, h = kotak
    return atlas.crop((x, y, x + w, y + h)).resize(ukuran, Image.LANCZOS)


def lukis(id_item: str, aksen_latar=None) -> Image.Image:
    covers = Image.open(os.path.join(ROOT, "assets/img/rak/covers.webp")).convert("RGB")
    spines = Image.open(os.path.join(ROOT, "assets/img/rak/spines.webp")).convert("RGB")
    data = open(os.path.join(ROOT, "rak/data.js"), encoding="utf-8").read()
    obj = json.loads(data[data.index("{"):data.rindex("}") + 1])
    items = obj["ITEMS"]
    crop = obj["CROP"]
    i = next(k for k, it in enumerate(items) if it["id"] == id_item)

    im = Image.new("RGB", (W, Hh), PAPER)
    d = ImageDraw.Draw(im)

    # --- bilah atas (84 px)
    d.rectangle([32, 31, 32 + 96, 31 + 21], outline=RULE, width=1)
    spasi(d, (80, 42), "KEMBALI / BACK", font("inter-600.ttf" if os.path.exists(os.path.join(FONT, "inter-600.ttf")) else "inter-latin-600-normal.ttf", 10), INK, 1.0)
    spasi(d, (W // 2, 34), "NOCTURNE", font("bricolage-grotesque-latin-800-normal.ttf", 22), ACCENT, 0.6)
    spasi(d, (W // 2, 56), "KOFFIE · BANYUWANGI", font("inter-latin-600-normal.ttf", 9), ACCENT, 3.0)
    spasi(d, (W - 32, 42), "RAK SANGRAI · 12 LOT · 2026", font("inter-latin-600-normal.ttf", 10), MUTED, 1.0, anchor="rm")

    # --- tab, tepat di atas rak (top = 50% − H/2 − 86)
    ty = Hh // 2 - H / 2 - 86
    tabs = ["SEMUA · SEMUA LOT", "ARABIKA · 4 LOT", "ROBUSTA · 2 LOT", "EXCELSA · 1 LOT", "RACIKAN · BLEND"]
    aktif = items[i]["tab"]
    peta = {"semua": 0, "arabika": 1, "robusta": 2, "excelsa": 3, "racikan": 4}
    lebar = [d.textlength(t, font=font("inter-latin-600-normal.ttf", 10)) + 22 for t in tabs]
    total = sum(lebar) - 4
    x = W / 2 - total / 2
    for n, (t, lw) in enumerate(zip(tabs, lebar)):
        if n == peta.get(aktif, 0):
            d.rectangle([x, ty, x + lw, ty + 23], fill=ACCENT)
        d.rectangle([x, ty, x + lw, ty + 23], outline=RULE, width=1)
        spasi(d, (x + lw / 2, ty + 11), t, font("inter-latin-600-normal.ttf", 10),
              (255, 255, 255) if n == peta.get(aktif, 0) else INK, 0.8)
        x += lw - 1

    # --- rak: rumus sama dengan rak.js
    def step_r(r):
        return (r + math.sin(math.pi * r) / math.pi) / 2 if abs(r) < 1 else math.copysign(0.5, r)

    def F(r):
        return r * (WS + GAP) + (D - WS + 1.6 * GAP) * step_r(r)

    cy = Hh // 2
    for r in [x / 1 for x in range(-8, 9)]:
        if r == 0:
            continue
        px = W / 2 + F(r)
        if abs(px - W / 2) > W / 2 + D:
            continue
        j = (i + int(r)) % len(items)
        kunci = "spine-" + items[j]["id"]
        c = crop[kunci]
        atlas = spines if c[0] == "spines" else covers
        s = Image.new("RGBA", (int(WS), int(H)), (0, 0, 0, 0))
        s.paste(potong(atlas, c[1:], (int(WS), int(H))).convert("RGBA"), (0, 0))
        o = max(0.0, 1 - abs(r))
        o = o * o * (3 - 2 * o)
        gelap = Image.new("RGBA", s.size, (0, 0, 0, int(min(0.55, o * 0.55 + 0.10) * 255)))
        s.alpha_composite(gelap)
        im.paste(s, (int(px - WS / 2), int(cy - H / 2)), s)

    # --- kotak aktif: sampul, diputar −4,5°, sedikit lebih besar
    c = crop["cover-" + items[i]["id"]]
    besar = int(D * 1.12)
    cv = potong(covers, c[1:], (besar, int(besar * 900 / 474))).convert("RGBA")
    cv = cv.rotate(-4.5, resample=Image.BICUBIC, expand=True)
    x0 = int(W / 2 - cv.width / 2)
    y0 = int(cy - cv.height / 2 - 0.025 * H)
    # bayangan lembut
    bay = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    ImageDraw.Draw(bay).rectangle([8, 10, cv.width - 8, cv.height - 6], fill=(20, 16, 10, 60))
    im.paste(bay, (x0 + 6, y0 + 14), bay.filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(18)))
    im.paste(cv, (x0, y0), cv)

    # --- tombol putar di sudut kiri bawah sampul
    rx, ry = W / 2 - D / 2 - 6 + 4, cy + 0.36 * H
    d.ellipse([rx - 21, ry - 21, rx + 21, ry + 21], fill=(245, 239, 228, 200), outline=ACCENT, width=1)
    d.polygon([(rx - 4, ry - 7), (rx + 7, ry), (rx - 4, ry + 7)], fill=ACCENT)

    # --- caption (top = 50% + H/2 + 30)
    it = items[i]
    cy2 = Hh // 2 + H / 2 + 30
    spasi(d, (W / 2, cy2 + 16), it["name"], font("fraunces-latin-700-normal.ttf", 31), INK, -0.3)
    spasi(d, (W / 2, cy2 + 16 + 26 + 9), it["line"], font("inter-latin-600-normal.ttf", 10), ACCENT, 1.1)
    spasi(d, (W / 2, cy2 + 16 + 52 + 12), it["meta"], font("inter-latin-500-normal.ttf", 11), INK, 0.9)

    # --- panah
    for sisi, arah in ((20, -1), (W - 20 - 44, 1)):
        ay = Hh // 2 + H / 2 + 40
        d.line([sisi + 14, ay + 22, sisi + 30, ay + 22], fill=INK, width=1)
        if arah < 0:
            d.line([sisi + 18, ay + 18, sisi + 14, ay + 22], fill=INK, width=1)
            d.line([sisi + 18, ay + 26, sisi + 14, ay + 22], fill=INK, width=1)
        else:
            d.line([sisi + 26, ay + 18, sisi + 30, ay + 22], fill=INK, width=1)
            d.line([sisi + 26, ay + 26, sisi + 30, ay + 22], fill=INK, width=1)

    # --- kaki
    spasi(d, (32, Hh - 33), "© NOCTURNE KOFFIE · BANYUWANGI", font("inter-latin-600-normal.ttf", 10), INK, 0.8, anchor="lm")
    spasi(d, (W - 32, Hh - 33), "IG / WA", font("inter-latin-600-normal.ttf", 10), INK, 0.8, anchor="rm")

    # --- label jujur
    spasi(d, (W / 2, Hh - 10), "PRATINJAU KOMPOSISI · BUKAN TANGKAPAN PERAMBAN",
          font("inter-latin-600-normal.ttf", 9), MUTED, 1.2)
    return im


def lukis_detail(id_item: str = "raung") -> Image.Image:
    """Perkiraan komposisi lembar detail: teks kiri, poster kanan (potongan sampul)."""
    covers = Image.open(os.path.join(ROOT, "assets/img/rak/covers.webp")).convert("RGB")
    data = open(os.path.join(ROOT, "rak/data.js"), encoding="utf-8").read()
    obj = json.loads(data[data.index("{"):data.rindex("}") + 1])
    items = obj["ITEMS"]
    crop = obj["CROP"]
    it = next(x for x in items if x["id"] == id_item)

    im = Image.new("RGB", (W, Hh), SHEET)
    d = ImageDraw.Draw(im)
    d.rectangle([32, 31, 32 + 96, 31 + 21], outline=RULE, width=1)
    spasi(d, (80, 41), "TUTUP / CLOSE", font("inter-latin-600-normal.ttf", 10), INK, 1.0)
    spasi(d, (W // 2, 34), "NOCTURNE", font("bricolage-grotesque-latin-800-normal.ttf", 22), ACCENT, 0.6)
    spasi(d, (W // 2, 56), "KOFFIE · BANYUWANGI", font("inter-latin-600-normal.ttf", 9), ACCENT, 3.0)

    kiri = 110
    kolom = 520
    atas = 250
    d.text((kiri, atas), it["line"], font=font("inter-latin-600-normal.ttf", 10), fill=ACCENT, anchor="lm")
    d.text((kiri, atas + 66), it["name"], font=font("fraunces-latin-700-normal.ttf", 76), fill=INK, anchor="lm")
    d.text((kiri, atas + 130), it["meta"], font=font("inter-latin-500-normal.ttf", 10), fill=MUTED, anchor="lm")
    # sinopsis dibungkus manual
    kata, baris, isi = it["synopsis"].split(), [], ""
    for k in kata:
        coba = (isi + " " + k).strip()
        if d.textlength(coba, font=font("fraunces-latin-300-normal.ttf", 17)) > kolom - 40:
            baris.append(isi); isi = k
        else:
            isi = coba
    baris.append(isi)
    y = atas + 170
    for b in baris:
        d.text((kiri, y), b, font=font("fraunces-latin-300-normal.ttf", 17), fill=INK)
        y += 26
    d.text((kiri, y + 12), it["harga_teks"] + " · " + it["ukuran_teks"],
           font=font("inter-latin-600-normal.ttf", 11), fill=(74, 44, 26))
    d.text((kiri, y + 40), "Disangrai Ais Coffee Roastery, Banyuwangi. Dikemas dan dikirim dari kota yang sama.",
           font=font("fraunces-latin-300-normal.ttf", 15), fill=MUTED)
    d.rectangle([kiri, y + 70, kiri + 250, y + 114], outline=ACCENT, width=1)
    spasi(d, (kiri + 125, y + 92), "PESAN " + ("PAKET" if it["kind"] == "Paket" else "LOT") + " / WHATSAPP",
          font("inter-latin-600-normal.ttf", 10), ACCENT, 1.0)

    # poster kanan dari potongan sampul
    c = crop["cover-" + it["id"]]
    tujuan_h = 700
    tujuan_w = int(tujuan_h * 474 / 900)
    pos = potong(covers, c[1:], (tujuan_w, tujuan_h))
    px = int(W * 0.63 - tujuan_w / 2 + 130)
    py = int(Hh / 2 - tujuan_h / 2)
    d.rectangle([px + 10, py + 14, px + tujuan_w + 10, py + tujuan_h + 14], fill=(232, 226, 214))
    im.paste(pos, (px, py))
    spasi(d, (W / 2, Hh - 10), "PRATINJAU KOMPOSISI · BUKAN TANGKAPAN PERAMBAN",
          font("inter-latin-600-normal.ttf", 9), MUTED, 1.2)
    return im


if __name__ == "__main__":
    if "--detail" in __import__("sys").argv:
        im = lukis_detail("raung")
        im.save(os.path.join(ROOT, "laporan", "rak-pratinjau-detail.png"), "PNG", optimize=True)
        print(f"laporan/rak-pratinjau-detail.png · {W}×{Hh}")
        raise SystemExit(0)
    im = lukis("raung")
    im.save(OUT, "PNG", optimize=True)
    print(f"laporan/rak-pratinjau.png · {W}×{Hh} · {os.path.getsize(OUT)/1024:.0f} KB")
    print(f"  H={H:.0f} px · punggung {WS:.0f} px · sampul {D:.0f} px · celah {GAP:.1f} px")
