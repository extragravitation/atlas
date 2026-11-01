"""Classes for coverage v3. python3 -I classify.py out.json -> prints JSON summary, writes table rows file."""
import sys, json, re
d = json.load(open(sys.argv[1]))
rows, hits, strict, chan = d['rows'], d['hits'], d['strict'], d['chan']

E_LUM = {'L1', 'L5a', 'L5c', 'L9', 'S2b', 'S3a', 'S3b', 'S16b'}
QL1 = {'L10', 'L23b'}            # S3a is already E
QL2R = {'L2', 'L8', 'LV3', 'S6'}
NOCOUNT = {'L4', 'S4b', 'S4d', 'S10a'}
PROJ = {'L1': '3D', 'S2b': '3D', 'L4': '3D'}
VAR = {'R': E_LUM | QL1 | QL2R, 'S': E_LUM | QL1}
# S9 stellar-mass records giving full coverage by an E record (v2), with geometry from the S9 readings
S9GEOM = {'S4b': 'not stated', 'S8d': 'not stated', 'S10b': '3D', 'S12b': '3D'}

def lumcount(i, var):
    return sorted({h['rid'] for h in hits.get(str(i), []) if h['rid'] in VAR[var] and not h['nolum']})

def s9full(i, v2rule):
    st = rows[i]['st']
    out = []
    for m in re.finditer(r'(S\d+[a-z]?) \(E; (full[^;]*);', st):
        if v2rule == 'strict' and 'reader A only' in m.group(2):
            continue
        out.append(m.group(1))
    return out

def cls(i, var, v2rule):
    base = rows[i]['cls'] if v2rule == 'main' else strict[str(i)]
    return 'a' if (base == 'a' or lumcount(i, var)) else base

def channels(i):
    a9 = rows[i]['a9'].split('· stacked')[0]
    ch = set()
    for rec in re.findall(r'(C\d+[a-z]?(?:/C\d+[a-z]?)?) \(', a9):
        c = chan.get(rec, '?')
        if c in ('L', 'O'): ch.add(c)
        elif c.startswith('K-band'): ch.add('O')
    return ch

res = {}
for var in 'RS':
    for rule in ('main', 'strict'):
        cnt = {k: 0 for k in 'abcd'}
        for i in range(len(rows)):
            cnt[cls(i, var, rule)] += 1
        res[f'{var}-{rule}'] = cnt
moved = {var: [rows[i]['name'] for i in range(len(rows)) if rows[i]['cls'] != 'a' and cls(i, var, 'main') == 'a'] for var in 'RS'}
diff = {var: [rows[i]['name'] for i in range(len(rows)) if cls(i, var, 'main') != cls(i, var, 'strict')] for var in 'RS'}

geo = {}
for var in 'RS':
    tally = {}
    det = []
    for i in range(len(rows)):
        if cls(i, var, 'main') != 'a': continue
        g = set()
        for r in lumcount(i, var): g.add(PROJ.get(r, 'projected'))
        for r in s9full(i, 'main'): g.add(S9GEOM[r])
        ch = channels(i)
        pl = 'projected' in g and 'L' in ch
        p3 = '3D' in g and 'O' in ch
        key = 'both' if (pl and p3) else 'projected–L only' if pl else '3D–O only' if p3 else 'not pairable / not determined'
        tally[key] = tally.get(key, 0) + 1
        star = '+'.join(sorted(g))
        tally['stars:' + star] = tally.get('stars:' + star, 0) + 1
        tally['chan:' + ''.join(sorted(ch)) if ch else 'chan:none'] = tally.get('chan:' + ''.join(sorted(ch)) if ch else 'chan:none', 0) + 1
        det.append((rows[i]['name'], star, ''.join(sorted(ch)) or 'none', key))
    geo[var] = dict(tally=tally, det=det)

json.dump(dict(res=res, moved=moved, diff=diff, geo=geo), sys.stdout, ensure_ascii=False, indent=1)
