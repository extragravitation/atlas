// Known issues (D-020): read at build from GitHub Issues labelled `known-issue`, joined to the
// affected measurements listed in each package's known_issues.json. If GitHub cannot be reached
// the build uses the package files alone and the page says so.
import { loadAtlas } from './atlas.mjs';
import { md } from './md.mjs';

const API = 'https://api.github.com/repos/extragravitation/atlas/issues?labels=known-issue&state=all&per_page=100';
let cache = null;

const field = (body, name) => { const m = (body || '').match(new RegExp('\\*\\*' + name + ':\\*\\*\\s*([^·\\n]+)')); return m ? m[1].trim() : null; };
const section = (body, name) => { const m = (body || '').match(new RegExp('## ' + name + '\\s*\\n+([\\s\\S]*?)(\\n## |$)')); return m ? m[1].trim() : null; };
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export async function loadIssues() {
  if (cache) return cache;
  const atlas = loadAtlas();
  const local = [];
  for (const d of atlas.datasets) for (const k of d.knownIssues) local.push({ ...k, dataset: d.key, datasetName: d.name, version: d.version });
  let remote = null, error = null;
  if (process.env.AEG_OFFLINE !== '1') {
    try {
      const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 8000);
      const headers = { Accept: 'application/vnd.github+json', 'User-Agent': 'aeg-site-build' };
      const res = await fetch(API, { headers, signal: ctl.signal }); clearTimeout(t);
      if (!res.ok) throw new Error('GitHub API ' + res.status);
      remote = (await res.json()).filter((i) => !i.pull_request);
    } catch (e) { error = String(e.message || e); }
  }
  const byNum = Object.fromEntries((remote || []).map((i) => [i.number, i]));
  const nums = [...new Set([...local.map((k) => k.issue), ...(remote || []).map((i) => i.number)])].sort((a, b) => a - b);
  const items = nums.map((n) => {
    const g = byNum[n], ls = local.filter((k) => k.issue === n);
    const what = g ? section(g.body, 'What') : null;
    return {
      number: n, url: g ? g.html_url : ls[0]?.url, title: g ? g.title : ls[0]?.title,
      state: g ? g.state : 'open', status: g ? field(g.body, 'Status') || g.state : 'open (from the package file)',
      found: g ? field(g.body, 'Found') || g.created_at.slice(0, 10) : null, closed: g?.closed_at ? g.closed_at.slice(0, 10) : null,
      whatHtml: what ? md(esc(what.split(/\n\n/)[0])) : '',
      packages: ls.map((k) => ({ dataset: k.dataset, name: k.datasetName, version: k.version, flag: k.flag, measurements: k.measurements || [], clusters: k.clusters || [] })),
    };
  });
  cache = { items, source: remote ? 'github' : 'packages', error, at: new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC' };
  return cache;
}
