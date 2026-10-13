'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const of = require('../listener/openfootball');
const { seedSeason, loadSeasonFile, parseArgs } = require('../listener/seedOpenfootball');
const { createMemoryStore } = require('../listener/memoryStore');
const { LEAGUES } = require('../listener/leagues');

const NOW = new Date('2026-10-13T12:00:00Z');
const EPL = LEAGUES['eng.1'];
const LA_LIGA = LEAGUES['esp.1'];

const FT_MATCH = {
  round: 'Regular Season - 1',
  date: '2025-08-15',
  time: '19:00 UTC+0',
  team1: 'Liverpool',
  team2: 'Bournemouth',
  score: { ht: [1, 0], ft: [4, 2] },
  goals1: [{ name: 'Hugo EKITIKE', minute: '37' }, { name: 'Cody GAKPO', minute: '49' }, { name: 'Federico Chiesa', minute: '88' }, { name: 'MOHAMED SALAH', minute: '90+4' }],
  goals2: [{ name: 'Antoine SEMENYO', minute: '64' }, { name: 'Antoine SEMENYO', minute: '76' }],
  bookings: [[{ type: 'Y', name: 'Milos KERKEZ', minute: '43' }], [{ type: 'Y', name: 'David BROOKS', minute: '14' }, { type: 'Y/R', name: 'Evanilson', minute: '81' }]],
  ground: 'Anfield, Liverpool',
  attendance: 60315,
};

test('parseKickoff: zona eksplisit UTC+0 dipakai apa adanya', () => {
  const r = of.parseKickoff('2025-08-15', '19:00 UTC+0', 'Europe/London');
  assert.equal(new Date(r.utcMs).toISOString(), '2025-08-15T19:00:00.000Z');
  assert.equal(r.timeKnown, true);
});

test('parseKickoff: jam tanpa zona dihitung dari zona liga, termasuk perbedaan musim panas dan dingin', () => {
  // London memakai BST (+1) pada Agustus.
  assert.equal(new Date(of.parseKickoff('2025-08-16', '15:00', 'Europe/London').utcMs).toISOString(), '2025-08-16T14:00:00.000Z');
  // Madrid memakai CEST (+2) pada Agustus, CET (+1) pada Januari.
  assert.equal(new Date(of.parseKickoff('2025-08-16', '21:00', 'Europe/Madrid').utcMs).toISOString(), '2025-08-16T19:00:00.000Z');
  assert.equal(new Date(of.parseKickoff('2026-01-10', '21:00', 'Europe/Madrid').utcMs).toISOString(), '2026-01-10T20:00:00.000Z');
});

test('parseKickoff: tanpa jam dan jam tidak valid ditandai timeKnown=false', () => {
  const none = of.parseKickoff('2025-08-16', undefined, 'Europe/Madrid');
  assert.equal(none.timeKnown, false);
  assert.equal(new Date(none.utcMs).toISOString(), '2025-08-16T00:00:00.000Z');
  assert.equal(of.parseKickoff('2025-08-16', '25:99', 'Europe/Madrid').timeKnown, false);
  assert.throws(() => of.parseKickoff('16/08/2025', '19:00', 'Europe/Madrid'), /tanggal tidak valid/);
});

test('parseMinute: menit biasa dan tambahan waktu', () => {
  assert.deepEqual(of.parseMinute('37'), { minute: 37, injury: 0 });
  assert.deepEqual(of.parseMinute('90+4'), { minute: 90, injury: 4 });
  assert.equal(of.parseMinute('abc'), null);
});

test('fullTimeOf: menerima bentuk {ft} dan array, menolak skor tanpa ft', () => {
  assert.deepEqual(of.fullTimeOf({ ht: [0, 0], ft: [1, 2] }), [1, 2]);
  assert.deepEqual(of.fullTimeOf([0, 0]), [0, 0]);
  assert.equal(of.fullTimeOf({ ht: [1, 0] }), null);
  assert.equal(of.fullTimeOf(null), null);
});

test('mapOpenfootballMatch: pertandingan selesai menghasilkan skor, pemenang, dan kejadian', () => {
  const r = of.mapOpenfootballMatch(FT_MATCH, { leagueSlug: 'eng.1', leagueName: EPL.name, seasonYear: 2025, tz: 'Europe/London', now: NOW });
  const { match, events } = r;
  assert.equal(match.status.state, 'post');
  assert.equal(match.status.completed, true);
  assert.equal(match.home.score, 4);
  assert.equal(match.away.score, 2);
  assert.equal(match.home.winner, true);
  assert.equal(match.away.winner, false);
  assert.equal(match.scoreboard_date, '20250815');
  assert.equal(match.source.provider, 'openfootball');
  assert.equal(match.attendance, 60315);
  assert.equal(match.play_by_play_available, true);

  // 4 + 2 gol, 2 kartu kuning, 1 kartu merah dari kuning kedua.
  assert.equal(events.length, 9);
  const types = events.map((e) => e.event_type.name);
  assert.equal(types.filter((t) => t === 'goal').length, 6);
  assert.equal(types.filter((t) => t === 'yellow-card').length, 2);
  assert.equal(types.filter((t) => t === 'red-card').length, 1);
  const injury = events.find((e) => e.text === 'Goal! MOHAMED SALAH');
  assert.equal(injury.clock.value, 90 * 60, 'menit 90+4 disimpan sebagai menit 90 ditambah tambahan waktu');
  assert.equal(injury.clock.added_value, 4 * 60);
  assert.equal(injury.clock.display_value, "90'+4");
  assert.ok(events.every((e) => e.source.provider === 'openfootball'));
  assert.equal(new Set(events.map((e) => e.source.event_key)).size, events.length);
});

test('mapOpenfootballMatch: event_key dan event_id stabil saat dipetakan ulang', () => {
  const ctx = { leagueSlug: 'eng.1', leagueName: EPL.name, seasonYear: 2025, tz: 'Europe/London', now: NOW };
  const a = of.mapOpenfootballMatch(FT_MATCH, ctx);
  const b = of.mapOpenfootballMatch(FT_MATCH, ctx);
  assert.equal(a.match.source.event_id, b.match.source.event_id);
  assert.deepEqual(a.events.map((e) => e.source.event_key), b.events.map((e) => e.source.event_key));
});

test('mapOpenfootballMatch: postponed tanpa skor tetap masuk, jadwal tanpa skor dilewati', () => {
  const ctx = { leagueSlug: 'eng.1', leagueName: EPL.name, seasonYear: 2025, tz: 'Europe/London', now: NOW };
  const postponed = of.mapOpenfootballMatch({ date: '2025-10-01', team1: 'A FC', team2: 'B FC', score: null, status: 'postponed' }, ctx);
  assert.equal(postponed.match.status.name, 'STATUS_POSTPONED');
  assert.equal(postponed.match.home.score, undefined);
  assert.equal(postponed.match.status.completed, false);

  assert.equal(of.mapOpenfootballMatch({ date: '2026-03-01', team1: 'A FC', team2: 'B FC', score: null }, ctx), null);
});

test('mapOpenfootballMatch: pertandingan tanpa jam diberi catatan, play_by_play tidak diklaim tanpa kejadian', () => {
  const ctx = { leagueSlug: 'esp.1', leagueName: LA_LIGA.name, seasonYear: 2025, tz: 'Europe/Madrid', now: NOW };
  const r = of.mapOpenfootballMatch({ date: '2025-09-01', team1: 'Girona FC', team2: 'Rayo Vallecano de Madrid', score: [1, 3] }, ctx);
  assert.equal(r.timeKnown, false);
  assert.match(r.match.note, /tidak tersedia/);
  assert.equal(r.match.play_by_play_available, false);
  assert.equal(r.match.home.score, 1);
  assert.equal(r.match.away.winner, true);
});

test('seedSeason: menulis pertandingan dan kejadian, dan aman dijalankan ulang', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'of-'));
  fs.mkdirSync(path.join(dir, '2025-26'));
  fs.writeFileSync(path.join(dir, '2025-26', 'en.1-full.json'), JSON.stringify({ name: 'EPL', matches: [FT_MATCH] }));
  const store = createMemoryStore();
  await store.upsertLeague('eng.1', { season: { year: 2026 } });

  const first = await seedSeason({ store, def: EPL, season: '2025-26', dir, now: NOW });
  assert.equal(first.mapped, 1);
  assert.equal(first.events, 9);
  assert.match(first.file, /en\.1-full\.json/);
  assert.equal(store._data.matches.size, 1);
  assert.equal(store._data.events.size, 9);

  await seedSeason({ store, def: EPL, season: '2025-26', dir, now: NOW });
  assert.equal(store._data.matches.size, 1, 'seed ulang tidak menggandakan pertandingan');
  assert.equal(store._data.events.size, 9, 'seed ulang tidak menggandakan kejadian');
});

test('seedSeason: menolak musim aktif, musim belum selesai, dan liga tanpa katalog', async () => {
  const store = createMemoryStore();
  await assert.rejects(seedSeason({ store, def: EPL, season: '2025-26', dir: '/x', now: NOW }), /belum punya musim aktif/);

  await store.upsertLeague('eng.1', { season: { year: 2026 } });
  await assert.rejects(seedSeason({ store, def: EPL, season: '2026-27', dir: '/x', now: NOW }), /musim aktif/);
  await assert.rejects(seedSeason({ store, def: EPL, season: '2025-27', dir: '/x', now: NOW }), /format musim/);
});

test('seedSeason: musim lampau dari remote memakai fetch, lalu fallback ke file biasa saat -full tidak ada', async () => {
  const store = createMemoryStore();
  await store.upsertLeague('esp.1', { season: { year: 2026 } });
  const requested = [];
  const fetchImpl = async (url) => {
    requested.push(url);
    if (url.endsWith('es.1-full.json')) return { ok: false, status: 404, text: async () => '' };
    return {
      ok: true,
      status: 200,
      text: async () => JSON.stringify({ name: 'La Liga', matches: [{ date: '2025-08-16', time: '21:00', team1: 'Girona FC', team2: 'Rayo Vallecano', score: { ft: [1, 3] } }] }),
    };
  };
  const r = await seedSeason({ store, def: LA_LIGA, season: '2025-26', fetchImpl, now: NOW });
  assert.deepEqual(requested, [
    'https://raw.githubusercontent.com/openfootball/football.json/master/2025-26/es.1-full.json',
    'https://raw.githubusercontent.com/openfootball/football.json/master/2025-26/es.1.json',
  ]);
  assert.equal(r.mapped, 1);
  assert.equal(r.events, 0);
});

test('loadSeasonFile: mengembalikan null jika tidak ada file', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'of-empty-'));
  assert.equal(await loadSeasonFile({ dir, season: '2025-26', code: 'en.1' }), null);
});

test('regresi: query detail football-data tidak mengambil pertandingan seed', async () => {
  const store = createMemoryStore();
  await store.upsertMatch('eng.1', of.mapOpenfootballMatch(FT_MATCH, { leagueSlug: 'eng.1', leagueName: EPL.name, seasonYear: 2025, tz: 'Europe/London', now: NOW }).match);
  const rows = await store.findMatchesForDetails('eng.1', '20250101', '20991231');
  assert.equal(rows.length, 0, 'pertandingan openfootball tidak boleh masuk antrean detail football-data');
});

test('parseArgs: membaca flag dan menolak argumen tanpa nilai', () => {
  assert.deepEqual(parseArgs(['--season', '2025-26', '--leagues', 'eng.1']), { season: '2025-26', leagues: 'eng.1' });
  assert.throws(() => parseArgs(['--season']), /butuh nilai/);
  assert.throws(() => parseArgs(['season', '2025-26']), /tidak dikenal/);
});
