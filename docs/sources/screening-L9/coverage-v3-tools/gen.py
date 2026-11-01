"""Write the per-cluster table and summary pieces for coverage v3 (names and redshifts only)."""
import sys, json, re
d = json.load(open(sys.argv[1]))
rows, hits, strict, chan = d['rows'], d['hits'], d['strict'], d['chan']
E_LUM = {'L1', 'L5a', 'L5c', 'L9', 'S2b', 'S3a', 'S3b', 'S16b'}
QL1 = {'L10', 'L23b'}; QL2R = {'L2', 'L8', 'LV3', 'S6'}
VAR = {'R': E_LUM | QL1 | QL2R, 'S': E_LUM | QL1}
PROJ = {'L1': '3D', 'S2b': '3D', 'L4': '3D', 'S4b': 'not stated', 'S4d': 'not stated', 'S10a': 'not stated'}
S9GEOM = {'S4b': 'not stated', 'S8d': 'not stated', 'S10b': '3D', 'S12b': '3D'}
LABEL = {**{r: 'E' for r in E_LUM}, 'L10': 'P; E by QL1', 'L23b': 'P; E by QL1',
         **{r: 'P; E recommended, X strict' for r in QL2R},
         **{r: 'P; X under both, does not count' for r in ('L4', 'S4b', 'S4d', 'S10a')}}

def lumcount(i, var):
    return sorted({h['rid'] for h in hits.get(str(i), []) if h['rid'] in VAR[var] and not h['nolum']})
def s9full(i, rule):
    return [m.group(1) for m in re.finditer(r'(S\d+[a-z]?) \(E; (full[^;]*);', rows[i]['st'])
            if not (rule == 'strict' and 'reader A only' in m.group(2))]
def base(i, rule): return rows[i]['cls'] if rule == 'main' else strict[str(i)]
def cls(i, var, rule): return 'a' if (base(i, rule) == 'a' or lumcount(i, var)) else base(i, rule)
def channels(i):
    ch = set()
    for rec in re.findall(r'(C\d+[a-z]?(?:/C\d+[a-z]?)?) \(', rows[i]['a9'].split('· stacked')[0]):
        c = chan.get(rec, '?')
        if c in ('L', 'O'): ch.add(c)
        elif c.startswith('K-band'): ch.add('O')
    return ch
def geom(i, var):
    g = {PROJ.get(r, 'projected') for r in lumcount(i, var)} | {S9GEOM[r] for r in s9full(i, 'main')}
    return g
def pairing(i, var):
    g, ch = geom(i, var), channels(i)
    pl, p3 = ('projected' in g and 'L' in ch), ('3D' in g and 'O' in ch)
    if pl and p3: return 'both'
    if pl: return 'projected with L'
    if p3: return '3D with O'
    if not ch: return 'not determined (no L or O record)'
    if g <= {'not stated'}: return 'not determined (geometry not stated)'
    return 'geometry does not match observed side'
def starsgeo(g):
    k = g - {'not stated'}
    if k == {'projected'}: return 'projected only'
    if k == {'3D'}: return '3D only'
    if k == {'projected', '3D'}: return 'projected and 3D'
    return 'not stated only'

extra_flags = {}
for i_s, hs in hits.items():
    for h in hs:
        f = []
        if h['how'].startswith('U5'): f.append(f"U5 ({h['rid']} {h['name']}: {h['how'][len('U5 computed: '):]})")
        if 'component' in h['how']: f.append(f"{h['rid']} prints a component row \"{h['name']}\", counted with this cluster (as U6)")
        if 'alternative' in h['how']: pass
        if h['nolum']: f.append(f"{h['rid']} names it without a luminosity (no K data, per both readings): does not count")
        extra_flags.setdefault(int(i_s), []).extend(f)
i_ms1006 = next(i for i, r in enumerate(rows) if r['name'] == 'MS 1006.0+1202')
extra_flags.setdefault(i_ms1006, []).append('L10 reading prints z 0.221 for "MS1006.0+1202" (A9 source C15a 0.2605; S16b 0.2605): z discrepancy in the L10 readings, unverified; exact designation match accepted')

def lumcell(i):
    out = []
    for h in sorted(hits.get(str(i), []), key=lambda h: h['rid']):
        z = f"z {h['z']}" if h['z'] else 'z not printed'
        out.append(f"{h['rid']} ({LABEL[h['rid']]}; {PROJ.get(h['rid'], 'projected')}; as \"{h['name']}\", {z})")
    return '; '.join(out) if out else '—'

order = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
idx = sorted(range(len(rows)), key=lambda i: (order[cls(i, 'R', 'main')], order[cls(i, 'S', 'main')], order[rows[i]['cls']], i))
lines = ['| Class (rec. QL2) | Class (strict QL2) | v2 class (main / strict) | Cluster | z (A9 sources, from v2) | A9 records (code) | Observed side | Stellar-mass records (from v2) | Luminosity records naming it (code; geometry; as printed) | Flags |',
         '|---|---|---|---|---|---|---|---|---|---|']
for i in idx:
    r = rows[i]
    fl = [] if r['flags'] == '—' else [r['flags']]
    fl += extra_flags.get(i, [])
    ch = channels(i)
    lines.append('| ' + ' | '.join([cls(i, 'R', 'main'), cls(i, 'S', 'main'), f"{r['cls']} / {strict[str(i)]}", r['name'], r['z'], r['a9'],
                                    ', '.join(sorted(ch)) if ch else 'not determined (gas-side record only)', r['st'], lumcell(i), '; '.join(fl) if fl else '—']) + ' |')
open(sys.argv[2], 'w').write('\n'.join(lines) + '\n')

# summaries
S = {}
for var in 'RS':
    for rule in ('main', 'strict'):
        S[f'{var}-{rule}'] = {k: [rows[i]['name'] for i in range(len(rows)) if cls(i, var, rule) == k] for k in 'abcd'}
geo = {}
for var in 'RS':
    t1, t2 = {}, {}
    for i in range(len(rows)):
        if cls(i, var, 'main') != 'a': continue
        a, b = starsgeo(geom(i, var)), pairing(i, var)
        t1[a] = t1.get(a, 0) + 1; t2[b] = t2.get(b, 0) + 1
    geo[var] = (t1, t2)
# per record
per = {}
for i_s, hs in hits.items():
    for h in hs:
        per.setdefault(h['rid'], set()).add(int(i_s))
perrec = {rid: dict(n=len(v), newa_R=len([i for i in v if rows[i]['cls'] != 'a' and cls(i, 'R', 'main') == 'a']),
                    newa_S=len([i for i in v if rows[i]['cls'] != 'a' and cls(i, 'S', 'main') == 'a'])) for rid, v in per.items()}
moved = {var: {k: [rows[i]['name'] for i in range(len(rows)) if rows[i]['cls'] == k and cls(i, var, 'main') == 'a'] for k in 'bcd'} for var in 'RS'}
json.dump(dict(S={k: {c: len(v) for c, v in x.items()} for k, x in S.items()}, lists={k: x for k, x in S.items() if k.endswith('main')},
               geo=geo, perrec=perrec, moved=moved), open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
