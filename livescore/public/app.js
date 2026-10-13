// Skor Langsung — frontend tanpa framework.
const DAY = 864e5;
const LIVE_STATUSES = new Set(['LIVE', 'HALF_TIME']);
const STATUS_LABEL = { POSTPONED: 'Ditunda', SUSPENDED: 'Ditangguhkan', CANCELLED: 'Dibatalkan' };

const $ = (sel) => document.querySelector(sel);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const utcKey = (ms) => new Date(ms).toISOString().slice(0, 10);
const keyToMs = (k) => Date.parse(`${k}T00:00:00Z`);
const localKey = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};
const fmtTime = (iso) => new Intl.DateTimeFormat('id-ID', { hour: '2-digit', minute: '2-digit' }).format(new Date(iso));
const fmtClock = (iso) => new Intl.DateTimeFormat('id-ID', { hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(new Date(iso));

const state = {
  date: localKey(),
  today: localKey(),
  tab: 'all',
  query: '',
  matches: new Map(),
  favorites: new Set(JSON.parse(localStorage.getItem('skor.fav') || '[]')),
  warnings: [],
  updatedAt: null,
};
let es = null;

// ---------- Tanggal ----------
function renderDates() {
  const base = keyToMs(state.today);
  const html = [];
  for (let off = -3; off <= 3; off++) {
    const key = utcKey(base + off * DAY);
    const label =
      off === 0 ? 'Hari ini' : off === -1 ? 'Kemarin' : off === 1 ? 'Besok'
        : new Intl.DateTimeFormat('id-ID', { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' }).format(new Date(base + off * DAY));
    html.push(`<button data-date="${key}" class="${key === state.date ? 'active' : ''}">${esc(label)}</button>`);
  }
  $('#dates').innerHTML = html.join('');
}

// ---------- Filter & render ----------
function matchesText(m, q) {
  return `${m.home.name} ${m.away.name} ${m.league.name} ${m.league.country}`.toLowerCase().includes(q);
}

function visibleMatches() {
  const q = state.query.trim().toLowerCase();
  return [...state.matches.values()].filter((m) => {
    if (state.tab === 'live' && !LIVE_STATUSES.has(m.status)) return false;
    if (state.tab === 'fav' && !state.favorites.has(m.id)) return false;
    if (q && !matchesText(m, q)) return false;
    return true;
  });
}

function statusCell(m) {
  switch (m.status) {
    case 'LIVE': return `<span class="live-min">${m.minute ?? ''}'</span>`;
    case 'HALF_TIME': return `<span class="ht">HT</span>`;
    case 'FINISHED': return `<span class="ft">FT</span>`;
    case 'SCHEDULED': case 'TIMED': return `<span class="time">${fmtTime(m.kickoff)}</span>`;
    default: return `<span class="off">${esc(STATUS_LABEL[m.status] || m.status)}</span>`;
  }
}

const scoreOf = (m, side) => (m.score ? m.score[side] : null) ?? '-';

function matchRow(m) {
  const done = m.status === 'FINISHED';
  const hWin = done && m.score && m.score.home > m.score.away;
  const aWin = done && m.score && m.score.away > m.score.home;
  const fav = state.favorites.has(m.id);
  return `
    <div class="match" data-id="${esc(m.id)}">
      <div class="status">${statusCell(m)}</div>
      <div class="teams">
        <div class="team ${done ? 'finished' : ''} ${hWin ? 'win' : ''}"><span class="name">${esc(m.home.name)}</span><span class="sc">${scoreOf(m, 'home')}</span></div>
        <div class="team ${done ? 'finished' : ''} ${aWin ? 'win' : ''}"><span class="name">${esc(m.away.name)}</span><span class="sc">${scoreOf(m, 'away')}</span></div>
      </div>
      <button class="star ${fav ? 'on' : ''}" data-fav="${esc(m.id)}" aria-label="Favorit" title="Tambah ke favorit">${fav ? '★' : '☆'}</button>
    </div>`;
}

function groupByLeague(list) {
  const groups = new Map();
  for (const m of list) {
    const key = m.league.id;
    if (!groups.has(key)) groups.set(key, { league: m.league, matches: [] });
    groups.get(key).matches.push(m);
  }
  const arr = [...groups.values()];
  for (const g of arr) g.matches.sort((a, b) => a.kickoff.localeCompare(b.kickoff));
  // Liga yang sedang ada pertandingan live tampil lebih dulu.
  const liveCount = (g) => g.matches.filter((m) => LIVE_STATUSES.has(m.status)).length;
  return arr.sort((a, b) => liveCount(b) - liveCount(a) || a.league.name.localeCompare(b.league.name));
}

function leagueBlock(g) {
  const flag = g.league.flag ? `<img src="${esc(g.league.flag)}" alt="" width="18" height="12" />` : flagEmoji(g.league.countryCode);
  return `
    <section class="league">
      <div class="league-head"><span class="flag">${flag}</span><span>${esc(g.league.name)}</span><span class="ctry">· ${esc(g.league.country)}</span></div>
      ${g.matches.map(matchRow).join('')}
    </section>`;
}

function flagEmoji(cc) {
  if (!cc || !/^[A-Z]{2}$/.test(cc)) return '🌍';
  return String.fromCodePoint(...[...cc].map((c) => 0x1f1e6 + c.charCodeAt(0) - 65));
}

function render() {
  const all = [...state.matches.values()];
  const live = all.filter((m) => LIVE_STATUSES.has(m.status)).length;
  $('#cntAll').textContent = all.length ? `(${all.length})` : '';
  $('#cntLive').textContent = live ? `(${live})` : '';
  $('#cntFav').textContent = state.favorites.size ? `(${state.favorites.size})` : '';
  document.querySelectorAll('.tab').forEach((t) => t.classList.toggle('active', t.dataset.tab === state.tab));

  const list = visibleMatches();
  const groups = groupByLeague(list);
  $('#list').innerHTML = groups.length
    ? groups.map(leagueBlock).join('')
    : `<p class="empty">${state.tab === 'fav' ? 'Belum ada pertandingan favorit. Tekan ☆ pada pertandingan.' : state.tab === 'live' ? 'Tidak ada pertandingan yang sedang berlangsung.' : 'Tidak ada pertandingan untuk tanggal ini.'}</p>`;

  const liveTxt = live ? ` · ${live} live` : '';
  $('#meta').textContent = `${list.length} pertandingan${liveTxt}${state.updatedAt ? ` · diperbarui ${fmtClock(state.updatedAt)}` : ''}`;

  const warn = $('#warn');
  warn.hidden = !state.warnings.length;
  warn.textContent = state.warnings.length ? `Sebagian data gagal dimuat: ${state.warnings.join('; ')}` : '';
}

// ---------- Data ----------
async function loadDay() {
  const date = state.date;
  try {
    const res = await fetch(`/api/matches?date=${date}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (date !== state.date) return; // tanggal sudah berganti
    state.matches = new Map(data.matches.map((m) => [m.id, m]));
    state.warnings = data.warnings || [];
    state.updatedAt = new Date().toISOString();
    render();
  } catch (err) {
    $('#list').innerHTML = `<p class="empty">Gagal memuat jadwal (${esc(err.message)}). Coba lagi sebentar.</p>`;
  }
}

function connectStream() {
  es?.close();
  es = new EventSource(`/api/stream?date=${state.date}`);
  es.onopen = () => setConn(true);
  es.onerror = () => setConn(false);
  es.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.type !== 'update' || msg.date !== state.date) return;
    for (const m of msg.matches) state.matches.set(m.id, { ...state.matches.get(m.id), ...m });
    state.updatedAt = msg.at;
    render();
    if (openId && msg.matches.some((m) => m.id === openId)) openDetail(openId, true);
  };
}

function setConn(on) {
  $('#conn').classList.toggle('on', on);
  $('#connText').textContent = on ? 'LANGSUNG' : 'Menghubungkan…';
}

function selectDate(date) {
  state.date = date;
  state.matches = new Map();
  state.warnings = [];
  $('#list').innerHTML = '<p class="empty">Memuat pertandingan…</p>';
  renderDates();
  render();
  loadDay();
  connectStream();
}

// ---------- Detail ----------
let openId = null;

const EVENT_ICON = { goal: '⚽', own_goal: '⚽ (gol bunuh diri)', yellow: '🟨', red: '🟥', sub: '🔁' };

function eventText(e) {
  if (e.type === 'sub') return `🔁 <b>${esc(e.playerIn || '')}</b> <span class="muted">↔ ${esc(e.playerOut || '')}</span>`;
  return `${EVENT_ICON[e.type] || '•'} ${esc(e.player || '')}${e.type === 'own_goal' ? ' (OG)' : ''}`;
}

function renderDetail(m) {
  const score = m.score ? `${m.score.home} – ${m.score.away}` : 'vs';
  const ht = m.score?.halfTime ? `HT ${m.score.halfTime.home}–${m.score.halfTime.away}` : '';
  const stateLabel = m.status === 'LIVE' ? `${m.minute}'` : m.status === 'HALF_TIME' ? 'Istirahat' : m.status === 'FINISHED' ? 'Selesai' : m.status === 'SCHEDULED' ? fmtTime(m.kickoff) : (STATUS_LABEL[m.status] || m.status);
  const events = (m.events || []).slice().sort((a, b) => (a.minute ?? 0) - (b.minute ?? 0));
  const rows = events.length
    ? events.map((e) => `
        <li class="ev">
          <div class="l">${e.team === 'home' ? eventText(e) : ''}</div>
          <div class="m">${e.minute ?? ''}'</div>
          <div class="r">${e.team === 'away' ? eventText(e) : ''}</div>
        </li>`).join('')
    : '<p class="muted">Belum ada kejadian pertandingan.</p>';
  return `
    <div class="d-league">${esc(m.league.name)} · ${esc(m.league.country)}</div>
    <div class="d-score">
      <div class="t">${esc(m.home.name)}</div>
      <div><div class="big" id="mTitle">${score}</div><div class="sub">${esc(stateLabel)}${ht ? ` · ${ht}` : ''}</div></div>
      <div class="t">${esc(m.away.name)}</div>
    </div>
    <div class="h3">Kejadian</div>
    <ul class="timeline">${rows}</ul>`;
}

async function openDetail(id, silent = false) {
  openId = id;
  $('#modal').hidden = false;
  if (!silent) $('#modalBody').innerHTML = '<p class="empty">Memuat detail…</p>';
  try {
    const res = await fetch(`/api/matches/${encodeURIComponent(id)}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const m = await res.json();
    if (openId === id) $('#modalBody').innerHTML = renderDetail(m);
  } catch (err) {
    if (openId === id) $('#modalBody').innerHTML = `<p class="empty">Gagal memuat detail: ${esc(err.message)}</p>`;
  }
}

function closeDetail() {
  openId = null;
  $('#modal').hidden = true;
}

// ---------- Event handlers ----------
$('#dates').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-date]');
  if (b && b.dataset.date !== state.date) selectDate(b.dataset.date);
});

document.querySelector('.tabs').addEventListener('click', (e) => {
  const b = e.target.closest('.tab');
  if (!b) return;
  state.tab = b.dataset.tab;
  render();
});

$('#search').addEventListener('input', (e) => {
  state.query = e.target.value;
  render();
});

$('#list').addEventListener('click', (e) => {
  const star = e.target.closest('[data-fav]');
  if (star) {
    const id = star.dataset.fav;
    state.favorites.has(id) ? state.favorites.delete(id) : state.favorites.add(id);
    localStorage.setItem('skor.fav', JSON.stringify([...state.favorites]));
    render();
    return;
  }
  const row = e.target.closest('.match');
  if (row) openDetail(row.dataset.id);
});

$('#closeModal').addEventListener('click', closeDetail);
$('#modal').addEventListener('click', (e) => { if (e.target.id === 'modal') closeDetail(); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeDetail(); });

// ---------- Init ----------
// Muat ulang berkala sebagai cadangan jika SSE terputus.
setInterval(() => { if (document.visibilityState === 'visible') loadDay(); }, 60_000);
// Perbarui tampilan waktu relatif dan hari ini saat tengah malam.
setInterval(() => {
  const t = localKey();
  if (t !== state.today) { state.today = t; renderDates(); render(); }
}, 60_000);

renderDates();
render();
loadDay();
connectStream();
