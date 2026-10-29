#!/usr/bin/env python3
"""
Riset konten & kata kunci — mesin analisis untuk D3 (Marketing) dan D4 (Kreatif).

Membaca tangkapan manual (bukan scraping):
    data/riset-referensi.csv   post ramai / pesaing yang layak dijadikan acuan
    data/riset-komentar.csv    kutipan komentar → keberatan & bahasa pembeli
    data/riset-kata-kunci.csv  kata kunci Google / marketplace / TikTok search

Menulis:
    riset/index.html           dasbor riset (outlier, pola, komentar, kata kunci, brief)
    riset/data.json            ringkasan untuk papan harian
    riset/swipe-file.md        swipe file ringkas untuk dibaca cepat
    riset/brief/brief-NN-*.md  brief konten siap dikerjakan D4

Tanpa dependensi eksternal. Tidak memanggil API apa pun.

Pakai:
    python3 tools/riset.py            # hitung + tulis semua keluaran
    python3 tools/riset.py --cek      # ringkasan terminal saja
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402
import re
import statistics
import unicodedata
from datetime import date
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "riset")
D = lambda *p: os.path.join(ROOT, "data", *p)

# ── bobot niat pencarian (bukan angka resmi; skala relatif 0,6–1,4) ─────────
BOBOT_NIAT = {"beli": 1.4, "lokal": 1.3, "banding": 1.2, "info": 0.8}

# ── taksonomi hook: kunci → (nama, ciri pengenal) ───────────────────────────
HOOK = [
    ("angka", "Angka / daftar", r"\d|satu|dua|tiga|empat|lima|tujuh"),
    ("larangan", "Larangan / peringatan", r"\bjangan\b|\bhindari\b|\bstop\b|\bberhenti\b|\bsalah\b"),
    ("pengakuan", "Pengakuan / biaya nyata", r"\bbuang\b|\btolak\b|\bgagal\b|\brugi\b|\bkami\b.*\bbuang\b"),
    ("diagnosis", "Diagnosis masalah", r"\bkenapa\b|\bpenyebab\b|\bbikin\b.*\b(pa|ham)bit\b|\bpadahal\b"),
    ("banding", "Perbandingan A vs B", r"\bvs\b|\bdibanding\b|\bbedanya\b|\bmana yang\b|\bmurah\b.*\bmahal\b"),
    ("pov", "Relatable / POV", r"\bpov\b|\b kamu\b|\bkalian\b|\bgue\b|\bbanget\b"),
    ("tutorial", "Tutorial langkah", r"\bcara\b|\blangkah\b|\btutorial\b|\bseduh\b|\bresep\b"),
    ("otoritas", "Otoritas / orang dalam", r"\bbarista\b|\broaster\b|\bpetani\b|\bqgrader\b|\bexpert\b"),
    ("harga", "Harga / penawaran", r"\brp\s?\d|\bribu\b|\bharga\b|\bpromo\b|\bdiskon\b"),
    ("proses", "Proses di balik layar", r"\bproses\b|\bsangrai\b|\bproduksi\b|\bpacking\b|\bqc\b"),
]
HOOK_RE = [(k, n, re.compile(p, re.I)) for k, n, p in HOOK]
# urutan prioritas: pola paling spesifik menang; "angka" & "harga" paling umum → paling akhir
PRIORITAS_HOOK = ["pengakuan", "larangan", "banding", "diagnosis", "otoritas", "pov",
                  "tutorial", "proses", "harga", "angka"]

# ── pola jual yang dipakai brand (untuk memetakan pola → sudut kita) ───────
# pola → (sudut kita, penjelasan singkat, hook versi kita, aset yang dipakai)
SUDUT = {
    "angka": ("Angka + daftar",
              "Angka menghentikan gulir lebih cepat daripada kata sifat. Pakai angka yang benar-benar kita catat, "
              "bukan angka bulat karangan.",
              "Tiga hal yang tercetak di tiap kantong: tanggal sangrai, kode batch, level roast",
              "carousel-01c"),
    "larangan": ("Larangan yang bisa dibuktikan",
                 "Larangan bekerja karena menantang kebiasaan, bukan karena menakut-nakuti. Setelah melarang, "
                 "wajib langsung menjelaskan alasannya.",
                 "Jangan beli kopi yang cuma mencetak tanggal kedaluwarsa",
                 "carousel-01a"),
    "pengakuan": ("Pengakuan biaya",
                  "Mengakui kerugian nyata membangun kepercayaan lebih kuat daripada klaim kualitas. "
                  "Sebut angkanya, sebut keputusannya.",
                  "Minggu ini satu batch tidak lolos — skornya 81,5, ambang kami 83",
                  "reel-batch-ditolak"),
    "diagnosis": ("Diagnosis masalah",
                  "Orang mencari konten ini karena sedang punya masalahnya. Jawab penyebabnya di 3 detik pertama, "
                  "jangan menyimpan jawaban di akhir.",
                  "Kopi pahit padahal baru beli: cek tanggal sangrai, gilingan, lalu suhu air",
                  "reel-tanggal-sangrai"),
    "banding": ("Perbandingan jujur",
                "Perbandingan menaikkan simpan karena orang memakainya untuk memutuskan. Bandingkan hal yang "
                "bisa kita buktikan: ketinggian, proses, cara seduh — bukan 'enak vs tidak'.",
                "Arabika Ijen vs robusta Raung: ketinggian, rasa, dan cara seduhnya",
                "carousel-02a"),
    "pov": ("Relatable tanpa wajah",
            "Boleh dipakai, tapi paling mudah jadi klise. Pakai hanya kalau ada detail spesifik "
            "(kulkas, grinder murah, kopi sisa sebulan).",
            "POV: kamu beli kopi mahal tapi disimpan di dekat bumbu dapur",
            "story-01"),
    "tutorial": ("Tutorial singkat",
                 "Tutorial menyimpan = orang berniat mengulang. Batasi 3 langkah, dan pastikan alatnya benar-benar "
                 "ada di dapur orang Indonesia.",
                 "Cara menyimpan kopi: 3 langkah, tanpa alat khusus",
                 "carousel-02b"),
    "otoritas": ("Orang dalam",
                 "Kami tidak punya barista terkenal — yang kami punya adalah catatan QC. Ganti otoritas 'orang' "
                 "dengan otoritas 'data yang bisa dicek'.",
                 "Yang diperiksa saat cupping, dan kenapa 83 jadi ambang kami",
                 "reel-first-crack"),
    "harga": ("Harga terbuka",
              "Menyebut harga di konten menaikkan niat beli dan menyaring penanya. Selalu sebut isi paket "
              "dan harga per gram.",
              "Peta Rasa: 3 × 100 g Rp79.000 — sekitar Rp263 per gram",
              "post-01-peta-rasa"),
    "proses": ("Proses di balik layar",
               "Proses hanya menarik kalau ada taruhannya (waktu, suhu, keputusan). Tanpa itu, ini video pabrik.",
               "12 menit terakhir sebelum kopi ini dikemas",
               "reel-menit-terakhir"),
}
SUDUT_LAIN = ("Pola belum terklasifikasi",
              "Hook-nya tidak masuk taksonomi. Baca ulang, lalu tentukan sendiri: masalah apa yang diselesaikan "
              "dalam 3 detik pertama?", "—", "")

HINDARI = {"promo", "diskon", "buruan", "termurah", "termurah!", "nomor satu", "terbaik di"}


# ─────────────────────────────── utilitas ─────────────────────────────────
def baca_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def angka(v, default=0.0):
    if v is None:
        return default
    s = str(v).strip().lower().replace("rp", "").replace(" ", "")
    if not s:
        return default
    mult = 1
    if s.endswith("k"):
        mult, s = 1000, s[:-1]
    elif s.endswith("jt"):
        mult, s = 1_000_000, s[:-2]
    s = s.replace(".", "").replace(",", ".") if s.count(",") == 1 and "." in s else s.replace(".", "")
    try:
        return float(s) * mult
    except ValueError:
        return default


def median(nilai):
    nilai = [n for n in nilai if n is not None]
    return statistics.median(nilai) if nilai else None


def fmt(n, satuan=""):
    if n is None:
        return "—"
    if satuan == "x":
        return f"{n:.1f}×".replace(".", ",")
    if abs(n) >= 1_000_000:
        return f"{n/1_000_000:.1f} jt".replace(".", ",")
    if abs(n) >= 1_000:
        return f"{n/1000:.0f} rb"
    if isinstance(n, float) and not n.is_integer():
        return f"{n:.1f}".replace(".", ",")
    return f"{int(n)}"


def slug(teks):
    t = unicodedata.normalize("NFKD", teks or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:48] or "pola"


def bersih_html(path):
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="ignore") as f:
        t = f.read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&[a-z]+;|&#\d+;", " ", t)
    return re.sub(r"\s+", " ", t).lower()


# ───────────────────────────── analisis referensi ──────────────────────────
def analisa_referensi(rows):
    data = []
    for r in rows:
        views = angka(r.get("views"))
        if views <= 0:
            continue
        interaksi = sum(angka(r.get(k)) for k in ("likes", "komentar", "simpan", "bagikan"))
        hook = (r.get("hook") or "").strip()
        data.append({
            "tanggal": (r.get("tanggal") or "").strip(),
            "platform": (r.get("platform") or "?").strip().lower(),
            "akun": (r.get("akun") or "").strip(),
            "url": (r.get("url") or "").strip(),
            "format": (r.get("format") or "?").strip().lower(),
            "hook": hook,
            "topik": (r.get("topik") or "").strip(),
            "detik": angka(r.get("detik")),
            "views": views,
            "interaksi": interaksi,
            "simpan": angka(r.get("simpan")),
            "komentar_n": angka(r.get("komentar")),
            "followers": angka(r.get("followers_akun")),
            "status": (r.get("status") or "contoh").strip().lower(),
            "catatan": (r.get("catatan") or "").strip(),
            "er": interaksi / views * 100,
            "simpan_rate": angka(r.get("simpan")) / views * 100,
            "reach_rate": (views / angka(r.get("followers_akun")) * 100) if angka(r.get("followers_akun")) else None,
        })

    if not data:
        return {"baris": [], "grup": [], "confidence": "tidak ada data"}

    # baseline: paling spesifik lebih dulu, minimal 3 baris
    def baseline(b):
        klaim = [
            ("akun", lambda x: x["akun"] == b["akun"] and x["format"] == b["format"]),
            ("platform+format", lambda x: x["platform"] == b["platform"] and x["format"] == b["format"]),
            ("platform", lambda x: x["platform"] == b["platform"]),
            ("global", lambda x: True),
        ]
        for nama, f in klaim:
            sampel = [x["views"] for x in data if f(x)]
            if len(sampel) >= 3:
                return median(sampel), len(sampel), nama
        return median([x["views"] for x in data]), len(data), "global"

    for b in data:
        dasar, n, tingkat = baseline(b)
        b["baseline"] = dasar
        b["baseline_n"] = n
        b["baseline_tingkat"] = tingkat
        b["lift"] = (b["views"] / dasar) if dasar else None
        lift = b["lift"] or 0
        b["label"] = ("outlier besar" if lift >= 5 else
                      "outlier kuat" if lift >= 2 else
                      "outlier ringan" if lift >= 1.5 else "normal")
        kategori = [k for k, _, rx in HOOK_RE if rx.search(b["hook"])]
        kategori.sort(key=lambda k: PRIORITAS_HOOK.index(k) if k in PRIORITAS_HOOK else 99)
        b["hook_kategori"] = kategori[0] if kategori else "lain"
        b["hook_semua"] = kategori
        b["hindari"] = [w for w in HINDARI if w in b["hook"].lower()]

    n_total = len(data)
    n_asli = sum(1 for b in data if b["status"] == "asli")
    # confidence hanya dihitung dari baris asli: sampel contoh tidak membuktikan apa pun
    confidence = ("belum ada data asli" if n_asli == 0 else
                  "tinggi" if n_asli >= 20 else "sedang" if n_asli >= 10 else
                  "rendah" if n_asli >= 5 else "sangat rendah")

    # pola per kategori hook — hanya dari baris yang benar-benar naik
    pola = {}
    for b in data:
        if (b["lift"] or 0) < 1.5:
            continue
        pola.setdefault(b["hook_kategori"], []).append(b)
    pola_rows = []
    for k, items in pola.items():
        nama = next((n for kk, n, _ in HOOK if kk == k), "Lainnya")
        sudut, penjelasan, contoh_hook, aset = SUDUT.get(k, SUDUT_LAIN)
        pola_rows.append({
            "kunci": k, "nama": nama, "n": len(items),
            "lift_median": median([i["lift"] for i in items]) or 0,
            "er_median": median([i["er"] for i in items]) or 0,
            "views_median": median([i["views"] for i in items]) or 0,
            "format": sorted({i["format"] for i in items}),
            "contoh": [i["hook"] for i in items[:3]],
            "sudut": sudut, "penjelasan": penjelasan,
            "hook_kita": contoh_hook, "aset": aset,
        })
    pola_rows.sort(key=lambda p: (p["lift_median"], p["n"]), reverse=True)

    # matriks format
    matriks = {}
    for b in data:
        matriks.setdefault((b["platform"], b["format"]), []).append(b)
    matriks_rows = [{
        "platform": k[0], "format": k[1], "n": len(v),
        "er_median": median([x["er"] for x in v]),
        "simpan_median": median([x["simpan_rate"] for x in v]),
        "lift_median": median([x["lift"] for x in v]),
        "detik_median": median([x["detik"] for x in v if x["detik"]]) or 0,
    } for k, v in matriks.items()]
    matriks_rows.sort(key=lambda r: r["er_median"] or 0, reverse=True)

    return {
        "baris": sorted(data, key=lambda x: x["lift"] or 0, reverse=True),
        "pola": pola_rows,
        "matriks": matriks_rows,
        "confidence": confidence,
        "n": n_total,
    }


# ───────────────────────────── analisis komentar ───────────────────────────
def analisa_komentar(rows):
    out = []
    for r in rows:
        kutipan = (r.get("kutipan") or "").strip()
        if not kutipan:
            continue
        if len(kutipan.split()) > 24:  # kutipan pendek saja, bukan salinan panjang
            kutipan = " ".join(kutipan.split()[:24]) + " …"
        out.append({
            "tanggal": (r.get("tanggal") or "").strip(),
            "platform": (r.get("platform") or "").strip().lower(),
            "kutipan": kutipan,
            "jenis": (r.get("jenis") or "lain").strip().lower(),
            "produk": (r.get("produk") or "").strip(),
            "tindakan": (r.get("tindakan") or "").strip(),
        })
    rekap = {}
    for x in out:
        rekap.setdefault(x["jenis"], []).append(x)
    rekap_rows = [{"jenis": k, "n": len(v), "contoh": v[0]["kutipan"]}
                  for k, v in sorted(rekap.items(), key=lambda kv: len(kv[1]), reverse=True)]
    return {"baris": out, "rekap": rekap_rows, "n": len(out)}


# ──────────────────────────── analisis kata kunci ──────────────────────────
def analisa_kata_kunci(rows):
    out = []
    for r in rows:
        kw = (r.get("kata_kunci") or "").strip()
        if not kw:
            continue
        niat = (r.get("niat") or "info").strip().lower()
        vol = angka(r.get("volume_skala"), 1) or 1
        kes = max(1.0, angka(r.get("kesulitan"), 3) or 3)
        target = (r.get("halaman_target") or "").strip()
        prioritas = round(vol * BOBOT_NIAT.get(niat, 0.8) / kes, 2)

        # cek cakupan: apakah kata kunci benar-benar muncul di halaman target
        if not target:
            cakupan, rasio = "belum ada halaman", 0.0
        elif not os.path.exists(os.path.join(ROOT, target)):
            cakupan, rasio = "halaman tidak ditemukan", 0.0
        else:
            teks = bersih_html(os.path.join(ROOT, target))
            token = [t for t in re.split(r"\s+", kw.lower())
                     if len(t) > 2 and t not in ("yang", "untuk", "dan", "dengan", "di", "ke")]
            kena = sum(1 for t in token if t in teks)
            rasio = kena / len(token) if token else 0.0
            cakupan = "tercakup" if kw.lower() in teks else ("sebagian" if rasio >= 0.6 else "belum")

        out.append({
            "kata_kunci": kw, "mesin": (r.get("mesin") or "google").strip().lower(),
            "niat": niat, "volume": vol, "kesulitan": kes,
            "prioritas": prioritas, "halaman": target, "cakupan": cakupan,
            "rasio": round(rasio * 100), "catatan": (r.get("catatan") or "").strip(),
        })

    out.sort(key=lambda x: x["prioritas"], reverse=True)
    gap = [x for x in out if x["cakupan"] in ("belum", "belum ada halaman", "halaman tidak ditemukan")]
    terjawab = sum(1 for x in out if x["cakupan"] in ("tercakup", "sebagian"))
    return {
        "baris": out, "celah": gap, "n": len(out),
        "persen_tercakup": round(terjawab / len(out) * 100) if out else 0,
        "persen_persis": round(sum(1 for x in out if x["cakupan"] == "tercakup") / len(out) * 100) if out else 0,
    }


# ─────────────────────────────── brief konten ─────────────────────────────
def buat_brief(pola, komentar, kreatif, maks=6):
    aset_ids = {i["id"]: i for i in (kreatif or {}).get("items", [])}
    keberatan = [k for k in komentar["baris"] if k["jenis"] == "keberatan"][:3]
    briefs = []
    for i, p in enumerate(pola[:maks], start=1):
        aset = p.get("aset") or ""
        aset_info = aset_ids.get(aset)
        briefs.append({
            "no": i,
            "judul": p["sudut"],
            "dasar": f"{p['n']} post pola “{p['nama']}” naik median {fmt(p['lift_median'], 'x')} "
                     f"(ER median {fmt(p['er_median'])}%) di {', '.join(p['format'])}"
                     + (" — n=1, indikatif" if p["n"] == 1 else ""),
            "contoh_acuan": p["contoh"],
            "sudut": p["sudut"],
            "penjelasan": p.get("penjelasan", ""),
            "hook": p["hook_kita"],
            "format": p["format"],
            "aset": aset,
            "aset_status": (aset_info or {}).get("status", "belum ada di manifest") if aset else "belum ada",
            "keberatan": [k["kutipan"] for k in keberatan],
            "bukti": "batch-qc.csv (skor & status batch) · catalog.json (harga) · label bertanggal sangrai",
            "cta": "Pesan via WhatsApp — sebutkan metode seduh & kotanya",
            "larangan": "jangan pakai kata promo/diskon/buruan; jangan klaim 'terbaik'; "
                        "jangan sebut Nocturne sebagai roastery",
        })
    return briefs


def brief_markdown(b, tgl):
    baris_acuan = "\n".join(f'  - "{escape(h)}"' for h in b["contoh_acuan"]) or "  - (tidak ada)"
    baris_keberatan = "\n".join(f'  - "{escape(k)}"' for k in b["keberatan"]) or "  - (belum tercatat)"
    return f"""# Brief {b['no']:02d} — {b['judul']}

> Dibuat {tgl.isoformat()} oleh `tools/riset.py` dari `data/riset-referensi.csv` dan
> `data/riset-komentar.csv`. **Status data:** lihat kolom `status` di CSV. Selama barisnya
> masih `contoh`, angka di brief ini adalah contoh mekanisme — bukan bukti pasar.

**Dasar (bukti dari data):** {b['dasar']}

## Acuan yang dianalisis (adaptasi, bukan salin)
{baris_acuan}

## Sudut untuk Nocturne
**{b['sudut']}** — {b['penjelasan']}

## Hook (3 detik pertama)
```
{b['hook']}
```

## Format & durasi
{', '.join(b['format'])} · 7 detik untuk video, 3–4 slide untuk carousel · teks ≥ 80 px, aman dari UI bawah.

## Aset yang dipakai
`{b['aset'] or '—'}` — status: **{b['aset_status']}**.
Kalau belum ada: jalankan `python3 tools/kreatif.py` atau tambahkan item di `data/kreatif.json`.

## Bukti yang wajib tampil
{b['bukti']}

## Keberatan pembeli yang harus dijawab
{baris_keberatan}

## CTA
{b['cta']}

## Larangan
{b['larangan']}

## Selesai bila
Aset jadi (status `siap` di manifest), caption tertulis, jadwal tercatat di
`data/konten-14hari.csv`, dan brief ini dihapus dari folder `riset/brief/` **setelah** ditandai
`dipakai` di `riset/data.json`.
"""


# ──────────────────────────────── dasbor HTML ─────────────────────────────
CSS = """
:root{--paper:#F5EFE4;--paper2:#EFE6D6;--ink:#16110D;--muted:#6b6156;--orange:#E1542B;
--gold:#D9A441;--espresso:#4A2C1A;--line:1px solid rgba(22,17,13,.14);--red:#8C2F1E}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 Inter,system-ui,sans-serif}
.wrap{max-width:1200px;margin:0 auto;padding:36px clamp(16px,4vw,40px) 80px}
h1{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(30px,5vw,46px);line-height:1;
letter-spacing:-.03em;margin:6px 0 10px}
h2{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(21px,2.6vw,28px);letter-spacing:-.02em;
margin:44px 0 6px;border-top:2px solid var(--ink);padding-top:14px}
h3{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:17px;margin:0 0 4px;letter-spacing:-.01em}
.kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.lede{max-width:70ch;color:var(--muted);margin:0 0 8px}
.grid{display:grid;gap:14px}
.kpi{grid-template-columns:repeat(auto-fit,minmax(170px,1fr));margin-top:20px}
.kpi div{border:var(--line);border-radius:8px;padding:14px 16px;background:#fff8}
.kpi span{display:block;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.kpi b{display:block;font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:26px;letter-spacing:-.02em;
line-height:1.1;margin:4px 0 2px}
.kpi em{font-size:11.5px;color:var(--muted);font-style:normal}
table{width:100%;border-collapse:collapse;font-size:13.2px;margin-top:12px}
th,td{text-align:left;padding:8px 9px;border-bottom:1px solid rgba(22,17,13,.12);vertical-align:top}
th{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr:last-child td{border-bottom:0}
.pill{display:inline-block;font-size:10.5px;letter-spacing:.03em;padding:2px 7px;border-radius:99px;border:1px solid}
.pill.ok{color:#1f6b3a;border-color:#1f6b3a;background:#e8f2ea}
.pill.warn{color:#8a5a00;border-color:#b78621;background:#fbf1d9}
.pill.dim{color:var(--muted);border-color:rgba(22,17,13,.2)}
.pill.hot{color:#fff;border-color:var(--orange);background:var(--orange)}
.banner{border-left:4px solid var(--gold);background:#fbf1d9;padding:12px 16px;border-radius:4px;
font-size:13px;margin:18px 0 0}
.banner b{display:block;margin-bottom:2px}
.card{border:var(--line);border-radius:8px;padding:16px 18px;background:#fff8}
.card .meta{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
.card ul{margin:6px 0 0;padding-left:18px;font-size:13.4px}
.card .hook{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:15.5px;background:var(--paper2);
padding:8px 12px;border-radius:4px;margin:8px 0}
.cards{grid-template-columns:repeat(auto-fit,minmax(300px,1fr));margin-top:16px}
code{background:var(--paper2);padding:1px 5px;border-radius:3px;font-size:12px}
footer{margin-top:44px;border-top:2px solid var(--ink);padding-top:14px;font-size:12px;color:var(--muted);
display:flex;flex-wrap:wrap;gap:8px 22px;justify-content:space-between}
a{color:inherit}
"""


def dasbor(ctx, tgl):
    ref, kom, kw, briefs = ctx["referensi"], ctx["komentar"], ctx["kata_kunci"], ctx["brief"]
    demo = ctx["asli"] == 0
    top = ref["baris"][0] if ref["baris"] else None
    pola_utama = ref["pola"][0] if ref["pola"] else None
    kw_top = kw["baris"][0] if kw["baris"] else None

    o = [f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Riset Konten &amp; Kata Kunci — Nocturne Koffie</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<p class="kicker">D3 Marketing × D4 Kreatif · dibuat {tgl.strftime('%d %B %Y')}</p>
<h1>Riset konten &amp; kata kunci</h1>
<p class="lede">Dasbor ini membaca tangkapan manual — bukan scraping. Yang dihitung: <b>outlier</b>
(post yang naik di atas kebiasaan akunnya), <b>pola hook</b>, <b>bahasa pembeli dari komentar</b>,
dan <b>celah kata kunci</b> antara yang dicari orang dan yang benar-benar tertulis di halaman kita.</p>"""]

    if demo:
        o.append(f"""<div class="banner"><b>Mode contoh — {ctx['contoh']} baris masih berlabel <code>contoh</code></b>
Angka di halaman ini menunjukkan cara kerja mesin analisis, bukan kondisi pasar nyata.
Ganti baris di <code>data/riset-referensi.csv</code> dengan tangkapan asli (lihat
<code>skills/social-media-riset/SKILL.md</code>), ubah kolom <code>status</code> menjadi
<code>asli</code>, lalu jalankan <code>python3 tools/riset.py</code>.</div>""")

    o.append(f"""<div class="grid kpi">
  <div><span>Post dianalisis</span><b>{ref['n']}</b><em>{ctx['asli']} asli · {ctx['contoh']} contoh</em></div>
  <div><span>Confidence</span><b>{ref['confidence']}</b><em>hanya dihitung dari {ctx['asli']} baris <code>asli</code></em></div>
  <div><span>Outlier teratas</span><b>{fmt(top['lift'], 'x') if top else '—'}</b><em>{escape(top['hook'][:46]) + '…' if top and len(top['hook'])>46 else (escape(top['hook']) if top else '—')}</em></div>
  <div><span>Pola dominan</span><b>{pola_utama['nama'] if pola_utama else '—'}</b><em>{pola_utama['n'] if pola_utama else 0} post · lift {fmt(pola_utama['lift_median'], 'x') if pola_utama else '—'}</em></div>
  <div><span>Komentar dianalisis</span><b>{kom['n']}</b><em>{kom['rekap'][0]['jenis'] if kom['rekap'] else '—'} terbanyak</em></div>
  <div><span>Kata kunci sudah dijawab halaman</span><b>{kw['persen_tercakup']}%</b><em>{len(kw['celah'])} celah dari {kw['n']} · persis {kw['persen_persis']}%</em></div>
</div>""")

    # ── 1. outlier
    o.append("<h2>1 · Post yang naik di atas kebiasaan akunnya</h2>")
    o.append('<p class="lede">Lift = views ÷ median akun/format yang sama. Bukan “views terbesar”, '
             'karena akun besar selalu menang di angka mentah. Ambang: 1,5× ringan · 2× kuat · 5× besar.</p>')
    o.append('<table><tr><th>#</th><th>Hook</th><th>Platform / format</th><th class="num">Views</th>'
             '<th class="num">Lift</th><th class="num">ER</th><th class="num">Simpan</th><th>Label</th><th>Status data</th></tr>')
    for i, b in enumerate(ref["baris"][:14], 1):
        pill = {"outlier besar": "hot", "outlier kuat": "ok", "outlier ringan": "warn"}.get(b["label"], "dim")
        jml = f'<a href="{escape(b["url"])}" target="_blank" rel="noopener">link</a>' if b["url"] else "—"
        o.append(f'<tr><td class="num">{i}</td><td>{escape(b["hook"])}<br><span class="kicker">'
                 f'{escape(b["akun"])}{" · " + escape(b["catatan"]) if b["catatan"] else ""} {jml}</span></td>'
                 f'<td>{b["platform"]} · {b["format"]}{" · " + fmt(b["detik"]) + "s" if b["detik"] else ""}</td>'
                 f'<td class="num">{fmt(b["views"])}</td><td class="num">{fmt(b["lift"], "x")}</td>'
                 f'<td class="num">{fmt(b["er"])}%</td><td class="num">{fmt(b["simpan_rate"])}%</td>'
                 f'<td><span class="pill {pill}">{b["label"]}</span></td>'
                 f'<td><span class="pill {"dim" if b["status"] != "asli" else "ok"}">{b["status"]}</span></td></tr>')
    o.append("</table>")

    # ── 2. pola
    o.append("<h2>2 · Pola yang berulang (bukan satu keberuntungan)</h2>")
    o.append('<p class="lede">Dihitung hanya dari baris dengan lift ≥ 1,5×. Kolom “sudut kita” adalah '
             'penerjemahan pola itu ke bukti yang kita punya — bukan menyalin konten orang lain.</p>')
    o.append('<table><tr><th>Pola</th><th class="num">Post</th><th class="num">Lift median</th>'
             '<th class="num">ER median</th><th>Format</th><th>Contoh acuan</th><th>Sudut kita</th></tr>')
    for p in ref["pola"]:
        contoh = "<br>".join(f'“{escape(c)}”' for c in p["contoh"])
        o.append(f'<tr><td><b>{escape(p["nama"])}</b></td><td class="num">{p["n"]}</td>'
                 f'<td class="num">{fmt(p["lift_median"], "x")}</td><td class="num">{fmt(p["er_median"])}%</td>'
                 f'<td>{", ".join(p["format"])}</td><td>{contoh}</td>'
                 f'<td><b>{escape(p["sudut"])}</b><br><span class="kicker">{escape(p["hook_kita"])}</span></td></tr>')
    o.append("</table>")

    # ── 3. matriks format
    o.append("<h2>3 · Format mana yang menyimpan, format mana yang menjual</h2>")
    o.append('<p class="lede">ER = (like + komentar + simpan + bagikan) ÷ views. Simpan tinggi = '
             'orang berniat kembali; itu sinyal yang kita kejar untuk pilar bukti &amp; edukasi.</p>')
    o.append('<table><tr><th>Platform</th><th>Format</th><th class="num">Post</th><th class="num">ER median</th>'
             '<th class="num">Simpan median</th><th class="num">Lift median</th><th class="num">Durasi</th></tr>')
    for m in ref["matriks"]:
        o.append(f'<tr><td>{m["platform"]}</td><td>{m["format"]}</td><td class="num">{m["n"]}</td>'
                 f'<td class="num">{fmt(m["er_median"])}%</td><td class="num">{fmt(m["simpan_median"])}%</td>'
                 f'<td class="num">{fmt(m["lift_median"], "x")}</td>'
                 f'<td class="num">{fmt(m["detik_median"]) + "s" if m["detik_median"] else "—"}</td></tr>')
    o.append("</table>")

    # ── 4. komentar
    o.append("<h2>4 · Bahasa pembeli — dari komentar ke copy</h2>")
    o.append('<p class="lede">Kutipan dipotong ≤ 24 kata; tidak menyalin identitas siapa pun. '
             'Yang diambil adalah <b>kalimatnya</b>, karena pembeli memakai kata yang berbeda dari brosur kita.</p>')
    if kom["baris"]:
        o.append('<table><tr><th>Jenis</th><th class="num">Jumlah</th><th>Kutipan</th><th>Tindakan</th></tr>')
        for r in kom["rekap"]:
            contoh = [k for k in kom["baris"] if k["jenis"] == r["jenis"]][:3]
            o.append(f'<tr><td><b>{escape(r["jenis"])}</b></td><td class="num">{r["n"]}</td>'
                     f'<td>{"<br>".join("“" + escape(k["kutipan"]) + "”" for k in contoh)}</td>'
                     f'<td>{"<br>".join(escape(k["tindakan"] or "—") for k in contoh)}</td></tr>')
        o.append("</table>")
        o.append('<p class="lede" style="margin-top:12px"><b>Cara pakai:</b> kalimat pembeli masuk ke '
                 'caption (bukan parafrase), setiap keberatan → satu slide carousel, setiap pertanyaan '
                 '→ satu FAQ WhatsApp otomatis.</p>')
    else:
        o.append('<div class="card">Belum ada komentar tercatat. Isi <code>data/riset-komentar.csv</code>.</div>')

    # ── 5. kata kunci
    o.append("<h2>5 · Kata kunci &amp; celah halaman</h2>")
    o.append('<p class="lede">Prioritas = volume (skala relatif 1–5) × bobot niat ÷ kesulitan. '
             'Kolom <b>cakupan</b> dicek langsung ke berkas halaman target — bukan perkiraan: '
             'kalau kata kuncinya tidak ada di halaman, angkanya tidak akan pernah datang.</p>')
    o.append('<table><tr><th>Kata kunci</th><th>Mesin</th><th>Niat</th><th class="num">Vol</th>'
             '<th class="num">Sulit</th><th class="num">Prioritas</th><th>Halaman</th><th>Cakupan</th></tr>')
    for k in kw["baris"]:
        pill = {"tercakup": "ok", "sebagian": "warn"}.get(k["cakupan"], "dim")
        o.append(f'<tr><td>{escape(k["kata_kunci"])}</td><td>{k["mesin"]}</td><td>{k["niat"]}</td>'
                 f'<td class="num">{fmt(k["volume"])}</td><td class="num">{fmt(k["kesulitan"])}</td>'
                 f'<td class="num">{fmt(k["prioritas"])}</td>'
                 f'<td>{"<code>" + escape(k["halaman"]) + "</code>" if k["halaman"] else "—"}</td>'
                 f'<td><span class="pill {pill}">{k["cakupan"]}</span>'
                 f'{" " + str(k["rasio"]) + "%" if k["cakupan"] == "sebagian" else ""}</td></tr>')
    o.append("</table>")
    if kw["celah"]:
        o.append('<h3 style="margin-top:18px">Tiga celah pertama yang layak dikerjakan</h3><ul>')
        for k in kw["celah"][:3]:
            hal = k["halaman"]
            if not hal:
                aksi = 'belum ada halaman — pertimbangkan satu bagian di halaman jual, atau jawab lewat konten'
            elif hal.endswith((".csv", ".md", ".json")):
                aksi = (f'<code>{escape(hal)}</code> bukan halaman HTML — pindahkan angkanya ke bagian '
                        f'yang bisa dibaca mesin pencari &amp; pembeli')
            else:
                aksi = f'tambahkan bagian untuk “{escape(k["kata_kunci"])}” di <code>{escape(hal)}</code>' 
            o.append(f'<li><b>{escape(k["kata_kunci"])}</b> (prioritas {fmt(k["prioritas"])}) — {aksi}.</li>')
        o.append("</ul>")

    # ── 6. brief
    o.append("<h2>6 · Brief untuk D4</h2>")
    o.append('<p class="lede">Tiap brief = satu pola + satu sudut + aset yang sudah ada + bukti yang harus tampil. '
             'Berkas markdown-nya ada di <code>riset/brief/</code>.</p>')
    o.append('<div class="grid cards">')
    for b in briefs:
        o.append(f"""<article class="card">
  <p class="meta">Brief {b['no']:02d} · {escape(', '.join(b['format']))}</p>
  <h3>{escape(b['judul'])}</h3>
  <div class="hook">{escape(b['hook'])}</div>
  <ul>
    <li><b>Dasar:</b> {escape(b['dasar'])}</li>
    <li><b>Aset:</b> <code>{escape(b['aset'] or '—')}</code> · {escape(b['aset_status'])}</li>
    <li><b>Bukti:</b> {escape(b['bukti'])}</li>
    <li><b>Jangan:</b> {escape(b['larangan'])}</li>
  </ul>
</article>""")
    o.append("</div>")

    o.append(f"""<footer>
  <span>Dibuat otomatis oleh <code>tools/riset.py</code> · sumber: <code>data/riset-*.csv</code> ·
    skill: <a href="../skills/social-media-riset/SKILL.md">social-media-riset</a> ·
    <a href="../skills/komentar-mining/SKILL.md">komentar-mining</a> ·
    <a href="../skills/search-intent-riset/SKILL.md">search-intent-riset</a></span>
  <span>Data publik saja · kutipan ≤ 24 kata · tidak menyalin konten pihak lain ·
    <a href="../dashboard/index.html">papan harian</a></span>
</footer></div></body></html>""")
    return "\n".join(o)


def swipe_md(ctx, tgl):
    ref, kom, kw, briefs = ctx["referensi"], ctx["komentar"], ctx["kata_kunci"], ctx["brief"]
    o = [f"""# Swipe file — referensi konten & kata kunci

> Dibuat {tgl.isoformat()} oleh `tools/riset.py`. {ctx['asli']} baris asli, {ctx['contoh']} baris contoh.
> Confidence: **{ref['confidence']}** ({ref['n']} post). Sampel kecil = arah, bukan kepastian.

## Post outlier

| # | Hook | Platform/format | Lift | ER | Label |
|---:|---|---|---:|---:|---|
"""]
    for i, b in enumerate(ref["baris"][:12], 1):
        o.append(f'| {i} | {b["hook"]} | {b["platform"]}/{b["format"]} | {fmt(b["lift"], "x")} | '
                 f'{fmt(b["er"])}% | {b["label"]} |\n')
    o.append("\n## Pola & sudut kita\n\n")
    for p in ref["pola"]:
        o.append(f'### {p["nama"]} — {p["n"]} post, lift median {fmt(p["lift_median"], "x")}\n\n')
        o.append(f'- Acuan: ' + "; ".join(f'“{c}”' for c in p["contoh"]) + "\n")
        o.append(f'- Sudut Nocturne: **{p["sudut"]}**\n')
        o.append(f'- Hook kita: `{p["hook_kita"]}`\n')
        o.append(f'- Aset: `{p["aset"] or "—"}`\n\n')
    o.append("## Kalimat pembeli (dari komentar)\n\n")
    for k in kom["baris"]:
        o.append(f'- *{k["jenis"]}* — “{k["kutipan"]}” → {k["tindakan"] or "—"}\n')
    o.append("\n## Celah kata kunci\n\n")
    for k in kw["celah"]:
        o.append(f'- **{k["kata_kunci"]}** ({k["mesin"]}, niat {k["niat"]}, prioritas {fmt(k["prioritas"])}) '
                 f'→ {k["halaman"] or "belum ada halaman"} · status: {k["cakupan"]}\n')
    o.append("\n## Brief\n\n")
    for b in briefs:
        o.append(f'- **{b["no"]:02d}. {b["judul"]}** — `{b["hook"]}` → `riset/brief/brief-{b["no"]:02d}-'
                 f'{slug(b["sudut"])}.md`\n')
    o.append("""
## Aturan pakai

1. **Adaptasi, bukan salin.** Yang diambil adalah pola (angka, larangan, pengakuan), bukan kalimat,
   footage, atau audio milik akun lain.
2. **Jangan pakai angka orang lain sebagai klaim kita.** Gunakan angka dari `data/batch-qc.csv`,
   `data/catalog.json`, atau `pesanan.csv`.
3. **Sebutkan sumber saat mengutip komentar publik**, dan potong ≤ 24 kata.
4. **Refresh ≤ 30 hari.** Pola konten cepat basi; tanggal dibuat ada di atas.
""")
    return "".join(o)


# ────────────────────────────────── main ──────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true", help="ringkasan terminal saja")
    args = ap.parse_args()

    ref_rows = baca_csv(D("riset-referensi.csv"))
    kom_rows = baca_csv(D("riset-komentar.csv"))
    kw_rows = baca_csv(D("riset-kata-kunci.csv"))
    kreatif = {}
    if os.path.exists(D("kreatif.json")):
        with open(D("kreatif.json"), encoding="utf-8") as f:
            kreatif = json.load(f)

    ref = analisa_referensi(ref_rows)
    kom = analisa_komentar(kom_rows)
    kw = analisa_kata_kunci(kw_rows)
    briefs = buat_brief(ref["pola"], kom, kreatif)
    tgl = hari_ini()

    asli = sum(1 for b in ref["baris"] if b["status"] == "asli")
    contoh = ref["n"] - asli
    ctx = {"referensi": ref, "komentar": kom, "kata_kunci": kw, "brief": briefs,
           "asli": asli, "contoh": contoh, "dibuat": tgl.isoformat()}

    print(f"Riset konten — {tgl.isoformat()}")
    print(f"  referensi   : {ref['n']} post ({asli} asli · {contoh} contoh) · confidence {ref['confidence']}")
    if ref["baris"]:
        t = ref["baris"][0]
        print(f"  outlier     : {fmt(t['lift'], 'x')} — {t['hook'][:56]}")
    print(f"  pola        : {len(ref['pola'])} kategori naik · dominan "
          f"{ref['pola'][0]['nama'] if ref['pola'] else '—'}")
    print(f"  komentar    : {kom['n']} kutipan · {kom['rekap'][0]['jenis'] if kom['rekap'] else '—'} terbanyak")
    print(f"  kata kunci  : {kw['n']} · dijawab halaman {kw['persen_tercakup']}% · {len(kw['celah'])} celah")
    print(f"  brief       : {len(briefs)}")
    if contoh:
        print(f"  PERINGATAN  : {contoh} baris masih berlabel contoh — ganti sebelum dipakai ambil keputusan.")

    if args.cek:
        return

    os.makedirs(OUT, exist_ok=True)
    brief_dir = os.path.join(OUT, "brief")
    os.makedirs(brief_dir, exist_ok=True)
    for lama in os.listdir(brief_dir):
        if lama.endswith(".md"):
            os.remove(os.path.join(brief_dir, lama))
    for b in briefs:
        with open(os.path.join(brief_dir, f"brief-{b['no']:02d}-{slug(b['sudut'])}.md"), "w",
                  encoding="utf-8") as f:
            f.write(brief_markdown(b, tgl))

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(dasbor(ctx, tgl))
    with open(os.path.join(OUT, "swipe-file.md"), "w", encoding="utf-8") as f:
        f.write(swipe_md(ctx, tgl))

    ringkas = {
        "dibuat": tgl.isoformat(),
        "referensi": ref["n"], "referensi_asli": asli, "referensi_contoh": contoh,
        "confidence": ref["confidence"],
        "outlier_teratas": (ref["baris"][0] if ref["baris"] else None),
        "pola": [{"nama": p["nama"], "n": p["n"], "lift_median": round(p["lift_median"], 2),
                  "sudut": p["sudut"]} for p in ref["pola"]],
        "komentar": kom["n"], "komentar_rekap": kom["rekap"],
        "kata_kunci": kw["n"], "persen_tercakup": kw["persen_tercakup"],
        "persen_persis": kw["persen_persis"],
        "celah": [{"kata_kunci": k["kata_kunci"], "prioritas": k["prioritas"],
                   "halaman": k["halaman"], "cakupan": k["cakupan"]} for k in kw["celah"]],
        "brief": [{"no": b["no"], "judul": b["judul"], "aset": b["aset"]} for b in briefs],
    }
    with open(os.path.join(OUT, "data.json"), "w", encoding="utf-8") as f:
        json.dump(ringkas, f, ensure_ascii=False, indent=2)

    print(f"  halaman     : riset/index.html · riset/swipe-file.md · {len(briefs)} brief")


if __name__ == "__main__":
    main()
