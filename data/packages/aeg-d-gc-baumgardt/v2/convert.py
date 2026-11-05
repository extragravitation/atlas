"""Re-issue aeg-d-gc-baumgardt/v1 under data standard 2.5.1 (v2).

Usage: python data/packages/aeg-d-gc-baumgardt/v2/convert.py

Method: the frozen test REPRODUCTION.md (data/frozen/gc-v2-test.json) and the frozen second reading in
reading/ (data/frozen/gc-v2-reading.json); decisions D-087, D-096 to D-102, standard 2.5.1.

Inputs:
  - v1's committed tables (every v1 value is carried over from them, bit for bit);
  - the frozen reading files: every D-096 change, D-097 class, possibility, D-099 rule 3 anchor,
    confidence level and binary-screening value comes from them, and from nowhere else. This file has
    no system-specific rule of its own;
  - source/mwgc.dat (Harris 2010; not committed, hash-checked against v1/sources.json) for the new
    V_t observables and E(B-V) column;
  - v1's frozen code (aeg.dispersion with aeg.king66 weights) for the one D-096 recomputation.

Writes tables/{measurements,observables,systems,uncertainty_terms}.ecsv, datapackage.json and
checksums.sha256. Scoring is separate (reproduction/score.py), after this has run.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
from astropy.table import MaskedColumn, Table
import astropy.units as u

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / "v1"
ROOT = HERE.parents[3]
sys.path.insert(0, str(V1))
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg import dispersion as D  # noqa: E402
from aeg.king66 import King66  # noqa: E402
from aeg.package import write_checksums, write_datapackage  # noqa: E402
from sources_io import read_harris, norm_name  # noqa: E402  (v1's frozen reader)

DATASET, VERSION, STANDARD = "aeg-d-gc-baumgardt", "v2", "2.5.1"
PID, PID1 = f"{DATASET}/{VERSION}", f"{DATASET}/v1"
READING = HERE / "reading"
SRC = HERE / "source"
NEW_ASSUMPTIONS = ["gc_distance_hb_slope", "gc_reddening", "gc_extinction_rv", "gc_rh_measured", "gc_luminosity_vt",
                   "gc_ml_scale"]
G = __import__("astropy.constants", fromlist=["G"]).G.to_value(u.m ** 3 / (u.kg * u.s ** 2))
PC = __import__("astropy.constants", fromlist=["pc"]).pc.to_value(u.m)
WOLF = 4.0 / 3.0  # v1 analysis.WOLF_FACTOR
HARRIS_ANCHOR_QUOTE = ("\"dynamical parallax from combined solutions to radial velocity and proper motion dispersions "
                       "(Rees 1996; McLaughlin et al.~2006; van de Ven et al.~2006; van den Bosch et al.~2006)\"")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_frozen() -> None:
    for rec in ("gc-v2-test.json", "gc-v2-reading.json"):
        d = json.loads((ROOT / "data/frozen" / rec).read_text(encoding="utf-8"))
        for rel, h in d["files"].items():
            if sha(ROOT / rel) != h:
                raise SystemExit(f"frozen file changed: {rel}")
    src = {s["file"]: s["sha256"] for s in json.loads((V1 / "sources.json").read_text(encoding="utf-8"))["sources"]}
    if sha(SRC / "mwgc.dat") != src["mwgc.dat"]:
        raise SystemExit("source/mwgc.dat does not match v1/sources.json")


def vals(col):
    out = []
    for v in col:
        if np.ma.is_masked(v):
            out.append(None)
        else:
            v = v.item() if hasattr(v, "item") else v
            out.append(None if isinstance(v, float) and np.isnan(v) and False else v)
    return out


def rows_of(t: Table) -> list[dict]:
    cols = {c: vals(t[c]) for c in t.colnames}
    return [{c: cols[c][i] for c in t.colnames} for i in range(len(t))]


def new_id(x):
    return None if x is None else str(x).replace(PID1 + "/", PID + "/")


def ids(s):
    return [x for x in str(s or "").split(";") if x]


def make_col(name, data, unit=None, ucd=None, description="", kind="str"):
    data = list(data)
    if kind in ("f8", "i8"):
        mask = [x is None for x in data]
        arr = np.array([(0 if kind == "i8" else np.nan) if x is None else x for x in data], dtype=kind)
        c = MaskedColumn(arr, name=name, mask=mask, unit=unit, description=description)
    else:
        c = MaskedColumn([("" if x is None else str(x)) for x in data], name=name, description=description, dtype=str)
    c.meta["ucd"] = ucd
    return c


def like(t1: Table, name: str, data, description: str | None = None):
    """A column with v1's metadata (unit, UCD, description, kind)."""
    c1 = t1[name]
    kind = {"f": "f8", "i": "i8"}.get(c1.dtype.kind, "str")
    return make_col(name, data, c1.unit, (c1.meta or {}).get("ucd"), description or c1.description, kind)


def read_reading():
    R = list(csv.DictReader((READING / "d096_d097.csv").open(encoding="utf-8")))
    levels = {r["dataset_code"]: r for r in csv.DictReader((READING / "err_levels.csv").open(encoding="utf-8"))}
    screen = {r["dataset_code"]: r for r in csv.DictReader((READING / "binary_screening.csv").open(encoding="utf-8"))}
    return R, levels, screen


def main() -> int:
    check_frozen()
    R, levels, screen = read_reading()
    m1 = Table.read(V1 / "tables/measurements.ecsv", format="ascii.ecsv")
    o1 = Table.read(V1 / "tables/observables.ecsv", format="ascii.ecsv")
    s1 = Table.read(V1 / "tables/systems.ecsv", format="ascii.ecsv")
    mrows, orows, srows = rows_of(m1), rows_of(o1), rows_of(s1)
    obs_by_id = {r["observable_id"]: r for r in orows}
    harris = {norm_name(k): v for k, v in read_harris(SRC / "mwgc.dat").items()}

    # ---------------------------------------------------------------- the frozen reading, parsed
    drops: dict[str, list[str]] = {}          # system_id -> v1 observable IDs to drop (D-096 rule 2)
    drop_rows: dict[str, dict] = {}
    for r in R:
        if r["field"] == "d096_excluded" and r["system_id"].startswith("aeg-s-") \
                and r["value"].startswith("Atlas computes from the same data points: yes"):
            drops[r["system_id"]] = [f"{PID1}/{x}" for x in re.findall(r"o\d{6}", r["value"])]
            drop_rows[r["system_id"]] = r
    for r in R:  # D-096 rules 1 and 3: a change only where the reading names one ("change:" in its value)
        if r["field"] in ("d096_preferred", "d096_fiducial") and r["value"].lower().startswith("change:"):
            raise SystemExit(f"reading names a D-096 rule 1/3 change this converter does not implement: {r}")
    cls = {r["system_id"]: r["value"] for r in R if r["field"] == "d097_class"}
    quotes: dict[str, list[dict]] = {}
    for r in R:
        if r["field"] == "d097" and r["value"] in ("finding", "possibility") and r["system_id"].startswith("aeg-s-"):
            quotes.setdefault(r["system_id"], []).append(r)
    anchors = {r["system_id"]: r for r in R if r["field"] == "harris_anchor" and r["value"] == "yes"}
    gbar_level = next(v for k, v in levels.items() if k.startswith("g_bar"))

    # ---------------------------------------------------------------- observables
    sys_with_rows = []
    for r in mrows:
        if r["system_id"] not in sys_with_rows:
            sys_with_rows.append(r["system_id"])
    order = [s["system_id"] for s in srows if s["system_id"] in sys_with_rows]
    name_of = {s["system_id"]: s["name_in_source"] for s in srows}
    ocols = list(o1.colnames)
    O = {c: [] for c in ocols + ["err_level", "err_level_status"]}
    for r in orows:
        for c in ocols:
            O[c].append(new_id(r[c]) if c == "observable_id" else r[c])
        lev = levels.get(r["x_gc_baumgardt_dataset"]) if r["quantity"] == "sigma_los" else None
        O["err_level"].append(float(lev["level"]) if lev and lev["status"] == "stated" else None)
        O["err_level_status"].append(lev["status"] if lev else None)
    n = len(orows)
    vt_obs = {}
    for sid in order:
        h = harris.get(norm_name(name_of[sid]))
        vt = None if not h else (float(h["II:V_t"]) if h.get("II:V_t", "").strip() else None)
        if vt is None:
            continue
        n += 1
        oid = f"{PID}/o{n:06d}"
        vt_obs[sid] = (oid, vt)
        row = {c: None for c in O}
        row.update({"observable_id": oid, "system_id": sid, "side": "baryonic", "quantity": "apparent_magnitude",
                    "value": vt, "unit": "mag", "band": "V", "limit": "none", "steps": "photometry", "evidence_tier": 1,
                    "source_ref": "mwgc.dat Part II, V_t", "x_gc_baumgardt_parameter": "V_t"})
        for c in O:
            O[c].append(row[c])
    obs_t = Table([like(o1, c, O[c]) for c in ocols] + [
        make_col("err_level", O["err_level"], None, "stat.value", "Confidence level of err_lo/err_hi as the source states it (standard 2.4.0 §4; frozen reading err_levels.csv)", "f8"),
        make_col("err_level_status", O["err_level_status"], ucd="meta.code", description="stated or not_given_by_source (sigma_los rows only)"),
    ])
    obs_t.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    # ---------------------------------------------------------------- measurements
    changes = []
    out = []
    for r in mrows:
        sid, code = r["system_id"], r["x_gc_baumgardt_dataset"]
        w = dict(r)
        notes = [r["notes"]] if r["notes"] else []
        flags = ids(r["flags"])
        w["measurement_id"] = new_id(r["measurement_id"])
        w["alternative_of"] = new_id(r["alternative_of"]) if r["alternative_of"] else r["alternative_of"]
        w["model_dependence"] = "none"
        w["assumptions"] = ";".join(ids(r["assumptions"]) + NEW_ASSUMPTIONS)
        bf = ids(r["baryonic_from"])
        if sid in vt_obs:
            bf.append(vt_obs[sid][0])
        w["baryonic_from"] = ";".join(new_id(x) for x in bf)
        of = ids(r["observed_from"])
        # D-096 rule 2: the frozen reading's dropped bins, recomputed with v1's frozen code
        if sid in drops and set(drops[sid]) & set(of):
            dropped = [x for x in of if x in drops[sid]]
            kept = [x for x in of if x not in drops[sid]]
            def bins_of(oids):
                b = sorted((obs_by_id[x] for x in oids), key=lambda o: o["x_gc_baumgardt_r_arcsec"])
                return D.bins_from_radii([o["x_gc_baumgardt_r_arcsec"] for o in b], [o["value"] for o in b],
                                         [o["err_lo"] for o in b], [o["err_hi"] for o in b])
            sp = {o["x_gc_baumgardt_parameter"]: o["value"] for o in orows if o["system_id"] == sid}
            model = King66(sp["McLaughlin & van der Marel 2005 King fit: W0/gamma"], sp["McLaughlin & van der Marel 2005 King fit: r0"])
            full = D.light_weighted_dispersion(bins_of(of), model, edges_inferred=True)
            if not (full.sigma_rms == r["x_gc_baumgardt_sigma"] and full.coverage == r["x_gc_baumgardt_coverage"]):
                raise SystemExit(f"v1's frozen code does not reproduce v1 for {sid}; refusing to apply D-096")
            res = D.light_weighted_dispersion(bins_of(kept), model, edges_inferred=True)
            sig, lo, hi = res.sigma_rms, res.err_lo, res.err_hi
            r_m = WOLF * r["x_gc_baumgardt_r_h_pc"] * PC
            g = 3.0 * (sig * 1e3) ** 2 / r_m
            w.update({"observed_from": ";".join(kept), "x_gc_baumgardt_sigma": sig, "x_gc_baumgardt_sigma_err_lo": lo,
                      "x_gc_baumgardt_sigma_err_hi": hi, "x_gc_baumgardt_coverage": res.coverage,
                      "x_gc_baumgardt_n_bins": res.n_bins, "g_obs": g, "g_obs_err_lo": g * (1 - ((sig - lo) / sig) ** 2),
                      "g_obs_err_hi": g * (((sig + hi) / sig) ** 2 - 1)})
            dr = drop_rows[sid]
            rs = ", ".join(f"{x.split('/')[-1]} ({obs_by_id[x]['x_gc_baumgardt_r_arcsec']}\")" for x in dropped)
            notes.append(f"D-096 rule 2 (D-098 rule 1): bins dropped as the source excluded them: {rs}. "
                         f"Source: {dr['source']}, {dr['location']}: \"{dr['quote']}\". Bins near the cut may straddle it "
                         f"(known issue #159)")
            if not res.plotted:
                w.update({"plotted": "false", "role": "alternative", "alternative_of": "",
                          "not_plotted_reason": "coverage_below_threshold"})
                notes.append(f"light coverage {res.coverage:.2f} or {res.n_bins} bins fails D-036 after the D-096 cut")
            changes.append({"measurement_id": w["measurement_id"], "system_id": sid, "dropped": dropped,
                            "old": {k: r[k] for k in ("x_gc_baumgardt_sigma", "x_gc_baumgardt_sigma_err_lo", "x_gc_baumgardt_sigma_err_hi",
                                                      "x_gc_baumgardt_coverage", "x_gc_baumgardt_n_bins", "g_obs", "g_obs_err_lo", "g_obs_err_hi", "plotted")},
                            "new": {k: w[k] for k in ("x_gc_baumgardt_sigma", "x_gc_baumgardt_sigma_err_lo", "x_gc_baumgardt_sigma_err_hi",
                                                      "x_gc_baumgardt_coverage", "x_gc_baumgardt_n_bins", "g_obs", "g_obs_err_lo", "g_obs_err_hi", "plotted")}})
        else:
            w["observed_from"] = ";".join(of)
        w["observed_from"] = ";".join(new_id(x) for x in ids(w["observed_from"]))
        # D-097: findings excluded, possibilities noted (frozen reading only)
        if cls.get(sid) == "finding":
            q = next(x for x in quotes[sid] if x["value"] == "finding")
            if r["plotted"] == "true":
                w["not_plotted_reason"] = "other"
            w.update({"plotted": "false", "role": "alternative", "alternative_of": ""})
            notes.append(f"D-097 finding (D-098, D-099): \"{q['quote']}\" ({q['source']}, {q['location']})")
        elif cls.get(sid) == "possibility":
            for q in quotes.get(sid, []):
                if q["value"] == "possibility":
                    notes.append(f"D-097 possibility, plotted (D-099 rule 4): \"{q['quote']}\" ({q['source']}, {q['location']})")
        if sid in anchors:
            a = anchors[sid]
            notes.append(f"D-099 rule 3: Harris 2010 (arXiv 1012.3224v1, l. 125–127) calibrates M_V(HB) partly with "
                         f"{HARRIS_ANCHOR_QUOTE}; this cluster's dynamical distance: {a['source']}, {a['location']}. "
                         f"D-036 #6 not triggered (D-099 rule 3)")
        # item 5: confidence levels
        lev = levels.get(code)
        w["err_level"] = float(lev["level"]) if lev and lev["status"] == "stated" else None
        w["err_level_status"] = lev["status"] if lev else None
        w["g_bar_err_level"] = float(gbar_level["level"]) if gbar_level["status"] == "stated" else None
        w["g_bar_err_level_status"] = gbar_level["status"]
        w["g_bar_err_point_lo"] = w["g_bar_err_point_hi"] = None
        # item 6: per-row size columns, copied from v1's observables
        bo = [obs_by_id[x] for x in ids(r["baryonic_from"])]
        def pick(param):
            return next((o for o in bo if o["x_gc_baumgardt_parameter"] == param), None)
        rh = pick("McLaughlin & van der Marel 2005 King fit: Rh")
        w0 = pick("McLaughlin & van der Marel 2005 King fit: W0/gamma")
        r0 = pick("McLaughlin & van der Marel 2005 King fit: r0")
        ml = pick("BC03 + Chabrier disk IMF")
        missing = []
        for colname, o, key in (("x_gc_baumgardt_log_rh_err", rh, None), ("x_gc_baumgardt_w0_err", w0, None),
                                ("x_gc_baumgardt_r0_err", r0, None)):
            lo_, hi_ = (o or {}).get("err_lo"), (o or {}).get("err_hi")
            w[colname + "_lo"], w[colname + "_hi"] = lo_, hi_
            if lo_ is None or hi_ is None:
                missing.append(colname + "_lo/_hi")
        w["x_gc_baumgardt_ml_v_err"] = (ml or {}).get("err_hi")
        if w["x_gc_baumgardt_ml_v_err"] is None:
            missing.append("x_gc_baumgardt_ml_v_err")
        if missing:
            if "no_uncertainty" not in flags:
                flags.append("no_uncertainty")
            notes.append("no_uncertainty: the source prints no error for " + ", ".join(missing))
        vt = vt_obs.get(sid, (None, None))[1]
        w["x_gc_baumgardt_vt_scatter_mag"] = None if vt is None else (0.22 if vt < 8 else 0.45 if vt <= 11 else 0.70)
        w["x_gc_baumgardt_binary_screening"] = screen[code]["value"] if code in screen else "not_stated"
        w["flags"] = ";".join(flags)
        w["notes"] = " | ".join(notes) if notes else None
        out.append(w)

    m_desc = {
        "model_dependence": "None (D-087): the King (1966) profiles are used only as light weights; every value comes from binned profiles",
        "assumptions": "Named assumptions affecting this row (v1's, plus the v2 registry entries of REPRODUCTION.md item 7)",
    }
    mcols = [like(m1, c, [w[c] for w in out], m_desc.get(c)) for c in m1.colnames]
    acc = u.m / u.s ** 2
    mcols += [
        make_col("err_level", [w["err_level"] for w in out], None, "stat.value", "Confidence level of g_obs_err_lo/hi, from the dispersion source (frozen reading err_levels.csv)", "f8"),
        make_col("err_level_status", [w["err_level_status"] for w in out], ucd="meta.code", description="stated or not_given_by_source"),
        make_col("g_bar_err_level", [w["g_bar_err_level"] for w in out], None, "stat.value", "Confidence level of g_bar_err_lo/hi: \"The 1{sigma} error in BC/ChD\" (MvdM clusters.vot, e_(M/L)1)", "f8"),
        make_col("g_bar_err_level_status", [w["g_bar_err_level_status"] for w in out], ucd="meta.code", description="stated or not_given_by_source"),
        make_col("g_bar_err_point_lo", [None] * len(out), acc, "stat.error;phys.acceleration", "Point-scale part: not given by the source (term g_bar_point)", "f8"),
        make_col("g_bar_err_point_hi", [None] * len(out), acc, "stat.error;phys.acceleration", "Point-scale part: not given by the source (term g_bar_point)", "f8"),
        make_col("x_gc_baumgardt_log_rh_err_lo", [w["x_gc_baumgardt_log_rh_err_lo"] for w in out], u.dex, "stat.error;phys.size.radius", "MvdM lower error of log R_h, from the half_light_radius observable; size of term half_light_radius", "f8"),
        make_col("x_gc_baumgardt_log_rh_err_hi", [w["x_gc_baumgardt_log_rh_err_hi"] for w in out], u.dex, "stat.error;phys.size.radius", "MvdM upper error of log R_h, from the half_light_radius observable; size of term half_light_radius", "f8"),
        make_col("x_gc_baumgardt_w0_err_lo", [w["x_gc_baumgardt_w0_err_lo"] for w in out], None, "stat.error;stat.fit.param", "MvdM lower error of W0, from the structural_param observable; size of term king_w0", "f8"),
        make_col("x_gc_baumgardt_w0_err_hi", [w["x_gc_baumgardt_w0_err_hi"] for w in out], None, "stat.error;stat.fit.param", "MvdM upper error of W0, from the structural_param observable; size of term king_w0", "f8"),
        make_col("x_gc_baumgardt_r0_err_lo", [w["x_gc_baumgardt_r0_err_lo"] for w in out], u.arcsec, "stat.error;phys.size.radius", "MvdM lower error of r0, from the structural_param observable; size of term king_r0", "f8"),
        make_col("x_gc_baumgardt_r0_err_hi", [w["x_gc_baumgardt_r0_err_hi"] for w in out], u.arcsec, "stat.error;phys.size.radius", "MvdM upper error of r0, from the structural_param observable; size of term king_r0", "f8"),
        make_col("x_gc_baumgardt_ml_v_err", [w["x_gc_baumgardt_ml_v_err"] for w in out], u.solMass / u.solLum, "stat.error;phys.composition.massLightRatio", "MvdM e_(M/L)1, from the stellar_ml_population observable; size of term ml_population", "f8"),
        make_col("x_gc_baumgardt_vt_scatter_mag", [w["x_gc_baumgardt_vt_scatter_mag"] for w in out], u.mag, "stat.error;phot.mag", "BSH20 Table tab:comp scatter about Harris (2010), by Harris V_t (V<8: 0.22; 8-11: 0.45; >11: 0.70 mag); size of term integrated_magnitude (upper bound)", "f8"),
        make_col("x_gc_baumgardt_binary_screening", [w["x_gc_baumgardt_binary_screening"] for w in out], ucd="meta.code", description="multi_epoch_stated, integrated_light or not_stated, per dispersion dataset code (frozen reading binary_screening.csv). multi_epoch_stated applies only to stars with more than one measurement"),
    ]
    meas = Table(mcols)
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    # ---------------------------------------------------------------- systems
    excluded = {sid for sid, c in cls.items() if c == "finding"}
    S = []
    for s in srows:
        w = dict(s)
        p = json.loads(s["properties"])
        if s["system_id"] in excluded:
            q = next(x for x in quotes[s["system_id"]] if x["value"] == "finding")
            p["status"] = "recorded"
            p["reasons_not_plotted"] = [f"D-097 finding (D-098, D-099): \"{q['quote']}\" ({q['source']}, {q['location']})"]
        for ch in changes:
            if ch["system_id"] == s["system_id"]:
                cand = p["candidates"]["RV"]
                cand.update({"coverage": round(ch["new"]["x_gc_baumgardt_coverage"], 4),
                             "sigma_rms_km_s": round(ch["new"]["x_gc_baumgardt_sigma"], 4), "n_bins": ch["new"]["x_gc_baumgardt_n_bins"]})
                if ch["new"]["plotted"] == "false":
                    p["status"] = "recorded"
                    p["reasons_not_plotted"] = ["no line-of-sight candidate passes the plotting rules (coverage ≥ 0.80, ≥ 2 bins) after the D-096 cut"]
        w["properties"] = json.dumps(p, ensure_ascii=False, sort_keys=True)
        h = harris.get(norm_name(s["name_in_source"]))
        e = (h or {}).get("II:E(B-V)", "").strip()
        w["x_gc_baumgardt_ebv_mag"] = float(e) if e else None
        S.append(w)
    sys_t = Table([like(s1, c, [w[c] for w in S]) for c in s1.colnames] + [
        make_col("x_gc_baumgardt_ebv_mag", [w["x_gc_baumgardt_ebv_mag"] for w in S], u.mag, "phot.color.excess",
                 "E(B-V), Harris 2010 (mwgc.dat Part II); read by the gc_reddening and gc_extinction_rv formulas", "f8")])
    sys_t.meta = dict(meas.meta)

    # ---------------------------------------------------------------- uncertainty terms (item 7)
    terms = build_terms()

    (HERE / "tables").mkdir(exist_ok=True)
    for name, tab in (("measurements", meas), ("observables", obs_t), ("systems", sys_t), ("uncertainty_terms", terms)):
        tab.write(HERE / f"tables/{name}.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    (HERE / "reproduction").mkdir(exist_ok=True)
    (HERE / "reproduction/changes.json").write_text(json.dumps(changes, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
    if changes:
        desc["x_value_change_ruling"] = "D-096"
    desc["x_known_issues"] = [f"https://github.com/extragravitation/atlas/issues/{k['issue']}"
                              for k in json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]]
    write_datapackage(HERE, desc, {"measurements": ("tables/measurements.ecsv", meas),
                                   "observables": ("tables/observables.ecsv", obs_t),
                                   "systems": ("tables/systems.ecsv", sys_t),
                                   "uncertainty_terms": ("tables/uncertainty_terms.ecsv", terms)})
    write_checksums(HERE)
    print(f"wrote {len(meas)} measurements ({sum(w['plotted'] == 'true' for w in out)} plotted), {len(obs_t)} observables, "
          f"{len(sys_t)} systems, {len(terms)} terms; {len(changes)} D-096 change(s); {len(excluded)} D-097 exclusion(s)")
    return 0


def build_terms() -> Table:
    keys = ["term_id", "scale", "applies_to", "moves", "status", "size_value", "size_lo", "size_hi", "size_unit",
            "size_column", "size_kind", "assumption_id", "correlated_with", "covariance", "citation", "locator", "note",
            "in_error_columns"]
    t = {k: [] for k in keys}

    def term(**kw):
        kw.setdefault("applies_to", "*")
        kw.setdefault("covariance", "not_published")
        for k in keys:
            t[k].append(kw.get(k))

    MVDM = "McLaughlin & van der Marel 2005, ApJS 161, 304 (arXiv astro-ph/0605132v1; VizieR J/ApJS/161/304)"
    H10 = "Harris 1996, AJ 112, 1487, 2010 edition (arXiv 1012.3224v1)"
    WOLF_C = "Wolf et al. 2010, MNRAS 406, 1220 (arXiv 0908.2995)"
    BH18 = "Baumgardt & Hilker 2018, MNRAS 478, 1520 (arXiv 1804.08359v2)"
    term(term_id="half_light_radius", scale="point", moves="both", status="given", size_column="x_gc_baumgardt_log_rh_err_hi",
         size_unit="dex", size_kind="one_sigma", assumption_id="gc_rh_measured", correlated_with="king_w0;king_r0",
         citation=MVDM, locator="Table 11 (tab:struc); errors \"chi^2 within 1 of the global minimum\" (l. 2187–2190)",
         in_error_columns="no",
         note="Lower side in x_gc_baumgardt_log_rh_err_lo. §2a rule 7: g_obs ∝ 1/R_h, g_bar ∝ 1/R_h²; left out of both point columns. Correlated with king_w0 and king_r0 (one fit; covariance not published)")
    term(term_id="king_w0", scale="system", moves="g_obs", status="given", size_column="x_gc_baumgardt_w0_err_hi",
         size_kind="one_sigma", citation=MVDM, locator="Table 10; \"Upper/Lower 1{sigma} error in WO\" (models VOT)",
         note="Lower side in x_gc_baumgardt_w0_err_lo. Moves the light weights; effect not computed in v2")
    term(term_id="king_r0", scale="system", moves="g_obs", status="given", size_column="x_gc_baumgardt_r0_err_hi",
         size_unit="arcsec", size_kind="one_sigma", citation=MVDM, locator="Table 10 (models VOT)",
         note="Lower side in x_gc_baumgardt_r0_err_lo. As king_w0")
    term(term_id="king_wilson_family", scale="system", moves="both", status="not_given_by_source", citation=MVDM,
         locator="l. 2703–2705",
         note="Wilson models are \"associated with slightly larger projected half-intensity radii $R_c$ and smaller half-light radii $R_h$\"; no size stated for Galactic clusters")
    term(term_id="centre_position", scale="system", moves="g_obs", status="not_given_by_source", citation=H10, locator="l. 94",
         note="Centres \"uncertain to typically 1-2 arcseconds\"; effect on σ not stated")
    term(term_id="distance_hb_zero_point", scale="dataset", moves="g_obs", status="given", size_value=0.049, size_unit="mag",
         size_kind="as_released", assumption_id="gc_distance_hb", correlated_with="distance_hb_slope", citation=H10, locator="l. 148",
         note="Harris does not say what its ± means. R_Sun and L_V move together, so g_bar is unchanged (F1). Correlated with distance_hb_slope (one fit; correlation not published). The calibration includes dynamical parallaxes (l. 125–127); D-036 #6 is not triggered (D-099 rule 3)")
    term(term_id="distance_hb_slope", scale="dataset", moves="g_obs", status="given", size_value=0.033,
         size_unit="mag per dex of [Fe/H]", size_kind="as_released", assumption_id="gc_distance_hb_slope",
         correlated_with="distance_hb_zero_point", citation=H10, locator="l. 148",
         note="The shift in M_V(HB) is the slope change × metallicity_feh")
    term(term_id="distance_hb_scatter", scale="system", moves="g_obs", status="given", size_value=0.11, size_unit="mag",
         size_kind="as_released", assumption_id="gc_distance_hb", citation=H10, locator="l. 152",
         note="The rms about the calibration")
    term(term_id="reddening", scale="system", moves="both", status="given_by_other_source", size_value=0.10,
         size_unit="fraction of E(B-V)", size_kind="as_released", assumption_id="gc_reddening",
         citation="Lützgendorf et al. 2013, A&A 552, A49 (arXiv 1212.3475v1)", locator="l. 489",
         note="\"the average errors on … the reddening (10 %)\": L13's description of Harris (1996), not read at source, applied here to the 2010 edition; the kind of error is not stated. Moves R_Sun only, so g_obs ∝ 1/D and g_bar ∝ 1/D² (F1). Uses each cluster's x_gc_baumgardt_ebv_mag")
    term(term_id="extinction_law_rv", scale="dataset", moves="both", status="not_given_by_source", assumption_id="gc_extinction_rv",
         citation=MVDM, locator="l. 1212: \"$A_V=3.1\\,E(B-V)$\"",
         note="R_V = 3.1 fixed; no range stated by Harris or MvdM; acts as reddening")
    term(term_id="integrated_magnitude", scale="system", moves="g_bar", status="given_by_other_source",
         size_column="x_gc_baumgardt_vt_scatter_mag", size_unit="mag", size_kind="upper_bound", assumption_id="gc_luminosity_vt",
         citation="Baumgardt, Sollima & Hilker 2020, PASA 37, e046 (arXiv 2009.09611v1)", locator="paper.tex Table tab:comp, l. 266; l. 254",
         note="The \"standard deviation around the mean\" of the differences from Harris (2010). It bounds the Harris error from above only because BSH20 calls the estimates \"more or less independent of each other\" (l. 254). It excludes the mean offsets (+0.03, +0.01 and −0.25 mag); the −0.25 mag offset for V > 11 is a systematic shift this row does not carry. Moves g_bar only (F1)")
    term(term_id="solar_magnitude", scale="dataset", moves="g_bar", status="not_given_by_source", citation=MVDM, locator="§4.2",
         note="M_V,sun = 4.85 (MvdM)")
    term(term_id="g_bar_point", scale="point", moves="g_bar", status="not_given_by_source",
         note="REPRODUCTION.md item 5: the source gives no point-scale part of the g_bar error")
    term(term_id="ml_population", scale="system", moves="g_bar", status="given", size_column="x_gc_baumgardt_ml_v_err",
         size_unit="solMass / solLum", size_kind="one_sigma", assumption_id="gc_ml_scale", citation=MVDM,
         locator="clusters VOT, e_(M/L)1: \"The 1{sigma} error in BC/ChD\"", in_error_columns="yes",
         note="It mixes a dataset-scale age term (13 ± 2 Gyr for every cluster) with a system-scale [Fe/H] term (± 0.2 dex), not split by MvdM (F6). Labelling it system is a simplification. Already inside g_bar_err_lo/hi, so not added again. As a fraction for gc_ml_scale: x_gc_baumgardt_ml_v_err / x_gc_baumgardt_ml_v")
    term(term_id="pop_synthesis_code", scale="dataset", moves="g_bar", status="given", size_value=0.10, size_unit="fraction of Υ_V",
         size_kind="as_released", assumption_id="gc_ml_scale", citation=MVDM, locator="l. 1357–1359",
         note="\"although there are some exceptions, these differences are generally slight: at the level of … $\\la 10\\%$ in $\\Upsilon_V$\". The hedge means this is not an upper bound")
    term(term_id="stellar_ml", scale="dataset", moves="g_bar", status="given", size_column="x_gc_baumgardt_ml_v_salpeter",
         size_unit="solMass / solLum", size_kind="range", assumption_id="gc_stellar_ml",
         citation=f"{MVDM}; Kruijssen & Mieske 2009 (arXiv 0903.4683)", locator="registry gc_stellar_ml; D-039",
         note="The registry range. Upper end: each cluster's Salpeter value, in the column. Lower end: 0.53 × x_gc_baumgardt_ml_v, from the registry's range_basis.min (Kruijssen & Mieske 2009; D-039), not from a column. MvdM's models build in about 30 % mass loss (MvdM Fig. 4); MvdM used Harris (1996) [Fe/H] (F8)")
    term(term_id="estimator_normalisation", scale="dataset", moves="g_obs", status="not_given_by_source", citation=WOLF_C, locator="l. 927",
         note="Wolf et al. 2010 shows \"±10% variation about the predicted relation\" as guide lines in a figure for classical dwarf spheroidals, not as a stated accuracy; none is stated for clusters")
    term(term_id="anisotropy_profile", scale="dataset", moves="g_obs", status="not_given_by_source", citation=WOLF_C, locator="l. 966–976",
         note="Wolf gives 0.05 dex \"in cases where extended kinematics are not available\", from the dEs and Es, \"to allow for a range of $\\beta$ profiles\". These rows have ≥ 80 % light coverage, so the condition does not describe them")
    term(term_id="deprojection_4_3", scale="dataset", moves="both", status="given", size_value=0.02, size_unit="fraction",
         size_kind="upper_bound", assumption_id="gc_rhalf_wolf", citation=WOLF_C, locator="l. 1829; l. 1814–1818",
         note="\"$\\rhalf/\\Rhalf \\simeq 4/3$ is accurate to better than 2\\% for most surface brightness profiles used to describe observed stellar systems\"; for King (1962) profiles. v1 uses King (1966) (F8). An assumption with a stated accuracy (§2a rule 4)")
    term(term_id="light_weighting", scale="dataset", moves="g_obs", status="not_given_by_source",
         note="Bins covering ≥ 80 % of the light, against Wolf's whole-system average (F8)")
    term(term_id="binaries", scale="system", moves="g_obs", status="not_given_by_source", citation=BH18, locator="l. 228–233; K18 l. 330",
         note="BH18 names Pal 13, Arp 2 and Ter 3 as possibly inflated. K18 gives +0.3 and +0.6 km/s for binary fractions of 5 % and 10 % in its own NGC 6121 data, not for these profiles")
    term(term_id="membership_contamination", scale="system", moves="g_obs", status="not_given_by_source", citation=BH18, locator="l. 206",
         note="Non-members \"removed iteratively\"")
    term(term_id="rotation", scale="system", moves="g_obs", status="not_given_by_source")
    term(term_id="tracer_mass", scale="system", moves="g_obs", status="not_given_by_source",
         citation="Kamann et al. 2018, MNRAS 473, 5591 (arXiv 1710.07257v1)", locator="l. 344; BH18 l. 185",
         note="K18 states \"≲5%\" in σ between its main-sequence samples and literature giant profiles, for NGC 3201 and NGC 6121 only. The RV code is mostly giants (BH18 l. 185)")
    term(term_id="rv_zero_points", scale="system", moves="g_obs", status="not_given_by_source", citation=BH18, locator="l. 199",
         note="Shifts \"usually less than 1 km/sec\"; effect on σ not stated")
    term(term_id="ellipticity", scale="system", moves="both", status="not_given_by_source")
    term(term_id="heterogeneity", scale="dataset", moves="both", status="not_given_by_source",
         note="The \"plus updates\" values are not documented; they differ slightly from BH18's printed table (F8)")

    desc = {"term_id": ("meta.id", "Term identifier"), "scale": ("meta.code", "point, system or dataset (standard 2.2.0 §2a)"),
            "applies_to": ("meta.id", "System, or * for all"), "moves": ("meta.code", "Axes the term moves"),
            "status": ("meta.code", "given, given_by_other_source or not_given_by_source"),
            "size_unit": ("meta.unit", "Unit of the size"),
            "size_column": ("meta.ref", "Systems or measurements column holding a per-system or per-row size (standard 2.5.1 §12)"),
            "size_kind": ("meta.code", "one_sigma, range, as_released, upper_bound or lower_bound"),
            "assumption_id": ("meta.id", "Registry assumption whose formula moves the values"),
            "correlated_with": ("meta.note", "Correlated terms"), "covariance": ("meta.code", "published, not_published or not_applicable"),
            "citation": ("meta.bib", "Where the size was read"), "locator": ("meta.ref", "Section, table, line or quote"),
            "note": ("meta.note", "What the term is"), "in_error_columns": ("meta.code", "yes or no: whether the term is inside the error columns")}
    cols = []
    for k in keys:
        if k in ("size_value", "size_lo", "size_hi"):
            cols.append(make_col(k, t[k], None, {"size_value": "stat.error", "size_lo": "stat.min", "size_hi": "stat.max"}[k],
                                 {"size_value": "Size as the source states it", "size_lo": "Lower end of a published range",
                                  "size_hi": "Upper end of a published range"}[k], "f8"))
        else:
            cols.append(make_col(k, t[k], ucd=desc[k][0], description=desc[k][1]))
    terms = Table(cols)
    terms.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    return terms


if __name__ == "__main__":
    sys.exit(main())
