#!/usr/bin/env python3
"""
D3 · Marketing & Pertumbuhan — generator landing page kampanye.

Membangun `kampanye/index.html`: halaman kampanye yang memakai aset dari
D4 (data/kreatif.json) dan harga asli dari data/catalog.json.

Pakai:
    python3 tools/kampanye.py            # tulis kampanye/index.html
    python3 tools/kampanye.py --cek      # cetak ringkasan tanpa menulis
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "kampanye")

# UTM: satu kampanye, beberapa kanal. Semua tautan keluar membawa label ini.
KAMPANYE = "kopi-jujur-soal-tanggal"
SUMBER = {
    "hero": "landing-hero",
    "video": "landing-video",
    "peta": "landing-peta-rasa",
    "langganan": "landing-langganan",
    "b2b": "landing-b2b",
}

rp = lambda n: "Rp" + f"{int(n):,}".replace(",", ".")


def baca(*path, default=None):
    p = os.path.join(ROOT, *path)
    if not os.path.exists(p):
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def wa(teks, kanal):
    """Tautan WhatsApp dengan pesan awal yang sudah membawa label kanal."""
    pesan = f"{teks}\n\n(utm: kampanye={KAMPANYE}; kanal={kanal}; halaman=kampanye)"
    return "https://wa.me/628988188800?text=" + __import__("urllib.parse", fromlist=["quote"]).quote(pesan)


def kartu_video(it, no):
    judul = it["judul"]
    caption = it["caption_ringkas"]
    poster = f"../konten/{it['poster']}"
    src = f"../konten/{it['file']}" if it.get("file", "").endswith(".mp4") else poster
    media = (f'<video class="klip__media" src="{src}" poster="{poster}" controls muted loop '
             f'playsinline preload="none" aria-label="{judul}"></video>'
             if src.endswith(".mp4")
             else f'<img class="klip__media" src="{poster}" alt="{judul}" loading="lazy" width="1080" height="1920">')
    return f"""    <figure class="klip">
      <div class="klip__frame">{media}</div>
      <figcaption>
        <span class="klip__no">{no:02d} · {it.get('platform','')} · {it.get('rasio','')}</span>
        <b>{judul}</b>
        <span class="klip__cap">{caption}</span>
      </figcaption>
    </figure>"""


def produk_pilihan(catalog):
    """Ambil tiga produk yang benar-benar ada di katalog, bukan karangan."""
    peta = next((b for b in catalog["bundles"] if b["id"] == "peta-rasa"), None)
    ijen = next((p for p in catalog["products"] if p["id"] == "blue-mount-ijen"), None)
    raung = next((p for p in catalog["products"] if p["id"] == "raung"), None)
    harga = lambda p, gram: next((v["price"] for v in p["variants"] if v["grams"] == gram), None)
    out = []
    if peta:
        out.append(dict(nama="Peta Rasa", ket="3 × 100 g · tiga keluarga kopi",
                        harga=peta["price"], normal=peta["price_normal"], sku=peta["sku"],
                        kanal="peta", produk="Peta Rasa"))
    if ijen:
        out.append(dict(nama="Blue Mount Ijen", ket="100 g · arabika 1.700–1.800 mdpl",
                        harga=harga(ijen, 100), normal=None, sku="NK-IJN-100", kanal="hero",
                        produk="Blue Mount Ijen 100 g"))
    if raung:
        out.append(dict(nama="Raung", ket="250 g · robusta 422–443 mdpl",
                        harga=harga(raung, 250), normal=None, sku="NK-RNG-250", kanal="hero",
                        produk="Raung 250 g"))
    return out


def bangun(catalog, kreatif, tgl):
    video = [i for i in kreatif.get("items", []) if i.get("format") == "video"]
    carousel = [i for i in kreatif.get("items", []) if i.get("id", "").startswith("carousel")]
    klip_html = "\n".join(kartu_video(v, n + 1) for n, v in enumerate(video))

    baris_produk = ""
    for p in produk_pilihan(catalog):
        normal = (f'<s>{rp(p["normal"])}</s>' if p.get("normal") else "")
        baris_produk += f"""      <a class="pilih" href="{wa(f'Halo, saya mau pesan {p["produk"]} (SKU {p["sku"]}). Lihat di halaman kampanye.', p["kanal"])}" target="_blank" rel="noopener">
        <span class="pilih__nama">{p["nama"]}</span>
        <span class="pilih__ket">{p["ket"]}</span>
        <span class="pilih__harga">{rp(p["harga"])} {normal}</span>
        <span class="pilih__cta">Pesan via WhatsApp →</span>
      </a>"""

    jadwal = ""
    for i in (video + carousel)[:8]:
        jadwal += (f'<tr><td>{i.get("jadwal","—")}</td><td>{i.get("platform","—")}</td>'
                   f'<td>{i.get("judul","—")}</td></tr>')

    judul_kampanye = "Kopi yang jujur soal tanggal"
    deskripsi = ("Kami tidak mencetak tanggal kedaluwarsa. Kami mencetak tanggal sangrai, "
                 "kode batch, dan level roast — lalu merekam prosesnya supaya bisa Anda periksa sendiri.")

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{judul_kampanye} — Nocturne Koffie</title>
<meta name="description" content="{deskripsi}" />
<meta name="theme-color" content="#F5EFE4" />
<link rel="canonical" href="https://nocturnekoffie.id/kampanye/" />
<link rel="icon" href="../brand/favicon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="../brand/apple-touch-icon.png" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{judul_kampanye} — Nocturne Koffie" />
<meta property="og:description" content="{deskripsi}" />
<meta property="og:image" content="https://nocturnekoffie.id/brand/og-1200x630.jpg" />
<meta name="twitter:card" content="summary_large_image" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;1,9..144,300&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="../assets/css/site.css" />
<style>
  /* ── lapisan khusus halaman kampanye (token dari site.css, tidak diubah) ── */
  .kp{{padding-block:clamp(34px,6vw,72px)}}
  .kp__head{{max-width:60ch}}
  .kp h1{{font-family:var(--display);font-size:clamp(38px,7.4vw,78px);line-height:.96;letter-spacing:-.035em;margin:14px 0 0;font-weight:800}}
  .kp h1 em{{font-family:var(--serif);font-style:italic;font-weight:300;color:var(--espresso)}}
  .kp h2{{font-family:var(--display);font-size:clamp(24px,3.6vw,36px);line-height:1.04;letter-spacing:-.025em;margin:0 0 12px}}
  .kp .lede{{margin-top:18px;font-size:clamp(15px,1.6vw,18px);max-width:52ch}}
  .kp__acts{{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px;align-items:center}}
  .kp__note{{font-size:12.5px;color:var(--ink-55)}}

  .angka{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1px;background:rgba(22,17,13,.16);border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);margin-top:clamp(30px,5vw,52px)}}
  .angka div{{background:var(--paper);padding:20px 18px}}
  .angka b{{display:block;font-family:var(--display);font-size:clamp(26px,3.4vw,34px);line-height:1;letter-spacing:-.03em}}
  .angka span{{display:block;font-size:12.5px;color:var(--ink-55);margin-top:6px}}

  .galeri{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:clamp(14px,2vw,24px);margin-top:26px;align-items:start}}
  .klip{{margin:0}}
  .klip__frame{{position:relative;aspect-ratio:9/16;background:var(--ink);border-radius:4px;overflow:hidden}}
  .klip__media{{width:100%;height:100%;object-fit:cover;display:block;background:var(--ink)}}
  .klip figcaption{{display:flex;flex-direction:column;gap:4px;padding-top:10px}}
  .klip__no{{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-55)}}
  .klip figcaption b{{font-family:var(--display);font-size:15px;line-height:1.2;letter-spacing:-.01em}}
  .klip__cap{{font-size:13px;color:var(--ink-80);line-height:1.5}}

  .bukti{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:clamp(16px,2.4vw,30px);margin-top:28px}}
  .bukti article{{border-top:2px solid var(--ink);padding-top:14px}}
  .bukti span{{font-family:var(--display);font-size:12px;letter-spacing:.2em;color:var(--orange)}}
  .bukti h3{{font-family:var(--display);font-size:19px;margin:8px 0 6px;letter-spacing:-.01em}}
  .bukti p{{font-size:13.6px;line-height:1.62;color:var(--ink-80);margin:0}}

  .pilih-grup{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:26px}}
  .pilih{{display:flex;flex-direction:column;gap:5px;padding:20px 20px 18px;border:2px solid var(--ink);border-radius:4px;text-decoration:none;color:inherit;background:rgba(255,255,255,.35);transition:transform .2s ease,background .2s ease}}
  .pilih:hover{{transform:translateY(-3px);background:#fff}}
  .pilih__nama{{font-family:var(--display);font-size:20px;letter-spacing:-.02em}}
  .pilih__ket{{font-size:12.5px;color:var(--ink-55)}}
  .pilih__harga{{font-family:var(--display);font-size:22px;margin-top:6px}}
  .pilih__harga s{{font-family:var(--body);font-size:13px;color:var(--ink-55);font-weight:400}}
  .pilih__cta{{font-size:12.5px;font-weight:600;color:var(--orange);margin-top:8px}}

  .tabel{{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:18px}}
  .tabel th,.tabel td{{text-align:left;padding:9px 10px;border-bottom:1px solid rgba(22,17,13,.14)}}
  .tabel th{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-55);font-weight:600}}
  .tabel tr:last-child td{{border-bottom:0}}

  .tutup{{background:var(--ink);color:var(--paper);margin-top:clamp(40px,7vw,80px)}}
  .tutup .kp h2{{color:var(--paper)}}
  .tutup p{{color:rgba(245,239,228,.78)}}
  .tutup .btn--orange{{margin-top:20px}}
  .kaki{{display:flex;flex-wrap:wrap;gap:10px 24px;justify-content:space-between;font-size:12px;color:var(--ink-55);padding:22px 0 40px;border-top:1px solid rgba(22,17,13,.16)}}
  .kaki a{{color:inherit}}
  @media (prefers-reduced-motion:reduce){{.pilih{{transition:none}}.pilih:hover{{transform:none}}}}
</style>
</head>
<body>

<header class="nav is-solid">
  <div class="wrap nav__in">
    <a class="brand" href="../index.html" aria-label="Nocturne Koffie — kembali ke situs utama">
      <span class="brand__mark" aria-hidden="true"></span>
      <span class="brand__type">
        <span class="brand__name">Nocturne</span>
        <span class="brand__line">Koffie Brand</span>
      </span>
    </a>
    <div class="nav__right">
      <a class="nav__member" href="../index.html">Situs utama</a>
      <a class="btn btn--pill" href="{wa('Halo, saya datang dari halaman kampanye “Kopi yang jujur soal tanggal”.', SUMBER['hero'])}" target="_blank" rel="noopener">Pesan via WhatsApp</a>
    </div>
  </div>
</header>

<main>
  <!-- ── HERO ───────────────────────────────────────────────── -->
  <section class="kp wrap">
    <div class="kp__head">
      <p class="kicker">Kampanye · {tgl.strftime('%B %Y')} · {len(video)} klip · 1 halaman</p>
      <h1>Kopi yang <em>jujur</em> soal tanggal.</h1>
      <p class="lede">Kami tidak mencetak tanggal kedaluwarsa. Yang tercetak di tiap kantong:
        <b>tanggal sangrai</b>, <b>kode batch</b>, dan <b>level roast</b>. Prosesnya kami rekam —
        supaya Anda tidak perlu percaya pada kata “fresh”.</p>
      <div class="kp__acts">
        <a class="btn btn--orange btn--lg" href="{wa('Halo, saya mau pesan kopi. Boleh dibantu pilih?', SUMBER['hero'])}" target="_blank" rel="noopener">Pesan via WhatsApp</a>
        <a class="btn" href="#klip">Lihat {len(video)} klip proses →</a>
      </div>
      <p class="kp__note">Senin–Sabtu 09.00–21.00 WIB · dibalas biasanya di bawah 2 jam · kirim hari yang sama untuk order sebelum 15.00.</p>
    </div>

    <div class="angka">
      <div><b>3 hal</b><span>tercetak di tiap kantong: tanggal sangrai, kode batch, level roast</span></div>
      <div><b>7–21 hari</b><span>jendela rasa terbaik setelah sangrai</span></div>
      <div><b>15.00 WIB</b><span>batas order untuk dikirim di hari yang sama</span></div>
    </div>
  </section>

  <!-- ── GALERI KONTEN ──────────────────────────────────────── -->
  <section class="kp wrap" id="klip">
    <p class="kicker">Konten media kreator · D4</p>
    <h2>Yang biasanya tidak diperlihatkan.</h2>
    <p class="lede lede--tight">Lima klip, masing-masing tujuh detik. Dirender dari data batch dan catatan QC —
      bukan stok video. Putar dengan suara mati dulu; caption di bawah tiap klip menjelaskan konteksnya.</p>
    <div class="galeri">
{klip_html}
    </div>
    <p class="kp__note" style="margin-top:18px">Video ini dibuat otomatis oleh <code>tools/kreatif.py</code> dari
      label produk dan catatan batch. Tanpa footage asli, tanpa model — yang ditampilkan adalah angka dan proses
      yang benar-benar kami catat.</p>
  </section>

  <!-- ── BUKTI ──────────────────────────────────────────────── -->
  <section class="kp wrap">
    <p class="kicker">Alasan, bukan slogan</p>
    <h2>Tiga hal yang kami pertanggungjawabkan.</h2>
    <div class="bukti">
      <article>
        <span>01 · QC</span>
        <h3>Batch ditolak tidak dikirim</h3>
        <p>Setiap batch dicicipi dan diberi skor. Ambang kami 83. Batch berskor 81,5 tidak dijual dengan
          diskon, tidak diganti label — disangrai ulang, dicicipi lagi.</p>
      </article>
      <article>
        <span>02 · Proses</span>
        <h3>Berhenti berdasarkan catatan</h3>
        <p>Titik henti sangrai ditentukan per batch, bukan perasaan. Dua puluh detik lebih lama bisa
          mengubah rasa — karena itu suhu dan waktu dicatat, lalu diulang untuk batch berikutnya.</p>
      </article>
      <article>
        <span>03 · Layanan</span>
        <h3>Order sebelum 15.00 dikirim hari itu</h3>
        <p>Senin–Sabtu. Resi dikirim hari yang sama, bukan besok. Kalau kami tidak bisa memenuhi,
          Anda kami kabari lebih dulu — bukan setelah paket telat.</p>
      </article>
    </div>
  </section>

  <!-- ── PRODUK ─────────────────────────────────────────────── -->
  <section class="kp wrap" id="pesan">
    <p class="kicker">Mulai dari sini</p>
    <h2>Tiga pintu masuk.</h2>
    <p class="lede lede--tight">Harga di bawah diambil langsung dari katalog — sama dengan yang Anda lihat di situs utama.
      Pesanan lewat WhatsApp, dibalas manusia, bukan bot.</p>
    <div class="pilih-grup">
{baris_produk}
    </div>
    <p class="kp__note" style="margin-top:16px">Ingin lebih hemat? <a class="linkbtn" href="{wa('Halo, saya mau tanya Langganan Kopi Nocturne.', SUMBER['langganan'])}" target="_blank" rel="noopener">Langganan</a>
      mengirim ulang otomatis sebelum kopi Anda habis. Untuk kafe/resto:
      <a class="linkbtn" href="../komersial/penawaran-b2b.html">penawaran grosir</a>.</p>
  </section>

  <!-- ── JADWAL ─────────────────────────────────────────────── -->
  <section class="kp wrap">
    <p class="kicker">Rencana tayang</p>
    <h2>Konten ini tayang di mana dan kapan.</h2>
    <p class="lede lede--tight">Semua aset sudah jadi. Jadwal di bawah adalah rencana terbit, bukan klaim sudah tayang.</p>
    <table class="tabel">
      <thead><tr><th>Tanggal</th><th>Platform</th><th>Aset</th></tr></thead>
      <tbody>
{jadwal}
      </tbody>
    </table>
  </section>

  <!-- ── PENUTUP ────────────────────────────────────────────── -->
  <section class="tutup">
    <div class="kp wrap">
      <h2>Kalau ragu, tanya dulu.</h2>
      <p class="lede">Sebutkan metode seduh dan alat yang Anda punya. Kami sarankan kopi dan tingkat gilingan
        yang cocok — atau bilang saja kalau belum ada yang cocok. Lebih baik tidak jadi beli daripada salah beli.</p>
      <a class="btn btn--orange btn--lg" href="{wa('Halo, saya mau tanya-tanya dulu soal kopi dan alat seduh saya.', SUMBER['hero'])}" target="_blank" rel="noopener">Tanya via WhatsApp</a>
    </div>
  </section>
</main>

<footer class="wrap">
  <div class="kaki">
    <span>Nocturne Koffie Brand · Banyuwangi, Jawa Timur · disangrai mingguan oleh Ais Coffee Roastery</span>
    <span>
      <a href="../index.html">Situs</a> ·
      <a href="../konten/index.html">Hub konten</a> ·
      <a href="../brand/index.html">Brand kit</a> ·
      <a href="../komersial/penawaran-b2b.html">Grosir</a>
    </span>
  </div>
  <p class="kp__note" style="padding-bottom:34px">Halaman dibuat otomatis oleh <code>tools/kampanye.py</code>
    pada {tgl.isoformat()} dari <code>data/catalog.json</code> dan <code>data/kreatif.json</code>.
    Label utm: <code>kampanye={KAMPANYE}</code>.</p>
</footer>

</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true")
    args = ap.parse_args()

    catalog = baca("data", "catalog.json", default={})
    kreatif = baca("data", "kreatif.json", default={})
    if not catalog:
        raise SystemExit("data/catalog.json tidak ada — tidak ada harga yang boleh dikarang.")

    html = bangun(catalog, kreatif, date.today())
    video = [i for i in kreatif.get("items", []) if i.get("format") == "video"]

    if args.cek:
        print(f"Kampanye siap: {len(video)} klip video · {len(catalog['products'])} produk · "
              f"{len(katalog['bundles'])} paket")
        return

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    kb = len(html.encode("utf-8")) / 1024
    print(f"kampanye/index.html ditulis · {kb:.0f} KB · {len(video)} klip · utm={KAMPANYE}")


if __name__ == "__main__":
    main()
