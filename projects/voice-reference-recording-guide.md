<div align="center">

# 🎤 Panduan Rekam Reference Voice — `VOICE-ID-v1`

### **Suara pemilik akun → narator brand hangat dan mudah dipahami**

*Status: persiapan rekaman lokal. Tidak ada upload, cloning, atau audio generation yang diizinkan pada tahap ini.*

</div>

---

## Jawaban singkat: rekam di mana dan upload ke mana?

| Pertanyaan | Jawaban |
|---|---|
| **Rekam di mana?** | Di ruangan tenang menggunakan ponsel, mikrofon USB, atau laptop yang mic-nya cukup bersih. Ponsel boleh dipakai bila tidak ada mic eksternal. |
| **Simpan di mana sekarang?** | Folder **privat di perangkat Anda**, misalnya `Documents/VOICE-ID-v1-reference/`. Backup terenkripsi/pribadi boleh setelah itu. |
| **Upload ke mana sekarang?** | **Jangan upload ke mana pun dulu.** Jangan ke GitHub/repository ini, chat, WhatsApp, Google Drive publik, atau link publik. |
| **Upload ke mana nanti?** | Hanya setelah engine/model mendapat clearance dan Anda menyetujui download: import file dari perangkat Anda langsung ke VoiceStudio lokal pada mesin yang disetujui. |
| **Apakah audio dikirim ke sandbox ini?** | **Tidak.** Sandbox ini bukan mesin produksi suara dan tidak memiliki model yang telah disetujui. |

Reference voice adalah data biometrik pribadi. Perlakukan seperti dokumen pribadi: simpan privat, batasi akses, dan jangan taruh dalam Git.

---

## 1. Persiapan sederhana

### Peralatan

Urutan pilihan dari paling ideal:

1. Mikrofon USB atau lavalier kabel + laptop/ponsel.
2. Ponsel dengan aplikasi perekam bawaan.
3. Mikrofon laptop, hanya jika ruangan benar-benar tenang.

Tidak perlu membeli alat terlebih dahulu. Rekaman ponsel yang dekat, stabil, dan bersih lebih baik daripada mikrofon mahal di ruangan bergema.

### Ruangan dan posisi

- Pilih ruangan paling tenang; tutup jendela/pintu dan matikan kipas, AC berisik, TV, musik, atau notifikasi.
- Rekam saat tidak ada orang lain berbicara di sekitar Anda.
- Posisikan mikrofon sekitar **15–20 cm** dari mulut, sedikit menyamping agar bunyi huruf “p”, “b”, dan napas tidak meledak.
- Duduk/berdiri tegak dan nyaman. Gunakan volume bicara normal, jangan berbisik atau berteriak.
- Beri hening sekitar satu detik di awal dan akhir setiap file.

### Pengaturan file

| Pengaturan | Pilihan |
|---|---|
| Format utama | **WAV PCM mono** bila aplikasi memungkinkan |
| Sample rate | **48 kHz** dianjurkan; 44,1 kHz juga dapat diterima |
| Bit depth | 24-bit bila tersedia; 16-bit dapat diterima |
| Efek audio | **Matikan** reverb, musik, auto-tune, voice changer, enhancement agresif, dan filter AI |
| Jika ponsel hanya membuat M4A | Simpan file asli M4A; jangan kompres ulang lewat WhatsApp. Konversi ke WAV hanya pada tahap yang disetujui nanti. |

Jangan gunakan rekaman telepon, voice note WhatsApp/Telegram, podcast lama, video YouTube, atau audio dengan musik sebagai reference.

---

## 2. Cara membaca untuk karakter yang dipilih

Karakter `VOICE-ID-v1` yang direncanakan:

> **Narator brand yang berbeda, hangat, jelas, mudah dipahami, dan tidak menggurui.**

Cara membacanya:

- Bayangkan Anda menjelaskan konsep menarik kepada satu teman yang ingin belajar.
- Beri jeda kecil pada koma dan akhir kalimat.
- Tekankan kata kunci secara ringan, bukan seperti iklan atau trailer dramatis.
- Tetap natural; jangan mencoba meniru suara orang lain.
- Bila salah satu kata, berhenti dua detik lalu ulangi **seluruh kalimat**. Jangan mengedit potongan sendiri.

Rekam setiap kalimat dua kali. Pilih satu take terbaik yang paling bersih dan natural; simpan take lain sebagai cadangan lokal.

---

## 3. Naskah rekaman

Bacalah lima teks berikut. Masing-masing umumnya berdurasi sekitar 8–15 detik pada tempo edukatif normal.

### File 1 — Nada netral

**Nama file:** `voice-neutral-01.wav`

> “Di kanal ini, kita membahas sains kesehatan dengan bahasa sederhana, sumber yang jelas, dan tanpa membuat diagnosis untuk siapa pun.”

### File 2 — Anatomi dan artikulasi

**Nama file:** `voice-anatomy-02.wav`

> “Udara yang kita hirup bergerak melalui saluran napas sampai ke alveoli, kantung kecil di paru-paru tempat pertukaran oksigen dan karbon dioksida berlangsung.”

### File 3 — Bukti ilmiah

**Nama file:** `voice-evidence-03.wav`

> “Satu penelitian bisa menarik, tetapi kesimpulan yang baik juga perlu melihat metode, jumlah peserta, keterbatasan, dan apakah hasilnya konsisten dengan penelitian lain.”

### File 4 — Angka dan tempo

**Nama file:** `voice-numbers-04.wav`

> “Dalam video berdurasi enam puluh sampai sembilan puluh detik, kita akan menjelaskan satu konsep, menunjukkan sumbernya, lalu menyebutkan batasannya.”

### File 5 — Penutup aman

**Nama file:** `voice-closing-05.wav`

> “Untuk kondisi pribadi, konsultasikan tenaga kesehatan yang sesuai. Mari belajar memahami tubuh dengan lebih kritis dan tanpa sensasi.”

Jangan mengubah istilah seperti **alveoli**, **oksigen**, **karbon dioksida**, atau **penelitian** pada saat membaca. Bila ada kata yang terasa kurang nyaman diucapkan, catat; ini akan menjadi bagian dari *pronunciation sheet*.

---

## 4. Struktur folder privat

Buat folder berikut **di perangkat pribadi**, bukan di folder repository Git:

```text
Documents/
└── VOICE-ID-v1-reference/
    ├── raw/
    │   ├── voice-neutral-01.wav
    │   ├── voice-anatomy-02.wav
    │   ├── voice-evidence-03.wav
    │   ├── voice-numbers-04.wav
    │   └── voice-closing-05.wav
    ├── voice-transcript.txt
    ├── recording-notes.txt
    └── voice-consent-private.md
```

### Isi `voice-transcript.txt`

Salin persis lima naskah di atas. Jika Anda mengucapkan kata yang berbeda, catat versi yang benar-benar diucapkan.

### Isi `recording-notes.txt`

```text
Tanggal rekam:
Perangkat / mikrofon:
Aplikasi perekam:
Format / sample rate / bit depth:
Lokasi rekam (umum saja, jangan tulis alamat):
Ada noise atau take yang diulang?:
Kata yang perlu panduan pelafalan:
```

### Isi `voice-consent-private.md`

Simpan sebagai catatan privat, bukan untuk GitHub:

```text
Saya adalah pemilik suara dalam file reference ini.
Saya mengizinkan file tersebut dievaluasi hanya untuk membentuk VOICE-ID-v1,
yaitu narator AI untuk kanal sains kesehatan milik saya.
Profile tidak boleh digunakan untuk meniru dokter, orang lain, endorsement palsu,
panggilan, atau tujuan di luar kanal tanpa persetujuan baru.

Nama pemilik suara:
Tanggal:
Cakupan persetujuan saat ini:
```

Untuk saat ini, cakupan persetujuan tetap **persiapan rekaman dan audit**. Model download, import ke engine, cloning, generation, atau publikasi audio memerlukan persetujuan tahap berikutnya.

---

## 5. Pemeriksaan mandiri sebelum disimpan

Dengarkan dengan earphone dan cek:

- [ ] Hanya suara Anda yang terdengar.
- [ ] Tidak ada musik, TV, kipas, jalan raya, notifikasi, atau gema kuat.
- [ ] Tidak ada bagian suara pecah/clipping.
- [ ] Semua kata dapat dipahami, terutama “alveoli”, “karbon dioksida”, angka, dan kalimat penutup.
- [ ] Nada terdengar hangat dan natural, tidak dibuat-buat.
- [ ] Nama file dan transcript sesuai.
- [ ] Semua file tetap berada di folder privat.

Jika ada gangguan, rekam ulang seluruh kalimat itu. Jangan memperbaiki dengan efek suara atau menggabungkan potongan-potongan audio.

---

## 6. Jangan lakukan hal ini

- Jangan upload audio ke repository/GitHub.
- Jangan mengirim audio mentah melalui voice note aplikasi chat yang mengompres file.
- Jangan memakai sample suara orang lain agar hasil terdengar lebih “profesional”.
- Jangan mengunggahnya ke VoiceStudio, provider cloud, atau website TTS sebelum engine/model disetujui.
- Jangan merekam atau mengunggah data pribadi yang tidak perlu, seperti alamat, nomor telepon, nomor identitas, informasi medis, atau percakapan orang lain.

---

## 7. Apa yang terjadi setelah rekaman siap?

Setelah Anda selesai merekam, cukup beri tahu bahwa folder dan lima file sudah siap **tanpa mengunggah file di chat ini**. Tahap berikutnya tetap menunggu clearance V2:

1. Verifikasi exact model, model weights, komponen, output rights, dan hardware.
2. Anda menerima ringkasan untuk menyetujui atau menolak download model.
3. Jika Anda menyetujui, file diimpor **lokal** ke VoiceStudio pada komputer yang disetujui.
4. Buat 5–10 sample uji; belum digunakan di video.
5. Lakukan Voice QA dan persetujuan `VOICE-ID-v1`.

Jika clearance model tidak terpenuhi, file tetap menjadi milik Anda dan tidak perlu diunggah; jalur aman adalah merekam narasi manual dari file tersebut.

---

## Keterkaitan dokumen

- [Voice Identity Production Plan](voice-identity-production-plan.md)
- [Audit kandidat engine 15 Oktober 2026](voice-engine-audit-2026-10-15.md)
- [Health Evidence Content Plan](health-evidence-content-plan.md)
