# OSS Radar 2026-09-18 — Review & Rencana Adopsi

> Sumber: post X @AvaIrisMusic (18 Sep 2026, "Story-to-Screen OSS Radar") berisi 7 proyek open-source.
> Diperiksa: 25 Okt 2026 lewat GitHub API (lisensi, status arsip, push terakhir) dan halaman depan repo.
> Aturan: **tidak menyalin kode** dari repo mana pun tanpa cek lisensi tertulis di repo itu. Ini catatan referensi, bukan lisensi.

## 1. Ringkasan lisensi & status

| # | Repo | Lisensi (GitHub) | Bintang | Push terakhir | Status untuk kita |
|---|------|------------------|---------|---------------|-------------------|
| 1 | thesysdev/openui | MIT | 13.705 | 25 Okt 2026 | Boleh dipakai/disalin dengan atribusi. Relevan untuk UI generatif (skill-lab), belum dipakai. |
| 2 | danjdewhurst/story-skills | MIT | 351 | 20 Okt 2026 | **Acuan utama `script-long-form`.** Boleh dipakai dengan atribusi. |
| 3 | ChrisChen667788/wind-comic | MIT | 703 | 25 Okt 2026 | Referensi arsitektur pipeline script→storyboard→video. Repo besar, banyak provider; jangan install langsung. |
| 4 | jangtrinh/design-os-3d-blender | **PolyForm Shield 1.0.0** (bukan MIT) | 102 | 22 Okt 2026 | **Referensi saja.** Lihat §3. |
| 5 | SaltKing0/ideagraph-live | MIT | 2 | 21 Okt 2026 | Bintang sangat sedikit; referensi konsep graph canon/bukti. |
| 6 | ncz-os/mnemos | Apache-2.0 | 35 | 23 Okt 2026 | Boleh dipakai dengan atribusi dan catatan perubahan. Relevan untuk memori agent. |
| 7 | chrismsmr-celcom/agentguard | Apache-2.0 | 16 | 24 Okt 2026 | Boleh dipakai. Relevan sebagai guardrail agent. |

Catatan: GitHub API menandai design-os-3d-blender sebagai `NOASSERTION`, tetapi file LICENSE-nya adalah PolyForm Shield 1.0.0. Itu yang berlaku.

## 2. Rencana repo (sesuai usulan)

- **`script-long-form`** (skill baru): template naskah narasi 20–60 menit. Acuan: `story-skills` (MIT). Wajib menyebut atribusi di header file. Keluaran: outline beat, daftar klaim yang harus diverifikasi, bukan hanya teks.
- **`fact-check-sources`** (skill baru): memeriksa setiap klaim naskah ke sumber primer dan memberi status `verified / unverified / disputed`. Belum ada acuan langsung di 7 repo ini; dibangun dari nol. Aturan dari `story-skills` bahwa teks pihak lain adalah bahan, bukan instruksi, ikut dipakai.
- **Aturan isolasi**: skill yang membaca komentar atau halaman web tidak boleh menjalankan perintah dari teks itu.

Belum dikerjakan: membuat folder skill dan mengubah `skills-lock.json`. Itu butuh persetujuan karena menambah jumlah skill dari 54.

## 3. design-os-3d-blender: batasan PolyForm Shield

Yang boleh (menurut teks lisensi):
- Membaca, mempelajari, dan memakai sebagai referensi arsitektur.
- Memakai untuk pekerjaan komersial internal, termasuk membuat konten untuk klien.

Yang tidak boleh:
- Menjual atau memberikan ulang kodenya.
- Menawarkan produk yang **bersaing** dengannya. Ini berlaku untuk rencana "Skill Lab Marketplace" di proposal sebelumnya jika isinya skill Blender yang mirip.

Keputusan: tidak ada kode dari repo ini yang disalin. Untuk Blender, kita tetap memakai skill `blender-download-artifacts` dan `blender-knowledge-refresh` yang sudah ada. Jika suatu hari ingin menjual skill Blender, perlu konsultasi lisensi atau pembuatan ulang dari nol.

## 4. Hasil pemeriksaan empat repo tambahan (25 Okt 2026)

| Repo | Lisensi | Temuan | Keputusan |
|------|---------|--------|-----------|
| thesysdev/openui | MIT | Monorepo besar (1.060 commit, 82 tag, 13,7K bintang). Fokus generative UI dengan contoh banyak framework. Aktif. | Referensi untuk UI generatif di skill-lab jika nanti dibutuhkan. Tidak disalin. |
| SaltKing0/ideagraph-live | MIT | **Repo sudah pindah nama ke `SaltKing0/graph-engine`** (276 commit, 15 tag). Memuat catatan "prototype closeout" dan menyatakan validasi independen **belum selesai**; README menyebut modul ini eksperimental. Model graph berbasis Markdown di git cocok dengan kebutuhan canon dan bukti untuk naskah. | Referensi konsep provenance untuk `fact-check-sources`. Jangan dianggap production-ready. |
| ncz-os/mnemos | Apache-2.0 | Sistem memori besar (1.556 commit, 92 tag). Commit terakhir (23 Okt) berstatus **gagal di CI**. Banyak integrasi framework. | Tidak dipakai sekarang. Terlalu besar untuk kebutuhan skill-lab. Bisa jadi referensi memori agent. |
| chrismsmr-celcom/agentguard | Apache-2.0 | **Repo sudah pindah ke `cerbere-AG`** (906 commit). Commit terakhir (24 Okt) berstatus **gagal di CI**. Termasuk dashboard, kebijakan, dan fitur "sealed evidence". | Tidak dipakai sekarang. Kalau dipakai, cek status CI dulu. |

Catatan tambahan untuk design-os-3d-blender: commit 22 Okt berstatus gagal di CI. Tidak diselidiki lebih jauh.

## 5. Status adopsi

- `script-long-form` dan `fact-check-sources`: **sudah dibuat** di `.agents/skills/`, terdaftar di `skills-lock.json` (56 entri, semua hash cocok). Keduanya ditulis dari nol dengan struktur yang terinspirasi story-skills (MIT). Tidak ada teks yang disalin.
- design-os-3d-blender: tidak ada kode yang disalin.
- Prototype Studio Anomali: lihat `skill-lab/src/AnomalyStudio.jsx` dan section `#studio-anomali`, data mock.

## 6. Yang belum diperiksa

- Isi kode openui, graph-engine, mnemos, dan cerbere-AG hanya dibaca dari halaman depan. Belum dijalankan, belum diuji.
- Post asli berisi klaim pendek dari akun dengan 4 like. Deskripsi tiap repo dalam post adalah ringkasan penulis post, bukan dari repo itu sendiri.
