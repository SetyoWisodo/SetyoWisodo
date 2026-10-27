# Alat Pemeriksa Kemiripan

Satu perintah, tiga lapis pemeriksaan.

```
python tools/plagiarism/check.py
```

Keluaran: skor kemiripan internal, laporan duplikasi kalimat, dan daftar kalimat
untuk diuji ke web.

---

## Kenapa tidak memakai alat yang sudah ada

Sudah dicoba, dan hasilnya dicatat di sini supaya tidak diulang:

| Alat | Hasil |
|---|---|
| `blingenf/copydetect` (328★, algoritma winnowing) | **gagal pada prosa.** Tokenizer Pygments menggabungkan seluruh berkas teks menjadi satu token; sidik jarinya degenerasi, 0 pasangan cocok. Alat ini untuk kode sumber. |
| `Kalebu/Plagiarism-checker-Python` (329★) | hanya cosine similarity antar-dokumen; tidak ada korpus luar |
| `Copyleaks/Python-Plagiarism-Checker` | SDK resmi, tetapi butuh kunci API berbayar |
| `Ganesh-403/semantic-plagiarism-detector` (16★) | mendeteksi parafrase antar-dokumen, bukan kemiripan dengan web |

Kesimpulannya: **tidak ada alat open-source yang bisa menghasilkan skor Turnitin**,
karena skornya bergantung sepenuhnya pada korpus berlangganan. Yang bisa dilakukan
adalah mengukur apa yang terukur, dan menyebut korpusnya.

---

## Lapis 1 — kemiripan internal (`winnow.py`)

Implementasi **winnowing** dari Schleimer, Wilkerson & Aiken (2003), *"Winnowing:
Local Algorithms for Document Fingerprinting"*, SIGMOD — algoritma yang sama dipakai
MOSS, dan menjadi dasar sidik jari dokumen pada Turnitin.

| Parameter | Nilai | Alasan |
|---|---|---|
| k-gram | **8 kata** | di bawah 8 kata, dua kalimat bisa cocok hanya karena frasa baku |
| jendela winnowing | 4 | standar pada makalah aslinya |
| hash | FNV-1a 64-bit | deterministik, tanpa dependensi |
| skor | cakupan kata | meniru cara Turnitin menghitung persentase teks yang cocok |

Skor = fraksi kata dalam dokumen yang tercakup k-gram yang juga muncul di dokumen
lain. Bukan jumlah fingerprint, karena satu paragraf panjang bisa menghasilkan
banyak fingerprint meski hanya cocok di satu tempat.

### Validasi wajib

Skor rendah tanpa kontrol positif tidak membuktikan apa pun — bisa saja alatnya
rusak. `check.py` karena itu selalu diuji dengan dua kontrol:

```python
# kontrol positif: salin satu paragraf ke berkas baru
#   -> 98,17% terdeteksi terhadap berkas asalnya
# kontrol negatif: teks karangan yang tidak berkaitan
#   -> 0%, di bawah ambang
```

Kalau kontrol positif gagal, skor internal tidak boleh dipercaya.

---

## Lapis 2 — duplikasi kalimat (`audit_plagiarism.py`)

Di akar repo. Memeriksa:

1. kalimat yang berulang **persis**,
2. pasangan kalimat yang **nyaris sama** (Jaccard ≥ 0,62 pada 4-shingle kata),
3. teks dalam **tanda kutip** yang tidak punya rujukan di sekitarnya,
4. paragraf panjang berangka tanpa sitasi.

Ambang 0,62 dipilih setelah diuji: 0,82 memberi negatif palsu — dua kalimat yang
hanya berbeda satu kata hanya mencapai Jaccard 0,714, sehingga luput terdeteksi.

---

## Lapis 3 — uji ke web

Tidak bisa diotomatiskan tanpa kunci API mesin pencari. `check.py` menyiapkan
kalimatnya (satu per bab, dipilih yang paling khas), lalu hasilnya dicatat di
`PHRASE_TESTS.md`.

Yang **perlu dicurigai**: hasil dengan 8 kata atau lebih berturut-turut sama persis
tanpa tanda kutip atau sitasi.

Yang **tidak perlu dicurigai**: artikel bertopik sama, angka sama, atau frasa teknis
baku yang sama (*"five consecutive failed rainy seasons"*).

---

## Hasil terakhir

| | Inggris | Indonesia |
|---|---|---|
| Kalimat diperiksa | 7.355 | 7.033 |
| Kemiripan internal | **0,41%** | — |
| Berulang persis | 2 | 4 |
| Nyaris sama | 7 | 2 |
| Teks dalam tanda kutip ≥ 40 huruf | **0** | **0** |
| Uji frasa ke web | **0 dari 12 cocok** | — |

Laporan lengkap: `PLAGIASI.md` di akar repo.
