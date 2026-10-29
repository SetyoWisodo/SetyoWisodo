# Cara link di-resolve dan diverifikasi

Postingan memakai 40+ shortlink `t.co`, jadi URL aslinya tidak terlihat. Prosedur
di bawah dipakai untuk menghasilkan `resources.md`, dan bisa diulang kalau nanti
ada tautan yang bergeser.

## Batasan lingkungan

Di sandbox agent ini, akses `curl` langsung ke `t.co` **diblokir** (exit 35),
jadi redirect harus diikuti oleh layanan penengah lewat tool `fetch_page`.
Urutannya: coba resolver, cocokkan judul, baru catat.

## Langkah verifikasi per tautan

1. **Ambil metadata tujuan** dengan resolver yang mengikuti redirect HTTP:

   ```text
   https://api.microlink.io/?url=https%3A%2F%2Ft.co%2F<kode>&meta=true
   ```

   Field yang dipakai: `data.url` (URL akhir), `data.title`, `data.publisher`,
   `redirects[].url` (rantai redirect).

2. **Kalau `data.url` kosong atau tetap `t.co`**, ulangi dengan
   `&force=true`, lalu dengan `&meta=false&data.title.selector=title&data.title.attr=text`
   untuk memotong ukuran respons.

3. **Kalau masih gagal**, buka shortlink langsung dengan `fetch_page` pada
   `https://t.co/<kode>`; halaman yang dimuat menunjukkan URL akhir.

4. **Kalau dua langkah itu gagal** (mis. proteksi antibot YouTube), pakai rantai
   redirect dari header respons:

   ```text
   https://api.microlink.io/?url=https%3A%2F%2Ft.co%2F<kode>&meta=false&data.title.selector=title&data.title.attr=text
   ```

   Nilai `redirects[0].url` berisi URL kanonik (contoh: `youtube.com/watch?v=…`).

5. **Kalau URL akhir tetap tersembunyi** (halaman tanpa canonical, mis.
   `beginners.re`), cocokkan *sidik jari halaman*: judul, `content-length`,
   `server`, dan `last-modified` harus identik dengan URL kandidat yang diuji
   terpisah.

6. **Kalau tautan mendarat di beranda penerbit** (kasus Wiley), tandai `mati` dan
   jangan mengarang URL produk pengganti. Catat ISBN/nama buku sebagai jalur
   pencarian.

## Bukti yang harus disimpan

Untuk tiap baris di `resources.md`, simpan minimal: kode `t.co`, URL akhir, judul
halaman, tanggal verifikasi, dan status (`terverifikasi` / `terverifikasi (judul)`
/ `mati`). Tanpa judul, sebuah redirect belum membuktikan apa pun.

## Regenerasi cepat

```bash
# 1. ambil daftar shortlink dari teks postingan
# 2. untuk setiap kode:
for c in BWBmiQEwNo 4dIHc21mvJ xNXl6J9VCc; do
  printf '%s -> ' "$c"
  curl -s "https://api.microlink.io/?url=https%3A%2F%2Ft.co%2F$c&meta=true" \
    | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("data",{}).get("url"))'
done
```

Kalau `curl` ke internet tersedia, cara paling ringkas tetap
`curl -sI https://t.co/<kode> | grep -i location`.

## Sumber isi skill (bukan link postingan)

| Bagian | Asal | Commit/versi |
| --- | --- | --- |
| 5 skill REA | `morluto/rea` → `.agents/skills/` | `bf115be2cd900724a5bbd59a5cefc7af1dc2576f` |
| `references/installation.md` | `morluto/rea` → `docs/installation.md` | commit yang sama |
| `references/mcp-prompts.md` | `morluto/rea` → `docs/mcp-prompts.md` | commit yang sama |
| `find-reverse-engineered` | `alexgaoth/awesome-reverse-engineered` → `plugin/skills/` | branch `main`, MIT (Alex Gao) |
| `rea-agents` npm | `registry.npmjs.org/rea-agents` | 6.8.0 saat verifikasi |
