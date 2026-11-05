// Unit tests for the build-time libraries (node --test).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseECSV, splitCSV, toCSV } from '../src/lib/ecsv.mjs';
import { parse, evaluate, names } from '../src/formula.mjs';
import { fmtParam, sigFig } from '../src/lib/labels.mjs';
import { md, resultLine } from '../src/lib/md.mjs';
import { tex, texHtml, hasTex } from '../src/lib/tex.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const tables = fs.readdirSync(path.join(ROOT, 'data/packages')).flatMap((n) => fs.readdirSync(path.join(ROOT, 'data/packages', n)).flatMap((v) => {
  const dir = path.join(ROOT, 'data/packages', n, v, 'tables');
  return fs.existsSync(dir) ? fs.readdirSync(dir).filter((f) => f.endsWith('.ecsv')).map((f) => path.join(dir, f)) : [];
}));

test('every package table parses, with as many rows as data lines in the file', () => {
  assert.ok(tables.length >= 5);
  for (const f of tables) {
    const text = fs.readFileSync(f, 'utf8');
    const t = parseECSV(text);
    const dataLines = text.split('\n').filter((l) => l && !l.startsWith('#')).length - 1;
    assert.equal(t.rows.length, dataLines, f);
  }
});

test('ECSV numbers round-trip exactly through the CSV download', () => {
  for (const f of tables) {
    const t = parseECSV(fs.readFileSync(f, 'utf8'));
    const lines = toCSV(t.columns, t.rows).trim().split('\n');
    assert.deepEqual(splitCSV(lines[0]), t.columns.map((c) => c.name));
    const numeric = t.columns.filter((c) => /^(float|int)/.test(c.datatype));
    lines.slice(1, 50).forEach((l, i) => {
      const cells = splitCSV(l);
      for (const c of numeric) { const k = t.columns.indexOf(c); const v = t.rows[i][c.name]; assert.equal(cells[k] === '' ? null : Number(cells[k]), v); }
    });
  }
});

test('splitCSV handles quotes and embedded commas', () => {
  assert.deepEqual(splitCSV('a,"b,c","d ""e"""'), ['a', 'b,c', 'd "e"']);
});

test('formula engine: names and evaluation', () => {
  const ast = parse('g_obs * system.distance_mpc / (system.distance_mpc + p * system.distance_err_mpc)');
  assert.deepEqual([...names(ast)].sort(), ['g_obs', 'p', 'system.distance_err_mpc', 'system.distance_mpc']);
  assert.equal(evaluate(ast, { g_obs: 2, 'system.distance_mpc': 10, 'system.distance_err_mpc': 1, p: 0 }), 2);
  assert.equal(evaluate(parse('sqrt(3^2 + 4^2)'), {}), 5);
});

test('every registry formula parses (identity at defaults is checked by aeg.formula_check)', () => {
  const reg = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/assumptions.json'), 'utf8'));
  for (const a of reg.assumptions) for (const [k, e] of Object.entries(a.datasets)) for (const f of e.effects || []) {
    const ast = parse(f.formula);
    assert.ok(names(ast).size > 0, `${a.id} ${k} ${f.column}`);
  }
});

test('labels format parameters', () => {
  assert.equal(fmtParam('sigma', -1), '−1.0σ');
  assert.equal(fmtParam('percent', 0.25), '25%');
  assert.equal(fmtParam('value', 0.5), '0.50');
  assert.equal(fmtParam('imf', 0), 'Chabrier/Kroupa');
  assert.equal(fmtParam('imf', 1), 'Salpeter');
  assert.equal(fmtParam('imf', 0.5), '50% to Salpeter');
  assert.equal(fmtParam('range', 0), 'default');
  assert.equal(fmtParam('range', -1), 'minimum');
  assert.equal(fmtParam('range', 1), 'maximum');
  assert.equal(fmtParam('range', -0.25), '25% to minimum');
  assert.equal(sigFig(38300000000), '3.83 × 10¹⁰');
  assert.equal(sigFig(150.1), '150');
});

test('markdown: relative links go to the repository; result lines are read', () => {
  assert.match(md('[t](REPRODUCTION.md)', 'data/packages/x/v1'), /href="https:\/\/github.com\/extragravitation\/atlas\/blob\/main\/data\/packages\/x\/v1\/REPRODUCTION.md"/);
  assert.match(md('[t](https://example.org)'), /href="https:\/\/example.org"/);
  assert.deepEqual(resultLine('**Result: PASSED** (x)'), { text: 'PASSED', pass: true });
  assert.equal(resultLine('**Result: FAILED** for 3').pass, false);
});

test('TeX in quotes is shown readably; text without TeX is unchanged (D-109 rule 4)', () => {
  const q = String.raw`clear evidence of a breakdown of hydrostatic equilibrium \citep[A2319,][]{ghirardini18}, valid at the $\lesssim20\%$ level out to $R_{200}$`;
  assert.equal(tex(q), 'clear evidence of a breakdown of hydrostatic equilibrium (A2319, citation), valid at the ≲20% level out to R₂₀₀');
  assert.equal(texHtml(q), 'clear evidence of a breakdown of hydrostatic equilibrium (A2319, citation), valid at the ≲20% level out to R<sub>200</sub>');
  assert.equal(tex(String.raw`NGC~2298 \citep{a, b}`), 'NGC 2298 (citation)');
  assert.equal(tex(String.raw`$1 \sigma$ $z=0.041\pm0.001$ $\alpha\gtrsim 0.5$ $3\times10$`), '1 σ z=0.041±0.001 α≳ 0.5 3×10');
  assert.equal(texHtml(String.raw`$M_{\rm star}$ $10^{-3}$ $150\,{\rm km}$`), 'M<sub>star</sub> 10<sup>-3</sup> 150 km');
  assert.equal(texHtml(String.raw`$a < b$`), 'a &lt; b');
  for (const plain of ['g_obs / g_bar ~ 1', 'x_gc_baumgardt_log_rh_err_lo', 'Ω_m as stated']) { assert.equal(hasTex(plain), false); assert.equal(tex(plain), plain); }
});
