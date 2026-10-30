# Skills — riset konten & mesin pencari

Enam skill untuk D3 (Marketing & Pertumbuhan) dan D4 (Kreatif & Media).
Formatnya mengikuti konvensi **SKILL.md** (YAML frontmatter + prosedur yang bisa dijalankan ulang),
diadaptasi dari tiga sumber: kerangka *social media research skills*, disiplin bukti *claude-ads*
(dibuka 29 Okt 2026), dan kerangka **10 folder / 50 agent** dari post `@dsqjaffa` (28 Okt 2026).

| Sumber | Yang diambil | Yang **tidak** diambil |
| --- | --- | --- |
| [`ScrapeCreators/social-media-research-skills`](https://github.com/ScrapeCreators/social-media-research-skills) (MIT) | kerangka *outlier post finder* & *comment mining*: baseline median per akun, lift, kenapa berhasil, swipe file, aturan "jangan mengarang kutipan" | panggilan API berbayar (`SCRAPECREATORS_API_KEY`) dan scraping otomatis |
| [`AgriciDaniel/claude-ads`](https://github.com/AgriciDaniel/claude-ads) | disiplin bukti: temuan deterministik, sumber tercatat, klaim yang tidak terverifikasi diturunkan statusnya, "tool tidak tersedia = keputusan, bukan sukses" | 12 integrasi platform iklan & perubahan akun |
| [`@thegreatest_sv` — 7 repo desain](https://x.com/thegreatest_sv/status/2115876572464812071) (30 Okt 2026) | struktur gerak & tata kelola desain: kontrak token, komponen, audit anti-slop, adegan HTML | 2 dari 7 tidak dipakai di sini (Figma tanpa akun, Blender tidak ada); sisanya ditulis ulang vanilla |
| [`@Mikadzyki_NFT` — 20 repo motion](https://x.com/Mikadzyki_NFT/status/2115407628138324221) (28 Okt 2026) | hukum produksi film: durasi = bobot, arc energi, beat-sync 120 BPM, larangan angka karangan, QA render (pop scan, seam loop) | 8 dari 20 tidak dipakai (Remotion, HyperFrames, After Effects, Lottie, Playwright/ffmpeg tidak ada di sini) |
| [`@dsqjaffa` — 10 folder / 50 agent](https://x.com/dsqjaffa/status/2115541614986711387) | **struktur kerja** 10 tahap: niche → pesaing → outlier → kreator → hook → format → skrip → skala → lapor → ops | 50 pemanggilan LLM berbayar, Claude connector, agent per post. Diganti fungsi Python: 46 slot otomatis, 2 manual, 2 tidak dipakai |

## Daftar skill

| Skill | Dipakai | Kapan dipakai | Keluaran |
| --- | --- | --- | --- |
| [`social-media-riset`](social-media-riset/SKILL.md) | D3 + D4 | ingin tahu post sejenis apa yang ramai dan **kenapa** | `riset/index.html` bagian 1–3 + swipe file |
| [`komentar-mining`](komentar-mining/SKILL.md) | D3 | butuh bahasa pembeli: keberatan, pertanyaan, permintaan | bagian 4 dasbor riset |
| [`search-intent-riset`](search-intent-riset/SKILL.md) | D3 | butuh kata kunci Google / marketplace / TikTok / mesin jawaban AI | bagian 5 dasbor riset |
| [`studio-konten`](studio-konten/SKILL.md) | D3 + D4 | butuh keputusan mingguan (dobel/hentikan/uji) & 5 skrip siap rekam | `studio/index.html`, `studio/brief-senin.md`, `studio/skrip/*.md` |
| [`motion-web`](motion-web/SKILL.md) | D4 + D3 | membuat gerak halaman / landing page, atau memeriksa "apakah ini terlihat buatan mesin" | `motion/index.html`, 5 adegan 9:16, `laporan/slop.md` |
| [`motion-film`](motion-film/SKILL.md) | D4 | mengubah 5 skrip studio jadi klip yang framenya konsisten: ketukan, arc energi, cue suara | `motion/film-sheet.md` + `.json` (540 frame, 120 BPM) |

Dua perintah menjalankan keempatnya (urutannya penting: studio membaca hasil riset):

```bash
python3 tools/riset.py         # hitung + tulis dasbor, swipe file, dan brief
python3 tools/studio.py        # 10 tahap → studio/index.html, brief Senin, 5 skrip
python3 tools/studio.py --cek  # ringkasan 10 tahap di terminal (0,2 detik)

python3 tools/motion.py        # lab gerak + 5 adegan 9:16 (dari skrip studio)
python3 tools/film.py          # lembar film: frame, ketukan, arc energi → motion/film-sheet.md
python3 tools/slop.py          # audit anti-slop & kontrak desain → laporan/slop.md
```

## Aturan yang berlaku untuk keenam skill

1. **Data publik saja.** Tidak mengambil konten akun privat, tidak menembus login, tidak menyalin
   database pihak lain. Semua baris masuk ke `data/riset-*.csv` **secara manual** oleh owner.
2. **Tidak ada angka karangan.** Kalau metrik tidak terlihat, kosongkan — jangan dikira-kira.
   `tools/riset.py` akan menandai baris tanpa `views` sebagai tidak terhitung.
3. **Status data wajib jujur.** Kolom `status` bernilai `contoh` atau `asli`. Selama belum ada baris
   `asli`, dasbor menampilkan peringatan dan confidence **"belum ada data asli"**.
4. **Adaptasi, bukan salin.** Yang diambil pola (angka, larangan, pengakuan, perbandingan), bukan
   kalimat, footage, audio, atau desain milik akun lain.
5. **Kutipan ≤ 24 kata** dan tanpa identitas pribadi. Kutipan panjang dipotong otomatis.
6. **Refresh ≤ 30 hari.** Pola konten cepat basi; tanggal dibuat tercetak di setiap keluaran.
7. **Skill tidak memutuskan tayang.** Keputusan tayang ada di D3, gerbang klaim di D7
   (`operasional/divisi/D7-brand-legal.md`).
