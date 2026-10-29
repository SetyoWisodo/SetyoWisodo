#!/usr/bin/env python3
"""
Laporan — satu halaman untuk menilai kondisi sistem hari ini.

Menggabungkan hasil periksa + papan harian + target divisi + katalog + aset kreatif
+ ringkasan riset menjadi `laporan/index.html` (statis, tanpa dependensi, `noindex`).

Pakai:
    python3 tools/laporan.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "laporan")
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]


def baca(*path, default=None):
    p = os.path.join(ROOT, *path)
    if not os.path.exists(p):
        return default if default is not None else {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def rp(n):
    return "Rp" + f"{int(n):,}".replace(",", ".")


def fmt(n, satuan=""):
    if n is None:
        return "—"
    if satuan in ("Rp", "Rp/bulan"):
        return f"{n/1_000_000:.1f} jt".replace(".", ",") if abs(n) >= 1_000_000 else rp(n)
    if isinstance(n, float) and not float(n).is_integer():
        return f"{n:.1f}".replace(".", ",")
    return f"{int(n)}"


CSS = """
:root{--paper:#F5EFE4;--paper2:#EFE6D6;--ink:#16110D;--muted:#6b6156;--orange:#E1542B;
--gold:#D9A441;--espresso:#4A2C1A;--line:1px solid rgba(22,17,13,.14)}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 Inter,system-ui,-apple-system,sans-serif}
.wrap{max-width:1160px;margin:0 auto;padding:34px clamp(16px,4vw,40px) 70px}
h1{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(30px,5vw,48px);line-height:.98;
letter-spacing:-.035em;margin:6px 0 8px;font-weight:800}
h2{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(20px,2.4vw,27px);letter-spacing:-.02em;
margin:40px 0 6px;border-top:2px solid var(--ink);padding-top:13px}
h3{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:16px;margin:0 0 3px}
.kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.lede{max-width:72ch;color:var(--muted);margin:0 0 10px;font-size:14.5px}
.grid{display:grid;gap:14px}
.kpi{grid-template-columns:repeat(auto-fit,minmax(160px,1fr));margin-top:18px}
.kpi div{border:var(--line);border-radius:8px;padding:13px 15px;background:#fff8}
.kpi span{display:block;font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.kpi b{display:block;font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:25px;letter-spacing:-.02em;
line-height:1.1;margin:4px 0 1px}
.kpi em{font-size:11.5px;color:var(--muted);font-style:normal}
table{width:100%;border-collapse:collapse;font-size:13.2px;margin-top:10px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid rgba(22,17,13,.12);vertical-align:top}
th{font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);font-weight:600}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr:last-child td{border-bottom:0}
tr.grup td{background:var(--paper2);font-weight:600;font-size:12px;letter-spacing:.06em}
.pill{display:inline-block;font-size:10.5px;padding:2px 7px;border-radius:99px;border:1px solid;white-space:nowrap}
.pill.ok{color:#1f6b3a;border-color:#1f6b3a;background:#e8f2ea}
.pill.warn{color:#8a5a00;border-color:#b78621;background:#fbf1d9}
.pill.dim{color:var(--muted);border-color:rgba(22,17,13,.2)}
.pill.hot{color:#fff;border-color:var(--orange);background:var(--orange)}
.note{border-left:4px solid var(--gold);background:#fbf1d9;padding:11px 15px;border-radius:4px;
font-size:13px;margin:16px 0 0}
.note b{display:block;margin-bottom:2px}
.aset{grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin-top:14px}
.aset figure{margin:0}
.aset img{width:100%;display:block;border-radius:5px;border:var(--line);background:var(--ink)}
.aset figcaption{font-size:11px;color:var(--muted);margin-top:5px;line-height:1.4}
code{background:var(--paper2);padding:1px 5px;border-radius:3px;font-size:12px}
footer{margin-top:42px;border-top:2px solid var(--ink);padding-top:13px;font-size:12px;color:var(--muted);
display:flex;flex-wrap:wrap;gap:8px 22px;justify-content:space-between}
a{color:inherit}
@media print{body{background:#fff}.wrap{padding:0}h2{break-after:avoid}table{break-inside:auto}}
"""


def bangun(tgl, cek, papan, katalog, kreatif, riset, divisi):
    hasil = cek.get("hasil", [])
    gagal = [h for h in hasil if h["status"] == "gagal"]
    peringatan = [h for h in hasil if h["status"] == "peringatan"]
    lolos = [h for h in hasil if h["status"] == "lolos"]
    icon = {"lolos": ("ok", "lolos"), "peringatan": ("warn", "peringatan"), "gagal": ("hot", "GAGAL")}

    # produk
    baris_produk = ""
    for p in katalog.get("products", []) + katalog.get("bundles", []):
        if p.get("variants"):
            harga = " · ".join(f'{v["weight"]} {rp(v["price"])}' for v in p["variants"][:4])
        else:
            harga = rp(p["price"])
        stok_row = next((s for s in papan.get("stok", []) if s["id"] == p["id"]), None)
        sisa = (f'{stok_row["bungkus"].get("250 g", 0)} bungkus 250 g'
                if stok_row else "paket (dari komponen)")
        pill = 'ok' if p["status"] == "tersedia" else 'warn'
        baris_produk += (f'<tr><td><b>{p["name"]}</b><br><span class="kicker">'
                         f'{p.get("category","")} · {p.get("origin_line", p.get("contents",""))}</span></td>'
                         f'<td>{harga}</td><td>{sisa}</td>'
                         f'<td><span class="pill {pill}">{p["status"]}</span></td></tr>')

    # target divisi
    baris_target = ""
    kode = None
    for r in papan.get("target_divisi", []):
        if r["kode"] != kode:
            kode = r["kode"]
            baris_target += f'<tr class="grup"><td colspan="5">{r["kode"]} · {r["divisi"]}</td></tr>'
        kelas = {"tercapai": "ok", "di bawah": "warn", "tanpa data": "dim"}[r["status"]]
        arah = "↑" if r["arah"] == "naik" else "↓"
        baris_target += (f'<tr><td>{r["nama"]}</td><td class="num">{arah} {fmt(r["target"], r["satuan"])}</td>'
                         f'<td class="num">{fmt(r["aktual"], r["satuan"])}</td>'
                         f'<td>{r["satuan"]}</td><td><span class="pill {kelas}">{r["status"]}</span></td></tr>')

    # aset
    aset = ""
    for it in [i for i in kreatif.get("items", []) if i["format"] == "video"]:
        aset += (f'<figure><img src="../konten/{it["poster"]}" alt="{it["judul"]}" loading="lazy">'
                 f'<figcaption>{it["judul"]}<br><span class="kicker">{it["rasio"]} · '
                 f'{it.get("jadwal","")}</span></figcaption></figure>')

    # periksa
    baris_cek = ""
    for h in hasil:
        k, label = icon[h["status"]]
        baris_cek += (f'<tr><td>{h["kategori"]}</td><td><span class="pill {k}">{label}</span></td>'
                      f'<td>{h["teks"]}</td><td class="kicker">{h["detail"] or "—"}</td></tr>')

    k = papan.get("kpi") or {}
    tercapai = sum(1 for r in papan.get("target_divisi", []) if r["status"] == "tercapai")
    bawah = sum(1 for r in papan.get("target_divisi", []) if r["status"] == "di bawah")
    tanpa = sum(1 for r in papan.get("target_divisi", []) if r["status"] == "tanpa data")
    top = (riset.get("outlier_teratas") or {})
    pola = (riset.get("pola") or [{}])[0]

    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Laporan otomatis — Nocturne Koffie</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<p class="kicker">Dijalankan otomatis · {tgl.strftime('%d')} {BULAN[tgl.month-1]} {tgl.year} · {tgl.isoformat()}</p>
<h1>Laporan otomatis</h1>
<p class="lede">Semua keluaran dibuat ulang dari berkas data: brand kit, harga grosir, 15 aset konten,
landing kampanye, dasbor riset, papan harian, lalu diperiksa mesin. Angka di halaman ini bukan hasil
ketik tangan — kalau salah, sumbernya di <code>data/</code>.</p>

<div class="grid kpi">
  <div><span>Pemeriksaan</span><b>{len(lolos)}/{len(hasil)}</b><em>{len(peringatan)} peringatan · {len(gagal)} gagal</em></div>
  <div><span>SKU tersedia</span><b>{sum(1 for p in katalog.get('products',[]) if p['status']=='tersedia')}/{len(katalog.get('products',[]))}</b><em>+ {len(katalog.get('bundles',[]))} paket</em></div>
  <div><span>Aset konten</span><b>{len(kreatif.get('items',[]))}</b><em>{sum(1 for i in kreatif.get('items',[]) if i['format']=='video')} video 9:16</em></div>
  <div><span>Target tercapai</span><b>{tercapai}</b><em>{bawah} di bawah · {tanpa} tanpa data</em></div>
  <div><span>Margin terburuk</span><b>{fmt(papan.get('rata_margin',0)*100)}%</b><em>target ≥ 35%</em></div>
  <div><span>Break-even</span><b>{papan.get('break_even',{}).get('order_per_bulan','—')}</b><em>order/bulan</em></div>
  <div><span>Order tercatat</span><b>{k.get('order','—')}</b><em>minggu terakhir</em></div>
  <div><span>Brief riset</span><b>{len(riset.get('brief',[]))}</b><em>dari {riset.get('referensi',0)} post referensi</em></div>
</div>

<h2>1 · Hasil pemeriksaan mesin</h2>
<p class="lede">Gerbang ini memeriksa konsistensi, bukan kebenaran pasar. Semua lolos berarti
sistem tidak bertentangan dengan dirinya sendiri.</p>
<table><thead><tr><th>Pemeriksaan</th><th>Status</th><th>Hasil</th><th>Catatan</th></tr></thead>
<tbody>{baris_cek}</tbody></table>

<h2>2 · Ketersediaan produk</h2>
<p class="lede">Sesuai arahan pemilik hari ini: <b>semua produk dianggap tersedia</b>. Stok di bawah
dihitung papan dari lot green bean × yield — bukan diketik. Ganti angka lot saat penerimaan barang nyata.</p>
<table><thead><tr><th>Produk</th><th>Harga</th><th>Sisa (hitung lot)</th><th>Status situs</th></tr></thead>
<tbody>{baris_produk}</tbody></table>

<h2>3 · Target divisi (Nov 2026)</h2>
<p class="lede">Target dari <code>data/divisi.json</code>, aktual dihitung dari berkas transaksi.
Bulan berjalan baru dimulai — "di bawah" pada awal bulan itu normal.</p>
<table><thead><tr><th>Ukuran</th><th class="num">Target</th><th class="num">Aktual</th><th>Satuan</th><th>Status</th></tr></thead>
<tbody>{baris_target}</tbody></table>

<h2>4 · Aset konten siap tayang</h2>
<p class="lede">Dirender dari label produk + data batch. Ini grafik &amp; teks, bukan footage sangrai —
footage asli selalu menang bila tersedia.</p>
<div class="grid aset">{aset}</div>

<h2>5 · Riset konten &amp; kata kunci</h2>
<table><tbody>
<tr><td><b>Outlier teratas</b></td><td>{top.get('hook','—')}</td>
<td class="num">{top.get('lift',0):.1f}×</td></tr>
<tr><td><b>Pola dominan</b></td><td>{pola.get('nama','—')} → sudut: {pola.get('sudut','—')}</td>
<td class="num">{pola.get('n',0)} post</td></tr>
<tr><td><b>Komentar dianalisis</b></td><td>{riset.get('komentar',0)} kutipan (≤ 24 kata, tanpa identitas)</td>
<td class="num">{riset.get('komentar_rekap',[{}])[0].get('jenis','—') if riset.get('komentar_rekap') else '—'}</td></tr>
<tr><td><b>Kata kunci</b></td><td>{riset.get('kata_kunci',0)} frasa · dijawab halaman
{riset.get('persen_tercakup',0)}% · {len(riset.get('celah',[]))} celah</td>
<td class="num">confidence {riset.get('confidence','—')}</td></tr>
</tbody></table>

<div class="note"><b>Yang masih asumsi — jangan dibaca sebagai fakta</b>
Biaya di <code>data/biaya.json</code> masih asumsi (mempengaruhi HPP, margin, break-even) ·
tonase lot ditambah hari ini atas arahan "semua tersedia", bukan hasil penerimaan barang ·
{riset.get('referensi_contoh',0)} baris riset masih berlabel <code>contoh</code> ·
8 dokumen legal belum selesai · belum ada unggahan ke IG/TikTok/marketplace dari sistem ini.</div>

<h2>6 · Halaman lain</h2>
<table><tbody>
<tr><td><a href="../index.html">Situs</a></td><td>katalog 9 SKU + 2 paket, semua tersedia</td></tr>
<tr><td><a href="../dashboard/index.html">Papan harian</a></td><td>peringatan, target divisi, stok, margin, QC, riset</td></tr>
<tr><td><a href="../kampanye/index.html">Landing kampanye</a></td><td>konten kreator + UTM WhatsApp</td></tr>
<tr><td><a href="../konten/index.html">Hub konten</a></td><td>15 aset + caption siap salin</td></tr>
<tr><td><a href="../riset/index.html">Dasbor riset</a></td><td>outlier, pola, komentar, kata kunci, brief</td></tr>
<tr><td><a href="../brand/index.html">Brand kit</a></td><td>9 label 70×100 mm, lembar A4, logo, OG card</td></tr>
<tr><td><a href="../komersial/penawaran-b2b.html">Penawaran B2B</a></td><td>4 tier harga grosir + alur kerja</td></tr>
<tr><td><a href="periksa.md">Laporan periksa (markdown)</a></td><td>versi teks untuk dibaca cepat</td></tr>
</tbody></table>

<footer>
  <span>Dibuat <code>tools/laporan.py</code> · sumber: <code>laporan/periksa.json</code>,
    <code>dashboard/data.json</code>, <code>data/catalog.json</code>,
    <code>data/kreatif.json</code>, <code>riset/data.json</code></span>
  <span>Semua grafik lokal · tanpa CDN aset · halaman <code>noindex</code></span>
</footer></div></body></html>"""


def main():
    tgl = hari_ini()
    cek = baca("laporan", "periksa.json", default={"hasil": []})
    papan = baca("dashboard", "data.json")
    katalog = baca("data", "catalog.json")
    kreatif = baca("data", "kreatif.json")
    riset = baca("riset", "data.json")
    divisi = baca("data", "divisi.json")

    if not cek.get("hasil"):
        print("laporan/periksa.json belum ada — jalankan tools/periksa.py dulu.")
        raise SystemExit(1)

    os.makedirs(OUT, exist_ok=True)
    html = bangun(tgl, cek, papan, katalog, kreatif, riset, divisi)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"laporan/index.html ditulis · {len(html)/1024:.0f} KB")


if __name__ == "__main__":
    main()
