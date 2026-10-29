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

**Prompt REA terpandu** (dari `docs/mcp-prompts.md`) — pakai ini kalau MCP aktif:

| Prompt | Dipakai saat |
| --- | --- |
| `investigate_feature` | pertanyaan "bagaimana fitur X bekerja" |
| `compare_application_versions` | pertanyaan "apa yang berubah antara versi A dan B" |
| `trace_crash` | ada gejala crash yang harus dihubungkan ke jalur kode |
| `prepare_bounded_process_capture` | butuh eksperimen runtime; rancang dulu, eksekusi belakangan (izin) |

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

**Oracle untuk mode rebuild.** Kalau deliverable-nya rekonstruksi, F5 wajib punya
minimal satu oracle konkret:

| Oracle | Cara | Batas |
| --- | --- | --- |
| Uji hitung manual | hitung ulang konstanta/aritmetika dengan contoh angka dari Evidence | tidak menangkap efek samping |
| `verify_reconstruction` | uji spesifikasi terhadap Evidence pembanding yang tersimpan | butuh MCP + dua artefak |
| Perilaku nyata (dengan izin) | jalankan target dan pembanding pada input yang sama | butuh izin eksekusi; bedakan lingkungan |
| Diff biner | bandingkan build sendiri vs asli pada bagian kritis | hanya menunjukkan perbedaan, bukan kesetaraan |

Tanpa salah satu di atas, rekonstruksi disebut **draft**, bukan hasil.

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

**Mode rebuild (clean-room).** Kalau permintaannya "bangun ulang fitur ini",
keluarannya adalah `SPEC.md` + implementasi, dengan urutan dari postingan
toolchain: `binary → REA → SPEC.md → rebuild → oracle → retry`.

Isi minimum `SPEC.md`: perilaku yang dibuktikan (dengan E-id), input/output,
konstanta, kondisi batas, yang **tidak** direkonstruksi, dan oracle yang akan
dipakai untuk menguji. Template: [`../templates/spec.md`](../templates/spec.md).

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
4. Kalau ada iterasi rebuild: selisih antara build sendiri dan target dicatat
   sebagai `unknown` baru, lalu F3 diulang **hanya untuk selisih itu** (bukan
   mengulang seluruh investigasi).
5. Kalau sesi ini menyelesaikan satu tahap roadmap, tandai lulusnya kriteria
   keluar di `rea-roadmap/references/learning-path.md` dan sebut tahap berikutnya.

**Keluaran:** ringkasan sesi + next step.

**Gate F7:** minimal satu `unknown` tercatat, atau pernyataan eksplisit "tidak ada
unknown karena …".

**Salah umum:** menutup sesi tanpa menyimpan Evidence; melupakan batas yang
dipakai (versi, digest) sehingga hasil tidak bisa direproduksi.
