# Font — sumber & lisensi

Empat berkas TTF di folder ini diturunkan dari paket npm **Fontsource**
(`@fontsource/bricolage-grotesque`, `@fontsource/fraunces`, `@fontsource/inter`),
bukan diunduh dari Google Fonts (CDN tidak dipakai).

| Berkas | Keluarga | Berat | Asal |
| --- | --- | --- | --- |
| `bricolage-grotesque-latin-800-normal.ttf` | Bricolage Grotesque | 800 | `@fontsource/bricolage-grotesque@5.3.0` |
| `fraunces-latin-300-normal.ttf` | Fraunces | 300 | `@fontsource/fraunces@5.3.0` |
| `fraunces-latin-700-normal.ttf` | Fraunces | 700 | `@fontsource/fraunces@5.3.0` |
| `inter-latin-400-normal.ttf` | Inter | 400 | `@fontsource/inter@5.3.0` |
| `inter-latin-500-normal.ttf` | Inter | 500 | `@fontsource/inter@5.3.0` |
| `inter-latin-600-normal.ttf` | Inter | 600 | `@fontsource/inter@5.3.0` |

Ketiganya berlisensi **SIL Open Font License 1.1** (OFL-1.1), boleh dipakai komersial,
boleh disematkan di produk, tidak boleh dijual sebagai font tersendiri.
Teks lisensi: https://openfontlicense.org/

Konversi `.woff2` → `.ttf` memakai `fontTools` + `brotli` (pypi), supaya Pillow bisa
membaca glyph untuk render video. Hanya subset Latin; aksara lain tidak disertakan.

**Catatan jujur:** video yang dirender `tools/render_film.py` memakai berkas ini, jadi
tipografinya benar-benar Bricolage/Fraunces/Inter — bukan font pengganti. Italic Fraunces
tidak tersedia di paket Fontsource, jadi `<em>` pada video tidak dimiringkan;
di halaman web italic tetap dipakai karena browser memiringkan sendiri.
