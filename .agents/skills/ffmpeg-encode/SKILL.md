---
name: ffmpeg-encode
description: Encode, gabung, dan potong video pakai FFmpeg dengan setelan yang benar-benar bisa diputar di semua perangkat — H.264 yuv420p, faststart, CRF, dan audio AAC. Dipakai di akhir setiap pekerjaan video sebelum berkas diserahkan.
license: LGPL/GPL (ikuti build yang dipakai) · FFmpeg/FFmpeg · commit 3a78197c4c96
---

# FFmpeg — potongan akhir

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/FFmpeg/FFmpeg> (mirror resmi) |
| Bintang saat dicatat | 67.522 |
| Lisensi | LGPL 2.1+ / GPL 2+ tergantung build — build `gpl` tidak boleh dipakai untuk hal yang menuntut LGPL |
| Commit yang dibaca | `3a78197c4c96` |
| Pasang | `apt install ffmpeg` / `brew install ffmpeg` / `pip install imageio-ffmpeg` |

## 1. Setelan wajib untuk web & media sosial

```bash
# mp4 H.264 yang diputar di mana saja (Safari, Android, WhatsApp, Instagram)
ffmpeg -y -framerate 30 -i frame/%04d.png \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -movflags +faststart -c:a aac -b:a 160k -ar 48000 out/video.mp4
```

| Setelan | Kenapa |
| --- | --- |
| `-pix_fmt yuv420p` | tanpanya, video 10-bit/444 tampil hitam di Safari |
| `-crf 18` | kualitas transparan ke mata; 23 lebih kecil, 15 hampir lossless |
| `-movflags +faststart` | moov atom di depan → bisa langsung diputar saat diunduh |
| `-framerate 30` di input PNG | kalau lupa, FFmpeg menebak 25 dan durasi jadi salah |
| `-c:a aac -ar 48000` | AAC 48 kHz paling aman untuk semua platform |

## 2. Perintah yang sering dipakai

```bash
# dari video yang ada → 9:16 untuk reels/status
ffmpeg -i in.mp4 -vf "scale=-2:1920:flags=lanczos,crop=1080:1920" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy reels.mp4

# GIF pendek dari potongan
ffmpeg -ss 1 -t 3 -i in.mp4 -vf "fps=15,scale=640:-1:flags=lanczos" -loop 0 out.gif

# poster 1 frame
ffmpeg -ss 0.5 -i in.mp4 -frames:v 1 -q:v 2 poster.jpg

# periksa hasil — jangan pernah percaya tanpa ini
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,pix_fmt,codec_name -of default=nw=1 out/video.mp4
```

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Video hitam di iPhone | `yuv444p` atau 10-bit | `-pix_fmt yuv420p` |
| Durasi salah | input PNG tanpa `-framerate` | set `-framerate` di input |
| Suara tidak sinkron | audio diproses terpisah dengan `-c:a copy` setelah dipotong | potong video dan audio pada titik yang sama, atau re-encode audio |
| Berkas 200 MB | CRF terlalu rendah | CRF 20–23 untuk media sosial |
| Tidak bisa diputar sebelum diunduh penuh | tanpa `+faststart` | tambahkan |
| Warna berubah | tanpa metadata warna | `-colorspace bt709 -color_primaries bt709 -color_trc bt709` |

## 4. Repo ini

Video untuk web ditaruh di `assets/video/`, dengan poster `.jpg`, dan `<video preload="none">`
supaya halaman awal tetap < 1,5 MB. Jangan pernah menjalankan encode di halaman; ini langkah
build, bukan langkah runtime.
