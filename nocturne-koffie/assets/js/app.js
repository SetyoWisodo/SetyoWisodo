/* ============================================================
   Nocturne Koffie — app.js
   - render katalog dari data/catalog.json
   - keranjang (localStorage) -> checkout via WhatsApp
   - filter, reveal, nav, JSON-LD
   Tanpa dependency. Ubah nomor WhatsApp di data/catalog.json.
   ============================================================ */

const WA_FALLBACK = "62812XXXXXXXX"; // dipakai hanya jika catalog.json gagal dimuat
const rupiah = (n) => "Rp " + n.toLocaleString("id-ID");
let CATALOG = null;
let cart = [];

/* ---------- util ---------- */
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

function saveCart() {
  try { localStorage.setItem("nk_cart_v1", JSON.stringify(cart)); } catch (e) {}
}
function loadCart() {
  try {
    const raw = localStorage.getItem("nk_cart_v1");
    cart = raw ? JSON.parse(raw) : [];
  } catch (e) { cart = []; }
  if (!Array.isArray(cart)) cart = [];
}
function waNumber() {
  const n = (CATALOG?.brand?.whatsapp || WA_FALLBACK).replace(/[^0-9]/g, "");
  return n || WA_FALLBACK;
}
function waLink(text) {
  return `https://wa.me/${waNumber()}?text=${encodeURIComponent(text)}`;
}
function openWA(text) {
  window.open(waLink(text), "_blank", "noopener");
}

/* ---------- render produk ---------- */
function productCard(p) {
  const v0 = p.variants[0];
  const opts = p.variants
    .map((v) => `<option value="${v.sku}">${v.weight} — ${rupiah(v.price)}</option>`)
    .join("");
  const grind = p.grind.map((g) => `<option value="${g}">${g}</option>`).join("");
  const notes = p.notes.map((n) => `<span class="note">${n}</span>`).join("");
  return `
    <article class="product reveal" data-category="${p.category}">
      <div class="product-media">
        <img src="${p.img}" alt="Kemasan ${p.name}" loading="lazy" />
        ${p.badge ? `<span class="badge">${p.badge}</span>` : ""}
        <span class="roast-tag">${p.roast}</span>
      </div>
      <div class="product-body">
        <div class="product-name">
          <h3>${p.name}</h3>
          <span class="product-price" data-price>${rupiah(v0.price)}</span>
        </div>
        <p class="product-origin">${p.origin}</p>
        <div class="notes">${notes}</div>
        <p class="product-desc">${p.desc}</p>
        <div class="controls" data-sku="${p.id}">
          <select class="variant" aria-label="Ukuran ${p.name}">${opts}</select>
          <select class="grind" aria-label="Gilingan ${p.name}">${grind}</select>
          <button class="add-btn" data-add="${p.id}">Tambah ke pesanan</button>
        </div>
      </div>
    </article>`;
}

function renderProducts() {
  const grid = $("#productGrid");
  if (!grid || !CATALOG) return;
  grid.innerHTML = CATALOG.products.map(productCard).join("");
  observeReveals();
}

function renderSubs() {
  const box = $("#subCards");
  if (!box || !CATALOG?.subscription) return;
  box.innerHTML = CATALOG.subscription.options
    .map(
      (o) => `
      <button class="sub-card" data-sub="${encodeURIComponent(o.label)}|${o.price}">
        <div>
          <strong>${o.label}</strong>
          <span>${o.save}</span>
        </div>
        <span class="sub-price">${rupiah(o.price)}</span>
      </button>`
    )
    .join("");
}

/* ---------- filter ---------- */
function bindFilters() {
  const wrap = $("#filters");
  if (!wrap) return;
  wrap.addEventListener("click", (e) => {
    const btn = e.target.closest(".chip");
    if (!btn) return;
    $$(".chip", wrap).forEach((c) => c.classList.toggle("is-active", c === btn));
    const f = btn.dataset.filter;
    $$(".product").forEach((card) => {
      const show = f === "all" || card.dataset.category === f;
      card.style.display = show ? "" : "none";
    });
  });
}

/* ---------- keranjang ---------- */
function addToCart(id, sku, grind) {
  const p = CATALOG.products.find((x) => x.id === id);
  if (!p) return;
  const variant = p.variants.find((v) => v.sku === sku) || p.variants[0];
  const key = `${p.id}::${variant.sku}::${grind}`;
  const found = cart.find((c) => c.key === key);
  if (found) found.qty += 1;
  else
    cart.push({
      key,
      productId: p.id,
      name: p.name,
      weight: variant.weight,
      grind,
      price: variant.price,
      sku: variant.sku,
      img: p.img,
      qty: 1,
    });
  saveCart();
  renderCart();
  flashAdded(id);
}
function flashAdded(id) {
  const btn = $(`[data-add="${id}"]`);
  if (!btn) return;
  const original = btn.textContent;
  btn.textContent = "Ditambahkan ✓";
  btn.classList.add("is-added");
  setTimeout(() => {
    btn.textContent = original;
    btn.classList.remove("is-added");
  }, 1400);
}
function changeQty(key, delta) {
  const item = cart.find((c) => c.key === key);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) cart = cart.filter((c) => c.key !== key);
  saveCart();
  renderCart();
}
function removeItem(key) {
  cart = cart.filter((c) => c.key !== key);
  saveCart();
  renderCart();
}
const cartTotal = () => cart.reduce((s, c) => s + c.price * c.qty, 0);
const cartCount = () => cart.reduce((s, c) => s + c.qty, 0);

function renderCart() {
  const count = cartCount();
  [$("#cartCount"), $("#fabCount")].forEach((el) => {
    if (!el) return;
    el.textContent = count;
    el.hidden = count === 0;
  });
  const body = $("#cartBody");
  const totalEl = $("#cartTotal");
  const checkout = $("#checkout");
  if (!body) return;

  if (!cart.length) {
    body.innerHTML = `<p class="empty">Keranjang masih kosong.<br />Pilih kopi dulu, lalu kembali ke sini.</p>`;
    if (totalEl) totalEl.textContent = rupiah(0);
    if (checkout) checkout.disabled = true;
    return;
  }
  if (checkout) checkout.disabled = false;
  body.innerHTML = cart
    .map(
      (c) => `
      <div class="cart-item">
        <img src="${c.img}" alt="" loading="lazy" />
        <div class="cart-item-main">
          <strong>${c.name}</strong>
          <span>${c.weight} · ${c.grind}</span>
          <div class="qty">
            <button data-qty="-1" data-key="${c.key}" aria-label="Kurangi">−</button>
            <span>${c.qty}</span>
            <button data-qty="1" data-key="${c.key}" aria-label="Tambah">+</button>
          </div>
        </div>
        <div class="cart-item-side">
          <strong>${rupiah(c.price * c.qty)}</strong>
          <button class="remove" data-remove="${c.key}">Hapus</button>
        </div>
      </div>`
    )
    .join("");
  if (totalEl) totalEl.textContent = rupiah(cartTotal());
}

function checkoutMessage() {
  const note = ($("#cartNote")?.value || "").trim();
  const lines = [
    "*Pesanan Nocturne Koffie*",
    "",
    ...cart.map(
      (c) => `• ${c.name} — ${c.weight} (${c.grind}) × ${c.qty} = ${rupiah(c.price * c.qty)}`
    ),
    "",
    `Subtotal: *${rupiah(cartTotal())}*`,
    "(belum termasuk ongkir)",
  ];
  if (note) lines.push("", `Nama & alamat: ${note}`);
  lines.push("", "Mohon konfirmasi stok, ongkir, dan cara pembayaran. Terima kasih!");
  return lines.join("\n");
}

/* ---------- event global ---------- */
function bindCartEvents() {
  document.addEventListener("click", (e) => {
    const add = e.target.closest("[data-add]");
    if (add) {
      const wrap = add.closest(".controls");
      addToCart(add.dataset.add, $(".variant", wrap).value, $(".grind", wrap).value);
      return;
    }
    const qty = e.target.closest("[data-qty]");
    if (qty) { changeQty(qty.dataset.key, Number(qty.dataset.qty)); return; }
    const rem = e.target.closest("[data-remove]");
    if (rem) { removeItem(rem.dataset.remove); return; }
    const sub = e.target.closest("[data-sub]");
    if (sub) {
      const [label, price] = decodeURIComponent(sub.dataset.sub).split("|");
      openWA(
        `*Langganan Nocturne Koffie*\n\nPaket: ${label}\nHarga: ${rupiah(
          Number(price)
        )}/bulan\n\nSaya ingin mulai langganan. Mohon info tanggal kirim dan cara pembayaran.`
      );
      return;
    }
  });

  // harga ikut berubah saat varian diganti
  document.addEventListener("change", (e) => {
    if (!e.target.classList.contains("variant")) return;
    const wrap = e.target.closest(".controls");
    const id = wrap.dataset.sku;
    const p = CATALOG.products.find((x) => x.id === id);
    const v = p?.variants.find((x) => x.sku === e.target.value);
    if (v) {
      const priceEl = wrap.closest(".product-body").querySelector("[data-price]");
      if (priceEl) priceEl.textContent = rupiah(v.price);
    }
  });

  const open = () => { $("#cartModal").hidden = false; document.body.style.overflow = "hidden"; };
  const close = () => { $("#cartModal").hidden = true; document.body.style.overflow = ""; };
  $("#cartOpen")?.addEventListener("click", open);
  $("#fab")?.addEventListener("click", open);
  $$("[data-close]").forEach((el) => el.addEventListener("click", close));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });

  $("#checkout")?.addEventListener("click", () => {
    if (!cart.length) return;
    openWA(checkoutMessage());
  });
}

/* ---------- nav + reveal ---------- */
function bindNav() {
  const nav = $("#nav");
  const fab = $("#fab");
  const onScroll = () => {
    nav?.classList.toggle("is-stuck", window.scrollY > 24);
    fab?.classList.toggle("is-visible", window.scrollY > window.innerHeight * 0.7);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

let io = null;
function observeReveals() {
  if (!("IntersectionObserver" in window)) {
    $$(".reveal").forEach((el) => el.classList.add("is-in"));
    return;
  }
  if (!io) {
    io = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
  }
  $$(".reveal").forEach((el) => io.observe(el));
}

/* ---------- brand link & SEO ---------- */
function hydrateBrand() {
  const b = CATALOG?.brand || {};
  const wa = b.whatsapp ? `https://wa.me/${b.whatsapp.replace(/[^0-9]/g, "")}` : "#";
  const intro = "Halo Nocturne Koffie, saya ingin tanya soal kopinya.";
  const grosir =
    "Halo Nocturne Koffie, saya ingin daftar harga grosir untuk kafe/kantor. Boleh dikirim?";
  const set = (id, href, text) => {
    const el = document.getElementById(id);
    if (!el) return;
    if (href) el.href = href;
    if (text) el.textContent = text;
  };
  set("waHero", `${wa}?text=${encodeURIComponent(intro)}`);
  set("waCta", `${wa}?text=${encodeURIComponent(intro)}`);
  set("waGrosir", `${wa}?text=${encodeURIComponent(grosir)}`);
  set("footerWa", wa);
  set("footerIg", b.instagram || "#");
  set("footerTt", b.tiktok || "#");
  if (b.city) $("#footerAddr").textContent = `${b.city} · Sangrai per batch`;
  const yearEl = $("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  const ld = $("#ldjson");
  if (ld) {
    ld.textContent = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      name: b.name || "Nocturne Koffie",
      description: "Roastery kopi kecil di Banyuwangi. Sangrai per batch dengan QC cupping.",
      address: { "@type": "PostalAddress", addressLocality: "Banyuwangi", addressRegion: "Jawa Timur", addressCountry: "ID" },
      telephone: b.whatsapp ? `+${b.whatsapp.replace(/[^0-9]/g, "")}` : undefined,
      sameAs: [b.instagram].filter(Boolean),
      priceRange: "Rp 65.000 – Rp 330.000",
    });
  }
  document.title = `${b.name || "Nocturne Koffie"} — Roastery kopi Banyuwangi | ${b.tagline || "Kopi untuk jam setelah gelap"}`;
}

/* ---------- init ---------- */
async function init() {
  bindNav();
  bindCartEvents();
  loadCart();
  try {
    const res = await fetch("data/catalog.json", { cache: "no-cache" });
    if (!res.ok) throw new Error("catalog gagal dimuat");
    CATALOG = await res.json();
  } catch (err) {
    console.warn("[nocturne] catalog.json tidak bisa dibaca:", err);
    $("#productGrid").innerHTML =
      `<p class="empty">Katalog sedang tidak bisa dimuat. Silakan pesan langsung lewat WhatsApp.</p>`;
    hydrateBrand();
    renderCart();
    return;
  }
  hydrateBrand();
  renderProducts();
  renderSubs();
  bindFilters();
  renderCart();
  observeReveals();
}

document.addEventListener("DOMContentLoaded", init);
