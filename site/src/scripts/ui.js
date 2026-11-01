// Page chrome shared by every page: theme, reading layer, system search, changed-assumptions bar.
import { state, init, onChange, setGlobal, setPer, resetAll } from './state.js';

const BASE = document.documentElement.dataset.base || '/';
const $ = (id) => document.getElementById(id);

export function fmtParam(item, v) {
  if (item.unitKind === 'sigma') return (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(1) + 'σ';
  if (item.unitKind === 'percent') return Math.round(v * 100) + '%';
  if (item.unitKind === 'span') { if (Math.abs(v) < 1e-9) return 'default'; if (v < 0) return (1 - 0.47 * Math.abs(v)).toFixed(2) + ' × default'; return v >= 1 ? 'Salpeter value' : Math.round(v * 100) + '% to Salpeter'; }
  if (item.unitKind === 'imf') { if (Math.abs(v) < 1e-9) return 'Chabrier/Kroupa'; return v >= 1 ? 'Salpeter' : Math.round(v * 100) + '% to Salpeter'; }
  if (item.unitKind === 'range') { if (Math.abs(v) < 1e-9) return 'default'; if (v <= -1) return 'minimum'; if (v >= 1) return 'maximum'; return Math.round(Math.abs(v) * 100) + '% to ' + (v < 0 ? 'minimum' : 'maximum'); }
  return v.toFixed(2);
}

function sliderIndex() { try { return JSON.parse($('slider-index').textContent); } catch (e) { return []; } }
function systemIndex() { try { return JSON.parse($('system-index').textContent); } catch (e) { return []; } }

function theme() {
  const root = document.documentElement;
  const sync = () => { const light = root.dataset.theme === 'light'; $('th-d')?.setAttribute('aria-pressed', String(!light)); $('th-l')?.setAttribute('aria-pressed', String(light)); };
  $('th-d')?.addEventListener('click', () => { root.dataset.theme = 'dark'; try { localStorage.setItem('atlas-theme', 'dark'); } catch (e) {} sync(); window.dispatchEvent(new Event('atlas-theme')); });
  $('th-l')?.addEventListener('click', () => { root.dataset.theme = 'light'; try { localStorage.setItem('atlas-theme', 'light'); } catch (e) {} sync(); window.dispatchEvent(new Event('atlas-theme')); });
  sync();
}

function layer() {
  const root = document.documentElement;
  const q = new URLSearchParams(location.search).get('layer');
  if (q === 'plain' || q === 'technical') { root.dataset.layer = q; try { localStorage.setItem('atlas-layer', q); } catch (e) {} }
  const sync = () => { const plain = root.dataset.layer === 'plain'; $('lay-t')?.setAttribute('aria-pressed', String(!plain)); $('lay-p')?.setAttribute('aria-pressed', String(plain)); };
  const setL = (v) => { root.dataset.layer = v; try { localStorage.setItem('atlas-layer', v); } catch (e) {} sync(); window.dispatchEvent(new Event('atlas-layer')); };
  $('lay-t')?.addEventListener('click', () => setL('technical'));
  $('lay-p')?.addEventListener('click', () => setL('plain'));
  sync();
}

function search() {
  const input = $('q'); if (!input) return;
  const sys = systemIndex();
  const go = () => { const v = input.value.trim().toLowerCase(); const s = sys.find((x) => x.name.toLowerCase() === v || x.id === v); if (s) location.href = BASE + 'systems/' + s.id + '/'; };
  input.addEventListener('change', go);
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
}

function changesBar() {
  const el = $('changes'); if (!el) return;
  const idx = sliderIndex(), sys = systemIndex();
  const nameOf = (id) => (sys.find((s) => s.id === id) || {}).name || id;
  const render = () => {
    const items = [];
    for (const [k, v] of Object.entries(state.global)) {
      const it = idx.find((x) => x.key === k); if (!it) continue;
      items.push(`<span class="chip"><span data-l="t">${it.label_t}</span><span data-l="p">${it.label_p}</span> ${fmtParam(it, v)} · ${it.scopeText}<button type="button" data-rg="${k}" aria-label="Reset ${it.short} to ${fmtParam(it, it.default)}">×</button></span>`);
    }
    for (const [id, o] of Object.entries(state.per)) {
      const parts = Object.entries(o).map(([a, v]) => { const it = idx.find((x) => x.id === a && x.scope === 'system'); return (it ? it.short : a) + ' ' + (it ? fmtParam(it, v) : v); });
      items.push(`<span class="chip"><a href="${BASE}systems/${id}/">${nameOf(id)}</a> ${parts.join(', ')} · this system only<button type="button" data-rs="${id}" aria-label="Reset ${nameOf(id)}">×</button></span>`);
    }
    el.hidden = !items.length;
    el.innerHTML = '<span class="cap">Changed assumptions</span>' + items.join('') + '<button class="btn" type="button" id="reset-all">Reset all</button>';
    el.querySelectorAll('[data-rg]').forEach((b) => b.addEventListener('click', () => { const it = idx.find((x) => x.key === b.dataset.rg); setGlobal(b.dataset.rg, it.default, it.default); }));
    el.querySelectorAll('[data-rs]').forEach((b) => b.addEventListener('click', () => { const o = state.per[b.dataset.rs] || {}; for (const a of Object.keys(o)) { const it = idx.find((x) => x.id === a && x.scope === 'system'); setPer(b.dataset.rs, a, it ? it.default : 0, it ? it.default : 0); } }));
    el.querySelector('#reset-all')?.addEventListener('click', resetAll);
  };
  onChange(render);
  render();
}

export function chrome() { init(); theme(); layer(); search(); changesBar(); }
export function plain() { return document.documentElement.dataset.layer === 'plain'; }
export function css(n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }
export { sliderIndex, systemIndex };
