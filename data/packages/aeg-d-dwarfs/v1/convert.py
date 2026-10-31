"""Convert the A5/A7 dwarf-galaxy inputs into the Atlas data standard 2.0.0.

Usage: python data/packages/aeg-d-dwarfs/v1/convert.py
       (AEG_REGISTER=1 once, by the maintainer, to add new systems to data/registry/systems.csv)

Reads reading/conversion_inputs.csv (assembled by the frozen reproduction/inputs.py from the
double-read originals and the rulings D-048 to D-061) and the LVDB index for positions and
host; writes tables/measurements.ecsv, tables/observables.ecsv, tables/systems.ecsv,
datapackage.json and checksums.sha256, then runs REPRODUCTION.md test 3 (arithmetic).
Test 2 (transcription against the second reading) runs in reproduction/test2_transcription.py.

Per plotted system (D-025):
  r_half   = 4/3 R_h, R_h circularised (D-048 item 2), at the package distance
  g_obs    = 3 sigma^2 / r_half                        (upper limit where sigma is a limit)
  g_bar    = G (L_V Upsilon_V / 2 + M_gas(<r_half)) / r_half^2
  errors:  g_obs from the printed sigma errors; g_bar from the magnitude errors only
           (Upsilon_V is the adjustable assumption dw_stellar_ml, D-060; distance enters both
           sides and has no slider).
"""

from __future__ import annotations

import csv
import glob
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
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg.package import write_checksums, write_datapackage  # noqa: E402

DATASET, VERSION, STANDARD = "aeg-d-dwarfs", "v1", "2.0.0"
PID = f"{DATASET}/{VERSION}"
TODAY = "2026-10-31"
G = 6.67430e-11
PC = 3.0856775814913673e16
M_SUN = 1.98840987e30
HOSTS = {"mw": "Milky Way", "m_031": "M31", "": "Local Group field"}
CORE_FLAGS = {"beyond_source_range"}
ASSUMPTIONS = ("dw_equilibrium;dw_rhalf_wolf;dw_rh_circularised;dw_distance;dw_magnitude_modulus;dw_stellar_ml;"
               "helium_factor;dw_hi_distance_rescaled;dw_gas_half_total")
METHOD = "half-light-radius estimator (Wolf et al. 2010) on the published line-of-sight velocity dispersion (D-025, D-038)"


def num(x):
    try:
        return float(str(x).replace("−", "-"))
    except (TypeError, ValueError):
        return None


def col(name, data, unit=None, ucd=None, description="", numeric=False, integer=False):
    data = list(data)
    if numeric or integer:
        mask = [x is None for x in data]
        arr = (np.array([0 if x is None else int(x) for x in data], dtype="i8") if integer
               else np.array([np.nan if x is None else x for x in data], dtype="f8"))
        c = MaskedColumn(arr, name=name, mask=mask, unit=unit, description=description)
    else:
        c = MaskedColumn([("" if x is None else str(x)) for x in data], name=name, description=description, dtype=str)
    c.meta["ucd"] = ucd
    return c


def registry(names: list[str]) -> dict[str, str]:
    path = ROOT / "data/registry/systems.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    ids = {r["primary_name"]: r["system_id"] for r in rows if r["first_dataset"] == PID}
    missing = [n for n in names if n not in ids]
    if missing:
        if os.environ.get("AEG_REGISTER") != "1":
            raise SystemExit(f"{len(missing)} systems not in the registry; run once with AEG_REGISTER=1")
        n = max(int(r["system_id"].split("-")[-1]) for r in rows)
        with path.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for name in missing:
                n += 1
                ids[name] = f"aeg-s-{n:06d}"
                w.writerow([ids[name], name, PID, TODAY])
    return ids


def accelerations(r: dict) -> dict:
    """g_obs and g_bar from the stored inputs; used for writing and for test 3."""
    d_pc = float(r["distance_kpc"]) * 1000.0
    R_h_pc = float(r["R_h_arcmin"]) / 60.0 * math.pi / 180.0 * d_pc
    r_half_m = 4.0 / 3.0 * R_h_pc * PC
    sig = float(r["sigma"]) * 1e3
    m_star = 0.5 * float(r["L_V"]) * float(r["upsilon_v"])
    m_gas = float(r["m_gas_rh"] or 0.0)
    return {"r_half_pc": r_half_m / PC, "g_obs": 3.0 * sig ** 2 / r_half_m,
            "g_bar_stars": G * m_star * M_SUN / r_half_m ** 2, "g_bar_gas": G * m_gas * M_SUN / r_half_m ** 2}


def main() -> int:
    inputs = list(csv.DictReader(open(HERE / "reading/conversion_inputs.csv", encoding="utf-8")))
    kinds = {r["key"]: r for r in csv.DictReader(open(HERE / "reading/kinds.csv", encoding="utf-8"))}
    lv = {}
    for f in sorted(glob.glob(str(HERE / "source/lvdb/dwarf_*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            lv[r["key"]] = r
    feh = {r["key"]: r for r in csv.DictReader(open(HERE / "reading/feh_values.csv", encoding="utf-8"))}
    woo = {r["key"]: r for r in csv.DictReader(open(HERE / "reading/woo_reading_1.csv", encoding="utf-8")) if r["quantity"] == "ml_star"}
    woo.update({r["key"]: r for r in csv.DictReader(open(HERE / "reading/woo_reading_1_followup.csv", encoding="utf-8")) if r["quantity"] == "ml_star"})
    gasv = {r["key"]: r for r in csv.DictReader(open(HERE / "reading/gas_values.csv", encoding="utf-8"))}
    ids = registry([kinds[r["key"]]["name"] for r in inputs])

    obs = {k: [] for k in ("observable_id", "system_id", "side", "quantity", "value", "err_lo", "err_hi", "unit", "band",
                           "limit", "steps", "evidence_tier", "source_ref", "x_dwarfs_parameter")}
    meas_rows, sys_rows = [], []

    def add_obs(sid, side, q, value, unit, steps, ref, lo=None, hi=None, band="", limit="none", param=""):
        oid = f"{PID}/o{len(obs['observable_id']) + 1:06d}"
        for k, v in (("observable_id", oid), ("system_id", sid), ("side", side), ("quantity", q), ("value", value),
                     ("err_lo", lo), ("err_hi", hi), ("unit", unit), ("band", band), ("limit", limit), ("steps", steps),
                     ("evidence_tier", 1), ("source_ref", ref), ("x_dwarfs_parameter", param)):
            obs[k].append(v)
        return oid

    for r in inputs:
        k = r["key"]
        name = kinds[k]["name"]
        sid = ids[name]
        L = lv[k]
        plotted = r.get("status") == "plotted"
        if plotted and float(r["sigma"]) == 0.0 and r["sigma_limit"] == "none":
            plotted = False
            r["reason"] = (f"best-fit dispersion 0.0 (+{r['sigma_err_plus']}) with no stated limit "
                           f"({r['sigma_paper']}); recorded, awaiting a ruling")
        fl = (r.get("flags") or "").split()
        if not r.get("distance_kpc"):
            r["distance_kpc"] = L.get("distance")
            r["distance_source"] = "LVDB index value, recorded only (never used for g_obs or g_bar)"
        sys_rows.append({"system_id": sid, "name_in_source": name, "class_in_source": "dwarf galaxy (LVDB)",
                         "taxonomy_kind": kinds[k]["kind"],
                         "kind_label": "dwarf galaxy" if kinds[k]["kind"] == "A5" else "ambiguous: dwarf galaxy or star cluster",
                         "host": HOSTS.get(L.get("host", ""), L.get("host", "")),
                         "ra_deg": num(L["ra"]), "dec_deg": num(L["dec"]),
                         "distance_mpc": num(r.get("distance_kpc")) / 1000.0 if num(r.get("distance_kpc")) else None,
                         "distance_method": ("LVDB index value; method not read, so treated as possibly kinematic (never used for g_obs or g_bar)" if r["distance_source"].startswith("LVDB index")
                                             else "stellar population (see distance_ref)"),
                         "distance_kinematic": "true" if r["distance_source"].startswith("LVDB index") else "false",
                         "distance_ref": r.get("distance_source", ""),
                         "metallicity_feh": num(feh.get(k, {}).get("feh")),
                         "properties": json.dumps({"status": "plotted" if plotted else "recorded",
                                                   "reason_not_plotted": r.get("reason") or None, "lvdb_key": k,
                                                   "flags": fl}, ensure_ascii=False, sort_keys=True)})
        if not plotted:
            continue
        lim = r["sigma_limit"] if r["sigma_limit"] in ("upper",) else "none"
        s_lo, s_hi = num(r["sigma_err_minus"]), num(r["sigma_err_plus"])
        o_sig = add_obs(sid, "observed", "sigma_los", float(r["sigma"]), "km / s",
                        "spectra;stellar_velocities;membership;binary_treatment;dispersion_global",
                        f"{r['sigma_paper']} (reading/sigma_selection_v3.csv)", s_lo, s_hi, limit=lim,
                        param=f"limit level {r['sigma_limit_level']}" if lim == "upper" else "")
        bar = []
        bar.append(add_obs(sid, "baryonic", "distance", float(r["distance_kpc"]), "kpc", "photometry", r["distance_source"],
                           num(r["distance_err_minus"]), num(r["distance_err_plus"])))
        bar.append(add_obs(sid, "baryonic", "half_light_radius", float(r["rh_printed"]), r["rh_unit"],
                           "photometry;structural_model", r["rh_source"], param=f"as printed ({r['rh_convention']})"))
        bar.append(add_obs(sid, "baryonic", "structural_param", float(r["ellipticity"]), "", "photometry;structural_model",
                           r["rh_source"], param="ellipticity 1 - b/a"))
        if r.get("m_V0"):
            bar.append(add_obs(sid, "baryonic", "apparent_magnitude", float(r["m_V0"]), "mag", "photometry;luminosity",
                               r["mag_source"], num(r["mag_err_minus"]), num(r["mag_err_plus"]), band="V",
                               param="extinction-corrected m_V,0"))
        bar.append(add_obs(sid, "baryonic", "luminosity", float(r["L_V"]), "solLum", "photometry;luminosity",
                           r["mag_source"] or "", band="V", param="L_V at the package distance, M_V,sun = 4.85"))
        fe = feh[k]
        bar.append(add_obs(sid, "baryonic", "metallicity_feh", float(r["feh"]), "", "spectra", fe["paper"],
                           num(fe["err_minus"]), num(fe["err_plus"]), param=fe["quantity"]))
        bar.append(add_obs(sid, "baryonic", "stellar_ml_population", float(r["upsilon_v"]), "solMass / solLum", "stellar_ml",
                           "J/ApJS/161/304/clusters (M/L)1, interpolated (reading/upsilon_v.csv)", band="V",
                           param="default; D-060 range in measurements x_dwarfs_upsilon_v_low/high"))
        if k in woo:
            add_obs(sid, "baryonic", "star_formation_history_ml", float(woo[k]["value"]), "solMass / solLum", "stellar_ml",
                    "Woo et al. 2008 Table 1, data set b", band="V", param="alternative (D-059 item 1); method per galaxy not stated")
        gv = gasv.get(k, {})
        if r["gas_status"] == "measured":
            bar.append(add_obs(sid, "baryonic", "mass_hi", float(r["m_hi_pkg"]), "solMass", "hi_21cm;mass",
                               f"Putman et al. 2021 Table 1, {gv.get('Galaxy')}", param=f"rescaled from D = {r['d_putman_kpc']} kpc (D-058)"))
        elif r["gas_status"].startswith("absent"):
            bar.append(add_obs(sid, "baryonic", "mass_gas_limit", float(r["m_hi_pkg"]), "solMass", "hi_21cm;mass",
                               f"Putman et al. 2021 Table 1, {gv.get('Galaxy')}", limit="upper",
                               param=f"5 sigma HI limit, rescaled from D = {r['d_putman_kpc']} kpc (D-058)"))
        a = accelerations(r)
        g_obs, g_st, g_gas = a["g_obs"], a["g_bar_stars"], a["g_bar_gas"]
        g_bar = g_st + g_gas
        zero = float(r["sigma"]) == 0.0 and lim == "none"
        if lim == "upper" or zero:
            go_lo = go_hi = None
        else:
            sig = float(r["sigma"])
            go_lo = g_obs * (1 - ((sig - (s_lo or 0)) / sig) ** 2)
            go_hi = g_obs * (((sig + (s_hi or 0)) / sig) ** 2 - 1)
        m_lo, m_hi = num(r.get("mag_err_minus")), num(r.get("mag_err_plus"))
        # brighter by m_lo -> more light: g_bar_stars up by 10^(0.4 m_lo) - 1
        gb_hi = g_st * (10 ** (0.4 * m_lo) - 1) if m_lo is not None else None
        gb_lo = g_st * (1 - 10 ** (-0.4 * m_hi)) if m_hi is not None else None
        core = [f for f in fl if f in CORE_FLAGS]
        if gb_lo is None and gb_hi is None:
            core.append("no_uncertainty")
        meas_rows.append({
            "measurement_id": f"{PID}/m{len(meas_rows) + 1:06d}", "system_id": sid, "kind": "system_value",
            "channel": "dynamics", "method_class": "kinematic", "method": METHOD, "measured_quantity": "g_obs",
            "r_kpc": a["r_half_pc"] / 1000.0, "r_kind": "3d", "g_obs": g_obs, "g_obs_err_lo": go_lo, "g_obs_err_hi": go_hi,
            "g_bar": g_bar, "g_bar_err_lo": gb_lo, "g_bar_err_hi": gb_hi, "g_bar_stars": g_st, "g_bar_gas_cold": g_gas,
            "limit": lim, "stars_status": "measured", "gas_cold_status": "measured" if r["gas_status"] == "measured" else "absent",
            "gas_hot_status": "absent", "observed_from": o_sig, "baryonic_from": ";".join(bar),
            "model_dependence": "none", "evidence_tier": 1, "role": "default", "plotted": "false" if zero else "true",
            "not_plotted_reason": "other" if zero else None,
            "assumptions": ASSUMPTIONS, "adjustable": "dw_stellar_ml", "flags": ";".join(dict.fromkeys(core)),
            "source_ref": f"{r['sigma_paper']}; {r['rh_source']}; {r['distance_source']}; {r['mag_source']}",
            "notes": (f"best-fit dispersion 0.0 (+{r['sigma_err_plus']}) with no stated limit; recorded, awaiting a ruling"
                      if zero else None), "x_dwarfs_flags": " ".join(f for f in fl if f not in CORE_FLAGS),
            "x_dwarfs_sigma": float(r["sigma"]), "x_dwarfs_sigma_err_lo": s_lo, "x_dwarfs_sigma_err_hi": s_hi,
            "x_dwarfs_sigma_limit_level": r["sigma_limit_level"], "x_dwarfs_R_h_arcmin": float(r["R_h_arcmin"]),
            "x_dwarfs_distance_kpc": float(r["distance_kpc"]), "x_dwarfs_l_v": float(r["L_V"]),
            "x_dwarfs_upsilon_v": float(r["upsilon_v"]), "x_dwarfs_upsilon_v_low": float(r["upsilon_v_low"]),
            "x_dwarfs_upsilon_v_high": float(r["upsilon_v_high"]), "x_dwarfs_m_gas_rh": float(r["m_gas_rh"] or 0.0),
            "x_dwarfs_gas_status": r["gas_status"],
        })

    acc = u.m / u.s ** 2
    M = {k: [row.get(k) for row in meas_rows] for k in meas_rows[0]}
    meas = Table([
        col("measurement_id", M["measurement_id"], ucd="meta.id;meta.main", description="Permanent measurement identifier"),
        col("system_id", M["system_id"], ucd="meta.id", description="Atlas system identifier"),
        col("kind", M["kind"], ucd="meta.code", description="Kind of measurement"),
        col("channel", M["channel"], ucd="meta.code", description="Observational channel"),
        col("method_class", M["method_class"], ucd="meta.code.class", description="Class of method"),
        col("method", M["method"], ucd="meta.note", description="Method"),
        col("measured_quantity", M["measured_quantity"], ucd="meta.code", description="Quantity measured (D-029)"),
        col("r_kpc", M["r_kpc"], u.kpc, "phys.size.radius", "Three-dimensional half-light radius r½ = 4/3 R_h", True),
        col("r_kind", M["r_kind"], ucd="meta.code", description="Radius is three-dimensional"),
        col("g_obs", M["g_obs"], acc, "phys.acceleration", "Observed acceleration at r½, 3 σ² / r½ (D-025); an upper limit where limit = upper", True),
        col("g_obs_err_lo", M["g_obs_err_lo"], acc, "stat.error;phys.acceleration", "From the dispersion's printed lower error only", True),
        col("g_obs_err_hi", M["g_obs_err_hi"], acc, "stat.error;phys.acceleration", "From the dispersion's printed upper error only", True),
        col("g_bar", M["g_bar"], acc, "phys.acceleration", "Baryonic acceleration at r½, G (L_V Υ_V / 2 + M_gas(<r½)) / r½² (D-025)", True),
        col("g_bar_err_lo", M["g_bar_err_lo"], acc, "stat.error;phys.acceleration", "From the magnitude error only (stars)", True),
        col("g_bar_err_hi", M["g_bar_err_hi"], acc, "stat.error;phys.acceleration", "From the magnitude error only (stars)", True),
        col("g_bar_stars", M["g_bar_stars"], acc, "phys.acceleration", "Stellar component of g_bar", True),
        col("g_bar_gas_cold", M["g_bar_gas_cold"], acc, "phys.acceleration", "Atomic gas with helium (1.33 M_HI), half the total inside r½ (D-058); 0 where absent", True),
        col("limit", M["limit"], ucd="meta.code", description="Whether g_obs is a limit"),
        col("stars_status", M["stars_status"], ucd="meta.code", description="Stars measured (starlight with population M/L)"),
        col("gas_cold_status", M["gas_cold_status"], ucd="meta.code", description="Atomic gas: measured (Putman et al. 2021 detection) or absent (5σ limit, or not addressed); see x_dwarfs_gas_status"),
        col("gas_hot_status", M["gas_hot_status"], ucd="meta.code", description="Hot gas not included (not addressed by the sources)"),
        col("observed_from", M["observed_from"], ucd="meta.ref", description="Observables used on the observed side"),
        col("baryonic_from", M["baryonic_from"], ucd="meta.ref", description="Observables used on the baryonic side"),
        col("model_dependence", M["model_dependence"], ucd="meta.code", description="No fitted form on the observed side"),
        col("evidence_tier", M["evidence_tier"], ucd="meta.code.qual", description="Evidence tier (D-035)", integer=True),
        col("role", M["role"], ucd="meta.code", description="Default value for the system"),
        col("plotted", M["plotted"], ucd="meta.code", description="Shown in default views"),
        col("not_plotted_reason", M["not_plotted_reason"], ucd="meta.note", description="Why not plotted (closed list)"),
        col("assumptions", M["assumptions"], ucd="meta.note", description="Named assumptions affecting this row"),
        col("adjustable", M["adjustable"], ucd="meta.note", description="Assumptions whose sliders can change this row"),
        col("flags", M["flags"], ucd="meta.code", description="Atlas flags"),
        col("source_ref", M["source_ref"], ucd="meta.ref", description="Originals: dispersion; structure; distance; magnitude"),
        col("notes", M["notes"], ucd="meta.note", description="Notes"),
        col("x_dwarfs_flags", M["x_dwarfs_flags"], ucd="meta.code", description="Package flags: how each input was chosen (rulings in docs/decisions.md)"),
        col("x_dwarfs_sigma", M["x_dwarfs_sigma"], u.km / u.s, "phys.veloc.dispersion", "Published line-of-sight dispersion (or its upper limit)", True),
        col("x_dwarfs_sigma_err_lo", M["x_dwarfs_sigma_err_lo"], u.km / u.s, "stat.error;phys.veloc.dispersion", "Printed lower error", True),
        col("x_dwarfs_sigma_err_hi", M["x_dwarfs_sigma_err_hi"], u.km / u.s, "stat.error;phys.veloc.dispersion", "Printed upper error", True),
        col("x_dwarfs_sigma_limit_level", M["x_dwarfs_sigma_limit_level"], ucd="meta.note", description="Confidence level of an upper limit, as stated"),
        col("x_dwarfs_R_h_arcmin", M["x_dwarfs_R_h_arcmin"], u.arcmin, "phys.angSize", "Circularised projected half-light radius", True),
        col("x_dwarfs_distance_kpc", M["x_dwarfs_distance_kpc"], u.kpc, "pos.distance", "Package distance", True),
        col("x_dwarfs_l_v", M["x_dwarfs_l_v"], u.solLum, "phys.luminosity", "V-band luminosity at the package distance, M_V,sun = 4.85", True),
        col("x_dwarfs_upsilon_v", M["x_dwarfs_upsilon_v"], u.solMass / u.solLum, "phys.composition.massLightRatio", "Population Υ_V default (D-059)", True),
        col("x_dwarfs_upsilon_v_low", M["x_dwarfs_upsilon_v_low"], u.solMass / u.solLum, "phys.composition.massLightRatio", "D-060 lower bound", True),
        col("x_dwarfs_upsilon_v_high", M["x_dwarfs_upsilon_v_high"], u.solMass / u.solLum, "phys.composition.massLightRatio", "D-060 upper bound", True),
        col("x_dwarfs_m_gas_rh", M["x_dwarfs_m_gas_rh"], u.solMass, "phys.mass", "Gas mass inside r½ (1.33 × half the rescaled HI mass), 0 where absent", True),
        col("x_dwarfs_gas_status", M["x_dwarfs_gas_status"], ucd="meta.code", description="measured, absent (measured limit) or not addressed (D-035 d)"),
    ])
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    obs_t = Table([
        col("observable_id", obs["observable_id"], ucd="meta.id;meta.main", description="Permanent observable identifier"),
        col("system_id", obs["system_id"], ucd="meta.id", description="Atlas system identifier"),
        col("side", obs["side"], ucd="meta.code", description="Observed or baryonic side"),
        col("quantity", obs["quantity"], ucd="meta.code", description="Quantity (closed list, data standard 2.0)"),
        col("value", obs["value"], None, "meta.number", "Value (as printed, or as converted where x_dwarfs_parameter says)", True),
        col("err_lo", obs["err_lo"], None, "stat.error", "Lower error", True),
        col("err_hi", obs["err_hi"], None, "stat.error", "Upper error", True),
        col("unit", obs["unit"], ucd="meta.unit", description="Unit of value"),
        col("band", obs["band"], ucd="instr.bandpass", description="Photometric band"),
        col("limit", obs["limit"], ucd="meta.code", description="Whether the value is a limit"),
        col("steps", obs["steps"], ucd="meta.note", description="Processing ladder from data to this quantity"),
        col("evidence_tier", obs["evidence_tier"], ucd="meta.code.qual", description="Evidence tier (D-035)", integer=True),
        col("source_ref", obs["source_ref"], ucd="meta.ref", description="Source and location"),
        col("x_dwarfs_parameter", obs["x_dwarfs_parameter"], ucd="meta.note", description="Which value this row is"),
    ])
    obs_t.meta = dict(meas.meta)
    S = {k: [row[k] for row in sys_rows] for k in sys_rows[0]}
    sys_t = Table([
        col("system_id", S["system_id"], ucd="meta.id;meta.main", description="Atlas system identifier"),
        col("name_in_source", S["name_in_source"], ucd="meta.id", description="Name as in the LVDB index"),
        col("class_in_source", S["class_in_source"], ucd="src.class", description="Class as the source gives it"),
        col("taxonomy_kind", S["taxonomy_kind"], ucd="meta.code", description="Taxonomy kind (D-048, D-049)"),
        col("kind_label", S["kind_label"], ucd="meta.note", description="Kind label"),
        col("host", S["host"], ucd="meta.id", description="Host (property, never a filter)"),
        col("ra_deg", S["ra_deg"], u.deg, "pos.eq.ra;meta.main", "Right ascension (J2000), LVDB", True),
        col("dec_deg", S["dec_deg"], u.deg, "pos.eq.dec;meta.main", "Declination (J2000), LVDB", True),
        col("distance_mpc", S["distance_mpc"], u.Mpc, "pos.distance", "Package distance", True),
        col("distance_method", S["distance_method"], ucd="meta.note", description="Distance method"),
        col("distance_kinematic", S["distance_kinematic"], ucd="meta.code", description="Distance derived from kinematics"),
        col("distance_ref", S["distance_ref"], ucd="meta.ref", description="Distance source"),
        col("metallicity_feh", S["metallicity_feh"], None, "phys.abund.Fe", "[Fe/H] (D-057, D-059)", True),
        col("properties", S["properties"], ucd="meta.note", description="Status, reasons and flags (JSON)"),
    ])
    sys_t.meta = dict(meas.meta)

    (HERE / "tables").mkdir(exist_ok=True)
    meas.write(HERE / "tables/measurements.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    obs_t.write(HERE / "tables/observables.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    sys_t.write(HERE / "tables/systems.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)

    # REPRODUCTION.md test 3: recompute g_obs and g_bar from the stored columns, to 1e-9
    back = Table.read(HERE / "tables/measurements.ecsv", format="ascii.ecsv")
    for row in back:
        r_m = row["r_kpc"] * 1000.0 * PC
        g1 = 3.0 * (row["x_dwarfs_sigma"] * 1e3) ** 2 / r_m
        g2 = G * (0.5 * row["x_dwarfs_l_v"] * row["x_dwarfs_upsilon_v"] + row["x_dwarfs_m_gas_rh"]) * M_SUN / r_m ** 2
        if abs(g1 / row["g_obs"] - 1) > 1e-9 or abs(g2 / row["g_bar"] - 1) > 1e-9:
            raise SystemExit(f"arithmetic test 3 failed at {row['measurement_id']}")
    desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
    write_datapackage(HERE, desc, {"measurements": ("tables/measurements.ecsv", meas),
                                   "observables": ("tables/observables.ecsv", obs_t),
                                   "systems": ("tables/systems.ecsv", sys_t)})
    write_checksums(HERE)
    print(f"wrote {len(meas)} measurements, {len(obs_t)} observables, {len(sys_t)} systems; test 3 passes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
