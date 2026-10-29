---
name: rea-roadmap
description: Jalankan roadmap belajar + kerja reverse engineering dari postingan @cabbitar sebagai alur kerja bertahap — setup REA, investigasi pertama, CTF binary, APK Android, game/Electron, lalu Ghidra/assembly/paper. Pakai skill ini saat user minta "mulai belajar RE dari nol", "kerjakan roadmap REA", "langkah berikutnya apa", atau saat butuh rute resource yang tepat (tutorial, showcase, repo, buku, paper, kursus) untuk satu target. English triggers: REA roadmap, reverse engineering learning path, REA setup, first investigation, which resource next.
metadata:
  version: "1"
  source: https://x.com/cabbitar/status/2115467413953056921
  upstream: https://github.com/morluto/rea
---

# REA roadmap → alur kerja

Skill ini mengubah satu postingan roadmap (46 link) menjadi urutan kerja yang
bisa dijalankan, bukan daftar bacaan. Setiap tahap punya **tujuan, resource
kanonik, perintah/prompt siap pakai, dan kriteria selesai**. Jangan lompat tahap
kecuali kriteria selesai tahap sebelumnya sudah terpenuhi atau user memintanya
secara eksplisit.

Aturan turunan: skill ini **tidak memberi izin** menjalankan target, mengubah
file, meng-install software, publish, atau merge. Setup dan instalasi selalu
butuh persetujuan eksplisit user (lihat `references/installation.md`).

## Peta file

| File | Isi |
| --- | --- |
| [`references/resources.md`](references/resources.md) | Semua 46 link postingan, sudah di-resolve dari shortlink `t.co` + status verifikasi + delta terhadap daftar kanonik user |
| [`references/resources.json`](references/resources.json) | Versi mesin dari tabel di atas (43 entri: label, URL, tco, kategori, tahap, status, berbayar/gratis) |
| [`references/learning-path.md`](references/learning-path.md) | 7 tahap: kriteria masuk/keluar, perintah, prompt, jebakan |
| [`references/installation.md`](references/installation.md) | Salinan `docs/installation.md` upstream (setup, client, engine, update/remove) |
| [`references/mcp-prompts.md`](references/mcp-prompts.md) | Salinan `docs/mcp-prompts.md` upstream (prompt MCP terpandu) |
| [`scripts/check_readiness.sh`](scripts/check_readiness.sh) | Cek read-only: Node, npx, CLI `rea`, engine (Ghidra/JADX/Frida/Java), target file |
| [`scripts/find_resource.sh`](scripts/find_resource.sh) | Query offline ke `resources.json`: `--stage N`, `--category repo|book|paper|…`, `--check`, atau pencarian kata bebas |

Skill pendamping di repo yang sama: `reverse-engineer-anything` (cara memilih
tool & Evidence), `find-reverse-engineered` (mencari tool open-source hasil RE
saat target tidak punya API/SDK).

## Alur kerja

### Langkah 0 — Tetapkan posisi user

Tentukan dulu satu hal: **user ini di tahap mana**. Tanyakan hanya jika tidak
bisa disimpulkan dari konteks; jangan interogasi.

- Belum punya agent/Node → Tahap 1
- Sudah `rea setup` tapi belum pernah investigasi → Tahap 2
- Sudah pernah investigasi, target masih binary kecil → Tahap 3
- Target Android/Electron/game → Tahap 4–5
- Butuh pseudocode, patch, atau baca paper → Tahap 6–7

Jalankan `bash scripts/check_readiness.sh` untuk mendapatkan fakta lingkungan
(versi Node, ada/tidak `rea`, engine yang terpasang). Laporkan hasilnya apa
adanya; jangan menyimpulkan "siap" dari asumsi.

### Langkah 1 — Pilih rute target

Sebelum menyentuh resource mana pun, klasifikasikan target memakai tabel rute di
`reverse-engineer-anything/SKILL.md` bagian "Route the target first". Roadmap ini
hanya menyuplai **urutan belajar**; pemilihan tool tetap milik skill itu.

### Langkah 2 — Jalankan tahap, bukan bacaan

Ambil tahap aktif dari `references/learning-path.md`. Untuk tahap itu:

1. Sebutkan tujuan satu kalimat dan resource kanoniknya. Ambil lewat
   `bash scripts/find_resource.sh --stage <N>` supaya URL yang dipakai selalu
   yang sudah diverifikasi, bukan hafalan.
2. Berikan **perintah atau prompt siap tempel** ke agent user.
3. Tunggu user mengerjakan; tawarkan mendampingi analisis hasilnya.
4. Uji kriteria selesai. Jika gagal, perbaiki penyebabnya (bukan mengulang
   langkah yang sama) lalu ulangi.

### Langkah 3 — Evidence sebelum klaim

Setiap hasil investigasi dilaporkan dalam bentuk: **fakta + sumber (path, digest,
byte range, tool) + batas/ketidaktahuan**. Kalau Evidence tidak tersedia, tulis
"belum diketahui" dan jelaskan apa yang dibutuhkan untuk mengetahuinya.

### Langkah 4 — Naik tahap hanya dengan bukti

Kriteria naik tahap ada di `references/learning-path.md`, misalnya tahap 2 selesai
kalau user bisa menunjukkan CSV formatter Notes dari Evidence, bukan karena
"sudah baca halamannya".

### Langkah 5 — Tutup dengan langkah berikutnya

Akhiri setiap sesi dengan: (a) tahap sekarang, (b) satu aksi berikutnya, (c)
resource yang dipakai. Simpan catatan belajar di luar tracked tree (mis.
`/tmp/rea-notes/`) kecuali user meminta dokumentasi di repo.

## Prompt pemicu yang bisa dipakai user

- "Jalankan roadmap REA dari awal untuk saya."
- "Saya di tahap mana? Cek environment dulu."
- "Target saya APK `<nama>`. Rute roadmap-nya bagaimana?"
- "Lanjut ke tahap berikutnya, buktikan kriteria selesainya."
- "Cari resource roadmap untuk topik `<topik>` (buku/paper/kursus)."

## Batasan yang harus disebut ke user

- Skill = instruksi. Ini tidak memasang MCP `rea`, Ghidra, JADX, Frida, atau
  Node. Instalasi lewat `npx rea-agents@latest setup` dan butuh persetujuan.
- Link `t.co` di postingan sudah di-resolve saat skill dibuat; kalau nanti tautan
  bergeser, ulangi verifikasi dengan cara di `references/source-verification.md`.
- Beberapa resource berbayar (buku No Starch, Wiley) — sebutkan itu, jangan
  menyarankan cara mengunduh ilegal.
