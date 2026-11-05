// Minimal reader for the ECSV 1.0 files written by the Atlas pipeline (astropy, comma-delimited).
// Reads column names and datatypes from the YAML header and the rows below it. Numbers are parsed
// with Number(), which reproduces the stored float64 values exactly; empty cells become null.

export function parseECSV(text) {
  const lines = text.split(/\r?\n/);
  const header = [];
  let i = 0;
  for (; i < lines.length && lines[i].startsWith('#'); i++) header.push(lines[i]);
  if (!header[0] || !header[0].startsWith('# %ECSV 1.0')) throw new Error('not an ECSV 1.0 file');
  const columns = [];
  let cur = null;
  const meta = {};
  let inMeta = false;
  const hl = header.slice(1);
  for (let h = 0; h < hl.length; h++) {
    let l = hl[h].replace(/^# ?/, '');
    // A double-quoted YAML scalar may continue over several lines: join them (an escaped line end joins with
    // nothing, a plain one with a space) before decoding.
    const open = l.match(/^ {2}(?:description|unit): "/);
    if (open) {
      const closed = (s) => /[^\\]"\s*$|^[^"]*"[^"]*"\s*$/.test(s.slice(s.indexOf('"') + 1)) || /(^|[^\\])"\s*$/.test(s.slice(s.indexOf('"') + 1));
      while (!closed(l) && h + 1 < hl.length) {
        const next = hl[++h].replace(/^# ?/, '').trim();
        l = l.endsWith('\\') ? l.slice(0, -1) + next : l + ' ' + next;
      }
    }
    let m;
    if ((m = l.match(/^- name: (.+)$/))) { cur = { name: unq(m[1]), datatype: 'string', unit: null, description: '' }; columns.push(cur); inMeta = false; continue; }
    if (cur && (m = l.match(/^ {2}datatype: (.+)$/))) { cur.datatype = m[1].trim(); continue; }
    if (cur && (m = l.match(/^ {2}unit: (.+)$/))) { cur.unit = unq(m[1]); continue; }
    if (cur && (m = l.match(/^ {2}description: (.+)$/))) { cur.description = unq(m[1]); continue; }
    if ((m = l.match(/^meta: !!omap$/)) || (m = l.match(/^meta:$/))) { inMeta = true; cur = null; continue; }
    if (inMeta && (m = l.match(/^- \{(\w+): (.*)\}$/))) { meta[m[1]] = unq(m[2]); continue; }
  }
  const head = splitCSV(lines[i]);
  if (head.length !== columns.length || head.some((h, k) => h !== columns[k].name)) throw new Error('ECSV header and CSV header disagree');
  const numeric = columns.map((c) => /^(float|int|uint)/.test(c.datatype));
  const rows = [];
  for (i = i + 1; i < lines.length; i++) {
    if (lines[i] === '') continue;
    const cells = splitCSV(lines[i]);
    if (cells.length !== columns.length) throw new Error(`row ${rows.length + 1}: ${cells.length} cells, expected ${columns.length}`);
    const row = {};
    columns.forEach((c, k) => {
      const v = cells[k];
      row[c.name] = numeric[k] ? (v === '' ? null : Number(v)) : v;
    });
    rows.push(row);
  }
  return { columns, meta, rows };
}

function unq(s) {
  s = s.trim();
  if (s.startsWith("'") && s.endsWith("'")) return s.slice(1, -1).replace(/''/g, "'");
  // YAML double-quoted scalar: decode its escapes (\xHH, \uHHHH, \UHHHHHHHH, \", \\, \n, \t).
  if (s.startsWith('"') && s.endsWith('"')) return s.slice(1, -1).replace(/\\(x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|.)/g, (_, e) => {
    if (e[0] === 'x' || e[0] === 'u' || e[0] === 'U') return String.fromCodePoint(parseInt(e.slice(1), 16));
    return ({ n: '\n', t: '\t', '"': '"', '\\': '\\', '/': '/', ' ': ' ', '0': '\0' })[e] ?? e;
  });
  return s;
}

export function splitCSV(line) {
  const out = [];
  let cur = '', q = false;
  for (let k = 0; k < line.length; k++) {
    const ch = line[k];
    if (q) {
      if (ch === '"') { if (line[k + 1] === '"') { cur += '"'; k++; } else q = false; }
      else cur += ch;
    } else if (ch === '"') q = true;
    else if (ch === ',') { out.push(cur); cur = ''; }
    else cur += ch;
  }
  out.push(cur);
  return out;
}

export function toCSV(columns, rows) {
  const esc = (v) => { if (v === null || v === undefined) return ''; const s = String(v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  return [columns.map((c) => c.name).join(','), ...rows.map((r) => columns.map((c) => esc(r[c.name])).join(','))].join('\n') + '\n';
}
