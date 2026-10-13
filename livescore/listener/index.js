'use strict';

// Listener football-data.org -> MongoDB (koleksi soccer_*).
// Jalankan terpisah dari API:  npm run listener
//
// Variabel environment:
//   FOOTBALL_DATA_TOKEN         (wajib) API key football-data.org
//   MONGODB_URL                 (wajib untuk produksi) koneksi MongoDB
//   LISTENER_LEAGUES            daftar slug, dipisah koma. Default: semua liga di leagues.js
//   LISTENER_SCOREBOARD_MS      interval jadwal/hasil            (default 60000)
//   LISTENER_DETAILS_MS         interval kejadian pertandingan   (default 60000)
//   LISTENER_STANDINGS_MS       interval klasemen                (default 1800000)
//   LISTENER_CATALOG_MS         interval katalog dan klub        (default 21600000)
//   FOOTBALL_DATA_MIN_INTERVAL_MS  jarak minimum antar request   (default 6500)

const { loadEnvConfig } = require('../config/env');
loadEnvConfig();

const { LEAGUES } = require('./leagues');
const { createFootballDataClient } = require('./footballData');
const { createSyncer } = require('./syncer');

const env = process.env;
const log = {
  info: (...a) => console.log(new Date().toISOString(), ...a),
  warn: (...a) => console.warn(new Date().toISOString(), ...a),
  error: (...a) => console.error(new Date().toISOString(), ...a),
};

function selectLeagues() {
  const wanted = (env.LISTENER_LEAGUES || Object.keys(LEAGUES).join(','))
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
  const unknown = wanted.filter((slug) => !LEAGUES[slug]);
  if (unknown.length) throw new Error(`Liga tidak dikenal di leagues.js: ${unknown.join(', ')}`);
  return wanted.map((slug) => LEAGUES[slug]);
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// connection.asPromise() di Mongoose 6 ikut resolve saat koneksi gagal,
// jadi kita menunggu event 'open' atau 'error' secara eksplisit.
function waitForMongo(mongoose, timeoutMs = 20000) {
  if (mongoose.connection.readyState === 1) return Promise.resolve();
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('timeout menghubungkan ke MongoDB')), timeoutMs);
    mongoose.connection.once('open', () => {
      clearTimeout(timer);
      resolve();
    });
    mongoose.connection.once('error', (err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

function startLoop(name, everyMs, task) {
  let stopped = false;
  (async () => {
    while (!stopped) {
      try {
        const result = await task();
        if (result?.status && result.status !== 'ok') log.warn(`[listener] ${name}: ${result.status} ${result.error || result.reason || ''}`.trim());
        else log.info(`[listener] ${name}: ${JSON.stringify(result || {})}`);
      } catch (err) {
        log.error(`[listener] ${name} gagal tak terduga:`, err.message);
      }
      await sleep(everyMs);
    }
  })();
  return () => {
    stopped = true;
  };
}

async function main() {
  const token = env.FOOTBALL_DATA_TOKEN;
  if (!token) {
    log.error('FOOTBALL_DATA_TOKEN belum diatur. Dapatkan API key gratis di football-data.org lalu set variabel ini.');
    process.exit(1);
  }

  const { createMongoStore } = require('./mongoStore');
  const mongoose = require('../database');
  await waitForMongo(mongoose);

  const leagues = selectLeagues();
  const client = createFootballDataClient({
    token,
    minIntervalMs: Number(env.FOOTBALL_DATA_MIN_INTERVAL_MS || 6500),
  });
  const syncer = createSyncer({ client, store: createMongoStore(), leagues, log });

  const every = {
    scoreboard: Number(env.LISTENER_SCOREBOARD_MS || 60000),
    details: Number(env.LISTENER_DETAILS_MS || 60000),
    standings: Number(env.LISTENER_STANDINGS_MS || 30 * 60000),
    catalog: Number(env.LISTENER_CATALOG_MS || 6 * 3600000),
  };

  const stops = [];
  leagues.forEach((def, i) => {
    // Sebar awal supaya request tidak menumpuk saat start.
    const offset = i * 1000;
    stops.push(startLoop(`${def.slug} catalog`, every.catalog, async () => {
      await sleep(offset);
      const catalog = await syncer.syncCatalog(def);
      const clubs = await syncer.syncClubs(def);
      return { catalog: catalog.status, clubs: clubs.status, clubCount: clubs.clubs ?? 0 };
    }));
    stops.push(startLoop(`${def.slug} standings`, every.standings, () => syncer.syncStandings(def)));
    stops.push(startLoop(`${def.slug} scoreboard`, every.scoreboard, () => syncer.syncScoreboard(def)));
    stops.push(startLoop(`${def.slug} details`, every.details, () => syncer.syncDetails(def)));
  });

  log.info(`[listener] berjalan untuk: ${leagues.map((l) => l.slug).join(', ')}`);

  const shutdown = async (signal) => {
    log.info(`[listener] ${signal} diterima, berhenti...`);
    stops.forEach((stop) => stop());
    await mongoose.disconnect().catch(() => {});
    process.exit(0);
  };
  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
}

if (require.main === module) {
  main().catch((err) => {
    log.error('Listener gagal dijalankan:', err.message);
    process.exit(1);
  });
}

module.exports = { selectLeagues };
