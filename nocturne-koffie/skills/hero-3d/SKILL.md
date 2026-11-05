> **Revisi 5 Nov 2026.** Biji di beranda tidak lagi digambar sebagai mesh
> WebGL. Bentuknya sekarang **render hiper-realistis** (`assets/img/biji-render-02.png`
> → `assets/img/biji-3d-poster.jpg` lewat `tools/biji_render.py`), dengan enam
> titik di atas gambar (`titik_foto`, persen) dan kemiringan halus ±7°.
> Bagian WebGL di bawah adalah cara lama — jangan dipakai untuk membuat hero baru.
> Alasan penggantian: mesh parametrik terbaca seperti gumpalan cokelat, bukan biji.

# Hero 3D — Satu Biji Kopi, Senyawa di Dalamnya

Sumber gagasan: tag **3D** di motionsite.ai (13 item) dan header 3D di jiro.build, ditambah
kebutuhan brand sendiri: hero Nocturne harus menunjukkan **benda** yang bisa disentuh, bukan
foto orang minum kopi.

Hasil kerja (lama): `index.html` hero + `assets/js/biji3d.js` (WebGL ±18 KB) + poster PNG mesh
(640×800) + `data/biji3d.json` (bentuk, warna, 6 zona, 12 senyawa, 4 sumber literatur).

## Kapan dipakai

- Menambah atau mengubah hero beranda, dan menambah titik senyawa baru.
- Merombak warna/bentuk biji tanpa mengubah token brand.
- Menjawab "kok biji 3D-nya beda dengan posternya?" — jawabnya: jalankan `node tools/verifikasi-biji.mjs`.

Jangan pakai untuk: klip video (`motion-film`), halaman biasa (`desain-prompt`), atau desain kemasan.

---

## 1 · Apa yang dilihat dari dua platform itu

| Sumber | Yang terbuka | Yang diambil |
| --- | --- | --- |
| motionsite.ai tag `#3d` (13 item) | nama, deskripsi gaya, tag | pola: hero 3D hampir selalu **satu objek**, latar nyaris kosong, satu titik interaksi |
| `motionsite.ai/sections/interactive-3d-hero` (Cripton) | deskripsi: "dynamic glassmorphism", **React Three Fiber + Framer Motion**, dark | peringatan: jalur mereka butuh three.js + R3F (±600 KB) dan latar gelap. Nocturne tidak memakai keduanya |
| `motionsite.ai/sections/3d-animation-hero`, `aero`, `netro` | tag `#3d`, `#scroll-animation`, `#interactive` | urutan: objek → gerak halus → satu ajakan. Tidak ada menu 3D berlapis |
| `jiro.build` header `Digital Art 3D — Cube`, `Auren`, `Morphi` | **hasil render** header | komposisi: objek di satu sisi, tipografi di sisi lain, ruang kosong besar di antaranya |
| `jiro.build/templates/...` (137 template) | struktur halaman | pelajaran: objek 3D tidak pernah jadi latar penuh teks — selalu ada blok teks yang bersih |

Kesimpulan yang bisa dipakai tanpa membayar: **satu objek, satu titik perhatian, tipografi tidak
bertumpuk dengan objek, dan gerak hanya sebagai umpan balik sentuhan.** Teks prompt mereka tetap
di balik paywall dan tidak disalin.

## 2 · Kenapa WebGL mentah, bukan three.js

| Pilihan | Berat | Bisa diverifikasi di sini? | Keputusan |
| --- | --- | --- | --- |
| three.js + React Three Fiber (jalur motionsite) | ±600 KB + React | tidak (tanpa browser) | **tidak dipakai** |
| three.js saja | ±155 KB | tidak | tidak dipakai |
| **WebGL mentah** | **±18 KB, tanpa dependensi** | **ya — matematikanya bisa diuji di Node** | **dipakai** |
| Model `.glb` hasil pindai | 1–8 MB | tidak ada model asli | ditolak: tidak boleh mengklaim hasil pindai |

Karena bentuknya ditulis sebagai rumus (bukan berkas model), poster CPU di Python dan render WebGL
di browser memakai **rumus yang sama**. Itu yang membuat klaim "poster = tampilan hidup" bisa diuji.

## 3 · Bentuk biji (deterministik, tanpa tekstur)

1. **Elipsoid** dengan setengah-sumbu `a=1,00 · b=0,62 · c=0,46` — kopi lebih pipih dari bola.
2. **Ujung meruncing**: `y,z × (1 − 0,16·(|x|/a)³)`.
3. **Sisi datar**: sisi +Z diratakan (`z × 0,72…1`) — biji kopi punya satu muka hampir rata.
4. **Dua belahan**: tonjolan `+0,2·c·cos(...)` di kiri-kanan alur.
5. **Alur S**: `d = 0,52·exp(−(Δθ − 0,42·sin(1,15πx/a))² / (2·0,115²))`, lalu `z −= d·c`.
   Dihitung dari **sudut azimut**, bukan dari z — z sudah diratakan dan tidak monoton.
6. **Pitting**: tiga fungsi sinus dikalikan, amplitudo `0,0045`. Ini yang membuat permukaan tidak
   terasa plastik saat kena specular.

Semua angka di atas hidup di `data/biji3d.json#geometri`. Tidak ada satu pun di JS atau Python.

## 4 · Warna medium roast

Tidak ada hex baru. Cokelat sangrai disusun dari token brand:

| Peran | Token | Hex |
| --- | --- | --- |
| bayangan / tepi bawah | `--g4b` | `#3A2013` |
| badan biji | `--g2b` | `#7A4A1E` |
| bagian atas yang kena panas | `--g4a` | `#B4703A` |
| kilau minyak | `--gold` | `#D9A441` |
| latar | `--paper` | `#F5EFE4` |

Plus satu `#93381F` (`--g3a`) untuk titik zona. Aturan `periksa.py` menolak hex di luar daftar token,
jadi "cokelat medium" tidak bisa diam-diam jadi hijau zaitun.

## 5 · Titik senyawa: apa yang muncul saat disentuh

Enam zona, dua senyawa per zona. Setiap senyawa membawa **rumus, rentang, peran, sumber, dan tanda
keyakinan** (`kuat` = terukur di literatur, `umum` = rentang buku teks).

| # | Zona | Senyawa |
| ---: | --- | --- |
| 01 | Cekungan tengah | Sukrosa sisa · 5-HMF |
| 02 | Kulit sangrai | Melanoidin · pirazin & furanon |
| 03 | Inti biji | Kafein · trigonelin |
| 04 | Bintik minyak | Lipid kopi · diterpen (kafestol, kahweol) |
| 05 | Ujung biji | Asam nikotinat · trigonelin sisa |
| 06 | Daging & serat | Klorogenat (5-CQA) · asam kuiniat & asetat |

Angka yang ditampilkan menyebut sumbernya (S1–S4 di `data/biji3d.json`), misalnya kafein
**0,9–1,3%** (Arabika, basis kering) dan trigonelin **0,87–0,90% → turun ±50%** pada sangrai medium.

**Yang wajib disebut di halaman:** rentang itu berasal dari literatur Arabika medium roast, **bukan
hasil lab biji Nocturne**, dan bentuk bijinya model 3D, bukan hasil pindai. Kalimat itu ada di
`kejujuran.catatan_tampil` dan tampil di panel serta di daftar statis.

## 5b · Susunan halaman

Biji **kiri**, teks **kanan** (revisi 5 Nov 2026). Motto "Terjaga untuk / rasa yang sesungguhnya."
jadi `h1`; headline lama turun jadi baris pendukung.

| Hal | Aturan |
| --- | --- |
| Grid | `0,86fr / 1,14fr`, jarak `clamp(26px, 4vw, 62px)`, hanya ≥900 px |
| Biji | maks 440 px, `justify-self: start` |
| Motto | `clamp(1,7rem, 3,2vw, 3,1rem)`, baris 2 Fraunces 300 italic |
| Mobile | satu kolom, teks dulu, motto `clamp(1,6rem, 7,2vw, 2,6rem)` |
| Sumber teks | `data/catalog.json#brand.motto` — jangan menulis motto langsung di HTML |

Ukuran motto tidak boleh dinaikkan tanpa mengukur: `periksa.py` menghitung lebar baris dengan
metrik font asli dan menolak kalau melewati 96% kolom.

## 6 · Interaksi

| Aksi | Perilaku |
| --- | --- |
| Geser (sentuh/tikus) | memutar biji, batas pitch ±22° |
| Tombol panah saat fokus | memutar 0,16 rad per tekan; `Home` kembali ke sudut awal |
| Ketuk titik | membuka panel: judul zona, ringkasan, daftar senyawa |
| Ketuk lagi / `Esc` / tombol × | menutup panel |
| Diam 1,6 detik | biji berputar sendiri 4,5°/detik (berhenti saat disentuh) |
| `prefers-reduced-motion` | tidak berputar sendiri, tidak mengambang, tanpa transisi |
| Tanpa WebGL | poster PNG tetap tampil; titik disembunyikan; senyawa tetap terbaca lewat `<details>` |
| Tanpa JavaScript | poster + `<details>` berisi enam zona tetap terbaca |

## 7 · Cara memverifikasi (tanpa browser)

```bash
python3 tools/biji.py --cek              # data: zona, senyawa, sumber, token warna
python3 tools/biji.py                    # render poster CPU + laporan/biji-3d.json
node tools/verifikasi-biji.mjs           # 8 butir: JS=Python, mesh, HTML, poster
python3 tools/periksa.py                 # cek "Biji 3D"
```

Butir terpenting: **posisi titik hasil matematika JS dibandingkan dengan hasil render Python**.
Selisih maksimum sekarang **0,005%**. Kalau seseorang mengubah rumus di satu sisi saja, angka itu
melonjak dan gerbang menolak.

Uji interaksi (butuh jsdom, tidak ikut repo): memasang skrip ke DOM tiruan dengan
`getContext('webgl') → null`, lalu mengetuk keenam titik. Hasil terakhir: **11 lolos · 0 gagal**.

## 8 · Batas yang tidak ditutupi

1. **WebGL belum pernah dirender di sandbox ini.** Chrome tidak bisa jalan (`libnspr4`). Yang terbukti:
   matematika, struktur DOM, jalur poster, dan kesesuaian JS↔Python. Bukan gambar GPU.
2. **Bentuk bukan hasil pindai.** Tidak ada model 3D biji Nocturne; ini model parametrik.
3. **Rentang senyawa bukan hasil lab Nocturne.** Literatur, dengan sumber tertulis.
4. **Agtron 55–60 adalah perkiraan visual**, bukan pengukuran. Sudah ditulis begitu di data.
