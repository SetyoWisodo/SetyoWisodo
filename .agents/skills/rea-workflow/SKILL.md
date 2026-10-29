---
name: rea-workflow
description: Satu alur kerja terpadu reverse engineering untuk percakapan ini — menggabungkan 7 skill REA (routing target, evidence, roadmap belajar, pencari tool, optimasi, audit CI, desain tool) menjadi satu loop 8 fase dengan gate yang harus lulus sebelum lanjut. Pakai skill ini setiap kali ada pekerjaan RE yang nyata: "analisa app/binary/APK/HAR ini", "kenapa fitur X begitu", "bandingkan dua versi", "rekonstruksi fitur", "lanjut ke tahap berikutnya", atau "mulai dari mana". English triggers: reverse engineering workflow, analyze this binary/APK/JS bundle, explain this feature, compare versions, run REA session, where do I start.
metadata:
  version: "1"
  composes:
    - reverse-engineer-anything
    - rea-roadmap
    - find-reverse-engineered
    - rea-analysis-optimization
    - rea-ci-tests-audit
    - rea-tool-design
    - rea-changelog-update
---

# Satu alur kerja REA

Ini adalah **pintu masuk tunggal**. Jangan memilih-milih skill lain di awal; jalankan
loop di bawah, dan biarkan loop memanggil skill yang tepat di fase yang tepat.
Skill lain tetap utuh sebagai rujukan detail — skill ini yang mengatur urutannya.

Dua hal yang digabung di sini:

- **Loop 8 fase** (cara mengerjakan satu target, dari permintaan sampai laporan).
- **Antrean tahap 0–7** (target mana yang dikerjakan berikutnya; dari
  `rea-roadmap`).

Keduanya bertemu di satu titik: **satu sesi = satu target = satu putaran loop**,
lalu antrean bergerak satu langkah.

## Aturan yang tidak bisa dinegosiasikan

1. **Evidence sebelum klaim.** Setiap pernyataan tentang target harus bisa
   ditelusuri ke: tool, path/alamat, digest/byte range, atau keluaran perintah.
   Tanpa itu → tulis sebagai dugaan atau `unknown`. Lihat
   [`references/evidence-contract.md`](references/evidence-contract.md).
2. **Scope dijaga.** Investigasi ≠ izin mengeksekusi target, mengubah file,
   memasang software, publish, atau merge. Tiap aksi berdampak butuh izin.
3. **Satu fase, satu tujuan.** Jangan mengumpulkan Evidence untuk pertanyaan yang
   belum dinyatakan. Tulis pertanyaannya dulu (F0), baru ambil Evidence (F3).
4. **Jangan ulangi call identik.** Kalau gagal: ubah input, atau bereskan
   blocker-nya dulu (`references/connection-and-recovery.md` di skill
   `reverse-engineer-anything`).
5. **Summary-first.** Mulai dari `detail: "summary"`, page bagian tertentu lewat
   `inspect_analysis_view`; jangan minta hasil lengkap tanpa alasan.
6. **Skill = instruksi, bukan engine.** Repo ini tidak memasang MCP `rea`,
   Ghidra, JADX, Frida, atau Node.

## Loop 8 fase

Setiap fase punya **gate**: kalau gate belum lulus, jangan maju. Detail, perintah,
dan contoh keluaran ada di [`references/phases.md`](references/phases.md).

| Fase | Nama | Keluaran wajib | Gate |
| --- | --- | --- | --- |
| **F0** | Intake & scope | Pertanyaan satu kalimat, target (path/URL/nama), batas (boleh/tidak boleh dieksekusi) | Pertanyaan bisa dijawab "ya/tidak/tidak diketahui"; target konkret |
| **F1** | Environment | Hasil `scripts/check_readiness.sh` + engine yang dipakai | Tool yang dibutuhkan pertanyaan ini tersedia; kalau tidak, turunkan klaim |
| **F2** | Route | Rute terpilih + alasan + alternatif yang ditolak | Rute cocok dengan jenis target di `references/target-routing.md` |
| **F3** | Evidence | Daftar Evidence (id/path), ringkasan tiap langkah | Tiap butir punya sumber; tidak ada "kayaknya" |
| **F4** | Interpretasi | Fakta vs inferensi dipisah | Setiap inferensi menyebut fakta yang menopangnya |
| **F5** | Verifikasi | Satu pemeriksaan silang (metode/target/versi lain) | Klaim utama lolos pemeriksaan, atau keterbatasannya dinyatakan |
| **F6** | Deliverable | Jawaban/penjelasan/rekonstruksi/ringkasan + sitasi Evidence | Format sesuai permintaan user; tidak menambah scope |
| **F7** | Catat & tutup | Daftar `unknown`, aksi berikutnya, arsip sesi | `unknown` tercatat; state sesi tersimpan |

### Bentuk ringkas (untuk diingat)

```
F0 tanya → F1 cek alat → F2 rute → F3 ambil bukti → F4 pisahkan fakta/dugaan
   → F5 uji silang → F6 jawab + sitasi → F7 catat unknown + langkah berikutnya
```

## Peta skill: siapa dipanggil di fase mana

| Fase | Skill yang dipakai | Untuk apa |
| --- | --- | --- |
| F0 | `rea-roadmap` | Menentukan target berikutnya dari antrean 7 tahap |
| F1 | `rea-roadmap` (`scripts/check_readiness.sh`) | Fakta lingkungan: Node, `rea`, Ghidra/JADX/Frida, target |
| F2 | `reverse-engineer-anything` | Routing resmi per jenis target (sumber kebenaran) |
| F3 | `reverse-engineer-anything` | Nama tool, kontrak, semantik Evidence |
| F3 | `references/re-toolchain.md` | Memilih tool konkret (Ghidra/IDA/jadx/Apktool/Frida/angr/mitmproxy/…) sesuai target |
| F3b | `find-reverse-engineered` | Kalau target tidak punya API/SDK/spesifikasi → cari tool open-source |
| F4–F6 | `reverse-engineer-anything` | Batas interpretasi, unknown, perbandingan versi |
| F6b | `rea-tool-design` | Kalau deliverable-nya justru tool/CLI/MCP baru |
| F6c | `rea-changelog-update` | Kalau deliverable-nya release notes |
| F7 | — | Tutup: `scripts/session.sh` mencatat state |
| kapan saja | `rea-analysis-optimization` | Hanya jika ada keluhan performa/biaya konkret |
| kapan saja | `rea-ci-tests-audit` | Hanya jika pertanyaannya soal CI/test suite |

Rincian pemicu & non-goal tiap skill: [`references/skill-map.md`](references/skill-map.md).

## Menjalankan sesi

State sesi disimpan di luar tracked tree (`/tmp/rea-workflow/<slug>/`), sesuai
aturan repo. Tidak ada yang ditulis ke Git kecuali user minta.

```bash
S=.agents/skills/rea-workflow/scripts/session.sh
bash $S init "apk aegis login" --target /path/app.apk   # buat sesi
bash $S status                                          # fase, gate, unknown
bash $S log "rute: inspect_android_package → kelas Login"  # catat langkah
bash $S gate F2 --pass  "jenis target APK, rute cocok"
bash $S advance F3                                      # maju satu fase
bash $S unknown "validasi native? cek lib*.so"          # catat pertanyaan terbuka
bash $S report                                          # ringkasan siap tempel
```

Aturan main `session.sh`:

- `advance` menolak maju kalau gate fase sekarang belum `pass`.
- `unknown` wajib punya teks; menutup unknown butuh `--resolved` + bukti.
- `report` mengeluarkan blok ringkasan (fase, target, evidence, unknown, next).

## Antrean tahap (dari roadmap)

Loop di atas adalah **cara**; ini **urutannya**:

```
T1 Setup → T2 Notes Export → T3 CTF binary → T4 Aegis APK
   → T5 Notion / DX-Ball / TH04 → T6 Ghidra + assembly → T7 Paper + tooling
```

Kriteria masuk/keluar, prompt siap tempel, dan jebakan tiap tahap ada di
[`../rea-roadmap/references/learning-path.md`](../rea-roadmap/references/learning-path.md).
Ambil resource dengan
`bash .agents/skills/rea-roadmap/scripts/find_resource.sh --stage <N>`.

Kalau user datang dengan target nyata di luar antrean (mis. APK kantor), tetap
pakai loop; antrean hanya dipakai saat user minta "belajar dari awal" atau
"lanjut tahap".

## Format jawaban akhir (F6)

Selalu empat bagian, dalam bahasa user:

```markdown
## Jawaban
<satu sampai tiga kalimat yang menjawab pertanyaan F0>

## Bukti
- <tool/perintah> → <path/alamat/digest> → artinya apa

## Fakta vs inferensi
- Fakta: …
- Inferensi: … (basis: bukti #…)

## Belum diketahui
- … (butuh: <alat/akses/izin>)
```

Kalau Evidence tidak lengkap, bagian "Belum diketahui" **wajib** ada isinya —
"tidak ada" hanya boleh kalau memang sudah diverifikasi lengkap.

## Batasan

- Tanpa MCP `rea` aktif, F3 dikerjakan dengan tool yang tersedia (shell, `file`,
`sha256sum`, `strings`, `python3`, dsb.) dan klaim diturunkan sesuai itu —
tidak menyamar sebagai keluaran decompiler.
- Skill ini tidak menambah izin apa pun di atas yang sudah diberikan user.
- Untuk repo sumber yang lengkap, analisis kode biasa lebih tepat; jangan
  memaksakan alur RE.
