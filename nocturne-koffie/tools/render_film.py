#!/usr/bin/env python3
"""
D4 · Kreatif & Media — perender klip 9 detik (jalur A: frame + ffmpeg).

Kenapa jalur ini, bukan Remotion/HyperFrames?
    Keduanya SUDAH terpasang (npm) dan komposisinya sudah ada, tetapi MERENDER
    butuh Chrome. Chrome di sandbox ini gagal jalan: `libnspr4.so` tidak ada dan
    tidak bisa dipasang (repositori OS di luar jangkauan jaringan). Jadi video
    dibuat dengan jalur yang bisa dibuktikan di sini:

        motion/film-sheet.json  →  540 frame PNG (Pillow)  →  ffmpeg (H.264)

Yang dipakai: angka, teks, warna, dan waktu dari lembar film & kontrak desain.
Yang TIDAK dipakai: Remotion, HyperFrames, GSAP, Lottie — ketiganya ada di
komposisi terpisah dan diperiksa terpisah (`film-studio/`), bukan di klaim.

Pakai:
    python3 tools/render_film.py                 # 540 frame + MP4
    python3 tools/render_film.py --still 90      # satu still (untuk QC visual)
    python3 tools/render_film.py --fps 30        # lebih cepat, 270 frame
    python3 tools/render_film.py --tanpa-encode  # hanya frame PNG
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "motion", "out")
FRAMES = os.path.join(OUT, "frame")

W, H = 1080, 1920
FONT = {
    "display": os.path.join(ROOT, "assets", "fonts", "bricolage-grotesque-latin-800-normal.ttf"),
    "serif": os.path.join(ROOT, "assets", "fonts", "fraunces-latin-300-normal.ttf"),
    "body": os.path.join(ROOT, "assets", "fonts", "inter-latin-400-normal.ttf"),
    "body-600": os.path.join(ROOT, "assets", "fonts", "inter-latin-600-normal.ttf"),
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def muat_kontrak():
    with open(os.path.join(ROOT, "data", "design-system.json"), encoding="utf-8") as f:
        ds = json.load(f)
    c = ds["warna"]["inti"]
    return {
        "paper": hex_rgb(c["--paper"]),
        "paper2": hex_rgb(c["--paper-2"]),
        "ink": hex_rgb(c["--ink"]),
        "orange": hex_rgb(c["--orange"]),
        "espresso": hex_rgb(c["--espresso"]),
    }


def cari_ffmpeg():
    """ffmpeg dari PATH, atau dari paket pypi imageio-ffmpeg (install cepat, tanpa root)."""
    p = shutil.which("ffmpeg")
    if p:
        return p, "PATH"
    try:
        import imageio_ffmpeg  # type: ignore
        return imageio_ffmpeg.get_ffmpeg_exe(), "pypi imageio-ffmpeg"
    except Exception:
        return None, "tidak ada"


def ease_out(p):
    """expo-out tanpa overshoot — keluarga easing yang sama dengan --ease-out di situs."""
    return 1 - (2 ** (-10 * p)) if p < 1 else 1


def bungkus(teks, font, lebar_maks):
    """Bungkus teks per kata memakai metrik font asli, bukan taksiran."""
    baris, kini = [], ""
    for kata in teks.split():
        coba = (kini + " " + kata).strip()
        if font.getlength(coba) <= lebar_maks or not kini:
            kini = coba
        else:
            baris.append(kini)
            kini = kata
    if kini:
        baris.append(kini)
    return baris


def gambar_frame(n, total, fps, adegan, warna, masih=False):
    from PIL import Image, ImageDraw, ImageFont

    t = n / fps
    cue = next((c for c in adegan["cues"] if c["mulai"] <= t < c["selesai"]), adegan["cues"][-1])
    latar = warna["paper"] if cue["cue"] % 2 else warna["paper2"]
    img = Image.new("RGB", (W, H), latar)
    d = ImageDraw.Draw(img)

    # garis halus latar (petunjuk grid, sama seperti komposisi Remotion)
    for y in range(0, H, 96):
        d.line([(0, y), (W, y)], fill=tuple(int(v * 0.94 + 6) for v in latar), width=1)

    # isi cue: waktu relatif terhadap cue
    mulai = cue["mulai"]
    lama = cue["durasi"]
    masuk = min(0.4, lama * 0.2)
    keluar = masuk * 0.65
    p_masuk = min(1.0, max(0.0, (t - mulai) / masuk))
    p_keluar = min(1.0, max(0.0, (t - (cue["selesai"] - keluar)) / keluar))
    alfa = ease_out(p_masuk) * (1 - ease_out(p_keluar)) if p_keluar > 0 else ease_out(p_masuk)
    geser = int(46 * (1 - ease_out(p_masuk)))

    judul = cue["cue"] == 1 or cue["tier"] == 5
    f_judul = ImageFont.truetype(FONT["display" if judul else "serif"], 92 if cue["cue"] == 1 else 84 if cue["tier"] == 5 else 62)
    f_label = ImageFont.truetype(FONT["body-600"], 22)
    f_kecil = ImageFont.truetype(FONT["body"], 20)

    # kanvas teks dengan alfa, lalu ditempel (opacity tanpa mengubah warna dasar)
    kanvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kanvas)

    x = 84
    baris = bungkus(cue["teks"], f_judul, W - 2 * x)
    tinggi_baris = int(f_judul.size * 1.06)
    blok = len(baris) * tinggi_baris + 34 + 40 + 4 + 40 + 22 + 28
    y = (H - blok) // 2 + geser

    kd.text((x, y), f"{cue['perangkat'].upper()} · TIER {cue['tier']}",
            font=f_label, fill=warna["espresso"] + (int(255 * alfa),))
    y += 34 + 20
    for b in baris:
        kd.text((x, y), b, font=f_judul, fill=warna["ink"] + (int(255 * alfa),))
        y += tinggi_baris
    y += 16
    kd.rectangle([x, y, x + 120, y + 4], fill=(warna["orange"] if cue["tier"] == 5 else warna["ink"]) + (int(255 * alfa),))
    y += 40
    kd.text((x, y), f"cue {cue['cue']} · {cue['mulai']}s–{cue['selesai']}s · {cue['sumber']}",
            font=f_kecil, fill=(111, 101, 90) + (int(255 * alfa),))

    img = Image.alpha_composite(img.convert("RGBA"), kanvas).convert("RGB")

    # bilah kemajuan gulir (lapisan yang memang terus bergerak)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 7], fill=tuple(int(v * 0.9 + 12) for v in warna["paper2"]))
    d.rectangle([0, 0, int(W * (n / max(1, total - 1))), 7], fill=warna["orange"])

    # kaki film
    f_kaki = ImageFont.truetype(FONT["body"], 20)
    d.text((84, H - 96), "NOCTURNE KOFFIE", font=f_kaki, fill=(111, 101, 90))
    kanan = f"{adegan['arc']} · {adegan['rasio_hold'] * 100:.0f}% lembah"
    d.text((W - 84 - f_kaki.getlength(kanan), H - 96), kanan, font=f_kaki, fill=(111, 101, 90))

    return img


def tulis_still(n, adegan, warna, fps):
    from PIL import Image  # noqa: F401
    os.makedirs(OUT, exist_ok=True)
    total = adegan["frame_total"]
    img = gambar_frame(n, total, fps, adegan, warna, masih=True)
    jalur = os.path.join(OUT, f"still-{n:03d}.png")
    img.save(jalur, optimize=True)
    print(f"still {n} → motion/out/{os.path.basename(jalur)} ({os.path.getsize(jalur) / 1024:.0f} KB)")
    return jalur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fps", type=int, default=0, help="default: 60 dari lembar film")
    ap.add_argument("--still", type=int, help="tulis satu frame PNG lalu berhenti")
    ap.add_argument("--tanpa-encode", action="store_true")
    ap.add_argument("--adegan", type=int, default=1)
    args = ap.parse_args()

    with open(os.path.join(ROOT, "motion", "film-sheet.json"), encoding="utf-8") as f:
        lembar = json.load(f)
    adegan = next(a for a in lembar["adegan"] if a["adegan"] == args.adegan)
    fps = args.fps or lembar["grid"]["fps"]
    total = int(round(adegan["durasi"] * fps))
    warna = muat_kontrak()

    if args.still is not None:
        tulis_still(args.still, adegan, warna, fps)
        return

    for jalur in FONT.values():
        if not os.path.exists(jalur):
            raise SystemExit(f"font hilang: {jalur} — jalankan scripts/vendor.mjs")
    try:
        import PIL  # noqa: F401
    except ImportError:
        raise SystemExit("Pillow tidak ada: pip install --break-system-packages pillow")

    os.makedirs(FRAMES, exist_ok=True)
    for lama in glob.glob(os.path.join(FRAMES, "*.png")):
        os.remove(lama)

    for n in range(total):
        gambar_frame(n, total, fps, adegan, warna).save(
            os.path.join(FRAMES, f"{n:04d}.png"), compress_level=1)
        if n % 90 == 0:
            print(f"  frame {n}/{total}")

    print(f"{total} frame ditulis · motion/out/frame/")
    if args.tanpa_encode:
        return

    ffmpeg, asal = cari_ffmpeg()
    if not ffmpeg:
        print("ffmpeg tidak ditemukan. Pasang tanpa root:\n"
              "  pip install --break-system-packages imageio-ffmpeg\n"
              "lalu jalankan ulang perintah ini.")
        return

    keluar = os.path.join(OUT, f"klip-{adegan['adegan']:02d}-nocturne-{int(adegan['durasi'])}s.mp4")
    if os.path.exists(keluar):
        os.remove(keluar)
    perintah = [
        ffmpeg, "-y", "-loglevel", "error",
        "-framerate", str(fps), "-i", os.path.join(FRAMES, "%04d.png"),
        "-vf", "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p",
        "-c:v", "libx264", "-crf", "20", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
        "-movflags", "+faststart", keluar,
    ]
    subprocess.run(perintah, check=True)

    versi = subprocess.run([ffmpeg, "-version"], capture_output=True, text=True).stdout.splitlines()[0]
    sha = hashlib.sha256(open(keluar, "rb").read()).hexdigest()[:16]
    manifest = {
        "dibuat": hari_ini().isoformat(),
        "berkas": os.path.relpath(keluar, ROOT),
        "ukuran_kb": round(os.path.getsize(keluar) / 1024, 1),
        "sha256_16": sha,
        "resolusi": [W, H], "fps": fps, "frame": total,
        "durasi_detik": adegan["durasi"],
        "adegan": adegan["adegan"], "judul": adegan["judul"],
        "sumber_angka": "motion/film-sheet.json (turunan motion/timeline.json ← studio/skrip)",
        "warna": "data/design-system.json",
        "font": [os.path.basename(p) for p in FONT.values()],
        "perender": f"tools/render_film.py (Pillow → ffmpeg) · ffmpeg {versi.split()[2]} dari {asal}",
        "bukan_perender": [
            "Remotion — terpasang & bundling lolos, render butuh Chrome (libnspr4 tidak ada)",
            "HyperFrames — terpasang & lint 0 error, render butuh Chrome",
            "GSAP — dipakai di halaman & komposisi HyperFrames, bukan di perender ini",
            "Lottie — JSON 9 detik dibuat & diverifikasi, bukan di perender ini",
        ],
    }
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"video jadi · {manifest['berkas']} · {manifest['ukuran_kb']} KB · sha {sha}")
    print(f"encoder   · {versi}")


if __name__ == "__main__":
    main()
