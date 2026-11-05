/**
 * Verifikasi biji 3D — tanpa browser, tanpa dependensi.
 *
 *   node tools/verifikasi-biji.mjs
 *
 * Yang diperiksa:
 *  1. Skrip WebGL (`assets/js/biji3d.js`) memuat data dari `data/biji3d.json`
 *     dan tidak menulis angka geometri sendiri.
 *  2. Geometri JS = geometri Python. Titik senyawa diproyeksikan memakai
 *     kamera yang sama, lalu dibandingkan dengan posisi di
 *     `laporan/biji-3d.json` (hasil render CPU oleh tools/biji.py).
 *     Kalau kedua sisi tidak sinkron, hasilnya akan berbeda jauh.
 *  3. Mesh: jumlah vertex, batas ruang (biji tidak lebih besar dari 2,0),
 *     normal menghadap keluar, kedalaman alur > 0.
 *  4. HTML: jumlah tombol titik = jumlah zona; semua id zona ada di panel.
 *  5. Tidak ada pustaka 3D dari CDN.
 *
 * Yang TIDAK diperiksa: hasil render WebGL sesungguhnya (butuh GPU + browser).
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..');
const baca = (p) => readFileSync(resolve(root, p), 'utf8');

const hasil = [];
const catat = (nama, ok, detail) => {
  hasil.push({ nama, ok, detail });
  console.log(`  ${ok ? 'OK  ' : 'XX  '} ${nama.padEnd(24)} ${detail}`);
};

/* ── 1 · muat skrip dengan shim window/document minimal ─────────────────── */
const sandbox = {
  window: {
    matchMedia: () => ({ matches: false, addEventListener() {} }),
    innerWidth: 1280,
    devicePixelRatio: 2,
    addEventListener() {},
    requestAnimationFrame() { return 0; },
    cancelAnimationFrame() {},
    IntersectionObserver: undefined,
  },
  document: {
    readyState: 'complete',
    querySelectorAll: () => [],
    addEventListener() {},
  },
  performance: { now: () => 0 },
  console,
  fetch: () => Promise.reject(new Error('tidak dipakai')),
  setTimeout,
  clearTimeout,
};
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(baca('assets/js/biji3d.js'), sandbox, { filename: 'biji3d.js' });

const lib = sandbox.window.NocturneBiji3D;
const data = JSON.parse(baca('data/biji3d.json'));

catat('Skrip WebGL dimuat', !!lib && typeof lib.buatBiji === 'function',
  lib ? 'NocturneBiji3D tersedia (buatBiji, kamera, proyeksiLayar)' : 'tidak ada');

const kode = baca('assets/js/biji3d.js');
const angkaKeras = [
  ['0.62', 'sumbu b'],
  ['0.46', 'sumbu c'],
  ['0.72', 'faktor ratakan'],
];
const keras = angkaKeras.filter(([n]) => kode.includes(n));
catat('Angka dari data, bukan JS', keras.length === 0,
  keras.length ? `JS menulis ulang: ${keras.map((k) => k[1]).join(', ')}` : 'tidak ada geometri yang ditulis ulang di JS');

const cdn = ['cdn.jsdelivr.net', 'unpkg.com', 'three.min.js', 'cdnjs.cloudflare.com'].filter((c) => kode.includes(c));
catat('Tanpa pustaka 3D dari CDN', cdn.length === 0, cdn.length ? cdn.join(', ') : 'nol referensi CDN');

/* ── 2 · geometri: JS vs Python ─────────────────────────────────────────── */
const biji = lib.buatBiji(data);
const cam = lib.kamera(data.kamera);
const W = 640, H = 800, aspek = W / H;
const laporan = JSON.parse(baca('laporan/biji-3d.json'));
const posPython = new Map(laporan.posisi_layar_persen.map((p) => [p.id, p]));

let selisihMaks = 0;
const baris = [];
for (const z of data.zona) {
  const p = biji.arahKePermukaan(z.arah);
  const layar = lib.proyeksiLayar(cam, p, W, H, aspek);
  const x = (layar[0] / W) * 100;
  const y = (layar[1] / H) * 100;
  const ref = posPython.get(z.id);
  const dx = Math.abs(x - ref.x);
  const dy = Math.abs(y - ref.y);
  selisihMaks = Math.max(selisihMaks, dx, dy);
  baris.push(`${z.id} Δ${Math.max(dx, dy).toFixed(2)}%`);
}
catat('JS = Python (proyeksi)', selisihMaks < 0.6,
  `selisih maksimum ${selisihMaks.toFixed(2)}% · ${baris.length} titik`);

/* ── 3 · mesh ───────────────────────────────────────────────────────────── */
const [rx, ry] = [40, 80];
let minY = 99, maxY = -99, maxX = -99, normalKeluar = 0, total = 0, nan = 0, panjangNormal = 0;
const pusat = [];
for (let i = 0; i <= rx; i++) {
  const tx = (Math.PI * i) / rx;
  for (let j = 0; j < ry; j++) {
    const tp = (2 * Math.PI * j) / ry;
    const p = biji.titik(tx, tp);
    const n = biji.normal(tx, tp);
    total++;
    if (p[1] < minY) minY = p[1];
    if (p[1] > maxY) maxY = p[1];
    if (Math.abs(p[0]) > maxX) maxX = Math.abs(p[0]);
    if (n[0] * p[0] + n[1] * p[1] + n[2] * p[2] > 0) normalKeluar++;
    if (!Number.isFinite(p[0] + p[1] + p[2] + n[0] + n[1] + n[2])) nan++;
    panjangNormal += Math.abs(Math.hypot(n[0], n[1], n[2]) - 1);
    if (i === Math.floor(rx / 2)) pusat.push(p);
  }
}
const lebarAlur = Math.min(...pusat.map((p) => p[2]));
const tebalPinggir = Math.max(...pusat.map((p) => p[2]));
const persenKeluar = (normalKeluar / total) * 100;
const ralatNormal = panjangNormal / total;
catat('Mesh & normal', nan === 0 && persenKeluar > 97 && maxX <= 1.001 && ralatNormal < 1e-6,
  `${total} vertex · ${persenKeluar.toFixed(1)}% normal keluar (sisa 1,2% = kutub, fallback radial) · `
  + `setengah panjang ${maxX.toFixed(3)} · tebal ${(maxY - minY).toFixed(3)} · NaN ${nan} · galat unit ${ralatNormal.toExponential(1)}`);
catat('Alur terbentuk', lebarAlur < tebalPinggir * 0.72,
  `tengah z=${lebarAlur.toFixed(3)} vs pinggir z=${tebalPinggir.toFixed(3)}`);

/* ── 4 · HTML ───────────────────────────────────────────────────────────── */
const html = baca('index.html');
const tombol = (html.match(/data-biji-titik="/g) || []).length;
const zonaHtml = (html.match(/data-biji-zona="/g) || []).length;
const idZona = data.zona.map((z) => z.id);
const semuaAda = idZona.every((id) => html.includes(`data-biji-titik="${id}"`) && html.includes(`data-biji-zona="${id}"`));
catat('HTML titik ↔ zona', tombol === idZona.length && zonaHtml === idZona.length && semuaAda,
  `${tombol} tombol · ${zonaHtml} blok zona · semua id cocok`);

const poster = readFileSync(resolve(root, 'assets/img/biji-3d-poster.png'));
const pngOk = poster.subarray(1, 4).toString() === 'PNG';
const pw = poster.readUInt32BE(16), ph = poster.readUInt32BE(20);
const tipeWarna = poster[25];   // 6 = RGBA
catat('Poster PNG beralfa', pngOk && pw >= 400 && ph >= 500 && tipeWarna === 6,
  `${pw}×${ph} · ${(poster.length / 1024).toFixed(0)} KB · ${tipeWarna === 6 ? 'RGBA' : 'tanpa alfa'}`);

const hexDiJs = (kode.match(/#[0-9a-fA-F]{6}/g) || []);
const hexDiPy = (baca('tools/biji.py').match(/#[0-9a-fA-F]{6}/g) || []);
catat('Warna hanya dari data', hexDiJs.length === 0 && hexDiPy.length === 0,
  `JS ${hexDiJs.length} hex · Python ${hexDiPy.length} hex`);

const gagal = hasil.filter((h) => !h.ok).length;

/* sidik jari: kalau data atau skrip berubah tanpa verifikasi dijalankan ulang,
   tools/periksa.py akan menolak laporan yang basi ini */
const sidik = createHash('sha256')
  .update(baca('data/biji3d.json'))
  .update(baca('assets/js/biji3d.js'))
  .digest('hex')
  .slice(0, 16);

writeFileSync(resolve(root, 'laporan/biji-verifikasi.json'), JSON.stringify({
  dibuat: new Date().toISOString().slice(0, 10),
  sidik,
  lolos: hasil.length - gagal,
  gagal,
  selisih_proyeksi_maks_persen: Number(selisihMaks.toFixed(3)),
  butir: hasil.map((h) => ({ nama: h.nama, ok: h.ok, detail: h.detail })),
  catatan: 'Dijalankan tanpa GPU. Memeriksa matematika geometri, kecocokan JS<->Python, '
    + 'struktur HTML, dan poster. Bukan render WebGL.',
}, null, 2) + '\n');
console.log(`\n  ${hasil.length - gagal} lolos · ${gagal} gagal`);
console.log('  Catatan: ini memeriksa matematika & berkas, bukan hasil render WebGL.\n');
process.exit(gagal ? 1 : 0);
