# Hero biji kopi 3D — laporan

Diperbarui 5 November 2026 · sumber: `data/biji3d.json`, `assets/js/biji3d.js`,
`tools/biji.py`, `laporan/biji-3d.json`, `laporan/biji-verifikasi.json`.

Permintaannya: **tampilan awal situs = satu biji kopi Arabika 3D yang sangat detail, roasted
beans cokelat khas medium roast; kalau bagian biji disentuh, muncul senyawa mikro di dalamnya.**
Referensi bentuk diambil dari tag 3D motionsite.ai dan header 3D jiro.build.

## 1 · Yang jadi

| Bagian | Berkas | Angka |
| --- | --- | --- |
| Data bentuk, warna, zona, senyawa | `data/biji3d.json` | 6 zona · 12 senyawa · 4 sumber literatur |
| Renderer WebGL (tanpa pustaka) | `assets/js/biji3d.js` | ±18 KB · WebGL 1 · 2 shader |
| Poster CPU (gambar awal & cadangan) | `assets/img/biji-3d-poster.png` | 640×800 RGBA · 104 KB |
| Gaya | `assets/css/biji.css` | token brand, tanpa hex baru |
| Hero | `index.html` | poster → kanvas → 6 titik → panel senyawa |
| Renderer poster | `tools/biji.py` | 359.400 segitiga · 20 detik |
| Verifikasi tanpa GPU | `tools/verifikasi-biji.mjs` | **9 lolos · 0 gagal** |
| Prompt untuk agen lain | `prompts/pustaka.json#hero-biji-3d` | 2.607 karakter |

## 2 · Bentuk: kopi, bukan bola cokelat

Enam langkah deformasi, semuanya angka di JSON, tidak ada yang ditulis di kode:

| Langkah | Angka | Efek |
| --- | --- | --- |
| Elipsoid | `a 1,00 · b 0,62 · c 0,46` | pipih, memanjang — proporsi biji kopi |
| Ujung meruncing | `×(1 − 0,16·(|x|/a)³)` | dua ujung tidak membulat sempurna |
| Sisi datar | `z × 0,72…1` di +Z | kopi punya satu muka hampir rata |
| Dua belahan | `+0,2c·cos(...)` | tonjolan di kiri-kanan alur |
| Alur S | `0,52·exp(−Δθ²/2·0,115²)` | alur tengah yang melengkung, bukan garis lurus |
| Pitting | sinus `0,0045` | permukaan tidak plastik saat kena kilau |

Alur dihitung dari **sudut azimut**, bukan dari koordinat z. Percobaan pertama memakai z dan
hasilnya alur menghilang saat sisi datar diratakan — kesalahan itu yang membuat poster pertama
tampak seperti bola.

## 2b · Susunan beranda (5 Nov 2026, revisi)

Permintaan pemilik: **biji 3D di kiri layar, motto Nocturne di kanan.**

| Kolom | Isi |
| --- | --- |
| kiri (0,86 fr) | bingkai 4:5 berisi biji 3D + 6 titik senyawa, lebar maks 440 px |
| kanan (1,14 fr) | label mikro · motto · baris pendukung · paragraf · petunjuk sentuh |

- **Motto:** "Terjaga untuk / rasa yang sesungguhnya." Baris 1 Bricolage Grotesque 800,
  baris 2 Fraunces 300 italic `--espresso`. Disimpan di `data/catalog.json#brand.motto`,
  jadi bukan teks liar di HTML.
- **Baris pendukung:** "Kopi dari petani. Diseduh untukmu." (headline brand lama, tetap ada
  sebagai kalimat kedua, Fraunces italic `--ink-55`).
- **DOM tetap teks-dulu, tampilan dibalik lewat CSS Grid** (`grid-column: 1` untuk biji,
  `grid-column: 2` untuk teks) supaya `h1` tidak tenggelam di urutan dokumen.
- **Ukuran motto dihitung, bukan ditebak.** `periksa.py` membaca `clamp()` dan fraksi kolom
  langsung dari `assets/css/biji.css`, lalu mengukur lebar baris dengan metrik font asli
  (Bricolage 800 & Fraunces 300) pada 360–1920 px. Uji negatif sudah dilakukan: menaikkan
  `clamp` ke 4,4rem membuat gerbang gagal ("motto meluap di 900px").
- Di bawah 900 px: satu kolom, teks dulu lalu biji; motto `clamp(1,6rem, 7,2vw, 2,6rem)`.

**Pratinjau:** `python3 tools/pratinjau.py` → `laporan/pratinjau-hero.png`
(skema 1280 px + 390 px). Skrip ini membaca angka dari CSS dan memakai font asli, jadi
posisi kiri/kanan serta lebar baris bisa dilihat. Ini **skema, bukan tangkapan layar
peramban** — Chromium tidak bisa dipasang di sandbox (libnspr4 hilang), dan gambar itu
menuliskan batas tersebut di dalam dirinya sendiri.

## 3 · Warna medium roast — hanya dari token

| Peran | Token | Hex |
| --- | --- | --- |
| bayangan, tepi bawah | `--g4b` | `#3A2013` |
| badan | `--g2b` | `#7A4A1E` |
| bagian atas kena panas | `--g4a` | `#B4703A` |
| kilau minyak | `--gold` | `#D9A441` |
| titik zona inti | `--g3a` | `#93381F` |

Tidak ada hex baru di CSS, JS, maupun Python — `verifikasi-biji.mjs` menghitung nol hex di kedua
berkas kode, dan `periksa.py` menolak warna di luar `boleh_dipakai`.

## 4 · Senyawa yang muncul saat disentuh

| # | Zona | Senyawa (rumus) | Angka yang tampil |
| ---: | --- | --- | --- |
| 01 | Cekungan tengah | Sukrosa sisa, 5-HMF | sisa <4% pada medium · HMF terukur |
| 02 | Kulit sangrai | Melanoidin, pirazin & furanon | terbentuk sejak ±150 °C |
| 03 | Inti biji | **Kafein**, **Trigonelin** | 0,9–1,3% · 0,87–0,90% → −50% |
| 04 | Bintik minyak | Lipid, diterpen (kafestol/kahweol) | ±15–16% massa |
| 05 | Ujung biji | Asam nikotinat, trigonelin sisa | 7,20–12,95 mg/g |
| 06 | Daging & serat | **Klorogenat (5-CQA)**, asam kuiniat & asetat | 4,38–4,66% → −65% |

Setiap butir membawa **rumus, rentang, peran, sumber (S1–S4), dan tanda keyakinan** (`kuat` =
terukur di literatur, `umum` = rentang buku teks). Sumber lengkap dengan DOI ada di
`data/biji3d.json#sumber_angka`.

Kalimat yang wajib tampil, dan memang tampil di panel serta daftar statis:

> Rentang senyawa = literatur Arabika medium roast, bukan hasil lab biji Nocturne.
> Bentuk biji = model 3D, bukan hasil pindai.

## 5 · Interaksi

| Aksi | Hasil |
| --- | --- |
| Geser / usap | memutar biji (pitch dibatasi ±22°) |
| Panah ← ↑ → ↓ saat fokus | memutar per 0,16 rad; `Home` kembali ke sudut awal |
| Ketuk titik | panel senyawa terbuka: zona, ringkasan, 2 senyawa |
| Ketuk lagi / × / `Esc` | panel tertutup |
| Diam 1,6 s | berputar sendiri 4,5°/detik, berhenti begitu disentuh |
| `prefers-reduced-motion` | tanpa putar otomatis, tanpa mengambang, tanpa transisi |
| Tanpa WebGL | poster tetap tampil; titik disembunyikan; `<details>` berisi 6 zona |
| Tanpa JavaScript | poster + `<details>` tetap terbaca |

## 6 · Kenapa tanpa three.js

Jalur motionsite.ai (`Interactive 3D Hero` versi Cripton) memakai React Three Fiber + Framer Motion.
Diukur untuk kebutuhan ini: three.js + R3F ±600 KB, dan **tidak satu baris pun bisa diuji di sandbox
ini** karena tidak ada browser. WebGL mentah ±18 KB dan seluruh matematikanya bisa dijalankan di Node.

Konsekuensinya: tidak ada model `.glb`, tidak ada tekstur PBR, tidak ada environment map. Sebagai
gantinya bentuknya rumus — dan justru itu yang membuat poster PNG dan render WebGL bisa dibuktikan
memakai geometri yang sama.

## 7 · Bukti: tiga lapis, dan apa yang tidak terbukti

| Lapis | Alat | Hasil |
| --- | --- | --- |
| Data & poster (CPU) | `python3 tools/biji.py` | 359.400 segitiga · 6/6 titik tampak · 0 masalah |
| Matematika & berkas (Node) | `node tools/verifikasi-biji.mjs` | **9 lolos** · selisih posisi JS↔Python **0,005%** |
| Gerbang konsistensi | `python3 tools/periksa.py` | **24 lolos · 0 peringatan · 0 gagal** |
| Interaksi (jsdom, di luar repo) | skrip uji sementara | **11 lolos** — panel, aria-pressed, Esc, 6 zona |

**Yang tidak terbukti:** render WebGL di layar. Chrome tidak bisa dijalankan di sandbox ini
(`libnspr4.so` tidak ada, unduhan Chrome diblokir). Jadi jangan menulis "sudah diuji di browser"
di materi mana pun. Yang bisa dikatakan: matematika, struktur, jalur poster, dan perilaku interaksi
sudah diuji; gambar GPU menunggu mesin yang punya browser.

## 8 · Perintah

```bash
python3 tools/biji.py --cek      # validasi data (0,1 detik)
python3 tools/biji.py            # render poster 640×800 RGBA + laporan/biji-3d.json
node tools/verifikasi-biji.mjs   # 9 butir, menulis laporan/biji-verifikasi.json (ber-sidik)
python3 tools/periksa.py         # cek "Biji 3D"
```

`periksa.py` juga menolak laporan verifikasi yang **basi**: sidik sha256 dari `data/biji3d.json`
+ `assets/js/biji3d.js` harus cocok. Kalau salah satu diubah tanpa menjalankan ulang verifikasi,
gerbang gagal.
