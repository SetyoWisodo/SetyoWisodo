#!/usr/bin/env python3
"""Halaman "Semua" — satu pintu untuk meninjau seluruh hasil kerja.

Kenapa ada: memberi orang delapan tautan terpisah membuat ia harus menebak
mana yang penting. Halaman ini jadi **satu alamat** yang memuat semuanya:
tautan ke setiap halaman, gambar pratinjau, angka gerbang terakhir, dan
daftar berkas yang bisa diunduh (video, label, poster).

Angka di halaman ini tidak diketik: semuanya dibaca dari
`laporan/periksa.json`, `data/catalog.json`, dan `data/biji3d.json`.

Pakai:
    python3 tools/semua.py           # tulis semua.html
    python3 tools/semua.py --cek     # periksa berkas + tautan
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KELUAR = os.path.join(ROOT, "semua.html")

# (berkas, judul, kelompok, keterangan, gambar pratinjau atau "")
HALAMAN = [
    ("index.html", "Beranda", "Situs",
     "Biji kopi render 3D di kiri, motto “Terjaga untuk rasa yang sesungguhnya.” di kanan. "
     "Enam titik senyawa bisa diketuk.", "assets/img/biji-3d-poster.webp"),
    ("rak/index.html", "Rak sangrai", "Situs",
     "Hero rak 3D: dua belas lot berdiri di rak, satu ditarik keluar dan diputar "
     "menghadap Anda. Panah, tab, geser, roda, dan kursor kustom.", ""),
    ("cutaway/index.html", "Potong-buka", "Situs",
     "Kemasan Blue Mount Ijen dibuka bagian demi bagian: 7 bagian, 9 ketukan, "
     "satu kamera per bagian. Metode Cutaway (MIT), dibangun dari kode tanpa WebGL.",
     "cutaway/still/lembar-still.png"),
    ("biji-sangrai/index.html", "Biji sangrai", "Situs",
     "Halaman jual roasted beans: 9 biji, tabel harga, tombol WhatsApp per biji, "
     "catatan rasa yang bisa digeser.", "assets/img/produk/ijen.jpg"),
    ("kampanye/index.html", "Landing kampanye", "Situs",
     "Halaman kampanye “kopi yang jujur soal tanggal”, lengkap dengan kode UTM.",
     "konten/carousel-01a.jpg"),
    ("komersial/penawaran-b2b.html", "Penawaran B2B", "Situs",
     "Harga grosir empat tier untuk kedai, kantor, dan reseller.",
     "assets/img/produk/gayo.jpg"),

    ("laporan/index.html", "Ringkasan penilaian", "Papan & laporan",
     "Satu halaman berisi apa yang sudah selesai, bukti, dan batasnya.",
     ""),
    ("dashboard/index.html", "Papan harian", "Papan & laporan",
     "Target 29 KPI per divisi, ritme kerja harian dan mingguan.", ""),
    ("laporan/slop.md", "Audit anti-slop", "Papan & laporan",
     "29 aturan desain, 0 temuan kritis. Berkas teks, bukan halaman.", ""),

    ("brand/index.html", "Brand kit", "Aset cetak",
     "Logo, palet, tipografi, 9 label siap cetak 70×100 mm, lembar A4.",
     "brand/label-blue-mount-ijen.png"),

    ("konten/index.html", "Konten siap pakai", "Konten",
     "15 aset: carousel, story, feed, dan 5 reel 9:16 dengan caption.",
     "konten/post-01-peta-rasa.jpg"),
    ("studio/index.html", "Studio konten", "Konten",
     "Sepuluh tahap dari nilai brand sampai brief hari Senin.", ""),
    ("riset/index.html", "Riset & swipe file", "Konten",
     "Pola konten ramai, kata kunci, dan lima brief turunan.", ""),
    ("motion/index.html", "Lab gerak", "Gerak",
     "Lima adegan 9:16, timeline 120 BPM, dan lembar film 540 frame.",
     "motion/render/frame/0000.png"),
    ("prompts/index.html", "Pustaka prompt", "Prompt",
     "Sembilan prompt kelas atas dengan tujuh blok dan token warna yang patuh.",
     ""),

    ("biji-sangrai/biji-sangrai-luring.html", "Versi 1 berkas (unduh)", "Berkas tunggal",
     "Halaman biji sangrai dengan CSS, JS, huruf, dan gambar disisipkan — "
     "bisa dibuka tanpa server.", ""),
]

UNDUHAN = [
    ("motion/render/klip-01-nocturne-9s.mp4", "Klip jadi 9 detik · 9:16", "MP4"),
    ("konten/reel-01-menit-terakhir.mp4", "Reel 01 · menit terakhir", "MP4"),
    ("brand/label-sheet-a4.png", "Lembar label A4 siap cetak", "PNG"),
    ("assets/img/biji-3d-poster.webp", "Render biji 640×800", "WebP"),
    ("cutaway/cutaway-luring.html", "Potong-buka · satu berkas", "HTML"),
    ("semua.html", "Halaman ini (satu berkas)", "HTML"),
]


def baca_json(rel: str):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def angka() -> dict:
    periksa = baca_json("laporan/periksa.json")
    # cek "Pintu semua" membaca berkas ini; kalau ia ikut dihitung, angkanya
    # berubah setiap kali gerbang dijalankan dan berkasnya selamanya "basi".
    hasil = [h for h in periksa["hasil"] if h["kategori"] != "Pintu semua"]
    katalog = baca_json("data/catalog.json")
    biji = baca_json("data/biji3d.json")
    return {
        "tanggal": periksa.get("dibuat", ""),
        "cek": len(hasil),
        "lolos": sum(1 for h in hasil if h["status"] == "lolos"),
        "gagal": sum(1 for h in hasil if h["status"] == "gagal"),
        "peringatan": sum(1 for h in hasil if h["status"] == "peringatan"),
        "sku": len(katalog["products"]),
        "ukuran": len({v["grams"] for p in katalog["products"] for v in p["variants"]}),
        "harga": min(v["price"] for p in katalog["products"] for v in p["variants"]),
        "zona": len(biji["zona"]),
        "senyawa": sum(len(z["senyawa"]) for z in biji["zona"]),
    }


def rupiah(n: int) -> str:
    return "Rp" + f"{n:,}".replace(",", ".")


def kartu(item, pertama: bool) -> str:
    path, judul, kelompok, ket, gambar = item
    ada = os.path.exists(os.path.join(ROOT, path))
    tanda = "" if ada else ' <span class="hilang">belum ada</span>'
    media = ""
    if gambar and os.path.exists(os.path.join(ROOT, gambar)):
        media = (f'<span class="kartu__media"><img src="{gambar}" alt="" '
                 f'loading="lazy" decoding="async" width="400" height="300"></span>')
    else:
        # tanpa gambar: pita tipis berisi siluet biji, supaya kartu tidak kosong
        media = ('<span class="kartu__media kartu__media--kosong" aria-hidden="true">'
                 '<svg viewBox="0 0 40 56" width="26" height="36">'
                 '<ellipse cx="20" cy="28" rx="14" ry="20" fill="none" stroke="currentColor" stroke-width="1.6"/>'
                 '<path d="M20 9c-3 6-3 12 0 19s3 13 0 19" fill="none" stroke="currentColor" stroke-width="1.6"/>'
                 '</svg></span>')
    return f"""      <a class="kartu{' kartu--utama' if pertama else ''}" href="{path}">
        {media}
        <span class="kartu__isi">
          <span class="kartu__kelompok">{html.escape(kelompok)}</span>
          <span class="kartu__judul">{html.escape(judul)}{tanda}</span>
          <span class="kartu__ket">{html.escape(ket)}</span>
          <span class="kartu__buka">Buka <span aria-hidden="true">→</span></span>
        </span>
      </a>"""


TPL_VER = "1"


def sidik() -> str:
    """Sidik struktur (daftar halaman + versi templat), tanpa angka apa pun."""
    import hashlib
    bahan = json.dumps(
        {"halaman": HALAMAN, "unduhan": UNDUHAN, "versi": TPL_VER},
        ensure_ascii=False, sort_keys=True,
    )
    return hashlib.sha256(bahan.encode("utf-8")).hexdigest()[:12]


def bangun() -> tuple[str, list[str], list[str]]:
    a = angka()
    b = baca_json("data/catalog.json")["brand"]
    kelompok = []
    for item in HALAMAN:
        if item[2] not in kelompok:
            kelompok.append(item[2])

    bagian = []
    for k in kelompok:
        isi = [kartu(i, i[1] == "Beranda") for i in HALAMAN if i[2] == k]
        bagian.append(f"""    <section class="bagian" id="{k.lower().replace(' ', '-').replace('&', 'dan')}">
      <div class="bagian__kepala">
        <h2>{html.escape(k)}</h2>
        <span class="bagian__jumlah">{len(isi)} halaman</span>
      </div>
      <div class="kisi">
{chr(10).join(isi)}
      </div>
    </section>""")

    unduhan = "\n".join(
        f'        <a class="unduh" href="{p}"><b>{html.escape(j)}</b>'
        f'<span>{t}'
        + ("" if p == "semua.html"
           else f' · {os.path.getsize(os.path.join(ROOT, p)) / 1024:.0f} KB')
        + '</span></a>'
        for p, j, t in UNDUHAN if os.path.exists(os.path.join(ROOT, p))
    )

    isi = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Semua halaman — Nocturne Koffie</title>
<meta name="description" content="Satu alamat untuk meninjau seluruh hasil kerja Nocturne Koffie: situs, halaman jual, brand kit, konten, gerak, dan laporan.">
<meta name="theme-color" content="#F5EFE4">
<!-- dibuat tools/semua.py · sidik struktur {sidik()} · jangan diedit tangan -->
<link rel="icon" href="brand/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="Semua halaman — Nocturne Koffie">
<meta property="og:image" content="assets/img/biji-3d-poster.webp">
<style>
@font-face{{font-family:"Bricolage Grotesque";src:url("assets/fonts/bricolage-grotesque-latin-800-normal.ttf") format("truetype");font-weight:800;font-display:swap}}
@font-face{{font-family:"Fraunces";src:url("assets/fonts/fraunces-latin-300-normal.ttf") format("truetype");font-weight:300;font-display:swap}}
@font-face{{font-family:"Inter";src:url("assets/fonts/inter-latin-400-normal.ttf") format("truetype");font-weight:400;font-display:swap}}
@font-face{{font-family:"Inter";src:url("assets/fonts/inter-latin-600-normal.ttf") format("truetype");font-weight:600;font-display:swap}}

:root{{
  --paper:#F5EFE4; --paper-2:#EFE6D6; --ink:#16110D; --orange:#E1542B;
  --gold:#D9A441; --espresso:#4A2C1A;
  --ink-80:rgba(22,17,13,.8); --ink-55:rgba(22,17,13,.55); --garis:rgba(22,17,13,.16);
  --display:"Bricolage Grotesque",Impact,system-ui,sans-serif;
  --serif:"Fraunces",Georgia,serif; --body:"Inter",system-ui,sans-serif;
  --pad:clamp(18px,4vw,52px); --ease:cubic-bezier(.22,.61,.36,1);
}}
*,*::before,*::after{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
  font-size:15.5px;line-height:1.6;-webkit-font-smoothing:antialiased}}
img{{display:block;max-width:100%;height:auto}}
a{{color:inherit;text-decoration:none}}
:focus-visible{{outline:2px solid var(--orange);outline-offset:3px}}
.wrap{{max-width:1240px;margin-inline:auto;padding-inline:var(--pad)}}

.kepala{{padding-block:clamp(34px,6vw,64px) clamp(20px,3vw,32px);border-bottom:2px solid var(--ink)}}
.kepala .micro{{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;font-weight:600;
  color:var(--ink-55);display:flex;align-items:center;gap:9px;margin:0 0 14px}}
.dot{{width:6px;height:6px;border-radius:50%;background:var(--orange)}}
h1{{font-family:var(--display);font-weight:800;font-size:clamp(2.2rem,7.6vw,4.6rem);
  line-height:.9;letter-spacing:-.04em;margin:0;text-transform:uppercase}}
h1 em{{font-family:var(--serif);font-style:italic;font-weight:300;text-transform:none;
  color:var(--espresso);font-size:.62em;display:block;letter-spacing:-.01em;margin-top:.14em}}
.lede{{margin:18px 0 0;max-width:56ch;color:var(--ink-80);font-size:clamp(14.5px,1.5vw,16.5px)}}

.angka{{display:grid;grid-template-columns:repeat(2,1fr);gap:0;margin-top:clamp(24px,4vw,36px);
  border-top:1px solid var(--garis)}}
.angka div{{padding:16px 0;border-bottom:1px solid var(--garis)}}
.angka div:nth-child(odd){{border-right:1px solid var(--garis);padding-right:14px}}
.angka div:nth-child(even){{padding-left:16px}}
.angka b{{display:block;font-family:var(--display);font-size:clamp(1.5rem,4vw,2.1rem);
  line-height:1;letter-spacing:-.03em;font-variant-numeric:tabular-nums}}
.angka span{{display:block;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-55);margin-top:7px}}
.angka .ok{{color:var(--espresso)}}

.bagian{{padding-block:clamp(28px,4.4vw,46px);border-bottom:1px solid var(--garis)}}
.bagian__kepala{{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:16px}}
h2{{font-family:var(--display);font-weight:800;font-size:clamp(1.1rem,2.6vw,1.5rem);
  letter-spacing:-.02em;text-transform:uppercase;margin:0}}
.bagian__jumlah{{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-55)}}
.kisi{{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr))}}

.kartu{{display:flex;flex-direction:column;border:2px solid var(--ink);border-radius:3px;
  overflow:hidden;background:rgba(255,255,255,.4);
  transition:transform .3s var(--ease),background .24s var(--ease),box-shadow .3s var(--ease)}}
.kartu:hover{{transform:translateY(-3px);background:#fff;box-shadow:0 16px 34px -22px rgba(0,0,0,.6)}}
.kartu__media{{display:block;background:var(--paper-2);border-bottom:1px solid var(--garis)}}
.kartu__media img{{width:100%;aspect-ratio:4/3;object-fit:cover}}
.kartu__media--kosong{{display:grid;place-items:center;height:74px;color:var(--espresso);
  background:repeating-linear-gradient(135deg,var(--paper-2) 0 8px,rgba(74,44,26,.05) 8px 16px)}}
.kartu__isi{{display:flex;flex-direction:column;gap:5px;padding:14px 15px 15px}}
.kartu__kelompok{{font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--orange);font-weight:600}}
.kartu__judul{{font-family:var(--display);font-weight:800;font-size:1.05rem;letter-spacing:-.02em;line-height:1.15}}
.kartu__ket{{font-size:12.5px;color:var(--ink-80);line-height:1.55}}
.kartu__buka{{margin-top:8px;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
  font-weight:600;color:var(--ink-55);transition:color .2s,gap .2s;display:flex;gap:6px}}
.kartu:hover .kartu__buka{{color:var(--orange);gap:10px}}
.hilang{{color:var(--orange);font-size:11px;letter-spacing:.06em;text-transform:none}}

.unduh-kisi{{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr))}}
.unduh{{display:flex;flex-direction:column;gap:3px;padding:13px 15px;border:1.5px solid var(--garis);
  border-radius:3px;transition:border-color .24s,background .24s}}
.unduh:hover{{border-color:var(--ink);background:#fff}}
.unduh b{{font-weight:600;font-size:13.5px}}
.unduh span{{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-55)}}

.kaki{{padding-block:26px 34px;font-size:12px;color:var(--ink-55);line-height:1.7}}
.kaki b{{color:var(--ink);font-weight:600}}

@media (min-width:720px){{
  .angka{{grid-template-columns:repeat(4,1fr)}}
  .angka div{{border-right:1px solid var(--garis);border-bottom:0;padding:20px 18px}}
  .angka div:first-child{{padding-left:0}}
  .angka div:last-child{{border-right:0}}
}}
@media (prefers-reduced-motion:reduce){{
  *,*::before,*::after{{transition:none!important;animation:none!important}}
  .kartu:hover{{transform:none}}
}}
</style>
</head>
<body>

<header class="kepala">
  <div class="wrap">
    <p class="micro"><span class="dot" aria-hidden="true"></span>Satu pintu · semua hasil kerja · {html.escape(a['tanggal'])}</p>
    <h1>Nocturne<em>Semua halaman</em></h1>
    <p class="lede">
      {html.escape(b['city'])}, {html.escape(b['province'])}. Biji sangrai dari petani bernama,
      disangrai mingguan oleh Ais Coffee Roastery. Di bawah ini seluruh yang bisa Anda tinjau —
      situs, halaman jual, aset cetak, konten, gerak, dan laporan.
    </p>
    <div class="angka">
      <div><b class="ok">{a['lolos']}/{a['cek']}</b><span>Gerbang QA lolos</span></div>
      <div><b>{a['sku']}</b><span>Biji · {a['ukuran']} ukuran</span></div>
      <div><b>{rupiah(a['harga'])}</b><span>Harga mulai 100 g</span></div>
      <div><b>{a['zona']} × {a['senyawa'] // a['zona']}</b><span>Zona senyawa di hero</span></div>
    </div>
  </div>
</header>

<main class="wrap">
{chr(10).join(bagian)}

    <section class="bagian">
      <div class="bagian__kepala">
        <h2>Berkas unduhan</h2>
        <span class="bagian__jumlah">siap diunduh</span>
      </div>
      <div class="unduh-kisi">
{unduhan}
      </div>
    </section>
</main>

<footer class="kaki">
  <div class="wrap">
    <b>Nocturne Koffie</b> — {html.escape(b['city'])}, {html.escape(b['province'])} ·
    {html.escape(b['wa_display'])} · {html.escape(b['email'])}<br>
    Halaman ini dibuat otomatis oleh <b>tools/semua.py</b> dari <b>laporan/periksa.json</b>,
    <b>data/catalog.json</b>, dan <b>data/biji3d.json</b>. Angkanya bukan karangan: kalau gerbang
    berubah, halaman ini ikut berubah.
  </div>
</footer>

</body>
</html>
"""
    masalah = []
    catatan = []
    for path, judul, _, _, gambar in HALAMAN:
        if not os.path.exists(os.path.join(ROOT, path)):
            masalah.append(f"{judul}: berkas {path} tidak ada")
        if gambar and not os.path.exists(os.path.join(ROOT, gambar)):
            # pratinjau yang belum dirender bukan alasan menolak membangun pintu:
            # media kosong ditampilkan sebagai pita siluet, dan dicatat di catatan
            catatan.append(f"{judul}: pratinjau {gambar} belum ada (ditampilkan siluet)")
    return isi, masalah, catatan


def periksa() -> int:
    if not os.path.exists(KELUAR):
        print("XX semua.html belum dibuat")
        return 1
    teks = open(KELUAR, encoding="utf-8").read()
    masalah = []
    for path, judul, *_ in HALAMAN:
        if path not in teks:
            masalah.append(f"{judul} tidak tertaut")
    if f"sidik struktur {sidik()}" not in teks:
        masalah.append("sidik struktur tidak cocok — jalankan python3 tools/semua.py")
    a = angka()
    if f"{a['lolos']}/{a['cek']}" not in teks:
        masalah.append("angka gerbang di halaman tidak mutakhir — jalankan tools/semua.py")
    if "periksa.json" not in teks:
        masalah.append("tidak menyebut sumber angka (periksa.json)")
    if "fonts.googleapis" in teks or "cdn." in teks:
        masalah.append("memuat CDN")
    if "prefers-reduced-motion" not in teks:
        masalah.append("tanpa prefers-reduced-motion")
    for m in masalah:
        print("XX", m)
    print(f"{'OK' if not masalah else 'GAGAL'} · {len(HALAMAN)} halaman tertaut · "
          f"{os.path.getsize(KELUAR) / 1024:.0f} KB · {len(masalah)} masalah")
    return 0 if not masalah else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true")
    a = ap.parse_args()
    if a.cek:
        return periksa()
    teks, masalah, catatan = bangun()
    if masalah:
        for m in masalah:
            print("XX", m)
        return 1
    for c in catatan:
        print("  catatan:", c)
    with open(KELUAR, "w", encoding="utf-8") as f:
        f.write(teks)
    print(f"semua.html · {len(teks):,} karakter · {len(HALAMAN)} halaman · "
          f"{os.path.getsize(KELUAR) / 1024:.0f} KB · 0 masalah")
    return 0


if __name__ == "__main__":
    sys.exit(main())
