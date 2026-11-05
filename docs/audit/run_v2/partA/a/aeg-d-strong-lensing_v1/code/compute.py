"""Reader A audit, stratum aeg-d-strong-lensing_v1.

Follows only the written method (methods_page.txt, REPRODUCTION.md,
A6S_PRECEDENCE.md, descriptor.json):
  g_obs = G M_E / R_E^2 ; g_bar = G (M* + M_gas)(<R_E) / R_E^2
  M_E = theta_E^2 c^2 D_s D_l / (4 G D_ls) where only theta_E is printed
  R_E = theta_E D_l in the source's cosmology
  M*(<R_E) = M*_tot x f(<R_E) (Sersic projected fraction) where only a total is printed
  M_gas = 0.12 % of M*(<R_E) (registered term a6s_gas_in_RE, hot; cold default 0; descriptor.json)

The method text states no numerical value for G, c, the solar mass in kg, or
the kpc/Mpc in metres. Per the brief, those constants are not taken from
elsewhere, so g_obs and g_bar cannot be computed: status "method incomplete".
This script computes only the constant-free intermediate quantities
(M_E where printed, f(<R_E), M*(<R_E), M_bar(<R_E), and M_E / M_bar where both
masses are available without constants), reported in notes.
"""
import csv
from scipy.special import gammainc, gammaincinv

GAS_FRAC_HOT = 0.0012  # descriptor.json x_baryon_inventory, hot gas default
GAS_FRAC_COLD = 0.0     # descriptor.json, cold component default


def sersic_fraction(R, Re, n):
    """Projected light fraction inside R for a Sersic profile:
    f = P(2n, b_n (R/Re)^(1/n)), with b_n defined by P(2n, b_n) = 1/2."""
    bn = gammaincinv(2 * n, 0.5)
    return gammainc(2 * n, bn * (R / Re) ** (1.0 / n))


rows = []

# ---- SLACS (observed R5, stellar R13) ----
# theta_E = bSIE (VizieR J/ApJ/682/964 table5); z from table4; MChaBC2 from J/A+A/501/461 lens
slacs = {
    "m000001": ("J0029-0055", 0.96, 0.2270, 0.9313, 5),
    "m000087": ("J2238-0754", 1.27, 0.1371, 0.7126, 5),
    "m000093": ("J2321-0939", 1.60, 0.0819, 0.5324, 6),
    "m000013": ("J0728+3835", 1.25, 0.2058, 0.6877, 6),
}
for mid, (name, bsie, zl, zs, mcha2) in slacs.items():
    mstar = mcha2 * 1e10
    mbar = mstar * (1 + GAS_FRAC_HOT + GAS_FRAC_COLD)
    rows.append((mid, name, None, mstar, mbar, None,
                 "M_E from theta_E needs c and G; R_E needs c (D_l from H0); not stated in method"))

# ---- S4TM (observed R10, stellar R10) ----
# b_SIE, log MEin, log M*Chab: Table 2; R_eff (intermediate axis, de Vaucouleurs): Table 1
s4tm = {
    "m000099": ("J0753+3416", 1.23, 11.05, 11.23, 1.89),
    "m000114": ("J1101+1523", 1.18, 11.23, 11.23, 0.89),
    "m000109": ("J1040+3626", 0.59, 10.54, 10.99, 1.30),
    "m000122": ("J1330+1750", 1.01, 11.32, 11.74, 2.85),
    "m000100": ("J0754+1927", 1.04, 10.99, 11.13, 1.46),
}
for mid, (name, b, lme, lms, reff) in s4tm.items():
    me = 10 ** lme
    f = sersic_fraction(b, reff, 4.0)
    mstar = 10 ** lms * f
    mbar = mstar * (1 + GAS_FRAC_HOT + GAS_FRAC_COLD)
    rows.append((mid, name, me, mstar, mbar, f,
                 "R_E = theta_E D_l needs c (and kpc in m); G not stated"))

# ---- SNL-0 ESO 325-G004 (observed R28, stellar R26) ----
me = 1.50e11                       # Smith & Lucey 2013, Table 3, M_Ein^MFL
mstar = 2.84e10 * 4.04             # Newman et al. 2017 Table 1: L_r,Ein x (M*/L_r)_MW (Kroupa)
mbar = mstar * (1 + GAS_FRAC_HOT + GAS_FRAC_COLD)
rows.append(("m000140", "ESO 325-G004 (SNL-0)", me, mstar, mbar, None,
             "R_E printed 1.96 kpc (R28 Fig.1 caption) / 0.687 kpc/arcsec; G and kpc-in-m not stated"))

out = "/home/claude/audit_v2/readers/a/aeg-d-strong-lensing_v1/code/intermediates.csv"
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["measurement_id", "system", "M_E_Msun", "Mstar_in_RE_Msun",
                "Mbar_in_RE_Msun", "f_lt_RE", "ME_over_Mbar", "missing"])
    for mid, name, me, ms, mb, f, miss in rows:
        ratio = me / mb if me is not None else None
        w.writerow([mid, name,
                    "" if me is None else f"{me:.6e}", f"{ms:.6e}", f"{mb:.6e}",
                    "" if f is None else f"{f:.6f}",
                    "" if ratio is None else f"{ratio:.6f}", miss])
print(open(out).read())
