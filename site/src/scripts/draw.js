// Drawing helpers shared by the figures: canvas setup at device resolution, framed axes on one
// scale for marks, ticks and labels, and the continuous colour scale for the discrepancy.
import { css } from './ui.js';

export function setup(c, w, h) {
  const r = window.devicePixelRatio || 1;
  c.width = Math.round(w * r); c.height = Math.round(h * r); c.style.height = h + 'px';
  const g = c.getContext('2d'); g.setTransform(r, 0, 0, r, 0, 0); g.clearRect(0, 0, w, h); return g;
}

export function niceStep(span) { const r = span / 5, e = Math.pow(10, Math.floor(Math.log10(r))), m = r / e; return (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * e; }

export function axes(g, W, L, T, pw, ph, rg, xlab, ylab, xstep, ystep, ydec, xfmt) {
  const X = (v) => L + (v - rg.x[0]) / (rg.x[1] - rg.x[0]) * pw;
  const Y = (v) => T + (rg.y[1] - v) / (rg.y[1] - rg.y[0]) * ph;
  g.font = '12px ' + css('--mono'); g.fillStyle = css('--muted'); g.lineWidth = 1; g.textAlign = 'center';
  for (let a = Math.ceil(rg.x[0] / xstep - 1e-9) * xstep; a <= rg.x[1] + 1e-9; a += xstep) {
    g.strokeStyle = css('--grid'); g.beginPath(); g.moveTo(X(a), T); g.lineTo(X(a), T + ph); g.stroke();
    g.fillText(xfmt ? xfmt(a) : (xstep < 1 ? a.toFixed(1) : String(Math.round(a))), X(a), T + ph + 16);
  }
  g.textAlign = 'right';
  for (let b = Math.ceil(rg.y[0] / ystep - 1e-9) * ystep; b <= rg.y[1] + 1e-9; b += ystep) {
    g.strokeStyle = css('--grid'); g.beginPath(); g.moveTo(L, Y(b)); g.lineTo(L + pw, Y(b)); g.stroke();
    g.fillText(b.toFixed(ydec), L - 6, Y(b) + 4);
  }
  g.strokeStyle = css('--ink'); g.strokeRect(L, T, pw, ph);
  g.font = (W < 560 ? '12px ' : '14px ') + css('--sans'); g.fillStyle = css('--ink'); g.textAlign = 'center';
  if (xlab) g.fillText(xlab, L + pw / 2, T + ph + 38);
  g.save(); g.translate(14, T + ph / 2); g.rotate(-Math.PI / 2); g.fillText(ylab, 0, 0); g.restore();
  return { X, Y };
}

function hex(h) { h = h.replace('#', ''); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); }
export function cmap(v) {
  const t = Math.max(0, Math.min(1, v / 1.5)) * 4, k = Math.min(3, Math.floor(t)), u = t - k;
  const a = hex(css('--c' + k)), b = hex(css('--c' + (k + 1)));
  return 'rgb(' + [0, 1, 2].map((j) => Math.round(a[j] + (b[j] - a[j]) * u)).join(',') + ')';
}

const SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹';
export function sci(v, digits = 3) {
  if (v === null || v === undefined || !isFinite(v)) return '–';
  if (v === 0) return '0';
  const neg = v < 0, a = Math.abs(v), e = Math.floor(Math.log10(a)), m = a / Math.pow(10, e);
  return (neg ? '−' : '') + m.toFixed(digits - 1) + '×10' + String(e).replace('-', '⁻').replace(/\d/g, (c) => SUP[c]);
}

export function showTip(el, wrap, html, x, y) {
  el.innerHTML = html; el.hidden = false;
  const bw = wrap.clientWidth; let left = x + 14; if (left + 260 > bw) left = x - 274;
  el.style.left = Math.max(0, left) + 'px'; el.style.top = (y + 14) + 'px';
}
