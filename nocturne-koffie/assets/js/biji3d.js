/* ============================================================
   Nocturne — biji3d.js
   Biji kopi Arabika 3D di hero: medium roast, satu biji, bisa diputar
   dengan sentuhan, dan titik-titik di permukaannya memunculkan senyawa
   yang ada di dalamnya.

   Aturan main
   -----------
   1. SEMUA angka (bentuk, warna, kamera, cahaya, zona, senyawa) dibaca dari
      data/biji3d.json. Tidak ada satu pun nilai desain yang ditulis ulang di
      sini, supaya poster CPU (tools/biji.py) dan render WebGL ini memakai
      mesh yang sama.
   2. Tidak ada tiga.js, tidak ada CDN. WebGL mentah ±9 KB skrip; geometri
      tidak diunduh sebagai .glb/.obj karena tidak ada model yang boleh
      diklaim hasil pindai.
   3. Kalau WebGL tidak ada, poster PNG tetap tampil dan daftar zona tetap
      terbaca (kontennya ada di HTML, bukan digambar oleh skrip).
   4. prefers-reduced-motion: tidak berputar sendiri, tidak mengambang.

   Dipasang oleh site.js saat .biji[data-biji3d] masuk viewport.
   ============================================================ */
(function () {
  'use strict';

  const KURANGI = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ── geometri: cermin 1:1 dari tools/biji.py ─────────────────────────── */

  function halus(t) {
    t = Math.max(0, Math.min(1, t));
    return t * t * (3 - 2 * t);
  }

  function hexRgb(h) {
    h = h.replace('#', '');
    return [parseInt(h.slice(0, 2), 16) / 255, parseInt(h.slice(2, 4), 16) / 255, parseInt(h.slice(4, 6), 16) / 255];
  }

  function buatBiji(d) {
    const g = d.geometri;
    const a = g.sumbu.a, b = g.sumbu.b, c = g.sumbu.c;
    const rataF = g.ratakan.faktor;
    const al = g.alur;
    const taper = g.ujung.taper;
    const tek = g.tekstur;

    function alurDalam(x, tp) {
      if (Math.sin(tp) <= 0) return 0;
      let dd = (tp - Math.PI / 2 + Math.PI) % (2 * Math.PI) - Math.PI;
      dd -= al.amplitudo * Math.sin(al.frekuensi * Math.PI * x / a);
      return al.dalam * Math.exp(-(dd * dd) / (2 * al.lebar * al.lebar));
    }

    function titik(tx, tp) {
      const st = Math.sin(tx), ct = Math.cos(tx);
      const sp = Math.sin(tp), cp = Math.cos(tp);
      let x = a * st * cp;
      let y = b * ct;
      let z = c * st * sp;

      const ujung = Math.abs(x) / a;
      const skala = 1 - taper * Math.pow(ujung, 3);
      y *= skala;
      z *= skala;
      x *= 1 - taper * 0.35 * Math.pow(ujung, 4);

      if (sp > 0) {
        const f = rataF + (1 - rataF) * (1 - halus(sp / 0.55));
        z *= f;
        z -= c * 0.04 * halus(sp / 0.55);
        let d0 = (tp - Math.PI / 2 + Math.PI) % (2 * Math.PI) - Math.PI;
        const lobe = Math.cos(Math.min(1, Math.abs(d0) / 1.15) * Math.PI / 2);
        z += c * 0.2 * lobe * (1 - halus(Math.abs(x) / a));
      }

      const dd = alurDalam(x, tp);
      z -= dd * c;
      const ciut = 1 - dd * 0.18;
      x *= ciut;
      y *= ciut;

      const n = Math.sin(x * tek.frekuensi + 1.7)
        * Math.cos(y * tek.frekuensi * 1.13 - 0.4)
        * Math.sin(z * tek.frekuensi * 0.87 + 2.1);
      const tarik = 1 + n * tek.amplitudo;
      return [x * tarik, y * tarik, z * tarik];
    }

    function normal(tx, tp, eps) {
      eps = eps || 1e-3;
      const p0 = titik(tx, tp);
      const p1 = titik(tx + eps, tp);
      const p2 = titik(tx, tp + eps);
      const u = [p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]];
      const v = [p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2]];
      let n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
      const L = Math.hypot(n[0], n[1], n[2]);
      if (L < 1e-9) {
        // kutub: turunan azimut nol, pakai arah radial sebagai normal
        const r = Math.hypot(p0[0], p0[1], p0[2]) || 1;
        return [p0[0] / r, p0[1] / r, p0[2] / r];
      }
      n = [n[0] / L, n[1] / L, n[2] / L];
      if (n[0] * p0[0] + n[1] * p0[1] + n[2] * p0[2] < 0) n = n.map((k) => -k);
      return n;
    }

    function ao(x, tp) {
      return 1 - 0.66 * Math.min(1, alurDalam(x, tp) / al.dalam);
    }

    function arahKePermukaan(arah) {
      const L = Math.hypot(arah[0], arah[1], arah[2]) || 1;
      const u = [arah[0] / L, arah[1] / L, arah[2] / L];
      let lo = 0.05, hi = 2.2;
      for (let i = 0; i < 40; i++) {
        const mid = (lo + hi) / 2;
        const p = [u[0] * mid, u[1] * mid, u[2] * mid];
        const r = Math.hypot(p[0] / a, p[1] / b, p[2] / c);
        if (r > 1) hi = mid; else lo = mid;
      }
      return [u[0] * lo, u[1] * lo, u[2] * lo];
    }

    return { titik, normal, ao, arahKePermukaan };
  }

  /* ── matriks 4×4 sederhana ──────────────────────────────────────────── */

  function putarY(a) {
    const c = Math.cos(a), s = Math.sin(a);
    return [c, 0, -s, 0, 0, 1, 0, 0, s, 0, c, 0, 0, 0, 0, 1];
  }
  function putarX(a) {
    const c = Math.cos(a), s = Math.sin(a);
    return [1, 0, 0, 0, 0, c, s, 0, 0, -s, c, 0, 0, 0, 0, 1];
  }
  function kali(A, B) {
    const O = new Array(16).fill(0);
    for (let i = 0; i < 4; i++)
      for (let j = 0; j < 4; j++)
        for (let k = 0; k < 4; k++) O[i * 4 + j] += A[i * 4 + k] * B[k * 4 + j];
    return O;
  }
  function terapkan(M, p) {
    return [
      M[0] * p[0] + M[1] * p[1] + M[2] * p[2] + M[3],
      M[4] * p[0] + M[5] * p[1] + M[6] * p[2] + M[7],
      M[8] * p[0] + M[9] * p[1] + M[10] * p[2] + M[11],
    ];
  }

  /* ── shader ─────────────────────────────────────────────────────────── */

  const VS = `
attribute vec3 aPos;
attribute vec3 aNrm;
attribute float aAo;
uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProj;
varying vec3 vNrm;
varying vec3 vPos;
varying float vAo;
void main() {
  vec4 w = uModel * vec4(aPos, 1.0);
  vPos = w.xyz;
  vNrm = mat3(uModel) * aNrm;
  vAo = aAo;
  gl_Position = uProj * uView * w;
}`;

  const FS = `
precision mediump float;
varying vec3 vNrm;
varying vec3 vPos;
varying float vAo;
uniform vec3 uGelap;
uniform vec3 uTengah;
uniform vec3 uTerang;
uniform vec3 uKilau;
uniform vec3 uKunci;
uniform vec3 uIsi;
uniform vec3 uMata;
uniform float uKekuatanKunci;
uniform float uKekuatanIsi;
uniform float uPangkat;
uniform float uSumbuY;
uniform float uKilauKekuatan;

float halus(float t) { return t * t * (3.0 - 2.0 * t); }

void main() {
  vec3 n = normalize(vNrm);
  vec3 v = normalize(uMata - vPos);
  if (dot(n, v) < 0.0) n = -n;            /* dua sisi: alur tidak berlubang */
  vec3 kunci = normalize(uKunci);
  vec3 isi = normalize(uIsi);
  float lam = max(0.0, dot(n, kunci)) * uKekuatanKunci;
  float fil = max(0.0, dot(n, isi)) * uKekuatanIsi;
  vec3 h = normalize(kunci + v);
  float spec = pow(max(0.0, dot(n, h)), uPangkat) * uKilauKekuatan;
  float rim = pow(1.0 - max(0.0, dot(n, v)), 3.0) * 0.14;

  float t = halus(lam * 1.15);
  vec3 dasar = mix(uGelap, uTengah, t);
  float atas = halus((vPos.y / uSumbuY + 1.0) * 0.5);
  dasar = mix(dasar, uTerang, 0.42 * t * atas);

  vec3 col = dasar * (0.42 + 0.58 * lam) + uIsi * fil * 0.9;
  col += uKilau * spec;
  col = col * (0.55 + 0.45 * vAo) + rim;

  col = pow(clamp(col, 0.0, 1.0), vec3(1.0 / 1.05));
  gl_FragColor = vec4(col, 1.0);
}`;

  /* ── utilitas matriks kamera ────────────────────────────────────────── */

  function normalisasi(v) {
    const L = Math.hypot(v[0], v[1], v[2]) || 1;
    return [v[0] / L, v[1] / L, v[2] / L];
  }
  function silang(a, b) {
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  }
  function titikDot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }

  function kamera(cam) {
    const mata = cam.posisi;
    const maju = normalisasi([cam.target[0] - mata[0], cam.target[1] - mata[1], cam.target[2] - mata[2]]);
    const kanan = normalisasi(silang(maju, [0, 1, 0]));
    const atas = silang(kanan, maju);
    const view = [
      kanan[0], kanan[1], kanan[2], -titikDot(kanan, mata),
      atas[0], atas[1], atas[2], -titikDot(atas, mata),
      -maju[0], -maju[1], -maju[2], titikDot(maju, mata),
      0, 0, 0, 1,
    ];
    const f = 1 / Math.tan((cam.fov_deg * Math.PI) / 180 / 2);
    return { mata, maju, kanan, atas, view, f };
  }

  function proyeksiLayar(k, p, lebar, tinggi, aspek) {
    const d = [p[0] - k.mata[0], p[1] - k.mata[1], p[2] - k.mata[2]];
    const z = titikDot(d, k.maju);
    if (z <= 0.01) return null;
    const f = k.f;
    const x = (titikDot(d, k.kanan) / z) * f;
    const y = (titikDot(d, k.atas) / z) * f;
    return [((x / aspek) * 0.5 + 0.5) * lebar, (0.5 - y * 0.5) * tinggi, z];
  }

  /* ── pasang ─────────────────────────────────────────────────────────── */

  function pasang(akar) {
    if (akar.dataset.bijiSiap) return;
    akar.dataset.bijiSiap = 'memuat';

    const kanvas = akar.querySelector('[data-biji-kanvas]');
    const panggung = akar.querySelector('[data-biji-panggung]');
    const lapisanTitik = akar.querySelector('[data-biji-lapis]');
    const panel = akar.querySelector('[data-biji-panel]');
    if (!kanvas || !panggung || !lapisanTitik) return;

    fetch(akar.dataset.bijiSumber || 'data/biji3d.json')
      .then((r) => r.json())
      .then((d) => mulai(d))
      .catch((e) => {
        akar.dataset.bijiGagal = e.message;
        console.warn('[biji3d]', e.message);
      });

    function mulai(d) {
      const biji = buatBiji(d);
      const cam = kamera(d.kamera);
      cam.fovDeg = d.kamera.fov_deg;
      const warna = {
        gelap: hexRgb(d.warna.gelap),
        tengah: hexRgb(d.warna.tengah),
        terang: hexRgb(d.warna.terang),
        kilau: hexRgb(d.warna.kilau),
      };

      const gl = kanvas.getContext('webgl', { antialias: true, alpha: true, premultipliedAlpha: false });
      let siap = null;

      if (gl) {
        siap = siapkanGL(gl);
      } else {
        akar.dataset.bijiMode = 'poster';
      }

      /* ── 1 · ukuran & mesh ─────────────────────────────────────────── */
      /* rotasi model mulai dari nol: sudut pandang sudah dibawa posisi kamera.
         Kalau diputar lagi di sini, hasilnya menyimpang dari poster PNG. */
      let yaw = 0;
      let pitch = 0;
      let yawSasaran = yaw, pitchSasaran = pitch;
      let geser = 0;
      let tidur = 0;
      let aktif = false;
      let jalan = true;
      let raf = 0;
      let lebar = 0, tinggi = 0, aspek = 1;
      let posTitik = [];

      function ukuranMesh() {
        const kecil = window.innerWidth < 760;
        const r = kecil ? d.geometri.resolusi.seluler : d.geometri.resolusi.desktop;
        const skala = 1;   /* 151×300 vertex = 45.300 < 65535, aman untuk Uint16 */
        return [Math.round(r[0] * skala), Math.round(r[1] * skala)];
      }

      function bangun(rx, ry) {
        const nVert = (rx + 1) * ry;
        const pos = new Float32Array(nVert * 3);
        const nrm = new Float32Array(nVert * 3);
        const aoArr = new Float32Array(nVert);
        let k = 0;
        for (let i = 0; i <= rx; i++) {
          const tx = (Math.PI * i) / rx;
          for (let j = 0; j < ry; j++) {
            const tp = (2 * Math.PI * j) / ry;
            const p = biji.titik(tx, tp);
            const n = biji.normal(tx, tp);
            pos[k * 3] = p[0]; pos[k * 3 + 1] = p[1]; pos[k * 3 + 2] = p[2];
            nrm[k * 3] = n[0]; nrm[k * 3 + 1] = n[1]; nrm[k * 3 + 2] = n[2];
            aoArr[k] = biji.ao(p[0], tp);
            k++;
          }
        }
        const idx = [];
        for (let i = 0; i < rx; i++) {
          for (let j = 0; j < ry; j++) {
            const a0 = i * ry + j;
            const a1 = i * ry + ((j + 1) % ry);
            const a2 = (i + 1) * ry + j;
            const a3 = (i + 1) * ry + ((j + 1) % ry);
            idx.push(a0, a2, a1, a1, a2, a3);
          }
        }
        return { pos, nrm, ao: aoArr, idx: new Uint16Array(idx), n: idx.length };
      }

      function siapkanGL(gl) {
        function sh(type, src) {
          const s = gl.createShader(type);
          gl.shaderSource(s, src);
          gl.compileShader(s);
          if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
            console.warn('[biji3d] shader', gl.getShaderInfoLog(s));
            return null;
          }
          return s;
        }
        const vs = sh(gl.VERTEX_SHADER, VS);
        const fs = sh(gl.FRAGMENT_SHADER, FS);
        if (!vs || !fs) return null;
        const prog = gl.createProgram();
        gl.attachShader(prog, vs);
        gl.attachShader(prog, fs);
        gl.linkProgram(prog);
        if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
          console.warn('[biji3d] link', gl.getProgramInfoLog(prog));
          return null;
        }
        gl.useProgram(prog);
        const buf = {
          pos: gl.createBuffer(), nrm: gl.createBuffer(), ao: gl.createBuffer(), idx: gl.createBuffer(),
        };
        const attr = {
          pos: gl.getAttribLocation(prog, 'aPos'),
          nrm: gl.getAttribLocation(prog, 'aNrm'),
          ao: gl.getAttribLocation(prog, 'aAo'),
        };
        const uni = {};
        ['uModel', 'uView', 'uProj', 'uGelap', 'uTengah', 'uTerang', 'uKilau', 'uKunci', 'uIsi',
          'uMata', 'uKekuatanKunci', 'uKekuatanIsi', 'uPangkat', 'uKilauKekuatan', 'uSumbuY']
          .forEach((n) => { uni[n] = gl.getUniformLocation(prog, n); });

        gl.enable(gl.DEPTH_TEST);
        gl.disable(gl.CULL_FACE);   /* dua sisi: alur cekung tidak boleh berlubang */
        gl.clearColor(0, 0, 0, 0);

        return { gl, prog, buf, attr, uni, mesh: null, jumlah: 0 };
      }

      function unggahMesh() {
        if (!siap) return;
        const [rx, ry] = ukuranMesh();
        const m = bangun(rx, ry);
        const { gl, buf, attr } = siap;
        gl.bindBuffer(gl.ARRAY_BUFFER, buf.pos);
        gl.bufferData(gl.ARRAY_BUFFER, m.pos, gl.STATIC_DRAW);
        gl.enableVertexAttribArray(attr.pos);
        gl.vertexAttribPointer(attr.pos, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, buf.nrm);
        gl.bufferData(gl.ARRAY_BUFFER, m.nrm, gl.STATIC_DRAW);
        gl.enableVertexAttribArray(attr.nrm);
        gl.vertexAttribPointer(attr.nrm, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, buf.ao);
        gl.bufferData(gl.ARRAY_BUFFER, m.ao, gl.STATIC_DRAW);
        gl.enableVertexAttribArray(attr.ao);
        gl.vertexAttribPointer(attr.ao, 1, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buf.idx);
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, m.idx, gl.STATIC_DRAW);
        siap.jumlah = m.n;
        siap.mesh = m;
        akar.dataset.bijiSegitiga = String(m.n / 3);
      }

      function ukur() {
        const kotak = panggung.getBoundingClientRect();
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        lebar = Math.max(1, Math.round(kotak.width * dpr));
        tinggi = Math.max(1, Math.round(kotak.height * dpr));
        aspek = kotak.width / Math.max(1, kotak.height);
        if (siap) {
          kanvas.width = lebar;
          kanvas.height = tinggi;
          siap.gl.viewport(0, 0, lebar, tinggi);
        }
        taruhTitik();
      }

      /* ── 2 · titik sentuh ───────────────────────────────────────────*/
      const zona = d.zona.map((z, i) => {
        const p = biji.arahKePermukaan(z["arah"]);
        return Object.assign({}, z, { no: i + 1, titik: p });
      });

      function matriksModel() {
        return kali(putarY(yaw), putarX(pitch));
      }

      function taruhTitik() {
        const M = matriksModel();
        const kotak = panggung.getBoundingClientRect();
        if (!kotak.width) return;
        posTitik = zona.map((z) => {
          const p = terapkan(M, z.titik);
          // perkiraan normal di permukaan elipsoid, diputar bersama model
          const s3 = d.geometri.sumbu;
          const n = normalisasi(terapkan(M, [
            z.titik[0] / (s3.a * s3.a), z.titik[1] / (s3.b * s3.b), z.titik[2] / (s3.c * s3.c),
          ]));
          const layar = proyeksiLayar(cam, p, kotak.width, kotak.height, aspek);
          const mata = normalisasi([cam.mata[0] - p[0], cam.mata[1] - p[1], cam.mata[2] - p[2]]);
          const tampak = titikDot(n, mata) > 0.12;
          return { id: z.id, layar, tampak };
        });

        const tombol = lapisanTitik.querySelectorAll('[data-biji-titik]');
        posTitik.forEach((pt, i) => {
          const b = tombol[i];
          if (!b) return;
          if (!pt.layar || !pt.tampak) {
            b.style.opacity = '0';
            b.style.pointerEvents = 'none';
            return;
          }
          b.style.opacity = '1';
          b.style.pointerEvents = 'auto';
          b.style.transform = `translate(${(pt.layar[0] / kotak.width) * 100}%, ${(pt.layar[1] / kotak.height) * 100}%)`;
          b.dataset.layarX = String((pt.layar[0] / kotak.width) * 100);
          b.dataset.layarY = String((pt.layar[1] / kotak.height) * 100);
        });
      }

      /* ── 3 · gambar ───────────────────────────────────────────────── */
      function gambar() {
        if (!siap || !siap.jumlah) return;
        const { gl, uni } = siap;
        const M = matriksModel();
        gl.useProgram(siap.prog);
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        gl.uniformMatrix4fv(uni.uModel, false, new Float32Array(M));
        gl.uniformMatrix4fv(uni.uView, false, new Float32Array(cam.view));
        const f = cam.f;
        const proj = [f / aspek, 0, 0, 0, 0, f, 0, 0, 0, 0, -1.002, -0.2, 0, 0, -1, 0];
        gl.uniformMatrix4fv(uni.uProj, false, new Float32Array(proj));
        gl.uniform3fv(uni.uGelap, warna.gelap);
        gl.uniform3fv(uni.uTengah, warna.tengah);
        gl.uniform3fv(uni.uTerang, warna.terang);
        gl.uniform3fv(uni.uKilau, warna.kilau);
        gl.uniform3fv(uni.uKunci, d.cahaya.kunci);
        gl.uniform3fv(uni.uIsi, d.cahaya.isi);
        gl.uniform3fv(uni.uMata, cam.mata);
        gl.uniform1f(uni.uKekuatanKunci, d.cahaya.kekuatan_kunci);
        gl.uniform1f(uni.uKekuatanIsi, d.cahaya.kekuatan_isi);
        gl.uniform1f(uni.uPangkat, d.cahaya.kilau_pangkat);
        gl.uniform1f(uni.uSumbuY, d.geometri.sumbu.b);
        gl.uniform1f(uni.uKilauKekuatan, d.cahaya.kilau_kekuatan);
        gl.drawElements(gl.TRIANGLES, siap.jumlah, gl.UNSIGNED_SHORT, 0);
      }

      /* ── 4 · loop ─────────────────────────────────────────────────── */
      let sebelumnya = performance.now();
      function loop(kini) {
        if (!jalan) return;
        const dt = Math.min(0.05, (kini - sebelumnya) / 1000);
        sebelumnya = kini;

        if (!aktif) tidur += dt;
        const diam = !KURANGI.matches && !aktif && tidur > 1.6;
        if (diam) {
          yawSasaran += (d.kamera.putar_otomatis_deg_per_detik * Math.PI / 180) * dt;
        }
        if (!KURANGI.matches) {
          geser = Math.sin(kini / 2400) * 0.012;
        }
        yaw += (yawSasaran - yaw) * Math.min(1, dt * 7);
        pitch += (pitchSasaran - pitch) * Math.min(1, dt * 7);

        panggung.style.transform = `translateY(${(geser * 100).toFixed(2)}%)`;
        gambar();
        taruhTitik();
        raf = requestAnimationFrame(loop);
      }

      /* ── 5 · tarik untuk memutar ─────────────────────────────────── */
      let tarik = null;
      const maks = (d.kamera.geser_maks_deg * Math.PI) / 180;

      panggung.addEventListener('pointerdown', (e) => {
        if (e.target.closest('[data-biji-titik]')) return;
        tarik = { x: e.clientX, y: e.clientY, yaw, pitch };
        aktif = true;
        tidur = 0;
        panggung.setPointerCapture(e.pointerId);
        panggung.classList.add('biji__panggung--tarik');
      });

      panggung.addEventListener('pointermove', (e) => {
        if (!tarik) return;
        const dx = e.clientX - tarik.x;
        const dy = e.clientY - tarik.y;
        yawSasaran = tarik.yaw + dx * 0.006;
        pitchSasaran = Math.max(-maks, Math.min(maks, tarik.pitch + dy * 0.004));
        yaw = yawSasaran;
        pitch = pitchSasaran;
        gambar();
      });

      function lepas(e) {
        if (!tarik) return;
        tarik = null;
        aktif = false;
        tidur = 0;
        panggung.classList.remove('biji__panggung--tarik');
        if (e && e.pointerId != null && panggung.hasPointerCapture(e.pointerId)) {
          panggung.releasePointerCapture(e.pointerId);
        }
      }
      panggung.addEventListener('pointerup', lepas);
      panggung.addEventListener('pointercancel', lepas);
      panggung.addEventListener('pointerleave', lepas);

      /* keyboard: panah memutar, agar bisa dipakai tanpa sentuh */
      panggung.setAttribute('tabindex', '0');
      panggung.addEventListener('keydown', (e) => {
        const langkah = 0.16;
        if (e.key === 'ArrowLeft') { yawSasaran -= langkah; e.preventDefault(); }
        if (e.key === 'ArrowRight') { yawSasaran += langkah; e.preventDefault(); }
        if (e.key === 'ArrowUp') { pitchSasaran = Math.max(-maks, pitchSasaran - langkah); e.preventDefault(); }
        if (e.key === 'ArrowDown') { pitchSasaran = Math.min(maks, pitchSasaran + langkah); e.preventDefault(); }
        if (e.key === 'Home') {
          yawSasaran = 0;
          pitchSasaran = 0;
          e.preventDefault();
        }
        aktif = true;
        tidur = 0;
      });

      /* ── 6 · panel senyawa ────────────────────────────────────────── */
      function buka(id) {
        const z = zona.find((x) => x.id === id);
        if (!z || !panel) return;
        const judul = panel.querySelector('[data-biji-judul]');
        const ringkas = panel.querySelector('[data-biji-ringkas]');
        const daftar = panel.querySelector('[data-biji-senyawa]');
        if (judul) judul.textContent = `${String(z.no).padStart(2, '0')} · ${z.nama}`;
        if (ringkas) ringkas.textContent = z.ringkas;
        if (daftar) {
          daftar.innerHTML = z.senyawa.map((s) => (
            `<li><b>${s.nama}</b> <span class="biji__rumus">${s.rumus}</span>`
            + `<span class="biji__rentang">${s.rentang}</span>`
            + `<span class="biji__peran">${s.peran}</span>`
            + `<span class="biji__sumber">${s.keyakinan === 'kuat' ? 'literatur terukur' : 'rentang umum'} · ${s.sumber}</span></li>`
          )).join('');
        }
        panel.hidden = false;
        akar.dataset.bijiAktif = id;
        akar.classList.add('biji--buka');
        lapisanTitik.querySelectorAll('[data-biji-titik]').forEach((b) => {
          const pilih = b.dataset.bijiTitik === id;
          b.setAttribute('aria-pressed', pilih ? 'true' : 'false');
          b.classList.toggle('biji__titik--aktif', pilih);
        });
        // sorot butir daftar statis yang sama (untuk pembaca layar & tanpa WebGL)
        document.querySelectorAll('[data-biji-zona]').forEach((el) => {
          el.classList.toggle('biji__zona--aktif', el.dataset.bijiZona === id);
        });
      }

      lapisanTitik.addEventListener('click', (e) => {
        const b = e.target.closest('[data-biji-titik]');
        if (!b) return;
        aktif = true;
        tidur = 0;
        buka(b.dataset.bijiTitik);
      });

      if (panel) {
        const tutup = panel.querySelector('[data-biji-tutup]');
        if (tutup) tutup.addEventListener('click', () => {
          panel.hidden = true;
          akar.classList.remove('biji--buka');
          akar.removeAttribute('data-biji-aktif');
          lapisanTitik.querySelectorAll('[data-biji-titik]').forEach((b) => {
            b.setAttribute('aria-pressed', 'false');
            b.classList.remove('biji__titik--aktif');
          });
        });
      }

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && panel && !panel.hidden) {
          panel.hidden = true;
          akar.classList.remove('biji--buka');
        }
      });

      /* ── 7 · mulai ────────────────────────────────────────────────── */
      if (siap) unggahMesh();
      ukur();
      akar.dataset.bijiMode = siap ? 'webgl' : 'poster';
      akar.classList.add('biji--siap');
      if (siap) {
        gambar();
        raf = requestAnimationFrame(loop);
      }
      taruhTitik();

      let jedaUkur = 0;
      window.addEventListener('resize', () => {
        clearTimeout(jedaUkur);
        jedaUkur = setTimeout(() => {
          const lama = JSON.stringify(ukuranMesh());
          ukur();
          unggahMesh();
          gambar();
          if (lama) taruhTitik();
        }, 140);
      });

      document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
          jalan = false;
          cancelAnimationFrame(raf);
        } else if (siap) {
          jalan = true;
          sebelumnya = performance.now();
          raf = requestAnimationFrame(loop);
        }
      });
    }
  }

  function mulaiOtomatis() {
    const target = Array.from(document.querySelectorAll('[data-biji3d]'));
    if (!target.length) return;
    if (!('IntersectionObserver' in window)) {
      target.forEach(pasang);
      return;
    }
    const io = new IntersectionObserver((masuk) => {
      masuk.forEach((m) => {
        if (!m.isIntersecting) return;
        io.unobserve(m.target);
        pasang(m.target);
      });
    }, { rootMargin: '240px 0px' });
    target.forEach((el) => io.observe(el));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mulaiOtomatis, { once: true });
  } else {
    mulaiOtomatis();
  }

  /* diekspor supaya bisa diperiksa tanpa browser: tools/verifikasi-biji.mjs
     membandingkan posisi titik hasil skrip ini dengan poster CPU (tools/biji.py) */
  window.NocturneBiji3D = {
    pasang, buatBiji, kamera, proyeksiLayar, terapkan, kali, putarY, putarX, normalisasi, titikDot,
  };
})();
