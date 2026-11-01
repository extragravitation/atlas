"""Coverage v3: match luminosity-record cluster lists to the v2 A9 cluster list.
Names, redshifts and positions only. Run with python3 -I cov3.py <v2.md> <toolsdir> <out.json>
"""
import sys, re, json, math
from astropy.coordinates import SkyCoord, FK4, FK5, Galactic
import astropy.units as u

V2, TD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

# ---------------- v2 table ----------------
rows = []
chan = {}
for line in open(V2, encoding='utf-8'):
    if not line.startswith('| '):
        continue
    c = [x.strip() for x in line.strip().strip('|').split('|')]
    if len(c) == 7 and c[0] in 'abcd' and len(c[0]) == 1:
        rows.append(dict(cls=c[0], name=c[1], forms=[] if c[2] == '—' else [f.strip() for f in c[2].split(',')],
                         z=c[3], a9=c[4], st=c[5], flags=c[6]))
    if len(c) == 10 and re.match(r'^C\d', c[0]):
        chan[c[0]] = c[2]
assert len(rows) == 319, len(rows)

def strict_cls(r):
    m = re.search(r'class ([cd]) if BCG inclusion must be stated by both readers', r['flags'])
    return m.group(1) if m else r['cls']

def norm(s):
    s = s.lower().replace('−', '-').replace('–', '-').replace(' ', '')
    s = re.sub(r'^\(?coma\)?.*', 'coma', s) if s.startswith('coma') else s
    s = s.replace('abell', 'a').replace('aco', 'a')
    s = re.sub(r'^zwcl', 'zw', s)
    s = re.sub(r'^rx-j', 'rxj', s)
    s = re.sub(r'^ms-', 'ms', s)
    s = re.sub(r'^act-cl-?j', 'actclj', s)
    s = re.sub(r'^a-?s0*(\d+)', r'as\1', s)
    s = re.sub(r'^s0*(\d+)$', r'as\1', s)          # L2 'S84' = Abell S 84 (v2 rule A S n = AS n)
    s = re.sub(r'^a0*(\d+)', r'a\1', s)
    s = re.sub(r'^mkw0*(\d)', r'mkw\1', s)
    s = re.sub(r'^xlssc0*(\d+)', lambda m: 'xlssc%03d' % int(m.group(1)), s)
    return s

index = {}
for i, r in enumerate(rows):
    keys = {norm(r['name'])} | {norm(f) for f in r['forms']}
    if r['name'].startswith('Coma'):
        keys |= {'a1656', 'coma'}
    for k in keys:
        assert index.get(k, i) == i, (k, r['name'])
        index[k] = i

def v2z(r):
    return [float(x) for x in re.findall(r'(?<![\d.])0\.\d+', r['z'].split('readings')[0])]

# ---------------- designations -> coordinates ----------------
def hms(h, m, s=0.0): return (h + m / 60 + s / 3600) * 15
def dms(sg, d, m, s=0.0): return (1 if sg == '+' else -1) * (d + m / 60 + s / 3600)

def parse(name):
    """Return (SkyCoord J2000, tolerance arcmin) or None. Tolerance = designation cell diagonal."""
    n = name.replace('−', '-').replace('–', '-').replace(' ', '')
    def cell(ra_unit_min, dec_unit_arcmin, dec):
        return math.hypot(ra_unit_min * 15 * math.cos(math.radians(dec)), dec_unit_arcmin)
    m = re.match(r'^(?:1eRASS|XMMXCS)J(\d\d)(\d\d)(\d\d(?:\.\d+)?)([+-])(\d\d)(\d\d)(\d\d(?:\.\d+)?)$', n)
    if m:
        ra = hms(int(m[1]), int(m[2]), float(m[3])); de = dms(m[4], int(m[5]), int(m[6]), float(m[7]))
        return SkyCoord(ra * u.deg, de * u.deg, frame=FK5(equinox='J2000')), 0.2
    m = re.match(r'^(?:RXCJ|RXJ|RX-J|ACT-CL-?J|SPT-CLJ|SDSSJ)(\d\d)(\d\d)(?:\.(\d))?([+-p])(\d\d)(\d\d)$', n)
    if m:
        ra = hms(int(m[1]), int(m[2]) + (int(m[3]) / 10 if m[3] else 0)); sg = '+' if m[4] in '+p' else '-'
        de = dms(sg, int(m[5]), int(m[6]))
        return SkyCoord(ra * u.deg, de * u.deg, frame=FK5(equinox='J2000')), cell(0.1 if m[3] else 1.0, 1.0, de)
    m = re.match(r'^(?:MS|ZwCl|Zw)(\d\d)(\d\d)(?:\.(\d))?([+-p])(\d\d)(\d\d)$', n)
    if m:
        ra = hms(int(m[1]), int(m[2]) + (int(m[3]) / 10 if m[3] else 0)); sg = '+' if m[4] in '+p' else '-'
        de = dms(sg, int(m[5]), int(m[6]))
        c = SkyCoord(ra * u.deg, de * u.deg, frame=FK4(equinox='B1950')).transform_to(FK5(equinox='J2000'))
        return c, cell(0.1 if m[3] else 1.0, 1.0, de)
    m = re.match(r'^PSZ2G(\d+\.\d\d)([+-]\d+\.\d\d)[ab]?$', n)
    if m:
        c = SkyCoord(float(m[1]) * u.deg, float(m[2]) * u.deg, frame=Galactic).transform_to(FK5(equinox='J2000'))
        return c, math.hypot(0.6, 0.6)
    return None

v2coords = []   # (row index, form, coord, tol)
for i, r in enumerate(rows):
    for f in [r['name']] + r['forms']:
        p = parse(f)
        if p: v2coords.append((i, f, p[0], p[1]))

# ---------------- luminosity records ----------------
def readcsv(fn):
    return [l.rstrip('\n').split(',') for l in open(f'{TD}/{fn}') if l.strip()]

L = {}
def add(rid, code, proj, entries, note=''):
    L[rid] = dict(code=code, proj=proj, entries=entries, note=note)

add('L1', 'E', '3D', [dict(name=n, z=z) for n, z in readcsv('L1.csv')])
l2pos = {r[0]: r[1].split(';')[0] for r in readcsv('L2pos.csv')}
add('L2', 'P/QL2', 'projected', [dict(name=n.strip(), z=None, b1950=l2pos.get(n.strip())) for n in open(f'{TD}/L2.txt') if n.strip()])
add('L4', 'P (does not count)', '3D', [dict(name=n, z=z) for n, z in
    [('A262', '0.0161'), ('A426', '0.0183'), ('A478', '0.09'), ('A1795', '0.0616'), ('A2052', '0.0348'), ('A2063', '0.0354'), ('A2199', '0.0302'), ('MKW4s', '0.0283')]])
add('L5a', 'E', 'projected', [dict(name=r[0], alt=r[1], ra=float(r[2]), dec=float(r[3]), z=r[4]) for r in readcsv('L5a.csv')])
add('L5c', 'E', 'projected', [dict(name=n, z=z) for n, z in readcsv('L5c.csv')])
add('L8', 'P/QL2', 'projected', [dict(name=n, z=z) for n, z in
    [('ABELL0068', '0.2546'), ('ABELL0115a', '0.1971'), ('ABELL0209', '0.2060'), ('RXJ0142.0+2131', '0.2803'), ('ABELL0267', '0.2300'), ('ABELL0291', '0.1960'),
     ('ABELL0383', '0.1883'), ('ABELL0586', '0.1710'), ('ABELL0611', '0.2880'), ('ABELL0697', '0.2820'), ('ABELL1835', '0.2528'), ('ZwCl1454.8+2233', '0.2578'),
     ('ABELL2219', '0.2281'), ('RXJ1720.1+2638', '0.1640'), ('RXJ2129.6+0005', '0.2350'), ('ABELL2390', '0.2329'), ('ABELL2485', '0.2472')]])
add('L9', 'E', 'projected', [dict(name='XLSSC ' + n, z=z) for n, z in
    [('027', '0.295'), ('054', '0.054'), ('055', '0.232'), ('056', '0.348'), ('060', '0.139'), ('061', '0.259'), ('083', '0.430'), ('084', '0.430'), ('087', '0.141'),
     ('088', '0.295'), ('091', '0.186'), ('098', '0.297'), ('103', '0.233'), ('104', '0.294'), ('105', '0.429'), ('106', '0.300'), ('109', '0.491'), ('110', '0.445'),
     ('111', '0.299'), ('112', '0.139')]])
add('L10', 'P/QL1', 'projected', [dict(name=n, z=z) for n, z in
    [('A267', '0.230'), ('MS0906.5+1110', '0.180'), ('A773', '0.217'), ('MS1006.0+1202', '0.221'), ('A1204', '0.171'), ('A1240', '0.159'), ('A1413', '0.143'),
     ('A1682', '0.234'), ('A1689', '0.183'), ('A1763', '0.223'), ('A1914', '0.171'), ('A1942', '0.224'), ('RXJ1504-0248', '0.215'), ('A2034', '0.113'),
     ('A2069', '0.116'), ('A2111', '0.229'), ('RXJ1701+6414', '0.225'), ('A2259', '0.164'), ('RXJ1720.1+2638', '0.164'), ('RXJ2129.6+0005', '0.235')]])
add('L23b', 'P/QL1', 'projected', [dict(name='Abell 1651', z='0.084')])
add('S2b', 'E', '3D', [dict(name=n, z=z) for n, z in [x.split(' ') for x in
    'A85 0.0556;A119 0.0440;A262 0.0161;A496 0.0328;A644 0.0704;A754 0.0528;A1367 0.0216;A1651 0.0850;A2255 0.0800;A2319 0.0564;A3266 0.0594;A3558 0.0480;A4038 0.0283;A133 0.0569;A548e 0.0410;A1185 0.0304;A1650 0.0845;A1767 0.0701;A2107 0.0421;A2147 0.0351;A2151 0.0370;A2440 0.0904;A2589 0.0416;A2593 0.0433;A2626 0.0573;A2634 0.0312;A3389 0.0265'.split(';')]])
add('S3a', 'E', 'projected', [dict(name=n, z=z) for n, z in [x.rsplit(' ', 1) for x in
    'Abell 0122 .1134;Abell 1651 .0847;Abell 2400 .0880;Abell 2401 .0571;Abell 2405 .0368;Abell 2571 .1091;Abell 2721 .1144;Abell 2730 .1201;Abell 2811 .1079;Abell 2955 .0943;Abell 2969 .1259;Abell 2984 .1042;Abell 3112 .0753;Abell 3166 .1174;Abell 3693 .1229;Abell 3705 .0895;Abell 3727 .1159;Abell 3809 .0623;Abell 3920 .1268;Abell 4010 .0955;APMC 020 .1098;Abell S0084 .1080;Abell S0296 .0696'.split(';')]])
add('S3b', 'E', 'projected', [dict(name=n, z=z) for n, z in [x.rsplit(' ', 1) for x in
    'Abell 0122 0.1134;Abell 1651 0.0845;Abell 2401 0.0571;Abell 2721 0.1144;Abell 2811 0.1079;Abell 2955 0.0943;Abell 2984 0.1042;Abell 3112 0.0750;Abell 3693 0.1237;Abell 4010 0.0963;Abell S0084 0.1100;Abell S0296 0.0696'.split(';')]])
add('S4b', 'P (does not count)', 'not stated', [dict(name=n, z=z) for n, z in [x.split(' ') for x in
    'A85 0.0556;A400 0.0240;IIIZw54 0.0311;A1367 0.0216;MKW4 0.0200;ZwCl1215 0.0750;A1650 0.0845;Coma 0.0232;A1795 0.0616;MKW8 0.0270;A2029 0.0767;A2052 0.0348;MKW3S 0.0450;A2065 0.0721;A2142 0.0899;A2147 0.0351;A2199 0.0302;A2255 0.0800;A2589 0.0416'.split(';')]])
add('S4d', 'P (does not count)', 'not stated', [dict(name=n, z=z) for n, z in [x.split(' ') for x in 'A496 0.033;A1689 0.1823;A2050 0.1183;A2631 0.273;A2667 0.23'.split(';')]])
s6 = 'Abell2697 0.2320;Abell0068 0.2546;Abell0115 0.1971;Abell0141 0.2300;Abell0209 0.2060;Abell0267 0.2300;Abell0291 0.1960;Abell0521 0.2475;Abell0586 0.1710;Abell0611 0.2880;Abell0697 0.2820;ZwCl0857.9+2107 0.2347;Abell0750 0.1630;Abell0773 0.2170;Abell0781 0.2984;ZwCl0949.6+5207 0.2140;Abell0907 0.1669;Abell0963 0.2050;ZwCl1021.0+0426 0.2906;Abell1423 0.2130;Abell1451 0.1992;ZwCl1231.4+1007 0.2290;Abell1682 0.2260;Abell1689 0.1832;Abell1763 0.2279;Abell1835 0.2528;Abell1914 0.1712;ZwCl1454.8+2233 0.2578;Abell2009 0.1530;RXCJ1504.1-0248 0.2153;Abell2111 0.2290;Abell2204 0.1524;Abell2219 0.2281;RXJ1720.1+2638 0.1640;Abell2261 0.2240;RXCJ2102.1-2431 0.1880;RXJ2129.6+0005 0.2350;Abell2390 0.2329;Abell2537 0.2966;Abell2552 0.2998;Abell2631 0.2779'
add('S6', 'P/QL2', 'projected', [dict(name=n, z=z, nolum=(n == 'Abell2697')) for n, z in [x.split(' ') for x in s6.split(';')]])
add('S10a', 'P (does not count)', 'not stated', [dict(name='ACT-CL J0235-5121', z='0.278')])
add('S16b', 'E', 'projected', [dict(name=n, z=z) for n, z in [x.split(' ') for x in
    'A2390 0.2279;MS0016+16 0.5466;MS0302+16 0.4246;MS0440+02 0.1965;MS0451+02 0.2010;MS0451-03 0.5392;MS0839+29 0.1928;MS1006+12 0.2605;MS1008-12 0.3062;MS1224+20 0.3255;MS1231+15 0.2350;MS1358+62 0.3290;MS1455+22 0.2570;MS1512+36 0.3726;MS1621+26 0.4274'.split(';')]])
add('LV3', 'P/QL2', 'projected', [], note='614 maxBCG IDs with positions and z in VizieR J/MNRAS/449/2345 only; host unreachable; not cross-matched')

# ---------------- matching ----------------
hits = {}       # row index -> list of (rid, name as printed, z, how)
unmatched = {}  # rid -> list
cands = []
for rid, rec in L.items():
    for e in rec['entries']:
        keys = [norm(e['name'])] + ([norm(e['alt'])] if e.get('alt') and e['alt'] != '...' else [])
        if rid == 'L2' and e['name'] == 'A1656b': keys = ['a1656']
        i = next((index[k] for k in keys if k in index), None)
        how = 'name'
        if e.get('alt') and e['alt'] != '...' and i is not None and norm(e['alt']) in index and norm(e['name']) not in index:
            how = 'name (alternative name printed in source)'
        if rid == 'L2' and e['name'] == 'A1656b': how = 'name (component row "A1656b", counted with A1656)'
        if i is None:
            # coordinate route
            pc, ptol = None, 0
            if 'ra' in e:
                pc, ptol = SkyCoord(e['ra'] * u.deg, e['dec'] * u.deg, frame=FK5(equinox='J2000')), 0.1
            elif e.get('b1950'):
                b = e['b1950'].replace('2400', '0000', 1) if e['b1950'].startswith('24') else e['b1950']
                m = re.match(r'(\d\d)(\d\d)(\d\d\.\d)([+-])(\d\d)(\d\d)(\d\d)', b)
                pc = SkyCoord(hms(int(m[1]), int(m[2]), float(m[3])) * u.deg, dms(m[4], int(m[5]), int(m[6]), int(m[7])) * u.deg,
                              frame=FK4(equinox='B1950')).transform_to(FK5(equinox='J2000')); ptol = 0.1
            else:
                p = parse(e['name'])
                if p: pc, ptol = p
            if pc is not None:
                for (j, f, c, tol) in v2coords:
                    sep = pc.separation(c).arcmin
                    t = max(tol, ptol)
                    if sep <= max(3 * t, 10):
                        zs = v2z(rows[j]); ze = float(e['z']) if e.get('z') else None
                        dz = min(abs(ze - x) for x in zs) if (ze is not None and zs) else None
                        ok = sep <= t and dz is not None and dz <= 0.02
                        cands.append(dict(rid=rid, name=e['name'], z=e.get('z'), v2=rows[j]['name'], form=f, sep=round(sep, 1), tol=round(t, 1),
                                          dz=None if dz is None else round(dz, 4), accepted=ok))
                        if ok and i is None:
                            i = j; how = f'U5 computed: {sep:.1f}′ from {f} (tolerance {t:.1f}′, Δz {dz:.3f})'
        if i is None:
            unmatched.setdefault(rid, []).append(f"{e['name']}" + (f" {e['z']}" if e.get('z') else ''))
        else:
            hits.setdefault(i, []).append(dict(rid=rid, name=e['name'], z=e.get('z'), how=how, nolum=e.get('nolum', False)))

json.dump(dict(rows=rows, chan=chan, hits={str(k): v for k, v in hits.items()}, unmatched=unmatched, cands=cands,
               L={k: dict(code=v['code'], proj=v['proj'], n=len(v['entries']), note=v['note']) for k, v in L.items()},
               strict={str(i): strict_cls(r) for i, r in enumerate(rows)}), open(OUT, 'w'), ensure_ascii=False, indent=1)
print('matched clusters', len(hits))
for rid, v in unmatched.items(): print(rid, 'unmatched', len(v))
for c in cands: print('CAND', c)
