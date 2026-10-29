// System page (object level): the pull budget. The source's baryonic components stacked against
// the observed acceleration, with the g_bar uncertainty, the full published ranges of the
// assumptions, each point's range within its own errors, and the share g_bar / g_obs. Optional
// orbital-speed view. Everything is computed from the package rows and the registry formulas.
import { loadData, adjusted, systemChanged, speed, ringed } from './model.js';
import { state, set, onChange } from './state.js';
import { css, plain } from './ui.js';
import { setup, axes, niceStep, sci, showTip } from './draw.js';
import { wireSliders } from './sliders.js';

const $ = (id) => document.getElementById(id);
const CFG = JSON.parse($('budget-config').textContent);
const COMP = { g_bar_stars_disk: ['--disc', 'Stars, disc', 'Stars in the disc'], g_bar_stars_bulge: ['--bulge', 'Stars, bulge', 'Stars in the central bulge'], g_bar_gas_cold: ['--gas', 'Cold gas (atomic, with helium)', 'Cold gas'], g_bar_stars: ['--stars', 'Stars', 'Stars'], g_bar_gas_hot: ['--gas', 'Hot gas (X-ray)', 'Hot gas'] };
let D = null, d = null, sys = null, rows = [], hits = [], hover = null;

function layers() {
  const cols = d.name === 'aeg-d-sparc' ? ['g_bar_stars_disk', 'g_bar_stars_bulge', 'g_bar_gas_cold'] : ['g_bar_stars', 'g_bar_gas_hot'];
  return cols.filter((c) => rows.some((r) => r[c] !== null && r[c] !== undefined && r[c] !== 0));
}

// Assumptions that apply to this system, split by what they move.
function groups() {
  const applies = d.sliders.filter((a) => rows.some((r) => (r.adjustable || '').split(';').includes(a.id)));
  const movesBar = applies.filter((a) => (a.effects || []).some((e) => e.column === 'g_bar'));
  const movesObs = applies.filter((a) => (a.effects || []).some((e) => e.column === 'g_obs'));
  return { movesBar, movesObs };
}

function draw() {
  const P = plain(), sp = state.unit === 'speed', box = $('budbox'), W = box.clientWidth;
  const q = rows.map((r) => adjusted(d, r));
  const lay = layers(), { movesBar, movesObs } = groups();
  const val = (g, r) => (sp ? speed(g, r) : g * 1e10);
  const isLog = d.name === 'aeg-d-xcop', rv = (r) => (isLog ? Math.log10(r) : r);
  const ghosts = state.rng && movesBar.length ? ['min', 'max'].map((k) => rows.map((r) => adjusted(d, r, Object.fromEntries(movesBar.map((a) => [a.id, a[k]]))))) : [];
  const ranges = state.rng ? rows.map((r, i) => movesObs.map((a) => [adjusted(d, r, { [a.id]: a.min }), adjusted(d, r, { [a.id]: a.max })])) : [];
  let ymax = 0, ymin = 0;
  q.forEach((x, i) => {
    ymax = Math.max(ymax, val(x.g_obs + (x.g_obs_err_hi || 0), x.r_kpc), val(x.g_bar + (state.eb ? x.g_bar_err_hi || 0 : 0), x.r_kpc));
    if (!sp) ymax = Math.max(ymax, lay.reduce((s, c) => s + Math.max(0, x[c] || 0), 0) * 1e10);
    for (const gh of ghosts) ymax = Math.max(ymax, val(gh[i].g_bar, gh[i].r_kpc));
    for (const pr of ranges[i] || []) for (const y of pr) ymax = Math.max(ymax, val(y.g_obs, y.r_kpc));
    for (const c of lay) ymin = Math.min(ymin, sp ? speed(x[c] || 0, x.r_kpc) : (x[c] || 0) * 1e10);
    if (!sp) ymin = Math.min(ymin, lay.reduce((s, c) => s + (x[c] || 0), 0) * 1e10);
  });
  ymax *= 1.06;
  const rr = q.map((x) => x.r_kpc);
  const rg = { x: isLog ? [Math.floor(rv(Math.min(...rr)) * 10) / 10, Math.ceil(rv(Math.max(...rr)) * 10) / 10] : [0, (() => { const m = Math.max(...rr) * 1.02, st = niceStep(m); return Math.ceil(m / st) * st; })()], y: [ymin < 0 ? ymin * 1.15 : 0, ymax] };
  const L = 64, R = 14, T = 14, B = 50, pw = W - L - R, ph = Math.round(Math.min(Math.max(pw * 0.55, 260), 460));
  const g = setup($('bud'), W, ph + T + B), ystep = niceStep(rg.y[1] - rg.y[0]);
  const ax = axes(g, W, L, T, pw, ph, rg, isLog ? 'radius (kpc, log scale)' : 'radius (kpc)', sp ? CFG.spd[+P] : CFG.acc[+P], isLog ? 0.5 : niceStep(rg.x[1]), ystep, ystep < 1 ? (ystep < 0.1 ? 2 : 1) : 0, isLog ? (a) => { const v = Math.pow(10, a); return v < 100 ? v.toFixed(0) : String(Math.round(v / 10) * 10); } : null);
  const X = (r) => ax.X(rv(r)), Y = ax.Y;
  const line = (pts, col, w, dash, alpha) => { g.strokeStyle = col; g.lineWidth = w; g.globalAlpha = alpha || 1; g.setLineDash(dash || []); g.beginPath(); pts.forEach((p, i) => (i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]))); g.stroke(); g.setLineDash([]); g.globalAlpha = 1; };
  const band = (top, bot, col, alpha) => { g.fillStyle = col; g.globalAlpha = alpha; g.beginPath(); top.forEach((p, i) => (i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]))); for (let i = bot.length - 1; i >= 0; i--) g.lineTo(bot[i][0], bot[i][1]); g.closePath(); g.fill(); g.globalAlpha = 1; };
  g.save(); g.beginPath(); g.rect(L, T, pw, ph); g.clip();
  if (!sp) {
    let base = q.map(() => 0);
    for (const c of lay) { const top = q.map((x, i) => base[i] + (x[c] || 0) * 1e10); band(q.map((x, i) => [X(x.r_kpc), Y(top[i])]), q.map((x, i) => [X(x.r_kpc), Y(base[i])]), css(COMP[c][0]), 0.85); base = top; }
    band(q.map((x) => [X(x.r_kpc), Y(x.g_obs * 1e10)]), q.map((x, i) => [X(x.r_kpc), Y(base[i])]), css('--rem'), parseFloat(css('--remAlpha')) || 0.12);
  } else {
    for (const c of lay) line(q.map((x) => [X(x.r_kpc), Y(speed(x[c] || 0, x.r_kpc))]), css(COMP[c][0]), 1.6, c.includes('gas') ? [5, 3] : null);
  }
  if (state.eb) band(q.map((x) => [X(x.r_kpc), Y(val(x.g_bar + (x.g_bar_err_hi || 0), x.r_kpc))]), q.map((x) => [X(x.r_kpc), Y(val(Math.max(0, x.g_bar - (x.g_bar_err_lo || 0)), x.r_kpc))]), css('--bar'), 0.22);
  line(q.map((x) => [X(x.r_kpc), Y(val(x.g_bar, x.r_kpc))]), css('--bar'), 1.9);
  if (ymin < 0) line([[L, Y(0)], [L + pw, Y(0)]], css('--muted'), 0.8);
  for (const gh of ghosts) line(gh.map((x) => [X(x.r_kpc), Y(val(x.g_bar, x.r_kpc))]), css('--range'), 1.2, [4, 4], 0.9);
  hits = [];
  q.forEach((x, i) => {
    const r = rows[i], px = X(x.r_kpc), py = Y(val(x.g_obs, x.r_kpc));
    if (state.rng) for (const [a0, a1] of ranges[i] || []) { g.strokeStyle = css('--range'); g.globalAlpha = 0.35; g.lineWidth = 2; g.lineCap = 'round'; g.beginPath(); g.moveTo(X(a0.r_kpc), Y(val(a0.g_obs, a0.r_kpc))); g.lineTo(X(a1.r_kpc), Y(val(a1.g_obs, a1.r_kpc))); g.stroke(); g.globalAlpha = 1; g.lineCap = 'butt'; }
    const lo = x.g_obs - (x.g_obs_err_lo || 0), hi = x.g_obs + (x.g_obs_err_hi || 0);
    g.strokeStyle = css('--sel'); g.globalAlpha = 0.7; g.lineWidth = 0.9; g.beginPath(); g.moveTo(px, Y(val(Math.max(lo, 0), x.r_kpc))); g.lineTo(px, Y(val(hi, x.r_kpc))); g.stroke(); g.globalAlpha = 1;
    g.fillStyle = css('--sel'); g.beginPath(); g.arc(px, py, 2.7, 0, 6.2832); g.fill();
    if (ringed(r.flags)) { g.strokeStyle = css('--flag'); g.lineWidth = 0.9; g.beginPath(); g.arc(px, py, 5, 0, 6.2832); g.stroke(); }
    hits.push({ x: px, y: py, r, q: x });
  });
  if (hover) { g.strokeStyle = css('--ink'); g.setLineDash([3, 3]); g.beginPath(); g.moveTo(hover.x, T); g.lineTo(hover.x, T + ph); g.stroke(); g.setLineDash([]); }
  g.restore();
  $('bud').setAttribute('aria-label', (sp ? CFG.ariaSpeed : CFG.ariaAcc)[+P]);

  // share strip: g_bar / g_obs
  const share = q.map((x) => x.g_bar / x.g_obs), sh = Math.round(Math.min(pw * 0.2, 150)) + 30, g2 = setup($('share'), W, sh), sph = sh - 30;
  const smax = Math.min(2, Math.max(1.1, Math.ceil(Math.max(...share) * 10) / 10)), clip = (v) => Math.min(v, smax);
  const rg2 = { x: rg.x, y: [Math.min(0, Math.floor(Math.min(...share) * 10) / 10), smax] };
  const ax2 = axes(g2, W, L, 6, pw, sph, rg2, null, CFG.share[+P], 99, rg2.y[1] - rg2.y[0] > 1.5 ? 0.5 : 0.25, 2);
  g2.save(); g2.beginPath(); g2.rect(L, 6, pw, sph); g2.clip();
  g2.setLineDash([5, 4]); g2.strokeStyle = css('--ink'); g2.lineWidth = 1; g2.beginPath(); g2.moveTo(L, ax2.Y(1)); g2.lineTo(L + pw, ax2.Y(1)); g2.stroke(); g2.setLineDash([]);
  if (state.eb) { g2.fillStyle = css('--bar'); g2.globalAlpha = 0.22; g2.beginPath(); q.forEach((x, i) => { const v = (x.g_bar + (x.g_bar_err_hi || 0)) / x.g_obs; i ? g2.lineTo(X(x.r_kpc), ax2.Y(v)) : g2.moveTo(X(x.r_kpc), ax2.Y(v)); }); for (let i = q.length - 1; i >= 0; i--) g2.lineTo(X(q[i].r_kpc), ax2.Y((q[i].g_bar - (q[i].g_bar_err_lo || 0)) / q[i].g_obs)); g2.closePath(); g2.fill(); g2.globalAlpha = 1; }
  g2.strokeStyle = css('--bar'); g2.lineWidth = 1.8; g2.beginPath(); q.forEach((x, i) => (i ? g2.lineTo(X(x.r_kpc), ax2.Y(clip(share[i]))) : g2.moveTo(X(x.r_kpc), ax2.Y(clip(share[i]))))); g2.stroke();
  g2.fillStyle = css('--bar'); q.forEach((x, i) => { if (share[i] > smax) { const px = X(x.r_kpc), py = ax2.Y(smax) + 2; g2.beginPath(); g2.moveTo(px, py); g2.lineTo(px - 4, py + 7); g2.lineTo(px + 4, py + 7); g2.closePath(); g2.fill(); } });
  g2.font = 'italic 12px ' + css('--serif'); g2.fillStyle = css('--ink'); g2.textAlign = 'right'; g2.fillText(P ? 'all of the observed pull' : 'g_bar = g_obs', L + pw - 6, ax2.Y(1) - 5 < 18 ? ax2.Y(1) + 14 : ax2.Y(1) - 5);
  if (hover) { g2.strokeStyle = css('--ink'); g2.setLineDash([3, 3]); g2.beginPath(); g2.moveTo(hover.x, 6); g2.lineTo(hover.x, 6 + sph); g2.stroke(); g2.setLineDash([]); }
  g2.restore();
  $('share').setAttribute('aria-label', CFG.ariaShare[+P]);

  // legend and caption
  const items = [];
  for (const c of lay) items.push(`<li><span class="item"><span class="sw" style="${sp ? 'height:3px;' : ''}background:var(${COMP[c][0]})" aria-hidden="true"></span><span>${COMP[c][1 + P]}${c === 'g_bar_stars' && rows.some((r) => r.stars_status === 'modelled') ? (P ? ' (estimated from a model, decision D-023)' : ' (modelled, D-023)') : ''}</span></span></li>`);
  items.push(`<li><span class="item"><span class="sw" style="height:3px;background:var(--bar)" aria-hidden="true"></span><span>${sp ? CFG.vbar[+P] : CFG.gbar[+P]}</span></span></li>`);
  if (state.eb) items.push(`<li><span class="item"><span class="sw" style="background:var(--bar);opacity:0.35" aria-hidden="true"></span><span>${CFG.ebText}</span></span></li>`);
  if (!sp) items.push(`<li><span class="item"><span class="sw" style="background:var(--rem);opacity:0.35" aria-hidden="true"></span><span>${CFG.rem[+P]}</span></span></li>`);
  items.push(`<li><span class="item"><span class="sw" style="border-radius:50%;background:var(--sel)" aria-hidden="true"></span><span>${sp ? CFG.vobs[+P] : CFG.gobs[+P]}, one-sigma bars</span></span></li>`);
  if (state.rng && movesBar.length) items.push(`<li><span class="item"><span class="sw" style="height:0;border-top:2px dashed var(--range)" aria-hidden="true"></span><span>${P ? 'Detected matter at the two ends of the published range of' : 'g_bar at both ends of the full published range of'} ${movesBar.map((a) => CFG.names[a.id] || a.id).join(' and ')}</span></span></li>`);
  if (state.rng && movesObs.length) items.push(`<li><span class="item"><span class="sw" style="width:4px;border-radius:2px;background:var(--range);opacity:0.6" aria-hidden="true"></span><span>${P ? 'Where each point could move within' : 'Each point across the full range of'} ${movesObs.map((a) => CFG.names[a.id] || a.id).join(' and ')}${movesObs.some((a) => a.id === 'distance') ? (P ? ' (slanted: the distance from the centre changes too)' : ' (slanted where the radius moves too)') : ''}</span></span></li>`);
  if (state.rng) items.push(`<li><span class="item muted">${P ? 'Ranges show what each assumption could do, whatever the sliders are set to.' : 'Full published ranges are shown independent of the current settings.'}</span></li>`);
  $('blegend').innerHTML = items.join('');
  const pick = (target) => { let b = 0; q.forEach((x, i) => { if (Math.abs(x.r_kpc - target) < Math.abs(q[b].r_kpc - target)) b = i; }); return b; };
  const pc = (i) => `${Math.round(share[i] * 100)}% at ${q[i].r_kpc < 10 ? q[i].r_kpc.toFixed(1) : Math.round(q[i].r_kpc)} kpc`;
  const iMid = pick(q[q.length - 1].r_kpc / 2), nClip = share.filter((v) => v > smax).length;
  $('bcaption').innerHTML = `<b>Figure.</b> ${sp ? CFG.capSpeed[+P] : CFG.capAcc[+P]} ${P ? 'Lower panel: the share of the observed pull that detected matter explains' : 'Lower panel: g_bar / g_obs, the share of the observed acceleration accounted for by detected matter'}: ${pc(0)}, ${pc(iMid)}, ${pc(q.length - 1)}.${nClip ? (P ? ` ${nClip} value${nClip > 1 ? 's' : ''} above ${Math.round(smax * 100)}% marked with a triangle at the top.` : ` ${nClip} value${nClip > 1 ? 's' : ''} above ${smax.toFixed(1)} shown as triangles at the top edge (see the table).`) : ''}${ymin < 0 ? (P ? ' A layer below zero means that part of the matter pulls outward at those distances, as the source gives it.' : ' A component below zero is a net outward pull from that component at those radii, as the source gives it.') : ''} ${systemChanged(d, sys.system_id) ? (P ? 'Some assumptions are changed (listed at the top).' : 'Assumptions differ from the source’s defaults (listed at the top).') : (P ? 'Assumptions as the source gives them.' : 'Assumptions at the source’s defaults.')}`;
  table(q);
}

function table(q) {
  $('tbody').innerHTML = q.map((x, i) => { const r = rows[i]; return `<tr><td class="l">${r.measurement_id.split('/').pop()}</td><td>${x.r_kpc < 10 ? x.r_kpc.toFixed(3) : x.r_kpc.toFixed(1)}</td><td>${sci(x.g_obs)}</td><td>${sci(x.g_obs_err_lo)} / ${sci(x.g_obs_err_hi)}</td><td>${sci(x.g_bar)}</td><td>${x.g_bar_err_lo === null || x.g_bar_err_lo === undefined ? '–' : sci(x.g_bar_err_lo) + ' / ' + sci(x.g_bar_err_hi)}</td><td>${(x.g_obs / x.g_bar).toFixed(2)}</td><td>${Math.round((x.g_bar / x.g_obs) * 100)}%</td><td class="l">${(r.flags || '').replace(/;/g, ', ')}</td></tr>`; }).join('');
  $('tnote').textContent = systemChanged(d, sys.system_id) ? 'Values at the changed assumptions listed at the top; the downloads hold the source’s defaults.' : 'Values at the source’s defaults, exactly as in the package table.';
}

export async function start() {
  D = await loadData();
  d = D.byKey[CFG.dataset]; sys = d.sysById[CFG.system]; rows = sys.rows.map((i) => d.rows[i]);
  document.querySelectorAll('[data-unit]').forEach((b) => b.addEventListener('click', () => set({ unit: b.dataset.unit })));
  $('show-eb').addEventListener('change', (e) => set({ eb: e.target.checked }));
  $('show-rng').addEventListener('change', (e) => set({ rng: e.target.checked }));
  const sync = () => { document.querySelectorAll('[data-unit]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.unit === state.unit))); $('show-eb').checked = state.eb; $('show-rng').checked = state.rng; };
  const bud = $('bud'), tip = $('btip'), box = $('budbox');
  bud.addEventListener('mousemove', (ev) => {
    const rect = bud.getBoundingClientRect(), mx = ev.clientX - rect.left; let best = null, bd = Infinity;
    for (const h of hits) { const dd = Math.abs(h.x - mx); if (dd < bd) { bd = dd; best = h; } }
    if (!best || bd > 30) { hover = null; tip.hidden = true; draw(); return; }
    hover = best; draw();
    const x = best.q, comps = layers().map((c) => `${COMP[c][1]} ${sci(x[c])}`).join('<br>');
    showTip(tip, box, `<b>r = ${x.r_kpc < 10 ? x.r_kpc.toFixed(2) : x.r_kpc.toFixed(0)} kpc</b><br>${state.unit === 'speed' ? `V_obs ${speed(x.g_obs, x.r_kpc).toFixed(1)} km s⁻¹<br>V_bar ${speed(x.g_bar, x.r_kpc).toFixed(1)} km s⁻¹<br>` : ''}g_obs ${sci(x.g_obs)} m s⁻²<br>g_bar ${sci(x.g_bar)} m s⁻²<br>${comps}<br>g_bar / g_obs ${Math.round((x.g_bar / x.g_obs) * 100)}%${best.r.flags ? '<br><span style="color:var(--flag)">' + best.r.flags.replace(/;/g, ', ') + '</span>' : ''}<br><span class="muted">${best.r.measurement_id}</span>`, best.x, best.y);
  });
  bud.addEventListener('mouseleave', () => { hover = null; tip.hidden = true; draw(); });
  wireSliders();
  onChange(() => { sync(); draw(); });
  window.addEventListener('atlas-theme', draw); window.addEventListener('atlas-layer', draw);
  new ResizeObserver(draw).observe(box);
  sync(); draw();
}
