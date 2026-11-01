"""Gas coverage and programme coherence for the A9 clusters pairable with an observed side (coverage v3,
recommended QL2). Names, redshifts, positions (matching only), record ids, centres, apertures and method names.
No result value is read or written.

python3 -I build.py <pairable.json> <positions.csv> <chexmate.csv> <xxl_pos.csv> <L5a.csv> <outdir>
"""
import sys, json, re, csv, math

PAIR, POS, CHX, XXLPOS, L5A, OUT = sys.argv[1:7]
pair = json.load(open(PAIR))

# ---------------- names (normalisation copied from coverage-v3-tools/cov3.py, plus RX J / RXC J spacing) ----
def norm(s):
    s = s.lower().replace('−', '-').replace('–', '-').replace(' ', '')
    s = 'coma' if s.startswith('coma') else s
    s = s.replace('abell', 'a').replace('aco', 'a')
    s = re.sub(r'^zwcl', 'zw', s)
    s = re.sub(r'^rx-?j', 'rxj', s)
    s = re.sub(r'^rxcj', 'rxcj', s)
    s = re.sub(r'^ms-', 'ms', s)
    s = re.sub(r'^a-?s0*(\d+)', r'as\1', s)
    s = re.sub(r'^a0*(\d+)', r'a\1', s)
    s = re.sub(r'^mkw0*(\d)', r'mkw\1', s)
    s = re.sub(r'^xlssc0*(\d+)', lambda m: 'xlssc%03d' % int(m.group(1)), s)
    return s

def keys(c):
    k = {norm(c['name'])} | {norm(f) for f in c['forms']} | {norm(v) for v in c['star_names'].values()}
    if c['name'].startswith('Coma'): k |= {'a1656', 'coma'}
    return k

def z0(c):
    m = re.search(r'(?<![\d.])0\.\d+', c['z'])
    return float(m.group(0))

# ---------------- positions (used only for matching; not written to the report) ----------------
pos = {}
def addpos(src, name, ra, dec):
    pos.setdefault(norm(name), []).append((src, float(ra), float(dec)))
for r in csv.DictReader(open(POS)):
    addpos(r['source'], r['name'], r['ra_deg'], r['dec_deg'])
for r in csv.reader(open(XXLPOS)):
    addpos('umetsu20', 'XLSSC ' + r[0], r[1], r[2])
for r in csv.reader(open(L5A)):
    addpos('L5a', r[0], r[2], r[3]); addpos('L5a', r[1], r[2], r[3])

def sep(a, b):
    ra1, d1, ra2, d2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(ra1 - ra2)
    return math.degrees(math.acos(max(-1, min(1, c)))) * 60

chx = []
for r in csv.DictReader(open(CHX)):
    h, m, s = map(float, r['ra_xpeak'].split(':'))
    d = r['dec_xpeak']; sg = -1 if d.startswith('-') else 1
    dd, dm, ds = map(float, d.lstrip('+-').split(':'))
    chx.append(dict(name=r['name'], ra=15 * (h + m / 60 + s / 3600), dec=sg * (dd + dm / 60 + ds / 3600), z=float(r['z']), tier=r['tier']))
TOL_ARCMIN, TOL_DZ = 3.0, 0.02
DR1 = set('G008.31-64.74 G041.45+29.10 G042.81+56.61 G046.88+56.48 G050.40+31.17 G056.77+36.32 G056.93-55.08 G057.78+52.31 '
          'G057.78+52.32 G057.92+27.64 G066.41+27.03 G072.62+41.46 G077.90-26.63 G083.86+85.09 G113.29-29.69 G113.91-37.01 '
          'G114.79-33.71 G149.39-36.84 G195.75-24.32 G207.88+81.31 G224.00+69.33 G238.69+63.26 G243.15-73.84 G243.64+67.74 '
          'G277.76-51.74 G287.46+81.12 G313.33+61.13 G313.88-17.11 G324.04+48.79 G340.94+35.07 G349.46-59.95'.split())

# ---------------- gas-source membership lists (read at source; see tools/*.csv) ----------------
XCOP = {norm(n) for n in 'A85 A644 A1644 A1795 A2029 A2142 A2255 A2319 A3158 A3266 RXC1825 ZW1215'.split()}
def srcnames(src): return {k for k, v in pos.items() if any(x[0] == src for x in v)}
MARTINO = srcnames('martino14'); MULROY19 = srcnames('mulroy19'); CHECS = srcnames('checs'); CLASHX = srcnames('clashx')
HICKS = srcnames('hicks06')
# Martino+2014 prints 'ABELL 0115s'; its position is 0.01' from Mulroy+2019 'Abell0115' (same component): flagged match
if 'a115s' in MARTINO: MARTINO.add('a115')

# ---------------- programme, centre and aperture of every input ----------------
OBS = {  # A9 observed-side records: programme, centre (as read), radial coverage (as in the A9 readings)
 'C1a': ('CLASH', 'BCG (Umetsu+2014 §, Table 1)', 'Subaru WL 0.9′–16′, 10 log bins'),
 'C1b': ('CLASH', 'BCG (Umetsu+2016 Table 1 note a)', 'HST SL bins + Subaru WL 0.9′–16′'),
 'C1c': ('CLASH', 'n/a (2D lens model)', 'HST field of view only'),
 'C4a': ('CLASH', 'n/a (SL model)', 'core, ≲ 0.2 R200c'),
 'C5a': ('CLASH', 'not read', 'to ≈ 3 Mpc/h70'),
 'C6a': ('LoCuSS', 'n/a (SL core model)', 'core, R < 250 kpc'),
 'C6c/C6d': ('LoCuSS', 'BCG (optical centroid of the BCG; Okabe & Smith 2016 §)', 'per-cluster shear profiles; NFW fits (tier 2)'),
 'C9a': ('A1689 (Broadhurst/Umetsu)', 'not read', 'SL core'), 'C9b': ('A1689 (Broadhurst/Umetsu)', 'not read', 'WL r < 2 Mpc/h'),
 'C9c': ('A1689 (Halkola)', 'not read', 'SL ≤ 0.3 Mpc/h70 + WL to ≈ 2.5 Mpc'),
 'C9d/C9e': ('A1689 (Broadhurst/Umetsu)', 'not read', 'WL + SL'), 'C9e/C9f': ('A1689 (Broadhurst/Umetsu)', 'not read', 'WL beyond r_vir'),
 'C9f/C9g': ('A1689 (Diego)', 'not read', 'SL + WL, binned mean profile'), 'C9g/C9h': ('CHEX-MATE', 'not read (gas: X-ray peak)', 'WL'),
 'C11a': ('AMiBA/Subaru (Umetsu+2009)', 'not read', 'Subaru WL'), 'C11b': ('Suzaku/Subaru (Okabe+2014)', 'not confirmed', 'WL to virial radius'),
 'C12c': ('CFH12k (Bardeau)', 'not read', 'WL'), 'C12d': ('CFH12k (Bardeau)', 'BCG (Bardeau+2007 §)', 'WL shear profiles'),
 'C12f': ('WFI (Clowe & Schneider)', 'not read', 'WL'), 'C13a': ('Coma WL (Gavazzi)', 'convergence-map peak (Gavazzi+2009)', 'WL'),
 'C13c': ('A209 WL (Paulin-Henriksson)', 'not read', 'WL'), 'C13h': ('A383 WL (Huang)', 'not read', 'WL'),
 'C14a': ('Euclid ERO', 'not read', 'SL + WL'), 'C14b': ('Euclid ERO', 'not read', 'WL to 3.07 Mpc'),
 'C18c': ('XXL', 'X-ray peak (Umetsu+2020 §)', 'HSC ΔΣ 0.3–3 h⁻¹ Mpc comoving, 8 bins'),
 'C18d': ('APEX-SZ', 'BCG (Klein+2019 §3.4)', 'WFI/Suprime-Cam shear; NFW fits'),
 'C20a': ('SAO caustic team (HeCS)', 'hierarchical centre (Rines+2013 §3)', 'caustic, to infall region'),
 'C20c': ('SAO caustic team (HeCS/CHeCS)', 'caustic centre from the caustic analysis (Logan+2022 §)', 'caustic profiles (figures)'),
 'C20d': ('SAO caustic team (CIRS+HeCS)', 'not stated in text searched', 'caustic, to ≈ 3 R200'),
 'C21a': ('SAO caustic team (CAIRNS)', 'hierarchical centre (Rines+2003 Table 9)', 'caustic, to 5–10 Mpc'),
 'C21b': ('SAO caustic team (CAIRNS)', 'as C21a', 'as C21a'), 'C21c': ('SAO caustic team (A2199)', 'not read', 'caustic, to ≈ 8 h⁻¹ Mpc'),
 'C23a': ('SAO caustic team (Coma)', 'not read', 'caustic to 10 h⁻¹ Mpc'), 'C23b': ('SAO caustic team (Coma)', 'not read', 'caustic'),
 'C23c': ('DESI Coma (Pedratti)', 'NGC 4874 (Pedratti+2026 §)', 'Jeans, R 0.10–2.30 Mpc'),
 'C28a': ('A2142 (Munari)', 'X-ray centre of De Grandi & Molendi 2002 (Munari+2014 §)', 'caustic/MAMPOSSt'),
 'C29a': ('eRASS1 (Li+2024)', 'not determined (BCG and X-ray centre both listed)', 'Jeans, ≈ 68–3820 kpc'),
 'C29b': ('CHEX-MATE', 'not stated in text searched', 'MAMPOSSt 0.05 Mpc–1.1 r200'),
}
STARS = {  # counting star records: programme, centre, aperture definition
 'L1': ('Lin & Mohr (2MASS)', 'X-ray centre (archival ROSAT or literature; Lin+2004 §2)', 'r500 and r200 from the M–T_X relation; 3D (NFW deprojection)'),
 'S2b': ('Lin & Mohr (2MASS)', 'not stated in text searched', 'r500 from the M–T_X relation; 3D (NFW c = 5)'),
 'L2': ('Girardi+2000', 'G98 centres (not read)', '0.5/1.0/1.5 h⁻¹ Mpc and R_vir (G98 virial); projected'),
 'L5a': ('RASS-SDSS (Popesso)', 'X-ray (L9 reader B)', 'fixed metric, 1.0 h70⁻¹ Mpc printed (20 apertures in catalogue); projected'),
 'L5c': ('RASS-SDSS (Popesso)', 'X-ray centre where definable (Popesso+2007 §)', 'r200 from σ (virial); projected'),
 'L8': ('LoCuSS', 'not stated in text searched', '1 Mpc and r500,WL (Okabe weak lensing); projected'),
 'S6': ('LoCuSS', 'BCG (Mulroy+2019 §2.4)', 'r500,WL (Okabe & Smith 2016); projected'),
 'L9': ('XXL', 'X-ray centroid (Ziparo+2016 §3.1)', 'r500,WL (XXL Paper IV) and 1 Mpc; projected'),
 'L10': ('Laganá+2009', 'X-ray centre of Maughan+2008 (Laganá+2009 §)', 'r500 from Maughan+2008 (X-ray); projected'),
 'S16b': ('CNOC (Muzzin)', 'not stated in text searched', 'R200 from σ; projected'),
 'S8d': ('CLASH-VLT (Annunziatella)', 'not read', 'stellar-mass density profile; geometry not stated'),
 'S10b': ('SPT (Chiu)', 'not stated in text searched', 'R500 from SZ mass; 3D'),
 'S12b': ('X-COP', 'X-ray centroid (Ghizzardi+2021 §)', 'cumulative profile + R500 (hydrostatic); 3D'),
 'S4b': ('—', '—', 'not stated'),
}
GAS = {  # gas sources: programme, centre, form (eligibility under §1 item 4)
 'X-COP': ('X-COP', 'X-ray peak (Ghirardini+2019 §)', 'binned deprojected profiles, public release (Atlas package aeg-d-xcop/v1)', 'eligible'),
 'CHEX-MATE': ('CHEX-MATE', 'X-ray peak (CHEX-MATE 2021 Table B.1 coordinates)', 'per-cluster density profiles not found published (DR1: temperature profiles only, CDS)', 'not yet available'),
 'C3a CLASH-X': ('CLASH', 'not stated in text searched', 'JACO parametric + non-parametric annuli; profiles in figures, inputs on MAST (tier 3)', 'eligible (tier 3)'),
 'Martino+2014': ('LoCuSS', 'X-ray centroid (Martino+2014 §3)', 'gas mass at r2500, r1000, r500 (hydrostatic radii) only; density model not tabulated', 'aperture only'),
 'Mulroy+2019 gas': ('LoCuSS', 'BCG (Mulroy+2019 §2.4)', 'gas mass within r500,WL only (from fitted density templates)', 'aperture only'),
 'C20c CHeCS': ('SAO caustic team (HeCS/CHeCS)', 'X-ray centroid (Logan+2022 §)', 'parametric 3D density (Vikhlinin 2006); per-cluster parameters not seen in tables', 'fit; release unverified'),
 'C15a Hicks+2006': ('CNOC (Hicks)', 'fitted X-ray centroid (Hicks+2006 §)', 'single and double β-model fits (Table 2)', 'fit (eligible within range)'),
 'C9h/C9i Peng+2009': ('A1689 (Peng)', 'not confirmed', 'annuli + parametric fits (Tables 10–11)', 'eligible'),
 'C9g/C9h CHEX-MATE A1689': ('CHEX-MATE', 'X-ray peak (Chappuis+2025 §)', 'XMM density (hydromass)', 'eligible (E record)'),
 'C11b Okabe+2014': ('Suzaku/Subaru (Okabe+2014)', 'not confirmed', 'fits in tables, binned in figures', 'eligible (E record)'),
 'C11a Umetsu+2009 (AMiBA)': ('AMiBA/Subaru (Umetsu+2009)', 'not read', 'SZ β/NFW model fit only', 'fit only (E record)'),
 'C29a Li+2024': ('eRASS1 (Li+2024)', 'best-fit X-ray centre (Li+2024 Table 1)', 'parametric density (MBProj2D), best-fit parameters Table 2', 'fit (E record)'),
 'Mirakhor & Walker 2020': ('Coma XMM+Planck', 'X-ray peak (Mirakhor & Walker 2020 §2)', 'onion-peeling deprojected profile; figures (tabulation not checked)', 'binned (figures)'),
 'Eckert+2016 (XXL XIII)': ('XXL', 'X-ray (best-fit position / peak; Eckert+2016 §2)', 'density profiles in Fig. 1 only; aperture r500,MT (M–T relation)', 'figures only'),
 'Akamatsu+2011': ('A2142 (Suzaku)', 'not read', 'named by C28a; not read', 'not read'),
 'Nagarajan+2018 (APEX-SZ)': ('APEX-SZ', 'not read', 'SZ analysis named by Klein+2019; not read; not stated as a density profile', 'not read'),
}

rows = []
for c in pair:
    K = keys(c); z = z0(c)
    recs = c['recs']
    gas = []
    # 1. X-COP
    if K & XCOP: gas.append('X-COP')
    # 2. CHEX-MATE: by PSZ2 name form, else by position (X-ray peak) within 3' and |dz| <= 0.02
    cm = None
    for f in c['forms'] + [c['name']]:
        if f.startswith('PSZ2'):
            for x in chx:
                if x['name'].replace(' ', '') == f.replace(' ', ''): cm = (x, 'name')
    if not cm:
        best = None
        for k in K:
            for (src, ra, dec) in pos.get(k, []):
                for x in chx:
                    d = sep((ra, dec), (x['ra'], x['dec']))
                    if d <= TOL_ARCMIN and abs(x['z'] - z) <= TOL_DZ and (best is None or d < best[1]):
                        best = (x, d, src)
        if best: cm = (best[0], f"position ({best[1]:.1f}′ from {best[2]} position; Δz ≤ {TOL_DZ})")
    c['_has_pos'] = any(pos.get(k) for k in K)
    if cm: gas.append('CHEX-MATE')
    # 3. survey gas named by the observed side
    rids = {r for r, _ in recs}
    if 'C3a' in rids or (K & CLASHX): gas.append('C3a CLASH-X')
    if K & MARTINO: gas.append('Martino+2014')
    if K & MULROY19: gas.append('Mulroy+2019 gas')
    if 'C20c' in rids or (K & CHECS): gas.append('C20c CHeCS')
    if 'C15a' in rids: gas.append('C15a Hicks+2006')
    if 'C9h/C9i' in rids: gas.append('C9h/C9i Peng+2009')
    if 'C9g/C9h' in rids: gas.append('C9g/C9h CHEX-MATE A1689')
    if 'C11b' in rids: gas.append('C11b Okabe+2014')
    if 'C11a' in rids: gas.append('C11a Umetsu+2009 (AMiBA)')
    if 'C29a' in rids: gas.append('C29a Li+2024')
    if c['name'].startswith('Coma'): gas.append('Mirakhor & Walker 2020')
    if 'C18c' in rids: gas.append('Eckert+2016 (XXL XIII)')
    if 'C28a' in rids: gas.append('Akamatsu+2011')
    if 'C18d' in rids: gas.append('Nagarajan+2018 (APEX-SZ)')
    # per channel
    out_ch = {}
    for ch in ('L', 'O'):
        if not (c['pair'] == ch or c['pair'] == 'both'): continue
        geo = 'projected' if ch == 'L' else '3D'
        obs = [r for r, cc in recs if cc == ch and r in OBS]
        stars = [s for s, g in c['stars'] if g == geo]
        best = None
        for o in obs:
            for s in stars:
                for g in gas or ['(none)']:
                    po = OBS[o][0]; ps = STARS[s][0]; pg = GAS[g][0] if g in GAS else '—'
                    same = max([po, ps, pg].count(p) for p in (po, ps, pg) if p != '—')
                    elig = GAS.get(g, ('', '', '', 'none'))[3]
                    rank = (same, elig.startswith('eligible'), elig.startswith('fit'))
                    if best is None or rank > best[0]:
                        best = (rank, o, s, g, same)
        out_ch[ch] = dict(obs=obs, stars=stars, best=best)
    rows.append(dict(name=c['name'], z=c['z'], pair=c['pair'], gas=gas, chx=(cm[0]['name'], cm[0]['tier'], cm[0]['name'][5:] in DR1, cm[1]) if cm else None,
                     ch=out_ch, has_pos=c['_has_pos']))

json.dump(dict(rows=rows, OBS=OBS, STARS=STARS, GAS=GAS), open(OUT + '/gas.json', 'w'), ensure_ascii=False, indent=1)

# ---------------- summaries ----------------
print('clusters', len(rows), 'no position:', [r['name'] for r in rows if not r['has_pos']])
print('CHEX-MATE matches:', [(r['name'], r['chx']) for r in rows if r['chx']])
from collections import Counter
cnt = Counter(g for r in rows for g in r['gas'])
print(cnt)
print('no gas candidate:', [r['name'] for r in rows if not r['gas']])
sc = Counter((ch, v['best'][4] if v['best'] else 0) for r in rows for ch, v in r['ch'].items())
print(sorted(sc.items()))
