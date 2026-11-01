// Build-time access to the repository's data: packages, registry, systems. Everything the site
// shows is read from these files; nothing is typed into the site by hand.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseECSV } from './ecsv.mjs';
import { names, parse } from '../formula.mjs';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const PKG = path.join(ROOT, 'data/packages');

const read = (p) => fs.readFileSync(p, 'utf8');
const readIf = (p) => (fs.existsSync(p) ? read(p) : null);

// Columns the site needs from every measurement row (when present).
const CORE = ['measurement_id', 'system_id', 'kind', 'limit', 'channel', 'method_class', 'method', 'r_kpc', 'r_kind', 'g_obs', 'g_obs_err_lo', 'g_obs_err_hi',
  'g_bar', 'g_bar_err_lo', 'g_bar_err_hi', 'g_bar_stars', 'g_bar_stars_disk', 'g_bar_stars_bulge', 'g_bar_gas_cold', 'g_bar_gas_hot',
  'stars_status', 'gas_cold_status', 'gas_hot_status', 'assumptions', 'adjustable', 'quality_source', 'source_ref', 'flags', 'known_issues',
  'plotted', 'role', 'not_plotted_reason'];

let cache = null;

// Minimal CSV reader for the packages' checks/ files (no embedded newlines; quotes allowed).
export function parseCSV(text) {
  const lines = text.split(/\r?\n/).filter((l) => l.length);
  const split = (l) => { const out = []; let cur = '', q = false; for (const ch of l) { if (ch === '"') q = !q; else if (ch === ',' && !q) { out.push(cur); cur = ''; } else cur += ch; } out.push(cur); return out; };
  const head = split(lines[0]);
  return lines.slice(1).map((l) => Object.fromEntries(split(l).map((v, i) => [head[i], v])));
}

export function loadAtlas() {
  if (cache) return cache;
  const registry = JSON.parse(read(path.join(ROOT, 'data/assumptions.json')));
  const datasets = [];
  for (const name of fs.readdirSync(PKG).sort()) {
    for (const version of fs.readdirSync(path.join(PKG, name)).sort()) {
      const dir = path.join(PKG, name, version);
      const mfile = path.join(dir, 'tables/measurements.ecsv');
      if (!fs.existsSync(mfile)) continue;
      const key = `${name}/${version}`;
      const dp = JSON.parse(read(path.join(dir, 'datapackage.json')));
      const meas = parseECSV(read(mfile));
      const sysText = readIf(path.join(dir, 'tables/systems.ecsv'));
      const systems = sysText ? parseECSV(sysText) : null;
      const covText = readIf(path.join(dir, 'tables/covariance.ecsv'));
      const obsText = readIf(path.join(dir, 'tables/observables.ecsv'));
      const checks = {};
      const cdir = path.join(dir, 'checks');
      if (fs.existsSync(cdir)) for (const f of fs.readdirSync(cdir).filter((x) => x.endsWith('.csv')).sort()) checks[f] = parseCSV(read(path.join(cdir, f)));
      const assumptions = registry.assumptions.filter((a) => a.datasets[key]);
      datasets.push({
        key, name, version, dir, dp,
        short: name.replace(/^aeg-d-/, ''),
        title: dp.title, citation: dp.x_citation || '', licence: dp.x_licence_status || '',
        measurements: meas, systems, hasCovariance: !!covText, observables: obsText ? parseECSV(obsText) : null, checks,
        knownIssues: JSON.parse(readIf(path.join(dir, 'known_issues.json')) || '{"issues": []}').issues,
        md: { source: readIf(path.join(dir, 'SOURCE.md')), reproduction: readIf(path.join(dir, 'REPRODUCTION.md')), reproductionResult: readIf(path.join(dir, 'REPRODUCTION_RESULT.md')), modelTest: readIf(path.join(dir, 'MODEL_TEST.md')), modelTestResult: readIf(path.join(dir, 'MODEL_TEST_RESULT.md')) },
        checksums: readIf(path.join(dir, 'checksums.sha256')) || '',
        sources: JSON.parse(read(path.join(dir, 'sources.json'))),
        assumptions,
        files: ['tables/measurements.ecsv', sysText ? 'tables/systems.ecsv' : null, covText ? 'tables/covariance.ecsv' : null, fs.existsSync(path.join(dir, 'tables/observables.ecsv')) ? 'tables/observables.ecsv' : null].filter(Boolean),
      });
    }
  }
  const ORDER = ['aeg-d-sparc', 'aeg-d-gc-baumgardt', 'aeg-d-dwarfs', 'aeg-d-strong-lensing', 'aeg-d-xcop', 'aeg-d-kids1000-rar'];
  datasets.sort((a, b) => (ORDER.indexOf(a.name) + 1 || 99) - (ORDER.indexOf(b.name) + 1 || 99) || a.key.localeCompare(b.key));
  const systems = [];
  for (const d of datasets) {
    if (!d.systems) continue;
    const byId = {};
    d.measurements.rows.forEach((r, i) => { (byId[r.system_id] = byId[r.system_id] || []).push(i); });
    for (const s of d.systems.rows) systems.push({ id: s.system_id, name: s.name_in_source, dataset: d.key, row: s, props: s.properties ? JSON.parse(s.properties) : {}, rows: byId[s.system_id] || [] });
  }
  cache = { registry, datasets, systems, standard: read(path.join(ROOT, 'docs/data-standard.md')), changelog: readIf(path.join(ROOT, 'CHANGELOG.md')) || '' };
  return cache;
}

// Columns referenced by the formulas of a dataset's adjustable assumptions.
function formulaColumns(d) {
  const row = new Set(), sys = new Set();
  for (const a of d.assumptions) for (const e of a.datasets[d.key].effects || []) {
    row.add(e.column);
    for (const n of names(parse(e.formula))) { if (n === 'p' || n === 'p0') continue; if (n.startsWith('system.')) sys.add(n.slice(7)); else row.add(n); }
  }
  return { row: [...row], sys: [...sys] };
}

// The compact payload the browser receives for one dataset: columnar arrays, exact values.
export function payload(d) {
  const fc = formulaColumns(d);
  const present = new Set(d.measurements.columns.map((c) => c.name));
  const cols = [...new Set([...CORE, ...fc.row])].filter((c) => present.has(c));
  // Extension columns carry the source's own quantities (the observables, as released): all are sent.
  const extra = d.measurements.columns.map((c) => c.name).filter((c) => c.startsWith('x_') && !cols.includes(c));
  const all = [...cols, ...extra];
  const out = { key: d.key, name: d.name, version: d.version, short: d.short, title: d.title, n: d.measurements.rows.length, columns: {} };
  for (const c of all) out.columns[c] = d.measurements.rows.map((r) => r[c]);
  if (d.systems) {
    const scols = ['system_id', 'name_in_source', 'class_in_source', 'distance_mpc', 'distance_method', 'inclination_deg', ...fc.sys].filter((c, i, a) => a.indexOf(c) === i && d.systems.columns.some((x) => x.name === c));
    out.systems = d.systems.rows.map((s) => { const o = {}; for (const c of scols) o[c] = s[c] ?? null; o.properties = s.properties ? JSON.parse(s.properties) : {}; return o; });
  }
  out.assumptions = d.assumptions.map((a) => ({ id: a.id, name_technical: a.name_technical, name_plain: a.name_plain, adjustable: a.adjustable, status: a.status, scope: a.scope || null, unit: a.parameter?.unit || '', ...a.datasets[d.key] }));
  out.knownIssues = d.knownIssues;
  return out;
}

export function systemSlug(id) { return id; }

// Flags that mark a reliability question (ringed on figures). `no_uncertainty` is information,
// stated in the row's details rather than ringed.
export const RING_FLAGS = ['reproduction_mismatch', 'source_quality_low'];
export function ringed(flags) { return (flags || '').split(';').some((f) => RING_FLAGS.includes(f)); }
