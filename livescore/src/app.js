import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { isDateKey, utcDateKey } from './util.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const PUBLIC_DIR = path.resolve(here, '..', 'public');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
};

export const isLive = (m) => m.status === 'LIVE' || m.status === 'HALF_TIME';

/** Versi ringkas untuk daftar (tanpa kejadian). */
export function summary(m) {
  const { events, ...rest } = m; // eslint-disable-line no-unused-vars
  return rest;
}

/** Sidik jari perubahan: hanya kirim pertandingan yang berubah. */
export function signature(m) {
  return `${m.status}|${m.minute}|${m.score?.home}-${m.score?.away}|${m.events?.length ?? 0}`;
}

function sendJson(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(body));
}

async function serveStatic(res, pathname) {
  const rel = pathname === '/' ? 'index.html' : pathname.slice(1);
  const file = path.resolve(PUBLIC_DIR, rel);
  if (!file.startsWith(PUBLIC_DIR + path.sep)) {
    res.writeHead(403).end('Forbidden');
    return;
  }
  try {
    const body = await readFile(file);
    res.writeHead(200, {
      'Content-Type': MIME[path.extname(file)] || 'application/octet-stream',
      'Cache-Control': 'no-cache',
    });
    res.end(body);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' }).end('Tidak ditemukan');
  }
}

/**
 * @param {object} opts
 * @param {object} opts.aggregator   hasil createAggregator()
 * @param {number} [opts.tickMs]     interval pengecekan perubahan untuk SSE
 * @param {() => number} [opts.now]  sumber waktu (mudah diuji)
 * @param {object} [opts.log]
 */
export function createApp({ aggregator, tickMs = 10_000, now = () => Date.now(), log = console }) {
  const subs = new Map(); // ServerResponse -> dateKey
  const lastSig = new Map(); // dateKey -> Map(matchId -> signature)
  let ticking = false;

  function sendEvent(res, payload) {
    res.write(`data: ${JSON.stringify(payload)}\n\n`);
  }

  async function tick() {
    if (ticking || subs.size === 0) return;
    ticking = true;
    try {
      for (const date of new Set(subs.values())) {
        const { matches } = await aggregator.getMatches(date, { now: now() });
        let sigs = lastSig.get(date);
        if (!sigs) {
          sigs = new Map();
          lastSig.set(date, sigs);
        }
        const changed = [];
        for (const m of matches) {
          const s = signature(m);
          if (sigs.get(m.id) !== s) {
            sigs.set(m.id, s);
            changed.push(summary(m));
          }
        }
        if (changed.length) {
          const payload = { type: 'update', date, at: new Date(now()).toISOString(), matches: changed };
          for (const [res, d] of subs) if (d === date) sendEvent(res, payload);
        }
      }
    } catch (err) {
      log.error('[stream] tick gagal:', err.message);
    } finally {
      ticking = false;
    }
  }

  function handleStream(req, res, date) {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream; charset=utf-8',
      'Cache-Control': 'no-cache, no-transform',
      Connection: 'keep-alive',
      'X-Accel-Buffering': 'no',
    });
    res.write('retry: 5000\n\n');
    sendEvent(res, { type: 'hello', date, at: new Date(now()).toISOString() });
    subs.set(res, date);
    req.on('close', () => {
      subs.delete(res);
      const stillUsed = new Set(subs.values());
      for (const key of lastSig.keys()) if (!stillUsed.has(key)) lastSig.delete(key);
    });
  }

  async function handleApi(req, res, url) {
    const p = url.pathname;

    if (p === '/api/health') {
      return sendJson(res, 200, { ok: true, providers: aggregator.providers, time: new Date(now()).toISOString() });
    }

    if (p === '/api/matches') {
      const date = url.searchParams.get('date') || utcDateKey(now());
      if (!isDateKey(date)) return sendJson(res, 400, { error: 'Format date harus YYYY-MM-DD' });
      const { matches, warnings } = await aggregator.getMatches(date, { now: now() });
      let out = matches;
      if (url.searchParams.get('status') === 'live') out = matches.filter(isLive);
      return sendJson(res, 200, { date, count: out.length, matches: out.map(summary), warnings });
    }

    const detail = /^\/api\/matches\/(.+)$/.exec(p);
    if (detail) {
      const match = await aggregator.getMatch(decodeURIComponent(detail[1]), { now: now() });
      if (!match) return sendJson(res, 404, { error: 'Pertandingan tidak ditemukan' });
      return sendJson(res, 200, match);
    }

    if (p === '/api/stream') {
      const date = url.searchParams.get('date') || utcDateKey(now());
      if (!isDateKey(date)) return sendJson(res, 400, { error: 'Format date harus YYYY-MM-DD' });
      return handleStream(req, res, date);
    }

    return sendJson(res, 404, { error: 'Endpoint tidak ditemukan' });
  }

  const server = http.createServer(async (req, res) => {
    try {
      if (req.method !== 'GET' && req.method !== 'HEAD') {
        return sendJson(res, 405, { error: 'Method tidak diizinkan' });
      }
      const url = new URL(req.url, 'http://localhost');
      if (url.pathname.startsWith('/api/')) return await handleApi(req, res, url);
      return await serveStatic(res, url.pathname);
    } catch (err) {
      log.error('[http] error:', err);
      if (!res.headersSent) sendJson(res, 500, { error: 'Terjadi kesalahan di server' });
      else res.end();
    }
  });

  const pollTimer = setInterval(tick, tickMs);
  const heartbeat = setInterval(() => {
    for (const res of subs.keys()) res.write(': ping\n\n');
  }, 25_000);
  pollTimer.unref();
  heartbeat.unref();
  server.on('close', () => {
    clearInterval(pollTimer);
    clearInterval(heartbeat);
  });

  return server;
}
