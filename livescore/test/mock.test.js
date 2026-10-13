import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mockMatchesForDate, mockMatchById, phaseAt, buildEvents } from '../src/providers/mock.js';

const DAY = '2026-10-13';
const dayStart = Date.parse(`${DAY}T00:00:00Z`);

test('jadwal mock deterministik untuk tanggal dan waktu yang sama', () => {
  const now = dayStart + 15 * 3600000;
  const a = mockMatchesForDate(DAY, now);
  const b = mockMatchesForDate(DAY, now);
  assert.deepEqual(a, b);
  assert.ok(a.length > 0, 'harus ada pertandingan pada hari yang dijadwalkan');
});

test('setiap pertandingan punya dua tim berbeda dan liga valid', () => {
  for (const m of mockMatchesForDate(DAY, dayStart)) {
    assert.notEqual(m.home.id, m.away.id);
    assert.ok(m.league.name);
    assert.equal(m.source, 'mock');
  }
});

test('fase pertandingan: terjadwal, babak 1, istirahat, babak 2, selesai', () => {
  const k = dayStart + 20 * 3600000;
  assert.equal(phaseAt(k, k - 1000).status, 'SCHEDULED');
  assert.deepEqual(phaseAt(k, k + 10 * 60000), { status: 'LIVE', minute: 11, played: 11 });
  assert.equal(phaseAt(k, k + 50 * 60000).status, 'HALF_TIME');
  assert.deepEqual(phaseAt(k, k + 75 * 60000), { status: 'LIVE', minute: 61, played: 61 });
  assert.equal(phaseAt(k, k + 120 * 60000).status, 'FINISHED');
});

test('skor langsung mengikuti kejadian gol sampai menit berjalan', () => {
  // Setelah seluruh pertandingan hari itu selesai (kick-off terakhir 23:30 UTC + 105 menit).
  for (const m of mockMatchesForDate(DAY, dayStart + 26 * 3600000)) {
    const goalsHome = m.events.filter((e) => e.type === 'goal' && e.team === 'home').length;
    const goalsAway = m.events.filter((e) => e.type === 'goal' && e.team === 'away').length;
    assert.equal(m.status, 'FINISHED');
    assert.equal(m.score.home, goalsHome);
    assert.equal(m.score.away, goalsAway);
  }
});

test('pertandingan yang belum mulai tidak punya skor', () => {
  const early = dayStart; // 00:00 UTC, sebelum sebagian besar kick-off
  for (const m of mockMatchesForDate(DAY, early - 60000)) {
    assert.equal(m.status, 'SCHEDULED');
    assert.equal(m.score, null);
    assert.deepEqual(m.events, []);
  }
});

test('kejadian selalu terurut menit dan berada dalam 90 menit', () => {
  const ev = buildEvents('seed-uji');
  for (let i = 1; i < ev.length; i++) assert.ok(ev[i - 1].minute <= ev[i].minute);
  for (const e of ev) assert.ok(e.minute >= 1 && e.minute <= 90);
});

test('mockMatchById menemukan pertandingan dari id hasil daftar', () => {
  const now = dayStart + 23 * 3600000;
  const [first] = mockMatchesForDate(DAY, now);
  assert.deepEqual(mockMatchById(first.id, now), first);
  assert.equal(mockMatchById('mock:tidak-ada:2026-10-13:0', now), null);
  assert.equal(mockMatchById('bukan-id', now), null);
});
