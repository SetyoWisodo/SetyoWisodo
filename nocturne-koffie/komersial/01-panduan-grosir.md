# Mesin Komersial — Panduan Grosir & B2B

Berkas di folder ini **dihasilkan** oleh `python3 tools/komersial.py`. Yang perlu Anda isi manual
hanya `pipeline-b2b.csv`. Harga dihitung dari `data/biaya.json` + `data/catalog.json`, jadi kalau
harga green bean berubah, semuanya ikut menyesuaikan.

| Berkas | Isi |
| --- | --- |
| `harga-grosir.csv` | harga per kg untuk 4 tingkat volume + margin aktual tiap tingkat |
| `penawaran-b2b.html` | proposal 1 halaman, siap dicetak / disimpan PDF dan dikirim ke kafe |
| `pipeline-b2b.csv` | daftar prospek + status + jadwal follow-up (dibaca papan harian) |

---

## 1. Empat tingkat harga (aturan, bukan tawaran bebas)

| Tingkat | Minimum | Target margin | Termin |
| --- | --- | --- | --- |
| Kafe kecil | 5 kg / pengiriman | 28% | transfer di muka / COD |
| Kafe aktif | 10 kg | 25% | Net 7 hari |
| Kantor / Hotel | 20 kg | 23% | Net 14 hari |
| Reseller / Private label | 30 kg | 20% | Net 14 hari + DP 50% |

Dua pagar yang tidak boleh dilanggar:

1. **Harga grosir tidak pernah di bawah margin 18%.** Generator menandai sendiri kalau ada yang
   jatuh di bawah itu — artinya harga retail produk tersebut terlalu murah, bukan grosirnya terlalu mahal.
2. **Harga grosir tidak melebihi 92% harga retail per kg.** Kalau tabrakan, generator memotong
   harga dan menandainya sebagai "margin tipis" untuk Anda putuskan.

> Temuan dari perhitungan pertama: **Blend 70/30 dan 60/40** paling sempit marginnya di volume kecil,
> karena harga retail 1 kg keduanya (Rp170.000 / Rp195.000) hampir menyentuh biaya komponen
> (70% robusta Rp52.000 + 30% arabika Ijen Rp140.000 = Rp106.400/kg green). Kalau blend mau dijual
> grosir 5 kg ke kafe, pertimbangkan menaikkan harga retail 1 kg blend ke ±Rp200.000.

---

## 2. Kenapa B2B lebih dulu daripada iklan

| Perbandingan | 1 akun kafe (5 kg/bulan) | Order retail |
| --- | --- | --- |
| Omzet | ±Rp 500.000–1.300.000/bulan (tergantung kopi) | ±Rp 88.000 |
| Frekuensi kerja | 1 pengiriman/bulan | 1 order + 1 chat + 1 packing |
| Beban konten | tidak perlu | perlu konten untuk memicu |
| Prediktabilitas | tinggi (jadwal tetap) | rendah |

Hitungan jalur: **30 prospek → 4 tes sampel → 1 akun**. Jadi 30 prospek = 1 akun = sekitar
6–15 order retail setara, dengan usaha yang jauh lebih kecil.

---

## 3. Alur menjual (dan bukti yang harus dicatat)

| Langkah | Aksi | Dicatat di `pipeline-b2b.csv` |
| --- | --- | --- |
| 1 | Susun daftar 30 kafe/kantor (nama, jenis, area, kontak) | status `belum` |
| 2 | Kirim pesan pertama (template B2B-1, 1 kalimat personal) | `tanggal_pesan`, status `dihubungi` |
| 3 | Kirim 2 sampel 100 g gratis (profil sesuai kebutuhan mereka) | status `sampel`, `profil_diminta` |
| 4 | Follow-up H+4 setelah sampel (satu pesan saja) | status `negosiasi`, `tanggal_followup` |
| 5 | Kirim `penawaran-b2b.html` (PDF) + tawarkan kalibrasi | status `penawaran` |
| 6 | Batch percobaan 5 kg, lalu jadwal tetap | status `aktif`, `volume_target_kg` |

Papan harian otomatis menampilkan prospek yang follow-up-nya jatuh tempo dan total volume aktif.
**Aturan:** satu pesan follow-up per prospek per minggu. Lebih dari itu = spam.

---

## 4. Aturan yang menjaga hubungan

1. **Satu area, satu mitra.** Jangan menjual ke lima kafe di jalan yang sama.
2. **Selalu kirim sampel dulu.** Kafe membeli rasa, bukan daftar harga.
3. **Kalibrasi gratis sekali** di kunjungan pertama (grinder, dosis, rasio). Ini yang membuat
   kafe bertahan dan sulit diganti kompetitor.
4. **Konsistensi = produk B2B Anda.** Catat profil batch yang disetujui, ulangi profil itu.
5. **Private label** ditawarkan setelah 10 kg/bulan stabil — bukan sebagai daya tarik awal.
6. **Jangan menjanjikan volume** yang belum ada green bean-nya. Cek `stok-lot.json` dulu.

---

## 5. Kalau kapasitas mitra sangrai terbatas

Urutan prioritas pemenuhan order saat kapasitas penuh:

1. Langganan retail (sudah dibayar berulang, ekspektasi tanggal tetap)
2. B2B aktif (kontrak volume)
3. Retail biasa
4. Prospek baru (tunda jadwal, jangan janji tanggal)

Kalau permintaan B2B melebihi 50% kapasitas sangrai mingguan, naikkan minimum order atau
buka tingkat harga baru — jangan diam-diam menurunkan kualitas.

---

## 6. Berkas yang dikirim ke prospek

1. `penawaran-b2b.html` → buka di browser → Print → **Save as PDF** → kirim lewat WhatsApp.
2. Sertakan 2 foto: label produk close-up + tumpukan kemasan siap kirim.
3. Jangan kirim daftar harga lengkap sebelum mereka mencoba sampel — harga tanpa rasa tidak berarti.
