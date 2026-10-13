'use strict';

// Normalisasi payload football-data.org ke dokumen kontrak soccer_* (lihat
// LIVE-LISTENER-DATABASE.md). Fungsi di sini murni: tidak menyentuh database.
//
// Aturan dari UPSTREAM-LIVE-DATA.md:
// - ID sumber selalu string dan hanya ada di dalam objek `source` / `source_id`.
// - Nilai yang tidak diketahui dibiarkan absent/null, tidak diisi tebakan.
// - Skor hanya diisi saat pertandingan sudah berjalan atau selesai.

const PROVIDER = 'football-data';

const slugify = (s) =>
  String(s || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');

const str = (v) => (v === null || v === undefined ? '' : String(v));
const finiteNum = (v) => (typeof v === 'number' && Number.isFinite(v) ? v : undefined);
const ymd = (date) => date.toISOString().slice(0, 10).replace(/-/g, '');

/** Ubah status football-data menjadi objek status kontrak (state: pre | in | post). */
function mapStatus(status, minute) {
  const base = { state: 'pre', name: '', description: '', detail: '', short_detail: '', clock: '', completed: false, suspended: false };
  const minuteOk = Number.isInteger(minute) && minute >= 0;
  switch (status) {
    case 'SCHEDULED':
    case 'TIMED':
      return { ...base, name: 'STATUS_SCHEDULED', description: 'Scheduled', detail: 'Scheduled', short_detail: 'Scheduled' };
    case 'IN_PLAY':
    case 'LIVE': {
      const clock = minuteOk ? `${minute}'` : '';
      return {
        ...base,
        state: 'in',
        name: 'STATUS_IN_PROGRESS',
        description: 'In Progress',
        detail: clock || 'In Progress',
        short_detail: clock || 'In Progress',
        clock,
        clock_seconds: minuteOk ? minute * 60 : undefined,
        period: minuteOk ? (minute > 45 ? 2 : 1) : undefined,
      };
    }
    case 'PAUSED':
      return { ...base, state: 'in', name: 'STATUS_HALFTIME', description: 'Halftime', detail: 'Halftime', short_detail: 'Halftime', period: 1 };
    case 'FINISHED':
    case 'AWARDED':
      return { ...base, state: 'post', name: 'STATUS_FULL_TIME', description: 'Full Time', detail: 'FT', short_detail: 'FT', completed: true };
    case 'POSTPONED':
      return { ...base, name: 'STATUS_POSTPONED', description: 'Postponed', detail: 'Postponed', short_detail: 'Postponed' };
    case 'SUSPENDED':
      return { ...base, state: 'in', name: 'STATUS_SUSPENDED', description: 'Suspended', detail: 'Suspended', short_detail: 'Suspended', suspended: true };
    case 'CANCELLED':
      return { ...base, name: 'STATUS_CANCELED', description: 'Canceled', detail: 'Canceled', short_detail: 'Canceled' };
    default:
      return { ...base, name: 'STATUS_UNKNOWN', description: str(status) || 'Unknown', detail: str(status), short_detail: str(status) };
  }
}

function seasonFrom(league, season) {
  if (!season || !season.startDate) return undefined;
  const year = Number(season.startDate.slice(0, 4));
  const endYear = String((Number(season.endDate?.slice(0, 4)) || year + 1) % 100).padStart(2, '0');
  return {
    year,
    display_name: `${year}-${endYear} ${league.name}`,
    current: true,
    type_id: '1',
    type_name: 'Regular Season',
  };
}

/** Dokumen soccer_leagues (kunci upsert: slug). */
function mapLeague(def, competition) {
  const season = seasonFrom(def, competition?.currentSeason);
  return {
    slug: def.slug,
    name: def.name,
    abbreviation: def.abbreviation,
    country: def.country,
    kind: def.kind,
    active: true,
    sort_order: def.sort_order,
    logo: str(competition?.emblem),
    source: { provider: PROVIDER, source_id: str(def.fd.id) },
    ...(season ? { season } : {}),
  };
}

function scoreFor(match, which, status) {
  if (status.state === 'pre') return undefined;
  const full = match.score?.fullTime?.[which];
  if (finiteNum(full) !== undefined) return full;
  // Saat berlangsung, fullTime kadang kosong sementara halfTime sudah terisi.
  if (status.state === 'in') return finiteNum(match.score?.halfTime?.[which]);
  return undefined;
}

function mapSide(team, which, match, status) {
  const winner = match.score?.winner;
  const side = {
    source_id: str(team?.id),
    uid: `fd:team:${str(team?.id)}`,
    name: str(team?.name),
    display_name: str(team?.name),
    abbreviation: str(team?.tla),
    logo: str(team?.crest),
    winner: status.completed && winner === (which === 'home' ? 'HOME_TEAM' : 'AWAY_TEAM'),
    form: '',
  };
  const score = scoreFor(match, which, status);
  if (score !== undefined) side.score = score;
  return side;
}

/** Dokumen soccer_matches (kunci upsert: source.provider + league_slug + source.event_id). */
function mapMatch(match, def, now) {
  const status = mapStatus(match.status, match.minute);
  const home = match.homeTeam || {};
  const away = match.awayTeam || {};
  const date = new Date(match.utcDate);
  return {
    source: {
      provider: PROVIDER,
      event_id: str(match.id),
      competition_id: str(match.competition?.id ?? def.fd.id),
      uid: `fd:match:${str(match.id)}`,
      modified_at: match.lastUpdated ? new Date(match.lastUpdated) : now,
    },
    league_slug: def.slug,
    scoreboard_date: ymd(date),
    date,
    name: `${str(away.name)} at ${str(home.name)}`,
    short_name: `${str(away.tla)} @ ${str(home.tla)}`,
    season: match.season ? seasonFrom(def, match.season) : undefined,
    status,
    home: mapSide(home, 'home', match, status),
    away: mapSide(away, 'away', match, status),
    venue: { source_id: '', name: str(match.venue), city: '', country: '' },
    note: def.name,
    last_synced_at: now,
  };
}

function teamSide(team, match) {
  if (team?.id === undefined || team?.id === null) return 'unknown';
  if (team.id === match.homeTeam?.id) return 'home';
  if (team.id === match.awayTeam?.id) return 'away';
  return 'unknown';
}

/** Kejadian pertandingan untuk soccer_match_events. Kunci event_key bersifat deterministik. */
function mapEvents(detail, def, now) {
  const eventId = str(detail.id);
  const competitionId = str(detail.competition?.id ?? def.fd.id);
  const raw = [];

  for (const g of detail.goals || []) {
    raw.push({ kind: 'goal', minute: g.minute, injury: g.injuryTime || 0, team: g.team, athlete: g.scorer, type: g.type, score: g.score });
  }
  for (const b of detail.bookings || []) {
    const red = b.card === 'RED_CARD' || b.card === 'YELLOW_RED_CARD';
    raw.push({ kind: red ? 'red' : 'yellow', minute: b.minute, injury: b.injuryTime || 0, team: b.team, athlete: b.player });
  }
  for (const s of detail.substitutions || []) {
    raw.push({ kind: 'sub', minute: s.minute, injury: s.injuryTime || 0, team: s.team, athlete: s.playerIn, playerOut: s.playerOut });
  }

  const order = { goal: 0, yellow: 1, red: 2, sub: 3 };
  raw.sort((a, b) => (a.minute ?? 0) - (b.minute ?? 0) || a.injury - b.injury || order[a.kind] - order[b.kind]);

  return raw.map((e, idx) => {
    const minute = Number.isFinite(e.minute) ? e.minute : null;
    const side = teamSide(e.team, detail);
    const teamName = str(e.team?.name);
    const athleteId = str(e.athlete?.id || e.athlete?.name);
    const clockText = minute === null ? '' : `${minute}'${e.injury ? `+${e.injury}` : ''}`;
    const playerName = str(e.athlete?.name);

    let eventType;
    let text;
    const flags = { scoring_play: false, yellow_card: false, red_card: false, substitution: false, penalty_kick: false, own_goal: false, shootout: false };
    if (e.kind === 'goal') {
      const own = e.type === 'OWN';
      const pen = e.type === 'PENALTY';
      eventType = { id: 'goal', name: 'goal', text: 'Goal' };
      text = `${own ? 'Own Goal' : pen ? 'Penalty - Scored' : 'Goal'}! ${playerName}`.trim();
      flags.scoring_play = true;
      flags.own_goal = own;
      flags.penalty_kick = pen;
    } else if (e.kind === 'yellow') {
      eventType = { id: 'yellow-card', name: 'yellow-card', text: 'Yellow Card' };
      text = `Yellow card: ${playerName}`.trim();
      flags.yellow_card = true;
    } else if (e.kind === 'red') {
      eventType = { id: 'red-card', name: 'red-card', text: 'Red Card' };
      text = `Red card: ${playerName}`.trim();
      flags.red_card = true;
    } else {
      eventType = { id: 'substitution', name: 'substitution', text: 'Substitution' };
      text = `Substitution: ${playerName} replaces ${str(e.playerOut?.name)}`.trim();
      flags.substitution = true;
    }

    const doc = {
      source: {
        provider: PROVIDER,
        event_key: `${e.kind}:${eventId}:${minute ?? 'x'}:${e.injury}:${athleteId}:${str(e.team?.id)}`,
        modified_at: now,
      },
      league_slug: def.slug,
      event_id: eventId,
      competition_id: competitionId,
      sequence: idx + 1,
      event_type: eventType,
      text,
      alternative_text: text,
      clock: {
        value: minute === null ? 0 : minute * 60,
        display_value: clockText,
        added_value: e.injury * 60,
        added_display_value: e.injury ? `+${e.injury}'` : '',
      },
      period: minute !== null && minute > 45 ? 2 : 1,
      club: { source_id: str(e.team?.id), side, name: teamName },
      athlete_source_ids: athleteId ? [athleteId] : [],
      flags,
      valid: true,
    };
    if (e.kind === 'goal' && e.score) {
      doc.home_score = finiteNum(e.score.home);
      doc.away_score = finiteNum(e.score.away);
    }
    return doc;
  });
}

/** Dokumen soccer_standings untuk grup "overall" (liga domestik). Null jika data tidak valid. */
function mapStandings(payload, def, seasonYear, now) {
  const groups = payload?.standings || [];
  const total = groups.find((g) => g.type === 'TOTAL') || groups[0];
  if (!total || !Array.isArray(total.table) || total.table.length === 0) return null;
  const entries = total.table.map((row) => ({
    rank: row.position,
    club: {
      source_id: str(row.team?.id),
      display_name: str(row.team?.name),
      abbreviation: str(row.team?.tla),
      logo: str(row.team?.crest),
    },
    stats: {
      gamesPlayed: row.playedGames,
      wins: row.won,
      ties: row.draw,
      losses: row.lost,
      points: row.points,
      goalsFor: row.goalsFor,
      goalsAgainst: row.goalsAgainst,
      goalDifference: row.goalDifference,
    },
  }));
  if (entries.some((e) => !e.club.source_id || !Number.isFinite(e.rank))) return null;
  return {
    league_slug: def.slug,
    season_year: seasonYear,
    group_id: 'overall',
    group_name: 'League Table',
    entries,
    last_synced_at: now,
  };
}

/** Dokumen soccer_clubs (kunci upsert: source.provider + source.club_id). */
function mapClub(team, def, now) {
  const name = str(team.name) || str(team.shortName) || `Team ${str(team.id)}`;
  const doc = {
    source: { provider: PROVIDER, club_id: str(team.id), uid: `fd:team:${str(team.id)}` },
    slug: slugify(name),
    name,
    display_name: name,
    short_display_name: str(team.shortName) || name,
    abbreviation: str(team.tla),
    country: str(team.area?.name) || def.country,
    logo: str(team.crest),
    logos: [],
    founded_year: finiteNum(team.founded),
    venue: team.venue ? { name: str(team.venue) } : undefined,
    active: true,
    roster: (team.squad || []).map((p) => ({
      source_id: str(p.id),
      display_name: str(p.name),
      position: str(p.position),
      nationality: str(p.nationality),
      date_of_birth: str(p.dateOfBirth),
    })),
    coach: team.coach?.name
      ? { source_id: str(team.coach.id), display_name: str(team.coach.name), nationality: str(team.coach.nationality) }
      : undefined,
    last_synced_at: now,
  };
  return doc;
}

module.exports = {
  PROVIDER,
  slugify,
  mapStatus,
  mapLeague,
  mapMatch,
  mapEvents,
  mapStandings,
  mapClub,
  ymd,
};
