// Adapter untuk football-data.org (v4). Memerlukan API key gratis:
// set FOOTBALL_DATA_TOKEN. Lihat ketentuan penggunaan penyedia sebelum dipakai.
// Catatan: endpoint detail menyediakan gol/kartu/pergantian; endpoint daftar
// biasanya hanya berisi skor dan status.

export const DEFAULT_BASE = 'https://api.football-data.org/v4';

const FD_STATUS = {
  SCHEDULED: 'SCHEDULED',
  TIMED: 'SCHEDULED',
  IN_PLAY: 'LIVE',
  LIVE: 'LIVE',
  PAUSED: 'HALF_TIME',
  FINISHED: 'FINISHED',
  AWARDED: 'FINISHED',
  POSTPONED: 'POSTPONED',
  SUSPENDED: 'SUSPENDED',
  CANCELLED: 'CANCELLED',
};

const SCORED = new Set(['LIVE', 'HALF_TIME', 'FINISHED']);

/** Ubah payload football-data menjadi model internal. Dipisah agar mudah diuji. */
export function normalizeFdMatch(m) {
  const area = m.competition?.area || {};
  const full = m.score?.fullTime || {};
  const half = m.score?.halfTime || {};
  const status = FD_STATUS[m.status] || 'SCHEDULED';
  const side = (team) => (team?.id === m.homeTeam?.id ? 'home' : 'away');

  const events = [];
  for (const g of m.goals || []) {
    events.push({
      minute: g.minute ?? null,
      type: g.type === 'OWN_GOAL' ? 'own_goal' : 'goal',
      team: side(g.team),
      player: g.scorer?.name ?? null,
    });
  }
  for (const b of m.bookings || []) {
    const red = b.card === 'RED_CARD' || b.card === 'YELLOW_RED_CARD';
    events.push({ minute: b.minute ?? null, type: red ? 'red' : 'yellow', team: side(b.team), player: b.player?.name ?? null });
  }
  for (const s of m.substitutions || []) {
    events.push({
      minute: s.minute ?? null,
      type: 'sub',
      team: side(s.team),
      playerIn: s.playerIn?.name ?? null,
      playerOut: s.playerOut?.name ?? null,
    });
  }
  events.sort((a, b) => (a.minute ?? 0) - (b.minute ?? 0));

  // Saat berlangsung, fullTime kadang kosong sementara halfTime sudah terisi.
  const current = full.home != null ? full : half.home != null ? half : null;
  const hasScore = SCORED.has(status) && current !== null;
  return {
    id: `fd:${m.id}`,
    source: 'footballdata',
    league: {
      id: `fd-${m.competition?.id}`,
      name: m.competition?.name ?? 'Kompetisi',
      country: area.name ?? '',
      countryCode: area.code ?? null,
      flag: area.flag ?? null,
    },
    kickoff: m.utcDate,
    status,
    minute: m.minute ?? null,
    home: { id: `fd-${m.homeTeam?.id}`, name: m.homeTeam?.name ?? 'Tuan rumah', short: m.homeTeam?.tla ?? null },
    away: { id: `fd-${m.awayTeam?.id}`, name: m.awayTeam?.name ?? 'Tamu', short: m.awayTeam?.tla ?? null },
    score: hasScore
      ? {
          home: current.home,
          away: current.away,
          halfTime: half.home !== null && half.home !== undefined ? { home: half.home, away: half.away } : null,
        }
      : null,
    events,
  };
}

export function createFootballDataProvider({
  token,
  base = DEFAULT_BASE,
  fetchImpl = globalThis.fetch,
  ttlMs = 60_000,
  now = () => Date.now(),
}) {
  if (!token) throw new Error('FOOTBALL_DATA_TOKEN belum diatur');
  const cache = new Map();

  async function request(path) {
    const res = await fetchImpl(base + path, { headers: { 'X-Auth-Token': token } });
    if (!res.ok) throw new Error(`football-data ${path} gagal: HTTP ${res.status}`);
    return res.json();
  }

  function cached(key, load) {
    const hit = cache.get(key);
    if (hit && now() - hit.at < ttlMs) return hit.value;
    const value = load();
    cache.set(key, { at: now(), value: value.catch((e) => { cache.delete(key); throw e; }) });
    return cache.get(key).value;
  }

  return {
    name: 'footballdata',
    owns: (id) => id.startsWith('fd:'),
    getMatches(dateKey) {
      return cached(`day:${dateKey}`, async () => {
        const data = await request(`/matches?dateFrom=${dateKey}&dateTo=${dateKey}`);
        return (data.matches || []).map(normalizeFdMatch);
      });
    },
    getMatch(id) {
      const raw = id.slice(3);
      return cached(`match:${raw}`, async () => normalizeFdMatch(await request(`/matches/${encodeURIComponent(raw)}`)));
    },
  };
}
