# Tujuh divisi — indeks alur kerja & target

Satu divisi = satu berkas = satu pemilik yang jelas. Tidak ada divisi yang "diurus bersama"
tanpa nama penanggung jawab; yang boleh dibagi adalah **orangnya**, bukan **keputusannya**.

| Kode | Divisi | Berkas | Mandat satu baris | Waktu/minggu |
| --- | --- | --- | --- | --- |
| D1 | Produksi & QC | [D1-produksi-qc.md](D1-produksi-qc.md) | Tidak ada bungkus keluar tanpa pernah dicicipi | ±2 jam |
| D2 | Penjualan & CRM | [D2-penjualan-crm.md](D2-penjualan-crm.md) | Chat jadi order, order jadi pelanggan yang kembali | ±3 jam |
| D3 | Marketing & Pertumbuhan | [D3-marketing-pertumbuhan.md](D3-marketing-pertumbuhan.md) | Proses produksi jadi alasan percaya, lalu ke WhatsApp | ±2 jam |
| D4 | Kreatif & Media | [D4-kreatif-media.md](D4-kreatif-media.md) | Aset visual layak brand premium, tanpa fotografer | ±40 menit |
| D5 | Operasional & Logistik | [D5-operasional-logistik.md](D5-operasional-logistik.md) | Paket utuh, hari yang sama, resi terlacak | ±4 jam |
| D6 | Keuangan | [D6-keuangan.md](D6-keuangan.md) | Tahu laba per bungkus, bukan hanya ramai | ±2 jam |
| D7 | Brand & Legal | [D7-brand-legal.md](D7-brand-legal.md) | Klaim bisa dibuktikan, tampilan sudah diizinkan | ±1,5 jam |

Total beban: **±15 jam/minggu** untuk satu orang — karena itu urutannya harus disiplin,
bukan karena semuanya harus dikerjakan setiap hari. Lihat ritme harian di
[`../00-struktur-divisi.md`](../00-struktur-divisi.md).

---

## Bagaimana target disimpan

Angka target **tidak** ditulis di berkas divisi. Sumber tunggalnya:

```
data/divisi.json
```

Setiap divisi punya blok `kpi` dengan 3–4 ukuran. Tiap ukuran membawa:

| Field | Arti |
| --- | --- |
| `nama` | label yang muncul di papan |
| `kunci` | penghubung ke perhitungan di `tools/papan.py` |
| `satuan` | `order`, `%, `Rp`, `post`, `video`, … |
| `arah` | `naik` (makin besar makin baik) atau `turun` |
| `target` | `[bulan_1, bulan_2, bulan_3]` → Nov 2026, Des 2026, Jan 2027 |

Papan harian membaca berkas itu dan menampilkan **target vs aktual** per divisi.
Aktual dihitung dari berkas data (`pesanan.csv`, `batch-qc.csv`, `konten-14hari.csv`,
`kpi.csv`, `kreatif.json`, `legal.json`) — **bukan diketik ke papan**.

```bash
python3 tools/papan.py --tanggal 2026-11-03   # regen papan + tabel target
python3 tools/papan.py --json | head -40      # cek angka tanpa membuka browser
```

### Mengubah target

1. Ubah angka di `data/divisi.json` (jangan di dokumen divisi).
2. Jalankan `python3 tools/papan.py`.
3. Tulis alasan perubahan di commit message — target yang bergerak tanpa alasan
   membuat semua perbandingan bulanan jadi tidak berarti.

### Status di tabel papan

| Status | Arti |
| --- | --- |
| `tercapai` | aktual sudah melewati (atau sama dengan) target bulan ini |
| `di bawah` | belum mencapai target — normal di awal bulan, perlu perhatian di akhir bulan |
| `tanpa data` | belum ada berkas yang mencatat ukuran ini (jujur, bukan bug) |

Tiga ukuran yang saat ini **tanpa data**: klip mentah (D4), klaim melanggar (D7), dan
sebagian angka iklan. Cara mengisinya tertulis di masing-masing berkas divisi.

---

## Urutan ketergantungan

```
D1 Produksi ──► D4 Kreatif ──► D3 Marketing ──► D2 Penjualan ──► D5 Logistik
     │                                                            │
     └──────────────► D6 Keuangan ◄───────────────────────────────┘
D7 Brand & Legal  ── menjaga semua divisi (gerbang klaim & izin)
```

| Bila divisi ini berhenti… | Yang paling cepat merasakan |
| --- | --- |
| D1 | D4 kehilangan bahan, D2 kehilangan stok, D5 tidak ada yang dikirim |
| D2 | D6 tidak bisa menghitung, D5 menganggur |
| D3 | D2 kehilangan permintaan baru dalam 2–3 minggu |
| D4 | D3 mulai memakai aset berulang; feed terasa basi |
| D5 | D2 menerima komplain; biaya per order naik |
| D6 | keputusan harga jadi tebakan |
| D7 | satu klaim salah bisa menghapus kerja 3 bulan |

## Berkas lama

SOP versi enam divisi (sebelum pemisahan D3/D4) dipindahkan ke [`../arsip/`](../arsip/)
tanpa dihapus, sebagai rujukan sejarah. Yang berlaku adalah berkas di folder ini.
