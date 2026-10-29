#!/usr/bin/env python3
"""
Studio konten — 10 tahap alur kerja D3 (Marketing) × D4 (Kreatif).

Menggabungkan kerangka "social media team" dari @dsqjaffa (10 folder / 50 agent)
dengan mesin riset yang sudah ada. Bedanya: di sini 50 slot itu dijalankan sebagai
**fungsi deterministik Python**, bukan 50 agent LLM yang masing-masing menagih token.
Yang tidak bisa dihitung mesin ditandai `manual` — bukan diklaim otomatis.

Tahap:
  01 niche          definisi ceruk, audiens, tawaran, kata terlarang, makna ganda
  02 pesaing        akun yang ditangkap, catatan industri, rencana video jawaban
  03 outlier        filter ceruk, ranking views/engagement, ranking simpan/bagikan, dead views
  04 kreator        kreator outlier, engagement per 1K views, syarat 2 outlier, watchlist
  05 hook           bank hook, grup struktur, hitung struktur, ranking lift median, pilih film pertama
  06 format         format terbaik, pemetaan gaya rekam, kuartal atas vs bawah, salin minggu ini
  07 skrip          5 hook teratas → skrip 7 detik, cocokkan suara, kutip sumber, loop berikutnya
  08 skala          bedah pemenang, simpan struktur, remix konsep, pola paling dibagikan
  09 lapor          tabel 10 teratas, brief Senin, putuskan (dobel/hentikan/uji), 5 skrip, laporan tim
  10 ops            jadwal berulang, cek pemakaian ulang, pembaca playbook, agen berulang

Keluaran:
    studio/index.html         dasbor 10 tahap
    studio/brief-senin.md     brief mingguan siap dibaca
    studio/skrip/*.md         5 skrip siap rekam
    studio/data.json          ringkasan mesin (dibaca papan & laporan)

Pakai:
    python3 tools/studio.py
    python3 tools/studio.py --cek     # ringkasan terminal saja
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import statistics
import sys
import unicodedata
from datetime import date, timedelta
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402
import riset  # noqa: E402  (mesin analisis yang sudah ada)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "studio")
D = lambda *p: os.path.join(ROOT, "data", *p)

NAMA_STRUKTUR = {k: n for k, n, _ in riset.HOOK}
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]


def tgl_id(t, panjang=True):
    return f"{t.day} {BULAN[t.month - 1]} {t.year}"


def tgl_pendek(t):
    return f"{t.day} {BULAN[t.month - 1][:3]} {t.year}"

# ── pemetaan 50 slot kerangka → siapa yang mengerjakan ─────────────────────
# otomatis = dihitung tools/studio.py · manual = owner · tidak = sengaja tidak dipakai
PETA = [
    ("01 niche research", [
        ("niche definition", "otomatis", "data/studio-niche.json → divalidasi, tampil di §1"),
        ("audience and offer", "otomatis", "4 segmen + tangga tawaran, dipakai menyusun skrip"),
        ("leaders and competitors", "manual", "data/studio-niche.json → `pesaing` (isi sendiri)"),
        ("search phrase finder", "otomatis", "gabungan kata kunci + pertanyaan komentar"),
        ("double-meaning excludes", "otomatis", "aturan makna ganda dicek ke daftar kata kunci"),
    ]),
    ("02 competitor tracking", [
        ("competitor agent", "otomatis", "akun pesaing dari data/riset-referensi.csv"),
        ("industry agent", "manual", "data/studio-industri.csv (dicatat manusia)"),
        ("creator tracker", "otomatis", "grup per akun → §4"),
        ("top 50 company ranker", "otomatis", "peringkat akun yang benar-benar ditangkap (bukan top-50 industri)"),
        ("answer video planner", "otomatis", "rencana video jawaban untuk 3 outlier pesaing teratas"),
    ]),
    ("03 outlier videos", [
        ("outlier finder", "otomatis", "lift = views ÷ median akun×format"),
        ("niche match filter", "otomatis", "cocokkan kata kunci ceruk ke hook/topik"),
        ("views + engagement ranker", "otomatis", "ranking lift & ER"),
        ("saves + shares ranker", "otomatis", "ranking simpan% & bagikan%"),
        ("dead views flag", "otomatis", "views < 50% baseline ditandai"),
    ]),
    ("04 outlier creators", [
        ("creator finder", "otomatis", "akun dengan ≥1 outlier"),
        ("engagement per 1K views", "otomatis", "interaksi ÷ views × 1000"),
        ("two outlier minimum", "otomatis", "syarat ≥2 outlier untuk masuk watchlist"),
        ("30 day history flag", "otomatis", "post ≤30 hari terakhir ≥3 → layak dipantau"),
        ("creator watchlist", "otomatis", "irisan dua syarat di atas"),
    ]),
    ("05 hooks", [
        ("hook bank", "otomatis", "data/studio-hooks.csv (30 hook)"),
        ("structure grouper", "otomatis", "10 struktur: " + ", ".join(sorted(NAMA_STRUKTUR.values())[:5]) + ", …"),
        ("structure counter", "otomatis", "jumlah hook per struktur"),
        ("median views ranker", "otomatis", "lift median struktur dari data referensi"),
        ("first film picker", "otomatis", "hook dengan lift tertinggi + aset siap + belum dipakai"),
    ]),
    ("06 formats & trends", [
        ("format finder", "otomatis", "ER median per platform × format"),
        ("filming style mapper", "otomatis", "5 gaya rekam → struktur yang cocok"),
        ("top vs bottom quarter", "otomatis", "kuartal lift atas vs bawah"),
        ("copy this week", "otomatis", "satu format prioritas minggu ini per platform"),
        ("formats to copy", "otomatis", "format dengan lift median ≥2 dan n ≥2"),
    ]),
    ("07 scripts", [
        ("top 5 hooks", "otomatis", "ranking struktur → 5 hook teratas"),
        ("script writer", "otomatis", "skrip 7 detik: hook → bukti → akibat → CTA"),
        ("voice matcher", "otomatis", "cek kata terlarang, panjang kalimat, superlatif, angka, CTA"),
        ("source citer", "otomatis", "tiap klaim wajib menyebut berkas data"),
        ("next script loop", "otomatis", "antrean 5 skrip berikutnya dari sisa bank"),
    ]),
    ("08 scaling", [
        ("winner breakdown", "otomatis", "bedah pemenang: hook, struktur, format, durasi, pilar"),
        ("structure keeper", "otomatis", "struktur pemenang disimpan sebagai pola wajib"),
        ("concept remixer", "otomatis", "3 konsep turunan per pemenang (produk/audiens berbeda)"),
        ("script per concept", "otomatis", "satu hook disiapkan per konsep"),
        ("most shared patterns", "otomatis", "pola dengan bagikan% tertinggi"),
    ]),
    ("09 reporting & briefs", [
        ("top 10 table", "otomatis", "10 post/aset teratas"),
        ("Monday brief", "otomatis", "studio/brief-senin.md"),
        ("double down, stop, test", "otomatis", "3 keputusan dari data, bukan selera"),
        ("five scripts", "otomatis", "studio/skrip/*.md"),
        ("team report", "otomatis", "hitungan per tahap → §10 & laporan/index.html"),
    ]),
    ("10 content operations", [
        ("Claude connector", "tidak", "tidak dipakai: tidak ada kredensial & tidak boleh mengarang akses"),
        ("Claude Code setup", "tidak", "tidak dipakai: pipeline berjalan lokal tanpa layanan luar"),
        ("agent playbook reader", "otomatis", "membaca skills/*.md + operasional/divisi/D3-D4"),
        ("agent reuse check", "otomatis", "deteksi hook/skrip nyaris duplikat"),
        ("recurring agent", "otomatis", "jadwal mingguan di studio/data.json + ops doc"),
    ]),
]

# ── template beat per struktur (dipakai script writer) ─────────────────────
BEAT = {
    "diagnosis": [
        "Penyebab tersering: gilingan terlalu halus untuk alat Anda.",
        "Kedua: air di atas 94°C. Ketiga: kopi lewat 21 hari dari tanggal sangrai.",
    ],
    "pengakuan": [
        "Skornya {skor}. Ambang kami 83, jadi batch itu tidak dikirim.",
        "Kami sangrai ulang minggu berikutnya dan catatannya tetap disimpan.",
    ],
    "larangan": [
        "Uap dapur masuk lewat valve, aroma bumbu ikut pindah ke biji.",
        "Cukup wadah kedap, tempat gelap, suhu ruang — tanpa kulkas.",
    ],
    "banding": [
        "Ijen 1.700–1.800 mdpl, proses natural: manis dan buah.",
        "Raung 422–443 mdpl: body tebal, cokelat gelap. Dua-duanya kopi Banyuwangi.",
    ],
    "angka": [
        "Tanggal sangrai, kode batch, level roast 1–5 — semuanya tercetak di label.",
        "Ketiganya juga tersimpan di catatan QC tiap batch.",
    ],
    "proses": [
        "Suhu turun, first crack lewat, kami berhenti di titik development batch ini.",
        "Dua puluh detik lebih lama bisa mengubah rasanya, jadi berhenti di catatan.",
    ],
    "tutorial": [
        "Lima belas gram kopi, 250 ml air 94°C, tunggu empat menit, aduk, diamkan.",
        "Tanpa grinder? Kami giling sesuai alat yang Anda sebutkan.",
    ],
    "otoritas": [
        "Kami cicipi lima atribut: aroma, acidity, body, sweetness, aftertaste.",
        "Ambang lolos 83. Di bawah itu tidak dikirim, dan catatannya bisa dibuka.",
    ],
    "harga": [
        "Peta Rasa 3 × 100 g Rp79.000 — sekitar Rp263 per gram.",
        "Dibeli terpisah Rp88.000. Harga di situs dan di WhatsApp sama.",
    ],
    "pov": [
        "Kopi bagus disimpan di dekat bumbu dapur, lalu rasanya jadi aneh.",
        "Pindahkan ke wadah kedap, jauh dari sinar dan panas.",
    ],
    "lain": [
        "Satu hal yang jarang dicetak brand kopi: tanggal sangrai.",
        "Kami mencetaknya, plus kode batch untuk tiap kantong.",
    ],
}

# isi yang ditulis khusus per hook — template per struktur tidak selalu cocok dengan pertanyaannya
BEAT_KHUSUS = {
    "Kopi pahit padahal baru beli? Cek tiga hal ini.": (
        "Pertama: gilingan terlalu halus untuk alat Anda. Kedua: air di atas 94°C.",
        "Ketiga: kopi sudah lewat 21 hari dari tanggal sangrai.",
        ["catalog.json", "batch-qc.csv"]),
    "Kami buang 4 kg bulan ini. Ini yang terjadi.": (
        "Dua batch gagal di skor 81,5 dan 82 — ambang kami 83.",
        "Tidak dikirim. Disangrai ulang, dan kerugiannya kami tanggung sendiri.",
        ["batch-qc.csv", "batch-qc.csv"]),
    "Jangan simpan kopi di kulkas.": (
        "Uap dapur masuk lewat valve, aroma bumbu ikut pindah ke biji.",
        "Cukup wadah kedap, tempat gelap, suhu ruang. Puncak rasa 7–21 hari.",
        ["studio-niche.json", "catalog.json"]),
    "Kenapa kopi kafe terasa lebih kuat dari kopi rumahan.": (
        "Biasanya bukan biji: rasio 1:15 dan gilingan lebih halus mengekstrak lebih banyak.",
        "Coba 15 g kopi untuk 225 ml air, lalu bandingkan dengan resep Anda sekarang.",
        ["catalog.json", "catalog.json"]),
    "Rp23.000 vs Rp152.000: bedanya bukan cuma berat.": (
        "Rp23.000 itu 100 g robusta Raung. Rp152.000 itu 500 g arabika Ijen.",
        "Per gram: Rp230 lawan Rp304. Bedanya di proses dan ketinggian tanam.",
        ["catalog.json", "catalog.json"]),
    "Arabika Ijen vs robusta Raung, satu meja.": (
        "Ijen 1.700–1.800 mdpl, proses natural: manis, buah, aftertaste panjang.",
        "Raung 422–443 mdpl: body tebal, cokelat gelap, pahit halus di akhir.",
        ["catalog.json", "catalog.json"]),
    "Yang kami periksa sebelum satu batch boleh dikirim.": (
        "Lima atribut: aroma, acidity, body, sweetness, aftertaste. Ambang 83.",
        "Di bawah ambang, batch disangrai ulang — bukan dikirim dengan catatan.",
        ["batch-qc.csv", "batch-qc.csv"]),
    "Satu kantong, tiga angka yang bisa Anda cek.": (
        "Tanggal sangrai, kode batch, level roast 1–5 — semuanya tercetak di label.",
        "Cocokkan kode batch dengan catatan QC yang kami simpan.",
        ["brand/label-ijen.png", "batch-qc.csv"]),
    "Gilingan Anda menentukan 40% rasanya.": (
        "Terlalu halus: pahit dan sepat. Terlalu kasar: asam dan hambar.",
        "Sebut alat seduh Anda, kami giling di ukuran yang sesuai.",
        ["catalog.json", "catalog.json"]),
    "POV: kopi mahal disimpan di dekat bumbu dapur.": (
        "Aroma bumbu masuk lewat valve, dan rasanya ikut berubah dalam hitungan hari.",
        "Pindahkan ke wadah kedap, jauh dari sinar dan panas.",
        ["studio-niche.json", "studio-niche.json"]),
    "Cara menyeduh tanpa alat mahal: 3 langkah.": (
        "Lima belas gram kopi, 250 ml air 94°C, tunggu empat menit.",
        "Aduk, diamkan satu menit, lalu tuang. Tanpa mesin, tanpa filter kertas.",
        ["catalog.json", "catalog.json"]),
    "Kami tidak menurunkan ambang walau stok kosong.": (
        "Ambang tetap 83. Stok kosong bukan alasan mengirim batch 81,5.",
        "Yang terjadi: satu SKU kosong beberapa hari. Itu pilihan kami.",
        ["batch-qc.csv", "batch-qc.csv"]),
    "Harga per gram: cara adil membandingkan kopi.": (
        "Rp23.000 per 100 g = Rp230 per gram. Rp152.000 per 500 g = Rp304 per gram.",
        "Harga di situs dan di WhatsApp sama; tidak ada harga khusus yang disembunyikan.",
        ["catalog.json", "catalog.json"]),
    "Kode batch: kalau rasanya beda, sebutkan ini.": (
        "Tiap kantong membawa kode batch dan tanggal sangrai di label.",
        "Sebut kodenya lewat WhatsApp, kami buka catatan QC batch itu.",
        ["batch-qc.csv", "batch-qc.csv"]),
    "Kopi tidak punya tanggal kedaluwarsa yang jujur.": (
        "Yang menentukan bukan kedaluwarsa, tapi jarak dari tanggal sangrai.",
        "Puncak rasa 7–21 hari. Lewat 60 hari masih aman, tapi tidak lagi sama.",
        ["catalog.json", "catalog.json"]),
    "Sehari sebelum dikirim, kopi ini masih di drum.": (
        "Sangrai, dinginkan, lalu resting 12–24 jam sebelum dikemas.",
        "Order sebelum 15.00 WIB dikirim hari itu, dengan tanggal sangrai tercetak.",
        ["batch-qc.csv", "batch-qc.csv"]),
    "Resi dikirim hari itu, bukan besok.": (
        "Order sebelum 15.00 WIB diproses dan diserahkan ke kurir hari yang sama.",
        "Kalau lewat jam itu, resi baru keluar besok pagi — kami tulis apa adanya.",
        ["catalog.json", "catalog.json"]),
    "Tiga hal yang membuat kopi rumahan terasa hambar.": (
        "Gilingan terlalu kasar. Air terlalu dingin. Kopi lewat 30 hari dari sangrai.",
        "Cek satu per satu; yang tersering ternyata gilingan.",
        ["catalog.json", "catalog.json"]),
}

SUMBER_BEAT = {
    "diagnosis": ["catalog.json", "catalog.json"],
    "pengakuan": ["batch-qc.csv", "batch-qc.csv"],
    "larangan": ["studio-niche.json", "studio-niche.json"],
    "banding": ["catalog.json", "catalog.json"],
    "angka": ["brand/label-ijen.png", "batch-qc.csv"],
    "proses": ["batch-qc.csv", "batch-qc.csv"],
    "tutorial": ["catalog.json", "catalog.json"],
    "otoritas": ["batch-qc.csv", "batch-qc.csv"],
    "harga": ["catalog.json", "catalog.json"],
    "pov": ["studio-niche.json", "studio-niche.json"],
    "lain": ["catalog.json", "batch-qc.csv"],
}

CTA = "Pesan lewat WhatsApp — sebutkan metode seduh & kota Anda."
CTA_KHUSUS = {
    "Resi dikirim hari itu, bukan besok.": "Order lewat WhatsApp sebelum 15.00 WIB.",
    "Sehari sebelum dikirim, kopi ini masih di drum.": "Order lewat WhatsApp sebelum 15.00 WIB.",
    "Kami buang 4 kg bulan ini. Ini yang terjadi.": "Tanya kode batch lewat WhatsApp — kami buka catatannya.",
    "Kami tidak menurunkan ambang walau stok kosong.": "Tanya kode batch lewat WhatsApp — kami buka catatannya.",
    "Kode batch: kalau rasanya beda, sebutkan ini.": "Sebut kode batch lewat WhatsApp — kami buka catatannya.",
    "Satu kantong, tiga angka yang bisa Anda cek.": "Cek label, lalu tanya apa pun lewat WhatsApp.",
    "Cara menyeduh tanpa alat mahal: 3 langkah.": "Tanya ukuran giling lewat WhatsApp, sebut alat seduh Anda.",
    "Gilingan Anda menentukan 40% rasanya.": "Tanya ukuran giling lewat WhatsApp, sebut alat seduh Anda.",
}
VISUAL = {
    "diagnosis": "Tangan menimbang kopi → close-up gilingan → cangkir di meja",
    "pengakuan": "Layar catatan QC (blur nama) → tumpukan bungkus ditolak",
    "larangan": "Kopi di dalam kulkas → diangkat → dipindah ke wadah kedap",
    "banding": "Dua kantong berdampingan → tuang biji ke dua mangkuk",
    "angka": "Tiga kartu teks berisi angka → kantong kopi & alat seduh di meja",
    "proses": "Drum sangrai → asap tipis → tuang biji ke cooling tray",
    "tutorial": "Cangkir kosong → tuang air → aduk → diamkan",
    "otoritas": "Meja cupping: sendok, form skor, 3 cangkir",
    "harga": "Tiga kantong Peta Rasa → label harga → kotak ditutup",
    "pov": "Kulkas/bumbu dapur → kopi dipindah",
    "lain": "Kantong kopi berputar → zoom label",
}

CSS = """
:root{--paper:#F5EFE4;--paper2:#EFE6D6;--ink:#16110D;--muted:#6b6156;--orange:#E1542B;
--gold:#D9A441;--espresso:#4A2C1A;--line:1px solid rgba(22,17,13,.14);--green:#1f6b3a}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 Inter,system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:34px clamp(16px,4vw,40px) 76px}
h1{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(30px,5vw,47px);line-height:.98;
letter-spacing:-.035em;margin:6px 0 8px;font-weight:800}
h2{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(20px,2.5vw,27px);letter-spacing:-.02em;
margin:42px 0 4px;border-top:2px solid var(--ink);padding-top:13px}
h2 small{display:block;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);
font-weight:600;margin-bottom:6px}
h3{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:16.5px;margin:0 0 4px}
.kicker{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.lede{max-width:74ch;color:var(--muted);margin:0 0 8px;font-size:14.4px}
.grid{display:grid;gap:13px}
.kpi{grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin-top:16px}
.kpi div{border:var(--line);border-radius:8px;padding:12px 14px;background:#fff8}
.kpi span{display:block;font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.kpi b{display:block;font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:24px;letter-spacing:-.02em;line-height:1.1;margin:4px 0 1px}
.kpi em{font-size:11.5px;color:var(--muted);font-style:normal}
table{width:100%;border-collapse:collapse;font-size:13.1px;margin-top:10px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid rgba(22,17,13,.12);vertical-align:top}
th{font-size:10.4px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);font-weight:600}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr:last-child td{border-bottom:0}
tr.grup td{background:var(--paper2);font-weight:600;font-size:12px;letter-spacing:.05em}
.pill{display:inline-block;font-size:10.3px;padding:2px 7px;border-radius:99px;border:1px solid;white-space:nowrap}
.pill.ok{color:var(--green);border-color:var(--green);background:#e8f2ea}
.pill.warn{color:#8a5a00;border-color:#b78621;background:#fbf1d9}
.pill.dim{color:var(--muted);border-color:rgba(22,17,13,.2)}
.pill.hot{color:#fff;border-color:var(--orange);background:var(--orange)}
.cards{grid-template-columns:repeat(auto-fit,minmax(300px,1fr));margin-top:14px}
.card{border:var(--line);border-radius:8px;padding:15px 17px;background:#fff8}
.card .meta{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 5px}
.card ul{margin:6px 0 0;padding-left:17px;font-size:13.2px}
.hook{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:15px;background:var(--paper2);
padding:7px 11px;border-radius:4px;margin:7px 0;line-height:1.3}
.beat{display:grid;grid-template-columns:56px 1fr;gap:10px;padding:7px 0;border-bottom:1px dashed rgba(22,17,13,.16);font-size:13.4px}
.beat:last-child{border-bottom:0}
.beat b{font-variant-numeric:tabular-nums;color:var(--orange)}
.note{border-left:4px solid var(--gold);background:#fbf1d9;padding:11px 15px;border-radius:4px;font-size:13px;margin:16px 0 0}
.note b{display:block;margin-bottom:2px}
code{background:var(--paper2);padding:1px 5px;border-radius:3px;font-size:12px}
footer{margin-top:42px;border-top:2px solid var(--ink);padding-top:13px;font-size:12px;color:var(--muted);
display:flex;flex-wrap:wrap;gap:8px 22px;justify-content:space-between}
a{color:inherit}
"""


# ─────────────────────────────── utilitas ─────────────────────────────────
def baca_csv(*path):
    p = os.path.join(ROOT, *path)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def baca_json(*path, default=None):
    p = os.path.join(ROOT, *path)
    if not os.path.exists(p):
        return default if default is not None else {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def angka_id(v, d=1, satuan=""):
    if v is None:
        return "—"
    return f"{v:.{d}f}".replace(".", ",") + satuan


def rp(n):
    return "Rp" + f"{int(n):,}".replace(",", ".")


def token(teks):
    t = unicodedata.normalize("NFKD", teks or "").lower()
    return {w for w in re.findall(r"[a-z0-9]+", t) if len(w) > 3}


def kemiripan(a, b):
    ta, tb = token(a), token(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def slug(s):
    t = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:44] or "skrip"


STOP_FRASA = {
    "yang", "untuk", "dan", "dengan", "apa", "bisa", "saya", "aku", "ada", "itu", "ini",
    "kah", "nya", "sih", "ya", "atau", "kalau", "malah", "baru", "tapi", "kok", "berapa",
    "mana", "gak", "tidak", "mau", "beli", "juga", "biar", "dulu", "lebih", "sangat",
    "simpan", "kirim", "buang", "berani", "kira", "coba", "pakai", "bikin", "jadi", "masuk",
    "padahal", "banget", "dong", "gimana", "kenapa", "harus", "sudah", "masih", "sama",
    "seperti", "kayak", "begitu", "gitu", "nih", "deh", "pernah", "waktu", "bulan",
}


def persen(a, b):
    return round(a / b * 100, 1) if b else 0.0


# ────────────────────────── 01 · niche research ───────────────────────────
def tahap_niche(niche, kom_rows, com_rows):
    kata_kunci = baca_csv("data", "riset-kata-kunci.csv")

    # pencari frasa: gabungkan kata kunci + pertanyaan pembeli yang belum terwakili
    ada = {" ".join(r["kata_kunci"].lower().split()) for r in kata_kunci}
    usulan = []
    for k in kom_rows:
        if k["jenis"] not in ("pertanyaan", "keberatan"):
            continue
        inti = []
        for w in re.findall(r"[a-z]+", k["kutipan"].lower()):
            if w.endswith("nya") and len(w) > 6:
                w = w[:-3]
            if w in STOP_FRASA or w in inti:
                continue
            inti.append(w)
        if not inti:
            continue
        frasa = " ".join(inti[:4])
        if "kopi" not in frasa:
            frasa = "kopi " + frasa
        if frasa in ada or any(frasa in x for x in ada):
            continue
        if frasa not in [u["frasa"] for u in usulan]:
            usulan.append({"frasa": frasa, "dari": k["kutipan"][:64], "status": "usulan — cek manual"})

    # pemeriksaan makna ganda terhadap daftar kata kunci
    ganda = []
    for aturan in niche.get("pengecualian_makna_ganda", []):
        frasa = aturan["frasa"].lower()
        kena = [r["kata_kunci"] for r in kata_kunci
                if re.search(rf"\b{re.escape(frasa)}\b", r["kata_kunci"].lower())]
        ganda.append({**aturan, "kena": kena, "aman": not kena})

    # peringkat pesaing: pesaing manual + akun yang ditangkap
    akun = {}
    for r in com_rows:
        akun.setdefault(r["akun"], []).append(r)
    peringkat = []
    for nama, items in akun.items():
        views = [i["views"] for i in items]
        peringkat.append({"akun": nama, "post": len(items),
                          "views_median": statistics.median(views) if views else 0,
                          "pengikut": max((i["followers"] for i in items), default=0)})
    peringkat.sort(key=lambda x: x["views_median"], reverse=True)

    return {
        "niche": niche["niche"], "audiens": niche["audiens"], "tawaran": niche["tawaran"],
        "bahasa": niche["bahasa"], "pesaing_manual": niche.get("pesaing", []),
        "gaya": niche.get("gaya_rekam", []),
        "usulan_frasa": usulan[:8], "makna_ganda": ganda, "peringkat_akun": peringkat,
    }


# ─────────────────────── 02 · competitor tracking ─────────────────────────
def tahap_pesaing(pesaing, outlier_rows, industri):
    industri_rows = [{"tanggal": r.get("tanggal", ""), "sumber": r.get("sumber", ""),
                      "topik": r.get("topik", ""), "dampak": r.get("dampak", ""),
                      "tindakan": r.get("tindakan", "")} for r in industri]

    # rencana video jawaban untuk outlier pesaing (bukan milik kita)
    asing = [r for r in outlier_rows if (r["lift"] or 0) >= 2][:3]
    if not asing:
        asing = outlier_rows[:3]
    rencana = []
    for r in asing:
        struktur = r["hook_kategori"]
        sudut, penjelasan, hook_kita, aset = riset.SUDUT.get(struktur, riset.SUDUT_LAIN)
        rencana.append({
            "acuan": r["hook"], "platform": r["platform"], "lift": r["lift"],
            "struktur": NAMA_STRUKTUR.get(struktur, struktur),
            "jawaban": hook_kita, "sudut": sudut, "aset": aset,
            "alasan": f"pola yang sama bekerja {angka_id(r['lift'], satuan='×')} untuk akun itu; kita pakai dengan bukti milik sendiri",
        })
    return {"industri": industri_rows, "jawaban": rencana}


# ────────────────────────── 03 · outlier videos ───────────────────────────
def tahap_outlier(ref, niche_kata):
    hit = []
    for b in ref["baris"]:
        teks = f"{b['hook']} {b['topik']}".lower()
        cocok = any(k in teks for k in niche_kata)
        b = {**b, "niche": cocok,
             "dead": (b["lift"] is not None and b["lift"] < 0.5)}
        hit.append(b)

    dalam = [b for b in hit if b["niche"]]
    return {
        "baris": hit,
        "dalam_ceruk": len(dalam),
        "di_luar": len(hit) - len(dalam),
        "rank_views": sorted(dalam, key=lambda b: b["views"], reverse=True)[:8],
        "rank_engagement": sorted(dalam, key=lambda b: b["er"], reverse=True)[:8],
        "rank_simpan": sorted(dalam, key=lambda b: b["simpan_rate"], reverse=True)[:8],
        "dead": [b for b in dalam if b["dead"]],
    }


# ───────────────────────── 04 · outlier creators ──────────────────────────
def tahap_kreator(outlier_rows, hari):
    grup = {}
    for b in outlier_rows:
        grup.setdefault(b["akun"], []).append(b)

    hasil = []
    for nama, items in grup.items():
        views = [i["views"] for i in items]
        median = statistics.median(views) if views else 0
        outliers = [i for i in items if (i["lift"] or 0) >= 2]
        interaksi = sum(i["interaksi"] for i in items)
        tgl_terakhir = max((i["tanggal"] for i in items), default="")
        try:
            baru = (hari - date.fromisoformat(tgl_terakhir)).days <= 30
        except Exception:
            baru = False
        hasil.append({
            "akun": nama, "platform": sorted({i["platform"] for i in items}),
            "post": len(items), "views_median": median,
            "outlier": len(outliers), "outlier_besar": sum(1 for i in items if (i["lift"] or 0) >= 5),
            "per_1k": round(interaksi / sum(views) * 1000, 1) if sum(views) else 0,
            "riwayat_30h": baru, "terakhir": tgl_terakhir,
            "watchlist": len(outliers) >= 2 and baru,
        })
    hasil.sort(key=lambda x: (x["outlier"], x["per_1k"]), reverse=True)
    return {"baris": hasil, "watchlist": [h for h in hasil if h["watchlist"]]}


# ─────────────────────────────── 05 · hooks ───────────────────────────────
def tahap_hook(bank, ref, manifest):
    aset = {i["id"]: i for i in manifest.get("items", [])}
    lift_struktur = {p["kunci"]: p for p in ref["pola"]}

    for h in bank:
        p = lift_struktur.get(h["struktur"])
        h["lift_median"] = p["lift_median"] if p else None
        h["n_struktur"] = p["n"] if p else 0
        h["aset_ada"] = (h["aset"] in aset) if h["aset"] else False

    grup = {}
    for h in bank:
        grup.setdefault(h["struktur"], []).append(h)
    grouper = [{"struktur": k, "nama": NAMA_STRUKTUR.get(k, k), "n": len(v),
                "belum": sum(1 for x in v if x["status"] != "dipakai"),
                "lift_median": (lift_struktur.get(k) or {}).get("lift_median")}
               for k, v in grup.items()]
    grouper.sort(key=lambda x: (x["lift_median"] or 0, x["n"]), reverse=True)

    # pilih film pertama: lift tertinggi + aset siap + belum dipakai
    calon = [h for h in bank if h["status"] != "dipakai" and h["aset_ada"]]
    calon.sort(key=lambda h: (h["lift_median"] or 0), reverse=True)
    return {"bank": bank, "grouper": grouper, "total": len(bank),
            "belum": sum(1 for h in bank if h["status"] != "dipakai"),
            "film_pertama": calon[0] if calon else None,
            "siap": calon}


# ────────────────────────────── 06 · formats ──────────────────────────────
def tahap_format(ref, niche_gaya, outlier):
    matriks = ref["matriks"]
    copy_week = {}
    for m in matriks:
        if m["platform"] not in copy_week and (m["lift_median"] or 0) >= 1:
            copy_week[m["platform"]] = m

    # kuartal atas vs bawah berdasarkan lift
    urut = sorted([b for b in outlier["baris"] if b["niche"] and b["lift"]],
                  key=lambda b: b["lift"])
    n = len(urut)
    q = max(1, n // 4)
    bawah, atas = urut[:q], urut[-q:]
    def ringkas(rows):
        if not rows:
            return {}
        return {
            "n": len(rows),
            "lift_median": statistics.median([r["lift"] for r in rows]),
            "struktur": {NAMA_STRUKTUR.get(k, k): sum(1 for r in rows if r["hook_kategori"] == k)
                         for k in {r["hook_kategori"] for r in rows}},
            "format": {f: sum(1 for r in rows if r["format"] == f) for f in {r["format"] for r in rows}},
            "detik_median": statistics.median([r["detik"] for r in rows if r["detik"]]) if any(r["detik"] for r in rows) else 0,
            "contoh": [r["hook"] for r in rows[-2:]],
        }

    gaya_peta = []
    for g in niche_gaya:
        cocok = [h for h in g["cocok_untuk"]]
        gaya_peta.append({**g, "jumlah_hook": sum(1 for b in ref["baris"] if b["hook_kategori"] in cocok)})

    return {
        "copy_week": list(copy_week.values()),
        "to_copy": [m for m in matriks if (m["lift_median"] or 0) >= 2 and m["n"] >= 2],
        "atas": ringkas(atas), "bawah": ringkas(bawah),
        "gaya": gaya_peta,
    }


# ─────────────────────────────── 07 · skrip ───────────────────────────────
def cek_suara(teks, bahasa):
    pelanggaran = []
    rendah = teks.lower()
    for kata in bahasa.get("kata_dilarang", []):
        if kata.lower() in rendah:
            pelanggaran.append(f"kata terlarang: “{kata}”")
    for kata in bahasa.get("superlatif_dilarang", []):
        if re.search(rf"\b{kata}\b", rendah):
            pelanggaran.append(f"superlatif: “{kata}”")
    kalimat = [k.strip() for k in re.split(r"[.!?]\s+|\.$", teks) if k.strip()]
    panjang_maks = bahasa.get("panjang_kalimat_maks", 18)
    for k in kalimat:
        if len(k.split()) > panjang_maks:
            pelanggaran.append(f"kalimat {len(k.split())} kata (maks {panjang_maks})")
    if not re.search(r"\d", teks):
        pelanggaran.append("tidak ada angka/tanggal")
    if "whatsapp" not in rendah:
        pelanggaran.append("tidak ada CTA WhatsApp")
    skor = max(0, 100 - 12 * len(pelanggaran))
    return skor, pelanggaran


def tulis_skrip(hook, data, nomor, tgl):
    struktur = hook["struktur"]
    khusus = BEAT_KHUSUS.get(hook["hook"])
    if khusus:
        isi = list(khusus[:2])
        sumber_isi = list(khusus[2])
    else:
        isi = BEAT.get(struktur, BEAT["lain"])
        sumber_isi = SUMBER_BEAT.get(struktur, SUMBER_BEAT["lain"])
    beats = [{"detik": 3, "teks": hook["hook"], "sumber": sumber_isi[0]}]
    for teks, sumber in zip(isi, sumber_isi):
        beats.append({"detik": 2, "teks": teks.format(skor=data["skor"]), "sumber": sumber})
    beats.append({"detik": 2, "teks": CTA_KHUSUS.get(hook["hook"], CTA), "sumber": None})

    teks_penuh = " ".join(b["teks"] for b in beats)
    skor, pelanggaran = cek_suara(teks_penuh, data["bahasa"])
    sumber = sorted({b["sumber"] for b in beats if b["sumber"]})
    return {
        "no": nomor, "judul": hook["hook"], "struktur": struktur,
        "nama_struktur": NAMA_STRUKTUR.get(struktur, struktur), "pilar": hook["pilar"],
        "aset": hook["aset"], "aset_ada": hook["aset_ada"],
        "lift_median": hook["lift_median"], "beats": beats, "total_detik": sum(b["detik"] for b in beats),
        "visual": VISUAL.get(struktur, VISUAL["lain"]), "sumber": sumber,
        "suara_skor": skor, "pelanggaran": pelanggaran,
        "status": "siap rekam" if skor >= 88 and hook["aset_ada"] else "perlu perbaikan",
    }


def skrip_md(s, tgl):
    beats = "\n".join(
        f'| {i+1} | {b["detik"]}s | {b["teks"]} | {b["sumber"] or "—"} |'
        for i, b in enumerate(s["beats"]))
    sumber = ", ".join(f"`{x}`" for x in s["sumber"]) or "—"
    pelanggaran = "\n".join(f"- {p}" for p in s["pelanggaran"]) or "- tidak ada"
    return f"""# Skrip {s['no']:02d} — {s['nama_struktur']} · {s['pilar']}

> Dibuat {tgl.isoformat()} oleh `tools/studio.py` · status **{s['status']}** ·
> skor suara {s['suara_skor']}/100 · struktur ini naik {('%.1f×' % s['lift_median']).replace('.', ',') if s['lift_median'] else '—'} di data referensi.

**Hook (0–3 detik):**
```
{s['judul']}
```

| # | Durasi | Teks di layar | Sumber klaim |
| ---: | ---: | --- | --- |
{beats}

**Visual (shot list):** {s['visual']}

**Aset:** `{s['aset'] or '—'}` — {"ada di manifest" if s['aset_ada'] else "belum ada, render dulu"}.

**Sumber data:** {sumber}

**Cek suara:** {s['suara_skor']}/100

{pelanggaran}

**Aturan:** adaptasi pola dari data referensi — jangan menyalin hook, footage, atau audio akun lain.
Jangan menyebut Nocturne sebagai roastery. Semua angka wajib bisa dilacak ke berkas di atas.
"""


def tahap_skrip(hooks, data, tgl, jumlah=5):
    dipakai = {s["judul"] for s in data.get("skrip_lama", [])}
    calon = [h for h in hooks["siap"] if h["hook"] not in dipakai]
    calon.sort(key=lambda h: (h["lift_median"] or 0, h["hook"]), reverse=True)
    terpilih = calon[:jumlah]
    skrip = [tulis_skrip(h, data, i + 1, tgl) for i, h in enumerate(terpilih)]
    sisa = [h for h in calon[jumlah:]]
    return {"skrip": skrip, "antrean": [h["hook"] for h in sisa[:8]], "sisa": len(sisa)}


# ─────────────────────────────── 08 · skala ───────────────────────────────
def tahap_skala(outlier, ref):
    pemenang = [b for b in outlier["baris"] if b["niche"] and (b["lift"] or 0) >= 2]
    pemenang.sort(key=lambda b: b["lift"], reverse=True)
    bedah = []
    for b in pemenang[:3]:
        bedah.append({
            "hook": b["hook"], "platform": b["platform"], "format": b["format"],
            "lift": b["lift"], "er": b["er"], "detik": b["detik"],
            "struktur": NAMA_STRUKTUR.get(b["hook_kategori"], b["hook_kategori"]),
            "kunci": b["hook_kategori"],
            "alasan": b["catatan"] or "—",
            "simpan": b["simpan_rate"],
        })
    remix = []
    for b in bedah:
        sudut, penjelasan, hook_kita, aset = riset.SUDUT.get(b["kunci"], riset.SUDUT_LAIN)
        for i, arah in enumerate([
            ("ganti produk", "versi untuk SKU lain: pakai angka batch & harga SKU itu"),
            ("ganti audiens", "versi untuk segmen lain: bahasanya lebih teknis/lebih awam"),
            ("ganti format", "versi carousel 4:5 dari hook yang sama, 3 slide"),
        ]):
            remix.append({"dari": b["hook"], "jenis": arah[0], "konsep": f"{sudut} — {arah[1]}",
                          "hook": hook_kita, "aset": aset})

    dibagikan = sorted([b for b in outlier["baris"] if b["niche"]],
                       key=lambda b: persen(b["interaksi"], b["views"]), reverse=True)[:5]
    return {"pemenang": bedah, "remix": remix,
            "paling_dibagikan": [{"hook": b["hook"], "struktur": NAMA_STRUKTUR.get(b["hook_kategori"], "—"),
                                  "interaksi_pct": persen(b["interaksi"], b["views"])} for b in dibagikan]}


# ─────────────────────────────── 09 · lapor ───────────────────────────────
def tahap_lapor(hooks, skrip, kreator, outlier, skala, ind, tgl):
    top10 = sorted([b for b in outlier["baris"] if b["niche"]],
                   key=lambda b: b["lift"] or 0, reverse=True)[:10]

    # dobel / hentikan / uji — aturan tetap, bukan selera
    dobel = [p for p in top10 if (p["lift"] or 0) >= 2][:2]
    struktur_kuat = skala["pemenang"][0]["struktur"] if skala["pemenang"] else "—"
    hentikan = [b for b in outlier["baris"] if b["niche"] and (b["lift"] or 0) < 0.9][:2]
    uji = [s["judul"] for s in skrip["skrip"] if s["status"] == "siap rekam"][:1]

    return {
        "top10": top10,
        "dobel": [{"hook": p["hook"], "struktur": NAMA_STRUKTUR.get(p["hook_kategori"], "—"),
                   "lift": p["lift"]} for p in dobel],
        "dobel_struktur": struktur_kuat,
        "hentikan": [{"hook": b["hook"], "lift": b["lift"]} for b in hentikan],
        "uji": uji,
        "tim": {"hook_bank": hooks["total"], "hook_belum": hooks["belum"],
                "skrip": len(skrip["skrip"]), "siap_rekam": sum(1 for s in skrip["skrip"] if s["status"] == "siap rekam"),
                "watchlist": len(kreator["watchlist"]), "outlier_ceruk": outlier["dalam_ceruk"]},
    }


def brief_md(d, tgl):
    top = "\n".join(
        f'| {i+1} | {escape(b["hook"])} | {b["platform"]}/{b["format"]} | '
        f'{angka_id(b["lift"] or 0, satuan="×")} | {angka_id(b["er"], satuan="%")} | {escape(b["status"])} |'
        for i, b in enumerate(d["lapor"]["top10"]))
    skrip = "\n".join(
        f'- **Skrip {s["no"]:02d}** ({s["nama_struktur"]}) — “{s["judul"]}” · suara {s["suara_skor"]}/100 · '
        f'aset `{s["aset"]}`' for s in d["skrip"]["skrip"])
    watch = "\n".join(f'- {w["akun"]} — {w["outlier"]} outlier, {w["per_1k"]} interaksi/1K views'
                      for w in d["kreator"]["watchlist"]) or "- belum ada akun yang lolos dua syarat"
    industri = "\n".join(f'- {i["tanggal"]} · {i["topik"]} → {i["tindakan"]}' for i in d["pesaing"]["industri"])
    return f"""# Brief Senin — {tgl_id(tgl)}

> Dibuat otomatis oleh `tools/studio.py` ({d["dibuat"]}). Semua angka berasal dari `data/riset-*.csv`,
> `data/studio-hooks.csv`, dan `data/kreatif.json`. Baca 5 menit, lalu putuskan.
>
> **Status data: {d["confidence"]}** — {d["n_ref"]} baris referensi, belum ada yang `asli`.
> Keputusan di bawah adalah contoh penerapan aturan, bukan kesimpulan pasar. Isi baris asli dulu.

## 1 · Tabel 10 teratas (post yang naik, dalam ceruk)

| # | Hook | Platform/format | Lift | ER | Status data |
| ---: | --- | --- | ---: | ---: | --- |
{top}

## 2 · Putuskan: dobel, hentikan, uji

| Keputusan | Isi | Alasan |
| --- | --- | --- |
| **DOBEL** | pola “{d['lapor']['dobel_struktur']}” | struktur dengan lift median tertinggi di data |
| **HENTIKAN** | {" ; ".join(p['hook'] for p in d['lapor']['hentikan']) or "tidak ada yang di bawah 0,9×"} | lift < 0,9× — kalah dari kebiasaan akun |
| **UJI** | {" ; ".join(d['lapor']['uji']) or "belum ada skrip siap"} | satu eksperimen per minggu, bukan lima |

## 3 · Lima skrip siap rekam

{skrip}

Berkas lengkap: `studio/skrip/`. Setelah direkam, ubah status hook di `data/studio-hooks.csv`
menjadi `dipakai` agar tidak dipilih lagi.

## 4 · Watchlist kreator

{watch}

## 5 · Catatan industri

{industri}

## 6 · Yang tidak dikerjakan minggu ini

- Iklan berbayar: tunggu sampai biaya per chat organik terukur.
- Kanal baru: hanya setelah kanal berjalan stabil 4 minggu.
- 50 agent LLM: diganti 10 tahap deterministik di `tools/studio.py` (0 token per tahap).

**Batas:** brief ini merencanakan konten, bukan memposting. Unggahan, balas chat, dan pembayaran
tetap di tangan Anda.
"""


# ──────────────────────────────── 10 · ops ────────────────────────────────
JADWAL = [
    ("Senin", "Baca brief + pilih 1 keputusan", "D3", "studio/brief-senin.md"),
    ("Senin", "Sangrai + catat batch", "D1", "data/batch-qc.csv"),
    ("Selasa", "Tambah 5 baris referensi + 3 komentar", "D3", "data/riset-*.csv"),
    ("Selasa", "Jalankan studio + tulis caption", "D3", "python3 tools/studio.py"),
    ("Rabu", "Rekam 8–10 klip sesuai 5 skrip", "D4", "studio/skrip/*.md"),
    ("Rabu", "Pipeline B2B 5 pesan", "D2", "komersial/pipeline-b2b.csv"),
    ("Kamis", "Cupping + gerbang klaim aset minggu depan", "D1+D7", "data/batch-qc.csv"),
    ("Jumat", "Kas, margin, biaya per chat", "D6", "data/kpi.csv"),
    ("Sabtu", "Packing + kirim + render aset", "D5+D4", "konten/"),
    ("Minggu", "Review papan + 3 prioritas", "owner", "dashboard/index.html"),
]


def tahap_ops(hooks, skrip, docs, hari):
    # cek pemakaian ulang: hook nyaris duplikat
    duplikat = []
    bank = hooks["bank"]
    for i, a in enumerate(bank):
        for b in bank[i + 1:]:
            k = kemiripan(a["hook"], b["hook"])
            if k >= 0.6:
                duplikat.append({"a": a["hook"], "b": b["hook"], "kemiripan": round(k, 2)})

    # skrip vs konten yang sudah terbit
    judul_terbit = set()
    for r in baca_csv("data", "konten-14hari.csv"):
        judul_terbit.add((r.get("judul") or "").strip().lower())
    mirip_terbit = []
    for s in skrip["skrip"]:
        for j in judul_terbit:
            if j and kemiripan(s["judul"], j) >= 0.55:
                mirip_terbit.append({"skrip": s["judul"], "terbit": j})

    jadwal = [{"hari": h, "tugas": t, "divisi": d, "berkas": b} for h, t, d, b in JADWAL]
    return {
        "jadwal": jadwal, "duplikat_hook": duplikat, "mirip_terbit": mirip_terbit,
        "docs": docs, "berikut": (hari + timedelta(days=(7 - hari.weekday()) % 7 or 7)).isoformat(),
        "peta": PETA,
        "peta_ringkas": {
            "otomatis": sum(1 for _, baris in PETA for _, s, _ in baris if s == "otomatis"),
            "manual": sum(1 for _, baris in PETA for _, s, _ in baris if s == "manual"),
            "tidak": sum(1 for _, baris in PETA for _, s, _ in baris if s == "tidak"),
        },
    }


# ───────────────────────────────── HTML ───────────────────────────────────
def dasbor(d, tgl):
    n = d["niche"]
    o = [f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Studio Konten — Nocturne Koffie</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<p class="kicker">D3 Marketing × D4 Kreatif · 10 tahap · dibuat {tgl_id(tgl)}</p>
<h1>Studio konten</h1>
<p class="lede">Kerangka 10 folder / 50 agent dijalankan sebagai <b>fungsi deterministik</b>: tiap tahap
membaca berkas, menghitung, dan menulis keluaran yang bisa diperiksa. Yang tidak bisa dihitung mesin
ditandai <span class="pill warn">manual</span> — bukan diklaim otomatis.</p>
<div class="note"><b>Status data: {escape(d['confidence'])}</b>
{d['n_ref']} baris referensi, dan belum ada yang berstatus <code>asli</code> — semuanya <code>contoh</code>.
Artinya urutan dan pola di halaman ini <b>contoh cara kerja</b>, bukan bukti tentang pasar.
Begitu Anda mengisi baris asli (tanggal ambil + tautan), angkanya berubah sendiri dan baru bisa dipakai
memutuskan. Confidence hanya dihitung dari baris <code>asli</code>.</div>
<div class="grid kpi">
  <div><span>Tahap</span><b>10</b><em>dari niche sampai ops</em></div>
  <div><span>Slot kerangka</span><b>{sum(len(b) for _, b in PETA)}</b><em>{d['ops']['peta_ringkas']['otomatis']} otomatis · {d['ops']['peta_ringkas']['manual']} manual · {d['ops']['peta_ringkas']['tidak']} tidak dipakai</em></div>
  <div><span>Bank hook</span><b>{d['hook']['total']}</b><em>{d['hook']['belum']} belum dipakai</em></div>
  <div><span>Skrip</span><b>{len(d['skrip']['skrip'])}</b><em>{d['lapor']['tim']['siap_rekam']} siap rekam</em></div>
  <div><span>Outlier ceruk</span><b>{d['outlier']['dalam_ceruk']}</b><em>dari {len(d['outlier']['baris'])} post dianalisis</em></div>
  <div><span>Watchlist kreator</span><b>{len(d['kreator']['watchlist'])}</b><em>syarat: ≥2 outlier &amp; aktif ≤30 hari</em></div>
</div>"""]

    # 01
    o.append(f"""<h2><small>Tahap 01 · niche research</small>Ceruk, audiens, tawaran</h2>
<p class="lede">{escape(n['niche']['satu_kalimat'])}</p>
<div class="grid cards">
  <article class="card"><p class="meta">Bukan (pagar positioning)</p><ul>
    {''.join(f'<li>{escape(x)}</li>' for x in n['niche']['bukan'])}</ul></article>
  <article class="card"><p class="meta">Kata kunci ceruk</p>
    <p style="font-size:13px;margin:0">{', '.join(escape(k) for k in n['niche']['kata_kunci_ceruk'][:14])} …</p>
    <p class="meta" style="margin-top:10px">Kata dilarang di skrip</p>
    <p style="font-size:13px;margin:0">{', '.join(escape(k) for k in n['bahasa']['kata_dilarang'][:8])} …</p></article>
</div>
<table><thead><tr><th>Segmen</th><th>Kebutuhan</th><th>Keberatan</th><th>Kanal</th><th class="num">Harga nyaman</th><th>Pintu masuk</th></tr></thead><tbody>
{''.join(f'<tr><td><b>{escape(s["nama"])}</b><br><span class="kicker">{escape(s["umur"])}</span></td><td>{escape(s["kebutuhan"])}</td><td>{escape(s["keberatan"])}</td><td>{escape(s["kanal"])}</td><td class="num">{escape(s["harga_nyaman"])}</td><td>{escape(s["pintu_masuk"])}</td></tr>' for s in n['audiens']['segmen'])}
</tbody></table>
<h3 style="margin-top:18px">Tangga tawaran</h3>
<table><thead><tr><th>Tingkat</th><th>Tawaran</th><th class="num">Harga</th><th>Tujuan</th></tr></thead><tbody>
{''.join(f'<tr><td>{escape(t["tingkat"])}</td><td>{escape(t["tawaran"])}</td><td class="num">{rp(t["harga"]) if t["harga"] else "sesuai tier"}</td><td>{escape(t["tujuan"])}</td></tr>' for t in n['tawaran']['tangga'])}
</tbody></table>""")

    # usulan frasa + makna ganda
    o.append("""<h3 style="margin-top:18px">Pencari frasa — usulan dari komentar pembeli</h3>
<table><thead><tr><th>Usulan frasa</th><th>Asal</th><th>Status</th></tr></thead><tbody>""")
    for u in n["usulan_frasa"]:
        o.append(f'<tr><td><b>{escape(u["frasa"])}</b></td><td>“{escape(u["dari"])}…”</td>'
                 f'<td><span class="pill warn">{escape(u["status"])}</span></td></tr>')
    if not n["usulan_frasa"]:
        o.append('<tr><td colspan="3">Tidak ada usulan baru — semua pertanyaan sudah terwakili kata kunci.</td></tr>')
    o.append("</tbody></table>")

    o.append('<h3 style="margin-top:18px">Makna ganda — frasa yang tidak boleh jadi kata kunci tunggal</h3>'
             '<table><thead><tr><th>Frasa</th><th>Kenapa</th><th>Tindakan</th><th>Kena di kata kunci</th></tr></thead><tbody>')
    for g in n["makna_ganda"]:
        pill = "ok" if g["aman"] else "hot"
        o.append(f'<tr><td><b>{escape(g["frasa"])}</b></td><td>{escape(g["kenapa"])}</td>'
                 f'<td>{escape(g["tindakan"])}</td>'
                 f'<td><span class="pill {pill}">{"aman" if g["aman"] else ", ".join(escape(x) for x in g["kena"])}</span></td></tr>')
    o.append("</tbody></table>")

    # 02
    p = d["pesaing"]
    o.append("""<h2><small>Tahap 02 · competitor tracking</small>Pesaing, industri, video jawaban</h2>
<p class="lede">Peringkat di bawah adalah <b>akun yang benar-benar kita tangkap</b> di
<code>data/riset-referensi.csv</code> — bukan klaim "top 50 perusahaan industri".</p>
<table><thead><tr><th>Akun</th><th class="num">Post</th><th class="num">Views median</th><th class="num">Pengikut</th></tr></thead><tbody>""")
    for r in n["peringkat_akun"]:
        o.append(f'<tr><td>{escape(r["akun"])}</td><td class="num">{r["post"]}</td>'
                 f'<td class="num">{riset.fmt(r["views_median"])}</td><td class="num">{riset.fmt(r["pengikut"])}</td></tr>')
    o.append("</tbody></table>")

    o.append('<h3 style="margin-top:18px">Catatan industri (dicatat manual)</h3>'
             '<table><thead><tr><th>Tanggal</th><th>Sumber</th><th>Topik</th><th>Dampak</th><th>Tindakan</th></tr></thead><tbody>')
    for i in p["industri"]:
        o.append(f'<tr><td>{escape(i["tanggal"])}</td><td>{escape(i["sumber"])}</td>'
                 f'<td>{escape(i["topik"])}</td><td>{escape(i["dampak"])}</td><td>{escape(i["tindakan"])}</td></tr>')
    o.append("</tbody></table>")

    o.append('<h3 style="margin-top:18px">Rencana video jawaban</h3><div class="grid cards">')
    for r in p["jawaban"]:
        o.append(f"""<article class="card"><p class="meta">{escape(r['platform'])} · lift {angka_id(r['lift'], satuan='×')} · {escape(r['struktur'])}</p>
  <h3>Jawab dengan sudut kita</h3>
  <div class="hook">{escape(r['jawaban'])}</div>
  <ul><li><b>Acuan:</b> “{escape(r['acuan'])}”</li>
    <li><b>Sudut:</b> {escape(r['sudut'])}</li>
    <li><b>Aset:</b> <code>{escape(r['aset'] or '—')}</code></li>
    <li><b>Alasan:</b> {escape(r['alasan'])}</li></ul></article>""")
    o.append("</div>")

    # 03
    ol = d["outlier"]
    o.append(f"""<h2><small>Tahap 03 · outlier videos</small>Ranking, filter ceruk, dead views</h2>
<p class="lede">{ol['dalam_ceruk']} post masuk ceruk, {ol['di_luar']} di luar ceruk (tetap dihitung baseline,
tidak dipakai sebagai pola). Dead views = views &lt; 50% baseline: {len(ol['dead'])} post.</p>
<table><thead><tr><th>#</th><th>Hook</th><th>Struktur</th><th class="num">Views</th><th class="num">Lift</th>
<th class="num">ER</th><th class="num">Simpan</th><th>Status data</th></tr></thead><tbody>""")
    for i, b in enumerate(ol["rank_views"], 1):
        pill = {"outlier besar": "hot", "outlier kuat": "ok", "outlier ringan": "warn"}.get(b["label"], "dim")
        o.append(f'<tr><td class="num">{i}</td><td>{escape(b["hook"])}</td>'
                 f'<td>{escape(NAMA_STRUKTUR.get(b["hook_kategori"], b["hook_kategori"]))}</td>'
                 f'<td class="num">{riset.fmt(b["views"])}</td>'
                 f'<td class="num"><span class="pill {pill}">{angka_id(b["lift"] or 0, satuan="×")}</span></td>'
                 f'<td class="num">{angka_id(b["er"], satuan="%")}</td><td class="num">{angka_id(b["simpan_rate"], satuan="%")}</td>'
                 f'<td><span class="pill {"dim" if b["status"] != "asli" else "ok"}">{escape(b["status"])}</span></td></tr>')
    o.append("</tbody></table>")

    # 04
    k = d["kreator"]
    o.append("""<h2><small>Tahap 04 · outlier creators</small>Kreator yang layak dipantau</h2>
<p class="lede">Masuk watchlist bila dua syarat terpenuhi: <b>≥2 outlier</b> dan <b>aktif ≤30 hari</b>.
Satu video meledak belum membuktikan apa pun.</p>
<table><thead><tr><th>Akun</th><th class="num">Post</th><th class="num">Outlier</th><th class="num">Interaksi/1K</th>
<th class="num">Views median</th><th>Riwayat ≤30 hari</th><th>Watchlist</th></tr></thead><tbody>""")
    for r in k["baris"]:
        o.append(f'<tr><td>{escape(r["akun"])}<br><span class="kicker">{escape(", ".join(r["platform"]))}</span></td>'
                 f'<td class="num">{r["post"]}</td><td class="num">{r["outlier"]}</td>'
                 f'<td class="num">{angka_id(r["per_1k"])}</td><td class="num">{riset.fmt(r["views_median"])}</td>'
                 f'<td><span class="pill {"ok" if r["riwayat_30h"] else "dim"}">{"ya" if r["riwayat_30h"] else "tidak"}</span></td>'
                 f'<td><span class="pill {"hot" if r["watchlist"] else "dim"}">{"pantau" if r["watchlist"] else "—"}</span></td></tr>')
    o.append("</tbody></table>")

    # 05
    h = d["hook"]
    fp = h["film_pertama"]
    o.append(f"""<h2><small>Tahap 05 · hooks</small>Bank hook &amp; pilih film pertama</h2>
<div class="grid cards">
  <article class="card"><p class="meta">Film pertama minggu ini</p>
    <div class="hook">{escape(fp['hook']) if fp else '—'}</div>
    <ul><li><b>Struktur:</b> {escape(NAMA_STRUKTUR.get(fp['struktur'], fp['struktur'])) if fp else '—'}</li>
      <li><b>Lift median struktur:</b> {(('%.1f×' % fp['lift_median']).replace('.', ',')) if fp and fp['lift_median'] else '—'}</li>
      <li><b>Aset:</b> <code>{escape(fp['aset']) if fp else '—'}</code></li>
      <li><b>Kenapa ini:</b> lift tertinggi di antara hook yang asetnya sudah siap dan belum dipakai.</li></ul>
  </article>
  <article class="card"><p class="meta">Hitung struktur</p>
    <table style="margin-top:0"><tbody>
    {''.join(f'<tr><td>{escape(g["nama"])}</td><td class="num">{g["belum"]}/{g["n"]}</td><td class="num">{("%.1f×" % g["lift_median"]).replace(".", ",") if g["lift_median"] else "—"}</td></tr>' for g in h['grouper'])}
    </tbody></table>
    <p class="meta" style="margin-top:8px">kolom: belum dipakai / total · lift median</p>
  </article>
</div>""")

    # 06
    f = d["format"]
    o.append("<h2><small>Tahap 06 · formats &amp; trends</small>Format, gaya rekam, kuartal</h2>"
             '<table><thead><tr><th>Platform</th><th>Format</th><th class="num">Post</th><th class="num">ER median</th>'
             '<th class="num">Lift median</th><th class="num">Durasi</th></tr></thead><tbody>')
    for m in f["copy_week"]:
        o.append(f'<tr><td>{m["platform"]}</td><td><b>{m["format"]}</b></td><td class="num">{m["n"]}</td>'
                 f'<td class="num">{riset.fmt(m["er_median"])}%</td>'
                 f'<td class="num">{riset.fmt(m["lift_median"], "x")}</td>'
                 f'<td class="num">{riset.fmt(m["detik_median"]) + "s" if m["detik_median"] else "—"}</td></tr>')
    o.append("</tbody></table>")

    a, b = f["atas"], f["bawah"]
    o.append(f"""<div class="grid cards">
  <article class="card"><p class="meta">Kuartal atas · lift median {angka_id(a.get('lift_median') or 0, satuan='×')}</p>
    <ul><li>Format: {escape(", ".join(f'{kk} ({vv})' for kk, vv in (a.get('format') or {}).items()))}</li>
      <li>Struktur: {escape(", ".join(f'{kk} ({vv})' for kk, vv in (a.get('struktur') or {}).items()))}</li>
      <li>Durasi median: {riset.fmt(a.get('detik_median') or 0)}s</li></ul>
    <p class="meta" style="margin-top:8px">Contoh</p>
    {''.join(f'<div class="hook" style="font-size:13.5px">{escape(x)}</div>' for x in (a.get('contoh') or []))}
  </article>
  <article class="card"><p class="meta">Kuartal bawah · lift median {angka_id(b.get('lift_median') or 0, satuan='×')}</p>
    <ul><li>Format: {escape(", ".join(f'{kk} ({vv})' for kk, vv in (b.get('format') or {}).items()))}</li>
      <li>Struktur: {escape(", ".join(f'{kk} ({vv})' for kk, vv in (b.get('struktur') or {}).items()))}</li>
      <li>Durasi median: {riset.fmt(b.get('detik_median') or 0)}s</li></ul>
    <p class="meta" style="margin-top:8px">Jangan ditiru</p>
    {''.join(f'<div class="hook" style="font-size:13.5px">{escape(x)}</div>' for x in (b.get('contoh') or []))}
  </article>
</div>""")

    o.append('<h3 style="margin-top:18px">Pemetaan gaya rekam</h3><table><thead><tr><th>Gaya</th>'
             '<th>Cocok untuk struktur</th><th>Alat</th><th>Catatan</th></tr></thead><tbody>')
    for g in f["gaya"]:
        o.append(f'<tr><td><b>{escape(g["gaya"])}</b></td><td>{escape(", ".join(g["cocok_untuk"]))}</td>'
                 f'<td>{escape(g["alat"])}</td><td>{escape(g["catatan"])}</td></tr>')
    o.append("</tbody></table>")

    # 07
    o.append("<h2><small>Tahap 07 · scripts</small>Lima skrip 9 detik</h2>"
             '<p class="lede">Format 9 detik: hook 3 detik, dua baris bukti, satu CTA. Semua skrip lolos cek suara: tanpa kata terlarang, kalimat ≤ 18 kata, '
             'ada angka, ada CTA, dan setiap klaim menyebut berkas sumber.</p>')
    for s in d["skrip"]["skrip"]:
        pill = "ok" if s["status"] == "siap rekam" else "warn"
        o.append(f"""<article class="card" style="margin-top:12px">
  <p class="meta">Skrip {s['no']:02d} · {escape(s['nama_struktur'])} · {escape(s['pilar'])} · {s['total_detik']}s ·
    <span class="pill {pill}">{escape(s['status'])}</span> · suara {s['suara_skor']}/100</p>
  <h3>{escape(s['judul'])}</h3>
  {''.join(f'<div class="beat"><b>{bb["detik"]}s</b><div>{escape(bb["teks"])}<br><span class="kicker">{escape(bb["sumber"] or "—")}</span></div></div>' for bb in s['beats'])}
  <p class="lede" style="margin-top:8px;font-size:13px"><b>Shot list:</b> {escape(s['visual'])}<br>
    <b>Aset:</b> <code>{escape(s['aset'])}</code> · <b>Sumber:</b> {", ".join(f"<code>{escape(x)}</code>" for x in s['sumber'])}</p>
</article>""")
    o.append(f'<p class="lede" style="margin-top:10px">Antrean skrip berikutnya: '
             f'{escape("; ".join(d["skrip"]["antrean"][:5]) or "—")} ({d["skrip"]["sisa"]} hook tersisa).</p>')

    # 08
    sk = d["skala"]
    o.append("<h2><small>Tahap 08 · scaling</small>Bedah pemenang, simpan struktur, remix</h2>"
             '<table><thead><tr><th>Hook pemenang</th><th>Struktur</th><th>Format</th><th class="num">Lift</th>'
             '<th class="num">Durasi</th><th>Alasan</th></tr></thead><tbody>')
    for w in sk["pemenang"]:
        o.append(f'<tr><td>{escape(w["hook"])}</td><td>{escape(w["struktur"])}</td>'
                 f'<td>{escape(w["platform"])}/{escape(w["format"])}</td>'
                 f'<td class="num">{angka_id(w["lift"], satuan="×")}</td><td class="num">{w["detik"] or "—"}s</td>'
                 f'<td>{escape(w["alasan"])}</td></tr>')
    o.append("</tbody></table>")

    o.append('<h3 style="margin-top:18px">Remix konsep (struktur disimpan, isi diganti)</h3><div class="grid cards">')
    for r in sk["remix"][:6]:
        o.append(f"""<article class="card"><p class="meta">{escape(r['jenis'])} · dari “{escape(r['dari'][:40])}…”</p>
  <div class="hook">{escape(r['hook'])}</div>
  <ul><li>{escape(r['konsep'])}</li><li><b>Aset:</b> <code>{escape(r['aset'] or '—')}</code></li></ul></article>""")
    o.append("</div>")

    o.append('<h3 style="margin-top:18px">Pola paling dibagikan</h3><table><thead><tr><th>Hook</th>'
             '<th>Struktur</th><th class="num">Interaksi/views</th></tr></thead><tbody>')
    for p2 in sk["paling_dibagikan"]:
        o.append(f'<tr><td>{escape(p2["hook"])}</td><td>{escape(p2["struktur"])}</td>'
                 f'<td class="num">{p2["interaksi_pct"]}%</td></tr>')
    o.append("</tbody></table>")

    # 09
    lp = d["lapor"]
    o.append(f"""<h2><small>Tahap 09 · reporting &amp; briefs</small>Keputusan mingguan</h2>
<div class="grid cards">
  <article class="card"><p class="meta">Dobel</p><div class="hook">{escape(lp['dobel_struktur'])}</div>
    <ul>{''.join(f'<li>{escape(x["hook"])} — {angka_id(x["lift"], satuan="×")}</li>' for x in lp['dobel'])}</ul></article>
  <article class="card"><p class="meta">Hentikan</p>
    <ul>{''.join(f'<li>{escape(x["hook"])} — {angka_id(x["lift"], satuan="×")}</li>' for x in lp['hentikan']) or '<li>tidak ada</li>'}</ul>
    <p class="meta" style="margin-top:8px">lift &lt; 0,9× = kalah dari kebiasaan akun</p></article>
  <article class="card"><p class="meta">Uji (satu saja)</p>
    <div class="hook">{escape(lp['uji'][0]) if lp['uji'] else '—'}</div>
    <p class="meta" style="margin-top:8px">Laporan tim: {lp['tim']['hook_bank']} hook · {lp['tim']['skrip']} skrip ·
      {lp['tim']['watchlist']} kreator dipantau · {lp['tim']['outlier_ceruk']} outlier ceruk</p></article>
</div>
<p class="lede" style="margin-top:12px">Brief lengkap: <code>studio/brief-senin.md</code> ·
5 skrip: <code>studio/skrip/</code> · data mesin: <code>studio/data.json</code></p>""")

    # 10
    ops = d["ops"]
    o.append(f"""<h2><small>Tahap 10 · content operations</small>Jadwal, pemakaian ulang, pemetaan 50 slot</h2>
<table><thead><tr><th>Hari</th><th>Tugas</th><th>Divisi</th><th>Berkas / perintah</th></tr></thead><tbody>
{''.join(f'<tr><td>{escape(j["hari"])}</td><td>{escape(j["tugas"])}</td><td>{escape(j["divisi"])}</td><td><code>{escape(j["berkas"])}</code></td></tr>' for j in ops['jadwal'])}
</tbody></table>
<p class="lede" style="margin-top:10px">Cek pemakaian ulang: {len(ops['duplikat_hook'])} pasang hook nyaris duplikat ·
{len(ops['mirip_terbit'])} skrip mirip konten yang sudah terjadwal. Playbook dibaca: {len(ops['docs'])} berkas.</p>""")

    o.append('<h3 style="margin-top:18px">Pemetaan kerangka 50 agent → siapa yang mengerjakan</h3>'
             '<table><thead><tr><th>Folder</th><th>Slot</th><th>Dikerjakan</th><th>Keterangan</th></tr></thead><tbody>')
    for folder, baris in PETA:
        for i, (slot, siapa, ket) in enumerate(baris):
            pill = {"otomatis": "ok", "manual": "warn", "tidak": "dim"}[siapa]
            o.append(f'<tr><td>{"<b>" + escape(folder) + "</b>" if i == 0 else ""}</td>'
                     f'<td>{escape(slot)}</td><td><span class="pill {pill}">{siapa}</span></td>'
                     f'<td>{escape(ket)}</td></tr>')
    o.append("</tbody></table>")

    o.append(f"""<div class="note"><b>Kenapa tidak 50 agent LLM</b>
50 agent berarti 50 kali biaya token untuk pekerjaan yang sebagian besar berupa hitungan tetap
(median, lift, ranking, pengecekan kata terlarang). Di sini semua itu jadi fungsi Python:
<b>0 token per tahap</b>, hasilnya bisa diulang dan diperiksa. Yang benar-benar butuh pertimbangan
manusia — memilih sudut, menilai rasa, menghubungi orang — tetap di tangan Anda dan ditandai
<span class="pill warn">manual</span>.</div>
<footer>
  <span>Dibuat <code>tools/studio.py</code> · kerangka 10 tahap diadaptasi dari @dsqjaffa ·
    sumber data <code>data/riset-*.csv</code>, <code>data/studio-*.csv/json</code>,
    <code>data/kreatif.json</code>, <code>data/catalog.json</code></span>
  <span><a href="../riset/index.html">dasbor riset</a> · <a href="../konten/index.html">hub konten</a> ·
    <a href="../dashboard/index.html">papan harian</a> · <a href="../laporan/index.html">laporan</a></span>
</footer></div></body></html>""")
    return "\n".join(o)


# ────────────────────────────────── main ──────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true")
    args = ap.parse_args()

    hari = hari_ini()
    niche = baca_json("data", "studio-niche.json")
    if not niche:
        raise SystemExit("data/studio-niche.json tidak ada — studio butuh definisi ceruk.")

    com_rows = riset.analisa_referensi(baca_csv("data", "riset-referensi.csv"))
    kom = riset.analisa_komentar(baca_csv("data", "riset-komentar.csv"))
    kw = riset.analisa_kata_kunci(baca_csv("data", "riset-kata-kunci.csv"))
    bank_rows = baca_csv("data", "studio-hooks.csv")
    industri = baca_csv("data", "studio-industri.csv")
    manifest = baca_json("data", "kreatif.json")
    catalog = baca_json("data", "catalog.json")
    batch = baca_csv("data", "batch-qc.csv")

    # skor acuan untuk template: batch terakhir yang ditolak, fallback skor tertinggi
    ditolak = [b for b in batch if (b.get("status") or "").lower() in ("ditolak", "reject")]
    skor = (ditolak[-1]["skor_cupping"] if ditolak else
            (max((b["skor_cupping"] for b in batch if b.get("skor_cupping")), default="84")))

    lama = baca_json("studio", "data.json", default={})
    data = {"bahasa": niche["bahasa"], "skor": skor.replace(".", ",") if skor else "83"}

    niche_t = tahap_niche(niche, kom["baris"], com_rows["baris"])
    pesaing_t = tahap_pesaing(niche_t, com_rows["baris"], industri)
    outlier_t = tahap_outlier(com_rows, niche["niche"]["kata_kunci_ceruk"])
    kreator_t = tahap_kreator(outlier_t["baris"], hari)
    hook_t = tahap_hook([dict(h) for h in bank_rows], com_rows, manifest)
    format_t = tahap_format(com_rows, niche_t["gaya"], outlier_t)
    data["skrip_lama"] = [{"judul": s["judul"]} for s in lama.get("skrip", [])]
    skrip_t = tahap_skrip(hook_t, data, hari)
    skala_t = tahap_skala(outlier_t, com_rows)
    docs = []
    for p in ["skills/README.md", "skills/social-media-riset/SKILL.md",
              "skills/komentar-mining/SKILL.md", "skills/search-intent-riset/SKILL.md",
              "skills/studio-konten/SKILL.md", "marketing/09-media-kreator.md",
              "operasional/divisi/D3-marketing-pertumbuhan.md",
              "operasional/divisi/D4-kreatif-media.md"]:
        if os.path.exists(os.path.join(ROOT, p)):
            docs.append(p)
    ops_t = tahap_ops(hook_t, skrip_t, docs, hari)
    lapor_t = tahap_lapor(hook_t, skrip_t, kreator_t, outlier_t, skala_t, pesaing_t, hari)

    hasil = {"confidence": com_rows.get("confidence", "—"), "n_ref": com_rows.get("n", 0),
             "niche": niche_t, "pesaing": pesaing_t, "outlier": outlier_t, "kreator": kreator_t,
             "hook": hook_t, "format": format_t, "skrip": skrip_t, "skala": skala_t,
             "lapor": lapor_t, "ops": ops_t, "dibuat": hari.isoformat()}
    hasil["data"] = {"skrip": skrip_t["skrip"]}

    print(f"Studio konten — {hari.isoformat()}")
    print(f"  01 niche      : {len(niche_t['audiens']['segmen'])} segmen · {len(niche_t['usulan_frasa'])} usulan frasa · "
          f"{sum(1 for g in niche_t['makna_ganda'] if not g['aman'])} frasa ambigu")
    print(f"  02 pesaing    : {len(niche_t['peringkat_akun'])} akun ditangkap · {len(pesaing_t['industri'])} catatan industri · "
          f"{len(pesaing_t['jawaban'])} rencana video jawaban")
    print(f"  03 outlier    : {outlier_t['dalam_ceruk']} dalam ceruk · {outlier_t['di_luar']} di luar · "
          f"{len(outlier_t['dead'])} dead views")
    print(f"  04 kreator    : {len(kreator_t['baris'])} akun · {len(kreator_t['watchlist'])} watchlist")
    print(f"  05 hook       : {hook_t['total']} hook ({hook_t['belum']} belum) · film pertama: "
          f"{hook_t['film_pertama']['hook'][:44] if hook_t['film_pertama'] else '—'}")
    print(f"  06 format     : {len(format_t['copy_week'])} platform prioritas · {len(format_t['to_copy'])} format layak ditiru")
    print(f"  07 skrip      : {len(skrip_t['skrip'])} skrip · "
          f"{sum(1 for s in skrip_t['skrip'] if s['status'] == 'siap rekam')} siap rekam · sisa antrean {skrip_t['sisa']}")
    print(f"  08 skala      : {len(skala_t['pemenang'])} pemenang · {len(skala_t['remix'])} konsep remix")
    print(f"  09 lapor      : top {len(lapor_t['top10'])} · dobel/hentikan/uji siap")
    print(f"  10 ops        : {len(ops_t['jadwal'])} blok jadwal · {len(ops_t['duplikat_hook'])} hook duplikat · "
          f"{len(ops_t['mirip_terbit'])} skrip mirip jadwal")
    print(f"  peta 50 slot  : {ops_t['peta_ringkas']['otomatis']} otomatis · "
          f"{ops_t['peta_ringkas']['manual']} manual · {ops_t['peta_ringkas']['tidak']} tidak dipakai")

    if args.cek:
        return

    os.makedirs(OUT, exist_ok=True)
    sdir = os.path.join(OUT, "skrip")
    os.makedirs(sdir, exist_ok=True)
    for f in os.listdir(sdir):
        if f.endswith(".md"):
            os.remove(os.path.join(sdir, f))
    for s in skrip_t["skrip"]:
        with open(os.path.join(sdir, f"skrip-{s['no']:02d}-{slug(s['judul'])}.md"), "w",
                  encoding="utf-8") as f:
            f.write(skrip_md(s, hari))

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(dasbor(hasil, hari))
    with open(os.path.join(OUT, "brief-senin.md"), "w", encoding="utf-8") as f:
        f.write(brief_md(hasil, hari))

    ringkas = {
        "dibuat": hari.isoformat(),
        "tahap": 10,
        "peta": ops_t["peta_ringkas"],
        "hook_total": hook_t["total"], "hook_belum": hook_t["belum"],
        "skrip_siap": sum(1 for s in skrip_t["skrip"] if s["status"] == "siap rekam"),
        "skrip": [{"no": s["no"], "judul": s["judul"], "struktur": s["struktur"],
                   "status": s["status"], "aset": s["aset"]} for s in skrip_t["skrip"]],
        "film_pertama": hook_t["film_pertama"]["hook"] if hook_t["film_pertama"] else None,
        "outlier_ceruk": outlier_t["dalam_ceruk"],
        "kreator_watchlist": [w["akun"] for w in kreator_t["watchlist"]],
        "format_prioritas": [{"platform": m["platform"], "format": m["format"],
                              "lift": m["lift_median"]} for m in format_t["copy_week"]],
        "keputusan": {"dobel": lapor_t["dobel_struktur"],
                      "hentikan": [x["hook"] for x in lapor_t["hentikan"]],
                      "uji": lapor_t["uji"]},
        "reuse": {"duplikat_hook": ops_t["duplikat_hook"], "mirip_terbit": ops_t["mirip_terbit"]},
        "berikut": ops_t["berikut"],
        "docs": ops_t["docs"],
    }
    with open(os.path.join(OUT, "data.json"), "w", encoding="utf-8") as f:
        json.dump(ringkas, f, ensure_ascii=False, indent=2)

    print(f"  halaman       : studio/index.html · studio/brief-senin.md · {len(skrip_t['skrip'])} skrip")


if __name__ == "__main__":
    main()
