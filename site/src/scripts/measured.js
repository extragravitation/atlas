// "As measured" panel (D-029, D-030): the quantities the source released, before the Atlas turns
// them into g_obs and g_bar. Values are the package's extension columns, exactly as released.
import { css, plain } from './ui.js';
import { setup, axes, niceStep, sci, showTip } from './draw.js';

const $ = (id) => document.getElementById(id);

export function drawMeasured(d, rows) {
  const box = $('measbox'); if (!box) return;
  const P = plain(), W = box.clientWidth, L = 64, R = 14, T = 12, B = 46, pw = W - L - R, ph = Math.round(Math.min(Math.max(pw * 0.5, 240), 400));
  const g = setup($('meas'), W, ph + T + B), cv = $('meas');
  let series = [], xlab, ylab, logX = false, logY = false, items = [];
  if (d.name === 'aeg-d-sparc') {
    series = [
      { k: 'x_sparc_v_obs', err: 'x_sparc_e_v_obs', col: '--sel', pts: true, lab: ['V_obs ± e_V_obs, observed circular velocity', 'Observed speed of rotation, with its uncertainty'] },
      { k: 'x_sparc_v_gas', col: '--gas', dash: [5, 3], lab: ['V_gas (atomic gas, × 1.33 for helium)', 'Speed the gas alone would give'] },
      { k: 'x_sparc_v_disk', col: '--disc', lab: ['V_disk at M/L = 1 (3.6 μm)', 'Speed the disc stars alone would give, before choosing their mass-to-light ratio'] },
      { k: 'x_sparc_v_bul', col: '--bulge', lab: ['V_bul at M/L = 1 (3.6 μm)', 'Speed the bulge stars alone would give, before choosing their mass-to-light ratio'] },
    ].filter((s) => rows.some((r) => r[s.k]));
    xlab = P ? 'distance from the centre (kpc)' : 'R (kpc)'; ylab = P ? 'speed (km s⁻¹)' : 'velocity (km s⁻¹)';
  } else if (d.name === 'aeg-d-xcop') {
    series = [
      { k: 'x_xcop_m_forw', relErr: true, col: '--sel', pts: true, lab: ['M_HSE(&lt;r), forward-method hydrostatic mass (source)', 'Total mass inferred by the source from the hot gas'] },
      { k: 'x_xcop_m_gas', col: '--gas', lab: ['M_gas(&lt;r), hot-gas mass (source)', 'Mass of hot gas'] },
      { k: 'x_xcop_m_star', col: '--stars', lab: ['M_★(&lt;r), stellar mass (source; modelled per D-022 where not measured)', 'Mass of stars'] },
    ];
    logX = true; logY = true; xlab = P ? 'distance from the centre (kpc, log scale)' : 'r (kpc, log scale)'; ylab = P ? 'mass within that distance (M☉, log)' : 'mass within r (M☉, log)';
  } else return;
  const xs = rows.map((r) => r.r_kpc), tx = (v) => (logX ? Math.log10(v) : v), ty = (v) => (logY ? (v > 0 ? Math.log10(v) : null) : v);
  let ymin = Infinity, ymax = -Infinity;
  for (const s of series) for (const r of rows) { const v = r[s.k]; if (v === null || v === undefined) continue; const e = s.err ? r[s.err] || 0 : 0; const a = ty(v - e), b = ty(v + e); if (a !== null) ymin = Math.min(ymin, a); if (b !== null) ymax = Math.max(ymax, b); }
  if (!logY) { ymin = Math.min(0, ymin); ymax *= 1.06; } else { ymin = Math.floor(ymin * 2) / 2; ymax = Math.ceil(ymax * 2) / 2; }
  const x0 = logX ? Math.floor(tx(Math.min(...xs)) * 10) / 10 : 0, x1 = logX ? Math.ceil(tx(Math.max(...xs)) * 10) / 10 : (() => { const m = Math.max(...xs) * 1.02, st = niceStep(m); return Math.ceil(m / st) * st; })();
  const rg = { x: [x0, x1], y: [ymin, ymax] }, ystep = logY ? 1 : niceStep(ymax - ymin);
  const ax = axes(g, W, L, T, pw, ph, rg, xlab, ylab, logX ? 0.5 : niceStep(x1), ystep, 0, logX ? (a) => { const v = Math.pow(10, a); return v < 100 ? v.toFixed(0) : String(Math.round(v / 10) * 10); } : null);
  const X = (r) => ax.X(tx(r)), Y = (v) => ax.Y(ty(v));
  g.save(); g.beginPath(); g.rect(L, T, pw, ph); g.clip();
  const hits = [];
  for (const s of series) {
    const c = css(s.col);
    if (s.pts) {
      for (const r of rows) { const v = r[s.k]; if (!(v > 0) && logY) continue; const e = s.err ? r[s.err] || 0 : s.relErr ? v * ((r.g_obs_err_hi || 0) / r.g_obs) : 0; const x = X(r.r_kpc);
        if (e) { g.strokeStyle = c; g.globalAlpha = 0.6; g.lineWidth = 0.9; g.beginPath(); g.moveTo(x, Y(Math.max(v - e, logY ? v * 0.01 : -Infinity))); g.lineTo(x, Y(v + e)); g.stroke(); g.globalAlpha = 1; }
        g.fillStyle = c; g.beginPath(); g.arc(x, Y(v), 2.6, 0, 6.2832); g.fill(); hits.push({ x, y: Y(v), r, s }); }
    } else {
      g.strokeStyle = c; g.lineWidth = 1.7; g.setLineDash(s.dash || []); g.beginPath(); let st = false;
      for (const r of rows) { const v = r[s.k]; if (v === null || v === undefined || (logY && !(v > 0))) { st = false; continue; } const p = [X(r.r_kpc), Y(v)]; if (st) g.lineTo(...p); else { g.moveTo(...p); st = true; } }
      g.stroke(); g.setLineDash([]);
    }
    items.push(`<li><span class="item"><span class="sw" style="${s.pts ? 'border-radius:50%;' : 'height:3px;'}background:var(${s.col})" aria-hidden="true"></span><span>${s.lab[+P]}</span></span></li>`);
  }
  if (!logY && ymin < 0) { g.strokeStyle = css('--muted'); g.lineWidth = 0.8; g.beginPath(); g.moveTo(L, Y(0)); g.lineTo(L + pw, Y(0)); g.stroke(); }
  g.restore();
  $('measlegend').innerHTML = items.join('');
  cv.setAttribute('aria-label', P ? 'The measurements as the source released them, against distance from the centre' : 'Source quantities as released, against radius');
  cv.onmousemove = (ev) => {
    const rect = cv.getBoundingClientRect(), mx = ev.clientX - rect.left; let best = null, bd = 1e9;
    for (const h of hits) { const dd = Math.abs(h.x - mx); if (dd < bd) { bd = dd; best = h; } }
    if (!best || bd > 24) { $('meastip').hidden = true; return; }
    const r = best.r, lines = series.map((s) => r[s.k] === null || r[s.k] === undefined ? '' : `${s.lab[0].split(',')[0].replace('&lt;', '<')} ${d.name === 'aeg-d-sparc' ? r[s.k] + ' km s⁻¹' : sci(r[s.k]) + ' M☉'}`).filter(Boolean);
    showTip($('meastip'), box, `<b>r = ${r.r_kpc < 10 ? r.r_kpc.toFixed(2) : Math.round(r.r_kpc)} kpc</b><br>${lines.join('<br>')}<br><span class="muted">${r.measurement_id}</span>`, best.x, best.y);
  };
  cv.onmouseleave = () => { $('meastip').hidden = true; };
}
