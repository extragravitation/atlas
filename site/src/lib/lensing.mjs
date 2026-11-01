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

  // Funnel. "Read" is every lens the two readers read in the A6 scopes: the tabulated systems (adjudicated below
  // z_l = 0.30; recorded from the readings at or above it, D-066 item 2) plus the lenses that cannot be tabulated.
  const readSet = new Set(adjudicated.filter((r) => r.system !== '(record)').map((r) => r.scope + '\u0000' + r.system));
  const sys = d.systems.rows.map((s) => ({ s, p: JSON.parse(s.properties || '{}') }));
  const gap = sys.filter(({ p }) => (p.flags || []).includes('epoch_gap_v1'));
  const below = sys.filter(({ s }) => s.redshift !== null && s.redshift < 0.30);
  const plotted = sys.filter(({ p }) => p.status === 'plotted');
  const recorded = below.filter(({ p }) => p.status !== 'plotted');
  const notTabAdj = notTab.filter((r) => readSet.has(r.scope + '\u0000' + r.system));
  if (readSet.size !== below.length + notTabAdj.length) throw new Error(`lensing funnel: ${readSet.size} lenses in the adjudicated readings, but ${below.length} tabulated below 0.30 + ${notTabAdj.length} not tabulated`);
  if (below.length + gap.length !== sys.length) throw new Error('lensing funnel: a tabulated lens is neither below z = 0.30 nor flagged epoch_gap_v1');
  if (gap.some(({ s, p }) => !(s.redshift >= 0.30) || p.plotted !== false)) throw new Error('lensing funnel: an epoch-gap lens is below 0.30 or plotted');
  const byScope = (list) => { const m = {}; for (const { p } of list) m[p.scope] = (m[p.scope] || 0) + 1; return m; };
  const reasonGroups = (list) => {
    const m = new Map();
    for (const { s, p } of list) { const k = (p.reasons_not_plotted || []).join('; '); if (!m.has(k)) m.set(k, []); m.get(k).push({ id: s.system_id, name: s.name_in_source, scope: p.scope, cls: s.class_in_source, words: kindWords(s, p) }); }
    return [...m.entries()].map(([reason, items]) => ({ reason, items }));
  };
  const notTabGroups = (() => { const m = new Map(); for (const r of notTab) { const k = r.scope + '\u0000' + r.reason; if (!m.has(k)) m.set(k, { scope: r.scope, reason: r.reason, names: [] }); m.get(k).names.push(r.system); } return [...m.values()]; })();
  const firstScope = (p) => (p.scope || '').split(' | ')[0];
  const gapByScope = {}; for (const { p } of gap) gapByScope[surveyName(firstScope(p))] = (gapByScope[surveyName(firstScope(p))] || 0) + 1;
  const funnel = { read: sys.length + notTab.length, adjudicated: readSet.size, tabulated: sys.length, below: below.length, plotted: plotted.length, recorded: recorded.length,
    gap: gap.length, gapByScope, gapDiffer: gap.filter(({ p }) => p.flags.includes('readers_differ')).length,
    gapItems: gap.map(({ s, p }) => ({ id: s.system_id, name: s.name_in_source, z: s.redshift, words: kindWords(s, p), differ: p.flags.includes('readers_differ') })),
    notTabulated: notTab.length, plottedByScope: byScope(plotted), recordedGroups: reasonGroups(recorded), notTabGroups };

  const out = {
    formula, profile, adjudicated, funnel,
    formulaGroups: grouped(formula.rows, (r) => `${r.record_m_e}|${r.record_theta}`, null),
    profileGroups: grouped(profile.rows, (r) => r.imf, 0.10),
    formulaMeta: formula.meta, profileMeta: profile.meta,
  };
  cache.set(d.key, out);
  return out;
}

// Survey name from an inventory scope, for plain sentences.
const SURVEY = [[/^SLACS/, 'SLACS V'], [/^S4TM/, 'S4TM'], [/^SL2S/, 'SL2S'], [/^SNL-/, 'SNELLS'], [/^MNELLS/, 'MNELLS'], [/^MaNGA/, 'MaNGA'],
  [/^Euclid/, 'Euclid'], [/^CASTLES/, 'CASTLES'], [/^SuGOHI/, 'SuGOHI'], [/^KiDS/, 'KiDS'], [/^Cosmic Horseshoe/, 'Cosmic Horseshoe papers'], [/^J0100\+1818/, 'J0100+1818 papers']];
export function surveyName(scope) { const m = SURVEY.find(([re]) => re.test(scope || '')); return m ? m[1] : scope; }

// The lens's kind in plain words, from the class the source prints (systems table class_in_source). The
// codes are explained only as far as the package records them: R5's Mph letter, and the first letter
// (morphology) of R10's class code; nothing is inferred beyond that.
export function kindWords(s, p) {
  const v = (s.class_in_source || '').trim(), who = surveyName((p.scope || '').split(' | ')[0]);
  if ((p.flags || []).includes('readers_differ') && s.taxonomy_kind === 'A7' && /^reader A/.test(v)) return { t: 'Kind not settled: the two readers recorded it differently (both readings below; not adjudicated)', p: 'The two people who read the paper described this galaxy differently, so its type is left open' };
  let m = v.match(/^Mph = ([ELU])$/);
  if (m) { const w = { E: 'Early-type', L: 'Late-type', U: 'Unclassified' }[m[1]]; return { t: `${w} (${m[1]}), as classified by ${who}`, p: `${{ E: 'A smooth, round or oval galaxy (elliptical or S0)', L: 'A spiral or irregular galaxy', U: 'Not classified' }[m[1]]}, according to ${who}` }; }
  m = v.match(/^([A-Z])-([A-Z])-([A-Z])$/);
  if (m) return m[1] === 'E' ? { t: `Early-type (E), from the class code ${v} printed by ${who} (only its first letter, the morphology, is used)`, p: `A smooth, round or oval galaxy (elliptical or S0), according to ${who}` } : { t: `Class code ${v} printed by ${who}`, p: `Classified ${v} by ${who}` };
  if (v === 'not stated' || !v) return { t: `Kind not stated by ${who}`, p: `${who} does not say what kind of galaxy this is` };
  if (/\(row notes\)$/.test(v)) return { t: `${cap(v.replace(/\s*\(row notes\)$/, ''))}, as noted in the ${who} reading`, p: `${cap(v.replace(/\s*\(row notes\)$/, ''))}, according to ${who}` };
  m = v.match(/^grade ([A-Z]); sample: '(.*)'$/);
  if (m) return { t: `Grade ${m[1]} lens, in a sample described by ${who} as ${m[2]}`, p: `${who} rates it a grade ${m[1]} lens, in a sample of ${m[2]}` };
  if (/^early-type \(sample statement\)$/.test(v)) return { t: `Early-type, as ${who} states for its sample as a whole (no per-lens class)`, p: `${who} describes its lenses as smooth, round or oval galaxies` };
  return { t: `${cap(v)}, as described by ${who}`, p: `${cap(v)}, according to ${who}` };
}
const cap = (x) => x.charAt(0).toUpperCase() + x.slice(1);

// The cosmology rows the readers recorded for a lens's observed-side record (H0, Ω_m, Ω_Λ or a named
// cosmology), with their location and quote; lens-specific rows first, then the record-level ones.
export function cosmologyRows(pkg, scope, name, record) {
  const q = ['H0', 'Om', 'OL', 'cosmology'];
  const rows = pkg.adjudicated.filter((r) => r.record === record && q.includes(r.quantity) && r.scope === scope && (r.system === name || r.system === '(record)'));
  const own = rows.filter((r) => r.system === name);
  return own.length ? own : rows;
}
