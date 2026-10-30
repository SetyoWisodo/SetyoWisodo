/**
 * Generator komposisi HyperFrames — 9 detik, dari lembar film.
 *
 *   node scripts/buat-hyperframes.mjs
 *
 * Keluaran:
 *   hyperframes/index.html              root: hanya mount + bilah kemajuan
 *   hyperframes/compositions/cue-N.html 4 sub-komposisi (satu per cue)
 *
 * Alasan strukturnya begini: `hyperframes lint` memberi tahu bahwa elemen
 * timeline yang berisi markup bertingkat harus jadi sub-komposisi dan dipasang
 * lewat `data-composition-src`. Root hanya boleh berisi mount. Itu diikuti,
 * bukan dilawan.
 *
 * GSAP diambil dari vendor lokal (`hyperframes/vendor/gsap.min.js`), bukan CDN.
 */
import { readFileSync, writeFileSync, copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const studio = resolve(here, '..');
const film = JSON.parse(readFileSync(resolve(studio, 'data/film-sheet.json'), 'utf8'));
const adegan = film.adegan[0];
const { bpm, frame_total: total, fps } = film.grid;
const durasiDetik = total / fps;

const esc = (s) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const AKAR = `      /* font brand: berkas lokal, bukan CDN — lint HyperFrames menolak keluarga
         font tanpa @font-face karena renderer tidak bisa menebak berkasnya */
      @font-face { font-family: "Bricolage Grotesque"; font-weight: 800; font-display: block;
                   src: url("__FONT__/bricolage-800.ttf") format("truetype"); }
      @font-face { font-family: "Fraunces"; font-weight: 300; font-display: block;
                   src: url("__FONT__/fraunces-300.ttf") format("truetype"); }
      @font-face { font-family: "Inter"; font-weight: 400; font-display: block;
                   src: url("__FONT__/inter-400.ttf") format("truetype"); }
      @font-face { font-family: "Inter"; font-weight: 600; font-display: block;
                   src: url("__FONT__/inter-600.ttf") format("truetype"); }
      :root {
        --paper: #f5efe4; --paper-2: #efe6d6; --ink: #16110d;
        --orange: #e1542b; --espresso: #4a2c1a;
        --display: "Bricolage Grotesque", sans-serif;
        --serif: "Fraunces", serif;
        --body: "Inter", sans-serif;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: transparent; }`;

/* ── satu cue = satu sub-komposisi ─────────────────────────────────────── */
const akarUntuk = (awalanFont) => AKAR.replace(/__FONT__/g, awalanFont);

function subKomposisi(c) {
  const lama = (c.frame[1] - c.frame[0]) / fps;
  const besar = c.cue === 1 ? 92 : c.tier === 5 ? 84 : 62;
  const dis = c.cue === 1 || c.tier === 5;
  const masuk = Math.min(0.4, lama * 0.2);
  const keluar = masuk * 0.65;                       // keluar 65% durasi masuk
  return `<!doctype html>
<html lang="id">
  <head>
    <meta charset="utf-8" />
    <script src="../vendor/gsap.min.js"></script>
    <style>
${akarUntuk('../vendor/fonts')}
      #cue-${c.cue} {
        width: 1080px; height: 1920px; padding: 300px 84px 240px;
        display: flex; flex-direction: column; justify-content: center;
        font-family: var(--body); color: var(--ink);
      }
      .label { font-size: 22px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--espresso); margin-bottom: 34px; }
      .teks { line-height: 0.98; letter-spacing: -0.025em; max-width: 960px;
              font-size: ${besar}px; font-family: ${dis ? 'var(--display)' : 'var(--serif)'};
              font-weight: ${dis ? 800 : 300}; }
      .garis { width: 120px; height: 4px; background: var(--ink); margin-top: 40px; }
      .garis--oranye { background: var(--orange); }
      .kecil { margin-top: 22px; font-size: 20px; letter-spacing: 0.1em; color: rgba(22, 17, 13, 0.55); }
    </style>
  </head>
  <body>
    <div id="cue-${c.cue}" data-composition-id="cue-${c.cue}" data-start="0"
         data-duration="${lama}" data-width="1080" data-height="1920">
      <p class="label">${esc(c.perangkat)} · tier ${c.tier}</p>
      <h1 class="teks">${esc(c.teks)}</h1>
      <div class="garis${c.tier === 5 ? ' garis--oranye' : ''}"></div>
      <p class="kecil">cue ${c.cue} · ${c.mulai}s–${c.selesai}s · ${esc(c.sumber)}</p>
    </div>
    <script>
      /* timeline sub-komposisi: paused, tanpa jam internal. Perender yang men-seek. */
      const tl = gsap.timeline({ paused: true });
      tl.fromTo(".teks", { y: 46, opacity: 0 }, { y: 0, opacity: 1, duration: ${masuk.toFixed(2)}, ease: "power3.out" }, 0);
      tl.fromTo(".label", { opacity: 0 }, { opacity: 1, duration: 0.24 }, 0);
      tl.to("#cue-${c.cue}", { opacity: 0, duration: ${keluar.toFixed(2)}, ease: "power2.in" }, ${Math.max(0.1, lama - keluar).toFixed(2)});
      window.__timelines = window.__timelines || {};
      window.__timelines["cue-${c.cue}"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
`;
}

/* ── root: mount + lapisan milik root ──────────────────────────────────── */
const mount = adegan.cues
  .map((c) => {
    const mulai = (c.frame[0] / fps).toFixed(2);
    const lama = ((c.frame[1] - c.frame[0]) / fps).toFixed(2);
    return `      <div class="mount" id="mount-cue-${c.cue}" data-composition-id="cue-${c.cue}"
           data-composition-src="./compositions/cue-${c.cue}.html"
           data-start="${mulai}" data-duration="${lama}" data-track-index="${c.cue - 1}"></div>`;
  })
  .join('\n');

const html = `<!doctype html>
<html lang="id" data-resolution="portrait">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Nocturne — ${esc(adegan.judul)}</title>
    <script src="./vendor/gsap.min.js"></script>
    <style>
${akarUntuk('./vendor/fonts')}
      #root { position: relative; width: 1080px; height: 1920px; background: var(--paper); }
      .latar { position: absolute; inset: 0; background: var(--paper-2); }
      .kemajuan { position: absolute; top: 0; left: 0; height: 8px; width: 1080px;
                  background: var(--orange); transform-origin: 0 50%; transform: scaleX(0); }
      .mount { position: absolute; inset: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${durasiDetik}"
         data-width="1080" data-height="1920">
      <div class="latar" id="latar"></div>
      <div class="kemajuan" id="kemajuan"></div>
${mount}
    </div>
    <script>
      /* Timeline root: hanya lapisan milik root. Gerak per cue ada di sub-komposisi.
         ${bpm} BPM · ${total} frame @ ${fps} fps · arc ${adegan.arc} */
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#kemajuan", { scaleX: 0 }, { scaleX: 1, duration: ${durasiDetik}, ease: "none" }, 0);
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
`;

const hfJson = {
  $schema: 'https://hyperframes.heygen.com/schema/hyperframes.json',
  registry: 'https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry',
  paths: { blocks: 'compositions', components: 'compositions/components', assets: 'vendor' },
  media: { autoProxy: false },
};

const metaJson = {
  id: 'nocturne-klip-9s',
  name: 'Nocturne — klip 9 detik',
  createdAt: '2026-10-30T00:00:00.000Z',
  catatan:
    'Dibuat scripts/buat-hyperframes.mjs dari motion/film-sheet.json. Jangan disunting tangan.',
};

mkdirSync(resolve(studio, 'hyperframes/vendor'), { recursive: true });
mkdirSync(resolve(studio, 'hyperframes/compositions'), { recursive: true });
mkdirSync(resolve(studio, 'hyperframes/vendor/fonts'), { recursive: true });
for (const [dari, ke] of [
  ['bricolage-grotesque-latin-800-normal.ttf', 'bricolage-800.ttf'],
  ['fraunces-latin-300-normal.ttf', 'fraunces-300.ttf'],
  ['inter-latin-400-normal.ttf', 'inter-400.ttf'],
  ['inter-latin-600-normal.ttf', 'inter-600.ttf'],
]) {
  const asal = resolve(studio, '..', 'assets', 'fonts', dari);
  if (existsSync(asal)) copyFileSync(asal, resolve(studio, 'hyperframes/vendor/fonts', ke));
}
const gsapVendor = resolve(studio, 'node_modules/gsap/dist/gsap.min.js');
if (!existsSync(resolve(studio, 'hyperframes/vendor/gsap.min.js')) && existsSync(gsapVendor)) {
  copyFileSync(gsapVendor, resolve(studio, 'hyperframes/vendor/gsap.min.js'));
}

for (const c of adegan.cues) {
  writeFileSync(resolve(studio, `hyperframes/compositions/cue-${c.cue}.html`), subKomposisi(c));
}
writeFileSync(resolve(studio, 'hyperframes/index.html'), html);
writeFileSync(resolve(studio, 'hyperframes/hyperframes.json'), JSON.stringify(hfJson, null, 2) + '\n');
writeFileSync(resolve(studio, 'hyperframes/meta.json'), JSON.stringify(metaJson, null, 2) + '\n');

console.log(
  `hyperframes/index.html + ${adegan.cues.length} sub-komposisi · ${durasiDetik} detik · ` +
    `${bpm} BPM · gsap lokal (bukan CDN)`,
);
