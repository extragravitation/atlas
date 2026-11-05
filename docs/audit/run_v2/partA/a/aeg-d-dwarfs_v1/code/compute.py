"""Reader A, stratum aeg-d-dwarfs_v1: compute g_obs and g_bar following the written method
(REPRODUCTION.md 'Inputs and rules'; methods page).

  D        = 10**(mu/5 + 1) pc                         (definition of distance modulus)
  a [pc]   = a [rad] * D                                (small-angle; method does not say)
  R_h      = a * sqrt(1 - eps)                          (method, D-048 item 2)
  r_half   = 4/3 R_h                                    (method, D-025)
  g_obs    = 3 sigma^2 / r_half                         (method, D-025)
  M_V      = m_V,0 - mu ; L_V = 10**(-0.4 (M_V - M_V,sun)), M_V,sun = 4.85 read in MvdM05 (method: 'read at source')
  Upsilon  = MvdM05 (M/L)_1, MW GCs, linear in [Fe/H], floor below lowest (upsilon_v.py)
  g_bar    = G (1/2 L_V Upsilon + M_gas(<r_half)) / r_half^2 ; M_gas = 0 for a Putman 5 sigma limit ('absent (measured limit)')

The method states NO value for G, for the parsec in metres, or for the solar mass in kg.
values.csv therefore carries status 'method incomplete' with g_obs and g_bar left empty.
The supplementary file values_declared_constants.csv gives the numbers with constants
DECLARED HERE (not from the method), for the coordinator's information only.
"""
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upsilon_v import mw_table, upsilon  # noqa: E402

BASE = "/home/claude/audit_v2"
VOT = f"{BASE}/packets/aeg-d-dwarfs_v1/sources/mvdm05/J_ApJS_161_304_clusters.vot"
OUT = f"{BASE}/readers/a/aeg-d-dwarfs_v1"

MV_SUN = 4.85  # read at source: McLaughlin & van der Marel 2005 p.22 (method says read at source)

# ---- constants NOT given by the method (declared, supplementary only) ----
G_DECL = 6.67430e-11            # m3 kg-1 s-2, CODATA 2018
PC_DECL = 3.0856775814913673e16  # m, IAU 2015 B2 (exact)
MSUN_DECL = 1.988409870698051e30  # kg, IAU 2015 nominal GM_sun / CODATA 2018 G
ARCMIN = math.pi / (180 * 60)

xs, pts = mw_table(VOT)


def dist_pc(mu):
    return 10 ** (mu / 5 + 1)


# Per-row parsed inputs (from inputs_table.py values) and the choices made where the method is silent.
# feh_choice: (value, provenance, within_method?)
R = {}
R["aeg-d-dwarfs/v1/m000003"] = dict(name="Andromeda III", sigma=9.3, a_arcmin=2.0, eps=0.59, mu=24.29, mV=14.8,
                                    feh=(-1.75, "LVDB index metallicity_spectroscopic (ref Kirby2020); original not in packet", False))
R["aeg-d-dwarfs/v1/m000007"] = dict(name="Andromeda IX", sigma=10.9, a_arcmin=2.0, eps=0.00, mu=24.23, mV=15.6,
                                    feh=(-2.03, "LVDB index metallicity_spectroscopic (ref Wojno2020); original not in packet", False))
R["aeg-d-dwarfs/v1/m000010"] = dict(name="Andromeda XII", sigma=4.0, a_arcmin=1.8, eps=0.61, mu=24.28, mV=17.7,
                                    feh=(-2.2, "Collins 2013 Table 4 [Fe/H]spec (dispersion paper)", True), limit=True)
R["aeg-d-dwarfs/v1/m000012"] = dict(name="Andromeda XV", sigma=4.0, a_arcmin=1.3, eps=0.24, mu=24.37, mV=16.0,
                                    feh=(-1.43, "LVDB index metallicity_spectroscopic (ref Wojno2020); original not in packet", False))
R["aeg-d-dwarfs/v1/m000013"] = dict(name="Andromeda XVI", sigma=3.8, a_arcmin=1.0, eps=0.29, mu=23.70, mV=16.1,
                                    feh=(-2.17, "LVDB index metallicity_photometric (ref Fu2024); no spectroscopic value indexed", False))
R["aeg-d-dwarfs/v1/m000020"] = dict(name="Andromeda XXIII", sigma=7.1, a_arcmin=5.4, eps=0.41, mu=24.36, mV=14.6,
                                    feh=(-2.2, "Collins 2013 Table 4 [Fe/H]spec (dispersion paper)", True))
# Draco II: M_V given directly; m_V = M_V + mu, then M_V = m_V - mu (identity)
R["aeg-d-dwarfs/v1/m000036"] = dict(name="Draco II", sigma=2.6, a_arcmin=3.0, eps=0.23, mu=16.67, mV=-0.8 + 16.67,
                                    feh=(-2.94, "Cerny 2026 Table 4 [Fe/H]model (dispersion paper); column choice not specified, all columns < -2.29 so same Upsilon", True),
                                    limit=True)
# CVn II: m_V = MV(Munoz) + 5 log10(D_Munoz/10 pc), D_Munoz = 160.0 kpc; mu from Greco 2008
R["aeg-d-dwarfs/v1/m000031"] = dict(name="Canes Venatici II", sigma=5.28, a_arcmin=1.51, eps=0.46, mu=21.02,
                                    mV=-5.17 + 5 * math.log10(160.0e3 / 10),
                                    feh=(-2.85, "LVDB index (ref Geha 2026 arXiv); Geha 2026 prints per-star [Fe/H] only, no system value", False))
# Leo I: mu = midpoint of 22.06 and 22.25 (locator); m_V = MV(Munoz) + 5 log10(254.0 kpc/10 pc)
R["aeg-d-dwarfs/v1/m000042"] = dict(name="Leo I", sigma=9.9, a_arcmin=3.30, eps=0.30, mu=(22.06 + 22.25) / 2,
                                    mV=-11.78 + 5 * math.log10(254.0e3 / 10),
                                    feh=(-1.31, "Koch 2007 median [Fe/H] on CG97 scale (dispersion paper); ZW84 value -1.61 also printed", True))
# Tucana: Re = 205 pc at (m-M)0 = 24.69 -> angle; distance mu = 24.74 (Bernard); m_V = MV + 24.69
D_SAV = dist_pc(24.69)
R["aeg-d-dwarfs/v1/m000059"] = dict(name="Tucana", sigma=14.4, a_arcmin=(205.0 / D_SAV) / ARCMIN, eps=0.48, mu=24.74,
                                    mV=-9.55 + 24.69,
                                    feh=(-1.58, "Taibi 2020 Table 1 (in packet; LVDB spectroscopic ref); Gregory 2019 gives no [Fe/H] of its own", False),
                                    geometric_Re=True)


def compute(r, circularise=True):
    D = dist_pc(r["mu"])
    a_pc = r["a_arcmin"] * ARCMIN * D
    Rh = a_pc * math.sqrt(1 - r["eps"]) if circularise else a_pc
    rhalf_pc = 4.0 / 3.0 * Rh
    MV = r["mV"] - r["mu"]
    LV = 10 ** (-0.4 * (MV - MV_SUN))
    ups, flag, br = upsilon(r["feh"][0], xs, pts)
    Mstar = 0.5 * LV * ups  # Msun inside r_half
    rhalf_m = rhalf_pc * PC_DECL
    g_obs = 3 * (r["sigma"] * 1e3) ** 2 / rhalf_m
    g_bar = G_DECL * Mstar * MSUN_DECL / rhalf_m ** 2
    return dict(D_pc=D, a_pc=a_pc, Rh_pc=Rh, rhalf_pc=rhalf_pc, MV=MV, LV=LV, ups=ups, ups_flag=flag,
                ups_rows=br, g_obs=g_obs, g_bar=g_bar)


def main():
    ids = [row["measurement_id"] for row in csv.DictReader(open(f"{BASE}/packets/aeg-d-dwarfs_v1/rows.csv"))]
    common = ("method does not state G, the parsec in metres, or the solar mass in kg (needed to express g_obs and g_bar in m s-2 "
              "from sigma in km s-1, radii in pc and masses in Msun)")
    with open(f"{OUT}/values.csv", "w", newline="") as f, open(f"{OUT}/values_declared_constants.csv", "w", newline="") as g:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["measurement_id", "g_obs", "g_bar", "status", "notes"])
        w2 = csv.writer(g, lineterminator="\n")
        w2.writerow(["measurement_id", "system", "g_obs", "g_bar", "D_pc", "a_pc", "R_h_pc", "r_half_pc", "M_V", "L_V_Lsun",
                     "Upsilon_V", "Upsilon_flag", "Fe_H_used", "Fe_H_provenance", "Fe_H_within_method", "alt_g_obs_no_circularisation",
                     "alt_g_bar_no_circularisation", "notes"])
        for mid in ids:
            r = R[mid]
            c = compute(r)
            extra = []
            if r.get("limit"):
                extra.append("limit")
            if not r["feh"][2]:
                extra.append("[Fe/H] source for Upsilon_V not determinable from method/locator (D-057 not supplied)")
            if r.get("geometric_Re"):
                extra.append("Saviane Re is a geometric (already circularised) radius, method assumes a semi-major a")
            if mid.endswith("m000042"):
                extra.append("[Fe/H] scale (CG97 -1.31 vs ZW84 -1.61) not specified")
            if mid.endswith("m000059"):
                extra.append("sigma: paper adopts 14.4 (36 stars) after removing one star; full sample 16.6; D-038 2B 'whole sample' not supplied")
            if mid.endswith("m000010"):
                extra.append("sigma printed 0.0+4.0 (unresolved, 1-sigma upper bound) taken as limit 4.0")
            note = "; ".join([common] + extra)
            w.writerow([mid, "", "", "method incomplete", note])
            alt = compute(r, circularise=False)
            w2.writerow([mid, r["name"], f"{c['g_obs']:.6e}", f"{c['g_bar']:.6e}", f"{c['D_pc']:.6e}", f"{c['a_pc']:.6g}",
                         f"{c['Rh_pc']:.6g}", f"{c['rhalf_pc']:.6g}", f"{c['MV']:.4f}", f"{c['LV']:.6e}", f"{c['ups']:.4f}",
                         c["ups_flag"], r["feh"][0], r["feh"][1], r["feh"][2],
                         f"{alt['g_obs']:.6e}", f"{alt['g_bar']:.6e}", "; ".join(extra)])
            print(mid, r["name"], f"g_obs={c['g_obs']:.4e} g_bar={c['g_bar']:.4e} ratio={c['g_obs']/c['g_bar']:.2f}",
                  f"rhalf={c['rhalf_pc']:.1f}pc Ups={c['ups']:.3f}{(' '+c['ups_flag']) if c['ups_flag'] else ''}")


if __name__ == "__main__":
    main()
