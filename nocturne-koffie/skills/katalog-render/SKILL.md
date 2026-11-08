---
name: katalog-render
description: Foto katalog dan hero landing page dirender dari satu rig: sudut, cahaya, dan latar yang sama untuk semua SKU, dengan angka yang bisa diperiksa. Dipakai D4 saat butuh foto produk yang konsisten tanpa sesi pemotretan ulang, atau saat menilai apakah foto baru masih satu keluarga dengan foto lama.
---

# Foto Katalog & Hero — Satu Rig, Sembilan Lot

**Sumber:** https://x.com/thegreatest_sv/status/2119129564047982889 (7 repo 3D, 7 Nov 2026) + Pillow (MIT-CMU)

Foto katalog dan hero landing page dirender dari satu rig: sudut, cahaya, dan latar yang sama untuk semua SKU, dengan angka yang bisa diperiksa. Dipakai D4 saat butuh foto produk yang konsisten tanpa sesi pemotretan ulang, atau saat menilai apakah foto baru masih satu keluarga dengan foto lama.

# Foto Katalog & Hero — Satu Rig, Sembilan Lot

**Posisi skill ini.** `skills/hero-3d` mengurus hero biji 3D. `skills/gaya-gambar` mengurus
gaya generator gambar (dan sejak 5 Nov pemilik menolak hasil generator). Skill ini mengurus
**foto produk**: kemasan yang harus tampil sama di katalog, kartu, dan header halaman jual —
tiga sudut per SKU, tinggi objek sama, bayangan sama, latar sama.

**Sumber gagasan:** post [`@thegreatest_sv`](https://x.com/thegreatest_sv/status/2119129564047982889)
(7 Nov 2026, 1.134 suka) — "7 repos every 3D designer NEEDS to know": MCP for Blender,
BlendRelay MCP, TRELLIS.2, Hunyuan3D, TripoSR, ShaderAgent, Nerfstudio. Angka bintang dan
lisensinya diperiksa sendiri lewat GitHub API, bukan dari post.

**Yang diambil:** resep **studio rig**-nya — satu kamera, satu lampu, satu latar, lalu SKU
digilir di depannya; dan pemisahan tugasnya (model, material, tangkapan nyata).
**Yang tidak diambil:** pemanggilan model 3D. Tidak ada GPU, tidak ada Blender, tidak ada
bobot model di sandbox ini, dan tidak ada izin memasang apa pun. Yang dikerjakan alat sendiri:
geometri kotak berperspektif dari label vektor yang sudah ada.

## Tujuh repo di post itu — status jujur di sini

| # | Repo | Bintang / lisensi (diperiksa 9 Nov 2026) | Status di proyek ini |
| ---: | --- | --- | --- |
| 1 | `ahujasid/blender-mcp` | 33.641 · MIT | **tidak dipakai** — butuh Blender + MCP runtime |
| 2 | `shefq/blendrelay-mcp` | 24 · MIT | **tidak dipakai** — di bawah ambang 3.000 bintang, butuh Blender |
| 3 | `microsoft/TRELLIS.2` | 12.732 · MIT | **tidak dipakai** — bobot model + CUDA |
| 4 | `Tencent-Hunyuan/Hunyuan3D-2` | 15.352 · lisensi tak terbaca (NOASSERTION) | **ditolak** — lisensi tidak jelas untuk aset komersial |
| 5 | `VAST-AI-Research/TripoSR` | 7.335 · MIT | **tidak dipakai** — sama, butuh GPU |
| 6 | `VAST-AI-Research/ShaderAgent` | 32 · belum jelas | **ditolak** — di bawah ambang, tanpa rilis yang bisa dipakai |
| 7 | `nerfstudio-project/nerfstudio` | 12.170 · Apache-2.0 | **tidak dipakai** — butuh tangkapan foto nyata, bukan aset yang ada |

Artinya: dari tujuh repo itu **nol** yang dijalankan di sini. Yang dipakai adalah **gagasan
rig-nya**, dan itu diakui di laporan. Yang benar-benar dipakai untuk menghasilkan foto:
`Pillow` (MIT-CMU) — proyeksi homografi, pencahayaan, bayangan.

## Resep yang dipakai (angka, bukan kesan)

| Bagian | Angka | Alasan |
| --- | --- | --- |
| Sudut | **0°, −18°, 40°** | depan untuk katalog, 3/4 untuk hover, sisi untuk meyakinkan bentuk |
| Pitch kamera | **−5°** | sedikit dari atas; lebih dari 8° membuat label terbaca miring |
| Tebal kemasan | **6,5% lebar depan** | karton terisi 200–250 g, bukan balok |
| Key light | arah **(−0,62, −0,78)** | kiri-atas, sama untuk semua SKU |
| Muka samping | **62%** kecerahan muka depan (kanan) · **96%** (kiri, saat kena lampu) | satu sumber cahaya |
| Gradien samping | turun **30%** ke tepi jauh | sisi jauh selalu lebih gelap |
| Muka atas | **102%** + turun 20% ke kanan | cahaya dari atas |
| Latar | `#EDEBE6` → `#F6F3EC` + vignette | kertas brand, bukan putih studio |
| Objek di katalog | **70%** tinggi bidang (toleransi 8% antar SKU) | sembilan foto harus terbaca satu seri |
| Objek di hero | **72%**, diletakkan di **x = 68%** | kiri kosong untuk judul |
| Ukuran | katalog **2000²**, hero **2400×1350**, JPEG q88 | muat retina, tetap < 300 KB per foto |
| Bayangan | kontak (elips sempit, 210 alfa) + jatuh (96 alfa, kabur 1/3 tinggi) | objek terasa di atas meja |

## Alur kerja

```bash
python3 tools/katalog.py            # render 9 SKU × 3 sudut + 9 hero  → 4 MB
python3 tools/katalog.py --satu gayo   # satu SKU saja, untuk mencoba sudut/cahaya
python3 tools/katalog.py --cek      # ukuran, tinggi objek, letak objek di hero, konsistensi
node tools/katalog-uji.mjs          # halaman katalog: data, kartu, sudut, harga, WA (tanpa peramban)
python3 tools/katalog-luring.py     # satu berkas HTML 1,1 MB, foto disisipkan (tanpa server)
```

Keluaran: `assets/img/katalog/<id>-{0,18,40,hero}.jpg`, `data/katalog.js` (harga dari
`data/catalog.json`), `laporan/katalog-render.png` (lembar kontak 9 × 3), dan halaman
`katalog/index.html`.

## Tiga kesalahan yang sudah dibayar di sini

1. **`Image.QUAD` bukan perspektif.** Pemetaan QUAD memakai interpolasi bilinear; muka kotak
   jadi berbentuk baji dan label terlihat melengkung. Yang benar: proyeksi titik 3D ke bidang
   kamera, lalu **homografi balik** (`Image.PERSPECTIVE`). Kesalahan ini terlihat langsung di
   still pertama — bukan setelah halaman jadi.
2. **Muka samping yang dicetak label.** Awalnya sisi diambil dari tepi kanan gambar label,
   sehingga potongan tulisan ikut tergambar di sisi kemasan. Sisi dan atas harus **papan
   kosong**: warna diambil dari median 4 sudut label, dicetak tidak.
3. **Pangkas dengan ambang warna.** Latar kertas `#EDEBE6` dan kertas label `#F0EBE0` hanya
   beda beberapa satuan; `getbbox` dengan ambang 12 ikut memotong tepi objek dan menyisakan
   kotak. Yang benar: pangkas tepat sebesar padding geometri yang sudah dihitung.

## Aturan yang memegang seluruh skill

- **Satu rig untuk semua SKU.** Kalau satu lot terlihat lebih besar, lebih terang, atau
  lebih miring, seri foto itu gagal walau tiap gambar bagus sendiri-sendiri. `--cek`
  membandingkan tinggi objek antar SKU (toleransi 8%) dan menolak yang menyimpang.
- **Jangan menipu material.** Sisi kemasan adalah karton, bukan logam: tidak ada kilau
  palsu, tidak ada refleksi yang tidak ada di produk nyata.
- **Foto asli tetap prioritas.** Begitu pemilik mengirim foto kemasan asli, pipa
  `tools/kemasan.py` yang dipakai (foto → tanpa latar → 3D). Render ini adalah **isi
  sementara yang jujur** selama foto belum ada — dan jangan pernah menyebutnya foto asli.
- **Harga tidak pernah diketik di halaman.** `data/katalog.js` dibangun dari
  `data/catalog.json`; uji memeriksa harga di JS sama dengan katalog.
- **Tanpa generator gambar.** Permintaan 5 Nov 2026 masih berlaku: hasil `generate_image`
  tidak dipakai. Yang dipakai pengolahan deterministik.

## Batas yang tidak diklaim

| Hal | Status |
| --- | --- |
| Rupa akhir halaman katalog | **belum pernah dilihat** — tidak ada Chromium; uji hanya memeriksa data & sambungan |
| Foto sebagai "foto produk" | ini render dari label, bukan pemotretan kemasan fisik |
| Akurasi bentuk | kemasan dimodelkan sebagai kotak; lipatan gusset dan zipper tidak dimodelkan |
| Model 3D dari tujuh repo | tidak satu pun dijalankan (butuh GPU/Blender/bobot) |
| Sudut 40° di versi luring | tidak disisipkan ke berkas tunggal (hemat 400 KB); tombolnya jatuh ke sudut 0° |
