import { createApp } from './app.js';
import { createAggregator } from './aggregator.js';
import { createProvidersFromEnv } from './providers/index.js';

const port = Number(process.env.PORT || 3000);
const host = process.env.HOST || '0.0.0.0';

const aggregator = createAggregator({ providers: createProvidersFromEnv(process.env) });
const server = createApp({ aggregator });

server.listen(port, host, () => {
  console.log(`Skor Langsung berjalan di http://${host}:${port} (provider: ${aggregator.providers.join(', ')})`);
});
