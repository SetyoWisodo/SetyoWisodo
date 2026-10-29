# Foto Marketplace Final

Dihasilkan oleh `python make_marketplace.py`. Semua 3000 × 3000 px, JPEG kualitas 92
dengan subsampling 0 (teks tepi tetap tajam saat diperbesar).

---

## Daftar berkas

Per edisi (`EN` / `ID`):

| Berkas | Sudut | Dipakai untuk |
|---|---|---|
| `*_mkt_hero.jpg` | 22° / 11° — depan, punggung, tepi atas | **gambar utama** produk |
| `*_mkt_front.jpg` | 0° / 7° — nyaris lurus | thumbnail kecil, iklan, katalog |
| `*_mkt_angle.jpg` | 38° / 16° — 3/4 tajam | gambar kedua, memperlihatkan ketebalan |
| `*_mkt_fore.jpg` | −28° / 10° — tepi kertas | membuktikan jumlah halaman |
| `*_mkt_back.jpg` | 205° / 9° — sampul belakang | gambar ketiga, untuk pembaca yang sudah tertarik |
| `*_mkt_spine.jpg` | 52° / 9° — punggung terbaca | daftar rak, katalog toko buku |
| `*_mkt_hero.png` | sama dengan hero | latar transparan, untuk banner dan situs |

Keduanya:

| Berkas | Isi |
|---|---|
| `pair_mkt_lineup.jpg` / `.png` | 3600 × 2400, dua edisi berdampingan — **tidak dipakai** karena hanya edisi Inggris yang dijual |

---

## Ke mana masing-masing pergi

### Gumroad

| Slot | Berkas |
|---|---|
| Cover 1 (utama) | `Surviving_the_Future_EN_mkt_hero.jpg` |
| Cover 2 | `cover_en_2_inside.png` (dari folder `gumroad/`) |
| Cover 3 | `Surviving_the_Future_EN_mkt_back.jpg` |
| Thumbnail | `thumb_en.png` (dari folder `gumroad/`) |
| ~~Produk bundle~~ | `pair_mkt_lineup.jpg` — tidak dipakai (hanya edisi Inggris yang dijual) |

### Amazon KDP / Etsy / toko lain

| Kebutuhan | Berkas |
|---|---|
| Gambar utama | `*_mkt_hero.jpg` |
| Gambar 2–7 | `front`, `angle`, `fore`, `back`, `spine` |
| Spesifikasi umum | 2000 px sisi terpanjang, latar putih bersih, tanpa teks tambahan |

Amazon meminta latar putih murni untuk gambar utama — berkas di sini sudah
`#FFFFFF`, bukan putih keabu-abuan.

---

## Kenapa sudutnya dipilih begitu

**Hero 22°**, bukan 38°. Sudut tajam terlihat mengesankan di layar besar, tetapi
pada ukuran thumbnail 200 px huruf di sampul depan menjadi terlalu miring untuk
dibaca. 22° cukup memperlihatkan ketebalan tanpa mengorbankan keterbacaan judul.

**Punggung 52°.** Punggung buku ada di sisi **yaw positif**, bukan negatif. Percobaan
pada −78° hanya menghasilkan tumpukan kertas. Pada 52°, teks punggung membelok
sampai bisa dibaca sementara sampul depan masih utuh.

**Tepi kertas −28°** diperlihatkan dengan sengaja: buku ini 447 dan 462 halaman, dan
ketebalan adalah bukti paling cepat bahwa isinya serius. Itu alasan orang membayar
$45, bukan $9.

---

## Mengubah sesuatu

Semua parameter ada di `make_marketplace.py`:

```python
PX = 3000        # sisi gambar final
SS = 1.7         # supersampling internal (naikkan ke 2.0 untuk tepi lebih halus, lebih lambat)
QUALITY = 92     # kualitas JPEG
SHOTS = [...]    # daftar sudut: ubah yaw_deg / pitch_deg
```

Satu render memakan sekitar 7 detik; seluruh set 90 detik. Render memakai ukuran
nyata dari `book/build_report.json`, jadi kalau tebal punggung berubah setelah
naskah disunting, gambar ini harus dibuat ulang.
