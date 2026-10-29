---
name: studio-konten
description: >
  Menjalankan alur kerja "tim social media" 10 tahap (niche → pesaing → outlier → kreator → hook →
  format → skrip → skala → lapor → ops) sebagai mesin deterministik, bukan 50 agent LLM. Gunakan
  saat butuh rencana konten mingguan yang bisa dipertanggungjawabkan: apa yang di-dobel, apa yang
  dihentikan, apa yang diuji, dan 5 skrip siap rekam. Menghasilkan studio/index.html,
  studio/brief-senin.md, dan studio/skrip/*.md dari data lokal. Tanpa API, tanpa token.
version: 1.0.0
author: Nocturne Koffie (D3 Marketing × D4 Kreatif)
license: internal
metadata:
  dipakai_divisi: [D3, D4]
  butuh_berkas:
    - data/studio-niche.json
    - data/studio-hooks.csv
    - data/studio-industri.csv
    - data/riset-referensi.csv
    - data/riset-komentar.csv
    - data/riset-kata-kunci.csv
    - data/kreatif.json
    - data/catalog.json
    - data/batch-qc.csv
  keluaran:
    - studio/index.html
    - studio/brief-senin.md
    - studio/skrip/skrip-01..05-*.md
    - studio/data.json
  perintah: python3 tools/studio.py
  izin_akses: baca berkas lokal + tulis folder studio/
---

# Studio Konten — 10 Tahap, 50 Slot, 0 Token

## Ikhtisar

Ada dua cara membangun "tim social media": menyewa 50 orang (atau 50 agent AI), atau menuliskan
50 pekerjaan itu sebagai **prosedur yang dihitung mesin**. Skill ini memilih cara kedua.

Kerangka 10 folder / 50 agent diadaptasi dari post `@dsqjaffa` (28 Okt 2026) — niche research,
competitor tracking, outlier videos, outlier creators, hooks, formats & trends, scripts, scaling,
reporting & briefs, content operations. Yang diambil **strukturnya**, bukan tool-nya: tidak ada
Claude connector, tidak ada API berbayar, tidak ada agent yang menagih token per post.

Alasannya praktis. Sebagian besar pekerjaan dalam kerangka itu adalah hitungan tetap: median,
lift, ranking, persentase simpan, cek kata terlarang, cek duplikat. Itu semua bisa jadi fungsi
Python — bisa diulang, bisa diperiksa, biayanya nol. Yang benar-benar butuh pertimbangan manusia
(memilih sudut, mencicipi rasa, menghubungi orang) tetap ditandai `manual` dan tetap di tangan owner.

## Kapan dipakai

Pakai saat:

- hari Senin, butuh brief mingguan yang memutuskan **dobel / hentikan / uji**;
- butuh 5 skrip yang siap direkam Rabu, bukan ide di kepala;
- ingin tahu format dan struktur hook mana yang layak diulang, dengan angka;
- ingin memastikan konten baru tidak mengulang hook yang sudah dipakai.

Jangan pakai untuk: memposting otomatis, membaca metrik live, atau menggantikan penilaian rasa.
Skill ini tidak punya akses akun sosial, tidak memanggil API, dan tidak mengunggah apa pun.

## Alur 10 tahap

| # | Tahap | Yang dihitung | Keluaran |
| ---: | --- | --- | --- |
| 01 | niche research | definisi ceruk, pagar "bukan", 4 segmen audiens, tangga tawaran, 7 kata dilarang, pemeriksaan makna ganda, usulan frasa dari komentar | `studio/index.html` §01 |
| 02 | competitor tracking | akun yang benar-benar ditangkap + catatan industri manual + rencana video jawaban | §02 |
| 03 | outlier videos | filter ceruk, lift vs baseline, ranking views/ER/simpan, **dead views flag** | §03 |
| 04 | outlier creators | interaksi per 1K views, syarat **≥2 outlier**, riwayat ≤30 hari, watchlist | §04 |
| 05 | hooks | bank 30 hook, 10 struktur, hitung per struktur, lift median, **film pertama** | §05 |
| 06 | formats & trends | ER & lift per platform×format, kuartal atas vs bawah, peta gaya rekam | §06 |
| 07 | scripts | 5 skrip 9 detik: hook 3s → 2 baris bukti → CTA, cek suara, kutip sumber | §07 + `studio/skrip/` |
| 08 | scaling | bedah pemenang, simpan struktur, 3 remix per pemenang, pola paling dibagikan | §08 |
| 09 | reporting & briefs | tabel 10 teratas, dobel/hentikan/uji, 5 skrip, laporan tim | §09 + `studio/brief-senin.md` |
| 10 | content operations | jadwal mingguan, cek pemakaian ulang, peta 50 slot, jadwal berulang | §10 |

## Pemetaan 50 slot → siapa yang mengerjakan

`tools/studio.py` menyimpan peta ini dan menampilkannya utuh di §10, supaya klaim "otomatis" bisa
diperiksa baris per baris. Ringkasnya: **46 otomatis · 2 manual · 2 sengaja tidak dipakai.**

| Folder | Slot | Dikerjakan |
| --- | --- | --- |
| 01 niche | definition, audience & offer, search phrase finder, double-meaning excludes | otomatis |
| 01 niche | leaders and competitors | manual (`data/studio-niche.json` → `pesaing`) |
| 02 pesaing | competitor agent, creator tracker, answer video planner | otomatis |
| 02 pesaing | top 50 company ranker | otomatis, tetapi hanya untuk akun yang **kita** tangkap — bukan klaim top-50 industri |
| 02 pesaing | industry agent | manual (`data/studio-industri.csv`) |
| 03 outlier | finder, niche filter, ranking, dead views | otomatis |
| 04 kreator | finder, per-1K, two-outlier minimum, 30-day flag, watchlist | otomatis |
| 05 hook | bank, grouper, counter, median ranker, first film picker | otomatis |
| 06 format | finder, filming style mapper, kuartal, copy this week | otomatis |
| 07 skrip | top 5, script writer, voice matcher, source citer, loop | otomatis |
| 08 skala | winner breakdown, keeper, remixer, script per concept | otomatis |
| 09 lapor | top 10, Monday brief, dobel/hentikan/uji, five scripts, team report | otomatis |
| 10 ops | playbook reader, reuse check, recurring | otomatis |
| 10 ops | Claude connector, Claude Code setup | **tidak dipakai** — tidak ada kredensial, dan tidak boleh dikarang |

## Aturan yang membuat skrip lolos

`cek_suara()` menolak skrip yang:

1. memakai kata terlarang brand (`promo`, `diskon`, `buruan`, `termurah`, …);
2. memakai superlatif (`paling`, `terbaik`, `terlezat`, …);
3. punya kalimat lebih dari 18 kata;
4. tidak memuat angka atau tanggal;
5. tidak memuat CTA WhatsApp.

Skor ≥ 88 **dan** asetnya ada di `data/kreatif.json` → status `siap rekam`. Selain itu
`perlu perbaikan`. Semua klaim di skrip mencantumkan berkas sumber (`catalog.json`,
`batch-qc.csv`, `brand/label-ijen.png`), jadi tidak ada angka yang muncul tanpa jejak.

## Cara pakai

```bash
python3 tools/studio.py          # hitung 10 tahap + tulis halaman, brief, 5 skrip
python3 tools/studio.py --cek    # ringkasan terminal saja (0,2 detik)
```

Siklus mingguan:

1. **Senin** — buka `studio/brief-senin.md`, ambil satu keputusan (dobel/hentikan/uji).
2. **Selasa** — tambah baris `asli` ke `data/riset-*.csv`, lalu jalankan `studio.py` lagi.
3. **Rabu** — rekam dari `studio/skrip/`; ubah `status` hook di `data/studio-hooks.csv` jadi `dipakai`.
4. **Sabtu** — render aset lewat `tools/kreatif.py`, cek di `konten/index.html`.

## Batas yang harus diingat

- **Keputusan dari data `contoh` belum membuktikan pasar.** Selama belum ada baris `asli`,
  brief menampilkan peringatan dan semua keputusan berlabel contoh.
- **Tidak ada angka live.** Views, ER, simpan, dan bagikan diisi manual dari tangkapan layar.
- **Tidak memposting.** Unggahan, balas chat, dan pembayaran tetap manual.
- **Data industri manual.** Dampak tren dicatat manusia; mesin hanya menyalin dan menautkan tindakan.
- **Angka pihak lain bukan klaim kita.** Lift referensi dipakai untuk memilih pola, bukan untuk
  menulis "lebih baik dari brand X".
