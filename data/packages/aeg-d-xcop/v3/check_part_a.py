"""Run the frozen X-COP v2 reproduction test, part A (REPRODUCTION.md, revision 6).

The test text is frozen by hash in data/frozen/xcop-v2-part-a.json. This script
implements it as written; where the text leaves a computational detail open,
the choice is stated in IMPLEMENTATION_NOTES below and in the result file.

Usage:
    python check_part_a.py DATA_E22_TAR_GZ MBAR_TAR_GZ OUT_JSON [a|b]

The optional last argument forces the downstream radius convention; such a run
is exploratory and is never the frozen outcome.

The archives are never committed (D-004, D-090 rule 5). The output holds check
outcomes, ratios and fitted parameters, not the source rows.
"""
import hashlib
import io
import json
import sys
import tarfile

import numpy as np
from astropy import constants as const
from astropy import units as u
from astropy.io import fits
from scipy.optimize import least_squares
from scipy.special import gamma as Gfun, gammainc, hyp2f1
from scipy.integrate import quad

IMPLEMENTATION_NOTES = [
    "Archives are read in memory from the tar files; nothing is extracted to disk.",
    "Log-log interpolation (R1) uses only grid rows with r > 0 and the interpolated quantity > 0.",
    "A2 and A3: a row with no testable value in a variant counts as untestable; a cluster with zero testable rows fails that variant.",
    "A3 'testable' also requires the two bracketing GP rows to give positive MASS (total part) or MGAS (gas part).",
    "A4: FGAS is interpolated log-log against log r like the masses. If every FGAS value is <= 1, FGAS is read as a fraction and multiplied by 100 to give per cent.",
    "A6: least_squares (trust-region reflective) on ln M_STAR from 12 starting points per model; the lowest rms is kept. Bounds: n in [0.3, 20], r_e in [0.1, 1000] kpc, R200 in [100, 20000] kpc.",
    "A6: b_n from the Ciotti & Bertin 1999 asymptotic series, b_n = 2n - 1/3 + 4/(405 n) + 46/(25515 n^2).",
    "A6: the 2D gNFW cylinder mass is M3D(<R) + integral_R^inf 4 pi r^2 rho(r) [1 - sqrt(1 - R^2/r^2)] dr, tabulated in R/r_s and interpolated.",
    "A8: 'inside the source's range' uses the GP row midpoint (R1 exception); a row with R_IN = 0 has no midpoint and is counted as outside.",
]

G = const.G.to(u.kpc * u.km**2 / u.s**2 / u.Msun).value  # kpc (km/s)^2 / Msun
KPC_M = u.kpc.to(u.m)
MSUN_KG = const.M_sun.value
G_SI = const.G.value

ARCH = {
    "data_E22": "ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d",
    "mbar": "0420a7edba60da7f2df6aa4f38cbb21135ab50949d579176a8c893bab712c496",
}
FIVE = ["A644", "A1795", "A2029", "A2142", "A2319"]
SEVEN = ["A85", "A1644", "A2255", "A3158", "A3266", "RXC1825", "ZW1215"]

TABLE1 = {  # z, R500 kpc, M500 1e14, M200 1e14
    "A85": (0.0555, 1214, 5.03, 7.04), "A644": (0.0704, 1398, 7.80, 10.97),
    "A1644": (0.0473, 1031, 3.06, 4.93), "A1795": (0.0622, 1160, 4.42, 6.04),
    "A2029": (0.0766, 1340, 6.91, 9.29), "A2142": (0.09, 1453, 8.93, 13.33),
    "A2255": (0.0809, 1202, 5.01, 8.94), "A2319": (0.0557, 1424, 8.12, 11.61),
    "A3158": (0.059, 1146, 4.25, 6.46), "A3266": (0.0589, 1381, 7.43, 12.22),
    "RXC1825": (0.065, 1109, 3.88, 5.66), "ZW1215": (0.0766, 1346, 7.00, 11.44),
}
TABLE4 = {  # (value, err) for gas, star, bar at 2500, 500, 200
    "A644": [(7.7, .1), (1.2, .4), (8.9, .5), (12.8, .6), (1.3, .5), (14.1, 1.1), (16.9, 1.2), (1.5, .6), (18.4, 1.7)],
    "A1795": [(9.6, .1), (1.7, .6), (11.3, .6), (13.4, .3), (1.3, .5), (14.7, .7), (15.8, .5), (1.3, .4), (17.1, 1.0)],
    "A2029": [(11.1, .1), (2.8, .9), (13.8, 1.1), (14.4, .3), (2.1, .7), (16.5, 1.0), (17.1, .7), (2.0, .7), (19.1, 1.4)],
    "A2142": [(12.0, .1), (2.3, .8), (14.3, .9), (14.1, .2), (1.7, .6), (15.8, .8), (14.7, .5), (1.5, .5), (16.2, 1.0)],
    "A2319": [(9.2, .1), (2.0, .7), (11.3, .8), (17.0, .2), (1.5, .5), (18.5, .7), (24.9, .5), (1.5, .5), (26.4, 1.0)],
}
GHIZ = {"A644": 3.70, "A1795": 3.02, "A2029": 6.51, "A2142": 6.97, "A2319": 5.11}  # 1e12 Msun
H0, OM = 67.8, 0.308


def rho_c(z):
    H = H0 * np.sqrt(OM * (1 + z) ** 3 + 1 - OM)  # km/s/Mpc
    Hk = H / 1000.0  # km/s/kpc
    return 3 * Hk**2 / (8 * np.pi * G)  # Msun/kpc^3


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_tar(path):
    data = open(path, "rb").read()
    tf = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
    files = {}
    for m in tf.getmembers():
        if m.isfile():
            files[m.name.lstrip("./")] = tf.extractfile(m).read()
    return sha(data), files


def table(b, ext=1):
    with fits.open(io.BytesIO(b)) as h:
        d = h[ext].data
        cols = {c.name: np.array(d[c.name], dtype=float) for c in h[ext].columns}
        units = {c.name: c.unit for c in h[ext].columns}
        name = h[ext].name
    return cols, units, name, len(d)


def loglog(rgrid, ygrid, r):
    """Log-log interpolation; nan outside the usable grid (no extrapolation)."""
    rgrid = np.asarray(rgrid, float); ygrid = np.asarray(ygrid, float)
    ok = (rgrid > 0) & (ygrid > 0) & np.isfinite(rgrid) & np.isfinite(ygrid)
    rg, yg = rgrid[ok], ygrid[ok]
    o = np.argsort(rg); rg, yg = rg[o], yg[o]
    r = np.atleast_1d(np.asarray(r, float))
    out = np.full(r.shape, np.nan)
    if len(rg) < 2:
        return out
    inside = (r >= rg[0]) & (r <= rg[-1])
    out[inside] = np.exp(np.interp(np.log(r[inside]), np.log(rg), np.log(yg)))
    return out


def g_of(M_msun, r_kpc):
    return G_SI * M_msun * MSUN_KG / (r_kpc * KPC_M) ** 2


def M_of_g(g, r_kpc):
    return g * (r_kpc * KPC_M) ** 2 / G_SI / MSUN_KG


def main(a_path, b_path, out_path, force_convention=None):
    R = {"exploratory_forced_convention": force_convention,"implementation_notes": IMPLEMENTATION_NOTES, "test": "data/packages/aeg-d-xcop/v2/REPRODUCTION.md",
         "test_sha256": "c7c949a087317f137913829b5047104c204e08b41b273ac9e041a3d89c81c4c1"}
    sa, A = read_tar(a_path)
    sb, B = read_tar(b_path)

    # ---------------- A1 ----------------
    a1 = {"archive_sha_ok": sa == ARCH["data_E22"] and sb == ARCH["mbar"], "problems": []}
    expA = set()
    for c in FIVE:
        for f in (f"gbar_gobs_{c}.fits", "GP_thermo.fits", "EIN3_bar_mass.fits", f"{c}_BCG.txt"):
            expA.add(f"{c}/{f}")
    expB = {f"{c.lower()}/GP_mass.fits" for c in FIVE + SEVEN} | {f"{c.lower()}/EIN3_bar_mass.fits" for c in FIVE}
    a1["members_A_ok"] = set(A) == expA
    a1["members_B_ok"] = set(B) == expB
    a1["member_sha256"] = {**{"data_E22/" + k: sha(v) for k, v in sorted(A.items())},
                           **{"mbar/" + k: sha(v) for k, v in sorted(B.items())}}
    exp_cols = {
        "gbar": ["RADIUS", "GBAR", "GBAR_ERR", "GOBS", "GOBS_ERR_LO", "GOBS_ERR_HI"],
        "thermo": ["R_IN", "R_OUT", "R_REF"] + [f"{q}{s}" for q in ["P_TOT", "T3D", "TSPEC", "NE", "K", "T_COOL", "LAMBDA"] for s in ("", "_LO", "_HI")],
        "ein": ["R_IN", "R_OUT", "R_REF"] + [f"{q}{s}" for q in ["MASS", "M_DM", "MGAS", "FGAS"] for s in ("", "_LO", "_HI")] + ["M_STAR"],
        "gp": ["R_IN", "R_OUT"] + [f"{q}{s}" for q in ["MASS", "MGAS", "FGAS"] for s in ("", "_LO", "_HI")],
    }
    GB, EIN, GP = {}, {}, {}
    for c in FIVE:
        cols, units, name, n = table(A[f"{c}/gbar_gobs_{c}.fits"])
        GB[c] = cols
        if sorted(cols) != sorted(exp_cols["gbar"]): a1["problems"].append(f"{c} gbar_gobs columns {list(cols)}")
        if n != 21: a1["problems"].append(f"{c} gbar_gobs rows {n}")
        if (units.get("RADIUS") or "").strip() != "kpc": a1["problems"].append(f"{c} RADIUS unit {units.get('RADIUS')}")
        for k in exp_cols["gbar"][1:]:
            if (units.get(k) or "").replace(" ", "") not in ("m/s^2", "m/s2", "ms-2", "m.s-2", "m/s**2"):
                a1["problems"].append(f"{c} {k} unit {units.get(k)}")
            if not np.all(np.isfinite(cols[k])): a1["problems"].append(f"{c} {k} non-finite")
        for k in ("GBAR", "GOBS"):
            if not np.all(cols[k] > 0): a1["problems"].append(f"{c} {k} not all positive")
        tc, _, tn, tnr = table(A[f"{c}/GP_thermo.fits"])
        if tn != "THERMODYNAMIC PROFILES" or tnr != 200 or sorted(tc) != sorted(exp_cols["thermo"]):
            a1["problems"].append(f"{c} GP_thermo structure {tn} {tnr}")
        ec, _, en, enr = table(A[f"{c}/EIN3_bar_mass.fits"])
        EIN[c] = ec
        if en != "MASS PROFILE" or enr != 200 or sorted(ec) != sorted(exp_cols["ein"]):
            a1["problems"].append(f"{c} EIN3 structure {en} {enr} {list(ec)}")
        if A[f"{c}/EIN3_bar_mass.fits"] != B[f"{c.lower()}/EIN3_bar_mass.fits"]:
            a1["problems"].append(f"{c} Einasto files differ between archives")
    for c in FIVE + SEVEN:
        gc, _, gn, gnr = table(B[f"{c.lower()}/GP_mass.fits"])
        GP[c] = gc
        if gn != "MASS PROFILE" or gnr != 200 or sorted(gc) != sorted(exp_cols["gp"]):
            a1["problems"].append(f"{c} GP_mass structure {gn} {gnr} {list(gc)}")
    a1["pass"] = a1["archive_sha_ok"] and a1["members_A_ok"] and a1["members_B_ok"] and not a1["problems"]
    R["A1"] = a1

    # ---------------- A2 ----------------
    a2 = {"variants": {}}
    order = [("a", "i"), ("a", "ii"), ("b", "i"), ("b", "ii")]
    for conv, gas in order:
        key = f"({conv})({gas})"
        res = {}
        allpass = True
        for c in FIVE:
            r = GB[c]["RADIUS"]
            er = EIN[c]["R_REF"] if conv == "a" else EIN[c]["R_OUT"]
            ms = loglog(er, EIN[c]["M_STAR"], r)
            mg = loglog(er, EIN[c]["MGAS"], r) if gas == "i" else loglog(GP[c]["R_OUT"], GP[c]["MGAS"], r)
            ratio = GB[c]["GBAR"] / g_of(mg + ms, r)
            t = np.isfinite(ratio)
            if t.sum() == 0:
                ok = False; med = None; mx = None
            else:
                med = float(np.median(ratio[t])); mx = float(np.max(np.abs(ratio[t] - 1)))
                ok = abs(med - 1) <= 0.02 and mx <= 0.05
            allpass &= ok
            res[c] = {"n_testable": int(t.sum()), "median_ratio": med, "max_abs_dev": mx, "pass": ok,
                      "ratios": [None if not np.isfinite(x) else round(float(x), 5) for x in ratio]}
        a2["variants"][key] = {"clusters": res, "pass_all_five": allpass}
    sel = next((k for k in [f"({c})({g})" for c, g in order] if a2["variants"][k]["pass_all_five"]), None)
    a2["selected"] = sel
    a2["pass"] = sel is not None
    conv = sel[1] if sel else "a"
    if force_convention:  # exploratory only: not the frozen test's outcome
        conv = force_convention
    a2["convention_used_downstream"] = conv
    R["A2"] = a2

    def ein_r(c):
        return EIN[c]["R_REF"] if conv == "a" else EIN[c]["R_OUT"]

    # ---------------- A3 ----------------
    a3 = {"clusters": {}, "notes": []}
    if sel == "(a)(ii)" or sel == "(b)(ii)":
        a3["notes"].append("A2 selected variant (ii): GBAR is built from MGAS_GP, so ratio_gas is close to 1 by construction, up to the labelling allowance.")
    cond_all = True
    coarse = False
    for c in FIVE:
        gp = GP[c]
        use = gp["R_IN"] > 0
        mid = np.sqrt(gp["R_IN"][use] * gp["R_OUT"][use])
        step = np.log(gp["R_OUT"][use] / gp["R_IN"][use])
        o = np.argsort(mid); mid, step = mid[o], step[o]
        massg, mgasg = gp["MASS"][use][o], gp["MGAS"][use][o]
        r = GB[c]["RADIUS"]
        R500 = TABLE1[c][1]
        testable = (r >= mid[0]) & (r <= mid[-1])
        idx = np.clip(np.searchsorted(mid, r) , 1, len(mid) - 1)
        delta = np.where(testable, np.maximum(step[idx - 1], step[idx]), np.nan)
        a = np.exp(1.5 * delta) - 1
        Mtot = loglog(mid, massg, r)
        Mgas = loglog(mid, mgasg, r)
        rt = GB[c]["GOBS"] / g_of(Mtot, r)
        Mbar = M_of_g(GB[c]["GBAR"], r)
        Mst = loglog(ein_r(c), EIN[c]["M_STAR"], r)
        gas_rows = testable & np.isfinite(Mst) & (Mst < 0.5 * Mbar) & np.isfinite(Mgas)
        rg = np.where(gas_rows, Mgas / (Mbar - Mst), np.nan)
        tot_rows = testable & np.isfinite(rt)
        inrng = (r >= 0.05 * R500) & (r <= 2 * R500)
        out = {"r_over_R500_range": [float(r.min() / R500), float(r.max() / R500)],
               "delta": [None if not np.isfinite(x) else round(float(x), 5) for x in delta],
               "max_delta_testable": float(np.nanmax(delta[testable])) if testable.any() else None}
        if testable.any() and np.nanmax(delta[testable]) > 0.05:
            coarse = True
        for part, rows, ratio, nmin in (("total", tot_rows, rt, 10), ("gas", gas_rows, rg, 5)):
            p = {"n_rows": int(rows.sum()), "ratios": [None if not np.isfinite(x) else round(float(x), 5) for x in ratio]}
            med_rows = rows & inrng
            p["n_median_rows"] = int(med_rows.sum())
            ok = rows.sum() >= nmin and med_rows.sum() >= 5
            if rows.sum():
                p["median_all_rows"] = float(np.median(ratio[rows])); p["max_abs_dev"] = float(np.max(np.abs(ratio[rows] - 1)))
                p["row_fail_count"] = int(np.sum(np.abs(ratio[rows] - 1) > 0.10 + a[rows]))
                ok &= p["row_fail_count"] == 0
            if med_rows.sum():
                med = float(np.median(ratio[med_rows])); ma = float(np.median(a[med_rows]))
                p["median_in_range"] = med; p["median_allowance"] = ma
                p["median_ok"] = abs(med - 1) <= 0.03 + ma
                ok &= p["median_ok"]
            if part == "gas" and not a2["pass"]:
                ok = False; p["note"] = "A2 failed, so the gas part fails (test l.151)."
            p["pass"] = bool(ok)
            out[part] = p
            cond_all &= ok
        ein_ratio = GB[c]["GOBS"] / g_of(loglog(ein_r(c), EIN[c]["MASS"], r), r)
        out["einasto_diagnostic"] = {"median": float(np.nanmedian(ein_ratio)), "max_abs_dev": float(np.nanmax(np.abs(ein_ratio - 1))),
                                     "ratios": [None if not np.isfinite(x) else round(float(x), 5) for x in ein_ratio]}
        a3["clusters"][c] = out
    a3["grid_too_coarse"] = coarse
    a3["stage2_condition_pass"] = bool(cond_all and not coarse)
    R["A3"] = a3

    # ---------------- R3 / A4 / A5 / A7 ----------------
    def r_delta(rg, Mg, z, D):
        rg = np.asarray(rg); Mg = np.asarray(Mg)
        ok = (rg > 0) & (Mg > 0); rg, Mg = rg[ok], Mg[ok]
        o = np.argsort(rg); rg, Mg = rg[o], Mg[o]
        dens = Mg / (4 / 3 * np.pi * rg**3)
        target = D * rho_c(z)
        y = np.log(dens) - np.log(target)
        for k in range(len(rg) - 1):
            if y[k] >= 0 > y[k + 1]:
                x0, x1 = np.log(rg[k]), np.log(rg[k + 1])
                return float(np.exp(x0 + (0 - y[k]) * (x1 - x0) / (y[k + 1] - y[k])))
        return None

    a4 = {"entries": {}, "notes": []}
    fgas_frac = all(np.nanmax(EIN[c]["FGAS"]) <= 1 for c in FIVE)
    a4["fgas_read_as"] = "fraction (x100)" if fgas_frac else "per cent"
    scale = 100.0 if fgas_frac else 1.0
    a5, a7 = {}, {}
    rd = {}
    n_in, n_01 = 0, 0
    for c in FIVE:
        z = TABLE1[c][0]; er = ein_r(c)
        rows = {}
        for j, D in enumerate((2500, 500, 200)):
            Rd = r_delta(er, EIN[c]["MASS"], z, D)
            rd[(c, D)] = Rd
            if Rd is None:
                for q in range(3):
                    rows[f"{['f_gas','f_star','f_bar'][q]}_{D}"] = {"atlas": None, "pass": False, "note": "not computable"}
                continue
            M = loglog(er, EIN[c]["MASS"], Rd)[0]
            fg = loglog(er, EIN[c]["FGAS"], Rd)[0] * scale
            fs = loglog(er, EIN[c]["M_STAR"], Rd)[0] / M * 100
            fg2 = loglog(er, EIN[c]["MGAS"], Rd)[0] / M * 100
            vals = {"f_gas": fg, "f_star": fs, "f_bar": fg + fs}
            for q, name in enumerate(("f_gas", "f_star", "f_bar")):
                pub, err = TABLE4[c][3 * j + q]
                d = vals[name] - pub
                ok = abs(d) <= err + 0.05 + 1e-9
                n_in += ok; n_01 += abs(d) <= 0.1 + 1e-9
                rows[f"{name}_{D}"] = {"atlas": round(float(vals[name]), 3), "table4": pub, "err": err, "diff": round(float(d), 3), "pass": bool(ok)}
            rows[f"f_gas_{D}"]["secondary_MGAS_over_MASS"] = round(float(fg2), 3)
            rows[f"R_{D}_kpc"] = round(Rd, 1)
        # variant with Table 1 R500
        Rt = TABLE1[c][1]
        M = loglog(er, EIN[c]["MASS"], Rt)[0]
        fg = loglog(er, EIN[c]["FGAS"], Rt)[0] * scale; fs = loglog(er, EIN[c]["M_STAR"], Rt)[0] / M * 100
        rows["variant_table1_R500"] = {"f_gas": round(float(fg), 3), "f_star": round(float(fs), 3), "f_bar": round(float(fg + fs), 3)}
        a4["entries"][c] = rows
        R500 = rd[(c, 500)]
        a5[c] = {"R500_files_kpc": None if R500 is None else round(R500, 1), "R500_table1_kpc": TABLE1[c][1],
                 "ratio": None if R500 is None else round(R500 / TABLE1[c][1], 4)}
        if R500 is not None:
            Mgp = loglog(GP[c]["R_OUT"], GP[c]["MASS"], R500)[0]
            Mein = loglog(er, EIN[c]["MASS"], R500)[0]
            Mt1 = TABLE1[c][2] * 1e14
            a7[c] = {"M_GP": float(Mgp), "M_EIN": float(Mein), "M500_table1": Mt1,
                     "GP/EIN": round(float(Mgp / Mein), 4), "GP/Table1": round(float(Mgp / Mt1), 4), "EIN/Table1": round(float(Mein / Mt1), 4),
                     "note": "Table 1 M500 is at Table 1's R500; the others at R500 from R3."}
    a4["n_entries"] = 45
    a4["n_within_tolerance"] = int(n_in)
    a4["n_within_0.1pp"] = int(n_01)
    a4["pass"] = all(v["pass"] for c in a4["entries"] for k, v in a4["entries"][c].items() if isinstance(v, dict) and "pass" in v) and n_in == 45
    R["A4"] = a4; R["A5"] = a5; R["A7"] = a7
    R["R2_units_accepted"] = a4["pass"]

    # ---------------- A6 / A9 ----------------
    def b_n(n):
        return 2 * n - 1 / 3 + 4 / (405 * n) + 46 / (25515 * n**2)

    def m_sersic(r, lrho0, lre, n):
        b = b_n(n); re = np.exp(lre)
        x = b * (r / re) ** (1 / n)
        return 4 * np.pi * np.exp(lrho0) * np.exp(b) * re**3 * n * b ** (-3 * n) * Gfun(3 * n) * gammainc(3 * n, x)

    def gnfw3d(y, al):  # dimensionless enclosed mass, y = r/rs
        return y ** (3 - al) / (3 - al) * hyp2f1(3 - al, 3 - al, 4 - al, -y)

    tab = {}
    ygrid = np.logspace(-4, 3, 400)
    for al in (1.63, 1.64):
        rho = lambda x: x ** (-al) * (1 + x) ** (al - 3)
        vals = []
        for y in ygrid:
            extra = quad(lambda x: 4 * np.pi * x**2 * rho(x) * (1 - np.sqrt(max(0.0, 1 - (y / x) ** 2))), y, np.inf, limit=400)[0]
            vals.append(4 * np.pi * gnfw3d(y, al) + extra)
        tab[al] = np.array(vals)

    def sat(r, rs, al, X):
        y = r / rs
        if X == "3D":
            return 4 * np.pi * gnfw3d(y, al)
        return np.exp(np.interp(np.log(y), np.log(ygrid), np.log(tab[al])))

    a6 = {"clusters": {}, "sets": {"(0.64,1.63)": (0.64, 1.63), "(0.72,1.64)": (0.72, 1.64)}}
    fits_store = {}
    rng = np.random.default_rng(20261103)
    for c in FIVE:
        r = ein_r(c); ms = EIN[c]["M_STAR"]
        ok = (r > 0) & (ms > 0); r, ms = r[ok], ms[ok]
        z = TABLE1[c][0]
        R200_t1 = (TABLE1[c][3] * 1e14 / (200 * rho_c(z) * 4 / 3 * np.pi)) ** (1 / 3)
        res = {"n_rows": int(len(r)), "R200_table1_M200_kpc": round(float(R200_t1), 1)}
        for sname, (cc, al) in a6["sets"].items():
            best = {}
            for X in ("3D", "2D"):
                def resid(p):
                    lrho0, lre, n, lN, lR200 = p
                    rs = np.exp(lR200) / cc
                    m = m_sersic(r, lrho0, lre, n) + np.exp(lN) * sat(r, rs, al, X)
                    return np.log(m) - np.log(ms)
                lo = [-50, np.log(0.1), 0.3, -50, np.log(100)]
                hi = [80, np.log(1000), 20, 80, np.log(20000)]
                bestfit = None
                for k in range(12):
                    lre0 = np.log(rng.uniform(5, 200)); n0 = rng.uniform(1, 8); lR0 = np.log(rng.uniform(800, 3000))
                    rs0 = np.exp(lR0) / cc
                    # scale initial normalisations to the data
                    mtot = ms[-1]
                    lN0 = np.log(0.7 * mtot / (4 * np.pi * gnfw3d(r[-1] / rs0, al)))
                    s0 = m_sersic(np.array([r[-1]]), 0.0, lre0, n0)[0]
                    lrho00 = np.log(0.3 * mtot / s0)
                    p0 = np.clip([lrho00, lre0, n0, lN0, lR0], np.array(lo) + 1e-6, np.array(hi) - 1e-6)
                    try:
                        f = least_squares(resid, p0, bounds=(lo, hi), x_scale="jac", max_nfev=4000)
                    except Exception:
                        continue
                    rms = float(np.sqrt(np.mean(f.fun**2)))
                    if np.isfinite(rms) and (bestfit is None or rms < bestfit[0]):
                        bestfit = (rms, f.x)
                rms, x = bestfit
                best[X] = {"rms": rms, "rho0": float(np.exp(x[0])), "r_e_kpc": float(np.exp(x[1])), "n": float(x[2]),
                           "N": float(np.exp(x[3])), "R200_kpc": float(np.exp(x[4]))}
            r3, r2 = best["3D"]["rms"], best["2D"]["rms"]
            v = "3D" if (r3 <= 1e-3 and r2 >= 5 * r3) else "2D" if (r2 <= 1e-3 and r3 >= 5 * r2) else "undetermined"
            res[sname] = {"fits": best, "verdict": v}
            fits_store[(c, sname)] = best
        a6["clusters"][c] = res
    overall = "undetermined"
    for V, opp in (("3D", "2D"), ("2D", "3D")):
        nV = sum(any(a6["clusters"][c][s]["verdict"] == V for s in a6["sets"]) for c in FIVE)
        nO = sum(any(a6["clusters"][c][s]["verdict"] == opp for s in a6["sets"]) for c in FIVE)
        if nV >= 4 and nO == 0:
            overall = V
    a6["overall"] = overall
    R["A6"] = a6

    a9 = {}
    for c in FIVE:
        R500 = rd[(c, 500)]
        if R500 is None:
            a9[c] = None; continue
        ms500 = loglog(ein_r(c), EIN[c]["M_STAR"], R500)[0]
        e = {"M_STAR_R500": float(ms500), "ratio_to_ghizzardi": round(float(ms500 / (GHIZ[c] * 1e12)), 4)}
        for sname in a6["sets"]:
            for X in ("3D", "2D"):
                f = fits_store[(c, sname)][X]
                ser = m_sersic(np.array([R500]), np.log(f["rho0"]), np.log(f["r_e_kpc"]), f["n"])[0]
                e[f"minus_sersic_{sname}_{X}"] = round(float((ms500 - ser) / (GHIZ[c] * 1e12)), 4)
        a9[c] = e
    R["A9"] = a9

    # ---------------- A8 ----------------
    a8 = {"clusters": {}}
    s1 = True
    for c in SEVEN:
        gp = GP[c]; R500 = TABLE1[c][1]
        n = len(gp["MASS"])
        mid = np.where(gp["R_IN"] > 0, np.sqrt(np.clip(gp["R_IN"], 0, None) * gp["R_OUT"]), np.nan)
        inr = np.isfinite(mid) & (mid >= 0.01 * R500) & (mid <= 2 * R500)
        pos = bool(np.all(gp["MASS"][inr] > 0) and np.all(gp["MGAS"][inr] > 0))
        ok = n == 200 and pos
        s1 &= ok
        o = np.argsort(mid[inr])
        dM = np.diff(gp["MASS"][inr][o]); dG = np.diff(gp["MGAS"][inr][o])
        fdiff = np.abs(gp["FGAS"] - gp["MGAS"] / gp["MASS"])
        a8["clusters"][c] = {"rows": int(n), "rows_in_source_range": int(inr.sum()), "positive_in_range": pos, "pass": ok,
                             "outward_decreases_MASS": int(np.sum(dM < 0)), "outward_decreases_MGAS": int(np.sum(dG < 0)),
                             "max_abs_FGAS_minus_ratio": float(np.nanmax(fdiff)), "median_abs_FGAS_minus_ratio": float(np.nanmedian(fdiff)),
                             "mid_range_over_R500": [float(np.nanmin(mid) / R500), float(np.nanmax(mid) / R500)]}
    a8["stage1_pass"] = s1
    R["A8"] = a8
    R["stage2_condition_c"] = bool(a3["stage2_condition_pass"] and s1)
    json.dump(R, open(out_path, "w"), indent=1, default=float)
    print(json.dumps({"A1": a1["pass"], "A1_problems": a1["problems"], "A2": a2["selected"], "A3_stage2": a3["stage2_condition_pass"],
                      "A4": a4["pass"], "A4_within": a4["n_within_tolerance"], "A6": a6["overall"], "A8_stage1": s1}, indent=1))


if __name__ == "__main__":
    # A 4th argument forces the downstream R1 convention ("a" or "b"). That run is
    # EXPLORATORY: it is not the frozen test's outcome and is labelled as such.
    main(*sys.argv[1:4], *(sys.argv[4:5]))
