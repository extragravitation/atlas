"""Score aeg-d-dwarfs/v2 against its frozen REPRODUCTION.md, items 1 to 11 and 13 (item 12's site checks
are run separately and recorded in REPRODUCTION_RESULT.md).

Usage (repository root): python data/packages/aeg-d-dwarfs/v2/reproduction/score.py > data/packages/aeg-d-dwarfs/v2/reproduction/score.json

Each item is scored mechanically and reported with its evidence. Nothing here changes the package.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from astropy.table import Table

ROOT = Path(__file__).resolve().parents[5]
V1, V2 = ROOT / "data/packages/aeg-d-dwarfs/v1", ROOT / "data/packages/aeg-d-dwarfs/v2"
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg.formula import apply_assumption  # noqa: E402

sys.path.insert(0, str(V2))
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("conv2", V2 / "convert.py")
conv2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conv2)

REF = "5dc4091"
CHANGED = {"aeg-s-000394", "aeg-s-000381"}  # filled from conversion_changes.json below and checked against the reading
G, PC, M_SUN = 6.67430e-11, 3.0856775814913673e16, 1.98840987e30


def rows(t):
    return conv2.vals(t)


def git_show(path):
    return subprocess.run(["git", "show", f"{REF}:{path}"], cwd=ROOT, capture_output=True, check=True).stdout


def same(a, b):
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, float) or isinstance(b, float):
        return float(a) == float(b)
    return a == b


def main() -> int:
    out = {}
    m1, o1, s1 = (Table.read(V1 / f"tables/{n}.ecsv", format="ascii.ecsv") for n in ("measurements", "observables", "systems"))
    m2, o2, s2 = (Table.read(V2 / f"tables/{n}.ecsv", format="ascii.ecsv") for n in ("measurements", "observables", "systems"))
    terms = Table.read(V2 / "tables/uncertainty_terms.ecsv", format="ascii.ecsv")
    M1, O1, S1, M2, O2, S2, T = rows(m1), rows(o1), rows(s1), rows(m2), rows(o2), rows(s2), rows(terms)
    reading = list(csv.DictReader(open(V2 / "reading/resolved.csv", encoding="utf-8")))
    rd = {}
    for r in reading:
        rd.setdefault((r["system_id"], r["field"]), []).append(r)
    ch = json.loads((V2 / "reading/conversion_changes.json").read_text(encoding="utf-8"))
    changed = {c["system_id"] for c in ch["changes"]}
    defaults = M2[:64]
    by2 = {m["system_id"]: m for m in defaults}

    # item 1
    ok1 = len(M2) >= 64 and all(a["system_id"] == b["system_id"] and a["measurement_id"].split("/")[-1] == b["measurement_id"].split("/")[-1]
                                for a, b in zip(M1, defaults))
    app = M2[64:]
    ok1 &= all(a["measurement_id"] == f"aeg-d-dwarfs/v2/m{65 + i:06d}" and a["role"] == "alternative" for i, a in enumerate(app))
    r_diff = [b["system_id"] for a, b in zip(M1, defaults) if not same(a["r_kpc"], b["r_kpc"])]
    ok1 &= set(r_diff) <= changed
    out["1"] = {"pass": bool(ok1), "rows_v1": len(M1), "rows_v2": len(M2), "appended": [a["measurement_id"] for a in app],
                "r_kpc_differs_on": r_diff}

    # item 2: measurements
    gcols = ["g_obs", "g_bar", "g_bar_stars", "g_bar_gas_cold", "g_obs_err_lo", "g_obs_err_hi", "g_bar_err_lo", "g_bar_err_hi"]
    allowed = {"plotted", "not_plotted_reason", "notes", "role", "alternative_of", "assumptions", "flags", "x_dwarfs_flags",
               "measurement_id", "observed_from", "baryonic_from"}
    new_allowed = {"g_bar_err_point_lo", "g_bar_err_point_hi", "err_level", "err_level_status", "g_bar_err_level",
                   "g_bar_err_level_status", "x_dwarfs_binary_screening", "x_dwarfs_rh_err_lo_arcmin", "x_dwarfs_rh_err_hi_arcmin",
                   "x_dwarfs_ellipticity", "x_dwarfs_ellipticity_err_lo", "x_dwarfs_ellipticity_err_hi", "x_dwarfs_eps_used",
                   "x_dwarfs_rh_semimajor_assumed", "x_dwarfs_distance_err_lo_kpc", "x_dwarfs_distance_err_hi_kpc",
                   "x_dwarfs_gbar_stars_distance_exponent", "alternative_of"}
    new_cols = set(m2.colnames) - set(m1.colnames)
    g_bad, other_bad, id_bad = [], [], []
    for a, b in zip(M1, defaults):
        if a["measurement_id"].replace("/v1/", "/v2/") != b["measurement_id"]:
            id_bad.append(b["measurement_id"])
        if b["system_id"] in changed:
            continue
        for c in gcols:
            if not same(a[c], b[c]):
                g_bad.append((b["measurement_id"], c))
        for c in m1.colnames:
            if c in gcols or c in allowed:
                continue
            if not same(a[c], b[c]):
                other_bad.append((b["measurement_id"], c))
        if a["observed_from"].replace("/v1/", "/v2/") != b["observed_from"] or a["baryonic_from"].replace("/v1/", "/v2/") != b["baryonic_from"]:
            other_bad.append((b["measurement_id"], "observed_from/baryonic_from"))
        if a["role"] != b["role"]:
            other_bad.append((b["measurement_id"], "role"))
    # alternatives: g columns bit-equal to the v1 default of their system
    v1_by = {m["system_id"]: m for m in M1}
    alt_bad = [(a["measurement_id"], c) for a in app for c in gcols + ["r_kpc", "x_dwarfs_sigma", "x_dwarfs_R_h_arcmin"]
               if not same(v1_by[a["system_id"]][c], a[c])]
    # item 2a: observables
    ob_bad = []
    for a, b in zip(O1, O2):
        if a["observable_id"].replace("/v1/", "/v2/") != b["observable_id"]:
            ob_bad.append((b["observable_id"], "id"))
        for c in o1.colnames:
            if c == "observable_id":
                continue
            if c in ("err_lo", "err_hi", "source_ref") and a["quantity"] in ("half_light_radius", "structural_param", "distance"):
                continue
            if not same(a[c], b[c]):
                ob_bad.append((b["observable_id"], c))
    o_new_cols = set(o2.colnames) - set(o1.colnames)
    o_appended = [(o["observable_id"], o["system_id"], o["quantity"], o["value"]) for o in O2[len(O1):]]
    ob_ok = not ob_bad and o_new_cols == {"err_level", "err_level_status"} and all(x[1] in changed for x in o_appended)
    # item 2b: systems
    excl = {e["system"] for e in ch["excluded"]}
    sys_bad = []
    for a, b in zip(S1, S2):
        for c in s1.colnames:
            if c == "properties" and (b["system_id"] in changed or b["system_id"] in excl):
                continue
            if not same(a[c], b[c]):
                sys_bad.append((b["system_id"], c))
    sys_ok = not sys_bad and set(s2.colnames) == set(s1.colnames) and len(S1) == len(S2)
    ok2 = not g_bad and not other_bad and not id_bad and not alt_bad and new_cols <= new_allowed and ob_ok and sys_ok
    out["2"] = {"pass": bool(ok2), "g_mismatch": g_bad, "other_mismatch": other_bad, "id_mismatch": id_bad,
                "alternative_mismatch": alt_bad, "new_columns": sorted(new_cols), "unexpected_new_columns": sorted(new_cols - new_allowed),
                "2a_observables": {"pass": ob_ok, "mismatch": ob_bad, "new_columns": sorted(o_new_cols), "appended": o_appended},
                "2b_systems": {"pass": sys_ok, "mismatch": sys_bad}}

    # item 3: changed values, traceable to the reading
    differ = sorted({b["system_id"] for a, b in zip(M1, defaults) if any(not same(a[c], b[c]) for c in gcols + ["r_kpc"])})
    in_reading = {r["system_id"] for r in reading if r["field"].startswith("d096") and r["resolution"] == "ruled" and "Change" in (r["note"] + r["value"])
                  or (r["field"] == "d096_conflict" and r["value"].startswith("ruled"))}
    ok3 = set(differ) == changed and changed <= in_reading
    out["3"] = {"pass": bool(ok3), "rows_whose_values_differ": differ, "listed_changes": sorted(changed),
                "reading_rows_marking_a_change": sorted(in_reading), "changes": ch["changes"]}

    # item 4: arithmetic
    worst = 0.0
    for r in M2:
        r_m = r["r_kpc"] * 1000.0 * PC
        g1 = 3.0 * (r["x_dwarfs_sigma"] * 1e3) ** 2 / r_m
        g2 = G * (0.5 * r["x_dwarfs_l_v"] * r["x_dwarfs_upsilon_v"] + r["x_dwarfs_m_gas_rh"]) * M_SUN / r_m ** 2
        worst = max(worst, abs(g1 / r["g_obs"] - 1), abs(g2 / r["g_bar"] - 1))
    out["4"] = {"pass": worst <= 1e-9, "max_relative_difference": worst}

    # item 5: error columns and levels
    p5 = []
    fold = conv2.MODULUS_FOLDED
    for m in M2:
        sid = m["system_id"]
        if sid in fold:
            em, ep = fold[sid]
            exp_lo = None if ep is None else m["g_bar_stars"] * (1 - 10 ** (-0.4 * ep))
            exp_hi = None if em is None else m["g_bar_stars"] * (10 ** (0.4 * em) - 1)
            if not (same(exp_lo, m["g_bar_err_point_lo"]) and same(exp_hi, m["g_bar_err_point_hi"])):
                p5.append((m["measurement_id"], "point errors (modulus systems)"))
        elif not (same(m["g_bar_err_point_lo"], m["g_bar_err_lo"]) and same(m["g_bar_err_point_hi"], m["g_bar_err_hi"])):
            p5.append((m["measurement_id"], "point = total"))
        lvl, st = (None, "not_given_by_source") if sid == conv2.AND_XII else conv2.parse_level(rd[(sid, "sigma_level")][0]["value"])
        if not (same(lvl, m["err_level"]) and st == m["err_level_status"]):
            p5.append((m["measurement_id"], "sigma level"))
        lvl, st = conv2.parse_level(rd[(sid, "mag_level")][0]["value"])
        if not (same(lvl, m["g_bar_err_level"]) and st == m["g_bar_err_level_status"]):
            p5.append((m["measurement_id"], "magnitude level"))
    leo = by2[conv2.LEO_T]
    p5 += [] if leo["g_bar_err_point_lo"] is None and leo["g_bar_err_point_hi"] is None else [("Leo T", "point not empty")]
    axii = by2[conv2.AND_XII]
    p5 += [] if axii["err_level"] is None and axii["err_level_status"] == "not_given_by_source" and "limit_from_1sigma_upper_error" in (axii["x_dwarfs_flags"] or "") else [("And XII", "level")]
    mods = {r["name"]: r["value"] for r in reading if r["field"] == "mv_modulus_match"}
    p5 += [] if all(v.startswith("yes") for v in mods.values()) and len(mods) == 5 else [("mv_modulus_match", mods)]
    out["5"] = {"pass": not p5, "problems": p5, "mv_modulus_match": mods,
                "levels": {"sigma_stated": sum(1 for m in M2[:64] if m["err_level_status"] == "stated"),
                           "magnitude_stated": sum(1 for m in M2[:64] if m["g_bar_err_level_status"] == "stated")}}

    # item 6: R_h, ellipticity and distance errors, against the reading and v1's structure reading
    p6, agree_v1, differ_v1 = [], 0, []
    sva = list(csv.DictReader(open(V1 / "reading/structure_values_all.csv", encoding="utf-8")))
    key_of = {s["system_id"]: json.loads(s["properties"])["lvdb_key"] for s in S1}
    ci = {r["key"]: r for r in csv.DictReader(open(V1 / "reading/conversion_inputs.csv", encoding="utf-8"))}
    oby = {o["observable_id"]: o for o in O2}
    for m in defaults:
        sid = m["system_id"]
        lo, hi = conv2.parse_err(rd[(sid, "rh_err")][0]["value"])
        bar = [oby[x] for x in m["baryonic_from"].split(";")]
        hl = [o for o in bar if o["quantity"] == "half_light_radius"][0]
        if sid == conv2.FORNAX:
            if not (hl["err_lo"] is None and m["x_dwarfs_rh_err_lo_arcmin"] is None):
                p6.append((sid, "rh"))
        elif "pc (" not in rd[(sid, "rh_err")][0]["value"]:
            fac = math.sqrt(1 - m["x_dwarfs_ellipticity"]) if m["x_dwarfs_eps_used"] == 1 else 1.0
            if not (same(hl["err_lo"], lo) and same(hl["err_hi"], hi)):
                p6.append((sid, "observable rh error"))
            if lo is not None and not (abs(m["x_dwarfs_rh_err_lo_arcmin"] - lo * fac) < 1e-12 and abs(m["x_dwarfs_rh_err_hi_arcmin"] - hi * fac) < 1e-12):
                p6.append((sid, "rh err column"))
            if lo is None and (m["x_dwarfs_rh_err_lo_arcmin"] is not None or "no_uncertainty" not in (hl["source_ref"] or "")):
                p6.append((sid, "rh none"))
        el, eh = conv2.parse_err(rd[(sid, "eps_err")][0]["value"])
        if m["x_dwarfs_eps_used"] == 1 and not (same(m["x_dwarfs_ellipticity_err_lo"], el) and same(m["x_dwarfs_ellipticity_err_hi"], eh)):
            p6.append((sid, "eps err column"))
        for c in ("x_dwarfs_rh_err", "x_dwarfs_ellipticity_err", "x_dwarfs_distance_err"):
            cl = [k for k in m if k.startswith(c) and k.endswith(("_lo", "_lo_arcmin", "_lo_kpc"))][0]
            chh = cl.replace("_lo", "_hi")
            if (m[cl] is None) != (m[chh] is None):
                p6.append((sid, f"{c} one side only"))
        # against v1's structure reading
        k = key_of[sid]
        cand = [r for r in sva if r["key"] == k and r["role"] == "structure" and r["quantity"] == "r_h"
                and conv2.v1c.num(r["value"]) is not None and abs(conv2.v1c.num(r["value"]) - float(ci[k]["rh_printed"])) < 1e-9]
        if cand and lo is not None and "pc (" not in rd[(sid, "rh_err")][0]["value"]:
            v1e = [(conv2.parse_err(f"+{c['err_plus']}/-{c['err_minus']}") if c["err_minus"] and c["err_plus"] else (None, None)) for c in cand]
            if (lo, hi) in v1e:
                agree_v1 += 1
            else:
                differ_v1.append((ci[k]["rh_printed"], sid, (lo, hi), v1e[:2]))
    out["6"] = {"pass": not p6, "problems": p6, "rh_errors_agreeing_with_v1_structure_reading": agree_v1,
                "rh_errors_differing_from_v1_structure_reading": differ_v1}

    # item 7: terms table and registry
    exp_fixed = {"half_light_radius", "ellipticity", "ellipticity_radial_variation", "rh_convention_profile", "deprojection_4_3",
                 "distance", "distance_calibration_savino", "distance_calibration_other", "velocity_error_model", "binaries",
                 "membership", "rotation", "light_weighting", "estimator_normalisation", "anisotropy_profile", "g_bar_point_leo_t",
                 "luminosity_function_martin", "luminosity_function_other", "band_transformation", "extinction", "solar_magnitude",
                 "stellar_ml", "helium_factor", "gas_inside_rhalf_aeg-s-000390", "gas_inside_rhalf_aeg-s-000393", "hi_flux",
                 "hi_limit_assumptions", "molecular_ionised_gas", "heterogeneity"}
    no_rh = {f"half_light_radius_{m['system_id']}" for m in defaults if rd[(m["system_id"], "rh_err")][0]["value"].lower().startswith("none")}
    no_eps = {f"ellipticity_{m['system_id']}" for m in defaults if m["x_dwarfs_eps_used"] == 1 and m["x_dwarfs_ellipticity_err_lo"] is None}
    no_d = {f"distance_{m['system_id']}" for m in defaults if m["x_dwarfs_distance_err_lo_kpc"] is None}
    ids = {t["term_id"] for t in T}
    exp = exp_fixed | no_rh | no_eps | no_d
    given = {t["term_id"] for t in T if t["status"] == "given"}
    p7 = []
    if ids != exp:
        p7.append(("term ids", sorted(ids ^ exp)))
    if given != {"half_light_radius", "ellipticity", "deprojection_4_3", "distance", "distance_calibration_savino", "stellar_ml"}:
        p7.append(("given set", sorted(given)))
    if any(t["covariance"] != "not_published" for t in T):
        p7.append(("covariance", None))
    reg = {a["id"]: a for a in json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))["assumptions"]}
    for aid in ("dw_equilibrium", "dw_rhalf_wolf", "dw_rh_circularised", "dw_distance", "dw_magnitude_modulus", "dw_gas_half_total",
                "dw_hi_distance_rescaled", "dw_stellar_ml", "dw_member_sample_sigma", "dw_ellipticity"):
        if aid not in reg or "aeg-d-dwarfs/v2" not in reg[aid]["datasets"]:
            p7.append(("registry", aid))
    worst7 = 0.0
    sysrow = {}
    for aid in ("dw_rhalf_wolf", "dw_distance", "dw_ellipticity", "dw_rh_circularised"):
        e = reg[aid]["datasets"]["aeg-d-dwarfs/v2"]
        p0 = e["default"]
        for m in M2:
            res = apply_assumption(m, sysrow, e["effects"], p0, p0)
            for eff in e["effects"]:
                a, b = res[eff["column"]], m[eff["column"]]
                worst7 = max(worst7, abs(a / b - 1) if b else abs(a))
    if worst7 > 1e-12:
        p7.append(("effects at default", worst7))
    # two-sided size columns filled together
    for lo, hi in (("x_dwarfs_rh_err_lo_arcmin", "x_dwarfs_rh_err_hi_arcmin"), ("x_dwarfs_ellipticity_err_lo", "x_dwarfs_ellipticity_err_hi"),
                   ("x_dwarfs_distance_err_lo_kpc", "x_dwarfs_distance_err_hi_kpc"), ("x_dwarfs_upsilon_v_low", "x_dwarfs_upsilon_v_high")):
        bad = [m["measurement_id"] for m in M2 if (m[lo] is None) != (m[hi] is None)]
        if bad:
            p7.append(("companion", lo, bad))
    out["7"] = {"pass": not p7, "problems": p7, "n_terms": len(T), "per_system": sorted(no_rh | no_eps | no_d),
                "effects_at_default_max_relative_difference": worst7}

    # item 8: plotting
    p8 = []
    cls = {sid: rd[(sid, "d097_class")][0]["value"] for sid in by2}
    reg_rows = list(csv.DictReader(open(ROOT / "data/registry/excluded.csv", encoding="utf-8")))
    reg_ds = {r["system"]: r for r in reg_rows if r["dataset"] == "aeg-d-dwarfs/v2"}
    for a, m in zip(M1, defaults):
        sid = m["system_id"]
        c = cls[sid]
        if c == "finding":
            if not (m["plotted"] == "false" and m["not_plotted_reason"] == "other" and "D-097 finding" in (m["notes"] or "")):
                p8.append((sid, "finding row"))
            r = reg_ds.get(sid)
            if not r or not r["reason"].startswith("D-097 finding: ") or not r["citation"]:
                p8.append((sid, "excluded.csv"))
            elif squash(r["reason"][len("D-097 finding: "):]) not in squash(m["notes"]):
                p8.append((sid, "excluded.csv quote not in notes"))
        elif c == "possibility":
            if not (m["plotted"] == a["plotted"] and "D-097 possibility" in (m["notes"] or "")):
                p8.append((sid, "possibility row"))
            quotes = [squash(r["quote"]) for r in rd[(sid, "d097")] if r["value"] == "possibility"]
            if not all(q in squash(m["notes"]) for q in quotes):
                p8.append((sid, "possibility quotes"))
        elif sid in CHANGED:
            pass
        elif m["plotted"] != a["plotted"] or m["not_plotted_reason"] != a["not_plotted_reason"]:
            p8.append((sid, "plotting differs from v1"))
    if set(reg_ds) != {s for s, c in cls.items() if c == "finding"}:
        p8.append(("excluded.csv set", sorted(set(reg_ds) ^ {s for s, c in cls.items() if c == "finding"})))
    for a in app:
        if not (a["plotted"] == "false" and a["not_plotted_reason"] == "alternative_value" and a["alternative_of"] == by2[a["system_id"]]["measurement_id"]):
            p8.append((a["measurement_id"], "alternative"))
    for sid in CHANGED:
        m = by2[sid]
        c = cls[sid]
        if c == "none" and m["plotted"] != "true":
            p8.append((sid, "changed row not plotted"))
    out["8"] = {"pass": not p8, "problems": p8, "findings": sorted(reg_ds), "plotted_defaults": sum(1 for m in defaults if m["plotted"] == "true")}

    # item 9
    p9 = []
    for m in M2:
        if "dw_member_sample_sigma" not in m["assumptions"].split(";") or "star_count_weighting" not in (m["flags"] or "").split(";"):
            p9.append((m["measurement_id"], "1A"))
        if m["x_dwarfs_binary_screening"] != rd[(m["system_id"], "binary_screening")][0]["value"]:
            p9.append((m["measurement_id"], "binary"))
    inherited = sum(1 for m in M2 if "distance_inherited" in (m["x_dwarfs_flags"] or "").split())
    out["9"] = {"pass": not p9, "problems": p9, "distance_inherited_count": inherited,
                "binary_screening": {k: sum(1 for m in defaults if m["x_dwarfs_binary_screening"] == k)
                                     for k in ("multi_epoch_stated", "no_multi_epoch_stated", "not_stated")},
                "note": "Every v1 row's selected σ passed D-038 1A in v1's coding (sigma_rules_rows_v3.csv status default: 18 by coverage = beyond_rh, 46 by a passing D-051 member table)"}

    # item 10
    dp = json.loads((V2 / "datapackage.json").read_text(encoding="utf-8"))
    ok10 = dp.get("standard_version") == "2.5.1" and dp.get("x_value_change_ruling") == "D-096" and m2.meta.get("standard_version") == "2.5.1"
    out["10"] = {"pass": bool(ok10), "standard_version": dp.get("standard_version"), "x_value_change_ruling": dp.get("x_value_change_ruling")}

    # item 11: package equals the hashed reading on every field it holds
    frozen = json.loads((ROOT / "data/frozen/dwarfs-v2-reading.json").read_text(encoding="utf-8"))
    hash_ok = frozen["files"]["data/packages/aeg-d-dwarfs/v2/reading/resolved.csv"] == hashlib.sha256((V2 / "reading/resolved.csv").read_bytes()).hexdigest()
    src = json.loads((V2 / "sources.json").read_text(encoding="utf-8"))
    hash_ok &= src["second_reading"]["sha256"] == frozen["files"]["data/packages/aeg-d-dwarfs/v2/reading/resolved.csv"]
    mism = [x for x in p5 if x[1] in ("sigma level", "magnitude level")] + [x for x in p9 if x[1] == "binary"] + \
           [x for x in p8 if "finding" in x[1] or "possibility" in x[1]] + ([("D-096 changes", differ)] if set(differ) != changed else [])
    stmt = {k: sum(1 for r in reading if r["field"] == "d097" and r["value"] == k) for k in ("finding", "possibility", "neither")}
    out["11"] = {"pass": hash_ok and not mism, "reading_hash_matches_freeze_record_and_sources_json": hash_ok, "mismatches": mism,
                 "d096_changes": len(changed),
                 "d097_system_classes_with_rows": {k: sum(1 for m in defaults if cls[m["system_id"]] == k) for k in ("finding", "possibility", "none")},
                 "d097_statements": stmt}

    # item 13: v1 untouched since the reference commit
    bad13 = []
    listing = subprocess.run(["git", "ls-tree", "-r", "--name-only", REF, "data/packages/aeg-d-dwarfs/v1/"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.split()
    now = subprocess.run(["git", "ls-files", "data/packages/aeg-d-dwarfs/v1/"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    for f in listing:
        if hashlib.sha256((ROOT / f).read_bytes()).hexdigest() != hashlib.sha256(git_show(f)).hexdigest():
            bad13.append(f)
    out["13"] = {"pass": not bad13 and sorted(listing) == sorted(now), "files_checked": len(listing), "changed": bad13,
                 "added_or_removed": sorted(set(listing) ^ set(now))}
    print(json.dumps(out, indent=1, default=str, ensure_ascii=False))
    return 0


def squash(s):
    return " ".join((s or "").split())


if __name__ == "__main__":
    sys.exit(main())
