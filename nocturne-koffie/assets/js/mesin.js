/* ============================================================
   Nocturne — mesin.js  (GSAP + Lottie, dimuat malas)

   Dua pustaka yang sekarang benar-benar terpasang di repo:
     · GSAP 3.15 (assets/vendor/gsap.min.js + ScrollTrigger.min.js)
     · lottie-web 5.13 (assets/vendor/lottie.min.js)

   Aturan pemuatan (supaya halaman awal tetap ringan):
     1. TIDAK ADA skrip ini di atas fold. Berkas ini sendiri kecil; GSAP dan
        Lottie baru diunduh saat bagian yang memakainya masuk viewport.
     2. Tanpa CDN: semuanya berkas lokal di assets/vendor/.
     3. Kalau pustaka gagal dimuat (berkas hilang), bagian itu tetap terbaca
        statis — tidak ada konten yang disembunyikan.
     4. prefers-reduced-motion: GSAP langsung diarahkan ke keadaan akhir,
        Lottie diparkir di frame terakhir cue; tidak ada yang bergerak.

   Atribut:
     data-mesin="gsap"    → timeline 4 cue dari lembar film (grid ketukan)
     data-mesin="lottie"  → pemutar Lottie 9 detik + kontrol cue
   ============================================================ */
(function () {
  'use strict';

  const html = document.documentElement;
  const KURANGI = window.matchMedia('(prefers-reduced-motion: reduce)');
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const muat = new Map();

  function skrip(src) {
    if (muat.has(src)) return muat.get(src);
    const p = new Promise((ok, gagal) => {
      const s = document.createElement('script');
      s.src = src;
      s.async = true;
      s.onload = () => ok(true);
      s.onerror = () => gagal(new Error('gagal memuat ' + src));
      document.head.appendChild(s);
    });
    muat.set(src, p);
    return p;
  }

  function saatTerlihat(el, fn) {
    if (!('IntersectionObserver' in window)) { fn(); return; }
    const io = new IntersectionObserver((masuk) => {
      if (!masuk.some((m) => m.isIntersecting)) return;
      io.disconnect();
      fn();
    }, { rootMargin: '200px 0px' });
    io.observe(el);
  }

  /* ── 1 · GSAP: timeline ketukan ─────────────────────────────────────── */
  function siapkanGsap() {
    $$('[data-mesin="gsap"]').forEach((blok) => {
      saatTerlihat(blok, () => {
        skrip('../assets/vendor/gsap.min.js')
          .then(() => skrip('../assets/vendor/ScrollTrigger.min.js').catch(() => null))
          .then(() => {
            const gsap = window.gsap;
            if (!gsap) return;
            if (window.ScrollTrigger) gsap.registerPlugin(window.ScrollTrigger);

            const batang = $$('[data-ketukan]', blok);
            const kurangi = KURANGI.matches;
            const tl = gsap.timeline({
              paused: true,
              defaults: { ease: 'power3.out' },
              onComplete: () => blok.classList.add('mesin-selesai'),
            });

            batang.forEach((b, i) => {
              const tinggi = Number(b.dataset.ketukan || 0);
              tl.fromTo(b,
                { scaleY: kurangi ? tinggi / 100 : 0.08, opacity: 0.4 },
                { scaleY: tinggi / 100, opacity: 1, duration: kurangi ? 0 : 0.42 },
                kurangi ? 0 : i * 0.09);
            });

            blok.dataset.mesinSiap = 'gsap';

            if (kurangi) { tl.progress(1); return; }

            if (window.ScrollTrigger) {
              window.ScrollTrigger.create({
                trigger: blok,
                start: 'top 78%',
                once: true,
                onEnter: () => tl.play(0),
              });
            } else {
              tl.play(0);
            }

            // tombol putar ulang (kontrol nyata, bukan hiasan)
            $$('[data-mesin-ulang]', blok).forEach((btn) => {
              btn.addEventListener('click', () => tl.play(0));
            });
          })
          .catch((e) => {
            blok.dataset.mesinGagal = e.message;
            console.warn('[mesin]', e.message);
          });
      });
    });
  }

  /* ── 2 · Lottie: pemutar 9 detik ────────────────────────────────────── */
  function siapkanLottie() {
    $$('[data-mesin="lottie"]').forEach((blok) => {
      const wadah = $('[data-lottie-tempat]', blok);
      if (!wadah) return;

      saatTerlihat(blok, () => {
        skrip('../assets/vendor/lottie.min.js')
          .then(() => fetch(blok.dataset.lottieSumber || '../assets/lottie/nocturne-9s.json'))
          .then((r) => r.json())
          .then((data) => {
            const lottie = window.lottie || window.bodymovin;
            if (!lottie) throw new Error('lottie tidak ada di window');

            const anim = lottie.loadAnimation({
              container: wadah,
              renderer: 'svg',
              loop: false,
              autoplay: false,
              animationData: data,
              rendererSettings: { preserveAspectRatio: 'xMidYMid meet' },
            });

            const total = data.op || 540;
            const fps = data.fr || 60;
            const sliders = $('[data-lottie-slider]', blok);
            const waktu = $('[data-lottie-waktu]', blok);
            const tombol = $('[data-lottie-putar]', blok);
            const cueLabel = $('[data-lottie-cue]', blok);
            let jalan = false;
            let raf = 0;

            const format = (f) => (f / fps).toFixed(2).replace('.', ',') + ' s';

            function lukis() {
              const f = Math.round(anim.currentFrame);
              if (sliders) sliders.value = String(f);
              if (waktu) waktu.textContent = format(f);
              const cue = (data.markers || []).filter((m) => m.tm <= f).pop();
              if (cueLabel) cueLabel.textContent = cue ? cue.cm.replace('cue-', 'cue ') : '—';
            }

            function loop() {
              if (!jalan) return;
              if (anim.currentFrame >= total - 1) {
                jalan = false;
                if (tombol) tombol.textContent = 'Putar ulang';
              }
              raf = requestAnimationFrame(loop);
            }

            if (tombol) {
              tombol.addEventListener('click', () => {
                if (jalan) {
                  anim.pause(); jalan = false; tombol.textContent = 'Putar';
                } else {
                  if (anim.currentFrame >= total - 2) anim.goToAndStop(0, true);
                  anim.play(); jalan = true; tombol.textContent = 'Jeda';
                  cancelAnimationFrame(raf); loop();
                }
              });
            }

            if (sliders) {
              sliders.max = String(total - 1);
              sliders.addEventListener('input', () => {
                jalan = false;
                anim.pause();
                anim.goToAndStop(Number(sliders.value), true);
                if (tombol) tombol.textContent = 'Putar';
                lukis();
              });
            }

            anim.addEventListener('enterFrame', lukis);
            anim.addEventListener('DOMLoaded', () => {
              anim.goToAndStop(KURANGI.matches ? total - 1 : 0, true);
              lukis();
            });

            blok.dataset.mesinSiap = 'lottie';
            if (KURANGI.matches) {
              anim.goToAndStop(Math.round(total * 0.86), true);
              lukis();
            }
          })
          .catch((e) => {
            blok.dataset.mesinGagal = e.message;
            console.warn('[mesin]', e.message);
          });
      });
    });
  }

  function mulai() {
    siapkanGsap();
    siapkanLottie();
    html.classList.add('mesin-aktif');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mulai, { once: true });
  } else {
    mulai();
  }
})();
