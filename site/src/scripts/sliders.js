// Wires the assumption sliders on a page to the shared state. Dataset-wide sliders set one value
// for the dataset; per-system sliders set a value for the system named in data-system.
import { state, setGlobal, setPer, onChange } from './state.js';
import { fmtParam } from './ui.js';

export function wireSliders(root = document) {
  const els = [...root.querySelectorAll('.slider[data-key]')];
  const sync = () => {
    for (const el of els) {
      const input = el.querySelector('input'), out = el.querySelector('output');
      const def = +el.dataset.def, kind = el.dataset.kind;
      const v = el.dataset.scope === 'system' ? ((state.per[el.dataset.system] || {})[el.dataset.id] ?? def) : (state.global[el.dataset.key] ?? def);
      if (document.activeElement !== input) input.value = v;
      out.textContent = fmtParam({ unitKind: kind }, v);
    }
  };
  for (const el of els) {
    const input = el.querySelector('input'), def = +el.dataset.def;
    input.addEventListener('input', () => {
      const v = parseFloat(input.value);
      if (el.dataset.scope === 'system') setPer(el.dataset.system, el.dataset.id, v, def);
      else setGlobal(el.dataset.key, v, def);
    });
  }
  onChange(sync);
  sync();
}
