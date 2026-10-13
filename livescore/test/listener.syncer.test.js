'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { createSyncer } = require('../listener/syncer');
const { createMemoryStore } = require('../listener/memoryStore');
const F = require('./listener.fixtures');

const NOW = new Date('2026-10-13T12:00:00Z');
const silentLog = { warn() {}, error() {}, info() {} };

// Client palsu: data bisa diubah per test, dan panggilan dicatat.
function fakeClient(overrides = {}) {
  const calls = [];
  const wrap = (name, value) => async (...args) => {
    calls.push([name, ...args]);
    const v = typeof value === 'function' ? value(...args) : value;
    if (v instanceof Error) throw v;
    return v;
  };
  return {
    calls,
    competition: wrap('competition', overrides.competition ?? F.COMPETITION),
    teams: wrap('teams', overrides.teams ?? F.TEAMS),
    standings: wrap('standings', overrides.standings ?? F.STANDINGS),
    matches: wrap('matches', overrides.matches ?? { matches: [F.match(), F.match({ id: 9002, status: 'IN_PLAY', score: { winner: null, fullTime: { home: 0, away: 0 }, halfTime: {} } })] }),
    match: wrap('match', overrides.match ?? ((id) => ({ ...F.DETAIL_FINISHED, id }))),
  };
}

function setup(clientOverrides = {}, opts = {}) {
  const store = createMemoryStore();
  const client = fakeClient(clientOverrides);
  const syncer = createSyncer({
    client,
    store,
    leagues: [F.LEAGUE],
    owner: 'test-owner',
    now: () => NOW,
    log: silentLog,
    ...opts,
  });
  return { store, client, syncer };
}

test('syncScoreboard menulis setiap pertandingan dan tidak menggandakan saat diulang', async () => {
  const { store, syncer } = setup();
  const first = await syncer.syncScoreboard(F.LEAGUE);
  assert.equal(first.status, 'ok');
  assert.equal(first.matches, 2);
  await syncer.syncScoreboard(F.LEAGUE);
  assert.equal(store._data.matches.size, 2, 'upsert harus idempotent');
  const state = store._syncState({ provider: 'football-data', league_slug: 'eng.1', resource_type: 'scoreboard', resource_key: 'window' });
  assert.equal(state.status, 'healthy');
  assert.equal(state.consecutive_errors, 0);
});

test('respons jadwal tidak valid: tidak menulis apa pun dan mencatat error', async () => {
  const { store, syncer } = setup({ matches: { foo: 1 } });
  const res = await syncer.syncScoreboard(F.LEAGUE);
  assert.equal(res.status, 'error');
  assert.equal(store._data.matches.size, 0);
  const state = store._syncState({ provider: 'football-data', league_slug: 'eng.1', resource_type: 'scoreboard', resource_key: 'window' });
  assert.equal(state.status, 'error');
  assert.equal(state.consecutive_errors, 1);
});

test('klasemen gagal: snapshot valid sebelumnya dipertahankan', async () => {
  const store = createMemoryStore();
  const good = setup({}, {});
  // Gunakan store yang sama untuk dua syncer: sukses lalu gagal.
  const syncerOk = createSyncer({ client: good.client, store, leagues: [F.LEAGUE], owner: 'o', now: () => NOW, log: silentLog });
  await syncerOk.syncStandings(F.LEAGUE);
  assert.equal(store._data.standings.size, 1);

  const bad = fakeClient({ standings: { standings: [] } });
  const syncerBad = createSyncer({ client: bad, store, leagues: [F.LEAGUE], owner: 'o', now: () => NOW, log: silentLog });
  const res = await syncerBad.syncStandings(F.LEAGUE);
  assert.equal(res.status, 'error');
  const kept = store._data.standings.get('eng.1|2026|overall');
  assert.equal(kept.entries.length, 2, 'klasemen lama tidak boleh dikosongkan');
});

test('kegagalan jaringan dicatat di sync state tanpa menghentikan proses', async () => {
  const err = Object.assign(new Error('HTTP 503 pada /standings'), { status: 503 });
  const { store, syncer } = setup({ standings: err });
  const res = await syncer.syncStandings(F.LEAGUE);
  assert.equal(res.status, 'error');
  const state = store._syncState({ provider: 'football-data', league_slug: 'eng.1', resource_type: 'standings', resource_key: 'overall' });
  assert.equal(state.error.code, '503');
  assert.equal(state.status, 'error');
});

test('lease: proses lain yang memegang lease membuat pekerjaan dilewati', async () => {
  const { store, client, syncer } = setup();
  const key = { provider: 'football-data', league_slug: 'eng.1', resource_type: 'scoreboard', resource_key: 'window' };
  assert.equal(await store.acquireLease(key, 'proses-lain', 60000, NOW), true);
  const res = await syncer.syncScoreboard(F.LEAGUE);
  assert.equal(res.status, 'skipped');
  assert.equal(client.calls.filter(([n]) => n === 'matches').length, 0, 'tidak boleh memanggil API saat lease dipegang');
});

test('lease kedaluwarsa boleh diambil alih', async () => {
  const store = createMemoryStore();
  const key = { provider: 'football-data', league_slug: 'eng.1', resource_type: 'scoreboard', resource_key: 'window' };
  await store.acquireLease(key, 'lama', 1000, new Date(NOW.getTime() - 60000));
  assert.equal(await store.acquireLease(key, 'baru', 1000, NOW), true);
});

test('syncDetails: pertandingan live diambil ulang, pertandingan selesai hanya sekali', async () => {
  const { store, syncer } = setup();
  await syncer.syncScoreboard(F.LEAGUE); // 9001 terjadwal, 9002 live
  // Ubah 9001 menjadi selesai.
  const m = store._data.matches.get('eng.1|9001');
  m.status = { state: 'post', completed: true, name: 'STATUS_FULL_TIME' };
  m.scoreboard_date = '20261013';
  store._data.matches.get('eng.1|9002').scoreboard_date = '20261013';

  const first = await syncer.syncDetails(F.LEAGUE);
  assert.equal(first.status, 'ok');
  assert.equal(first.fetched, 2);

  const second = await syncer.syncDetails(F.LEAGUE);
  assert.equal(second.fetched, 1, 'hanya pertandingan live yang diambil lagi');
  assert.ok(store._data.events.size > 0);
  assert.equal(store._data.matches.get('eng.1|9001').play_by_play_available, true);
});

test('syncDetails: gagal pada satu pertandingan tidak menghentikan yang lain', async () => {
  const { store, syncer } = setup({
    match: (id) => (id === '9001' ? Object.assign(new Error('HTTP 500'), { status: 500 }) : { ...F.DETAIL_FINISHED, id }),
  });
  await syncer.syncScoreboard(F.LEAGUE);
  store._data.matches.get('eng.1|9001').status = { state: 'post', completed: true };
  store._data.matches.get('eng.1|9002').status = { state: 'post', completed: true };
  store._data.matches.get('eng.1|9002').scoreboard_date = '20261013';
  store._data.matches.get('eng.1|9001').scoreboard_date = '20261013';

  const res = await syncer.syncDetails(F.LEAGUE);
  assert.equal(res.failed, 1);
  assert.equal(res.fetched, 1);
  assert.equal(res.status, 'ok');
  const failed = store._syncState({ provider: 'football-data', league_slug: 'eng.1', resource_type: 'plays', resource_key: '9001' });
  assert.equal(failed.status, 'error');
});

test('syncClubs dan syncCatalog menulis katalog dan menolak daftar tim kosong', async () => {
  const { store, syncer } = setup();
  await syncer.syncCatalog(F.LEAGUE);
  assert.equal(store._data.leagues.get('eng.1').season.year, 2026);
  const res = await syncer.syncClubs(F.LEAGUE);
  assert.equal(res.clubs, 1);
  assert.deepEqual(store._data.clubs.get('football-data|57').league_slugs, ['eng.1']);

  const empty = setup({ teams: { teams: [] } });
  const bad = await empty.syncer.syncClubs(F.LEAGUE);
  assert.equal(bad.status, 'error');
  assert.equal(empty.store._data.clubs.size, 0);
});
