/* ============================================================
   Nocturne Koffie — site.js
   Satu sumber data: data/catalog.json
   Tidak ada framework, tidak ada build step.
   ============================================================ */
(function () {
  'use strict';

  const RP = new Intl.NumberFormat('id-ID');
  const rupiah = (n) => 'Rp' + RP.format(n);
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  let DATA = null;

  /* ---------- util ---------- */
  function waLink(number, text) {
    return 'https://wa.me/' + number + '?text=' + encodeURIComponent(text);
  }

  function orderMessage(p, variant, grind, qty) {
    return [
      'Halo Nocturne Koffie! Saya mau order:',
      '— Produk: ' + p.name,
      '— Berat: ' + variant.weight.replace(' ', ''),
      '— Grind: ' + grind,
      '— Jumlah: ' + qty,
      '',
      'Mohon info stok & ongkirnya ya. Terima kasih!'
    ].join('\n');
  }

  function notifyMessage(p) {
    return [
      'Halo Nocturne Koffie, saya mau dikabari kalau ' + p.name + ' tersedia lagi.',
      'Boleh dihubungi di nomor ini ya. Terima kasih!'
    ].join('\n');
  }

  function roastDots(level, confirmed) {
    let html = '<div class="roast__dots" aria-hidden="true">';
    for (let i = 1; i <= 5; i++) {
      html += '<span class="roast__dot' + (i <= level ? ' is-on' : '') + '"></span>';
    }
    html += '</div>';
    const scale = DATA.roast_scale.find((r) => r.level === level);
    const label = scale ? scale.level + '/5 · ' + scale.name : 'per batch';
    return '<div class="roast">' + html + '<span>' + label + (confirmed === false ? ' · konfirmasi' : '') + '</span></div>';
  }

  function stockNote(p) {
    const s = DATA.stock_states[p.status || 'tersedia'];
    if (!s || !s.note) return '';
    return '<p class="card__stock-note">' + s.note.replace('{bulan}', 'Desember') + '</p>';
  }

  function statusBadge(p) {
    const s = p.status || 'tersedia';
    const label = (DATA.stock_states[s] && DATA.stock_states[s].label) || 'Tersedia';
    return '<span class="badge badge--' + s + '">' + label + '</span>';
  }

  /* ---------- hydrate brand ---------- */
  function hydrateBrand() {
    const b = DATA.brand;
    document.title = b.name + ' — ' + b.headline.join(' ');
    $$('[data-brand="intro"]').forEach((el) => (el.textContent = b.intro));
    $$('[data-brand="stock_updated"]').forEach((el) => (el.textContent = b.stock_updated));

    const promo = $('[data-promo-text]');
    if (promo) promo.textContent = b.promo_bar.text;
    const promoLink = $('[data-promo]');
    if (promoLink) promoLink.href = b.promo_bar.href;

    // tautan brand (whatsapp / instagram / email)
    $$('[data-brand-link="whatsapp"], [data-brand-link="whatsapp-raw"]').forEach((el) => {
      el.href = waLink(b.whatsapp, 'Halo Nocturne Koffie! Saya mau tanya soal kopinya.');
      el.textContent = el.textContent.trim() === '' ? b.wa_display : el.textContent;
    });
    $$('[data-brand-link="instagram"]').forEach((el) => {
      el.href = b.instagram;
      el.textContent = b.instagram_label;
    });
    $$('[data-brand-link="email"]').forEach((el) => {
      el.href = 'mailto:' + b.email;
      el.textContent = b.email;
    });

    // jam operasional
    const hours = b.hours + ' — ' + b.reply_note + '.';
    const ch = $('#closing-hours');
    if (ch) ch.textContent = hours;

    // JSON-LD
    const ld = $('#ldjson');
    if (ld) {
      try {
        const obj = JSON.parse(ld.textContent);
        obj.name = b.name;
        obj.description = b.intro;
        obj.email = b.email;
        obj.telephone = b.wa_display;
        obj.address.addressLocality = b.city;
        obj.sameAs = [b.instagram];
        ld.textContent = JSON.stringify(obj);
      } catch (e) { /* diamkan */ }
    }
  }

  /* ---------- tombol WhatsApp kontekstual ---------- */
  const WA_CONTEXT = {
    nav: 'Halo Nocturne Koffie! Saya mau tanya soal kopi dan mau order. Mohon info stok & ongkirnya ya.',
    menu: 'Halo Nocturne Koffie! Saya mau tanya soal kopi dan mau order. Mohon info stok & ongkirnya ya.',
    fab: 'Halo Nocturne Koffie! Saya mau tanya soal kopi.',
    closing: 'Halo Nocturne Koffie! Saya mau pesan kopi. Cara seduh saya: ... (boleh dibantu pilihkan?)',
    member: 'Halo Nocturne Koffie! Saya mau daftar Member Nocturne Circle. Nama saya: ... Domisili: ... Email: ...',
    footer: 'Halo Nocturne Koffie! Saya mau tanya soal kopinya.',
    journal: 'Halo Nocturne Koffie! Saya mau tahu kapan Journal-nya terbit.',
    kafe: 'Halo Nocturne Koffie! Saya tertarik untuk kebutuhan kafe/kantor. Boleh info harga & sampelnya?'
  };
  function hydrateWaButtons() {
    $$('[data-wa]').forEach((el) => {
      const key = el.getAttribute('data-wa');
      const text = WA_CONTEXT[key] || WA_CONTEXT.closing;
      el.href = waLink(DATA.brand.whatsapp, text);
      el.target = '_blank';
      el.rel = 'noopener';
    });
  }

  /* ---------- hero marquee ---------- */
  function buildMarquee() {
    const track = $('#marquee-track');
    if (!track) return;
    const list = DATA.products;
    const make = (p, i, dup) => {
      const a = document.createElement('a');
      a.className = 'hcard hcard--' + ((i % 4) + 1);
      a.href = '#kartu-' + p.id;
      a.setAttribute('data-jump', p.id);
      if (dup) { a.setAttribute('aria-hidden', 'true'); a.tabIndex = -1; }
      a.innerHTML =
        '<span class="hcard__meta">' + p.category + ' · ' + p.region + '</span>' +
        '<span class="hcard__arrow" aria-hidden="true">↗</span>' +
        '<span class="hcard__name">' + p.name + '</span>';
      return a;
    };
    list.forEach((p, i) => track.appendChild(make(p, i, false)));
    list.forEach((p, i) => track.appendChild(make(p, i, true)));

    // jeda manual (syarat aksesibilitas konten bergerak)
    const marquee = $('#marquee');
    const btn = $('#marquee-pause');
    if (btn) {
      btn.addEventListener('click', () => {
        const paused = marquee.classList.toggle('is-paused');
        btn.setAttribute('aria-pressed', paused ? 'true' : 'false');
        btn.setAttribute('aria-label', paused ? 'Lanjutkan guliran nama produk' : 'Jeda guliran nama produk');
      });
    }
    // keyboard: fokus pada kartu → berhenti
    track.addEventListener('focusin', () => marquee.classList.add('is-paused'));
    track.addEventListener('focusout', () => {
      if (btn && btn.getAttribute('aria-pressed') !== 'true') marquee.classList.remove('is-paused');
    });
    // click → lompat ke kartu produk
    track.addEventListener('click', (e) => {
      const a = e.target.closest('[data-jump]');
      if (!a) return;
      e.preventDefault();
      jumpTo(a.getAttribute('data-jump'));
    });
  }

  function jumpTo(id) {
    const card = document.getElementById('kartu-' + id);
    if (!card) return;
    history.replaceState(null, '', '#' + id);
    card.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    $$('.card.is-target').forEach((c) => c.classList.remove('is-target'));
    card.classList.add('is-target');
    window.setTimeout(() => card.classList.remove('is-target'), 2100);
  }

  /* ---------- rail editorial ---------- */
  function buildRails() {
    const groups = [
      { el: '#rail-single', items: DATA.products.filter((p) => p.category === 'Single Origin') },
      { el: '#rail-blend', items: DATA.products.filter((p) => p.category === 'Signature Blend') },
      { el: '#rail-paket', items: DATA.bundles }
    ];
    groups.forEach((g) => {
      const host = $(g.el);
      if (!host) return;
      g.items.forEach((p) => {
        const li = document.createElement('li');
        const status = DATA.stock_states[p.status || 'tersedia'];
        li.innerHTML =
          '<button class="rail__item" type="button" data-jump="' + p.id + '">' +
            '<b>' + p.name + '</b>' +
            '<span class="rail__status">' + (status ? status.label : 'Tersedia') + '</span>' +
            '<small>' + (p.category === 'Paket' ? p.contents + ' · ' + rupiah(p.price) : p.origin_line + ' · ' + p.elevation) + '</small>' +
          '</button>';
        host.appendChild(li);
      });
    });
    document.addEventListener('click', (e) => {
      const b = e.target.closest('[data-jump]');
      if (!b) return;
      e.preventDefault();
      jumpTo(b.getAttribute('data-jump'));
    });
  }

  /* ---------- kartu produk ---------- */
  function productCard(p) {
    const el = document.createElement('article');
    el.className = 'card';
    el.id = 'kartu-' + p.id;
    el.setAttribute('data-kategori', p.category);
    el.setAttribute('data-daerah', p.region);
    el.setAttribute('data-status', p.status || 'tersedia');

    const variants = p.variants.map((v, i) =>
      '<button class="vbtn' + (i === 0 ? ' is-on' : '') + '" type="button" data-i="' + i + '">' + v.weight + '</button>'
    ).join('');

    const grindOptions = (p.grind || ['Biji utuh'])
      .map((g) => '<option>' + g + '</option>').join('');

    const plaque = p.farmer_type === 'blend'
      ? '<div class="plaque">' +
          '<p class="plaque__label">Signature Blend</p>' +
          '<p class="plaque__name">' + (p.composition || p.variety) + '</p>' +
          '<dl class="plaque__data"><div><dt>Catatan</dt><dd>Detail petani tidak ditampilkan pada blend.</dd></div></dl>' +
        '</div>'
      : '<div class="plaque">' +
          '<p class="plaque__label">' + (p.farmer_type === 'collective' ? 'Kolektif petani' : 'Ditanam oleh') + '</p>' +
          '<p class="plaque__name">' + p.farmer + '</p>' +
          '<dl class="plaque__data">' +
            '<div><dt>Wilayah</dt><dd>' + [p.village, p.district, p.region].filter(Boolean).join(', ') + '</dd></div>' +
            '<div><dt>Ketinggian</dt><dd>' + p.elevation + '</dd></div>' +
            '<div><dt>Varietas</dt><dd>' + p.variety + '</dd></div>' +
          '</dl>' +
        '</div>';

    el.innerHTML =
      '<div class="card__media">' +
        statusBadge(p) +
        '<span class="card__no">' + p.no + '</span>' +
        '<img src="' + p.img + '" alt="Kemasan ' + p.name + ' — ' + p.origin_line + '" width="760" height="950" loading="lazy" decoding="async">' +
      '</div>' +
      '<p class="eyebrow">' + p.no + ' · ' + p.origin_line + ' · ' + p.process + '</p>' +
      '<h3 class="card__name">' + p.name + '</h3>' +
      '<p class="card__sub">' + p.kind + ' · ' + p.variety + '</p>' +
      '<ul class="card__notes">' + p.notes.map((n) => '<li>' + n + '</li>').join('') + '</ul>' +
      roastDots(p.roast_level, p.roast_confirmed) +
      plaque +
      '<div class="price">' +
        '<div class="price__now"><span class="price__value" data-price>' + rupiah(p.variants[0].price) + '</span><span class="price__unit" data-unit>/ ' + p.variants[0].weight + '</span></div>' +
        '<div class="price__variants">' + variants + '</div>' +
      '</div>' +
      '<div class="buy">' +
        '<div class="field"><label for="grind-' + p.id + '">Gilingan</label><select id="grind-' + p.id + '" data-grind>' + grindOptions + '</select></div>' +
        '<div class="field"><label for="qty-' + p.id + '">Jumlah</label>' +
          '<div class="qty"><button type="button" data-step="-1" aria-label="Kurangi jumlah">−</button>' +
          '<input id="qty-' + p.id + '" type="number" min="1" max="20" value="1" inputmode="numeric" data-qty>' +
          '<button type="button" data-step="1" aria-label="Tambah jumlah">+</button></div>' +
        '</div>' +
      '</div>' +
      '<a class="btn btn--ink card__btn" href="#" data-order>Pesan via WhatsApp</a>' +
      stockNote(p) +
      '<p class="micro" style="margin-top:10px">Seduh: ' + (p.brew || []).join(' · ') + '</p>';

    /* interaksi kartu */
    let idx = 0;
    const btnOrder = $('[data-order]', el);
    const priceEl = $('[data-price]', el);
    const unitEl = $('[data-unit]', el);
    const grindEl = $('[data-grind]', el);
    const qtyEl = $('[data-qty]', el);

    const soldOut = p.status === 'habis' || p.status === 'menunggu-panen';
    if (soldOut) {
      btnOrder.textContent = 'Kabari saya saat ada';
      btnOrder.href = waLink(DATA.brand.whatsapp, notifyMessage(p));
    }

    $$('.vbtn', el).forEach((btn) => {
      btn.addEventListener('click', () => {
        idx = Number(btn.getAttribute('data-i'));
        $$('.vbtn', el).forEach((b) => b.classList.toggle('is-on', b === btn));
        priceEl.textContent = rupiah(p.variants[idx].price);
        unitEl.textContent = '/ ' + p.variants[idx].weight;
        setOrderHref();
      });
    });

    function setOrderHref() {
      if (soldOut) {
        btnOrder.href = waLink(DATA.brand.whatsapp, notifyMessage(p));
        return;
      }
      const qty = Math.max(1, Math.min(20, Number((qtyEl && qtyEl.value) || 1)));
      const grind = (grindEl && grindEl.value ? grindEl.value : (p.grind && p.grind[0]) || 'Biji utuh').trim();
      btnOrder.href = waLink(DATA.brand.whatsapp, orderMessage(p, p.variants[idx], grind, qty));
    }

    qtyEl.addEventListener('input', setOrderHref);
    grindEl.addEventListener('change', setOrderHref);
    $$('[data-step]', el).forEach((b) => {
      b.addEventListener('click', () => {
        const next = (Number(qtyEl.value) || 1) + Number(b.getAttribute('data-step'));
        qtyEl.value = Math.max(1, Math.min(20, next));
        setOrderHref();
      });
    });
    btnOrder.target = '_blank';
    btnOrder.rel = 'noopener';
    setOrderHref();

    return el;
  }

  function bundleCard(b) {
    const el = document.createElement('article');
    el.className = 'card';
    el.id = 'kartu-' + b.id;
    el.setAttribute('data-kategori', 'Paket');
    el.setAttribute('data-daerah', '');
    el.setAttribute('data-status', b.status || 'tersedia');
    el.innerHTML =
      '<div class="card__media">' +
        statusBadge(b) +
        '<span class="card__no">' + b.no + '</span>' +
        '<img src="' + b.img + '" alt="Paket ' + b.name + ' — ' + b.contents + '" width="760" height="950" loading="lazy" decoding="async">' +
      '</div>' +
      '<p class="eyebrow">' + b.no + ' · Paket · ' + b.contents + '</p>' +
      '<h3 class="card__name">' + b.name + '</h3>' +
      '<p class="card__sub">' + b.desc + '</p>' +
      '<div class="price">' +
        '<div class="price__now">' +
          '<span class="price__value">' + rupiah(b.price) + '</span>' +
          '<span class="price__unit">hemat ' + rupiah(b.price_normal - b.price) + ' dari ' + rupiah(b.price_normal) + '</span>' +
        '</div>' +
      '</div>' +
      '<a class="btn btn--orange card__btn" href="#" data-order>Pesan via WhatsApp</a>' +
      '<p class="micro" style="margin-top:10px">Isi: ' + b.contents + ' · SKU ' + b.sku + '</p>';
    const a = $('[data-order]', el);
    a.href = waLink(DATA.brand.whatsapp,
      'Halo Nocturne Koffie! Saya mau order:\n— Produk: Paket ' + b.name + '\n— Isi: ' + b.contents + '\n— Jumlah: 1\n\nMohon info stok & ongkirnya ya. Terima kasih!');
    a.target = '_blank';
    a.rel = 'noopener';
    return el;
  }

  function buildGrid() {
    const grid = $('#grid');
    if (!grid) return;
    DATA.products.forEach((p) => grid.appendChild(productCard(p)));
    DATA.bundles.forEach((b) => grid.appendChild(bundleCard(b)));
  }

  /* ---------- filter ---------- */
  function initFilters() {
    const state = { jenis: 'all', daerah: 'all', stok: 'all' };
    const empty = $('#empty');

    function apply() {
      let visible = 0;
      $$('.card').forEach((card) => {
        const okJenis = state.jenis === 'all' || card.getAttribute('data-kategori') === state.jenis;
        const okDaerah = state.daerah === 'all' || card.getAttribute('data-daerah') === state.daerah;
        const okStok = state.stok === 'all' || card.getAttribute('data-status') === state.stok;
        const show = okJenis && okDaerah && okStok;
        card.hidden = !show;
        if (show) visible++;
      });

      // rail ikut menyaring + disembunyikan bila kosong
      $$('.rail').forEach((rail) => {
        const items = $$('.rail__item', rail);
        let n = 0;
        items.forEach((item) => {
          const id = item.getAttribute('data-jump');
          const card = document.getElementById('kartu-' + id);
          const show = card ? !card.hidden : true;
          item.parentElement.hidden = !show;
          if (show) n++;
        });
        rail.hidden = n === 0;
      });

      empty.hidden = visible !== 0;
    }

    $$('.filter').forEach((group) => {
      const key = group.getAttribute('data-filter-group');
      $$('.chip', group).forEach((chip) => {
        chip.addEventListener('click', () => {
          $$('.chip', group).forEach((c) => c.classList.toggle('is-on', c === chip));
          state[key] = chip.getAttribute('data-value');
          apply();
        });
      });
    });

    $$('[data-reset]').forEach((b) => b.addEventListener('click', () => {
      state.jenis = state.daerah = state.stok = 'all';
      $$('.filter').forEach((group) => {
        const chips = $$('.chip', group);
        chips.forEach((c, i) => c.classList.toggle('is-on', i === 0));
      });
      apply();
    }));

    apply();
  }

  /* ---------- langganan ---------- */
  function buildSubs() {
    const host = $('#subs-cards');
    if (!host || !DATA.subscription) return;
    DATA.subscription.options.forEach((o) => {
      const div = document.createElement('div');
      div.className = 'plan';
      div.innerHTML =
        '<div class="plan__top"><h3 class="plan__name">' + o.name + '</h3><span class="plan__comp">' + o.composition + '</span></div>' +
        '<p class="plan__price">' + o.price_note + '</p>' +
        '<p class="plan__note">' + o.note + '</p>' +
        '<a class="btn btn--ink plan__cta" href="#">Mulai paket ini</a>';
      const a = $('a', div);
      a.href = waLink(DATA.brand.whatsapp,
        'Halo Nocturne Koffie! Saya mau mulai langganan:\n— Paket: ' + o.name + ' (' + o.composition + ')\n— Kopi pilihan: ...\n— Nama: ...\n— Alamat kirim: ...\n— Preferensi grind: biji utuh / bubuk\n\nMohon info jadwal & ongkirnya ya. Terima kasih!');
      a.target = '_blank';
      a.rel = 'noopener';
      host.appendChild(div);
    });
  }

  /* ---------- member ---------- */
  function buildMember() {
    const host = $('#member-steps');
    if (!host || !DATA.member) return;
    DATA.member.steps.forEach((s) => {
      const li = document.createElement('li');
      li.innerHTML = '<b>' + s.no + '</b><span>' + s.text + '</span>';
      host.appendChild(li);
    });
    const note = $('#member-note');
    if (note) note.textContent = DATA.member.tiers_note;
  }

  /* ---------- UI kecil ---------- */
  function initUI() {
    const nav = $('#nav');
    const filters = $('#filters');
    const onScroll = () => {
      const y = window.scrollY;
      if (nav) nav.classList.toggle('is-solid', y > 12);
      if (filters) {
        const top = filters.getBoundingClientRect().top;
        filters.classList.toggle('is-stuck', top <= (parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 66) + 2);
      }
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    const burger = $('#burger');
    const menu = $('#mobilemenu');
    const close = $('#mclose');
    const openMenu = (open) => {
      if (!menu) return;
      menu.hidden = !open;
      document.body.classList.toggle('is-locked', open);
      if (burger) {
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        burger.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
      }
      if (open && close) close.focus();
    };
    if (burger) burger.addEventListener('click', () => openMenu(menu.hidden));
    if (close) close.addEventListener('click', () => openMenu(false));
    if (menu) menu.addEventListener('click', (e) => {
      if (e.target.closest('a')) openMenu(false);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && menu && !menu.hidden) openMenu(false);
    });

    const y = $('#year');
    if (y) y.textContent = new Date().getFullYear();
  }

  /* ---------- hash awal ---------- */
  function handleHash() {
    const id = location.hash.replace('#', '');
    if (!id) return;
    const card = document.getElementById('kartu-' + id);
    if (card) window.setTimeout(() => jumpTo(id), 300);
  }

  /* ---------- error state ---------- */
  function fail(err) {
    console.error('[Nocturne] katalog gagal dimuat:', err);
    const grid = $('#grid');
    if (grid) {
      grid.innerHTML = '<p class="empty">Katalog gagal dimuat di browser ini. ' +
        'Silakan pesan langsung lewat <a class="linkbtn" href="https://wa.me/628988188800" target="_blank" rel="noopener">WhatsApp</a> ' +
        'atau buka halaman ini lewat server (bukan file://).</p>';
    }
    const subs = $('#subs-cards');
    if (subs) subs.innerHTML = '<p class="micro micro--light">Daftar paket tidak dapat dimuat. Hubungi kami lewat WhatsApp.</p>';
    window.__nocturneReady = true;
    document.dispatchEvent(new CustomEvent('nocturne:ready'));
  }

  /* ---------- boot ---------- */
  fetch('data/catalog.json', { cache: 'no-cache' })
    .then((r) => {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then((json) => {
      DATA = json;
      hydrateBrand();
      hydrateWaButtons();
      buildMarquee();
      buildRails();
      buildGrid();
      initFilters();
      buildSubs();
      buildMember();
      initUI();
      handleHash();
      document.documentElement.classList.add('is-ready');
      window.__nocturneReady = true;
      document.dispatchEvent(new CustomEvent('nocturne:ready'));
    })
    .catch(fail);
})();
