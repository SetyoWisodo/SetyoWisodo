/* ============================================================
   Nocturne — motion-ui.js  (komponen gerak, v1)

   Ditulis ulang sebagai vanilla JS dari pola tiga repo:
     · DavidHDev/react-bits   — SpotlightCard, CountUp, MagneticButton,
                                TextReveal (di sini tanpa React)
     · greensock/gsap-skills  — pin + scrub dikerjakan satu loop rAF,
                                hanya transform/opacity, listener pasif
     · pbakaus/impeccable     — tak ada overshoot, tak ada kedip/denyut,
                                efek pointer mati di perangkat sentuh

   Cara pakai (atribut, tanpa build step):
     data-ui="reveal"  [data-ui-delay="120"]
     data-ui="words"   ── teks dipecah per kata, naik berurutan
     data-ui="count"   data-to="79" data-prefix="Rp" data-suffix=".000"
     data-ui="spotlight"   (kartu/tombol; sorotan mengikuti kursor)
     data-ui="magnet"      (tombol; geser maksimal 6 px)
     data-ui="pin"         (bungkus .ui-pin__step untuk adegan bertahap)
     <div class="ui-progress"><i></i></div>   (bilah kemajuan gulir)

   Kontrak keras:
     · tanpa JS: tidak ada yang disembunyikan (CSS memakai html.ui-motion)
     · prefers-reduced-motion: seluruh efek dimatikan, isi tetap terbaca
     · semua listener scroll pasif; satu rAF per gulir; tanpa layout read
       di dalam loop kecuali getBoundingClientRect yang memang perlu
   ============================================================ */
(function () {
  'use strict';

  const html = document.documentElement;
  const REDUCE = window.matchMedia('(prefers-reduced-motion: reduce)');
  const FINE = window.matchMedia('(hover: hover) and (pointer: fine)');
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  let reduce = REDUCE.matches;
  const pinState = [];

  /* ── 1 · reveal & teks per kata ─────────────────────────── */
  function pecahKata(el) {
    if (el.dataset.uiSplit === '1') return;
    /* jangan pecah elemen yang punya markup di dalamnya (mis. <em>jujur</em>):
       memecah per kata akan menghapus tag dan mengubah tipografi brief */
    if (el.children.length > 0) {
      el.classList.add('ui-word-utuh');
      return;
    }
    const teks = el.textContent.trim().replace(/\s+/g, ' ');
    el.textContent = '';
    teks.split(' ').forEach((kata, i) => {
      const s = document.createElement('span');
      s.className = 'ui-word';
      s.style.setProperty('--w', i);
      s.textContent = kata;
      el.appendChild(s);
      if (i < teks.split(' ').length - 1) el.appendChild(document.createTextNode(' '));
    });
    el.dataset.uiSplit = '1';
    el.setAttribute('aria-label', teks);
  }

  /* ── 2 · hitung angka (CountUp) ─────────────────────────── */
  function hitungAngka(el) {
    const to = parseFloat(el.dataset.to || '0');
    const dari = parseFloat(el.dataset.from || '0');
    const desimal = parseInt(el.dataset.decimals || '0', 10);
    const awalan = el.dataset.prefix || '';
    const akhiran = el.dataset.suffix || '';
    const fmt = (n) => {
      const bulat = desimal > 0 ? n.toFixed(desimal) : Math.round(n).toString();
      const [utuh, sisa] = bulat.split('.');
      const ribuan = utuh.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
      return awalan + ribuan + (sisa ? ',' + sisa : '') + akhiran;
    };
    if (reduce || !isFinite(to)) { el.textContent = fmt(to); return; }
    const durasi = parseInt(el.dataset.duration || '900', 10);
    const mulai = performance.now();
    function langkah(t) {
      const p = clamp((t - mulai) / durasi, 0, 1);
      const e = 1 - Math.pow(1 - p, 3);            /* ease-out kubik, tanpa overshoot */
      el.textContent = fmt(dari + (to - dari) * e);
      if (p < 1) requestAnimationFrame(langkah);
    }
    requestAnimationFrame(langkah);
  }

  function siapkanReveal() {
    $$('[data-ui="words"]').forEach(pecahKata);
    const target = $$('[data-ui="reveal"], [data-ui="words"]').filter((el) => !el.classList.contains('ui-word-utuh'));
    if (!('IntersectionObserver' in window)) {
      target.forEach((el) => el.classList.add('ui-in'));
      $$('[data-ui="count"]').forEach(hitungAngka);
      return;
    }
    const io = new IntersectionObserver((masuk) => {
      masuk.forEach((e) => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const d = el.dataset.uiDelay;
        if (d) el.style.setProperty('--ui-delay', d + 'ms');
        el.classList.add('ui-in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.15 });
    target.forEach((el) => io.observe(el));

    const ioAngka = new IntersectionObserver((masuk) => {
      masuk.forEach((e) => {
        if (!e.isIntersecting) return;
        hitungAngka(e.target);
        ioAngka.unobserve(e.target);
      });
    }, { threshold: 0.4 });
    $$('[data-ui="count"]').forEach((el) => ioAngka.observe(el));
  }

  /* ── 3 · pin + langkah (semantik ScrollTrigger tanpa GSAP) ─ */
  function siapkanPin() {
    $$('[data-ui="pin"]').forEach((blok) => {
      const langkah = $$('.ui-pin__step', blok);
      if (!langkah.length) return;
      pinState.push({ blok, langkah, aktif: -1 });
    });
  }

  function perbaruiPin() {
    const vh = window.innerHeight;
    pinState.forEach((s) => {
      const r = s.blok.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      /* progres 0 → 1 selama blok melintasi viewport */
      const total = r.height + vh * 0.35;
      const p = clamp((vh * 0.35 - r.top) / Math.max(1, total - vh * 0.35), 0, 0.999);
      const idx = Math.min(s.langkah.length - 1, Math.floor(p * s.langkah.length));
      if (idx === s.aktif) return;
      s.aktif = idx;
      s.langkah.forEach((el, i) => el.classList.toggle('ui-on', i <= idx));
    });
  }

  /* ── 4 · bilah kemajuan ─────────────────────────────────── */
  function siapkanProgress() {
    const bar = $('.ui-progress i');
    if (!bar) return null;
    return bar;
  }

  /* ── 5 · efek pointer: spotlight & magnet ───────────────── */
  function siapkanPointer() {
    if (reduce || !FINE.matches) return;

    $$('[data-ui="spotlight"]').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left).toFixed(0) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top).toFixed(0) + 'px');
      }, { passive: true });
    });

    $$('[data-ui="magnet"]').forEach((el) => {
      const kuat = parseFloat(el.dataset.uiStrength || '6');
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
        const dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
        el.style.transform = 'translate3d(' + (dx * kuat).toFixed(1) + 'px,'
          + (dy * kuat * 0.6).toFixed(1) + 'px,0)';
      }, { passive: true });
      el.addEventListener('pointerleave', () => {
        el.style.transform = '';
      });
    });
  }

  /* ── 6 · satu loop gulir ────────────────────────────────── */
  function siapkanLoop(bar) {
    let ticking = false;
    function frame() {
      ticking = false;
      if (bar) {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        const p = max > 0 ? clamp(window.scrollY / max, 0, 1) : 0;
        bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
      }
      perbaruiPin();
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

  /* ── 7 · berhenti total saat reduced-motion berubah ─────── */
  function matikan() {
    html.classList.remove('ui-motion');
    $$('[data-ui]').forEach((el) => el.classList.add('ui-in'));
    pinState.forEach((s) => s.langkah.forEach((el) => el.classList.add('ui-on')));
  }

  function boot() {
    if (reduce) { matikan(); return; }
    html.classList.add('ui-motion');
    siapkanReveal();
    siapkanPin();
    siapkanPointer();
    siapkanLoop(siapkanProgress());
    html.classList.add('ui-ready');
  }

  if (REDUCE.addEventListener) {
    REDUCE.addEventListener('change', (e) => {
      reduce = e.matches;
      if (reduce) matikan();
    });
  }

  try {
    boot();
  } catch (err) {
    console.error('[Nocturne motion-ui]', err);
    matikan();
  }
})();
