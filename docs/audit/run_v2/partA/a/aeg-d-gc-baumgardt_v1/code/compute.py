"""Audit reader A, stratum aeg-d-gc-baumgardt_v1.
Computes g_bar = G (1/2 L_V Y_V) / r_half^2 per REPRODUCTION.md (D-025), with
  r_half = 4/3 R_h, R_h = 10**Rh[pc] (MvdM05 King fit) * R_Sun(Harris)/Dist(MvdM05)
  L_V = 10**(-0.4 (M_V,t - M_V,sun)), M_V,sun = +4.85 (MvdM05 e-print, tex line 2161)
  Y_V = (M/L)1 (MvdM05 clusters table)
g_obs is NOT computed: the light-weighted dispersion step is not specified in the written method.
Run: python3 -I compute.py
"""
import csv, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vot, veldis
from astropy import constants as const, units as u
import astropy

PK = '/home/claude/audit_v2/packets/aeg-d-gc-baumgardt_v1'
OUT = os.path.dirname(HERE)
S = PK + '/sources'
MVSUN = 4.85  # MvdM05 arXiv:astro-ph/0605132, mclaughlin_vandermarel.tex line 2161

rows = list(csv.DictReader(open(PK + '/rows.csv')))

# Harris mwgc.dat: Part I (R_Sun col 7) and Part II (M_V,t col 8), by line
mw = open(S + '/mwgc.dat').read().split('\n')
part2_start = next(i for i, l in enumerate(mw) if 'Part II:' in l)
part3_start = next(i for i, l in enumerate(mw) if 'Part III:' in l)
def harris(name):
    out = {}
    for i, l in enumerate(mw):
        if l[:12].strip() != name:  # ID occupies first 12 chars
            continue
        tok = l.split()
        if i < part2_start and re.search(r'\d\d \d\d ', l):
            # Part I: last 5 tokens are R_Sun R_gc X Y Z
            out['R_Sun'] = (tok[-5], i + 1)
        elif part2_start < i < part3_start:
            # Part II after the name: [Fe/H] wt E(B-V) V_HB (m-M)V V_t M_V,t ...
            rest = l[12:].split()
            out['M_V,t'] = (rest[6], i + 1)
            out['V_t'] = (rest[5], i + 1)
            out['(m-M)V'] = (rest[4], i + 1)
    return out

fm, rm = vot.read(S + '/mvdm05/J_ApJS_161_304_models.vot')
fc, rc = vot.read(S + '/mvdm05/J_ApJS_161_304_clusters.vot')
bins = veldis.parse(S + '/veldis.html')

G = const.G
vals, inputs = [], []
for r in rows:
    mid, name = r['measurement_id'], r['system_name']
    key = 'MW-' + name.replace(' ', '').upper()
    h = harris(name)
    kfit = [dict(zip(fm, x)) for x in rm if x[1].strip() == key and dict(zip(fm, x))['Mod'].strip() == 'K']
    cl = [dict(zip(fc, x)) for x in rc if x[1].strip() == key]
    assert len(kfit) == 1 and len(cl) == 1, (name, len(kfit), len(cl))
    k, c = kfit[0], cl[0]
    def add(inp, v, unit, loc):
        inputs.append(dict(measurement_id=mid, input=inp, value=v, unit=unit, locator=loc))
    add('R_Sun', h['R_Sun'][0], 'kpc', f"mwgc.dat line {h['R_Sun'][1]} (Part I, {name}, col 7 R_Sun)")
    add('M_V,t', h['M_V,t'][0], 'mag', f"mwgc.dat line {h['M_V,t'][1]} (Part II, {name}, col 8 M_V,t)")
    mvloc = f"mvdm05/J_ApJS_161_304_models.vot recno {k['recno']} ({key}, Mod=K)"
    add('Rh', k['Rh'], 'log(pc)', mvloc + ' col Rh')
    add('Dist', k['Dist'], 'kpc', mvloc + ' col Dist')
    add('W0/gamma', k['W0/gamma'], '', mvloc + ' col W0/gamma (needed only for g_obs light weights)')
    add('r0pc', k['r0pc'], 'pc', mvloc + ' col r0pc (needed only for g_obs light weights)')
    add('(M/L)1', c['(M/L)1'], 'Sun (M/L_V, solar units)', f"mvdm05/J_ApJS_161_304_clusters.vot recno {c['recno']} ({key}) col (M/L)1")
    add('M_V,sun', '+4.85', 'mag', 'arXiv:astro-ph/0605132 e-print, mclaughlin_vandermarel.tex line 2161')
    rv = [b for b in bins if b['cluster'] == name and b['type'] == 'RV']
    for j, b in enumerate(rv, 1):
        loc = f"veldis.html line {b['line']} ({name}, RV bin {j})"
        add(f'<r> RV bin {j}', b['r'], 'arcsec', loc)
        add(f'NStar RV bin {j}', b['N'], '', loc)
        add(f'sigma RV bin {j}', b['sigma'], 'km/sec', loc)
        add(f'DsigmaUp RV bin {j}', b['up'], 'km/sec', loc)
        add(f'DsigmaLow RV bin {j}', b['low'], 'km/sec', loc)

    Rh_pc = 10 ** float(k['Rh']) * float(h['R_Sun'][0]) / float(k['Dist'])
    r_half = (4.0 / 3.0) * Rh_pc * u.pc
    L_V = 10 ** (-0.4 * (float(h['M_V,t'][0]) - MVSUN))
    M = 0.5 * L_V * float(c['(M/L)1']) * u.M_sun
    g_bar = (G * M / r_half ** 2).to(u.m / u.s ** 2).value
    note = ("g_obs not computed: the written method names aeg.dispersion.light_weighted_dispersion 'as frozen' and King (1966) light weights "
            "but gives no formula for the light-weighted global sigma (sigma vs sigma^2 weighting, annulus light integral), no rule for inferring bin edges "
            "from mean radii, no definition of light coverage, and no rule for the light outside the covered radii; "
            f"{len(rv)} RV bins read. g_bar computed: r_half={r_half.value:.6g} pc, L_V={L_V:.6g} Lsun; M_sun and pc taken from astropy {astropy.__version__} "
            "(method names astropy.constants.G only).")
    vals.append(dict(measurement_id=mid, g_obs='', g_bar=f'{g_bar:.6e}', status='method incomplete', notes=note))

with open(OUT + '/values.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['measurement_id', 'g_obs', 'g_bar', 'status', 'notes']); w.writeheader(); w.writerows(vals)
with open(OUT + '/inputs.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['measurement_id', 'input', 'value', 'unit', 'locator']); w.writeheader(); w.writerows(inputs)
print(len(vals), 'rows;', len(inputs), 'inputs')
