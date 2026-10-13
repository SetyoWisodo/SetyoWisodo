// Menggabungkan beberapa provider menjadi satu sumber data.
// Kegagalan satu provider tidak menggagalkan provider lain; error dilaporkan sebagai warning.

const byKickoff = (a, b) => (a.kickoff || '').localeCompare(b.kickoff || '') || a.id.localeCompare(b.id);

export function createAggregator({ providers }) {
  return {
    providers: providers.map((p) => p.name),

    async getMatches(dateKey, opts = {}) {
      const results = await Promise.allSettled(providers.map((p) => p.getMatches(dateKey, opts)));
      const merged = new Map();
      const warnings = [];
      results.forEach((r, i) => {
        if (r.status === 'fulfilled') {
          for (const m of r.value) merged.set(m.id, m);
        } else {
          warnings.push(`${providers[i].name}: ${r.reason?.message || 'gagal'}`);
        }
      });
      return { matches: [...merged.values()].sort(byKickoff), warnings };
    },

    async getMatch(id, opts = {}) {
      const provider = providers.find((p) => p.owns(id));
      if (!provider) return null;
      return provider.getMatch(id, opts);
    },
  };
}
