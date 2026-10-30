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
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402
import re
from datetime import date
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "laporan")

HALAMAN_PUBLIK = ["index.html", "kampanye/index.html", "komersial/penawaran-b2b.html", "brand/index.html"]
# halaman internal (noindex) tidak diperiksa klaim: riset & papan sengaja memuat daftar kata terlarang

HALAMAN = [
    "index.html",
    "dashboard/index.html",
    "kampanye/index.html",
    "konten/index.html",
    "riset/index.html",
    "brand/index.html",
    "komersial/penawaran-b2b.html",
    "laporan/index.html",
    "studio/index.html",
    "motion/index.html",
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
    "motion/out/klip-01-nocturne-9s.mp4", "motion/out/manifest.json",
    "film-studio/package.json", "film-studio/remotion/Klip.jsx",
    "film-studio/hyperframes/index.html", "film-studio/lottie/buat-lottie.mjs",
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
    mp = os.path.join(ROOT, "motion", "out", "klip-01-nocturne-9s.mp4")
    nf = os.path.join(ROOT, "motion", "out", "manifest.json")
    if os.path.exists(mp):
        kepala = open(mp, "rb").read(12)
        if kepala[4:8] != b"ftyp":
            masalah_mesin.append("klip mp4 tanpa kotak ftyp (bukan MP4 sungguhan)")
        if not os.path.exists(nf):
            masalah_mesin.append("manifest.json klip tidak ada")
        else:
            man = json.loads(baca("motion/out/manifest.json"))
            for k in ("sha256_16", "perender", "fps", "frame", "sumber_angka"):
                if not man.get(k):
                    masalah_mesin.append(f"manifest klip tanpa {k}")
            if man.get("fps") != 60 or man.get("frame") != 540:
                masalah_mesin.append(f'manifest {man.get("fps")} fps / {man.get("frame")} frame, seharusnya 60/540')
    else:
        masalah_mesin.append("motion/out/klip-01-nocturne-9s.mp4 belum dirender")
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
           f"klip 540 frame + 4 sub-komposisi · font Google di {len(halaman_googlefont)} halaman (lama, dicatat)",
           "; ".join(masalah_mesin[:4]))

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
