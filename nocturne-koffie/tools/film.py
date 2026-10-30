#!/usr/bin/env python3
"""
D4 · Kreatif & Media — lembar film 9 detik (frame-accurate), dari 20 repo motion.

Membaca `motion/timeline.json` (hasil tools/motion.py) lalu menurunkannya menjadi
lembar kerja film yang bisa dieksekusi mesin lain:

    motion/film-sheet.md     tabel cue → frame → ketukan → tier energi → kamera → SFX
    motion/film-sheet.json   ringkasan mesin (dipakai tools/periksa.py)

Yang diadopsi dari 20 repo pada post @Mikadzyki_NFT (28 Okt 2026), semuanya
sebagai ATURAN — tidak ada library yang dipasang di sini:

  · howseen-ai/claude-motion-design — satu `seek(t)` deterministik, 2 rAF setelah
    seek sebelum menangkap frame, sinkron ke ketukan, larangan mengarang angka.
  · t3knobox/klik-anim-skill-creation — hukum A1 (durasi = bobot), A6/A18 (arc
    energi), A16 (ADSR), B1 (matematika beat-sync).
  · LottieFiles/motion-design-skill — tabel durasi, 1/3 rule, anggaran stagger.
  · remotion-dev/remotion + skills, heygen-com/hyperframes, cth9191/animate —
    struktur komposisi & render; mesinnya tidak dipasang di sandbox ini.
  · greensock/GSAP, motiondivision/motion, 199-biotechnologies/motion-dev-animations-skill,
    airbnb/lottie-web — semantik gerak & batas format (tidak dipasang).

Pakai:
    python3 tools/film.py            # tulis motion/film-sheet.md + .json
    python3 tools/film.py --cek      # cetak ringkasan, tanpa menulis
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "motion")

# ── grid ────────────────────────────────────────────────────────────────────
# 120 BPM adalah satu-satunya tempo di mana batas cue studio (3/5/7 detik)
# jatuh TEPAT di ketukan: 3 s = ketukan 6, 5 s = 10, 7 s = 14.
BPM = 120
FPS = 60
DURASI = 9.0
FRAME_PER_BEAT = (60.0 / BPM) * FPS      # 30 frame
FRAME_PER_BAR = FRAME_PER_BEAT * 4       # 120 frame
FRAME_TOTAL = int(round(DURASI * FPS))   # 540

# ── arc energi (hukum A18) ──────────────────────────────────────────────────
# Satu adegan punya SATU bentuk: cold-open — puncak di hook, lembah di isi,
# bangun lagi, ditutup payoff. Tier 1 = diam, 5 = puncak.
ARC = {
    "nama": "cold-open",
    "alasan": "9 detik terlalu pendek untuk ramp; hook harus memukul di 0-3 s, "
              "lalu beri satu lembah supaya payoff terasa naik.",
    "tier": [4, 2, 3, 5],
    "perangkat": ["judul masuk", "daftar 1-2", "daftar 3 + angka", "payoff + CTA"],
    "kamera": ["dorong 4%", "diam (lembah)", "geser 2%", "tarik 3%"],
    "sfx": ["whoosh masuk (puncak terukur)", "tick", "tick", "impact + logo"],
}

# Tabel durasi (klik A1, dibulatkan ke frame pada 60 fps).
BAND = [
    ("micro-feedback", 0.12, 0.24),
    ("elemen kecil masuk/keluar", 0.32, 0.48),
    ("panel/kartu", 0.56, 0.88),
    ("gerak adegan", 0.80, 1.20),
    ("frasa kamera", 1.60, 3.60),
]


def baca(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return json.load(f)


def band(nama_durasi):
    for nama, lo, hi in BAND:
        if lo - 0.01 <= nama_durasi <= hi + 0.01:
            return nama
    return "di luar band"


def pada_grid(detik):
    """Selisih ke ketukan terdekat, dalam frame."""
    beat = detik * BPM / 60.0
    return abs(beat - round(beat)) * FRAME_PER_BEAT


def bangun(tl):
    adegan = []
    masalah = []
    for a in tl["adegan"]:
        cue_out = []
        tier_arc = ARC["tier"]
        for i, c in enumerate(a["cues"]):
            f0 = int(round(c["mulai"] * FPS))
            f1 = int(round(c["selesai"] * FPS))
            beat = c["mulai"] * BPM / 60.0
            tier = tier_arc[i] if i < len(tier_arc) else tier_arc[-1]
            item = {
                "cue": i + 1,
                "mulai": round(c["mulai"], 2),
                "selesai": round(c["selesai"], 2),
                "durasi": round(c["durasi"], 2),
                "frame": [f0, f1],
                "frame_total": f1 - f0,
                "ketukan": round(beat, 2),
                "di_grid": pada_grid(c["mulai"]) <= 1.0,
                "di_birama": abs((beat / 4) - round(beat / 4)) < 0.02,
                "tier": tier,
                "band": band(c["durasi"]),
                "perangkat": ARC["perangkat"][i] if i < len(ARC["perangkat"]) else "—",
                "kamera": ARC["kamera"][i] if i < len(ARC["kamera"]) else "—",
                "sfx": ARC["sfx"][i] if i < len(ARC["sfx"]) else "—",
                "teks": c["teks"],
                "sumber": c.get("sumber", ""),
                "ada_angka": bool(re.search(r"\d", c["teks"])),
            }
            if not item["sumber"]:
                # cue CTA tidak mengklaim angka, jadi tidak butuh sumber;
                # cue yang memuat angka wajib menyebut sumbernya.
                item["sumber"] = "—" if item["ada_angka"] else "tanpa angka"
            if not item["di_grid"]:
                masalah.append(f"adegan {a['adegan']} cue {i+1} tidak di ketukan")
            if c["durasi"] > BAND[-1][2] + 0.01:
                masalah.append(f"adegan {a['adegan']} cue {i+1} {c['durasi']}s "
                               f"melebihi frasa kamera 3,6 s")
            if not c.get("sumber") and re.search(r"\d", c["teks"]):
                masalah.append(f"adegan {a['adegan']} cue {i+1}: ada angka tanpa sumber")
            cue_out.append(item)

        total = round(sum(c["durasi"] for c in a["cues"]), 2)
        if abs(total - DURASI) > 0.01:
            masalah.append(f"adegan {a['adegan']}: total {total}s, seharusnya 9s")
        tiers = [c["tier"] for c in cue_out]
        if max(tiers) - min(tiers) < 2:
            masalah.append(f"adegan {a['adegan']}: arc energi rata (tidak ada lembah)")

        # hold/rest: cue ber-tier rendah dianggap lembah; target 20-40% durasi
        hold = sum(c["durasi"] for c in cue_out if c["tier"] <= 2)
        rasio_hold = hold / total if total else 0
        if not (0.15 <= rasio_hold <= 0.45):
            masalah.append(f"adegan {a['adegan']}: porsi lembah {rasio_hold:.0%}, di luar 15-45%")

        adegan.append({
            "adegan": a["adegan"],
            "judul": a["judul"],
            "berkas": a["berkas"],
            "aset": a.get("aset", ""),
            "durasi": total,
            "frame_total": int(round(total * FPS)),
            "arc": ARC["nama"],
            "rasio_hold": round(rasio_hold, 2),
            "cues": cue_out,
        })

    return {
        "dibuat": hari_ini().isoformat(),
        "grid": {
            "bpm": BPM, "fps": FPS, "frame_per_beat": FRAME_PER_BEAT,
            "frame_per_bar": FRAME_PER_BAR, "frame_total": FRAME_TOTAL,
            "durasi": DURASI,
            "catatan": "120 BPM dipilih karena batas cue studio (3/5/7 s) jatuh di "
                       "ketukan 6/10/14. Pada 100 atau 133 BPM batas itu meleset.",
        },
        "arc": {"nama": ARC["nama"], "tier": ARC["tier"], "alasan": ARC["alasan"]},
        "adegan": adegan,
        "masalah": masalah,
    }


TEMPLATE = """# Lembar film — {n} adegan, {d} detik, {fps} fps

Dibuat `tools/film.py` pada {tgl} dari `motion/timeline.json` (yang lahir dari 5 skrip
`tools/studio.py`). Lembar ini **tidak merender video**: ia menghitung frame, ketukan,
dan urutan kerja supaya render di mesin lain bisa deterministik.

| Parameter | Nilai |
| --- | --- |
| Tempo | **{bpm} BPM** · 4/4 · satu ketukan = **{fpb:.0f} frame** · satu birama = **{fpbar:.0f} frame** |
| Durasi | **{d_id} detik = {total} frame** per adegan |
| Arc energi | **{arc}** — tier per cue {tier} (1 = diam, 5 = puncak) |
| Sumber | `motion/timeline.json` · `studio/skrip/` · `data/` |

> Kenapa 120 BPM: batas cue studio (3 / 5 / 7 detik) jatuh **tepat** di ketukan 6 / 10 / 14.
> Di 100 BPM atau 133 BPM batas itu meleset 2–6 frame, dan gerak berhenti terasa "nyaris" pas.

## 1 · Grid per adegan

| Adegan | Judul | Cue | Waktu | Frame | Ketukan | Tier | Perangkat | Kamera | SFX |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{tabel}

## 2 · Yang diperiksa mesin sebelum render

| Pemeriksaan | Aturan | Hasil |
| --- | --- | --- |
| Batas cue di ketukan | ≤ 1 frame dari grid {bpm} BPM | {grid_status} |
| Total durasi | {d:g} detik ({total} frame) | {durasi_status} |
| Arc energi | ada puncak (5) dan lembah (≤ 2) | {arc_status} |
| Porsi lembah | 15–45% durasi adegan | {hold_status} |
| Durasi cue | ≤ frasa kamera 3,6 s | {band_status} |
| Sumber angka | tiap cue menyebut sumber data | {sumber_status} |
| Tekstur | tidak ada cue > 1 s tanpa perubahan (A6) | manual: lihat 4 still di bawah |

Masalah terbuka: **{masalah}**

## 3 · Cara menangkap frame (di mesin yang punya browser)

```bash
# 1 · sajikan folder
python3 -m http.server 8080 --bind 0.0.0.0

# 2 · tangkap tiap frame (Playwright, Chromium) — 540 frame per adegan
#    di wajib: await document.fonts.ready, lalu 2x requestAnimationFrame
#    setelah seek(t) sebelum screenshot
#    window.seek(t) sudah ada di motion/frame-0N.html

# 3 · encode: 60 fps, bt709, yuv420p, faststart
ffmpeg -framerate 60 -i frame-%04d.png \\
  -vf "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p" \\
  -c:v libx264 -crf 16 -pix_fmt yuv420p -color_range tv -colorspace bt709 \\
  -movflags +faststart out.mp4
```

Tanpa ffmpeg/Playwright (kondisi sandbox ini): **rekam layar** 1080×1920 selama 9 detik
dengan `?t=0` sebagai awal, atau serahkan lembar ini ke mesin yang punya keduanya.
Jangan menulis "sudah dirender" bila belum ada berkas `.mp4`.

## 4 · Empat still sebelum render penuh

Urutan kerja dari `claude-motion-design` §1: beat map → **4 still** (satu per cue) →
perbaiki → baru render penuh. Tangkap `?t=0.5`, `?t=3.2`, `?t=5.2`, `?t=7.2`
untuk tiap adegan; nilai keterbacaan, kontras, dan apakah teks masuk akal di 9:16.

## 5 · Peta suara

| Cue | SFX | Aturan |
| --- | --- | --- |
{sfx_tabel}

Sumber nada: Mixkit (bebas komersial). SFX diletakkan **pada puncak terukur**
(`argmax|s|`), bukan ditebak; gain 0,04–0,30; fade ekor; loudnorm dua-pass ke −14 LUFS.
Di sandbox ini tidak ada berkas audio, jadi peta ini adalah rencana, bukan hasil.

## 6 · Larangan yang diwarisi 20 repo

1. **Tanpa angka karangan.** Tiap cue menyebut sumbernya; kalau tidak ada di `data/`, angka dicabut.
2. **Satu hal bergerak pada satu waktu** (kecuali slider/skala kontinu). Kalau dua bergerak, salah satu dipindah ke cue lain.
3. **Tanpa easing linear** untuk gerak ruang; tanpa pantulan kartun. Spring dengan damping ≥ 0,72.
4. **Masuk ≠ keluar**: durasi keluar 60–70% durasi masuk.
5. **Stagger ≤ 500 ms** total; 1/3 rule: tidak lebih dari 1/3 elemen bergerak bersamaan.
6. **Loop harus cocok posisi DAN kecepatan** — bukan hanya frame terakhir = frame 0.
7. **Nama gerak harus bermakna**: kamera tidak goyang tanpa alasan cerita.
"""


def md(d, tgl):
    tabel = []
    sfx = []
    for a in d["adegan"]:
        for c in a["cues"]:
            tabel.append(
                f"| {a['adegan']:02d} | {a['judul'][:46]}{'…' if len(a['judul'])>46 else ''} | {c['cue']} | "
                f"{c['mulai']:g}–{c['selesai']:g} s | {c['frame'][0]}–{c['frame'][1]} | "
                f"{c['ketukan']:g} | {c['tier']} | {c['perangkat']} | {c['kamera']} | {c['sfx']} |")
        for c in a["cues"]:
            sfx.append(f"| {a['adegan']:02d}·{c['cue']} | {c['sfx']} | "
                       f"tier {c['tier']} · {c['frame'][0]}–{c['frame'][1]} frame |")

    semua = [c for a in d["adegan"] for c in a["cues"]]
    grid_ok = all(c["di_grid"] for c in semua)
    durasi_ok = all(a["frame_total"] == FRAME_TOTAL for a in d["adegan"])
    arc_ok = all(max(c["tier"] for c in a["cues"]) == 5 and
                 min(c["tier"] for c in a["cues"]) <= 2 for a in d["adegan"])
    hold_ok = all(0.15 <= a["rasio_hold"] <= 0.45 for a in d["adegan"])
    band_ok = all(c["durasi"] <= BAND[-1][2] + 0.01 for c in semua)
    sumber_ok = all(c["sumber"] != "—" for c in semua)   # "—" = angka tanpa sumber
    t = lambda ok: "lolos" if ok else "gagal"

    return TEMPLATE.format(
        n=len(d["adegan"]), d=DURASI, d_id=f"{DURASI:g}".replace(".", ","),
        fps=FPS, tgl=tgl.isoformat(),
        bpm=BPM, fpb=FRAME_PER_BEAT, fpbar=FRAME_PER_BAR, total=FRAME_TOTAL,
        arc=d["arc"]["nama"], tier=" / ".join(str(x) for x in d["arc"]["tier"]),
        tabel="\n".join(tabel),
        grid_status=t(grid_ok), durasi_status=t(durasi_ok), arc_status=t(arc_ok),
        hold_status=t(hold_ok), band_status=t(band_ok), sumber_status=t(sumber_ok),
        masalah="; ".join(d["masalah"]) if d["masalah"] else "tidak ada",
        sfx_tabel="\n".join(sfx),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true")
    args = ap.parse_args()

    tl = baca("motion/timeline.json")
    d = bangun(tl)
    tgl = hari_ini()

    cue = sum(len(a["cues"]) for a in d["adegan"])
    if args.cek:
        print(f"Lembar film siap: {len(d['adegan'])} adegan · {cue} cue · "
              f"{BPM} BPM · {FRAME_TOTAL} frame · {len(d['masalah'])} masalah")
        for m in d["masalah"]:
            print("  !", m)
        return

    with open(os.path.join(OUT, "film-sheet.md"), "w", encoding="utf-8") as f:
        f.write(md(d, tgl))
    with open(os.path.join(OUT, "film-sheet.json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

    kb = os.path.getsize(os.path.join(OUT, "film-sheet.md")) / 1024
    print(f"motion/film-sheet.md ditulis · {kb:.0f} KB · {len(d['adegan'])} adegan · "
          f"{cue} cue · {BPM} BPM · {FRAME_TOTAL} frame · {len(d['masalah'])} masalah")


if __name__ == "__main__":
    main()
