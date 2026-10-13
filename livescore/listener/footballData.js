'use strict';

// Client football-data.org v4 dengan throttle, timeout, dan retry terbatas.
// Tier gratis membatasi sekitar 10 request per menit, jadi semua request
// diantrekan dengan jarak minimum `minIntervalMs`.

const DEFAULT_BASE = 'https://api.football-data.org/v4';

class FootballDataError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'FootballDataError';
    this.status = status;
  }
}

function createFootballDataClient({
  token,
  base = DEFAULT_BASE,
  fetchImpl = globalThis.fetch,
  minIntervalMs = 6500,
  timeoutMs = 15000,
  maxRetries = 2,
  now = () => Date.now(),
  sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms)),
} = {}) {
  if (!token) throw new Error('FOOTBALL_DATA_TOKEN belum diatur');

  let lastAt = -Infinity;
  let queue = Promise.resolve();

  // Semua request berjalan berurutan dengan jarak minimum antar request.
  function throttled(task) {
    const run = async () => {
      const wait = lastAt + minIntervalMs - now();
      if (wait > 0) await sleep(wait);
      lastAt = now();
      return task();
    };
    const result = queue.then(run, run);
    queue = result.catch(() => {});
    return result;
  }

  async function attempt(path) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const res = await fetchImpl(base + path, {
        headers: { 'X-Auth-Token': token, Accept: 'application/json' },
        signal: controller.signal,
      });
      if (!res.ok) {
        throw new FootballDataError(`HTTP ${res.status} pada ${path}`, res.status);
      }
      const type = res.headers?.get?.('content-type') || '';
      if (type && !type.includes('json')) {
        throw new FootballDataError(`Content-Type tidak valid pada ${path}: ${type}`, res.status);
      }
      return await res.json();
    } finally {
      clearTimeout(timer);
    }
  }

  async function get(path) {
    return throttled(async () => {
      for (let i = 0; ; i++) {
        try {
          return await attempt(path);
        } catch (err) {
          const retryable = !(err instanceof FootballDataError) || err.status === 429 || err.status >= 500;
          if (!retryable || i >= maxRetries) throw err;
          // Batas tier gratis (429) memakai backoff lebih lama.
          const delay = err.status === 429 ? 60000 : 1000 * 2 ** i;
          await sleep(delay);
        }
      }
    });
  }

  return {
    competition: (code) => get(`/competitions/${encodeURIComponent(code)}`),
    teams: (code) => get(`/competitions/${encodeURIComponent(code)}/teams`),
    standings: (code) => get(`/competitions/${encodeURIComponent(code)}/standings`),
    matches: (code, dateFrom, dateTo) =>
      get(`/competitions/${encodeURIComponent(code)}/matches?dateFrom=${dateFrom}&dateTo=${dateTo}`),
    match: (id) => get(`/matches/${encodeURIComponent(id)}`),
  };
}

module.exports = { createFootballDataClient, FootballDataError, DEFAULT_BASE };
