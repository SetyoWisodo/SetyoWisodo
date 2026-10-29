# Detail 8 fase

Format tiap fase: **Masuk** (syarat) → **Lakukan** → **Keluaran** → **Gate** →
**Salah umum**. Gate yang gagal harus diperbaiki, bukan dilewati.

---

## F0 — Intake & scope

**Masuk:** user menyebut sesuatu yang ingin diketahui/dikerjakan.

**Lakukan:**

1. Tulis pertanyaannya dalam satu kalimat yang bisa dijawab. Buruk: "jelaskan app
   ini". Baik: "kenapa tombol % setelah + menghasilkan 220 untuk 200 + 10%?".
2. Tetapkan target konkret: path file, URL halaman, nama paket, atau "belum ada"
   (kalau belum ada, sesi berhenti di sini dan menjadi permintaan artefak).
3. Tetapkan batas izin: boleh dijalankan? boleh ditulis? boleh di-install?
4. Tentukan keluaran yang diminta: penjelasan, potongan kode, perbandingan versi,
   rekonstruksi, atau laporan.

**Keluaran:** blok intake (pertanyaan, target, batas, keluaran) + `session.sh init`.

**Gate F0:** pertanyaan bisa dijawab ya/tidak/tidak diketahui; target menunjuk satu
artefak (bukan "app saya"); batas izin eksplisit.

**Salah umum:** menerima target ambigu lalu mencari-cari sendiri dan memilih
artefak yang salah. Kalau ambigu → tanya.

---

## F1 — Environment

**Masuk:** F0 lulus.

**Lakukan:**

```bash
bash .agents/skills/rea-roadmap/scripts/check_readiness.sh <target>
```

Catat: versi Node, ada/tidak CLI `rea`, state `~/.rea`, engine (Ghidra/JADX/
Java/Frida/tshark), `sha256` target, `file(1)` target.

Lalu jawab satu pertanyaan: **tool apa yang dibutuhkan pertanyaan F0, dan apakah
tersedia?** Kalau tidak tersedia, tulis konsekuensinya (mis. "tanpa decompiler,
klaim dibatasi pada string/simbol/struktur").

**Keluaran:** tabel kesiapan + daftar tool yang akan dipakai + konsekuensi.

**Gate F1:** setiap tool yang disebut di F2 ada, atau klaim diturunkan secara
eksplisit. Jangan lanjut dengan rencana memakai tool yang tidak ada.

**Salah umum:** menjalankan `npx rea-agents@latest setup` tanpa izin; menganggap
skill terpasang = MCP aktif.

---

## F2 — Route

**Masuk:** F1 lulus.

**Lakukan:** klasifikasikan target dengan tabel di
[`target-routing.md`](target-routing.md). Tulis: rute terpilih, alasan, dan satu
alternatif yang ditolak beserta alasannya.

Contoh: "APK → `inspect_android_package` dulu (butuh engine Android); alternatif
`open_binary`+inventory ditolak karena yang ditanya kode Java, bukan isi arsip."

**Keluaran:** satu baris rute + alasan + alternatif ditolak.

**Gate F2:** rute ada di tabel; kalau tidak ada, tulis sebagai kasus baru dan
sebutkan rujukan yang dipakai (`reverse-engineer-anything/SKILL.md`).

**Salah umum:** langsung `open_binary` untuk semua hal; mencampur pertanyaan
runtime dengan pertanyaan statis.

---

## F3 — Evidence

**Masuk:** F2 lulus.

**Lakukan:**

1. Panggil tool rute dengan `detail: "summary"` bila tersedia.
2. Catat identitas hasil: `evidence_id`, path, digest, alamat/byte range.
3. Paging hanya bagian yang menjawab pertanyaan (`inspect_analysis_view`).
4. Untuk target tanpa API/SDK resmi, jalankan
   `find-reverse-engineered` (`scripts/re_index.py search …`) dan catat kandidat
   + lisensi + aktivitas repo.
5. Catat langkah di `session.sh log`.

**Keluaran:** daftar Evidence bernomor (E1, E2, …) dengan sumber dan arti.

**Gate F3:** tiap butir E punya tool + sumber; tidak ada butir tanpa sumber.
Kalau Evidence tidak lengkap, tulis batasnya sekarang (bukan nanti).

**Salah umum:** menyalin keluaran besar tanpa menyaring; mengulang call yang
sama; melaporkan kesimpulan tanpa mencatat alamat/path.

---

## F4 — Interpretasi

**Masuk:** minimal satu Evidence relevan.

**Lakukan:** pisahkan tegas:

- **Fakta** — apa yang tertulis di Evidence (instruksi, konstanta, nama fungsi,
  field, endpoint).
- **Inferensi** — makna yang kamu simpulkan; sebut Evidence penopangnya.
- **Tidak diketahui** — yang tidak bisa disimpulkan dari Evidence yang ada.

**Keluaran:** tiga daftar itu.

**Gate F4:** tidak ada inferensi tanpa rujukan E; tidak ada fakta yang sebenarnya
inferensi (cek kata "berarti", "mungkin", "pasti").

**Salah umum:** menyebut perilaku runtime dari kode statis; menggeneralisasi satu
cabang ke semua input.

---

## F5 — Verifikasi

**Masuk:** F4 lulus.

**Lakukan:** pilih satu metode silang yang proporsional:

- jalur kedua: string/xref vs pseudocode;
- target kedua: versi lain dari artefak yang sama;
- sumber ketiga: dokumentasi resmi/changelog (hanya untuk konteks, bukan bukti
  perilaku);
- hitung manual: konstanta dan aritmetika diuji dengan contoh angka.

**Keluaran:** hasil uji silang: cocok / tidak cocok / tidak bisa diuji (+ alasan).

**Gate F5:** klaim utama punya status verifikasi eksplisit.

**Salah umum:** "verifikasi" dengan mengulang tool yang sama; menganggap
dokumentasi vendor membuktikan isi binary.

---

## F6 — Deliverable

**Masuk:** F5 selesai (atau dinyatakan tidak bisa diuji).

**Lakukan:** susun jawaban dengan format empat bagian di `SKILL.md`
(Jawaban / Bukti / Fakta vs inferensi / Belum diketahui). Sesuaikan bentuk dengan
permintaan: penjelasan, potongan kode rekonstruksi, tabel perbandingan, atau
ringkasan.

Kalau deliverable-nya tool → pindah ke `rea-tool-design`. Kalau release notes →
`rea-changelog-update`.

**Keluaran:** jawaban final.

**Gate F6:** setiap klaim di "Jawaban" punya penopang di "Bukti"; scope tidak
bertambah dari F0.

---

## F7 — Catat & tutup

**Masuk:** F6 selesai.

**Lakukan:**

1. Daftar `unknown` (yang tersisa) + apa yang dibutuhkan untuk menutupnya.
2. Satu aksi berikutnya yang konkret.
3. `session.sh report` → simpan/ tempel ringkasan.
4. Kalau sesi ini menyelesaikan satu tahap roadmap, tandai lulusnya kriteria
   keluar di `rea-roadmap/references/learning-path.md` dan sebut tahap berikutnya.

**Keluaran:** ringkasan sesi + next step.

**Gate F7:** minimal satu `unknown` tercatat, atau pernyataan eksplisit "tidak ada
unknown karena …".

**Salah umum:** menutup sesi tanpa menyimpan Evidence; melupakan batas yang
dipakai (versi, digest) sehingga hasil tidak bisa direproduksi.
