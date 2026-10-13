'use strict';

// Parser untuk dataset openfootball/football.json (domain publik, CC0).
// Dipakai hanya sebagai pengisi awal (seed) untuk musim yang sudah selesai.
// Data ini tidak live dan tidak punya ID klub; ID tim dibuat dari nama tim.
//
// Format sumber (per pertandingan):
//   date   "2025-08-15"
//   time   "19:00"            (tanpa zona: waktu lokal liga)
//          "19:00 UTC+0"      (dengan zona eksplisit)
//   score  {ft:[h,a], ht:[h,a]} | [h,a] | {ht:..} tanpa ft (belum/tidak ada skor)
//   status "postponed" | "canceled" | "awarded" (opsional)
//   goals1 / goals2  [{name, minute:"37" | "90+4"}]  (tim 1 / tim 2)
//   bookings         [[{type:"Y"|"R"|"Y/R", name, minute}], [...]]  (tim 1 / tim 2)
//   ground, attendance, round, team1, team2

const PROVIDER = 'openfootball';

const slugify = (s) =>
  String(s || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');

/** Selisih zona waktu (menit) untuk tz pada saat utcMs, memakai ICU bawaan Node. */
function offsetMinutes(tz, utcMs) {
  const dtf = new Intl.DateTimeFormat('en-US', {
    timeZone: tz,
    hourCycle: 'h23',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
  });
  const p = Object.fromEntries(dtf.formatToParts(new Date(utcMs)).map((x) => [x.type, x.value]));
  const asUtc = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second);
  return (asUtc - utcMs) / 60000;
}

/** Waktu lokal di zona tz ke epoch ms (UTC). */
function localToUtc(dateStr, hh, mm, tz) {
  const [y, m, d] = dateStr.split('-').map(Number);
  const guess = Date.UTC(y, m - 1, d, hh, mm);
  const off1 = offsetMinutes(tz, guess);
  let utc = guess - off1 * 60000;
  const off2 = offsetMinutes(tz, utc);
  if (off2 !== off1) utc = guess - off2 * 60000;
  return utc;
}

/**
 * Kick-off dalam UTC. Mengembalikan { utcMs, timeKnown }.
 * Jika jam tidak ada, tanggal dipakai pada 00:00 UTC dan timeKnown = false.
 */
function parseKickoff(dateStr, timeStr, tz) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(dateStr || ''))) throw new Error(`tanggal tidak valid: ${dateStr}`);
  const midnight = Date.parse(`${dateStr}T00:00:00Z`);
  if (!timeStr) return { utcMs: midnight, timeKnown: false };
  const m = /^(\d{1,2}):(\d{2})(?:\s*UTC([+-]\d{1,2}))?$/.exec(String(timeStr).trim());
  if (!m) return { utcMs: midnight, timeKnown: false };
  const hh = Number(m[1]);
  const mm = Number(m[2]);
  if (hh > 23 || mm > 59) return { utcMs: midnight, timeKnown: false };
  if (m[3] !== undefined) {
    // Zona eksplisit, misalnya UTC+0 atau UTC+9: waktu lokal dikurangi offset.
    const [y, mo, d] = dateStr.split('-').map(Number);
    return { utcMs: Date.UTC(y, mo - 1, d, hh, mm) - Number(m[3]) * 3600000, timeKnown: true };
  }
  if (!tz) return { utcMs: midnight, timeKnown: false };
  return { utcMs: localToUtc(dateStr, hh, mm, tz), timeKnown: true };
}

/** Ambil skor full time. Mengembalikan [h,a] atau null. */
function fullTimeOf(score) {
  if (Array.isArray(score) && score.length === 2 && score.every(Number.isInteger)) return score;
  if (score && Array.isArray(score.ft) && score.ft.length === 2 && score.ft.every(Number.isInteger)) return score.ft;
  return null;
}

/** "37" -> {minute:37, injury:0}; "90+4" -> {minute:90, injury:4}. */
function parseMinute(text) {
  const m = /^(\d{1,3})(?:\+(\d{1,2}))?$/.exec(String(text || '').trim());
  if (!m) return null;
  return { minute: Number(m[1]), injury: Number(m[2] || 0) };
}

function statusOf(match, fulltime) {
  const s = String(match.status || '').toLowerCase();
  if (s === 'postponed') return 'POSTPONED';
  if (s === 'canceled' || s === 'cancelled') return 'CANCELLED';
  if (fulltime) return 'FINISHED';
  return null;
}

function buildEvents(match, eventId, homeId, awayId, leagueSlug, competitionId, now) {
  const raw = [];
  const addGoals = (list, side) => {
    for (const g of list || []) {
      const t = parseMinute(g.minute);
      if (!t || !g.name) continue;
      raw.push({ kind: 'goal', side, name: String(g.name).trim(), ...t });
    }
  };
  addGoals(match.goals1, 'home');
  addGoals(match.goals2, 'away');

  const cardSides = ['home', 'away'];
  (match.bookings || []).forEach((list, i) => {
    if (!Array.isArray(list)) return;
    for (const b of list) {
      const t = parseMinute(b.minute);
      if (!t || !b.name || !cardSides[i]) continue;
      if (!['Y', 'R', 'Y/R'].includes(b.type)) continue;
      raw.push({ kind: b.type === 'Y' ? 'yellow' : 'red', side: cardSides[i], name: String(b.name).trim(), ...t, second: b.type === 'Y/R' });
    }
  });

  const order = { goal: 0, yellow: 1, red: 2 };
  raw.sort((a, b) => a.minute - b.minute || a.injury - b.injury || order[a.kind] - order[b.kind]);

  return raw.map((e, idx) => {
    const clubId = e.side === 'home' ? homeId : awayId;
    const clubName = e.side === 'home' ? match.team1 : match.team2;
    const clock = `${e.minute}'${e.injury ? `+${e.injury}` : ''}`;
    const flags = { scoring_play: false, yellow_card: false, red_card: false, substitution: false, penalty_kick: false, own_goal: false, shootout: false };
    let eventType;
    let text;
    if (e.kind === 'goal') {
      eventType = { id: 'goal', name: 'goal', text: 'Goal' };
      text = `Goal! ${e.name}`;
      flags.scoring_play = true;
    } else if (e.kind === 'yellow') {
      eventType = { id: 'yellow-card', name: 'yellow-card', text: 'Yellow Card' };
      text = `Yellow card: ${e.name}`;
      flags.yellow_card = true;
    } else {
      eventType = { id: 'red-card', name: 'red-card', text: 'Red Card' };
      text = e.second ? `Second yellow card: ${e.name}` : `Red card: ${e.name}`;
      flags.red_card = true;
    }
    return {
      source: {
        provider: PROVIDER,
        event_key: `${e.kind}:${e.side}:${e.minute}:${e.injury}:${slugify(e.name)}:${idx}`,
        modified_at: now,
      },
      league_slug: leagueSlug,
      event_id: eventId,
      competition_id: competitionId,
      sequence: idx + 1,
      event_type: eventType,
      text,
      alternative_text: text,
      clock: { value: e.minute * 60, display_value: clock, added_value: e.injury * 60, added_display_value: e.injury ? `+${e.injury}'` : '' },
      period: e.minute > 45 ? 2 : 1,
      club: { source_id: clubId, side: e.side, name: clubName || '' },
      athlete_source_ids: [],
      flags,
      valid: true,
    };
  });
}

/**
 * Ubah satu pertandingan sumber menjadi dokumen soccer_matches dan soccer_match_events.
 * Mengembalikan null jika pertandingan dilewati (tidak ada skor dan bukan postponed/canceled).
 */
function mapOpenfootballMatch(match, ctx) {
  const { leagueSlug, leagueName, seasonYear, tz, competitionId = 'openfootball', now } = ctx;
  const fulltime = fullTimeOf(match.score);
  const status = statusOf(match, fulltime);
  if (!status) return null;

  const { utcMs, timeKnown } = parseKickoff(match.date, match.time, tz);
  const kickoff = new Date(utcMs);
  const homeId = `of:${slugify(match.team1)}`;
  const awayId = `of:${slugify(match.team2)}`;
  const eventId = `of-${match.date}-${slugify(match.team1)}-${slugify(match.team2)}`;

  const finished = status === 'FINISHED';
  // source_id tim memakai awalan "of:" agar tidak tercampur dengan ID football-data.
  const side = (name, id, which) => {
    const doc = {
      source_id: id,
      uid: `of:team:${id}`,
      name: String(name || ''),
      display_name: String(name || ''),
      abbreviation: '',
      logo: '',
      winner: Boolean(finished && fulltime && (which === 'home' ? fulltime[0] > fulltime[1] : fulltime[1] > fulltime[0])),
      form: '',
    };
    if (finished && fulltime) doc.score = which === 'home' ? fulltime[0] : fulltime[1];
    return doc;
  };
  const homeDoc = side(match.team1, homeId, 'home');
  const awayDoc = side(match.team2, awayId, 'away');

  const events = buildEvents(match, eventId, homeId, awayId, leagueSlug, competitionId, now);

  const doc = {
    source: { provider: PROVIDER, event_id: eventId, competition_id: competitionId, uid: `of:match:${eventId}`, modified_at: now },
    league_slug: leagueSlug,
    scoreboard_date: kickoff.toISOString().slice(0, 10).replace(/-/g, ''),
    date: kickoff,
    name: `${match.team2} at ${match.team1}`,
    short_name: '',
    season: { year: seasonYear, type_id: '1', slug: 'regular-season', name: `${seasonYear}-${String((seasonYear + 1) % 100).padStart(2, '0')} ${leagueName}` },
    status: {
      state: finished ? 'post' : 'pre',
      name: finished ? 'STATUS_FULL_TIME' : status === 'POSTPONED' ? 'STATUS_POSTPONED' : 'STATUS_CANCELED',
      description: finished ? 'Full Time' : status === 'POSTPONED' ? 'Postponed' : 'Canceled',
      detail: finished ? 'FT' : status === 'POSTPONED' ? 'Postponed' : 'Canceled',
      short_detail: finished ? 'FT' : status === 'POSTPONED' ? 'Postponed' : 'Canceled',
      completed: finished,
      suspended: false,
    },
    home: homeDoc,
    away: awayDoc,
    venue: { source_id: '', name: String(match.ground || ''), city: '', country: '' },
    attendance: Number.isInteger(match.attendance) ? match.attendance : undefined,
    note: timeKnown ? `Seed dari openfootball (CC0). Round: ${match.round || '-'}` : `Seed dari openfootball (CC0). Jam kick-off tidak tersedia. Round: ${match.round || '-'}`,
    play_by_play_available: events.length > 0,
    last_synced_at: now,
  };
  if (doc.attendance === undefined) delete doc.attendance;
  return { match: doc, events, timeKnown };
}

/** Konversi seluruh file musim. Mengembalikan pertandingan yang valid dan statistik. */
function mapOpenfootballSeason(json, ctx) {
  const stats = { total: 0, mapped: 0, skipped: 0, withoutTime: 0, events: 0 };
  const matches = [];
  for (const m of json.matches || []) {
    stats.total++;
    let mapped = null;
    try {
      mapped = mapOpenfootballMatch(m, ctx);
    } catch {
      // Tanggal rusak pada satu baris tidak boleh menggagalkan seluruh musim.
      mapped = null;
    }
    if (!mapped) {
      stats.skipped++;
      continue;
    }
    stats.mapped++;
    if (!mapped.timeKnown) stats.withoutTime++;
    stats.events += mapped.events.length;
    matches.push(mapped);
  }
  return { matches, stats };
}

module.exports = {
  PROVIDER,
  slugify,
  offsetMinutes,
  localToUtc,
  parseKickoff,
  parseMinute,
  fullTimeOf,
  mapOpenfootballMatch,
  mapOpenfootballSeason,
};
