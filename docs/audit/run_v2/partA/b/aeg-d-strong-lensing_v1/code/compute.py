"""Reader B audit, stratum aeg-d-strong-lensing_v1.

Follows the written method (REPRODUCTION.md, A6S_PRECEDENCE.md, descriptor.json):
  M_E   = printed, or theta_E^2 c^2 D_s D_l / (4 G D_ls) in the source's cosmology
  R_E   = theta_E * D_l (flat FRW, source cosmology)
  M*    = printed inside R_E, or M*_tot * f(<R_E) (Sersic/de Vaucouleurs light fraction)
  M_gas = 0.0012 * M*(<R_E) (hot, registered default; cold default 0) -- descriptor.json
  g_obs = G M_E / R_E^2 ; g_bar = G (M* + M_gas) / R_E^2

The method states no numerical value for G, c, the solar mass, the parsec/kpc, or the
arcsec->rad conversion is pure maths. Per the brief, constants may only come from the
method text, so g_obs and g_bar are NOT written to values.csv (status 'method incomplete').
For diagnostics only, the script also evaluates the same formulas with
CONDITIONAL constants (astropy CODATA2018 / IAU2015) and prints them to
conditional_values.csv. These are not method-sourced.
"""
import csv, math, os, sys
from scipy.integrate import quad
from scipy.special import gammainc
from scipy.optimize import brentq

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- conditional constants (NOT from the method) ----
from astropy import constants as const, units as u
G = const.G.si.value            # m^3 kg^-1 s^-2 (CODATA 2018)
C = const.c.si.value            # m/s
MSUN = const.M_sun.si.value     # kg (IAU 2015 nominal)
MPC = u.Mpc.to(u.m)
KPC = u.kpc.to(u.m)
ARCSEC = math.pi / (180 * 3600)


def dc_mpc(z, H0, Om):
    OL = 1.0 - Om  # flat, radiation neglected
    I, _ = quad(lambda x: 1.0 / math.sqrt(Om * (1 + x) ** 3 + OL), 0, z)
    return (C / 1e3) / H0 * I  # Mpc


def dists(zl, zs, H0, Om):
    dl_c = dc_mpc(zl, H0, Om)
    Dl = dl_c / (1 + zl)
    if zs is None:
        return Dl, None, None
    ds_c = dc_mpc(zs, H0, Om)
    Ds = ds_c / (1 + zs)
    Dls = (ds_c - dl_c) / (1 + zs)
    return Dl, Ds, Dls


def b_n(n):
    return brentq(lambda b: gammainc(2 * n, b) - 0.5, 1e-6, 50)


def sersic_frac(R, Re, n):
    return gammainc(2 * n, b_n(n) * (R / Re) ** (1.0 / n))


COSMO = {
    "R5": (70.0, 0.3),          # 0805.1931v1 p.2 Sec.1: OmegaM=0.3, OmegaL=0.7, H0=70
    "R10": (70.0, 0.274),       # 1711.00072v2 Sec.1: Om=0.274, OL=0.726, H0=70
    "R28": (70.4, 0.272),       # 1306.4983v1 Sec.1: WMAP7 H0=70.4, Om=0.272, OL=0.728
}

GAS_FRAC = 0.0012  # descriptor.json x_baryon_inventory hot gas: 0.12% of M*(<R_E); cold default 0

rows = []
# SLACS: observed R5 (theta_E=bSIE table5, zFG/zBG table4); stellar R13 MChaBC2 (1e10 Msun, inside R_Ein)
slacs = {
    "aeg-d-strong-lensing/v1/m000001": ("J0029-0055", 0.96, 0.2270, 0.9313, 5),
    "aeg-d-strong-lensing/v1/m000087": ("J2238-0754", 1.27, 0.1371, 0.7126, 5),
    "aeg-d-strong-lensing/v1/m000093": ("J2321-0939", 1.60, 0.0819, 0.5324, 6),
    "aeg-d-strong-lensing/v1/m000013": ("J0728+3835", 1.25, 0.2058, 0.6877, 6),
}
for mid, (name, th, zl, zs, mch) in slacs.items():
    H0, Om = COSMO["R5"]
    Dl, Ds, Dls = dists(zl, zs, H0, Om)
    thr = th * ARCSEC
    ME_kg = thr ** 2 * C ** 2 * (Ds * MPC) * (Dl * MPC) / (4 * G * Dls * MPC)
    RE_m = thr * Dl * MPC
    Ms_kg = mch * 1e10 * MSUN
    rows.append((mid, name, ME_kg / MSUN, RE_m / KPC, mch * 1e10, None, RE_m, ME_kg, Ms_kg))

# S4TM: R10 table2 b_SIE, log M_Ein, log M*^Chab (total); table1 z_L, R_eff (deV, intermediate axis)
s4tm = {
    "aeg-d-strong-lensing/v1/m000099": ("J0753+3416", 1.23, 11.05, 11.23, 0.1371, 1.89),
    "aeg-d-strong-lensing/v1/m000114": ("J1101+1523", 1.18, 11.23, 11.23, 0.1780, 0.89),
    "aeg-d-strong-lensing/v1/m000109": ("J1040+3626", 0.59, 10.54, 10.99, 0.1225, 1.30),
    "aeg-d-strong-lensing/v1/m000122": ("J1330+1750", 1.01, 11.32, 11.74, 0.2074, 2.85),
    "aeg-d-strong-lensing/v1/m000100": ("J0754+1927", 1.04, 10.99, 11.13, 0.1534, 1.46),
}
for mid, (name, th, lME, lMs, zl, Reff) in s4tm.items():
    H0, Om = COSMO["R10"]
    Dl, _, _ = dists(zl, None, H0, Om)
    RE_m = th * ARCSEC * Dl * MPC
    f = sersic_frac(th, Reff, 4.0)
    Ms = 10 ** lMs * f
    rows.append((mid, name, 10 ** lME, RE_m / KPC, Ms, f, RE_m, 10 ** lME * MSUN, Ms * MSUN))

# SNL-0: R28 M_Ein^MFL = 1.50e11 Msun, R_Ein = 2.85 arcsec, zl = 0.0347 (CMB frame);
# stellar R26 L_r,Ein = 2.84e10 Lsun,r x (M*/L_r)_MW = 4.04 (Kroupa)
H0, Om = COSMO["R28"]
Dl, _, _ = dists(0.0347, None, H0, Om)
RE_m = 2.85 * ARCSEC * Dl * MPC
Ms = 2.84e10 * 4.04
rows.append(("aeg-d-strong-lensing/v1/m000140", "ESO 325-G004 (SNL-0)", 1.50e11, RE_m / KPC, Ms, None,
             RE_m, 1.50e11 * MSUN, Ms * MSUN))

with open(os.path.join(OUT, "conditional_values.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["measurement_id", "system", "M_E_Msun", "R_E_kpc", "Mstar_inRE_Msun", "f_deV",
                "g_obs_conditional", "g_bar_conditional"])
    for mid, name, ME, REk, Ms, f, RE_m, ME_kg, Ms_kg in rows:
        gobs = G * ME_kg / RE_m ** 2
        gbar = G * Ms_kg * (1 + GAS_FRAC) / RE_m ** 2
        w.writerow([mid, name, f"{ME:.6e}", f"{REk:.6f}", f"{Ms:.6e}", "" if f is None else f"{f:.6f}",
                    f"{gobs:.6e}", f"{gbar:.6e}"])
print("wrote conditional_values.csv; b_4 =", b_n(4.0))
