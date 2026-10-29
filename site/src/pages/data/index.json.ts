// Index of the browser payloads, one per dataset version (built from the packages).
import { loadAtlas } from '../../lib/atlas.mjs';

export function GET() {
  const { datasets } = loadAtlas();
  return new Response(JSON.stringify({ datasets: datasets.map((d) => ({ key: d.key, file: `${d.name}-${d.version}.json` })) }), { headers: { 'Content-Type': 'application/json' } });
}
