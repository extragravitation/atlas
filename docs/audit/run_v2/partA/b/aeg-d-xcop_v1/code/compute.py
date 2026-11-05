"""Audit reader B, stratum aeg-d-xcop_v1.

Follows the written method in method/SOURCE.md (aeg-d-xcop/v1):
  g_obs = G * M_FORW(<r) / r^2, r = hydro file RADIUS (kpc)  [bias default b = 0]
  g_bar = G * (M_gas(<r) + M_star(<r)) / r^2
  M_gas: FGAS ext, RADIUS (R/R500) * header R500 -> kpc, MGAS; interpolated
         linearly in log M vs log r
  M_star (measured): MSTAR_SMOOTHED ext, RADIUS (kpc), MSTAR; same interpolation
  M_star (modelled; A1644, A2255, A3158, A3266, RXC1825):
         M*(<r) = K [ln(1+x) - x/(1+x)], x = r/r_s, r_s = R200/2.9,
         K set so that M*(<R500) = 0.39 (M500/1e14 Msun)^-0.84 * M_gas(<R500)
         R500, M500, R200 from Ettori et al. 2019 Table 1 (arXiv:1805.00035).
  G and Msun from astropy (as the method states); kpc -> m from astropy.units.
Row locator "row N" is taken as 1-based (see notes.md).

Usage: python3 -I compute.py <packet_dir> <extract_dir> <out_dir>
"""
import csv
import sys

import numpy as np
from astropy import constants as const
from astropy import units as u
from astropy.io import fits

packet, extract, out = sys.argv[1], sys.argv[2], sys.argv[3]

G = const.G.to_value(u.m**3 / u.kg / u.s**2)
MSUN = const.M_sun.to_value(u.kg)
KPC = (1 * u.kpc).to_value(u.m)

# Ettori et al. 2019, Table 1 (arXiv e-print source mass_xcop.tex, table tab:mass)
# R500 [Mpc], M500 [1e14 Msun], R200 [Mpc], exactly as printed.
TABLE1 = {
    "A1644": ("1.054", "3.48", "1.778", 315),
    "A2255": ("1.196", "5.26", "2.033", 319),
    "A3158": ("1.123", "4.26", "1.766", 321),
    "A3266": ("1.430", "8.80", "2.325", 322),
    "RXC1825": ("1.105", "4.08", "1.719", 324),
}
MODELLED = set(TABLE1)


def loglog(x, xp, fp):
    return 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))


def nfw_shape(x):
    return np.log1p(x) - x / (1 + x)


def fmt(v):
    """Shortest repr of the stored value (FITS E = float32), i.e. the value as stored."""
    if isinstance(v, np.floating):
        return str(v)
    return str(v)


def bracket(inps, mid, xs, cols, fname, ext, rcol, mcol, rr, unit_r, unit_m):
    """Record the two tabulated rows that bracket radius rr (in the file's own units)."""
    j = int(np.searchsorted(xs, rr))
    for k in sorted({max(j - 1, 0), min(j, len(xs) - 1)}):
        loc = f"allfiles.tar.gz:{fname} ext {ext} row {k + 1}"
        inps.append((mid, rcol, fmt(cols[rcol][k]), unit_r, loc + f" col {rcol}"))
        inps.append((mid, mcol, fmt(cols[mcol][k]), unit_m, loc + f" col {mcol}"))


rows = list(csv.DictReader(open(f"{packet}/rows.csv")))
vals, inps = [], []
for row in rows:
    mid, c = row["measurement_id"], row["system_name"]
    ref = row["source_ref"]
    n = int(ref.rsplit("row", 1)[1])
    i = n - 1  # 1-based row
    hfile = f"{c}/{c}_hydro_mass.fits"
    gfile = f"{c}/{c}_fgas_profile.fits"
    sfile = f"{c}/{c}_mstar.fits"
    h = fits.open(f"{extract}/{hfile}")["HYDRO_MASS"]
    r = float(h.data["RADIUS"][i])
    mf = float(h.data["M_FORW"][i])
    inps.append((mid, "RADIUS", fmt(h.data["RADIUS"][i]), "kpc", f"allfiles.tar.gz:{hfile} ext HYDRO_MASS row {n} col RADIUS"))
    inps.append((mid, "M_FORW", fmt(h.data["M_FORW"][i]), "Msun", f"allfiles.tar.gz:{hfile} ext HYDRO_MASS row {n} col M_FORW"))

    g = fits.open(f"{extract}/{gfile}")["FGAS"]
    R500g = float(g.header["R500"])
    rg = g.data["RADIUS"].astype(float) * R500g
    mg = g.data["MGAS"].astype(float)
    inps.append((mid, "R500", fmt(g.header["R500"]), "kpc", f"allfiles.tar.gz:{gfile} ext FGAS header R500"))
    bracket(inps, mid, g.data["RADIUS"].astype(float), g.data, gfile, "FGAS", "RADIUS", "MGAS",
            r / R500g, "R/R500", "Msun")
    note = []
    in_range = rg.min() <= r <= rg.max()
    Mgas = loglog(r, rg, mg)

    if c in MODELLED:
        R500s, M500s, R200s, line = TABLE1[c]
        R500, M500, R200 = float(R500s) * 1000, float(M500s), float(R200s) * 1000
        loc = f"arXiv:1805.00035 e-print mass_xcop.tex line {line}, Table 1, row {c}"
        inps.append((mid, "R_500", R500s, "Mpc", loc + ", col R_500"))
        inps.append((mid, "M_500", M500s, "1e14 Msun", loc + ", col M_500"))
        inps.append((mid, "R_200", R200s, "Mpc", loc + ", col R_200"))
        rs = R200 / 2.9
        Mgas500 = loglog(R500, rg, mg)
        bracket(inps, mid, g.data["RADIUS"].astype(float), g.data, gfile, "FGAS", "RADIUS", "MGAS",
                R500 / R500g, "R/R500", "Msun")
        target = 0.39 * M500 ** -0.84 * Mgas500
        K = target / nfw_shape(R500 / rs)
        Mstar = K * nfw_shape(r / rs)
        x500 = r / R500
        note.append(f"modelled stars (D-022 item 3); r/R500(Table1)={x500:.4f}")
        if not (0.145 <= x500 <= 1.38):
            note.append("outside D-023 cut 0.145-1.38 R500")
    else:
        s = fits.open(f"{extract}/{sfile}")["MSTAR_SMOOTHED"]
        rs_ = s.data["RADIUS"].astype(float)
        ms = s.data["MSTAR"].astype(float)
        bracket(inps, mid, rs_, s.data, sfile, "MSTAR_SMOOTHED", "RADIUS", "MSTAR", r, "kpc", "M_sun")
        in_range = in_range and (rs_.min() <= r <= rs_.max())
        Mstar = loglog(r, rs_, ms)
        note.append("measured stars (MSTAR_SMOOTHED)")
    if not in_range:
        note.append("radius outside tabulated component range")

    rm = r * KPC
    gobs = G * mf * MSUN / rm**2
    gbar = G * (Mgas + Mstar) * MSUN / rm**2
    note.append(f"Mgas={Mgas:.5e} Msun; Mstar={Mstar:.5e} Msun; b=0 (default)")
    vals.append((mid, f"{gobs:.6e}", f"{gbar:.6e}", "ok", "; ".join(note)))

with open(f"{out}/values.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["measurement_id", "g_obs", "g_bar", "status", "notes"])
    w.writerows(vals)
with open(f"{out}/inputs.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["measurement_id", "input", "value", "unit", "locator"])
    w.writerows(inps)
print(len(vals), "rows")
