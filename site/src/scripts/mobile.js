// Phone "Explore" screen for the map: a full-screen view that does not scroll. The chart fills the
// top of the screen and the controls sit in a fixed area below it, so every change is seen as it is
// made. The rail's own sections (and their handlers) are moved in, never copied, and go back on close.
// Opened from the Explore button on the phone page, or with #explore in the address; the phone's Back
// button closes it.
import { state, onChange, save } from './state.js';
import { plain, sliderIndex, fmtParam } from './ui.js';

const $ = (id) => document.getElementById(id);
const PHONE = '(max-width: 760px)';
const NOTES = { lens: 'lens-note', points: 'pick-note', colours: 'colkey' };

let homes = [];
let active = 'lens';
let open = false;

function moveInto(node, target) {
  if (!node) return;
  homes.push([node, node.parentNode, node.nextSibling]);
  target.appendChild(node);
}

function clampNotes(root) {
  root.querySelectorAll('p.small').forEach((p) => {
    if (p.dataset.clamp) return;
    p.dataset.clamp = '1'; p.classList.add('clamp'); p.tabIndex = 0; p.setAttribute('role', 'button'); p.setAttribute('aria-expanded', 'false');
    const t = () => { const o = p.classList.toggle('open'); p.setAttribute('aria-expanded', String(o)); };
    p.addEventListener('click', t); p.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t(); } });
  });
}

function fit() {
  // Size the chart to the space between the top bar and the controls.
  if (!open) return;
  const box = $('figbox'), bar = $('xbar'), zoom = document.querySelector('#figbox .zoombar');
  const avail = window.innerHeight * 0.58 - (bar ? bar.offsetHeight : 44) - (zoom ? zoom.offsetHeight + 4 : 0);
  box.dataset.maxh = String(Math.max(160, Math.round(avail)));
  window.dispatchEvent(new Event('atlas-theme')); // redraw at the new size
}

function enter() {
  if (open) return;
  open = true;
  const sheet = $('msheet'), panels = $('mpanels');
  panels.innerHTML = '';
  for (const b of sheet.querySelectorAll('[data-mtab]')) {
    const key = b.dataset.mtab, panel = document.createElement('div');
    panel.className = 'mpanel'; panel.dataset.panel = key; panel.setAttribute('role', 'tabpanel');
    panels.appendChild(panel);
    moveInto(document.querySelector(`.rail [data-tab="${key}"]`), panel);
    if (NOTES[key]) moveInto($(NOTES[key]), panel);
    if (key === 'system') moveInto(document.querySelector('.layout > .card'), panel);
  }
  clampNotes(panels);
  document.body.classList.add('explore');
  sheet.hidden = false; $('xbar').hidden = false;
  select(active);
  summary();
  requestAnimationFrame(fit);
}

function leave() {
  if (!open) return;
  open = false;
  for (const [node, parent, next] of homes.reverse()) parent.insertBefore(node, next && next.parentNode === parent ? next : null);
  homes = [];
  document.body.classList.remove('explore');
  $('msheet').hidden = true; $('xbar').hidden = true;
  delete $('figbox').dataset.maxh;
  save(); // keep the address in step with the settings chosen in Explore
  window.dispatchEvent(new Event('atlas-theme'));
}

function select(key) {
  active = key;
  document.querySelectorAll('[data-mtab]').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.mtab === key)));
  document.querySelectorAll('.mpanel').forEach((p) => { p.hidden = p.dataset.panel !== key; });
  const panels = $('mpanels'); if (panels) panels.scrollTop = 0;
  if (key === 'system') window.dispatchEvent(new Event('atlas-theme'));
}

// What the chart is based on, in words: lens, points, datasets, colours and assumptions (changed
// ones named with their values). Shown above the chart and in the Explore top bar.
export function describe() {
  const P = plain(), idx = sliderIndex();
  const lens = { obs: P ? 'pull view' : 'Acceleration lens', ex: P ? 'extra-pull view' : 'Excess lens', mass: P ? 'mass view' : 'Mass lens', rad: P ? 'distance view' : 'Scale lens', speed: P ? 'speed view' : 'Speed lens' }[state.view] || state.view;
  const pick = { all: P ? 'every point' : 'every measurement', outer: P ? 'one per galaxy, farthest point' : 'one per system, outermost radius', light: P ? 'one per galaxy, same relative size' : 'one per system, 2 × half-light radius' }[state.pick];
  const total = document.querySelectorAll('.rail [id^="ds-"], .mpanel [id^="ds-"]').length || 3, on = total - state.hide.length;
  const data = on === total ? (P ? 'all datasets' : `${total} of ${total} datasets`) : `${on} of ${total} datasets`;
  const col = ((document.querySelector('#colsel option:checked') || {}).textContent || 'Dataset').replace(/ \(.*\)$/, '').toLowerCase();
  const changed = Object.entries(state.global).map(([k, v]) => { const it = idx.find((x) => x.key === k); return it ? `${P ? it.label_p : it.label_t} ${fmtParam(it, v)} (changed)` : null; }).filter(Boolean);
  const per = Object.keys(state.per).length;
  if (per) changed.push(`${per} system${per > 1 ? 's' : ''} adjusted on ${per > 1 ? 'their' : 'its'} own page`);
  const assum = changed.length ? changed.join(', ') : (P ? 'assumptions as published' : 'assumptions at the sources’ defaults');
  return `${lens} · ${pick} · ${data} · ${P ? 'coloured by' : 'colours by'} ${col} · ${assum}${state.zoom ? (P ? ' · zoomed in' : ' · zoomed') : ''}`;
}

function summary() {
  const text = describe();
  const a = $('msum'), b = $('showing-text');
  if (a) a.textContent = text;
  if (b) b.textContent = text;
}

export function mobilePanel() {
  const sheet = $('msheet'); if (!sheet) return;
  const mq = window.matchMedia(PHONE);
  document.body.classList.toggle('touch', window.matchMedia('(pointer: coarse)').matches);
  sheet.querySelectorAll('[data-mtab]').forEach((b) => b.addEventListener('click', () => select(b.dataset.mtab)));
  const openX = () => { if (!mq.matches) return; if (location.hash !== '#explore') location.hash = 'explore'; else enter(); };
  $('explore-open').addEventListener('click', (e) => { e.stopPropagation(); openX(); });
  $('showing').addEventListener('click', openX);
  $('explore-close').addEventListener('click', () => { if (location.hash === '#explore') history.back(); else leave(); });
  const sync = () => { if (mq.matches && location.hash === '#explore') enter(); else leave(); };
  window.addEventListener('hashchange', sync);
  window.addEventListener('popstate', sync); // Back can change the query as well as the hash

  mq.addEventListener('change', sync);
  let lastSel = state.sel;
  onChange(() => { summary(); if (open && state.sel && state.sel !== lastSel) select('system'); lastSel = state.sel; });
  window.addEventListener('atlas-layer', summary);
  window.addEventListener('resize', () => { if (open) fit(); });
  // Expandable notes: closed on phones, open on wide screens.
  const notes = () => document.querySelectorAll('details[data-more]').forEach((d) => { d.open = !mq.matches; });
  mq.addEventListener('change', notes); notes();
  sync();
  summary();
}
