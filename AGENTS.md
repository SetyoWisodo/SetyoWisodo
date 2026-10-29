# AGENTS.md — aturan kerja di repo ini

Berlaku untuk agent mana pun yang bekerja di repo ini (Arena agent, Claude Code,
Codex, Copilot, atau manusia yang mengikuti alurnya).

## Pintu masuk

Semua pekerjaan **reverse engineering** mengikuti satu alur kerja:

> **[`.agents/skills/rea-workflow/SKILL.md`](.agents/skills/rea-workflow/SKILL.md)**

Alur kerja itu menggabungkan 7 skill di `.agents/skills/` menjadi loop 8 fase
dengan gate. Jangan memilih skill sendiri di awal — jalankan loop, biarkan loop
memanggil skill yang tepat.

## Lima aturan

1. **Evidence sebelum klaim.** Setiap pernyataan tentang target harus bisa
   ditelusuri: tool, path/alamat, digest/byte range. Tanpa itu → tulis sebagai
   dugaan atau `unknown`.
2. **Scope dijaga.** Investigasi ≠ izin mengeksekusi target, mengubah file,
   memasang software, publish, atau merge.
3. **Satu fase, satu tujuan.** Nyatakan pertanyaan (F0) sebelum mengambil
   Evidence (F3).
4. **Jangan ulangi call identik.** Gagal → ubah input atau bereskan blocker dulu.
5. **Summary-first.** `detail: "summary"`, lalu page lewat `inspect_analysis_view`.

## Titik cepat

| Kebutuhan | Jalankan |
| --- | --- |
| Cek kesiapan lingkungan | `bash .agents/skills/rea-roadmap/scripts/check_readiness.sh <target>` |
| Cari resource per tahap/kategori | `bash .agents/skills/rea-roadmap/scripts/find_resource.sh --stage 4` |
| Mulai sesi kerja | `bash .agents/skills/rea-workflow/scripts/session.sh init "<label>" --target <path>` |
| Status & gate | `bash .agents/skills/rea-workflow/scripts/session.sh status` |
| Cari tool open-source | `python3 .agents/skills/find-reverse-engineered/scripts/re_index.py search <kata>` |
| Pilih tool untuk target | `bash .agents/skills/rea-workflow/scripts/session.sh tools --stage 4` |
| Cek batas nyata lingkungan | `.agents/skills/rea-workflow/references/capability-matrix.md` |

## Indeks & provenance

- [`SKILLS.md`](SKILLS.md) — daftar skill, semua link kedua postingan, status verifikasi.
- [`.agents/skills/README.md`](.agents/skills/README.md) — asal tiap skill + lisensi.

State sesi disimpan di `/tmp/rea-workflow/` (di luar tracked tree). Jangan
menambahkan artefak sesi, Evidence mentah, atau dataset besar ke Git.
