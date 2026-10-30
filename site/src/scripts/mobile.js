// Phone "Explore" screen for the map: a full-screen view that does not scroll. The chart fills the
// top of the screen and the controls sit in a fixed area below it, so every change is seen as it is
// made. The rail's own sections (and their handlers) are moved in, never copied, and go back on close.
// Opened from the Explore button on the phone page, or with #explore in the address; the phone's Back
// button closes it.
import { state, onChange, save } from './state.js';
import { plain } from './ui.js';

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

function summary() {
  const el = $('msum'); if (!el) return;
  const P = plain();
  const lens = { obs: P ? 'Pull' : 'Acceleration', ex: P ? 'Extra pull' : 'Excess', mass: 'Mass', rad: P ? 'Distance' : 'Scale', speed: 'Speed' }[state.view] || state.view;
  const pick = { all: P ? 'every point' : 'every measurement', outer: P ? 'one per galaxy' : 'one per system (outermost)', light: P ? 'one per galaxy (same size)' : 'one per system (2 × half-light)' }[state.pick];
  const col = ((document.querySelector('#colsel option:checked') || {}).textContent || 'Dataset').replace(/ \(.*\)$/, '');
  const changed = Object.keys(state.global).length + Object.keys(state.per).length;
  el.textContent = `${lens} · ${pick} · ${col}${state.hide.length ? ` · ${state.hide.length} off` : ''}${changed ? ` · ${changed} changed` : ''}`;
}

export function mobilePanel() {
  const sheet = $('msheet'); if (!sheet) return;
  const mq = window.matchMedia(PHONE);
  document.body.classList.toggle('touch', window.matchMedia('(pointer: coarse)').matches);
  sheet.querySelectorAll('[data-mtab]').forEach((b) => b.addEventListener('click', () => select(b.dataset.mtab)));
  $('explore-open').addEventListener('click', () => { if (location.hash !== '#explore') location.hash = 'explore'; else enter(); });
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
}
