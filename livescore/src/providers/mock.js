// Provider mock: jadwal, status, dan skor disimulasikan secara deterministik
// berdasarkan waktu sekarang. Cocok untuk pengembangan dan demo tanpa API key.
import { LEAGUES, LEAGUE_BY_ID } from '../catalog.js';
import { dateKeyToMs, hash32, rng, shuffle } from '../util.js';

export const PHASE = { HALF: 45, BREAK: 15, TOTAL: 105 }; // menit

const SURNAMES = [
  'Silva', 'Santos', 'Rahman', 'Kim', 'Tanaka', 'Garcia', 'Müller', 'Dubois', 'Rossi', 'Smith',
  'Pratama', 'Saputra', 'Hernandez', 'Okafor', 'Yilmaz', 'Novak', 'Haddad', 'Ito', 'Costa', 'Jensen',
  'Park', 'Nguyen', 'Lopez', 'Bakr', 'Fernandes', 'Mendes', 'Wijaya', 'Hidayat',
];

const pick = (r) => SURNAMES[Math.floor(r() * SURNAMES.length)];

/** Fase pertandingan pada waktu tertentu. */
export function phaseAt(kickoffMs, nowMs) {
  const { HALF, BREAK, TOTAL } = PHASE;
  const e = (nowMs - kickoffMs) / 60000;
  if (e < 0) return { status: 'SCHEDULED', minute: null, played: null };
  if (e < HALF) {
    const m = Math.floor(e) + 1;
    return { status: 'LIVE', minute: m, played: m };
  }
  if (e < HALF + BREAK) return { status: 'HALF_TIME', minute: HALF, played: HALF };
  if (e < TOTAL) {
    const m = Math.floor(e - BREAK) + 1;
    return { status: 'LIVE', minute: m, played: m };
  }
  return { status: 'FINISHED', minute: 90, played: 90 };
}

/** Kejadian pertandingan (gol, kartu, pergantian) yang sudah ditentukan dari seed. */
export function buildEvents(seed) {
  const r = rng(seed);
  const events = [];
  const goals = Math.floor(r() * r() * 6.5); // skew ke skor rendah
  for (let g = 0; g < goals; g++) {
    events.push({ minute: 1 + Math.floor(r() * 90), type: 'goal', team: r() < 0.5 ? 'home' : 'away', player: pick(r) });
  }
  const yellows = Math.floor(r() * 6);
  for (let y = 0; y < yellows; y++) {
    events.push({ minute: 1 + Math.floor(r() * 90), type: 'yellow', team: r() < 0.5 ? 'home' : 'away', player: pick(r) });
  }
  if (r() < 0.12) {
    events.push({ minute: 1 + Math.floor(r() * 90), type: 'red', team: r() < 0.5 ? 'home' : 'away', player: pick(r) });
  }
  for (const team of ['home', 'away']) {
    const subs = 2 + Math.floor(r() * 2);
    for (let s = 0; s < subs; s++) {
      events.push({ minute: 46 + Math.floor(r() * 40), type: 'sub', team, playerIn: pick(r), playerOut: pick(r) });
    }
  }
  return events.sort((a, b) => a.minute - b.minute);
}

function buildMatch(league, dateKey, idx, home, away, kickoffMs, nowMs) {
  const events = buildEvents(`${league.id}|${dateKey}|${idx}|events`);
  const ph = phaseAt(kickoffMs, nowMs);
  const played = ph.played;

  let score = null;
  let visible = [];
  if (played !== null) {
    visible = events.filter((e) => e.minute <= played);
    const count = (side, upto) =>
      visible.filter((e) => e.type === 'goal' && e.team === side && e.minute <= upto).length;
    score = {
      home: count('home', played),
      away: count('away', played),
      halfTime: played >= PHASE.HALF ? { home: count('home', PHASE.HALF), away: count('away', PHASE.HALF) } : null,
    };
  }

  return {
    id: `mock:${league.id}:${dateKey}:${idx}`,
    source: 'mock',
    league: { id: league.id, name: league.name, country: league.country, countryCode: league.countryCode },
    kickoff: new Date(kickoffMs).toISOString(),
    status: ph.status,
    minute: ph.minute,
    home: { id: home.id, name: home.name, short: home.short },
    away: { id: away.id, name: away.name, short: away.short },
    score,
    events: visible,
  };
}

/** Semua pertandingan mock pada tanggal (UTC, "YYYY-MM-DD"). */
export function mockMatchesForDate(dateKey, nowMs = Date.now()) {
  const dayStart = dateKeyToMs(dateKey);
  const matches = [];
  for (const league of LEAGUES) {
    // Setiap liga bermain sekitar 3 hari dalam seminggu.
    if (hash32(`${league.id}|${dateKey}|day`) % 7 >= 3) continue;
    const teams = shuffle(league.teams, rng(`${league.id}|${dateKey}|fixtures`));
    const pairs = Math.floor(teams.length / 2);
    for (let i = 0; i < pairs; i++) {
      const slot = league.slots[hash32(`${league.id}|${dateKey}|${i}|slot`) % league.slots.length];
      const kickoff = dayStart + Math.round(slot * 3600000);
      matches.push(buildMatch(league, dateKey, i, teams[2 * i], teams[2 * i + 1], kickoff, nowMs));
    }
  }
  return matches.sort((a, b) => a.kickoff.localeCompare(b.kickoff) || a.id.localeCompare(b.id));
}

const ID_RE = /^mock:([^:]+):(\d{4}-\d{2}-\d{2}):(\d+)$/;

/** Ambil satu pertandingan mock berdasarkan id. */
export function mockMatchById(id, nowMs = Date.now()) {
  const m = ID_RE.exec(id);
  if (!m || !LEAGUE_BY_ID.has(m[1])) return null;
  return mockMatchesForDate(m[2], nowMs).find((x) => x.id === id) || null;
}

export function createMockProvider() {
  return {
    name: 'mock',
    owns: (id) => id.startsWith('mock:'),
    async getMatches(dateKey, { now } = {}) {
      return mockMatchesForDate(dateKey, now ?? Date.now());
    },
    async getMatch(id, { now } = {}) {
      return mockMatchById(id, now ?? Date.now());
    },
  };
}
