/**
 * Uji halaman katalog (`katalog/index.html`) tanpa peramban.
 *
 * Yang diuji: data hasil rig benar-benar terpakai, dan sambungan halaman jalan —
 * kartu terbentuk dari data, tombol sudut mengganti berkas, detail menampilkan
 * harga varian yang dipilih, tautan WhatsApp memuat nama + harga, Escape menutup.
 *
 * Yang TIDAK diuji (dan tidak boleh diklaim): rupa halaman. Tidak ada Chromium di
 * sandbox ini; tampilan foto hanya bisa dinilai dengan mata di Live Preview.
 *
 *   node tools/katalog-uji.mjs [--verbose]
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

const html = fs.readFileSync(path.join(ROOT, 'katalog/index.html'), 'utf8');
const dataJs = fs.readFileSync(path.join(ROOT, 'data/katalog.js'), 'utf8');
const kode = fs.readFileSync(path.join(ROOT, 'katalog/katalog.js'), 'utf8');
const css = fs.readFileSync(path.join(ROOT, 'katalog/katalog.css'), 'utf8');

const berkas = html
  .replace(/<script src="\.\.\/data\/katalog\.js"><\/script>/, `<script>${dataJs}</script>`)
  .replace(/<script src="katalog\.js"><\/script>/, `<script>${kode}</script>`);

const dom = new JSDOM(berkas, {
  runScripts: 'dangerously',
  url: 'https://nocturnekoffie.id/katalog/',
  pretendToBeVisual: false,
  beforeParse(window) {
    window.innerWidth = 1440;
    window.innerHeight = 900;
    Object.defineProperty(window, 'matchMedia', {
      value: () => ({ matches: false, addEventListener() {}, removeEventListener() {} }),
    });
    window.Element.prototype.animate = function () { return { onfinish: null, cancel() {} }; };
    window.requestAnimationFrame = () => 1;
    window.addEventListener('error', (e) => masalah.push('galat JS: ' + e.message));
  },
});

const { window } = dom;
const doc = window.document;
const K = window.KATALOG;
const SKU = K.SKU || K.sku;
const katalog = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/catalog.json'), 'utf8'));

// ------------------------------------------------------------ 1. data rig ---
catat(SKU.length === 9, '9 SKU dari data/katalog.js', String(SKU.length));
catat(!!window.KATALOG_STATUS, 'katalog.js memasang KATALOG_STATUS (bisa diuji tanpa layar)');
for (const s of SKU) {
  for (const kunci of ['0', '18', '40', 'hero']) {
    if (!s.foto[kunci]) catat(false, `${s.id}: foto sudut ${kunci} tidak ada di data`);
  }
  const jalur = path.join(ROOT, s.foto.hero);
  if (!fs.existsSync(jalur)) catat(false, `${s.id}: berkas ${s.foto.hero} tidak ada di disk`);
}
catat(true, 'semua jalur foto di data menunjuk berkas yang ada');

// harga harus sama dengan katalog
const katalogHarga = new Map(katalog.products.map((p) => [p.id, p.variants.map((v) => v.price).sort((a, b) => a - b)]));
let hargaOk = true;
for (const s of SKU) {
  const kk = katalogHarga.get(s.id) || [];
  if (kk[0] !== s.harga) { hargaOk = false; catat(false, `${s.id}: harga ${s.harga} ≠ katalog ${kk[0]}`); }
  if (s.ukuran.length !== kk.length) { hargaOk = false; catat(false, `${s.id}: ${s.ukuran.length} varian ≠ katalog ${kk.length}`); }
}
catat(hargaOk, 'harga & varian di data sama dengan data/catalog.json');

// ------------------------------------------- 1b. spesifikasi kemasan ---
// Angka di halaman harus sama dengan berkas spesifikasi, bukan diketik di JS.
const spek = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/kemasan-katalog.json'), 'utf8'));
const aktif = spek.ukuran[spek.ukuran_aktif];
catat(!!K.kemasan, 'data katalog memuat spesifikasi kemasan');
catat(K.kemasan && K.kemasan.lebar === aktif.lebar && K.kemasan.tinggi === aktif.tinggi,
  'lebar & tinggi di data = data/kemasan-katalog.json',
  K.kemasan ? `${K.kemasan.lebar}×${K.kemasan.tinggi} mm` : '—');
catat(K.kemasan && K.kemasan.gusset === aktif.gusset,
  'gusset di data = data/kemasan-katalog.json', K.kemasan ? `${K.kemasan.gusset} mm` : '—');
const teksKemasan = doc.getElementById('kemasan').textContent;
catat(teksKemasan.includes(String(aktif.lebar)) && teksKemasan.includes(String(aktif.tinggi)),
  'halaman menulis ukuran kemasan', teksKemasan.slice(0, 60) + '…');
catat(/sementara|belum/i.test(spek.status || '')
  ? doc.getElementById('kemasan').classList.contains('is-sementara')
  : true, 'status spesifikasi sementara ditandai di halaman');

// foto marketplace: putih murni, dua rasio, sembilan lot
const strip = [...doc.querySelectorAll('#pasarStrip li')];
catat(strip.length === 9, 'strip marketplace berisi 9 lot', String(strip.length));
let pasarOk = true;
for (const s of SKU) {
  for (const r of ['1x1', '4x5']) {
    const j = path.join(ROOT, (s.pasar || {})[r] || '');
    if (!fs.existsSync(j)) { pasarOk = false; catat(false, `${s.id}: foto pasar ${r} tidak ada`); }
  }
  if (!/-1x1\.jpg$/.test((s.pasar || {})['1x1'] || '')) {
    pasarOk = false; catat(false, `${s.id}: jalur foto pasar salah`);
  }
}
catat(pasarOk, 'foto marketplace 1:1 dan 4:5 ada untuk semua lot');
catat(/latar #FFFFFF/.test(doc.getElementById('pasarCatatan').textContent),
  'catatan marketplace menyebut latar putih murni',
  doc.getElementById('pasarCatatan').textContent);

// --------------------------------------------------------- 2. kartu DOM ---
const kartu = [...doc.querySelectorAll('.kartu')];
catat(kartu.length === 9, '9 kartu katalog dibuat', String(kartu.length));
catat(doc.querySelectorAll('.kartu__bingkai img').length === 18, 'tiap kartu punya 2 gambar (0° dan 3/4)',
  String(doc.querySelectorAll('.kartu__bingkai img').length));
const srcPertama = kartu[0].querySelector('img').getAttribute('src');
catat(/assets\/img\/katalog\/.+-0\.jpg$/.test(srcPertama), 'kartu memakai foto sudut 0°', srcPertama);
catat(/katalog\/.+-18\.jpg$/.test(kartu[0].querySelectorAll('img')[1].getAttribute('src')),
  'gambar kedua memakai sudut 3/4');

// hero
const heroSrc = doc.getElementById('heroImg').getAttribute('src');
catat(/-hero\.jpg$/.test(heroSrc), 'hero memakai foto 16:9', heroSrc);
catat(doc.querySelectorAll('#heroMeta dt').length === 3, 'hero menampilkan 3 metadata');

// --------------------------------------------------------- 3. tombol sudut ---
const tombol = [...doc.querySelectorAll('.sudut__btn')];
catat(tombol.length === 3, '3 tombol sudut', String(tombol.length));
tombol[2].dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
const srcSetelah = kartu[0].querySelector('img').getAttribute('src');
catat(/-40\.jpg$/.test(srcSetelah), 'klik tombol 40° mengganti berkas kartu', srcSetelah);
catat(tombol[2].classList.contains('is-on'), 'tombol aktif ditandai');
tombol[0].dispatchEvent(new window.MouseEvent('click', { bubbles: true }));

// -------------------------------------------------------------- 4. detail ---
kartu[2].dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
const detal = doc.getElementById('detal');
catat(detal.classList.contains('is-buka'), 'klik kartu membuka detail');
const nama = doc.getElementById('dNama').textContent;
catat(nama === SKU[2].nama, 'judul detail = SKU yang diklik', nama);
catat(/\d+ × \d+ mm/.test(doc.getElementById('dKemasan').textContent),
  'panel detail menyebut ukuran kemasan', doc.getElementById('dKemasan').textContent.slice(0, 52) + '…');
catat(doc.getElementById('dHarga').textContent.includes('Rp'), 'harga tampil sebagai rupiah',
  doc.getElementById('dHarga').textContent);
const varianBtns = [...doc.querySelectorAll('#dPilih button')];
catat(varianBtns.length === SKU[2].ukuran.length, 'tombol varian sesuai jumlah ukuran');
if (varianBtns.length > 1) {
  const sebelum = doc.getElementById('dHarga').textContent;
  varianBtns[1].dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
  catat(doc.getElementById('dHarga').textContent !== sebelum, 'ganti varian mengubah harga',
    sebelum + ' → ' + doc.getElementById('dHarga').textContent);
}
const cta = doc.getElementById('dCta').getAttribute('href');
catat(cta.startsWith('https://wa.me/') && decodeURIComponent(cta).includes(SKU[2].nama),
  'tautan WhatsApp memuat nama lot', cta.slice(0, 60) + '…');
const sudutBtn = [...doc.querySelectorAll('#dSudut button')];
catat(sudutBtn.length === 3, 'detail punya 3 tombol sudut');
sudutBtn[1].dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
catat(/-18\.jpg$/.test(doc.getElementById('dFot').getAttribute('src')),
  'tombol sudut di detail mengganti foto', doc.getElementById('dFot').getAttribute('src'));

doc.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
catat(!detal.classList.contains('is-buka'), 'Escape menutup detail');

// -------------------------------------------------------------- 5. larangan ---
const tanpaKomentar = (s) => s.replace(/\/\*[\s\S]*?\*\//g, '').split('\n')
  .filter((l) => !/^\s*(\/\/|\*)/.test(l)).join('\n');
const js = tanpaKomentar(kode);
const cssBersih = tanpaKomentar(css);
catat(!/Math\.random/.test(js), 'katalog.js tanpa Math.random');
catat(!/@keyframes/.test(cssBersih), 'katalog.css tanpa @keyframes');
catat(!/Rp\s?\d/.test(js), 'tidak ada harga diketik di katalog.js — semuanya dari data');
catat(!/opacity\s*:/.test(js), 'tanpa opacity fade di katalog.js');
catat(/prefers-reduced-motion/.test(css), 'ada jalur gerak-dikurangi');

// ---------------------------------------------------------------- hasil ---
console.log('');
if (masalah.length) {
  console.log(`  ${masalah.length} masalah:`);
  masalah.forEach((m) => console.log('   ·', m));
  process.exit(1);
}
console.log('  semua butir lolos · tampilan belum pernah dilihat (tanpa peramban)');
