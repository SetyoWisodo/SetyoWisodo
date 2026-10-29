# SPEC.md — spesifikasi rekonstruksi (clean-room)

<!--
Dipakai di F6 mode rebuild. Satu file per fitur/target.
Aturan: setiap butir perilaku WAJIB menunjuk Evidence (E-id). Yang tidak
dibuktikan masuk ke bagian "Tidak direkonstruksi", bukan diisi tebakan.
-->

## Identitas

| Field | Nilai |
| --- | --- |
| Fitur yang direkonstruksi | <!-- satu kalimat --> |
| Target asal | <!-- path + sha256 --> |
| Evidence sesi | <!-- id sesi / path findings.md --> |
| Oracle yang dipakai | <!-- uji hitung / verify_reconstruction / perilaku / diff --> |
| Status | draft \| teruji (isi hasil oracle) |

## Perilaku yang dibuktikan

| # | Perilaku | Bukti | Catatan |
| --- | --- | --- | --- |
| 1 | … | E1 | … |

## Input / output

| Input | Perilaku | Output |
| --- | --- | --- |
| <!-- contoh konkret dari Evidence --> | … | … |

## Konstanta & ambang

| Nama | Nilai | Asal (alamat/file) |
| --- | --- | --- |
| … | … | … |

## Kondisi batas

- … (dari cabang yang ditemukan di Evidence)

## Tidak direkonstruksi

- … (alasan: tidak ada Evidence / di luar scope)

## Rencana oracle

| Uji | Input | Ekspektasi | Hasil |
| --- | --- | --- | --- |
| … | … | … | belum dijalankan |

## Iterasi

| Putaran | Selisih yang ditemukan | Evidence baru | Perubahan |
| --- | --- | --- | --- |
| 1 | … | E… | … |
