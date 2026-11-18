---
name: librosa-beat
description: Deteksi tempo, ketukan, dan onset audio pakai librosa untuk menyelaraskan potongan gambar dengan musik. Dipakai saat waktu potong harus ikut irama, bukan angka detik yang ditebak.
license: ISC · librosa/librosa · commit 76f10b8d2d00
---

# librosa — potong di ketukan

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/librosa/librosa> |
| Bintang saat dicatat | 9.005 |
| Lisensi | ISC |
| Commit yang dibaca | `76f10b8d2d00` |
| Pasang | `pip install librosa` (menarik numpy, scipy, soundfile) |

## 1. Kapan dipakai

**Pakai** untuk mendapat daftar waktu ketukan (detik) dari lagu, lalu memakai daftar itu
sebagai penanda potongan di Remotion/FFmpeg.

**Jangan** pakai untuk mengubah audio itu sendiri (itu FFmpeg), atau mengharapkan hasil
sempurna pada musik tanpa ritme jelas (ambience, drone).

## 2. Resep yang sudah terbukti

```python
import librosa, numpy as np, json

y, sr = librosa.load("assets/audio/lagu.mp3", sr=22050, mono=True)
tempo, ketukan = librosa.beat.beat_track(y=y, sr=sr)      # tempo BPM, ketukan = indeks frame
waktu = librosa.frames_to_time(ketukan, sr=sr)            # detik
onset = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
waktu_onset = librosa.frames_to_time(onset, sr=sr)

json.dump({"tempo": float(np.atleast_1d(tempo)[0]),
           "ketukan": [round(float(t), 3) for t in waktu],
           "onset": [round(float(t), 3) for t in waktu_onset]},
          open("data/beat.json", "w"), indent=1)
```

`backtrack=True` menggeser onset ke awal serangan sebenarnya — tanpa itu, potongan terasa telat.

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Tempo salah separuh/dobel | lagu 6/8 atau beat kuat di off-beat | bandingkan dengan `librosa.feature.tempo`; periksa manual 8 ketukan |
| Hasil beda tiap mesin | versi librosa/numpy berbeda | kunci versi, simpan `data/beat.json` (jangan hitung ulang saat render) |
| Audio lambat dimuat | `sr=None` (44,1 kHz) padahal deteksi cukup 22 kHz | `sr=22050` |
| Onset terlalu rapat | ambang default | `onset_detect(..., delta=0.2, wait=10)` |

## 4. Repo ini

`data/beat.json` disimpan bersama video, bukan dihitung ulang saat build — hasil deteksi
harus bisa diulang. Untuk video produk, potongan mengikuti ketukan 1 dan 3 saja; terlalu
banyak potong membuat label kopi tidak sempat terbaca.
