import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createFootballDataProvider, normalizeFdMatch } from '../src/providers/footballData.js';
import { createProvidersFromEnv } from '../src/providers/index.js';

const payload = {
  id: 555,
  utcDate: '2026-10-13T14:00:00Z',
  status: 'PAUSED',
  minute: null,
  competition: { id: 2021, name: 'Premier League', area: { name: 'England', code: 'ENG', flag: 'https://x/eng.png' } },
  homeTeam: { id: 1, name: 'Arsenal FC', tla: 'ARS' },
  awayTeam: { id: 2, name: 'Chelsea FC', tla: 'CHE' },
  score: { fullTime: { home: null, away: null }, halfTime: { home: 1, away: 0 } },
  goals: [{ minute: 33, type: 'REGULAR', team: { id: 1 }, scorer: { name: 'Saka' } }],
  bookings: [{ minute: 40, team: { id: 2 }, player: { name: 'Caicedo' }, card: 'YELLOW_CARD' }],
  substitutions: [],
};

test('normalisasi: status PAUSED menjadi HALF_TIME dan skor paruh waktu terbaca', () => {
  const m = normalizeFdMatch(payload);
  assert.equal(m.id, 'fd:555');
  assert.equal(m.status, 'HALF_TIME');
  assert.equal(m.score.halfTime.home, 1);
  assert.equal(m.home.short, 'ARS');
  assert.equal(m.league.countryCode, 'ENG');
});

test('normalisasi: gol & kartu diberi sisi tim yang benar', () => {
  const m = normalizeFdMatch(payload);
  assert.deepEqual(m.events[0], { minute: 33, type: 'goal', team: 'home', player: 'Saka' });
  assert.deepEqual(m.events[1], { minute: 40, type: 'yellow', team: 'away', player: 'Caicedo' });
});

test('normalisasi: pertandingan terjadwal tidak punya skor', () => {
  const m = normalizeFdMatch({ ...payload, status: 'TIMED', score: { fullTime: { home: null, away: null } } });
  assert.equal(m.status, 'SCHEDULED');
  assert.equal(m.score, null);
});

test('provider memakai header token dan cache per tanggal', async () => {
  const calls = [];
  const fetchImpl = async (url, opts) => {
    calls.push({ url, token: opts.headers['X-Auth-Token'] });
    return { ok: true, json: async () => ({ matches: [payload] }) };
  };
  let t = 0;
  const p = createFootballDataProvider({ token: 'abc', fetchImpl, ttlMs: 60000, now: () => t });
  const a = await p.getMatches('2026-10-13');
  const b = await p.getMatches('2026-10-13');
  assert.equal(a.length, 1);
  assert.deepEqual(a, b);
  assert.equal(calls.length, 1, 'panggilan kedua harus dari cache');
  assert.equal(calls[0].token, 'abc');
  assert.match(calls[0].url, /matches\?dateFrom=2026-10-13&dateTo=2026-10-13$/);

  t = 61000;
  await p.getMatches('2026-10-13');
  assert.equal(calls.length, 2, 'setelah TTL harus memanggil API lagi');
});

test('provider melempar error saat HTTP gagal', async () => {
  const p = createFootballDataProvider({
    token: 'abc',
    fetchImpl: async () => ({ ok: false, status: 429 }),
  });
  await assert.rejects(p.getMatches('2026-10-13'), /HTTP 429/);
});

test('tanpa token, provider footballdata dilewati dan memakai mock', () => {
  const warns = [];
  const providers = createProvidersFromEnv({ PROVIDERS: 'footballdata' }, { warn: (m) => warns.push(m) });
  assert.deepEqual(providers.map((p) => p.name), ['mock']);
  assert.equal(warns.length, 2);
});
