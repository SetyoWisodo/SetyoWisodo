# D7 · Brand & Legal — alur kerja & target

> **Mandat:** semua yang diklaim bisa dipertanggungjawabkan; semua yang ditampilkan sudah diizinkan.
> **Pemilik:** owner · **Waktu:** 30 menit/minggu + 45 menit/bulan.
> **Berkas kerja:** `data/legal.json` · `brand/` · brief FINAL 3.7 bagian 11.8.
> **Target & KPI:** `data/divisi.json` (D7).

D7 tidak membuat desain baru dan tidak menulis konten. D7 memeriksa:
**apakah yang kita tampilkan dan janjikan bisa dibuktikan** — dan menyiapkan dokumen agar usaha ini
bisa tumbuh (marketplace, B2B, iklan berbayar) tanpa kejutan administratif.

---

## 1. Alur kerja inti — gerbang klaim

```
[1] D3/D4/D2 mengajukan aset atau teks baru
        │
        ▼
[2] Uji 4 pertanyaan klaim:
        ├─ Bisa dibuktikan dengan berkas/angka? ───── tidak ──► [3a] ubah jadi kalimat faktual
        ├─ Menyebut kami "roastery" / menyangrai sendiri? ─ ya ─► [3b] tolak, ganti ke Ais Coffee Roastery
        ├─ Menampilkan orang/lokasi tanpa izin? ────────── ya ─► [3c] tahan sampai ada izin tertulis
        └─ Menjanjikan yang belum diputuskan? ──────────── ya ─► [3d] hapus atau tunda
        │
        ▼ semua lolos
[4] Aset boleh tayang → catat keputusan (tanggal, siapa yang memutuskan)
        │
        ▼
[5] Bulanan: cek dokumen usaha (NIB, izin, perjanjian mitra) → perbarui data/legal.json
        │
        ▼
[6] Temuan pelanggaran → evaluasi akar masalah, bukan hanya menghapus unggahan
```

### Empat klaim yang tidak boleh dipakai (brief 11.8, mengikat semua kanal)

| Dilarang | Ganti dengan |
| --- | --- |
| "Kami roastery" / "kami menyangrai sendiri" | "Disangrai mingguan oleh Ais Coffee Roastery di Banyuwangi" |
| "Terbaik di Banyuwangi" / "nomor satu" | "Skor cupping batch ini 84,0 dengan catatan …" |
| "Fresh from the roaster" tanpa tanggal | "Tanggal sangrai 21 Okt 2026 · kode batch NK-RNG-2610-A" |
| "Kopi petani [nama]" tanpa izin | "Biji dari [desa], ketinggian [x] mdpl" (tanpa nama bila belum ada izin) |

Selain itu: **jangan pernah** mempublikasikan foto petani, titik lokasi kebun, atau nama lengkap
mitra tanpa izin tertulis. Data yang belum diizinkan tampil boleh dipakai internal, tidak untuk publik.

---

## 2. Ritme kerja

### Mingguan — 30 menit (Kamis)
| Menit | Kegiatan | Bukti |
| --- | --- | --- |
| 10 | Periksa aset yang akan tayang minggu depan (dari manifest D4) | aset: lolos / ditahan |
| 10 | Cek konsistensi visual & verbal: nama brand, penulisan "Koffie", label tanggal | daftar koreksi |
| 10 | Perbarui `data/legal.json` bila ada dokumen yang selesai | status dokumen |

### Bulanan — 45 menit
1. Cek masa berlaku izin & dokumen; tandai yang kedaluwarsa < 60 hari.
2. Tinjau satu halaman situs/konten lama untuk klaim yang sudah tidak akurat.
3. Periksa aturan platform marketplace (judul, klaim kesehatan, kata terlarang).
4. Catat temuan klaim: jumlah, penyebab, tindakan.

### Per kuartal
1. Perjanjian mitra sangrai: volume, harga, kepemilikan label, tanggung jawab QC.
2. Izin publikasi data petani (nama, desa, elevasi) — per petani, tertulis.
3. Peninjauan merek: kelas barang yang didaftarkan, pemakaian logo oleh pihak lain.

---

## 3. Target kerja 3 bulan

Dari `data/divisi.json` → D7.

| Ukuran | Nov 2026 | Des 2026 | Jan 2027 | Cara hitung | Arah |
| --- | --- | --- | --- | --- | --- |
| Dokumen legal selesai | 5 | 7 | 8 | dokumen berstatus `selesai`/`ada` di `data/legal.json` | naik |
| Dokumen tertunda | ≤ 3 | ≤ 1 | 0 | total dokumen − selesai | turun |
| Klaim melanggar | 0 | 0 | 0 | temuan per bulan | turun |

Pendukung: izin publikasi petani 3 → 6 → 7 petani.
"Klaim melanggar" belum punya berkas pencatat; sampai ada, angkanya tampil **tanpa data** di papan.
Untuk mengisinya: tambahkan kolom `klaim_melanggar` di `data/kpi.csv`.

---

## 4. Definisi selesai

| Rentang | Selesai bila… |
| --- | --- |
| Satu aset | ada keputusan tertulis: lolos / ditahan / diubah |
| Satu minggu | semua aset minggu depan sudah diperiksa sebelum tayang |
| Satu bulan | `legal.json` akurat; 0 temuan klaim yang lolos tanpa sengaja |
| Satu kuartal | perjanjian mitra & izin petani diperbarui |

## 5. Serah terima

| Kepada | Apa | Kapan |
| --- | --- | --- |
| D3 | daftar klaim yang boleh/tidak boleh dipakai | sebelum jadwal tayang |
| D4 | aturan visual & izin tampil | sebelum render aset kampanye |
| D2 | batasan klaim saat menjawab chat/penawaran | berkelanjutan |
| D6 | dokumen yang butuh biaya (pendaftaran, izin) | saat penyusunan anggaran |

## 6. Jebakan

1. **Memeriksa setelah tayang.** Menghapus unggahan tidak menghapus tangkapan layar.
2. **Menganggap "sudah biasa dilakukan orang lain" sebagai izin.** Aturan platform tetap berlaku.
3. **Menunda NIB karena "belum perlu".** Marketplace & iklan berbayar menuntut dokumen ini.
4. **Menyebut nama petani karena "sudah dipakai di label".** Label cetak dan publikasi digital punya izin berbeda.
5. **Menilai klaim dari niat, bukan dari bunyi kalimat.** Yang dibaca orang adalah kalimatnya.
