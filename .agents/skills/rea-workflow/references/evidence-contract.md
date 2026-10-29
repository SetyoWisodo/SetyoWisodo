# Kontrak Evidence

Diambil dari semantik Evidence di `reverse-engineer-anything` dan
`references/evidence-workflows.md`, disederhanakan jadi aturan yang bisa dipakai
di percakapan ini.

## Satu butir Evidence minimal memuat

| Field | Isi | Contoh |
| --- | --- | --- |
| `id` | nomor stabil dalam sesi | `E3` |
| `tool` | cara mendapatkannya | `inspect_android_package`, `strings -n 6`, `sha256sum` |
| `sumber` | path/alamat/byte range/digest | `app.apk!classes2.dex`, alamat `0x180124960` |
| `isi` | potongan yang relevan saja | 6 instruksi, nama method, field |
| `arti` | apa yang ditunjukkan | "cabang membandingkan operator dengan 0x5c ('\\\\')" |
| `batas` | yang **tidak** dibuktikan | "tidak menunjukkan nilai saat runtime" |

Tanpa `sumber` + `batas`, butir itu bukan Evidence — hanya catatan.

## Fakta / inferensi / unknown

- **Fakta**: dapat dibaca langsung di Evidence. Boleh dikutip verbatim.
- **Inferensi**: kesimpulan; wajib menunjuk `id` Evidence penopang dan menyebut
  asumsi.
- **Unknown**: tidak dapat disimpulkan dari Evidence yang ada; wajib menyebut apa
  yang dibutuhkan (alat, akses, izin, versi).

Aturan praktis: kalau sebuah kalimat masih benar setelah Evidence-nya dihapus,
itu bukan fakta.

## Larangan

1. Menyebut perilaku runtime dari kode statis tanpa menyatakan asumsi.
2. Mengklaim "lengkap"/"tidak ada" dari Evidence yang parsial atau terpaginasi —
   kelengkapan halaman ≠ kelengkapan program.
3. Menyajikan keluaran alat bantu (`strings`, `grep`) sebagai hasil decompiler.
4. Menggabungkan dua artefak berbeda (versi/provider) tanpa menyebut perbedaan
   identitas/digest.
5. Menghapus batas yang sudah dinyatakan tool (coverage, `source_complete`,
   `omitted_fields`).

## Perbandingan (dua versi / dua target)

Klaim kesamaan atau perubahan hanya sah bila:

- kedua sisi punya himpunan halaman yang lengkap dan kompatibel;
- identitas dicatat (path + digest + provider + versi tool);
- perbedaan statis dilaporkan sebagai **kandidat** perubahan, bukan bukti kausal.

## Template finding (satu temuan)

```markdown
### E<n> — <judul singkat>
- tool   :
- sumber :
- isi    :
- arti   :
- batas  :
- status : fakta | inferensi | unknown (butuh: …)
```

Template siap pakai: [`../templates/finding.md`](../templates/finding.md).

## Penutupan sesi

Ringkasan akhir wajib memuat: target + digest, tool yang dipakai, Evidence inti
(E-id), fakta utama, inferensi utama, unknown, dan next step. Tanpa digest/versi,
hasil tidak dapat direproduksi dan tidak boleh disebut terverifikasi.
