"""Audit reader A, stratum aeg-d-xcop_v1.

Computes g_obs and g_bar following only the written method in
packets/aeg-d-xcop_v1/method/SOURCE.md (the package method file for v1).

Usage: python3 -I compute.py <extract_dir> <rows.csv> <out_dir>

Locator convention: "row N" is read as the 1-based FITS table row (FITS
convention), i.e. numpy index N-1. See notes.md for why.
"""
import csv
import sys
import numpy as np
from astropy.io import fits
from astropy import constants as const
from astropy import units as u

EXTRACT, ROWS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

G = const.G.to_value(u.m**3 / u.kg / u.s**2)       # method: G from astropy
MSUN = const.M_sun.to_value(u.kg)                   # method: Msun from astropy
KPC = (1 * u.kpc).to_value(u.m)

# Ettori et al. 2019 (arXiv:1805.00035 e-print, mass_xcop.tex, Table 1 = tab:mass)
# Only used for the five modelled-star clusters (method: D-022 item 3).
TABLE1 = {  # name: (R500 [Mpc], M500 [1e14 Msun], R200 [Mpc]) as printed
    'A1644': ('1.054', '3.48', '1.778'),
    'A2255': ('1.196', '5.26', '2.033'),
    'A3158': ('1.123', '4.26', '1.766'),
    'A3266': ('1.430', '8.80', '2.325'),
    'RXC1825': ('1.105', '4.08', '1.719'),
}
TABLE1_LINE = {'A1644': 'mass_xcop.tex line 315', 'A2255': 'mass_xcop.tex line 319',
               'A3158': 'mass_xcop.tex line 321', 'A3266': 'mass_xcop.tex line 322',
               'RXC1825': 'mass_xcop.tex line 324'}
MODELLED = set(TABLE1)


def p32(v):
    """Print a FITS float32 value with its own shortest repr (as stored)."""
    return str(np.float32(v)) if not isinstance(v, str) else v


def loglog_interp(r, rgrid, mgrid):
    """Linear in log M against log r (method: Interpolation). Returns value
    and the bracketing indices used."""
    lr, lrg, lmg = np.log10(r), np.log10(rgrid), np.log10(mgrid)
    j = np.searchsorted(lrg, lr)  # rgrid[j-1] < r <= rgrid[j]
    if j == 0:
        if lr == lrg[0]:
            return float(mgrid[0]), (0, 0)
        raise ValueError('below grid')
    if j >= len(lrg):
        raise ValueError('above grid')
    t = (lr - lrg[j - 1]) / (lrg[j] - lrg[j - 1])
    return float(10 ** (lmg[j - 1] + t * (lmg[j] - lmg[j - 1]))), (j - 1, j)


def nfw_shape(x):
    return np.log1p(x) - x / (1 + x)


vals, inps = [], []
with open(ROWS) as f:
    rows = list(csv.DictReader(f))

for row in rows:
    mid, c = row['measurement_id'], row['system_name']
    ref = row['source_ref']
    nrow = int(ref.rsplit('row', 1)[1])
    i = nrow - 1
    notes = []
    status = 'ok'

    def add(name, value, unit, loc):
        inps.append([mid, name, value, unit, loc])

    hf = f'{c}/{c}_hydro_mass.fits'
    hd = fits.open(f'{EXTRACT}/{hf}')['HYDRO_MASS'].data
    r_kpc = float(hd['RADIUS'][i])
    m_forw = float(hd['M_FORW'][i])
    add('RADIUS', p32(hd['RADIUS'][i]), 'kpc', f'allfiles.tar.gz:{hf}:ext HYDRO_MASS:row {nrow}:col RADIUS')
    add('M_FORW', p32(hd['M_FORW'][i]), 'Msun', f'allfiles.tar.gz:{hf}:ext HYDRO_MASS:row {nrow}:col M_FORW')
    r_m = r_kpc * KPC
    g_obs = G * m_forw * MSUN / r_m**2

    # gas
    gf = f'{c}/{c}_fgas_profile.fits'
    gh = fits.open(f'{EXTRACT}/{gf}')['FGAS']
    R500h = float(gh.header['R500'])
    add('R500', p32(gh.header['R500']), 'kpc (header comment "NFW R500"; unit not stated in header)',
        f'allfiles.tar.gz:{gf}:ext FGAS:header R500')
    rg = np.array(gh.data['RADIUS'], float) * R500h
    mg = np.array(gh.data['MGAS'], float)
    mgas, (a, b) = loglog_interp(r_kpc, rg, mg)
    for k in sorted({a, b}):
        add('RADIUS', p32(gh.data['RADIUS'][k]), 'R/R500', f'allfiles.tar.gz:{gf}:ext FGAS:row {k+1}:col RADIUS')
        add('MGAS', p32(gh.data['MGAS'][k]), 'Msun', f'allfiles.tar.gz:{gf}:ext FGAS:row {k+1}:col MGAS')
    g_gas = G * mgas * MSUN / r_m**2

    # stars
    if c in MODELLED:
        R500s, M500s, R200s = TABLE1[c]
        loc = f'arXiv:1805.00035 e-print {TABLE1_LINE[c]} (Table 1, row {c})'
        add('R_500', R500s, 'Mpc', loc + ', col R_500')
        add('M_500', M500s, '1e14 Msun', loc + ', col M_500')
        add('R_200', R200s, 'Mpc', loc + ', col R_200')
        R500 = float(R500s) * 1000.0  # Mpc -> kpc
        M500 = float(M500s)           # in 1e14 Msun
        rs = float(R200s) * 1000.0 / 2.9
        mgas500, (a5, b5) = loglog_interp(R500, rg, mg)
        for k in sorted({a5, b5}):
            add('RADIUS', p32(gh.data['RADIUS'][k]), 'R/R500', f'allfiles.tar.gz:{gf}:ext FGAS:row {k+1}:col RADIUS (for M_gas(<R500))')
            add('MGAS', p32(gh.data['MGAS'][k]), 'Msun', f'allfiles.tar.gz:{gf}:ext FGAS:row {k+1}:col MGAS (for M_gas(<R500))')
        mstar500 = 0.39 * M500 ** (-0.84) * mgas500
        mstar = mstar500 * nfw_shape(r_kpc / rs) / nfw_shape(R500 / rs)
        notes.append('stars modelled (D-022 item 3)')
        x500 = r_kpc / R500h
        if not (0.145 <= x500 <= 1.38):
            notes.append(f'r/R500={x500:.4f} outside D-023 cut 0.145-1.38')
    else:
        sf = f'{c}/{c}_mstar.fits'
        sd = fits.open(f'{EXTRACT}/{sf}')['MSTAR_SMOOTHED'].data
        rsg = np.array(sd['RADIUS'], float)
        msg = np.array(sd['MSTAR'], float)
        mstar, (a, b) = loglog_interp(r_kpc, rsg, msg)
        for k in sorted({a, b}):
            add('RADIUS', p32(sd['RADIUS'][k]), 'kpc', f'allfiles.tar.gz:{sf}:ext MSTAR_SMOOTHED:row {k+1}:col RADIUS')
            add('MSTAR', p32(sd['MSTAR'][k]), 'M_sun', f'allfiles.tar.gz:{sf}:ext MSTAR_SMOOTHED:row {k+1}:col MSTAR')
        notes.append('stars measured (MSTAR_SMOOTHED)')
    g_st = G * mstar * MSUN / r_m**2
    g_bar = g_gas + g_st
    notes.append(f'g_gas={g_gas:.6e}; g_stars={g_st:.6e}')
    vals.append([mid, f'{g_obs:.6e}', f'{g_bar:.6e}', status, '; '.join(notes)])

with open(f'{OUT}/values.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['measurement_id', 'g_obs', 'g_bar', 'status', 'notes'])
    w.writerows(vals)
with open(f'{OUT}/inputs.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['measurement_id', 'input', 'value', 'unit', 'locator'])
    w.writerows(inps)
print(len(vals), 'rows;', len(inps), 'inputs')
