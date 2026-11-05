#!/usr/bin/env python3
"""Halaman "biji sangrai" — landing penjualan roasted beans.

Bentuk halaman ini belajar dari struktur publik template portfolio di
jiro.build (Matteo Backer): nama besar di hero dengan gambar yang tersibak,
satu pernyataan panjang yang menyala kata demi kata saat digulir, daftar
layanan bernomor, proses kerja empat langkah, tabel bergaris, angka besar,
kutipan yang bisa digeser, lalu penutup "let's work together" + jam lokal.

Yang TIDAK diambil: teks, gambar, kode, dan prompt-nya. Prompt/source di
jiro.build di balik paywall ($179) dan tidak dilewati. Halaman itu juga
portofolio motion artist — di sini isinya diganti Sepenuhnya dengan data
Nocturne: 9 biji, harga, petani, ketinggian, catatan rasa.

Sumber angka: data/catalog.json (tidak ada yang dikarang).

Pakai:
    python3 tools/roasted.py           # tulis biji-sangrai/index.html
    python3 tools/roasted.py --cek     # validasi berkas + data, tanpa menulis
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "biji-sangrai")
HALAMAN = os.path.join(OUT, "index.html")

# klaim yang tidak boleh muncul (Nocturne bukan penyangrai; tanpa data pendukung)
TERLARANG = [
    (r"\broastery kami\b", "menyebut Nocturne sebagai roastery"),
    (r"\bkami menyangrai sendiri\b", "klaim menyangrai sendiri"),
    (r"\btermurah\b", "klaim termurah"),
    (r"\bnomor satu\b|\bno\.?\s?1\b", "klaim nomor satu"),
    (r"\bbest ?seller\b", "klaim laris tanpa data"),
    (r"\bterbaik di indonesia\b", "klaim tanpa bukti"),
    (r"\bdiskon \d+", "diskon tanpa sumber"),
    (r"\bgaransi uang kembali\b", "janji yang tidak ada di data"),
]


def rupiah(n: int) -> str:
    return "Rp" + f"{n:,}".replace(",", ".")


def baca(rel: str):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def hitung(katalog: dict) -> dict:
    produk = katalog["products"]
    ukuran = sorted({v["grams"] for p in produk for v in p["variants"]})
    level = sorted({p["roast_level"] for p in produk})
    harga = min(v["price"] for p in produk for v in p["variants"])
    return {
        "jumlah": len(produk),
        "single": sum(1 for p in produk if p.get("category") == "Single Origin"),
        "daerah": len({p["region"] for p in produk}),
        "ukuran": ukuran,
        "level": level,
        "harga": harga,
        "paket": len(katalog.get("bundles", [])),
    }


def wa(nomor: str, pesan: str) -> str:
    return f"https://wa.me/{nomor}?text={quote(pesan)}"


def daftar_biji(katalog: dict) -> str:
    baris = []
    for p in katalog["products"]:
        mulai = min(v["price"] for v in p["variants"])
        kecil = p["variants"][0]["weight"]
        besar = p["variants"][-1]["weight"]
        tempat = p["region"]
        if p.get("district") and p["district"] != p["region"]:
            tempat = f'{p["district"]}, {p["region"]}'
        # blend tidak punya ketinggian tunggal: tulis apa adanya, jangan tanda hubung
        elev = p.get("elevation") or "campuran lot"
        pesan = (
            f"Halo Nocturne, saya mau pesan {p['name']} "
            f"({p['category']}). Boleh info stok dan tanggal sangrai terbaru?"
        )
        baris.append(
            f"""          <tr>
            <td class="td-no">{p['no']}</td>
            <td class="td-nama">{html.escape(p['name'])}
              <small>{html.escape(p['kind'])} · level {p['roast_level']}/5</small>
            </td>
            <td>{html.escape(tempat)}<br><span class="td-no">{html.escape(elev)}</span></td>
            <td>{html.escape(p['process'])}</td>
            <td class="td-rasa">{html.escape(', '.join(p['notes']))}</td>
            <td class="td-harga">{rupiah(mulai)}<small>{kecil} – {besar}</small></td>
            <td class="td-aksi"><a class="pesan" href="{wa(katalog['brand']['whatsapp'], pesan)}"
              target="_blank" rel="noopener">Pesan <span aria-hidden="true">↗</span></a></td>
          </tr>"""
        )
    return "\n".join(baris)


def kartu_rasa(katalog: dict) -> str:
    kartu = []
    for i, p in enumerate(katalog["products"]):
        catatan = [n.lower() for n in p["notes"]]
        catatan[0] = catatan[0][:1].upper() + catatan[0][1:]
        if len(catatan) > 2:
            teks = ", ".join(html.escape(n) for n in catatan[:-1])
            teks += f", dan <em>{html.escape(catatan[-1])}</em>"
        elif len(catatan) == 2:
            teks = f"{html.escape(catatan[0])} dan <em>{html.escape(catatan[1])}</em>"
        else:
            teks = f"<em>{html.escape(catatan[0])}</em>"
        tempat = p["region"]
        if p.get("district") and p["district"] != p["region"]:
            tempat = f'{p["district"]}, {p["region"]}'
        kartu.append(
            f"""        <figure class="rasa__satu" data-rasa="{i}"{' hidden' if i else ''}>
          <blockquote class="rasa__kutip">{teks}.</blockquote>
          <figcaption class="rasa__meta">
            <span><b>{html.escape(p['name'])}</b></span>
            <span>{html.escape(tempat)} · {html.escape(p.get('elevation') or 'campuran lot')}</span>
            <span>{html.escape(p['process'])}</span>
            <span>{'Petani: ' + html.escape(p['farmer']) if p.get('farmer') else 'Racikan Nocturne'}</span>
          </figcaption>
        </figure>"""
        )
    return "\n".join(kartu)


def pita(katalog: dict) -> str:
    item = []
    for p in katalog["products"]:
        item.append(
            f"""        <figure class="pita__item">
          <img src="../{p['img']}" alt="Label {html.escape(p['name'])}" loading="lazy" decoding="async" width="164" height="205">
          <figcaption>{html.escape(p['name'])}</figcaption>
        </figure>"""
        )
    return "\n".join(item)


def kata_kata(teks: str) -> str:
    """Pecah intro jadi kata; kalimat terakhir diserif-miringkan.

    Titik kalimat menempel pada kata terakhirnya — bukan span sendiri, supaya
    tidak ada spasi menggantung sebelum titik dan tidak ada titik dobel.
    Tanpa JavaScript semua kata tetap terbaca; warna redup hanya aktif ketika
    kelas `js` ada di <html>.
    """
    kalimat = [k.strip() for k in teks.split(". ") if k.strip()]
    keluaran, total = [], len(kalimat)
    for i, kal in enumerate(kalimat):
        kal = kal.rstrip(".")
        kelas = "kata kata--serif" if i == total - 1 else "kata"
        kata = kal.split()
        for j, w in enumerate(kata):
            isi = html.escape(w)
            if j == len(kata) - 1:
                isi += "."
            keluaran.append(f'<span class="{kelas}">{isi}</span>')
    return "\n        ".join(keluaran)


def bangun(katalog: dict, ds: dict) -> str:
    b = katalog["brand"]
    n = hitung(katalog)
    nav = wa(b["whatsapp"], "Halo Nocturne, saya mau tanya-tanya soal biji sangrai.")
    hero_produk = next(p for p in katalog["products"] if p["id"] == "blue-mount-ijen")
    ukuran_teks = f'{n["ukuran"][0] // 1000 if n["ukuran"][0] >= 1000 else n["ukuran"][0]} g – ' \
                  f'{n["ukuran"][-1] // 1000} kg' if n["ukuran"][-1] >= 1000 else ""
    ukuran_teks = f'{n["ukuran"][0]} g – {n["ukuran"][-1] // 1000} kg'

    langkah = [
        ("Pesan", "Sebutkan biji, ukuran (100 g / 250 g / 500 g / 1 kg), dan giling: biji utuh, "
                  "V60-filter, tubruk, atau espresso. Lewat WhatsApp cukup satu pesan."),
        ("Sangrai", "Penyangraian dikerjakan Ais Coffee Roastery di Banyuwangi pada jadwal mingguan. "
                    "Tiap batch punya catatan sendiri — bukan disangrai jauh hari lalu disimpan lama."),
        ("Kemas", "Label menyebut nama petani, daerah, ketinggian, level sangrai, tanggal sangrai, "
                  "dan kode batch. Yang Anda butuhkan untuk memeriksa, bukan hiasan."),
        ("Kirim", "Dikemas dan dikirim dari Banyuwangi. Bisa juga diambil langsung di kota. "
                  "Nomor resi dan tanggal sangrai dikirim menyusul di chat yang sama."),
    ]
    langkah_html = "\n".join(
        f"""          <li>
            <span class="langkah__no" aria-hidden="true">{i:02d}</span>
            <div>
              <h3>{html.escape(judul)}</h3>
              <p>{html.escape(isi)}</p>
            </div>
          </li>""" for i, (judul, isi) in enumerate(langkah, 1)
    )

    kirim = [
        (f"{n['single']} single origin",
         f"Dari {n['daerah']} daerah: {', '.join(sorted({p['region'] for p in katalog['products'] if p.get('category') == 'Single Origin'}))}. "
         "Nama petani dan ketinggian kebunnya tercetak di tiap kemasan."),
        ("Dua blend", "Racikan 70/30 dan 60/40 untuk susu, tubruk harian, dan kantor. "
                      "Tetap dengan catatan rasa yang jelas, bukan \"kopi biasa\"."),
        ("Giling sesuai alat", "Biji utuh, bubuk V60-filter, bubuk tubruk, bubuk espresso. "
                               "Giling dilakukan dekat waktu kirim, bukan stok lama."),
        ("Langganan", "Solo, Duo, atau Rumah/Kantor tiap siklus. Kopi bebas dipilih tiap siklus, "
                      "dan kami ingat kapan terakhir Anda kirim."),
        ("Paket & grosir", f"{n['paket']} paket rasa siap kirim, plus harga per kilo untuk kedai, "
                           "kantor, dan reseller lewat penawaran B2B."),
    ]
    kirim_html = "\n".join(
        f"""          <li class="kirim__baris">
            <span class="kirim__no" aria-hidden="true">{i:02d}</span>
            <h3 class="kirim__judul">{html.escape(judul)}</h3>
            <p class="kirim__ket">{html.escape(ket)}</p>
            <span class="kirim__panah" aria-hidden="true">↗</span>
          </li>""" for i, (judul, ket) in enumerate(kirim, 1)
    )

    return f"""<!DOCTYPE html>
<html lang="id" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Biji sangrai dari Banyuwangi — Nocturne Koffie</title>
<meta name="description" content="{n['jumlah']} biji kopi sangrai dari petani bernama. Disangrai mingguan oleh Ais Coffee Roastery di Banyuwangi, dikemas dan dikirim dari kota yang sama. Mulai {rupiah(n['harga'])}.">
<meta name="theme-color" content="#16110D">
<link rel="canonical" href="https://nocturnekoffie.id/biji-sangrai/">
<link rel="icon" href="../brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../brand/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="Biji sangrai dari Banyuwangi — Nocturne Koffie">
<meta property="og:description" content="{n['jumlah']} biji kopi sangrai, nama petani tercetak di kemasan. Disangrai mingguan di Banyuwangi. Mulai {rupiah(n['harga'])}.">
<meta property="og:image" content="https://nocturnekoffie.id/brand/og-1200x630.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="toko.css">
<script>document.documentElement.className="js";</script>
</head>
<body>

<a class="lewati" href="#daftar">Langsung ke daftar biji &amp; harga</a>

<div class="bar__prog" id="prog" aria-hidden="true"></div>

<header class="bar" id="bar">
  <a class="bar__mark" href="../index.html">NOCTURNE<small>KOFFIE · BANYUWANGI</small></a>
  <nav class="bar__nav" aria-label="Bagian halaman">
    <a href="#kirim">Yang dikirim</a>
    <a href="#proses">Proses</a>
    <a href="#daftar">Biji &amp; harga</a>
    <a href="../komersial/penawaran-b2b.html">Grosir</a>
  </nav>
  <div class="bar__aksi">
    <a class="bar__wa" href="{nav}" target="_blank" rel="noopener">WhatsApp <span aria-hidden="true">↗</span></a>
  </div>
</header>

<main>

  <section class="hero" aria-labelledby="judul-hero">
    <div class="hero__grid">
      <div class="hero__kiri">
        <p class="micro"><span class="micro__dot" aria-hidden="true"></span>Roasted beans · Banyuwangi, Jawa Timur</p>
        <h1 class="hero__judul" id="judul-hero">
          <span class="lini"><span>Nocturne</span></span>
          <span class="lini"><span><em>Koffie</em></span></span>
        </h1>
        <p class="hero__p">
          {n['jumlah']} biji kopi sangrai, nama petani tercetak di kemasan. Disangrai mingguan oleh
          <b>Ais Coffee Roastery</b> di Banyuwangi, lalu dikemas dan dikirim dari kota yang sama.
        </p>
        <div class="hero__aksi">
          <a class="btn btn--isi" href="#daftar">Pilih bijimu <span class="btn__panah" aria-hidden="true">→</span></a>
          <a class="btn btn--garis" href="{nav}" target="_blank" rel="noopener">Tanya stok hari ini</a>
        </div>
      </div>

      <div class="hero__kanan">
        <figure class="foto">
          <span class="foto__noda" aria-hidden="true">SANRAI<br>MINGGUAN</span>
          <div class="foto__bingkai">
            <img src="../{hero_produk['img']}" alt="Label {html.escape(hero_produk['name'])}: {html.escape(', '.join(hero_produk['notes']).lower())}"
                 width="430" height="537" fetchpriority="high">
          </div>
          <figcaption class="foto__cap">
            <span><b>{html.escape(hero_produk['name'])}</b> · {html.escape(hero_produk['process'])}</span>
            <span>{html.escape(hero_produk['farmer'])} · {html.escape(hero_produk['elevation'])}</span>
          </figcaption>
        </figure>
      </div>
    </div>

    <div class="hero__kaki">
      <span class="hero__gulir"><i aria-hidden="true"></i> Gulir</span>
      <span>Banyuwangi · <strong class="hero__jam" id="jam">--:--:--</strong> WIB</span>
      <span><strong>{n['jumlah']}</strong> biji · <strong>{len(n['ukuran'])}</strong> ukuran · mulai <strong>{rupiah(n['harga'])}</strong></span>
    </div>
  </section>

  <section class="pita" aria-label="Sembilan label biji Nocturne">
    <div class="pita__jalur">
{pita(katalog)}
{pita(katalog)}
    </div>
  </section>

  <section class="bagian nyata" id="tentang">
    <div class="wrap">
      <p class="micro"><span class="micro__dot" aria-hidden="true"></span>Tentang</p>
      <p class="nyata__teks" id="nyata">
        {kata_kata(b['intro'])}
      </p>
      <div class="nyata__kaki">
        <p><b>Yang kami jual</b>Biji sangrai, bukan janji. Tiap kemasan punya tanggal sangrai, kode batch, dan nama petani yang bisa Anda cek.</p>
        <p><b>Yang kami jaga</b>Jadwal sangrai mingguan supaya yang sampai ke Anda masih segar, dan racikan yang sama tiap kali dipesan ulang.</p>
        <p><b>Yang kami tidak klaim</b>Kami bukan penyangrai. Penyangraian dikerjakan Ais Coffee Roastery; kami yang memilih lot, menentukan level, mengemas, dan mengirim.</p>
      </div>
    </div>
  </section>

  <section class="bagian" id="kirim">
    <div class="wrap">
      <div class="kirim">
        <div class="kirim__kiri">
          <p class="micro"><span class="micro__dot" aria-hidden="true"></span>Yang dikirim</p>
          <h2>Empat ukuran,<br>lima cara<br><em>menikmati.</em></h2>
          <p>Semua tersedia sekarang. Pilih biji dan ukuran; sisanya kami urus sampai di depan pintu.</p>
        </div>
        <ul class="kirim__daftar">
{kirim_html}
        </ul>
      </div>
    </div>
  </section>

  <section class="bagian" id="proses">
    <div class="wrap">
      <div class="kepala">
        <h2>Dari pesan<br>ke <em>cangkir</em></h2>
        <p class="kepala__kanan">Empat langkah · tanpa antre panjang</p>
      </div>
      <ol class="langkah">
{langkah_html}
      </ol>
    </div>
  </section>

  <section class="bagian" id="daftar">
    <div class="wrap">
      <div class="kepala">
        <h2>Biji &amp; <em>harga</em></h2>
        <p class="kepala__kanan">{n['jumlah']} SKU · harga bersumber dari katalog</p>
      </div>
      <div class="tabel-bungkus">
        <table class="tabel">
          <caption class="sr">{n['jumlah']} biji sangrai Nocturne, harga mulai dari {rupiah(n['harga'])} per 100 g.</caption>
          <thead>
            <tr>
              <th scope="col">No</th>
              <th scope="col">Biji</th>
              <th scope="col">Daerah</th>
              <th scope="col">Proses</th>
              <th scope="col">Catatan rasa</th>
              <th scope="col">Mulai</th>
              <th scope="col"><span class="sr">Pesan</span></th>
            </tr>
          </thead>
          <tbody>
{daftar_biji(katalog)}
          </tbody>
        </table>
      </div>
      <p class="catatan-kecil">
        <b>Harga di atas untuk 100 g.</b> Ukuran 250 g, 500 g, dan 1 kg punya harga sendiri —
        klik pesan untuk daftar lengkapnya. Seluruh biji di tabel berstatus tersedia saat halaman ini dibuat.
        Level sangrai tercatat 1–5; level 3 berarti medium.
      </p>
    </div>
  </section>

  <section class="bagian" id="angka">
    <div class="wrap">
      <div class="kepala">
        <h2>Angkanya</h2>
        <p class="kepala__kanan">Dihitung dari katalog, bukan dari perasaan</p>
      </div>
      <div class="angka">
        <div class="angka__sel">
          <span class="angka__b" data-hitung="{n['jumlah']}">0</span>
          <span class="angka__ket">Pilihan biji</span>
        </div>
        <div class="angka__sel">
          <span class="angka__b" data-hitung="{len(n['ukuran'])}">0</span>
          <span class="angka__ket">Ukuran · {ukuran_teks}</span>
        </div>
        <div class="angka__sel">
          <span class="angka__b" data-hitung="{len(n['level'])}">0</span>
          <span class="angka__ket">Level sangrai</span>
        </div>
        <div class="angka__sel">
          <span class="angka__b"><small>Rp</small><span data-hitung="{n['harga'] // 1000}" data-format="ribu">0</span><small>rb</small></span>
          <span class="angka__ket">Harga mulai · 100 g</span>
        </div>
      </div>
      <p class="angka__teks">
        Tidak ada angka pembanding industri di halaman ini. Yang tertulis hanya isi katalog:
        jumlah biji, ukuran, level sangrai, dan harga terendah.
      </p>
    </div>
  </section>

  <section class="bagian" id="rasa">
    <div class="wrap">
      <div class="kepala">
        <h2>Catatan <em>rasa</em></h2>
        <p class="kepala__kanan">Dari 9 kemasan · geser untuk berikutnya</p>
      </div>
      <div class="rasa" id="rasa" tabindex="0" role="group" aria-label="Catatan rasa, geser dengan tombol panah">
{kartu_rasa(katalog)}
      </div>
      <div class="rasa__nav">
        <button class="rasa__btn" id="rasa-mundur" aria-label="Catatan sebelumnya">←</button>
        <button class="rasa__btn" id="rasa-maju" aria-label="Catatan berikutnya">→</button>
        <span class="rasa__hitung" id="rasa-hitung" aria-live="polite">01 / {n['jumlah']:02d}</span>
      </div>
    </div>
  </section>

  <section class="bagian tutup" id="pesan">
    <div class="wrap">
      <p class="micro"><span class="micro__dot" aria-hidden="true"></span>Ayo mulai</p>
      <h2>Pilih biji.<br><em>Kami sangrai.</em></h2>
      <p class="tutup__p">
        Sebut satu biji dan satu ukuran. Kami balas dengan stok, tanggal sangrai terakhir,
        dan ongkir ke alamat Anda.
      </p>
      <div class="tutup__baris">
        <a class="btn btn--isi" href="{nav}" target="_blank" rel="noopener">WhatsApp {html.escape(b['wa_display'])} <span class="btn__panah" aria-hidden="true">↗</span></a>
        <a class="btn btn--garis" href="mailto:{b['email']}">{html.escape(b['email'])}</a>
      </div>

      <footer class="kaki">
        <div class="kaki__kiri">
          <b>Nocturne Koffie</b> — biji sangrai dari {html.escape(b['city'])}, {html.escape(b['province'])}.
          Penyangraian oleh Ais Coffee Roastery. Dikemas dan dikirim dari kota yang sama.
          Halaman ini dibuat dari <code>data/catalog.json</code>; kalau harga di katalog berubah, halaman ikut berubah.
        </div>
        <nav class="kaki__tautan" aria-label="Tautan lain">
          <a href="../index.html">Beranda</a>
          <a href="../kampanye/index.html">Kampanye</a>
          <a href="../komersial/penawaran-b2b.html">Grosir &amp; kafe</a>
          <a href="{b['instagram']}" target="_blank" rel="noopener">{html.escape(b['instagram_label'])}</a>
        </nav>
        <div class="kaki__bawah">
          <span>Banyuwangi, Jawa Timur · <span id="jam-kaki">--:--</span> WIB</span>
          <span>© {__import__('datetime').date.today().year} Nocturne Koffie</span>
        </div>
      </footer>
    </div>
  </section>

</main>

<script src="toko.js" defer></script>
</body>
</html>
"""


def periksa(teks: str, katalog: dict, ds: dict) -> list[str]:
    import re

    masalah = []
    for pola, alasan in TERLARANG:
        for m in re.finditer(pola, teks, re.I):
            masalah.append(f"{alasan} → \"{m.group(0)}\"")

    # semua harga & nama dari katalog harus muncul
    for p in katalog["products"]:
        if html.escape(p["name"]) not in teks:
            masalah.append(f"biji {p['name']} tidak tampil")
        mulai = min(v["price"] for v in p["variants"])
        if rupiah(mulai) not in teks:
            masalah.append(f"harga mulai {p['name']} ({rupiah(mulai)}) tidak tampil")

    # jangan ada harga yang tidak ada di katalog
    semua = {rupiah(v["price"]) for p in katalog["products"] for v in p["variants"]}
    semua |= {rupiah(b["price"]) for b in katalog.get("bundles", [])}
    for m in set(re.findall(r"Rp\d{2,3}(?:\.\d{3})+", teks)):
        if m not in semua:
            masalah.append(f"harga {m} tidak ada di katalog")

    # warna: hanya token dari design-system
    boleh = {w.lower() for w in ds["warna"]["boleh_dipakai"]}
    css = open(os.path.join(OUT, "toko.css"), encoding="utf-8").read()
    for m in set(re.findall(r"#[0-9a-fA-F]{6}\b", css)):
        if m.lower() not in boleh:
            masalah.append(f"warna {m} di toko.css bukan token design-system")

    # tanpa CDN
    for pola in ("fonts.googleapis", "cdn.", "unpkg", "jsdelivr"):
        if pola in teks:
            masalah.append(f"halaman memuat {pola} (harus tanpa CDN)")

    # ukuran judul hero harus muat di kolomnya — diukur dengan font asli
    try:
        from PIL import ImageFont
        import re as _re
        blok_dasar = css.split("@media (min-width:860px)")[0]
        blok_besar = css.split("@media (min-width:860px)")[1].split("@media (max-width:859px)")[0]
        blok_kecil = css.split("@media (max-width:859px)")[1]

        def clamp_huruf(txt):
            m = _re.search(r"font-size:\s*clamp\(([\d.]+)rem,\s*([\d.]+)vw,\s*([\d.]+)rem\)", txt)
            return tuple(float(x) for x in m.groups()) if m else None

        def badan(txt, sel):
            m = _re.search(_re.escape(sel) + r"\s*\{([^}]*)\}", txt)
            return m.group(1) if m else ""

        dasar = clamp_huruf(badan(blok_dasar, ".hero__judul"))
        kecil = clamp_huruf(badan(blok_kecil, ".hero__judul")) or dasar
        m_grid = _re.search(r"grid-template-columns:\s*minmax\(0,\s*([\d.]+)fr\)\s*minmax\(0,\s*([\d.]+)fr\)", blok_besar)
        m_gap = _re.search(r"gap:\s*clamp\(([\d.]+)px,\s*([\d.]+)vw,\s*([\d.]+)px\)", blok_besar)
        kata = "NOCTURNE"
        if not (dasar and m_grid):
            masalah.append("judul hero tidak memakai clamp() + grid dua kolom yang bisa diperiksa")
        else:
            fr1, fr2 = float(m_grid.group(1)), float(m_grid.group(2))
            fb = os.path.join(ROOT, "assets", "fonts", "bricolage-grotesque-latin-800-normal.ttf")
            acuan = ImageFont.truetype(fb, 100).getlength(kata) / 100
            for vw in (360, 390, 414, 768, 860, 1024, 1280, 1440, 1920):
                pad = min(52, max(18, vw * 0.042))
                isi = min(1320, vw) - 2 * pad
                c = dasar if vw >= 860 else kecil
                ukuran = max(c[0] * 16, min(vw * c[1] / 100, c[2] * 16))
                if vw >= 860:
                    gap = 0.0
                    if m_gap:
                        g0, g1, g2 = (float(x) for x in m_gap.groups())
                        gap = max(g0, min(vw * g1 / 100, g2))
                    lebar_kolom = (isi - gap) * fr1 / (fr1 + fr2)
                else:
                    lebar_kolom = isi
                lebar = acuan * ukuran
                if lebar > lebar_kolom * 0.98:
                    masalah.append(f"judul hero meluap di {vw}px ({lebar:.0f}px > kolom {lebar_kolom:.0f}px)")
    except ImportError:
        pass

    if "prefers-reduced-motion" not in css:
        masalah.append("toko.css tidak menghormati prefers-reduced-motion")
    if '"motto"' in teks:
        masalah.append("motto ditulis manual di HTML, bukan dari data")

    return masalah


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true")
    a = ap.parse_args()

    katalog = baca("data/catalog.json")
    ds = baca("data/design-system.json")

    if a.cek:
        if not os.path.exists(HALAMAN):
            print("XX biji-sangrai/index.html belum ada")
            return 1
        teks = open(HALAMAN, encoding="utf-8").read()
        masalah = periksa(teks, katalog, ds)
        for m in masalah:
            print("XX", m)
        n = hitung(katalog)
        print(f"{'OK' if not masalah else 'GAGAL'} · {n['jumlah']} biji · "
              f"{len(n['ukuran'])} ukuran · mulai {rupiah(n['harga'])} · "
              f"{len(masalah)} masalah")
        return 0 if not masalah else 1

    teks = bangun(katalog, ds)
    masalah = periksa(teks, katalog, ds)
    if masalah:
        for m in masalah:
            print("XX", m)
        print(f"tidak ditulis · {len(masalah)} masalah")
        return 1
    os.makedirs(OUT, exist_ok=True)
    with open(HALAMAN, "w", encoding="utf-8") as f:
        f.write(teks)
    n = hitung(katalog)
    print(f"biji-sangrai/index.html · {len(teks):,} karakter · {n['jumlah']} biji · "
          f"mulai {rupiah(n['harga'])} · 0 masalah")
    return 0


if __name__ == "__main__":
    sys.exit(main())
