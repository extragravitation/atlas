// Build-time reader for the strong-lensing package (aeg-d-strong-lensing): the two reported checks,
// the funnel from lenses read to lenses plotted, and the cosmology each lens's observed side used.
// Every number comes from the package files; nothing here is typed in by hand.
import fs from 'node:fs';
import path from 'node:path';
import { parseECSV } from './ecsv.mjs';
import { parseCSV } from './atlas.mjs';

const cache = new Map();
const read = (dir, f) => fs.readFileSync(path.join(dir, f), 'utf8');

export function isLensing(d) { return d.measurements.rows.some((r) => r.r_kind === 'projected'); }

function stats(v, within) {
  const s = [...v].sort((a, b) => a - b), n = s.length;
  const mean = s.reduce((a, b) => a + b, 0) / n;
  // Population standard deviation (divide by n), as in the package's RESULT_SUMMARY.md.
  const sd = n > 1 ? Math.sqrt(s.reduce((a, b) => a + (b - mean) ** 2, 0) / n) : null;
  const median = n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
  return { n, min: s[0], median, max: s[n - 1], mean, sd, within: within ? s.filter((x) => Math.abs(x - 1) <= within + 1e-12).length : null };
}

// Groups rows by a key, in first-seen order, with summary statistics of the ratio column.
function grouped(rows, key, within) {
  const out = [];
  for (const r of rows) { let g = out.find((x) => x.key === key(r)); if (!g) { g = { key: key(r), rows: [] }; out.push(g); } g.rows.push(r); }
  for (const g of out) g.stats = stats(g.rows.map((r) => r.ratio), within);
  return out;
}

export function lensPackage(d) {
  if (cache.has(d.key)) return cache.get(d.key);
  const dir = d.dir;
  const formula = parseECSV(read(dir, 'checks/formula_check.ecsv'));
  const profile = parseECSV(read(dir, 'checks/profile_step.ecsv'));
  const notTab = d.checks['not_tabulated.csv'] || [];
  const adjudicated = [...parseCSV(read(dir, 'reading/adjudicated_inputs.csv')), ...parseCSV(read(dir, 'reading/adjudicated_supplement.csv'))];

  // Funnel. "Read" is the adjudicated reading set: every lens with a value read at source and adjudicated.
  const readSet = new Set(adjudicated.filter((r) => r.system !== '(record)').map((r) => r.scope + '\u0000' + r.system));
  const sys = d.systems.rows.map((s) => ({ s, p: JSON.parse(s.properties || '{}') }));
  const below = sys.filter(({ s }) => s.redshift !== null && s.redshift < 0.30);
  const plotted = sys.filter(({ p }) => p.status === 'plotted');
  const recorded = sys.filter(({ p }) => p.status !== 'plotted');
  if (readSet.size !== sys.length + notTab.length) throw new Error(`lensing funnel: ${readSet.size} lenses in the adjudicated readings, but ${sys.length} tabulated + ${notTab.length} not tabulated`);
  if (below.length !== sys.length) throw new Error('lensing funnel: a tabulated lens is not below z = 0.30');
  const byScope = (list) => { const m = {}; for (const { p } of list) m[p.scope] = (m[p.scope] || 0) + 1; return m; };
  const reasonGroups = (list) => {
    const m = new Map();
    for (const { s, p } of list) { const k = (p.reasons_not_plotted || []).join('; '); if (!m.has(k)) m.set(k, []); m.get(k).push({ id: s.system_id, name: s.name_in_source, scope: p.scope, cls: s.class_in_source }); }
    return [...m.entries()].map(([reason, items]) => ({ reason, items }));
  };
  const notTabGroups = (() => { const m = new Map(); for (const r of notTab) { const k = r.scope + '\u0000' + r.reason; if (!m.has(k)) m.set(k, { scope: r.scope, reason: r.reason, names: [] }); m.get(k).names.push(r.system); } return [...m.values()]; })();
  const funnel = { read: readSet.size, below: below.length, plotted: plotted.length, recorded: recorded.length, notTabulated: notTab.length,
    plottedByScope: byScope(plotted), recordedGroups: reasonGroups(recorded), notTabGroups };

  const out = {
    formula, profile, adjudicated, funnel,
    formulaGroups: grouped(formula.rows, (r) => `${r.record_m_e}|${r.record_theta}`, null),
    profileGroups: grouped(profile.rows, (r) => r.imf, 0.10),
    formulaMeta: formula.meta, profileMeta: profile.meta,
  };
  cache.set(d.key, out);
  return out;
}

// The cosmology rows the readers recorded for a lens's observed-side record (H0, Ω_m, Ω_Λ or a named
// cosmology), with their location and quote; lens-specific rows first, then the record-level ones.
export function cosmologyRows(pkg, scope, name, record) {
  const q = ['H0', 'Om', 'OL', 'cosmology'];
  const rows = pkg.adjudicated.filter((r) => r.record === record && q.includes(r.quantity) && r.scope === scope && (r.system === name || r.system === '(record)'));
  const own = rows.filter((r) => r.system === name);
  return own.length ? own : rows;
}
