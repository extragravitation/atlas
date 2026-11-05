// Markdown from the repository (package documents, decision log, plans), rendered at build.
// Relative links are pointed at the file in the repository on GitHub, so they never break.
import { marked } from 'marked';
import { tex } from './tex.mjs';

export const REPO = 'https://github.com/extragravitation/atlas';

export function md(text, repoDir = '') {
  if (!text) return '';
  // Quoted source text with TeX in it is shown readably (D-109 rule 4); the file itself is unchanged.
  // Only straight-quoted strings outside code spans are touched.
  const shown = text.split(/(`[^`]*`)/).map((part, i) => (i % 2 ? part : part.replace(/"([^"\n]*\\[A-Za-z][^"\n]*)"/g, (m, q) => `"${tex(q)}"`))).join('');
  const html = marked.parse(shown, { async: false, gfm: true });
  return html.replace(/href="([^"#][^"]*)"/g, (m, href) => {
    if (/^(https?:|mailto:|\/)/.test(href)) return m;
    const clean = href.replace(/^\.\//, '');
    return `href="${REPO}/blob/main/${repoDir ? repoDir.replace(/\/$/, '') + '/' : ''}${clean}"`;
  }).replace(/<table>/g, '<div tabindex="0" class="tablebox prose-table"><table>').replace(/<\/table>/g, '</table></div>');
}

// First "**Result: …**" line of a frozen-test result file.
export function resultLine(text) {
  if (!text) return null;
  const m = text.match(/\*\*Result:\s*([^*]+)\*\*/) || text.match(/^\*\*((?:PASS|FAIL)[^*]*)\*\*/m);
  if (!m) return null;
  const v = m[1].trim();
  return { text: v, pass: /^PASS(ED)?\b|^validated/i.test(v) };
}
