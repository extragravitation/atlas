"""List the A9 clusters pairable with an observed side (coverage v3, recommended QL2, v2 main).
Logic copied from coverage-v3-tools/gen.py. Names, records, channels and geometry only.
python3 -I pairable.py cov3.json out.json"""
import sys, json, re
d = json.load(open(sys.argv[1]))
rows, hits, chan = d['rows'], d['hits'], d['chan']
E_LUM = {'L1', 'L5a', 'L5c', 'L9', 'S2b', 'S3a', 'S3b', 'S16b'}
COUNT = E_LUM | {'L10', 'L23b'} | {'L2', 'L8', 'LV3', 'S6'}
PROJ = {'L1': '3D', 'S2b': '3D', 'L4': '3D'}
S9GEOM = {'S4b': 'not stated', 'S8d': 'not stated', 'S10b': '3D', 'S12b': '3D'}
def lum(i): return sorted({h['rid'] for h in hits.get(str(i), []) if h['rid'] in COUNT and not h['nolum']})
def s9(i): return [m.group(1) for m in re.finditer(r'(S\d+[a-z]?) \(E; (full[^;]*);', rows[i]['st'])]
def recs(i):
    out = []
    for rec in re.findall(r'(C\d+[a-z]?(?:/C\d+[a-z]?)?) \(', rows[i]['a9'].split('· stacked')[0]):
        c = chan.get(rec, '?'); c = 'O' if c.startswith('K-band') else c
        out.append((rec, c))
    return out
res = []
for i, r in enumerate(rows):
    if r['cls'] != 'a' and not lum(i): continue
    stars = [(x, PROJ.get(x, 'projected')) for x in lum(i)] + [(x, S9GEOM[x]) for x in s9(i)]
    g = {s[1] for s in stars}
    ch = {c for _, c in recs(i) if c in ('L', 'O')}
    pl, p3 = 'projected' in g and 'L' in ch, '3D' in g and 'O' in ch
    if not (pl or p3): continue
    names = {h['rid']: h['name'] for h in hits.get(str(i), [])}
    res.append(dict(name=r['name'], forms=r['forms'], z=r['z'], recs=recs(i), stars=stars, star_names=names,
                    pair=('both' if pl and p3 else 'L' if pl else 'O')))
json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print(len(res), {k: sum(x['pair'] == k for x in res) for k in ('L', 'O', 'both')})
