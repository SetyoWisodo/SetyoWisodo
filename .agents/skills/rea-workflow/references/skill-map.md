# Peta 7 skill: kapan dipakai, kapan tidak

Semua skill berada di `.agents/skills/`. Yang diatur di sini hanya **urutan dan
batas**; isi teknisnya tetap milik masing-masing `SKILL.md`.

| Skill | Pemicu (gunakan) | Non-goal (jangan) | Dipanggil di |
| --- | --- | --- | --- |
| **rea-workflow** (ini) | Setiap pekerjaan RE nyata; "mulai dari mana", "analisa ini", "lanjut" | Menjadi ensiklopedia tool | Selalu |
| **reverse-engineer-anything** | Perlu memilih tool, membaca Evidence, membandingkan versi, membangun AgentEnv | Analisis arsitektur repo sumber yang lengkap | F2–F6 |
| **rea-roadmap** | Belajar bertahap, menentukan target berikutnya, mencari resource belajar | Menjadi alat analisis target nyata | F0, F1, F7 |
| **find-reverse-engineered** | Target tertutup tanpa API/SDK/driver/spesifikasi; butuh tool open-source | Menggantikan analisis target yang sedang diperiksa | F3 (bila perlu) |
| **rea-analysis-optimization** | Ada keluhan performa/biaya konkret: context, latency, CPU, memory, cache | "Biar lebih cepat" tanpa pengukuran | Kapan saja, atas permintaan |
| **rea-ci-tests-audit** | Investigasi CI/test suite: false pass, fixture drift, biaya suite | Testing fitur biasa atau satu test gagal | Kapan saja, atas permintaan |
| **rea-tool-design** | Deliverable-nya tool/CLI/MCP baru atau perubahan kontrak | Investigasi biasa yang hasilnya penjelasan | F6 (bila deliverable = tool) |
| **rea-changelog-update** | Menyusun release notes/changelog + atribusi kontributor | Menulis dokumentasi fitur biasa | F6 (bila deliverable = notes) |

## Aturan delegasi

1. **Satu skill utama per fase.** Di F3 hanya `reverse-engineer-anything`;
   `find-reverse-engineered` dipakai sebagai langkah tambahan bila target tidak
   punya spesifikasi.
2. **Tidak ada skill yang memberi izin tambahan.** Semua tunduk pada scope F0.
3. **Konflik rujukan:** `reverse-engineer-anything/SKILL.md` menang untuk urusan
   tool dan Evidence; `rea-roadmap/references/resources.md` menang untuk URL.
4. **Skill khusus tidak dipakai untuk kerja rutin.** Optimasi dan audit CI butuh
   pertanyaan konkret, bukan sekadar keinginan mempercepat.
5. **Kalau dua skill sama-sama relevan**, jalankan yang lebih dekat ke
   deliverable, dan catat yang lain di `unknown` sebagai pekerjaan lanjutan.

## Alur keputusan cepat

```
ada target nyata? ──tidak──> rea-roadmap (pilih tahap & resource)
        │ya
        ▼
butuh tool/target routing? → reverse-engineer-anything (F2)
        │
        ├─ target tanpa API/SDK ──> find-reverse-engineered
        │
        ├─ keluhan performa ──────> rea-analysis-optimization
        ├─ soal CI/test ──────────> rea-ci-tests-audit
        │
        ▼
deliverable = tool?  ──> rea-tool-design
deliverable = notes? ──> rea-changelog-update
selain itu ────────────> jawaban 4 bagian (F6)
```

## Sumber skill (untuk sinkronisasi)

| Skill | Asal |
| --- | --- |
| reverse-engineer-anything, rea-analysis-optimization, rea-ci-tests-audit, rea-tool-design, rea-changelog-update | `morluto/rea` → `.agents/skills/` |
| find-reverse-engineered | `alexgaoth/awesome-reverse-engineered` → `plugin/skills/` (MIT) |
| rea-roadmap, rea-workflow | ditulis di repo ini dari postingan @cabbitar + link yang sudah diverifikasi |
