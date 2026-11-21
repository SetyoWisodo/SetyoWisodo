/* Kursor kustom — cincin, titik, label. Bukti bahwa halaman ini rekreasi penuh
 * dari rujukan "Leon Vasari", bukan versi yang mirip.
 *
 * Rak kemasan sebelumnya belum punya kursor; di rujukan kursor adalah bagian dari
 * desainnya (cincin 58 px yang membesar & mengisi warna saat di atas sampul).
 * Tidak ada efek baru: hanya memindahkan satu lapisan DOM dengan
 * 1 - e^(-16·dt), jadi biayanya satu transform per frame.
 *
 * Kode menulis ke window.RAK_KURSOR; rak.js memanggil setState() dari loop-nya.
 * Kalau berkas ini tidak dimuat, rak.js tetap jalan (dicek dengan typeof).
 */
(() => {
  'use strict';

  const el = document.getElementById('cur');
  if (!el || !window.matchMedia('(pointer:fine)').matches) return;

  let x = window.innerWidth / 2;
  let y = window.innerHeight / 2;
  let tx = x, ty = y;
  let jalan = false;

  document.addEventListener('pointermove', (e) => {
    tx = e.clientX;
    ty = e.clientY;
    if (!jalan) { jalan = true; tick(); }
  }, { passive: true });

  function tick() {
    x += (tx - x) * (1 - Math.exp(-16 * (1 / 60)));
    y += (ty - y) * (1 - Math.exp(-16 * (1 / 60)));
    el.style.transform = 'translate3d(' + x.toFixed(2) + 'px,' + y.toFixed(2) + 'px,0)';
    if (Math.abs(tx - x) > 0.2 || Math.abs(ty - y) > 0.2) requestAnimationFrame(tick);
    else jalan = false;
  }

  window.RAK_KURSOR = {
    setState(nama) {
      el.classList.toggle('is-open', nama === 'open');
      el.classList.toggle('is-spine', nama === 'spine');
      el.classList.toggle('is-btn', nama === 'btn');
    },
  };
})();
