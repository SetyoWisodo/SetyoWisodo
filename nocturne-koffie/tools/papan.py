#!/usr/bin/env python3
"""
Papan Harian Nocturne Koffie — generator dashboard operasional.

Membaca seluruh data di ./data, menghitung stok, margin, pesanan, konten,
QC, dan KPI, lalu menulis dashboard/index.html + dashboard/data.json.

Pakai:
    python3 tools/papan.py                # pakai tanggal hari ini (Asia/Jakarta)
    python3 tools/papan.py --tanggal 2026-11-03
    python3 tools/papan.py --json         # hanya cetak ringkasan JSON

Tanpa dependensi eksternal (stdlib saja).
"""
from __future__ import annotations

import argparse
import csv
import re
import json
import math
import os
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Asia/Jakarta")
except Exception:  # pragma: no cover
    TZ = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, "data", *p)

RP = lambda n: "Rp" + f"{round(n):,}".replace(",", ".")

TARGET = {            # target 90 hari, dari marketing/00-strategi-90hari.md
    "order_bulan": 25,
    "aov": 130000,
    "langganan": 3,
    "b2b": 1,
    "margin": 0.35,
}


# ───────────────────────────── pembacaan data ──────────────────────────────
def baca_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def baca_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def parse_tanggal(s, fallback=None):
    s = (s or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return fallback


# ───────────────────────────────── hitungan ───────────────────────────────
def hitung_margin(catalog, biaya):
    a = biaya.get("asumsi", {})
    yield_ = float(a.get("yield_sangrai", 0.8) or 0.8)
    per_pack = sum(float(a.get(k, 0) or 0) for k in (
        "kemasan_per_bungkus", "label_stiker", "tenaga_kerja_per_bungkus",
        "lain_lain_per_bungkus"))
    harga_green = biaya.get("harga_green_per_kg", {})
    target = float(a.get("target_margin_kotor", TARGET["margin"]))

    hasil = []
    for p in catalog.get("products", []):
        green = float(harga_green.get(p["id"], 0) or 0)
        baris = {"produk": p["name"], "id": p["id"], "green_per_kg": green, "varian": []}
        for v in p.get("variants", []):
            gram = float(v.get("grams") or 0)
            hpp_gram = (gram / 1000.0) / yield_ * green
            hpp = hpp_gram + per_pack
            harga = float(v.get("price") or 0)
            margin = (harga - hpp) / harga if harga else 0
            baris["varian"].append({
                "ukuran": v["weight"], "harga": harga, "hpp": round(hpp),
                "laba": round(harga - hpp), "margin": round(margin, 4),
                "sehat": margin >= target,
            })
        if baris["varian"]:
            baris["margin_terburuk"] = min(x["margin"] for x in baris["varian"])
            baris["sehat"] = baris["margin_terburuk"] >= target
        hasil.append(baris)
    return hasil, per_pack, yield_, target


def hitung_stok(catalog, stok, biaya, pesanan, hari_ini):
    yield_ = float(biaya.get("asumsi", {}).get("yield_sangrai", 0.8) or 0.8)
    sisa_green = defaultdict(float)
    total_green = defaultdict(float)
    for lot in stok.get("lots", []):
        if (lot.get("status") or "aktif") != "aktif":
            continue
        g = float(lot.get("green_kg") or 0)
        t = float(lot.get("terpakai_kg") or 0)
        sisa_green[lot["produk"]] += max(0.0, g - t)
        total_green[lot["produk"]] += g

    # penjualan 28 hari terakhir per produk (gram)
    sejak = hari_ini - timedelta(days=28)
    gram_terjual = defaultdict(float)
    nama_ke_id = {p["name"].lower(): p["id"] for p in catalog.get("products", [])}
    for o in pesanan:
        tgl = parse_tanggal(o.get("tanggal"))
        if not tgl or tgl < sejak:
            continue
        if (o.get("status") or "").lower() in ("batal", "dibatalkan"):
            continue
        pid = nama_ke_id.get((o.get("produk") or "").strip().lower())
        if not pid:
            continue
        ukuran = (o.get("ukuran") or "").lower().replace(" ", "")
        gram = 1000 if ukuran.startswith("1kg") else 500 if ukuran.startswith("500") else 250 if ukuran.startswith("250") else 100
        try:
            qty = int(float(o.get("qty") or 1))
        except ValueError:
            qty = 1
        gram_terjual[pid] += gram * qty

    # stok blend dihitung dari komponennya (brief 6.6), bukan dari lot sendiri
    def sisa_efektif(pid, produk):
        sisa = sisa_green.get(pid, 0.0)
        if produk.get("category") != "Signature Blend":
            return sisa
        komp = produk.get("variety", "")  # "Robusta Raung 70% · Arabika Ijen 30%"
        pasangan = {"raung": "raung", "ijen": "blue-mount-ijen"}
        porsi = {}
        for m in re.finditer(r"(Raung|Ijen)\s*(\d+)%", komp, re.I):
            nama = m.group(1).lower()
            porsi[pasangan.get(nama, nama)] = int(m.group(2)) / 100.0
        if not porsi:
            return sisa
        tersedia = [sisa_green.get(k, 0.0) / v for k, v in porsi.items() if v > 0]
        return min(tersedia) if tersedia else sisa

    hasil = []
    for p in catalog.get("products", []):
        pid = p["id"]
        sisa = sisa_green.get(pid, 0.0)
        sisa_hitung = sisa_efektif(pid, p) if p.get("category") == "Signature Blend" else sisa
        roasted_g = sisa_hitung * yield_ * 1000.0
        awal_roasted = total_green.get(pid, 0.0) * yield_ * 1000.0
        if p.get("category") == "Signature Blend":
            awal_roasted = 0.0  # blend tidak punya lot sendiri; status mengikuti ketersediaan komponen
        if roasted_g <= 0:
            status = "habis"
        elif awal_roasted and roasted_g <= awal_roasted * 0.2:
            status = "terbatas"
        else:
            status = "tersedia"

        per_ukuran = {}
        for v in p.get("variants", []):
            g = float(v.get("grams") or 0)
            per_ukuran[v["weight"]] = int(roasted_g // g) if g else 0

        jual_harian = gram_terjual.get(pid, 0) / 28.0
        hari_tersisa = int(roasted_g / jual_harian) if jual_harian > 0 else None

        situs = p.get("status", "tersedia")
        hasil.append({
            "id": pid, "produk": p["name"],
            "sisa_green_kg": None if p.get("category") == "Signature Blend" else round(sisa, 2),
            "blend": p.get("category") == "Signature Blend",
            "roasted_g": round(roasted_g), "bungkus": per_ukuran,
            "status_hitung": status, "status_situs": situs,
            "beda_status": not (status == "habis" and situs == "menunggu-panen") and status != situs,
            "hari_tersisa": hari_tersisa,
            "terjual_28h_g": round(gram_terjual.get(pid, 0)),
        })
    return hasil


def analisa_pesanan(pesanan, hari_ini):
    perlu_proses, resi_kosong, follow_up = [], [], []
    nomor_terakhir = {}
    for o in pesanan:
        tgl = parse_tanggal(o.get("tanggal"))
        st = (o.get("status") or "").strip().lower()
        if st in ("batal", "dibatalkan"):
            continue
        umur = (hari_ini - tgl).days if tgl else None
        if st in ("baru", "diproses") and umur is not None:
            perlu_proses.append({**o, "umur_hari": umur, "telat": umur > 1})
        if st in ("dikirim", "diproses") and not (o.get("resi") or "").strip():
            resi_kosong.append({**o, "umur_hari": umur})
        wa = (o.get("wa") or "").strip()
        if wa and (not tgl or tgl > nomor_terakhir.get(wa, date.min)):
            nomor_terakhir[wa] = tgl

    # follow-up restock: 18 hari setelah order terakhir, belum order lagi
    for wa, tgl in nomor_terakhir.items():
        if not tgl:
            continue
        jatuh = tgl + timedelta(days=18)
        if jatuh <= hari_ini:
            contoh = next(o for o in pesanan if (o.get("wa") or "").strip() == wa and parse_tanggal(o.get("tanggal")) == tgl)
            follow_up.append({
                "nama": contoh.get("nama"), "wa": wa, "order_terakhir": tgl.isoformat(),
                "jatuh_tempo": jatuh.isoformat(), "lewat_hari": (hari_ini - jatuh).days,
                "produk": contoh.get("produk"),
            })
    follow_up.sort(key=lambda x: x["lewat_hari"], reverse=True)
    return perlu_proses, resi_kosong, follow_up


def analisa_konten(konten, hari_ini):
    hari_ini_konten, terlambat, berikut = [], [], []
    for k in konten:
        tgl = parse_tanggal(k.get("tanggal"))
        if not tgl:
            continue
        st = (k.get("status") or "belum").lower()
        if tgl == hari_ini:
            hari_ini_konten.append(k)
        elif tgl < hari_ini and st not in ("selesai", "terbit", "done"):
            terlambat.append({**k, "lewat": (hari_ini - tgl).days})
        elif tgl > hari_ini:
            berikut.append(k)
    berikut.sort(key=lambda x: x["tanggal"])
    return hari_ini_konten, terlambat, berikut[:4]


def analisa_qc(batch, hari_ini):
    sejak = hari_ini - timedelta(days=30)
    bulan = []
    for b in batch:
        tgl = parse_tanggal(b.get("tanggal"))
        if tgl and tgl >= sejak:
            bulan.append({**b, "_tgl": tgl})
    bulan.sort(key=lambda x: x["_tgl"], reverse=True)
    ditolak = [b for b in bulan if (b.get("status") or "").lower() in ("ditolak", "reject")]
    skor = [float(b["skor_cupping"]) for b in bulan if (b.get("skor_cupping") or "").strip()]
    return {
        "jumlah_30h": len(bulan), "ditolak": ditolak,
        "skor_rata": round(sum(skor) / len(skor), 1) if skor else None,
        "terakhir": bulan[:5],
    }


def analisa_kpi(kpi):
    if not kpi:
        return None
    baris = sorted(kpi, key=lambda r: r.get("mulai", ""))
    last = baris[-1]
    g = lambda k: float(last.get(k) or 0)
    return {
        "minggu": last.get("minggu"), "mulai": last.get("mulai"),
        "order": int(g("order_retail")), "omzet": g("omzet_retail"),
        "aov": g("aov"), "langganan": int(g("langganan_aktif")),
        "b2b": int(g("akun_b2b")), "chat": int(g("chat_wa")),
        "followers": int(g("followers_ig")), "catatan": last.get("catatan", ""),
    }


# ──────────────────────────────── peringatan ──────────────────────────────
def susun_peringatan(stok, margin, proses, resi, follow, konten_telat, qc, legal):
    out = []

    def add(level, divisi, teks, aksi):
        out.append({"level": level, "divisi": divisi, "teks": teks, "aksi": aksi})

    for s in stok:
        if s["beda_status"]:
            add("kritis", "Produksi & QC",
                f"{s['produk']}: situs menampilkan “{s['status_situs']}”, stok lot menunjukkan “{s['status_hitung']}”.",
                "Perbarui status produk di data/catalog.json hari ini.")
        elif s["status_hitung"] == "habis" and s["status_situs"] not in ("menunggu-panen", "habis"):
            add("kritis", "Produksi & QC", f"{s['produk']} habis (0 bungkus).", "Ubah status jadi Habis/Menunggu panen, lalu tawarkan produk serupa.")
        elif s["status_hitung"] == "terbatas":
            add("peringatan", "Produksi & QC", f"{s['produk']} tersisa {s['bungkus'].get('250 g', 0)} bungkus 250 g.", "Jadwalkan lot berikutnya; beri prioritas ke langganan.")

    for m in margin:
        if m.get("sehat") is False:
            v = min(m["varian"], key=lambda x: x["margin"])
            add("peringatan", "Keuangan", f"{m['produk']} margin {v['ukuran']} hanya {v['margin']*100:.0f}%.", "Naikkan harga, ubah ukuran terkecil, atau negosiasi harga green bean.")

    for o in proses:
        if o["telat"]:
            add("peringatan", "Penjualan & CRM", f"Order {o.get('nomor')} ({o.get('nama')}) menunggu {o['umur_hari']} hari.", "Konfirmasi & kirim hari ini; balas < 2 jam.")

    for r in resi:
        add("info", "Operasional & Logistik", f"Order {r.get('nomor')} belum punya nomor resi.", "Kirim resi ke pembeli lewat WhatsApp.")

    if follow:
        add("info", "Penjualan & CRM", f"{len(follow)} pelanggan jatuh tempo restock.", "Kirim template WA-4 (jangan lebih dari 1 pesan).")

    if konten_telat:
        add("info", "Marketing & Konten", f"{len(konten_telat)} konten lewat jadwal.", "Selesaikan atau jadwalkan ulang hari ini.")

    for b in qc["ditolak"]:
        add("info", "Produksi & QC", f"Batch {b.get('kode_batch')} ditolak ({b.get('skor_cupping')}).", "Pastikan batch pengganti sudah disangrai dan dicicipi.")

    belum = [x for x in legal if (x.get("status") or "").lower() not in ("selesai", "ada", "done")]
    if belum:
        add("info", "Brand & Legal", f"{len(belum)} dokumen legal belum selesai.", "Lihat daftar di papan bagian Legal.")

    urut = {"kritis": 0, "peringatan": 1, "info": 2}
    out.sort(key=lambda x: urut.get(x["level"], 3))
    return out


# ──────────────────────────────── render HTML ─────────────────────────────
CSS = """
:root{--paper:#F5EFE4;--paper2:#EFE6D6;--ink:#16110D;--muted:rgba(22,17,13,.58);
--orange:#E1542B;--espresso:#4A2C1A;--gold:#D9A441;--green:#2F6B4F;--red:#A32A1B;
--line:1px solid rgba(22,17,13,.14)}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Inter,system-ui,sans-serif}
h1,h2,h3{font-family:"Bricolage Grotesque",Inter,system-ui,sans-serif;letter-spacing:-.02em;margin:0}
.wrap{max-width:1180px;margin:0 auto;padding:24px clamp(16px,4vw,36px) 80px}
header.top{display:flex;flex-wrap:wrap;gap:14px;justify-content:space-between;align-items:flex-end;border-bottom:2px solid var(--ink);padding-bottom:16px;margin-bottom:22px}
.brand{font-weight:800;font-size:22px}
.brand small{display:block;font-size:9px;letter-spacing:.34em;text-transform:uppercase;color:var(--muted);font-weight:600}
.tanggal{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(22px,4vw,34px);font-weight:700;line-height:1}
.tanggal small{display:block;font:600 11px/1.6 Inter,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-top:6px}
.grid{display:grid;gap:16px}
.kpi{grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin-bottom:22px}
.kpi div{background:var(--paper2);border:var(--line);border-radius:6px;padding:12px 14px}
.kpi b{display:block;font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:24px;line-height:1.1}
.kpi span{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.kpi em{font-style:normal;font-size:11px;color:var(--muted)}
section{margin-bottom:26px}
h2{font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
.alert{display:grid;grid-template-columns:64px 1fr auto;gap:12px;align-items:start;border:var(--line);border-left:4px solid var(--muted);border-radius:5px;padding:11px 13px;background:#fff8}
.alert.kritis{border-left-color:var(--red)}.alert.peringatan{border-left-color:var(--gold)}.alert.info{border-left-color:var(--espresso)}
.alert .lvl{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.alert .div{font-size:10.5px;color:var(--muted);letter-spacing:.04em}
.alert b{display:block;font-weight:600}
.alert p{margin:2px 0 0;font-size:13.5px;color:var(--muted)}
.badge{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 8px;border-radius:99px;border:1px solid}
.b-tersedia{color:var(--green);border-color:var(--green)}.b-terbatas{color:#8a5a00;border-color:var(--gold);background:#fdf3dd}
.b-habis{color:#fff;background:var(--ink);border-color:var(--ink)}.b-baru{color:#fff;background:var(--orange);border-color:var(--orange)}
table{width:100%;border-collapse:collapse;font-size:13.5px;background:#fff8}
th,td{text-align:left;padding:8px 10px;border-bottom:var(--line);vertical-align:top}
th{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:600}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
tr.alert-row td{background:#fff1ec}
.divisi{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.card{border:var(--line);border-radius:6px;padding:14px;background:#fff8}
.card h3{font-size:15px;margin-bottom:2px}
.card .owner{font-size:11px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.card dl{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;margin:10px 0 0;font-size:13px}
.card dt{color:var(--muted)}.card dd{margin:0;text-align:right;font-variant-numeric:tabular-nums}
.card .next{margin-top:10px;font-size:12.5px;border-top:var(--line);padding-top:8px}
.empty{padding:14px;border:1px dashed rgba(22,17,13,.25);border-radius:6px;color:var(--muted);font-size:13.5px}
footer{margin-top:34px;border-top:2px solid var(--ink);padding-top:14px;font-size:12px;color:var(--muted);display:flex;flex-wrap:wrap;gap:8px 22px;justify-content:space-between}
code{background:var(--paper2);padding:1px 5px;border-radius:3px;font-size:12px}
.legend{font-size:12px;color:var(--muted);margin:-4px 0 10px}
"""

DIVISI = [
    ("Produksi & QC", "Ais Coffee Roastery · Nocturne memeriksa"),
    ("Penjualan & CRM", "owner · WhatsApp Business"),
    ("Marketing & Konten", "owner · IG / TikTok"),
    ("Operasional & Logistik", "owner · packing & kurir"),
    ("Keuangan", "owner · catatan kas"),
    ("Brand & Legal", "owner · dokumen usaha"),
]


def render(ctx):
    h = ctx["hari_ini"]
    tgl_teks = h.strftime("%A, %d %B %Y")
    hari_id = {"Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis",
               "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"}
    for en, idn in hari_id.items():
        tgl_teks = tgl_teks.replace(en, idn)
    bln_id = {"January": "Januari", "February": "Februari", "March": "Maret", "April": "April",
              "May": "Mei", "June": "Juni", "July": "Juli", "August": "Agustus",
              "September": "September", "October": "Oktober", "November": "November",
              "December": "Desember"}
    for en, idn in bln_id.items():
        tgl_teks = tgl_teks.replace(en, idn)

    k = ctx["kpi"]
    o = []

    o.append(f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Papan Harian — Nocturne Koffie</title>
<meta name="robots" content="noindex,nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<header class="top">
  <div class="brand">Nocturne<small>Koffie Brand · papan harian</small></div>
  <div class="tanggal">{tgl_teks}<small>Divisi aktif: 6 · dibuat {ctx['dibuat']}</small></div>
</header>""")

    # KPI
    if k:
        aov_target = TARGET["aov"]
        o.append('<div class="grid kpi">')
        for label, nilai, ket in [
            ("Order minggu ini", f"{k['order']}", f"target 90 hari: {TARGET['order_bulan']}/bulan"),
            ("Omzet minggu ini", RP(k["omzet"]), "retail, belum termasuk ongkir"),
            ("Nilai order rata-rata", RP(k["aov"]), f"target {RP(aov_target)}"),
            ("Langganan aktif", str(k["langganan"]), f"target {TARGET['langganan']}"),
            ("Akun B2B", str(k["b2b"]), f"target {TARGET['b2b']}"),
            ("Chat WA", str(k["chat"]), "masuk minggu ini"),
        ]:
            o.append(f'<div><span>{label}</span><b>{nilai}</b><em>{ket}</em></div>')
        o.append("</div>")

    # Peringatan
    o.append('<section><h2>Perlu keputusan hari ini</h2><div class="grid">')
    if ctx["peringatan"]:
        for a in ctx["peringatan"]:
            o.append(f"""<div class="alert {a['level']}">
      <div><div class="lvl">{a['level']}</div><div class="div">{a['divisi']}</div></div>
      <div><b>{a['teks']}</b><p>{a['aksi']}</p></div>
      <div></div></div>""")
    else:
        o.append('<div class="empty">Tidak ada peringatan. Sistem bersih untuk hari ini.</div>')
    o.append("</div></section>")

    # Divisi
    st = ctx["divisi"]
    o.append('<section><h2>Enam divisi</h2><div class="grid divisi">')
    for nama, owner in DIVISI:
        info = st.get(nama, {})
        o.append(f"""<div class="card"><h3>{nama}</h3><div class="owner">{owner}</div>
      <dl>{''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in info.get('metrics', []))}</dl>
      <div class="next"><b>Langkah berikutnya:</b> {info.get('next', '—')}</div></div>""")
    o.append("</div></section>")

    # Konten hari ini
    o.append('<section><h2>Marketing — jadwal konten</h2>')
    if ctx["konten_hari"]:
        for c in ctx["konten_hari"]:
            o.append(f'<div class="alert info"><div><div class="lvl">hari ini</div><div class="div">{c.get("platform")}</div></div>'
                     f'<div><b>{c.get("judul")}</b><p>Pilar {c.get("pilar")} · status {c.get("status")}</p></div><div></div></div>')
    else:
        o.append('<div class="empty">Tidak ada konten terjadwal hari ini. Rekam 3 klip saat sangrai/packing untuk stok konten.</div>')
    if ctx["konten_telat"]:
        o.append('<h2 style="margin-top:14px">Terlambat</h2>')
        for c in ctx["konten_telat"]:
            o.append(f'<div class="alert peringatan"><div><div class="lvl">lewat {c["lewat"]}h</div><div class="div">{c.get("platform")}</div></div>'
                     f'<div><b>{c.get("judul")}</b><p>Jadwal {c.get("tanggal")} · status {c.get("status")}</p></div><div></div></div>')
    if ctx["konten_berikut"]:
        o.append('<h2 style="margin-top:14px">Berikutnya</h2><table><tr><th>Tanggal</th><th>Platform</th><th>Judul</th><th>Pilar</th></tr>')
        for c in ctx["konten_berikut"]:
            o.append(f'<tr><td>{c.get("tanggal")}</td><td>{c.get("platform")}</td><td>{c.get("judul")}</td><td>{c.get("pilar")}</td></tr>')
        o.append("</table>")
    o.append("</section>")

    # Pesanan
    o.append('<section><h2>Penjualan — pesanan perlu diproses</h2>')
    if ctx["proses"]:
        o.append('<table><tr><th>Nomor</th><th>Tanggal</th><th>Nama</th><th>Produk</th><th>Ukuran</th><th class="num">Qty</th><th class="num">Total</th><th>Status</th><th class="num">Umur</th></tr>')
        for p in ctx["proses"]:
            cls = ' class="alert-row"' if p["telat"] else ""
            o.append(f'<tr{cls}><td>{p.get("nomor")}</td><td>{p.get("tanggal")}</td><td>{p.get("nama")}</td>'
                     f'<td>{p.get("produk")}</td><td>{p.get("ukuran")}</td><td class="num">{p.get("qty")}</td>'
                     f'<td class="num">{RP(float(p.get("total") or 0))}</td><td><span class="badge b-baru">{p.get("status")}</span></td>'
                     f'<td class="num">{p["umur_hari"]}h</td></tr>')
        o.append("</table>")
    else:
        o.append('<div class="empty">Tidak ada pesanan menunggu. Waktu terbaik untuk menjemput B2B.</div>')
    if ctx["follow"]:
        o.append('<h2 style="margin-top:14px">Restock jatuh tempo</h2><table><tr><th>Nama</th><th>Produk terakhir</th><th>Order terakhir</th><th class="num">Lewat</th></tr>')
        for f in ctx["follow"]:
            o.append(f'<tr><td>{f["nama"]}</td><td>{f["produk"]}</td><td>{f["order_terakhir"]}</td><td class="num">{f["lewat_hari"]}h</td></tr>')
        o.append("</table>")
    o.append("</section>")

    # Stok
    o.append('<section><h2>Produksi — stok per SKU</h2><div class="legend">Sisa dihitung dari green bean × yield, bukan dari kopi jadi. “Beda” = status di situs berbeda dari hitungan lot.</div>')
    o.append('<table><tr><th>Produk</th><th class="num">Green sisa</th><th class="num">Roasted</th><th class="num">100g</th><th class="num">250g</th><th class="num">500g</th><th class="num">1kg</th><th class="num">Terjual 28h</th><th class="num">Hari</th><th>Status lot</th><th>Situs</th></tr>')
    for s in ctx["stok"]:
        cls = ' class="alert-row"' if s["beda_status"] else ""
        hari = "—" if s["hari_tersisa"] is None else (">365" if s["hari_tersisa"] > 365 else str(s["hari_tersisa"]))
        o.append(f'<tr{cls}><td>{s["produk"]}</td><td class="num">{s["sisa_green_kg"]} kg</td><td class="num">{s["roasted_g"]/1000:.2f} kg</td>'
                 f'<td class="num">{s["bungkus"].get("100 g",0)}</td><td class="num">{s["bungkus"].get("250 g",0)}</td>'
                 f'<td class="num">{s["bungkus"].get("500 g",0)}</td><td class="num">{s["bungkus"].get("1 kg",0)}</td>'
                 f'<td class="num">{s["terjual_28h_g"]} g</td><td class="num">{hari}</td>'
                 f'<td><span class="badge b-{s["status_hitung"]}">{s["status_hitung"]}</span></td>'
                 f'<td><span class="badge b-{s["status_situs"]}">{s["status_situs"]}</span></td></tr>')
    o.append("</table></section>")

    # Margin
    o.append('<section><h2>Keuangan — margin per ukuran</h2><div class="legend">HPP = green bean ÷ yield + kemasan + label + tenaga. Target margin kotor ≥ 35%.</div>')
    o.append('<table><tr><th>Produk</th><th class="num">Green/kg</th>' +
             "".join(f'<th class="num">{v["ukuran"]}</th>' for v in ctx["margin"][0]["varian"]) +
             '<th class="num">Terburuk</th></tr>')
    for m in ctx["margin"]:
        sel = "".join(
            f'<td class="num" style="color:{"var(--red)" if not v["sehat"] else "inherit"}">{v["margin"]*100:.0f}%<br><small>{RP(v["hpp"])}</small></td>'
            for v in m["varian"])
        o.append(f'<tr><td>{m["produk"]}</td><td class="num">{RP(m["green_per_kg"])}</td>{sel}'
                 f'<td class="num"><b>{m.get("margin_terburuk",0)*100:.0f}%</b></td></tr>')
    o.append("</table>")
    be = ctx["break_even"]
    o.append(f'<div class="legend" style="margin-top:10px">Biaya tetap {RP(be["biaya_tetap"])}/bulan · '
             f'rata-rata laba per order {RP(be["laba_per_order"])} · break-even <b>{be["order_per_bulan"]} order/bulan</b> '
             f'(±{be["order_per_minggu"]} order/minggu).</div></section>')

    # QC
    q = ctx["qc"]
    o.append(f'<section><h2>Produksi — QC batch (30 hari)</h2><div class="legend">{q["jumlah_30h"]} batch · {len(q["ditolak"])} ditolak · skor rata-rata {q["skor_rata"] if q["skor_rata"] is not None else "—"}</div>')
    if q["terakhir"]:
        o.append('<table><tr><th>Tanggal</th><th>Kode batch</th><th>Produk</th><th class="num">Yield</th><th class="num">Skor</th><th>Status</th><th>Catatan</th></tr>')
        for b in q["terakhir"]:
            warna = "var(--red)" if (b.get("status") or "").lower() == "ditolak" else "inherit"
            o.append(f'<tr><td>{b.get("tanggal")}</td><td>{b.get("kode_batch")}</td><td>{b.get("produk")}</td>'
                     f'<td class="num">{b.get("yield")}</td><td class="num">{b.get("skor_cupping")}</td>'
                     f'<td style="color:{warna}"><b>{b.get("status")}</b></td><td>{b.get("catatan")}</td></tr>')
        o.append("</table>")
    else:
        o.append('<div class="empty">Belum ada catatan batch 30 hari terakhir. Mulai catat setiap sangrai di <code>data/batch-qc.csv</code>.</div>')
    o.append("</section>")

    # Legal
    o.append('<section><h2>Brand & Legal</h2><table><tr><th>Dokumen</th><th>Status</th><th>Catatan</th></tr>')
    for x in ctx["legal"]:
        stt = (x.get("status") or "").lower()
        warna = "var(--green)" if stt in ("selesai", "ada", "done") else "var(--red)"
        o.append(f'<tr><td>{x.get("nama")}</td><td style="color:{warna}"><b>{x.get("status")}</b></td><td>{x.get("catatan","")}</td></tr>')
    o.append("</table></section>")

    o.append(f"""<footer>
  <span>Dibuat otomatis oleh <code>tools/papan.py</code> pada {ctx['dibuat']}.</span>
  <span>Angka biaya di <code>data/biaya.json</code> masih <b>asumsi</b> — ganti dengan angka nyata.</span>
</footer></div></body></html>""")
    return "\n".join(o)


# ────────────────────────────────── main ──────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tanggal", help="YYYY-MM-DD (default: hari ini WIB)")
    ap.add_argument("--json", action="store_true", help="cetak ringkasan JSON saja")
    args = ap.parse_args()

    now = datetime.now(TZ) if TZ else datetime.now()
    hari_ini = parse_tanggal(args.tanggal) if args.tanggal else now.date()

    catalog = baca_json(D("catalog.json"))
    biaya = baca_json(D("biaya.json"))
    stok_raw = baca_json(D("stok-lot.json"))
    legal = baca_json(D("legal.json"), {}).get("dokumen", [])
    pesanan = baca_csv(D("pesanan.csv"))
    konten = baca_csv(D("konten-14hari.csv"))
    batch = baca_csv(D("batch-qc.csv"))
    kpi = baca_csv(D("kpi.csv"))

    margin, per_pack, yield_, target_margin = hitung_margin(catalog, biaya)
    stok = hitung_stok(catalog, stok_raw, biaya, pesanan, hari_ini)
    proses, resi, follow = analisa_pesanan(pesanan, hari_ini)
    konten_hari, konten_telat, konten_berikut = analisa_konten(konten, hari_ini)
    qc = analisa_qc(batch, hari_ini)
    kpi_last = analisa_kpi(kpi)

    biaya_tetap = sum(float(x.get("nilai") or 0) for x in biaya.get("asumsi", {}).get("biaya_tetap_bulanan", []))
    margins = [m for m in margin if m.get("varian")]
    rata_margin = sum(m["margin_terburuk"] for m in margins) / len(margins) if margins else 0
    aov = kpi_last["aov"] if kpi_last and kpi_last["aov"] else 130000
    laba_per_order = max(1000.0, aov * rata_margin)
    break_even = {
        "biaya_tetap": biaya_tetap,
        "laba_per_order": round(laba_per_order),
        "order_per_bulan": math.ceil(biaya_tetap / laba_per_order) if laba_per_order else 0,
        "order_per_minggu": math.ceil((biaya_tetap / laba_per_order) / 4.3) if laba_per_order else 0,
    }

    peringatan = susun_peringatan(stok, margin, proses, resi, follow, konten_telat, qc, legal)

    kritis = sum(1 for s in stok if s["beda_status"] or s["status_hitung"] == "habis")
    divisi = {
        "Produksi & QC": {
            "metrics": [("Batch 30 hari", qc["jumlah_30h"]),
                        ("Batch ditolak", len(qc["ditolak"])),
                        ("SKU stok kritis", kritis),
                        ("Skor cupping rata", qc["skor_rata"] if qc["skor_rata"] is not None else "—")],
            "next": "Catat batch sangrai berikutnya & perbarui status stok di situs." if kritis else "Jadwalkan sangrai mingguan; tidak ada SKU kritis.",
        },
        "Penjualan & CRM": {
            "metrics": [("Order perlu diproses", len(proses)),
                        ("Restock jatuh tempo", len(follow)),
                        ("Chat masuk", kpi_last["chat"] if kpi_last else "—"),
                        ("Resi belum dikirim", len(resi))],
            "next": "Balas semua chat < 2 jam dan kirim resi yang tertunda." if (proses or resi) else "Tidak ada yang menunggu — pakai waktu untuk menyapa 5 pelanggan lama.",
        },
        "Marketing & Konten": {
            "metrics": [("Konten hari ini", len(konten_hari)),
                        ("Konten terlambat", len(konten_telat)),
                        ("Followers IG", kpi_last["followers"] if kpi_last else "—"),
                        ("Chat dari konten", "—")],
            "next": "Selesaikan konten terjadwal; kalau kosong, rekam 3 klip mentah hari ini.",
        },
        "Operasional & Logistik": {
            "metrics": [("Siap dikirim", len(proses)),
                        ("Tanpa resi", len(resi)),
                        ("Order 30 hari", len([p for p in pesanan if (p.get("status") or "").lower() not in ("batal", "dibatalkan")])),
                        ("Kemasan tersedia", "cek stok")],
            "next": "Packing hanya setelah pembayaran terkonfirmasi; kirim resi hari yang sama.",
        },
        "Keuangan": {
            "metrics": [("Omzet minggu ini", RP(kpi_last["omzet"]) if kpi_last else "—"),
                        ("AOV", RP(aov)),
                        ("Margin terburuk", f"{rata_margin*100:.0f}%"),
                        ("Break-even", f"{break_even['order_per_bulan']} order/bln")],
            "next": "Perbarui catatan kas mingguan; jangan memutuskan harga dari angka asumsi." if rata_margin < target_margin else "Catat pengeluaran mingguan dan cocokkan dengan biaya tetap.",
        },
        "Brand & Legal": {
            "metrics": [("Dokumen selesai", f"{sum(1 for x in legal if (x.get('status') or '').lower() in ('selesai','ada','done'))}/{len(legal)}"),
                        ("Izin yang ditunggu", f"{sum(1 for x in legal if (x.get('status') or '').lower() not in ('selesai','ada','done'))}"),
                        ("Klaim situs", "sesuai brief 11.8"),
                        ("Data petani", "izin publikasi")],
            "next": "Lengkapi NIB & izin publikasi nama petani sebelum kampanye besar.",
        },
    }

    ctx = {
        "hari_ini": hari_ini, "dibuat": (now.strftime("%d %b %Y %H:%M") + " WIB"),
        "kpi": kpi_last, "peringatan": peringatan, "divisi": divisi,
        "konten_hari": konten_hari, "konten_telat": konten_telat, "konten_berikut": konten_berikut,
        "proses": proses, "follow": follow, "resi": resi,
        "stok": stok, "margin": margin, "qc": qc, "legal": legal,
        "break_even": break_even, "rata_margin": rata_margin,
    }

    if args.json:
        ringkas = {k: v for k, v in ctx.items() if k not in ("margin", "stok", "qc")}
        ringkas["alerts"] = peringatan
        ringkas["break_even"] = break_even
        print(json.dumps(ringkas, ensure_ascii=False, indent=2, default=str))
        return

    out_dir = os.path.join(ROOT, "dashboard")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(render(ctx))
    with open(os.path.join(out_dir, "data.json"), "w", encoding="utf-8") as f:
        json.dump(ctx, f, ensure_ascii=False, indent=2, default=str)

    # ringkasan terminal
    print(f"Papan harian — {hari_ini.isoformat()}")
    print(f"  peringatan      : {len(peringatan)} ({sum(1 for x in peringatan if x['level']=='kritis')} kritis)")
    print(f"  order diproses  : {len(proses)} | restock due: {len(follow)} | resi kosong: {len(resi)}")
    print(f"  konten hari ini : {len(konten_hari)} | terlambat: {len(konten_telat)}")
    print(f"  margin terburuk : {rata_margin*100:.0f}% | break-even {break_even['order_per_bulan']} order/bulan")
    print(f"  dashboard       : dashboard/index.html")


if __name__ == "__main__":
    main()
