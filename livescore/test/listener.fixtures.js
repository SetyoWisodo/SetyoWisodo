'use strict';

// Fixture yang meniru bentuk payload football-data.org v4 (disederhanakan).

const LEAGUE = {
  slug: 'eng.1',
  fd: { code: 'PL', id: 2021 },
  name: 'English Premier League',
  abbreviation: 'Premier League',
  country: 'England',
  kind: 'club',
  sort_order: 10,
};

const SEASON = { id: 1, startDate: '2026-08-22', endDate: '2027-05-30', currentMatchday: 7 };

const team = (id, name, tla) => ({ id, name, shortName: name.replace(' FC', ''), tla, crest: `https://crests.example/${id}.png` });

const HOME = team(57, 'Arsenal FC', 'ARS');
const AWAY = team(61, 'Chelsea FC', 'CHE');

function match(overrides = {}) {
  return {
    id: 9001,
    utcDate: '2026-10-13T14:00:00Z',
    status: 'SCHEDULED',
    matchday: 7,
    stage: 'REGULAR_SEASON',
    competition: { id: 2021, name: 'Premier League', code: 'PL' },
    season: SEASON,
    homeTeam: HOME,
    awayTeam: AWAY,
    score: { winner: null, duration: 'REGULAR', fullTime: { home: null, away: null }, halfTime: { home: null, away: null } },
    lastUpdated: '2026-10-13T12:00:00Z',
    ...overrides,
  };
}

const DETAIL_FINISHED = {
  ...match({
    status: 'FINISHED',
    score: { winner: 'HOME_TEAM', duration: 'REGULAR', fullTime: { home: 2, away: 1 }, halfTime: { home: 1, away: 0 } },
  }),
  goals: [
    { minute: 33, injuryTime: null, type: 'REGULAR', team: HOME, scorer: { id: 101, name: 'Bukayo Saka' }, assist: null, score: { home: 1, away: 0 } },
    { minute: 61, injuryTime: null, type: 'OWN', team: AWAY, scorer: { id: 202, name: 'Defender X' }, assist: null, score: { home: 2, away: 0 } },
    { minute: 88, injuryTime: 2, type: 'REGULAR', team: AWAY, scorer: { id: 203, name: 'Striker Y' }, assist: null, score: { home: 2, away: 1 } },
  ],
  bookings: [
    { minute: 40, injuryTime: null, team: AWAY, player: { id: 301, name: 'Enzo F' }, card: 'YELLOW_CARD' },
    { minute: 77, injuryTime: null, team: HOME, player: { id: 302, name: 'Declan R' }, card: 'YELLOW_RED_CARD' },
  ],
  substitutions: [
    { minute: 70, injuryTime: null, team: HOME, playerOut: { id: 401, name: 'Martinelli' }, playerIn: { id: 402, name: 'Trossard' } },
  ],
};

const STANDINGS = {
  competition: { id: 2021, code: 'PL' },
  standings: [
    {
      stage: 'REGULAR_SEASON',
      type: 'TOTAL',
      table: [
        { position: 1, team: HOME, playedGames: 7, won: 5, draw: 1, lost: 1, points: 16, goalsFor: 15, goalsAgainst: 6, goalDifference: 9 },
        { position: 2, team: AWAY, playedGames: 7, won: 4, draw: 2, lost: 1, points: 14, goalsFor: 12, goalsAgainst: 7, goalDifference: 5 },
      ],
    },
    { stage: 'REGULAR_SEASON', type: 'HOME', table: [] },
  ],
};

const COMPETITION = {
  id: 2021,
  name: 'Premier League',
  code: 'PL',
  emblem: 'https://crests.example/pl.png',
  currentSeason: SEASON,
};

const TEAMS = {
  count: 1,
  teams: [
    {
      id: 57,
      name: 'Arsenal FC',
      shortName: 'Arsenal',
      tla: 'ARS',
      crest: 'https://crests.example/57.png',
      venue: 'Emirates Stadium',
      founded: 1886,
      area: { name: 'England' },
      coach: { id: 900, name: 'Mikel A', nationality: 'Spain' },
      squad: [{ id: 101, name: 'Bukayo Saka', position: 'Offence', nationality: 'England', dateOfBirth: '2001-09-05' }],
    },
  ],
};

module.exports = { LEAGUE, SEASON, HOME, AWAY, match, DETAIL_FINISHED, STANDINGS, COMPETITION, TEAMS };
