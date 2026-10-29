// The browser's view of the data: payloads built from the packages, and assumption effects
// computed by executing the registry's own formula text (site/src/formula.mjs, the twin of the
// pipeline's evaluator; the build checks they agree on every measurement).
import { parse, evaluate } from '../formula.mjs';
import { state } from './state.js';

const BASE = (typeof document !== 'undefined' && document.documentElement.dataset.base) || '/';
let loaded = null;

export async function loadData(keys) {
  if (loaded) return loaded;
  const list = await (await fetch(BASE + 'data/index.json')).json();
  const want = keys ? list.datasets.filter((d) => keys.includes(d.key)) : list.datasets;
  const ds = await Promise.all(want.map(async (d) => prepare(await (await fetch(BASE + 'data/' + d.file)).json())));
  loaded = { datasets: ds, byKey: Object.fromEntries(ds.map((d) => [d.key, d])) };
  return loaded;
}

function prepare(d) {
  d.rows = [];
  const cols = Object.keys(d.columns);
  for (let i = 0; i < d.n; i++) { const r = {}; for (const c of cols) r[c] = d.columns[c][i]; d.rows.push(r); }
  d.sysById = {};
  (d.systems || []).forEach((s, i) => { s.index = i; d.sysById[s.system_id] = s; s.rows = []; });
  d.rows.forEach((r, i) => { r.index = i; if (r.system_id && d.sysById[r.system_id]) d.sysById[r.system_id].rows.push(i); });
  d.sliders = d.assumptions.filter((a) => a.adjustable && a.status === 'confirmed');
  for (const a of d.sliders) a.compiled = (a.effects || []).map((e) => ({ column: e.column, ast: parse(e.formula) }));
  return d;
}

// Parameter value for an assumption on a row, from the state: dataset-wide or per-system.
export function paramFor(d, a, row) {
  if (a.scope === 'system') { const s = state.per[row.system_id]; return s && s[a.id] !== undefined ? s[a.id] : a.default; }
  const v = state.global[d.key + ':' + a.id];
  return v !== undefined ? v : a.default;
}

// The row at the given parameters (override: {assumptionId: p}). Assumptions apply in registry
// order; the effects of one assumption are evaluated together against the row before it.
export function adjusted(d, row, override) {
  let out = row, sys = null;
  for (const a of d.sliders) {
    if (!(row.adjustable || '').split(';').includes(a.id)) continue;
    const p = override && override[a.id] !== undefined ? override[a.id] : paramFor(d, a, row);
    if (Math.abs(p - a.default) < 1e-12) continue;
    if (!sys) { sys = {}; const s = d.sysById[row.system_id]; if (s) for (const k of Object.keys(s)) if (typeof s[k] !== 'object') sys['system.' + k] = s[k]; }
    const env = Object.assign({}, out, sys, { p: p, p0: a.default });
    const next = Object.assign({}, out);
    for (const e of a.compiled) next[e.column] = evaluate(e.ast, env);
    out = next;
  }
  return out;
}

export function anyChange(datasets) {
  if (Object.keys(state.per).length) return true;
  return datasets.some((d) => d.sliders.some((a) => a.scope === 'dataset' && state.global[d.key + ':' + a.id] !== undefined && Math.abs(state.global[d.key + ':' + a.id] - a.default) > 1e-12));
}

export function systemChanged(d, sysId) {
  if (state.per[sysId]) return true;
  const rows = d.sysById[sysId] ? d.sysById[sysId].rows.map((i) => d.rows[i]) : [];
  return d.sliders.some((a) => a.scope === 'dataset' && rows.some((r) => (r.adjustable || '').split(';').includes(a.id)) && state.global[d.key + ':' + a.id] !== undefined && Math.abs(state.global[d.key + ':' + a.id] - a.default) > 1e-12);
}

export const RING_FLAGS = ['reproduction_mismatch', 'source_quality_low'];
export function ringed(flags) { return (flags || '').split(';').some((f) => RING_FLAGS.includes(f)); }

export const KPC_M = 3.0856775814913673e19;
export function speed(g, rKpc) { return (g >= 0 ? 1 : -1) * Math.sqrt(Math.abs(g) * rKpc * KPC_M) / 1000; }
