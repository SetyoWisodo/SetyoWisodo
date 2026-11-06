# novel_en — "Before the Light Arrives" / "Sebelum Cahaya Sampai"

Volume I dari rencana 100 bab. Naskah bahasa Inggris (Wattpad + Fizzo), fiksi ilmiah nyata
dibalut romance, 1.500–2.500 kata per bab.

## Berkas yang dibaca manusia

| Berkas | Isi |
|---|---|
| `SKRIP_FINAL.md` | **naskah lengkap hasil rakitan**: halaman judul, daftar isi, pembatas arc, seluruh bab |
| `SKRIP_FINAL.txt` | versi teks polos untuk unggah (Wattpad/Fizzo); pemisah scene menjadi `* * *` |
| `vol1/ch_XXX.md` | sumber naskah per bab (satu-satunya tempat menyunting kalimat) |
| `bible/struktur_100.py` | sumber kebenaran 100 bab: judul, POV, tanggal, beat, hook, tanam/bayar, sains, cast |
| `bible/FILM_GRAMMAR.md` | 12 templat adegan G-01…G-12 hasil kajian Interstellar, Inception, The Matrix, Ant-Man, Arrival + aturan romance |
| `bible/adegan.json` | peta 100 bab → templat, lensa, cahaya, warna |
| `bible/ADEGAN.md` | papan visual per bab: templat, shot, aksen tiap scene |
| `bible/STORYBOARD.md` | ukuran struktural per bab: kata, scene, rasio dialog, panjang kalimat, templat |
| `bible/tokoh.json`, `world.json`, `sains.json`, `petunjuk.json`, `twist.json`, `kontinuitas.json` | kanon: tokoh, dunia, 9 kartu sains ber-DOI, 26 petunjuk, 6 twist, 12 jangkar kontinuitas |
| `bible/KERANGKA_PER_BAB.md` | kerangka bab yang belum ditulis |
| `research/kutipan.json` | kartu sitasi (klaim, batas klaim, DOI) |

## Urutan menjalankan alat

```bash
python3 novel_en/tools/build_adegan.py      # (opsional) bangun ulang peta templat
python3 novel_en/tools/audit_webnovel.py    # gerbang mutu: wajib FAIL 0
python3 novel_en/tools/cek_kontinuitas.py   # jangkar kanon: wajib gagal 0
python3 novel_en/tools/make_storyboard.py   # perbarui STORYBOARD.md
python3 novel_en/tools/make_adegan.py       # perbarui ADEGAN.md
python3 novel_en/tools/build_skrip.py       # rakit SKRIP_FINAL.md + .txt
```

`build_skrip.py --cek` memeriksa tanpa menulis (panjang bab, sisa `*Next:*`, kata terlarang).

## Aturan naskah (gerbang audit)

- 1.500–2.500 kata/bab, 3–6 scene, dialog 20–60%, rata-rata kalimat 8–17 kata.
- Tiap bab wajib memperlihatkan templatnya: minimal 2 istilah khas dari `adegan.json`.
- Sains yang dipakai harus punya kartu ber-DOI di `sains.json` + `research/kutipan.json`.
- Tanggal bab harus berurutan; ejaan nama tokoh mengikuti `tokoh.json`; tanpa paragraf kembar.
- Tipografi: tanda kutip/apostrof lengkung — jalankan `fix_typography.py` setelah menulis bab.
