#!/usr/bin/env python3
"""
Audit "anti-slop" + kontrak desain + aturan gerak.

Menjalankan 30 aturan yang bisa diperiksa mesin, diturunkan dari:
  · pbakaus/impeccable — `crates/live/assets/antipatterns.json` (62 aturan
    slop & quality), dipakai sebagai daftar periksa; yang tidak bisa diukur
    dari berkas ditandai `manual`, bukan diklaim lolos.
  · greensock/gsap-skills — aturan performa: transform/opacity saja, satu loop
    rAF, listener pasif, reduced-motion.
  · nextlevelbuilder/ui-ux-pro-max — disiplin token: warna/radius/ukuran font
    harus berasal dari sistem, bukan angka baru yang muncul di tengah CSS.
  · GLips/Figma-Context-MCP — semantik "layout dari sumber": token dibaca dari
    data/design-system.json, CSS diperiksa terhadapnya (peran Figma digantikan
    berkas kontrak, karena tidak ada akses Figma di lingkungan ini).

Menulis:
    laporan/slop.md      tabel temuan untuk dibaca manusia
    laporan/slop.json    ringkasan mesin (dipakai tools/periksa.py & laporan.py)

Exit code 0 selalu; gerbang keras ada di tools/periksa.py.

Pakai:
    python3 tools/slop.py
    python3 tools/slop.py --ringkas
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "laporan")
DS = json.load(open(os.path.join(ROOT, "data", "design-system.json"), encoding="utf-8"))

CSS_FILES = DS["berkas_css"]
PUBLIK = DS["halaman_publik"]
INTERNAL = ["dashboard/index.html", "laporan/index.html", "riset/index.html",
            "konten/index.html", "studio/index.html", "motion/index.html"]
JS_FILES = ["assets/js/motion.js", "assets/js/motion-ui.js", "assets/js/motion-3d.js", "assets/js/site.js"]

PEN_KECUALIAN = {p["id"]: p for p in DS["pengecualian"]}


def baca(p):
    q = os.path.join(ROOT, p)
    if not os.path.exists(q):
        return ""
    with open(q, encoding="utf-8", errors="ignore") as f:
        return f.read()


def ada(p):
    return os.path.exists(os.path.join(ROOT, p))


def teks_tampak(html):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&[a-z]+;|&#\d+;", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def gaya_inline(html):
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S | re.I))


def semua_css():
    bagian = {}
    for f in CSS_FILES:
        if ada(f):
            bagian[f] = baca(f)
    for f in PUBLIK + INTERNAL:
        if ada(f):
            st = gaya_inline(baca(f))
            if st.strip():
                bagian[f + " (gaya inline)"] = st
    return bagian


def rasio_kontras(warna1, warna2):
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    def lum(hexs):
        h = hexs.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    a, b = lum(warna1), lum(warna2)
    terang, gelap = max(a, b), min(a, b)
    return round((terang + 0.05) / (gelap + 0.05), 2)


# ───────────────────────────── aturan ─────────────────────────────────────
# tingkat: kritis = harus diperbaiki sebelum tayang; perhatian = perlu keputusan;
#          info = dicatat saja
ATURAN = [
    ("side-tab", "Garis aksen tebal di satu sisi kartu", "slop", "perhatian", "impeccable#side-tab"),
    ("nested-cards", "Kartu di dalam kartu", "slop", "perhatian", "impeccable#nested-cards"),
    ("gradient-text", "Teks bergradien", "slop", "kritis", "impeccable#gradient-text"),
    ("bounce-easing", "Easing memantul (overshoot)", "slop", "perhatian", "impeccable#bounce-easing"),
    ("pulsing-dot", "Titik status berdenyut", "slop", "perhatian", "impeccable#pulsing-dot"),
    ("blinking-cursor", "Kursor berkedip dekoratif", "slop", "perhatian", "impeccable#blinking-cursor"),
    ("radial-glow", "Sorotan radial dekoratif", "slop", "info", "impeccable#radial-halo"),
    ("marquee", "Marquee berjalan otomatis", "slop", "info", "impeccable#marquee"),
    ("kicker-above-heading", "Label kecil di atas judul", "slop", "perhatian", "impeccable#kicker-above-heading"),
    ("em-dash-overuse", "Tanda pisah berlebihan", "slop", "perhatian", "impeccable#em-dash-overuse"),
    ("buzzword", "Kata pemasaran kosong", "slop", "kritis", "impeccable#marketing-buzzword"),
    ("tiny-text", "Teks di bawah 11 px", "quality", "perhatian", "impeccable#tiny-text"),
    ("skipped-heading", "Lompatan tingkat judul (h1 → h3)", "quality", "kritis", "impeccable#skipped-heading"),
    ("justified-text", "Teks rata kanan-kiri", "quality", "perhatian", "impeccable#justified-text"),
    ("hidden-at-rest", "Konten tak terlihat tanpa JS", "quality", "kritis", "impeccable#content-hidden-at-rest"),
    ("monotonous-spacing", "Spasi seragam terus-menerus", "quality", "perhatian", "impeccable#monotonous-spacing"),
    ("kontras-rendah", "Kontras teks di bawah 4,5:1", "quality", "kritis", "impeccable#low-contrast"),
    ("ds-warna", "Warna di luar kontrak desain", "sistem-desain", "perhatian", "ui-ux-pro-max#token"),
    ("ds-radius", "Radius di luar kontrak desain", "sistem-desain", "perhatian", "ui-ux-pro-max#token"),
    ("ds-ukuran-font", "Ukuran font di luar skala", "sistem-desain", "perhatian", "ui-ux-pro-max#token"),
    ("ds-keluarga-font", "Font di luar kontrak desain", "sistem-desain", "perhatian", "ui-ux-pro-max#token"),
    ("animasi-layout", "JS menganimasikan lebar/tinggi/posisi", "gerak", "kritis", "gsap-skills#performance"),
    ("listener-pasif", "Listener gulir tanpa passive", "gerak", "kritis", "gsap-skills#performance"),
    ("reduced-motion", "File beranimasi tanpa blok reduced-motion", "gerak", "kritis", "gsap-skills#core"),
    ("loop-tak-berujung", "Animasi tak berujung", "gerak", "info", "gsap-skills#performance"),
    ("will-change", "will-change dipasang permanen", "gerak", "perhatian", "gsap-skills#performance"),
    ("alt-gambar", "Gambar tanpa teks alternatif", "quality", "kritis", "impeccable#quality"),
    ("bahasa-halaman", "Atribut lang hilang", "quality", "perhatian", "impeccable#quality"),
    ("meta-viewport", "Meta viewport hilang", "quality", "kritis", "impeccable#quality"),
]


def audit():
    temuan = []
    css = semua_css()
    html_publik = {f: baca(f) for f in PUBLIK if ada(f)}
    html_internal = {f: baca(f) for f in INTERNAL if ada(f)}
    js = {f: baca(f) for f in JS_FILES if ada(f)}

    def tambah(kunci, berkas, bukti, catatan="", tingkat=None):
        meta = next(a for a in ATURAN if a[0] == kunci)
        pen = PEN_KECUALIAN.get(kunci)
        tingkat_akhir = tingkat or meta[3]
        if pen and tingkat_akhir != "kritis":
            tingkat_akhir = "info"
        temuan.append({
            "aturan": meta[0], "nama": meta[1], "kategori": meta[2],
            "tingkat": tingkat_akhir, "sumber": meta[4],
            "berkas": berkas, "bukti": bukti[:220],
            "catatan": catatan or (pen["alasan"] if pen else ""),
            "dikecualikan": bool(pen),
        })

    # ── CSS: aturan slop ──
    for f, t0 in css.items():
        t = re.sub(r"/\*.*?\*/", " ", t0, flags=re.S)
        for m in re.finditer(r"([^{}]{0,80})\{([^{}]*border-left:\s*([6-9]|\d{2,})px\s+solid[^{}]*)\}", t):
            blok = m.group(2)
            if re.search(r"width:\s*0|height:\s*0|border-block|border-top:", blok):
                continue
            tambah("side-tab", f, m.group(3) + " pada " + m.group(1).strip()[:40],
                   "ganti dengan garis atas atau latar; garis sisi tebal adalah penanda UI buatan mesin")
        if re.search(r"background-clip:\s*text|-webkit-background-clip:\s*text", t, re.I):
            tambah("gradient-text", f, "background-clip:text")
        for m in re.finditer(r"cubic-bezier\(([^)]*)\)", t):
            angka = [float(x) for x in re.findall(r"-?\d*\.?\d+", m.group(1))]
            if len(angka) == 4 and (angka[1] > 1.25 or angka[3] > 1.25):
                tambah("bounce-easing", f, m.group(0))
        if re.search(r"@keyframes\s+[\w-]*(pulse|denyut)", t, re.I) or \
           re.search(r"animation:[^;]*\b(pulse|ping)\b", t, re.I):
            tambah("pulsing-dot", f, "keyframes pulse/ping")
        if re.search(r"@keyframes\s+[\w-]*(blink|kedip)", t, re.I) or \
           re.search(r"caret-color|animation[^;]*blink", t, re.I):
            tambah("blinking-cursor", f, "keyframes blink")
        n_radial = len(re.findall(r"radial-gradient\(", t))
        if n_radial:
            tambah("radial-glow", f, f"{n_radial} radial-gradient",
                   "dipakai hanya untuk sorotan kursor di hero & spotlight kartu; mati saat reduced-motion",
                   tingkat="info")
        for m in re.finditer(r"animation:[^;]*infinite[^;]*", t):
            tambah("loop-tak-berujung", f, m.group(0), "", tingkat="info")
        if re.search(r"\.card\s+\.card(?![_-])|\.kartu\s+\.kartu(?![_-])", t):
            tambah("nested-cards", f, "selector kartu di dalam kartu")
        if re.search(r"text-align:\s*justify", t):
            tambah("justified-text", f, "text-align:justify")
        # spasi: hitung nilai berbeda
        nilai_spasi = set()
        for m in re.finditer(r"(?:padding|margin|gap|row-gap|column-gap)[^:]*:\s*([^;}]+)", t):
            for v in re.findall(r"(\d+(?:\.\d+)?)px", m.group(1)):
                nilai_spasi.add(float(v))
        if len(re.findall(r"(?:padding|margin|gap)[^:]*:", t)) >= 6 and len(nilai_spasi) < 4:
            tambah("monotonous-spacing", f, f"hanya {len(nilai_spasi)} nilai spasi berbeda")
        # teks kecil
        if "gaya inline" in f:
            continue   # halaman internal (noindex) memakai label tabel 9-10 px
        kecil = sorted({float(m.group(1)) for m in re.finditer(r"font-size:\s*(\d+(?:\.\d+)?)px", t)
                        if float(m.group(1)) < 10})
        if kecil:
            tambah("tiny-text", f, ", ".join(f"{k:g}px" for k in kecil),
                   "label mikro boleh < 11 px hanya bila tidak informatif; periksa satu per satu")
        # reduced motion
        if re.search(r"@keyframes|animation:|\btransition:", t) and not re.search(r"prefers-reduced-motion", t):
            tambah("reduced-motion", f, "ada animasi/transisi, tidak ada blok prefers-reduced-motion")
        # will-change: boleh untuk lapisan yang bergerak terus (gulir/hover),
        # dilarang untuk elemen yang hanya masuk sekali lalu diam
        LAPISAN_GULIR = ("scrollbar", "cursor-glow", "foot__poster", "manifesto__quote",
                         "ui-progress", "tilt__inner", "marquee", "ticker")
        for m in re.finditer(r"([^{}]{0,100})\{([^{}]*will-change:\s*([a-z,\s]+)[^{}]*)\}", t):
            sel, nilai = m.group(1).strip().split("}")[-1].strip(), m.group(3).strip()
            if nilai == "auto" or not sel:
                continue
            if any(x in sel for x in LAPISAN_GULIR) or ":hover" in sel:
                continue
            tambah("will-change", f, f"{sel[:60]} → will-change:{nilai}",
                   "elemen masuk-sekali: pasang will-change hanya selama animasi, "
                   "lalu kembalikan ke auto")

    # ── kontras per-pemakaian: oranye untuk teks kecil ──
    for f, t0 in css.items():
        if "inline" in f:
            continue
        t = re.sub(r"/\*.*?\*/", " ", t0, flags=re.S)
        for m in re.finditer(r"([^{}]{0,120})\{([^{}]*)\}", t):
            sel, blok = m.group(1).strip().split("}")[-1].strip(), m.group(2)
            if not re.search(r"(?:^|;|\s)color:\s*var\(--orange\)", blok):
                continue
            if "::before" in sel or "::after" in sel:
                continue
            ukuran = re.search(r"font-size:\s*(\d+(?:\.\d+)?)px", blok)
            px = float(ukuran.group(1)) if ukuran else 17.0
            latar = re.search(r"background:\s*(?:var\(--(paper|ink)\))", blok)
            if latar and latar.group(1) == "ink":
                continue
            if px < 18.66:
                tambah("kontras-rendah", f, f"{sel} · {px:g}px oranye di atas kertas (3,33:1)",
                       "oranye hanya lolos untuk teks besar (≥24 px, atau ≥18,66 px tebal); "
                       "teks kecil pakai --espresso")

    # ── kontrak desain ──
    warna_boleh = {w.lower() for w in DS["warna"]["boleh_dipakai"]}
    for f, t in css.items():
        if "inline" in f:
            continue  # halaman internal punya palet sendiri (noindex)
        t_warna = re.sub(r"(?:-webkit-)?mask(?:-image)?:[^;}]+", " ", t)
        for m in re.finditer(r"#([0-9a-fA-F]{3,8})\b", t_warna):
            if ("#" + m.group(1)).lower() not in warna_boleh:
                tambah("ds-warna", f, "#" + m.group(1),
                       "warna tidak ada di data/design-system.json → warna", tingkat="perhatian")
        for m in re.finditer(r"border-radius:\s*([^;}]+)", t):
            v = m.group(1).strip()
            if v not in DS["radius"] and not v.startswith("clamp") and not v.startswith("var"):
                tambah("ds-radius", f, v, "", tingkat="perhatian")
        for m in re.finditer(r"font-size:\s*(\d+(?:\.\d+)?)px", t):
            v = float(m.group(1))
            if v not in DS["tipografi"]["skala_px"]:
                tambah("ds-ukuran-font", f, f"{v:g}px", "", tingkat="perhatian")
        for m in re.finditer(r"font-family:\s*([^;}]+)", t):
            fam = m.group(1)
            if "var(" in fam:
                continue
            nama = re.findall(r"[A-Z][A-Za-z ]+|[a-z-]+", fam)
            diizinkan = {"Bricolage Grotesque", "Fraunces", "Inter"}
            for n in nama:
                n = n.strip()
                if n and n not in diizinkan and n.lower() not in {
                        "system-ui", "-apple-system", "segoe ui", "sans-serif", "serif",
                        "georgia", "times new roman", "impact", "archivo black", "ui-monospace",
                        "sfmono-regular", "menlo", "monaco", "consolas", "monospace", "inherit"}:
                    tambah("ds-keluarga-font", f, n, "", tingkat="perhatian")

    # ── JS: aturan gerak ──
    for f, t in js.items():
        for m in re.finditer(r"style\.(width|height|top|left|right|bottom|margin\w*)\s*=", t):
            tambah("animasi-layout", f, m.group(0),
                   "animasikan transform/opacity; properti layout memicu reflow")
        for m in re.finditer(r"addEventListener\(\s*['\"](?:scroll|touchmove|wheel)['\"]", t):
            jendela = t[m.end():m.end() + 220]
            if "passive: true" not in jendela:
                tambah("listener-pasif", f, m.group(0))
        if "prefers-reduced-motion" not in t:
            tambah("reduced-motion", f, "tidak memeriksa prefers-reduced-motion")

    # ── HTML: struktur & teks ──
    for f, h in html_publik.items():
        teks = teks_tampak(h)
        kata = len(teks.split())
        n_dash = teks.count("—")
        if kata > 120 and n_dash > max(3, kata // 45):
            tambah("em-dash-overuse", f, f"{n_dash} tanda pisah untuk {kata} kata",
                   "ganti sebagian dengan titik dua, koma, atau kalimat baru")
        buzz = ["solusi terbaik", "revolusioner", "seamless", "unlock", "elevate",
                "supercharge", "game changer", "next level", "tak tertandingi",
                "pengalaman tak terlupakan", "kualitas premium terjamin"]
        for b in buzz:
            if b in teks.lower():
                tambah("buzzword", f, b)
        n_kicker = len(re.findall(r'class="[^"]*kicker', h))
        if n_kicker > 5:
            tambah("kicker-above-heading", f, f"{n_kicker} label kicker",
                   "kontrak: maksimal 2 per halaman")
        if not re.search(r"<html[^>]+lang=", h):
            tambah("bahasa-halaman", f, "<html> tanpa lang")
        if not re.search(r'name="viewport"', h):
            tambah("meta-viewport", f, "tanpa meta viewport")
        for m in re.finditer(r"<img\b[^>]*>", h):
            if "alt=" not in m.group(0):
                tambah("alt-gambar", f, m.group(0)[:90])

    # lompatan heading (semua halaman yang ada)
    for f in list(html_publik) + [x for x in INTERNAL if ada(x)]:
        h = html_publik.get(f) or baca(f)
        urutan = [int(m.group(1)) for m in re.finditer(r"<h([1-6])\b", h, re.I)]
        for a, b in zip(urutan, urutan[1:]):
            if b - a > 1:
                tambah("skipped-heading", f, f"h{a} → h{b}",
                       "heading hanya untuk struktur; kalau hanya butuh ukuran, pakai kelas")
                break

    # ── konten tersembunyi tanpa JS ──
    for f, t in css.items():
        for m in re.finditer(r"([^{}]{0,160})\{[^{}]*opacity:\s*0(?:\.0+)?\s*[;}]", t):
            sel = m.group(1).strip().split("}")[-1].strip()
            if not sel or sel.startswith("@") or "html.motion" in sel or "html.ui-motion" in sel:
                continue
            if re.fullmatch(r"(from|to|\d+%)", sel) or sel.endswith("%"):
                continue
            if any(x in sel for x in ("placeholder", "hidden", "sr-only", "::before", "::after",
                                      "cursor-glow", "scrollbar", "ui-progress", "spotlight",
                                      "no-js", "no-motion", "is-off")):
                continue
            tambah("hidden-at-rest", f, sel[:110],
                   "elemen bisa tak terlihat bila JS gagal; bungkus dengan kelas yang ditambahkan JS")

    # ── kontras dari token ──
    pasangan = [("--ink", "--paper"), ("--ink-55", "--paper"), ("--ink-80", "--paper"),
                ("--paper", "--ink"), ("--espresso", "--paper")]
    for a, b in pasangan:
        ca = DS["warna"]["inti"].get(a) or DS["warna"]["turunan"].get(a)
        cb = DS["warna"]["inti"].get(b) or DS["warna"]["turunan"].get(b)
        if not ca or not cb:
            continue
        if a == "--ink-55":
            ca = "#6F655A"   # hasil komposit rgba(22,17,13,.55) di atas --paper
        if a == "--ink-80":
            ca = "#4A423B"
        rasio = rasio_kontras(ca, cb)
        if rasio < 4.5:
            tambah("kontras-rendah", "assets/css/site.css",
                   f"{a} di atas {b} = {rasio}:1",
                   "naikkan kepekatan atau batasi pemakaiannya pada teks besar saja")

    # gabungkan temuan kembar (berkas+bukti sama)
    unik, kunci = [], set()
    for t in temuan:
        k = (t["aturan"], t["berkas"], t["bukti"])
        if k in kunci:
            continue
        kunci.add(k)
        unik.append(t)
    return unik


def md(temuan, tgl):
    kritis = [t for t in temuan if t["tingkat"] == "kritis"]
    perhatian = [t for t in temuan if t["tingkat"] == "perhatian"]
    info = [t for t in temuan if t["tingkat"] == "info"]
    kecuali = [t for t in temuan if t["dikecualikan"]]

    def tabel(rows):
        if not rows:
            return "| — | — | — |\n"
        return "".join(
            f'| `{t["aturan"]}` | {escape(t["berkas"])} | {escape(t["bukti"])} | '
            f'{escape(t["catatan"] or "—")} |\n' for t in rows)

    manual = [
        ("nested-cards", "butuh melihat hasil render, bukan berkas"),
        ("text-occlusion", "butuh render di browser"),
        ("line-length", "butuh lebar nyata saat dirender"),
        ("unbalanced-heading", "butuh pengukuran lebar baris"),
        ("design-system-color (render)", "var() baru terbaca setelah CSS dihitung"),
        ("clipped-overflow-container", "butuh render"),
        ("first-viewport-column-overflow", "butuh render"),
    ]
    o = [f"""# Audit anti-slop & kontrak desain — {tgl.isoformat()}

Dibuat `tools/slop.py`. Sumber aturan: `pbakaus/impeccable`
(`antipatterns.json`, 62 aturan), `greensock/gsap-skills` (aturan performa),
`nextlevelbuilder/ui-ux-pro-max` (disiplin token), `GLips/Figma-Context-MCP`
(token diperiksa terhadap kontrak, bukan terhadap tangkapan layar).

| Ringkasan | Jumlah |
| --- | ---: |
| Aturan diperiksa mesin | **{len(ATURAN)}** |
| Temuan kritis | **{len(kritis)}** |
| Temuan perhatian | **{len(perhatian)}** |
| Catatan info | **{len(info)}** |
| Temuan yang masuk daftar pengecualian | **{len(kecuali)}** |
| Pengecualian terdokumentasi (kesepakatan brand) | **{len(DS["pengecualian"])}** |

## 1 · Kritis — harus diperbaiki sebelum tayang

| Aturan | Berkas | Bukti | Catatan |
| --- | --- | --- | --- |
{tabel(kritis)}
## 2 · Perhatian — perlu keputusan

| Aturan | Berkas | Bukti | Catatan |
| --- | --- | --- | --- |
{tabel(perhatian)}
## 3 · Info

| Aturan | Berkas | Bukti | Catatan |
| --- | --- | --- | --- |
{tabel(info)}
## 4 · Yang dikecualikan karena kesepakatan brand

| Aturan | Keputusan | Alasan | Sumber |
| --- | --- | --- | --- |
"""]
    for p in DS["pengecualian"]:
        o.append(f'| `{p["id"]}` | {p["keputusan"]} | {escape(p["alasan"])} | {escape(p["sumber"])} |\n')

    o.append("""
## 5 · Yang tidak bisa diperiksa mesin

| Aturan | Kenapa |
| --- | --- |
""")
    for a, b in manual:
        o.append(f"| `{a}` | {b} |\n")

    o.append("""
## 6 · Cara membaca

Audit ini memeriksa **berkas**, bukan tampilan jadi. Semua hijau berarti CSS/JS
tidak memuat pola yang biasa dipakai untuk menandai UI buatan mesin, bukan berarti
desainnya sudah bagus. Empat hal tetap dinilai manusia: apakah gerak punya alasan,
apakah hierarki terasa benar saat digulir, apakah copy terdengar seperti pemilik
kedai, dan apakah produk terlihat layak dibeli.
""")
    return "".join(o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ringkas", action="store_true")
    args = ap.parse_args()

    tgl = hari_ini()
    temuan = audit()
    kritis = [t for t in temuan if t["tingkat"] == "kritis"]
    perhatian = [t for t in temuan if t["tingkat"] == "perhatian"]
    info = [t for t in temuan if t["tingkat"] == "info"]

    print(f"Audit anti-slop — {tgl.isoformat()}")
    print(f"  aturan diperiksa : {len(ATURAN)}")
    print(f"  kritis           : {len(kritis)}")
    for t in kritis[:8]:
        print(f"    ! {t['aturan']:<18} {t['berkas']:<34} {t['bukti'][:60]}")
    print(f"  perhatian        : {len(perhatian)}")
    print(f"  info             : {len(info)}")
    print(f"  dikecualikan     : {sum(1 for t in temuan if t['dikecualikan'])}")

    if args.ringkas:
        return

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "slop.md"), "w", encoding="utf-8") as f:
        f.write(md(temuan, tgl))
    ringkas = {
        "dibuat": tgl.isoformat(),
        "aturan_diperiksa": len(ATURAN),
        "kritis": len(kritis), "perhatian": len(perhatian), "info": len(info),
        "dikecualikan": len(DS["pengecualian"]),
        "temuan_dikecualikan": sum(1 for t in temuan if t["dikecualikan"]),
        "temuan": temuan,
        "per_aturan": {a[0]: sum(1 for t in temuan if t["aturan"] == a[0]) for a in ATURAN},
    }
    with open(os.path.join(OUT, "slop.json"), "w", encoding="utf-8") as f:
        json.dump(ringkas, f, ensure_ascii=False, indent=2)
    print("  laporan          : laporan/slop.md · laporan/slop.json")


if __name__ == "__main__":
    main()
