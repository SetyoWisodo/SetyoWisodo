'use strict';

// Pengisi awal (seed) database dari openfootball/football.json (CC0).
// Hanya untuk musim yang SUDAH selesai. Musim aktif tetap diurus oleh listener
// football-data.org, jadi seeder menolak menulis musim aktif agar tidak ada dua sumber
// untuk pertandingan yang sama.
//
// Pemakaian:
//   npm run seed:openfootball -- --season 2025-26
//   npm run seed:openfootball -- --season 2025-26 --dir /path/ke/clone/football.json
//   npm run seed:openfootball -- --season 2025-26 --leagues eng.1

const fs = require('fs');
const path = require('path');
const { LEAGUES } = require('./leagues');
const openfootball = require('./openfootball');

const RAW_BASE = 'https://raw.githubusercontent.com/openfootball/football.json/master';

/** Ambil file musim: versi -full (ada gol dan kartu) lebih dulu, lalu versi biasa. */
async function loadSeasonFile({ dir, fetchImpl, season, code }) {
  for (const name of [`${code}-full.json`, `${code}.json`]) {
    if (dir) {
      const file = path.join(dir, season, name);
      if (!fs.existsSync(file)) continue;
      return { json: JSON.parse(fs.readFileSync(file, 'utf8')), file: name, source: file };
    }
    const url = `${RAW_BASE}/${season}/${name}`;
    const res = await fetchImpl(url);
    if (res.status === 404) continue;
    if (!res.ok) throw new Error(`gagal mengunduh ${url}: HTTP ${res.status}`);
    return { json: JSON.parse(await res.text()), file: name, source: url };
  }
  return null;
}

/**
 * Seed satu liga untuk satu musim.
 * @param {object} opts
 * @param {object} opts.store      store (mongoStore atau memoryStore)
 * @param {object} opts.def        definisi liga dari leagues.js
 * @param {string} opts.season     "2025-26"
 * @param {string} [opts.dir]      folder lokal hasil clone openfootball/football.json
 * @param {Function} [opts.fetchImpl]
 * @param {Date} [opts.now]
 */
async function seedSeason({ store, def, season, dir, fetchImpl = globalThis.fetch, now = new Date() }) {
  if (!def.openfootball) throw new Error(`${def.slug} belum punya konfigurasi openfootball`);
  const m = /^(\d{4})-(\d{2})$/.exec(String(season || ''));
  if (!m || (Number(m[1]) + 1) % 100 !== Number(m[2])) {
    throw new Error(`format musim harus YYYY-YY, contoh 2025-26 (diterima: ${season})`);
  }
  const seasonYear = Number(m[1]);

  // Syarat: liga sudah terdaftar oleh listener (katalog), dan musim ini harus lampau.
  const league = await store.getLeague(def.slug);
  const activeYear = league?.season?.year;
  if (!activeYear) {
    throw new Error(`${def.slug} belum punya musim aktif di database. Jalankan listener (katalog) dulu.`);
  }
  if (seasonYear >= activeYear) {
    throw new Error(`${season} adalah musim aktif atau belum selesai (aktif: ${activeYear}). Seeder hanya untuk musim lampau.`);
  }

  const loaded = await loadSeasonFile({ dir, fetchImpl, season, code: def.openfootball.code });
  if (!loaded) throw new Error(`file musim ${season} untuk ${def.openfootball.code} tidak ditemukan`);

  const { matches, stats } = openfootball.mapOpenfootballSeason(loaded.json, {
    leagueSlug: def.slug,
    leagueName: def.name,
    seasonYear,
    tz: def.openfootball.tz,
    now,
  });

  for (const { match, events } of matches) {
    await store.upsertMatch(def.slug, match);
    if (events.length) await store.upsertEvents(events);
    await store.setPlayByPlayAvailable(def.slug, match.source.event_id, events.length > 0);
  }
  return { slug: def.slug, season, source: loaded.source, file: loaded.file, ...stats };
}

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (!key.startsWith('--')) throw new Error(`argumen tidak dikenal: ${key}`);
    const value = argv[i + 1];
    if (value === undefined || value.startsWith('--')) throw new Error(`${key} butuh nilai`);
    out[key.slice(2)] = value;
    i++;
  }
  return out;
}

async function main(argv = process.argv.slice(2)) {
  require('../config/env').loadEnvConfig();
  const args = parseArgs(argv);
  if (!args.season) throw new Error('wajib: --season 2025-26');
  const slugs = args.leagues ? args.leagues.split(',').map((s) => s.trim()) : Object.keys(LEAGUES);
  const defs = slugs.map((slug) => {
    if (!LEAGUES[slug]) throw new Error(`liga tidak dikenal: ${slug}`);
    return LEAGUES[slug];
  });

  const { createMongoStore, waitForMongo } = require('./mongoStore');
  const mongoose = require('../database');
  await waitForMongo(mongoose);
  const store = createMongoStore();

  try {
    for (const def of defs) {
      try {
        const r = await seedSeason({ store, def, season: args.season, dir: args.dir });
        console.log(`[seed] ${r.slug} ${r.season} dari ${r.file}: ${r.mapped} pertandingan, ${r.events} kejadian, ${r.skipped} dilewati, ${r.withoutTime} tanpa jam`);
      } catch (err) {
        console.error(`[seed] ${def.slug} gagal: ${err.message}`);
        process.exitCode = 1;
      }
    }
  } finally {
    await mongoose.disconnect().catch(() => {});
  }
}

if (require.main === module) {
  main().catch((err) => {
    console.error('Seed gagal:', err.message);
    process.exit(1);
  });
}

module.exports = { seedSeason, loadSeasonFile, parseArgs };
