# Atribusi dan Lisensi

Folder `livescore/` berisi kode dari proyek open-source berikut:

- Sumber: https://github.com/rezarahiminia/livescoreFootball
- Commit yang disalin: `8581d29fae6ce71f093c34cf07c5c93f602826ce` (branch `main`)
- Penulis pada `package.json`: jp2435
- Lisensi: ISC (tercantum di `package.json`; repo asal tidak menyertakan file LICENSE terpisah)

Kode di bawah lisensi ISC berikut, sesuai teks lisensi asalnya:

```
ISC License

Copyright (c) the authors of rezarahiminia/livescoreFootball

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

Modifikasi yang ditambahkan di atas kode asal:

- Folder `listener/`: pengambil data dari football-data.org (lisensi/ketentuan penggunaan
  API tersebut berlaku terpisah dan harus dipatuhi).
- Test untuk listener di `test/listener.*.test.js`.
- Entri `listener` di `Procfile` dan `package.json`, serta variabel baru di `.env.example`.

Jika Anda memakai kode ini secara komersial, pastikan juga ketentuan penggunaan data dari
penyedia (football-data.org) dipenuhi, termasuk atribusi dan batas penggunaan.
