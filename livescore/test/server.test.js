import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { createApp } from '../src/app.js';
import { createAggregator } from '../src/aggregator.js';
import { createMockProvider } from '../src/providers/mock.js';

const DAY = '2026-10-13';
const NOW = Date.parse(`${DAY}T15:00:00Z`);
let server;
let base;

before(async () => {
  const aggregator = createAggregator({ providers: [createMockProvider()] });
  server = createApp({ aggregator, now: () => NOW, tickMs: 60_000, log: { error() {} } });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  base = `http://127.0.0.1:${server.address().port}`;
});

after(() => new Promise((r) => server.close(r)));

test('GET /api/health', async () => {
  const body = await (await fetch(`${base}/api/health`)).json();
  assert.equal(body.ok, true);
  assert.deepEqual(body.providers, ['mock']);
});

test('GET /api/matches mengembalikan daftar tanpa events dan terurut', async () => {
  const res = await fetch(`${base}/api/matches?date=${DAY}`);
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.date, DAY);
  assert.equal(body.count, body.matches.length);
  assert.ok(body.matches.length > 0);
  assert.ok(!('events' in body.matches[0]));
  const kicks = body.matches.map((m) => m.kickoff);
  assert.deepEqual(kicks, [...kicks].sort());
});

test('filter status=live hanya mengembalikan pertandingan yang berlangsung', async () => {
  const body = await (await fetch(`${base}/api/matches?date=${DAY}&status=live`)).json();
  for (const m of body.matches) assert.ok(m.status === 'LIVE' || m.status === 'HALF_TIME');
});

test('tanggal tidak valid ditolak dengan 400', async () => {
  const res = await fetch(`${base}/api/matches?date=13-10-2026`);
  assert.equal(res.status, 400);
});

test('detail pertandingan menyertakan kejadian', async () => {
  const { matches } = await (await fetch(`${base}/api/matches?date=${DAY}`)).json();
  const id = matches[0].id;
  const res = await fetch(`${base}/api/matches/${encodeURIComponent(id)}`);
  assert.equal(res.status, 200);
  const m = await res.json();
  assert.equal(m.id, id);
  assert.ok(Array.isArray(m.events));
});

test('pertandingan tidak dikenal mengembalikan 404', async () => {
  const res = await fetch(`${base}/api/matches/${encodeURIComponent('mock:xx:2026-10-13:0')}`);
  assert.equal(res.status, 404);
});

test('file statis dilayani dan path traversal ditolak', async () => {
  const home = await fetch(`${base}/`);
  assert.equal(home.status, 200);
  assert.match(await home.text(), /Skor Langsung/);
  const js = await fetch(`${base}/app.js`);
  assert.equal(js.status, 200);
  assert.match(js.headers.get('content-type'), /javascript/);
  const bad = await fetch(`${base}/..%2F..%2Fpackage.json`);
  assert.notEqual(bad.status, 200);
});

test('metode selain GET ditolak', async () => {
  const res = await fetch(`${base}/api/matches`, { method: 'POST' });
  assert.equal(res.status, 405);
});

test('SSE /api/stream mengirim hello pada koneksi baru', async () => {
  const ctrl = new AbortController();
  const res = await fetch(`${base}/api/stream?date=${DAY}`, { signal: ctrl.signal });
  assert.equal(res.headers.get('content-type'), 'text/event-stream; charset=utf-8');
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let text = '';
  while (!text.includes('\n\n')) {
    const { value, done } = await reader.read();
    if (done) break;
    text += decoder.decode(value);
  }
  assert.match(text, /"type":"hello"/);
  ctrl.abort();
});
