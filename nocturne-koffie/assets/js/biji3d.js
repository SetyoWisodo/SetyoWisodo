/* ============================================================
   Nocturne Koffie — biji kopi di beranda
   Versi 2 (5 Nov 2026): render hiper-realistis + kemiringan halus.
   Versi 1 menggambar mesh sendiri lewat WebGL; hasilnya terbaca seperti
   gumpalan cokelat mengilap, jadi diganti.

   Tugas skrip ini:
     1. menaruh enam titik senyawa di atas gambar, dari data/biji3d.json
     2. memberi kemiringan 3D halus saat digeser / panah keyboard
     3. membuka panel senyawa, menyorot butir daftar statis
     4. menghormati prefers-reduced-motion (tanpa kemiringan sama sekali)

   Tanpa JavaScript: poster tetap tampil, dan <details> 6 zona tetap terbaca.
   ============================================================ */
(function () {
  'use strict';

  var gerak = typeof window.matchMedia === 'function'
    ? window.matchMedia('(prefers-reduced-motion: reduce)')
    : { matches: false };
  function santai() { return !!gerak.matches; }

  var MAKS_DERAJAT = 7;

  function pasang(akar) {
    var panggung = akar.querySelector('[data-biji-panggung]');
    var lapis = akar.querySelector('[data-biji-lapis]');
    var panel = akar.querySelector('[data-biji-panel]');
    var poster = akar.querySelector('.biji__poster');
    var sumber = akar.getAttribute('data-biji-sumber');
    if (!panggung || !lapis || !sumber) return;

    var zona = [];
    var siap = false;

    /* ---------- 1 · baca data ---------- */
    function muat(d) {
      zona = (d.zona || []).map(function (z, i) {
        return {
          id: z.id,
          no: i + 1,
          nama: z.nama,
          ringkas: z.ringkas,
          senyawa: z.senyawa || [],
          titik: z.titik_foto || null
        };
      });
      taruhTitik();
    }

    fetch(sumber, { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { if (d) muat(d); })
      .catch(function () { /* data gagal: tombol tetap ada, panel pakai <details> */ });

    /* ---------- 2 · letak titik ---------- */
    function taruhTitik() {
      var tombol = lapis.querySelectorAll('[data-biji-titik]');
      Array.prototype.forEach.call(tombol, function (b) {
        var z = zona.filter(function (x) { return x.id === b.getAttribute('data-biji-titik'); })[0];
        if (!z || !z.titik) return;
        b.style.left = z.titik[0] + '%';
        b.style.top = z.titik[1] + '%';
      });
    }

    /* ---------- 3 · kemiringan halus ---------- */
    var sasaran = { x: 0, y: 0 };
    var kini = { x: 0, y: 0 };
    var jalan = false;
    var raf = 0;
    var lepasTimer = 0;

    function terapkan() {
      if (panggung) {
        panggung.style.transform =
          'perspective(1000px) rotateX(' + kini.x.toFixed(2) + 'deg) rotateY(' +
          kini.y.toFixed(2) + 'deg)';
      }
      if (poster) poster.style.transform = 'scale(' + (1 + Math.abs(kini.y) / 240).toFixed(4) + ')';
    }

    function loop() {
      kini.x += (sasaran.x - kini.x) * 0.12;
      kini.y += (sasaran.y - kini.y) * 0.12;
      terapkan();
      if (Math.abs(sasaran.x - kini.x) + Math.abs(sasaran.y - kini.y) < 0.04) {
        jalan = false;
        return;
      }
      raf = requestAnimationFrame(loop);
    }

    function gerakkan() {
      if (santai()) return;
      if (!jalan) {
        jalan = true;
        raf = requestAnimationFrame(loop);
      }
    }

    function pulang() {
      sasaran.x = 0;
      sasaran.y = 0;
      gerakkan();
    }

    var tarik = null;
    panggung.addEventListener('pointerdown', function (e) {
      if (santai() || e.button > 0) return;
      tarik = { x: e.clientX, y: e.clientY };
      panggung.classList.add('biji__panggung--tarik');
      if (panggung.setPointerCapture) panggung.setPointerCapture(e.pointerId);
    });

    panggung.addEventListener('pointermove', function (e) {
      if (!tarik) return;
      var dx = e.clientX - tarik.x;
      var dy = e.clientY - tarik.y;
      sasaran.y = Math.max(-MAKS_DERAJAT, Math.min(MAKS_DERAJAT, dx * 0.09));
      sasaran.x = Math.max(-MAKS_DERAJAT, Math.min(MAKS_DERAJAT, -dy * 0.09));
      gerakkan();
    });

    function lepas(e) {
      if (!tarik) return;
      tarik = null;
      panggung.classList.remove('biji__panggung--tarik');
      if (e && e.pointerId != null && panggung.hasPointerCapture && panggung.hasPointerCapture(e.pointerId)) {
        panggung.releasePointerCapture(e.pointerId);
      }
      clearTimeout(lepasTimer);
      lepasTimer = setTimeout(pulang, 900);
    }
    panggung.addEventListener('pointerup', lepas);
    panggung.addEventListener('pointercancel', lepas);
    panggung.addEventListener('pointerleave', function (e) {
      if (tarik) lepas(e);
      else pulang();
    });

    /* keyboard: panah memiringkan, Home mengembalikan */
    panggung.setAttribute('tabindex', '0');
    panggung.addEventListener('keydown', function (e) {
      var langkah = 2.5;
      if (e.key === 'ArrowLeft') { sasaran.y = Math.max(-MAKS_DERAJAT, sasaran.y - langkah); e.preventDefault(); }
      else if (e.key === 'ArrowRight') { sasaran.y = Math.min(MAKS_DERAJAT, sasaran.y + langkah); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { sasaran.x = Math.max(-MAKS_DERAJAT, sasaran.x - langkah); e.preventDefault(); }
      else if (e.key === 'ArrowDown') { sasaran.x = Math.min(MAKS_DERAJAT, sasaran.x + langkah); e.preventDefault(); }
      else if (e.key === 'Home') { sasaran.x = 0; sasaran.y = 0; e.preventDefault(); }
      else return;
      gerakkan();
    });

    document.addEventListener('visibilitychange', function () {
      if (document.hidden && jalan) {
        cancelAnimationFrame(raf);
        jalan = false;
      }
    });

    /* ---------- 4 · panel senyawa ---------- */
    function tutupPanel() {
      if (!panel) return;
      panel.hidden = true;
      akar.classList.remove('biji--buka');
      akar.removeAttribute('data-biji-aktif');
      Array.prototype.forEach.call(lapis.querySelectorAll('[data-biji-titik]'), function (b) {
        b.setAttribute('aria-pressed', 'false');
        b.classList.remove('biji__titik--aktif');
      });
    }

    function buka(id) {
      var z = zona.filter(function (x) { return x.id === id; })[0];
      if (!z || !panel) return;
      var judul = panel.querySelector('[data-biji-judul]');
      var ringkas = panel.querySelector('[data-biji-ringkas]');
      var daftar = panel.querySelector('[data-biji-senyawa]');
      if (judul) judul.textContent = String(z.no).padStart(2, '0') + ' · ' + z.nama;
      if (ringkas) ringkas.textContent = z.ringkas;
      if (daftar) {
        daftar.innerHTML = z.senyawa.map(function (s) {
          return '<li><b>' + s.nama + '</b> <span class="biji__rumus">' + s.rumus + '</span>'
            + '<span class="biji__rentang">' + s.rentang + '</span>'
            + '<span class="biji__peran">' + s.peran + '</span>'
            + '<span class="biji__sumber">'
            + (s.keyakinan === 'kuat' ? 'literatur terukur' : 'rentang umum')
            + ' · ' + s.sumber + '</span></li>';
        }).join('');
      }
      panel.hidden = false;
      akar.dataset.bijiAktif = id;
      akar.classList.add('biji--buka');
      Array.prototype.forEach.call(lapis.querySelectorAll('[data-biji-titik]'), function (b) {
        var pilih = b.getAttribute('data-biji-titik') === id;
        b.setAttribute('aria-pressed', pilih ? 'true' : 'false');
        b.classList.toggle('biji__titik--aktif', pilih);
      });
      Array.prototype.forEach.call(document.querySelectorAll('[data-biji-zona]'), function (el) {
        el.classList.toggle('biji__zona--aktif', el.getAttribute('data-biji-zona') === id);
      });
    }

    lapis.addEventListener('click', function (e) {
      var b = e.target.closest('[data-biji-titik]');
      if (b) buka(b.getAttribute('data-biji-titik'));
    });

    if (panel) {
      var tombolTutup = panel.querySelector('[data-biji-tutup]');
      if (tombolTutup) tombolTutup.addEventListener('click', tutupPanel);
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel && !panel.hidden) tutupPanel();
    });

    /* ---------- 5 · tandai siap ---------- */
    akar.dataset.bijiMode = 'render';
    akar.classList.add('biji--siap');
    siap = true;

    return {
      buka: buka,
      tutup: tutupPanel,
      taruhTitik: taruhTitik,
      setZona: function (z) { muat({ zona: z }); }
    };
  }

  function mulaiOtomatis() {
    var target = Array.prototype.slice.call(document.querySelectorAll('[data-biji3d]'));
    if (!target.length) return;
    target.forEach(pasang);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mulaiOtomatis, { once: true });
  } else {
    mulaiOtomatis();
  }

  /* diekspor supaya bisa diuji tanpa peramban (tools/verifikasi-biji.mjs) */
  window.NocturneBiji = {
    pasang: pasang,
    maksDerajat: MAKS_DERAJAT,
    santai: santai
  };
})();
