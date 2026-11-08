/* Foto katalog & hero — mesin gerak.
 *
 * Satu permintaan: halaman ini harus membuktikan bahwa foto hasil rig
 * (`tools/katalog.py`) bisa dipakai: hero 16:9, katalog tiga sudut, dan
 * detail per lot. Semua gerak dari satu requestAnimationFrame + Web Animations
 * API; tidak ada @keyframes, tidak ada opacity fade — pemunculan teks memakai
 * mask slide, pergantian sudut memakai clip-path.
 *
 * Data dari window.KATALOG (dibangun tools/katalog.py dari data/catalog.json).
 * Tidak ada harga yang diketik di berkas ini.
 */
(() => {
  'use strict';

  const K = window.KATALOG;
  const SKU = K.SKU || K.sku || [];
  const SUDUT = K.RIG ? K.RIG.sudut : [0, -18, 40];
  const RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const EASE = 'cubic-bezier(.2,.8,.2,1)';
  const WA = 'https://wa.me/628988188800';
  const $ = (s) => document.querySelector(s);
  const rupiah = (n) => 'Rp' + n.toLocaleString('id-ID');

  const grid = $('#grid');
  const heroImg = $('#heroImg');
  const cur = $('#cur');
  const detal = $('#detal');

  /* ------------------------------------------------------------ hero --- */
  const unggulan = SKU[5] || SKU[0];      // Blue Mount Ijen — lot yang sama dengan hero rak
  if (unggulan) {
    heroImg.src = unggulan.foto.hero;
    heroImg.alt = 'Kemasan ' + unggulan.nama + ' — foto hero 16:9 dari rig studio';
    $('#heroCta').href = WA + '?text=' + encodeURIComponent(
      'Halo Nocturne, saya mau pesan ' + unggulan.nama + ' (' + unggulan.harga_teks + ').');
    const m = $('#heroMeta');
    m.innerHTML = [
      ['Lot hero', unggulan.nama],
      ['Catatan rasa', unggulan.notes.join(' · ')],
      ['Mulai', unggulan.harga_teks],
    ].map(([k, v]) => '<div><dt>' + k + '</dt><dd>' + v + '</dd></div>').join('');
  }

  /* ----------------------------------------------------- teks masuk --- */
  function naik(sel, tunda = 0) {
    document.querySelectorAll(sel).forEach((el, i) => {
      const isi = el.firstElementChild || el;
      if (RM) return;
      isi.animate(
        [{ transform: 'translateY(110%)' }, { transform: 'translateY(0)' }],
        { duration: 900, delay: tunda + i * 70, easing: EASE, fill: 'both' });
    });
  }
  naik('.hero .mask', 120);

  /* --------------------------------------------------------- katalog --- */
  const kartu = [];
  SKU.forEach((s, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'kartu';
    b.dataset.id = s.id;
    b.setAttribute('aria-label', 'Buka detail ' + s.nama);
    b.innerHTML =
      '<span class="kartu__no">' + s.no + '</span>' +
      '<span class="kartu__bingkai">' +
        '<img src="' + s.foto['0'] + '" alt="' + s.nama + ' sudut 0 derajat" width="2000" height="2000" loading="lazy" />' +
        '<img src="' + s.foto['18'] + '" alt="" aria-hidden="true" width="2000" height="2000" loading="lazy" />' +
      '</span>' +
      '<span class="kartu__kaki">' +
        '<span class="kartu__nama">' + s.nama + '</span>' +
        '<span class="kartu__harga">' + s.harga_teks + '</span>' +
      '</span>' +
      '<span class="kartu__notes">' + s.notes.join(' · ') + '</span>';
    b.addEventListener('click', () => buka(i));
    grid.appendChild(b);
    kartu.push(b);
  });

  /* ------------------------------------------------------------ detal --- */
  let aktif = -1, sudutAktif = 0, varianAktif = 0;

  function isiDetal(i, sudut) {
    const s = SKU[i];
    const sudutKunci = Math.abs(sudut);
    $('#dFot').src = s.foto[String(sudutKunci)] || s.foto['0'];
    $('#dFot').alt = 'Kemasan ' + s.nama + ' sudut ' + sudutKunci + ' derajat';
    $('#dCap').textContent = sudutKunci + '°';
    $('#dNo').textContent = s.no + ' / ' + String(SKU.length).padStart(2, '0');
    $('#dNama').textContent = s.nama;
    $('#dAsal').textContent = s.asal + ' · ' + s.proses;
    $('#dNotes').textContent = s.notes.join(' · ');

    const pilih = $('#dPilih');
    pilih.innerHTML = '';
    s.ukuran.forEach((u, j) => {
      const li = document.createElement('li');
      const bt = document.createElement('button');
      bt.type = 'button';
      bt.textContent = u.label;
      if (j === varianAktif) bt.className = 'is-on';
      bt.addEventListener('click', () => { varianAktif = j; isiDetal(i, sudut); });
      li.appendChild(bt);
      pilih.appendChild(li);
    });
    const u = s.ukuran[varianAktif] || s.ukuran[0];
    $('#dHarga').textContent = rupiah(u.harga) + ' · ' + u.label;
    $('#dCta').href = WA + '?text=' + encodeURIComponent(
      'Halo Nocturne, saya mau pesan ' + s.nama + ' ' + u.label + ' (' + rupiah(u.harga) + ').');

    const sd = $('#dSudut');
    sd.innerHTML = '';
    SUDUT.forEach((x) => {
      const k = Math.abs(x);
      const bt = document.createElement('button');
      bt.type = 'button';
      bt.textContent = k + '°';
      if (k === sudutKunci) bt.className = 'is-on';
      bt.addEventListener('click', () => { isiDetal(i, x); });
      sd.appendChild(bt);
    });
  }

  function buka(i) {
    aktif = i;
    varianAktif = 0;
    sudutAktif = 0;
    isiDetal(i, sudutAktif);
    detal.classList.add('is-buka');
    const isi = detal.querySelectorAll('.detal__teks .mask');
    isi.forEach((el, j) => {
      if (RM) return;
      el.firstElementChild.animate(
        [{ transform: 'translateY(110%)' }, { transform: 'translateY(0)' }],
        { duration: 800, delay: 60 + j * 70, easing: EASE, fill: 'both' });
    });
    $('#tutup').focus({ preventScroll: true });
  }

  function tutup() {
    if (aktif < 0) return;
    aktif = -1;
    detal.classList.remove('is-buka');
    kartu.forEach((b) => b.blur());
  }

  $('#tutup').addEventListener('click', tutup);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') tutup();
    if (e.key === 'ArrowRight' && aktif >= 0) buka((aktif + 1) % SKU.length);
    if (e.key === 'ArrowLeft' && aktif >= 0) buka((aktif - 1 + SKU.length) % SKU.length);
  });

  /* --------------------------------------------------- tombol sudut ----- */
  document.querySelectorAll('.sudut__btn').forEach((b) => {
    b.addEventListener('click', () => {
      document.querySelectorAll('.sudut__btn').forEach((x) => x.classList.remove('is-on'));
      b.classList.add('is-on');
      const s = String(b.dataset.sudut);
      kartu.forEach((k, i) => {
        const imgs = k.querySelectorAll('.kartu__bingkai img');
        imgs[0].src = SKU[i].foto[s] || SKU[i].foto['0'];
        imgs[0].alt = SKU[i].nama + ' sudut ' + s + ' derajat';
        imgs[1].src = SKU[i].foto[s === '18' ? '40' : '18'];
      });
      $('#katalogKet').textContent = '9 lot · ' + b.textContent + ' · hover untuk sudut lain';
    });
  });

  /* --------------------------------------------------------- kursor --- */
  let mx = window.innerWidth / 2, my = window.innerHeight / 2, px = mx, py = my;
  let heroY = 0, heroT = 0;
  const ease = (dt, k) => 1 - Math.exp(-k * dt);

  window.addEventListener('pointermove', (e) => {
    mx = e.clientX; my = e.clientY;
    const t = e.target;
    const diKartu = !!(t.closest && t.closest('.kartu'));
    const diTombol = !!(t.closest && t.closest('button,a'));
    cur.classList.toggle('is-kartu', diKartu);
    cur.classList.toggle('is-tombol', !diKartu && diTombol);
  }, { passive: true });

  let last = performance.now();
  function frame(now) {
    const dt = Math.min(48, now - last) / 1000;
    last = now;
    px += (mx - px) * ease(dt, 16);
    py += (my - py) * ease(dt, 16);
    cur.style.transform = 'translate3d(' + px.toFixed(1) + 'px,' + py.toFixed(1) + 'px,0)';

    /* parallax hero: gambar bergeser sedikit saat halaman digulir */
    const y = window.scrollY || 0;
    heroT = Math.max(-1, Math.min(1, (y - 120) / 900));
    heroY += (heroT - heroY) * ease(dt, 6);
    if (heroImg) {
      heroImg.style.transform = 'translate3d(0,' + (heroY * -18).toFixed(2) + 'px,0) scale(' +
        (1 + Math.abs(heroY) * 0.012).toFixed(4) + ')';
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  /* ------------------------------------------------------ muat awal --- */
  // sudut 40° hanya diunduh saat benar-benar dibutuhkan (kartu detail / tombol)
  window.KATALOG_STATUS = { sku: SKU.length, sudut: SUDUT, kartu: kartu.length };
})();
