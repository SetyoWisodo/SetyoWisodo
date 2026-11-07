/* Cutaway Nocturne — potong-buka kemasan.
   Aturan inti dari skill Cutaway yang dipegang berkas ini:
   · render(t) MURNI — tidak ada Math.random, tidak ada Date, tidak ada state
     yang dibawa antar frame. Semua yang tampak diturunkan dari t saja.
   · satu kamera per ketukan (data.js → KAMERA), 9 ketukan, 9 sudut berbeda.
   · setiap ketukan 2–3 s; bagian terbuka 1 s, tahan, menutup 0,55 s.
   · frame 0 = gambar sampul: objek besar, 3/4 depan, sudah bergerak.
   · frame 0 s harus sama persis dengan frame 25 s (loop tanpa lompat).
   Tanpa WebGL, tanpa pustaka: tiga transform CSS per bidang. */

(function () {
  "use strict";

  var D = window.CUTAWAY;
  var KETUKAN = D.KETUKAN, KAMERA = D.KAMERA, BAGIAN = D.BAGIAN, DURASI = D.DURASI;
  var U = 3.2;                      /* piksel per satuan; diperbarui satuan() */

  var adegan = document.getElementById("adegan");
  var kameraEl = document.getElementById("kamera");
  var kartuNo = document.getElementById("kartuNo");
  var kartuPeran = document.getElementById("kartuPeran");
  var kartuJudul = document.getElementById("kartuJudul");
  var kartuSpek = document.getElementById("kartuSpek");
  var kartuCatatan = document.getElementById("kartuCatatan");
  var ukuranEl = document.getElementById("ukuran");
  var daftarEl = document.getElementById("daftar");
  var relEl = document.getElementById("rel");
  var relIsi = document.getElementById("relIsi");
  var relTitik = document.getElementById("relTitik");
  var waktuEl = document.getElementById("waktu");
  var mainkanEl = document.getElementById("mainkan");

  var OBJEK = document.createElement("div");
  OBJEK.className = "objek";
  kameraEl.appendChild(OBJEK);

  /* --------------------------------------------------------------- bagian --- */
  var simpul = {};              /* id → [elemen, …] (dua elemen untuk lipatan) */
  BAGIAN.forEach(function (b, i) {
    simpul[b.id] = [];
    var jumlah = b.kembar ? 2 : 1;
    for (var sisi = 0; sisi < jumlah; sisi++) {
      var el = document.createElement("div");
      el.className = "bagian";
      el.dataset.id = b.id;
      if (jumlah === 2) el.dataset.cermin = sisi ? "1" : "0";
      el.style.setProperty("--w", b.w);
      el.style.setProperty("--h", b.h);

      var muka = document.createElement("div");
      muka.className = "muka";
      var no = document.createElement("span");
      no.className = "muka__no";
      no.textContent = ("0" + (i + 1)).slice(-2);
      muka.appendChild(no);

      if (b.id === "biji") {
        /* tujuh biji, tiga di antaranya terlihat dari celah (ceklis 7) */
        for (var k = 0; k < 7; k++) {
          var biji = document.createElement("i");
          biji.className = "sebutir";
          biji.style.left = (26 + (k % 3) * 23) + "%";
          biji.style.top = (16 + Math.floor(k / 3) * 33) + "%";
          biji.style.transform = "rotate(" + ((k * 37) % 60 - 30) + "deg)";
          muka.appendChild(biji);
        }
      }
      if (b.id === "stiker") {
        var lot = document.createElement("span");
        lot.className = "muka__no";
        lot.textContent = "LOT 041 · 03.11.26";
        muka.appendChild(lot);
      }
      el.appendChild(muka);
      OBJEK.appendChild(el);
      simpul[b.id].push(el);
    }
  });

  /* ------------------------------------------------------------------ math --- */
  function klem(x, a, b) { return x < a ? a : x > b ? b : x; }
  function halus(x) { x = klem(x, 0, 1); return x * x * x * (x * (x * 6 - 15) + 10); }
  function lerp(a, b, p) { return a + (b - a) * p; }

  function ketukanPada(t) {
    for (var i = KETUKAN.length - 1; i >= 0; i--) if (t >= KETUKAN[i].mulai) return i;
    return 0;
  }

  /* kamera per t: interpolasi 0,9 s di awal ketukan, plus goyang halus.
     Nilai kembalian murni dari t — tidak menyimpan apa pun. */
  function kamera(t) {
    var i = ketukanPada(t);
    var k = KAMERA[KETUKAN[i].id];
    var s = KAMERA[KETUKAN[Math.max(0, i - 1)].id];
    var p = i === 0 ? 1 : halus((t - KETUKAN[i].mulai) / 0.9);
    var goyang = Math.sin(t * 0.44) * 1.5;
    var angkat = Math.sin(t * 0.31 + 1.1) * 0.9;
    return {
      i: i,
      ry: lerp(s.ry, k.ry, p) + goyang,
      rx: lerp(s.rx, k.rx, p) + angkat,
      zoom: lerp(s.zoom, k.zoom, p) + Math.sin(t * 0.6) * 0.004,
      ty: lerp(s.ty, k.ty, p)
    };
  }

  /* satu bagian: pelat bukaan 0..1 dari t saja.
     Bisa terbuka di lebih dari satu ketukan (panel depan disingkirkan saat
     isi sangrai ditampilkan), jadi ambil nilai terbesar. */
  function bukaan(t, id) {
    var hasil = 0;
    for (var i = 0; i < KETUKAN.length; i++) {
      var k = KETUKAN[i];
      var ikut = k.bagian === id || (k.bukaLagi && k.bukaLagi.indexOf(id) >= 0);
      if (!ikut) continue;
      var a = k.mulai + 0.12, b = a + 1.0, c = k.selesai - 0.55, d = k.selesai;
      var p = 0;
      if (t > a && t < d) {
        if (t < b) p = halus((t - a) / 1.0);
        else if (t < c) p = 1;
        else p = 1 - halus((t - c) / 0.55);
      }
      if (p > hasil) hasil = p;
    }
    return hasil;
  }

  function panjang(v) { return Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) || 1; }

  function bagianTransform(b, p, cermin) {
    var m = cermin ? -1 : 1;
    var n = panjang(b.arah);
    var x = (b.pos[0] + (b.arah[0] / n) * b.jarak * p) * m;
    var y = b.pos[1] + (b.arah[1] / n) * b.jarak * p;
    var z = b.pos[2] + (b.arah[2] / n) * b.jarak * p;
    var ry = (b.muka_ry + b.putar * p) * m;
    var rx = b.muka_rx * (1 - 0.6 * p);
    var rz = 0;
    return "translate3d(" + (x * U).toFixed(2) + "px," + (y * U).toFixed(2) + "px," + (z * U).toFixed(2) + "px) "
      + "rotateY(" + ry.toFixed(2) + "deg) rotateX(" + rx.toFixed(2) + "deg) rotateZ(" + rz.toFixed(2) + "deg)";
  }

  /* ---------------------------------------------------------------- render --- */
  function render(t) {
    t = ((t % DURASI) + DURASI) % DURASI;
    var k = kamera(t);
    kameraEl.style.transform =
      "translate3d(0," + (k.ty * 0.1 * U).toFixed(2) + "px,0) "
      + "rotateX(" + (-k.rx).toFixed(3) + "deg) rotateY(" + k.ry.toFixed(3) + "deg) "
      + "scale(" + k.zoom.toFixed(4) + ")";
    var terbuka = null, terbanyak = 0;
    var peta = {};
    BAGIAN.forEach(function (b) {
      var p = bukaan(t, b.id);
      peta[b.id] = p;
      simpul[b.id].forEach(function (el, i) {
        el.style.transform = bagianTransform(b, p, i === 1);
        el.dataset.terbuka = p > 0.5 ? "1" : "0";
      });
      if (p > terbanyak) { terbanyak = p; terbuka = b.id; }
    });
    return {
      t: t, i: k.i, ketukan: KETUKAN[k.i].id, kamera: k,
      terbuka: terbuka, terbanyak: terbanyak, bukaan: peta
    };
  }

  window.CUTAWAY_RENDER = render;   /* dipakai tools/cutaway-uji.mjs (tanpa peramban) */

  /* ------------------------------------------------------------- tampilan --- */
  function satuan() {
    var w = adegan.clientWidth || 900, h = adegan.clientHeight || 620;
    var tinggiSatuan = 100 / D.UKUR.rasio;
    U = Math.min(h * 0.60 / tinggiSatuan, (w * 0.44) / 100);
    document.documentElement.style.setProperty("--u", U.toFixed(3) + "px");
  }

  var noBagian = ("0" + BAGIAN.length).slice(-2);

  function tulisKartu(id) {
    var b = null;
    BAGIAN.forEach(function (x) { if (x.id === id) b = x; });
    if (!b) return;
    var i = BAGIAN.indexOf(b);
    kartuNo.textContent = ("0" + (i + 1)).slice(-2) + " / " + noBagian;
    kartuPeran.textContent = b.peran;
    kartuJudul.textContent = b.nama;
    kartuSpek.textContent = b.spesifikasi;
    kartuCatatan.textContent = b.catatan;
    ukuranEl.innerHTML =
      "<dt>Lebar</dt><dd>" + b.w + " satuan</dd>" +
      "<dt>Tinggi</dt><dd>" + b.h + " satuan</dd>" +
      "<dt>Buka</dt><dd>" + b.jarak + " satuan</dd>" +
      "<dt>Posisi</dt><dd>" + b.pos.join(" / ") + "</dd>";
    Array.prototype.forEach.call(daftarEl.querySelectorAll("button"), function (el) {
      el.setAttribute("aria-current", el.dataset.id === id ? "true" : "false");
    });
  }

  /* ------------------------------------------------------------ kendali x --- */
  /* kalau sistem meminta gerak dikurangi, jangan autoplay: rel & tombol tetap jalan */
  var kurangGerak = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var waktu = 0, main = !kurangGerak, terakhir = 0, dipilih = false;
  var labelPutar = "Putar · " + DURASI + " s";
  mainkanEl.textContent = main ? "Jeda" : labelPutar;

  function keWaktu(t) {
    waktu = ((t % DURASI) + DURASI) % DURASI;
    var s = render(waktu);
    relIsi.style.width = (waktu / DURASI * 100).toFixed(2) + "%";
    relTitik.style.left = (waktu / DURASI * 100).toFixed(2) + "%";
    relEl.setAttribute("aria-valuenow", waktu.toFixed(1));
    waktuEl.textContent = (waktu < 10 ? "0" : "") + waktu.toFixed(1) + " s";
    if (s.terbuka) tulisKartu(s.terbuka);
    else if (s.i === 0) tulisKartu("badan");
    return s;
  }

  function maju(ms) {
    var dt = Math.min(64, ms - terakhir || 16) / 1000;
    terakhir = ms;
    if (main && !dipilih) keWaktu(waktu + dt);
    requestAnimationFrame(maju);
  }

  mainkanEl.addEventListener("click", function () {
    main = !main; dipilih = false;
    mainkanEl.textContent = main ? "Jeda" : labelPutar;
    terakhir = performance.now();
  });

  BAGIAN.forEach(function (b, i) {
    var li = document.createElement("li");
    var bt = document.createElement("button");
    bt.type = "button";
    bt.dataset.id = b.id;
    bt.innerHTML = '<span class="no">' + ("0" + (i + 1)).slice(-2) + "</span><span>" + b.nama + "</span>";
    bt.addEventListener("click", function () {
      var k = null;
      KETUKAN.forEach(function (x) { if (x.bagian === b.id) k = x; });
      main = false; dipilih = true;
      mainkanEl.textContent = labelPutar;
      keWaktu(k ? k.mulai + 1.3 : 0);
    });
    li.appendChild(bt);
    daftarEl.appendChild(li);
  });

  function geser(e) {
    var r = relEl.getBoundingClientRect();
    var x = klem((e.clientX - r.left) / r.width, 0, 1);
    main = false; dipilih = true;
    mainkanEl.textContent = labelPutar;
    keWaktu(x * DURASI);
  }
  var menyeret = false;
  relEl.addEventListener("pointerdown", function (e) { menyeret = true; relEl.setPointerCapture(e.pointerId); geser(e); });
  relEl.addEventListener("pointermove", function (e) { if (menyeret) geser(e); });
  relEl.addEventListener("pointerup", function () { menyeret = false; });
  relEl.addEventListener("keydown", function (e) {
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    e.preventDefault(); dipilih = true; main = false;
    keWaktu(waktu + (e.key === "ArrowRight" ? 1 : -1));
  });

  window.addEventListener("resize", function () { satuan(); keWaktu(waktu); });

  satuan();
  tulisKartu("badan");
  render(0);
  requestAnimationFrame(function (ms) { terakhir = ms; maju(ms); });
})();
