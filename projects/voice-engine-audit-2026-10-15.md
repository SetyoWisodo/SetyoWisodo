<div align="center">

# 🔎 Audit Kandidat Engine — Voice Identity `VOICE-ID-v1`

### **Narator brand hangat untuk konten sains kesehatan Indonesia**

*Tanggal audit: 15 Oktober 2026 · Ruang lingkup: evaluasi dokumentasi dan inventaris lokal VoiceStudio, tanpa download model atau pembuatan audio*

</div>

---

## Keputusan sementara

| Keputusan | Status |
|---|---|
| **Sumber suara** | Suara pemilik akun yang dimodifikasi menjadi karakter narator AI |
| **Karakter** | **Narator brand yang berbeda, hangat, mudah dipahami, dan tidak menggurui** |
| **Kandidat teknis terkuat** | **VoxCPM2 melalui VoiceStudio** |
| **Kelayakan produksi/monetisasi** | **HOLD — belum diizinkan** |
| **Alasan HOLD** | Hak komersial exact artifact, hak output, dan seluruh komponen belum memiliki clearance lengkap dalam inventaris VoiceStudio; kebutuhan hardware juga belum divalidasi pada mesin produksi |
| **Yang tidak dilakukan** | Tidak ada install, model download, cloning, voice profile, reference recording, synthesis, atau upload audio |

> Audit ini adalah pemeriksaan teknis dan dokumentasi lisensi yang tersedia, bukan pendapat hukum. Label `Apache-2.0`, `MIT`, atau `OpenRAIL` pada ringkasan model tidak otomatis merupakan izin produksi komersial yang lengkap.

---

## 1. Kebutuhan yang harus dipenuhi

`VOICE-ID-v1` harus dapat melakukan seluruh hal berikut:

1. Menggunakan **hanya suara pemilik akun** sebagai sumber apabila reference audio diperlukan.
2. Membentuk **narator brand** yang lebih sesuai untuk video: hangat, jelas, edukatif, dan mudah dipahami—bukan sekadar salinan suara mentah.
3. Mengucapkan Bahasa Indonesia, istilah anatomi, angka, singkatan, dan istilah Inggris yang digunakan dalam konten dengan baik.
4. Memakai satu Voice ID/profile yang stabil untuk setiap batch.
5. Memenuhi consent, non-impersonation, hak komersial model/komponen/output, dan Voice QA sebelum dipakai dalam video.
6. Tidak mengesankan narator sebagai dokter atau tenaga kesehatan berlisensi.

---

## 2. Kandidat yang dievaluasi

| Engine via VoiceStudio | Kesesuaian fungsi | Bahasa Indonesia | Status lisensi menurut inventaris VoiceStudio | Keputusan |
|---|---|---|---|---|
| **VoxCPM2** | Voice design, zero-shot cloning, dan *controllable cloning* dengan style instruction | Tercantum didukung | Metadata Apache-2.0, tetapi `commercial_use: false`, review belum selesai, component closure belum lengkap, dan output rights belum terverifikasi | **Kandidat teknis #1 — HOLD** |
| **OmniVoice (default)** | Cloning dan instruksi gaya | Cakupan bahasa luas | Komponen/weights tercatat non-komersial atau tidak memberi clearance komersial menyeluruh | **Tolak untuk produksi monetisasi** |
| **MOSS-TTS-Nano** | Reference-only cloning; tidak ada voice design/style control | Bahasa Indonesia tidak tercantum dalam daftar engine | Review komersial/output/components belum selesai | **Tidak cocok untuk kebutuhan narator brand** |
| **Supertonic-3** | Preset voice; tidak ada cloning maupun voice design | Broad language coverage, tetapi perlu uji aktual | OpenRAIL-M dengan syarat penggunaan; output/component review belum selesai | **Tidak cocok untuk sumber suara pemilik akun** |

### Mengapa VoxCPM2 adalah kandidat teknis terkuat

Dokumentasi VoiceStudio menyatakan VoxCPM2 mendukung:

- Bahasa Indonesia;
- **voice design** dari deskripsi tanpa reference audio;
- zero-shot voice cloning dari reference audio;
- **controllable cloning**: reference menyumbang *timbre*, sedangkan style instruction mengatur pembawaan; dan
- output 48 kHz.

Untuk arah yang dipilih, ini berarti reference suara pemilik dapat dipakai sebagai sumber yang sah, sementara pembawaannya diarahkan ke persona **“narator brand hangat dan mudah dipahami”**. Tidak ada contoh suara artis, dokter, kreator, atau orang lain yang boleh dipakai sebagai acuan.

### Mengapa VoxCPM2 tetap belum boleh diinstal

Inventaris lisensi VoiceStudio pada audit ini mencatat untuk `openbmb/VoxCPM2`:

- label lisensi upstream: `Apache-2.0`;
- `commercial_use: false` dan `review_status: unreviewed`;
- `commercial_inference: unknown` dan `commercial_outputs: unknown` pada record utama;
- *component closure* masih `incomplete`;
- komponen yang perlu ditutup secara eksplisit mencakup weights, audio VAE, tokenizer, code, provenance MiniCPM-4, dan jalur optional denoiser/text-normalization; serta
- catatan inventaris menyatakan evidence license yang ada belum cukup untuk mengonfirmasi hak output atau seluruh komponen.

Dokumentasi engine juga menyatakan model pertama kali diunduh sebagai checkpoint **multi-GB**, CPU/MPS dapat digunakan tetapi CUDA direkomendasikan untuk kecepatan penuh. Sandbox kerja saat ini tidak memiliki GPU dan hanya memiliki sekitar 3,8 GiB RAM, sehingga tidak dipakai untuk validasi runtime.

---

## 3. Jalur penyelesaian yang direkomendasikan

```text
V1 — Arah suara & consent terbatas                   ✅ dicatat
     Suara pemilik → narator brand hangat
                    ↓
V2 — Legal + technical clearance untuk engine       🔒 HOLD
     Exact model revision, weights, semua komponen,
     output rights, attribution, hardware, data path
                    ↓
V3 — Persetujuan khusus model/download               ⛔ belum diberikan
                    ↓
V4 — Reference recording privat + sample test        ⛔ belum diizinkan
                    ↓
V5 — Voice QA Gate & kunci VOICE-ID-v1               ⛔ belum diizinkan
                    ↓
V6 — Narasi batch + PPU                              ⛔ belum diizinkan
```

### V2 — Bukti yang harus lengkap sebelum model boleh disetujui

| Bukti | Standar minimum |
|---|---|
| **Exact artifact** | Nama repo, revision/hash, daftar file weights, hash jika tersedia, dan sumber unduhan resmi |
| **Hak komersial inference** | Teks lisensi/kartu model resmi yang berlaku untuk revision yang benar, bukan hanya badge/metadata |
| **Komponen** | Lisensi/terms untuk model, audio tokenizer/VAE, base model, code/runtime, normalizer/denoiser yang benar-benar diaktifkan |
| **Output use** | Terms yang tidak melarang penggunaan output untuk channel monetisasi; kewajiban attribution/disclosure dicatat |
| **Reference rights** | Consent pemilik suara, lokasi penyimpanan privat, transcript, dan batas penggunaan |
| **Restrictions** | Larangan impersonation, fraud, health misinformation, atau penggunaan terlarang lain diterjemahkan ke SOP produksi |
| **Hardware & storage** | Mesin target, disk ruang bebas, RAM/VRAM, estimasi waktu render, lokasi cache, dan akses private diperiksa |

Jika satu bukti belum jelas, statusnya tetap **HOLD**. Tidak boleh “menganggap aman” hanya karena kode atau model card menunjukkan Apache/MIT.

### V3 — Persetujuan model/download yang akan diminta nanti

Hanya setelah V2 selesai, pemilik akun akan menerima ringkasan:

```text
Engine + exact model revision:
Sumber download resmi:
Ukuran unduhan + dependensi:
Mesin target dan kebutuhan storage/compute:
Lisensi code/model/component/output yang telah diverifikasi:
Attribution/disclosure yang wajib:
Risiko yang tersisa:
Aksi yang diminta: setujui / tolak download dan uji sample
```

Tanpa persetujuan khusus ini, tidak ada download atau instalasi yang dijalankan.

---

## 4. Rancangan `VOICE-ID-v1`

```text
Voice ID: VOICE-ID-v1
Status sekarang: concept / HOLD
Sumber: suara pemilik akun, owner-authorized AI-adapted narrator
Persona: narator brand berbeda; hangat, jelas, mudah dipahami
Larangan persona: dokter, ahli kesehatan berlisensi, selebritas, public figure,
                  kreator lain, atau orang nyata lain
Bahasa: Bahasa Indonesia
Transformasi yang ditargetkan: artikulasi, tempo, jeda, penekanan, kehangatan,
                               dan energi—bukan imitasi pihak ketiga
Engine kandidat: VoxCPM2 via VoiceStudio (teknis; belum cleared)
Reference audio: belum ada
Model download: belum ada
Audio generation: belum ada
```

---

## 5. Paket rekaman privat setelah clearance

Setelah model dan download disetujui, bukan sekarang, pemilik suara dapat menyiapkan:

| File | Isi | Target |
|---|---|---:|
| `voice-neutral-01.wav` | Penjelasan anatomi sederhana | 8–15 detik |
| `voice-explainer-02.wav` | Istilah ilmiah dan angka | 8–15 detik |
| `voice-warm-03.wav` | Penutup edukatif/CTA netral | 8–15 detik |
| `voice-transcript.txt` | Transkrip persis setiap klip | Lengkap |
| `voice-consent.md` | Izin, tanggal, pemilik, cakupan penggunaan | Lengkap |

Rekam dekat mikrofon di ruangan tenang, tanpa musik, reverb berat, kebisingan, atau suara orang lain. File referensi dan consent disimpan privat—**jangan dimasukkan ke GitHub atau repository ini**.

---

## 6. Uji sample sesudah ada persetujuan model

Sample awal tidak boleh langsung memakai naskah produksi. Uji 5–10 kalimat pendek berikut:

1. Pembuka edukatif yang hangat.
2. Istilah anatomi: “alveoli” dan “sistem saraf”.
3. Bukti penelitian: “systematic review” dan “meta-analysis”.
4. Angka/satuan/singkatan yang akan dipakai pada video.
5. Disclaimer netral: “Untuk kondisi pribadi, konsultasikan tenaga kesehatan.”

### Voice QA Gate

| Pemeriksaan | Kriteria PASS |
|---|---|
| Identitas | Konsisten sebagai satu narator brand; tidak menyerupai orang lain |
| Persona | Hangat, jelas, mudah diikuti; tidak berlebihan atau menggurui |
| Pelafalan | Tidak mengubah arti istilah kesehatan/angka/singkatan |
| Audio | Tidak ada clipping, artefak, kata hilang, atau jeda salah |
| Hak & consent | Voice card, consent, engine/model/output evidence lengkap |
| Disclosure | Keputusan disclosure AI per platform terdokumentasi |

Hanya sample yang memperoleh PASS dan disetujui pemilik akun yang dapat mengubah status `VOICE-ID-v1` menjadi `approved`.

---

## 7. Fallback bila VoxCPM2 tidak memperoleh clearance

1. **Rekam suara pemilik secara manual** dengan panduan tempo, EQ, noise control, dan pronunciation sheet. Ini adalah fallback paling aman untuk kepemilikan dan jadwal produksi.
2. Cari provider/engine lain hanya jika dapat dibuktikan: Bahasa Indonesia memadai, tidak membutuhkan imitasi pihak ketiga, dan hak komersial model serta output-nya jelas.
3. Jangan mengganti ke OmniVoice default, MOSS, atau preset voice secara diam-diam hanya karena lebih mudah dipasang.

---

## Sumber audit

- [VoiceStudio — VoxCPM2 engine guide](https://github.com/debpalash/VoiceStudio/blob/main/docs/engines/voxcpm2.md)
- [VoiceStudio — MOSS-TTS-Nano engine guide](https://github.com/debpalash/VoiceStudio/blob/main/docs/engines/moss-tts-nano.md)
- [VoiceStudio — Supertonic-3 engine guide](https://github.com/debpalash/VoiceStudio/blob/main/docs/engines/supertonic3.md)
- [VoiceStudio — Model licence inventory](https://github.com/debpalash/VoiceStudio/blob/main/docs/licensing/model-inventory.md)
- [VoiceStudio repository](https://github.com/debpalash/VoiceStudio)
