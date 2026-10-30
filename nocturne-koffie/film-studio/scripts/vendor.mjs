/**
 * Sinkron aset ke mesin film — dijalankan sebelum bundling.
 *
 *   node scripts/vendor.mjs
 *
 * 1. Menyalin build GSAP + Lottie dari node_modules ke `assets/vendor/`
 *    (situs memakai berkas lokal; tidak ada CDN di halaman).
 * 2. Menyalin GSAP yang sama ke `film-studio/hyperframes/vendor/` karena
 *    komposisi HyperFrames harus mandiri.
 * 3. Menyalin `motion/film-sheet.json` → `film-studio/data/film-sheet.json`
 *    supaya Remotion & HyperFrames membaca angka yang SAMA dengan lembar film.
 * 4. Menyalin TTF brand ke `film-studio/public/fonts/` untuk `staticFile()`.
 *
 * Tidak ada yang diunduh di sini: semua sudah ada di repo atau di node_modules.
 */
import { copyFileSync, mkdirSync, existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..', '..');          // nocturne-koffie/
const studio = resolve(here, '..');              // film-studio/

const tugas = [
  ['node_modules/gsap/dist/gsap.min.js', 'assets/vendor/gsap.min.js'],
  ['node_modules/gsap/dist/ScrollTrigger.min.js', 'assets/vendor/ScrollTrigger.min.js'],
  ['node_modules/lottie-web/build/player/lottie.min.js', 'assets/vendor/lottie.min.js'],
  ['node_modules/gsap/dist/gsap.min.js', 'film-studio/hyperframes/vendor/gsap.min.js'],
  ['motion/film-sheet.json', 'film-studio/data/film-sheet.json'],
  ['assets/fonts/bricolage-grotesque-latin-800-normal.ttf', 'film-studio/public/fonts/bricolage-800.ttf'],
  ['assets/fonts/fraunces-latin-300-normal.ttf', 'film-studio/public/fonts/fraunces-300.ttf'],
  ['assets/fonts/inter-latin-400-normal.ttf', 'film-studio/public/fonts/inter-400.ttf'],
  ['assets/fonts/inter-latin-600-normal.ttf', 'film-studio/public/fonts/inter-600.ttf'],
];

let n = 0;
for (const [dari, ke] of tugas) {
  // node_modules hidup di film-studio/, berkas repo di akar nocturne-koffie/
  const src = dari.startsWith('node_modules/') ? resolve(studio, dari) : resolve(root, dari);
  const dst = resolve(root, ke);
  if (!existsSync(src)) {
    console.error(`  lewat  ${dari} (tidak ada — jalankan npm install dulu)`);
    continue;
  }
  mkdirSync(dirname(dst), { recursive: true });
  copyFileSync(src, dst);
  n += 1;
  console.log(`  ok     ${ke}`);
}

// manifest versi: supaya "terpasang" bisa diperiksa, bukan diklaim
const baca = (p) => JSON.parse(readFileSync(resolve(studio, p), 'utf8'));
const manifest = {
  dibuat: new Date().toISOString().slice(0, 10),
  catatan: 'Dibuat scripts/vendor.mjs. Semua berkas di bawah ini ada di repo, bukan CDN.',
  paket: {
    gsap: baca('node_modules/gsap/package.json').version,
    'lottie-web': baca('node_modules/lottie-web/package.json').version,
    remotion: baca('node_modules/remotion/package.json').version,
    '@remotion/cli': baca('node_modules/@remotion/cli/package.json').version,
    hyperframes: baca('node_modules/hyperframes/package.json').version,
    jsdom: baca('node_modules/jsdom/package.json').version,
    react: baca('node_modules/react/package.json').version,
  },
  vendor: [
    { berkas: 'assets/vendor/gsap.min.js', paket: 'gsap', lisensi: 'Standard "no charge" (gsap.com/standard-license)' },
    { berkas: 'assets/vendor/ScrollTrigger.min.js', paket: 'gsap', lisensi: 'Standard "no charge" (gsap.com/standard-license)' },
    { berkas: 'assets/vendor/lottie.min.js', paket: 'lottie-web', lisensi: 'MIT' },
  ],
  font: [
    { berkas: 'assets/fonts/bricolage-grotesque-latin-800-normal.ttf', keluarga: 'Bricolage Grotesque', lisensi: 'OFL-1.1' },
    { berkas: 'assets/fonts/fraunces-latin-300-normal.ttf', keluarga: 'Fraunces', lisensi: 'OFL-1.1' },
    { berkas: 'assets/fonts/inter-latin-400-normal.ttf', keluarga: 'Inter', lisensi: 'OFL-1.1' },
    { berkas: 'assets/fonts/inter-latin-600-normal.ttf', keluarga: 'Inter', lisensi: 'OFL-1.1' },
  ],
};
writeFileSync(resolve(root, 'assets/vendor/mesin.json'), JSON.stringify(manifest, null, 2) + '\n');
writeFileSync(resolve(root, 'laporan/mesin.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(`\n${n} berkas disalin · manifest → assets/vendor/mesin.json`);
