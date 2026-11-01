// One dataset's payload for the browser: exact values from the package tables (columnar).
import { loadAtlas, payload } from '../../lib/atlas.mjs';
import { isLensing, kindWords } from '../../lib/lensing.mjs';

export function getStaticPaths() {
  return loadAtlas().datasets.map((d) => ({ params: { file: `${d.name}-${d.version}` }, props: { key: d.key } }));
}

export function GET({ props }) {
  const d = loadAtlas().datasets.find((x) => x.key === props.key);
  const out = payload(d);
  // Lenses: the kind in plain words for the map card and tooltips (both layers), keyed by system. The systems
  // themselves stay exactly as in the package table (aeg.site_check compares them).
  if (isLensing(d) && out.systems) out.kind_words = Object.fromEntries(d.systems.rows.map((row, i) => [row.system_id, kindWords(row, out.systems[i].properties)]));
  return new Response(JSON.stringify(out), { headers: { 'Content-Type': 'application/json' } });
}
