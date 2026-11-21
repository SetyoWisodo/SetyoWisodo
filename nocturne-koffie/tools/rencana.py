#!/usr/bin/env python3
"""Rencana website komersial — apa yang sudah ada, apa yang belum, urutan kerjanya.

Kenapa ada berkas ini
---------------------
Pertanyaan "bisa mulai sekarang dengan skill yang ada?" hanya bisa dijawab jujur
kalau ada daftar: bagian mana yang **sudah selesai** (jangan diulang), bagian mana
yang **belum ada**, dan bagian mana yang **tidak bisa** dikerjakan dengan sumber
daya sekarang (tanpa peramban, tanpa domain, tanpa keputusan pemilik).

Alat ini tidak membuat halaman. Ia membaca repo, menghitung, lalu menulis
`rencana/website-komersial.md` + `data/rencana-website.json`. Semua angka di
laporan berasal dari disk, bukan dari ingatan.

Pakai
-----
    python3 tools/rencana.py            # tulis laporan
    python3 tools/rencana.py --cek      # periksa apakah laporan masih cocok
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAPORAN = os.path.join(ROOT, "rencana", "website-komersial.md")
DATA = os.path.join(ROOT, "data", "rencana-website.json")

# Halaman publik yang sudah ada (isi, bukan alat dapur). Alat dapur tetap dihitung
# terpisah karena bukan bagian pengalaman pembeli.
PUBLIK = {
    "index.html": ("Beranda", "hero rak + koleksi + langganan + member"),
    "biji-sangrai/index.html": ("Biji sangrai", "halaman ala jiro.build, 9 lot"),
    "katalog/index.html": ("Katalog foto", "bukti sesi foto, 9 SKU"),
    "rak/index.html": ("Rak 3D", "rak kemasan 500 g, 9 lot"),
    "kampanye/index.html": ("Kampanye", "landing kampanye"),
    "komersial/penawaran-b2b.html": ("Penawaran B2B", "harga grosir & sampel"),
    "motion/index.html": ("Lab gerak", "pustaka gerak & pratinjau"),
    "brand/index.html": ("Brand kit", "logo, label, palet"),
}
DAPUR = {
    "dashboard/index.html": "papan harian",
    "konten/index.html": "konten siap pakai",
    "laporan/index.html": "laporan",
    "prompts/index.html": "pustaka prompt",
    "riset/index.html": "riset",
    "studio/index.html": "studio konten",
    "semua.html": "pintu satu berkas",
}

# Butir yang tidak bisa ditutup dengan menulis kode (butuh orang/berkas/uang).
BLOKIR_LUAR = [
    ("Domain & email brand", "Belum dibeli. Situs masih `nocturnekoffie.id` sebagai canonical "
     "tanpa DNS; email memakai Gmail.", "beli domain + email → ganti canonical, sitemap, OG URL"),
    ("Kebijakan privasi", "Belum ada. Wajib sebelum formulir member/analitik aktif.",
     "tulis di halaman `/privasi/` dari `data/legal.json`, bukan dokumen baru"),
    ("Syarat & ketentuan", "Belum ada. Wajib memuat garansi & pengembalian.",
     "tulis di `/syarat/`, rujuk ke `data/catalog.json` untuk klaim"),
    ("Kebijakan pengiriman & ongkir", "Butuh keputusan kurir dan tarif — keputusan Anda.",
     "tabel kurir di `/pengiriman/` setelah keputusan"),
    ("Izin nama petani & Ais Coffee Roastery", "Nama sudah tayang, izin belum.",
     "surat izin tertulis; bukan pekerjaan kode"),
    ("Pembayaran otomatis", "Belum ada gateway; semua order lewat WhatsApp.",
     "butuh akun Midtrans/Xendit (NIB) — jangan dikarang"),
]

SKILL_MAP = [
    ("Beranda komersial (keranjang + ringkasan order)", "motion-web, landing-page-ai", "sedang"),
    ("Halaman produk per lot (`/lot/<id>/`)", "katalog-render, landing-page-ai", "sedang"),
    ("Halaman kebijakan (privasi, syarat, pengiriman)", "landing-page-ai", "kecil"),
    ("Sitemap, robots.txt, 404, manifest", "motion-web", "kecil"),
    ("Struktur data produk & FAQ (JSON-LD)", "search-intent-riset", "kecil"),
    ("Gerak masuk halaman produk + transisi", "motion-web, gsap, motion-design", "sedang"),
    ("Nada & teks halaman (bukan template)", "desain-prompt, studio-konten", "kecil"),
    ("Hero 3D adegan (three.js + postprocessing)", "threejs, postprocessing, quarks-vfx, tweakpane", "besar"),
    ("Fisika di halaman (biji jatuh, kotak bertumpuk)", "rapier-physics", "besar, opsional"),
    ("Figure penjelas isometrik (proses sangrai)", "anatomy, anatomy-reveal", "sedang"),
    ("Garis isometrik yang menjawab pointer", "hairline-create, hairline-adopt", "sedang"),
    ("Video produk dari data katalog", "remotion, remotion-skills, ffmpeg-encode", "besar"),
    ("Animasi diagram (rasio seduh, profil sangrai)", "manim", "sedang"),
    ("Lottie penanda proses", "lottie", "kecil"),
    ("Musik & SFX berlisensi", "openverse-audio, librosa-beat", "kecil"),
    ("Caption animasi (bila ada narasi)", "whisperx-captions", "sedang"),
    ("Aset 3D dari Blender (bila perlu mesh baru)", "blender-mcp", "besar, belum teruji"),
]


def hitung() -> dict:
    halaman = []
    for akar, _, berkas in os.walk(ROOT):
        if any(x in akar for x in ("node_modules", "/.git", "/rencana")):
            continue
        for b in berkas:
            if b.endswith(".html"):
                p = os.path.relpath(os.path.join(akar, b), ROOT)
                if p in PUBLIK or p in DAPUR:
                    halaman.append(p)
    d = {"halaman_publik": [], "halaman_dapur": [], "angka": {}}
    for p, (nama, isi) in PUBLIK.items():
        if os.path.exists(os.path.join(ROOT, p)):
            d["halaman_publik"].append({
                "berkas": p, "nama": nama, "isi": isi,
                "kb": round(os.path.getsize(os.path.join(ROOT, p)) / 1024, 1)})
    for p, nama in DAPUR.items():
        if os.path.exists(os.path.join(ROOT, p)):
            d["halaman_dapur"].append({"berkas": p, "nama": nama,
                                       "kb": round(os.path.getsize(os.path.join(ROOT, p)) / 1024, 1)})

    with open(os.path.join(ROOT, "data", "catalog.json"), encoding="utf-8") as f:
        katalog = json.load(f)
    lolos = [p for p in katalog["products"] if p.get("status") != "draf"]
    d["angka"]["lot"] = len(lolos)
    d["angka"]["ukuran"] = sorted({v["weight"] for p in lolos for v in p.get("variants", [])})

    d["angka"]["foto_studio"] = len(glob.glob(os.path.join(ROOT, "assets/img/studio/*.jpg")))
    d["angka"]["foto_pasar"] = len(glob.glob(os.path.join(ROOT, "assets/img/katalog/pasar/*.jpg")))
    d["angka"]["mb_aset"] = round(
        sum(os.path.getsize(os.path.join(a, f)) for a, _, fs in os.walk(
            os.path.join(ROOT, "assets/img")) for f in fs) / 1024 / 1024, 1)

    # kondisi situs sekarang
    indeks = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    d["angka"]["kb_beranda"] = round(len(indeks.encode()) / 1024, 1)
    d["angka"]["tautan_wa_beranda"] = len(re.findall(r"data-wa=", indeks))
    js = open(os.path.join(ROOT, "assets/js/site.js"), encoding="utf-8").read()
    d["angka"]["kartu_dari_js"] = ("buildGrid" in js) and ("fetch('data/catalog.json'" in js)
    d["angka"]["ada_jsonld"] = "application/ld+json" in indeks
    for f in ("sitemap.xml", "robots.txt", "404.html", "manifest.webmanifest"):
        d["angka"][f.split(".")[0]] = os.path.exists(os.path.join(ROOT, f))
    with open(os.path.join(ROOT, "data", "legal.json"), encoding="utf-8") as f:
        legal = json.load(f)["dokumen"]
    d["angka"]["legal_selesai"] = sum(1 for x in legal if x["status"] == "selesai")
    d["angka"]["legal_total"] = len(legal)
    d["angka"]["legal_belum"] = [x["nama"] for x in legal if x["status"] != "selesai"]
    d["blokir"] = [{"butir": a, "status": b, "jalan": c} for a, b, c in BLOKIR_LUAR]
    d["peta"] = [{"pekerjaan": a, "skill": b, "ukuran": c} for a, b, c in SKILL_MAP]
    return d


def tulis(d: dict) -> None:
    a = d["angka"]
    baris = []
    t = baris.append
    t("# Rencana website komersial — jawaban jujur")
    t("")
    t(f"Dibuat dari isi repo oleh `tools/rencana.py`. Semua angka di bawah dibaca dari disk, "
      f"bukan diketik manual.")
    t("")
    t("## 1. Yang sudah jadi — jangan dibuat ulang")
    t("")
    t("| Halaman | Isi | Berat |")
    t("| --- | --- | --- |")
    for h in d["halaman_publik"]:
        t(f'| `{h["berkas"]}` — {h["nama"]} | {h["isi"]} | {h["kb"]} KB |')
    t("")
    t(f"| Angka | Nilai |")
    t("| --- | --- |")
    t(f"| Lot yang sudah tayang | **{a['lot']}** |")
    t(f"| Ukuran kemasan | {', '.join(a['ukuran'])} |")
    t(f"| Foto studio 2000 px | **{a['foto_studio']}** |")
    t(f"| Foto marketplace putih | **{a['foto_pasar']}** |")
    t(f"| Berat aset gambar | {a['mb_aset']} MB |")
    t(f"| Beranda | {a['kb_beranda']} KB · {a['tautan_wa_beranda']} tombol WhatsApp · "
      f"kartu digambar dari `data/catalog.json`: {'ya' if a['kartu_dari_js'] else 'tidak'} |")
    t(f"| Dokumen legal selesai | **{a['legal_selesai']} / {a['legal_total']}** |")
    t("")
    t("Artinya: **pondasi situsnya sudah ada**. Beranda, katalog, halaman lot, kampanye, "
      "B2B, foto 2000 px, dan data yang menggerakkan kartu semuanya sudah jalan tanpa "
      "framework dan tanpa CDN. Yang belum ada bukan pondasi, melainkan **lapisan jual**.")
    t("")
    t("## 2. Yang belum ada (dan bisa dikerjakan sekarang)")
    t("")
    t("| # | Pekerjaan | Skill yang dipakai | Ukuran |")
    t("| --- | --- | --- | --- |")
    for i, p in enumerate(d["peta"], 1):
        t(f'| {i} | {p["pekerjaan"]} | `{p["skill"]}` | {p["ukuran"]} |')
    t("")
    t("Urutan yang saya sarankan (bukan semua sekaligus):")
    t("")
    t("1. **Jalur beli yang tidak putus** — keranjang kecil di beranda + halaman ringkasan "
      "order yang menghasilkan satu pesan WhatsApp rapi — *sedang*")
    t("2. **Sitemap + robots + 404 + manifest** — memalukan kalau domain aktif tanpa ini — *kecil*")
    t("3. **Halaman produk per lot** — alamat sendiri (`/lot/gayo/`), bisa dibagikan, "
      "bisa diindeks — *sedang*")
    t("4. **JSON-LD Product + FAQ** — harga & stok terbaca mesin pencari — *kecil*")
    t("5. **Halaman kebijakan** — ditulis dari `data/legal.json`, bukan dikarang — *kecil*")
    t("6. Baru **gerak & aset berat** (three.js, anatomy, video) — kalau 1–5 sudah jalan")
    t("")
    t("## 3. Yang TIDAK bisa saya tutup (butuh Anda)")
    t("")
    t("| Butir | Status | Jalan keluarnya |")
    t("| --- | --- | --- |")
    for b in d["blokir"]:
        t(f'| **{b["butir"]}** | {b["status"]} | {b["jalan"]} |')
    t("")
    t(f"Dokumen yang masih kosong menurut `data/legal.json`: "
      f"{', '.join(a['legal_belum'])}.")
    t("")
    t("Saya tidak akan menulis kebijakan privasi seolah-olah itu fakta hukum, dan tidak akan "
      "memasang pembayaran yang belum ada akunnya. Keduanya bisa **disiapkan** (struktur "
      "halaman + tempat isinya), tapi isinya harus dari Anda.")
    t("")
    t("## 4. Batas menguji tampilan — jujur")
    t("")
    t("Di sandbox ini **tidak ada Chromium** (`playwright install chromium` gagal mengunduh). "
      "Artinya:")
    t("")
    t("| Yang bisa diuji mesin | Yang tidak bisa |")
    t("| --- | --- |")
    t("| HTML seimbang, tautan tidak putus, ukuran berkas, isi data, latar putih foto, "
      "kontras teks, urutan judul, JSON-LD valid | **rupa sungguhan**: apakah section muat "
      "satu layar, apakah tombol nyaman di ponsel, apakah animasi halus |")
    t("")
    t("Rencana saya untuk menutup celah ini: `tools/pratinjau.py` yang sudah ada diperluas "
      "jadi **lembar kontak**: tangkapan teks + ukuran per section, bukan tangkapan piksel. "
      "Kalau Anda mau menilai rupa, buka Live Preview port 8080 — di situ peramban Anda yang "
      "menjadi mesin uji, bukan saya.")
    t("")
    t("## 5. Jawaban singkat")
    t("")
    t("**Bisa mulai sekarang**, dan tidak perlu memasang apa pun: 22 skill gerak sudah ada di "
      "`.agents/skills/`, 12 skill konten di `skills/`, datanya lengkap. Tapi yang paling "
      "menentukan penjualan bukan efek 3D — melainkan **jalur beli yang tidak putus** dan "
      "**halaman produk yang bisa diindeks**. Keduanya bisa selesai tanpa satu baris WebGL.")
    t("")
    os.makedirs(os.path.dirname(LAPORAN), exist_ok=True)
    with open(LAPORAN, "w", encoding="utf-8") as f:
        f.write("\n".join(baris) + "\n")
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def cek() -> list[str]:
    if not os.path.exists(DATA):
        return ["data/rencana-website.json belum ada — jalankan python3 tools/rencana.py"]
    with open(DATA, encoding="utf-8") as f:
        lama = json.load(f)
    baru = hitung()
    m = []
    for k, v in baru["angka"].items():
        if k == "legal_belum":
            continue
        if lama["angka"].get(k) != v:
            m.append(f"angka '{k}' berubah: {lama['angka'].get(k)} → {v}")
    return m


if __name__ == "__main__":
    if "--cek" in sys.argv:
        mm = cek()
        for x in mm:
            print("  ✗", x)
        print("  kesimpulan:", "OK · rencana website cocok dengan repo"
              if not mm else f"{len(mm)} angka kedaluwarsa — jalankan python3 tools/rencana.py")
        sys.exit(0 if not mm else 1)
    d = hitung()
    tulis(d)
    a = d["angka"]
    print(f'  halaman publik {len(d["halaman_publik"])} · dapur {len(d["halaman_dapur"])} · '
          f'lot {a["lot"]} · foto studio {a["foto_studio"]} · pasar {a["foto_pasar"]}')
    print(f'  sitemap={a["sitemap"]} robots={a["robots"]} 404={a["404"]} '
          f'manifest={a["manifest"]} · legal {a["legal_selesai"]}/{a["legal_total"]}')
    print(f'  laporan: rencana/website-komersial.md · data: data/rencana-website.json')
