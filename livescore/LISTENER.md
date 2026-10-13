# Listener football-data.org → MongoDB

Listener adalah proses terpisah yang mengambil data pertandingan dari
[football-data.org](https://www.football-data.org/) (API v4), menormalisasinya,
lalu menulisnya ke koleksi `soccer_*` di MongoDB. API publik (`index.js`) hanya
membaca dari MongoDB dan tidak pernah memanggil penyedia data saat ada permintaan
pengguna. Aturan ini tertulis di `BUSINESS-CONTEXT.md` dan `UPSTREAM-LIVE-DATA.md`.

```
football-data.org  ──►  listener/ (fetch, validasi, normalisasi)  ──►  MongoDB soccer_*  ──►  API (index.js)
```

## Menjalankan

Persyaratan: Node.js 20+, MongoDB 6+, dan API key gratis dari football-data.org.

```bash
cd livescore
npm install
cp .env.example .env.development   # isi FOOTBALL_DATA_TOKEN dan MONGODB_URL
npm run db:init-live               # buat koleksi dan index (idempotent)
npm run listener                   # terminal 1: mengisi database
npm start                          # terminal 2: API di http://localhost:3050
```

Di produksi, `Procfile` sudah berisi dua proses: `web` (API) dan `listener`.

## Liga yang didukung

Didefinisikan di `listener/leagues.js`. Slug publik tetap stabil.

| Slug | Liga | Kode football-data |
| --- | --- | --- |
| `eng.1` | English Premier League | `PL` (id 2021) |
| `esp.1` | LaLiga | `PD` (id 2014) |

Tambah liga baru satu per satu sesuai rencana rollout di `BUSINESS-CONTEXT.md`,
dan pastikan token Anda punya akses ke kompetisi tersebut.

## Yang diambil dan kapan

| Resource | Sumber | Default | Catatan |
| --- | --- | --- | --- |
| Katalog liga | `/competitions/{code}` | 6 jam | Menentukan tahun musim |
| Klub dan skuad | `/competitions/{code}/teams` | 6 jam | Pelatih dan roster jika tersedia |
| Jadwal dan skor | `/competitions/{code}/matches` | 60 detik | Jendela: kemarin sampai 7 hari ke depan |
| Klasemen | `/competitions/{code}/standings` | 30 menit | Hanya tabel `TOTAL` |
| Kejadian | `/matches/{id}` | 60 detik | Gol, kartu, dan pergantian; pertandingan live diprioritaskan |

## Aturan keamanan data

- **Lease** per resource di `soccer_sync_states` mencegah dua proses bekerja bersamaan.
  Lease yang kedaluwarsa bisa diambil alih.
- **Validasi sebelum tulis.** Respons yang tidak sesuai bentuk tidak menghapus data lama.
  Contoh: klasemen kosong tidak menimpa klasemen yang sudah tersimpan.
- **Kegagalan dicatat** di `soccer_sync_states` (`status`, `error`, `consecutive_errors`).
  Proses tidak berhenti karena satu pertandingan gagal.
- **Idempotent.** Semua upsert memakai kunci unik dari kontrak
  (`source.provider` + `league_slug` + `source.event_id`, dan `source.event_key` untuk kejadian).
  Menjalankan ulang tidak menggandakan data.
- **Rate limit.** Semua request diantrekan dengan jarak minimum 6,5 detik. Respons 429
  dicoba ulang setelah 60 detik. Tier gratis sekitar 10 request per menit, jadi jika
  banyak pertandingan live bersamaan, sinkronisasi detail bisa tertunda.
- `play_by_play_available` hanya diset `true` setelah detail pertandingan berhasil diambil.

## Variabel environment

| Variabel | Default | Keterangan |
| --- | --- | --- |
| `FOOTBALL_DATA_TOKEN` | (wajib) | API key football-data.org |
| `MONGODB_URL` | `mongodb://localhost:27017/soccer` | Koneksi MongoDB |
| `LISTENER_LEAGUES` | `eng.1,esp.1` | Daftar slug, dipisah koma |
| `LISTENER_SCOREBOARD_MS` | `60000` | Interval jadwal dan skor |
| `LISTENER_DETAILS_MS` | `60000` | Interval kejadian |
| `LISTENER_STANDINGS_MS` | `1800000` | Interval klasemen |
| `LISTENER_CATALOG_MS` | `21600000` | Interval katalog dan klub |
| `FOOTBALL_DATA_MIN_INTERVAL_MS` | `6500` | Jarak minimum antar request |

## Pemetaan status

| football-data | Kontrak (`status.state`) | Keterangan |
| --- | --- | --- |
| `SCHEDULED`, `TIMED` | `pre` | |
| `IN_PLAY`, `LIVE` | `in` | Menit dihitung dari `minute` jika ada |
| `PAUSED` | `in` | `STATUS_HALFTIME` |
| `FINISHED`, `AWARDED` | `post` | `completed: true` |
| `POSTPONED`, `CANCELLED` | `pre` | Nama status membedakan keduanya |
| `SUSPENDED` | `in` | `suspended: true` |

## Seed musim lampau dari openfootball

Untuk mengisi riwayat musim yang sudah selesai (misalnya 2025-26) sebelum listener football-data
berjalan, pakai seeder. Sumber: [openfootball/football.json](https://github.com/openfootball/football.json)
dengan lisensi CC0 1.0 (domain publik).

```bash
# Dari GitHub raw (butuh akses ke raw.githubusercontent.com)
npm run seed:openfootball -- --season 2025-26 --leagues eng.1,esp.1

# Dari clone lokal (lebih cepat, dan bisa dipakai tanpa akses raw.githubusercontent.com)
git clone --depth 1 https://github.com/openfootball/football.json /tmp/fj
npm run seed:openfootball -- --season 2025-26 --dir /tmp/fj
```

Aturan:

- **Hanya musim lampau.** Seeder menolak musim yang sama atau lebih baru dari musim aktif di
  `soccer_leagues`. Liga harus sudah ada di database (jalankan listener katalog dulu).
- Jika tersedia, file `{code}-full.json` dipakai (ada gol dan kartu). Jika tidak, `{code}.json`
  (hanya skor).
- Pertandingan dengan skor selesai menjadi `post`, `postponed` menjadi `POSTPONED`, dan
  `canceled` menjadi `CANCELLED`. Jadwal tanpa skor dilewati.
- Jam tanpa penanda zona dihitung dari zona waktu liga. Jika jam tidak ada, kick-off diisi
  00:00 UTC dan catatan pada dokumen menyebutkannya.
- `source.provider` = `openfootball`. Pertandingan ini **tidak pernah** ikut diminta detailnya
  ke football-data.org (`findMatchesForDetails` hanya memilih `football-data`).
- Seed aman dijalankan ulang: ID pertandingan dan `event_key` bersifat deterministik.

Batasan data openfootball:

- Tidak ada ID klub. Tim diberi ID `of:{slug nama}`, sehingga tidak tercampur dengan klub football-data.
- Gol bunuh diri tidak ditandai di sumber, jadi tim yang tercatat bisa keliru untuk gol tersebut.
- Data tidak live dan tidak diperbarui otomatis. Pertandingan musim aktif tetap berasal dari football-data.

## Batasan yang perlu diketahui

- **Belum diuji terhadap API dan MongoDB sungguhan.** Lingkungan pengembangan tidak punya
  akses ke football-data.org maupun MongoDB. Yang sudah diuji: mapping payload, logika
  sinkronisasi (dengan store in-memory), throttle dan retry client, serta jalur error
  startup. Jalankan `npm run listener` dengan token Anda dan periksa `soccer_sync_states`.
- **Bentuk payload** mengikuti dokumentasi football-data.org v4 dan fixture di
  `test/listener.fixtures.js`. Jika ada field yang berbeda di respons nyata, sesuaikan
  `listener/mapper.js`.
- **Cakupan** hanya dua liga. Untuk "semua pertandingan dunia" perlu lisensi data dari
  penyedia yang mencakup liga tersebut, dan listener harus diperluas per liga.
- **Tim nasional dan turnamen** belum dipetakan (`kind: international` belum dipakai).
- **Pelatih dan roster** hanya tersedia jika penyedia mengirimkannya untuk tier token Anda.
- **Topskor liga** tidak tersedia, sesuai catatan di `BUSINESS-CONTEXT.md`.
