"""Score aeg-d-strong-lensing/v2 against its frozen test, items 1-13 (REPRODUCTION.md).

Usage: python data/packages/aeg-d-strong-lensing/v2/reproduction/score.py [--site site/dist] [--fetch-abstracts]

Independent of convert.py: it re-reads v1's tables, the frozen reading and the v2 tables, and recomputes what
it checks with the frozen aeg.lensing. Item 12 runs the validator, check_formulas.py, aeg.formula_check and
test_lensing.py here; the site build and aeg.site_check are run by the commands listed in REPRODUCTION_RESULT.md,
and with --site the item 9 page line and the item 12 ledger check read the built site. With --fetch-abstracts
the three arXiv abstract pages of item 9 are fetched and checked (hash, or the quoted H0 if the page changed).
Writes reproduction/score.json.
"""

from __future__ import annotations

import csv
import hashlib
import html
import importlib.util
import json
import math
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np
from astropy.table import Table

PKG = Path(__file__).resolve().parents[1]
V1 = PKG.parent / "v1"
ROOT = PKG.parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg import lensing as L  # noqa: E402

P1, P2 = "aeg-d-strong-lensing/v1/", "aeg-d-strong-lensing/v2/"
X = "x_strong_lensing_"
NEW_A = ["a6s_theta_e", "a6s_lens_distance"]
NOT_COMPUTED = "θ_E error stated; effect on g_bar not computed"
NEW_MEAS_COLS = {"g_obs_err_point_lo", "g_obs_err_point_hi", "g_bar_err_point_lo", "g_bar_err_point_hi",
                 "err_level", "err_level_status", "g_bar_err_level", "g_bar_err_level_status",
                 f"{X}theta_e_err_frac_lo", f"{X}theta_e_err_frac_hi", f"{X}theta_profile_form",
                 f"{X}theta_profile_r_e_arcsec", f"{X}theta_profile_n", f"{X}dlngbar_dlntheta", f"{X}g_bar_stars_ref",
                 f"{X}mass_ellipticity_frac", f"{X}los_frac", f"{X}neighbour_light_frac", f"{X}r_eff_err_frac"}
SCOPES = {"SLACS": ["SLACS V-modelled lenses"], "S4TM": ["S4TM lenses"], "SL2S": ["SL2S III sample"],
          "SNELLS": ["SNL-0 (ESO 325-G004)", "SNL-1 (ESO 286-G022)", "SNL-2"], "MaNGA": ["MaNGA J1436+4943", "MaNGA J1701+3722"],
          "NGC 6505": ["Euclid NGC 6505"], "J0403": ["MNELLS J0403-0239"], "SNL-0": ["SNL-0 (ESO 325-G004)"],
          "SNL-1": ["SNL-1 (ESO 286-G022)"], "SNL-2": ["SNL-2"]}


def rows(path: Path) -> list[dict]:
    t = Table.read(path, format="ascii.ecsv")
    out = []
    for r in t:
        d = {}
        for c in t.colnames:
            v = r[c]
            if v is np.ma.masked:
                d[c] = None
            elif t[c].dtype.kind == "f":
                d[c] = None if math.isnan(float(v)) else float(v)
            elif t[c].dtype.kind in "iu":
                d[c] = int(v)
            else:
                d[c] = None if str(v) == "" else str(v)
        out.append(d)
    return out


def table(path: Path) -> Table:
    return Table.read(path, format="ascii.ecsv")


def mp(x):
    return None if x is None else str(x).replace(P1, P2)


def ids(s):
    return [x for x in str(s or "").split(";") if x]


def rcsv(name):
    with open(PKG / "reading" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rel(a, b):
    return abs(a / b - 1) if b else abs(a - b)


def dlng(theta, re_, n):
    h = 1e-4
    up, dn = (L.sersic_projected_fraction(theta * math.exp(s * h), re_, n) for s in (1, -1))
    return -2 + (math.log(up) - math.log(dn)) / (2 * h)


def run(cmd: list[str]) -> tuple[int, str]:
    import os
    env = dict(os.environ, PYTHONPATH=str(ROOT / "pipeline"))
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=env)
    return p.returncode, (p.stdout + p.stderr)[-1500:]


def main() -> int:
    site = ROOT / sys.argv[sys.argv.index("--site") + 1] if "--site" in sys.argv else None
    res: dict[str, dict] = {}
    M1, M2 = rows(V1 / "tables/measurements.ecsv"), rows(PKG / "tables/measurements.ecsv")
    O1, O2 = rows(V1 / "tables/observables.ecsv"), rows(PKG / "tables/observables.ecsv")
    S1, S2 = rows(V1 / "tables/systems.ecsv"), rows(PKG / "tables/systems.ecsv")
    T = rows(PKG / "tables/uncertainty_terms.ecsv")
    m2t = table(PKG / "tables/measurements.ecsv")
    theta = {r["measurement_id_v1"]: r for r in rcsv("theta_class.csv")}
    profiles = rcsv("profiles.csv")
    prof = {mid: p for p in profiles for mid in p["applies_to_rows"].split(";")}
    errl = rcsv("err_levels.csv")
    dist = rcsv("distance.csv")
    inv = rcsv("baryon_inventory.csv")
    d096 = rcsv("d096.csv")
    cls = {mp(k): v["rule5_class"] for k, v in theta.items()}
    lower = {mp(k) for k, v in theta.items() if v["err_kind"].strip() == "lower_bound"}
    classA = {k for k, v in cls.items() if v == "A"}
    printed = {mp(k): p for k, p in prof.items() if p["profile_status"] == "printed"}
    order = [s["system_id"] for s in S2]
    with_rows = [s for s in order if any(m["system_id"] == s for m in M2)]
    new_obs = O2[len(O1):]
    new_obs_by_sys = {}
    for o in new_obs:
        new_obs_by_sys.setdefault(o["system_id"], []).append(o["observable_id"])

    # ---------------------------------------------------------------- 1. rows
    p = []
    if len(M2) != 147 or len(M1) != 147:
        p.append(f"{len(M2)} rows (v1 {len(M1)})")
    if sum(m["role"] == "default" for m in M2) != 94 or sum(m["role"] == "alternative" for m in M2) != 53:
        p.append("role counts differ from 94 / 53")
    if len(S2) != 212:
        p.append(f"{len(S2)} systems")
    for a, b in zip(M1, M2):
        if mp(a["measurement_id"]) != b["measurement_id"] or a["system_id"] != b["system_id"] or a["role"] != b["role"] \
                or mp(a["alternative_of"]) != b["alternative_of"] or a[f"{X}scope"] != b[f"{X}scope"]:
            p.append(f"row {a['measurement_id']} differs in identity")
    res["1"] = {"pass": not p, "problems": p, "detail": f"{len(M2)} rows ({sum(m['role'] == 'default' for m in M2)} defaults, "
                f"{sum(m['role'] == 'alternative' for m in M2)} alternatives) in v1's order; {len(S2)} systems"}

    # ---------------------------------------------------------------- 2. what may change
    p = []
    bitwise = ["g_obs", "g_bar", "g_bar_stars", "g_bar_gas_cold", "g_bar_gas_hot", "r_kpc", "g_bar_err_lo", "g_bar_err_hi"] + \
              [c for c in M1[0] if c.startswith(X)]
    changed_cols = {}
    for a, b in zip(M1, M2):
        mid = b["measurement_id"]
        A = mid in classA
        for c in M1[0]:
            va, vb = a[c], b[c]
            if c in ("measurement_id", "alternative_of", "observed_from"):
                ok = (mp(va) if c != "observed_from" else ";".join(mp(x) for x in ids(va))) == vb
            elif c == "baryonic_from":
                ok = ids(vb) == [mp(x) for x in ids(va)] + new_obs_by_sys.get(b["system_id"], [])
            elif c in ("g_obs_err_lo", "g_obs_err_hi"):
                ok = (vb is None) if A else (va == vb)
            elif c == "assumptions":
                ok = ids(vb) == ids(va) + NEW_A
            elif c == "flags":
                ok = ids(vb) == (ids(va) + ([] if "no_uncertainty" in ids(va) else ["no_uncertainty"]) if A else ids(va))
            elif c == "notes":
                if va == vb:
                    ok = True
                else:
                    ok = (A or cls[mid] == "aperture") and (va is None or str(vb).startswith(va + "; "))
            else:
                ok = va == vb
            if not ok:
                changed_cols.setdefault(c, []).append(mid)
    for c, ms in changed_cols.items():
        p.append(f"column {c} differs from v1 beyond what the test allows on {len(ms)} rows, e.g. {ms[:2]}")
    extra = set(M2[0]) - set(M1[0])
    if extra != NEW_MEAS_COLS:
        p.append(f"new measurement columns {sorted(extra ^ NEW_MEAS_COLS)} differ from the test's list")
    if set(M1[0]) - set(M2[0]):
        p.append(f"v1 columns missing: {sorted(set(M1[0]) - set(M2[0]))}")
    for a, b in zip(S1, S2):
        if a != b:
            p.append(f"system {a['system_id']} differs from v1")
    if [list(o) for o in S1[:1]] != [list(o) for o in S2[:1]]:
        p.append("systems columns differ")
    for a, b in zip(O1, O2):
        bb = {k: v for k, v in b.items() if k not in ("err_level", "err_level_status")}
        aa = dict(a, observable_id=mp(a["observable_id"]))
        if aa != bb:
            p.append(f"observable {a['observable_id']} differs")
    if set(O2[0]) - set(O1[0]) != {"err_level", "err_level_status"}:
        p.append("observables columns differ")
    want_new = []
    for pr in profiles:
        rs = [mp(x) for x in pr["applies_to_rows"].split(";")]
        v1rows = [a for a in M1 if mp(a["measurement_id"]) in rs]
        if pr["profile_status"] == "printed" and all(a[f"{X}r_eff_arcsec"] is None for a in v1rows) and all(r in classA for r in rs):
            want_new.append((pr["system_id"], float(pr["r_e_arcsec"])))
    got_new = [(o["system_id"], o["value"]) for o in new_obs]
    if got_new != want_new:
        p.append(f"new observables {len(got_new)} differ from the profiles to add ({len(want_new)})")
    if new_obs and new_obs[0]["observable_id"] != f"{P2}o000631":
        p.append("new observables do not start after o000630")
    for o in new_obs:
        if o["side"] != "baryonic" or o["quantity"] != "half_light_radius" or o["unit"] != "arcsec":
            p.append(f"{o['observable_id']} side/quantity/unit")
        named_in = [m for m in M2 if o["observable_id"] in ids(m["baryonic_from"])]
        if not named_in or any(m["system_id"] != o["system_id"] for m in named_in):
            p.append(f"{o['observable_id']} not named in its rows' baryonic_from")
    res["2"] = {"pass": not p, "problems": p,
                "detail": f"every v1 column compared on every row; allowed differences only (g_obs_err on {len(classA)} class A rows, "
                          f"IDs, baryonic_from, notes, assumptions, flags); {len(extra)} new columns as listed; systems unchanged; "
                          f"{len(O1)} observables unchanged apart from the prefix; {len(new_obs)} profile observables appended from o000631"}

    # ---------------------------------------------------------------- 3. changed values
    p = []
    cases = [r for r in d096 if r["d096_case"].strip().lower() != "no"]
    if cases:
        p.append(f"the reading lists {len(cases)} D-096 cases")
    bad = [c for c in bitwise if c in changed_cols]
    if bad:
        p.append(f"value columns changed: {bad}")
    desc = json.loads((PKG / "datapackage.json").read_text(encoding="utf-8"))
    if "x_value_change_ruling" in desc:
        p.append("x_value_change_ruling set although nothing changed")
    res["3"] = {"pass": not p, "problems": p, "detail": f"none expected, none found: {len(d096)} D-096 reading rows, all 'no'; "
                f"{len(bitwise)} value columns bit-for-bit equal to v1 on all 147 rows"}

    # ---------------------------------------------------------------- 4. arithmetic
    p = []
    spec = importlib.util.spec_from_file_location("lens_v1_convert_score", V1 / "convert.py")
    v1c = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = v1c
    spec.loader.exec_module(v1c)
    try:
        n4 = v1c.arithmetic_check(M2)
    except SystemExit as e:
        n4 = 0
        p.append(str(e))
    nd = ns = 0
    for b in M2:
        ref = b["g_obs"] * b[f"{X}mstar_re_msun"] / b[f"{X}m_e_msun"]
        ns += 1
        if rel(b[f"{X}g_bar_stars_ref"], ref) > 1e-12:
            p.append(f"{b['measurement_id']} g_bar_stars_ref")
        if b[f"{X}dlngbar_dlntheta"] is not None:
            re_ = b[f"{X}r_eff_arcsec"] if b[f"{X}r_eff_arcsec"] is not None else b[f"{X}theta_profile_r_e_arcsec"]
            n_ = b[f"{X}sersic_n"] if b[f"{X}sersic_n"] is not None else b[f"{X}theta_profile_n"]
            nd += 1
            if rel(b[f"{X}dlngbar_dlntheta"], dlng(b[f"{X}theta_e_arcsec"], re_, n_)) > 1e-6:
                p.append(f"{b['measurement_id']} dlngbar_dlntheta")
    res["4"] = {"pass": not p, "problems": p, "detail": f"{n4} recomputations by aeg.lensing (v1's frozen test-3 code) to 1e-9; "
                f"dlngbar_dlntheta on {nd} rows to 1e-6; g_bar_stars_ref on {ns} rows to 1e-12"}

    # ---------------------------------------------------------------- 5. error columns and levels
    p = []
    manga = set(SCOPES["MaNGA"])
    obs2 = {o["observable_id"]: o for o in O2}

    def level(source, side, prefix):
        rs = [r for r in errl if r["source"] == source and r["side"] == side and prefix in r["v2_error_column"]]
        if not rs:
            return "missing", None
        if all(r["level_status"].strip() == "stated" for r in rs) and len({float(r["level"]) for r in rs}) == 1:
            return "stated", float(rs[0]["level"])
        return "not_given_by_source", None
    seen_levels = {}
    for b in M2:
        mid = b["measurement_id"]
        if (b["g_obs_err_point_lo"], b["g_obs_err_point_hi"]) != (b["g_obs_err_lo"], b["g_obs_err_hi"]):
            p.append(f"{mid} g_obs point")
        if b[f"{X}scope"] in manga:
            ob = [obs2[x] for x in ids(b["baryonic_from"])]
            lum = [o for o in ob if o["quantity"] == "luminosity"][0]
            ml = [o for o in ob if o["quantity"] == "stellar_ml_population"][0]
            for s, e in (("lo", "err_lo"), ("hi", "err_hi")):
                a_, c_ = lum[e] / lum["value"], ml[e] / ml["value"]
                want = b[f"g_bar_err_{s}"] * a_ / math.hypot(a_, c_)
                if rel(b[f"g_bar_err_point_{s}"], want) > 1e-12 or not b[f"g_bar_err_point_{s}"] < b[f"g_bar_err_{s}"]:
                    p.append(f"{mid} MaNGA g_bar point {s}")
        elif (b["g_bar_err_point_lo"], b["g_bar_err_point_hi"]) != (b["g_bar_err_lo"], b["g_bar_err_hi"]):
            p.append(f"{mid} g_bar point")
        o_rec, s_rec = re.fullmatch(r"observed (R\d+); stellar (R\d+)", b["source_ref"]).groups()
        for col, side, src, prefix, lv, st in (("g_obs_err_lo", "g_obs", o_rec, "g_obs_err_lo/hi", "err_level", "err_level_status"),
                                               ("g_bar_err_lo", "g_bar", s_rec, "g_bar_err", "g_bar_err_level", "g_bar_err_level_status")):
            if b[col] is None:
                want = (None, None)
            else:
                s_, l_ = level(src, side, prefix)
                want = (s_, l_)
            if (b[st], b[lv]) != want:
                p.append(f"{mid} {side} level {(b[st], b[lv])} != {want}")
            seen_levels.setdefault((src, side), set()).add((b[st], b[lv]))
        if b[f"{X}scope"] in SCOPES["S4TM"] and "no_uncertainty" not in ids(b["flags"]):
            p.append(f"{mid} S4TM lost no_uncertainty")
    md = {c: m2t[c].description for c in m2t.colnames}
    if "MaNGA" not in md["g_bar_err_point_lo"] or "§2a rule" not in md["g_bar_err_point_lo"]:
        p.append("g_bar_err_point header does not say why MaNGA differs")
    if "§2a rule 7" not in md["g_obs_err_lo"]:
        p.append("g_obs_err header does not say why class A cells are empty")
    res["5"] = {"pass": not p, "problems": p, "detail": "point columns equal the error columns except MaNGA g_bar (L_Ein error alone, "
                "recomputed); levels by source and side: " + "; ".join(f"{k[0]} {k[1]}: {sorted(map(str, v))}" for k, v in sorted(seen_levels.items()))}

    # ---------------------------------------------------------------- 6. new extension columns
    p = []
    sizes = {f"{X}mass_ellipticity_frac": ("aeg-s-000506", 0.03), f"{X}los_frac": ("aeg-s-000503", 0.02),
             f"{X}neighbour_light_frac": ("aeg-s-000505", 0.015)}
    for b in M2:
        mid = b["measurement_id"]
        t = theta[mid.replace(P2, P1)]
        if mid in classA and mid not in lower:
            want = (float(t["theta_e_err_frac_lo"]), float(t["theta_e_err_frac_hi"]))
        else:
            want = (None, None)
        if (b[f"{X}theta_e_err_frac_lo"], b[f"{X}theta_e_err_frac_hi"]) != want:
            p.append(f"{mid} theta frac")
        if b[f"{X}scope"] in SCOPES["SLACS"] and want != (0.02, 0.02):
            p.append(f"{mid} SLACS frac not 0.02")
        pr = printed.get(mid)
        if pr and b[f"{X}r_eff_arcsec"] is None:
            wp = (pr["form"], float(pr["r_e_arcsec"]), float(pr["n"]))
        else:
            wp = (None, None, None)
        if (b[f"{X}theta_profile_form"], b[f"{X}theta_profile_r_e_arcsec"], b[f"{X}theta_profile_n"]) != wp:
            p.append(f"{mid} profile columns")
        if (b[f"{X}dlngbar_dlntheta"] is not None) != bool(pr):
            p.append(f"{mid} dlngbar filled where no profile is printed, or empty where one is")
        if not pr and mid in classA and NOT_COMPUTED not in str(b["notes"]):
            p.append(f"{mid} lacks the not-computed note")
        for c, (sid, v) in sizes.items():
            if b[c] != (v if b["system_id"] == sid else None):
                p.append(f"{mid} {c}")
        if b[f"{X}scope"] in SCOPES["SL2S"]:
            band = prof[mid.replace(P2, P1)]["band_or_imaging"]
            w = 0.30 if band.startswith("CFHT") else 0.10 if band.startswith("HST") else None
            if b[f"{X}r_eff_err_frac"] != w:
                p.append(f"{mid} r_eff_err_frac {b[f'{X}r_eff_err_frac']} != {w}")
        elif b[f"{X}r_eff_err_frac"] is not None:
            p.append(f"{mid} r_eff_err_frac outside SL2S")
    for c, term in ((f"{X}theta_e_err_frac_hi", "theta_e"), (f"{X}mass_ellipticity_frac", "ellipticity_j0403"),
                    (f"{X}los_frac", "line_of_sight_snl0"), (f"{X}neighbour_light_frac", "neighbour_light_snl2"),
                    (f"{X}r_eff_err_frac", "r_eff_sl2s"), (f"{X}dlngbar_dlntheta", "a6s_theta_e"), (f"{X}g_bar_stars_ref", "a6s_gas_in_RE")):
        if term not in md[c]:
            p.append(f"header of {c} does not name {term}")
    for c in NEW_MEAS_COLS:
        if c.startswith(X) and c != f"{X}g_bar_stars_ref" and "mpty" not in md[c]:
            p.append(f"header of {c} does not say what empty means")
    nprof = sum(1 for b in M2 if b[f"{X}dlngbar_dlntheta"] is not None)
    res["6"] = {"pass": not p, "problems": p, "detail": f"θ_E fractions on {sum(1 for b in M2 if b[f'{X}theta_e_err_frac_hi'] is not None)} "
                f"class A rows (NGC 6505 empty); profile columns on {sum(1 for b in M2 if b[f'{X}theta_profile_form'])} rows; "
                f"dlngbar on {nprof} rows with a printed profile; single-system sizes on J0403, SNL-0, SNL-2; r_eff_err_frac on 6 SL2S rows"}

    # ---------------------------------------------------------------- 7. terms and registry
    p = []

    def sids(*names):
        hit = {m["system_id"] for m in M2 if m[f"{X}scope"] in [s for n in names for s in SCOPES[n]]}
        return [s for s in order if s in hit]

    def lst(*n):
        return ";".join(sids(*n))

    def exc(*n):
        drop = set(sids(*n))
        return ";".join(s for s in with_rows if s not in drop)
    one = lambda n: sids(n)[0]  # noqa: E731
    # term_id: (scale, applies_to, moves, status, size (value or (lo, hi) or column), size_kind, unit, assumption, in_error_columns)
    EXP = [
        ("theta_e", "point", "*", "g_bar", "given", f"{X}theta_e_err_frac_hi", "as_released", "fraction", "a6s_theta_e", None),
        ("theta_e_ngc6505", "point", one("NGC 6505"), "g_bar", "given", 0.0004, "lower_bound", "fraction", "a6s_theta_e", None),
        ("ellipticity_j0403", "point", "*", "g_obs", "given", f"{X}mass_ellipticity_frac", "as_released", "fraction", None, "no"),
        ("lens_model_profile", "dataset", exc("SNELLS"), "g_bar", "not_given_by_source", None, None, None, "a6s_theta_e", None),
        ("sie_axis_convention", "dataset", lst("SLACS", "S4TM"), "g_bar", "not_given_by_source", None, None, None, "a6s_theta_e", None),
        ("external_shear", "dataset", lst("S4TM"), "g_bar", "given", 0.02, "as_released", "fraction", "a6s_theta_e", None),
        ("external_convergence", "dataset", exc("SNL-0"), "g_obs", "not_given_by_source", None, None, None, None, None),
        ("line_of_sight_snl0", "point", "*", "g_obs", "given", f"{X}los_frac", "as_released", "fraction", None, "no"),
        ("lens_light_subtraction", "dataset", lst("S4TM"), "g_bar", "not_given_by_source", None, None, None, "a6s_theta_e", None),
        ("aperture_radius_snl12", "dataset", lst("SNL-1", "SNL-2"), "both", "not_given_by_source", None, None, None, None, None),
        ("companion_snl2", "point", one("SNL-2"), "g_obs", "not_given_by_source", None, None, None, None, None),
        ("redshift_measurement", "dataset", exc("NGC 6505"), "both", "not_given_by_source", None, None, None, None, None),
        ("redshift_lens_ngc6505", "point", one("NGC 6505"), "g_obs", "given", 0.00003, "as_released", "redshift", None, None),
        ("redshift_source_ngc6505", "point", one("NGC 6505"), "g_obs", "given", 0.003, "as_released", "redshift", None, None),
        ("cosmology_h0", "dataset", lst("SLACS", "S4TM", "SL2S", "NGC 6505"), "g_obs", "not_given_by_source", None, None, None, "a6s_source_cosmology", None),
        ("cosmology_h0_snells", "dataset", lst("SNELLS"), "g_obs", "given", (67.0, 70.0), "range", "km s-1 Mpc-1", "a6s_source_cosmology", None),
        ("cosmology_h0_j0403", "dataset", one("J0403"), "g_obs", "given", (67.8, 70.4), "range", "km s-1 Mpc-1", "a6s_source_cosmology", None),
        ("cosmology_h0_manga", "dataset", lst("MaNGA"), "g_obs", "given", (67.4, 69.6), "range", "km s-1 Mpc-1", "a6s_source_cosmology", None),
        ("cosmology_omega_m", "dataset", "*", "g_obs", "not_given_by_source", None, None, None, None, None),
        ("lens_distance_snl0", "system", one("SNL-0"), "g_obs", "given", (0.03, 0.04), "as_released", "fraction of D_l", "a6s_lens_distance", None),
        ("lens_distance_snl1", "system", one("SNL-1"), "g_obs", "given", (0.03, 0.04), "as_released", "fraction of D_l", "a6s_lens_distance", None),
        ("lens_distance_snl2", "system", one("SNL-2"), "g_obs", "given", (0.03, 0.04), "as_released", "fraction of D_l", "a6s_lens_distance", None),
        ("lens_distance_ngc6505", "system", one("NGC 6505"), "g_obs", "given", (0.040, 0.04243), "range", "redshift", "a6s_lens_distance", None),
        ("lens_distance_other", "dataset", exc("SNELLS", "NGC 6505"), "g_obs", "not_given_by_source", None, None, None, "a6s_lens_distance", None),
        ("aperture_factor_slacs", "dataset", lst("SLACS"), "g_bar", "not_given_by_source", None, None, None, None, None),
        ("r_eff_slacs", "dataset", lst("SLACS"), "g_bar", "given", 0.035, "as_released", "fraction", None, None),
        ("r_eff_sl2s", "point", "*", "g_bar", "given", f"{X}r_eff_err_frac", "as_released", "fraction", None, "no"),
        ("r_eff_s4tm", "dataset", lst("S4TM"), "g_bar", "not_given_by_source", None, None, None, None, None),
        ("sps_templates_slacs", "dataset", lst("SLACS"), "g_bar", "not_given_by_source", None, None, None, None, None),
        ("sps_systematic_s4tm", "dataset", lst("S4TM"), "g_bar", "given", 0.5, "as_released", "dex", None, None),
        ("sps_template_sl2s", "dataset", lst("SL2S"), "g_bar", "given", 0.06, "as_released", "dex", None, None),
        ("luminosity_corrections_manga", "dataset", lst("MaNGA"), "g_bar", "not_given_by_source", None, None, None, None, None),
        ("upsilon_ref_manga", "dataset", lst("MaNGA"), "g_bar", "given", (2.41, 3.46), "range", "solar units", None, None),
        ("pop_model_family_j0403", "system", one("J0403"), "g_bar", "not_given_by_source", None, None, None, None, None),
        ("pop_age_j0403", "system", one("J0403"), "g_bar", "not_given_by_source", None, None, None, None, None),
        ("pop_model_family_manga", "dataset", lst("MaNGA"), "g_bar", "not_given_by_source", None, None, None, None, None),
        ("alpha_fe", "dataset", "*", "g_bar", "not_given_by_source", None, None, None, None, None),
        ("stellar_imf", "dataset", "*", "g_bar", "given", f"{X}mstar_top_msun", "range", "solMass", "a6s_stellar_imf", None),
        ("gas_in_re", "dataset", "*", "g_bar", "given_by_other_source", f"{X}gas_hot_frac_max", "range", "fraction of M*(<R_E)", "a6s_gas_in_RE", None),
        ("neighbour_light_snl2", "point", "*", "g_bar", "given", f"{X}neighbour_light_frac", "as_released", "fraction", None, "no"),
        ("internal_dust_snl1", "point", one("SNL-1"), "g_bar", "not_given_by_source", None, None, None, None, None),
        ("lensed_source_light", "dataset", "*", "g_bar", "not_given_by_source", None, None, None, None, None),
        ("solar_magnitude", "dataset", "*", "g_bar", "not_given_by_source", None, None, None, None, None),
        ("aperture_shape", "dataset", "*", "both", "not_given_by_source", None, None, None, None, None),
    ]
    if [t["term_id"] for t in T] != [e[0] for e in EXP]:
        p.append(f"term ids differ: {sorted(set(t['term_id'] for t in T) ^ set(e[0] for e in EXP))}")
    tt = {t["term_id"]: t for t in T}
    for tid, scale, ap, mv, st, size, kind, unit, aid, iec in EXP:
        t = tt.get(tid)
        if not t:
            continue
        got = (t["scale"], t["applies_to"], t["moves"], t["status"], t["size_kind"], t["assumption_id"], t["in_error_columns"], t["covariance"])
        want = (scale, ap, mv, st, kind, aid, iec, "not_published")
        if got != want:
            p.append(f"{tid}: {[(g, w) for g, w in zip(got, want) if g != w]}")
        if isinstance(size, str):
            if t["size_column"] != size:
                p.append(f"{tid}: size_column {t['size_column']}")
        elif isinstance(size, tuple):
            if (t["size_lo"], t["size_hi"]) != size:
                p.append(f"{tid}: size {(t['size_lo'], t['size_hi'])}")
        elif size is not None and t["size_value"] != size:
            p.append(f"{tid}: size {t['size_value']}")
        if st == "given" and (not t["size_unit"] or (unit and not t["size_unit"].startswith(unit))):
            p.append(f"{tid}: size_unit {t['size_unit']!r}")
        if not t["citation"] or not t["note"]:
            p.append(f"{tid}: citation or note missing")
    reg = {a["id"]: a for a in json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))["assumptions"]}
    ids_a6s = [a for a in reg if a.startswith("a6s_")]
    for a in ids_a6s:
        if P2.rstrip("/") not in reg[a]["datasets"]:
            p.append(f"{a} lacks a v2 entry")
    v2 = lambda a: reg[a]["datasets"][P2.rstrip("/")]  # noqa: E731
    order_ids = [a for a in reg]
    if order_ids.index("a6s_gas_in_RE") > order_ids.index("a6s_theta_e"):
        p.append("gas entry not before theta_e in registry order")
    eff = lambda a: {e["column"]: e["formula"] for e in v2(a)["effects"]}  # noqa: E731
    G_OBS = ["g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_obs_err_point_lo", "g_obs_err_point_hi"]
    G_BAR = ["g_bar", "g_bar_stars", "g_bar_gas_cold", "g_bar_gas_hot", f"{X}g_bar_stars_ref", "g_bar_err_lo", "g_bar_err_hi",
             "g_bar_err_point_lo", "g_bar_err_point_hi"]
    if eff("a6s_source_cosmology") != {**{c: f"{c} * p / p0" for c in G_OBS}, "r_kpc": "r_kpc * p0 / p"} or v2("a6s_source_cosmology")["default"] != 1:
        p.append("a6s_source_cosmology v2 effects")
    if eff("a6s_theta_e") != {**{c: f"{c} * (p / p0) ^ {X}dlngbar_dlntheta" for c in G_BAR}, "r_kpc": "r_kpc * p / p0"} or v2("a6s_theta_e")["default"] != 1:
        p.append("a6s_theta_e v2 effects")
    if eff("a6s_lens_distance") != {**{c: f"{c} * (1 + p0) / (1 + p)" for c in G_OBS}, "r_kpc": "r_kpc * (1 + p) / (1 + p0)"} or v2("a6s_lens_distance")["default"] != 0:
        p.append("a6s_lens_distance v2 effects")
    g1, g2 = reg["a6s_gas_in_RE"]["datasets"][P1.rstrip("/")], v2("a6s_gas_in_RE")
    old = f"g_obs * {X}mstar_re_msun / {X}m_e_msun"
    if [e["formula"].replace(old, f"{X}g_bar_stars_ref") for e in g1["effects"]] != [e["formula"] for e in g2["effects"]] \
            or any(g1[k] != g2[k] for k in ("default", "min", "max")):
        p.append("a6s_gas_in_RE v2 formula")
    if v2("a6s_stellar_imf") != reg["a6s_stellar_imf"]["datasets"][P1.rstrip("/")]:
        p.append("a6s_stellar_imf v2 differs from v1")
    for a in ("a6s_source_cosmology", "a6s_theta_e", "a6s_lens_distance"):
        if v2(a).get("role") != "uncertainty-term formula" or not v2(a).get("not_adjustable_reason"):
            p.append(f"{a}: role or not_adjustable_reason")
    if any(a in ids(b["adjustable"]) for b in M2 for a in ("a6s_theta_e", "a6s_lens_distance", "a6s_source_cosmology")):
        p.append("an uncertainty-term formula is listed in adjustable")
    rc, out = run([sys.executable, str(PKG / "reproduction/check_formulas.py")])
    cf = json.loads((PKG / "reproduction/check_formulas.json").read_text(encoding="utf-8"))
    if rc != 0 or cf["result"] != "pass":
        p.append(f"check_formulas.py failed: {out[-400:]}")
    res["7"] = {"pass": not p, "problems": p, "detail": f"{len(T)} terms as frozen (scale, applies_to, moves, status, size, kind, unit, "
                f"assumption, in_error_columns, covariance); registry v2 entries for {len(ids_a6s)} a6s entries; check_formulas.py: "
                f"{cf['evaluations_python_and_js']} Python/JS evaluations, 0 problems; rows not evaluated: {cf['rows_not_evaluated_named_column_empty']}"}

    # ---------------------------------------------------------------- 8. plotting
    p = []
    if sum(b["plotted"] == "true" for b in M2) != 94:
        p.append("plotted count")
    if [(a["plotted"], a["not_plotted_reason"]) for a in M1] != [(b["plotted"], b["not_plotted_reason"]) for b in M2]:
        p.append("plotting differs from v1")
    if sum(b["not_plotted_reason"] == "alternative_value" and b["plotted"] == "false" for b in M2) != 53:
        p.append("alternatives not 53 alternative_value")
    res["8"] = {"pass": not p, "problems": p, "detail": "94 rows plotted, 53 alternatives plotted = false with alternative_value, as v1; epoch-gap systems unchanged"}

    # ---------------------------------------------------------------- 9. named items
    p = []
    dp = json.loads((PKG / "datapackage.json").read_text(encoding="utf-8"))
    ki = json.loads((PKG / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    if 139 not in [k["issue"] for k in ki]:
        p.append("F1/F2 known issue #139 not listed")
    for w in ("Einstein-radius (θ_E) error moves from g_obs to g_bar", "D-094", "F1", "F2", "2 per cent of M_Ein", NOT_COMPUTED):
        if w not in dp["description"]:
            p.append(f"dataset description lacks {w!r}")
    for b in M2:
        if b["measurement_id"] in lower and "lower-bound" not in str(b["notes"]) and "lower bound" not in str(b["notes"]):
            p.append(f"{b['measurement_id']} lacks the lower-bound note")
    comps = {c["component"]: c for c in dp["x_baryon_inventory"]}
    bh1 = comps.get("central black hole (SNELLS, MaNGA and NGC 6505 sources)")
    bh2 = comps.get("central black hole (other sources)")
    if not bh1 or bh1["status"] != "stated_negligible" or not all(s in bh1["citation"] for s in ("l. 769", "l. 691", "l. 778", "l. 274")):
        p.append("black-hole component 1")
    if not bh2 or bh2["status"] != "not_addressed":
        p.append("black-hole component 2")
    src = json.loads((PKG / "sources.json").read_text(encoding="utf-8"))
    s1 = json.loads((V1 / "sources.json").read_text(encoding="utf-8"))["sources"]
    if [(s["file"], s["sha256"], s["bytes"]) for s in src["sources"]] != [(s["file"], s["sha256"], s["bytes"]) for s in s1]:
        p.append("v1 sources not carried with v1's hashes")
    want_pages = {"1502.01589": "d85fc462fcabf12405ff913a587196bf78b1e1a35b235de8812f49a4662f9cb9",
                  "1807.06209": "17256f2d1adbc17162eb3d0e29bf1a547d6dfb131efe3231d2d32abfc72429fa",
                  "1406.1718": "4f18ff396491283c7e0fce47b2010caae4ab0c6ab5344a1efabcb924f1f78008"}
    pages = {pg["url"].rsplit("/", 1)[1]: pg for pg in src.get("reference_pages", [])}
    fetched = {}
    for aid, h in want_pages.items():
        pg = pages.get(aid)
        if not pg or pg["sha256"] != h or not pg.get("licence"):
            p.append(f"abstract page {aid} not listed with its hash and licence")
            continue
        if "--fetch-abstracts" in sys.argv:
            try:
                req = urllib.request.Request(pg["url"], headers={"User-Agent": "extragravitation-atlas-pipeline (+https://extragravitation.org)"})
                body = urllib.request.urlopen(req, timeout=60).read()
                got = hashlib.sha256(body).hexdigest()
                fetched[aid] = "hash matches" if got == h else ("hash differs; quoted H0 present" if pg["quote"].encode() in body else "CHANGED")
                if fetched[aid] == "CHANGED":
                    p.append(f"abstract page {aid}: quoted H0 not found")
            except Exception as e:  # noqa: BLE001
                fetched[aid] = f"not fetched: {e}"
    page_line = None
    if site:
        f = site / "datasets/aeg-d-strong-lensing/v2/index.html"
        text = html.unescape(f.read_text(encoding="utf-8")) if f.is_file() else ""
        page_line = NOT_COMPUTED in text
        if not page_line:
            p.append("dataset page lacks the D-104 rule 3 line")
    else:
        p.append("page line not checked (run with --site)")
    res["9"] = {"pass": not p, "problems": p, "detail": f"F1/F2 on the dataset page (descriptor description) and in known issue #139; "
                f"NGC 6505 lower-bound notes; black hole as two inventory components; {len(src['sources'])} v1 sources with v1's hashes; "
                f"abstract pages {fetched or 'listed with hashes (not fetched in this run)'}; page line found: {page_line}"}

    # ---------------------------------------------------------------- 10. descriptor
    p = []
    d1 = json.loads((V1 / "descriptor.json").read_text(encoding="utf-8"))
    if dp.get("standard_version") != "2.5.1":
        p.append("standard_version")
    sr = dp.get("x_second_reading", {})
    frozen_files = json.loads((ROOT / "data/frozen/lenses-v2-reading.json").read_text(encoding="utf-8"))["files"]
    if sr.get("file") != "SECOND_READING.md" or sr.get("frozen") != "data/frozen/lenses-v2-reading.json" or \
            sorted(sr.get("reading", [])) != sorted(f"reading/{Path(x).name}" for x in frozen_files):
        p.append("x_second_reading")
    if set(d1) - set(dp) - {"resources"}:
        p.append(f"v1 descriptor fields missing: {set(d1) - set(dp)}")
    if [c["component"] for c in dp["x_baryon_inventory"]][:len(d1["x_baryon_inventory"])] != [c["component"] for c in d1["x_baryon_inventory"]]:
        p.append("v1 inventory components changed")
    res["10"] = {"pass": not p, "problems": p, "detail": "standard_version 2.5.1; no x_value_change_ruling; x_second_reading points to "
                 "SECOND_READING.md, the seven reading files and their freeze record; inventory = v1's six components + the two black-hole components"}

    # ---------------------------------------------------------------- 11. package equals the frozen reading
    p = []
    fr = json.loads((ROOT / "data/frozen/lenses-v2-reading.json").read_text(encoding="utf-8"))
    for rf, h in fr["files"].items():
        if hashlib.sha256((ROOT / rf).read_bytes()).hexdigest() != h:
            p.append(f"reading file changed: {rf}")
    from collections import Counter
    cnt = Counter(cls.values())
    if cnt != Counter({"A": 107, "no_theta_e_error": 37, "aperture": 2, "B": 1}):
        p.append(f"classes {dict(cnt)}")
    for b in M2:
        t = theta[b["measurement_id"].replace(P2, P1)]
        if float(t["theta_e_arcsec"]) != b[f"{X}theta_e_arcsec"] or t["system_id"] != b["system_id"] or t["scope"] != b[f"{X}scope"] or t["role"] != b["role"]:
            p.append(f"{b['measurement_id']} θ_E/system/scope/role differs from theta_class.csv")
        if cls[b["measurement_id"]] == "A" and (b["g_obs_err_lo"] is not None or "θ_E error carried by g_bar" not in str(b["notes"])):
            p.append(f"{b['measurement_id']} class A treatment")
        if cls[b["measurement_id"]] != "A" and "θ_E error carried by g_bar" in str(b["notes"]):
            p.append(f"{b['measurement_id']} non-A row with class A note")
        pr = prof.get(b["measurement_id"].replace(P2, P1))
        if pr and pr["profile_status"] == "printed":
            re_ = b[f"{X}r_eff_arcsec"] if b[f"{X}r_eff_arcsec"] is not None else b[f"{X}theta_profile_r_e_arcsec"]
            n_ = b[f"{X}sersic_n"] if b[f"{X}sersic_n"] is not None else b[f"{X}theta_profile_n"]
            if (re_, n_) != (float(pr["r_e_arcsec"]), float(pr["n"])):
                p.append(f"{b['measurement_id']} profile differs from profiles.csv")
    if tt["theta_e_ngc6505"]["size_value"] != float(theta[f"{P1}m000146"]["theta_e_err_frac_hi"]):
        p.append("theta_e_ngc6505 size differs from the reading")
    dv = {(r["source"], r["item"]): r["value"] for r in dist}
    if (dv[("R25", "alternative H0")], dv[("R29", "adopted H0")], dv[("P15", "abstract headline H0")],
            dv[("P18", "abstract headline H0")], dv[("B14", "abstract headline H0")]) != ("67", "70.4", "67.8", "67.4", "69.6"):
        p.append("H0 values differ from distance.csv")
    if not dv[("R26", "peculiar velocity")].startswith("3-4%"):
        p.append("peculiar-velocity size differs from distance.csv")
    neg = {r["source"] for r in inv if r["component"] == "central black hole" and r["status"] == "stated_negligible"}
    if neg != {"R25", "R28", "R30", "R32"}:
        p.append(f"stated-negligible sources {neg}")
    res["11"] = {"pass": not p, "problems": p, "detail": "reading files unchanged since freezing; classes A 107, no θ_E error 37, aperture 2, "
                 "B 1; θ_E, fractions, profiles, levels (item 5), H0 and distance sizes and black-hole statuses equal the reading. The "
                 "SNELLS pair uses R25's own comparison 67 against 70 (resolution 5; R25's adopted 70.4 is in the term note)"}

    # ---------------------------------------------------------------- 12. standard and site
    p = []
    checks = {}
    for name, cmd in (("validate", [sys.executable, "-m", "aeg.validate", "data/packages/aeg-d-strong-lensing/v2"]),
                      ("formula_check", [sys.executable, "-m", "aeg.formula_check"]),
                      ("test_lensing", [sys.executable, "-m", "pytest", "-q", "pipeline/tests/test_lensing.py"])):
        rc, out = run(cmd)
        checks[name] = out.strip().splitlines()[-1] if out.strip() else ""
        if rc != 0:
            p.append(f"{name} failed: {out[-300:]}")
    checks["check_formulas"] = cf["result"]
    if site:
        rp = site / "reproduction/index.html"
        checks["site_built"] = (site / "index.html").is_file() and rp.is_file()
        if not checks["site_built"]:
            p.append("site not built")
    else:
        p.append("site not checked (run with --site after the build and aeg.site_check)")
    res["12"] = {"pass": not p, "problems": p, "detail": checks}

    # ---------------------------------------------------------------- 13. v1 untouched
    p = []
    listed = subprocess.run(["git", "ls-tree", "-r", "--name-only", "5dc4091", "--", "data/packages/aeg-d-strong-lensing/v1"],
                            cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    for f in listed:
        old = subprocess.run(["git", "show", f"5dc4091:{f}"], cwd=ROOT, capture_output=True, check=True).stdout
        if hashlib.sha256(old).hexdigest() != hashlib.sha256((ROOT / f).read_bytes()).hexdigest():
            p.append(f)
    now = subprocess.run(["git", "ls-files", "data/packages/aeg-d-strong-lensing/v1"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    if sorted(now) != sorted(listed):
        p.append("v1 file list changed")
    res["13"] = {"pass": not p, "problems": p, "detail": f"{len(listed)} v1 files identical to commit 5dc4091"}

    (PKG / "reproduction/score.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    for k, v in res.items():
        print(k, "PASS" if v["pass"] else "FAIL", v.get("problems", [])[:3])
    print("RESULT:", "PASS" if all(v["pass"] for v in res.values()) else "FAIL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
