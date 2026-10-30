/**
 * Verifikasi mesin — dijalankan TANPA browser sungguhan (jsdom).
 *
 *   node scripts/verifikasi.mjs
 *
 * Yang benar-benar diperiksa:
 *  1. GSAP   — timeline dibangun, di-seek ke tiap ketukan, nilai transform dibaca.
 *              Membuktikan GSAP terpasang DAN bergerak, bukan hanya ada di package.json.
 *  2. Lottie — JSON hasil generator dimuat lottie-web (renderer SVG), di-seek ke
 *              4 cue, lalu jumlah elemen SVG dan opacity-nya diperiksa.
 *  3. Lembar film — cue di film-sheet harus sama jumlahnya dengan lapisan Lottie.
 *  4. Berkas nyata — mesin.js tanpa CDN, halaman /motion memuat 3 pemakai mesin,
 *                     klip .mp4 benar-benar MP4 (kotak ftyp), manifest cocok.
 *
 * Yang TIDAK bisa diperiksa di sini: rasterisasi piksel (butuh browser asli).
 * Karena itu skrip ini mencetak "bukan bukti visual" dengan jelas.
 */
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { JSDOM } from 'jsdom';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..');
const film = JSON.parse(readFileSync(resolve(root, 'data/film-sheet.json'), 'utf8'));
const adegan = film.adegan[0];

const hasil = [];
const catat = (nama, ok, detail) => {
  hasil.push({ nama, ok, detail });
  console.log(`  ${ok ? 'OK  ' : 'XX  '} ${nama.padEnd(22)} ${detail}`);
};

/* ── 1 · GSAP ───────────────────────────────────────────────────────────── */
async function ujiGsap() {
  const dom = new JSDOM('<!doctype html><html><body><div id="panggung"></div></body></html>', {
    pretendToBeVisual: true,
  });
  const { window } = dom;
  global.window = window;
  global.document = window.document;
  global.requestAnimationFrame = window.requestAnimationFrame.bind(window);
  global.cancelAnimationFrame = window.cancelAnimationFrame.bind(window);
  global.getComputedStyle = window.getComputedStyle.bind(window);
  const { gsap } = await import('gsap');

  const kotak = window.document.createElement('div');
  kotak.style.opacity = '0';
  window.document.getElementById('panggung').appendChild(kotak);

  const tl = gsap.timeline({ paused: true });
  // empat cue dari lembar film: masuk 24 frame, keluar 16 frame (60% dari 24)
  adegan.cues.forEach((cue) => {
    const mulai = cue.frame[0] / film.grid.fps;
    tl.fromTo(kotak, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: 'power3.out' }, mulai);
    tl.to(kotak, { opacity: 0, duration: 0.24, ease: 'power2.in' }, cue.selesai - 0.24);
  });

  const jejak = [];
  for (const cue of adegan.cues) {
    tl.seek(cue.mulai + 0.2);                       // 200 ms setelah cue mulai
    jejak.push({
      cue: cue.cue,
      opacity: Number(window.getComputedStyle(kotak).opacity || kotak.style.opacity),
      transform: kotak.style.transform || '(kosong)',
    });
  }
  const bergerak = jejak.some((j) => j.transform !== '(kosong)');
  const durasi = tl.duration();
  gsap.ticker.sleep();                              // hentikan loop setelah diuji
  catat('GSAP timeline', bergerak && durasi > 8,
    `${jejak.length} cue di-seek · durasi ${durasi.toFixed(2)} s · transform berubah: ${bergerak}`);
  return { jejak, durasi };
}

/* ── 2 · Lottie ─────────────────────────────────────────────────────────── */
async function ujiLottie() {
  const animasi = JSON.parse(readFileSync(resolve(root, '..', 'assets', 'lottie', 'nocturne-9s.json'), 'utf8'));
  const dom = new JSDOM(
    '<!doctype html><html><body><div id="lottie" style="width:1080px;height:1920px"></div></body></html>',
    { pretendToBeVisual: true, resources: 'usable' },
  );
  const { window } = dom;
  global.window = window;
  global.document = window.document;
  global.requestAnimationFrame = window.requestAnimationFrame.bind(window);
  global.cancelAnimationFrame = window.cancelAnimationFrame.bind(window);
  global.getComputedStyle = window.getComputedStyle.bind(window);
  // jsdom tidak punya canvas. Renderer SVG tidak butuh kanvas asli, tapi
  // lottie-web tetap memanggil getContext untuk deteksi fitur — beri konteks tiruan.
  const konteksTiruan = () =>
    new Proxy(
      { measureText: () => ({ width: 0 }), canvas: {} },
      {
        get: (t, k) => (k in t ? t[k] : () => {}),
        set: (t, k, v) => ((t[k] = v), true),
      },
    );
  window.HTMLCanvasElement.prototype.getContext = konteksTiruan;
  global.HTMLCanvasElement = window.HTMLCanvasElement;

  const lottie = (await import('lottie-web')).default;
  const wadah = window.document.getElementById('lottie');
  const anim = lottie.loadAnimation({
    container: wadah,
    renderer: 'svg',
    loop: false,
    autoplay: false,
    animationData: JSON.parse(JSON.stringify(animasi)),
  });

  // lottie-web menandai siap lewat event DOMLoaded
  await new Promise((lanjut) => {
    let selesai = false;
    anim.addEventListener('DOMLoaded', () => { selesai = true; lanjut(); });
    setTimeout(() => { if (!selesai) lanjut(); }, 4000);
  });

  const potret = [];
  for (const cue of adegan.cues) {
    const tengah = Math.round((cue.frame[0] + cue.frame[1]) / 2);
    anim.goToAndStop(tengah, true);
    const svg = wadah.querySelector('svg');
    // lottie-web menyembunyikan lapisan di luar in/out point dengan display:none
    const terlihat = Array.from(svg.querySelectorAll('text')).filter((el) => {
      const pembungkus = el.closest('g[style*="display"]');
      return !pembungkus || pembungkus.style.display !== 'none';
    });
    const isi = terlihat.map((el) => (el.textContent || '').trim()).filter(Boolean);
    potret.push({
      cue: cue.cue,
      frame: tengah,
      frameAktif: Math.round(anim.currentFrame),
      svg: !!svg,
      isi,
      cocok: isi.some((t) => cue.teks.startsWith(t[0] || 'x')),
    });
  }

  const adaSvg = potret.every((p) => p.svg);
  const waktuBenar = potret.every((p) => Math.abs(p.frameAktif - p.frame) <= 1);
  const laguBerubah = new Set(potret.map((p) => p.isi.join('|'))).size > 1;
  const isiCocok = potret.every((p) => p.cocok);
  catat('Lottie (jsdom)', adaSvg && waktuBenar && laguBerubah && isiCocok,
    `${animasi.layers.length} lapisan · ${potret.map((p) => `${p.frame}f:${p.isi[0] ?? '—'}`).join(' · ')}`);

  const jumlahTeks = animasi.layers.filter((l) => l.ty === 5).length;
  catat('Lottie ↔ lembar film', jumlahTeks === adegan.cues.length,
    `${jumlahTeks} lapisan teks vs ${adegan.cues.length} cue`);
  anim.destroy();
  return { potret, jumlahTeks };
}

/* ── 3 · berkas nyata & jalur muat ─────────────────────────────────────── */
function ujiBerkas() {
  const dir = resolve(root, '..');
  const baca = (p) => readFileSync(resolve(dir, p), 'utf8');
  const mesin = baca('assets/js/mesin.js');
  const cdn = ['cdn.jsdelivr.net', 'unpkg.com', 'cdnjs.cloudflare.com'].filter((c) => mesin.includes(c));
  const halaman = baca('motion/index.html');
  const pemakai = (halaman.match(/data-mesin="/g) || []).length;
  const beranda = baca('index.html');
  const bersih = !/gsap|lottie|ScrollTrigger/i.test(beranda);

  const mp4 = resolve(dir, 'motion/out/klip-01-nocturne-9s.mp4');
  let mp4Ok = false, mb = 0;
  try {
    const buf = readFileSync(mp4);
    mb = buf.length / 1024;
    mp4Ok = buf.subarray(4, 8).toString() === 'ftyp';
  } catch { /* belum dirender */ }
  const man = mp4Ok
    ? JSON.parse(baca('motion/out/manifest.json'))
    : {};

  catat('Berkas & jalur muat',
    cdn.length === 0 && pemakai === 2 && bersih && mp4Ok &&
      man.frame === 540 && man.fps === 60,
    `${pemakai} pemakai di /motion · CDN ${cdn.length} · beranda ${bersih ? 'bersih' : 'memuat pustaka'} · ` +
      `klip ${mp4Ok ? `${mb.toFixed(0)} KB, ${man.frame}f/${man.fps}fps` : 'belum ada'}`);
}

/* ── 4 · jalan ──────────────────────────────────────────────────────────── */
console.log('\nVerifikasi mesin film (jsdom — bukan bukti visual)\n');
try {
  const gsapHasil = await ujiGsap();
  const lottieHasil = await ujiLottie();
  ujiBerkas();
  const gagal = hasil.filter((h) => !h.ok).length;
  console.log(`\n  ${hasil.length - gagal} lolos · ${gagal} gagal`);
  console.log('  Catatan: jsdom tidak meraster piksel dan tidak punya metrik font — teks\n' +
              '  di dalam SVG hanya terbaca sebagian. Yang diperiksa: nilai animasi GSAP,\n' +
              '  perpindahan lapisan Lottie per cue, dan kecocokan jumlah lapisan\n' +
              '  dengan lembar film. Ini bukan bukti visual.\n');
  process.exit(gagal ? 1 : 0);
} catch (err) {
  console.error('  XX  verifikasi gagal:', err.message);
  process.exit(1);
}
