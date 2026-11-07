/**
 * Uji potong-buka (`cutaway/index.html`) tanpa peramban.
 *
 * Yang diperiksa di sini adalah bagian metode Cutaway yang bisa dibuktikan
 * dengan angka — bukan tampilan:
 *
 *   1. render(t) murni: t yang sama → hasil yang sama, tanpa Math.random/Date;
 *   2. setiap ketukan punya kamera sendiri (tidak ada ketukan yang parkir);
 *   3. bukaan bagian: 0 → 1 → 0 mengikuti pelat waktu, tidak "nyangkut";
 *   4. loop mulus: frame 0 = frame 22 s;
 *   5. sambungan: 7 tombol bagian, kartu berganti, rel bisa digeser;
 *   6. ceklis 12 baris ada dan angkanya sama dengan data.js.
 *
 * Yang TIDAK diperiksa dan tidak boleh diklaim: film 60 fps. Sandbox ini tidak
 * punya Chromium maupun ffmpeg, jadi tidak ada satu pun frame yang dirender
 * jadi gambar di sini.
 *
 *   node tools/cutaway-uji.mjs [--verbose]
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const verbose = process.argv.includes('--verbose');

const kandidat = ['/tmp/jsdom/node_modules/jsdom/lib/api.js', path.join(ROOT, 'node_modules/jsdom/lib/api.js')];
const jalurJsdom = process.env.JSDOM_PATH || kandidat.find((p) => fs.existsSync(p));
if (!jalurJsdom) {
  console.error('jsdom tidak ditemukan. Jalankan: npm i jsdom --prefix /tmp/jsdom');
  process.exit(2);
}
const { JSDOM } = createRequire(import.meta.url)(jalurJsdom);

const masalah = [];
const catat = (ok, teks, detail = '') => {
  if (!ok) masalah.push(teks + (detail ? ` — ${detail}` : ''));
  if (verbose || !ok) console.log(`  ${ok ? 'OK' : 'XX'} ${teks}${detail ? ' · ' + detail : ''}`);
  return ok;
};

const html = fs.readFileSync(path.join(ROOT, 'cutaway/index.html'), 'utf8');
const dataJs = fs.readFileSync(path.join(ROOT, 'cutaway/data.js'), 'utf8');
const kodeJs = fs.readFileSync(path.join(ROOT, 'cutaway/cutaway.js'), 'utf8');
const kodeCss = fs.readFileSync(path.join(ROOT, 'cutaway/cutaway.css'), 'utf8');

const berkas = html
  .replace(/<script src="data\.js"><\/script>/, `<script>${dataJs}</script>`)
  .replace(/<script src="cutaway\.js"><\/script>/, `<script>${kodeJs}</script>`);

let rafQueue = [];
let waktu = 0;
const dom = new JSDOM(berkas, {
  runScripts: 'dangerously',
  url: 'https://nocturnekoffie.id/cutaway/',
  pretendToBeVisual: false,
  beforeParse(window) {
    window.innerWidth = 1440;
    window.innerHeight = 900;
    Object.defineProperty(window.performance, 'now', { value: () => waktu });
    Object.defineProperty(window, 'matchMedia', {
      value: () => ({ matches: false, addEventListener() {}, removeEventListener() {} }),
    });
    window.requestAnimationFrame = (cb) => { rafQueue.push(cb); return rafQueue.length; };
    window.cancelAnimationFrame = () => {};
    window.Element.prototype.setPointerCapture = function () {};
    window.Element.prototype.releasePointerCapture = function () {};
    window.Element.prototype.getBoundingClientRect = function () {
      const lebar = this.id === 'rel' ? 800 : 100;
      return { x: 0, y: 0, left: 0, top: 0, right: lebar, bottom: 22, width: lebar, height: 22 };
    };
    window.addEventListener('error', (e) => masalah.push('galat JS: ' + e.message));
  },
});

const { window } = dom;
const doc = window.document;
const D = window.CUTAWAY;
const R = window.CUTAWAY_RENDER;
const langkah = (n = 1, dt = 16) => {
  for (let i = 0; i < n; i++) {
    waktu += dt;
    const q = rafQueue; rafQueue = [];
    for (const cb of q) cb(waktu);
  }
};

// ---------------------------------------------------------------- 1. data ---
catat(!!D, 'cutaway/data.js termuat');
catat(!!R, 'cutaway.js memasang CUTAWAY_RENDER (bisa diuji tanpa layar)');
catat(D.BAGIAN.length === 7, '7 bagian', String(D.BAGIAN.length));
catat(D.KETUKAN.length === 9, '9 ketukan', String(D.KETUKAN.length));
catat(Object.keys(D.KAMERA).length === D.KETUKAN.length, 'kamera = jumlah ketukan',
  String(Object.keys(D.KAMERA).length));
catat(D.DURASI === 25, 'film 25 s', String(D.DURASI));
catat(D.KETUKAN.every((k) => k.selesai - k.mulai >= 2 && k.selesai - k.mulai <= 3),
  'setiap ketukan 2–3 s (selera dengan angka)');
catat(D.CEKLIS.length >= 10 && D.CEKLIS.length <= 12, 'ceklis 10–12 baris', String(D.CEKLIS.length));
catat(D.CEKLIS.every((c) => /^\d+\./.test(c)), 'setiap baris ceklis bernomor');
catat(D.CEKLIS.some((c) => c.includes('NEVER')), 'ceklis memuat "NEVER" (aturan metode)');

// ------------------------------------------------------------- 2. kemurnian ---
// cek pada kode saja: komentar dibuang dulu (komentar menyebut aturannya, bukan melanggarnya)
const tanpaKomentar = (s) => s
  .replace(/\/\*[\s\S]*?\*\//g, '')
  .split('\n').filter((l) => !/^\s*(\/\/|\*)/.test(l)).join('\n');
const js = tanpaKomentar(kodeJs);
const css = tanpaKomentar(kodeCss);
catat(!/Math\.random/.test(js), 'cutaway.js tanpa Math.random');
catat(!/Date\.now|new Date/.test(js), 'cutaway.js tanpa Date');
catat(!/@keyframes/.test(css), 'cutaway.css tanpa @keyframes (gerak hanya dari t)');

const a = R(3.7);
const b = R(3.7);
catat(JSON.stringify(a) === JSON.stringify(b), 'render(3.7) dua kali → hasil identik (murni)');
const urutan = [0, 3.7, 11.2, 3.7, 0].map((t) => JSON.stringify(R(t)));
catat(urutan[1] === urutan[3] && urutan[0] === urutan[4], 'urutan panggilan tidak mengubah hasil');

const t0 = R(0).kamera;
const tH = R(0.5).kamera;
catat(t0.ry !== tH.ry || t0.rx !== tH.rx, 'frame 0 sudah bergerak (bukan pose diam)');
catat(Math.abs(R(0).kamera.zoom - 1) < 0.02, 'frame 0 = sampul: zoom 1,00', String(R(0).kamera.zoom));

// ----------------------------------------------------------- 3. loop mulus ---
const awal = JSON.stringify(R(0));
const akhir = JSON.stringify(R(D.DURASI));
catat(awal === akhir, 'frame 0 = frame ' + D.DURASI + ' s (loop tanpa lompat)');

// ------------------------------------------------ 4. satu kamera per ketukan ---
const nilai = new Set(Object.values(D.KAMERA).map((k) => `${k.ry}|${k.rx}|${k.zoom}`));
catat(nilai.size === D.KETUKAN.length, 'setiap ketukan punya kamera sendiri',
  `${nilai.size} dari ${D.KETUKAN.length}`);
const posisi = D.KETUKAN.map((k) => {
  const s = R(k.mulai + 1.6);
  return `${s.kamera.ry.toFixed(2)}|${s.kamera.rx.toFixed(2)}|${s.kamera.zoom.toFixed(3)}`;
});
catat(new Set(posisi).size === D.KETUKAN.length, 'kamera benar-benar berpindah saat film berjalan',
  `${new Set(posisi).size} sudut unik`);

// ------------------------------------------------------------- 5. bukaan ---
let bukaOk = true;
for (const k of D.KETUKAN) {
  if (!k.bagian) continue;
  const tengah = R((k.mulai + k.selesai) / 2).bukaan[k.bagian];
  const luar = R(k.mulai - 0.05 > 0 ? k.mulai - 0.05 : 0).bukaan[k.bagian];
  if (tengah < 0.99) { bukaOk = false; catat(false, `${k.bagian}: tidak terbuka penuh di tengah ketukan`, String(tengah)); }
  if (luar > 0.01 && k.mulai > 0.1) { bukaOk = false; catat(false, `${k.bagian}: sudah terbuka sebelum ketukan`, String(luar)); }
}
catat(bukaOk, 'setiap bagian buka penuh di ketukannya, tertutup di luar ketukan');
catat(D.KETUKAN.filter((k) => !k.bagian).length === 2, '2 ketukan tanpa bagian (sampul & tutup)', String(D.KETUKAN.filter((k) => !k.bagian).length));
catat(new Set(D.KETUKAN.filter((k) => k.bagian).map((k) => k.bagian)).size === 7,
  'ketujuh bagian punya ketukan sendiri');
// panel depan harus ikut bergeser saat isi sangrai ditampilkan
const tb = D.KETUKAN.find((k) => k.bagian === 'biji');
const sBiji = R((tb.mulai + tb.selesai) / 2);
catat(sBiji.bukaan.badan > 0.9, 'panel depan disingkirkan saat isi sangrai tampil',
  String(sBiji.bukaan.badan));
const tutup = R(D.DURASI - 0.02).bukaan;
catat(Object.values(tutup).every((v) => v < 0.02), 'semua bagian tertutup di akhir film');

// ---------------------------------------------------------- 6. tata letak ---
const elBagian = [...doc.querySelectorAll('.bagian')];
catat(elBagian.length === 8, '8 bidang di DOM (7 bagian, lipatan dibuat kembar)', String(elBagian.length));
catat(elBagian.filter((el) => el.dataset.id === 'sisi').length === 2, 'lipatan samping dua bidang');
catat(elBagian.every((el) => /px/.test(el.style.transform) && !/\du[,)]/.test(el.style.transform)),
  'semua transform memakai px, bukan satuan "u" (tidak sah di CSS)');
catat(doc.querySelectorAll('.sebutir').length === 7, '7 biji di dalam kemasan', String(doc.querySelectorAll('.sebutir').length));
catat(/label-blue-mount-ijen\.png/.test(kodeCss), 'bidang depan memakai label asli Nocturne');

// ------------------------------------------------------------ 7. sambungan ---
const tombol = [...doc.querySelectorAll('.daftar button')];
catat(tombol.length === 7, '7 tombol bagian', String(tombol.length));
const judulAwal = doc.getElementById('kartuJudul').textContent;
tombol[4].dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
const judulBaru = doc.getElementById('kartuJudul').textContent;
catat(judulAwal !== judulBaru, 'klik tombol mengganti kartu', `${judulAwal} → ${judulBaru}`);
catat(tombol[4].getAttribute('aria-current') === 'true', 'tombol aktif ditandai aria-current');
catat(doc.querySelector('.bagian[data-id="katup"]').dataset.terbuka === '1', 'bagian yang dipilih benar-benar terbuka');

const rel = doc.getElementById('rel');
rel.dispatchEvent(new window.MouseEvent('pointerdown', { bubbles: true, clientX: 400 }));
catat(doc.getElementById('relTitik').style.left !== '', 'rel waktu bisa digeser (pointer)');
const sebelum = doc.getElementById('waktu').textContent;
rel.dispatchEvent(new window.MouseEvent('pointerdown', { bubbles: true, clientX: 100 }));
catat(doc.getElementById('waktu').textContent !== sebelum, 'geser rel mengubah waktu');
rel.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
catat(Number(rel.getAttribute('aria-valuenow')) >= 0, 'panah kanan tidak merusak waktu');

// putar lagi & maju 60 frame: tidak boleh ada galat
doc.getElementById('mainkan').dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
langkah(60);
catat(true, '60 frame berjalan tanpa galat', 'rAF ditumpuk di sandbox');

// -------------------------------------------------------------- 8. ceklis ---
const ceklis = fs.readFileSync(path.join(ROOT, 'laporan/cutaway-checklist.md'), 'utf8');
const baris = ceklis.split('\n').filter((l) => /^\d+\./.test(l));
catat(baris.length >= 10 && baris.length <= 12, 'laporan/cutaway-checklist.md 10–12 baris', String(baris.length));
catat(baris[baris.length - 1].includes('0,8'), 'baris terakhir = porsi gelap × 0,8 (aturan metode)');
const rasio = String(D.UKUR.rasio);
catat(baris[0].includes(rasio), 'baris 1 memakai rasio terukur', rasio);
catat(ceklis.includes('Cutaway'), 'ceklis menyebut sumber metode');

// ------------------------------------------------------------------ hasil ---
console.log('');
if (masalah.length) {
  console.log(`  ${masalah.length} masalah:`);
  masalah.forEach((m) => console.log('   ·', m));
  process.exit(1);
}
console.log('  semua butir lolos · film 60 fps TIDAK dirender di sini (tanpa Chromium/ffmpeg)');
