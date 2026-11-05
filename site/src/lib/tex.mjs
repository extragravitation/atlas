// Display of TeX in quoted source text (D-109 rule 4). Stored quotes stay exactly as read; this only
// changes how they are shown. Common TeX becomes readable text: Greek letters, sub- and superscripts,
// ±, ∼, ≲, ≳, ×, thin spaces, and citation commands to "(citation)". Pages show the raw quote beside
// it under "show as read" (components/Quote.astro). No maths-rendering library (D-109, rejected).

const GREEK = {
  alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', epsilon: 'ϵ', varepsilon: 'ε', zeta: 'ζ', eta: 'η', theta: 'θ', vartheta: 'ϑ',
  iota: 'ι', kappa: 'κ', lambda: 'λ', mu: 'μ', nu: 'ν', xi: 'ξ', pi: 'π', rho: 'ρ', varrho: 'ϱ', sigma: 'σ', varsigma: 'ς',
  tau: 'τ', upsilon: 'υ', phi: 'ϕ', varphi: 'φ', chi: 'χ', psi: 'ψ', omega: 'ω',
  Gamma: 'Γ', Delta: 'Δ', Theta: 'Θ', Lambda: 'Λ', Xi: 'Ξ', Pi: 'Π', Sigma: 'Σ', Upsilon: 'Υ', Phi: 'Φ', Psi: 'Ψ', Omega: 'Ω',
};
const SYMBOL = {
  pm: '±', mp: '∓', sim: '∼', simeq: '≃', approx: '≈', lesssim: '≲', gtrsim: '≳', la: '≲', ga: '≳', lapprox: '≲', gapprox: '≳',
  times: '×', cdot: '·', leq: '≤', le: '≤', geq: '≥', ge: '≥', ll: '≪', gg: '≫', neq: '≠', ne: '≠', propto: '∝', infty: '∞',
  odot: '⊙', sun: '☉', star: '⋆', ast: '∗', prime: '′', circ: '∘', degr: '°', deg: '°', ldots: '…', dots: '…', cdots: '⋯',
  rightarrow: '→', to: '→', leftarrow: '←', partial: '∂', nabla: '∇', sqrt: '√', int: '∫', sum: 'Σ', ell: 'ℓ', hbar: 'ℏ',
  kms: 'km s⁻¹', AA: 'Å', angstrom: 'Å',
};
// Commands that only style their argument: {\rm X}, \mathrm{X} and the like show X.
const STYLE = ['rm', 'mathrm', 'textrm', 'text', 'mathit', 'textit', 'it', 'bf', 'mathbf', 'textbf', 'mathcal', 'mathsf', 'sf', 'tt', 'texttt', 'emph', 'operatorname', 'mbox', 'hbox'];
const DROP = ['left', 'right', 'big', 'Big', 'bigg', 'Bigg', 'displaystyle', 'textstyle', 'scriptstyle', 'limits', 'nolimits', 'quad', 'qquad'];
const THIN = ' ';

/** True if the string holds TeX that the display would change. */
export function hasTex(s) {
  if (typeof s !== 'string' || !s) return false;
  return /\$|\\[A-Za-z,;:!% _&{}~^]|(^|[^\\])~/.test(s) && /\$|\\/.test(s);
}

const escHtml = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// Read one {…} group starting at s[i] === '{'; returns [content, index after the closing brace].
function group(s, i) {
  let depth = 0;
  for (let j = i; j < s.length; j++) {
    if (s[j] === '\\') { j++; continue; }
    if (s[j] === '{') depth++;
    else if (s[j] === '}' && --depth === 0) return [s.slice(i + 1, j), j + 1];
  }
  return [s.slice(i + 1), s.length];
}
// Read one […] optional argument starting at s[i] === '['.
function optArg(s, i) {
  const j = s.indexOf(']', i);
  return j < 0 ? [s.slice(i + 1), s.length] : [s.slice(i + 1, j), j + 1];
}

// Citation commands: \citep[pre][post]{keys} → "(pre citation, post)"; the keys are not shown.
function citations(s) {
  return s.replace(/\\(citep|citet|cite|citealt|citealp|citeauthor|citeyear|citeyearpar|ref|eqref|autoref)\*?((?:\s*\[[^\]]*\])*)\s*\{[^}]*\}/g, (m, cmd, opts) => {
    if (/ref$/.test(cmd)) return '(cross-reference)';
    const args = [...opts.matchAll(/\[([^\]]*)\]/g)].map((x) => x[1].trim());
    let pre = '', post = '';
    if (args.length === 1) post = args[0];
    if (args.length >= 2) { pre = args[0]; post = args[1]; }
    const core = [pre ? `${pre} citation` : 'citation', post].filter(Boolean).join(', ');
    return cmd === 'citealt' || cmd === 'citealp' ? core : `(${core})`;
  });
}

// Superscript and subscript characters, where Unicode has them.
const SUP = { 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹', '+': '⁺', '-': '⁻', '−': '⁻', '=': '⁼', '(': '⁽', ')': '⁾', n: 'ⁿ', i: 'ⁱ', '*': '*', '⋆': '⋆', '∗': '∗', '′': '′' };
const SUB = { 0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉', '+': '₊', '-': '₋', '−': '₋', '=': '₌', '(': '₍', ')': '₎', a: 'ₐ', e: 'ₑ', h: 'ₕ', i: 'ᵢ', j: 'ⱼ', k: 'ₖ', l: 'ₗ', m: 'ₘ', n: 'ₙ', o: 'ₒ', p: 'ₚ', r: 'ᵣ', s: 'ₛ', t: 'ₜ', u: 'ᵤ', v: 'ᵥ', x: 'ₓ' };
const uni = (txt, map) => ([...txt].every((c) => c in map) ? [...txt].map((c) => map[c]).join('') : null);

// Convert one maths segment (the text between $…$) to tokens: plain text and {sup|sub: text}.
function mathTokens(s) {
  const out = [];
  let buf = '';
  const flush = () => { if (buf) { out.push({ t: buf }); buf = ''; } };
  for (let i = 0; i < s.length;) {
    const c = s[i];
    if (c === '^' || c === '_') {
      let arg, j = i + 1;
      while (s[j] === ' ') j++;
      if (s[j] === '{') [arg, j] = group(s, j);
      else if (s[j] === '\\') { const m = s.slice(j).match(/^\\([A-Za-z]+|.)/); arg = m[0]; j += m[0].length; }
      else { arg = s[j] || ''; j += 1; }
      flush();
      out.push({ [c === '^' ? 'sup' : 'sub']: inlineText(arg, true) });
      i = j;
      continue;
    }
    if (c === '{' || c === '}') { i++; continue; }
    buf += c; i++;
  }
  flush();
  return out;
}

// Commands, spacing and escapes, for text outside or inside maths. Unknown commands (a paper's own
// macros, such as \BooI) lose their backslash, so the name stays readable.
function inlineText(s, math = false) {
  let t = s.replace(/\\\\/g, ' ');
  t = t.replace(/\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, '$1/$2');
  t = t.replace(/\{\\(?:rm|it|bf|sf|tt)\s+([^{}]*)\}/g, '{$1}');
  t = t.replace(new RegExp(`\\\\(?:${STYLE.join('|')})\\s*\\{([^{}]*)\\}`, 'g'), '{$1}');
  t = t.replace(new RegExp(`\\\\(?:${STYLE.join('|')})(?![A-Za-z])\\s*`, 'g'), '');
  t = t.replace(new RegExp(`\\\\(?:${DROP.join('|')})(?![A-Za-z])\\s*`, 'g'), '');
  t = t.replace(/\\[,;:]/g, THIN).replace(/\\!/g, '').replace(/\\ /g, ' ');
  t = t.replace(/\\([%&_#{}$])/g, '$1');
  t = t.replace(/\\([A-Za-z]+) ?/g, (m, name) => {
    const v = GREEK[name] ?? SYMBOL[name];
    if (v !== undefined) return v + (m.endsWith(' ') ? ' ' : '');
    return name + (m.endsWith(' ') ? ' ' : '');
  });
  t = t.replace(/~/g, ' ');
  if (!math) t = t.replace(/\{([^{}]*)\}/g, '$1');
  return t;
}

// Split into maths ($…$) and text segments.
function segments(s) {
  const out = [];
  const re = /\$\$?([^$]*)\$\$?/g;
  let last = 0, m;
  while ((m = re.exec(s))) {
    if (m.index > last) out.push({ text: s.slice(last, m.index) });
    out.push({ math: m[1] });
    last = m.index + m[0].length;
  }
  if (last < s.length) out.push({ text: s.slice(last) });
  return out;
}

function render(s, { html, link }) {
  if (!hasTex(s)) return html ? link(s) : s;
  const segs = segments(citations(s));
  let out = '';
  for (const g of segs) {
    if (g.text !== undefined) { const t = inlineText(g.text); out += html ? link(t) : t; continue; }
    const body = inlineText(g.math, true);
    for (const tok of mathTokens(body)) {
      if (tok.t !== undefined) out += html ? escHtml(tok.t) : tok.t;
      else {
        const k = tok.sup !== undefined ? 'sup' : 'sub', v = tok[k];
        if (html) out += `<${k}>${escHtml(v)}</${k}>`;
        else out += uni(v, k === 'sup' ? SUP : SUB) ?? (k === 'sup' ? '^' : '_') + (v.length > 1 ? `(${v})` : v);
      }
    }
  }
  return out.replace(/ {2,}/g, ' ');
}

/** Readable plain text (Unicode sub- and superscripts where they exist). */
export function tex(s) { return render(s, { html: false }); }

/** Readable HTML (<sup>, <sub>); `link` turns a text segment into escaped HTML (default: escape only). */
export function texHtml(s, link = escHtml) { return render(s, { html: true, link }); }
