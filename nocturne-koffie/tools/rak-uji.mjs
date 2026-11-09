/**
 * Uji asap untuk hero rak (`rak/index.html`) tanpa peramban.
 *
 * Kenapa ada berkas ini: halaman ini tidak bisa saya buka di peramban (tidak ada
 * Chromium di sandbox, dan tidak boleh memasang apa pun di mesin pemilik tanpa
 * izin). Yang bisa diperiksa tanpa peramban tetap banyak, dan tiga kesalahan
 * paling mahal di halaman seperti ini semuanya tertangkap di sini:
 *
 *   1. galat saat jalan (nama elemen salah, TDZ, fungsi hilang) — dulu baru
 *      ketahuan saat halaman dibuka;
 *   2. geometri salah: jarak antar punggung harus `ws + gap`, kotak aktif harus
 *      berputar −90° dengan kemiringan −4,5°;
 *   3. sambungan tidak jalan: panah, tab, klik punggung, klik sampul, Escape.
 *
 * Yang TIDAK diperiksa (dan tidak bisa diklaim): tampilan sungguhan — perspektif
 * 3D, bayangan, ketajaman teks. Itu hanya bisa dinilai mata di peramban.
 *
 * Pakai:
 *   npm i jsdom --prefix /tmp/jsdom      # sekali, di luar repo
 *   node tools/rak-uji.mjs [--verbose]
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const verbose = process.argv.includes('--verbose');

const kandidat = [
  '/tmp/jsdom/node_modules/jsdom/lib/api.js',
  path.join(ROOT, 'node_modules/jsdom/lib/api.js'),
];
const jalurJsdom = process.env.JSDOM_PATH || kandidat.find((p) => fs.existsSync(p));
if (!jalurJsdom) {
  console.error('jsdom tidak ditemukan. Jalankan: npm i jsdom --prefix /tmp/jsdom');
  process.exit(2);
}
const { JSDOM } = createRequire(import.meta.url)(jalurJsdom);

const html = fs.readFileSync(path.join(ROOT, 'rak/index.html'), 'utf8');
const dataJs = fs.readFileSync(path.join(ROOT, 'rak/data.js'), 'utf8');
const rakJs = fs.readFileSync(path.join(ROOT, 'rak/rak.js'), 'utf8');

// buang <script src> (jsdom tidak memuat berkas), sisipkan isinya
const berkas = html
  .replace(/<script src="data\.js"><\/script>/, `<script>${dataJs}</script>`)
  .replace(/<script src="rak\.js"><\/script>/, `<script>${rakJs}</script>`);

const masalah = [];
const catat = (ok, teks, detail = '') => {
  if (!ok) masalah.push(teks + (detail ? ` — ${detail}` : ''));
  if (verbose || !ok) console.log(`  ${ok ? 'OK' : 'XX'} ${teks}${detail ? ' · ' + detail : ''}`);
  return ok;
};

// ---------------------------------------------------------------- stub ---
let rafQueue = [];
let waktu = performance.now();   // jam yang sama dengan rAF di peramban
const animasi = [];

const dom = new JSDOM(berkas, {
  runScripts: 'dangerously',
  url: 'https://nocturnekoffie.id/rak/',
  pretendToBeVisual: false,
  beforeParse(window) {
    window.innerWidth = 1440;
    window.innerHeight = 900;
    Object.defineProperty(window, 'matchMedia', {
      value: () => ({ matches: false, addEventListener() {}, removeEventListener() {} }),
    });
    // satu jam untuk semuanya: rAF, performance.now(), dan animasi
    Object.defineProperty(window.performance, 'now', { value: () => waktu });
    window.requestAnimationFrame = (cb) => { rafQueue.push(cb); return rafQueue.length; };
    window.cancelAnimationFrame = () => {};
    window.Element.prototype.animate = function (frames, opt) {
      const a = {
        frames, opt, onfinish: null, _batal: false, _id: setImmediate,
        cancel() { this._batal = true; if (this._timer) clearTimeout(this._timer); },
        finish() {},
      };
      animasi.push(a);
      const durasi = (opt && opt.duration) || 0;
      const tunda = (opt && opt.delay) || 0;
      a._timer = setTimeout(() => { if (!a._batal && a.onfinish) a.onfinish(); }, tunda + durasi);
      return a;
    };
    window.HTMLElement.prototype.setPointerCapture = function () {};
    window.Element.prototype.getAnimations = function () { return animasi.filter((a) => !a._batal); };
    window.HTMLElement.prototype.releasePointerCapture = function () {};
    window.Element.prototype.getBoundingClientRect = function () {
      const w = 218, h = 414;
      return { x: 611, y: 243, left: 611, top: 243, right: 611 + w, bottom: 243 + h, width: w, height: h };
    };
    Object.defineProperty(window.HTMLElement.prototype, 'offsetHeight', {
      get() { return /var\(--H\)/.test(this.style.height || '') ? 414 : 100; },
    });
    Object.defineProperty(window.HTMLElement.prototype, 'offsetWidth', {
      get() { return this.classList && this.classList.contains('tab') ? 90 : 100; },
    });
    Object.defineProperty(window.HTMLElement.prototype, 'offsetLeft', {
      get() { return this.dataset && this.dataset.tab ? this.dataset.tab.length * 40 : 0; },
    });
    window.addEventListener('error', (e) => masalah.push('galat JS: ' + e.message));
  },
});

const { window } = dom;
const doc = window.document;
const langkah = (n = 1, dt = 16) => {
  for (let i = 0; i < n; i++) {
    waktu += dt;
    const q = rafQueue; rafQueue = [];
    for (const cb of q) cb(waktu);
  }
};
const tunggu = (ms = 30) => new Promise((r) => setTimeout(r, ms));
const teks = (sel) => {
  const el = doc.querySelector(sel);
  if (!el) return '';
  const baris = el.querySelectorAll('.line');
  return (baris.length ? baris[baris.length - 1].textContent : el.textContent).trim();
};
const angka = (t, nama) => {
  const m = new RegExp(nama + '\\(([-\\d.]+)').exec(t || '');
  return m ? parseFloat(m[1]) : NaN;
};

// ---------------------------------------------------------------- uji ---
await tunggu(20);
langkah(3);

const R = window.RAK;
catat(!!R, 'window.RAK tersedia');
const jumlahKotak = doc.querySelectorAll('.tape').length;
// Jumlah kotak mengikuti data (9 kemasan × 3 salinan = 27); dulu dipaku 36
// karena rak berisi 12 kaset. Yang penting: tiga salinan per lot, tidak kurang.
const harapKotak = R.ITEMS.length * 3;
catat(jumlahKotak === harapKotak, `${R.ITEMS.length} lot × 3 salinan = ${harapKotak} kotak`,
  String(jumlahKotak));
catat(doc.querySelectorAll('.tape .sp').length === harapKotak &&
      doc.querySelectorAll('.tape .cv').length === harapKotak,
  'tiap kotak punya dua sisi (sisi gusset + muka stiker)');
catat(doc.querySelectorAll('.tab').length === R.TABS.length, 'tab dibangun dari data',
  `${doc.querySelectorAll('.tab').length} tab`);

// geometri: jarak antar kotak = ws + gap
// rasio muka dari data (kemasan 500 g), bukan angka kaset yang dipaku di uji
const FACE = R.FACE || { cv: 474 / 900, sp: 142 / 840 };
const ws = 414 * FACE.sp, gap = 414 * 0.03, d = 414 * FACE.cv;
const posisi = Array.from(doc.querySelectorAll('.tape'))
  .map((el) => ({ x: angka(el.style.transform, 'translate3d'), vis: el.style.visibility }))
  .filter((p) => p.vis !== 'hidden')
  .map((p) => p.x)
  .sort((a, b) => a - b);
catat(posisi.length >= 10, 'minimal 10 kotak terlihat pada 1440 px', String(posisi.length));
let jarakSalah = 0;
for (let i = 1; i < posisi.length; i++) {
  const jarak = posisi[i] - posisi[i - 1];
  // di sekitar kotak aktif, tetangga terdorong setengah lebar sampul
  const dekat = Math.abs(posisi[i]) < d || Math.abs(posisi[i - 1]) < d;
  const harap = dekat ? ws + gap + (d - ws) * 0.9 : ws + gap;
  if (jarak < 0.9 * (ws + gap) || jarak > harap + 1) jarakSalah++;
}
catat(jarakSalah === 0, 'jarak punggung = lebar punggung + celah, melebar di kotak aktif',
  `${jarakSalah} jarak menyimpang`);

// kotak aktif: berputar −90° dengan kemiringan −4,5°
const aktifEl = Array.from(doc.querySelectorAll('.tape'))
  .filter((el) => el.style.transform.includes('translate3d'))
  .map((el) => ({ el, x: Math.abs(angka(el.style.transform, 'translate3d')) }))
  .sort((a, b) => a.x - b.x)[0].el;
const tf = aktifEl.style.transform;
const rotY = angka(tf, 'rotateY'), rotZ = angka(tf, 'rotateZ'), rotX = angka(tf, 'rotateX');
catat(Math.abs(rotY + 90) < 2, 'kotak aktif berputar −90° (sampul menghadap kita)', `${rotY}°`);
catat(Math.abs(rotZ + 4.5) < 0.2, 'kotak aktif miring −4,5°', `${rotZ}°`);
catat(Math.abs(rotX) < 1, 'kotak aktif nyaris tegak', `${rotX}°`);
catat(/translate3d\(0\.00px/.test(tf) || Math.abs(angka(tf, 'translate3d')) < 1,
  'kotak aktif tepat di tengah');

// judul awal = item ke-5 (Raung)
catat(teks('.cap__title') === R.ITEMS[R.START].name, 'judul awal dari START',
  `${teks('.cap__title')} vs ${R.ITEMS[R.START].name}`);
catat(teks('.cap__meta') === R.ITEMS[R.START].meta, 'baris meta awal ikut');
catat(doc.querySelector('.tab.is-on')?.dataset.tab === R.ITEMS[R.START].tab,
  'tab aktif = kategori lot pertama');

// panah kanan: rak bergeser & judul berganti
doc.querySelector('#next').click();
langkah(120);
catat(teks('.cap__title') === R.ITEMS[R.START + 1].name, 'panah kanan memajukan satu lot',
  `${teks('.cap__title')}`);

// tab: lompat ke lot pertama kategori "robusta"
const firstRobusta = R.ITEMS.findIndex((x) => x.tab === 'robusta');
doc.querySelector('.tab[data-tab="robusta"]').click();
langkah(160);
catat(teks('.cap__title') === R.ITEMS[firstRobusta].name, 'tab melompat ke lot pertama kategori',
  `${teks('.cap__title')} vs ${R.ITEMS[firstRobusta].name}`);
catat(doc.querySelector('.tab.is-on')?.dataset.tab === 'robusta', 'tab robusta menyala');

// buka detail dari tombol putar
langkah(80);
doc.querySelector('#ring').click();
await tunggu(20);
catat(doc.querySelector('#detail').style.visibility === 'visible', 'detail terbuka');
catat(teks('#dTitle') === R.ITEMS[firstRobusta].name, 'judul detail = lot aktif', teks('#dTitle'));
catat(/Rp\d/.test(teks('#dHarga')), 'harga di detail berasal dari katalog', teks('#dHarga').slice(0, 60));
const href = doc.querySelector('#dCta').getAttribute('href') || '';
catat(href.startsWith('https://wa.me/628988188800'), 'tombol pesan menuju WhatsApp resmi', href.slice(0, 60));
catat(/%20/.test(href) && href.includes(encodeURIComponent(R.ITEMS[firstRobusta].name).slice(0, 6)),
  'pesan WhatsApp menyebut nama lot');
const img = doc.querySelector('#pimg');
catat(!!img.getAttribute('href') && !/NaN|Infinity/.test(img.getAttribute('width')),
  'gambar poster memakai potongan atlas', `${img.getAttribute('x')} ${img.getAttribute('width')}`);
const csel = doc.querySelectorAll('#blobs circle');
catat(csel.length === 7, 'tujuh bulatan tinta di poster');
langkah(90, 20);
const jariJari = Array.from(csel).map((c) => parseFloat(c.getAttribute('r')));
catat(jariJari.some((r) => r > 0), 'tinta mulai menyebar', jariJari.map((r) => r.toFixed(0)).join(','));

// Escape menutup
doc.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
await tunggu(1000);
catat(doc.querySelector('#detail').style.visibility === 'hidden', 'Escape menutup lembar');

// roda & geser tidak melempar galat
window.dispatchEvent(new window.WheelEvent('wheel', { deltaY: 240 }));
langkah(60);
catat(true, 'roda mouse tidak melempar galat');

// ------------------------------------------------------------- kesimpulan ---
langkah(1);
const gagal = masalah.length;
console.log(`\n  ${gagal ? 'XX' : 'OK'} rak/index.html · ${gagal ? gagal + ' gagal' : 'semua butir lolos'} · ` +
  `${doc.querySelectorAll('.tape').length} kotak · jsdom (tanpa peramban)`);
if (gagal) {
  for (const m of masalah) console.log('   -', m);
  process.exit(1);
}
console.log('  Catatan: uji ini memeriksa skrip, geometri, dan sambungan — bukan tampilan.');
window.close();
