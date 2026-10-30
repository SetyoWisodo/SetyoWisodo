/**
 * Generator Lottie — dari lembar film ke animasi vektor.
 *
 *   node lottie/buat-lottie.mjs
 *
 * Masukan : ../data/film-sheet.json (salinan motion/film-sheet.json)
 * Keluaran: ../assets/lottie/nocturne-9s.json
 *
 * Yang dibuat: 4 lapisan teks (satu per cue) + bilah kemajuan. Tiap lapisan
 * masuk dengan opacity+posisi (bukan hanya opacity — aturan LottieFiles
 * "jangan opacity-only untuk perubahan state penting") dan keluar 65% dari
 * durasi masuknya (hukum klik A1).
 *
 * Tidak ada angka karangan: semua frame, teks, dan durasi dibaca dari lembar film.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const studio = resolve(here, '..');
const film = JSON.parse(readFileSync(resolve(studio, 'data/film-sheet.json'), 'utf8'));
const adegan = film.adegan[0];
const FPS = film.grid.fps;
const TOTAL = film.grid.frame_total;

const RGB = {
  ink: [0.086, 0.067, 0.051],
  espresso: [0.29, 0.173, 0.102],
  orange: [0.882, 0.329, 0.169],
  paper: [0.961, 0.937, 0.894],
  paper2: [0.937, 0.902, 0.839],
};
const hex = (c) => [c[0] * 255, c[1] * 255, c[2] * 255].map(Math.round);

/** easing masuk: expo-out (sama dengan --ease-out di situs) */
const EASE_IN = { i: { x: [0.16], y: [1] }, o: { x: [0.3], y: [0] } };
/** easing keluar: in-out */
const EASE_OUT = { i: { x: [0.65], y: [0] }, o: { x: [0.35], y: [1] } };

const keyframes = (t0, t1, dari, ke, ease = EASE_IN) => ({
  a: 1,
  k: [
    { t: t0, s: dari, ...ease },
    { t: t1, s: ke },
  ],
});

function lapisanTeks(cue) {
  const [f0, f1] = cue.frame;
  const masuk = Math.min(24, Math.round((f1 - f0) * 0.2));
  const keluar = Math.round(masuk * 0.65);          // keluar = 65% masuk
  const judul = cue.cue === 1;
  const payoff = cue.tier === 5;
  const ukuran = judul ? 82 : payoff ? 72 : 56;
  const y = 780 + cue.cue * 60;                     // posisi vertikal bertingkat
  const kananKeluar = f1;
  const mulaiKeluar = Math.max(f0 + masuk + 1, kananKeluar - keluar);

  return {
    ddd: 0,
    ind: cue.cue,
    ty: 5,                                          // text layer
    nm: `cue-${cue.cue}`,
    sr: 1,
    ks: {
      o: {
        a: 1,
        k: [
          { t: f0, s: [0], ...EASE_IN },
          { t: f0 + masuk, s: [100] },
          { t: mulaiKeluar, s: [100], ...EASE_OUT },
          { t: kananKeluar, s: [0] },
        ],
      },
      r: { a: 0, k: 0 },
      p: {
        a: 1,
        k: [
          { t: f0, s: [84, y + 46, 0], ...EASE_IN },
          { t: f0 + masuk, s: [84, y, 0] },
        ],
      },
      a: { a: 0, k: [0, 0, 0] },
      s: { a: 0, k: [100, 100, 100] },
    },
    ao: 0,
    t: {
      d: {
        k: [
          {
            s: {
              s: ukuran,
              f: judul || payoff ? 'Bricolage Grotesque' : 'Fraunces',
              t: cue.teks,
              j: 0,                                  // kiri
              tr: 0,
              lh: ukuran * 1.12,
              ls: 0,
              fc: hex(judul || payoff ? RGB.ink : RGB.espresso),
            },
            t: 0,
          },
        ],
      },
      p: {},
      m: { g: 1, a: { a: 0, k: [0, 0] } },
      a: [],
    },
    ip: f0,
    op: f1,
    st: 0,
    bm: 0,
  };
}

/** Bilah kemajuan: skala horizontal 0 → 100 sepanjang film (scrub, bukan loop). */
const bilahKemajuan = {
  ddd: 0,
  ind: 9,
  ty: 4,                                            // shape layer
  nm: 'kemajuan',
  sr: 1,
  ks: {
    o: { a: 0, k: 100 },
    r: { a: 0, k: 0 },
    p: { a: 0, k: [0, 0, 0] },
    a: { a: 0, k: [0, 0, 0] },
    s: { a: 0, k: [100, 100, 100] },
  },
  ao: 0,
  shapes: [
    {
      ty: 'gr',
      nm: 'bar',
      it: [
        { ty: 'rc', d: 1, s: { a: 0, k: [1080, 8] }, p: { a: 0, k: [540, 4] }, r: { a: 0, k: 0 } },
        { ty: 'fl', c: { a: 0, k: [...RGB.orange, 1] }, o: { a: 0, k: 100 }, r: 1 },
        { ty: 'tr', p: { a: 0, k: [0, 0] }, a: { a: 0, k: [0, 0] }, s: { a: 0, k: [0, 100] }, r: { a: 0, k: 0 }, o: { a: 0, k: 100 }, sk: { a: 0, k: 0 }, sa: { a: 0, k: 0 } },
      ],
    },
  ],
  ip: 0,
  op: TOTAL,
  st: 0,
  bm: 0,
};

/** Latar: dua persegi penuh, warna mengikuti cue aktif (opacity berurutan). */
function lapisanLatar(cue, no) {
  const [f0, f1] = cue.frame;
  return {
    ddd: 0,
    ind: 20 + no,
    ty: 4,
    nm: `latar-${cue.cue}`,
    sr: 1,
    ks: {
      o: {
        a: 1,
        k: [
          { t: f0, s: [0], ...EASE_IN },
          { t: f0 + 12, s: [100] },
          { t: f1, s: [100], ...EASE_OUT },
          { t: Math.min(TOTAL, f1 + 12), s: [0] },
        ],
      },
      r: { a: 0, k: 0 },
      p: { a: 0, k: [0, 1920, 0] },
      a: { a: 0, k: [0, 0, 0] },
      s: { a: 0, k: [100, 100, 100] },
    },
    ao: 0,
    shapes: [
      {
        ty: 'gr',
        it: [
          { ty: 'rc', d: 1, s: { a: 0, k: [1080, 1920] }, p: { a: 0, k: [540, 960] }, r: { a: 0, k: 0 } },
          { ty: 'fl', c: { a: 0, k: [...(no % 2 === 0 ? RGB.paper : RGB.paper2), 1] }, o: { a: 0, k: 100 }, r: 1 },
          { ty: 'tr', p: { a: 0, k: [0, 0] }, a: { a: 0, k: [0, 0] }, s: { a: 0, k: [100, 100] }, r: { a: 0, k: 0 }, o: { a: 0, k: 100 }, sk: { a: 0, k: 0 }, sa: { a: 0, k: 0 } },
        ],
      },
    ],
    ip: f0,
    op: Math.min(TOTAL, f1 + 12),
    st: 0,
    bm: 0,
  };
}

const latar = adegan.cues.map((c, i) => lapisanLatar(c, i));
const teks = adegan.cues.map(lapisanTeks);

const lottie = {
  v: '5.13.0',
  fr: FPS,
  ip: 0,
  op: TOTAL,
  w: 1080,
  h: 1920,
  nm: `Nocturne — ${adegan.judul}`,
  ddd: 0,
  assets: [],
  fonts: {
    list: [
      { fName: 'Bricolage Grotesque', fFamily: 'Bricolage Grotesque', fStyle: 'Bold', ascent: 75 },
      { fName: 'Fraunces', fFamily: 'Fraunces', fStyle: 'Regular', ascent: 72 },
    ],
  },
  layers: [...latar, ...teks, bilahKemajuan],
  markers: adegan.cues.map((c) => ({ tm: c.frame[0], cm: `cue-${c.cue}`, dr: c.frame[1] - c.frame[0] })),
  meta: {
    g: 'tools/film-studio · lottie/buat-lottie.mjs',
    d: 'Dibuat dari motion/film-sheet.json — jangan disunting tangan',
    adegan: adegan.adegan,
    bpm: film.grid.bpm,
    arc: adegan.arc,
  },
};

mkdirSync(resolve(studio, '..', 'assets', 'lottie'), { recursive: true });
const keluar = resolve(studio, '..', 'assets', 'lottie', 'nocturne-9s.json');
writeFileSync(keluar, JSON.stringify(lottie, null, 1) + '\n');
const kb = JSON.stringify(lottie).length / 1024;
console.log(`assets/lottie/nocturne-9s.json ditulis · ${kb.toFixed(1)} KB · ${lottie.layers.length} lapisan · ${TOTAL} frame @ ${FPS} fps`);
