/* ============================================================
   Nocturne — motion.js
   Lapisan gerak. Tanpa library, tanpa build step.
   Prinsip: transform + opacity saja, satu keluarga easing,
   stagger 60–90 ms, hormati prefers-reduced-motion.
   ============================================================ */
(function () {
  'use strict';

  const html = document.documentElement;
  const REDUCE = window.matchMedia('(prefers-reduced-motion: reduce)');
  const HOVER = window.matchMedia('(hover: hover) and (pointer: fine)');

  function staticMode() {
    html.classList.remove('motion');
    html.classList.add('no-motion', 'motion-ready');
  }
  if (REDUCE.matches) { staticMode(); return; }

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  /* ---------- 1 · bar kemajuan gulir ---------- */
  function initProgress() {
    if ($('.scrollbar')) return;
    const bar = document.createElement('div');
    bar.className = 'scrollbar';
    bar.setAttribute('aria-hidden', 'true');
    bar.innerHTML = '<i></i>';
    document.body.appendChild(bar);
  }

  /* ---------- 2 · reveal saat masuk viewport ---------- */
  const revealTargets = new Set();

  function markAll() {
    // kartu produk & paket: teks ikut naik, media pakai topeng (CSS)
    $$('.card').forEach((c, i) => {
      c.classList.add('rv');
      if (!c.style.getPropertyValue('--rv-delay')) {
        c.style.setProperty('--rv-delay', (i % 2) * 80 + 'ms');
      }
      revealTargets.add(c);
    });
    $$('.rail').forEach((r) => { r.classList.add('rv-fade'); revealTargets.add(r); });
    $$('.subs__cards, .member__steps, .steps').forEach((r) => revealTargets.add(r));
    $$('[data-rv]').forEach((el, i) => {
      el.classList.add('rv');
      const d = el.getAttribute('data-rv-delay');
      if (d) el.style.setProperty('--rv-delay', d);
      revealTargets.add(el);
    });
    // langkah member: index untuk stagger via --i
    $$('.member__steps li').forEach((li, i) => li.style.setProperty('--i', i));
  }

  function initObserver() {
    if (!('IntersectionObserver' in window)) {
      revealTargets.forEach((el) => el.classList.add('is-in'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const el = e.target;
        el.classList.add('is-in');
        io.unobserve(el);

        // kartu: beri kelas is-in juga ke media (topeng)
        if (el.classList.contains('card')) {
          const media = $('.card__media', el);
          if (media) media.classList.add('is-in');
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });

    revealTargets.forEach((el) => io.observe(el));
  }

  /* ---------- 3 · loop gulir: parallax, poster, quote, FAB ---------- */
  function initScrollLoop() {
    const bar = $('.scrollbar i');
    const hero = $('.hero');
    const heroTitle = $('.hero__title');
    const heroIntro = $('.hero__intro');
    const marquee = $('.marquee');
    const poster = $('.foot__poster');
    const quote = $('.manifesto__quote');
    const fab = $('.fab');
    const layers = $$('[data-parallax]').map((el) => ({
      el,
      k: parseFloat(el.getAttribute('data-parallax')) || 0.1
    }));

    let vh = window.innerHeight;
    let ticking = false;

    function frame() {
      ticking = false;
      const y = window.scrollY;
      const max = document.documentElement.scrollHeight - vh;

      if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? clamp(y / max, 0, 1) : 0) + ')';

      // hero: judul turun pelan & memudar (parallax keluar)
      if (hero && y < vh * 1.2) {
        const p = clamp(y / vh, 0, 1);
        if (heroTitle) heroTitle.style.transform = 'translate3d(0,' + (p * 58).toFixed(1) + 'px,0)';
        if (heroIntro) heroIntro.style.transform = 'translate3d(0,' + (p * 34).toFixed(1) + 'px,0)';
        if (marquee) marquee.style.transform = 'translate3d(' + (-p * 80).toFixed(1) + 'px,0)';
        if (hero) hero.style.opacity = String(clamp(1 - p * 0.5, 0, 1));
      }

      // parallax umum
      layers.forEach((l) => {
        const r = l.el.getBoundingClientRect();
        if (r.bottom < -100 || r.top > vh + 100) return;
        const mid = r.top + r.height / 2 - vh / 2;
        l.el.style.transform = 'translate3d(0,' + (-mid * l.k).toFixed(1) + 'px,0)';
      });

      // poster footer: bergeser horizontal selama footer terlihat
      if (poster) {
        const r = poster.getBoundingClientRect();
        if (r.bottom > 0 && r.top < vh) {
          const p = 1 - (r.top + r.height) / (vh + r.height); // 0 → 1
          poster.style.transform = 'translate3d(' + (-clamp(p, 0, 1) * 46).toFixed(1) + 'px,0)';
        }
      }

      // quote manifesto: naik & menguat mengikuti guliran
      if (quote) {
        const r = quote.getBoundingClientRect();
        if (r.bottom > 0 && r.top < vh) {
          const p = clamp((vh - r.top) / (vh * 0.9), 0, 1);
          quote.style.opacity = (0.35 + p * 0.65).toFixed(2);
          quote.style.transform = 'translate3d(0,' + ((1 - p) * 16).toFixed(1) + 'px,0)';
        }
      }

      // FAB muncul setelah hero lewat
      if (fab) fab.classList.toggle('is-in', y > 520);
    }

    window.addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(frame);
    }, { passive: true });

    window.addEventListener('resize', () => {
      vh = window.innerHeight;
      frame();
    });

    frame();
  }

  /* ---------- 4 · pointer: glow hero, magnet, tilt ---------- */
  function initPointer() {
    if (!HOVER.matches) return;

    // 4a · glow
    const hero = $('.hero');
    if (hero) {
      const glow = document.createElement('div');
      glow.className = 'cursor-glow';
      glow.setAttribute('aria-hidden', 'true');
      document.body.appendChild(glow);
      let gx = 0, gy = 0, tx = 0, ty = 0, on = false;

      hero.addEventListener('pointerenter', () => { glow.classList.add('is-on'); on = true; });
      hero.addEventListener('pointerleave', () => { glow.classList.remove('is-on'); on = false; });
      hero.addEventListener('pointermove', (e) => {
        tx = e.clientX; ty = e.clientY;
        if (!gx) { gx = tx; gy = ty; }
      }, { passive: true });

      (function glowLoop() {
        gx += (tx - gx) * 0.09;
        gy += (ty - gy) * 0.09;
        if (on) glow.style.transform = 'translate3d(' + gx.toFixed(1) + 'px,' + gy.toFixed(1) + 'px,0)';
        requestAnimationFrame(glowLoop);
      })();
    }

    // 4b · tombol magnetik
    $$('.btn, .fab').forEach((btn) => {
      btn.classList.add('mag');
      const strength = btn.classList.contains('fab') ? 5 : 7;
      btn.addEventListener('pointermove', (e) => {
        const r = btn.getBoundingClientRect();
        const dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
        const dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
        btn.style.transform = 'translate3d(' + (dx * strength).toFixed(1) + 'px,' + (dy * strength * 0.6).toFixed(1) + 'px,0)';
      });
      btn.addEventListener('pointerleave', () => {
        btn.style.transform = '';
      });
    });

    // 4c · tilt pada media kartu (maks 3,5° — lebih dari itu terasa mainan)
    $$('.card__media').forEach((media) => {
      const card = media.closest('.card');
      if (!card) return;
      let raf = 0, rx = 0, ry = 0, trx = 0, try_ = 0, active = false;

      const loop = () => {
        rx += (trx - rx) * 0.14;
        ry += (try_ - ry) * 0.14;
        media.style.transform = 'perspective(900px) rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg)';
        if (active || Math.abs(rx) > 0.02 || Math.abs(ry) > 0.02) raf = requestAnimationFrame(loop);
        else { raf = 0; media.style.transform = ''; }
      };

      card.addEventListener('pointermove', (e) => {
        if (!HOVER.matches) return;
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        try_ = clamp(px * 7, -3.5, 3.5);
        trx = clamp(-py * 7, -3.5, 3.5);
        active = true;
        if (!raf) raf = requestAnimationFrame(loop);
      });
      card.addEventListener('pointerleave', () => {
        trx = 0; try_ = 0; active = false;
        if (!raf) raf = requestAnimationFrame(loop);
      });
    });
  }

  /* ---------- 5 · harga berganti dengan geser ---------- */
  function initPriceSwap() {
    document.addEventListener('click', (e) => {
      const b = e.target.closest('.vbtn');
      if (!b) return;
      const card = b.closest('.card');
      const val = card && $('.price__value', card);
      if (!val) return;
      val.classList.remove('is-swap');
      void val.offsetWidth; /* paksa reflow agar animasi bisa diulang */
      val.classList.add('is-swap');
    });
  }

  /* ---------- 6 · kartu hero: index untuk stagger ---------- */
  function initHeroCards() {
    $$('.hcard').forEach((c, i) => {
      c.style.setProperty('--i', i % 9);
    });
  }

  /* ---------- 7 · kurangi gerak saat runtime ---------- */
  function watchReduce() {
    const onChange = () => {
      if (REDUCE.matches) staticMode();
    };
    if (REDUCE.addEventListener) REDUCE.addEventListener('change', onChange);
    else if (REDUCE.addListener) REDUCE.addListener(onChange);
  }

  /* ---------- boot ---------- */
  let booted = false;

  function boot() {
    booted = true;
    initProgress();
    initHeroCards();
    markAll();
    initObserver();
    initScrollLoop();
    initPointer();
    initPriceSwap();
    watchReduce();
    html.classList.add('motion-ready');
    window.setTimeout(() => {
      if (!html.classList.contains('motion-ready')) html.classList.remove('motion');
    }, 100);
  }

  // skrip sudah termuat — matikan jaring aman di index.html
  html.classList.add('motion-ready');

  function safeBoot() {
    try {
      boot();
    } catch (err) {
      // kalau ada yang gagal, konten tidak boleh tertinggal tersembunyi
      console.error('[Nocturne motion]', err);
      staticMode();
    }
  }

  // jaring aman terakhir: halaman tidak boleh punya bagian yang tak terlihat
  window.setTimeout(function () {
    if (!booted) { console.warn('[Nocturne motion] sinyal katalog tidak datang, gerak dimatikan'); staticMode(); }
  }, 4000);

  // site.js menandai selesai render katalog
  if (window.__nocturneReady) safeBoot();
  else document.addEventListener('nocturne:ready', safeBoot, { once: true });
})();
