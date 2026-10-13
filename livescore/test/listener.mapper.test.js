'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const mapper = require('../listener/mapper');
const F = require('./listener.fixtures');

const NOW = new Date('2026-10-13T12:00:00Z');

test('mapStatus memetakan status football-data ke state kontrak', () => {
  assert.equal(mapper.mapStatus('SCHEDULED').state, 'pre');
  assert.equal(mapper.mapStatus('TIMED').state, 'pre');

  const live = mapper.mapStatus('IN_PLAY', 67);
  assert.equal(live.state, 'in');
  assert.equal(live.clock, "67'");
  assert.equal(live.period, 2);
  assert.equal(live.clock_seconds, 67 * 60);

  const ht = mapper.mapStatus('PAUSED');
  assert.equal(ht.state, 'in');
  assert.equal(ht.name, 'STATUS_HALFTIME');

  const ft = mapper.mapStatus('FINISHED');
  assert.equal(ft.state, 'post');
  assert.equal(ft.completed, true);

  assert.equal(mapper.mapStatus('POSTPONED').name, 'STATUS_POSTPONED');
  assert.equal(mapper.mapStatus('SUSPENDED').suspended, true);
  assert.equal(mapper.mapStatus('NEW_UNKNOWN_STATUS').name, 'STATUS_UNKNOWN');
});

test('mapMatch: pertandingan terjadwal tidak punya skor dan tanggal scoreboard benar', () => {
  const doc = mapper.mapMatch(F.match(), F.LEAGUE, NOW);
  assert.equal(doc.league_slug, 'eng.1');
  assert.equal(doc.scoreboard_date, '20261013');
  assert.equal(doc.source.event_id, '9001');
  assert.equal(doc.source.provider, 'football-data');
  assert.equal(doc.status.state, 'pre');
  assert.equal(doc.home.score, undefined, 'skor tidak boleh diisi sebelum kick-off');
  assert.equal(doc.home.winner, false);
  assert.equal(doc.season.year, 2026);
});

test('mapMatch: saat berlangsung skor memakai halfTime jika fullTime belum ada', () => {
  const doc = mapper.mapMatch(
    F.match({ status: 'PAUSED', score: { winner: null, fullTime: { home: null, away: null }, halfTime: { home: 1, away: 0 } } }),
    F.LEAGUE,
    NOW
  );
  assert.equal(doc.status.state, 'in');
  assert.equal(doc.home.score, 1);
  assert.equal(doc.away.score, 0);
});

test('mapMatch: pertandingan selesai punya skor penuh dan pemenang', () => {
  const doc = mapper.mapMatch(F.DETAIL_FINISHED, F.LEAGUE, NOW);
  assert.equal(doc.status.completed, true);
  assert.equal(doc.home.score, 2);
  assert.equal(doc.away.score, 1);
  assert.equal(doc.home.winner, true);
  assert.equal(doc.away.winner, false);
});

test('mapMatch: pemenang tidak ditandai selama pertandingan masih berjalan', () => {
  const doc = mapper.mapMatch(
    F.match({ status: 'IN_PLAY', score: { winner: 'HOME_TEAM', fullTime: { home: 1, away: 0 }, halfTime: {} } }),
    F.LEAGUE,
    NOW
  );
  assert.equal(doc.home.winner, false);
});

test('mapEvents: urutan, tipe, flag, dan sisi tim benar', () => {
  const events = mapper.mapEvents(F.DETAIL_FINISHED, F.LEAGUE, NOW);
  assert.equal(events.length, 6);
  const minutes = events.map((e) => e.clock.value / 60);
  assert.deepEqual(minutes, [...minutes].sort((a, b) => a - b));

  const [goal1, ownGoal, lateGoal] = events.filter((e) => e.event_type.name === 'goal');
  assert.equal(goal1.club.side, 'home');
  assert.equal(goal1.home_score, 1);
  assert.equal(goal1.flags.scoring_play, true);

  assert.equal(ownGoal.flags.own_goal, true);
  assert.equal(ownGoal.text.startsWith('Own Goal'), true);

  assert.equal(lateGoal.clock.display_value, "88'+2");
  assert.equal(lateGoal.period, 2);

  const yellowRed = events.find((e) => e.minute === 77 || e.clock.value === 77 * 60);
  assert.equal(yellowRed.flags.red_card, true, 'YELLOW_RED_CARD dihitung sebagai kartu merah');

  const sub = events.find((e) => e.event_type.name === 'substitution');
  assert.match(sub.text, /Trossard replaces Martinelli/);
});

test('mapEvents: event_key deterministik dan unik untuk setiap kejadian', () => {
  const a = mapper.mapEvents(F.DETAIL_FINISHED, F.LEAGUE, NOW);
  const b = mapper.mapEvents(F.DETAIL_FINISHED, F.LEAGUE, NOW);
  assert.deepEqual(a.map((e) => e.source.event_key), b.map((e) => e.source.event_key));
  assert.equal(new Set(a.map((e) => e.source.event_key)).size, a.length);
});

test('mapEvents: tim yang tidak dikenal tidak diberi sisi home/away', () => {
  const detail = { ...F.DETAIL_FINISHED, goals: [{ minute: 10, team: { id: 999, name: 'Other' }, scorer: { id: 1, name: 'A' }, type: 'REGULAR' }], bookings: [], substitutions: [] };
  const [e] = mapper.mapEvents(detail, F.LEAGUE, NOW);
  assert.equal(e.club.side, 'unknown');
});

test('mapStandings: memetakan tabel dan menolak data kosong', () => {
  const doc = mapper.mapStandings(F.STANDINGS, F.LEAGUE, 2026, NOW);
  assert.equal(doc.group_id, 'overall');
  assert.equal(doc.entries.length, 2);
  assert.equal(doc.entries[0].rank, 1);
  assert.equal(doc.entries[0].club.source_id, '57');
  assert.equal(doc.entries[0].stats.points, 16);
  assert.equal(doc.entries[0].stats.goalDifference, 9);

  assert.equal(mapper.mapStandings({ standings: [] }, F.LEAGUE, 2026, NOW), null);
  assert.equal(mapper.mapStandings(null, F.LEAGUE, 2026, NOW), null);
  const broken = { standings: [{ type: 'TOTAL', table: [{ team: { id: 1, name: 'X' } }] }] };
  assert.equal(mapper.mapStandings(broken, F.LEAGUE, 2026, NOW), null, 'baris tanpa posisi dianggap tidak valid');
});

test('mapClub: slug, sumber, pelatih, dan skuad', () => {
  const doc = mapper.mapClub(F.TEAMS.teams[0], F.LEAGUE, NOW);
  assert.equal(doc.source.club_id, '57');
  assert.equal(doc.slug, 'arsenal-fc');
  assert.equal(doc.coach.display_name, 'Mikel A');
  assert.equal(doc.roster[0].display_name, 'Bukayo Saka');
  assert.equal(doc.venue.name, 'Emirates Stadium');

  const noCoach = mapper.mapClub({ id: 5, name: 'Club Ñ', tla: 'CLN' }, F.LEAGUE, NOW);
  assert.equal(noCoach.coach, undefined);
  assert.equal(noCoach.slug, 'club-n');
});

test('mapLeague: tahun musim diambil dari currentSeason', () => {
  const doc = mapper.mapLeague(F.LEAGUE, F.COMPETITION);
  assert.equal(doc.slug, 'eng.1');
  assert.equal(doc.season.year, 2026);
  assert.equal(doc.season.display_name, '2026-27 English Premier League');
  assert.equal(doc.source.source_id, '2021');
});
