'use strict';

// Registri liga yang didukung listener.
// slug : slug publik di API (eng.1, esp.1). Stabil, jangan diubah.
// fd   : identitas kompetisi di football-data.org (code dan id numerik).
//
// Tambah liga baru satu per satu sesuai BUSINESS-CONTEXT.md (rollout per negara).
const LEAGUES = {
  'eng.1': {
    slug: 'eng.1',
    fd: { code: 'PL', id: 2021 },
    name: 'English Premier League',
    abbreviation: 'Premier League',
    country: 'England',
    kind: 'club',
    sort_order: 10,
  },
  'esp.1': {
    slug: 'esp.1',
    fd: { code: 'PD', id: 2014 },
    name: 'LaLiga',
    abbreviation: 'LaLiga',
    country: 'Spain',
    kind: 'club',
    sort_order: 20,
  },
};

module.exports = { LEAGUES };
