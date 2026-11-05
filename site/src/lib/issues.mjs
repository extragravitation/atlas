// Known issues (D-020): read at build from GitHub Issues labelled `known-issue`, joined to the
// affected measurements listed in each package's known_issues.json. If GitHub cannot be reached
// the build uses the package files alone and the page says so.
import { loadAtlas } from './atlas.mjs';
import { md } from './md.mjs';
import { marked } from 'marked';
import { tex } from './tex.mjs';

const API = 'https://api.github.com/repos/extragravitation/atlas/issues?labels=known-issue&state=all&per_page=100';
let cache = null;

// A "**Name:** value" field: the value runs to the next "·", the next bold field label or the end of the line.
const field = (body, name) => { const m = (body || '').match(new RegExp('\\*\\*' + name + ':\\*\\*\\s*(.+?)(?=\\s*·|\\s*\\*\\*[^*\\n]+:\\*\\*|\\n|$)')); return m ? m[1].trim() : null; };
const section = (body, name) => { const m = (body || '').match(new RegExp('## ' + name + '\\s*\\n+([\\s\\S]*?)(\\n## |$)')); return m ? m[1].trim() : null; };
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// One line of issue markdown (bold, code, links) as inline HTML, with any raw HTML escaped.
const inline = (s) => (s ? marked.parseInline(esc(s), { async: false, gfm: true }) : '');
// The issue's description. Issues with a "## What" section give it whole (tables and lists included).
// Otherwise the body is used without its leading metadata line(s) ("**Dataset:** …"), up to the
// status, action or plan, the next section, or the footer.
function whatOf(body) {
  if (!body) return null;
  const w = section(body, 'What');
  if (w) return w;
  let t = body.replace(/\n---\s*\n[\s\S]*$/, '').trim();
  const paras = t.split(/\n\s*\n/);
  while (paras.length > 1 && /^\*\*(Datasets?|Dataset versions?)[:.]\*\*/.test(paras[0].trim())) paras.shift();
  t = paras.join('\n\n');
  t = t.split(/\n(?=\*\*(?:Status|Action|Plan|Ruling|Fix)\b[^*]*\*\*|## )/)[0];
  t = t.replace(/^\*\*What[:.]\*\*\s*/, '');
  return t.trim() || null;
}

// Quoted source text with TeX (a citation command, or $…$ holding a TeX command) is shown readably;
// the text as written stays available under "show as read" (D-109 rule 4). Code blocks are left alone.
const texy = (s) => !!s && !/```/.test(s) && /\\cite[a-z]*[\[{]|\$[^$\n`]*\\[A-Za-z][^$\n`]*\$/.test(s);

export async function loadIssues() {
  if (cache) return cache;
  const atlas = loadAtlas();
  const local = [];
  for (const d of atlas.all) for (const k of d.knownIssues) local.push({ ...k, dataset: d.key, datasetName: d.name, version: d.version });
  let remote = null, error = null;
  if (process.env.AEG_OFFLINE !== '1') {
    try {
      const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 8000);
      const headers = { Accept: 'application/vnd.github+json', 'User-Agent': 'aeg-site-build' };
      const res = await fetch(API, { headers, signal: ctl.signal }); clearTimeout(t);
      if (!res.ok) throw new Error('GitHub API ' + res.status);
      remote = (await res.json()).filter((i) => !i.pull_request);
      // Issues listed in a package file but not labelled known-issue are read one by one.
      const have = new Set(remote.map((i) => i.number));
      for (const n of [...new Set(local.map((k) => k.issue))].filter((n) => !have.has(n))) {
        const r1 = await fetch(API.replace(/issues\?.*$/, 'issues/' + n), { headers });
        if (r1.ok) remote.push(await r1.json());
      }
    } catch (e) { error = String(e.message || e); }
  }
  const byNum = Object.fromEntries((remote || []).map((i) => [i.number, i]));
  const nums = [...new Set([...local.map((k) => k.issue), ...(remote || []).map((i) => i.number)])].sort((a, b) => a - b);
  const items = nums.map((n) => {
    const g = byNum[n], ls = local.filter((k) => k.issue === n);
    const what = g ? whatOf(g.body) : null;
    const statusRaw = g ? field(g.body, 'Status') || g.state : 'open (from the package file)';
    return {
      number: n, url: g ? g.html_url : ls[0]?.url, title: g ? g.title : ls[0]?.title,
      state: g ? g.state : 'open', status: statusRaw, statusHtml: inline(statusRaw),
      found: g ? field(g.body, 'Found') || g.created_at.slice(0, 10) : null, foundHtml: g ? inline(field(g.body, 'Found') || g.created_at.slice(0, 10)) : '', closed: g?.closed_at ? g.closed_at.slice(0, 10) : null,
      whatHtml: what ? md(esc(texy(what) ? tex(what) : what)) : '',
      whatRaw: what && texy(what) ? what : null,
      // Dataset versions the issue names in its body, e.g. `aeg-d-dwarfs/v1` (issues not listed in a package file).
      mentions: g ? [...new Set(((g.title || '') + '\n' + (g.body || '')).match(/aeg-d-[a-z0-9-]+\/v\d+/g) || [])] : [],
      packages: ls.map((k) => ({ dataset: k.dataset, name: k.datasetName, version: k.version, flag: k.flag, measurements: k.measurements || [], clusters: k.clusters || [] })),
    };
  });
  cache = { items, source: remote ? 'github' : 'packages', error, at: new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC' };
  return cache;
}
