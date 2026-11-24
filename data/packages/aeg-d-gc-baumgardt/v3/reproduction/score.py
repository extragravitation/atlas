"""Score aeg-d-gc-baumgardt/v2 against its frozen test, items 1-11 and 13 (REPRODUCTION.md).

Usage: python data/packages/aeg-d-gc-baumgardt/v2/reproduction/score.py [--site site/dist]

Item 12 (validator, site build, site check, ledger) is run by the commands listed in
REPRODUCTION_RESULT.md; with --site, item 8's page check reads the built site. Writes score.json.
Independent of convert.py: it re-reads v1, the frozen reading and the v2 tables, and recomputes the
D-096 change with v1's frozen code from the reading's own list of dropped bins.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from astropy.table import Table
import astropy.constants as const
import astropy.units as u

HERE = Path(__file__).resolve().parents[1]
V1 = HERE.parent / "v1"
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg import dispersion as D  # noqa: E402
from aeg.king66 import King66  # noqa: E402
from aeg.formula import apply_assumption, names, parse  # noqa: E402

P1, P2 = "aeg-d-gc-baumgardt/v1/", "aeg-d-gc-baumgardt/v2/"
G = const.G.to_value(u.m ** 3 / (u.kg * u.s ** 2))
MSUN = const.M_sun.to_value(u.kg)
PC = const.pc.to_value(u.m)
NEW_A = ["gc_distance_hb_slope", "gc_reddening", "gc_extinction_rv", "gc_rh_measured", "gc_luminosity_vt", "gc_ml_scale"]


def vals(col):
    return [None if np.ma.is_masked(v) else (v.item() if hasattr(v, "item") else v) for v in col]


def rows(t):
    c = {k: vals(t[k]) for k in t.colnames}
    return [{k: c[k][i] for k in t.colnames} for i in range(len(t))]


def rd(p):
    return Table.read(p, format="ascii.ecsv")


def mp(x):
    return None if x is None else str(x).replace(P1, P2)


def ids(s):
    return [x for x in str(s or "").split(";") if x]


def same(a, b):
    if a is None or b is None:
        return a is None and b is None or (a in ("", None) and b in ("", None))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or (np.isnan(a) and np.isnan(b))
    return a == b


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def main() -> int:
    site = None
    if "--site" in sys.argv:
        site = ROOT / sys.argv[sys.argv.index("--site") + 1]
    res: dict[str, dict] = {}
    m1, o1, s1 = rd(V1 / "tables/measurements.ecsv"), rd(V1 / "tables/observables.ecsv"), rd(V1 / "tables/systems.ecsv")
    m2, o2, s2 = rd(HERE / "tables/measurements.ecsv"), rd(HERE / "tables/observables.ecsv"), rd(HERE / "tables/systems.ecsv")
    tt = rd(HERE / "tables/uncertainty_terms.ecsv")
    M1, M2, O1, O2, S1, S2 = rows(m1), rows(m2), rows(o1), rows(o2), rows(s1), rows(s2)
    R = list(csv.DictReader((HERE / "reading/d096_d097.csv").open(encoding="utf-8")))
    LEV = {r["dataset_code"]: r for r in csv.DictReader((HERE / "reading/err_levels.csv").open(encoding="utf-8"))}
    SCR = {r["dataset_code"]: r for r in csv.DictReader((HERE / "reading/binary_screening.csv").open(encoding="utf-8"))}
    o1_by = {r["observable_id"]: r for r in O1}

    # the frozen reading
    drops = {}
    for r in R:
        if r["field"] == "d096_excluded" and r["system_id"].startswith("aeg-s-") and r["value"].startswith("Atlas computes from the same data points: yes"):
            drops[r["system_id"]] = [P1 + x for x in re.findall(r"o\d{6}", r["value"])]
    cls = {r["system_id"]: r["value"] for r in R if r["field"] == "d097_class"}
    excluded = {s for s, c in cls.items() if c == "finding"}
    possible = {s for s, c in cls.items() if c == "possibility"}
    anchors = {r["system_id"] for r in R if r["field"] == "harris_anchor" and r["value"] == "yes"}
    changed = {r["measurement_id"] for r in M1 if r["system_id"] in drops and set(drops[r["system_id"]]) & set(ids(r["observed_from"]))}
    q_of = {r["system_id"]: r for r in R if r["field"] == "d097" and r["value"] == "finding"}

    # ------------------------------------------------------------ 1. rows
    p = []
    if len(M2) != len(M1) or len(M2) != 79:
        p.append(f"{len(M2)} rows, v1 has {len(M1)}")
    for a, b in zip(M1, M2):
        if b["system_id"] != a["system_id"] or b["x_gc_baumgardt_dataset"] != a["x_gc_baumgardt_dataset"] or b["measurement_id"] != mp(a["measurement_id"]):
            p.append(f"row mismatch {a['measurement_id']}")
    res["1"] = {"pass": not p, "problems": p, "detail": f"{len(M2)} rows; IDs, systems and dataset codes match v1 row by row"}

    # ------------------------------------------------------------ 2. what may change
    p = []
    cols1 = set(m1.colnames)
    allowed_new = {"err_level", "err_level_status", "g_bar_err_level", "g_bar_err_level_status", "g_bar_err_point_lo",
                   "g_bar_err_point_hi", "x_gc_baumgardt_log_rh_err_lo", "x_gc_baumgardt_log_rh_err_hi", "x_gc_baumgardt_w0_err_lo",
                   "x_gc_baumgardt_w0_err_hi", "x_gc_baumgardt_r0_err_lo", "x_gc_baumgardt_r0_err_hi", "x_gc_baumgardt_ml_v_err",
                   "x_gc_baumgardt_vt_scatter_mag", "x_gc_baumgardt_binary_screening"}
    extra = set(m2.colnames) - cols1
    if extra - allowed_new:
        p.append(f"unexpected new columns {sorted(extra - allowed_new)}")
    if cols1 - set(m2.colnames):
        p.append(f"v1 columns missing {sorted(cols1 - set(m2.colnames))}")
    vt_ids = {r["system_id"]: r["observable_id"] for r in O2 if r["quantity"] == "apparent_magnitude"}
    value_cols = ["g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_bar", "g_bar_err_lo", "g_bar_err_hi", "g_bar_stars", "r_kpc"] + \
                 [c for c in m1.colnames if c.startswith("x_gc_baumgardt_")]
    changed_ok = {"x_gc_baumgardt_sigma", "x_gc_baumgardt_sigma_err_lo", "x_gc_baumgardt_sigma_err_hi", "x_gc_baumgardt_coverage",
                  "x_gc_baumgardt_n_bins", "g_obs", "g_obs_err_lo", "g_obs_err_hi"}
    diffs = []
    for a, b in zip(M1, M2):
        mid, sid = a["measurement_id"], a["system_id"]
        isch, isex = mid in changed, sid in excluded
        for c in m1.colnames:
            va, vb = a[c], b[c]
            if c in ("measurement_id", "alternative_of"):
                va = mp(va)
            if c == "observed_from":
                exp = ";".join(mp(x) for x in ids(va) if not (isch and x in drops.get(sid, [])))
                if vb != exp:
                    diffs.append((mid, c))
                continue
            if c == "baryonic_from":
                exp = ";".join([mp(x) for x in ids(va)] + ([vt_ids[sid]] if sid in vt_ids else []))
                if vb != exp:
                    diffs.append((mid, c))
                continue
            if c == "assumptions":
                if vb != ";".join(ids(va) + NEW_A):
                    diffs.append((mid, c))
                continue
            if c == "model_dependence":
                if vb != "none":
                    diffs.append((mid, c))
                continue
            if c == "notes" and (isex or isch or sid in possible or sid in anchors or "no_uncertainty" in ids(b["flags"])):
                if va and not str(vb or "").startswith(str(va)):
                    diffs.append((mid, "notes (v1 text not kept)"))
                continue
            if c == "flags" and "no_uncertainty" in ids(vb):
                if [f for f in ids(vb) if f != "no_uncertainty"] != ids(va):
                    diffs.append((mid, c))
                continue
            if isex and c in ("plotted", "role", "alternative_of", "not_plotted_reason"):
                continue
            if isch and c in changed_ok:
                continue
            if isch and c in ("plotted", "role", "not_plotted_reason", "alternative_of") and b["plotted"] == "false":
                continue
            if not same(va, vb):
                diffs.append((mid, c))
    if diffs:
        p.append(f"{len(diffs)} unexpected measurement differences: {diffs[:8]}")
    # systems
    if set(s2.colnames) - set(s1.colnames) != {"x_gc_baumgardt_ebv_mag"}:
        p.append(f"systems new columns {sorted(set(s2.colnames) - set(s1.colnames))}")
    ch_sys = {a["system_id"] for a in M1 if a["measurement_id"] in changed}
    for a, b in zip(S1, S2):
        for c in s1.colnames:
            if c == "properties":
                pa, pb = json.loads(a[c]), json.loads(b[c])
                keys = set(pa) | set(pb)
                for k in keys:
                    if pa.get(k) == pb.get(k):
                        continue
                    if a["system_id"] in excluded and k in ("status", "reasons_not_plotted"):
                        continue
                    if a["system_id"] in ch_sys and k == "candidates":
                        ca, cb = pa[k], pb[k]
                        bad = [d for d in set(ca) | set(cb) if ca.get(d) != cb.get(d) and d != "RV"]
                        rvbad = [kk for kk in set(ca["RV"]) | set(cb["RV"]) if ca["RV"].get(kk) != cb["RV"].get(kk)
                                 and kk not in ("coverage", "n_bins", "sigma_rms_km_s")]
                        if bad or rvbad:
                            p.append(f"{a['system_id']} candidates changed beyond RV coverage/n_bins/sigma: {bad} {rvbad}")
                        continue
                    p.append(f"{a['system_id']} properties.{k} changed")
            elif not same(a[c], b[c]):
                p.append(f"systems {a['system_id']} {c} changed")
    # observables
    n1 = len(O1)
    for a, b in zip(O1, O2[:n1]):
        for c in o1.colnames:
            va = mp(a[c]) if c == "observable_id" else a[c]
            if not same(va, b[c]):
                p.append(f"observable {a['observable_id']} {c} changed")
    newo = O2[n1:]
    order = [s["system_id"] for s in S1 if s["system_id"] in {r["system_id"] for r in M1}]
    exp_sys = [s for s in order if s in vt_ids]
    if [r["system_id"] for r in newo] != exp_sys:
        p.append("new observables not in systems-table order or not one per system with rows")
    for i, r in enumerate(newo, start=n1 + 1):
        if r["observable_id"] != f"{P2}o{i:06d}" or r["quantity"] != "apparent_magnitude":
            p.append(f"new observable {r['observable_id']} misnumbered or wrong quantity")
    if n1 != 3182:
        p.append(f"v1 has {n1} observables, test expects 3182")
    res["2"] = {"pass": not p, "problems": p[:20], "detail": f"measurements, systems and observables compared with v1 column by column; {len(newo)} new V_t observables from o{n1 + 1:06d}"}

    # ------------------------------------------------------------ 3. changed values
    p = []
    ch2 = {mp(a["measurement_id"]) for a in M1 if any(not same(a[c], b[c]) for c in ("g_obs", "x_gc_baumgardt_sigma")
                                                       for b in [M2[M1.index(a)]])}
    if ch2 != {mp(x) for x in changed}:
        p.append(f"rows with changed values {sorted(ch2)} differ from the reading's {sorted(mp(x) for x in changed)}")
    detail = []
    for a in M1:
        if a["measurement_id"] not in changed:
            continue
        b = M2[M1.index(a)]
        sid = a["system_id"]
        kept = [x for x in ids(a["observed_from"]) if x not in drops[sid]]
        bo = sorted((o1_by[x] for x in kept), key=lambda o: o["x_gc_baumgardt_r_arcsec"])
        sp = {o["x_gc_baumgardt_parameter"]: o["value"] for o in O1 if o["system_id"] == sid}
        model = King66(sp["McLaughlin & van der Marel 2005 King fit: W0/gamma"], sp["McLaughlin & van der Marel 2005 King fit: r0"])
        r_ = D.light_weighted_dispersion(D.bins_from_radii([o["x_gc_baumgardt_r_arcsec"] for o in bo], [o["value"] for o in bo],
                                                           [o["err_lo"] for o in bo], [o["err_hi"] for o in bo]), model, edges_inferred=True)
        for k, v in (("x_gc_baumgardt_sigma", r_.sigma_rms), ("x_gc_baumgardt_sigma_err_lo", r_.err_lo),
                     ("x_gc_baumgardt_sigma_err_hi", r_.err_hi), ("x_gc_baumgardt_coverage", r_.coverage)):
            if rel(v, b[k]) > 1e-9:
                p.append(f"{b['measurement_id']} {k}: package {b[k]} vs recomputed {v}")
        if r_.n_bins != b["x_gc_baumgardt_n_bins"]:
            p.append(f"{b['measurement_id']} n_bins {b['x_gc_baumgardt_n_bins']} vs {r_.n_bins}")
        dr = next(r for r in R if r["system_id"] == sid and r["field"] == "d096_excluded")
        if "D-096" not in str(b["notes"]):
            p.append(f"{b['measurement_id']} has no D-096 note")
        detail.append({"measurement_id": b["measurement_id"], "system": sid, "rule": "D-096 rule 2 (D-098 rule 1)",
                       "quote": dr["quote"], "location": f"{dr['source']}, {dr['location']}",
                       "dropped": [(x.split("/")[-1], o1_by[x]["x_gc_baumgardt_r_arcsec"]) for x in drops[sid]],
                       "old": {k: a[k] for k in ("x_gc_baumgardt_sigma", "x_gc_baumgardt_sigma_err_lo", "x_gc_baumgardt_sigma_err_hi",
                                                 "x_gc_baumgardt_coverage", "x_gc_baumgardt_n_bins", "g_obs", "g_obs_err_lo", "g_obs_err_hi", "plotted")},
                       "new": {k: b[k] for k in ("x_gc_baumgardt_sigma", "x_gc_baumgardt_sigma_err_lo", "x_gc_baumgardt_sigma_err_hi",
                                                 "x_gc_baumgardt_coverage", "x_gc_baumgardt_n_bins", "g_obs", "g_obs_err_lo", "g_obs_err_hi", "plotted")}})
    res["3"] = {"pass": not p, "problems": p, "changes": detail}

    # ------------------------------------------------------------ 4. arithmetic
    p, worst = [], 0.0
    for b in M2:
        r_m = b["r_kpc"] * 1000.0 * PC
        g1 = 3.0 * (b["x_gc_baumgardt_sigma"] * 1e3) ** 2 / r_m
        g2 = G * 0.5 * b["x_gc_baumgardt_l_v"] * b["x_gc_baumgardt_ml_v"] * MSUN / r_m ** 2
        worst = max(worst, rel(g1, b["g_obs"]), rel(g2, b["g_bar"]))
        if rel(g1, b["g_obs"]) > 1e-9 or rel(g2, b["g_bar"]) > 1e-9:
            p.append(b["measurement_id"])
    res["4"] = {"pass": not p, "problems": p, "detail": f"79 rows; largest relative difference {worst:.1e}"}

    # ------------------------------------------------------------ 5. errors and levels
    p = []
    expected = {"RV": ("stated", 0.683), "K18": ("stated", 0.68), "D21": ("stated", 0.68), "L13": ("not_given_by_source", None),
                "F13": ("not_given_by_source", None), "L15": ("not_given_by_source", None)}
    notes5 = []
    for code, (st, lv) in expected.items():
        r = LEV.get(code)
        got = (r["status"], float(r["level"]) if r and r["level"] else None) if r else None
        if got != (st, lv):
            notes5.append(f"reading for {code} is {got}, test expected {(st, lv)}; the reading governs")
    for b in M2:
        r = LEV.get(b["x_gc_baumgardt_dataset"])
        want = (r["status"], float(r["level"]) if r["level"] else None) if r else (None, None)
        if (b["err_level_status"] or None, b["err_level"]) != want:
            p.append(f"{b['measurement_id']} err_level {(b['err_level_status'], b['err_level'])} vs reading {want}")
        if (b["g_bar_err_level"], b["g_bar_err_level_status"]) != (0.683, "stated"):
            p.append(f"{b['measurement_id']} g_bar_err_level")
        if b["g_bar_err_point_lo"] is not None or b["g_bar_err_point_hi"] is not None:
            p.append(f"{b['measurement_id']} g_bar point errors not empty")
    if any(c.startswith("g_obs_err_point") for c in m2.colnames):
        p.append("g_obs point columns added")
    for o in O2:
        if o["quantity"] == "sigma_los":
            r = LEV.get(o["x_gc_baumgardt_dataset"])
            want = (r["status"], float(r["level"]) if r["level"] else None) if r else (None, None)
            if ((o.get("err_level_status") or None), o.get("err_level")) != want:
                p.append(f"observable {o['observable_id']} level")
    trow = {r["term_id"]: r for r in rows(tt)}
    for t in ("g_bar_point", "ml_population"):
        if t not in trow:
            p.append(f"term {t} missing")
    res["5"] = {"pass": not p, "problems": p[:10], "notes": notes5,
                "detail": "per-code levels on 79 rows and every sigma_los observable equal the frozen err_levels.csv; g_bar level 0.683 stated; g_bar point columns empty"}

    # ------------------------------------------------------------ 6. size columns
    p = []
    n_nou = 0
    for a, b in zip(M1, M2):
        bo = [o1_by[x] for x in ids(a["baryonic_from"])]
        def pick(par):
            return next((o for o in bo if o["x_gc_baumgardt_parameter"] == par), None)
        miss = []
        for col, par in (("x_gc_baumgardt_log_rh_err", "McLaughlin & van der Marel 2005 King fit: Rh"),
                         ("x_gc_baumgardt_w0_err", "McLaughlin & van der Marel 2005 King fit: W0/gamma"),
                         ("x_gc_baumgardt_r0_err", "McLaughlin & van der Marel 2005 King fit: r0")):
            o = pick(par) or {}
            if not (same(b[col + "_lo"], o.get("err_lo")) and same(b[col + "_hi"], o.get("err_hi"))):
                p.append(f"{b['measurement_id']} {col}")
            if o.get("err_lo") is None or o.get("err_hi") is None:
                miss.append(col)
        o = pick("BC03 + Chabrier disk IMF") or {}
        if not same(b["x_gc_baumgardt_ml_v_err"], o.get("err_hi")):
            p.append(f"{b['measurement_id']} ml_v_err")
        if o.get("err_hi") is None:
            miss.append("x_gc_baumgardt_ml_v_err")
        has = "no_uncertainty" in ids(b["flags"])
        if bool(miss) != has or (miss and not all(m in str(b["notes"]) for m in miss)):
            p.append(f"{b['measurement_id']} no_uncertainty flag/notes {miss}")
        n_nou += has
        sid = b["system_id"]
        vt = next((o["value"] for o in O2 if o["observable_id"] == vt_ids.get(sid)), None)
        exp = None if vt is None else (0.22 if vt < 8 else 0.45 if vt <= 11 else 0.70)
        if not same(exp, b["x_gc_baumgardt_vt_scatter_mag"]):
            p.append(f"{b['measurement_id']} vt_scatter")
    for c in ("x_gc_baumgardt_log_rh_err_hi", "x_gc_baumgardt_w0_err_hi", "x_gc_baumgardt_r0_err_hi", "x_gc_baumgardt_ml_v_err", "x_gc_baumgardt_vt_scatter_mag"):
        if "term" not in (m2[c].description or ""):
            p.append(f"{c} header names no term")
    res["6"] = {"pass": not p, "problems": p[:10], "detail": f"size columns equal v1's observables on 79 rows; {n_nou} rows flagged no_uncertainty"}

    # ------------------------------------------------------------ 7. terms and registry
    p = []
    E = [  # term_id, scale, moves, status, size_value, size_column, size_kind, assumption_id (transcribed from the frozen table)
        ("half_light_radius", "point", "both", "given", None, "x_gc_baumgardt_log_rh_err_hi", "one_sigma", "gc_rh_measured"),
        ("king_w0", "system", "g_obs", "given", None, "x_gc_baumgardt_w0_err_hi", "one_sigma", None),
        ("king_r0", "system", "g_obs", "given", None, "x_gc_baumgardt_r0_err_hi", "one_sigma", None),
        ("king_wilson_family", "system", "both", "not_given_by_source", None, None, None, None),
        ("centre_position", "system", "g_obs", "not_given_by_source", None, None, None, None),
        ("distance_hb_zero_point", "dataset", "g_obs", "given", 0.049, None, "as_released", "gc_distance_hb"),
        ("distance_hb_slope", "dataset", "g_obs", "given", 0.033, None, "as_released", "gc_distance_hb_slope"),
        ("distance_hb_scatter", "system", "g_obs", "given", 0.11, None, "as_released", "gc_distance_hb"),
        ("reddening", "system", "both", "given_by_other_source", 0.10, None, "as_released", "gc_reddening"),
        ("extinction_law_rv", "dataset", "both", "not_given_by_source", None, None, None, "gc_extinction_rv"),
        ("integrated_magnitude", "system", "g_bar", "given_by_other_source", None, "x_gc_baumgardt_vt_scatter_mag", "upper_bound", "gc_luminosity_vt"),
        ("solar_magnitude", "dataset", "g_bar", "not_given_by_source", None, None, None, None),
        ("g_bar_point", "point", "g_bar", "not_given_by_source", None, None, None, None),
        ("ml_population", "system", "g_bar", "given", None, "x_gc_baumgardt_ml_v_err", "one_sigma", "gc_ml_scale"),
        ("pop_synthesis_code", "dataset", "g_bar", "given", 0.10, None, "as_released", "gc_ml_scale"),
        ("stellar_ml", "dataset", "g_bar", "given", None, "x_gc_baumgardt_ml_v_salpeter", "range", "gc_stellar_ml"),
        ("estimator_normalisation", "dataset", "g_obs", "not_given_by_source", None, None, None, None),
        ("anisotropy_profile", "dataset", "g_obs", "not_given_by_source", None, None, None, None),
        ("deprojection_4_3", "dataset", "both", "given", 0.02, None, "upper_bound", "gc_rhalf_wolf"),
        ("light_weighting", "dataset", "g_obs", "not_given_by_source", None, None, None, None),
        ("binaries", "system", "g_obs", "not_given_by_source", None, None, None, None),
        ("membership_contamination", "system", "g_obs", "not_given_by_source", None, None, None, None),
        ("rotation", "system", "g_obs", "not_given_by_source", None, None, None, None),
        ("tracer_mass", "system", "g_obs", "not_given_by_source", None, None, None, None),
        ("rv_zero_points", "system", "g_obs", "not_given_by_source", None, None, None, None),
        ("ellipticity", "system", "both", "not_given_by_source", None, None, None, None),
        ("heterogeneity", "dataset", "both", "not_given_by_source", None, None, None, None),
    ]
    T = rows(tt)
    if [r["term_id"] for r in T] != [e[0] for e in E]:
        p.append(f"term rows differ: {[r['term_id'] for r in T]}")
    for r, e in zip(T, E):
        got = (r["term_id"], r["scale"], r["moves"], r["status"], r["size_value"], r["size_column"] or None, r["size_kind"] or None, r["assumption_id"] or None)
        if got != e:
            p.append(f"term {e[0]}: {got} vs {e}")
        if r["applies_to"] != "*" or r["covariance"] != "not_published":
            p.append(f"term {e[0]} applies_to/covariance")
    reg = json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))
    A = {a["id"]: a for a in reg["assumptions"]}
    gc_ids = [a for a in A if a.startswith("gc_")]
    mcols = set(m2.colnames)
    scols = set(s2.colnames)
    sysrows = {r["system_id"]: r for r in S2}
    n_eval = 0
    for aid in gc_ids:
        spec = A[aid]["datasets"].get("aeg-d-gc-baumgardt/v2")
        if spec is None:
            p.append(f"{aid} has no v2 entry")
            continue
        if A[aid]["datasets"].get("aeg-d-gc-baumgardt/v1") is None and aid not in NEW_A:
            p.append(f"{aid}: v1 entry missing")
        effs = spec.get("effects") or []
        if effs and not isinstance(spec["default"], (int, float)):
            p.append(f"{aid} v2 default not numeric")
        for e in effs:
            bad = names(parse(e["formula"])) - ({"p", "p0"} | mcols | {f"system.{c}" for c in scols})
            if bad or e["column"] not in mcols:
                p.append(f"{aid} {e['column']}: bad names {bad}")
        if effs:
            for b in M2:
                out = apply_assumption(b, sysrows[b["system_id"]], effs, spec["default"], spec["default"])
                for e in effs:
                    n_eval += 1
                    if b[e["column"]] is not None and rel(out[e["column"]], b[e["column"]]) > 1e-12:
                        p.append(f"{aid} changes {e['column']} at p0 on {b['measurement_id']}")
    adj = sorted(a for a in gc_ids if A[a]["adjustable"])
    if adj != ["gc_stellar_ml"]:
        p.append(f"adjustable gc entries {adj}")
    sm1, sm2 = A["gc_stellar_ml"]["datasets"]["aeg-d-gc-baumgardt/v1"], A["gc_stellar_ml"]["datasets"]["aeg-d-gc-baumgardt/v2"]
    if sm1["effects"] != sm2["effects"] or (sm1["min"], sm1["default"], sm1["max"]) != (sm2["min"], sm2["default"], sm2["max"]):
        p.append("gc_stellar_ml v2 slider differs from v1")
    res["7"] = {"pass": not p, "problems": p[:10], "detail": f"{len(T)} terms as frozen; {len(gc_ids)} gc_* registry entries with v2 entries; {n_eval} formula evaluations unchanged at p0"}

    # ------------------------------------------------------------ 8. plotting, notes, register, site
    p = []
    for a, b in zip(M1, M2):
        sid = a["system_id"]
        exp = a["plotted"]
        if sid in excluded:
            exp = "false"
        if a["measurement_id"] in changed:
            exp = b["plotted"]  # rule 1: as D-036 decides on the recomputed profile (checked in item 3)
        if b["plotted"] != exp:
            p.append(f"{b['measurement_id']} plotted {b['plotted']} vs {exp}")
        if sid in excluded:
            q = q_of[sid]["quote"]
            if q not in str(b["notes"]) or "D-097 finding (D-098, D-099)" not in str(b["notes"]):
                p.append(f"{b['measurement_id']} excluded without quotation")
            if b["role"] != "alternative" or (b["alternative_of"] or "") != "":
                p.append(f"{b['measurement_id']} role/alternative_of")
            want = "other" if a["plotted"] == "true" else a["not_plotted_reason"]
            if b["not_plotted_reason"] != want:
                p.append(f"{b['measurement_id']} not_plotted_reason")
        if sid in anchors and "D-036 #6 not triggered (D-099 rule 3)" not in str(b["notes"]):
            p.append(f"{b['measurement_id']} anchor note missing")
        if sid not in anchors and "D-099 rule 3" in str(b["notes"]):
            p.append(f"{b['measurement_id']} anchor note on a non-anchor")
    pal1 = [b for b in M2 if "PAL1" in str(b["notes"]).upper() or b["system_id"] == "aeg-s-000316"]
    reg_rows = list(csv.DictReader((ROOT / "data/registry/excluded.csv").open(encoding="utf-8")))
    mine = [r for r in reg_rows if r["dataset"] == "aeg-d-gc-baumgardt/v2"]
    if sorted(r["system"] for r in mine) != sorted(excluded):
        p.append(f"excluded.csv rows {sorted(r['system'] for r in mine)} vs findings {sorted(excluded)}")
    for r in mine:
        if q_of[r["system"]]["quote"] not in r["reason"] or not r["citation"]:
            p.append(f"excluded.csv {r['system']} reason/citation")
    site_res = "not run"
    if site:
        def norm(s):
            return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
        ok = []
        for r in mine:
            page = site / "systems" / r["system"] / "index.html"
            text = norm(page.read_text(encoding="utf-8")) if page.is_file() else ""
            good = re.sub(r"\s+", " ", r["reason"]) in text and re.sub(r"\s+", " ", r["citation"]) in text
            ok.append(good)
            if not good:
                p.append(f"site page of {r['system']} lacks its quotation or citation")
        site_res = f"{sum(ok)} of {len(ok)} excluded-system pages contain the quotation and citation"
    counts = {"rows_changed_D096": len(changed), "systems_excluded_D097": len(excluded), "possibilities": len(possible),
              "rows_with_D099_anchor_note": sum(1 for b in M2 if b["system_id"] in anchors)}
    res["8"] = {"pass": not p, "problems": p[:10], "counts": counts, "site": site_res,
                "detail": f"plotted {sum(b['plotted'] == 'true' for b in M2)} of 79 (v1: {sum(a['plotted'] == 'true' for a in M1)})"}

    # ------------------------------------------------------------ 9. named items
    p = []
    for b in M2:
        code = b["x_gc_baumgardt_dataset"]
        want = SCR[code]["value"] if code in SCR else "not_stated"
        if b["x_gc_baumgardt_binary_screening"] != want:
            p.append(f"{b['measurement_id']} screening")
        if b["system_id"] not in vt_ids:
            p.append(f"{b['measurement_id']} has no V_t observable")
    if "Harris 2010" not in (s2["x_gc_baumgardt_ebv_mag"].description or "") or "gc_reddening" not in (s2["x_gc_baumgardt_ebv_mag"].description or ""):
        p.append("ebv header")
    if "tab:pred" not in A["gc_stellar_ml"]["datasets"]["aeg-d-gc-baumgardt/v2"]["range_ref"]:
        p.append("KM09 tab:pred correction missing")
    if "Table 11" not in A["gc_light_model"]["datasets"]["aeg-d-gc-baumgardt/v2"]["default_ref"]:
        p.append("MvdM Table 11 correction missing")
    src = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))
    v1src = json.loads((V1 / "sources.json").read_text(encoding="utf-8"))
    files2 = {s["file"]: s for s in src["sources"]}
    for s in v1src["sources"]:
        if s["file"] not in files2:
            p.append(f"v1 source {s['file']} not listed")
    bsh = [s for s in src["sources"] if "2009.09611" in s.get("url", "")]
    if not bsh or bsh[0]["sha256"] != "0e1a2b34d587ba8dacfc0ddd243e534ac15e22c3ea4b72d0606b0340dcf636b2" or "licen" not in json.dumps(bsh[0]) \
            or "redistributable" not in bsh[0]:
        p.append("BSH20 source entry")
    ki = json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    titles = " ".join(k["title"] for k in ki)
    if "M54" not in titles or "dynamical parallax" not in titles:
        p.append("known issues for M54 bins and Harris anchors")
    res["9"] = {"pass": not p, "problems": p[:10], "detail": f"screening on 79 rows; {len(vt_ids)} V_t observables; known issues {[k['issue'] for k in ki]}"}

    # ------------------------------------------------------------ 10. descriptor
    p = []
    dp = json.loads((HERE / "datapackage.json").read_text(encoding="utf-8"))
    if dp.get("standard_version") != "2.5.1" or m2.meta.get("standard_version") != "2.5.1":
        p.append("standard_version")
    if changed and dp.get("x_value_change_ruling") != "D-096":
        p.append("x_value_change_ruling")
    xs = dp.get("x_second_reading", {})
    if xs.get("file") != "SECOND_READING.md" or sorted(xs.get("reading", [])) != sorted(
            ["reading/d096_d097.csv", "reading/err_levels.csv", "reading/binary_screening.csv", "reading/resolutions.md"]):
        p.append("x_second_reading")
    res["10"] = {"pass": not p, "problems": p}

    # ------------------------------------------------------------ 11. package equals the frozen reading
    p = []
    if {a["system_id"] for a in M1 if a["measurement_id"] in changed} != set(drops):
        p.append("changed systems differ from the reading's D-096 list")
    pl_ex = {b["system_id"] for b in M2 if b["system_id"] in excluded and b["plotted"] == "false"}
    if pl_ex != (excluded & {b["system_id"] for b in M2}):
        p.append("exclusions differ from the reading")
    for b in M2:
        if b["system_id"] in possible and "D-097 possibility" not in str(b["notes"]):
            p.append(f"{b['measurement_id']} possibility note")
    fr = json.loads((ROOT / "data/frozen/gc-v2-reading.json").read_text(encoding="utf-8"))
    for rel_, h in fr["files"].items():
        if hashlib.sha256((ROOT / rel_).read_bytes()).hexdigest() != h:
            p.append(f"reading file changed: {rel_}")
    res["11"] = {"pass": not p, "problems": p,
                 "detail": "D-096 changes, D-097 exclusions and possibilities, D-099 anchors, levels (item 5) and screening (item 9) equal the frozen reading; reading files unchanged since freezing"}

    # ------------------------------------------------------------ 13. v1 untouched
    p = []
    listed = subprocess.run(["git", "ls-tree", "-r", "--name-only", "5dc4091", "--", "data/packages/aeg-d-gc-baumgardt/v1"],
                            cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    for f in listed:
        old = subprocess.run(["git", "show", f"5dc4091:{f}"], cwd=ROOT, capture_output=True, check=True).stdout
        if hashlib.sha256(old).hexdigest() != hashlib.sha256((ROOT / f).read_bytes()).hexdigest():
            p.append(f)
    now = subprocess.run(["git", "ls-files", "data/packages/aeg-d-gc-baumgardt/v1"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    if sorted(now) != sorted(listed):
        p.append("v1 file list changed")
    res["13"] = {"pass": not p, "problems": p, "detail": f"{len(listed)} v1 files identical to commit 5dc4091"}

    (HERE / "reproduction/score.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    for k, v in res.items():
        print(k, "PASS" if v["pass"] else "FAIL", v.get("problems", [])[:3])
    return 0


if __name__ == "__main__":
    sys.exit(main())
