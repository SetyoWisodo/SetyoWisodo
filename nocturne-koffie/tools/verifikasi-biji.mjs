/**
 * Verifikasi biji kopi beranda — tanpa peramban, tanpa dependensi.
 *
 *   node tools/verifikasi-biji.mjs
 *
 * Yang diperiksa (versi 2, 5 Nov 2026 — render hiper-realistis, bukan mesh WebGL):
 *   1. berkas wajib ada dan poster benar-benar JPEG 4:5
 *   2. skrip membaca data lewat fetch, bukan menulis angka sendiri
 *   3. setiap zona punya titik_foto dua angka 0–100
 *   4. tidak ada titik yang menumpuk atau keluar dari gambar
 *   5. tombol di HTML cocok satu-satu dengan zona di data
 *   6. urutan & aria-label tombol menyebut nama zona yang benar
 *   7. <details> 6 zona tetap ada untuk pembaca tanpa JavaScript
 *   8. jalur prefers-reduced-motion ada di CSS maupun JS
 *   9. tanpa pustaka 3D dari CDN, tanpa sisa jalur WebGL
 *  10. catatan kejujuran menyebut render, bukan pindai
 *
 * Keluaran: laporan/biji-verifikasi.json (berisi sidik sha256 supaya
 * periksa.py bisa menolak laporan yang basi).
 */
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const baca = (rel) => readFileSync(join(ROOT, rel), 'utf8');
const bacaBin = (rel) => readFileSync(join(ROOT, rel));
const ada = (rel) => existsSync(join(ROOT, rel));

const butir = [];
const cek = (nama, ok, detail = '') => butir.push({ nama, ok: !!ok, detail });

/* ── 1 · berkas wajib ─────────────────────────────────────────────── */
const WAJIB = [
  'data/biji3d.json',
  'assets/js/biji3d.js',
  'assets/css/biji.css',
  'assets/img/biji-3d-poster.jpg',
  'index.html',
  'laporan/biji-render.json'
];
const hilang = WAJIB.filter((f) => !ada(f));
cek('Berkas wajib ada', hilang.length === 0, hilang.length ? 'hilang: ' + hilang.join(', ') : `${WAJIB.length} berkas lengkap`);

/* poster: JPEG 4:5, ukuran wajar */
let posterOk = false;
let posterDetail = 'poster tidak ada';
if (ada('assets/img/biji-3d-poster.jpg')) {
  const buf = bacaBin('assets/img/biji-3d-poster.jpg');
  const jpeg = buf[0] === 0xff && buf[1] === 0xd8;
  const kb = Math.round(buf.length / 1024);
  /* ukuran piksel: cari marker SOF0/SOF2 (0xFFC0-0xFFCF) */
  let lebar = 0, tinggi = 0;
  for (let i = 2; i < buf.length - 9; i++) {
    if (buf[i] === 0xff && buf[i + 1] >= 0xc0 && buf[i + 1] <= 0xcf && buf[i + 1] !== 0xc4 && buf[i + 1] !== 0xc8 && buf[i + 1] !== 0xcc) {
      tinggi = buf.readUInt16BE(i + 5);
      lebar = buf.readUInt16BE(i + 7);
      break;
    }
  }
  posterOk = jpeg && lebar === 640 && tinggi === 800 && kb < 300;
  posterDetail = `${jpeg ? 'JPEG' : 'bukan JPEG'} ${lebar}×${tinggi} · ${kb} KB`;
}
cek('Poster JPEG 4:5 · 640×800', posterOk, posterDetail);

/* ── 2 · data ─────────────────────────────────────────────────────── */
const data = JSON.parse(baca('data/biji3d.json'));
const js = baca('assets/js/biji3d.js');
const idx = baca('index.html');
const css = baca('assets/css/biji.css');
const zona = data.zona || [];

cek('Skrip membaca data (fetch)', js.includes('fetch(') && js.includes('titik_foto'),
  js.includes('titik_foto') ? 'fetch + titik_foto dipakai' : 'titik_foto tidak dipakai');

/* ── 3 · titik_foto ───────────────────────────────────────────────── */
const tanpaTitik = zona.filter((z) => !Array.isArray(z.titik_foto) || z.titik_foto.length !== 2);
const luar = zona.filter((z) => Array.isArray(z.titik_foto) &&
  (z.titik_foto[0] < 5 || z.titik_foto[0] > 95 || z.titik_foto[1] < 5 || z.titik_foto[1] > 95));
cek('Setiap zona punya titik_foto', tanpaTitik.length === 0,
  tanpaTitik.length ? 'tanpa titik: ' + tanpaTitik.map((z) => z.id).join(', ') : `${zona.length} zona`);
cek('Titik di dalam bingkai', luar.length === 0,
  luar.length ? 'keluar: ' + luar.map((z) => z.id).join(', ') : 'semua 5–95%');

/* ── 4 · jarak antar titik ────────────────────────────────────────── */
let rapat = '';
for (let i = 0; i < zona.length; i++) {
  for (let j = i + 1; j < zona.length; j++) {
    const a = zona[i].titik_foto, b = zona[j].titik_foto;
    const d = Math.hypot(a[0] - b[0], (a[1] - b[1]) * 0.8);
    if (d < 8) rapat += `${zona[i].id}–${zona[j].id} (${d.toFixed(1)}%) `;
  }
}
cek('Titik tidak menumpuk', rapat === '', rapat || 'jarak semua ≥ 8%');

/* ── 5 · tombol HTML ↔ zona ───────────────────────────────────────── */
const idsData = zona.map((z) => z.id).sort();
const idsHtml = [...idx.matchAll(/data-biji-titik="([^"]+)"/g)].map((m) => m[1]).sort();
cek('Tombol HTML = zona data', JSON.stringify(idsData) === JSON.stringify(idsHtml),
  `${idsHtml.length} tombol · ${idsData.length} zona`);

/* ── 6 · urutan & label tombol ────────────────────────────────────── */
const urutan = [...idx.matchAll(/aria-label="Titik (\d+): ([^—]+)—/g)];
const cocokUrut = urutan.length === zona.length &&
  urutan.every((m, i) => Number(m[1]) === i + 1 && zona[i].nama.toLowerCase().startsWith(m[2].trim().toLowerCase().split(' ')[0]));
cek('Label tombol menyebut zona berurutan', cocokUrut,
  urutan.map((m) => `${m[1]}=${m[2].trim()}`).join(' · ') || 'pola aria-label tidak ditemukan');

/* ── 7 · tanpa JavaScript tetap terbaca ───────────────────────────── */
const blokDetail = (idx.match(/data-biji-zona="/g) || []).length;
cek('<details> 6 zona tanpa JS', blokDetail === zona.length && idx.includes('<details'),
  `${blokDetail} blok zona di <details>`);

/* ── 8 · reduced motion ───────────────────────────────────────────── */
cek('Hormat prefers-reduced-motion', css.includes('prefers-reduced-motion') && js.toLowerCase().includes('reduced'),
  'CSS + JS');

/* ── 9 · tanpa CDN / sisa WebGL ───────────────────────────────────── */
const cdn = ['three.min.js', 'three.module', 'cdn.jsdelivr', 'unpkg.com', 'skypack'];
const kenaCdn = cdn.filter((p) => idx.includes(p) || js.includes(p));
const sisaWebgl = js.includes('getContext(') || idx.includes('data-biji-kanvas');
cek('Tanpa pustaka 3D / sisa WebGL', kenaCdn.length === 0 && !sisaWebgl,
  kenaCdn.length ? 'CDN: ' + kenaCdn.join(', ') : (sisaWebgl ? 'masih ada jalur kanvas' : 'bersih'));

/* ── 10 · kejujuran ───────────────────────────────────────────────── */
const jujur = /render 3D/i.test(idx) && /bukan hasil pindai/i.test(idx);
cek('Catatan kejujuran tampil', jujur, jujur ? 'menyebut render 3D, bukan pindai' : 'catatan tidak sesuai');

/* ── keluaran ─────────────────────────────────────────────────────── */
const sidik = createHash('sha256')
  .update(baca('data/biji3d.json'))
  .update(baca('assets/js/biji3d.js'))
  .update(bacaBin('assets/img/biji-3d-poster.jpg'))
  .digest('hex')
  .slice(0, 16);

const lolos = butir.filter((b) => b.ok).length;
const gagal = butir.length - lolos;

for (const b of butir) {
  console.log(`  ${b.ok ? 'OK ' : 'XX '}  ${b.nama.padEnd(32)} ${b.detail}`);
}
console.log(`\n  ${lolos} lolos · ${gagal} gagal`);
console.log('  Catatan: ini memeriksa data, gambar, dan markup — bukan hasil render di peramban.');

writeFileSync(
  join(ROOT, 'laporan/biji-verifikasi.json'),
  JSON.stringify({
    dibuat: new Date().toISOString().slice(0, 10),
    sidik,
    lolos,
    gagal,
    poster: { berkas: 'assets/img/biji-3d-poster.jpg', ukuran_kb: Math.round(statSync(join(ROOT, 'assets/img/biji-3d-poster.jpg')).size / 1024) },
    butir
  }, null, 2) + '\n',
  'utf8'
);

process.exit(gagal ? 1 : 0);
