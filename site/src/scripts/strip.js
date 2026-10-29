// Scale strip (population level): one bar per system across the radii where it was measured,
// shaded by log (g_obs / g_bar) on a continuous scale. Empty ranges are shown as empty.
import { loadData, adjusted } from './model.js';
import { state, set, onChange } from './state.js';
import { css, plain } from './ui.js';
import { setup, cmap, showTip } from './draw.js';
import { wireSliders } from './sliders.js';

const BASE = document.documentElement.dataset.base || '/';
const $ = (id) => document.getElementById(id);
const LBL = JSON.parse($('strip-labels').textContent);
let D = null, hits = [];

function draw() {
  const box = $('figbox'), W = box.clientWidth, narrow = W < 560, P = plain();
  const groups = D.datasets.filter((d) => d.systems && !state.hide.includes(d.key)).map((d) => {
    const sys = d.systems.map((s) => ({ d, s, q: s.rows.map((i) => adjusted(d, d.rows[i])).filter((q) => q.g_bar > 0 && q.r_kpc > 0) })).filter((x) => x.q.length);
    sys.sort((a, b) => a.q[a.q.length - 1].r_kpc - b.q[b.q.length - 1].r_kpc);
    return { d, sys };
  });
  let minR = Infinity; D.datasets.forEach((d) => d.systems && d.rows.forEach((r) => { if (r.r_kpc > 0) minR = Math.min(minR, r.r_kpc); }));
  const L = 12, R = 12, T = 52, rowH = narrow ? 3 : 3.4, gap = 34, pw = W - L - R;
  const rows = groups.reduce((n, gr) => n + gr.sys.length, 0), ph = rows * rowH + gap * Math.max(0, groups.length - 1) + 20 * groups.length;
  const H = Math.round(T + ph + 80), g = setup($('fig'), W, H);
  const xr = [-3, 3.5], X = (v) => L + (v - xr[0]) / (xr[1] - xr[0]) * pw;
  const tick = { '-3': '1 pc', '-2': '10 pc', '-1': '100 pc', '0': '1 kpc', '1': '10 kpc', '2': '100 kpc', '3': '1 Mpc' };
  g.font = '12px ' + css('--mono'); g.textAlign = 'center';
  for (let a = -3; a <= 3; a++) { g.strokeStyle = css('--grid'); g.beginPath(); g.moveTo(X(a), T - 6); g.lineTo(X(a), T + ph); g.stroke(); if (!narrow || a % 2 !== 0) { g.fillStyle = css('--muted'); g.fillText(tick[a], Math.max(X(a), L + 18), T - 26); } }
  g.fillStyle = css('--grid'); g.fillRect(X(xr[0]), T, X(Math.log10(minR)) - X(xr[0]), ph);
  g.fillStyle = css('--muted'); g.font = 'italic 13px ' + css('--serif'); const ex = (X(xr[0]) + X(Math.log10(minR))) / 2;
  (narrow ? LBL.emptyShort : LBL.empty)[+P].split('\n').forEach((line, i, all) => g.fillText(line, ex, T + ph / 2 + (i - (all.length - 1) / 2) * 18));
  hits = []; let y = T + 4;
  groups.forEach((gr, gi) => {
    if (gi) y += gap;
    g.font = '600 12px ' + css('--sans'); g.fillStyle = css('--ink'); g.textAlign = 'left'; g.fillText(`${LBL.group[gr.d.key][+P]} · ${gr.sys.length}`, X(Math.log10(minR)) + 6, y - 6);
    for (const { d, s, q } of gr.sys) {
      for (let i = 0; i < q.length; i++) {
        const r = q[i].r_kpc, r0 = i ? Math.sqrt(q[i - 1].r_kpc * r) : r, r1 = i < q.length - 1 ? Math.sqrt(r * q[i + 1].r_kpc) : r * 1.04;
        g.fillStyle = cmap(Math.log10(q[i].g_obs / q[i].g_bar)); g.fillRect(X(Math.log10(r0)), y, Math.max(1, X(Math.log10(r1)) - X(Math.log10(r0))), rowH - 0.6);
      }
      if (s.system_id === state.sel) { g.strokeStyle = css('--sel'); g.lineWidth = 1.5; g.strokeRect(X(Math.log10(q[0].r_kpc)) - 2, y - 1.5, X(Math.log10(q[q.length - 1].r_kpc)) - X(Math.log10(q[0].r_kpc)) + 4, rowH + 2); }
      hits.push({ y0: y, y1: y + rowH, d, s, q });
      y += rowH;
    }
    y += 20;
  });
  const cbW = Math.min(320, pw - 20), cbX = L + (pw - cbW) / 2, cbY = H - 40;
  for (let i = 0; i < cbW; i++) { g.fillStyle = cmap(i / cbW * 1.5); g.fillRect(cbX + i, cbY, 1.2, 10); }
  g.font = '12px ' + css('--mono'); g.fillStyle = css('--muted'); g.textAlign = 'center';
  [0, 0.5, 1, 1.5].forEach((v) => g.fillText((v === 1.5 ? '≥ ' : v === 0 ? '≤ ' : '') + v.toFixed(1), cbX + v / 1.5 * cbW, cbY + 24));
  g.font = '13px ' + css('--sans'); g.fillStyle = css('--ink'); g.fillText(LBL.scale[+P], cbX + cbW / 2, cbY - 6);
  $('fig').setAttribute('aria-label', LBL.aria[+P]);
}

export async function start() {
  D = await loadData();
  const fig = $('fig'), tip = $('tip'), box = $('figbox');
  const at = (ev) => { const r = fig.getBoundingClientRect(), my = ev.clientY - r.top; return { h: hits.find((h) => my >= h.y0 - 0.5 && my < h.y1 + 0.5), mx: ev.clientX - r.left, my }; };
  fig.addEventListener('mousemove', (ev) => {
    const { h, mx, my } = at(ev); if (!h) { tip.hidden = true; return; }
    const ex = h.q.map((q) => Math.log10(q.g_obs / q.g_bar));
    showTip(tip, box, `<b>${h.s.name_in_source}</b><br>${h.s.class_in_source}<br>${h.q[0].r_kpc.toFixed(h.q[0].r_kpc < 10 ? 2 : 0)}–${h.q[h.q.length - 1].r_kpc.toFixed(h.q[h.q.length - 1].r_kpc < 100 ? 1 : 0)} kpc, ${h.q.length} radii<br>log (g_obs/g_bar) ${Math.min(...ex).toFixed(2)} to ${Math.max(...ex).toFixed(2)}<br><span class="muted">Click to open its page</span>`, mx, my);
  });
  fig.addEventListener('mouseleave', () => { tip.hidden = true; });
  fig.addEventListener('click', (ev) => { const { h } = at(ev); if (h) location.href = BASE + 'systems/' + h.s.system_id + '/'; });
  D.datasets.forEach((d) => { const cb = $('ds-' + d.short); if (cb) { cb.checked = !state.hide.includes(d.key); cb.addEventListener('change', () => set({ hide: cb.checked ? state.hide.filter((k) => k !== d.key) : [...state.hide, d.key] })); } });
  wireSliders();
  onChange(draw); window.addEventListener('atlas-theme', draw); window.addEventListener('atlas-layer', draw);
  new ResizeObserver(draw).observe(box);
  draw();
}
