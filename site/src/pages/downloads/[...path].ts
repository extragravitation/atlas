// Downloads: the package tables exactly as committed (ECSV), a plain CSV copy of each, and the
// package descriptor and checksums. Generated at build from the repository; never edited by hand.
import fs from 'node:fs';
import path from 'node:path';
import { loadAtlas } from '../../lib/atlas.mjs';
import { parseECSV, toCSV } from '../../lib/ecsv.mjs';

export function getStaticPaths() {
  const out = [];
  for (const d of loadAtlas().datasets) {
    for (const f of d.files) {
      const stem = f.replace(/^tables\//, '').replace(/\.ecsv$/, '');
      out.push({ params: { path: `${d.name}/${d.version}/${stem}.ecsv` }, props: { file: path.join(d.dir, f), kind: 'ecsv' } });
      out.push({ params: { path: `${d.name}/${d.version}/${stem}.csv` }, props: { file: path.join(d.dir, f), kind: 'csv' } });
    }
    for (const f of ['datapackage.json', 'checksums.sha256', 'sources.json']) out.push({ params: { path: `${d.name}/${d.version}/${f}` }, props: { file: path.join(d.dir, f), kind: 'raw' } });
  }
  return out;
}

export function GET({ props }) {
  const text = fs.readFileSync(props.file, 'utf8');
  if (props.kind === 'csv') { const t = parseECSV(text); return new Response(toCSV(t.columns, t.rows), { headers: { 'Content-Type': 'text/csv; charset=utf-8' } }); }
  const type = props.file.endsWith('.json') ? 'application/json' : 'text/plain; charset=utf-8';
  return new Response(text, { headers: { 'Content-Type': type } });
}
