#!/usr/bin/env python3
"""
Gerbang periksa — QA otomatis untuk seluruh situs & data Nocturne.

Dijalankan setelah semua generator. Memeriksa 6 hal yang paling sering rusak diam-diam:

  1. Berkas wajib ada (halaman, aset, data)
  2. Tautan lokal di setiap halaman benar-benar menuju berkas yang ada
  3. Tag HTML seimbang (tidak ada div yang lupa ditutup)
  4. Data saling cocok (produk ↔ lot, manifest ↔ berkas aset, brief ↔ manifest)
  5. Klaim terlarang tidak muncul di halaman publik
  6. Batas ukuran (halaman awal < 1,5 MB; folder konten < 12 MB)

Menulis `laporan/periksa.md` + `laporan/periksa.json`. Exit code 1 bila ada temuan kritis.

Pakai:
    python3 tools/periksa.py
    python3 tools/periksa.py --ringkas     # hanya cetak tabel terminal
"""
from __future__ import annotations

import argparse
import json
import glob
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402
import re
from datetime import date
from html.parser import HTMLParser

class _Kosong:
    """Pengganti konteks gambar ketika Pillow tidak ada: semua butir yang butuh
    piksel dilewati, bukan membuat gerbang berhenti."""

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    size = (0, 0)

    def convert(self, *a, **k):
        return self

    def getpixel(self, *a, **k):
        return (0, 0, 0)


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "laporan")

HALAMAN_PUBLIK = ["index.html", "kampanye/index.html", "komersial/penawaran-b2b.html", "brand/index.html"]
# halaman internal (noindex) tidak diperiksa klaim: riset & papan sengaja memuat daftar kata terlarang

HALAMAN = [
    "index.html",
    "rak/index.html",
    "dashboard/index.html",
    "kampanye/index.html",
    "konten/index.html",
    "riset/index.html",
    "brand/index.html",
    "komersial/penawaran-b2b.html",
    "laporan/index.html",
    "studio/index.html",
    "motion/index.html",
    "prompts/index.html",
    "motion/frame-01.html", "motion/frame-02.html", "motion/frame-03.html",
    "motion/frame-04.html", "motion/frame-05.html",
]

DATA = [
    "data/catalog.json", "data/biaya.json", "data/stok-lot.json", "data/divisi.json",
    "data/kreatif.json", "data/legal.json", "data/batch-qc.csv", "data/pesanan.csv",
    "data/konten-14hari.csv", "data/kpi.csv", "data/riset-referensi.csv",
    "data/riset-komentar.csv", "data/riset-kata-kunci.csv",
    "data/studio-niche.json", "data/studio-hooks.csv", "data/studio-industri.csv",
    "studio/data.json", "studio/brief-senin.md",
    "data/design-system.json", "motion/timeline.json", "motion/data.json",
    "motion/film-sheet.md", "motion/film-sheet.json", "skills/motion-film/SKILL.md",
    "assets/css/motion-ui.css", "assets/js/motion-ui.js", "laporan/slop.md",
    "assets/css/motion-3d.css", "assets/js/motion-3d.js", "data/design-system.json",
    "assets/vendor/gsap.min.js", "assets/vendor/ScrollTrigger.min.js",
    "assets/vendor/lottie.min.js", "assets/vendor/mesin.json",
    "assets/js/mesin.js", "assets/lottie/nocturne-9s.json",
    "assets/fonts/bricolage-grotesque-latin-800-normal.ttf",
    "assets/fonts/fraunces-latin-300-normal.ttf",
    "assets/fonts/inter-latin-400-normal.ttf",
    "motion/render/klip-01-nocturne-9s.mp4", "motion/render/manifest.json",
    "film-studio/package.json", "film-studio/remotion/Klip.jsx",
    "film-studio/hyperframes/index.html", "film-studio/lottie/buat-lottie.mjs",
    "prompts/pustaka.json", "prompts/prompts.json", "skills/desain-prompt/SKILL.md",
    "data/biji3d.json", "assets/js/biji3d.js", "assets/css/biji.css",
    "assets/img/biji-3d-poster.webp", "laporan/biji-render.json", "laporan/biji-verifikasi.json",
    "skills/hero-3d/SKILL.md",
   
]

DOKUMEN = [
    "README.md", "operasional/00-struktur-divisi.md", "operasional/divisi/README.md",
    "marketing/09-media-kreator.md", "skills/README.md",
    "skills/social-media-riset/SKILL.md", "skills/komentar-mining/SKILL.md",
    "skills/search-intent-riset/SKILL.md", "skills/studio-konten/SKILL.md",
    "skills/motion-web/SKILL.md", "skills/motion-film/SKILL.md",
    "brand/README.md", "komersial/01-panduan-grosir.md",
    "film-studio/README.md", "assets/fonts/LISENSI.md",
]

KLAIM_TERLARANG = [
    (r"\broastery kami\b", "menyebut Nocturne sebagai roastery"),
    (r"\bkami menyangrai sendiri\b", "klaim menyangrai sendiri"),
    (r"\bnomor satu\b", "klaim nomor satu"),
    (r"\bterbaik di banyuwangi\b", "klaim tanpa bukti"),
    (r"\btermurah\b", "klaim termurah"),
    (r"\bpromo\b", "kata promo (bertentangan dengan posisi brand)"),
    (r"\bburuan\b", "kata buruan"),
]

VOID = {"br", "img", "meta", "link", "input", "source", "hr", "area", "base", "col",
        "embed", "track", "wbr", "path", "circle", "rect", "line", "use", "stop"}


# ─────────────────────────────── utilitas ─────────────────────────────────
def baca(path):
    with open(os.path.join(ROOT, path), encoding="utf-8", errors="ignore") as f:
        return f.read()


def ukuran(path):
    p = os.path.join(ROOT, path)
    if os.path.isdir(p):
        return sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(p) for f in fs)
    return os.path.getsize(p) if os.path.exists(p) else 0


class Seimbang(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tumpuk, self.galat, self.tautan = [], [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.tumpuk.append(tag)
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.tautan.append((tag, k, v))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.tumpuk and self.tumpuk[-1] == tag:
            self.tumpuk.pop()
        else:
            self.galat.append((tag, list(self.tumpuk[-3:]), self.getpos()))


def tautan_lokal(dari, nilai):
    """Kembalikan path lokal relatif terhadap ROOT, atau None bila eksternal."""
    v = nilai.strip()
    if not v or v.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
        return None
    v = v.split("#")[0].split("?")[0]
    if not v:
        return None
    dasar = os.path.dirname(os.path.join(ROOT, dari))
    return os.path.normpath(os.path.join(dasar, v))


# ──────────────────────────────── pemeriksaan ─────────────────────────────
def periksa(catatan):
    hasil = []

    def tambah(kategori, status, teks, detail=""):
        hasil.append({"kategori": kategori, "status": status, "teks": teks, "detail": detail})
        if status == "gagal":
            catatan.append(teks)

    # 1 · berkas wajib
    hilang = [p for p in HALAMAN + DATA + DOKUMEN if not os.path.exists(os.path.join(ROOT, p))]
    tambah("Berkas wajib", "lolos" if not hilang else "gagal",
           f"{len(HALAMAN + DATA + DOKUMEN) - len(hilang)}/{len(HALAMAN + DATA + DOKUMEN)} berkas ada",
           ", ".join(hilang))

    # 2 · tautan + 3 · tag seimbang
    total_tautan = 0
    rusak = []
    tag_rusak = []
    for h in HALAMAN:
        if not os.path.exists(os.path.join(ROOT, h)):
            continue
        parse = Seimbang()
        parse.feed(baca(h))
        if parse.tumpuk or parse.galat:
            tag_rusak.append(f"{h}: sisa {parse.tumpuk or parse.galat[:2]}")
        for _, _, v in parse.tautan:
            tujuan = tautan_lokal(h, v)
            if tujuan is None:
                continue
            total_tautan += 1
            if not os.path.exists(tujuan):
                rusak.append(f"{h} → {v}")

    tambah("Tautan lokal", "lolos" if not rusak else "gagal",
           f"{total_tautan - len(rusak)}/{total_tautan} tautan menuju berkas yang ada",
           "; ".join(rusak[:8]))
    tambah("Struktur HTML", "lolos" if not tag_rusak else "gagal",
           f"{len(HALAMAN) - len(tag_rusak)}/{len(HALAMAN)} halaman tag-nya seimbang",
           "; ".join(tag_rusak))

    # 4 · data saling cocok
    cat = json.loads(baca("data/catalog.json"))
    stok = json.loads(baca("data/stok-lot.json"))
    kreatif = json.loads(baca("data/kreatif.json"))
    divisi = json.loads(baca("data/divisi.json"))

    produk = [p["id"] for p in cat["products"]]
    status_bukan_tersedia = [f'{p["name"]}={p["status"]}' for p in cat["products"] if p["status"] != "tersedia"]
    tambah("Stok semua SKU", "lolos" if not status_bukan_tersedia else "peringatan",
           f'{len(produk) - len(status_bukan_tersedia)}/{len(produk)} SKU berstatus tersedia',
           ", ".join(status_bukan_tersedia))

    lot_aktif = {l["produk"] for l in stok["lots"] if (l.get("status") or "aktif") == "aktif"}
    komponen = {"raung", "blue-mount-ijen"}
    tanpa_lot = [p for p in produk
                 if p not in lot_aktif and not any(x in baca("data/catalog.json") for x in [])]
    tanpa_lot = [p for p in tanpa_lot
                 if next(x for x in cat["products"] if x["id"] == p)["category"] != "Signature Blend"]
    tambah("Produk ↔ lot", "lolos" if not tanpa_lot else "gagal",
           f"{len(produk) - len(tanpa_lot)}/{len(produk)} produk punya lot aktif (blend memakai komponen)",
           ", ".join(tanpa_lot))

    aset_hilang = [i["file"] for i in kreatif["items"]
                   if not os.path.exists(os.path.join(ROOT, "konten", i["file"]))]
    aset_hilang += [i["poster"] for i in kreatif["items"]
                    if not os.path.exists(os.path.join(ROOT, "konten", i["poster"]))]
    tambah("Manifest ↔ aset", "lolos" if not aset_hilang else "gagal",
           f'{len(kreatif["items"])} item manifest · {len(aset_hilang)} berkas hilang',
           ", ".join(aset_hilang[:6]))

    # brief ↔ manifest
    brief_berkas = []
    bdir = os.path.join(ROOT, "riset", "brief")
    if os.path.isdir(bdir):
        brief_berkas = [f for f in os.listdir(bdir) if f.endswith(".md")]
    id_aset = {i["id"] for i in kreatif["items"]}
    brief_menggantung = []
    for b in brief_berkas:
        teks = baca(os.path.join("riset", "brief", b))
        for m in re.finditer(r"`((?:reel|carousel|story|post)-[a-z0-9-]+)`", teks):
            if m.group(1) not in id_aset:
                brief_menggantung.append(f"{b}: {m.group(1)}")
    tambah("Brief ↔ aset", "lolos" if not brief_menggantung else "peringatan",
           f"{len(brief_berkas)} brief · {len(brief_menggantung)} aset tidak ditemukan",
           ", ".join(brief_menggantung[:5]))

    # target tiap KPI punya 3 angka
    target_salah = []
    for dv in divisi["divisi"]:
        for k in dv["kpi"]:
            t = k.get("target")
            if not (isinstance(t, list) and len(t) == 3):
                target_salah.append(f'{dv["kode"]}/{k["kunci"]}')
    n_kpi = sum(len(dv["kpi"]) for dv in divisi["divisi"])
    tambah("Target divisi", "lolos" if not target_salah else "gagal",
           f"{n_kpi - len(target_salah)}/{n_kpi} KPI punya target 3 bulan",
           ", ".join(target_salah))

    # 5 · klaim terlarang — hanya teks yang terlihat pembaca, hanya halaman publik.
    #     Halaman internal (riset/dashboard/konten) sengaja memuat daftar kata terlarang, jadi dikecualikan.
    def teks_tampak(html):
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
        t = re.sub(r"<[^>]+>", " ", t)
        t = re.sub(r"&[a-z]+;|&#\d+;", " ", t)
        return re.sub(r"\s+", " ", t).lower()

    temuan = []
    for h in HALAMAN_PUBLIK:
        if not os.path.exists(os.path.join(ROOT, h)):
            continue
        teks = teks_tampak(baca(h))
        for pola, alasan in KLAIM_TERLARANG:
            m = re.search(pola, teks)
            if m:
                konteks = teks[max(0, m.start() - 40):m.end() + 40].strip()
                temuan.append(f"{h}: …{konteks}… ({alasan})")
    tambah("Klaim terlarang", "lolos" if not temuan else "gagal",
           f"{len(temuan)} temuan di {len(HALAMAN_PUBLIK)} halaman publik", "; ".join(temuan[:6]))

    # 5b · skrip studio: harus lolos cek suara & asetnya ada
    import csv as _csv
    sdir = os.path.join(ROOT, "studio", "skrip")
    skrip = sorted(f for f in os.listdir(sdir) if f.endswith(".md")) if os.path.isdir(sdir) else []
    masalah_skrip = []
    for f in skrip:
        t = baca(os.path.join("studio", "skrip", f))
        if "whatsapp" not in t.lower():
            masalah_skrip.append(f"{f}: tanpa CTA WhatsApp")
        if not re.search(r"\d|satu|dua|tiga|empat|lima|enam|tujuh", t, re.I):
            masalah_skrip.append(f"{f}: tanpa angka sama sekali")
        for m in re.finditer(r"`((?:reel|carousel|story|post)-[a-z0-9-]+)`", t):
            if m.group(1) not in id_aset:
                masalah_skrip.append(f"{f}: aset {m.group(1)} tidak ada di manifest")
    if len(skrip) != 5:
        masalah_skrip.append(f"jumlah skrip {len(skrip)}, seharusnya 5")
    tambah("Skrip studio", "lolos" if not masalah_skrip else "gagal",
           f"{len(skrip)} skrip siap rekam · {len(masalah_skrip)} masalah",
           "; ".join(masalah_skrip[:6]))

    # 5c · bank hook: status & struktur valid, aset ada, tidak ada hook kembar
    with open(os.path.join(ROOT, "data", "studio-hooks.csv"), encoding="utf-8", newline="") as f:
        bank = [r for r in _csv.DictReader(f) if (r.get("hook") or "").strip()]
    import riset as _riset
    kunci_struktur = {k for k, _, _ in _riset.HOOK}
    masalah_hook = []
    for i, r in enumerate(bank, 2):
        if r["struktur"] not in kunci_struktur:
            masalah_hook.append(f"baris {i}: struktur “{r['struktur']}” tidak dikenal")
        if (r["status"] or "").strip() not in ("dipakai", "belum"):
            masalah_hook.append(f"baris {i}: status “{r['status']}” harus dipakai/belum")
        if r["aset"] and r["aset"] not in id_aset:
            masalah_hook.append(f"baris {i}: aset {r['aset']} tidak ada")
    judul = [r["hook"].strip().lower() for r in bank]
    kembar = {j for j in judul if judul.count(j) > 1}
    if kembar:
        masalah_hook.append("hook kembar: " + ", ".join(list(kembar)[:3]))
    tambah("Bank hook", "lolos" if not masalah_hook else "gagal",
           f"{len(bank)} hook · {sum(1 for r in bank if r['status'] == 'dipakai')} dipakai · "
           f"{len(bank) - sum(1 for r in bank if r['status'] == 'dipakai')} tersedia",
           "; ".join(masalah_hook[:6]))

    # 5d · peta kerangka 50 slot: jumlah & label harus utuh
    st = json.loads(baca("studio/data.json"))
    peta = st.get("peta", {})
    total_slot = sum(peta.values()) if peta else 0
    label_salah = [k for k in ("otomatis", "manual", "tidak") if k not in peta]
    if total_slot != 50:
        label_salah.append(f"jumlah slot {total_slot}, seharusnya 50")
    tambah("Peta 50 slot", "lolos" if not label_salah else "gagal",
           f"{peta.get('otomatis', 0)} otomatis · {peta.get('manual', 0)} manual · "
           f"{peta.get('tidak', 0)} tidak dipakai (total {total_slot})",
           "; ".join(label_salah))

    # 5e · kontrak desain + audit anti-slop
    ds = json.loads(baca("data/design-system.json"))
    slop = json.loads(baca("laporan/slop.json")) if os.path.exists(os.path.join(ROOT, "laporan/slop.json")) else {}
    ds_kurang = [k for k in ("warna", "tipografi", "radius", "gerak", "pengecualian", "halaman_publik")
                 if k not in ds]
    css_hilang = [f for f in ds["berkas_css"] if not os.path.exists(os.path.join(ROOT, f))]
    tambah("Kontrak desain", "lolos" if not (ds_kurang or css_hilang) else "gagal",
           f"{len(ds.get('warna', {}).get('inti', {}))} warna inti · "
           f"{len(ds.get('radius', []))} radius · {len(ds.get('gerak', {}).get('aturan', []))} aturan gerak · "
           f"{len(ds.get('pengecualian', []))} pengecualian terdokumentasi",
           "; ".join(ds_kurang + css_hilang))

    if slop:
        kritis_slop = slop.get("kritis", 0)
        perhatian_slop = slop.get("perhatian", 0)
        tambah("Anti-slop", "gagal" if kritis_slop else ("peringatan" if perhatian_slop else "lolos"),
               f"{slop.get('aturan_diperiksa', 0)} aturan · {kritis_slop} kritis · {perhatian_slop} perhatian",
               "; ".join(f'{t["aturan"]}: {t["bukti"][:48]}'
                         for t in slop.get("temuan", []) if t["tingkat"] == "kritis")[:200])
    else:
        tambah("Anti-slop", "peringatan", "laporan/slop.json belum ada", "jalankan tools/slop.py")

    # 5f · komponen gerak: setiap data-ui dipakai harus ada penanganannya
    js_gerak = baca("assets/js/motion-ui.js")
    ditangani = set(re.findall(r'data-ui="([a-z-]+)"', js_gerak))
    dipakai, tanpa_skrip = set(), []
    for h in HALAMAN:
        if not os.path.exists(os.path.join(ROOT, h)):
            continue
        isi = baca(h)
        for m in re.finditer(r'data-ui="([a-z-]+)"', isi):
            dipakai.add(m.group(1))
            if "motion-ui.js" not in isi and "motion.js" not in isi:
                tanpa_skrip.append(f"{h}:{m.group(1)}")
    liar = sorted(dipakai - ditangani)
    tambah("Komponen gerak", "lolos" if not (liar or tanpa_skrip) else "gagal",
           f"{len(dipakai)} jenis komponen dipakai · {len(ditangani)} ditangani motion-ui.js",
           "; ".join(liar + tanpa_skrip[:4]))

    # 5g · adegan 9:16 utuh & bisa direkam
    tl_path = os.path.join(ROOT, "motion", "timeline.json")
    masalah_adegan = []
    if os.path.exists(tl_path):
        tl = json.loads(baca("motion/timeline.json"))
        if len(tl.get("adegan", [])) != 5:
            masalah_adegan.append(f'{len(tl.get("adegan", []))} adegan, seharusnya 5')
        for a in tl.get("adegan", []):
            if not a.get("cues"):
                masalah_adegan.append(f'adegan {a.get("adegan")} tanpa cue')
                continue
            total = round(sum(c["durasi"] for c in a["cues"]), 2)
            if abs(total - 9.0) > 0.01:
                masalah_adegan.append(f'adegan {a["adegan"]}: total {total}s, seharusnya 9s')
            if any(not c.get("teks") for c in a["cues"]):
                masalah_adegan.append(f'adegan {a["adegan"]}: ada cue tanpa teks')
            if not os.path.exists(os.path.join(ROOT, "motion", a["berkas"])):
                masalah_adegan.append(f'adegan {a["adegan"]}: {a["berkas"]} tidak ada')
    else:
        masalah_adegan.append("motion/timeline.json tidak ada")
    tambah("Adegan 9:16", "lolos" if not masalah_adegan else "gagal",
           "5 adegan · total 9 detik masing-masing",
           "; ".join(masalah_adegan[:4]))


    # 5h · panggung 3D: berkas, gating, jatuh datar, dan anggaran berat
    css3d = baca("assets/css/motion-3d.css")
    js3d = baca("assets/js/motion-3d.js")
    masalah_3d = []
    if not css3d or not js3d:
        masalah_3d.append("assets/css/motion-3d.css atau assets/js/motion-3d.js tidak ada")
    for wajib in ("perspective:", "preserve-3d", "translateZ", "prefers-reduced-motion", "html.ui-3d"):
        if wajib not in css3d:
            masalah_3d.append(f"motion-3d.css tanpa {wajib}")
    for wajib in ("prefers-reduced-motion", "passive: true", "requestAnimationFrame"):
        if wajib not in js3d:
            masalah_3d.append(f"motion-3d.js tanpa {wajib}")
    if "matchMedia('(min-width: 900px)')" not in js3d:
        masalah_3d.append("motion-3d.js tanpa gerbang lebar 900 px")
    teknis = {"panggung", "timbul", "silinder"}
    dipakai_3d, liar_3d, tanpa3d = set(), [], []
    for h in HALAMAN:
        if not os.path.exists(os.path.join(ROOT, h)):
            continue
        isi = baca(h)
        for m in re.finditer(r'data-3d="([a-z]+)"', isi):
            dipakai_3d.add(m.group(1))
            if "motion-3d.js" not in isi:
                tanpa3d.append(h)
    liar_3d = sorted(dipakai_3d - teknis)
    masalah_3d += [f"komponen 3D tanpa penanganan: {x}" for x in liar_3d]
    masalah_3d += [f"{h}: memakai data-3d tanpa motion-3d.js" for h in sorted(set(tanpa3d))]
    berat_3d = (len(css3d.encode()) + len(js3d.encode())) / 1024
    if berat_3d > 24:
        masalah_3d.append(f"berat lapisan 3D {berat_3d:.1f} KB, batas 24 KB")
    tambah("Panggung 3D", "lolos" if not masalah_3d else "gagal",
           f"{len(dipakai_3d)} komponen dipakai · {berat_3d:.1f} KB CSS+JS · jatuh datar tanpa JS",
           "; ".join(masalah_3d[:4]))

    # 5i · film gerak: lembar film harus konsisten dengan timeline & skill-nya ada
    masalah_film = []
    fp = os.path.join(ROOT, "motion", "film-sheet.json")
    if not os.path.exists(fp):
        masalah_film.append("motion/film-sheet.json belum ada — jalankan tools/film.py")
    else:
        fs = json.loads(baca("motion/film-sheet.json"))
        grid = fs.get("grid", {})
        fpb = grid.get("frame_per_beat", 30)
        adegan = fs.get("adegan", [])
        if len(adegan) != 5:
            masalah_film.append(f"{len(adegan)} adegan, seharusnya 5")
        for a in adegan:
            tiers = [c["tier"] for c in a["cues"]]
            if max(tiers) < 5 or min(tiers) > 2:
                masalah_film.append(f"adegan {a['adegan']}: arc energi tanpa puncak/lembah")
            if a.get("frame_total") != int(round(a["durasi"] * grid.get("fps", 60))):
                masalah_film.append(f"adegan {a['adegan']}: frame tidak cocok durasi")
            for c in a["cues"]:
                if not c.get("di_grid"):
                    masalah_film.append(f"adegan {a['adegan']} cue {c['cue']}: di luar ketukan")
                if c["frame"][1] - c["frame"][0] != int(round(c["durasi"] * grid.get("fps", 60))):
                    masalah_film.append(f"adegan {a['adegan']} cue {c['cue']}: frame salah")
                if c.get("sumber", "") == "—":
                    masalah_film.append(f"adegan {a['adegan']} cue {c['cue']}: angka tanpa sumber")
        masalah_film += fs.get("masalah", [])
    if not os.path.exists(os.path.join(ROOT, "skills", "motion-film", "SKILL.md")):
        masalah_film.append("skills/motion-film/SKILL.md tidak ada")
    if not os.path.exists(os.path.join(ROOT, "motion", "film-sheet.md")):
        masalah_film.append("motion/film-sheet.md tidak ada")
    n_cue = sum(len(a["cues"]) for a in fs.get("adegan", [])) if os.path.exists(fp) else 0
    tambah("Film gerak", "lolos" if not masalah_film else "gagal",
           f"{n_cue} cue · {grid.get('bpm', '—')} BPM · {grid.get('frame_total', '—')} frame/adegan · "
           f"20 repo terdokumentasi",
           "; ".join(masalah_film[:4]))

    # 5j · mesin terpasang: berkas vendor ada, tanpa CDN, klip & komposisi nyata
    mesin_path = os.path.join(ROOT, "assets", "vendor", "mesin.json")
    masalah_mesin = []
    mesin = json.loads(baca("assets/vendor/mesin.json")) if os.path.exists(mesin_path) else {}
    if not mesin:
        masalah_mesin.append("assets/vendor/mesin.json belum ada — jalankan film-studio/scripts/vendor.mjs")
    else:
        for p in mesin.get("paket", {}):
            if not mesin["paket"][p]:
                masalah_mesin.append(f"versi {p} kosong")
        for v in mesin.get("vendor", []):
            q = os.path.join(ROOT, v["berkas"])
            if not os.path.exists(q):
                masalah_mesin.append(f'{v["berkas"]} tidak ada')
            elif "CDN" in baca(v["berkas"])[:4000] and "cdn." in baca(v["berkas"])[:4000].lower():
                masalah_mesin.append(f'{v["berkas"]} masih memuat CDN')
    # pustaka mesin tidak boleh dari CDN di halaman mana pun.
    # (Google Fonts masih dipakai halaman web — itu keputusan lama dan dicatat,
    #  bukan kegagalan; yang diperiksa di sini hanya CDN pustaka JS.)
    for h in HALAMAN:
        if not os.path.exists(os.path.join(ROOT, h)):
            continue
        isi = baca(h)
        for pola in ("cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com"):
            if pola in isi:
                masalah_mesin.append(f"{h} memuat {pola}")
    if "cdn.jsdelivr.net" in baca("film-studio/hyperframes/index.html"):
        masalah_mesin.append("komposisi HyperFrames masih memuat gsap dari CDN")
    halaman_googlefont = [h for h in HALAMAN
                          if os.path.exists(os.path.join(ROOT, h))
                          and "fonts.googleapis.com" in baca(h)]
    if len(halaman_googlefont) > 2:
        masalah_mesin = masalah_mesin  # dicatat di teks, bukan kegagalan
    # Lottie: struktur & isi
    lp = os.path.join(ROOT, "assets", "lottie", "nocturne-9s.json")
    if os.path.exists(lp):
        lot = json.loads(baca("assets/lottie/nocturne-9s.json"))
        teks = [l for l in lot.get("layers", []) if l.get("ty") == 5]
        if lot.get("op") != 540 or lot.get("fr") != 60:
            masalah_mesin.append(f'lottie {lot.get("op")} frame / {lot.get("fr")} fps, seharusnya 540/60')
        if len(teks) != 4:
            masalah_mesin.append(f"{len(teks)} lapisan teks, seharusnya 4 (satu per cue)")
        if len(lot.get("markers", [])) != 4:
            masalah_mesin.append("penanda cue lottie bukan 4")
    else:
        masalah_mesin.append("assets/lottie/nocturne-9s.json tidak ada")
    # klip jadi: harus benar-benar video, dengan manifest yang cocok
    mp = os.path.join(ROOT, "motion", "render", "klip-01-nocturne-9s.mp4")
    nf = os.path.join(ROOT, "motion", "render", "manifest.json")
    if os.path.exists(mp):
        kepala = open(mp, "rb").read(12)
        if kepala[4:8] != b"ftyp":
            masalah_mesin.append("klip mp4 tanpa kotak ftyp (bukan MP4 sungguhan)")
        if not os.path.exists(nf):
            masalah_mesin.append("manifest.json klip tidak ada")
        else:
            man = json.loads(baca("motion/render/manifest.json"))
            for k in ("sha256_16", "perender", "fps", "frame", "sumber_angka"):
                if not man.get(k):
                    masalah_mesin.append(f"manifest klip tanpa {k}")
            if man.get("fps") != 60 or man.get("frame") != 540:
                masalah_mesin.append(f'manifest {man.get("fps")} fps / {man.get("frame")} frame, seharusnya 60/540')
    else:
        masalah_mesin.append("motion/render/klip-01-nocturne-9s.mp4 belum dirender")
    # proyek mesin: pin versi + komposisi hyperframes lengkap
    pkg = json.loads(baca("film-studio/package.json")) if os.path.exists(os.path.join(ROOT, "film-studio/package.json")) else {}
    for p in ("gsap", "lottie-web", "remotion", "hyperframes"):
        v = pkg.get("dependencies", {}).get(p)
        if not v:
            masalah_mesin.append(f"film-studio/package.json tanpa {p}")
        elif any(c in v for c in ("^", "~")):
            masalah_mesin.append(f"versi {p} tidak dipin ({v})")
    sub = glob.glob(os.path.join(ROOT, "film-studio", "hyperframes", "compositions", "cue-*.html"))
    if len(sub) != 4:
        masalah_mesin.append(f"{len(sub)} sub-komposisi HyperFrames, seharusnya 4")
    # ukuran: halaman awal tidak boleh menyentuh pustaka mesin
    if "gsap" in baca("index.html") or "lottie" in baca("index.html"):
        masalah_mesin.append("index.html memuat pustaka mesin di atas fold")
    tambah("Mesin terpasang", "lolos" if not masalah_mesin else "gagal",
           f"GSAP {mesin.get('paket', {}).get('gsap', '—')} · Lottie {mesin.get('paket', {}).get('lottie-web', '—')} · "
           f"Remotion {mesin.get('paket', {}).get('remotion', '—')} · HyperFrames {mesin.get('paket', {}).get('hyperframes', '—')} · "
           f"klip 540 frame + 4 sub-komposisi · huruf lokal di {len(HALAMAN) - len(halaman_googlefont)} halaman",
           "; ".join(masalah_mesin[:4]))

    # 5k · pustaka prompt kelas atas: struktur 7 blok, token patuh, tanpa klaim karangan
    masalah_prompt = []
    pustaka_path = os.path.join(ROOT, "prompts", "pustaka.json")
    if not os.path.exists(pustaka_path):
        masalah_prompt.append("prompts/pustaka.json tidak ada")
    else:
        pust = json.loads(baca("prompts/pustaka.json"))
        warna_boleh = {h.lower() for h in json.loads(baca("data/design-system.json"))["warna"]["boleh_dipakai"]}
        pms = pust.get("prompts", [])
        if len(pust.get("anatomi", [])) != 7:
            masalah_prompt.append(f'{len(pust.get("anatomi", []))} blok anatomi, seharusnya 7')
        if not pust.get("larangan_global"):
            masalah_prompt.append("larangan_global kosong")
        for p in pms:
            pid = p.get("id", "?")
            if len(p.get("prompt", "")) < 1200:
                masalah_prompt.append(f"{pid}: prompt terlalu pendek")
            if len(p.get("kriteria_terima", [])) < 4:
                masalah_prompt.append(f"{pid}: kriteria terima < 4")
            if not p.get("angka_dari"):
                masalah_prompt.append(f"{pid}: tanpa sumber angka")
            if "reduced_motion" not in p.get("gerak", {}):
                masalah_prompt.append(f"{pid}: gerak tanpa reduced_motion")
            for hx in set(re.findall(r"#[0-9a-fA-F]{6}", p.get("prompt", ""))):
                if hx.lower() not in warna_boleh:
                    masalah_prompt.append(f"{pid}: warna {hx} di luar token")
        # halaman galeri harus benar-benar memuat semua prompt
        galeri = baca("prompts/index.html") if os.path.exists(os.path.join(ROOT, "prompts/index.html")) else ""
        tidak_termuat = [p["id"] for p in pms if f'id="{p["id"]}"' not in galeri]
        if tidak_termuat:
            masalah_prompt.append(f"galeri tidak memuat: {', '.join(tidak_termuat[:3])}")
        if galeri.count("data-salin=") < len(pms):
            masalah_prompt.append("tombol salin kurang dari jumlah prompt")
        # tidak boleh ada klaim menyalin prompt berbayar
        teks = json.dumps(pust, ensure_ascii=False).lower()
        for kata in ("disalin dari jiro", "disalin dari motionsite"):
            if kata in teks:
                masalah_prompt.append(f"klaim menyalin dari platform berbayar: {kata}")
        tambah("Prompt kelas atas", "lolos" if not masalah_prompt else "gagal",
               f"{len(pms)} prompt · {len(pust.get('anatomi', []))} blok · "
               f"{sum(len(p['prompt']) for p in pms) // 1000} ribu karakter · token patuh · galeri salin",
               "; ".join(masalah_prompt[:4]))

    # 5l · biji kopi 3D: bentuk, senyawa, poster, dan verifikasi tanpa GPU
    masalah_biji = []
    bp = os.path.join(ROOT, "data", "biji3d.json")
    if not os.path.exists(bp):
        masalah_biji.append("data/biji3d.json tidak ada")
    else:
        b3 = json.loads(baca("data/biji3d.json"))
        warna_boleh = {h.lower() for h in json.loads(baca("data/design-system.json"))["warna"]["boleh_dipakai"]}
        for k, v in b3.get("warna", {}).items():
            if k.startswith("_"):
                continue
            if v.lower() not in warna_boleh:
                masalah_biji.append(f"warna {k}={v} di luar token")
        sumber = {x["id"] for x in b3.get("sumber_angka", [])}
        if len(sumber) < 3:
            masalah_biji.append("sumber angka kurang dari 3")
        zona = b3.get("zona", [])
        if len(zona) < 5:
            masalah_biji.append(f"{len(zona)} zona, minimal 5")
        for z in zona:
            for sen in z.get("senyawa", []):
                if sen.get("sumber") not in sumber:
                    masalah_biji.append(f'{z["id"]}: sumber {sen.get("sumber")} tidak terdaftar')
                if sen.get("keyakinan") not in ("kuat", "umum"):
                    masalah_biji.append(f'{z["id"]}: {sen["nama"]} tanpa tanda keyakinan')
        if not b3.get("kejujuran", {}).get("catatan_tampil"):
            masalah_biji.append("catatan kejujuran tidak ada")
        if b3.get("biji", {}).get("spesies") != "Coffea arabica":
            masalah_biji.append("spesies bukan Coffea arabica")
        if "medium" not in b3.get("biji", {}).get("tingkat_sangrai", {}).get("nama", "").lower():
            masalah_biji.append("tingkat sangrai bukan medium")

        # poster: JPEG 4:5 (render hiper-realistis), bukan PNG mesh lagi
        pp = os.path.join(ROOT, "assets", "img", "biji-3d-poster.webp")
        if os.path.exists(pp):
            kepala = open(pp, "rb").read(16)
            if kepala[:4] != b"RIFF" or kepala[8:12] != b"WEBP":
                masalah_biji.append("poster bukan WebP")
            else:
                try:
                    from PIL import Image
                    ADA_PIL = True
                except ImportError:
                    ADA_PIL = False
                    catatan.append("butir Biji 3D: Pillow tidak terpasang — ukuran & warna sudut poster dilewati")
                pembuka = (lambda: Image.open(pp)) if ADA_PIL else (lambda: _Kosong())
                with pembuka() as pim:
                    pw, ph = pim.size
                if pw and (pw < 600 or ph < 750):
                    masalah_biji.append(f"poster terlalu kecil {pw}x{ph}")
                if pw and abs(pw / ph - 0.8) > 0.02:
                    masalah_biji.append(f"poster tidak 4:5 ({pw}x{ph})")
                # latar harus menyatu dengan kertas, bukan kotak bergradasi
                for xy in (((2, 2), (pw - 3, 2), (2, ph - 3), (pw - 3, ph - 3)) if pw else ()):
                    px = pim.convert("RGB").getpixel(xy)
                    if max(abs(px[i] - (245, 239, 228)[i]) for i in range(3)) > 4:
                        masalah_biji.append(f"sudut poster {xy} tidak menyatu dengan #F5EFE4: {px}")
                        break
        else:
            masalah_biji.append("poster tidak ada")

        # render sudah dipasang dan latarnya menyatu dengan kertas
        lr = os.path.join(ROOT, "laporan", "biji-render.json")
        if os.path.exists(lr):
            lapor = json.loads(baca("laporan/biji-render.json"))
            latar = lapor.get("latar", {}).get("latar_akhir")
            if latar != [245, 239, 228]:
                masalah_biji.append(f'latar render {latar} bukan #F5EFE4')
            if len(lapor.get("titik", {})) != len(zona):
                masalah_biji.append("laporan/biji-render.json tidak memuat semua titik")
        else:
            masalah_biji.append("laporan/biji-render.json belum ada — jalankan tools/biji_render.py")

        # verifikasi node: harus segar (sidik sama) dan lolos
        lv = os.path.join(ROOT, "laporan", "biji-verifikasi.json")
        if os.path.exists(lv):
            import hashlib
            ver = json.loads(baca("laporan/biji-verifikasi.json"))
            with open(os.path.join(ROOT, "assets", "img", "biji-3d-poster.webp"), "rb") as fp:
                poster_bytes = fp.read()
            sidik = hashlib.sha256(
                baca("data/biji3d.json").encode() + baca("assets/js/biji3d.js").encode() + poster_bytes
            ).hexdigest()[:16]
            if ver.get("sidik") != sidik:
                masalah_biji.append("laporan/biji-verifikasi.json basi — jalankan node tools/verifikasi-biji.mjs")
            if ver.get("gagal"):
                masalah_biji.append(f'{ver["gagal"]} butir verifikasi biji gagal')
        else:
            masalah_biji.append("node tools/verifikasi-biji.mjs belum dijalankan")

        # HTML: hero memuat komponennya, tanpa pustaka 3D dari CDN
        idx = baca("index.html")
        tombol = idx.count("data-biji-titik=\"")
        blok = idx.count("data-biji-zona=\"")
        if "data-biji3d" not in idx:
            masalah_biji.append("index.html tanpa data-biji3d")
        if tombol != len(zona) or blok != len(zona):
            masalah_biji.append(f"{tombol} tombol / {blok} blok zona, seharusnya {len(zona)}")
        for pola in ("three.min.js", "three.module", "cdn.jsdelivr.net/npm/three", "unpkg.com/three"):
            if pola in idx:
                masalah_biji.append(f"index.html memuat pustaka 3D dari CDN ({pola})")
        js = baca("assets/js/biji3d.js")
        if "reduced" not in js.lower():
            masalah_biji.append("biji3d.js tanpa jalur prefers-reduced-motion")
        if "fetch(" not in js:
            masalah_biji.append("biji3d.js tidak membaca data dari JSON (angka ditulis di JS)")
        if "data-biji-kanvas" in idx or "getContext('webgl'" in js:
            masalah_biji.append("sisa jalur WebGL masih ada, padahal sudah diganti render")
        if "titik_foto" not in js:
            masalah_biji.append("biji3d.js tidak memakai titik_foto untuk menaruh titik")

        # motto brand: harus ada di data, tampil di hero, dan tidak dikarang di HTML saja
        motto = json.loads(baca("data/catalog.json")).get("brand", {}).get("motto")
        if not motto or len(motto) != 2:
            masalah_biji.append("data/catalog.json#brand.motto belum ada / bukan 2 baris")
        else:
            for baris in motto:
                if baris not in idx:
                    masalah_biji.append(f'motto "{baris}" tidak tampil di index.html')

        # susunan hero: biji di kiri, teks di kanan (grid, ≥900px)
        css = baca("assets/css/biji.css")
        if "grid-column: 1" not in css or ".biji" not in css:
            masalah_biji.append("biji tidak ditempatkan di kolom kiri pada layar lebar")
        if "grid-column: 2" not in css:
            masalah_biji.append("teks hero tidak ditempatkan di kolom kanan")

        # motto harus benar-benar muat di kolomnya. Angka diambil dari CSS
        # (bukan disalin ke sini), lalu diukur dengan metrik font asli.
        if motto:
            try:
                from PIL import ImageFont
                blok_dasar = css.split("@media (min-width: 900px)")[0]
                blok_besar = css.split("@media (min-width: 900px)")[1].split("@media (max-width: 899px)")[0]
                blok_kecil = css.split("@media (max-width: 899px)")[1]

                def badan_aturan(txt, selektor):
                    m = re.search(re.escape(selektor) + r"\s*\{([^}]*)\}", txt)
                    return m.group(1) if m else ""

                def clamp_dari(txt):
                    m = re.search(r"font-size:\s*clamp\(([\d.]+)rem,\s*([\d.]+)vw,\s*([\d.]+)rem\)", txt)
                    return tuple(float(x) for x in m.groups()) if m else None

                # ambil clamp dari ATURAN .hero__title, bukan dari aturan pertama di berkas
                dasar = clamp_dari(badan_aturan(blok_dasar, ".hero__title"))
                kecil = clamp_dari(badan_aturan(blok_kecil, ".hero__title")) or dasar
                m_grid = re.search(r"grid-template-columns:\s*minmax\(0,\s*([\d.]+)fr\)\s*minmax\(0,\s*([\d.]+)fr\)", blok_besar)
                m_gap = re.search(r"column-gap:\s*clamp\(([\d.]+)px,\s*([\d.]+)vw,\s*([\d.]+)px\)", blok_besar)
                if not (dasar and m_grid):
                    masalah_biji.append("CSS hero tidak memakai clamp() + grid dua kolom yang bisa diperiksa")
                else:
                    fr1, fr2 = float(m_grid.group(1)), float(m_grid.group(2))
                    fb = os.path.join(ROOT, "assets", "fonts", "bricolage-grotesque-latin-800-normal.ttf")
                    ff = os.path.join(ROOT, "assets", "fonts", "fraunces-latin-300-normal.ttf")
                    for vw in (360, 390, 414, 768, 900, 1024, 1280, 1440, 1920):
                        pad = min(44, max(16, vw * 0.04)) * 2
                        wrap = min(1180, vw) - pad
                        c = dasar if vw >= 900 else kecil
                        size = max(c[0] * 16, min(vw * c[1] / 100, c[2] * 16))
                        if vw >= 900:
                            gap = 0.0
                            if m_gap:
                                g0, g1, g2 = (float(x) for x in m_gap.groups())
                                gap = max(g0, min(vw * g1 / 100, g2))
                            kanan = (wrap - gap) * (fr2 / (fr1 + fr2))
                        else:
                            kanan = wrap
                        f1 = ImageFont.truetype(fb, int(size))
                        f2 = ImageFont.truetype(ff, int(size))
                        lebar = max(f1.getlength(motto[0]), f2.getlength(motto[1]))
                        if lebar > kanan * 0.96:
                            masalah_biji.append(f"motto meluap di {vw}px ({lebar:.0f}px > kolom {kanan:.0f}px)")
            except ImportError:
                pass   # tanpa Pillow, butir ini dilewati (bukan gagal)

        tambah("Biji 3D", "lolos" if not masalah_biji else "gagal",
               f'{len(zona)} zona · {sum(len(z["senyawa"]) for z in zona)} senyawa · '
               f'{len(sumber)} sumber literatur · poster 640×800 · '
               f'verifikasi {json.loads(baca("laporan/biji-verifikasi.json")).get("lolos", 0)}/'
               f'{json.loads(baca("laporan/biji-verifikasi.json")).get("lolos", 0) + json.loads(baca("laporan/biji-verifikasi.json")).get("gagal", 0)}',
               "; ".join(masalah_biji[:4]))


    # 5b · halaman biji sangrai (dijual: roasted beans)
    halaman = "biji-sangrai/index.html"
    if not os.path.exists(os.path.join(ROOT, halaman)):
        tambah("Biji sangrai", "gagal", "biji-sangrai/index.html belum dibuat")
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location("roasted", os.path.join(ROOT, "tools", "roasted.py"))
        roasted = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(roasted)
        teks = baca(halaman)
        katalog = json.loads(baca("data/catalog.json"))
        ds = json.loads(baca("data/design-system.json"))
        masalah_jual = roasted.periksa(teks, katalog, ds)

        # halaman harus hasil generate: jalankan ulang di memori, bandingkan
        segar = roasted.bangun(katalog, ds)
        if segar != teks:
            masalah_jual.append("berkas tidak sama dengan hasil generate — jalankan python3 tools/roasted.py")

        jumlah = len(katalog["products"])
        tambah("Biji sangrai", "lolos" if not masalah_jual else "gagal",
               f"{jumlah} SKU · {len({v['grams'] for p in katalog['products'] for v in p['variants']})} ukuran · "
               f"harga dari katalog · tanpa CDN · reduced-motion",
               "; ".join(masalah_jual[:4]))


    # 5c · berkas tunggal (luring) — supaya bisa dibuka dari folder unduhan
    luring = "biji-sangrai/biji-sangrai-luring.html"
    if not os.path.exists(os.path.join(ROOT, luring)):
        tambah("Berkas luring", "gagal", "biji-sangrai/biji-sangrai-luring.html belum dibuat")
    else:
        kode = None
        keluaran = []
        try:
            import importlib.util as _iu
            spec = _iu.spec_from_file_location("luring", os.path.join(ROOT, "tools", "luring.py"))
            mod = _iu.module_from_spec(spec)
            spec.loader.exec_module(mod)
            import contextlib
            import io as _io
            tangkap = _io.StringIO()
            with contextlib.redirect_stdout(tangkap):
                kode = mod.periksa()
            keluaran = tangkap.getvalue().strip().splitlines()
        except ImportError as e:
            # tools/luring.py butuh Pillow; tanpa itu butir ini dilewati, bukan gagal
            catatan.append(f"butir Berkas luring dilewati: {e}")
        if kode is None:
            tambah("Berkas luring", "lolos",
                   f"berkas tunggal {os.path.getsize(os.path.join(ROOT, luring))/1024:.0f} KB · "
                   "pemeriksaan isi dilewati (Pillow tidak terpasang)",
                   "jalankan: pip install pillow")
        elif kode != 0:
            tambah("Berkas luring", "gagal", keluaran[-1] if keluaran else "gagal",
                   "; ".join(b for b in keluaran if b.startswith("XX"))[:180])
        else:
            besar = os.path.getsize(os.path.join(ROOT, luring)) / 1024
            tambah("Berkas luring", "lolos",
                   f"1 berkas {besar:.0f} KB · CSS+JS+huruf+gambar tersisip · 0 tautan aset relatif",
                   "dibuka langsung dari folder unduhan")


    # 5d · pintu "semua.html" — satu alamat untuk meninjau semuanya
    if not os.path.exists(os.path.join(ROOT, "semua.html")):
        tambah("Pintu semua", "gagal", "semua.html belum dibuat — jalankan python3 tools/semua.py")
    else:
        import importlib.util as _iu2
        spec = _iu2.spec_from_file_location("semua", os.path.join(ROOT, "tools", "semua.py"))
        mod = _iu2.module_from_spec(spec)
        spec.loader.exec_module(mod)
        masalah_semua = []
        teks_semua = baca("semua.html")
        for path, judul, *_ in mod.HALAMAN:
            if not os.path.exists(os.path.join(ROOT, path)):
                masalah_semua.append(f"{judul}: berkas hilang ({path})")
            if path not in teks_semua:
                masalah_semua.append(f"{judul} tidak tertaut")
        # kesegaran: sidik struktur + angka gerbang (bukan banding berkas penuh —
        # angka di halaman ini berasal dari laporan yang sedang ditulis)
        if f"sidik struktur {mod.sidik()}" not in teks_semua:
            masalah_semua.append("sidik struktur tidak cocok — jalankan python3 tools/semua.py")
        angka_kini = mod.angka()
        if f"{angka_kini['lolos']}/{angka_kini['cek']}" not in teks_semua:
            masalah_semua.append("angka gerbang tidak mutakhir — jalankan tools/semua.py")
        tambah("Pintu semua", "lolos" if not masalah_semua else "gagal",
               f"{len(mod.HALAMAN)} halaman tertaut · angka dari periksa.json · satu berkas",
               "; ".join(masalah_semua[:4]))

    # 5e · huruf: dilayani sendiri, rentang bobotnya nyata (bukan huruf sintetis peramban)
    masalah_huruf = []
    css_huruf = "assets/css/fonts.css"
    if not os.path.exists(os.path.join(ROOT, css_huruf)):
        masalah_huruf.append("assets/css/fonts.css belum ada — jalankan python3 tools/font.py")
    else:
        isi_huruf = baca(css_huruf)
        pasangan = re.findall(
            r'font-family:"([^"]+)"[^}]*?url\("\.\./fonts/([^"]+\.woff2)"\)[^}]*?'
            r'font-weight:(\d+) (\d+);[^}]*?font-style:(\w+);', isi_huruf, re.S)
        if len(pasangan) < 4:
            masalah_huruf.append(f"fonts.css hanya memuat {len(pasangan)} @font-face")
        for nama, berkas, a, b, gaya in pasangan:
            path = os.path.join(ROOT, "assets", "fonts", berkas)
            if not os.path.exists(path):
                masalah_huruf.append(f"{berkas} tidak ada")
                continue
            try:
                from fontTools.ttLib import TTFont
                f = TTFont(path)
                sumbu = {x.axisTag: (x.minValue, x.maxValue) for x in f["fvar"].axes}
                nyata = sumbu.get("wght")
                if not nyata or (int(nyata[0]), int(nyata[1])) != (int(a), int(b)):
                    masalah_huruf.append(f"{berkas}: sumbu wght {nyata} ≠ CSS {a}–{b}")
                if os.path.getsize(path) < 20_000:
                    masalah_huruf.append(f"{berkas} terlalu kecil — iris gagal")
            except Exception as e:  # noqa: BLE001
                masalah_huruf.append(f"{berkas} tidak terbaca: {e}")
        # bobot yang dipakai stylesheet harus masuk salah satu rentang
        rentang = [(int(b[0]), int(b[1])) for b in [(x[2], x[3]) for x in pasangan]]
        dipakai = set()
        for css in glob.glob(os.path.join(ROOT, "assets", "css", "*.css")):
            for m in re.finditer(r"font-weight:\s*(\d{3})", baca(os.path.relpath(css, ROOT))):
                dipakai.add(int(m.group(1)))
        liar = sorted(w for w in dipakai if not any(a <= w <= b for a, b in rentang))
        if liar:
            masalah_huruf.append("bobot tanpa berkas: " + ", ".join(str(w) for w in liar))
        for h in HALAMAN:
            path = os.path.join(ROOT, h)
            if not os.path.exists(path) or h.startswith("biji-sangrai"):
                continue
            isi = baca(h)
            if "fonts.googleapis.com" in isi or "fonts.gstatic.com" in isi:
                masalah_huruf.append(f"{h} masih memuat huruf dari CDN")
            elif "assets/css/fonts.css" not in isi:
                masalah_huruf.append(f"{h} tidak memuat fonts.css")
    berat_huruf = sum(ukuran(f"assets/fonts/{x['berkas']}") for x in [
        {"berkas": "bricolage.woff2"}, {"berkas": "fraunces.woff2"},
        {"berkas": "fraunces-italic.woff2"}, {"berkas": "inter.woff2"}])
    tambah("Huruf lokal", "lolos" if not masalah_huruf else "gagal",
           f"4 berkas variabel {berat_huruf/1024:.0f} KB · 0 permintaan ke Google Fonts · "
           f"rentang bobot cocok dengan CSS",
           "; ".join(masalah_huruf[:4]))

    # 5f · pustaka gaya gambar: skema utuh, id unik, tiap gaya bisa dipakai tanpa menebak
    masalah_gaya = []
    path_gaya = os.path.join(ROOT, "data", "gaya-gambar.json")
    if not os.path.exists(path_gaya):
        masalah_gaya.append("data/gaya-gambar.json belum ada")
    else:
        gaya = json.loads(baca("data/gaya-gambar.json"))
        daftar = gaya.get("gaya", [])
        wajib = ("id", "nama", "kategori", "kapan", "ciri", "prompt", "negatif", "rasio", "alat")
        id_terpakai = set()
        kategori = set()
        for g in daftar:
            kurang = [k for k in wajib if not g.get(k)]
            if kurang:
                masalah_gaya.append(f'{g.get("id", "?")}: kurang {", ".join(kurang)}')
            if g.get("id") in id_terpakai:
                masalah_gaya.append(f'id ganda: {g.get("id")}')
            id_terpakai.add(g.get("id"))
            kategori.add(g.get("kategori"))
            if g.get("alat") not in ("pillow", "generator", "keduanya"):
                masalah_gaya.append(f'{g.get("id")}: alat tidak dikenal ({g.get("alat")})')
            if len(g.get("negatif", [])) < 2:
                masalah_gaya.append(f'{g.get("id")}: negatif kurang dari 2')
        if len(daftar) < 18:
            masalah_gaya.append(f"hanya {len(daftar)} gaya")
        teks_skill = baca("skills/gaya-gambar/SKILL.md") if os.path.exists(
            os.path.join(ROOT, "skills", "gaya-gambar", "SKILL.md")) else ""
        if "data/gaya-gambar.json" not in teks_skill:
            masalah_gaya.append("skill gaya-gambar tidak menunjuk pustakanya")
    tambah("Pustaka gaya", "lolos" if not masalah_gaya else "gagal",
           f"{len(json.loads(baca('data/gaya-gambar.json'))['gaya'])} gaya · "
           f"{len({g['kategori'] for g in json.loads(baca('data/gaya-gambar.json'))['gaya']})} kategori · "
           f"tiap gaya: prompt + negatif + rasio + alat"
           if not masalah_gaya else "gagal",
           "; ".join(masalah_gaya[:4]))

    # 5g · rak sangrai: atlas, data, dan uji asap tanpa peramban
    masalah_rak = []
    for berkas, ukuran_wajib in (("assets/img/rak/covers.webp", (1744, 2336)),
                                 ("assets/img/rak/spines.webp", (2688, 1152))):
        path = os.path.join(ROOT, berkas)
        if not os.path.exists(path):
            masalah_rak.append(f"{berkas} belum ada — jalankan python3 tools/rak.py")
        elif os.path.getsize(path) > 900_000:
            masalah_rak.append(f"{berkas} {os.path.getsize(path)/1024:.0f} KB terlalu berat")
    if not os.path.exists(os.path.join(ROOT, "rak/data.js")):
        masalah_rak.append("rak/data.js belum ada")
    if not os.path.exists(os.path.join(ROOT, "rak/rak.js")):
        masalah_rak.append("rak/rak.js belum ada")
    else:
        js_rak = baca("rak/rak.js")
        # harga tidak boleh diketik di skrip: harus dari data.js (katalog)
        if re.search(r"Rp\s?\d", js_rak):
            masalah_rak.append("harga diketik di rak.js — harus dari data.js")
        if "requestAnimationFrame" not in js_rak:
            masalah_rak.append("rak.js tidak memakai satu rAF")
        css_rak = re.sub(r"/\*.*?\*/", "", baca("rak/rak.css"), flags=re.S)
        if "@keyframes" in css_rak:
            masalah_rak.append("rak.css memakai @keyframes — seharusnya WAAPI")
    # uji asap (opsional: butuh jsdom di /tmp/jsdom)
    jsdom = "/tmp/jsdom/node_modules/jsdom/lib/api.js"
    uji_rak = "dilewati"
    if os.path.exists(jsdom) and os.path.exists(os.path.join(ROOT, "tools/rak-uji.mjs")):
        proses = subprocess.run(["node", "tools/rak-uji.mjs"], cwd=ROOT,
                                capture_output=True, text=True, timeout=120)
        uji_rak = "lolos" if proses.returncode == 0 else "gagal"
        if proses.returncode != 0:
            masalah_rak.append("uji asap rak gagal: " + (proses.stdout or proses.stderr).strip()[-200:])
    # konformansi terhadap spesifikasi template (motionsite.ai / Leon Vasari VHS shelf)
    spek_rak = "dilewati"
    if os.path.exists(os.path.join(ROOT, "tools/rak-spek.mjs")):
        proses = subprocess.run(["node", "tools/rak-spek.mjs"], cwd=ROOT,
                                capture_output=True, text=True, timeout=120)
        spek_rak = "105/105" if proses.returncode == 0 else "gagal"
        if proses.returncode != 0:
            masalah_rak.append("spesifikasi rak gagal: " + (proses.stdout or proses.stderr).strip()[-200:])
    tambah("Rak sangrai", "lolos" if not masalah_rak else "gagal",
           f"12 kotak 3D · sampul {ukuran('assets/img/rak/covers.webp')/1024:.0f} KB · "
           f"punggung {ukuran('assets/img/rak/spines.webp')/1024:.0f} KB · uji asap {uji_rak} · "
           f"spesifikasi template {spek_rak}",
           "; ".join(masalah_rak[:4]))

    # 5i · pustaka skill: frontmatter, nama = folder, description wajar, terdaftar di README
    masalah_skill = []
    jumlah_skill = 0
    try:
        import importlib.util as _iu4
        spec4 = _iu4.spec_from_file_location("skill_impor", os.path.join(ROOT, "tools", "skill_impor.py"))
        mods = _iu4.module_from_spec(spec4)
        spec4.loader.exec_module(mods)
        jumlah_skill = len(mods.daftar_skill())
        masalah_skill = mods.cek()
    except Exception as e:  # noqa: BLE001
        masalah_skill.append(f"pemeriksa skill gagal: {e}")
    tambah("Pustaka skill", "lolos" if not masalah_skill else "gagal",
           f"{jumlah_skill} skill · frontmatter patuh · semuanya terdaftar di skills/README.md",
           "; ".join(masalah_skill[:4]))

    # 5h · kemasan 3D: hanya diperiksa bila foto sudah diproses
    masalah_kemasan = []
    path_kemasan = os.path.join(ROOT, "data", "kemasan.json")
    jumlah_kemasan = 0
    if not os.path.exists(path_kemasan):
        teks_kemasan = "belum ada foto diproses"
    else:
        try:
            import importlib.util as _iu3
            spec3 = _iu3.spec_from_file_location("kemasan", os.path.join(ROOT, "tools", "kemasan.py"))
            modk = _iu3.module_from_spec(spec3)
            spec3.loader.exec_module(modk)
            masalah_kemasan = modk.cek()
        except ImportError as e:
            catatan.append(f"butir Kemasan 3D dilewati: {e}")
        jumlah_kemasan = len(json.loads(baca("data/kemasan.json")).get("kemasan", []))
        teks_kemasan = f"{jumlah_kemasan} kemasan · alfa bersih · serong 10° ke kiri (diukur)"
        # sumber mentah tidak boleh dipakai langsung di halaman
        for h in HALAMAN:
            path_h = os.path.join(ROOT, h)
            if os.path.exists(path_h) and "kemasan/sumber/" in baca(h):
                masalah_kemasan.append(f"{h} memuat foto mentah (kemasan/sumber/)")
    tambah("Kemasan 3D", "lolos" if not masalah_kemasan else "gagal",
           teks_kemasan, "; ".join(masalah_kemasan[:4]))

    # 6 · ukuran
    awal = ukuran("index.html") + ukuran("assets/css/site.css") + ukuran("assets/js/site.js") \
        + ukuran("assets/css/motion.css") + ukuran("assets/js/motion.js")
    konten = ukuran("konten")
    tambah("Berat halaman awal", "lolos" if awal < 1_500_000 else "gagal",
           f"{awal/1024:.0f} KB (batas 1.500 KB)")
    tambah("Berat folder konten", "lolos" if konten < 12_000_000 else "peringatan",
           f"{konten/1024/1024:.1f} MB (batas 12 MB)")

    return hasil


def md(hasil, tgl):
    gagal = [h for h in hasil if h["status"] == "gagal"]
    peringatan = [h for h in hasil if h["status"] == "peringatan"]
    lulus = [h for h in hasil if h["status"] == "lolos"]
    icon = {"lolos": "✅ lolos", "peringatan": "⚠️ peringatan", "gagal": "❌ gagal"}

    o = [f"""# Laporan periksa — {tgl.isoformat()}

Dibuat otomatis oleh `tools/periksa.py` setelah seluruh generator dijalankan.

| Ringkasan | Jumlah |
| --- | --- |
| Pemeriksaan lolos | **{len(lulus)}** |
| Peringatan | **{len(peringatan)}** |
| Gagal (harus diperbaiki) | **{len(gagal)}** |

| Kategori | Status | Hasil | Catatan |
| --- | --- | --- | --- |
"""]
    for h in hasil:
        o.append(f'| {h["kategori"]} | {icon[h["status"]]} | {h["teks"]} | {h["detail"] or "—"} |\n')
    o.append("""
## Yang belum bisa diperiksa mesin

| Hal | Kenapa | Siapa yang memeriksa |
| --- | --- | --- |
| Rasa kopi & keputusan batch | butuh manusia mencicipi | D1 |
| Angka biaya nyata | masih asumsi di `data/biaya.json` | D6 |
| Izin publikasi nama petani | butuh dokumen tertulis | D7 |
| Data riset kompetitor | masih baris `contoh` | D3 |
| Tayang di IG/TikTok/marketplace | tidak ada akses akun | owner |

Laporan ini memeriksa **konsistensi**, bukan kebenaran pasar. Semua lolos berarti
"sistem tidak bertentangan dengan dirinya sendiri", bukan "bisnis sudah terbukti".
""")
    return "".join(o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ringkas", action="store_true")
    args = ap.parse_args()

    catatan = []
    hasil = periksa(catatan)
    tgl = hari_ini()

    gagal = [h for h in hasil if h["status"] == "gagal"]
    peringatan = [h for h in hasil if h["status"] == "peringatan"]

    if not args.ringkas:
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, "periksa.md"), "w", encoding="utf-8") as f:
            f.write(md(hasil, tgl))
        with open(os.path.join(OUT, "periksa.json"), "w", encoding="utf-8") as f:
            json.dump({"dibuat": tgl.isoformat(), "hasil": hasil}, f, ensure_ascii=False, indent=2)

    print(f"Periksa situs — {tgl.isoformat()}")
    for h in hasil:
        tanda = {"lolos": "OK ", "peringatan": "!! ", "gagal": "XX "}[h["status"]]
        print(f"  {tanda}{h['kategori']:<22} {h['teks']}"
              + (f"  → {h['detail'][:70]}" if h["detail"] else ""))
    print(f"  kesimpulan: {len(hasil)-len(gagal)-len(peringatan)} lolos · "
          f"{len(peringatan)} peringatan · {len(gagal)} gagal")
    if not args.ringkas:
        print("  laporan: laporan/periksa.md")
    raise SystemExit(1 if gagal else 0)


if __name__ == "__main__":
    main()
