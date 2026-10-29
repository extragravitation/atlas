// One dataset's payload for the browser: exact values from the package tables (columnar).
import { loadAtlas, payload } from '../../lib/atlas.mjs';

export function getStaticPaths() {
  return loadAtlas().datasets.map((d) => ({ params: { file: `${d.name}-${d.version}` }, props: { key: d.key } }));
}

export function GET({ props }) {
  const d = loadAtlas().datasets.find((x) => x.key === props.key);
  return new Response(JSON.stringify(payload(d)), { headers: { 'Content-Type': 'application/json' } });
}
