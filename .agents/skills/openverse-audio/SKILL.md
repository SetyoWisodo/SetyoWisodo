---
name: openverse-audio
description: Mencari musik, ambience, dan efek suara berlisensi terbuka lewat API Openverse, lalu mencatat atribusinya per berkas. Dipakai saat video atau halaman butuh audio yang legal dipakai, bukan hasil unduhan tanpa jejak lisensi.
license: MIT · WordPress/openverse · commit 6a3bd6cb07f8
---

# Openverse — audio berlisensi terbuka

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/WordPress/openverse> |
| Bintang saat dicatat | 688 (**di bawah ambang 3.000**) |
| Lisensi | MIT |
| Commit yang dibaca | `6a3bd6cb07f8` |
| API | `https://api.openverse.org/v1/audio/` |

## 1. Kapan dipakai

**Pakai** saat butuh SFX (tuang air, gemeretak, halaman, klik) atau ambience, dan tidak punya
rekaman sendiri. Katalog Openverse menggabungkan banyak sumber (Freesound, Jamendo, Wikimedia).

**Jangan** pakai asal comot: setiap trek punya lisensi berbeda (CC0, CC BY, CC BY-NC).
**CC BY-NC tidak boleh** untuk konten jualan.

## 2. Memanggil API

```bash
# pencarian anonim (kuota kecil, cukup untuk cari-cari)
curl -s "https://api.openverse.org/v1/audio/?q=coffee%20pour&license=cc0,by&page_size=10" \
  | jq '.results[] | {title, creator, license, license_version, url, foreign_landing_url}'
```

- Filter `license=cc0,by` sejak awal; jangan menyaring belakangan.
- Untuk kuota lebih besar, daftar kunci API (tanpa ini pun jalan, lebih lambat).
- Simpan hasil ke `data/audio.json` **bersama** judul, pembuat, lisensi, dan URL sumber.

## 3. Aturan atribusi di repo ini

1. Tiap berkas audio punya baris di `data/audio.json`: `berkas`, `judul`, `pembuat`,
   `lisensi`, `sumber`, `diunduh`.
2. Lisensi CC BY wajib ditulis di halaman yang memakainya (kredit kecil di footer).
3. CC0 tetap dicatat — bukti bahwa asal-usulnya jelas.
4. **Jangan** memakai audio tanpa entri; itu langsung menggugurkan butir "aset sendiri" di gate.

## 4. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Trek hilang saat dipakai | URL sumber berubah | unduh berkasnya, simpan lokal + catat URL asal |
| Video diblokir platform | lisensi NC atau "editorial" | saring `license=cc0,by` |
| Kualitas buruk | hasil pencarian berupa potongan pendek | periksa `duration` dan `bit_rate` di respons |
| Atribusi lupa | dicatat di kepala | tulis langsung ke `data/audio.json` saat unduh |

## 5. Repo ini

Audio hanya untuk video/landing, bukan halaman awal (aturan: tanpa beban berat di atas fold,
dan tanpa pemutaran otomatis). Volume selalu bisa dimatikan, tanpa audio wajib.
