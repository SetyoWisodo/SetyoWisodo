# D3 · Marketing & Pertumbuhan — alur kerja & target

> **Mandat:** menjadikan proses produksi sebagai alasan orang percaya, lalu menuntun mereka ke WhatsApp.
> **Pemilik:** owner dibantu agent · **Waktu:** 90 menit/minggu + 10 menit/hari.
> **Berkas kerja:** `data/konten-14hari.csv` · `data/kpi.csv` · `marketing/00-strategi-90hari.md` · `marketing/09-media-kreator.md`.
> **Aset dari mana:** D4 (`konten/`, `data/kreatif.json`). D3 **tidak membuat** video; D3 memilih, menulis, menjadwalkan, mengukur.
> **Target & KPI:** `data/divisi.json` (D3).

D3 adalah satu-satunya divisi yang boleh berbicara kepada orang di luar. Karena itu D3 juga
satu-satunya divisi yang paling mudah merusak brand — setiap klaim di sini mengikat D1 dan D7.

---

## 1. Alur kerja inti — konten dari produksi ke chat

```
[1] Produksi terjadi (D1) ─► [2] D4 merekam 8–10 klip mentah
                                        │
                                        ▼
                       [3] D4 render aset (tools/kreatif.py)
                              video 9:16 · carousel 4:5 · story
                                        │
                                        ▼
              [4] D3 pilih 7 aset/minggu sesuai pilar (Bukti 30 · Proses 30 · Edukasi 25 · Jualan 15)
                                        │
                                        ▼
              [5] Tulis caption + hook + CTA (marketing/08-konten-siap-pakai.md)
                                        │
                                        ▼
              [6] Jadwalkan di 3 kanal + WhatsApp Status + marketplace
                                        │
                                        ▼
              [7] Isi data/konten-14hari.csv (tanggal, platform, status)
                                        │
                                        ▼
              [8] Setelah tayang: ubah status → `terbit` di CSV / `data/kreatif.json`
                                        │
                                        ▼
              [9] Ukur: simpan, chat dari konten, biaya per chat → data/kpi.csv
```

**Aturan urutan:** tidak boleh ada dua post jualan berurutan. Kalau kampanye menuntut jualan,
selipkan satu bukti (QC/catatan batch) di antaranya.

---

## 2. Kanal & beban per kanal

| Kanal | Frekuensi | Isi | Penanggung jawab | Cek mingguan |
| --- | --- | --- | --- | --- |
| Instagram Reels | 2/minggu | proses & bukti (9:16 dari D4) | D3 | simpan ≥ 10, tayangan |
| Instagram carousel | 1/minggu | bukti/edukasi (4:5 dari D4) | D3 | simpan & share |
| Instagram Story | 2–3/minggu | jajak pendapat, batch baru | D3 | balasan DM |
| TikTok | 3/minggu | vertikal tanpa wajah, audio asli | D3 | watch-time |
| WhatsApp Status | 2–3/minggu | foto batch + tanggal sangrai | D3 | balasan chat |
| Marketplace | 9 listing | judul + foto + tanya-jawab | D3 | chat & konversi |
| Landing kampanye | 1 halaman | `kampanye/index.html` (dari `tools/kampanye.py`) | D3 | klik WA (utm) |

Tidak menambah kanal baru sebelum kanal yang ada stabil 4 minggu berturut-turut.

---

## 3. Ritme kerja

### Harian — 10 menit
1. Buka papan → bagian **Marketing — jadwal konten**. Ada yang tayang hari ini?
2. Kalau kosong: ambil satu aset siap dari `konten/` dan tayangkan (tidak perlu menunggu jadwal ideal).
3. Catat chat/DM yang masuk karena konten (angka kasar cukup, isi di KPI mingguan).

### Mingguan — 90 menit (Selasa)
| Menit | Kegiatan | Output |
| --- | --- | --- |
| 10 | Pilih 7 aset minggu ini dari `konten/` | daftar aset + pilar |
| 25 | Tulis caption/hook; ganti 1–2 detail agar tidak terasa template | 7 caption final |
| 15 | Susun jadwal (Meta Business Suite + TikTok + Status) | jadwal terisi |
| 10 | Isi `data/konten-14hari.csv` | baris terjadwal |
| 20 | Ukur minggu lalu: simpan, chat, biaya per chat | baris `data/kpi.csv` |
| 10 | Pilih satu hal yang akan diulang & satu yang dihentikan | catatan 2 baris |

### Bulanan — 60 menit
1. Ranking 12 konten terakhir: mana yang menghasilkan chat, bukan hanya tayangan.
2. Hentikan format yang 3× berturut tidak menghasilkan chat.
3. Perbarui `campaign`/utm dan regenerate `kampanye/index.html` bila harga atau aset berubah.
4. Hitung biaya per chat: total biaya iklan ÷ jumlah chat yang menyebut konten.
5. Ajukan ke D7 setiap klaim baru sebelum dipakai (bukan sesudah).

---

## 4. Target kerja 3 bulan

Dari `data/divisi.json` → D3.

| Ukuran | Nov 2026 | Des 2026 | Jan 2027 | Cara hitung | Arah |
| --- | --- | --- | --- | --- | --- |
| Konten terbit | 16 | 20 | 24 | baris CSV berstatus `terbit` per bulan | naik |
| Konten terlambat | 0 | 0 | 0 | jadwal lewat & status belum `terbit` | turun |
| Chat masuk | 40 | 100 | 180 | `chat_wa` di `data/kpi.csv` | naik |
| Followers IG | 300 | 800 | 1.500 | angka akun, dicatat tiap minggu | naik |

Pendukung: simpan per post ≥ 10 → 15 → 20; listing marketplace 3 → 6 → 9;
biaya per chat ≤ Rp25.000 → Rp20.000 → Rp18.000.

**Target konten dihitung dari aset yang benar-benar terbit**, bukan dari aset yang dirender.
Manifest `data/kreatif.json` yang menentukan ketersediaan; CSV yang menentukan kebenaran.

---

## 5. Definisi selesai

| Rentang | Selesai bila… |
| --- | --- |
| Satu aset | caption + hook + CTA tertulis, jadwal tercatat di CSV |
| Satu minggu | 7 aset terjadwal; KPI minggu lalu terisi; 1 keputusan ulang/hentikan ditulis |
| Satu bulan | 16–24 konten terbit; biaya per chat dihitung; klaim baru sudah lewat D7 |
| Satu kampanye | landing page punya utm, semua tautan WA membawa label kanal |

## 6. Serah terima

| Dari | Kepada | Apa |
| --- | --- | --- |
| D4 | D3 | aset siap tayang + manifest |
| D1 | D3 | angka batch nyata (skor, tanggal, kode) untuk caption |
| D3 | D2 | permintaan yang masuk lewat konten (jangan dibiarkan menunggu) |
| D3 | D7 | setiap klaim/angka baru sebelum tayang |
| D3 | D6 | biaya iklan & hasil per chat |

## 7. Jebakan

1. **Mengejar tayangan, bukan chat.** 10.000 tayangan tanpa chat = konten hiasan.
2. **Menulis klaim yang tidak bisa dibuktikan** ("terbaik di Banyuwangi", "nomor satu").
3. **Menunggu footage sempurna.** Aset dari data (label, angka batch) sudah cukup jujur.
4. **Menjadwalkan 20 konten sekaligus** lalu berhenti 3 minggu. Ritme lebih penting dari volume.
5. **Mengubah caption tanpa memperbarui CSV** — papan jadi buta dan target jadi fiksi.
