# Laporan periksa — 2026-10-30

Dibuat otomatis oleh `tools/periksa.py` setelah seluruh generator dijalankan.

| Ringkasan | Jumlah |
| --- | --- |
| Pemeriksaan lolos | **20** |
| Peringatan | **0** |
| Gagal (harus diperbaiki) | **0** |

| Kategori | Status | Hasil | Catatan |
| --- | --- | --- | --- |
| Berkas wajib | ✅ lolos | 57/57 berkas ada | — |
| Tautan lokal | ✅ lolos | 124/124 tautan menuju berkas yang ada | — |
| Struktur HTML | ✅ lolos | 15/15 halaman tag-nya seimbang | — |
| Stok semua SKU | ✅ lolos | 9/9 SKU berstatus tersedia | — |
| Produk ↔ lot | ✅ lolos | 9/9 produk punya lot aktif (blend memakai komponen) | — |
| Manifest ↔ aset | ✅ lolos | 15 item manifest · 0 berkas hilang | — |
| Brief ↔ aset | ✅ lolos | 5 brief · 0 aset tidak ditemukan | — |
| Target divisi | ✅ lolos | 29/29 KPI punya target 3 bulan | — |
| Klaim terlarang | ✅ lolos | 0 temuan di 4 halaman publik | — |
| Skrip studio | ✅ lolos | 5 skrip siap rekam · 0 masalah | — |
| Bank hook | ✅ lolos | 30 hook · 12 dipakai · 18 tersedia | — |
| Peta 50 slot | ✅ lolos | 46 otomatis · 2 manual · 2 tidak dipakai (total 50) | — |
| Kontrak desain | ✅ lolos | 6 warna inti · 10 radius · 8 aturan gerak · 8 pengecualian terdokumentasi | — |
| Anti-slop | ✅ lolos | 29 aturan · 0 kritis · 0 perhatian | — |
| Komponen gerak | ✅ lolos | 6 jenis komponen dipakai · 6 ditangani motion-ui.js | — |
| Adegan 9:16 | ✅ lolos | 5 adegan · total 9 detik masing-masing | — |
| Panggung 3D | ✅ lolos | 3 komponen dipakai · 15.8 KB CSS+JS · jatuh datar tanpa JS | — |
| Film gerak | ✅ lolos | 20 cue · 120 BPM · 540 frame/adegan · 20 repo terdokumentasi | — |
| Berat halaman awal | ✅ lolos | 89 KB (batas 1.500 KB) | — |
| Berat folder konten | ✅ lolos | 3.8 MB (batas 12 MB) | — |

## Yang belum bisa diperiksa mesin

| Hal | Kenapa | Siapa yang memeriksa |
| --- | --- | --- |
| Rasa kopi & keputusan batch | butuh manusia mencicipi | D1 |
| Angka biaya nyata | masih asumsi di `data/biaya.json` | D6 |
| Izin publikasi nama petani | butuh dokumen tertulis | D7 |
| Data riset kompetitor | masih baris `contoh` | D3 |
| Tayang di IG/TikTok/marketplace | tidak ada akses akun | owner |

Laporan ini memeriksa **konsistensi**, bukan kebenaran pasar. Semua lolos berarti
"sistem tidak bertentangan dengan dirinya sendiri", bukan "bisnis sudah terbukti".
