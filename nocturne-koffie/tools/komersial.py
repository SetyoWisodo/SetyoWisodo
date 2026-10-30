#!/usr/bin/env python3
"""
Mesin komersial Nocturne — harga grosir, penawaran B2B, pipeline.

Menulis ke folder komersial/:
  harga-grosir.csv        harga per kg untuk 4 tingkat volume + marginnya
  penawaran-b2b.html      proposal satu halaman (siap cetak / simpan PDF)
  pipeline-b2b.csv        kerangka 30 prospek (kalau belum ada)

Pakai:
    python3 tools/komersial.py
    python3 tools/komersial.py --tanggal 2026-11-02
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "komersial")
D = lambda *p: os.path.join(ROOT, "data", *p)
RP = lambda n: "Rp" + f"{round(n):,}".replace(",", ".")

# target margin kotor per tingkat volume (dari penjualan ke pembeli bisnis)
TIER = [
    {"nama": "Kafe kecil", "min_kg": 5, "margin": 0.28, "termin": "COD / transfer di muka"},
    {"nama": "Kafe aktif", "min_kg": 10, "margin": 0.25, "termin": "Net 7 hari"},
    {"nama": "Kantor / Hotel", "min_kg": 20, "margin": 0.23, "termin": "Net 14 hari"},
    {"nama": "Reseller / Private label", "min_kg": 30, "margin": 0.20, "termin": "Net 14 hari + DP 50%"},
]


def baca(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def hitung(catalog, biaya):
    a = biaya.get("asumsi", {})
    yield_ = float(a.get("yield_sangrai", 0.8) or 0.8)
    per_pack = sum(float(a.get(k, 0) or 0) for k in (
        "kemasan_per_bungkus", "label_stiker", "tenaga_kerja_per_bungkus", "lain_lain_per_bungkus"))
    green = biaya.get("harga_green_per_kg", {})

    baris = []
    for p in catalog.get("products", []):
        kg_harga = green.get(p["id"])
        if not kg_harga:
            continue
        # grosir dikemas 1 kantong 1 kg: biaya kemas 1x, bukan 4x
        hpp_kg = float(kg_harga) / yield_ + per_pack

        retail_kg = None
        for v in p.get("variants", []):
            if v.get("grams") == 1000:
                retail_kg = float(v["price"])
        if retail_kg is None:
            var = max(p.get("variants", []), key=lambda v: v.get("grams", 0))
            retail_kg = float(var["price"]) * (1000 / float(var["grams"]))

        row = {
            "produk": p["name"], "id": p["id"], "kategori": p["category"],
            "green_per_kg": int(float(kg_harga)), "hpp_per_kg": round(hpp_kg),
            "retail_per_kg": round(retail_kg),
            "margin_retail": round((retail_kg - hpp_kg) / retail_kg, 4),
        }
        for t in TIER:
            harga_target = hpp_kg / (1 - t["margin"])
            # harga grosir tidak boleh melebihi retail (kecuali retail terlalu murah → ditandai)
            batas = retail_kg * 0.92
            harga = min(harga_target, batas)
            harga = int(round(harga / 500.0) * 500)
            margin = (harga - hpp_kg) / harga if harga else 0
            row[f"grosir_{t['min_kg']}kg"] = harga
            row[f"margin_{t['min_kg']}kg"] = round(margin, 4)
            if margin < 0.18:
                row.setdefault("_masalah", []).append(
                    f"margin grosir {t['min_kg']} kg hanya {margin*100:.0f}% — harga retail mungkin terlalu murah")
        baris.append(row)
    return baris, TIER


def tulis_csv(baris):
    path = os.path.join(OUT, "harga-grosir.csv")
    cols = ["produk", "kategori", "green_per_kg", "hpp_per_kg", "retail_per_kg", "margin_retail"]
    for t in TIER:
        cols += [f"grosir_{t['min_kg']}kg", f"margin_{t['min_kg']}kg"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in baris:
            r = dict(r)
            r["margin_retail"] = f"{r['margin_retail']*100:.0f}%"
            for t in TIER:
                k = f"margin_{t['min_kg']}kg"
                if k in r:
                    r[k] = f"{r[k]*100:.0f}%"
            w.writerow(r)
    return path


def html_proposal(baris, tgl):
    contoh = sorted(baris, key=lambda r: -r["retail_per_kg"])[:4]
    rows = "".join(
        f"<tr><td>{r['produk']}</td><td class='num'>{RP(r['retail_per_kg'])}</td>"
        f"<td class='num'>{RP(r['grosir_5kg'])}</td><td class='num'>{RP(r['grosir_10kg'])}</td>"
        f"<td class='num'>{RP(r['grosir_20kg'])}</td><td class='num'>{RP(r['grosir_30kg'])}</td></tr>"
        for r in baris)

    def blok_tier(t):
        idx = TIER.index(t) + 1
        return f"""<div class="tier">
      <div class="tier__no">0{idx}</div>
      <h3>{t['nama']}</h3>
      <p class="tier__min">Mulai {t['min_kg']} kg / pengiriman</p>
      <p class="tier__term">Termin: {t['termin']}</p>
    </div>"""

    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Penawaran Kemitraan — Nocturne Koffie</title>
<style>
:root{{--paper:#F5EFE4;--ink:#16110D;--muted:#6b6156;--orange:#E1542B;--gold:#D9A441;--line:1px solid rgba(22,17,13,.16)}}
*{{box-sizing:border-box}}
body{{margin:0;background:#fff;color:var(--ink);font:15px/1.6 Inter,system-ui,sans-serif}}
.page{{max-width:860px;margin:0 auto;padding:56px 54px 64px;background:var(--paper)}}
.mark{{width:26px;height:26px;border-radius:50%;background:var(--ink);position:relative;display:inline-block;vertical-align:middle}}
.mark::after{{content:"";position:absolute;top:-2px;bottom:-2px;left:47%;width:6%;background:var(--paper)}}
.lock{{display:flex;align-items:center;gap:10px;font-family:"Bricolage Grotesque",Inter,sans-serif;font-weight:800;font-size:22px}}
.lock small{{display:block;font:600 8px/1.6 Inter,sans-serif;letter-spacing:.34em;color:var(--muted);text-transform:uppercase}}
.kicker{{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin:38px 0 8px}}
h1{{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:42px;line-height:1.02;letter-spacing:-.03em;margin:0 0 14px}}
h2{{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin:38px 0 12px;border-top:2px solid var(--ink);padding-top:12px}}
h3{{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:20px;margin:0 0 6px}}
.tier h3{{font-size:16px;margin:8px 0 2px}}
.tier{{border-top:2px solid var(--ink);padding-top:14px}}
p{{margin:0 0 12px;max-width:62ch}}
.lede{{font-size:17px;max-width:56ch}}
.hero{{display:grid;grid-template-columns:1.4fr 1fr;gap:34px;align-items:start}}
.box{{background:var(--ink);color:var(--paper);padding:20px 22px}}
.box p{{color:rgba(245,239,228,.8);margin:0 0 8px;font-size:13.5px}}
.box b{{color:var(--gold);font-size:11px;letter-spacing:.16em;text-transform:uppercase;display:block;margin-bottom:10px}}
ul{{margin:0 0 16px;padding-left:18px}}
li{{margin-bottom:6px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th,td{{text-align:left;padding:8px 8px;border-bottom:var(--line)}}
th{{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:600}}
td.num,th.num{{text-align:right;font-variant-numeric:tabular-nums}}
.tiers{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:8px}}
.tier{{border:var(--line);padding:12px}}
.tier__no{{font:700 10px/1 Inter,sans-serif;letter-spacing:.16em;color:var(--espresso)}}
.tier__min{{font-size:12.5px;margin:6px 0 0}}
.tier__term{{font-size:11.5px;color:var(--muted);margin:2px 0 0}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:30px}}
.foot{{margin-top:44px;border-top:2px solid var(--ink);padding-top:14px;display:flex;justify-content:space-between;font-size:12px;color:var(--muted)}}
.sig{{margin-top:30px;display:grid;grid-template-columns:1fr 1fr;gap:30px;font-size:12.5px;color:var(--muted)}}
.sig div{{border-top:1px solid var(--ink);padding-top:8px}}
@media print{{body{{background:#fff}} .page{{padding:24px 28px;max-width:none}} h2{{break-after:avoid}} table{{break-inside:avoid}}}}
@media (max-width:760px){{.hero,.two,.tiers{{grid-template-columns:1fr}} .page{{padding:28px 20px}} h1{{font-size:30px}}}}
</style></head><body><div class="page">

<div class="lock"><span class="mark"></span><span>Nocturne<small>Koffie Brand</small></span></div>

<p class="kicker">Penawaran kemitraan · {tgl.strftime('%d %B %Y')}</p>
<h1>Kopi yang bisa Anda pertanggungjawabkan<br>ke pelanggan Anda.</h1>
<p class="lede">Kami brand kopi dari Banyuwangi. Biji kami pilih sendiri dari petani, disangrai mingguan
oleh Ais Coffee Roastery, dan setiap batch kami cicipi sebelum dikirim. Yang Anda beli bukan
sekadar kopi: ada tanggal sangrai, kode batch, dan catatan skor rasa untuk setiap pengiriman.</p>

<div class="hero">
  <div>
    <h2>Kenapa ini berbeda</h2>
    <ul>
      <li><b>Konsistensi terjaga.</b> Profil sangrai dicatat per batch dan diulang pada pengiriman berikutnya — bukan mengandalkan perasaan barista.</li>
      <li><b>Tanggal sangrai, bukan tanggal kedaluwarsa.</b> Anda tahu persis umur kopi yang masuk ke bar.</li>
      <li><b>Nama petani & elevasi tercantum.</b> Bisa diceritakan ke pelanggan Anda, dan itu menjual.</li>
      <li><b>Kalibrasi awal gratis.</b> Kami bantu setel grinder dan rasio di kunjungan pertama agar rasa di cangkir sesuai yang kami uji.</li>
      <li><b>Satu area, satu mitra.</b> Kami tidak menjual ke tetangga Anda di jalan yang sama.</li>
    </ul>
  </div>
  <div class="box">
    <b>Ringkas</b>
    <p>Minimum 5 kg per pengiriman</p>
    <p>Lead time 5–7 hari setelah konfirmasi</p>
    <p>Pengiriman mingguan atau dua mingguan</p>
    <p>Kemasan 1 kg (valve) atau sesuai permintaan</p>
    <p style="margin-top:14px"><span style="color:#D9A441">Sampel 2 × 100 g gratis</span> sebelum Anda memutuskan.</p>
  </div>
</div>

<h2>Empat tingkat kemitraan</h2>
<div class="tiers">{''.join(blok_tier(t) for t in TIER)}</div>

<h2>Daftar harga per kg</h2>
<p style="font-size:13px;color:var(--muted)">Harga sudah termasuk kemasan 1 kg. Harga retail dicantumkan sebagai pembanding — bukan harga yang Anda bayar.
Berlaku sampai stok lot tersedia; harga lot baru dapat berbeda dan akan diberitahukan lebih dulu.</p>
<table>
<tr><th>Kopi</th><th class="num">Retail /kg</th><th class="num">5 kg</th><th class="num">10 kg</th><th class="num">20 kg</th><th class="num">30 kg</th></tr>
{rows}
</table>

<div class="two" style="margin-top:34px">
  <div>
    <h2>Alur kerja</h2>
    <ol style="padding-left:18px">
      <li>Sampel gratis 2 × 100 g (Anda pilih profilnya).</li>
      <li>Anda tes; kami minta 1 kalimat kesan agar profil bisa disesuaikan.</li>
      <li>Kalibrasi di tempat (grinder, dosis, rasio) — gratis, sekali.</li>
      <li>Batch percobaan 5 kg; setelah cocok, jadwal tetap.</li>
    </ol>
  </div>
  <div>
    <h2>Yang kami minta</h2>
    <ul>
      <li>Konfirmasi volume per bulan agar jadwal sangrai bisa dipesan.</li>
      <li>Pembayaran sesuai termin tingkat yang dipilih.</li>
      <li>Kabar kalau rasa berubah drastis — biasanya soal penyimpanan atau kalibrasi, dan itu bisa kami bantu.</li>
    </ul>
  </div>
</div>

<h2>Kontak</h2>
<p>WhatsApp <b>+62 898-8188-800</b> · {os.environ.get('NK_EMAIL', 'nocturnekoffiebrand@gmail.com')} · nocturnekoffie.id<br>
Senin–Sabtu 09.00–21.00 WIB, balasan biasanya di bawah 2 jam.</p>

<div class="sig">
  <div>Untuk Nocturne Koffie<br><span style="opacity:.6">Nama & tanda tangan</span></div>
  <div>Untuk mitra<br><span style="opacity:.6">Nama, jabatan, tanggal</span></div>
</div>

<div class="foot">
  <span>Nocturne Koffie Brand · Banyuwangi, Jawa Timur</span>
  <span>Dokumen ini bukan kontrak; harga & ketersediaan dikonfirmasi per batch.</span>
</div>
</div></body></html>"""


def tulis_pipeline():
    path = os.path.join(OUT, "pipeline-b2b.csv")
    if os.path.exists(path):
        return path, False
    kolom = ["nama_tempat", "jenis", "area", "kontak", "sumber", "tanggal_pesan",
             "status", "volume_target_kg", "profil_diminta", "tanggal_followup", "catatan"]
    contoh = [
        ["(contoh) Kedai Senja", "kafe", "Banyuwangi kota", "62812xxxxxxx", "riset map", "", "belum", "10", "espresso / milk-based", "", ""],
        ["(contoh) Kantor PT Sinar", "kantor", "Banyuwangi", "62813xxxxxxx", "referensi", "", "belum", "20", "filter / tubruk", "", ""],
        ["(contoh) Hotel Ijen View", "hotel", "Banyuwangi", "62814xxxxxxx", "instagram", "", "belum", "20", "drip bag", "", ""],
        ["(contoh) Toko Oleh-oleh", "reseller", "Banyuwangi", "62815xxxxxxx", "walk-in", "", "belum", "30", "blend 70/30", "", ""],
    ]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(kolom)
        w.writerows(contoh)
    return path, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tanggal", default=None)
    args = ap.parse_args()
    tgl = date.fromisoformat(args.tanggal) if args.tanggal else date.today()

    os.makedirs(OUT, exist_ok=True)
    catalog = baca(D("catalog.json"))
    biaya = baca(D("biaya.json"))

    baris, _ = hitung(catalog, biaya)
    csv_path = tulis_csv(baris)
    html_path = os.path.join(OUT, "penawaran-b2b.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_proposal(baris, tgl))
    pipe_path, baru = tulis_pipeline()

    print("Mesin komersial siap")
    print("  harga grosir :", os.path.relpath(csv_path, ROOT))
    print("  penawaran    :", os.path.relpath(html_path, ROOT))
    print("  pipeline     :", os.path.relpath(pipe_path, ROOT), "(baru)" if baru else "(sudah ada)")
    print()
    print(f"  {'produk':<18}{'retail/kg':>12}{'5 kg':>11}{'m':>5}{'10 kg':>11}{'m':>5}{'20 kg':>11}{'m':>5}")
    for r in baris:
        print(f"  {r['produk']:<18}{RP(r['retail_per_kg']):>12}"
              f"{RP(r['grosir_5kg']):>11}{r['margin_5kg']*100:>4.0f}%"
              f"{RP(r['grosir_10kg']):>11}{r['margin_10kg']*100:>4.0f}%"
              f"{RP(r['grosir_20kg']):>11}{r['margin_20kg']*100:>4.0f}%")
    masalah = [(r['produk'], m) for r in baris for m in r.get("_masalah", [])]
    if masalah:
        print("\n  ⚠ perlu keputusan harga:")
        for nama, m in masalah[:8]:
            print(f"    - {nama}: {m}")


if __name__ == "__main__":
    main()
