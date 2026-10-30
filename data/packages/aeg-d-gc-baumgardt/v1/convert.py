"""Convert the Baumgardt globular cluster database profiles into the Atlas data standard 2.0.0.

Usage: python data/packages/aeg-d-gc-baumgardt/v1/convert.py
       (AEG_REGISTER=1 once, by the maintainer, to add new systems to data/registry/systems.csv)

Reads the hash-verified files in source/ (never committed) and writes
tables/measurements.ecsv, tables/observables.ecsv, tables/systems.ecsv,
datapackage.json and checksums.sha256. Method: REPRODUCTION.md (frozen) and
decisions D-025, D-036, D-038, D-039, D-042, D-045, D-046, D-047. The
computation is in analysis.py; this file only writes it out and runs the
frozen transcription (1) and arithmetic (3) tests.

Per plotted cluster (D-025):
  sigma      light-weighted line-of-sight dispersion of the default dataset's binned profile,
             weights from the King (1966) fit (aeg.dispersion + aeg.king66)
  r_half     4/3 x projected half-light radius (McLaughlin & van der Marel 2005, at the Harris distance)
  g_obs      3 sigma^2 / r_half
  g_bar      G (L_V Upsilon_V / 2) / r_half^2, L_V from Harris M_V,t with M_V,sun = 4.85, Upsilon_V = (M/L)_1
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from astropy.table import MaskedColumn, Table
import astropy.units as u

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg.package import write_checksums, write_datapackage  # noqa: E402

import analysis as A  # noqa: E402
from sources_io import LOS_TYPES, PM_TYPES  # noqa: E402

DATASET, VERSION, STANDARD = "aeg-d-gc-baumgardt", "v1", "2.0.0"
PID = f"{DATASET}/{VERSION}"
TODAY = "2026-10-30"

LOS_STEPS = "spectra;stellar_velocities;membership;binary_treatment;dispersion_profile"
PM_STEPS = "astrometry;proper_motions;dispersion_pm"
ASSUMPTIONS = "gc_equilibrium;gc_rhalf_wolf;gc_light_model;gc_distance_hb;gc_stellar_ml;gc_gas_absent"
METHOD = ("half-light-radius estimator (Wolf et al. 2010) on the light-weighted line-of-sight dispersion of a binned "
          "profile (D-036 ii; King 1966 light weights, D-045)")


def col(name, data, unit=None, ucd=None, description="", numeric=False, integer=False):
    data = list(data)
    if numeric or integer:
        mask = [x is None for x in data]
        if integer:
            arr = np.array([0 if x is None else int(x) for x in data], dtype="i8")
        else:
            arr = np.array([np.nan if x is None else x for x in data], dtype="f8")
        c = MaskedColumn(arr, name=name, mask=mask, unit=unit, description=description)
    else:
        c = MaskedColumn([("" if x is None else str(x)) for x in data], name=name, description=description, dtype=str)
    c.meta["ucd"] = ucd
    return c


def registry(systems) -> dict[str, str]:
    path = ROOT / "data/registry/systems.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    ids = {r["primary_name"]: r["system_id"] for r in rows if r["first_dataset"] == PID}
    missing = [s.name for s in systems if s.name not in ids]
    if missing:
        if os.environ.get("AEG_REGISTER") != "1":
            raise SystemExit(f"{len(missing)} systems not in the registry; run once with AEG_REGISTER=1")
        n = max(int(r["system_id"].split("-")[-1]) for r in rows)
        with path.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for name in missing:
                n += 1
                sid = f"aeg-s-{n:06d}"
                w.writerow([sid, name, PID, TODAY])
                ids[name] = sid
    return ids


def reason_code(s: "A.System", c: "A.Candidate") -> str:
    if s.default is c and s.plotted:
        return ""
    if not c.plotted:
        return "coverage_below_threshold"
    if s.default is not None and s.default is not c and s.plotted:
        return "alternative_value"
    return "other"


def transcription_test(sys_t) -> None:
    """REPRODUCTION.md test 1: the written tables, read back, equal freshly parsed source values (exact)."""
    from sources_io import norm_name, read_harris, read_veldis, read_votable
    src = HERE / "source"
    t = Table.read(HERE / "tables/observables.ecsv", format="ascii.ecsv")
    name_of = dict(zip(sys_t["system_id"], sys_t["name_in_source"]))
    got = {}
    for r in t:
        got.setdefault((name_of[r["system_id"]], r["x_gc_baumgardt_parameter"] or r["x_gc_baumgardt_dataset"], r["quantity"],
                        None if np.ma.is_masked(r["x_gc_baumgardt_r_arcsec"]) else float(r["x_gc_baumgardt_r_arcsec"])), []).append(r)
    bad, n = [], 0
    for b in read_veldis(src / "veldis.html"):
        q = "sigma_los" if b["type"] in LOS_TYPES else "sigma_pm"
        rows = got.get((b["cluster"], b["type"], q, float(b["r_arcsec"])), [])
        n += 1
        if not any(float(r["value"]) == float(b["sigma"]) and float(r["err_lo"]) == float(b["err_lo"])
                   and float(r["err_hi"]) == float(b["err_hi"]) and
                   (np.ma.is_masked(r["x_gc_baumgardt_n_star"]) if not b["n_star"].strip() else int(r["x_gc_baumgardt_n_star"]) == int(b["n_star"]))
                   for r in rows):
            bad.append(("veldis", b["cluster"], b["type"], b["r_arcsec"]))
    harris = {norm_name(k): v for k, v in read_harris(src / "mwgc.dat").items()}
    king = {norm_name(r["Cluster"]): r for r in read_votable(src / "mvdm05/J_ApJS_161_304_models.vot") if r["Mod"] == "K"}
    pop = {norm_name(r["Cluster"]): r for r in read_votable(src / "mvdm05/J_ApJS_161_304_clusters.vot")}
    for (name, param, q, _), rows in got.items():
        key = norm_name(name)
        for r in rows:
            v = float(r["value"])
            if param == "R_Sun (horizontal branch)":
                exp = float(harris[key]["I:R_Sun"])
            elif param == "M_V,t":
                exp = float(harris[key]["II:M_V,t"])
            elif param.startswith("McLaughlin & van der Marel 2005 King fit: "):
                exp = float(king[key][param.split(": ", 1)[1]])
            elif param.startswith("Harris 2010 "):
                exp = float(harris[key]["III:" + param.split()[2]])
            elif param == "BC03 + Chabrier disk IMF":
                exp = float(pop[key]["(M/L)1"])
            else:
                continue
            n += 1
            if v != exp:
                bad.append((name, param, v, exp))
    if bad:
        raise SystemExit(f"transcription test 1 failed ({len(bad)} of {n}): {bad[:5]}")
    print(f"test 1 (transcription): {n} values checked, all equal")


def main() -> int:
    systems = A.build(harris_rc_as_r0=False)  # reproduction test 4 rejected the r0 reading (D-047)
    ids = registry(systems)

    obs = {k: [] for k in ("observable_id", "system_id", "side", "quantity", "value", "err_lo", "err_hi", "unit", "band",
                           "limit", "r_kpc", "r_kind", "steps", "evidence_tier", "source_ref", "x_gc_baumgardt_r_arcsec",
                           "x_gc_baumgardt_n_star", "x_gc_baumgardt_dataset", "x_gc_baumgardt_parameter")}
    n_obs = 0

    def add_obs(sid, side, q, value, unit, steps, ref, err_lo=None, err_hi=None, band="", r_kpc=None, r_kind="",
                r_arcsec=None, n_star=None, dataset="", parameter=""):
        nonlocal n_obs
        n_obs += 1
        oid = f"{PID}/o{n_obs:06d}"
        for k, v in (("observable_id", oid), ("system_id", sid), ("side", side), ("quantity", q), ("value", value),
                     ("err_lo", err_lo), ("err_hi", err_hi), ("unit", unit), ("band", band), ("limit", "none"),
                     ("r_kpc", r_kpc), ("r_kind", r_kind), ("steps", steps), ("evidence_tier", 1), ("source_ref", ref),
                     ("x_gc_baumgardt_r_arcsec", r_arcsec), ("x_gc_baumgardt_n_star", n_star), ("x_gc_baumgardt_dataset", dataset),
                     ("x_gc_baumgardt_parameter", parameter)):
            obs[k].append(v)
        return oid

    m = {k: [] for k in ("measurement_id", "system_id", "kind", "channel", "method_class", "method", "measured_quantity",
                         "r_kpc", "r_kind", "g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_bar", "g_bar_err_lo", "g_bar_err_hi",
                         "g_bar_stars", "limit", "stars_status", "gas_cold_status", "gas_hot_status", "observed_from",
                         "baryonic_from", "model_dependence", "evidence_tier", "role", "alternative_of", "plotted",
                         "not_plotted_reason", "assumptions", "adjustable", "flags", "source_ref", "notes",
                         "x_gc_baumgardt_dataset", "x_gc_baumgardt_sigma", "x_gc_baumgardt_sigma_err_lo", "x_gc_baumgardt_sigma_err_hi", "x_gc_baumgardt_coverage",
                         "x_gc_baumgardt_n_bins", "x_gc_baumgardt_r_h_pc", "x_gc_baumgardt_l_v", "x_gc_baumgardt_ml_v", "x_gc_baumgardt_distance_kpc")}
    from sources_io import read_parameter
    param = read_parameter(HERE / "source/parameter.html")
    s_rows = {k: [] for k in ("system_id", "name_in_source", "class_in_source", "taxonomy_kind", "kind_label", "host",
                              "ra_deg", "dec_deg", "distance_mpc", "distance_method", "distance_kinematic", "distance_ref", "metallicity_feh",
                              "properties")}
    n_meas = 0
    transcription_errors = []

    for s in systems:
        sid = ids[s.name]
        D = s.distance_kpc
        kpc_per_arcsec = D / A.ARCSEC_PER_RAD if D else None
        # observed side: every bin, line of sight and proper motion, exactly as printed
        bin_ids = {}
        for row in sorted([b for c in s.candidates for b in c.bins] + s.pm_bins,
                          key=lambda b: (b["type"], float(b["r_arcsec"]))):
            los = row["type"] in LOS_TYPES
            r_as = float(row["r_arcsec"])
            oid = add_obs(sid, "observed", "sigma_los" if los else "sigma_pm", float(row["sigma"]), "km / s",
                          LOS_STEPS if los else PM_STEPS, f"veldis.html: {s.name}, {row['type']}, <r> = {row['r_arcsec']}\"",
                          err_lo=float(row["err_lo"]), err_hi=float(row["err_hi"]),
                          r_kpc=r_as * kpc_per_arcsec if D else None, r_kind="projected", r_arcsec=r_as,
                          n_star=int(row["n_star"]) if row["n_star"].strip() else None, dataset=row["type"])
            bin_ids.setdefault(row["type"], []).append(oid)
        # baryonic side
        bar = []
        if D:
            bar.append(add_obs(sid, "baryonic", "distance", D, "kpc", "photometry", "mwgc.dat Part I, R_Sun",
                               parameter="R_Sun (horizontal branch)"))
        if s.harris and A.num(s.harris.get("II:M_V,t")) is not None:
            bar.append(add_obs(sid, "baryonic", "absolute_magnitude", float(s.harris["II:M_V,t"]), "mag",
                               "photometry;luminosity", "mwgc.dat Part II, M_V,t", band="V", parameter="M_V,t"))
        if s.king_row:
            k = s.king_row
            for p, q, unit in (("W0/gamma", "structural_param", ""), ("r0", "structural_param", "arcsec"),
                               ("Rh", "half_light_radius", "log(pc)"), ("Dist", "distance", "kpc")):
                e_lo = A.num(k.get({"W0/gamma": "e_W0/gamma", "r0": "e_r0", "Rh": "e_Rh"}.get(p, "")))
                e_hi = A.num(k.get({"W0/gamma": "E_W0/gamma", "r0": "E_r0", "Rh": "E_Rh"}.get(p, "")))
                bar.append(add_obs(sid, "baryonic", q, float(k[p]), unit, "photometry;structural_model"
                                   if q != "distance" else "photometry", f"J/ApJS/161/304/models {k['Cluster']} K, {p}",
                                   err_lo=e_lo, err_hi=e_hi, parameter=f"McLaughlin & van der Marel 2005 King fit: {p}"))
        elif s.harris:
            for p in ("III:c", "III:r_c", "III:r_h"):
                if A.num(s.harris.get(p)) is not None:
                    bar.append(add_obs(sid, "baryonic", "half_light_radius" if p == "III:r_h" else "structural_param",
                                       float(s.harris[p]), "" if p == "III:c" else "arcmin", "photometry;structural_model",
                                       f"mwgc.dat Part III, {p[4:]}", parameter=f"Harris 2010 {p[4:]}"
                                       + (f" (flag '{s.harris.get('III:flags')}')" if p == "III:c" and s.harris.get("III:flags") else "")))
        if s.ml_v is not None:
            e = A.num(s.pop_row.get("e_(M/L)1"))
            bar.append(add_obs(sid, "baryonic", "stellar_ml_population", s.ml_v, "solMass / solLum", "stellar_ml",
                               f"J/ApJS/161/304/clusters {s.pop_row['Cluster']}, (M/L)1", err_lo=e, err_hi=e, band="V",
                               parameter="BC03 + Chabrier disk IMF"))

        # measurements: every converted line-of-sight candidate with complete inputs
        default_mid = None
        cand_rows = []
        for c in sorted(s.candidates, key=lambda c: c.dataset):
            if c.result is None or s.r_h_pc is None or s.l_v is None or s.ml_v is None or D is None:
                continue
            n_meas += 1
            mid = f"{PID}/m{n_meas:06d}"
            r_half = A.WOLF_FACTOR * s.r_h_pc
            r_m = r_half * A.PC
            sig, lo, hi = c.result.sigma_rms, c.result.err_lo, c.result.err_hi
            g_obs = 3.0 * (sig * 1e3) ** 2 / r_m
            g_bar = A.G * 0.5 * s.l_v * s.ml_v * A.M_SUN / r_m ** 2
            e_ml = A.num(s.pop_row.get("e_(M/L)1")) or 0.0
            is_default = (s.default is c and s.plotted)
            reason = reason_code(s, c)
            notes = []
            if not s.plotted and s.reasons:
                notes.append("; ".join(s.reasons))
            if not c.plotted:
                notes.append(f"light coverage {c.result.coverage:.2f} < 0.80 (D-036)")
            if is_default:
                default_mid = mid
            cand_rows.append(mid)
            row = {
                "measurement_id": mid, "system_id": sid, "kind": "system_value", "channel": "dynamics",
                "method_class": "kinematic", "method": METHOD, "measured_quantity": "g_obs",
                "r_kpc": r_half / 1000.0, "r_kind": "3d", "g_obs": g_obs,
                "g_obs_err_lo": g_obs * (1 - ((sig - lo) / sig) ** 2), "g_obs_err_hi": g_obs * (((sig + hi) / sig) ** 2 - 1),
                "g_bar": g_bar, "g_bar_err_lo": g_bar * e_ml / s.ml_v, "g_bar_err_hi": g_bar * e_ml / s.ml_v,
                "g_bar_stars": g_bar, "limit": "none", "stars_status": "measured", "gas_cold_status": "absent",
                "gas_hot_status": "absent", "observed_from": ";".join(bin_ids[c.dataset]), "baryonic_from": ";".join(bar),
                "model_dependence": "observable_form", "evidence_tier": 1,
                "role": "default" if is_default else "alternative", "alternative_of": None,
                "plotted": "true" if is_default else "false", "not_plotted_reason": reason or None,
                "assumptions": ASSUMPTIONS, "adjustable": "", "flags": "edges_inferred",
                "source_ref": f"veldis.html {s.name} ({c.dataset}); mwgc.dat; J/ApJS/161/304 models, clusters",
                "notes": " | ".join(notes) or None, "x_gc_baumgardt_dataset": c.dataset, "x_gc_baumgardt_sigma": sig,
                "x_gc_baumgardt_sigma_err_lo": lo, "x_gc_baumgardt_sigma_err_hi": hi, "x_gc_baumgardt_coverage": c.result.coverage,
                "x_gc_baumgardt_n_bins": c.result.n_bins, "x_gc_baumgardt_r_h_pc": s.r_h_pc, "x_gc_baumgardt_l_v": s.l_v, "x_gc_baumgardt_ml_v": s.ml_v,
                "x_gc_baumgardt_distance_kpc": D,
            }
            for k, v in row.items():
                m[k].append(v)
        # alternatives point at the default
        for i in range(len(m["measurement_id"]) - len(cand_rows), len(m["measurement_id"])):
            if m["role"][i] == "alternative":
                m["alternative_of"][i] = default_mid or ""

        props = {"status": "plotted" if s.plotted else "recorded",
                 "reasons_not_plotted": [] if s.plotted else (s.reasons or ["no candidate passes the plotting rules"]),
                 "structural_model": s.model_source or None, "r_h_source": s.r_h_source or None,
                 "r_h_pc": s.r_h_pc, "default_dataset": s.default.dataset if s.default else None,
                 "line_of_sight_datasets": sorted(c.dataset for c in s.candidates),
                 "proper_motion_datasets": sorted({b["type"] for b in s.pm_bins}),
                 "candidates": {c.dataset: ({"coverage": round(c.result.coverage, 4), "sigma_rms_km_s": round(c.result.sigma_rms, 4),
                                             "n_bins": c.result.n_bins} if c.result else {"refused": c.refused})
                                for c in s.candidates},
                 "harris_core_flag": (s.harris or {}).get("III:flags") or None}
        s_rows["system_id"].append(sid)
        s_rows["name_in_source"].append(s.name)
        s_rows["class_in_source"].append("globular cluster")
        s_rows["taxonomy_kind"].append(s.kind)
        s_rows["kind_label"].append("ambiguous: dwarf galaxy or star cluster" if s.kind == "A7" else "globular cluster")
        s_rows["host"].append("Milky Way")
        pr = param.get(s.key, {})
        s_rows["ra_deg"].append(A.num(pr.get("RA")))
        s_rows["dec_deg"].append(A.num(pr.get("DEC")))
        if D:
            s_rows["distance_mpc"].append(D / 1000.0)
            s_rows["distance_method"].append("horizontal branch (Harris 1996, 2010 edition)")
            s_rows["distance_kinematic"].append("false")
            s_rows["distance_ref"].append("Harris 1996 (2010 edition), mwgc.dat Part I")
        else:  # recorded only; the database average may include kinematic distances (D-042), so it is marked as such
            s_rows["distance_mpc"].append(A.num(pr.get("R_Sun")) / 1000.0 if A.num(pr.get("R_Sun")) else None)
            s_rows["distance_method"].append("Baumgardt & Vasiliev 2021 average, as listed in parameter.html (may include kinematic methods; never used for g_obs or g_bar)")
            s_rows["distance_kinematic"].append("true")
            s_rows["distance_ref"].append("parameter.html, R_Sun")
        s_rows["metallicity_feh"].append(A.num((s.harris or {}).get("II:[Fe/H]")))
        s_rows["properties"].append(json.dumps(props, ensure_ascii=False, sort_keys=True))

    acc = u.m / u.s ** 2
    meas = Table([
        col("measurement_id", m["measurement_id"], ucd="meta.id;meta.main", description="Permanent measurement identifier"),
        col("system_id", m["system_id"], ucd="meta.id", description="Atlas system identifier"),
        col("kind", m["kind"], ucd="meta.code", description="Kind of measurement"),
        col("channel", m["channel"], ucd="meta.code", description="Observational channel"),
        col("method_class", m["method_class"], ucd="meta.code.class", description="Class of method"),
        col("method", m["method"], ucd="meta.note", description="Method"),
        col("measured_quantity", m["measured_quantity"], ucd="meta.code", description="Quantity measured (D-029)"),
        col("r_kpc", m["r_kpc"], u.kpc, "phys.size.radius", "Three-dimensional half-light radius r½ = 4/3 R_h", True),
        col("r_kind", m["r_kind"], ucd="meta.code", description="Radius is three-dimensional"),
        col("g_obs", m["g_obs"], acc, "phys.acceleration", "Observed acceleration at r½, 3 σ² / r½ (D-025)", True),
        col("g_obs_err_lo", m["g_obs_err_lo"], acc, "stat.error;phys.acceleration", "From the dispersion's lower one-sigma error only", True),
        col("g_obs_err_hi", m["g_obs_err_hi"], acc, "stat.error;phys.acceleration", "From the dispersion's upper one-sigma error only", True),
        col("g_bar", m["g_bar"], acc, "phys.acceleration", "Baryonic acceleration at r½, G (L_V Υ_V / 2) / r½² (D-025)", True),
        col("g_bar_err_lo", m["g_bar_err_lo"], acc, "stat.error;phys.acceleration", "From the population M/L_V one-sigma error only", True),
        col("g_bar_err_hi", m["g_bar_err_hi"], acc, "stat.error;phys.acceleration", "From the population M/L_V one-sigma error only", True),
        col("g_bar_stars", m["g_bar_stars"], acc, "phys.acceleration", "Stellar component of g_bar (all of it; gas absent)", True),
        col("limit", m["limit"], ucd="meta.code", description="Whether g_obs is a limit"),
        col("stars_status", m["stars_status"], ucd="meta.code", description="Stars measured (starlight with population M/L)"),
        col("gas_cold_status", m["gas_cold_status"], ucd="meta.code", description="Absent: literature limit for the kind (D-036 #4)"),
        col("gas_hot_status", m["gas_hot_status"], ucd="meta.code", description="Absent: literature limit for the kind (D-036 #4)"),
        col("observed_from", m["observed_from"], ucd="meta.ref", description="Observables used on the observed side"),
        col("baryonic_from", m["baryonic_from"], ucd="meta.ref", description="Observables used on the baryonic side"),
        col("model_dependence", m["model_dependence"], ucd="meta.code", description="Light weights from a parametric light profile (D-029)"),
        col("evidence_tier", m["evidence_tier"], ucd="meta.code.qual", description="Evidence tier (D-035)", integer=True),
        col("role", m["role"], ucd="meta.code", description="Default value for the system, or an alternative"),
        col("alternative_of", m["alternative_of"], ucd="meta.ref", description="The default measurement this is an alternative to"),
        col("plotted", m["plotted"], ucd="meta.code", description="Shown in default views"),
        col("not_plotted_reason", m["not_plotted_reason"], ucd="meta.note", description="Why not plotted (closed list)"),
        col("assumptions", m["assumptions"], ucd="meta.note", description="Named assumptions affecting this row"),
        col("adjustable", m["adjustable"], ucd="meta.note", description="Assumptions whose sliders can change this row"),
        col("flags", m["flags"], ucd="meta.code", description="Atlas flags"),
        col("source_ref", m["source_ref"], ucd="meta.ref", description="Source files and rows"),
        col("notes", m["notes"], ucd="meta.note", description="Notes"),
        col("x_gc_baumgardt_dataset", m["x_gc_baumgardt_dataset"], ucd="meta.id", description="Dataset code of the profile in veldis.html"),
        col("x_gc_baumgardt_sigma", m["x_gc_baumgardt_sigma"], u.km / u.s, "phys.veloc.dispersion", "Light-weighted line-of-sight dispersion σ_rms", True),
        col("x_gc_baumgardt_sigma_err_lo", m["x_gc_baumgardt_sigma_err_lo"], u.km / u.s, "stat.error;phys.veloc.dispersion", "Lower one-sigma error of σ_rms", True),
        col("x_gc_baumgardt_sigma_err_hi", m["x_gc_baumgardt_sigma_err_hi"], u.km / u.s, "stat.error;phys.veloc.dispersion", "Upper one-sigma error of σ_rms", True),
        col("x_gc_baumgardt_coverage", m["x_gc_baumgardt_coverage"], None, "stat.fit.param", "Fraction of the King-model light inside the bins", True),
        col("x_gc_baumgardt_n_bins", m["x_gc_baumgardt_n_bins"], None, "meta.number", "Number of bins", integer=True),
        col("x_gc_baumgardt_r_h_pc", m["x_gc_baumgardt_r_h_pc"], u.pc, "phys.size.radius", "Projected half-light radius at the Harris distance", True),
        col("x_gc_baumgardt_l_v", m["x_gc_baumgardt_l_v"], u.solLum, "phys.luminosity", "V-band luminosity from Harris M_V,t, M_V,sun = 4.85", True),
        col("x_gc_baumgardt_ml_v", m["x_gc_baumgardt_ml_v"], u.solMass / u.solLum, "phys.composition.massLightRatio", "Population M/L_V (BC03, Chabrier disk IMF)", True),
        col("x_gc_baumgardt_distance_kpc", m["x_gc_baumgardt_distance_kpc"], u.kpc, "pos.distance", "Harris distance", True),
    ])
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    obs_t = Table([
        col("observable_id", obs["observable_id"], ucd="meta.id;meta.main", description="Permanent observable identifier"),
        col("system_id", obs["system_id"], ucd="meta.id", description="Atlas system identifier"),
        col("side", obs["side"], ucd="meta.code", description="Observed or baryonic side"),
        col("quantity", obs["quantity"], ucd="meta.code", description="Quantity (closed list, data standard 2.0)"),
        col("value", obs["value"], None, "meta.number", "Value as printed by the source", True),
        col("err_lo", obs["err_lo"], None, "stat.error", "Lower error as printed", True),
        col("err_hi", obs["err_hi"], None, "stat.error", "Upper error as printed", True),
        col("unit", obs["unit"], ucd="meta.unit", description="Unit of value"),
        col("band", obs["band"], ucd="instr.bandpass", description="Photometric band"),
        col("limit", obs["limit"], ucd="meta.code", description="Whether the value is a limit"),
        col("r_kpc", obs["r_kpc"], u.kpc, "pos.distance;phys.size.radius", "Projected radius of the bin at the Harris distance", True),
        col("r_kind", obs["r_kind"], ucd="meta.code", description="Radius kind"),
        col("steps", obs["steps"], ucd="meta.note", description="Processing ladder from data to this quantity"),
        col("evidence_tier", obs["evidence_tier"], ucd="meta.code.qual", description="Evidence tier (D-035)", integer=True),
        col("source_ref", obs["source_ref"], ucd="meta.ref", description="Source file and row"),
        col("x_gc_baumgardt_r_arcsec", obs["x_gc_baumgardt_r_arcsec"], u.arcsec, "pos.angDistance", "Mean projected radius of the bin, as printed", True),
        col("x_gc_baumgardt_n_star", obs["x_gc_baumgardt_n_star"], None, "meta.number", "Stars in the bin, as printed (empty for IFU data)", True),
        col("x_gc_baumgardt_dataset", obs["x_gc_baumgardt_dataset"], ucd="meta.id", description="Dataset code in veldis.html"),
        col("x_gc_baumgardt_parameter", obs["x_gc_baumgardt_parameter"], ucd="meta.note", description="Which source parameter this row is"),
    ])
    obs_t.meta = dict(meas.meta)
    sys_t = Table([
        col("system_id", s_rows["system_id"], ucd="meta.id;meta.main", description="Atlas system identifier"),
        col("name_in_source", s_rows["name_in_source"], ucd="meta.id", description="Cluster name as in veldis.html"),
        col("class_in_source", s_rows["class_in_source"], ucd="src.class", description="Class as the source gives it"),
        col("taxonomy_kind", s_rows["taxonomy_kind"], ucd="meta.code", description="Taxonomy kind (A0–A10)"),
        col("kind_label", s_rows["kind_label"], ucd="meta.note", description="Kind label"),
        col("host", s_rows["host"], ucd="meta.id", description="Host galaxy (property, never a filter)"),
        col("ra_deg", s_rows["ra_deg"], u.deg, "pos.eq.ra;meta.main", "Right ascension (J2000), parameter.html", True),
        col("dec_deg", s_rows["dec_deg"], u.deg, "pos.eq.dec;meta.main", "Declination (J2000), parameter.html", True),
        col("distance_mpc", s_rows["distance_mpc"], u.Mpc, "pos.distance", "Distance (see distance_method)", True),
        col("distance_method", s_rows["distance_method"], ucd="meta.note", description="Distance method"),
        col("distance_kinematic", s_rows["distance_kinematic"], ucd="meta.code", description="Distance derived from kinematics"),
        col("distance_ref", s_rows["distance_ref"], ucd="meta.ref", description="Distance source"),
        col("metallicity_feh", s_rows["metallicity_feh"], None, "phys.abund.Fe", "[Fe/H], Harris 2010", True),
        col("properties", s_rows["properties"], ucd="meta.note", description="Status, reasons and candidates (JSON)"),
    ])
    sys_t.meta = dict(meas.meta)

    (HERE / "tables").mkdir(exist_ok=True)
    meas.write(HERE / "tables/measurements.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    obs_t.write(HERE / "tables/observables.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    sys_t.write(HERE / "tables/systems.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)

    transcription_test(sys_t)

    # arithmetic test 3: recompute from the stored columns
    for i in range(len(meas)):
        r_m = meas["r_kpc"][i] * 1000.0 * A.PC
        g1 = 3.0 * (meas["x_gc_baumgardt_sigma"][i] * 1e3) ** 2 / r_m
        g2 = A.G * 0.5 * meas["x_gc_baumgardt_l_v"][i] * meas["x_gc_baumgardt_ml_v"][i] * A.M_SUN / r_m ** 2
        if abs(g1 / meas["g_obs"][i] - 1) > 1e-9 or abs(g2 / meas["g_bar"][i] - 1) > 1e-9:
            raise SystemExit(f"arithmetic test 3 failed at {meas['measurement_id'][i]}")

    desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
    write_datapackage(HERE, desc, {"measurements": ("tables/measurements.ecsv", meas),
                                   "observables": ("tables/observables.ecsv", obs_t),
                                   "systems": ("tables/systems.ecsv", sys_t)})
    write_checksums(HERE)
    n_plot = sum(1 for v in m["plotted"] if v == "true")
    print(f"wrote {len(meas)} measurements ({n_plot} plotted), {len(obs_t)} observables, {len(sys_t)} systems; "
          "tests 1 and 3 pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
