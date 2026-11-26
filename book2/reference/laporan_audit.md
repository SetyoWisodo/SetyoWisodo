# Laporan Audit Kesiapan Rujukan — Edisi Inggris

Dihasilkan otomatis oleh `book2/tools/audit_rujukan.py --lang en`.

## Ringkasan

| Metrik | Nilai | Ambang rujukan | Status |
|---|---:|---:|---|
| Kata | 26.060 | — | — |
| Sitasi dalam teks | 86 | ≥ 1 per 500 kata | lolos |
| Sitasi per 1.000 kata | 3.30 | ≥ 2,0 | lolos |
| Sumber unik | 47 | ≥ 40 | lolos |
| Sitasi yatim (tak ada di bibliografi) | 0 | 0 | lolos |
| Kalimat berangka tanpa sumber | 5 | ≤ 26 | lolos |
| Klaim di buku besar bukti | 45 | ≥ 120 | gagal |
| Klaim terverifikasi | 40 | semua | gagal |

## Sitasi yatim

Tidak ada. Setiap sitasi punya entri bibliografi.

## Catatan atas angka-angka ini

- **Sumber unik** dihitung dari kunci `@…` yang benar-benar muncul di `src/en/`. Bibliografi
  memuat 79 entri; 47 di antaranya dikutip edisi ini, sisanya tersedia untuk bab Indonesia
  dan untuk penambahan berikutnya.
- **Kalimat berangka tanpa sumber** yang tersisa sebagian besar adalah pernyataan
  mekanisme, bukan data (mis. "30 sentimeter air mengalir dapat menggeser mobil").
- **Klaim buku besar** 45 baris adalah buku besar bersama untuk edisi ID dan EN; angka 45
  belum mencerminkan seluruh 17 bab Inggris. Setiap angka baru yang masuk wajib menambah baris.

## Status per bagian

| Bagian | Bab | Kata | Sitasi | Sumber unik |
|---|---:|---:|---:|---:|
| Pengantar | — | 1.138 | 0 | 0 |
| I — Diagnosis | 1–3 | 5.454 | 20 | 12 |
| II — Vulnerability | 4–7 | 5.845 | 21 | 13 |
| III — Capacity | 8–11 | 5.749 | 21 | 12 |
| IV — Decisions | 12–14 | 3.763 | 10 | 7 |
| V — Action | 15–17 | 4.032 | 14 | 8 |

## Yang belum selesai

1. **Edisi Indonesia** baru 4 dari 17 bab ditulis ulang ber-sitasi. 13 bab masih memakai
   teks v0.3 tanpa sitasi; sasaran berikutnya adalah menyelaraskannya bab demi bab.
2. **Buku besar klaim** perlu tumbuh dari 45 menjadi ±120 baris agar setiap angka di 17 bab
   Inggris punya baris sendiri. 5 klaim masih `perlu-cek`.
3. **Glosarium, soal diskusi, latihan riset** tidak termasuk cakupan yang disepakati
   (paket "standar") — jangan ditambahkan tanpa persetujuan.
