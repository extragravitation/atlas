// System flags ruled in the decision log and shown on the system page and the map card.
// D-109 rule 3: until one written equilibrium test is applied to hydrostatic and rotation-curve
// sources, A2319 stays plotted, flagged with its source's statement quoted. The quote is checked at
// build against the package's own reading record, so the page can only quote what was read.
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, parseCSV } from './atlas.mjs';
import { decisionUrl, fileUrl } from './refs.mjs';

const FLAGS = [
  {
    dataset: 'aeg-d-xcop/v2', system: 'aeg-s-000183', decision: 'D-109', rule: 'rule 3',
    quote: 'clear evidence of a breakdown of hydrostatic equilibrium',
    // Where the Atlas read it: the package's reading record, row `order` 27.
    record: 'data/packages/aeg-d-xcop/v2/reading/hse_statements.csv', order: '27',
  },
];

let cache = null;
export function systemFlags() {
  if (cache) return cache;
  cache = {};
  for (const f of FLAGS) {
    const rows = parseCSV(fs.readFileSync(path.join(ROOT, f.record), 'utf8'));
    const row = rows.find((r) => r.order === f.order);
    if (!row || !row.quote.includes(f.quote)) throw new Error(`flags: "${f.quote}" not found in ${f.record} order ${f.order}`);
    // The statement cites Ghirardini et al. 2018 (\citep{ghirardini18}); D-109 names that paper.
    const cites = /ghirardini18/.test(row.quote) ? 'Ghirardini et al. 2018' : null;
    const where = `${row.source.split(', A&A')[0]}, ${row.file} l. ${row.line}`;
    cache[`${f.dataset}|${f.system}`] = {
      ...f, where, cites, source: row.source, recordUrl: fileUrl(f.record), decisionUrl: decisionUrl(f.decision),
    };
  }
  return cache;
}
export const flagFor = (dataset, system) => systemFlags()[`${dataset}|${system}`] || null;
