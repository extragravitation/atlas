"""Write the per-cluster table and programme summary for gas-coherence-A9.md from gas.json (names only).
python3 -I gen_md.py gas.json out_dir"""
import sys, json, re
from collections import defaultdict
d = json.load(open(sys.argv[1])); OUT = sys.argv[2]
rows, OBS, STARS, GAS = d['rows'], d['OBS'], d['STARS'], d['GAS']

STATUS = {  # usable form of the gas source under §1 item 4, as read
 'X-COP': 'A', 'C9h/C9i Peng+2009': 'A', 'C15a Hicks+2006': 'A', 'C11b Okabe+2014': 'A', 'C29a Li+2024': 'A',
 'C9g/C9h CHEX-MATE A1689': 'A', 'C11a Umetsu+2009 (AMiBA)': 'A',
 'C3a CLASH-X': 'B', 'Mirakhor & Walker 2020': 'B', 'Eckert+2016 (XXL XIII)': 'B', 'C20c CHeCS': 'B',
 'Martino+2014': 'C', 'Mulroy+2019 gas': 'C',
 'CHEX-MATE': 'D', 'Akamatsu+2011': 'D', 'Nagarajan+2018 (APEX-SZ)': 'D'}
ORDER = ['X-COP', 'CHEX-MATE', 'C3a CLASH-X', 'Martino+2014', 'Mulroy+2019 gas', 'C20c CHeCS', 'Mirakhor & Walker 2020',
         'Eckert+2016 (XXL XIII)', 'Nagarajan+2018 (APEX-SZ)', 'Akamatsu+2011', 'C15a Hicks+2006', 'C9h/C9i Peng+2009',
         'C9g/C9h CHEX-MATE A1689', 'C11b Okabe+2014', 'C11a Umetsu+2009 (AMiBA)', 'C29a Li+2024']
# survey gas named by each observed-side programme (§3.1 third step)
SURVEY_GAS = {'CLASH': {'C3a CLASH-X'}, 'LoCuSS': {'Martino+2014', 'Mulroy+2019 gas'}, 'XXL': {'Eckert+2016 (XXL XIII)'},
              'APEX-SZ': {'Nagarajan+2018 (APEX-SZ)'}, 'SAO caustic team (HeCS)': {'C20c CHeCS'},
              'SAO caustic team (HeCS/CHeCS)': {'C20c CHeCS'}, 'SAO caustic team (CIRS+HeCS)': {'C20c CHeCS'},
              'A2142 (Munari)': {'Akamatsu+2011', 'X-COP'}, 'DESI Coma (Pedratti)': {'Mirakhor & Walker 2020'},
              'CHEX-MATE': {'CHEX-MATE'}}

def ccat(s):
    s = s.lower()
    if s.startswith(('not', 'n/a', '—', 'as c21a')) or 'g98' in s: return None if not s.startswith('as c21a') else 'hierarchical'
    if 'bcg' in s or 'ngc 4874' in s: return 'BCG'
    if 'hierarchical' in s or 'caustic centre' in s: return 'galaxy distribution'
    if 'peak' in s and 'x-ray' in s: return 'X-ray peak'
    if 'centroid' in s: return 'X-ray centroid'
    if 'x-ray' in s: return 'X-ray (unspecified)'
    if 'convergence' in s: return 'lensing peak'
    return None

def short(lbl): return lbl.split(' (')[0] if not lbl.startswith('C') else lbl

def gascell(r):
    out = []
    for g in ORDER:
        if g in r['gas']:
            t = f"{g} [{STATUS[g]}]"
            if g == 'CHEX-MATE' and r['chx']:
                n, tier, dr1, how = r['chx']; t = f"CHEX-MATE as {n}, Tier {tier}{', DR1' if dr1 else ''} [D] ({'name' if how == 'name' else 'position'})"
            out.append(t)
    return '; '.join(out) if out else '**none found**'

def assess(o, s, g):
    po, ps, pg = OBS[o][0], STARS[s][0], (GAS[g][0] if g in GAS else None)
    progs = [p for p in (po, ps, pg) if p]
    sc = max(progs.count(p) for p in progs)
    cats = [ccat(OBS[o][1]), ccat(STARS[s][1]), ccat(GAS[g][1]) if g in GAS else None]
    shared = None not in cats and len(set(cats)) == 1
    same_ap = g == 'Mulroy+2019 gas' and 'r500,WL' in STARS[s][2]
    stated = sum(c is not None for c in cats)
    return (sc, {'A': 3, 'B': 2, 'C': 1, 'D': 0}.get(STATUS.get(g), -1), shared, same_ap, stated)

def best_combo(r, ch):
    v = r['ch'][ch]; best = None
    for o in v['obs']:
        for s in v['stars']:
            for g in (r['gas'] or ['none']):
                k = assess(o, s, g)
                if best is None or k > best[0]: best = (k, o, s, g)
    return best

def combo(r, ch):
    b = best_combo(r, ch)
    if not b: return '—', '—', '—', '—', '—'
    (sc, _, _, _, _), o, s, g = b
    r['ch'][ch]['best'] = [None, o, s, g, sc]
    co, cs, cg = OBS[o][1], STARS[s][1], GAS[g][1] if g in GAS else '—'
    cats = [ccat(co), ccat(cs), ccat(cg) if g in GAS else None]
    if None in cats: shared = 'not determined (' + ', '.join(n for n, c in zip(('obs', 'stars', 'gas'), cats) if c is None) + ' centre not stated/read)'
    else: shared = 'yes (' + cats[0] + ')' if len(set(cats)) == 1 else 'no (' + ' / '.join(cats) + ')'
    ap_s = STARS[s][2]; ap_g = GAS[g][2] if g in GAS else '—'
    if g in ('Mulroy+2019 gas',) and 'r500,WL' in ap_s: same_ap = 'yes (r500,WL)'
    elif STATUS.get(g) == 'C': same_ap = 'no (gas at other apertures)'
    elif STATUS.get(g) in ('A', 'B'): same_ap = 'n/a (gas is a profile or fitted model; read at the star aperture)'
    else: same_ap = 'not determined (gas not available)'
    progs = f"{OBS[o][0]} / {STARS[s][0]} / {GAS[g][0] if g in GAS else '—'}"
    return f"**{sc}**", f"{o} · {s} · {g if g in GAS else 'none'}", progs, f"obs {co}; stars {cs}; gas {cg}; shared: {shared}", f"stars {ap_s}; gas {ap_g}; same: {same_ap}"

lines = ['| Cluster | z (A9, first printed) | Channel | Observed-side records (this channel) | Stars (record, geometry) | Gas candidates in §3.1 order [status] | Coherence score | Most coherent inputs (obs · stars · gas) | Programmes (obs / stars / gas) | Centres | Apertures |',
         '|---|---|---|---|---|---|---|---|---|---|---|']
for r in sorted(rows, key=lambda r: (r['pair'], r['name'])):
    for ch in ('L', 'O'):
        if ch not in r['ch']: continue
        v = r['ch'][ch]
        z = re.search(r'(?<![\d.])0\.\d+', r['z']).group(0)
        sc, inp, pg, cen, ap = combo(r, ch)
        lines.append('| ' + ' | '.join([r['name'], z, ch + (' (both)' if r['pair'] == 'both' else ''), ', '.join(v['obs']),
                    ', '.join(f"{s} ({'projected' if ch == 'L' else '3D'})" for s in v['stars']), gascell(r), sc, inp, pg, cen, ap]) + ' |')
open(OUT + '/table.md', 'w').write('\n'.join(lines) + '\n')

# programme summary: a cluster counts for programme P in channel ch if one of its observed-side records in ch is from P
prog = defaultdict(lambda: defaultdict(list))
for r in rows:
    for ch, v in r['ch'].items():
        ps = {OBS[o][0] for o in v['obs']}
        sp = {STARS[s][0] for s in v['stars']}
        for P in ps:
            own_gas = [g for g in r['gas'] if GAS[g][0] == P or g in SURVEY_GAS.get(P, set())]
            prog[(P, ch)]['all'].append(r['name'])
            if P in sp or (P == 'SAO caustic team (CIRS+HeCS)' and False): prog[(P, ch)]['stars_own'].append(r['name'])
            if own_gas: prog[(P, ch)]['gas_own'].append(r['name'])
            if own_gas and P in sp: prog[(P, ch)]['three_own'].append(r['name'])
            if own_gas and P in sp and any(STATUS[g] in 'AB' for g in own_gas): prog[(P, ch)]['three_own_usable'].append(r['name'])
            if any(STATUS[g] in 'AB' for g in r['gas']): prog[(P, ch)]['usable_gas_any'].append(r['name'])
            if r['gas']: prog[(P, ch)]['gas_any'].append(r['name'])
# star-programme and gas-programme groupings (for programmes that supply stars or gas but not the observed side)
sprog = defaultdict(lambda: defaultdict(list))
for r in rows:
    for ch, v in r['ch'].items():
        for s in v['stars']:
            P = STARS[s][0]; sprog[(P, ch)]['all'].append(r['name'])
            if any(GAS[g][0] == P for g in r['gas']): sprog[(P, ch)]['gas_same'].append(r['name'])
            if any(STATUS[g] in 'AB' for g in r['gas']): sprog[(P, ch)]['usable_gas_any'].append(r['name'])
json.dump(dict(obs={f'{k[0]}|{k[1]}': {kk: sorted(set(vv)) for kk, vv in v.items()} for k, v in prog.items()},
               stars={f'{k[0]}|{k[1]}': {kk: sorted(set(vv)) for kk, vv in v.items()} for k, v in sprog.items()}),
          open(OUT + '/programmes.json', 'w'), ensure_ascii=False, indent=1)
for k, v in sorted(prog.items()):
    print(k, {kk: len(set(vv)) for kk, vv in v.items()})
print('---- star programmes')
for k, v in sorted(sprog.items()):
    print(k, {kk: len(set(vv)) for kk, vv in v.items()})
