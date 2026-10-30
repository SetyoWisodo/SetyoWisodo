# Lembar film — 5 adegan, 9.0 detik, 60 fps

Dibuat `tools/film.py` pada 2026-10-30 dari `motion/timeline.json` (yang lahir dari 5 skrip
`tools/studio.py`). Lembar ini **tidak merender video**: ia menghitung frame, ketukan,
dan urutan kerja supaya render di mesin lain bisa deterministik.

| Parameter | Nilai |
| --- | --- |
| Tempo | **120 BPM** · 4/4 · satu ketukan = **30 frame** · satu birama = **120 frame** |
| Durasi | **9 detik = 540 frame** per adegan |
| Arc energi | **cold-open** — tier per cue 4 / 2 / 3 / 5 (1 = diam, 5 = puncak) |
| Sumber | `motion/timeline.json` · `studio/skrip/` · `data/` |

> Kenapa 120 BPM: batas cue studio (3 / 5 / 7 detik) jatuh **tepat** di ketukan 6 / 10 / 14.
> Di 100 BPM atau 133 BPM batas itu meleset 2–6 frame, dan gerak berhenti terasa "nyaris" pas.

## 1 · Grid per adegan

| Adegan | Judul | Cue | Waktu | Frame | Ketukan | Tier | Perangkat | Kamera | SFX |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Kopi pahit padahal baru beli? Cek tiga hal ini… | 1 | 0–3 s | 0–180 | 0 | 4 | judul masuk | dorong 4% | whoosh masuk (puncak terukur) |
| 01 | Kopi pahit padahal baru beli? Cek tiga hal ini… | 2 | 3–5 s | 180–300 | 6 | 2 | daftar 1-2 | diam (lembah) | tick |
| 01 | Kopi pahit padahal baru beli? Cek tiga hal ini… | 3 | 5–7 s | 300–420 | 10 | 3 | daftar 3 + angka | geser 2% | tick |
| 01 | Kopi pahit padahal baru beli? Cek tiga hal ini… | 4 | 7–9 s | 420–540 | 14 | 5 | payoff + CTA | tarik 3% | impact + logo |
| 02 | Kenapa kopi kafe terasa lebih kuat dari kopi r… | 1 | 0–3 s | 0–180 | 0 | 4 | judul masuk | dorong 4% | whoosh masuk (puncak terukur) |
| 02 | Kenapa kopi kafe terasa lebih kuat dari kopi r… | 2 | 3–5 s | 180–300 | 6 | 2 | daftar 1-2 | diam (lembah) | tick |
| 02 | Kenapa kopi kafe terasa lebih kuat dari kopi r… | 3 | 5–7 s | 300–420 | 10 | 3 | daftar 3 + angka | geser 2% | tick |
| 02 | Kenapa kopi kafe terasa lebih kuat dari kopi r… | 4 | 7–9 s | 420–540 | 14 | 5 | payoff + CTA | tarik 3% | impact + logo |
| 03 | Rp23.000 vs Rp152.000: bedanya bukan cuma bera… | 1 | 0–3 s | 0–180 | 0 | 4 | judul masuk | dorong 4% | whoosh masuk (puncak terukur) |
| 03 | Rp23.000 vs Rp152.000: bedanya bukan cuma bera… | 2 | 3–5 s | 180–300 | 6 | 2 | daftar 1-2 | diam (lembah) | tick |
| 03 | Rp23.000 vs Rp152.000: bedanya bukan cuma bera… | 3 | 5–7 s | 300–420 | 10 | 3 | daftar 3 + angka | geser 2% | tick |
| 03 | Rp23.000 vs Rp152.000: bedanya bukan cuma bera… | 4 | 7–9 s | 420–540 | 14 | 5 | payoff + CTA | tarik 3% | impact + logo |
| 04 | Arabika Ijen vs robusta Raung, satu meja. | 1 | 0–3 s | 0–180 | 0 | 4 | judul masuk | dorong 4% | whoosh masuk (puncak terukur) |
| 04 | Arabika Ijen vs robusta Raung, satu meja. | 2 | 3–5 s | 180–300 | 6 | 2 | daftar 1-2 | diam (lembah) | tick |
| 04 | Arabika Ijen vs robusta Raung, satu meja. | 3 | 5–7 s | 300–420 | 10 | 3 | daftar 3 + angka | geser 2% | tick |
| 04 | Arabika Ijen vs robusta Raung, satu meja. | 4 | 7–9 s | 420–540 | 14 | 5 | payoff + CTA | tarik 3% | impact + logo |
| 05 | Tiga hal yang membuat kopi rumahan terasa hamb… | 1 | 0–3 s | 0–180 | 0 | 4 | judul masuk | dorong 4% | whoosh masuk (puncak terukur) |
| 05 | Tiga hal yang membuat kopi rumahan terasa hamb… | 2 | 3–5 s | 180–300 | 6 | 2 | daftar 1-2 | diam (lembah) | tick |
| 05 | Tiga hal yang membuat kopi rumahan terasa hamb… | 3 | 5–7 s | 300–420 | 10 | 3 | daftar 3 + angka | geser 2% | tick |
| 05 | Tiga hal yang membuat kopi rumahan terasa hamb… | 4 | 7–9 s | 420–540 | 14 | 5 | payoff + CTA | tarik 3% | impact + logo |

## 2 · Yang diperiksa mesin sebelum render

| Pemeriksaan | Aturan | Hasil |
| --- | --- | --- |
| Batas cue di ketukan | ≤ 1 frame dari grid 120 BPM | lolos |
| Total durasi | 9 detik (540 frame) | lolos |
| Arc energi | ada puncak (5) dan lembah (≤ 2) | lolos |
| Porsi lembah | 15–45% durasi adegan | lolos |
| Durasi cue | ≤ frasa kamera 3,6 s | lolos |
| Sumber angka | tiap cue menyebut sumber data | lolos |
| Tekstur | tidak ada cue > 1 s tanpa perubahan (A6) | manual: lihat 4 still di bawah |

Masalah terbuka: **tidak ada**

## 3 · Cara menangkap frame (di mesin yang punya browser)

```bash
# 1 · sajikan folder
python3 -m http.server 8080 --bind 0.0.0.0

# 2 · tangkap tiap frame (Playwright, Chromium) — 540 frame per adegan
#    di wajib: await document.fonts.ready, lalu 2x requestAnimationFrame
#    setelah seek(t) sebelum screenshot
#    window.seek(t) sudah ada di motion/frame-0N.html

# 3 · encode: 60 fps, bt709, yuv420p, faststart
ffmpeg -framerate 60 -i frame-%04d.png \
  -vf "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p" \
  -c:v libx264 -crf 16 -pix_fmt yuv420p -color_range tv -colorspace bt709 \
  -movflags +faststart out.mp4
```

Tanpa ffmpeg/Playwright (kondisi sandbox ini): **rekam layar** 1080×1920 selama 9 detik
dengan `?t=0` sebagai awal, atau serahkan lembar ini ke mesin yang punya keduanya.
Jangan menulis "sudah dirender" bila belum ada berkas `.mp4`.

## 4 · Empat still sebelum render penuh

Urutan kerja dari `claude-motion-design` §1: beat map → **4 still** (satu per cue) →
perbaiki → baru render penuh. Tangkap `?t=0.5`, `?t=3.2`, `?t=5.2`, `?t=7.2`
untuk tiap adegan; nilai keterbacaan, kontras, dan apakah teks masuk akal di 9:16.

## 5 · Peta suara

| Cue | SFX | Aturan |
| --- | --- | --- |
| 01·1 | whoosh masuk (puncak terukur) | tier 4 · 0–180 frame |
| 01·2 | tick | tier 2 · 180–300 frame |
| 01·3 | tick | tier 3 · 300–420 frame |
| 01·4 | impact + logo | tier 5 · 420–540 frame |
| 02·1 | whoosh masuk (puncak terukur) | tier 4 · 0–180 frame |
| 02·2 | tick | tier 2 · 180–300 frame |
| 02·3 | tick | tier 3 · 300–420 frame |
| 02·4 | impact + logo | tier 5 · 420–540 frame |
| 03·1 | whoosh masuk (puncak terukur) | tier 4 · 0–180 frame |
| 03·2 | tick | tier 2 · 180–300 frame |
| 03·3 | tick | tier 3 · 300–420 frame |
| 03·4 | impact + logo | tier 5 · 420–540 frame |
| 04·1 | whoosh masuk (puncak terukur) | tier 4 · 0–180 frame |
| 04·2 | tick | tier 2 · 180–300 frame |
| 04·3 | tick | tier 3 · 300–420 frame |
| 04·4 | impact + logo | tier 5 · 420–540 frame |
| 05·1 | whoosh masuk (puncak terukur) | tier 4 · 0–180 frame |
| 05·2 | tick | tier 2 · 180–300 frame |
| 05·3 | tick | tier 3 · 300–420 frame |
| 05·4 | impact + logo | tier 5 · 420–540 frame |

Sumber nada: Mixkit (bebas komersial). SFX diletakkan **pada puncak terukur**
(`argmax|s|`), bukan ditebak; gain 0,04–0,30; fade ekor; loudnorm dua-pass ke −14 LUFS.
Di sandbox ini tidak ada berkas audio, jadi peta ini adalah rencana, bukan hasil.

## 6 · Larangan yang diwarisi 20 repo

1. **Tanpa angka karangan.** Tiap cue menyebut sumbernya; kalau tidak ada di `data/`, angka dicabut.
2. **Satu hal bergerak pada satu waktu** (kecuali slider/skala kontinu). Kalau dua bergerak, salah satu dipindah ke cue lain.
3. **Tanpa easing linear** untuk gerak ruang; tanpa pantulan kartun. Spring dengan damping ≥ 0,72.
4. **Masuk ≠ keluar**: durasi keluar 60–70% durasi masuk.
5. **Stagger ≤ 500 ms** total; 1/3 rule: tidak lebih dari 1/3 elemen bergerak bersamaan.
6. **Loop harus cocok posisi DAN kecepatan** — bukan hanya frame terakhir = frame 0.
7. **Nama gerak harus bermakna**: kamera tidak goyang tanpa alasan cerita.
