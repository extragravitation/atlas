// The map (population level): g_obs against g_bar with the line g_obs = g_bar (D-012), display
// controls of D-027, no fitted relation (D-026). Every value comes from the package tables,
// adjusted only by the registry formulas for the assumptions the reader has changed.
import { loadData, adjusted, anyChange, ringed } from './model.js';
import { state, set, onChange } from './state.js';
import { css, plain } from './ui.js';
import { setup, axes, sci, showTip, niceStep, cmap } from './draw.js';
import { wireSliders } from './sliders.js';

const BASE = document.documentElement.dataset.base || '/';
const $ = (id) => document.getElementById(id);
const COLOR = { 'aeg-d-sparc': '--sparc', 'aeg-d-xcop': '--xcop', 'aeg-d-kids1000-rar': '--kids' };
const LBL = JSON.parse($('map-labels').textContent);
let D = null, hits = [], hover = null, cache = null, geom = null, brush = null;

const lg = (v) => (v > 0 ? Math.log10(v) : null);
// Lenses (D-030): the same measurements in different framings. Spherical-equivalent enclosed mass
// M(<r) = g r² / G (in M☉, with the IAU nominal G M☉); equivalent circular speed V = √(g r).
const GM_SUN = 1.3271244e20, KPC = 3.0856775814913673e19;
const massOf = (g, r) => (g > 0 && r > 0 ? (g * (r * KPC) ** 2) / GM_SUN : null);
const speedOf = (g, r) => (g > 0 && r > 0 ? Math.sqrt(g * r * KPC) / 1000 : null);
const RADIAL = ['rad', 'mass', 'speed'];
// Colour by a source property (systematics checks, D-033). Values exactly as the source gives them;
// measurements without the property are drawn faint grey and counted in the key.
const sysOf = (d, r) => (r.system_id && d.sysById ? d.sysById[r.system_id] : null);
const PROPS = {
  incl: { label: 'Inclination (°)', kind: 'cont', get: (d, r) => sysOf(d, r)?.inclination_deg ?? null, lo: 0, hi: 90, fmt: (v) => v.toFixed(0) + '°' },
  dist: { label: 'Distance (Mpc, log scale)', kind: 'cont', log: true, get: (d, r) => sysOf(d, r)?.distance_mpc ?? null, lo: 0, hi: Math.log10(150), fmt: (v) => (v < 10 ? v.toFixed(1) : Math.round(v)) + ' Mpc' },
  z: { label: 'Redshift', kind: 'cont', get: (d, r) => sysOf(d, r)?.properties?.redshift ?? null, lo: 0, hi: 0.12, fmt: (v) => v.toFixed(3) },
  rext: { label: 'Outermost measured radius of the system (kpc, log scale)', kind: 'cont', log: true, get: (d, r) => { const s = sysOf(d, r); if (!s) return null; if (s._rext === undefined) s._rext = Math.max(...s.rows.map((i) => d.rows[i].r_kpc || 0)) || null; return s._rext; }, lo: Math.log10(0.3), hi: Math.log10(3000), fmt: (v) => (v < 10 ? v.toFixed(1) : Math.round(v)) + ' kpc' },
  dmethod: { label: 'Distance method', kind: 'cat', get: (d, r) => sysOf(d, r)?.distance_method ?? null },
  q: { label: 'Source quality flag Q (1 high, 3 low)', kind: 'cat', get: (d, r) => { const v = sysOf(d, r)?.properties?.quality_flag_Q; return v === undefined || v === null ? null : 'Q = ' + v; } },
};
const CATS = ['--sparc', '--xcop', '--kids', '--gas', '--bulge', '--flag'];
let catIndex = {};
function propValue(d, r) { const P = PROPS[state.col]; return P ? P.get(d, r) : undefined; }
function colorFor(d, row) {
  const P = PROPS[state.col];
  if (P) {
    const v = P.get(d, row);
    if (v === null || v === undefined) return css('--muted');
    if (P.kind === 'cat') return css(CATS[(catIndex[v] ?? 0) % CATS.length]);
    const x = P.log ? Math.log10(v) : v, t = Math.max(0, Math.min(1, (x - P.lo) / (P.hi - P.lo)));
    return cmap(t * 1.5);
  }
  return state.col === 'channel' ? css(row.channel === 'lensing' ? '--kids' : '--sparc') : css(COLOR[d.name] || '--sparc');
}
function prepareCats() {
  const P = PROPS[state.col]; catIndex = {};
  if (!P || P.kind !== 'cat') return;
  const counts = {};
  D.datasets.forEach((d) => d.rows.forEach((r) => { const v = P.get(d, r); if (v !== null && v !== undefined) counts[v] = (counts[v] || 0) + 1; }));
  Object.keys(counts).sort((a, b) => counts[b] - counts[a]).forEach((k, i) => { catIndex[k] = i; });
  return counts;
}
function colorKey() {
  const P = PROPS[state.col], el = $('colkey');
  if (!P) { el.hidden = true; return; }
  let have = 0, miss = 0;
  D.datasets.forEach((d) => { if (state.hide.includes(d.key)) return; d.rows.forEach((r) => { const v = P.get(d, r); if (v === null || v === undefined) miss++; else have++; }); });
  let html = `<b>${P.label}.</b> `;
  if (P.kind === 'cat') { const counts = prepareCats(); html += Object.keys(catIndex).map((k) => `<span style="white-space:nowrap"><span class="sw" style="display:inline-block;background:var(${CATS[catIndex[k] % CATS.length]})"></span> ${k} (${counts[k]})</span>`).join(' · '); }
  else { const stops = [0, 0.5, 1].map((t) => P.lo + t * (P.hi - P.lo)).map((x) => P.fmt(P.log ? Math.pow(10, x) : x)); html += `<span class="ramp" aria-hidden="true"></span> ${stops[0]} → ${stops[1]} → ${stops[2]}`; }
  el.innerHTML = `<p style="margin:0">${html}</p><details class="more" data-more ${document.body.classList.contains('phone-map') ? '' : 'open'}><summary>${have.toLocaleString('en')} coloured · ${miss.toLocaleString('en')} grey (no value)</summary>${have.toLocaleString('en')} measurements are coloured by this property; ${miss.toLocaleString('en')} whose source does not give it are drawn faint grey.</details>`;
  el.hidden = false;
}

// One point per system (D-043). Every point is an existing measured row, chosen by a rule; nothing is
// interpolated or extrapolated. 'outer': the row at the largest measured radius (everything within the
// measured extent). 'light': the first measured row at or beyond LIGHT_K times the source's effective
// (half-light) radius; systems whose data do not reach it, or whose source gives no such radius, are
// left out and counted. Population bins (stacked lensing) are averages, not systems, and are unchanged.
const LIGHT_K = 2;
const lightRadius = (s) => s?.properties?.r_eff_kpc ?? null;
let pickKey = null, picked = null, pickStats = null;
function computePick() {
  const key = state.pick + '|' + cacheKey;
  if (key === pickKey) return;
  pickKey = key;
  if (state.pick === 'all') { picked = null; pickStats = null; return; }
  picked = []; pickStats = { shown: 0, noRadius: 0, short: 0, systems: 0 };
  D.datasets.forEach((d, di) => {
    if (!d.systems) { picked.push(null); return; }
    const set = new Set();
    for (const s of d.systems) {
      pickStats.systems++;
      const idx = s.rows.filter((i) => d.rows[i].r_kpc > 0);
      if (!idx.length) continue;
      if (state.pick === 'outer') { let best = idx[0]; for (const i of idx) if (d.rows[i].r_kpc > d.rows[best].r_kpc) best = i; set.add(best); pickStats.shown++; continue; }
      const re = lightRadius(s);
      if (!(re > 0)) { pickStats.noRadius++; continue; }
      const target = LIGHT_K * re, ok = idx.filter((i) => d.rows[i].r_kpc >= target);
      if (!ok.length) { pickStats.short++; continue; }
      let best = ok[0]; for (const i of ok) if (d.rows[i].r_kpc < d.rows[best].r_kpc) best = i;
      set.add(best); pickStats.shown++;
    }
    picked.push(set);
  });
}

let cacheKey = null;
function compute() {
  // Adjusted values for every row, recomputed only when an assumption changes (not on zoom or pan).
  const key = JSON.stringify([state.global, state.per]);
  if (key === cacheKey && cache) return;
  cacheKey = key;
  cache = D.datasets.map((d) => d.rows.map((r) => adjusted(d, r)));
}

function ranges() {
  if (state.view === 'obs') return { x: [-15, -7.5], y: [-13.5, -7.5], equal: true };
  if (state.view === 'ex') return { x: [-15, -7.5], y: [-0.5, 2.0] };
  if (state.view === 'mass') return { x: [5, 15.5], y: [5, 15.5], equal: true };
  if (state.view === 'speed') return { x: [-1.2, 3.5], y: [0.5, 3.5] };
  return { x: [-1.2, 3.5], y: [-0.5, 2.0] };
}
const VIEWS = ['obs', 'ex', 'mass', 'rad', 'speed'];

// Zoom (reader's choice, kept in the address as z=x0,x1,y0,y1): the plotted window only; it never
// changes which measurements exist or their values.
function view() {
  const base = ranges(), z = state.zoom;
  if (!z) return { base, rg: base, zoomed: false };
  const cl = (a, lo, hi) => Math.min(hi, Math.max(lo, a));
  const x0 = cl(z[0], base.x[0], base.x[1]), x1 = cl(z[1], base.x[0], base.x[1]), y0 = cl(z[2], base.y[0], base.y[1]), y1 = cl(z[3], base.y[0], base.y[1]);
  if (x1 - x0 < 1e-3 || y1 - y0 < 1e-3) return { base, rg: base, zoomed: false };
  return { base, rg: { x: [x0, x1], y: [y0, y1] }, zoomed: true };
}

function draw() {
  const box = $('figbox'), fig = $('fig'), W = box.clientWidth, narrow = W < 560, { base, rg, zoomed } = view();
  const L = 58, R = 14, T = 12, B = 46, pw = W - L - R, ph = base.equal ? pw * (base.y[1] - base.y[0]) / (base.x[1] - base.x[0]) : pw * 0.62;
  geom = { L, T, pw, ph, rg, base };
  const g = setup(fig, W, Math.round(ph + T + B));
  const P = plain();
  if (!VIEWS.includes(state.view)) state.view = 'obs';
  const v = state.view, n = narrow ? 's' : '';
  const xl = v === 'mass' ? LBL['xm' + n][+P] : RADIAL.includes(v) ? LBL.xr[+P] : (narrow ? LBL.xs[+P] : LBL.x[+P]);
  const yl = v === 'obs' ? (narrow ? LBL.ys[+P] : LBL.y[+P]) : v === 'mass' ? LBL['ym' + n][+P] : v === 'speed' ? LBL['yv' + n][+P] : (narrow ? LBL.yxs[+P] : LBL.yx[+P]);
  const xs = zoomed ? niceStep(rg.x[1] - rg.x[0]) : 1, ys = zoomed ? niceStep(rg.y[1] - rg.y[0]) : (v === 'obs' || v === 'mass' ? 1 : 0.5);
  const { X, Y } = axes(g, W, L, T, pw, ph, rg, xl, yl, xs, ys, zoomed ? null : (v === 'obs' || v === 'mass' ? 0 : 1));
  const ink = css('--ink'), alpha = parseFloat(css('--ptAlpha')) || 0.4, moved = anyChange(D.datasets);
  g.save(); g.beginPath(); g.rect(L, T, pw, ph); g.clip();
  g.setLineDash([6, 4]); g.strokeStyle = ink; g.lineWidth = 1.1; g.beginPath();
  if (v === 'obs' || v === 'mass') { g.moveTo(X(base.x[0]), Y(base.x[0])); g.lineTo(X(base.x[1]), Y(base.x[1])); } else if (v !== 'speed') { g.moveTo(L, Y(0)); g.lineTo(L + pw, Y(0)); }
  g.stroke(); g.setLineDash([]);
  g.font = 'italic 13px ' + css('--serif'); g.fillStyle = ink;
  if (zoomed) { /* the line's label is placed for the full view only */ }
  else if (v === 'obs') { const lx = narrow ? -12.4 : -12.7; g.save(); g.translate(X(lx), Y(lx) + 14); g.rotate(Math.atan2(Y(-10) - Y(-11), X(-10) - X(-11))); g.textAlign = 'center'; g.fillText(narrow ? LBL.zero[+P] : LBL.line[+P], 0, 0); g.restore(); }
  else if (v === 'mass') { const lx = 7.2; g.save(); g.translate(X(lx), Y(lx) + 14); g.rotate(Math.atan2(Y(9) - Y(8), X(9) - X(8))); g.textAlign = 'center'; g.fillText(LBL.zerom[+P], 0, 0); g.restore(); }
  else if (v !== 'speed') { g.textAlign = 'left'; g.fillText(LBL.zero[+P], L + 8, Y(0) + 16); }
  hits = []; let nNeg = 0;
  const pos = (q) => {
    if (v === 'mass') { const mb = lg(massOf(q.g_bar, q.r_kpc)), mo = lg(massOf(q.g_obs, q.r_kpc)); return mb === null || mo === null ? null : [X(mb), Y(mo)]; }
    if (v === 'speed') { const x = lg(q.r_kpc), y = lg(speedOf(q.g_obs, q.r_kpc)); return x === null || y === null ? null : [X(x), Y(y)]; }
    const x = v === 'rad' ? lg(q.r_kpc) : lg(q.g_bar); const yo = lg(q.g_obs), yb = lg(q.g_bar); if (x === null || yo === null || yb === null) return null; return [X(x), Y(v === 'obs' ? yo : yo - yb)];
  };
  const posDef = (r) => pos(r);
  D.datasets.forEach((d, di) => {
    if (state.hide.includes(d.key)) return;
    const pop = !d.systems;
    if (RADIAL.includes(v) && pop) return; // population bins have no radius
    const col = (r) => colorFor(d, r);
    // tracks
    if (state.marks !== 'points' && !pop && state.pick === 'all') {
      g.lineWidth = 0.9; g.globalAlpha = d.name === 'aeg-d-xcop' ? 0.8 : 0.4;
      for (const s of d.systems) { g.strokeStyle = col(d.rows[s.rows[0]]); g.beginPath(); let st = false; for (const i of s.rows) { const xy = pos(cache[di][i]); if (!xy) { st = false; continue; } if (st) g.lineTo(xy[0], xy[1]); else { g.moveTo(xy[0], xy[1]); st = true; } } g.stroke(); }
      g.globalAlpha = 1;
    }
    const only = picked && picked[di];
    d.rows.forEach((r, i) => {
      if (only && !only.has(i)) return;
      const q = cache[di][i], xy = pos(q);
      if (!xy) { if (!(q.g_bar > 0) && v !== 'speed') nNeg++; return; }
      const [x, y] = xy, c = col(r), shape = r.method_class;
      if (moved && state.arrows !== false && q !== r) {
        const xy0 = posDef(r);
        if (xy0) { const dx = x - xy0[0], dy = y - xy0[1], len = Math.hypot(dx, dy); if (len > 1.2) { g.strokeStyle = css('--range'); g.globalAlpha = 0.3; g.lineWidth = 0.6; g.beginPath(); g.moveTo(xy0[0], xy0[1]); g.lineTo(x, y); const a = Math.atan2(dy, dx), h = Math.min(4, len * 0.5); g.lineTo(x - h * Math.cos(a - 0.5), y - h * Math.sin(a - 0.5)); g.moveTo(x, y); g.lineTo(x - h * Math.cos(a + 0.5), y - h * Math.sin(a + 0.5)); g.stroke(); g.globalAlpha = 1; } }
      }
      if (state.err && state.view === 'obs') {
        const lo = q.g_obs - (q.g_obs_err_lo ?? 0), hi = q.g_obs + (q.g_obs_err_hi ?? 0);
        g.strokeStyle = c; g.globalAlpha = pop ? 0.9 : 0.45; g.lineWidth = pop ? 0.9 : 0.6; g.beginPath(); g.moveTo(x, lo > 0 ? Y(lg(lo)) : T + ph); g.lineTo(x, Y(lg(hi))); g.stroke(); g.globalAlpha = 1;
      }
      const faint = PROPS[state.col] && (propValue(d, r) === null || propValue(d, r) === undefined);
      if (faint) { g.globalAlpha = 0.18; }
      if (shape === 'lensing') { g.save(); g.translate(x, y); g.rotate(Math.PI / 4); g.fillStyle = css('--bg'); g.fillRect(-3, -3, 6, 6); g.strokeStyle = c; g.lineWidth = 1.3; g.strokeRect(-3, -3, 6, 6); g.restore(); }
      else if (state.marks !== 'tracks' || state.pick !== 'all') { g.fillStyle = c; g.globalAlpha = faint ? 0.15 : shape === 'hydrostatic' ? 0.8 : alpha; const rr = state.pick === 'all' ? 1.7 : 3; if (shape === 'kinematic') { g.beginPath(); g.arc(x, y, rr, 0, 6.2832); g.fill(); } else g.fillRect(x - rr - 0.1, y - rr - 0.1, 2 * rr + 0.2, 2 * rr + 0.2); g.globalAlpha = 1; }
      g.globalAlpha = faint ? 0.25 : 1;
      if (ringed(r.flags)) { g.strokeStyle = css('--flag'); g.lineWidth = 0.7; g.beginPath(); g.arc(x, y, 3.6, 0, 6.2832); g.stroke(); }
      g.globalAlpha = 1;
      if (r.system_id && state.per[r.system_id]) { g.strokeStyle = css('--range'); g.lineWidth = 1; g.strokeRect(x - 3.5, y - 3.5, 7, 7); }
      if (x >= L && x <= L + pw && y >= T && y <= T + ph) hits.push({ x, y, d, r, q });
    });
  });
  // selected system as a highlighted track
  const sel = state.sel && D.datasets.find((d) => d.sysById && d.sysById[state.sel]);
  if (sel) {
    const di = D.datasets.indexOf(sel), s = sel.sysById[state.sel];
    const only = picked && picked[di];
    // One-per-system view: highlight only the chosen point; the full profile is in the side card.
    const rowsShown = only ? s.rows.filter((i) => only.has(i)) : s.rows;
    const pts = rowsShown.map((i) => pos(cache[di][i])).filter(Boolean);
    if (only) {
      pts.forEach((xy) => { g.strokeStyle = css('--sel'); g.lineWidth = 2; g.beginPath(); g.arc(xy[0], xy[1], 6, 0, 6.2832); g.stroke(); g.fillStyle = css('--sel'); g.beginPath(); g.arc(xy[0], xy[1], 3, 0, 6.2832); g.fill(); });
      if (pts.length) { const l = pts[0]; g.font = '600 13px ' + css('--sans'); g.textAlign = 'left'; g.fillText(s.name_in_source, l[0] + 10, l[1] + 4); }
    } else {
    g.strokeStyle = css('--sel'); g.lineWidth = 2.2; g.beginPath(); pts.forEach((xy, i) => (i ? g.lineTo(xy[0], xy[1]) : g.moveTo(xy[0], xy[1]))); g.stroke();
    g.fillStyle = css('--sel'); pts.forEach((xy) => { g.beginPath(); g.arc(xy[0], xy[1], 2.6, 0, 6.2832); g.fill(); });
    if (pts.length) { const l = pts[pts.length - 1]; g.font = '600 13px ' + css('--sans'); g.textAlign = 'left'; g.fillText(s.name_in_source, l[0] + 8, l[1] + 4); }
    }
  }
  if (hover) { g.strokeStyle = ink; g.lineWidth = 1.5; g.beginPath(); g.arc(hover.x, hover.y, 6, 0, 6.2832); g.stroke(); }
  if (brush) { g.fillStyle = css('--sel'); g.globalAlpha = 0.08; g.fillRect(brush.x0, brush.y0, brush.x1 - brush.x0, brush.y1 - brush.y0); g.globalAlpha = 1; g.strokeStyle = css('--sel'); g.lineWidth = 1; g.setLineDash([4, 3]); g.strokeRect(brush.x0, brush.y0, brush.x1 - brush.x0, brush.y1 - brush.y0); g.setLineDash([]); }
  g.restore();
  $('zoom-reset').disabled = !zoomed; $('zoom-out').disabled = !zoomed;
  $('zoom-state').textContent = zoomed ? (P ? 'Zoomed in.' : 'Zoomed: ' + rg.x.map((a) => a.toFixed(2)).join(' to ') + ' by ' + rg.y.map((a) => a.toFixed(2)).join(' to ') + '.') : '';
  $('neg-note').textContent = nNeg ? `${nNeg} measurements have g_bar ≤ 0 at these settings (a component pulls outward) and cannot be placed on log axes; they are listed in the downloads.` : '';
  $('fig').setAttribute('aria-label', LBL['aria_' + v][+P]);
  const pn = $('pick-note');
  if (pickStats) {
    const t = state.pick === 'outer' ? LBL.pickOuter[+P] : LBL.pickLight[+P].replace('{k}', LIGHT_K);
    const left = state.pick === 'light' ? ' ' + LBL.pickLeft[+P].replace('{short}', pickStats.short).replace('{none}', pickStats.noRadius) : '';
    pn.innerHTML = t.replace('{n}', pickStats.shown).replace('{N}', pickStats.systems) + left; pn.hidden = false;
  } else pn.hidden = true;
  $('lens-note').innerHTML = LBL.lens[v][+P] + (RADIAL.includes(v) && D.datasets.some((d) => !d.systems && !state.hide.includes(d.key)) ? ' ' + LBL.noRadius[+P] : '');
}

function legend() {
  const P = plain();
  const items = D.datasets.map((d) => {
    const shape = d.rows[0].method_class, c = PROPS[state.col] ? '--muted' : COLOR[d.name] || '--sparc';
    const sw = shape === 'lensing' ? `width:8px;height:8px;border:1.5px solid var(${state.col === 'channel' ? '--kids' : c});transform:rotate(45deg)` : `${shape === 'kinematic' ? 'border-radius:50%;' : ''}background:var(${state.col === 'channel' ? '--sparc' : c})`;
    const on = !state.hide.includes(d.key);
    return `<li><button type="button" class="item" data-leg="${d.key}" aria-pressed="${on}"><span class="sw" style="${sw}" aria-hidden="true"></span><span>${LBL.ds[d.key][+P]}: ${LBL.weight[d.key]}</span></button></li>`;
  });
  items.push(`<li><span class="item"><span class="sw" style="border-radius:50%;border:1.2px solid var(--flag)" aria-hidden="true"></span><span>${LBL.flagged}</span></span></li>`);
  if (Object.keys(state.per).length) items.push(`<li><span class="item"><span class="sw" style="border:1px solid var(--range)" aria-hidden="true"></span><span>${P ? 'Square: a system changed on its own page' : 'Square: distance or inclination changed for this system on its page'}</span></span></li>`);
  if (anyChange(D.datasets) && state.arrows !== false) items.push(`<li><span class="item"><span class="sw" style="height:2px;background:var(--range)" aria-hidden="true"></span><span>${P ? 'Arrow: where each point moved from' : 'Arrow: from the default position to the position at the changed assumptions'}</span></span></li>`);
  $('legend').innerHTML = items.join('');
  $('legend').querySelectorAll('[data-leg]').forEach((b) => b.addEventListener('click', () => {
    const k = b.dataset.leg, others = D.datasets.map((d) => d.key).filter((x) => x !== k);
    const only = !state.hide.includes(k) && others.every((x) => state.hide.includes(x));
    set({ hide: only ? [] : others });
  }));
  D.datasets.forEach((d) => { const cb = $('ds-' + d.short); if (cb) cb.checked = !state.hide.includes(d.key); });
  $('caption-state').textContent = anyChange(D.datasets) ? (P ? 'Some assumptions are changed (listed at the top); arrows show where points moved.' : 'Assumptions changed from the sources’ defaults (listed at the top); arrows show each point’s shift.') : (P ? 'Assumptions as the sources give them.' : 'Assumptions at the sources’ defaults.');
}

function card() {
  const d = state.sel && D.datasets.find((x) => x.sysById && x.sysById[state.sel]);
  $('card-empty').hidden = !!d; $('card-body').hidden = !d;
  if (!d) return;
  const s = d.sysById[state.sel], di = D.datasets.indexOf(d), rows = s.rows.map((i) => cache[di][i]).filter((q) => q.g_bar > 0);
  $('card-name').textContent = s.name_in_source;
  $('card-meta').textContent = `${s.class_in_source} · ${d.title.split(':')[0]} · ${rows.length} radii` + (state.pick !== 'all' ? ' · the map shows one of them (' + (state.pick === 'outer' ? 'the outermost' : 'the first at ≥ ' + LIGHT_K + ' × half-light radius') + ')' : '');
  $('card-link').href = BASE + 'systems/' + s.system_id + '/';
  $('card-flags').textContent = s.rows.some((i) => ringed(d.rows[i].flags)) ? 'Some measurements are flagged; see Known issues.' : 'No flags on this system.';
  const prof = $('card-prof'), W = Math.max(220, prof.parentElement.clientWidth - 34), H = Math.round(W * 0.62), g = setup(prof, W, H);
  const isLog = d.name === 'aeg-d-xcop';
  let lo = Infinity, hi = -Infinity; rows.forEach((q) => { lo = Math.min(lo, lg(q.g_bar), lg(q.g_obs)); hi = Math.max(hi, lg(q.g_bar), lg(q.g_obs)); });
  lo = Math.floor(lo * 2) / 2; hi = Math.ceil(hi * 2) / 2;
  const rv = (r) => (isLog ? Math.log10(r) : r), r0 = isLog ? rv(rows[0].r_kpc) : 0, r1 = rv(rows[rows.length - 1].r_kpc);
  const L = 44, T = 8, B = 30, pw = W - L - 6, ph = H - T - B;
  const X = (r) => L + (rv(r) - r0) / (r1 - r0) * pw, Y = (v) => T + (hi - v) / (hi - lo) * ph;
  g.strokeStyle = css('--ink'); g.lineWidth = 0.8; g.strokeRect(L, T, pw, ph);
  g.font = '11px ' + css('--mono'); g.fillStyle = css('--muted'); g.textAlign = 'right';
  [lo, (lo + hi) / 2, hi].forEach((v) => g.fillText(v.toFixed(1), L - 5, Y(v) + 4));
  g.textAlign = 'center'; const rS = rows[0].r_kpc, rE = rows[rows.length - 1].r_kpc;
  (isLog ? [rS, Math.sqrt(rS * rE), rE] : [0, rE / 2, rE]).forEach((r) => g.fillText(r < 10 ? r.toFixed(1) : String(Math.round(r)), X(r), T + ph + 14));
  g.font = '12px ' + css('--sans'); g.fillStyle = css('--ink'); g.fillText(isLog ? 'radius (kpc, log scale)' : 'radius (kpc)', L + pw / 2, H - 2);
  g.strokeStyle = css('--bar'); g.lineWidth = 1.8; g.beginPath(); rows.forEach((q, i) => (i ? g.lineTo(X(q.r_kpc), Y(lg(q.g_bar))) : g.moveTo(X(q.r_kpc), Y(lg(q.g_bar))))); g.stroke();
  g.fillStyle = css('--sel'); rows.forEach((q) => { g.beginPath(); g.arc(X(q.r_kpc), Y(lg(q.g_obs)), 2.3, 0, 6.2832); g.fill(); });
  prof.setAttribute('aria-label', `log g_obs and log g_bar of ${s.name_in_source} against radius`);
}

function render() { compute(); computePick(); prepareCats(); draw(); legend(); colorKey(); card(); syncControls(); }
function syncControls() {
  document.querySelectorAll('[data-view]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.view === state.view)));
  document.querySelectorAll('[data-marks]').forEach((b) => { b.setAttribute('aria-pressed', String(b.dataset.marks === state.marks)); b.disabled = state.pick !== 'all'; });
  document.querySelectorAll('[data-pick]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.pick === state.pick)));
  $('colsel').value = state.col in PROPS || state.col === 'channel' ? state.col : 'dataset';
  $('err').checked = state.err;
}

function nearest(ev) {
  const rect = $('fig').getBoundingClientRect(), mx = ev.clientX - rect.left, my = ev.clientY - rect.top;
  let best = null, bd = 64; for (const h of hits) { const dd = (h.x - mx) ** 2 + (h.y - my) ** 2; if (dd < bd) { bd = dd; best = h; } } return best;
}

export async function start() {
  D = await loadData();
  document.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => set({ view: b.dataset.view, zoom: null })));
  document.querySelectorAll('[data-marks]').forEach((b) => b.addEventListener('click', () => set({ marks: b.dataset.marks })));
  document.querySelectorAll('[data-pick]').forEach((b) => b.addEventListener('click', () => set({ pick: b.dataset.pick })));
  $('colsel').addEventListener('change', (e) => set({ col: e.target.value }));
  $('err').addEventListener('change', (e) => set({ err: e.target.checked }));
  $('arrows').addEventListener('change', (e) => { state.arrows = e.target.checked; render(); });
  D.datasets.forEach((d) => { const cb = $('ds-' + d.short); if (cb) cb.addEventListener('change', () => set({ hide: cb.checked ? state.hide.filter((k) => k !== d.key) : [...state.hide, d.key] })); });
  $('card-clear').addEventListener('click', () => set({ sel: null }));
  const fig = $('fig'), tip = $('tip'), box = $('figbox');
  wireZoom(fig);
  fig.addEventListener('mousemove', (ev) => {
    if (brush || pinch || panning) return;
    const h = nearest(ev); hover = h; draw();
    if (!h) { tip.hidden = true; return; }
    const q = h.q, r = h.r, name = r.system_id ? h.d.sysById[r.system_id].name_in_source : (LBL.bin + (r.x_kids1000_rar_sample ? ' · ' + r.x_kids1000_rar_sample.replace(/_/g, ' ') : ''));
    const Pp = PROPS[state.col], pv = Pp ? Pp.get(h.d, r) : null;
    const propLine = Pp ? `<br>${Pp.label.replace(/ \(.*\)$/, '')}: ${pv === null || pv === undefined ? 'not given' : Pp.kind === 'cont' ? Pp.fmt(pv) : pv}` : '';
    const extra = propLine + (state.view === 'mass' ? `<br>M_obs(&lt;r) ${sci(massOf(q.g_obs, q.r_kpc))} M☉<br>M_bar(&lt;r) ${sci(massOf(q.g_bar, q.r_kpc))} M☉` : state.view === 'speed' ? `<br>V_obs ${speedOf(q.g_obs, q.r_kpc).toFixed(1)} km s⁻¹` : '');
    showTip(tip, box, `<b>${name}</b>${state.pick !== 'all' && r.system_id ? '<br><span class="muted">' + (state.pick === 'outer' ? 'Outermost measured radius' : 'First measured radius ≥ ' + LIGHT_K + ' × half-light radius') + '</span>' : ''}<br>${h.d.title.split(':')[0]}${r.r_kpc !== null && r.r_kpc !== undefined ? ' · r = ' + (q.r_kpc < 10 ? q.r_kpc.toFixed(2) : Math.round(q.r_kpc)) + ' kpc' : ''}<br>g_obs ${sci(q.g_obs)} m s⁻²<br>g_bar ${sci(q.g_bar)} m s⁻²${extra}<br>g_obs / g_bar ${(q.g_obs / q.g_bar).toFixed(2)}${r.flags ? '<br><span style="color:var(--flag)">Flagged: ' + r.flags.replace(/;/g, ', ') + '</span>' : ''}<br><span class="muted">${r.measurement_id}</span>${r.system_id ? '<br><span class="muted">Click to select</span>' : ''}`, h.x, h.y);
  });
  fig.addEventListener('mouseleave', () => { hover = null; tip.hidden = true; draw(); });
  fig.addEventListener('click', (ev) => { if (suppressClick) { suppressClick = false; return; } const h = nearest(ev); if (h && h.r.system_id) set({ sel: h.r.system_id }); });
  wireSliders();
  onChange(render);
  window.addEventListener('atlas-theme', render); window.addEventListener('atlas-layer', render);
  new ResizeObserver(() => render()).observe(box);
  render();
}

// --- Zoom interactions: drag a box, Ctrl/⌘ + wheel, pinch, buttons and keys --------------------
let suppressClick = false, pinch = null, panMode = false, panning = null;
const toData = (px, py) => ({ x: geom.rg.x[0] + (px - geom.L) / geom.pw * (geom.rg.x[1] - geom.rg.x[0]), y: geom.rg.y[1] - (py - geom.T) / geom.ph * (geom.rg.y[1] - geom.rg.y[0]) });
function setZoom(x0, x1, y0, y1) {
  const b = geom.base, cx = (a) => Math.min(b.x[1], Math.max(b.x[0], a)), cy = (a) => Math.min(b.y[1], Math.max(b.y[0], a));
  let z = [cx(Math.min(x0, x1)), cx(Math.max(x0, x1)), cy(Math.min(y0, y1)), cy(Math.max(y0, y1))];
  const full = z[0] <= b.x[0] + 1e-9 && z[1] >= b.x[1] - 1e-9 && z[2] <= b.y[0] + 1e-9 && z[3] >= b.y[1] - 1e-9;
  if (z[1] - z[0] < (b.x[1] - b.x[0]) / 400 || z[3] - z[2] < (b.y[1] - b.y[0]) / 400) return; // smallest window: 1/400 of the full range
  set({ zoom: full ? null : z });
}
function scaleAbout(fx, fy, cxData, cyData) {
  const r = geom.rg;
  setZoom(cxData - (cxData - r.x[0]) * fx, cxData + (r.x[1] - cxData) * fx, cyData - (cyData - r.y[0]) * fy, cyData + (r.y[1] - cyData) * fy);
}
function shift(dx, dy) {
  const r = geom.rg, b = geom.base, w = r.x[1] - r.x[0], h = r.y[1] - r.y[0];
  const x0 = Math.min(b.x[1] - w, Math.max(b.x[0], r.x[0] + dx * w)), y0 = Math.min(b.y[1] - h, Math.max(b.y[0], r.y[0] + dy * h));
  setZoom(x0, x0 + w, y0, y0 + h);
}
function panTo(r0, dxPx, dyPx) {
  const b = geom.base, w = r0.x[1] - r0.x[0], h = r0.y[1] - r0.y[0];
  const x0 = Math.min(b.x[1] - w, Math.max(b.x[0], r0.x[0] - dxPx / geom.pw * w)), y0 = Math.min(b.y[1] - h, Math.max(b.y[0], r0.y[0] + dyPx / geom.ph * h));
  setZoom(x0, x0 + w, y0, y0 + h);
}
function setPanMode(on) {
  panMode = on; const fig = $('fig');
  $('zoom-pan').setAttribute('aria-pressed', String(on));
  fig.classList.toggle('panning', on);
}
function wireZoom(fig) {
  const local = (ev) => { const rc = fig.getBoundingClientRect(); return { x: ev.clientX - rc.left, y: ev.clientY - rc.top }; };
  const inPlot = (p) => p.x >= geom.L && p.x <= geom.L + geom.pw && p.y >= geom.T && p.y <= geom.T + geom.ph;
  const touches = new Map();
  let start = null;
  fig.addEventListener('pointerdown', (ev) => {
    if (ev.pointerType === 'touch') {
      touches.set(ev.pointerId, local(ev));
      if (touches.size === 2) { const [a, b] = [...touches.values()]; pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), c: { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }, rg: { x: [...geom.rg.x], y: [...geom.rg.y] } }; }
      return;
    }
    const p = local(ev); if (!inPlot(p)) return;
    if (ev.button === 1 || (ev.button === 0 && panMode)) { // middle button, or pan mode: drag to pan
      ev.preventDefault(); panning = { p, rg: { x: [...geom.rg.x], y: [...geom.rg.y] }, moved: false }; fig.setPointerCapture(ev.pointerId); fig.classList.add('grabbing'); return;
    }
    if (ev.button !== 0) return;
    start = p; fig.setPointerCapture(ev.pointerId);
  });
  // Stop the browser's own middle-button autoscroll over the chart.
  fig.addEventListener('mousedown', (ev) => { if (ev.button === 1) ev.preventDefault(); });
  fig.addEventListener('auxclick', (ev) => { if (ev.button === 1) ev.preventDefault(); });
  fig.addEventListener('pointermove', (ev) => {
    if (ev.pointerType === 'touch') {
      if (!touches.has(ev.pointerId)) return;
      touches.set(ev.pointerId, local(ev));
      if (panMode && touches.size === 1 && !pinch) {
        const t = [...touches.values()][0];
        if (!panning) panning = { p: t, rg: { x: [...geom.rg.x], y: [...geom.rg.y] }, moved: false };
        else { panning.moved = true; panTo(panning.rg, t.x - panning.p.x, t.y - panning.p.y); }
        return;
      }
      if (pinch && touches.size === 2) {
        const [a, b] = [...touches.values()], d = Math.hypot(a.x - b.x, a.y - b.y), c = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
        const k = pinch.d / Math.max(d, 1), r0 = pinch.rg, sx = (r0.x[1] - r0.x[0]) / geom.pw, sy = (r0.y[1] - r0.y[0]) / geom.ph;
        const cx = r0.x[0] + (pinch.c.x - geom.L) * sx, cy = r0.y[1] - (pinch.c.y - geom.T) * sy;
        const w = (r0.x[1] - r0.x[0]) * k, h = (r0.y[1] - r0.y[0]) * k, mx = -(c.x - pinch.c.x) * sx * k, my = (c.y - pinch.c.y) * sy * k;
        const fx = (cx - r0.x[0]) / (r0.x[1] - r0.x[0]), fy = (cy - r0.y[0]) / (r0.y[1] - r0.y[0]);
        setZoom(cx - fx * w + mx, cx + (1 - fx) * w + mx, cy - fy * h + my, cy + (1 - fy) * h + my);
      }
      return;
    }
    if (panning) { const p = local(ev), dx = p.x - panning.p.x, dy = p.y - panning.p.y; if (Math.abs(dx) + Math.abs(dy) > 2) { panning.moved = true; $('tip').hidden = true; panTo(panning.rg, dx, dy); } return; }
    if (!start) return;
    const p = local(ev), L = geom.L, T = geom.T, R = L + geom.pw, Bm = T + geom.ph;
    const cx = (v) => Math.min(R, Math.max(L, v)), cy = (v) => Math.min(Bm, Math.max(T, v));
    if (Math.abs(p.x - start.x) > 4 || Math.abs(p.y - start.y) > 4) { brush = { x0: Math.min(start.x, cx(p.x)), x1: Math.max(start.x, cx(p.x)), y0: Math.min(start.y, cy(p.y)), y1: Math.max(start.y, cy(p.y)) }; $('tip').hidden = true; draw(); }
  });
  const end = (ev) => {
    if (ev.pointerType === 'touch') { touches.delete(ev.pointerId); if (touches.size < 2) pinch = null; if (panning && touches.size === 0) { if (panning.moved) suppressClick = true; panning = null; } return; }
    if (panning) { if (panning.moved) suppressClick = true; panning = null; fig.classList.remove('grabbing'); return; }
    if (!start) return;
    const b = brush; start = null; brush = null;
    if (b && b.x1 - b.x0 > 8 && b.y1 - b.y0 > 8) { suppressClick = true; const p0 = toData(b.x0, b.y1), p1 = toData(b.x1, b.y0); setZoom(p0.x, p1.x, p0.y, p1.y); }
    else draw();
  };
  fig.addEventListener('pointerup', end); fig.addEventListener('pointercancel', end);
  fig.addEventListener('dblclick', () => set({ zoom: null }));
  fig.addEventListener('wheel', (ev) => {
    // Inside the plot the wheel zooms about the pointer: forward in, backward out. Outside the plot,
    // or backward at the full view (nothing further to zoom out to), the page scrolls as usual.
    const p = local(ev); if (!inPlot(p)) return;
    const dy = ev.deltaMode === 1 ? ev.deltaY * 33 : ev.deltaY;
    if (dy > 0 && !state.zoom) return;
    ev.preventDefault();
    const d = toData(p.x, p.y), f = Math.exp(Math.sign(dy) * Math.min(Math.abs(dy), 300) * 0.002);
    scaleAbout(f, f, d.x, d.y);
  }, { passive: false });
  fig.addEventListener('keydown', (ev) => {
    const r = geom.rg, c = { x: (r.x[0] + r.x[1]) / 2, y: (r.y[0] + r.y[1]) / 2 };
    const k = ev.key;
    if (k === '+' || k === '=') scaleAbout(0.67, 0.67, c.x, c.y);
    else if (k === '-' || k === '_') scaleAbout(1.5, 1.5, c.x, c.y);
    else if (k === '0') set({ zoom: null });
    else if (k === 'p' || k === 'P') setPanMode(!panMode);
    else if (k === 'ArrowLeft') shift(-0.2, 0); else if (k === 'ArrowRight') shift(0.2, 0);
    else if (k === 'ArrowUp') shift(0, 0.2); else if (k === 'ArrowDown') shift(0, -0.2);
    else return;
    ev.preventDefault();
  });
  $('zoom-in').addEventListener('click', () => { const r = geom.rg; scaleAbout(0.67, 0.67, (r.x[0] + r.x[1]) / 2, (r.y[0] + r.y[1]) / 2); });
  $('zoom-out').addEventListener('click', () => { const r = geom.rg; scaleAbout(1.5, 1.5, (r.x[0] + r.x[1]) / 2, (r.y[0] + r.y[1]) / 2); });
  $('zoom-reset').addEventListener('click', () => set({ zoom: null }));
  $('zoom-pan').addEventListener('click', () => setPanMode(!panMode));
}
