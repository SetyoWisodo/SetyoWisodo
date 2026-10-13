'use strict';

// Orkestrasi listener: mengambil data dari client, memvalidasi, lalu menulis
// lewat store. Store bisa berupa MongoDB (mongoStore.js) atau in-memory (test).
//
// Aturan (LIVE-LISTENER-DATABASE.md, "ترتیب امن listener"):
// - setiap resource diambil dengan lease agar tidak ada dua proses yang bekerja bersamaan;
// - data hanya ditulis setelah respons tervalidasi;
// - jika sumber gagal, dokumen valid sebelumnya dipertahankan dan hanya sync state yang berubah.

const mapper = require('./mapper');

const dayKey = (date) => mapper.ymd(date);
const isoDay = (date) => date.toISOString().slice(0, 10);
const addDays = (date, n) => new Date(date.getTime() + n * 86400000);

function createSyncer({
  client,
  store,
  leagues,
  owner = `listener-${process.pid}`,
  now = () => new Date(),
  log = console,
  matchWindowDays = 1,
  lookaheadDays = 7,
  detailsPerCycle = 5,
  leaseMs = 120000,
  retryAfterMs = 60000,
}) {
  const seasonYears = new Map(); // slug -> tahun musim aktif (dari katalog)

  async function guarded(def, resource, resourceKey, task) {
    const key = { provider: mapper.PROVIDER, league_slug: def.slug, resource_type: resource, resource_key: resourceKey };
    const at = now();
    const leased = await store.acquireLease(key, owner, leaseMs, at);
    if (!leased) return { status: 'skipped', reason: 'lease dipegang proses lain' };
    try {
      const result = await task();
      await store.recordSync(key, {
        status: 'healthy',
        last_polled_at: at,
        last_success_at: now(),
        next_poll_at: null,
        consecutive_errors: 0,
        error: { code: '', message: '', occurred_at: null },
        ...(result.cursor ? { cursor: result.cursor } : {}),
      });
      return { status: 'ok', ...result.summary };
    } catch (err) {
      log.warn(`[listener] ${def.slug} ${resource}: ${err.message}`);
      await store.recordSync(
        key,
        {
          status: 'error',
          last_polled_at: at,
          next_poll_at: new Date(now().getTime() + retryAfterMs),
          error: { code: String(err.status || 'ERROR'), message: err.message.slice(0, 300), occurred_at: now() },
        },
        { consecutive_errors: 1 }
      );
      return { status: 'error', error: err.message };
    } finally {
      await store.releaseLease(key);
    }
  }

  async function syncCatalog(def) {
    return guarded(def, 'clubs', 'catalog', async () => {
      const competition = await client.competition(def.fd.code);
      const doc = mapper.mapLeague(def, competition);
      if (doc.season?.year) seasonYears.set(def.slug, doc.season.year);
      await store.upsertLeague(def.slug, doc);
      return { summary: { season: doc.season?.year ?? null } };
    });
  }

  async function syncClubs(def) {
    return guarded(def, 'clubs', 'all', async () => {
      const data = await client.teams(def.fd.code);
      if (!Array.isArray(data?.teams) || data.teams.length === 0) {
        throw new Error('daftar tim kosong atau tidak valid');
      }
      const at = now();
      for (const team of data.teams) {
        await store.upsertClub(def.slug, mapper.mapClub(team, def, at));
      }
      return { summary: { clubs: data.teams.length } };
    });
  }

  async function syncStandings(def) {
    return guarded(def, 'standings', 'overall', async () => {
      const season = await seasonYear(def);
      const payload = await client.standings(def.fd.code);
      const doc = mapper.mapStandings(payload, def, season, now());
      if (!doc) throw new Error('klasemen kosong atau tidak valid');
      await store.upsertStanding(def.slug, season, 'overall', doc);
      return { summary: { entries: doc.entries.length } };
    });
  }

  async function syncScoreboard(def) {
    return guarded(def, 'scoreboard', 'window', async () => {
      const today = now();
      const from = isoDay(addDays(today, -matchWindowDays));
      const to = isoDay(addDays(today, lookaheadDays));
      const data = await client.matches(def.fd.code, from, to);
      if (!Array.isArray(data?.matches)) throw new Error('respons pertandingan tidak valid');
      const at = now();
      for (const match of data.matches) {
        await store.upsertMatch(def.slug, mapper.mapMatch(match, def, at));
      }
      return { summary: { matches: data.matches.length }, cursor: { from, to, count: data.matches.length } };
    });
  }

  // Detail (kejadian) diambil untuk pertandingan yang sedang berlangsung
  // dan untuk pertandingan selesai yang belum pernah diambil.
  async function syncDetails(def) {
    const today = now();
    const from = dayKey(addDays(today, -matchWindowDays));
    const to = dayKey(addDays(today, 0));
    const candidates = await store.findMatchesForDetails(def.slug, from, to);
    const synced = await store.syncedPlayKeys(def.slug);
    const queue = candidates
      .filter((m) => m.state === 'in' || (m.completed && !synced.has(m.event_id)))
      // Pertandingan live diprioritaskan.
      .sort((a, b) => (b.state === 'in') - (a.state === 'in'))
      .slice(0, detailsPerCycle);

    let ok = 0;
    let failed = 0;
    for (const m of queue) {
      const key = { provider: mapper.PROVIDER, league_slug: def.slug, resource_type: 'plays', resource_key: m.event_id };
      const leased = await store.acquireLease(key, owner, leaseMs, now());
      if (!leased) continue;
      try {
        const detail = await client.match(m.event_id);
        const events = mapper.mapEvents(detail, def, now());
        await store.upsertEvents(events);
        await store.setPlayByPlayAvailable(def.slug, m.event_id, true);
        await store.recordSync(key, {
          status: 'healthy',
          last_polled_at: now(),
          last_success_at: now(),
          consecutive_errors: 0,
          error: { code: '', message: '', occurred_at: null },
          cursor: { last_event_key: events.at(-1)?.source.event_key ?? null, count: events.length },
        });
        ok++;
      } catch (err) {
        failed++;
        log.warn(`[listener] ${def.slug} plays ${m.event_id}: ${err.message}`);
        await store.recordSync(
          key,
          {
            status: 'error',
            last_polled_at: now(),
            error: { code: String(err.status || 'ERROR'), message: err.message.slice(0, 300), occurred_at: now() },
          },
          { consecutive_errors: 1 }
        );
      } finally {
        await store.releaseLease(key);
      }
    }
    return { status: failed && !ok ? 'error' : 'ok', fetched: ok, failed, candidates: candidates.length };
  }

  async function seasonYear(def) {
    if (seasonYears.has(def.slug)) return seasonYears.get(def.slug);
    const stored = await store.getLeague(def.slug);
    const year = stored?.season?.year;
    if (year) seasonYears.set(def.slug, year);
    return year ?? new Date().getUTCFullYear();
  }

  return {
    leagues,
    syncCatalog,
    syncClubs,
    syncStandings,
    syncScoreboard,
    syncDetails,
  };
}

module.exports = { createSyncer };
