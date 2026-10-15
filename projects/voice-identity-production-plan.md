<div align="center">

# 🎙️ Voice Identity Production Plan

### **Satu suara narator yang konsisten untuk brand kesehatan berbasis bukti**

*Integrasi kandidat: [VoiceStudio](https://github.com/debpalash/VoiceStudio) · Status: rencana bersyarat, belum ada cloning atau model download*

</div>

---

## Ringkasan keputusan

| Area | Keputusan |
|---|---|
| **Tujuan** | Menciptakan satu identitas suara yang konsisten untuk seluruh video kesehatan, agar audiens mengenali brand melalui narasi yang sama |
| **Tool kandidat** | VoiceStudio: desktop/local workflow untuk voice cloning, voice design, batch narration, local API, dan MCP |
| **Sumber suara** | **Belum dipilih.** Hanya boleh memakai suara pemilik akun yang memberi persetujuan eksplisit, atau suara sintetis yang lisensi penggunaan komersialnya telah diverifikasi |
| **Status sekarang** | Belum ada clone, voice profile, reference audio, model download, API key, atau audio render |
| **Kebijakan brand** | Satu profile yang dikunci per versi (`VOICE-ID-v1`), bukan berganti-ganti suara antarvideo |
| **Kebijakan kesehatan** | Narator tidak boleh tampil/ditulis sebagai dokter atau ahli kesehatan bila tidak ada kredensial tersebut |

> **Prinsip utama:** konsistensi suara harus meningkatkan pengenalan brand, bukan menciptakan otoritas medis palsu.

---

## 1. Evaluasi VoiceStudio

VoiceStudio adalah aplikasi lokal/open-source untuk voice cloning, voice design, dubbing, batch narration, dan koneksi local API/MCP. Proyeknya berlisensi **AGPL-3.0**; jika aplikasi dimodifikasi lalu disediakan kepada pengguna melalui jaringan, ada kewajiban AGPL terkait penyediaan source code. Lisensi aplikasi **berbeda** dari lisensi setiap model, tokenizer, reference voice, dan output suara.

### Keputusan kompatibilitas

| Pertanyaan | Jawaban untuk workflow ini |
|---|---|
| Cocok untuk satu voice identity? | **Ya, secara fungsional.** Voice profile dapat disimpan dan dipakai ulang untuk narasi batch. |
| Boleh langsung digunakan untuk konten monetisasi? | **Belum.** Model/weights yang dipilih harus memiliki izin komersial yang diverifikasi, termasuk output dan komponen pendukungnya. |
| Apakah suara bisa langsung dikloning? | **Tidak.** Harus ada sumber suara berizin dan consent tertulis dari pemilik suara. |
| Apakah aplikasi akan diinstal di lingkungan saat ini? | **Tidak sekarang.** Sandbox ini tidak memiliki GPU dan hanya memiliki memori terbatas; tidak cocok untuk uji model TTS berat secara bertanggung jawab. |
| Apakah Bahasa Indonesia dijamin kualitasnya? | **Tidak dijanjikan sebelum uji.** Engine yang dipilih harus lulus tes pelafalan Bahasa Indonesia dan istilah kesehatan. |

### Temuan lisensi yang memblokir aktivasi langsung

1. VoiceStudio sendiri menggunakan AGPL-3.0.
2. Inventaris lisensi proyek menyatakan lisensi aplikasi tidak menyelesaikan hak model/weights, tokenizer, voice, dan generated output.
3. Default OmniVoice di inventaris proyek tercatat dengan komponen/weights non-komersial atau status yang tidak memberi clearance produksi komersial menyeluruh.
4. Inventaris tersebut juga menyatakan tidak ada record yang mengklaim semua model produksi telah selesai ditinjau untuk commercial use.

**Konsekuensi:** VoiceStudio dapat dijadikan *orchestrator* atau kandidat tool, tetapi **model default tidak diaktifkan** untuk channel yang menargetkan monetisasi sampai lisensi exact model dan seluruh komponennya disetujui.

---

## 2. Voice Identity Card

Satu kartu identitas suara harus dibuat dan dikunci sebelum dipakai di produksi.

```text
Voice ID: VOICE-ID-v1
Status: draft / test / approved / retired
Pemilik suara atau sumber desain:
Bukti consent / lisensi:
Tool dan versi:
Engine + exact model/weight revision:
Lisensi engine/model/output yang diverifikasi:
Bahasa utama: Bahasa Indonesia
Gaya: edukatif, tenang, jelas, hangat, tidak menggurui
Kecepatan target: diuji per naskah; utamakan kejelasan
Larangan: impersonasi dokter, selebritas, public figure, atau orang lain
Reference audio path + transcript:
Tanggal uji:
Hasil QA:
Approval pemilik akun:
```

Profile hanya dianggap **approved** jika semua data di atas terisi dan lulus Voice QA Gate.

---

## 3. Consent dan sumber suara

### Jalur A — Suara pemilik akun sendiri

Ini jalur yang paling kuat untuk identitas personal, tetapi membutuhkan persetujuan eksplisit.

Sebelum reference audio dipakai, pemilik suara harus menyetujui pernyataan berikut:

> “Saya adalah pemilik suara pada rekaman referensi ini dan memberi izin untuk membuat profile suara AI yang hanya digunakan sebagai narasi pada kanal kesehatan [nama brand]. Saya memahami profile ini tidak boleh digunakan untuk meniru dokter, orang lain, endorsement palsu, panggilan, atau tujuan di luar persetujuan ini tanpa persetujuan baru.”

### Jalur B — Suara sintetis yang didesain

Boleh digunakan jika:

- engine/model/output memiliki izin komersial yang terdokumentasi;
- tidak menyerupai orang nyata, dokter, selebritas, atau public figure;
- voice card menyatakan sumbernya “synthetic design”; dan
- hasil uji Bahasa Indonesia lulus.

### Yang tidak diizinkan

- Mengkloning suara orang lain tanpa persetujuan eksplisit.
- Menggunakan sampel dari podcast, video, film, dokter, kreator, atau public figure sebagai reference.
- Menjual/membagikan profile suara tanpa persetujuan baru.
- Memakai voice identity untuk konten sponsor/produk kesehatan tanpa disclosure dan approval baru.

---

## 4. Paket reference recording

VoiceStudio mendukung cloning dari reference clip pendek; dokumentasinya menyebut 3–10 detik sebagai rentang reference clip untuk engine OmniVoice. Untuk identitas brand, jangan bergantung pada satu potongan pendek saja. Siapkan paket referensi yang konsisten, dengan transcript yang benar.

| File | Target | Isi |
|---|---:|---|
| `voice-neutral-01.wav` | 8–15 dtk | Narasi tenang tentang anatomi sederhana |
| `voice-explainer-02.wav` | 8–15 dtk | Kalimat dengan penekanan pada istilah ilmiah umum |
| `voice-warm-03.wav` | 8–15 dtk | Penutup edukatif dan CTA netral |
| `voice-transcript.txt` | Lengkap | Transkrip persis dari seluruh rekaman referensi |
| `voice-consent.md` | 1 file | Pernyataan izin, tanggal, pemilik, dan batas penggunaan |

### Standar rekaman

- Rekam suara pemilik saja, di ruangan tenang dan kering (*dry*), dekat mikrofon.
- Hindari musik, reverb, kipas, jalan raya, kompresi aplikasi chat, dan suara orang lain.
- Jangan memakai rekaman yang sudah diproses dengan efek suara berat.
- Simpan file asli dan transcript; jangan mengunggahnya ke Git atau memasukkannya ke artifact publik.
- Reference audio hanya disimpan pada storage privat yang aksesnya dibatasi.

---

## 5. Voice QA Gate

### Uji wajib sebelum profile dipakai

| Uji | Kriteria lulus |
|---|---|
| **Consent & ownership** | Consent/izin atau lisensi synthetic voice lengkap dan dapat diaudit |
| **Lisensi komersial** | Engine, model/weights, komponen, dan output use telah diperiksa untuk channel monetisasi |
| **Identitas suara** | Lima sampel terdengar sebagai identitas yang sama, bukan suara berganti/artefak |
| **Bahasa Indonesia** | Pelafalan natural untuk kata umum, istilah anatomi, angka, dan singkatan yang direncanakan |
| **Kejelasan** | Tidak ada clipping, noise, lompat nada, kata hilang, atau jeda tak wajar yang mengubah arti |
| **Gaya brand** | Tenang, edukatif, hangat; tidak terdengar sebagai dokter/otoritas medis personal |
| **Konsistensi teknis** | Format sample, loudness, kecepatan, dan profile ID tetap pada seluruh output uji |
| **Disclosure** | Keputusan label/disclosure AI ditetapkan untuk YouTube, TikTok, dan Instagram jika diperlukan |

### Ambang keputusan

- **PASS:** seluruh uji wajib lulus dan pemilik akun menyetujui sample A/B.
- **REVISE:** ada masalah pelafalan, tempo, atau gaya; profile/setting direvisi lalu diuji ulang.
- **HOLD:** consent tidak ada, lisensi tidak jelas, voice menyerupai orang lain, atau engine tidak cocok untuk Bahasa Indonesia.

Tidak ada video kesehatan yang memakai voice profile tersebut sebelum Voice QA Gate memperoleh **PASS**.

---

## 6. Integrasi ke Divisi Produksi

Voice Identity menjadi *sub-skill* wajib di **Divisi 3 — Production & Hook/Retention**.

```text
Naskah lulus source card
        ↓
Production menentukan phrase pronunciation sheet
        ↓
Voice skill memanggil satu VOICE-ID-v1 yang approved
        ↓
Audio QA: pengucapan + artefak + tempo + consistency
        ↓
Visual/subtitle assembly
        ↓
PPU memeriksa versi video final + voice card
```

### Pronunciation sheet per video

```text
Content ID:
Voice ID dan versi:
Kata/istilah: alveoli | suprachiasmatic nucleus | meta-analysis | systematic review
Pelafalan yang disetujui:
Singkatan/angka yang harus dieja:
Kata yang dilarang/diubah:
Tempo target:
Reviewer audio:
```

### Aturan produksi

- Gunakan **satu Voice ID approved** pada setiap video dalam satu channel.
- Jangan mengganti model, voice profile, atau gaya secara diam-diam di tengah batch.
- Jika istilah kesehatan diucapkan buruk, Production wajib memperbaiki text normalization/phonetic guide atau merekam ulang; jangan membiarkan subtitle menutupi audio yang salah.
- Semua audio output adalah draft sampai PPU memeriksa file final.
- Voice skill tidak boleh menambahkan atau mengubah klaim ilmiah pada naskah yang telah disetujui.

---

## 7. Rencana aktivasi bertahap

| Tahap | Output | Status sekarang |
|---|---|---|
| **V0 — Due diligence** | Audit VoiceStudio, lisensi, consent, hardware, dan batas brand | ✅ Selesai |
| **V1 — Pilih sumber suara** | Keputusan: suara pemilik atau synthetic design + consent/lisensi | ⏳ Menunggu pemilik akun |
| **V2 — Model & environment review** | Exact engine/model, revision, license evidence, hardware, data path | ⏳ Jangan download/install tanpa approval |
| **V3 — Sample test** | 5–10 clip pendek Bahasa Indonesia untuk uji identity & pronunciation | ⏳ Hanya setelah V1–V2 PASS |
| **V4 — Voice QA Gate** | Voice ID `approved` atau `hold` | ⏳ |
| **V5 — Batch narration** | Narasi untuk naskah yang telah disetujui; QA audio dan PPU | 🔒 Belum diizinkan |

---

## 8. Catatan environment saat ini

Pemeriksaan sandbox kerja saat plan dibuat menemukan sekitar **2 vCPU, 3,8 GiB RAM, dan tidak ada GPU yang terdeteksi**. VoiceStudio dapat memiliki mode CPU, tetapi environment ini bukan tempat yang tepat untuk mengunduh atau memvalidasi model cloning produksi yang berat. Aktivasi kelak harus dilakukan pada mesin pemilik akun atau server yang memenuhi kebutuhan engine terpilih.

Tidak ada model VoiceStudio yang diunduh saat menyusun dokumen ini.

---

## 9. Persetujuan untuk langkah selanjutnya

Jika memilih **suara sendiri**, gunakan persetujuan berikut:

> “Saya memilih suara saya sendiri sebagai sumber `VOICE-ID-v1` untuk kanal kesehatan. Saya memberi izin terbatas untuk membuat profile narasi AI bagi kanal ini. Lanjutkan ke V2: audit engine/model dan siapkan naskah reference recording. Jangan mengunduh model, membuat clone, atau menghasilkan audio sebelum saya menyetujui model dan menyerahkan reference recording.”

Jika memilih **suara sintetis**, gunakan:

> “Saya memilih suara sintetis untuk `VOICE-ID-v1`. Cari kandidat engine/model yang izin komersialnya dapat diverifikasi dan cocok untuk Bahasa Indonesia. Jangan mengunduh model atau menghasilkan audio sebelum saya menyetujui kandidatnya.”

---

## Sumber

- [VoiceStudio GitHub repository](https://github.com/debpalash/VoiceStudio)
- [VoiceStudio agent/install guide](https://github.com/debpalash/VoiceStudio/blob/main/docs/install/agent.md)
- [VoiceStudio OmniVoice engine guide](https://github.com/debpalash/VoiceStudio/blob/main/docs/engines/omnivoice.md)
- [VoiceStudio model license inventory](https://github.com/debpalash/VoiceStudio/blob/main/docs/licensing/model-inventory.md)
- [VoiceStudio license notice](https://github.com/debpalash/VoiceStudio/blob/main/LICENSE-NOTICE.md)
