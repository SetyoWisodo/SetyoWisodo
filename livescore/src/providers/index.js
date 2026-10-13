import { createMockProvider } from './mock.js';
import { createFootballDataProvider } from './footballData.js';

/**
 * Membuat daftar provider dari environment.
 *   PROVIDERS=mock                  (default)
 *   PROVIDERS=footballdata          (butuh FOOTBALL_DATA_TOKEN)
 *   PROVIDERS=mock,footballdata     (digabung)
 */
export function createProvidersFromEnv(env = process.env, log = console) {
  const names = (env.PROVIDERS || 'mock').split(',').map((s) => s.trim()).filter(Boolean);
  const providers = [];
  for (const name of names) {
    if (name === 'mock') {
      providers.push(createMockProvider());
    } else if (name === 'footballdata') {
      if (!env.FOOTBALL_DATA_TOKEN) {
        log.warn('[provider] footballdata dilewati: FOOTBALL_DATA_TOKEN belum diatur');
        continue;
      }
      providers.push(createFootballDataProvider({ token: env.FOOTBALL_DATA_TOKEN, base: env.FOOTBALL_DATA_BASE }));
    } else {
      throw new Error(`Provider tidak dikenal: ${name}`);
    }
  }
  if (providers.length === 0) {
    log.warn('[provider] tidak ada provider aktif, memakai mock');
    providers.push(createMockProvider());
  }
  return providers;
}
