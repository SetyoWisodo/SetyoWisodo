/* ============================================================
   Nocturne — motion-3d.js  (panggung 3D, v1)

   Menghidupkan tiga komponen yang dibaca dari galeri desain pada
   post @viktoroddy (30 Okt 2026):
     · panggung   — kamera mengikuti kursor (maks 14°) dan mundur
                    saat halaman digulir (dolly, bukan parallax liar)
     · silinder   — 5 klip di satu lingkaran; tombol & panah kiri/kanan
                    memutar 72° per langkah
     · kartu timbul — kemiringan maks 8°, memakai sorotan yang sama
                    dengan data-ui="spotlight"

   Kontrak keras:
     · kelas html.ui-3d hanya dipasang bila JS jalan, layar ≥ 900 px,
       dan pengguna tidak meminta reduced-motion. Tanpa itu semua
       lapisan jatuh datar dan isi tetap terbaca.
     · hanya transform & opacity yang disentuh; satu rAF saat gulir;
       semua listener pasif.
   ============================================================ */
(function () {
  'use strict';

  const html = document.documentElement;
  const KURANGI = window.matchMedia('(prefers-reduced-motion: reduce)');
  const PRESISI = window.matchMedia('(hover: hover) and (pointer: fine)');
  const LEBAR = window.matchMedia('(min-width: 900px)');
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const jepit = (v, a, b) => Math.min(b, Math.max(a, v));

  let reduce = KURANGI.matches;
  const panggung = [];
  const silinder = [];

  /* ── 1 · panggung: kursor + dolly gulir ─────────────────── */
  function siapkanPanggung() {
    $$('[data-3d="panggung"]').forEach((el) => {
      const objek = $('[data-3d-objek]', el);
      if (!objek) return;
      panggung.push({ el, objek });
    });
  }

  function pasangKursor() {
    if (!PRESISI.matches) return;
    panggung.forEach(({ el, objek }) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const nx = (e.clientX - r.left) / Math.max(1, r.width) - 0.5;
        const ny = (e.clientY - r.top) / Math.max(1, r.height) - 0.5;
        objek.style.setProperty('--ry', (nx * 14).toFixed(2) + 'deg');
        objek.style.setProperty('--rx', (-ny * 8).toFixed(2) + 'deg');
      }, { passive: true });
      el.addEventListener('pointerleave', () => {
        objek.style.setProperty('--ry', '0deg');
        objek.style.setProperty('--rx', '0deg');
      }, { passive: true });
    });
  }

  function dolly() {
    const vh = window.innerHeight;
    panggung.forEach(({ el, objek }) => {
      const r = el.getBoundingClientRect();
      const p = jepit((vh * 0.55 - r.top) / Math.max(1, r.height), 0, 1);
      objek.style.setProperty('--pz', (-150 * p).toFixed(0) + 'px');
    });
  }

  /* ── 2 · kartu timbul ───────────────────────────────────── */
  function siapkanTimbul() {
    if (!PRESISI.matches) return;
    $$('[data-3d="timbul"]').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const nx = (e.clientX - r.left) / Math.max(1, r.width) - 0.5;
        const ny = (e.clientY - r.top) / Math.max(1, r.height) - 0.5;
        el.style.setProperty('--ty', (nx * 8).toFixed(2) + 'deg');
        el.style.setProperty('--tx', (-ny * 6).toFixed(2) + 'deg');
      }, { passive: true });
      el.addEventListener('pointerleave', () => {
        el.style.setProperty('--ty', '0deg');
        el.style.setProperty('--tx', '0deg');
      }, { passive: true });
    });
  }

  /* ── 3 · silinder klip ──────────────────────────────────── */
  function siapkanSilinder() {
    $$('[data-3d="silinder"]').forEach((bungkus) => {
      const rim = $('.silinder__rim', bungkus);
      const pane = $$('.silinder__pane', bungkus);
      if (!rim || pane.length < 2) return;
      const cap = $('.silinder__cap', bungkus);
      const hitung = $('[data-hitungan]', bungkus);
      const langkah = 360 / pane.length;
      let aktif = 0;

      pane.forEach((p, i) => p.style.setProperty('--i', i));

      function lukis() {
        rim.style.setProperty('--sudut', (-aktif * langkah).toFixed(1) + 'deg');
        pane.forEach((p, i) => p.classList.toggle('is-on', i === aktif));
        const fig = $('figcaption', pane[aktif]);
        if (cap) cap.textContent = fig ? fig.textContent.replace(/\s+/g, ' ').trim() : '';
        if (hitung) hitung.textContent = (aktif + 1) + ' / ' + pane.length;
      }

      $$('[data-putar]', bungkus).forEach((btn) => {
        btn.addEventListener('click', () => {
          const arah = parseInt(btn.dataset.putar || '1', 10);
          aktif = (aktif + arah + pane.length) % pane.length;
          lukis();
        });
      });

      bungkus.addEventListener('keydown', (e) => {
        if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
        e.preventDefault();
        aktif = (aktif + (e.key === 'ArrowRight' ? 1 : -1) + pane.length) % pane.length;
        lukis();
      });

      silinder.push({ bungkus, lukis });
      lukis();
    });
  }

  /* ── 4 · satu loop gulir ────────────────────────────────── */
  function siapkanLoop() {
    let ticking = false;
    function frame() {
      ticking = false;
      dolly();
    }
    window.addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(frame);
    }, { passive: true });
    window.addEventListener('resize', () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(frame);
    }, { passive: true });
    frame();
  }

  /* ── 5 · mode 3D: hidup/hidupkan ulang ──────────────────── */
  function aturMode() {
    const bisa = !reduce && LEBAR.matches;
    html.classList.toggle('ui-3d', bisa);
    if (!bisa) {
      panggung.forEach(({ objek }) => {
        objek.style.setProperty('--rx', '0deg');
        objek.style.setProperty('--ry', '0deg');
        objek.style.setProperty('--pz', '0px');
      });
    }
    silinder.forEach((s) => s.lukis());
  }

  function matikan() {
    html.classList.remove('ui-3d');
  }

  function boot() {
    siapkanPanggung();
    siapkanSilinder();
    if (reduce) { matikan(); return; }
    aturMode();
    pasangKursor();
    siapkanTimbul();
    siapkanLoop();
  }

  ['(prefers-reduced-motion: reduce)', '(min-width: 900px)'].forEach((q) => {
    const mq = window.matchMedia(q);
    if (!mq.addEventListener) return;
    mq.addEventListener('change', () => {
      reduce = KURANGI.matches;
      aturMode();
    });
  });

  try {
    boot();
  } catch (err) {
    console.error('[Nocturne motion-3d]', err);
    matikan();
  }
})();
