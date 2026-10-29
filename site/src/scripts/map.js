// The map (population level): g_obs against g_bar with the line g_obs = g_bar (D-012), display
// controls of D-027, no fitted relation (D-026). Every value comes from the package tables,
// adjusted only by the registry formulas for the assumptions the reader has changed.
import { loadData, adjusted, anyChange, ringed } from './model.js';
import { state, set, onChange } from './state.js';
import { css, plain } from './ui.js';
import { setup, axes, sci, showTip } from './draw.js';
import { wireSliders } from './sliders.js';

const BASE = document.documentElement.dataset.base || '/';
const $ = (id) => document.getElementById(id);
const COLOR = { 'aeg-d-sparc': '--sparc', 'aeg-d-xcop': '--xcop', 'aeg-d-kids1000-rar': '--kids' };
const LBL = JSON.parse($('map-labels').textContent);
let D = null, hits = [], hover = null, cache = null;

const lg = (v) => (v > 0 ? Math.log10(v) : null);
// Lenses (D-030): the same measurements in different framings. Spherical-equivalent enclosed mass
// M(<r) = g r² / G (in M☉, with the IAU nominal G M☉); equivalent circular speed V = √(g r).
const GM_SUN = 1.3271244e20, KPC = 3.0856775814913673e19;
const massOf = (g, r) => (g > 0 && r > 0 ? (g * (r * KPC) ** 2) / GM_SUN : null);
const speedOf = (g, r) => (g > 0 && r > 0 ? Math.sqrt(g * r * KPC) / 1000 : null);
const RADIAL = ['rad', 'mass', 'speed'];
function colorFor(d, row) { return state.col === 'channel' ? css(row.channel === 'lensing' ? '--kids' : '--sparc') : css(COLOR[d.name] || '--sparc'); }

function compute() {
  // Adjusted values for every row, once per state change.
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

function draw() {
  const box = $('figbox'), fig = $('fig'), W = box.clientWidth, narrow = W < 560, rg = ranges();
  const L = 58, R = 14, T = 12, B = 46, pw = W - L - R, ph = rg.equal ? pw * (rg.y[1] - rg.y[0]) / (rg.x[1] - rg.x[0]) : pw * 0.62;
  const g = setup(fig, W, Math.round(ph + T + B));
  const P = plain();
  if (!VIEWS.includes(state.view)) state.view = 'obs';
  const v = state.view, n = narrow ? 's' : '';
  const xl = v === 'mass' ? LBL['xm' + n][+P] : RADIAL.includes(v) ? LBL.xr[+P] : (narrow ? LBL.xs[+P] : LBL.x[+P]);
  const yl = v === 'obs' ? (narrow ? LBL.ys[+P] : LBL.y[+P]) : v === 'mass' ? LBL['ym' + n][+P] : v === 'speed' ? LBL['yv' + n][+P] : (narrow ? LBL.yxs[+P] : LBL.yx[+P]);
  const { X, Y } = axes(g, W, L, T, pw, ph, rg, xl, yl, 1, v === 'obs' || v === 'mass' ? 1 : 0.5, v === 'obs' || v === 'mass' ? 0 : 1);
  const ink = css('--ink'), alpha = parseFloat(css('--ptAlpha')) || 0.4, moved = anyChange(D.datasets);
  g.save(); g.beginPath(); g.rect(L, T, pw, ph); g.clip();
  g.setLineDash([6, 4]); g.strokeStyle = ink; g.lineWidth = 1.1; g.beginPath();
  if (v === 'obs' || v === 'mass') { g.moveTo(X(rg.x[0]), Y(rg.x[0])); g.lineTo(X(rg.x[1]), Y(rg.x[1])); } else if (v !== 'speed') { g.moveTo(L, Y(0)); g.lineTo(L + pw, Y(0)); }
  g.stroke(); g.setLineDash([]);
  g.font = 'italic 13px ' + css('--serif'); g.fillStyle = ink;
  if (v === 'obs') { const lx = narrow ? -12.4 : -12.7; g.save(); g.translate(X(lx), Y(lx) + 14); g.rotate(Math.atan2(Y(-10) - Y(-11), X(-10) - X(-11))); g.textAlign = 'center'; g.fillText(narrow ? LBL.zero[+P] : LBL.line[+P], 0, 0); g.restore(); }
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
    if (state.marks !== 'points' && !pop) {
      g.lineWidth = 0.9; g.globalAlpha = d.name === 'aeg-d-xcop' ? 0.8 : 0.4;
      for (const s of d.systems) { g.strokeStyle = col(d.rows[s.rows[0]]); g.beginPath(); let st = false; for (const i of s.rows) { const xy = pos(cache[di][i]); if (!xy) { st = false; continue; } if (st) g.lineTo(xy[0], xy[1]); else { g.moveTo(xy[0], xy[1]); st = true; } } g.stroke(); }
      g.globalAlpha = 1;
    }
    d.rows.forEach((r, i) => {
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
      if (shape === 'lensing') { g.save(); g.translate(x, y); g.rotate(Math.PI / 4); g.fillStyle = css('--bg'); g.fillRect(-3, -3, 6, 6); g.strokeStyle = c; g.lineWidth = 1.3; g.strokeRect(-3, -3, 6, 6); g.restore(); }
      else if (state.marks !== 'tracks') { g.fillStyle = c; g.globalAlpha = shape === 'hydrostatic' ? 0.8 : alpha; if (shape === 'kinematic') { g.beginPath(); g.arc(x, y, 1.7, 0, 6.2832); g.fill(); } else g.fillRect(x - 1.8, y - 1.8, 3.6, 3.6); g.globalAlpha = 1; }
      if (ringed(r.flags)) { g.strokeStyle = css('--flag'); g.lineWidth = 0.7; g.beginPath(); g.arc(x, y, 3.6, 0, 6.2832); g.stroke(); }
      if (r.system_id && state.per[r.system_id]) { g.strokeStyle = css('--range'); g.lineWidth = 1; g.strokeRect(x - 3.5, y - 3.5, 7, 7); }
      hits.push({ x, y, d, r, q });
    });
  });
  // selected system as a highlighted track
  const sel = state.sel && D.datasets.find((d) => d.sysById && d.sysById[state.sel]);
  if (sel) {
    const di = D.datasets.indexOf(sel), s = sel.sysById[state.sel], pts = s.rows.map((i) => pos(cache[di][i])).filter(Boolean);
    g.strokeStyle = css('--sel'); g.lineWidth = 2.2; g.beginPath(); pts.forEach((xy, i) => (i ? g.lineTo(xy[0], xy[1]) : g.moveTo(xy[0], xy[1]))); g.stroke();
    g.fillStyle = css('--sel'); pts.forEach((xy) => { g.beginPath(); g.arc(xy[0], xy[1], 2.6, 0, 6.2832); g.fill(); });
    if (pts.length) { const l = pts[pts.length - 1]; g.font = '600 13px ' + css('--sans'); g.textAlign = 'left'; g.fillText(s.name_in_source, l[0] + 8, l[1] + 4); }
  }
  if (hover) { g.strokeStyle = ink; g.lineWidth = 1.5; g.beginPath(); g.arc(hover.x, hover.y, 6, 0, 6.2832); g.stroke(); }
  g.restore();
  $('neg-note').textContent = nNeg ? `${nNeg} measurements have g_bar ≤ 0 at these settings (a component pulls outward) and cannot be placed on log axes; they are listed in the downloads.` : '';
  $('fig').setAttribute('aria-label', LBL['aria_' + v][+P]);
  $('lens-note').innerHTML = LBL.lens[v][+P] + (RADIAL.includes(v) && D.datasets.some((d) => !d.systems && !state.hide.includes(d.key)) ? ' ' + LBL.noRadius[+P] : '');
}

function legend() {
  const P = plain();
  const items = D.datasets.map((d) => {
    const shape = d.rows[0].method_class, c = COLOR[d.name] || '--sparc';
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
  $('card-meta').textContent = `${s.class_in_source} · ${d.title.split(':')[0]} · ${rows.length} radii`;
  $('card-link').href = BASE + 'systems/' + s.system_id + '/';
  $('card-flags').textContent = s.rows.some((i) => ringed(d.rows[i].flags)) ? 'Some measurements are flagged; see Known issues.' : 'No flags on this system.';
  const prof = $('card-prof'), W = prof.parentElement.clientWidth - 34, H = Math.round(W * 0.62), g = setup(prof, W, H);
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

function render() { compute(); draw(); legend(); card(); syncControls(); }
function syncControls() {
  document.querySelectorAll('[data-view]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.view === state.view)));
  document.querySelectorAll('[data-marks]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.marks === state.marks)));
  document.querySelectorAll('[data-col]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.col === state.col)));
  $('err').checked = state.err;
}

function nearest(ev) {
  const rect = $('fig').getBoundingClientRect(), mx = ev.clientX - rect.left, my = ev.clientY - rect.top;
  let best = null, bd = 64; for (const h of hits) { const dd = (h.x - mx) ** 2 + (h.y - my) ** 2; if (dd < bd) { bd = dd; best = h; } } return best;
}

export async function start() {
  D = await loadData();
  document.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => set({ view: b.dataset.view })));
  document.querySelectorAll('[data-marks]').forEach((b) => b.addEventListener('click', () => set({ marks: b.dataset.marks })));
  document.querySelectorAll('[data-col]').forEach((b) => b.addEventListener('click', () => set({ col: b.dataset.col })));
  $('err').addEventListener('change', (e) => set({ err: e.target.checked }));
  $('arrows').addEventListener('change', (e) => { state.arrows = e.target.checked; render(); });
  D.datasets.forEach((d) => { const cb = $('ds-' + d.short); if (cb) cb.addEventListener('change', () => set({ hide: cb.checked ? state.hide.filter((k) => k !== d.key) : [...state.hide, d.key] })); });
  $('card-clear').addEventListener('click', () => set({ sel: null }));
  const fig = $('fig'), tip = $('tip'), box = $('figbox');
  fig.addEventListener('mousemove', (ev) => {
    const h = nearest(ev); hover = h; draw();
    if (!h) { tip.hidden = true; return; }
    const q = h.q, r = h.r, name = r.system_id ? h.d.sysById[r.system_id].name_in_source : (LBL.bin + (r.x_kids1000_rar_sample ? ' · ' + r.x_kids1000_rar_sample.replace(/_/g, ' ') : ''));
    const extra = state.view === 'mass' ? `<br>M_obs(&lt;r) ${sci(massOf(q.g_obs, q.r_kpc))} M☉<br>M_bar(&lt;r) ${sci(massOf(q.g_bar, q.r_kpc))} M☉` : state.view === 'speed' ? `<br>V_obs ${speedOf(q.g_obs, q.r_kpc).toFixed(1)} km s⁻¹` : '';
    showTip(tip, box, `<b>${name}</b><br>${h.d.title.split(':')[0]}${r.r_kpc !== null && r.r_kpc !== undefined ? ' · r = ' + (q.r_kpc < 10 ? q.r_kpc.toFixed(2) : Math.round(q.r_kpc)) + ' kpc' : ''}<br>g_obs ${sci(q.g_obs)} m s⁻²<br>g_bar ${sci(q.g_bar)} m s⁻²${extra}<br>g_obs / g_bar ${(q.g_obs / q.g_bar).toFixed(2)}${r.flags ? '<br><span style="color:var(--flag)">Flagged: ' + r.flags.replace(/;/g, ', ') + '</span>' : ''}<br><span class="muted">${r.measurement_id}</span>${r.system_id ? '<br><span class="muted">Click to select</span>' : ''}`, h.x, h.y);
  });
  fig.addEventListener('mouseleave', () => { hover = null; tip.hidden = true; draw(); });
  fig.addEventListener('click', (ev) => { const h = nearest(ev); if (h && h.r.system_id) set({ sel: h.r.system_id }); });
  wireSliders();
  onChange(render);
  window.addEventListener('atlas-theme', render); window.addEventListener('atlas-layer', render);
  new ResizeObserver(() => render()).observe(box);
  render();
}
