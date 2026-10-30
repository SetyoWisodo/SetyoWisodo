# Film Gerak dari Kode — 20 Repo, 1 Lembar Kerja

Sumber: post `@Mikadzyki_NFT`, 28 Okt 2026 — "20 GitHub repos that turn your agents into a
motion empire". Semua 20 tautan sudah dilacak ke repo aslinya (30 Okt 2026), bukan ditebak.

**Posisi skill ini.** `skills/motion-web` mengurus halaman yang bergerak (CSS/JS di browser).
Skill ini mengurus **film**: klip 9 detik yang frame-nya dihitung, bukan dirasa. Batasnya jelas:
di lingkungan ini tidak ada browser, tidak ada `ffmpeg`, tidak ada Node runtime — jadi yang
dihasilkan adalah **lembar kerja yang deterministik** (`tools/film.py`), bukan berkas `.mp4`.

## Kapan dipakai

- Merekam adegan 9:16 dari `motion/frame-0N.html` menjadi video yang konsisten shot-to-shot.
- Menyusun 5 klip D4 supaya tempo, ketukan, dan payoff-nya sama — bukan lima gaya berbeda.
- Menerjemahkan skrip studio (3/5/7 detik) menjadi nomor frame dan cue suara.
- Menolak permintaan "buatkan video" yang tidak bisa dibuktikan: tidak ada `.mp4`, tidak ada klaim.

Jangan pakai untuk: halaman web (itu `motion-web`), desain kemasan (itu `brand/`), atau
mengarang footage proses sangrai yang tidak pernah ada kameranya.

## 20 repo: apa isinya, dan apa yang dipakai di sini

| # | Repo | Inti | Status di repo ini |
| ---: | --- | --- | --- |
| 1 | `whaleyxbt/claude-motion` | toolkit motion untuk coding agent; pipeline Remotion + "web sims" dengan `render(t)` murni; mesin SFX + beat grid | **dipakai prinsipnya** — `seek(t)` murni waktu, beat grid |
| 2 | `howseen-ai/claude-motion-design` | HTML + Playwright + ffmpeg; deterministik `seek(t)`; beat map; anti-"AI motion"; render QA | **dipakai** — alur 10 langkah, aturan anti-AI, template render |
| 3 | `charlie947/motion-graphics-skills` | 15 skill motion graphics + prompt; `validate-skills.sh` | **dipakai idenya** — bank prompt & pemeriksaan mandiri |
| 4 | `haidrrrry/claude-remotion-skill` | skill Remotion; verifikasi frame via `remotion still`; SFX sintetis | tidak dipakai (butuh Node + Chromium) |
| 5 | `t3knobox/klik-anim-skill-creation` | `klik-anim`: hukum A0–A18 (timing, arc energi, ADSR, anti-repetisi) + `klik-cam` | **dipakai** — tabel durasi, arc energi, beat-sync |
| 6 | `Sunwood-ai-labs/hyperframes-motion-reel-skill` | reel ber-sinkron ketukan untuk HyperFrames, 120 BPM / 60 fps ke MP4 | tidak dipakai (HyperFrames = Node CLI) |
| 7 | `AbubakrChan/product-launch-motion` | satu bentuk yang tak pernah cut, spring, kursor sebagai penggerak, SFX per ketukan | **dipakai prinsipnya** — "satu bentuk, transformasi bukan cut" |
| 8 | `cth9191/animate` | video kanvas satu berkas, 7 gaya bawaan, musik dipetakan ke ketukan | **kandidat** — pola "satu berkas HTML mandiri" |
| 9 | `iart-ai/motion-design-skills` | fundamental + mesin + elemen brand (timing, tipografi, warna, komposisi; AE, Remotion, logo) | **dipakai** — urutan: tata bahasa gerak dulu, mesin kemudian |
| 10 | `nateherkai/hyperframes-student-kit` | kit editing 15 skill: cut dari transkrip, storytelling, 406 kartu motion, template HyperFrames | tidak dipakai (butuh editor + Node) |
| 11 | `heygen-com/hyperframes` | tulis HTML → render video; katalog blok siap pakai | **dipakai idenya** — adegan HTML + timeline (tanpa render server) |
| 12 | `remotion-dev/remotion` | video dari React, `useCurrentFrame`, interpolate/spring | tidak dipakai (React + bundler) |
| 13 | `remotion-dev/skills` | skill resmi agent untuk Remotion | **rujukan** — struktur komposisi, bukan runtime |
| 14 | `greensock/GSAP` | timeline, ScrollTrigger, morph | tidak dipakai runtime (±70 KB + CDN); semantiknya ditiru |
| 15 | `LottieFiles/motion-design-skill` | prinsip universal: timing, easing, koreografi, 12 prinsip Disney untuk UI | **dipakai** — tabel durasi, 1/3 rule, anggaran stagger |
| 16 | `frankxai/awesome-motion-design-agent-skills` | indeks skill motion (GSAP, Motion, Remotion, Lottie, Rive) | **dipakai** — peta jalan pemilihan mesin |
| 17 | `Barty-Bart/motion-graphics` | skill motion graphics untuk Claude Code/Codex | belum dibuka isinya; tidak diklaim |
| 18 | `199-biotechnologies/motion-dev-animations-skill` | Motion.dev: spring, scroll, gesture, 120 fps | **prinsipnya** — spring untuk momen fisika, bukan untuk semua gerak |
| 19 | `motiondivision/motion` | library animasi JS (spring, layout, gesture) | tidak dipasang; parameternya dipakai sebagai acuan |
| 20 | `airbnb/lottie-web` | memutar animasi After Effects (JSON) di web | tidak dipakai — tidak ada AE/ekspor Lottie di sini |

Ringkas: **6 dipakai utuh aturannya, 6 dipakai prinsipnya, 8 tidak dipakai** karena menuntut
Node/React/Chromium/ffmpeg/After Effects yang tidak ada di lingkungan ini.

## Empat jalur mesin (dan mengapa jalur A yang dipilih)

| Jalur | Cara kerja | Berat | Kenapa (tidak) dipakai |
| --- | --- | --- | --- |
| **A · HTML + `seek(t)`** | satu berkas HTML, semua posisi dihitung dari waktu; tangkap per frame | 0 dependency | **dipakai** — adegan sudah ada di `motion/frame-0N.html`, tanpa build |
| B · Remotion | React + bundler + renderer | ratusan MB | tidak ada Node runtime di sandbox |
| C · HyperFrames | HTML + GSAP, CLI render | Node CLI | tidak terpasang; idenya dipakai |
| D · Canvas satu berkas | gambar prosedural, 7 gaya | ringan | kandidat untuk klip yang butuh partikel/tekstur |

Jalur A yang dipilih bukan karena paling canggih, tapi karena **satu-satunya yang bisa
diperiksa sekarang**: berkasnya ada, waktunya eksplisit, dan 5 adegan sudah dibangun di atasnya.

## Hukum produksi yang dipegang (dengan angka)

| # | Hukum | Angka | Dari |
| ---: | --- | --- | --- |
| 1 | Durasi = bobot. Mikro-feedback 120–240 ms, panel 560–880 ms, frasa kamera 1,6–3,6 s | lihat tabel | klik A1 |
| 2 | Kalau ragu: **−20% durasi, +settle** | — | klik A1 |
| 3 | Keluar ≠ masuk: durasi keluar **60–70%** durasi masuk | 60–70% | klik A1 |
| 4 | Overshoot kecil di UI (**2–4%**), besar hanya di momen hero | 2–4% | klik A1 |
| 5 | Stagger **≤ 500 ms** total; mikro-kaskade 20–40 ms, standar 50–100 ms | ≤500 ms | LottieFiles |
| 6 | **1/3 rule**: tak lebih dari 1/3 elemen bergerak bersamaan; tak ada gerak > 1/3 layar tanpa keyframe baru | 1/3 | LottieFiles |
| 7 | **Satu hal bergerak pada satu waktu**; satu warna aksen; tanpa gradien pelangi, partikel, emoji | — | claude-motion-design §9b |
| 8 | Spring dengan **damping ≥ 0,72** — pantulan kartun dilarang | ≥0,72 | claude-motion-design |
| 9 | **Arc energi** satu bentuk per adegan: puncak, lembah, puncak. Lembah itu menopang puncak | 1 arc | klik A18 |
| 10 | **Tidak ada frame yang benar-benar diam** > 1 detik | ≤1 s | claude-motion-design §1 |
| 11 | Loop cocok **posisi DAN kecepatan** (frame terakhir = frame 0 secara gerak) | — | howseen §3 |
| 12 | Tanpa angka karangan: tiap angka punya sumber, dan itu ditulis di layar | — | howseen §0 |

## Matematika beat-sync (jalur A)

```
frame_per_beat = (60 / BPM) * fps          # 120 BPM, 60 fps → 30 frame
frame_per_bar  = frame_per_beat * 4        # 120 frame
durasi         = 9 s → 540 frame = 18 ketukan
```

Pilihan tempo bukan selera: batas cue skrip studio adalah **3 / 5 / 7 detik**. Pada **120 BPM**
ketiganya jatuh tepat di ketukan **6 / 10 / 14**. Pada 100 BPM meleset 5 frame, pada 133 BPM
meleset 6 frame — gerak berhenti terasa "nyaris pas", dan itu yang membuat hasilnya terlihat amatir.

Payoff (cue 4) mulai di ketukan 14, bukan di garis birama. Ini **disengaja**: ia perubahan di
dalam satu adegan, bukan cut antar-adegan, dan hukum B1 mengizinkan perubahan internal naik
ketukan tanpa harus sempurna per frame. Kalau nanti ada musik bertanda drop di birama, drop
dipasang di detik 8 (ketukan 16) dan payoff digeser — dicatat di lembar film, bukan diingat.

## Alur kerja satu klip (10 langkah)

1. **Fakta dulu.** Buka `studio/skrip/` + `data/`. Angka yang tidak ada di `data/` dicabut.
2. **Arc energi.** Tentukan bentuknya: `cold-open` (default 9 detik), `ramp`, `wave`, atau `plateau-drop`.
3. **Beat map.** `python3 tools/film.py` → `motion/film-sheet.md` (frame, ketukan, tier).
4. **Empat still.** Tangkap `?t=0.5`, `?t=3.2`, `?t=5.2`, `?t=7.2`. Perbaiki yang gagal baca.
5. **Render penuh.** 540 frame, 60 fps, bt709 (`ffmpeg` di mesin yang punya).
6. **Pindai pop.** Lonjakan beda-frame > 3× tetangganya = ada yang tidak dimaksudkan.
7. **Seam loop.** Cocokkan posisi *dan* kecepatan, bukan hanya frame terakhir.
8. **Suara.** SFX pada puncak terukur; gain 0,04–0,30; loudnorm dua-pass ke −14 LUFS.
9. **Kritik 2–4 putaran.** Satu kontak sheet per ketukan; nilai keterbacaan, ritme, kesinambungan bentuk.
10. **Serah.** Berkas + caption jujur + lembar film. Jangan sebut "dirender" bila tidak ada `.mp4`.

## Peta suara (rencana, bukan hasil)

| Cue | Tier | SFX | Aturan |
| --- | --- | --- | --- |
| 1 · judul masuk | 4 | whoosh masuk | diletakkan di puncak terukur, bukan awal berkas |
| 2 · isi (lembah) | 2 | tick | volume lebih rendah dari cue 1; ritme mengikuti teks per kata |
| 3 · angka | 3 | tick | keyakinan angka ditandai satu hit, bukan rentetan |
| 4 · payoff | 5 | impact + logo | hit terkuat di adegan; fade ekor 300 ms |

Nada memakai **Mixkit** (bebas komersial). Tidak ada berkas audio di repo ini; rencananya ada,
hasilnya tidak diklaim.

## Yang harus dijaga saat mengubah

1. **Jangan ubah `motion/timeline.json` dengan tangan.** Ia lahir dari `tools/motion.py`;
   ubah skrip di `studio/` atau generatornya.
2. **Jangan menambah cue tanpa memperbarui arc.** Jumlah tier harus sama dengan jumlah cue.
3. **Jangan memilih tempo lain tanpa menghitung ulang grid.** 120 BPM dipilih karena alasan aritmetika.
4. **Jangan menyebut nama repo sebagai bukti kualitas.** Yang bisa diperiksa cuma angka di
   `motion/film-sheet.md` dan hasil di layar.
5. **Jangan memasang dependency "sekali coba".** Remotion/HyperFrames/GSAP hanya masuk kalau
   ada mesin yang menjalankannya dan ada alasan yang lebih kuat dari "biar canggih".

## Memeriksa

```bash
python3 tools/film.py --cek     # 5 adegan · 20 cue · 0 masalah
python3 tools/film.py           # tulis motion/film-sheet.md + .json
python3 tools/periksa.py        # cek "Film gerak": grid, arc, sumber, durasi
```
