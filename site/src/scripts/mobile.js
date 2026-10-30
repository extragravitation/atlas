// Phone layout for the map: the chart stays pinned at the top and the controls live in a sheet
// below it (peek · half · full), so every change is seen as it is made. The rail's own sections
// (and their event handlers) are moved into the sheet, never copied; on a wide screen they go back.
import { state, onChange } from './state.js';
import { plain } from './ui.js';

const $ = (id) => document.getElementById(id);
const PHONE = '(max-width: 760px)';
const STATES = ['peek', 'half', 'full'];
const NOTES = { lens: 'lens-note', points: 'pick-note', colours: 'colkey' };

let homes = [];   // [node, parent, nextSibling] to restore on a wide screen
let active = 'lens';

function moveInto(node, target) {
  homes.push([node, node.parentNode, node.nextSibling]);
  target.appendChild(node);
}

function enter() {
  const sheet = $('msheet'), panels = $('mpanels');
  document.body.classList.add('phone-map');
  sheet.hidden = false;
  panels.innerHTML = '';
  for (const b of sheet.querySelectorAll('[data-mtab]')) {
    const key = b.dataset.mtab, panel = document.createElement('div');
    panel.className = 'mpanel'; panel.dataset.panel = key; panel.setAttribute('role', 'tabpanel');
    panels.appendChild(panel);
    const sec = document.querySelector(`.rail [data-tab="${key}"]`);
    if (sec) moveInto(sec, panel);
    if (NOTES[key] && $(NOTES[key])) moveInto($(NOTES[key]), panel);
    if (key === 'system') moveInto(document.querySelector('.layout > .card'), panel);
  }
  clampNotes(panels);
  select(active);
  setState(sheet.dataset.state || 'peek');
  document.querySelectorAll('details[data-more]').forEach((d) => { d.open = false; });
}

function leave() {
  const sheet = $('msheet');
  for (const [node, parent, next] of homes.reverse()) parent.insertBefore(node, next && next.parentNode === parent ? next : null);
  homes = [];
  sheet.hidden = true;
  document.body.classList.remove('phone-map');
  document.documentElement.style.removeProperty('--sheet-h');
  document.querySelectorAll('details[data-more]').forEach((d) => { d.open = true; });
}

function select(key) {
  active = key;
  document.querySelectorAll('[data-mtab]').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.mtab === key)));
  document.querySelectorAll('.mpanel').forEach((p) => { p.hidden = p.dataset.panel !== key; });
  if (key === 'system') window.dispatchEvent(new Event('atlas-theme')); // redraw the profile at its new width
}

function setState(s) {
  const sheet = $('msheet');
  sheet.dataset.state = s;
  const fig = document.querySelector('#figbox');
  const chartBottom = fig ? Math.min(fig.getBoundingClientRect().bottom, window.innerHeight * 0.62) : window.innerHeight * 0.5;
  const h = s === 'peek' ? 112 : s === 'half' ? Math.max(220, window.innerHeight - chartBottom - 8) : Math.round(window.innerHeight * 0.86);
  document.documentElement.style.setProperty('--sheet-h', h + 'px');
}

// Bring the chart to the top of the screen, then open the sheet to fill the space below it.
function openHalf() {
  const fig = document.querySelector('.layout > main figure');
  if (fig) { const top = fig.getBoundingClientRect().top + window.scrollY; window.scrollTo({ top, behavior: 'instant' }); }
  requestAnimationFrame(() => setState('half'));
}

// Long notes inside the sheet show two lines; a tap opens the rest.
function clampNotes(root) {
  root.querySelectorAll('p.small').forEach((p) => {
    if (p.dataset.clamp) return;
    p.dataset.clamp = '1'; p.classList.add('clamp'); p.tabIndex = 0; p.setAttribute('role', 'button'); p.setAttribute('aria-expanded', 'false');
    const t = () => { const o = p.classList.toggle('open'); p.setAttribute('aria-expanded', String(o)); };
    p.addEventListener('click', t); p.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t(); } });
  });
}

function summary() {
  const el = $('msum'); if (!el) return;
  const P = plain();
  const lens = { obs: P ? 'Pull' : 'Acceleration', ex: P ? 'Extra pull' : 'Excess', mass: 'Mass', rad: P ? 'Distance' : 'Scale', speed: 'Speed' }[state.view] || state.view;
  const pick = { all: P ? 'every point' : 'every measurement', outer: P ? 'one per galaxy, farthest' : 'one per system, outermost', light: P ? 'one per galaxy, same relative size' : 'one per system, 2 × half-light' }[state.pick];
  const col = (document.querySelector('#colsel option:checked') || {}).textContent || 'Dataset';
  const hidden = state.hide.length ? ` · ${state.hide.length} dataset${state.hide.length > 1 ? 's' : ''} off` : '';
  const changed = Object.keys(state.global).length + Object.keys(state.per).length;
  el.textContent = `${lens} · ${pick} · colours: ${col}${hidden}${changed ? ` · ${changed} assumption${changed > 1 ? 's' : ''} changed` : ''}`;
}

function wireDrag() {
  const handle = $('mhandle'), sheet = $('msheet');
  let y0 = null, h0 = 0, moved = false;
  handle.addEventListener('pointerdown', (e) => { y0 = e.clientY; h0 = sheet.getBoundingClientRect().height; moved = false; handle.setPointerCapture(e.pointerId); });
  handle.addEventListener('pointermove', (e) => {
    if (y0 === null) return;
    const dy = y0 - e.clientY; if (Math.abs(dy) > 6) moved = true;
    if (moved) document.documentElement.style.setProperty('--sheet-h', Math.max(80, Math.min(window.innerHeight * 0.9, h0 + dy)) + 'px');
  });
  const end = (e) => {
    if (y0 === null) return;
    if (!moved) { const i = STATES.indexOf(sheet.dataset.state); setState(STATES[(i + 1) % STATES.length]); }
    else {
      const h = sheet.getBoundingClientRect().height, vh = window.innerHeight;
      setState(h < vh * 0.25 ? 'peek' : h < vh * 0.65 ? 'half' : 'full');
    }
    y0 = null;
  };
  handle.addEventListener('pointerup', end); handle.addEventListener('pointercancel', end);
}

export function mobilePanel() {
  const sheet = $('msheet'); if (!sheet) return;
  const mq = window.matchMedia(PHONE);
  const touch = window.matchMedia('(pointer: coarse)').matches;
  document.body.classList.toggle('touch', touch);
  sheet.querySelectorAll('[data-mtab]').forEach((b) => b.addEventListener('click', () => {
    select(b.dataset.mtab);
    if (sheet.dataset.state === 'peek') openHalf();
  }));
  wireDrag();
  // Selecting a point opens the Selected tab; the chart stays in view.
  let lastSel = state.sel;
  onChange(() => {
    summary();
    if (mq.matches && state.sel && state.sel !== lastSel) { select('system'); if (sheet.dataset.state === 'peek') openHalf(); }
    lastSel = state.sel;
  });
  window.addEventListener('atlas-layer', summary);
  const apply = () => { if (mq.matches) { if (!homes.length) enter(); } else if (homes.length) leave(); else document.querySelectorAll('details[data-more]').forEach((d) => { d.open = true; }); summary(); };
  mq.addEventListener('change', apply);
  window.addEventListener('resize', () => { if (mq.matches) setState(sheet.dataset.state); });
  apply();
}
