// Links for the references in registry and package text: decision numbers (D-039), repository
// paths (docs/sources/…), and file names relative to a package (gas_term.json, REPRODUCTION.md).
// Only references that resolve to a file or a decision heading are linked; the rest stay as text.
import fs from 'node:fs';
import path from 'node:path';
import { ROOT } from './atlas.mjs';
import { REPO } from './md.mjs';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
// GitHub's heading anchors: lower case, punctuation removed, spaces to hyphens.
const ghSlug = (h) => h.trim().toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu, '').replace(/\s/g, '-');
let decisions = null;
function decisionAnchors() {
  if (decisions) return decisions;
  decisions = {};
  const text = fs.readFileSync(path.join(ROOT, 'docs/decisions.md'), 'utf8');
  for (const m of text.matchAll(/^## (D-\d{3})\b(.*)$/gm)) if (!decisions[m[1]]) decisions[m[1]] = ghSlug(m[1] + m[2]);
  return decisions;
}
// Named method documents cited by their short name.
const NAMED = { A6S_PRECEDENCE: 'docs/methods/A6S_PRECEDENCE.md' };
const exists = (rel) => { try { return fs.statSync(path.join(ROOT, rel)).isFile(); } catch (e) { return false; } };

// Other versions of the same package, newest first: data/packages/<name>/<version>.
function siblings(pkgDir) {
  if (!pkgDir) return [];
  const parent = path.dirname(pkgDir);
  try {
    return fs.readdirSync(path.join(ROOT, parent)).filter((v) => `${parent}/${v}` !== pkgDir).sort((a, b) => (Number(b.replace(/^v/, '')) || 0) - (Number(a.replace(/^v/, '')) || 0)).map((v) => `${parent}/${v}`);
  } catch (e) { return []; }
}
export function decisionUrl(id) { const a = decisionAnchors()[id]; return a ? `${REPO}/blob/main/docs/decisions.md#${a}` : null; }
export function fileUrl(rel) { return `${REPO}/blob/main/${rel}`; }

// HTML for `text`, with each resolvable reference made a link. `pkgDir` is the package's
// repository directory (data/packages/<name>/<version>), for file names given relative to it.
export function linkRefs(text, pkgDir = '') {
  if (!text) return '';
  const re = /\b(D-\d{3})\b|((?:docs|data|pipeline)\/[\w./-]*\w)|\b(A6S_PRECEDENCE)\b|((?:[\w-]+\/)*[\w-]+\.(?:md|json|csv|py))\b/g;
  let out = '', last = 0;
  for (const m of String(text).matchAll(re)) {
    out += esc(text.slice(last, m.index));
    last = m.index + m[0].length;
    let url = null;
    if (m[1]) url = decisionUrl(m[1]);
    else if (m[2]) url = exists(m[2]) ? fileUrl(m[2]) : null;
    else if (m[3]) url = fileUrl(NAMED[m[3]]);
    else if (m[4]) {
      // The package itself first, then its other versions (a v2 entry may cite a v1 file), then docs.
      const cands = [pkgDir && `${pkgDir}/${m[4]}`, ...siblings(pkgDir).map((v) => `${v}/${m[4]}`), `docs/sources/${m[4]}`, `docs/methods/${m[4]}`, `docs/plans/${m[4]}`].filter(Boolean);
      const hit = cands.find(exists);
      url = hit ? fileUrl(hit) : null;
    }
    out += url ? `<a href="${esc(url)}">${esc(m[0])}</a>` : esc(m[0]);
  }
  return out + esc(String(text).slice(last));
}
