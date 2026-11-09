/* Rak Sangrai — mesin gerak.
 *
 * Kenapa ditulis begini: seluruh halaman digerakkan satu requestAnimationFrame
 * (posisi, kemiringan, kursor) dan Web Animations API (tirai kertas, baris teks,
 * pergantian judul). Tidak ada @keyframes, tidak ada opacity fade — setiap
 * pemunculan adalah mask slide, klip, atau skala. Alasannya bukan gaya-gayaan:
 * animasi yang dihitung per frame bisa diperiksa nilainya (s, T, r, o) dan
 * dihentikan dengan satu flag, sedangkan CSS keyframes tidak bisa.
 *
 * Semua data (harga, nama, potongan gambar) berasal dari window.RAK yang
 * dibangun tools/rak.py dari data/catalog.json. Jangan menulis angka di sini.
 */
(() => {
  'use strict';

  const R = window.RAK;
  const ITEMS = R.ITEMS;
  const N = ITEMS.length;
  const COPIES = 3;
  const TOTAL = N * COPIES;
  const HALF = TOTAL / 2;
  const RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const EASE = 'cubic-bezier(.2,.8,.2,1)';
  const SPEET = 'cubic-bezier(.76,0,.18,1)';

  const $ = (s) => document.querySelector(s);
  const stage = $('#stage'), shelf = $('#shelf'), ring = $('#ring'), detail = $('#detail');
  const capTitle = $('.cap__title'), capSub = $('.cap__sub'), capMeta = $('.cap__meta');
  const tabsEl = $('.tabs'), tabsInd = $('#tabsInd');
  const cur = $('#cur');

  // ------------------------------------------------------------- geometri ---
  const probe = document.createElement('div');
  probe.style.cssText = 'position:absolute;left:-9999px;top:0;width:0;height:var(--H)';
  document.body.appendChild(probe);

  // Rasio muka datang dari data (`FACE`): untuk kemasan kopi 500 g, muka stiker
  // ≈ 0,519 × tinggi dan sisi gusset ≈ 0,173 × tinggi. Angka kaset lama
  // (142/840 dan 474/900) hanya dipakai kalau data belum menyebutnya — jadi
  // mengganti bentuk objek tidak perlu menyunting mesin animasinya.
  const FACE = R.FACE || { cv: 474 / 900, sp: 142 / 840 };

  let H = 0, ws = 0, d = 0, gap = 0;
  function ukur() {
    H = probe.offsetHeight || 320;
    ws = H * FACE.sp;
    d = H * FACE.cv;
    gap = H * 0.03;
    stage.style.setProperty('--ws', ws + 'px');
    stage.style.setProperty('--d', d + 'px');
    document.documentElement.style.setProperty('--ws', ws + 'px');
    document.documentElement.style.setProperty('--d', d + 'px');
  }
  ukur();

  // ------------------------------------------------------------------ peta ---
  // r = +18 … −18 mengelilingi lingkaran 36 kotak, supaya pembungkusan selalu
  // terjadi jauh di luar layar.
  const rel = (v) => (((v - s + HALF) % TOTAL) + TOTAL) % TOTAL - HALF;
  const step = (r) => (Math.abs(r) < 1 ? (r + Math.sin(Math.PI * r) / Math.PI) / 2 : Math.sign(r) * 0.5);
  const F = (r) => r * (ws + gap) + (d - ws + 1.6 * gap) * step(r);
  const lerp = (a, b, t) => a + (b - a) * t;
  const ease = (dt, k) => 1 - Math.exp(-k * dt);

  // ----------------------------------------------------------------- kotak ---
  function potong(el, kunci) {
    const c = R.CROP[kunci];
    const sheet = R.SHEET[c[0]];
    const [url, W, Hs] = sheet;
    const [, x, y, w, h] = c;
    el.style.backgroundImage = 'url("' + url + '")';
    el.style.backgroundSize = (W / w * 100) + '% ' + (Hs / h * 100) + '%';
    el.style.backgroundPosition = (x / (W - w) * 100) + '% ' + (y / (Hs - h) * 100) + '%';
  }

  const tapes = [];
  for (let c = 0; c < COPIES; c++) {
    for (let i = 0; i < N; i++) {
      const v = c * N + i;
      const id = ITEMS[i].id;
      const el = document.createElement('div');
      el.className = 'tape';
      el.dataset.i = i;
      const sp = document.createElement('div'); sp.className = 'face sp';
      const cv = document.createElement('div'); cv.className = 'face cv';
      potong(sp, 'spine-' + id);
      potong(cv, 'cover-' + id);
      el.append(sp, cv);
      el.addEventListener('pointerenter', () => { hover = v; });
      el.addEventListener('pointerleave', () => { if (hover === v) hover = -1; });
      el.addEventListener('click', () => {
        if (dragged) return;
        const r = rel(v);
        if (Math.abs(r) < 0.5) openDetail();
        else T = Math.round(T + r);
      });
      stage.appendChild(el);
      tapes.push({ v, i, el, sp, cv, lift: 0 });
    }
  }

  // ----------------------------------------------------------------- state ---
  let s = R.START + N;
  let T = s;
  let hover = -1;
  let active = -1;
  let mx = window.innerWidth / 2, my = window.innerHeight / 2;
  let px = mx, py = my;
  let tiltX = 0, tiltY = 0, tX = 0, tY = 0;
  let onCover = false;
  let isOpen = false;
  let dragging = false, dragged = false, drag0 = null;
  let wheelT = 0;
  let last = performance.now();

  // --------------------------------------------------------------- kompas ---
  function tapeAktif() {
    let best = null, bd = 9;
    for (const t of tapes) {
      const r = Math.abs(rel(t.v));
      if (r < bd) { bd = r; best = t; }
    }
    return best;
  }

  // -------------------------------------------------------------- caption ---
  function ganti(mask, teks, dir) {
    const baru = document.createElement('span');
    baru.className = 'line';
    baru.textContent = teks;
    for (const lama of mask.querySelectorAll('.line')) {
      if (lama.dataset.leaving) continue;
      lama.dataset.leaving = '1';
      const dari = getComputedStyle(lama).transform;
      const a = lama.animate(
        [{ transform: dari === 'none' ? 'translateY(0)' : dari },
         { transform: 'translateY(' + (-dir * 105) + '%)' }],
        { duration: RM ? 1 : 650, easing: EASE, fill: 'both' });
      a.onfinish = () => lama.remove();
    }
    mask.appendChild(baru);
    baru.animate([{ transform: 'translateY(' + (dir * 105) + '%)' }, { transform: 'translateY(0)' }],
      { duration: RM ? 1 : 650, easing: EASE, fill: 'both' });
  }

  function setActive(i, dir) {
    active = i;
    const it = ITEMS[i];
    ganti(capTitle, it.name, dir);
    ganti(capSub, it.line, dir);
    ganti(capMeta, it.meta, dir);
    tabAktif(it.tab);
  }

  // ----------------------------------------------------------------- tab ---
  const tabBtns = [];
  for (const t of R.TABS) {
    const b = document.createElement('button');
    b.className = 'tab';
    b.dataset.tab = t.id;
    b.innerHTML = '<span>' + t.label + '</span><span aria-hidden="true">·</span><span>' + t.sub + '</span>';
    b.addEventListener('click', () => {
      const first = t.id === 'semua' ? 0 : ITEMS.findIndex((x) => x.tab === t.id);
      if (first < 0) return;
      let best = T, bd = Infinity;
      for (let k = -2; k <= 2; k++) {
        const cand = first + k * N;
        if (Math.abs(cand - T) < bd) { bd = Math.abs(cand - T); best = cand; }
      }
      T = best;
    });
    tabsEl.appendChild(b);
    tabBtns.push(b);
  }

  function tabAktif(id) {
    const b = tabBtns.find((x) => x.dataset.tab === id);
    if (!b) return;
    for (const x of tabBtns) x.classList.toggle('is-on', x === b);
    tabsInd.style.width = b.offsetWidth + 'px';
    tabsInd.style.transform = 'translateX(' + b.offsetLeft + 'px)';
  }

  // ----------------------------------------------------------------- loop ---
  function frame(now) {
    const dts = Math.min(50, now - last) / 1000;
    last = now;
    const W = window.innerWidth, cy = window.innerHeight / 2;

    // --- pegas posisi
    const k = RM ? 60 : (dragging ? 18 : 5.2);
    s += (T - s) * ease(dts, k);
    if (Math.abs(T - s) < 1e-4) s = T;
    if (Math.abs(s) > TOTAL * 4) {
      const geser = Math.round(s / TOTAL) * TOTAL;
      s -= geser; T -= geser;
    }

    // --- judul aktif
    const ai = ((Math.round(s) % N) + N) % N;
    if (ai !== active) setActive(ai, Math.sign(T - s) || 1);

    // --- kemiringan: menuju kursor bila kursor di atas sampul
    const dekat = Math.abs(T - s) < 0.3 && !isOpen
      && Math.abs(mx - W / 2) < 0.55 * d
      && Math.abs(my - cy) < 0.55 * H;
    onCover = dekat;
    if (dekat) {
      tY = (mx - W / 2) / (0.55 * d) * 9;
      tX = -((my - cy) / (H / 2)) * 6;
    } else {
      tY = (mx - W / 2) / W * 5;
      tX = 0;
    }
    tiltY = lerp(tiltY, tY, ease(dts, RM ? 40 : 7));
    tiltX = lerp(tiltX, tX, ease(dts, RM ? 40 : 7));

    // --- kotak
    for (const t of tapes) {
      const r = rel(t.v);
      const a = Math.max(0, 1 - Math.abs(r));
      const o = a * a * (3 - 2 * a);
      const tujuan = (hover === t.v && Math.abs(r) > 0.5 && !isOpen) ? 1 : 0;
      t.lift = lerp(t.lift, tujuan, ease(dts, RM ? 40 : 12));

      const x = F(r);
      if (Math.abs(x) > W / 2 + 1.5 * d) { t.el.style.visibility = 'hidden'; continue; }
      t.el.style.visibility = 'visible';

      const y = -o * 0.025 * H - t.lift * 0.045 * H;
      const z = o * 0.2 * H;
      t.el.style.transform =
        'translate3d(' + x.toFixed(2) + 'px,' + y.toFixed(2) + 'px,' + z.toFixed(2) + 'px)' +
        ' rotateZ(' + (-4.5 * o).toFixed(3) + 'deg)' +
        ' rotateX(' + (tiltX * o).toFixed(3) + 'deg)' +
        ' rotateY(' + (-90 * o + tiltY * o).toFixed(3) + 'deg)';
      t.el.style.zIndex = String(Math.round(100 - Math.abs(r) * 4));
      t.sp.style.setProperty('--shade', (o * 0.55).toFixed(3));
      t.cv.style.setProperty('--shade', ((1 - o) * 0.5).toFixed(3));
    }

    // --- tombol putar: muncul saat rak hampir diam
    const rs = isOpen ? 0 : (() => { const q = Math.max(0, 1 - Math.abs(T - s) * 3); return q * q * (3 - 2 * q); })();
    ring.style.left = (W / 2 - d / 2 - 6) + 'px';
    ring.style.top = (cy + 0.36 * H) + 'px';
    ring.style.transform = 'scale(' + rs.toFixed(3) + ')';
    ring.style.pointerEvents = rs > 0.5 ? 'auto' : 'none';
    ring.tabIndex = rs > 0.5 ? 0 : -1;

    // --- kursor
    px = lerp(px, mx, ease(dts, 16));
    py = lerp(py, my, ease(dts, 16));
    cur.style.transform = 'translate3d(' + px.toFixed(2) + 'px,' + py.toFixed(2) + 'px,0)';

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  // --------------------------------------------------------------- pointer ---
  function kursor(ev) {
    const diAtasKotak = ev.target.closest && ev.target.closest('.tape');
    const diAtasTombol = ev.target.closest && ev.target.closest('button,a');
    cur.classList.toggle('is-open', onCover && !isOpen && !!diAtasKotak);
    cur.classList.toggle('is-spine', !onCover && !isOpen && !!diAtasKotak);
    cur.classList.toggle('is-btn', isOpen ? !!(diAtasTombol && !diAtasKotak) : !!diAtasTombol);
  }

  window.addEventListener('pointermove', (ev) => {
    mx = ev.clientX; my = ev.clientY;
    kursor(ev);
  }, { passive: true });

  window.addEventListener('pointerdown', (ev) => { mx = ev.clientX; my = ev.clientY; }, { passive: true });

  // geser rak
  shelf.addEventListener('pointerdown', (ev) => {
    if (isOpen) return;
    drag0 = { x: ev.clientX, T };
    dragging = false;
    shelf.setPointerCapture(ev.pointerId);
  });
  shelf.addEventListener('pointermove', (ev) => {
    if (!drag0) return;
    const dx = ev.clientX - drag0.x;
    if (!dragging && Math.abs(dx) > 5) { dragging = true; dragged = true; }
    if (dragging) T = drag0.T - dx / (ws + gap);
  });
  const lepas = () => {
    if (dragging) T = Math.round(T);
    drag0 = null; dragging = false;
    setTimeout(() => { dragged = false; }, 60);
  };
  shelf.addEventListener('pointerup', lepas);
  shelf.addEventListener('pointercancel', lepas);

  // roda: sumbu mana pun yang lebih besar
  window.addEventListener('wheel', (ev) => {
    if (isOpen) return;
    const delta = Math.abs(ev.deltaY) > Math.abs(ev.deltaX) ? ev.deltaY : ev.deltaX;
    T += delta / (ws + gap) * 0.5;
    clearTimeout(wheelT);
    wheelT = setTimeout(() => { T = Math.round(T); }, 160);
  }, { passive: true });

  // papan tombol
  window.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape' && isOpen) { closeDetail(); return; }
    if (isOpen) return;
    if (ev.key === 'ArrowRight') { T = Math.round(T) + 1; ev.preventDefault(); }
    if (ev.key === 'ArrowLeft') { T = Math.round(T) - 1; ev.preventDefault(); }
    if (ev.key === 'Enter' && !document.activeElement.closest('button,a')) { openDetail(); ev.preventDefault(); }
  });

  $('#prev').addEventListener('click', () => { T = Math.round(T) - 1; });
  $('#next').addEventListener('click', () => { T = Math.round(T) + 1; });
  ring.addEventListener('click', () => { if (!isOpen) openDetail(); });

  // ----------------------------------------------------------------- detail ---
  const pimg = $('#pimg');
  const blobs = Array.from(document.querySelectorAll('#blobs circle'));
  const DELAY = [0, 120, 220, 300, 360, 420, 180];
  let inkRaf = 0;

  function poster(id) {
    const c = R.CROP['cover-' + id];
    const [url, W, Hs] = R.SHEET[c[0]];
    const [, x, y, w, h] = c;
    pimg.setAttribute('href', url);
    pimg.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', url);
    pimg.setAttribute('x', String(-x * 474 / w));
    pimg.setAttribute('y', String(-y * 900 / h));
    pimg.setAttribute('width', String(W * 474 / w));
    pimg.setAttribute('height', String(Hs * 900 / h));
  }

  function tinta() {
    cancelAnimationFrame(inkRaf);
    if (RM) { blobs.forEach((b) => b.setAttribute('r', '720')); return; }
    blobs.forEach((b) => b.setAttribute('r', '0'));
    const t0 = performance.now();
    const langkah = (now) => {
      const el = now - t0;
      blobs.forEach((b, i) => {
        const p = Math.max(0, Math.min(1, (el - 520 - DELAY[i]) / 1250));
        b.setAttribute('r', ((1 - Math.pow(1 - p, 3)) * 720).toFixed(1));
      });
      if (el < 520 + 420 + 1250) inkRaf = requestAnimationFrame(langkah);
    };
    inkRaf = requestAnimationFrame(langkah);
  }

  function isi(it) {
    $('#dSub').textContent = it.line;
    $('#dTitle').textContent = it.name;
    $('#dMeta').textContent = it.meta;
    $('#dSyn').textContent = it.synopsis;
    $('#dHarga').textContent = it.harga_teks + ' · ' + it.ukuran_teks;
    $('#dCredit').textContent = 'Disangrai Ais Coffee Roastery, Banyuwangi. Dikemas dan dikirim dari kota yang sama.';
    const jenis = it.kind === 'Paket' ? 'paket' : (it.kind === 'Member' ? 'member' : 'lot');
    const cta = $('#dCta');
    cta.textContent = 'Pesan ' + jenis + ' / WhatsApp';
    cta.href = 'https://wa.me/628988188800?text=' + encodeURIComponent(
      'Halo Nocturne, saya mau pesan ' + it.name + ' (' + it.harga_teks + ').');
  }

  function bukaLembar() {
    const W = window.innerWidth, Hh = window.innerHeight;
    T = Math.round(T); s = T;
    const i = ((Math.round(s) % N) + N) % N;
    const it = ITEMS[i];
    isi(it);
    poster(it.id);
    isOpen = true;
    cur.classList.remove('is-open', 'is-spine');

    const t = tapeAktif();
    const rect = t.cv.getBoundingClientRect();
    detail.style.visibility = 'visible';
    detail.style.transformOrigin = (rect.left + rect.width / 2) + 'px ' + (rect.top + rect.height / 2) + 'px';

    const dari = 'inset(' + rect.top + 'px ' + Math.max(0, W - rect.right) + 'px '
      + Math.max(0, Hh - rect.bottom) + 'px ' + Math.max(0, rect.left) + 'px round 3px)';
    const ke = 'inset(0px 0px 0px 0px round 0px)';
    detail.animate(
      [{ clipPath: dari, transform: 'rotate(-4.5deg)' }, { clipPath: ke, transform: 'rotate(0deg)' }],
      { duration: RM ? 1 : 1050, easing: SPEET, fill: 'both' });

    const baris = Array.from(detail.querySelectorAll('.detail__left .mask > *'));
    baris.forEach((el, idx) => {
      el.animate([{ transform: 'translateY(110%)' }, { transform: 'translateY(0)' }],
        { duration: RM ? 1 : 900, delay: RM ? 0 : 620 + idx * 75, easing: EASE, fill: 'both' });
    });

    tinta();
    $('#close').focus({ preventScroll: true });
  }

  function closeDetail() {
    if (!isOpen) return;
    isOpen = false;
    const W = window.innerWidth, Hh = window.innerHeight;
    const t = tapeAktif();
    const rect = t.cv.getBoundingClientRect();
    const ke = 'inset(' + rect.top + 'px ' + Math.max(0, W - rect.right) + 'px '
      + Math.max(0, Hh - rect.bottom) + 'px ' + Math.max(0, rect.left) + 'px round 3px)';
    const a = detail.animate(
      [{ clipPath: 'inset(0px 0px 0px 0px round 0px)', transform: 'rotate(0deg)' },
       { clipPath: ke, transform: 'rotate(-4.5deg)' }],
      { duration: RM ? 1 : 850, easing: SPEET, fill: 'both' });
    a.onfinish = () => {
      cancelAnimationFrame(inkRaf);
      detail.style.visibility = 'hidden';
      detail.getAnimations().forEach((x) => x.cancel());
      a.cancel();
    };
  }

  function openDetail() {
    if (isOpen) return;
    bukaLembar();
  }

  $('#close').addEventListener('click', closeDetail);
  detail.addEventListener('click', (ev) => { if (ev.target === detail) closeDetail(); });

  // --------------------------------------------------------------- muat awal ---
  Object.values(R.SHEET).forEach(([url]) => { const im = new Image(); im.src = url; });

  window.addEventListener('resize', () => { ukur(); });

  // judul pertama langsung terpasang tanpa slide
  const i0 = ((Math.round(s) % N) + N) % N;
  active = i0;
  const it0 = ITEMS[i0];
  capTitle.querySelector('.line').textContent = it0.name;
  capSub.querySelector('.line').textContent = it0.line;
  capMeta.querySelector('.line').textContent = it0.meta;
  tabAktif(it0.tab);
})();
