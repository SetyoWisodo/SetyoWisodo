#!/usr/bin/env python3
"""Pratinjau tata letak hero — gambar skema, BUKAN tangkapan layar peramban.

Alasannya jujur: Chromium tidak bisa dipasang di sandbox ini (libnspr4 hilang),
jadi tidak ada render peramban sungguhan. Skrip ini menyusun ulang kotak-kotak
hero memakai angka yang benar-benar dibaca dari `assets/css/biji.css`
(clamp ukuran huruf, fraksi kolom, jarak kolom) dan font asli proyek, supaya
posisi kiri/kanan serta lebar baris motto bisa diperiksa dengan mata.

Keluaran: laporan/pratinjau-hero.png (1280 px dan 390 px, ditumpuk).

    python3 tools/pratinjau.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "css" / "biji.css"
CATALOG = ROOT / "data" / "catalog.json"
DESIGN = ROOT / "data" / "design-system.json"
POSTER = ROOT / "assets" / "img" / "biji-3d-poster.webp"
FONT_DIR = ROOT / "assets" / "fonts"

F_JUDUL = FONT_DIR / "bricolage-grotesque-latin-800-normal.ttf"
F_ITALIC = FONT_DIR / "fraunces-latin-300-normal.ttf"
F_TEKS = FONT_DIR / "inter-latin-400-normal.ttf"
F_LABEL = FONT_DIR / "inter-latin-600-normal.ttf"


def warna() -> dict:
    d = json.loads(DESIGN.read_text(encoding="utf-8"))["warna"]
    gabung = {}
    for kelompok in ("inti", "turunan"):
        for k, v in d.get(kelompok, {}).items():
            gabung[k] = v
    return gabung


def aturan(css: str, selektor: str) -> str:
    m = re.search(re.escape(selektor) + r"\s*\{([^}]*)\}", css)
    return m.group(1) if m else ""


def clamp(txt: str) -> tuple[float, float, float] | None:
    m = re.search(r"font-size:\s*clamp\(([\d.]+)rem,\s*([\d.]+)vw,\s*([\d.]+)rem\)", txt)
    return tuple(float(x) for x in m.groups()) if m else None


def ukuran(c: tuple[float, float, float], vw: int) -> float:
    return max(c[0] * 16, min(vw * c[1] / 100, c[2] * 16))


def tata(css: str, vw: int) -> dict:
    dasar = css.split("@media (min-width: 900px)")[0]
    besar = css.split("@media (min-width: 900px)")[1].split("@media (max-width: 899px)")[0]
    kecil = css.split("@media (max-width: 899px)")[1]

    m_grid = re.search(
        r"grid-template-columns:\s*minmax\(0,\s*([\d.]+)fr\)\s*minmax\(0,\s*([\d.]+)fr\)", besar
    )
    m_gap = re.search(r"column-gap:\s*clamp\(([\d.]+)px,\s*([\d.]+)vw,\s*([\d.]+)px\)", besar)
    m_maks = re.search(r"width:\s*min\(100%,\s*(\d+)px\)", besar)

    fr1, fr2 = (float(m_grid.group(1)), float(m_grid.group(2))) if m_grid else (0.86, 1.14)
    gap = 0.0
    if m_gap:
        g0, g1, g2 = (float(x) for x in m_gap.groups())
        gap = max(g0, min(vw * g1 / 100, g2))
    maks_biji = int(m_maks.group(1)) if m_maks else 440

    pad = min(44, max(16, vw * 0.04))
    lebar = min(1180, vw) - pad * 2
    dua_kolom = vw >= 900
    if dua_kolom:
        kolom_1 = (lebar - gap) * fr1 / (fr1 + fr2)
        kolom_2 = (lebar - gap) * fr2 / (fr1 + fr2)
        biji_w = min(kolom_1, maks_biji)
    else:
        kolom_1 = kolom_2 = lebar
        biji_w = min(lebar, maks_biji)

    c_judul = clamp(aturan(dasar, ".hero__title")) or (1.7, 3.2, 3.1)
    if not dua_kolom:
        c_judul = clamp(aturan(kecil, ".hero__title")) or c_judul

    return {
        "vw": vw,
        "pad": pad,
        "lebar": lebar,
        "dua_kolom": dua_kolom,
        "gap": gap,
        "kolom_1": kolom_1,
        "kolom_2": kolom_2,
        "biji_w": biji_w,
        "judul_px": ukuran(c_judul, vw),
    }


def bungkus(d, teks: str, font, lebar: float) -> list[str]:
    baris, kini = [], ""
    for k in teks.split():
        uji = (kini + " " + k).strip()
        if kini and d.textlength(uji, font=font) > lebar:
            baris.append(kini)
            kini = k
        else:
            kini = uji
    if kini:
        baris.append(kini)
    return baris


def buat(vw: int, css: str, isi: dict, pal: dict) -> Image.Image:
    t = tata(css, vw)

    def huruf(path: Path, px: float) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(str(path), int(px))

    ukuran_judul = t["judul_px"]
    f1 = huruf(F_JUDUL, ukuran_judul)
    f2 = huruf(F_ITALIC, ukuran_judul)
    f_label = huruf(F_LABEL, 11)
    f_dukung = huruf(F_ITALIC, 17)
    f_intro = huruf(F_TEKS, 15)
    f_mikro = huruf(F_TEKS, 12)

    ukur = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    baris_judul = [(motto[0], f1), (motto[1], f2)]
    tinggi_judul = sum(f.size * 1.02 for _, f in baris_judul)
    baris_intro = bungkus(ukur, isi["intro"], f_intro, t["kolom_2"])
    tinggi_teks = (16 + 10) + tinggi_judul + 14 + 22 + 20 \
        + len(baris_intro) * 19 + 26 + 16

    biji_h = int(t["biji_w"] * 1.25)
    if t["dua_kolom"]:
        tinggi = int(max(biji_h, tinggi_teks) + t["pad"] * 2)
    else:
        tinggi = int(tinggi_teks + 40 + biji_h + t["pad"] * 2)

    img = Image.new("RGB", (vw, tinggi), pal["--paper"])
    d = ImageDraw.Draw(img)

    if t["dua_kolom"]:
        x_biji = t["pad"]
        y_biji = (tinggi - biji_h) // 2
        x_teks = t["pad"] + t["kolom_1"] + t["gap"]
        y = (tinggi - tinggi_teks) // 2
    else:
        x_biji = t["pad"]
        x_teks = t["pad"]
        y = t["pad"] + 8

    # label mikro
    d.ellipse((x_teks, y + 4, x_teks + 6, y + 10), fill=pal["--orange"])
    d.text((x_teks + 14, y - 2), isi["label"], font=f_label, fill=pal["--ink-55"])
    y += 16 + 10

    for teks, f in baris_judul:
        w = d.textlength(teks, font=f)
        melebihi = w > t["kolom_2"] * 0.96
        isi_warna = pal["--orange"] if melebihi else (pal["--ink"] if f is f1 else pal["--espresso"])
        d.text((x_teks, y), teks, font=f, fill=isi_warna)
        if melebihi:
            d.line((x_teks, y + f.size * 0.9, x_teks + t["kolom_2"], y + f.size * 0.9),
                   fill=pal["--orange"], width=2)
        y += int(f.size * 1.02)

    y += 14
    d.text((x_teks, y), isi["dukung"], font=f_dukung, fill=pal["--ink-55"])
    y += 22 + 20
    d.multiline_text((x_teks, y), "\n".join(baris_intro), font=f_intro,
                     fill=pal["--ink"], spacing=4)
    y += len(baris_intro) * 19 + 26
    d.text((x_teks, y), isi["mikro"], font=f_mikro, fill=pal["--ink-55"])

    if POSTER.exists():
        poster = Image.open(POSTER).convert("RGBA")
        poster = poster.resize((int(t["biji_w"]), biji_h), Image.LANCZOS)
        if t["dua_kolom"]:
            img.paste(poster, (int(x_biji), int(y_biji)), poster)
        else:
            img.paste(poster, (int(x_biji), int(y + 40)), poster)

    d.text((t["pad"], tinggi - 20), f"skema tata letak {vw}px · bukan tangkapan layar peramban",
           font=huruf(F_TEKS, 11), fill=pal["--ink-55"])
    return img


def main() -> int:
    css = CSS.read_text(encoding="utf-8")
    isi_katalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    global motto
    motto = isi_katalog["brand"]["motto"]
    isi = {
        "label": "SINGLE ORIGIN · JAWA TIMUR",
        "dukung": isi_katalog["brand"]["headline"][0] + " " + isi_katalog["brand"]["headline"][1],
        "intro": isi_katalog["brand"]["intro"],
        "mikro": "Sentuh titik untuk membaca senyawa di tiap bagian biji.",
    }
    pal = warna()
    pal.setdefault("--ink-55", "rgba(22,17,13,.55)")
    if pal["--ink-55"].startswith("rgba"):
        pal["--ink-55"] = "#8A8378"

    lebar = buat(1280, css, isi, pal)
    ponsel = buat(390, css, isi, pal)
    kanvas = Image.new("RGB", (1280, lebar.height + ponsel.height + 24), pal["--paper"])
    kanvas.paste(lebar, (0, 0))
    kanvas.paste(ponsel, (0, lebar.height + 24))

    keluar = ROOT / "laporan" / "pratinjau-hero.png"
    keluar.parent.mkdir(exist_ok=True)
    kanvas.save(keluar, optimize=True)

    for vw in (1280, 390):
        t = tata(css, vw)
        f2 = ImageFont.truetype(str(F_ITALIC), int(t["judul_px"]))
        w = f2.getlength(motto[1])
        print(f"{vw}px · kolom teks {t['kolom_2']:.0f}px · baris terpanjang {w:.0f}px "
              f"· {'muat' if w <= t['kolom_2'] * 0.96 else 'MELUAP'}")
    print(f"→ {keluar.relative_to(ROOT)} · {keluar.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
