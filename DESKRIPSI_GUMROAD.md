# Mengisi Kotak Description di Gumroad

Kotak **Description** hanya menerima teks. Berkas buku diunggah di tab **Content**, bukan di sini.

---

## Kalau teks yang ditempel jadi satu blok panjang (gejala yang Anda alami)

Itu terjadi karena teks disalin **sebagai teks polos**: semua pemisah baris dibuang oleh editor Gumroad, sehingga 20 paragraf melebur jadi satu. Obatnya: salin **versi berformat (HTML)**, bukan teks polos.

### Langkah perbaikan, dari keadaan sekarang

1. Klik di dalam kotak **Description** → **Ctrl+A** (semua teks tersorot) → **Delete** (kotak kosong).
2. Buka **`/copy/en`** di panel *Live Preview* Arena. Halaman itu berisi teks yang sama, sudah berformat.
3. Di halaman itu: **Ctrl+A**, lalu **Ctrl+C**.
4. Klik kotak **Description** lagi, lalu **Ctrl+V**.
5. **Save and continue**.

Hasil yang benar: tiap bagian punya jarak, judul bagian tampil tebal, dan tiap poin ada di barisnya sendiri.

> Catatan: halaman `/copy/en` sengaja **tanpa** judul besar dan tanpa kotak petunjuk, jadi Ctrl+A hanya menyalin isi yang memang dibutuhkan.

### Kalau cara itu masih menghasilkan satu blok

Berarti editor Anda membuang format HTML juga. Jangan berkelahi dengan editor: pakai **deskripsi ringkas** di bawah. Teks ini tetap enak dibaca walaupun melebur jadi satu paragraf.

```
Surviving the Future: Crisis, Climate, and Human Resilience.

Across 24 chapters and 457 pages, this book follows heat, flood, drought, fire, food, water, migration and conflict, and asks one question each time: what decides whether the same shock kills or spares a community? Every chapter ends by naming the observation that would prove it wrong.

Inside: 25 data tables, 11 figures, 152 cited sources and 24 case studies, each traceable to a named source. Four files in one purchase — PDF (bookmarked), EPUB, DOCX, and a figure pack at 300 dpi cleared for use in your own slides. Free lifetime updates to this edition.

Published 2026, Setyo Wisodo.
```

Tiga paragraf itu, walaupun melebur, tetap terbaca sebagai satu paragraf pendek yang wajar. Deskripsi panjang boleh dipakai nanti setelah Anda sempat menambahkan pemisah baris secara manual.

---

## Setelah berhasil: rapikan judul bagian (opsional)

Kalau ingin judul bagian tampil tebal, letakkan kursor di barisnya lalu pilih **Text → Heading 2**:

`WHAT MAKES IT DIFFERENT` · `WHAT YOU GET` · `WHO IT IS FOR` · `WHY $45` · `LICENCE`

Baris poin tidak perlu diapa-apakan. Jangan pakai Heading 1 — judul produk sudah tampil di atas halaman.

---

## Teks untuk tiga produk lainnya

| Produk | Buka | Catatan |
|---|---|---|
| Free sample (EN) | `/copy/sample` | — |
| Bertahan Hidup di Masa Depan (ID) | `/copy/id` | 473 halaman, 152 sumber |
| Bundle EN + ID | `/copy/bundle` | 457 + 473 halaman |

**Ganti setelah sampel terbit:** di deskripsi EN dan ID ada baris rujukan ke sampel. Ganti dengan URL produk sampel Anda, mis. `setyowisodo.gumroad.com/l/surviving-the-future-sample`.

---

## Dua hal lain yang terlihat di layar Anda

| Yang terlihat | Seharusnya |
|---|---|
| URL: `surviving-thefuture` (tanpa tanda hubung) | `surviving-the-future` |
| Deskripsi masih satu blok | ulangi Langkah 1–5 di atas |

Tanda hubung itu penting: alamat yang Anda sebar ke orang lain harus bisa dibaca dan diingat.
