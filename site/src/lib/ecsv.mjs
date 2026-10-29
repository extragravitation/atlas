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
  for (const raw of header.slice(1)) {
    const l = raw.replace(/^# ?/, '');
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
  if ((s.startsWith("'") && s.endsWith("'")) || (s.startsWith('"') && s.endsWith('"'))) return s.slice(1, -1).replace(/''/g, "'");
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
