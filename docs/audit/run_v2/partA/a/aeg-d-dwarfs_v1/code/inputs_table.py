"""Inputs read at source by reader A for stratum aeg-d-dwarfs_v1.

Each entry: (measurement_id, input label as printed at source, value as printed, unit, locator).
Unicode minus signs in the PDFs are written here as ASCII '-'; digits are as printed.
Asymmetric errors are recorded as separate inputs ('<label> err+' / 'err-').
Page numbers are PDF page numbers of the arXiv e-print (they match the printed page
numbers for the arXiv preprints listed).
"""

PKT = "packets/aeg-d-dwarfs_v1/sources"
MVDM = f"{PKT}/mvdm05/J_ApJS_161_304_clusters.vot"
PUT = f"{PKT}/gas/putman2021/apjabe391t1_mrt.txt"
DL = "readers/a/aeg-d-dwarfs_v1/downloads"
MVDM_PAPER = (f"{DL}/astro-ph_0605132.pdf (arXiv:astro-ph/0605132, McLaughlin & van der Marel 2005) "
              "p.22, Sec. 4 bullet on log I0: 'corresponds to a solar absolute magnitude MV,sun = +4.85'")

T12 = "papers/Tollerud2012ApJ...752...45T.pdf p.9, Table 3 (Summary of M31 dSph properties)"
C13 = "papers/Collins2013ApJ...768..172C.pdf p.27, Table 4 (Kinematic properties of Andromeda dSph galaxies)"
M16T1 = "papers/Martin2016ApJ...833..167M.pdf p.9, Table 1 (Derived structural parameters of the dwarf galaxies)"
M16T2 = "papers/Martin2016ApJ...833..167M.pdf p.9, Table 2 (Derived luminosity-related properties of the dwarf galaxies)"
S22 = "papers/Savino2022ApJ...938..101S.pdf p.15, Table 5"
MZ18_T1 = "papers/Munoz2018ApJ...860...66M.pdf p.22, Table 1 (Adopted and Derived Parameters), Primary Sample"
MZ18_T5 = "papers/Munoz2018ApJ...860...66M.pdf p.27, Table 5 (Measured Structural Parameters: Sersic Models), Primary Sample"
MZ18_T6 = "papers/Munoz2018ApJ...860...66M.pdf p.28, Table 6 (Derived Parameters: Magnitude, Luminosity and Surface Brightness), Primary Sample"

ROWS = []


def add(mid, label, value, unit, loc):
    ROWS.append((mid, label, value, unit, loc))


def m31(mid, name, sig_src, sigma, sig_errs, eps, eps_errs, rh, rh_errs, mu, mu_errs, mu_loc, mv, mv_errs):
    if sig_src == "T12":
        add(mid, "sigma_LOS", sigma, "km s-1", f"{T12}, row {name}, col sigma_LOS (9)")
    else:
        add(mid, "sigma_v", sigma, "km s-1", f"{C13}, row {name}, col sigma_v")
    for k, v in sig_errs:
        add(mid, f"sigma {k}", v, "km s-1", "same cell")
    add(mid, "epsilon", eps, "dimensionless (1-b/a)", f"{M16T1}, row {name}, col epsilon")
    for k, v in eps_errs:
        add(mid, f"epsilon {k}", v, "", "same cell")
    add(mid, "rh", rh, "arcmin (semi-major; elliptical radius, Martin 2016 eqs. 3 and 5)", f"{M16T1}, row {name}, col rh (arcmin)")
    for k, v in rh_errs:
        add(mid, f"rh {k}", v, "arcmin", "same cell")
    add(mid, "mu" if "Savino" in mu_loc else "mu0 (PWR)", mu, "mag", mu_loc)
    for k, v in mu_errs:
        add(mid, f"mu {k}", v, "mag", "same cell")
    add(mid, "mV,0", mv, "mag (extinction-corrected apparent V)", f"{M16T2}, row {name}, col mV,0")
    for k, v in mv_errs:
        add(mid, f"mV,0 {k}", v, "mag", "same cell")


# ---- Andromeda XV (m000012)
m31("aeg-d-dwarfs/v1/m000012", "And XV", "T12", "4.0", [("err+-", "1.4")], "0.24", [("err+-", "0.10")],
    "1.3", [("err+-", "0.1")], "24.37", [("err+-", "0.05")], f"{S22}, row And XV, col mu", "16.0", [("err+-", "0.3")])
# ---- Andromeda IX (m000007)
m31("aeg-d-dwarfs/v1/m000007", "And IX", "T12", "10.9", [("err+-", "2.0")], "0.00", [("err+", "0.16"), ("err-", "0.00")],
    "2.0", [("err+", "0.3"), ("err-", "0.2")], "24.23", [("err+-", "0.06")], f"{S22}, row And IX, col mu", "15.6", [("err+-", "0.3")])
# ---- Andromeda XVI (m000013)
m31("aeg-d-dwarfs/v1/m000013", "And XVI", "T12", "3.8", [("err+-", "2.9")], "0.29", [("err+-", "0.08")],
    "1.0", [("err+-", "0.1")], "23.70", [("err+-", "0.08 (0.09)")],
    "papers/MartinezVazquez2017ApJ...850..137M.pdf p.18, Table 8, row And XVI, col PWR (the paper's adopted distances: p.17 'We adopt the distances obtained with the PWR')",
    "16.1", [("err+-", "0.3")])
# ---- Andromeda III (m000003)
m31("aeg-d-dwarfs/v1/m000003", "And III", "T12", "9.3", [("err+-", "1.4")], "0.59", [("err+-", "0.04")],
    "2.0", [("err+-", "0.2")], "24.29", [("err+-", "0.05")], f"{S22}, row And III, col mu", "14.8", [("err+-", "0.2")])
# ---- Andromeda XXIII (m000020)
m31("aeg-d-dwarfs/v1/m000020", "And XXIII", "C13", "7.1", [("err+-", "1.0")], "0.41", [("err+", "0.05"), ("err-", "0.06")],
    "5.4", [("err+-", "0.4")], "24.36", [("err+-", "0.07")], f"{S22}, row And XXIII, col mu", "14.6", [("err+-", "0.2")])
add("aeg-d-dwarfs/v1/m000020", "[Fe/H]spec", "-2.2", "dex", f"{C13}, row And XXIII, col [Fe/H]spec (err 0.3)")
# ---- Andromeda XII (m000010)
m31("aeg-d-dwarfs/v1/m000010", "And XII", "C13", "0.0", [("err+", "4.0"), ("err-", "(none printed)")], "0.61", [("err+", "0.16"), ("err-", "0.48")],
    "1.8", [("err+", "1.2"), ("err-", "0.7")], "24.28", [("err+", "0.08"), ("err-", "0.07")], f"{S22}, row And XII, col mu", "17.7", [("err+-", "0.5")])
add("aeg-d-dwarfs/v1/m000010", "sigma_v note", "unresolved; upper bound is the formal 1 sigma uncertainty", "",
    "papers/Collins2013ApJ...768..172C.pdf p.40, App. B.4: 'an unresolved velocity dispersion of sigma_v = 0.0+4.0 km s-1, where the upper bound represents the formal 1 sigma uncertainty'")
add("aeg-d-dwarfs/v1/m000010", "[Fe/H]spec", "-2.2", "dex", f"{C13}, row And XII, col [Fe/H]spec (err 0.2)")

# ---- Draco II (m000036)
M = "aeg-d-dwarfs/v1/m000036"
CER_T3 = "papers/Cerny2026arXiv260217652C.pdf p.38, Table 3 (Dynamical Properties of the UFCSs), row Draco II"
add(M, "sigma_v", "< 2.6", "km s-1 (95% credible upper limit, table note)", f"{CER_T3}, col sigma_v")
L18 = "papers/Longeard2018MNRAS.480.2609L.pdf p.8, Table 1 (Inferred properties of Dra II)"
add(M, "rh", "3.0", "arcmin (half-light radius along the major axis, p.5 Sec. 3)", f"{L18}, row rh (arcmin), Favoured model")
add(M, "rh err+", "0.7", "arcmin", "same row")
add(M, "rh err-", "0.5", "arcmin", "same row")
add(M, "epsilon", "0.23", "dimensionless (1-b/a)", f"{L18}, row ellipticity (symbol not rendered in text layer; between theta and Distance modulus), Favoured model")
add(M, "epsilon err+-", "0.15", "", "same row")
add(M, "Distance modulus", "16.67", "mag", f"{L18}, row Distance modulus")
add(M, "Distance modulus err+-", "0.05", "mag", "same row")
add(M, "MV", "-0.8", "mag", f"{L18}, row MV")
add(M, "MV err+", "0.4", "mag", "same row")
add(M, "MV err-", "1.0", "mag", "same row")
add(M, "[Fe/H]model", "-2.94", "dex", "papers/Cerny2026arXiv260217652C.pdf p.40, Table 4 (Metallicity Properties), row Draco II, col [Fe/H]model (+0.32 -0.39); same table also gives [Fe/H]w.avg. -2.74 and [Fe/H]brightest -2.49")

# ---- Canes Venatici II (m000031)
M = "aeg-d-dwarfs/v1/m000031"
add(M, "sigma", "5.28", "km s-1 (stars inside 2*Reff, MRT note 4)",
    "papers/Geha2026ApJ...999..140G.pdf p.32, Table A1, row CVn II, col 14; same in sources/members/geha2026/apjae290dt1_mrt.txt line 56, bytes 85-91")
add(M, "e_sigma", "0.96", "km s-1", "same row, col 15 / MRT bytes 93-99")
add(M, "E_sigma", "1.25", "km s-1", "same row, col 16 / MRT bytes 101-107")
add(M, "re,s", "1.51", "arcmin", f"{MZ18_T5}, row 26 CVn II, col re,s (arcmin)")
add(M, "re,s err+-", "0.23", "arcmin", "same cell")
add(M, "epsilon_s", "0.46", "dimensionless", f"{MZ18_T5}, row 26 CVn II, col epsilon_s (not named in locator; same table row)")
add(M, "epsilon_s err+-", "0.11", "", "same cell")
add(M, "mu0", "21.02", "mag", "papers/Greco2008ApJ...675L..73G.pdf p.7, Sec. 5 'the distance modulus of CVn II is 21.02 +- 0.06 mag'")
add(M, "mu0 err+-", "0.06", "mag", "same sentence")
add(M, "MV", "-5.17", "mag", f"{MZ18_T6}, row 26 CVn II, col MV")
add(M, "MV err+-", "0.32", "mag", "same cell")
add(M, "R", "160.0", "kpc", f"{MZ18_T1}, row 26 CVn II, col R (kpc)")
add(M, "[Fe/H] (not used: Munoz Table 1 literature value)", "-2.12", "dex", f"{MZ18_T1}, row 26 CVn II, col [Fe/H]; recorded only, see notes")

# ---- Leo I (m000042)
M = "aeg-d-dwarfs/v1/m000042"
add(M, "dispersion (combined GMOS plus DEIMOS)", "9.9", "km s-1",
    "downloads/astro-ph_0611372.pdf (Koch et al. 2007, ApJ 657, 241) p.5, Sec. 3: 'a dispersion of 9.9 +-1.5 km s-1 from the combined GMOS plus DEIMOS sample'")
add(M, "dispersion err+-", "1.5", "km s-1", "same sentence")
add(M, "re,s", "3.30", "arcmin", f"{MZ18_T5}, row 16 Leo I, col re,s (arcmin)")
add(M, "re,s err+-", "0.03", "arcmin", "same cell")
add(M, "epsilon_s", "0.30", "dimensionless", f"{MZ18_T5}, row 16 Leo I, col epsilon_s (not named in locator; same table row)")
add(M, "epsilon_s err+-", "0.01", "", "same cell")
add(M, "mu0 ([Fe/H]=-1.43)", "22.06", "mag", "papers/Stetson2014PASP..126..616S.pdf p.11, Sec. 5: 'the two distance moduli turn out to be mu0 = 22.06 +- 0.08 and 22.25 +- 0.07 mag'")
add(M, "mu0 ([Fe/H]=-1.43) err+-", "0.08", "mag", "same sentence")
add(M, "mu0 ([Fe/H]=-2.15)", "22.25", "mag", "same sentence")
add(M, "mu0 ([Fe/H]=-2.15) err+-", "0.07", "mag", "same sentence")
add(M, "MV", "-11.78", "mag", f"{MZ18_T6}, row 16 Leo I, col MV")
add(M, "MV err+-", "0.28", "mag", "same cell")
add(M, "R", "254.0", "kpc", f"{MZ18_T1}, row 16 Leo I, col R (kpc)")
add(M, "median [Fe/H] (CG97 scale)", "-1.31", "dex",
    "downloads/astro-ph_0611372.pdf p.12, Sec. 8.2: 'median metallicity of -1.31 +- 0.02 dex on the scale of CG97 ... (-1.61 on the scale of Zinn & West 1984)'")
add(M, "median [Fe/H] (ZW84 scale)", "-1.61", "dex", "same sentence")

# ---- Tucana (m000059)
M = "aeg-d-dwarfs/v1/m000059"
add(M, "sigma_v,Tuc", "14.4", "km s-1",
    "downloads/1902.07228.pdf (Gregory et al. 2019, arXiv v2) p.8, Sec. 3: 'Removing object 37852 reduces the velocity dispersion to sigma_v,Tuc = 14.4+2.8-2.3 km s-1'; also abstract p.1 and conclusions")
add(M, "sigma_v,Tuc err+", "2.8", "km s-1", "same")
add(M, "sigma_v,Tuc err-", "2.3", "km s-1", "same")
add(M, "sigma_v,Tuc (all 37 members, not adopted by the paper)", "16.6", "km s-1", "downloads/1902.07228.pdf p.7: 'a velocity dispersion of sigma_v,Tuc = 16.6+3.1-2.6'; recorded only")
add(M, "Re (pc)", "205", "pc (effective GEOMETRIC radius, p.10: 'The effective geometric radius Re')",
    "downloads/astro-ph_9601165.pdf (Saviane et al. 1996) p.9, Table 5 (Structural parameters for Tucana), row Re (pc)")
add(M, "Re (pc) err+-", "32", "pc", "same")
add(M, "1 - b/a", "0.48", "dimensionless", "downloads/astro-ph_9601165.pdf p.9, Table 5, row 1 - b/a")
add(M, "1 - b/a err+-", "0.03", "", "same")
add(M, "(m - M)0 (Saviane TRGB)", "24.69", "mag", "downloads/astro-ph_9601165.pdf p.1 abstract '(m - M)0 = 24.69 +- 0.16'; p.7 Sec. 4 '(m - M) = 24.69 +- 0.16'")
add(M, "(m - M)0 (Saviane TRGB) err+-", "0.16", "mag", "same")
add(M, "(m-M)0,Tuc (Bernard RR Lyrae)", "24.74", "mag", "downloads/0904.4463.pdf (Bernard et al. 2009) p.19, Sec. 6.3: 'we adopt reddening-corrected distance moduli of 24.46+-0.12 and 24.74+-0.12' (Cetus, Tucana)")
add(M, "(m-M)0,Tuc err+-", "0.12", "mag", "same")
add(M, "MV", "-9.55", "mag", "downloads/astro-ph_9601165.pdf p.9, Table 5, row MV")
add(M, "MV err+-", "0.27", "mag", "same")
add(M, "VT (recorded, not used)", "15.15", "mag", "downloads/astro-ph_9601165.pdf p.9, Table 5, row VT")
add(M, "[Fe/H] (Taibi 2020; supplementary only, not named by method or locator)", "-1.58", "dex",
    "papers/Taibi2020A&A...635A.152T.pdf p.3, Table 1, row [Fe/H] (ref 4 = this work)")

# ---- common inputs (written once per row for the comparison script)
COMMON = []
for mid in sorted({r[0] for r in ROWS}):
    COMMON.append((mid, "MV,sun", "+4.85", "mag", MVDM_PAPER))
ROWS.extend(COMMON)

# Putman et al. 2021 Table 1 MRT, HI mass limits
PUTMAN = {
    "aeg-d-dwarfs/v1/m000059": ("Tucana", 185, "< 8.5E+04"),
    "aeg-d-dwarfs/v1/m000012": ("Andromeda XV", 151, "< 4.1E+04"),
    "aeg-d-dwarfs/v1/m000007": ("Andromeda IX", 168, "< 5.5E+04"),
    "aeg-d-dwarfs/v1/m000036": ("Draco II", 86, "< 57"),
    "aeg-d-dwarfs/v1/m000013": ("Andromeda XVI", 148, "< 2.0E+04"),
    "aeg-d-dwarfs/v1/m000003": ("Andromeda III", 162, "< 6.2E+04"),
    "aeg-d-dwarfs/v1/m000031": ("Canes Venatici II", 134, "< 2.4E+03"),
    "aeg-d-dwarfs/v1/m000020": ("Andromeda XXIII", 170, "< 8.2E+04"),
    "aeg-d-dwarfs/v1/m000042": ("Leo I", 143, "< 1.0E+04"),
    "aeg-d-dwarfs/v1/m000010": ("Andromeda XII", 188, "< 7.9E+04"),
}
for mid, (gal, line, v) in PUTMAN.items():
    ROWS.append((mid, "l_MHI MHI", v, "Msun (5 sigma upper limit)", f"{PUT} line {line} ({gal}), bytes 86-94"))

if __name__ == "__main__":
    import csv, sys
    w = csv.writer(sys.stdout, lineterminator="\n")
    w.writerow(["measurement_id", "input", "value", "unit", "locator"])
    for r in sorted(ROWS, key=lambda r: r[0]):
        w.writerow(r)
