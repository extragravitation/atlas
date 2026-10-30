// Reader state shared by every page: display choices, dataset-wide assumptions and per-system
// assumptions. Kept in the address (shareable, D-027) and in this tab's session storage, so it
// survives moving between pages. Nothing is sent anywhere.

const KEYS = ['view', 'pick', 'marks', 'err', 'col', 'hide', 'sel', 'a', 's', 'unit', 'eb', 'rng', 'z'];
export const state = { view: 'obs', pick: 'all', marks: 'points', err: false, col: 'dataset', hide: [], sel: null, global: {}, per: {}, unit: 'acc', eb: true, rng: true, zoom: null };
const listeners = [];

function decode(q) {
  if (q.has('view')) state.view = q.get('view');
  if (q.has('pick')) state.pick = ['all', 'outer', 'light'].includes(q.get('pick')) ? q.get('pick') : 'all';
  if (q.has('marks')) state.marks = q.get('marks');
  if (q.has('err')) state.err = q.get('err') === '1';
  if (q.has('col')) state.col = q.get('col');
  if (q.has('hide')) state.hide = q.get('hide').split(',').filter(Boolean);
  if (q.has('sel')) state.sel = q.get('sel') || null;
  if (q.has('unit')) state.unit = q.get('unit');
  if (q.has('eb')) state.eb = q.get('eb') !== '0';
  if (q.has('rng')) state.rng = q.get('rng') !== '0';
  if (q.has('z')) { const z = q.get('z').split(',').map(Number); state.zoom = z.length === 4 && z.every(isFinite) && z[0] < z[1] && z[2] < z[3] ? z : null; }
  if (q.has('a')) { state.global = {}; for (const part of q.get('a').split(';').filter(Boolean)) { const [k, v] = part.split('='); if (k && v !== undefined && isFinite(+v)) state.global[k] = +v; } }
  if (q.has('s')) { state.per = {}; for (const part of q.get('s').split(';').filter(Boolean)) { const m = part.match(/^([^:]+):([^=]+)=(.+)$/); if (m && isFinite(+m[3])) (state.per[m[1]] = state.per[m[1]] || {})[m[2]] = +m[3]; } }
}

export function encode(forPage) {
  const q = new URLSearchParams();
  const page = forPage || '';
  if (page !== 'other') {
    if (state.view !== 'obs') q.set('view', state.view);
    if (state.pick !== 'all') q.set('pick', state.pick);
    if (state.marks !== 'points') q.set('marks', state.marks);
    if (state.err) q.set('err', '1');
    if (state.col !== 'dataset') q.set('col', state.col);
    if (state.hide.length) q.set('hide', state.hide.join(','));
    if (state.sel) q.set('sel', state.sel);
    if (state.unit !== 'acc') q.set('unit', state.unit);
    if (!state.eb) q.set('eb', '0');
    if (!state.rng) q.set('rng', '0');
    if (state.zoom) q.set('z', state.zoom.map((v) => +v.toFixed(3)).join(','));
  }
  const a = Object.entries(state.global).map(([k, v]) => k + '=' + v).join(';');
  if (a) q.set('a', a);
  const s = Object.entries(state.per).flatMap(([id, o]) => Object.entries(o).map(([k, v]) => id + ':' + k + '=' + v)).join(';');
  if (s) q.set('s', s);
  return q.toString();
}

let inited = false;
export function init() {
  if (inited) return;
  inited = true;
  let q = new URLSearchParams(location.search);
  const hasState = KEYS.some((k) => q.has(k));
  if (!hasState) { try { const saved = sessionStorage.getItem('atlas-state'); if (saved) q = new URLSearchParams(saved); } catch (e) { /* storage unavailable */ } }
  decode(q);
  save();
}

export function save() {
  const s = encode();
  try { sessionStorage.setItem('atlas-state', s); } catch (e) { /* storage unavailable */ }
  // Display choices go in the address only on the pages that show figures; assumptions always do.
  const shown = document.body && document.body.dataset.figures === '1' ? s : encode('other');
  const url = location.pathname + (shown ? '?' + shown : '') + location.hash;
  try { history.replaceState(null, '', url); } catch (e) { /* ignore */ }
}

export function set(patch) { Object.assign(state, patch); save(); listeners.forEach((f) => f()); }
export function setGlobal(key, value, def) { if (Math.abs(value - def) < 1e-12) delete state.global[key]; else state.global[key] = value; save(); listeners.forEach((f) => f()); }
export function setPer(sysId, id, value, def) {
  const o = state.per[sysId] || {};
  if (Math.abs(value - def) < 1e-12) delete o[id]; else o[id] = value;
  if (Object.keys(o).length) state.per[sysId] = o; else delete state.per[sysId];
  save(); listeners.forEach((f) => f());
}
export function resetAll() { state.global = {}; state.per = {}; save(); listeners.forEach((f) => f()); }
export function onChange(f) { listeners.push(f); }
export function emit() { listeners.forEach((f) => f()); }

if (typeof window !== 'undefined') init();
