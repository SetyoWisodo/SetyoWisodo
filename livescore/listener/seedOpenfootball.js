'use strict';

// Pengisi awal (seed) database dari openfootball/football.json (CC0).
// Hanya untuk musim yang SUDAH selesai. Data ini tidak live.
//
// Aturan musim:
// - Liga yang juga dicakup listener football-data (live: true): musim yang sama atau lebih baru
//   dari musim aktif di soccer_leagues ditolak. Liga harus sudah ada di database.
// - Liga seed saja: musim dianggap selesai jika sudah lewat 1 Juli tahun berakhirnya.
//   Dokumen soccer_leagues dibuat dengan source.provider = openfootball agar API bisa melayaninya.
//   Dokumen football-data tidak pernah ditimpa.
//
// Pemakaian:
//   npm run seed:openfootball -- --season 2025-26
//   npm run seed:openfootball -- --season 2025-26 --leagues eng.1,ita.1
//   npm run seed:openfootball -- --season 2025-26 --dir /path/ke/clone/football.json

const fs = require('fs');
const path = require('path');
const openfootball = require('./openfootball');

const SEED_INDEX = new Map(openfootball.SEED_LEAGUES.map((l, i) => [l.slug, i]));
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

/** Ubah "2025-26" menjadi { year: 2025 }. Melempar error jika format salah. */
function parseSeason(season) {
  const m = /^(\d{4})-(\d{2})$/.exec(String(season || ''));
  if (!m || (Number(m[1]) + 1) % 100 !== Number(m[2])) {
    throw new Error(`format musim harus YYYY-YY, contoh 2025-26 (diterima: ${season})`);
  }
  return { year: Number(m[1]) };
}

/** Musim selesai jika sudah lewat 1 Juli tahun berakhirnya (contoh 2025-26 selesai setelah 2026-07-01). */
function seasonEnded(seasonYear, now) {
  return now.getTime() >= Date.UTC(seasonYear + 1, 6, 1);
}

/**
 * Seed satu liga untuk satu musim.
 * @param {object} opts
 * @param {object} opts.store      store (mongoStore atau memoryStore)
 * @param {object} opts.def        entri dari openfootball.SEED_LEAGUES
 * @param {string} opts.season     "2025-26"
 * @param {string} [opts.dir]      folder lokal hasil clone openfootball/football.json
 * @param {Function} [opts.fetchImpl]
 * @param {Date} [opts.now]
 */
async function seedSeason({ store, def, season, dir, fetchImpl = globalThis.fetch, now = new Date() }) {
  const { year: seasonYear } = parseSeason(season);
  const existing = await store.getLeague(def.slug);
  const isFootballData = existing?.source?.provider === 'football-data';

  if (def.live) {
    // Liga live: musim aktif dari database menjadi batas.
    const activeYear = existing?.season?.year;
    if (!activeYear) {
      throw new Error(`${def.slug} belum punya musim aktif di database. Jalankan listener (katalog) dulu.`);
    }
    if (seasonYear >= activeYear) {
      throw new Error(`${season} adalah musim aktif atau belum selesai (aktif: ${activeYear}). Seeder hanya untuk musim lampau.`);
    }
  } else {
    if (isFootballData) {
      throw new Error(`${def.slug} sudah dikelola football-data; seed openfootball tidak boleh menimpanya`);
    }
    if (!seasonEnded(seasonYear, now)) {
      throw new Error(`${season} belum selesai pada ${now.toISOString().slice(0, 10)}. Seeder hanya untuk musim lampau.`);
    }
  }

  const loaded = await loadSeasonFile({ dir, fetchImpl, season, code: def.code });
  if (!loaded) throw new Error(`file musim ${season} untuk ${def.code} tidak ditemukan`);

  const { matches, stats } = openfootball.mapOpenfootballSeason(loaded.json, {
    leagueSlug: def.slug,
    leagueName: def.name,
    seasonYear,
    tz: def.tz,
    now,
  });

  if (!def.live) {
    // Dokumen liga seed: simpan musim terbaru yang sudah di-seed, jangan turunkan.
    const keepYear = Math.max(existing?.season?.year || 0, seasonYear);
    await store.upsertLeague(def.slug, {
      slug: def.slug,
      name: def.name,
      abbreviation: def.name,
      country: def.country,
      kind: 'club',
      active: true,
      sort_order: 1000 + SEED_INDEX.get(def.slug),
      logo: '',
      source: { provider: openfootball.PROVIDER, source_id: def.code },
      season: { year: keepYear, display_name: `${keepYear}-${String((keepYear + 1) % 100).padStart(2, '0')}`, current: false },
    });
  }

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

/** Pilih liga dari registri. Tanpa --leagues, semua liga dipakai. */
function selectLeagues(list) {
  if (!list) return openfootball.SEED_LEAGUES.slice();
  const bySlug = new Map(openfootball.SEED_LEAGUES.map((l) => [l.slug, l]));
  return list.split(',').map((s) => s.trim()).filter(Boolean).map((slug) => {
    const def = bySlug.get(slug);
    if (!def) throw new Error(`liga tidak dikenal: ${slug}`);
    return def;
  });
}

async function main(argv = process.argv.slice(2)) {
  require('../config/env').loadEnvConfig();
  const args = parseArgs(argv);
  if (!args.season) throw new Error('wajib: --season 2025-26');
  const defs = selectLeagues(args.leagues);

  const { createMongoStore, waitForMongo } = require('./mongoStore');
  const mongoose = require('../database');
  await waitForMongo(mongoose);
  const store = createMongoStore();

  let failed = 0;
  try {
    for (const def of defs) {
      try {
        const r = await seedSeason({ store, def, season: args.season, dir: args.dir });
        console.log(`[seed] ${r.slug} ${r.season} dari ${r.file}: ${r.mapped} pertandingan, ${r.events} kejadian, ${r.skipped} dilewati, ${r.withoutTime} tanpa jam`);
      } catch (err) {
        failed++;
        console.error(`[seed] ${def.slug} gagal: ${err.message}`);
      }
    }
  } finally {
    await mongoose.disconnect().catch(() => {});
  }
  if (failed) process.exitCode = 1;
}

if (require.main === module) {
  main().catch((err) => {
    console.error('Seed gagal:', err.message);
    process.exit(1);
  });
}

module.exports = { seedSeason, loadSeasonFile, parseArgs, parseSeason, seasonEnded, selectLeagues };
