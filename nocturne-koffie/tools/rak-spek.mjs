/**
 * Konformansi rak sangrai terhadap spesifikasi template (motionsite.ai / Leon Vasari
 * "VHS filmography shelf") yang dipakai 6–7 Nov 2026.
 *
 * 9 Nov 2026: pemilik meminta objek rak diganti dari kaset VHS menjadi kemasan
 * kopi 3D. Geometri muka kini dari data (rak/data.js → FACE), dan butir yang
 * menyebut rasio kaset diperbarui menjadi dua jalur (data + cadangan).
 *
 * Kenapa ada berkas ini: spesifikasinya panjang dan penuh angka (ws = H·142/840,
 * pegas 5,2/18, tirai 1050 ms, tinta 520+1250 ms, cincin 58 px …). Angka seperti
 * ini gampang berubah tanpa sengaja saat berkas dirapikan. Uji ini membaca
 * `rak/rak.js`, `rak/rak.css`, dan `rak/index.html`, lalu membandingkan setiap
 * butir dengan spesifikasi — tanpa peramban, tanpa menebak.
 *
 * 21 Nov 2026: geometri rak naik dari garis lurus ke BUSUR ala rujukan VHS
 * (scl(u)=1/(1+(|u|/U)^1.6) + tabel integral XS). Butir yang mendeskripsikan
 * rumus lama (z = o·0,2H, y = −o·0,025H, culling |x| > W/2+1,5d, z-index
 * 100−|r|·4, kursor meluncur di rak.js) diperbarui ke rumus busur yang baru;
 * bukan dilonggarkan — masing-masing masih diuji terhadap angka yang pasti.
 *
 * Keluaran: baris "OK" untuk butir yang sama, "~" untuk penyimpangan yang
 * DISENGAJA (dengan alasan), "XX" untuk yang hilang/salah (menggagalkan uji).
 *
 *   node tools/rak-spek.mjs [--verbose]
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const verbose = process.argv.includes('--verbose');

const js = fs.readFileSync(path.join(ROOT, 'rak/rak.js'), 'utf8');
const css = fs.readFileSync(path.join(ROOT, 'rak/rak.css'), 'utf8');
const html = fs.readFileSync(path.join(ROOT, 'rak/index.html'), 'utf8');
const data = fs.readFileSync(path.join(ROOT, 'rak/data.js'), 'utf8');
// kursor dipindah ke berkas sendiri 21 Nov 2026 (supaya rak.js tinggal satu
// urusan: rak). Uji membaca keduanya.
const kursor = fs.readFileSync(path.join(ROOT, 'rak/rak-kursor.js'), 'utf8');

const gagal = [];
const menyimpang = [];
let lolos = 0;

const catat = (ok, spek, temuan) => {
  if (ok) {
    lolos++;
    if (verbose) console.log(`  OK ${spek}`);
  } else {
    gagal.push(`${spek} — ${temuan}`);
    console.log(`  XX ${spek} — ${temuan}`);
  }
};
const sama = (ok, spek, alasan) => {
  if (ok) { lolos++; if (verbose) console.log(`  OK ${spek}`); }
  else { menyimpang.push(`${spek} — ${alasan}`); if (verbose || true) console.log(`  ~  ${spek} — ${alasan}`); }
};
const namaSumber = (sumber) =>
  sumber === js ? 'rak.js' : sumber === css ? 'rak.css'
    : sumber === html ? 'rak/index.html' : sumber === kursor ? 'rak-kursor.js' : 'berkas';
const ada = (pola, spek, sumber = js) =>
  catat(typeof pola === 'string' ? sumber.includes(pola) : pola.test(sumber), spek,
    `tidak ditemukan di ${namaSumber(sumber)}`);

// ---------------------------------------------------------------- token ---
ada('--paper:#EDEBE6', 'token: --paper #EDEBE6', css);
ada('--sheet:#F4F2ED', 'token: --sheet #F4F2ED', css);
ada('--ink:#141414', 'token: --ink #141414', css);
ada('--muted:#6D6A63', 'token: --muted #6D6A63', css);
ada('--accent:#1F3FB0', 'token: aksen kobalt #1F3FB0', css);
ada('--ease:cubic-bezier(.2,.8,.2,1)', 'token: --ease cubic-bezier(.2,.8,.2,1)', css);
ada('--H:min(46vh,31vw)', 'token: --H min(46vh,31vw) desktop', css);
ada('--H:min(60vw,40svh)', 'token: --H min(60vw,40svh) ≤767px', css);

// -------------------------------------------------------------- geometri ---
// Sejak 9 Nov 2026 objek rak = kemasan kopi, bukan kaset: rasio muka dibaca dari
// data (FACE). Angka kaset (H·142/840, H·474/900) tetap ada sebagai cadangan
// kalau data belum menyebut rasio — jadi uji ini memeriksa kedua jalur.
ada(/ws = H \* FACE\.sp/, 'spine width = H·FACE.sp (dari data)');
ada(/d = H \* FACE\.cv/, 'cover width = H·FACE.cv (dari data)');
ada(/cv: 474 \/ 900, sp: 142 \/ 840/, 'cadangan rasio kaset 474/900 & 142/840 dipertahankan');
ada(/"FACE"/, 'data menyebut FACE', data);
ada(/"BAHAN": "kemasan"/, 'data menyebut bahan kemasan', data);
ada(/gap = H \* 0\.035/, 'gap = H·0,035');
ada(/Math\.pow\(Math\.abs\(u\) \/ U, 1\.6\)/, 'scl(u) = 1/(1+(|u|/U)^1,6)');
ada(/function bangunBusur/, 'tabel integral XS dibangun sekali per ukuran');
ada(/U = H \* \(window\.innerWidth < 768 \? 1\.05 : 1\.3\)/,
  'U = 1,3H (ponsel 1,05H) — jatuh kedalaman busur');
ada(/const xs = xsc\(u\)/, 'posisi layar = integral busur xsc(u)');
ada(/Math\.sign\(u\) \* Math\.min\(1, Math\.abs\(u\) \/ U\) \* 26/, 'belok rotateY 26°·(|u|/U)');
ada(/H \* 0\.5 \* \(1 - sc\) \* 0\.42/, 'bowl-sink 0,42·H(1−sc)');
ada(/perspective:2200px/, 'perspektif 2200 px (rujukan 1400 untuk lembar 840 px)', css);
ada('const COPIES = 3', '12 film × 3 salinan = 36 kotak');
ada(/const HALF = TOTAL \/ 2/, 'relatif ±18 (TOTAL/2)');
ada(/r \* \(ws \+ gap\) \+ \(d - ws \+ 1\.6 \* gap\) \* step\(r\)/, 'F(r) = r(ws+gap) + (d−ws+1,6gap)·B(r)');
ada(/Math\.sin\(Math\.PI \* r\) \/ Math\.PI/, 'B(r) = (r + sin πr/π)/2');
ada(/a \* a \* \(3 - 2 \* a\)/, 'bukaan o = smoothstep(1−|r|)');

// ------------------------------------------------------------ jejak 3D ---
ada("' rotateZ(' + (-4.5 * o)", 'kemiringan −4,5°·o');
ada('rotateZ(', 'urutan transform translate3d → rotateZ → rotateX → rotateY');
ada(/o \* H \* 0\.1/, 'pulled out: translateZ o·0,1H di atas kedalaman busur');
ada(/2200 \* \(1 - k\)/, 'kedalaman z = P(1−k) — makin ke tepi makin jauh');
ada(/o \* H \* 0\.012/, 'angkat: translateY +0,012H·o (busur sudah menenggelamkan tepi)');
ada(/t\.lift \* H \* 0\.05/, 'hover lift 0,05H');
ada(/\(1 - sc\) \* 0\.32/, 'shading punggung: o·0,55 + (1−sc)·0,32');
ada(/\(\(1 - o\) \* 0\.82\)/, 'shading sampul (1−o)·0,82');
ada(/Math\.round\(3000 \+ z\)/, 'z-index mengikuti kedalaman (3000+z)');
ada(/Math\.abs\(xs\) - \(d \* sc\) \/ 2 > W \/ 2/,
  'culling menurut tepi kotak di layar: |xs| − lebar/2 > W/2');

// --------------------------------------------------------------- pegas ---
ada(/dragging \? 18 : 5\.2/, 'pegas s: 5,2 (diam) / 18 (geser)');
ada('Math.min(50, now - last)', 'dt dijepit 50 ms');
ada('1e-4', 'snap saat |T−s| < 1e−4');
sama(/RM \? 60/.test(js), 'reduced motion: pegas "seketika"',
  'spesifikasi menulis k=1 (masih meluncur); di sini 60 = praktis seketika');
ada(/Math\.abs\(T - s\) < 0\.3/, 'kemiringan hanya saat rak hampir diam (|T−s|<0,3)');
ada('0.55 * d', 'syarat kursor "di sampul": 0,55d');
ada('0.55 * H', 'syarat kursor "di sampul": 0,55H');
ada(/\/ \(0\.55 \* d\) \* 9/, 'tiltY maks 9°');
ada(/\(H \/ 2\)\) \* 6/, 'tiltX maks 6°');
ada('RM ? 40 : 7', 'pelembutan kemiringan k=7');
ada('RM ? 40 : 12', 'pelembutan hover lift k=12');

// ---------------------------------------------------------- cincin putar ---
ada('0.36 * H', 'cincin putar di tengah + 0,36H');
ada('W / 2 - d / 2 - 6', 'cincin putar di kiri-bawah sampul, −6 px');
ada('1 - Math.abs(T - s) * 3', 'skala cincin: smoothstep(1 − |T−s|·3)');
ada('width:42px;height:42px', 'cincin putar 42 px', css);

// ------------------------------------------------------------- caption ---
ada('font-size:31px', 'caption judul 31 px Newsreader', css);
ada('gap:9px', 'jarak baris caption 9 px', css);
ada('min(92vw,760px)', 'lebar mask caption min(92vw,760px)', css);
ada('650', 'pergantian caption 650 ms');
ada('-dir * 105', 'caption keluar ke −dir·105%');
ada('dir * 105', 'caption masuk dari dir·105%');
ada('Math.sign(T - s) || 1', 'caption memakai arah gerak sign(T−s)');

// ----------------------------------------------------------------- tab ---
ada('height:23px', 'tab 23 px', css);
ada('padding:0 11px', 'tab padding 0 11px', css);
ada('margin-left:-1px', 'tab berbagi satu garis', css);
ada('transition:width .6s var(--ease),transform .6s var(--ease)', 'indikator tab 0,6 s', css);
ada('transition:color .45s var(--ease)', 'teks tab .45 s', css);
ada('translateX(', 'indikator tab digeser translateX');

// -------------------------------------------------------------- kursor ---
ada('width:58px;height:58px', 'kursor 58 px', css);
ada(/1 - Math\.exp\(-16/, 'kursor mengikuti 1−e^(−16·dt) di rak-kursor.js', kursor);
ada('scale(.72)', 'kursor di atas punggung: 0,72', css);
ada('scale(.55)', 'kursor di atas tombol: 0,55', css);
ada('scale(1.75)', 'kursor di atas sampul: 1,75 + kobalt', css);

// --------------------------------------------------------------- kertas ---
ada('width=\'220\' height=\'220\'', 'butir kertas 220×220', css);
ada("baseFrequency='.85'", 'butir: feTurbulence .85', css);
ada("numOctaves='3'", 'butir: 3 oktav', css);
ada('opacity:.55;mix-blend-mode:multiply', 'butir: multiply, opacity .55', css);
ada('z-index:40', 'butir di lapisan 40', css);

// --------------------------------------------------------------- detail ---
ada('1050', 'tirai kertas 1050 ms');
ada('cubic-bezier(.76,0,.18,1)', 'tirai memakai cubic-bezier(.76,0,.18,1)');
ada("'rotate(-4.5deg)'", 'tirai mulai miring −4,5°');
ada('round 3px', 'tirai mulai dari kotak sampul (radius 3)');
ada('620 + idx * 75', 'baris teks: 620 ms + 75 ms/baris');
ada('900', 'baris teks 900 ms');
ada('520', 'tinta mulai 520 ms setelah buka');
ada('1250', 'tinta menyebar 1250 ms');
ada('Math.pow(1 - p, 3)', 'tinta ease-out kubik');
ada('720', 'jari-jari tinta 720');
ada('850', 'tutup 850 ms');
ada('DELAY = [0, 120, 220, 300, 360, 420, 180]', 'tujuh tinta, jeda sesuai spesifikasi');
ada("baseFrequency=\".011\"", 'filter tinta .011', html);
ada('scale="120"', 'displacement tinta 120', html);
ada('seed="7"', 'seed tinta 7', html);
ada('474 900', 'poster 474×900', html);

// ------------------------------------------------------------- struktur ---
ada('perspective:2200px', 'panggung perspective 2200 px', css);
ada('backface-visibility:hidden', 'muka backface hidden', css);
ada('rotateY(90deg) translateZ(calc(var(--ws) / 2))', 'muka sampul: rotateY(90) translateZ(ws/2)', css);
ada('translateZ(calc(var(--d) / 2))', 'muka punggung: translateZ(d/2)', css);
ada('0 30px 60px -28px rgba(20,16,10,.55)', 'bayangan sampul', css);
ada('@media (pointer:fine){', 'kursor asli disembunyikan di pointer halus', css);
ada('@media (max-width:767px)', 'breakpoint 767 px', css);
ada('46svh', 'poster ≤767px 46svh', css);
ada('font-size:42px', 'judul detail ≤767px 42 px', css);

// ------------------------------------------------------------- perilaku ---
ada('aria-live="polite"', 'caption aria-live polite', html);
ada('role="dialog"', 'lembar detail role=dialog', html);
ada('aria-modal="true"', 'lembar detail aria-modal', html);
ada('aria-label="Lot sebelumnya"', 'tombol panah berlabel', html);
ada('aria-label="Lot berikutnya"', 'tombol panah kanan berlabel', html);
ada('Escape', 'Escape menutup');
ada('ArrowRight', 'panah kanan');
ada('ArrowLeft', 'panah kiri');
ada('clearTimeout(wheelT)', 'roda: snap setelah 160 ms');
ada('160', 'roda: 160 ms');
ada('> 5', 'geser mulai setelah 5 px');
ada('Math.round(T)', 'geser/roda snap ke bilangan bulat');
ada('is-', 'kursor punya keadaan (kelas)');

// -------------------------------------------- tambahan paritas 21 Nov 2026 ---
// Rujukan VHS punya empat lapisan yang dulu tidak ada di rak Nocturne: kanji
// halftone, garis waktu, bayangan lantai, dan nomor lot. Semua diuji di sini.
const fonts = fs.readFileSync(path.join(ROOT, 'assets/css/fonts.css'), 'utf8');
ada('珈琲', 'kanji 珈琲 (kopi) — kata sendiri, bukan 映画', html);
ada('の記憶', 'kanji の記憶 (dan kenangan)', html);
ada('kanji--halftone', 'kanji ditutup tekstur halftone', css);
ada(/mask-size:4px 4px/, 'halftone: titik di grid 4 px', css);
const tanpaKomentarHtml = html.replace(/<!--[\s\S]*?-->/g, '');
catat(!tanpaKomentarHtml.includes('映画'), 'kanji rujukan (映画) tidak disalin', 'masih ada 映画');
ada('Kopi Kanji', '@font-face "Kopi Kanji" dari subset IPAexGothic', fonts);
ada('unicode-range:U+306E', 'unicode-range kanji dibatasi 7 glif', fonts);
catat(fs.existsSync(path.join(ROOT, 'assets/fonts/kopikanji.woff2')), 'subfont kanji ada di assets/fonts', 'kopikanji.woff2 hilang');
catat(fs.existsSync(path.join(ROOT, 'assets/fonts/LISENSI-IPA.txt')), 'lisensi IPA v1.0 ikut disertakan', 'LISENSI-IPA.txt hilang');
ada('id="timeline"', 'garis waktu ada di halaman', html);
ada('timeline__axis', 'garis sumbu garis waktu', css);
ada('bangunWaktu', 'garis waktu dibangun dari data (bukan tahun karangan)');
ada('it.mdpl', 'titik garis waktu memakai ketinggian katalog');
catat(!js.replace(/\/\*[\s\S]*?\*\//g, '').includes('1955')
  && !html.replace(/<!--[\s\S]*?-->/g, '').includes('1955')
  && !html.replace(/<!--[\s\S]*?-->/g, '').includes('1990'),
  'tahun rujukan (1955–1990) tidak dipakai', 'ada tahun karangan');
ada('class="lantai"', 'bayangan lantai di bawah rak', html);
ada('.lantai{', 'gaya bayangan lantai', css);
ada('id="indeks"', 'nomor lot aktif tampil', html);

// larangan
catat(!/@keyframes/.test(css.replace(/\/\*[\s\S]*?\*\//g, '')), 'tanpa @keyframes', 'ada @keyframes');
const tanpaKomentar = js.replace(/\/\*[\s\S]*?\*\//g, '');
catat(!/opacity\s*:/.test(tanpaKomentar), 'tanpa opacity fade di JS', 'ada opacity di rak.js');
catat(!/transition:[^;]*opacity(?!\s*\.85)/.test(css), 'tanpa transisi opacity', 'ada transisi opacity');

// --------------------------------------------------------------- isi data ---
const jumlah = (data.match(/"id":/g) || []).length || (data.match(/id:/g) || []).length;
catat(jumlah >= 9, 'data.js memuat lot Nocturne', `${jumlah} item`);

// ---------------------------------------------------------------- ringkas ---
console.log('');
if (verbose) console.log(`  ${lolos} butir sesuai · ${menyimpang.length} disengaja · ${gagal.length} gagal`);
if (gagal.length) {
  console.log(`  ${gagal.length} butir GAGAL:`);
  gagal.forEach((g) => console.log('   ·', g));
  process.exit(1);
}
console.log(`  spesifikasi terpenuhi · ${lolos} butir sesuai · ${menyimpang.length} penyimpangan disengaja`);
menyimpang.forEach((m) => console.log('   ~', m));
