"""Reader B audit computation for aeg-d-dwarfs_v1.

Method (REPRODUCTION.md, D-025 as written there):
  R_h  = a * sqrt(1 - eps)            (circularised, from semi-major a)
  r_half = 4/3 * R_h
  g_obs = 3 sigma^2 / r_half
  g_bar = G (1/2 L_V Upsilon_V + M_gas(<r_half)) / r_half^2
  L_V from extinction-corrected apparent V and distance modulus, M_V,sun from the
  Upsilon_V source (McLaughlin & van der Marel 2005: +4.85).
  Upsilon_V: linear interpolation in [Fe/H] of (M/L)1 (BC03 + Chabrier disk) over
  the MW globular clusters of MvdM05; below the lowest tabulated [Fe/H] use the
  lowest value (flag beyond_source_range).
Constants: the method states no value of G, of the parsec in metres, or of the
solar mass, so g_bar is NOT computed (method incomplete). g_obs uses only unit
definitions: 1 km = 1000 m; 1 pc = 648000/pi au, 1 au = 149597870700 m (IAU 2012/2015
exact definitions) -- flagged in notes as a unit definition not stated in the method.
"""
import sys, math, csv, json
from astropy.io.votable import parse_single_table

VOT = sys.argv[1]
OUT = sys.argv[2]

AU_M = 149597870700.0
PC_M = 648000.0 / math.pi * AU_M
MV_SUN = 4.85  # MvdM05 p.22 (arXiv astro-ph/0605132v1), the Upsilon_V source
HE = 1.33      # descriptor.json x_baryon_inventory (not needed: all gas absent)

# --- Upsilon_V table ---
t = parse_single_table(VOT).to_table()
pts = {}
for r in t:
    if not str(r['Cluster']).startswith('MW-'):
        continue
    feh = round(float(r['__Fe_H_']), 2)
    ml = round(float(r['__M_L_1']), 3)
    if feh in pts and pts[feh] != ml:
        raise SystemExit(f'non-unique M/L at [Fe/H]={feh}')
    pts[feh] = ml
xs = sorted(pts)

def upsilon(feh):
    if feh <= xs[0]:
        return pts[xs[0]], feh < xs[0]
    if feh >= xs[-1]:
        return pts[xs[-1]], feh > xs[-1]
    for x0, x1 in zip(xs, xs[1:]):
        if x0 <= feh <= x1:
            y0, y1 = pts[x0], pts[x1]
            return y0 + (y1 - y0) * (feh - x0) / (x1 - x0), False

def dist_pc(mu):
    return 10 ** (mu / 5 + 1)

ARCMIN = math.pi / (180 * 60)

# Per-system inputs as read (see inputs.csv). a in arcmin unless a_pc given.
S = [
 dict(id='aeg-d-dwarfs/v1/m000059', name='Tucana', sigma=14.4, limit=False,
      a_pc_at=(205.0, 24.69), geometric=True, eps=0.48, mu=24.74,
      MV_own=(-9.55, 24.69), feh=-1.95),
 dict(id='aeg-d-dwarfs/v1/m000012', name='And XV', sigma=4.0, limit=False,
      a=1.3, eps=0.24, mu=24.37, mV0=16.0, feh=None),
 dict(id='aeg-d-dwarfs/v1/m000007', name='And IX', sigma=10.9, limit=False,
      a=2.0, eps=0.00, mu=24.23, mV0=15.6, feh=None),
 dict(id='aeg-d-dwarfs/v1/m000036', name='Draco II', sigma=2.6, limit=True,
      a=3.0, eps=0.23, mu=16.67, MV_own=(-0.8, 16.67), feh=-2.94),
 dict(id='aeg-d-dwarfs/v1/m000013', name='And XVI', sigma=3.8, limit=False,
      a=1.0, eps=0.29, mu=23.70, mV0=16.1, feh=None),
 dict(id='aeg-d-dwarfs/v1/m000003', name='And III', sigma=9.3, limit=False,
      a=2.0, eps=0.59, mu=24.29, mV0=14.8, feh=None),
 dict(id='aeg-d-dwarfs/v1/m000031', name='CVn II', sigma=5.28, limit=False,
      a=1.51, eps=0.46, mu=21.02, MV_D=(-5.17, 160.0), feh=-2.12),
 dict(id='aeg-d-dwarfs/v1/m000020', name='And XXIII', sigma=7.1, limit=False,
      a=5.4, eps=0.41, mu=24.36, mV0=14.6, feh=-2.2),
 dict(id='aeg-d-dwarfs/v1/m000042', name='Leo I', sigma=9.9, limit=False,
      a=3.30, eps=0.30, mu=(22.06 + 22.25) / 2, MV_D=(-11.78, 254.0), feh=-1.31),
 dict(id='aeg-d-dwarfs/v1/m000010', name='And XII', sigma=4.0, limit=True,
      a=1.8, eps=0.61, mu=24.28, mV0=17.7, feh=-2.2),
]

res = []
for s in S:
    D = dist_pc(s['mu'])
    if 'a_pc_at' in s:
        a_pc0, mu0 = s['a_pc_at']
        ang = a_pc0 / dist_pc(mu0)          # radians
        r_pc = ang * D
        Rh_pc = r_pc if s.get('geometric') else r_pc * math.sqrt(1 - s['eps'])
        Rh_alt = r_pc * math.sqrt(1 - s['eps'])
    else:
        a_pc = s['a'] * ARCMIN * D
        Rh_pc = a_pc * math.sqrt(1 - s['eps'])
        Rh_alt = None
    rhalf_pc = 4 / 3 * Rh_pc
    rhalf_m = rhalf_pc * PC_M
    g_obs = 3 * (s['sigma'] * 1e3) ** 2 / rhalf_m
    # luminosity
    if 'mV0' in s:
        MV = s['mV0'] - s['mu']
    elif 'MV_own' in s:
        mv, muown = s['MV_own']; MV = (mv + muown) - s['mu']
    else:
        mv, dkpc = s['MV_D']; MV = (mv + 5 * math.log10(dkpc * 1e3 / 10)) - s['mu']
    LV = 10 ** (-0.4 * (MV - MV_SUN))
    if s['feh'] is not None:
        ups, beyond = upsilon(s['feh'])
        mstar_half = 0.5 * LV * ups
    else:
        ups = beyond = mstar_half = None
    res.append(dict(id=s['id'], name=s['name'], D_kpc=D / 1e3, Rh_pc=Rh_pc,
                    Rh_alt_semimajor_pc=Rh_alt, rhalf_kpc=rhalf_pc / 1e3,
                    g_obs=g_obs, MV=MV, LV_Lsun=LV, feh=s['feh'], upsilon=ups,
                    beyond_source_range=beyond, M_bar_half_Msun=mstar_half,
                    M_gas=0.0, limit=s['limit']))
    if Rh_alt:
        res[-1]['g_obs_alt_if_Re_semimajor'] = 3 * (s['sigma'] * 1e3) ** 2 / (4 / 3 * Rh_alt * PC_M)
# diagnostic: Upsilon at alternative [Fe/H] choices
diag = {'Leo I [Fe/H]=-1.61 (ZW84)': upsilon(-1.61)[0], 'Leo I [Fe/H]=-1.45 (Munoz T1)': upsilon(-1.45)[0],
        'Tucana [Fe/H]=-1.82 (Saviane)': upsilon(-1.82)[0], 'lowest': (xs[0], pts[xs[0]])}
json.dump(dict(results=res, diag=diag), open(OUT, 'w'), indent=1)
for r in res:
    print(r['name'], f"Rh={r['Rh_pc']:.2f}pc r½={r['rhalf_kpc']:.5f}kpc g_obs={r['g_obs']:.4e} MV={r['MV']:.3f} LV={r['LV_Lsun']:.4e} ups={r['upsilon']} Mhalf={r['M_bar_half_Msun']}")
print(diag)
