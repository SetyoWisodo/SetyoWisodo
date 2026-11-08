---
name: rea-catalog
description: Baca katalog reacher-z/Awesome-REA sebelum memilih tool atau paper RE, dan periksa satu catatan baru terhadap format katalognya sebelum diusulkan. Menjawab "alat apa untuk target protokol/game/app?", "repo ini berelasi resmi dengan REA atau tidak?", dan "catatan ini lolos validator atau tidak". Pakai saat butuh rujukan tool/paper yang bisa diaudit, saat menyusun entri katalog, atau saat memutuskan sebuah repo layak disebut "dipakai di REA". English triggers — Awesome-REA catalog search, which tool for this target, catalog record format, relationship to REA, source-reviewed evidence, validate catalog entry.
metadata:
  version: "1"
  source: https://github.com/reacher-z/Awesome-REA
  upstream: https://github.com/reacher-z/Awesome-REA/tree/a1a6b24191bcc039c0a0483506fac13bb8335b57
  diperiksa: "2026-11-09"
---

# Awesome-REA → katalog yang dibaca, bukan daftar yang dipercaya

> **Bagian dari alur kerja terpadu.** `rea-workflow` memutuskan *fase* dan *routing target*;
> skill ini menyediakan **bukti rujukan**: entri mana yang sudah ditinjau sumbernya, untuk target
> apa, dengan relasi apa ke REA — dan bagaimana menambah satu entri tanpa mengarang.

Repo sumber: [`reacher-z/Awesome-REA`](https://github.com/reacher-z/Awesome-REA) — **MIT**,
54 MB, ~1.400 berkas, 1.999 bintang, push 8 Nov 2026, situs `awesomerea.org`. Katalog independen
(bukan proyek REA itu sendiri) berisi tool, studi kasus, paper, dan temuan otomatis — semuanya
berbahasa Inggris + Mandarin.

**Kenapa skill ini ada, dan bukan sekadar "buka README-nya".** README-nya 316 KB (melewati batas
tampil GitHub 500 KB, jadi mereka menulis batas peringatan 420 KB sendiri), dan yang paling berguna
justru **field terstruktur** yang tidak terlihat di README: `relationship`, `targets`, `kind`,
`verified_at`. Membaca README tidak bisa menjawab "mana yang berelasi resmi dengan REA dan mana yang
cuma kebetulan menyebut REA". JSON-nya bisa.

## Isi katalog (angka dari API, 9 Nov 2026)

| Berkas | Catatan | Isi |
| --- | ---: | --- |
| `data/tool-resources.json` | **1.130** | tool, integrasi, studi kasus, koleksi, dokumentasi |
| `data/rea-resources.json` | **123** | yang benar-benar berelasi dengan proyek REA (`official-*`, `community-*`) |
| `data/papers.json` | **235** | bibliografi riset (arXiv/DOI), tiap entri `runtime_tested: false` |
| `data/source-index.json` | 6,7 MB | indeks hasil pindai otomatis — **bukan** tinjauan, jangan dicampur |

## Kapan dipakai

- "Alat apa untuk target *protocol*?" → saring `targets` + `relationship`, jangan menebak dari nama.
- Sebelum merekomendasikan repo: cek apakah sudah ditinjau, tanggalnya, dan apa batasnya.
- Sebelum menulis "tool ini terintegrasi dengan REA": cek `relationship`-nya
  (`independent-agent-integration` ≠ `official-skill`).
- Saat menyusun entri/studi kasus baru untuk repo ini atau repo lain dengan format yang sama.
- Saat butuh paper pendukung (mis. metode rekonstruksi UI dari screenshot).

Jangan pakai untuk: mengklaim alat sudah diuji. Katalog ini **tidak pernah** menguji jalannya alat —
lihat kolom kejujurannya di bawah.

## Dua mode skrip (`scripts/rea_catalog.py`)

```bash
# 1 · BACA — satu berkas diambil lewat GitHub API, di-cache 12 jam di /tmp/rea-cache
python3 scripts/rea_catalog.py cari ghidra
python3 scripts/rea_catalog.py cari --target protocol --relasi foundation --batas 5
python3 scripts/rea_catalog.py cari --rea --relasi official-skill
python3 scripts/rea_catalog.py cari --kertas "code reconstruction"

# 2 · PERIKSA — menguji satu berkas catatan lokal terhadap format katalog (luring)
python3 scripts/rea_catalog.py periksa catatan-saya.json
```

Mode `cari` menerima kata bebas + tiga saringan (`--target`, `--relasi`, `--kategori`), memilih
berkas dengan `--rea` / `--kertas`, dan menampilkan `kind · relationship · category · target`,
URL, tanggal tinjauan, serta ringkasan 220 karakter. Mode `periksa` menegakkan aturan di bawah dan
mengembalikan kode keluar ≠ 0 bila ada yang gagal — bisa dipakai di CI.

## Kolom kejujuran katalog (dan kenapa bentuknya begitu)

| Field | Arti sebenarnya | Salah tafsir yang umum |
| --- | --- | --- |
| `verification: source-reviewed` | **dokumennya** dibaca, bukan kode dijalankan | dianggap "sudah diuji" |
| `verified_at` | tanggal tinjauan sumber (boleh +1 hari untuk zona waktu) | dianggap tanggal rilis |
| `added_at` | tanggal entri pertama masuk `main` (dari squash merge) | dianggap tanggal tinjauan |
| `requirements` | prasyarat, cakupan, batas, bukti uji, lisensi, atribusi | diisi cerita hasil |
| `relationship` | hubungan yang **dibuktikan bukti**, bukan oleh antarmuka | "ada MCP" → dianggap integrasi resmi |
| `class` | hanya untuk record data (studi kasus satu benda nyata) | dipasang di tool umum |
| `reconstruction_method` | hanya untuk studi kasus `game` | dipasang di tool biasa |

Aturan yang paling sering menyelamatkan: **nama, daftar pihak ketiga, atau adanya antarmuka MCP
tidak membuktikan kemampuan.** Katalognya sendiri memberi contoh: `playwright-mcp` ber-relationship
`independent-agent-integration` justru karena antarmuka MCP saja tidak cukup; `kef-lsx-volume-case`
ber-`targets: [app]` walau memakai jaringan, karena akses jaringan tidak otomatis berarti target
`protocol`.

## Alur menambah satu entri (6 langkah)

1. **Cari dulu** — `cari <kata>`; mungkin sudah ada. Jangan bikin duplikat.
2. **Pilih dimensi terpisah**: `kind` (apa yang dibagikan), `relationship` (hubungan yang
   dibuktikan), `category` (keluarga tugas), `targets` (sasaran yang dibantu). Satu tidak
   menentukan yang lain.
3. **Sumber primer + commit yang dipin.** Tautan bukti GitHub harus `/blob/<commit>/…` atau
   `/tree/<commit>/…`; tautan akar repo ditolak. Tautan `url` tetap tautan proyek yang bergerak.
4. **Tulis dua bahasa.** `description_en` + `description_zh` ringkas, satu kalimat yang berdiri
   sendiri. `requirements`: prasyarat dulu, lalu batas (lisensi, hasil yang belum terbit).
5. **Periksa lokal** — `python3 scripts/rea_catalog.py periksa catatan.json`.
6. **Validasi upstream** kalau mengusulkan ke repo itu:
   `python3 scripts/build_readme.py && python3 scripts/build_repository_index.py && python3 scripts/validate.py`
   (lalu `build_site.py` + `node --check site/app.js`; `python3 scripts/check_links.py` untuk tautan).

## Jebakan yang sudah ditulis di sumbernya

- **Pindai ≠ tinjauan.** `source-index.json` hasil otomatis; untuk menaikkannya dipakai *promotion
  worksheet*, dan objek pindai tidak pernah "dinaikkan" atau ditulis ulang.
- **Batas laju bukan tautan mati.** 403, 429, halaman login, timeout, dan redirect saja **tidak**
  membuktikan entri dicabut. Untuk melaporkan tautan mati, sertakan status, tanggal, dan bukti primer.
- **README punya batas ukur.** GitHub berhenti menampilkan README di 500 KiB; repo ini memberi
  peringatan (bukan gagal) sejak 420.000 byte. Jangan menambah entri langsung ke README — bangun.
- **Jangan sunting hasil generator.** README, `docs/papers.md`, `docs/cases.md`, direktori repo, dan
  ringkasan cakupan kasus dibangun dari JSON. Yang disunting JSON-nya.
- **Tanpa kalimat defensif.** "Ini bukan X", "tidak menyiratkan Y" tidak dipakai di teks yang dibaca
  pengunjung; ketelitian ditaruh di label status, tanggal, dan lisensi.
- **Tanggal karangan = gagal.** Tanggal publikasi, tanggal arXiv, dan tanggal konferensi adalah tiga
  fakta berbeda; publisher-date tidak boleh disamakan dengan event-date.

## Hasil yang bisa dipakai sekarang

```bash
python3 scripts/rea_catalog.py cari --target protocol --relasi foundation --batas 5
# → mitmproxy · Kaitai Struct · Wireshark … (masing-masing dengan tanggal tinjauan)

python3 scripts/rea_catalog.py cari --rea --relasi official-skill
# → 1 entri: skill resmi reverse-engineer-anything di repo morluto/rea

python3 scripts/rea_catalog.py cari --kertas "code reconstruction" --batas 3
# → paper-screencoder (2026, arXiv 2507.22827), dll.
```

## Batas skill ini

| Hal | Status |
| --- | --- |
| Kebenaran isi entri | mengikuti `source-reviewed` sumbernya: dokumen dibaca, **bukan** alat dijalankan |
| Cakupan | hanya tiga berkas katalog JSON; indeks pindai 6,7 MB tidak diambil |
| Jaringan | mode `cari` butuh `gh` + api.github.com; tanpa jaringan hanya cache 12 jam yang tersisa |
| Kesetaraan validator | `periksa` menegakkan aturan yang terbaca dari `data/README.md` + `validate.py`; validator upstream tetap otoritatif |
| Bahasa | entri katalog berbahasa Inggris + Mandarin; skill ini menjelaskannya dalam Bahasa Indonesia, tidak menerjemahkan isi entri |
