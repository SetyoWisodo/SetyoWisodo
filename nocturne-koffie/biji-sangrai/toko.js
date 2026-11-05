/* ============================================================
   Nocturne Koffie — biji sangrai
   Tanpa pustaka, tanpa CDN. Semua efek dimatikan kalau pengguna
   memilih "kurangi gerak" (prefers-reduced-motion).
   ============================================================ */
(function () {
  'use strict';

  /* matchMedia tidak selalu ada (peramban lama, lingkungan uji): anggap saja
     pengguna tidak minta gerak dikurangi, jangan sampai seluruh skrip mati. */
  var kurangi = typeof window.matchMedia === 'function'
    ? window.matchMedia('(prefers-reduced-motion: reduce)')
    : { matches: false };
  var santai = function () { return !!kurangi.matches; };

  /* ---------- 1 · jam Banyuwangi (WIB) ---------- */
  function jam() {
    var el = document.getElementById('jam');
    var kaki = document.getElementById('jam-kaki');
    if (!el && !kaki) return;
    var f = new Intl.DateTimeFormat('id-ID', {
      timeZone: 'Asia/Jakarta',
      hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
    });
    var fpendek = new Intl.DateTimeFormat('id-ID', {
      timeZone: 'Asia/Jakarta', hour: '2-digit', minute: '2-digit', hour12: false
    });
    function tulis() {
      var kini = new Date();
      if (el) el.textContent = f.format(kini).replace(/\./g, ':');
      if (kaki) kaki.textContent = fpendek.format(kini).replace(/\./g, ':');
    }
    tulis();
    setInterval(tulis, 1000);
  }

  /* ---------- 2 · bilah atas + garis kemajuan ---------- */
  function bilah() {
    var bar = document.getElementById('bar');
    var prog = document.getElementById('prog');
    var nunggu = false;
    function gambar() {
      nunggu = false;
      var y = window.scrollY || window.pageYOffset;
      if (bar) bar.classList.toggle('is-lekat', y > 24);
      if (prog) {
        var tinggi = document.documentElement.scrollHeight - window.innerHeight;
        var rasio = tinggi > 0 ? Math.min(1, Math.max(0, y / tinggi)) : 0;
        prog.style.transform = 'scaleX(' + rasio.toFixed(4) + ')';
      }
    }
    window.addEventListener('scroll', function () {
      if (!nunggu) { nunggu = true; requestAnimationFrame(gambar); }
    }, { passive: true });
    gambar();
  }

  /* ---------- 3 · gerak masuk ---------- */
  function masuk() {
    if (santai() || !('IntersectionObserver' in window)) return;
    var target = document.querySelectorAll(
      '.nyata__kaki p, .kirim__baris, .langkah li, .tabel tbody tr, .angka__sel, .rasa__kutip, .tutup h2, .foto, .kepala'
    );
    if (!target.length) return;
    var lihat = new IntersectionObserver(function (masuk) {
      masuk.forEach(function (m) {
        if (!m.isIntersecting) return;
        m.target.classList.add('is-in');
        lihat.unobserve(m.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });

    Array.prototype.forEach.call(target, function (el, i) {
      el.classList.add('r');
      el.style.transitionDelay = Math.min(i % 6, 5) * 55 + 'ms';
      lihat.observe(el);
    });
  }

  /* ---------- 4 · pernyataan menyala kata demi kata ---------- */
  function nyala() {
    var blok = document.getElementById('nyata');
    if (!blok) return;
    var kata = blok.querySelectorAll('.kata');
    if (!kata.length) return;
    if (santai()) {
      Array.prototype.forEach.call(kata, function (k) { k.classList.add('is-on'); });
      return;
    }
    var nunggu = false;
    function gambar() {
      nunggu = false;
      var r = blok.getBoundingClientRect();
      var vh = window.innerHeight || 800;
      /* 0 saat blok baru masuk dari bawah, 1 saat bagian atasnya lewat 1/3 layar */
      var mulai = vh * 0.92;
      var akhir = vh * 0.24;
      var p = (mulai - r.top) / Math.max(1, (mulai - akhir) + r.height * 0.55);
      p = Math.min(1, Math.max(0, p));
      var tampil = Math.round(p * kata.length);
      for (var i = 0; i < kata.length; i++) {
        kata[i].classList.toggle('is-on', i < tampil);
      }
    }
    window.addEventListener('scroll', function () {
      if (!nunggu) { nunggu = true; requestAnimationFrame(gambar); }
    }, { passive: true });
    window.addEventListener('resize', gambar);
    gambar();
  }

  /* ---------- 5 · angka berjalan ---------- */
  function angka() {
    var sel = document.querySelectorAll('[data-hitung]');
    if (!sel.length) return;
    function isi(el, nilai) {
      el.textContent = nilai.toLocaleString('id-ID');
    }
    function jalankan(el) {
      var tujuan = parseInt(el.getAttribute('data-hitung'), 10) || 0;
      if (santai()) { isi(el, tujuan); return; }
      var awal = performance.now();
      var lama = 1100;
      function langkah(t) {
        var p = Math.min(1, (t - awal) / lama);
        var lunak = 1 - Math.pow(1 - p, 3);
        isi(el, Math.round(tujuan * lunak));
        if (p < 1) requestAnimationFrame(langkah);
      }
      requestAnimationFrame(langkah);
    }
    if (!('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(sel, function (el) {
        isi(el, parseInt(el.getAttribute('data-hitung'), 10) || 0);
      });
      return;
    }
    var lihat = new IntersectionObserver(function (masuk) {
      masuk.forEach(function (m) {
        if (!m.isIntersecting) return;
        jalankan(m.target);
        lihat.unobserve(m.target);
      });
    }, { threshold: 0.5 });
    Array.prototype.forEach.call(sel, function (el) { lihat.observe(el); });
  }

  /* ---------- 6 · catatan rasa (geser) ---------- */
  function rasa() {
    var wadah = document.getElementById('rasa');
    if (!wadah) return;
    var kartu = wadah.querySelectorAll('.rasa__satu');
    var hitung = document.getElementById('rasa-hitung');
    var mundur = document.getElementById('rasa-mundur');
    var maju = document.getElementById('rasa-maju');
    if (kartu.length < 2) return;

    var i = 0;
    function tampil(baru, arah) {
      if (baru === i) return;
      i = (baru + kartu.length) % kartu.length;
      Array.prototype.forEach.call(kartu, function (k, n) {
        if (n === i) {
          k.hidden = false;
          if (!santai()) {
            k.classList.remove('geser-kiri', 'geser-kanan');
            /* paksa reflow supaya animasi bisa diulang */
            void k.offsetWidth;
            k.classList.add(arah < 0 ? 'geser-kiri' : 'geser-kanan');
          }
        } else {
          k.hidden = true;
        }
      });
      if (hitung) {
        hitung.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(kartu.length).padStart(2, '0');
      }
    }

    if (mundur) mundur.addEventListener('click', function () { tampil(i - 1, -1); });
    if (maju) maju.addEventListener('click', function () { tampil(i + 1, 1); });

    wadah.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { tampil(i + 1, 1); }
      if (e.key === 'ArrowLeft') { tampil(i - 1, -1); }
    });

    /* geser di layar sentuh */
    var x0 = null;
    wadah.addEventListener('pointerdown', function (e) { x0 = e.clientX; });
    wadah.addEventListener('pointerup', function (e) {
      if (x0 === null) return;
      var beda = e.clientX - x0;
      x0 = null;
      if (Math.abs(beda) < 44) return;
      tampil(beda < 0 ? i + 1 : i - 1, beda < 0 ? 1 : -1);
    });
  }

  /* ---------- 7 · luncurkan ---------- */
  function mulai() {
    jam();
    bilah();
    masuk();
    nyala();
    angka();
    rasa();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mulai);
  } else {
    mulai();
  }
})();
