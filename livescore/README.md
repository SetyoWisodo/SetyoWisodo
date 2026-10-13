# ⚽ Skor Langsung — Live Score Sepakbola Dunia

Platform live score sepakbola: jadwal, skor langsung, dan kejadian pertandingan (gol, kartu, pergantian pemain) dari liga-liga di seluruh dunia, diperbarui secara realtime lewat Server-Sent Events (SSE).

Aplikasi ini **tanpa dependency eksternal** (Node.js 18+; uji dengan Node 22).

## Fitur

- **Jadwal per tanggal** dengan navigasi 7 hari (3 hari sebelum dan sesudah hari ini).
- **Live score realtime**: status (menit berjalan, HT, FT), skor, dan perubahan dikirim otomatis tanpa refresh.
- **Tab Live**, **Favorit** (tersimpan di browser), dan **pencarian** tim/liga/negara.
- **Pengelompokan per liga**; liga yang sedang live tampil lebih dulu.
- **Detail pertandingan**: skor paruh waktu, timeline gol, kartu, dan pergantian pemain.
- **Multi-provider**: data dari beberapa penyedia bisa digabung. Jika satu provider gagal, yang lain tetap tampil.
- **Ringan**: cache per tanggal, pembaruan SSE hanya mengirim pertandingan yang berubah.

## Menjalankan

```bash
cd livescore
npm start            # http://localhost:3000 (0.0.0.0:3000)
npm test             # 23 test: data, adapter, API, dan SSE
```

Variabel environment:

| Variabel | Default | Keterangan |
| --- | --- | --- |
| `PORT` | `3000` | Port HTTP |
| `HOST` | `0.0.0.0` | Alamat bind |
| `PROVIDERS` | `mock` | Daftar provider, dipisah koma: `mock`, `footballdata` |
| `FOOTBALL_DATA_TOKEN` | — | API key football-data.org (tier gratis tersedia) |
| `FOOTBALL_DATA_BASE` | `https://api.football-data.org/v4` | Opsional, untuk proxy atau mock server |

Contoh memakai data sungguhan:

```bash
PROVIDERS=footballdata FOOTBALL_DATA_TOKEN=xxxxx npm start
```

## Mode data

**Mode `mock` (default)** dibuat untuk pengembangan dan demo. Jadwal, status, dan skor dihasilkan secara deterministik dari waktu sekarang, sehingga pertandingan terlihat "berjalan" dan skornya bertambah. Nama tim adalah nama klub dan tim nasional nyata, tetapi **hasil pertandingannya bukan kenyataan**.

**Mode `footballdata`** memakai API football-data.org v4. Catatan:
- Tier gratis punya batas jumlah request dan cakupan kompetisi yang terbatas. Cache 60 detik membantu menjaga pemakaian.
- Adapter ini ditulis berdasarkan dokumentasi API. Belum diuji terhadap API langsung karena lingkungan pengembangan tidak punya akses ke host tersebut. Silakan uji dengan token Anda sendiri.

## Arsitektur

```
livescore/
├── public/            # Frontend (HTML, CSS, JS tanpa framework)
├── src/
│   ├── index.js       # Titik masuk (bind 0.0.0.0)
│   ├── app.js         # HTTP server, API, SSE, dan file statis
│   ├── aggregator.js  # Menggabungkan provider, isolasi kegagalan
│   ├── catalog.js     # Katalog liga untuk provider mock
│   ├── util.js
│   └── providers/
│       ├── index.js        # Pemilih provider dari environment
│       ├── mock.js         # Data simulasi deterministik
│       └── footballData.js # Adapter football-data.org + normalisasi
└── test/              # node:test
```

### API

| Method | Path | Keterangan |
| --- | --- | --- |
| GET | `/api/health` | Status dan provider aktif |
| GET | `/api/matches?date=YYYY-MM-DD[&status=live]` | Daftar pertandingan (tanpa kejadian) |
| GET | `/api/matches/:id` | Detail pertandingan termasuk kejadian |
| GET | `/api/stream?date=YYYY-MM-DD` | SSE: `hello` lalu `update` berisi pertandingan yang berubah |

Contoh event SSE:

```json
{"type":"update","date":"2026-10-13","at":"2026-10-13T10:12:00.000Z","matches":[{"id":"mock:epl:2026-10-13:0","status":"LIVE","minute":11,"score":{"home":1,"away":0}}]}
```

### Menambah provider

Provider cukup memenuhi kontrak ini:

```js
{
  name: 'nama-provider',
  owns: (id) => id.startsWith('prefix:'),      // menentukan provider untuk id detail
  async getMatches(dateKey, { now }) { /* -> Match[] */ },
  async getMatch(id, { now }) { /* -> Match | null */ },
}
```

Model `Match` ada di `src/providers/footballData.js` (`normalizeFdMatch`) dan `src/providers/mock.js`. Status yang dipakai: `SCHEDULED`, `LIVE`, `HALF_TIME`, `FINISHED`, `POSTPONED`, `SUSPENDED`, `CANCELLED`.

## Catatan penting: data, lisensi, dan skala

- **Data live adalah bagian paling mahal.** Kode bisa ditulis dalam hitungan hari, tetapi data pertandingan dunia yang akurat dan cepat berasal dari penyedia berlisensi. Pastikan kontrak dan ketentuan penggunaannya mengizinkan penayangan di platform Anda.
- **Jangan melakukan scraping** dari situs live score lain. Itu melanggar ketentuan layanan dan hak database mereka.
- Untuk bersaing dengan layanan besar seperti LiveScore, fokus pada cakupan liga, kecepatan update (idealnya push, bukan polling), aplikasi mobile, notifikasi gol, dan keandalan saat trafik tinggi.

### Langkah berikutnya menuju skala produksi

1. Simpan data di database (PostgreSQL) dan ingest dari provider lewat worker terpisah.
2. Ganti SSE per-instance dengan pub/sub (Redis) agar bisa di-scale horizontal.
3. Cache di CDN untuk endpoint jadwal; SSE/WebSocket hanya untuk pertandingan live.
4. Aplikasi mobile (PWA atau React Native) dan notifikasi push gol.
5. Observabilitas (metrik latensi update, error provider) dan rate limiting.
