/* ============================================================
   Nocturne Koffie — katalog3d.js
   Foto produk 3D: ganti gambar kartu + pemutar 360°.

   Data berasal dari data/katalog3d.js (dibangun tools/katalog3d.py).
   Semua gambar adalah render sendiri: latar transparan, 640 px tinggi untuk
   kartu, 440 px untuk 16 langkah putar.

   Aturan yang dipegang:
   · Tanpa perpustakaan. Hanya Gambar + rAF + pointer events.
   · Gambar pertama dimuat dengan prioritas normal; 15 langkah putar sisanya
     baru diunduh saat pengunjung benar-benar menyentuh kartu itu.
   · prefers-reduced-motion: hover tidak memutar apa pun, hanya berganti ke
     sudut 28°. Pemutar manual (seret) tetap boleh — itu kendali pengunjung.
   ============================================================ */
(function () {
  'use strict';

  const K3 = window.KATALOG3D;
  if (!K3 || !Array.isArray(K3.sku)) return;

  const peta = {};
  K3.sku.forEach((s) => { peta[s.id] = s; });

  const kurangiGerak = window.matchMedia('(prefers-reduced-motion: reduce)');
  const LANGKAH = K3.langkah || 16;

  /* Muat semua langkah sebuah lot (sekali saja). Dipakai saat hover pertama
     dan saat pembaca menyentuh pemutar. */
  function muatPutar(sku) {
    if (sku._janji) return sku._janji;
    sku._janji = Promise.all(sku.putar.map((src) => new Promise((selesai) => {
      const im = new Image();
      im.decoding = 'async';
      im.onload = im.onerror = () => selesai();
      im.src = src;
    })));
    return sku._janji;
  }

  /* ---------------------------------------------------------- kartu --- */
  function pasangKartu() {
    document.querySelectorAll('.card__media img').forEach((img) => {
      const kartu = img.closest('.card');
      if (!kartu) return;
      const id = (kartu.id || '').replace('kartu-', '');
      const sku = peta[id];
      if (!sku) return;                       // paket & kartu member tetap foto lama

      img.src = sku.kartu['0'];
      img.removeAttribute('width');
      img.removeAttribute('height');
      img.classList.add('k3-img');

      const media = img.parentElement;
      media.classList.add('k3');

      /* Sudut 3/4 saat hover: satu berkas, bukan animasi. Di layar sentuh
         tidak ada hover, jadi tidak ada yang berubah. */
      const sudutHover = sku.kartu['28'] ? '28' : Object.keys(sku.kartu)[0];
      let asal = null;
      media.addEventListener('pointerenter', (ev) => {
        if (ev.pointerType !== 'mouse') return;
        if (kurangiGerak.matches) {
          if (sudutHover && img.src.indexOf(sku.kartu[sudutHover]) === -1) img.src = sku.kartu[sudutHover];
          return;
        }
        muatPutar(sku).then(() => putarHover(sku, img));
      });
      media.addEventListener('pointerleave', () => {
        if (asal) { cancelAnimationFrame(asal); asal = null; }
        img.src = sku.kartu['0'];
      });

      /* Klik gambar = buka pemutar. Klik di area lain kartu (tombol, varian,
         WhatsApp) tidak diganggu. */
      img.style.cursor = 'grab';
      img.addEventListener('click', () => bukaPutar(sku));
    });
  }

  /* Hover: 8 langkah pelan bolak-balik (0° → 90°), 2,4 detik per putaran.
     Sengaja lebih lambat daripada pemutar manual: ini hiasan, bukan alat. */
  function putarHover(sku, img) {
    const mulai = performance.now();
    const durasi = 2600;
    // langkah 0,1,2,3,4 lalu balik 3,2,1 — 0° → 90° → 0°, tanpa lompatan
    const deret = [0, 1, 2, 3, 4, 3, 2, 1].map((i) => sku.putar[i]).filter(Boolean);
    if (kurangiGerak.matches || deret.length < 2) {
      img.src = sku.kartu['28'] || img.src;
      return;
    }
    const langkah = (t) => {
      const f = ((t - mulai) % durasi) / durasi;
      const i = Math.floor(f * deret.length);
      const src = deret[i];
      if (img.dataset.k3 !== src) { img.src = src; img.dataset.k3 = src; }
      asal = requestAnimationFrame(langkah);
    };
    asal = requestAnimationFrame(langkah);
  }

  /* --------------------------------------------------- pemutar 360° --- */
  function bukaPutar(sku) {
    let dlg = document.getElementById('k3-putar');
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.id = 'k3-putar';
      dlg.className = 'k3d';
      dlg.innerHTML =
        '<div class="k3d__kepala">' +
          '<p class="k3d__nama" id="k3d-nama"></p>' +
          '<button class="k3d__tutup" type="button" aria-label="Tutup pemutar">✕</button>' +
        '</div>' +
        '<div class="k3d__panggung" id="k3d-panggung">' +
          '<img id="k3d-img" alt="" draggable="false">' +
        '</div>' +
        '<p class="k3d__petunjuk">Seret ke kiri/kanan untuk memutar · <kbd>←</kbd> <kbd>→</kbd> · Esc menutup</p>';
      document.body.appendChild(dlg);

      dlg.querySelector('.k3d__tutup').addEventListener('click', () => dlg.close());
      dlg.addEventListener('click', (ev) => { if (ev.target === dlg) dlg.close(); });
    }

    const img = dlg.querySelector('#k3d-img');
    dlg.querySelector('#k3d-nama').textContent = sku.no + ' · ' + sku.nama;
    img.src = sku.kartu['0'];
    img.alt = 'Kemasan ' + sku.nama + ' — putaran 360 derajat';

    let i = 0;
    const tampil = () => { img.src = sku.putar[i]; };
    muatPutar(sku).then(() => {
      /* Sinkronkan dengan gambar yang sedang tampil (0° = langkah 0). */
      tampil();
    });

    let seret = null;
    const panggung = dlg.querySelector('#k3d-panggung');
    panggung.addEventListener('pointerdown', (ev) => {
      seret = { x: ev.clientX, i };
      panggung.setPointerCapture(ev.pointerId);
      panggung.classList.add('is-seret');
    });
    panggung.addEventListener('pointermove', (ev) => {
      if (!seret) return;
      const lebar = panggung.clientWidth || 1;
      const langkah = Math.round((ev.clientX - seret.x) / lebar * LANGKAH * 0.9);
      const baru = ((seret.i + langkah) % LANGKAH + LANGKAH) % LANGKAH;
      if (baru !== i) { i = baru; tampil(); }
    });
    const lepas = (ev) => {
      if (!seret) return;
      seret = null;
      panggung.classList.remove('is-seret');
      if (ev && ev.pointerId !== undefined && panggung.hasPointerCapture(ev.pointerId)) {
        panggung.releasePointerCapture(ev.pointerId);
      }
    };
    panggung.addEventListener('pointerup', lepas);
    panggung.addEventListener('pointercancel', lepas);

    dlg.onkeydown = (ev) => {
      if (ev.key === 'ArrowRight') { i = (i + 1) % LANGKAH; tampil(); ev.preventDefault(); }
      if (ev.key === 'ArrowLeft') { i = (i - 1 + LANGKAH) % LANGKAH; tampil(); ev.preventDefault(); }
    };

    if (typeof dlg.showModal === 'function') dlg.showModal();
    else dlg.setAttribute('open', '');
  }

  /* Kartu dibuat site.js SETELAH catalog.json selesai diambil, jadi urutan
     skrip saja tidak cukup. MutationObserver memastikan setiap kartu baru
     ikut mendapat render 3D — termasuk saat penyaring menyembunyikan dan
     menampilkan ulang kartu. */
  function mulai() {
    pasangKartu();
    const grid = document.getElementById('grid');
    if (!grid || typeof MutationObserver !== 'function') return;
    let jeda = null;
    const obs = new MutationObserver(() => {
      if (jeda) return;
      jeda = window.setTimeout(() => { jeda = null; pasangKartu(); }, 60);
    });
    obs.observe(grid, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mulai);
  } else {
    mulai();
  }
})();
