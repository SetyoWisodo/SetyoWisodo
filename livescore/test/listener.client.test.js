'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { createFootballDataClient, FootballDataError } = require('../listener/footballData');

function response(status, body = {}, type = 'application/json') {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: (k) => (k.toLowerCase() === 'content-type' ? type : null) },
    json: async () => body,
  };
}

function makeClock() {
  let t = 0;
  const sleeps = [];
  return {
    now: () => t,
    sleep: async (ms) => {
      sleeps.push(ms);
      t += ms;
    },
    sleeps,
  };
}

test('token wajib diisi', () => {
  assert.throws(() => createFootballDataClient({}), /FOOTBALL_DATA_TOKEN/);
});

test('header token dikirim dan path dibentuk dengan benar', async () => {
  const seen = [];
  const clock = makeClock();
  const client = createFootballDataClient({
    token: 'secret',
    minIntervalMs: 0,
    now: clock.now,
    sleep: clock.sleep,
    fetchImpl: async (url, opts) => {
      seen.push({ url, token: opts.headers['X-Auth-Token'] });
      return response(200, { ok: true });
    },
  });
  await client.matches('PL', '2026-10-12', '2026-10-20');
  assert.equal(seen[0].token, 'secret');
  assert.equal(seen[0].url, 'https://api.football-data.org/v4/competitions/PL/matches?dateFrom=2026-10-12&dateTo=2026-10-20');
});

test('request diberi jarak minimal sesuai throttle', async () => {
  const clock = makeClock();
  const client = createFootballDataClient({
    token: 't',
    minIntervalMs: 6500,
    now: clock.now,
    sleep: clock.sleep,
    fetchImpl: async () => response(200, {}),
  });
  await Promise.all([client.teams('PL'), client.standings('PL'), client.match(1)]);
  // Request pertama tidak menunggu; dua berikutnya menunggu 6.5 detik.
  assert.deepEqual(clock.sleeps, [6500, 6500]);
});

test('429 dicoba ulang setelah jeda, lalu berhasil', async () => {
  const clock = makeClock();
  let n = 0;
  const client = createFootballDataClient({
    token: 't',
    minIntervalMs: 0,
    now: clock.now,
    sleep: clock.sleep,
    fetchImpl: async () => (++n === 1 ? response(429, {}) : response(200, { done: true })),
  });
  const body = await client.competition('PL');
  assert.deepEqual(body, { done: true });
  assert.equal(n, 2);
  assert.ok(clock.sleeps.includes(60000));
});

test('404 tidak dicoba ulang dan melempar FootballDataError', async () => {
  let n = 0;
  const client = createFootballDataClient({
    token: 't',
    minIntervalMs: 0,
    sleep: async () => {},
    fetchImpl: async () => {
      n++;
      return response(404, {});
    },
  });
  await assert.rejects(client.match(999), (err) => err instanceof FootballDataError && err.status === 404);
  assert.equal(n, 1);
});

test('5xx dicoba ulang maksimal maxRetries kali', async () => {
  let n = 0;
  const client = createFootballDataClient({
    token: 't',
    minIntervalMs: 0,
    maxRetries: 2,
    sleep: async () => {},
    fetchImpl: async () => {
      n++;
      return response(503, {});
    },
  });
  await assert.rejects(client.teams('PL'), (err) => err.status === 503);
  assert.equal(n, 3);
});

test('respons non-JSON ditolak', async () => {
  const client = createFootballDataClient({
    token: 't',
    minIntervalMs: 0,
    sleep: async () => {},
    fetchImpl: async () => response(200, '<html>', 'text/html'),
  });
  await assert.rejects(client.teams('PL'), /Content-Type tidak valid/);
});
