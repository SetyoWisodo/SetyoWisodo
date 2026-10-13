import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createApp } from '../src/app.js';
import { createAggregator } from '../src/aggregator.js';
import { createMockProvider, mockMatchesForDate } from '../src/providers/mock.js';

const DAY = '2026-10-13';
const dayStart = Date.parse(`${DAY}T00:00:00Z`);

test('SSE mengirim pembaruan ketika pertandingan mulai berlangsung', async () => {
  // Cari waktu di mana ada pertandingan yang baru mulai (kick-off 10 menit lalu).
  const kickoffs = mockMatchesForDate(DAY, dayStart).map((m) => Date.parse(m.kickoff));
  const firstKick = Math.min(...kickoffs);
  let clock = firstKick - 60_000; // sebelum kick-off pertama
  const aggregator = createAggregator({ providers: [createMockProvider()] });
  const server = createApp({ aggregator, now: () => clock, tickMs: 50, log: { error() {} } });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;

  const ctrl = new AbortController();
  const res = await fetch(`http://127.0.0.1:${port}/api/stream?date=${DAY}`, { signal: ctrl.signal });
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = '';
  const readEvent = async (predicate, timeoutMs = 3000) => {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      const idx = buf.indexOf('\n\n');
      if (idx !== -1) {
        const chunk = buf.slice(0, idx);
        buf = buf.slice(idx + 2);
        const line = chunk.split('\n').find((l) => l.startsWith('data: '));
        if (line) {
          const payload = JSON.parse(line.slice(6));
          if (predicate(payload)) return payload;
        }
        continue;
      }
      const { value, done } = await reader.read();
      if (done) break;
      buf += decoder.decode(value);
    }
    return null;
  };

  try {
    const hello = await readEvent((p) => p.type === 'hello');
    assert.ok(hello, 'hello harus diterima');

    // Pembaruan awal: semua pertandingan (status SCHEDULED) dikirim sebagai perubahan pertama.
    const initial = await readEvent((p) => p.type === 'update');
    assert.ok(initial && initial.matches.length > 0);

    // Majukan waktu 10 menit setelah kick-off pertama: status pertandingan harus berubah ke LIVE.
    clock = firstKick + 10 * 60_000;
    const live = await readEvent((p) => p.type === 'update' && p.matches.some((m) => m.status === 'LIVE'));
    assert.ok(live, 'harus ada pembaruan dengan pertandingan LIVE');
    const liveMatch = live.matches.find((m) => m.status === 'LIVE');
    assert.equal(liveMatch.minute, 11);
    assert.ok(!('events' in liveMatch));
  } finally {
    ctrl.abort();
    await new Promise((r) => server.close(r));
  }
});
