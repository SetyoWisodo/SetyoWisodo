'use strict';

// Store in-memory dengan antarmuka yang sama seperti mongoStore.js.
// Dipakai untuk test dan untuk menjalankan listener tanpa MongoDB (dry run).

const keyOf = (k) => [k.provider, k.league_slug, k.resource_type, k.resource_key].join('|');

function createMemoryStore() {
  const leagues = new Map();
  const clubs = new Map(); // key: `${provider}|${club_id}` -> doc
  const matches = new Map(); // key: `${slug}|${event_id}` -> doc
  const events = new Map(); // key: `${slug}|${event_id}|${event_key}` -> doc
  const standings = new Map(); // key: `${slug}|${season}|${group}` -> doc
  const syncStates = new Map();
  const leases = new Map();

  return {
    _data: { leagues, clubs, matches, events, standings, syncStates },

    async upsertLeague(slug, doc) {
      leagues.set(slug, { ...doc });
    },
    async getLeague(slug) {
      return leagues.get(slug) || null;
    },
    async upsertClub(slug, doc) {
      const id = `${doc.source.provider}|${doc.source.club_id}`;
      const prev = clubs.get(id);
      const slugs = new Set([...(prev?.league_slugs || []), slug]);
      clubs.set(id, { ...doc, league_slugs: [...slugs] });
    },
    async upsertMatch(slug, doc) {
      matches.set(`${slug}|${doc.source.event_id}`, { ...doc, league_slug: slug });
    },
    async upsertStanding(slug, season, group, doc) {
      standings.set(`${slug}|${season}|${group}`, { ...doc });
    },
    async upsertEvents(docs) {
      for (const d of docs) events.set(`${d.league_slug}|${d.event_id}|${d.source.event_key}`, { ...d });
    },
    async setPlayByPlayAvailable(slug, eventId, value) {
      const m = matches.get(`${slug}|${eventId}`);
      if (m) m.play_by_play_available = value;
    },
    async findMatchesForDetails(slug, fromYmd, toYmd) {
      return [...matches.values()]
        .filter((m) => m.league_slug === slug && m.scoreboard_date >= fromYmd && m.scoreboard_date <= toYmd)
        .filter((m) => ['in', 'post'].includes(m.status.state))
        .map((m) => ({ event_id: m.source.event_id, state: m.status.state, completed: Boolean(m.status.completed) }));
    },
    async syncedPlayKeys(slug) {
      const out = new Set();
      for (const s of syncStates.values()) {
        if (s.league_slug === slug && s.resource_type === 'plays' && s.last_success_at) out.add(s.resource_key);
      }
      return out;
    },
    async acquireLease(key, owner, ttlMs, nowDate) {
      const id = keyOf(key);
      const cur = leases.get(id);
      if (cur && cur.owner !== owner && cur.expires_at > nowDate) return false;
      leases.set(id, { owner, expires_at: new Date(nowDate.getTime() + ttlMs) });
      syncStates.set(id, { ...key, ...(syncStates.get(id) || {}), status: 'polling' });
      return true;
    },
    async releaseLease(key) {
      leases.delete(keyOf(key));
    },
    async recordSync(key, set, inc = {}) {
      const id = keyOf(key);
      const prev = syncStates.get(id) || { ...key, consecutive_errors: 0 };
      const next = { ...prev, ...set };
      for (const [field, delta] of Object.entries(inc)) next[field] = (prev[field] || 0) + delta;
      syncStates.set(id, next);
    },
    _syncState(key) {
      return syncStates.get(keyOf(key));
    },
  };
}

module.exports = { createMemoryStore, keyOf };
