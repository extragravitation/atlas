"""Convert SPARC mass models into the Atlas data standard 2.3.0 (aeg-d-sparc/v2; D-083, D-084).

Usage: python data/packages/aeg-d-sparc/v2/convert.py

Reads source/ (fetched and hash-verified by `python -m aeg.fetch`); writes tables/measurements.ecsv,
tables/observables.ecsv, tables/systems.ecsv, tables/uncertainty_terms.ecsv, datapackage.json and
checksums.sha256.

v2 changes no value of v1 (REPRODUCTION.md test 1): g_obs, g_bar and its components are computed
with v1's expressions, in v1's order, so they are bit-for-bit identical. What v2 adds:
  - point-scale g_obs errors (velocity only) and empty point-scale g_bar errors (none given);
  - the uncertainty-terms table (system- and dataset-scale terms, sizes as the source states them);
  - the 2.0 structure: observables, the 2.0 measurement columns, descriptor fields.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.table import MaskedColumn, Table

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "pipeline"))
from aeg.package import write_checksums, write_datapackage  # noqa: E402

DATASET, VERSION, STANDARD = "aeg-d-sparc", "v2", "2.3.0"

# Catalogue defaults, read at source: arXiv:1606.09251 (eq. 2) and arXiv:1610.08981 (Table 1). As v1.
ML_DISK, ML_BULGE = 0.5, 0.7
HELIUM_FACTOR = 1.33  # included in Vgas by the source (arXiv:1606.09251 §3.4)

KMS2_PER_KPC_TO_MS2 = (1 * u.km / u.s) ** 2 / (1 * u.kpc)
CONV = KMS2_PER_KPC_TO_MS2.to(u.m / u.s**2).value  # (km/s)^2 / kpc -> m/s^2, as v1

HUBBLE_TYPES = {0: "S0", 1: "Sa", 2: "Sab", 3: "Sb", 4: "Sbc", 5: "Sc", 6: "Scd",
                7: "Sd", 8: "Sdm", 9: "Sm", 10: "Im", 11: "BCD"}
DISTANCE_METHODS = {
    1: "Hubble flow (H0 = 73 km/s/Mpc, Virgo-centric infall corrected)",
    2: "Tip of the red giant branch",
    3: "Cepheids",
    4: "Ursa Major cluster",
    5: "Supernova light curve",
}
# Processing steps (standard §4b) for each distance method, as described in arXiv:1606.09251 §2.2.
DISTANCE_STEPS = {1: "spectra", 2: "photometry", 3: "photometry", 4: "photometry", 5: "photometry"}
GAS_MODELLED = {"D512-2", "D564-8", "D631-7"}  # arXiv:1606.09251 §3.4: exponential gas profile assumed

LTG_KIND = ("A4", "late-type or irregular galaxy (Hubble type from SPARC)")
S0_KIND = ("A6", "lenticular galaxy (Hubble type S0 from SPARC)")


def tokens(path: Path, n: int, numeric_from: tuple[int, int]) -> list[list[str]]:
    """Whitespace-separated data rows with exactly n fields (as v1; see its docstring)."""
    out = []
    for line in path.read_text(encoding="ascii").splitlines():
        parts = line.split()
        if len(parts) != n:
            continue
        try:
            [float(x) for x in parts[numeric_from[0]:numeric_from[1]]]
        except ValueError:
            continue
        out.append(parts)
    return out


def read_table1(path: Path) -> list[dict]:
    out = []
    for p in tokens(path, 19, (1, 18)):
        out.append({
            "name": p[0], "T": int(p[1]),
            "D": float(p[2]), "e_D": float(p[3]), "f_D": int(p[4]),
            "inc": float(p[5]), "e_inc": float(p[6]),
            "L36": float(p[7]), "e_L36": float(p[8]),
            "Reff": float(p[9]), "SBeff": float(p[10]),
            "Rdisk": float(p[11]), "SBdisk": float(p[12]),
            "MHI": float(p[13]), "RHI": float(p[14]),
            "Vflat": float(p[15]), "e_Vflat": float(p[16]),
            "Q": int(p[17]), "ref": p[18],
        })
    return out


def read_table2(path: Path) -> list[dict]:
    out = []
    for p in tokens(path, 10, (1, 10)):
        out.append({
            "name": p[0], "D": float(p[1]), "R": float(p[2]),
            "Vobs": float(p[3]), "e_Vobs": float(p[4]),
            "Vgas": float(p[5]), "Vdisk": float(p[6]), "Vbul": float(p[7]),
            "SBdisk": float(p[8]), "SBbul": float(p[9]),
        })
    return out


def signed_sq(v: float) -> float:
    """V|V|: keeps the sign of a contribution (source eq. 2)."""
    return v * abs(v)


def col(name, data, unit=None, ucd=None, description="", dtype=None):
    data = list(data)
    if dtype == "f8":
        mask = [x is None for x in data]
        arr = np.array([np.nan if x is None else x for x in data], dtype="f8")
        c = MaskedColumn(arr, name=name, mask=mask, unit=unit, description=description)
    elif dtype == "i8":
        c = MaskedColumn(np.array(data, dtype="i8"), name=name, description=description)
    elif dtype == "bool":
        c = MaskedColumn(np.array(data, dtype=bool), name=name, description=description)
    else:
        c = MaskedColumn([("" if x is None else x) for x in data], name=name, description=description, dtype=str)
    c.meta["ucd"] = ucd
    return c


def build(source_dir: Path):
    galaxies = read_table1(source_dir / "SPARC_Lelli2016c.mrt")
    rows = read_table2(source_dir / "MassModels_Lelli2016c.mrt")
    by_name = {g["name"]: g for g in galaxies}
    if len(galaxies) != 175 or len(by_name) != 175:
        raise SystemExit(f"expected 175 galaxies, found {len(galaxies)} ({len(by_name)} unique)")
    if len(rows) != 3391:
        raise SystemExit(f"expected 3391 mass-model rows, found {len(rows)}")
    missing = {r["name"] for r in rows} - set(by_name)
    if missing:
        raise SystemExit(f"mass-model galaxies missing from Table 1: {sorted(missing)}")
    if not GAS_MODELLED <= set(by_name):
        raise SystemExit("galaxies with modelled gas not found in Table 1")

    system_ids = {g["name"]: f"aeg-s-{i:06d}" for i, g in enumerate(galaxies, start=1)}
    issues = json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    has_bulge = {r["name"] for r in rows if r["Vbul"] != 0.0}

    # --- observables -------------------------------------------------------------------------
    o = {k: [] for k in ["observable_id", "system_id", "side", "quantity", "value", "err_lo", "err_hi", "unit",
                         "band", "limit", "r_kpc", "r_kind", "steps", "evidence_tier", "source_ref"]}

    def add_obs(system_id, side, quantity, value, err, unit, band, r_kpc, steps, ref) -> str:
        oid = f"{DATASET}/{VERSION}/o{len(o['observable_id']) + 1:06d}"
        o["observable_id"].append(oid)
        o["system_id"].append(system_id)
        o["side"].append(side)
        o["quantity"].append(quantity)
        o["value"].append(value)
        o["err_lo"].append(err)
        o["err_hi"].append(err)
        o["unit"].append(unit)
        o["band"].append(band)
        o["limit"].append("none")
        o["r_kpc"].append(r_kpc)
        o["r_kind"].append("3d" if r_kpc is not None else None)
        o["steps"].append(steps)
        o["evidence_tier"].append(1)
        o["source_ref"].append(ref)
        return oid

    dist_obs = {}
    for k, g in enumerate(galaxies, start=1):
        dist_obs[g["name"]] = add_obs(
            system_ids[g["name"]], "observed", "distance", g["D"], g["e_D"], "Mpc", None, None,
            DISTANCE_STEPS[g["f_D"]],
            f"SPARC_Lelli2016c.mrt:data row {k}, columns D and e_D; method f_D={g['f_D']} "
            f"({DISTANCE_METHODS[g['f_D']]}; arXiv:1606.09251 §2.2)")

    # --- measurements ------------------------------------------------------------------------
    m = {k: [] for k in [
        "measurement_id", "system_id", "kind", "channel", "method_class", "method", "r_kpc", "r_kind",
        "measured_quantity", "g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_obs_err_point_lo", "g_obs_err_point_hi",
        "limit", "g_bar", "g_bar_err_lo", "g_bar_err_hi", "g_bar_err_point_lo", "g_bar_err_point_hi",
        "g_bar_stars", "g_bar_stars_disk", "g_bar_stars_bulge", "g_bar_gas_cold", "g_bar_gas_hot",
        "stars_status", "gas_cold_status", "gas_hot_status", "observed_from", "baryonic_from",
        "model_dependence", "evidence_tier", "role", "plotted", "assumptions", "adjustable",
        "quality_source", "source_ref", "flags", "known_issues", "notes",
        "x_sparc_v_obs", "x_sparc_e_v_obs", "x_sparc_v_gas", "x_sparc_v_disk", "x_sparc_v_bul",
        "x_sparc_sb_disk", "x_sparc_sb_bul"]}

    for i, r in enumerate(rows, start=1):
        g = by_name[r["name"]]
        if abs(r["D"] - g["D"]) > 0.0051:
            raise SystemExit(f"{r['name']}: distance differs between tables ({r['D']} vs {g['D']})")
        sid = system_ids[r["name"]]
        R = r["R"]
        # --- v1 arithmetic, unchanged (REPRODUCTION.md test 1) ---
        g_obs = r["Vobs"] ** 2 / R * CONV
        rel = math.sqrt((2 * r["e_Vobs"] / r["Vobs"]) ** 2
                        + (2 * math.radians(g["e_inc"]) / math.tan(math.radians(g["inc"]))) ** 2
                        + (g["e_D"] / g["D"]) ** 2)
        disk = ML_DISK * signed_sq(r["Vdisk"]) / R * CONV
        bul = ML_BULGE * signed_sq(r["Vbul"]) / R * CONV
        gas = signed_sq(r["Vgas"]) / R * CONV
        stars = disk + bul
        g_bar = stars + gas
        g_bar_err = math.sqrt((0.10 * gas) ** 2 + (0.25 * stars) ** 2)
        # --- v2 additions ---
        point = g_obs * 2 * r["e_Vobs"] / r["Vobs"]  # standard §2a: velocity error only
        bulge = r["name"] in has_bulge
        ref = f"MassModels_Lelli2016c.mrt:data row {i}"
        o_vrot = add_obs(sid, "observed", "v_rot", r["Vobs"], r["e_Vobs"], "km / s", None, R,
                         "rotation_curve", f"{ref}, columns Vobs and e_Vobs")
        bar_ids = [
            add_obs(sid, "baryonic", "v_circ_component", r["Vgas"], None, "km / s", None, R,
                    "hi_21cm;surface_density;helium_factor;potential_from_density",
                    f"{ref}, column Vgas: atomic gas with helium (factor 1.33)"
                    + ("; gas profile assumed exponential (arXiv:1606.09251 §3.4)" if r["name"] in GAS_MODELLED else "")),
            add_obs(sid, "baryonic", "v_circ_component", r["Vdisk"], None, "km / s", "[3.6]", R,
                    "photometry;surface_density;potential_from_density",
                    f"{ref}, column Vdisk: stellar disc at Υ = 1 M☉/L☉"),
            add_obs(sid, "baryonic", "surface_brightness", r["SBdisk"], None, "solLum / pc2", "[3.6]", R,
                    "photometry;surface_density", f"{ref}, column SBdisk: stellar disc"),
        ]
        if bulge:
            bar_ids += [
                add_obs(sid, "baryonic", "v_circ_component", r["Vbul"], None, "km / s", "[3.6]", R,
                        "photometry;surface_density;potential_from_density",
                        f"{ref}, column Vbul: bulge at Υ = 1 M☉/L☉"),
                add_obs(sid, "baryonic", "surface_brightness", r["SBbul"], None, "solLum / pc2", "[3.6]", R,
                        "photometry;surface_density", f"{ref}, column SBbul: bulge"),
            ]
        assumptions = [f"ml_disk={ML_DISK}"] + ([f"ml_bulge={ML_BULGE}"] if bulge else []) + [
            "distance=source", "inclination=source", f"helium_factor={HELIUM_FACTOR}"]
        adjustable = ["ml_disk"] + (["ml_bulge"] if bulge else []) + ["distance", "inclination"]
        mid = f"{DATASET}/{VERSION}/m{i:06d}"
        flags = (["source_quality_low"] if g["Q"] == 3 else []) + sorted({ki["flag"] for ki in issues if mid in ki["measurements"]})
        modelled_gas = r["name"] in GAS_MODELLED

        m["measurement_id"].append(mid)
        m["system_id"].append(sid)
        m["kind"].append("profile_point")
        m["channel"].append("dynamics")
        m["method_class"].append("kinematic")
        m["method"].append("HI/Halpha rotation curve")
        m["r_kpc"].append(R)
        m["r_kind"].append("3d")
        m["measured_quantity"].append("g_obs")
        m["g_obs"].append(g_obs)
        m["g_obs_err_lo"].append(g_obs * rel)
        m["g_obs_err_hi"].append(g_obs * rel)
        m["g_obs_err_point_lo"].append(point)
        m["g_obs_err_point_hi"].append(point)
        m["limit"].append("none")
        m["g_bar"].append(g_bar)
        m["g_bar_err_lo"].append(g_bar_err)
        m["g_bar_err_hi"].append(g_bar_err)
        m["g_bar_err_point_lo"].append(None)
        m["g_bar_err_point_hi"].append(None)
        m["g_bar_stars"].append(stars)
        m["g_bar_stars_disk"].append(disk)
        m["g_bar_stars_bulge"].append(bul if bulge else None)
        m["g_bar_gas_cold"].append(gas)
        m["g_bar_gas_hot"].append(None)
        m["stars_status"].append("measured")
        m["gas_cold_status"].append("modelled" if modelled_gas else "measured")
        m["gas_hot_status"].append("absent")
        m["observed_from"].append(";".join([o_vrot, dist_obs[r["name"]]]))
        m["baryonic_from"].append(";".join(bar_ids))
        m["model_dependence"].append("observable_form" if modelled_gas else "none")
        m["evidence_tier"].append(1)
        m["role"].append("default")
        m["plotted"].append("true")
        m["assumptions"].append(";".join(assumptions))
        m["adjustable"].append(";".join(adjustable))
        m["quality_source"].append(f"Q={g['Q']}")
        m["source_ref"].append(ref)
        m["flags"].append(";".join(flags))
        m["known_issues"].append(";".join(f"#{ki['issue']}" for ki in issues if mid in ki["measurements"]))
        m["notes"].append("Gas profile assumed exponential with scale length 2 R_d; no HI surface density available (arXiv:1606.09251 §3.4)" if modelled_gas else None)
        m["x_sparc_v_obs"].append(r["Vobs"])
        m["x_sparc_e_v_obs"].append(r["e_Vobs"])
        m["x_sparc_v_gas"].append(r["Vgas"])
        m["x_sparc_v_disk"].append(r["Vdisk"])
        m["x_sparc_v_bul"].append(r["Vbul"])
        m["x_sparc_sb_disk"].append(r["SBdisk"])
        m["x_sparc_sb_bul"].append(r["SBbul"])

    acc = u.m / u.s**2
    kms = u.km / u.s
    sb = u.solLum / u.pc**2
    meas = Table([
        col("measurement_id", m["measurement_id"], ucd="meta.id;meta.main", description="Permanent measurement identifier"),
        col("system_id", m["system_id"], ucd="meta.id", description="Permanent system identifier"),
        col("kind", m["kind"], ucd="meta.code", description="Kind of measurement"),
        col("channel", m["channel"], ucd="meta.code", description="Observational channel"),
        col("method_class", m["method_class"], ucd="meta.code.class", description="Class of method"),
        col("method", m["method"], ucd="meta.note", description="Method as given by the source"),
        col("r_kpc", m["r_kpc"], u.kpc, "phys.size.radius", "Galactocentric radius in the disc plane", "f8"),
        col("r_kind", m["r_kind"], ucd="meta.code", description="Radius type"),
        col("measured_quantity", m["measured_quantity"], ucd="meta.code", description="What is measured (standard §3)"),
        col("g_obs", m["g_obs"], acc, "phys.acceleration", "Observed acceleration, V_obs^2/R", "f8"),
        col("g_obs_err_lo", m["g_obs_err_lo"], acc, "stat.error;phys.acceleration", "Lower one-sigma bound, total as in the source (arXiv:1610.08981 eq. 2): velocity (point scale) with inclination and distance (system scale) in quadrature", "f8"),
        col("g_obs_err_hi", m["g_obs_err_hi"], acc, "stat.error;phys.acceleration", "Upper one-sigma bound, total as in the source (arXiv:1610.08981 eq. 2): velocity (point scale) with inclination and distance (system scale) in quadrature", "f8"),
        col("g_obs_err_point_lo", m["g_obs_err_point_lo"], acc, "stat.error;phys.acceleration", "Point-scale part only: velocity error, g_obs * 2 e_Vobs / Vobs (standard 2.2.0 §2a)", "f8"),
        col("g_obs_err_point_hi", m["g_obs_err_point_hi"], acc, "stat.error;phys.acceleration", "Point-scale part only: velocity error, g_obs * 2 e_Vobs / Vobs (standard 2.2.0 §2a)", "f8"),
        col("limit", m["limit"], ucd="meta.code", description="Limit on the measured quantity"),
        col("g_bar", m["g_bar"], acc, "phys.acceleration;meta.modelled", "Newtonian acceleration from detected baryons at catalogue defaults", "f8"),
        col("g_bar_err_lo", m["g_bar_err_lo"], acc, "stat.error;phys.acceleration", "Lower one-sigma bound as in the source (10% HI flux calibration, 25% Υ⋆ scatter; arXiv:1610.08981 §2.1.2). Both terms are system scale (uncertainty_terms.ecsv)", "f8"),
        col("g_bar_err_hi", m["g_bar_err_hi"], acc, "stat.error;phys.acceleration", "Upper one-sigma bound as in the source (10% HI flux calibration, 25% Υ⋆ scatter; arXiv:1610.08981 §2.1.2). Both terms are system scale (uncertainty_terms.ecsv)", "f8"),
        col("g_bar_err_point_lo", m["g_bar_err_point_lo"], acc, "stat.error;phys.acceleration", "Point-scale part: not given by the source (term g_bar_point in uncertainty_terms.ecsv)", "f8"),
        col("g_bar_err_point_hi", m["g_bar_err_point_hi"], acc, "stat.error;phys.acceleration", "Point-scale part: not given by the source (term g_bar_point in uncertainty_terms.ecsv)", "f8"),
        col("g_bar_stars", m["g_bar_stars"], acc, "phys.acceleration;meta.modelled", "Stellar component of g_bar", "f8"),
        col("g_bar_stars_disk", m["g_bar_stars_disk"], acc, "phys.acceleration;meta.modelled", "Stellar disc component of g_bar", "f8"),
        col("g_bar_stars_bulge", m["g_bar_stars_bulge"], acc, "phys.acceleration;meta.modelled", "Bulge component of g_bar; empty where the source has no bulge", "f8"),
        col("g_bar_gas_cold", m["g_bar_gas_cold"], acc, "phys.acceleration;meta.modelled", "Cold gas (atomic hydrogen with helium) component of g_bar; sign kept", "f8"),
        col("g_bar_gas_hot", m["g_bar_gas_hot"], acc, "phys.acceleration;meta.modelled", "Hot gas component of g_bar; not given by the source", "f8"),
        col("stars_status", m["stars_status"], ucd="meta.code", description="Status of the stellar component"),
        col("gas_cold_status", m["gas_cold_status"], ucd="meta.code", description="Status of the cold gas component (modelled for D512-2, D564-8, D631-7)"),
        col("gas_hot_status", m["gas_hot_status"], ucd="meta.code", description="Status of the hot gas component"),
        col("observed_from", m["observed_from"], ucd="meta.id", description="Observables used for g_obs"),
        col("baryonic_from", m["baryonic_from"], ucd="meta.id", description="Observables used for g_bar"),
        col("model_dependence", m["model_dependence"], ucd="meta.code", description="observable_form only where the gas profile is assumed (D-084 addendum)"),
        col("evidence_tier", m["evidence_tier"], ucd="meta.code.qual", description="1 released files", dtype="i8"),
        col("role", m["role"], ucd="meta.code", description="Default or alternative value"),
        col("plotted", m["plotted"], ucd="meta.code", description="Plotted in default views (true/false)"),
        col("assumptions", m["assumptions"], ucd="meta.note", description="Named assumptions affecting this row, with catalogue values"),
        col("adjustable", m["adjustable"], ucd="meta.note", description="Assumptions whose sliders can change this row"),
        col("quality_source", m["quality_source"], ucd="meta.code.qual", description="Source's rotation-curve quality flag (1 high, 2 medium, 3 low); never used to hide rows"),
        col("source_ref", m["source_ref"], ucd="meta.ref", description="Pointer to the source row"),
        col("flags", m["flags"], ucd="meta.code", description="Atlas flags"),
        col("known_issues", m["known_issues"], ucd="meta.ref", description="Open known issues affecting this row (GitHub issue numbers)"),
        col("notes", m["notes"], ucd="meta.note", description="Notes"),
        col("x_sparc_v_obs", m["x_sparc_v_obs"], kms, "phys.veloc.rotat", "SPARC Vobs, as published", "f8"),
        col("x_sparc_e_v_obs", m["x_sparc_e_v_obs"], kms, "stat.error;phys.veloc.rotat", "SPARC e_Vobs, as published", "f8"),
        col("x_sparc_v_gas", m["x_sparc_v_gas"], kms, "phys.veloc.rotat;meta.modelled", "SPARC Vgas, as published (includes helium factor 1.33)", "f8"),
        col("x_sparc_v_disk", m["x_sparc_v_disk"], kms, "phys.veloc.rotat;meta.modelled", "SPARC Vdisk, as published (for M/L = 1 at 3.6 micron)", "f8"),
        col("x_sparc_v_bul", m["x_sparc_v_bul"], kms, "phys.veloc.rotat;meta.modelled", "SPARC Vbul, as published (for M/L = 1 at 3.6 micron)", "f8"),
        col("x_sparc_sb_disk", m["x_sparc_sb_disk"], sb, "phot.flux.sb", "SPARC SBdisk at 3.6 micron, as published", "f8"),
        col("x_sparc_sb_bul", m["x_sparc_sb_bul"], sb, "phot.flux.sb", "SPARC SBbul at 3.6 micron, as published", "f8"),
    ])
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    obs_t = Table([
        col("observable_id", o["observable_id"], ucd="meta.id;meta.main", description="Permanent observable identifier"),
        col("system_id", o["system_id"], ucd="meta.id", description="Permanent system identifier"),
        col("side", o["side"], ucd="meta.code", description="observed or baryonic"),
        col("quantity", o["quantity"], ucd="meta.code", description="Quantity (standard §4a)"),
        col("value", o["value"], None, "meta.number", "Value as the source gives it", "f8"),
        col("err_lo", o["err_lo"], None, "stat.error", "Lower error as the source gives it; empty if none", "f8"),
        col("err_hi", o["err_hi"], None, "stat.error", "Upper error as the source gives it; empty if none", "f8"),
        col("unit", o["unit"], ucd="meta.unit", description="Unit of value and errors"),
        col("band", o["band"], ucd="instr.bandpass", description="Photometric band for stellar quantities"),
        col("limit", o["limit"], ucd="meta.code", description="Limit"),
        col("r_kpc", o["r_kpc"], u.kpc, "phys.size.radius", "Radius of the value", "f8"),
        col("r_kind", o["r_kind"], ucd="meta.code", description="Radius type"),
        col("steps", o["steps"], ucd="meta.note", description="Processing steps the source performed (standard §4b)"),
        col("evidence_tier", o["evidence_tier"], ucd="meta.code.qual", description="1 released files", dtype="i8"),
        col("source_ref", o["source_ref"], ucd="meta.ref", description="Pointer to the source row and column"),
    ])
    obs_t.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    s = {k: [] for k in ["system_id", "name_in_source", "class_in_source", "taxonomy_kind", "kind_label",
                         "distance_mpc", "distance_err_mpc", "distance_method", "distance_kinematic",
                         "ra_deg", "dec_deg", "inclination_deg", "inclination_err_deg", "properties"]}
    for g in galaxies:
        kind = S0_KIND if g["T"] == 0 else LTG_KIND
        s["system_id"].append(system_ids[g["name"]])
        s["name_in_source"].append(g["name"])
        s["class_in_source"].append(f"{HUBBLE_TYPES[g['T']]} (Hubble type T={g['T']})")
        s["taxonomy_kind"].append(kind[0])
        s["kind_label"].append(kind[1])
        s["distance_mpc"].append(g["D"])
        s["distance_err_mpc"].append(g["e_D"])
        s["distance_method"].append(DISTANCE_METHODS[g["f_D"]])
        s["distance_kinematic"].append("false")
        s["ra_deg"].append(None)
        s["dec_deg"].append(None)
        s["inclination_deg"].append(g["inc"])
        s["inclination_err_deg"].append(g["e_inc"])
        s["properties"].append(json.dumps({
            "quality_flag_Q": g["Q"],
            "luminosity_3p6_1e9_solLum": g["L36"], "luminosity_3p6_err_1e9_solLum": g["e_L36"],
            "r_eff_kpc": g["Reff"], "sb_eff_solLum_per_pc2": g["SBeff"],
            "r_disk_kpc": g["Rdisk"], "sb_disk_solLum_per_pc2": g["SBdisk"],
            "m_hi_1e9_solMass": g["MHI"], "r_hi_kpc": g["RHI"],
            "v_flat_km_s": g["Vflat"], "v_flat_err_km_s": g["e_Vflat"],
            "rotation_curve_refs": g["ref"],
        }, separators=(",", ":")))
    systems = Table([
        col("system_id", s["system_id"], ucd="meta.id;meta.main", description="Permanent system identifier"),
        col("name_in_source", s["name_in_source"], ucd="meta.id", description="Galaxy name as given by SPARC"),
        col("class_in_source", s["class_in_source"], ucd="src.class", description="Hubble type as given by SPARC"),
        col("taxonomy_kind", s["taxonomy_kind"], ucd="src.class", description="Atlas kind (docs/plans/TAXONOMY.md) by the source's morphology: S0 is A6, all other SPARC types A4"),
        col("kind_label", s["kind_label"], ucd="src.class", description="Kind label"),
        col("distance_mpc", s["distance_mpc"], u.Mpc, "pos.distance", "Distance as given by SPARC", "f8"),
        col("distance_err_mpc", s["distance_err_mpc"], u.Mpc, "stat.error;pos.distance", "Distance error as given by SPARC", "f8"),
        col("distance_method", s["distance_method"], ucd="meta.code", description="Distance method as given by SPARC"),
        col("distance_kinematic", s["distance_kinematic"], ucd="meta.code", description="False: no distance is derived from the galaxy's own internal kinematics (Hubble-flow distances use the systemic recession velocity; standard §5)"),
        col("ra_deg", s["ra_deg"], u.deg, "pos.eq.ra", "Right ascension (not given by SPARC)", "f8"),
        col("dec_deg", s["dec_deg"], u.deg, "pos.eq.dec", "Declination (not given by SPARC)", "f8"),
        col("inclination_deg", s["inclination_deg"], u.deg, "src.orbital.inclination", "Disc inclination as given by SPARC", "f8"),
        col("inclination_err_deg", s["inclination_err_deg"], u.deg, "stat.error;src.orbital.inclination", "Inclination error as given by SPARC", "f8"),
        col("properties", s["properties"], ucd="meta.note", description="Other source-given properties (JSON; units in key names)"),
    ])
    systems.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    t = {k: [] for k in ["term_id", "scale", "applies_to", "moves", "status", "size_value", "size_lo", "size_hi",
                         "size_unit", "size_column", "size_kind", "assumption_id", "correlated_with", "covariance",
                         "citation", "locator", "note"]}

    def term(**kw):
        for k in t:
            t[k].append(kw.get(k))

    L17 = "Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836, 152 (arXiv:1610.08981)"
    L16 = "Lelli, McGaugh & Schombert 2016, AJ 152, 157 (arXiv:1606.09251)"
    term(term_id="inclination", scale="system", applies_to="*", moves="g_obs", status="given",
         size_column="inclination_err_deg", size_unit="deg", size_kind="one_sigma", assumption_id="inclination",
         covariance="not_published", citation=f"{L16}; {L17}", locator="SPARC Table 1 e_Inc; arXiv:1610.08981 eq. 2",
         note="One inclination per galaxy: moves every point of the galaxy together; g_obs scales as 1/sin^2 i.")
    term(term_id="distance", scale="system", applies_to="*", moves="g_obs", status="given",
         size_column="distance_err_mpc", size_unit="Mpc", size_kind="one_sigma", assumption_id="distance",
         covariance="not_published", citation=f"{L16}; {L17}", locator="SPARC Table 1 e_D; arXiv:1610.08981 eq. 2 and §2.1.2",
         note="One distance per galaxy: g_obs scales as 1/D; g_bar is distance independent (source, §2.1.2).")
    term(term_id="hi_flux_calibration", scale="system", applies_to="*", moves="g_bar", status="given",
         size_value=0.10, size_unit="fraction of the gas term", size_kind="as_released", covariance="not_published",
         citation=L17, locator="§2.1.2: \"a typical 10% error on the HI flux calibration\"",
         note="One calibration per galaxy's HI data: the gas term of every point of the galaxy moves together.")
    term(term_id="ml_scatter_galaxy", scale="system", applies_to="*", moves="g_bar", status="given",
         size_value=0.25, size_unit="fraction of the stellar term", size_kind="as_released", covariance="not_published",
         citation=L17, locator="§2.1.2: \"a 25% scatter on Υ⋆\"; §3.2: \"variations in Υ⋆ (0.11 dex)\"",
         note="System scale is the Atlas's assignment (D-084 addendum): the source does not say whether the 25% varies between or within galaxies; at 3.6 micron most variation is expected between galaxies, but variation within a galaxy is possible and is not separated.")
    term(term_id="ml_disk", scale="dataset", applies_to="*", moves="g_bar", status="given",
         size_lo=0.2, size_hi=0.7, size_unit="solMass / solLum", size_kind="range", assumption_id="ml_disk",
         covariance="not_published", citation=L16, locator="abstract: 0.2 (DiskMass survey) to 0.7 (maximum-disc limit)",
         note="The population value adopted for every galaxy (default 0.5).")
    term(term_id="ml_bulge", scale="dataset", applies_to="*", moves="g_bar", status="given",
         size_lo=0.28, size_hi=0.98, size_unit="solMass / solLum", size_kind="range", assumption_id="ml_bulge",
         covariance="not_published", citation=L16, locator="registry ml_bulge (Υ_bul = 1.4 Υ_disk over the Υ_disk range)",
         note="The population value adopted for every bulge (default 0.7).")
    term(term_id="geometry_3d_molecular", scale="system", applies_to="*", moves="g_bar", status="given",
         size_value=0.20, size_unit="fraction", size_kind="as_released", covariance="not_published",
         citation=f"{L17}; {L16}",
         locator="arXiv:1610.08981 §2.1.2: \"may add another ~20% uncertainty to points at small radii\"; arXiv:1606.09251 §3.4",
         note="Vertical disc structure, bulge flattening and molecular gas; stated only as about 20% at small radii, so no shift is computed. Also: the stellar profile is extrapolated by an exponential fit beyond the last measured radius (arXiv:1606.09251 §3.4).")
    term(term_id="g_bar_point", scale="point", applies_to="*", moves="g_bar", status="not_given_by_source",
         covariance="not_published", note="No point-scale uncertainty on g_bar is given; the source states that Spitzer photometric calibration uncertainties are negligible (arXiv:1610.08981 §2.1.2).")
    terms = Table([
        col("term_id", t["term_id"], ucd="meta.id", description="Term identifier"),
        col("scale", t["scale"], ucd="meta.code", description="point, system or dataset (standard 2.2.0 §2a)"),
        col("applies_to", t["applies_to"], ucd="meta.id", description="System, or * for all"),
        col("moves", t["moves"], ucd="meta.code", description="Axes the term moves"),
        col("status", t["status"], ucd="meta.code", description="given, given_by_other_source or not_given_by_source"),
        col("size_value", t["size_value"], None, "stat.error", "Size as the source states it", "f8"),
        col("size_lo", t["size_lo"], None, "stat.min", "Lower end of a published range", "f8"),
        col("size_hi", t["size_hi"], None, "stat.max", "Upper end of a published range", "f8"),
        col("size_unit", t["size_unit"], ucd="meta.unit", description="Unit of the size"),
        col("size_column", t["size_column"], ucd="meta.ref", description="Systems column holding a per-system size"),
        col("size_kind", t["size_kind"], ucd="meta.code", description="one_sigma, range or as_released"),
        col("assumption_id", t["assumption_id"], ucd="meta.id", description="Registry assumption whose formula moves the values"),
        col("correlated_with", t["correlated_with"], ucd="meta.note", description="Correlations as the source states them"),
        col("covariance", t["covariance"], ucd="meta.code", description="published, not_published or not_applicable"),
        col("citation", t["citation"], ucd="meta.bib", description="Where the size was read"),
        col("locator", t["locator"], ucd="meta.ref", description="Section, table or quote"),
        col("note", t["note"], ucd="meta.note", description="What the term is"),
    ])
    terms.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    return meas, obs_t, systems, terms


def main() -> int:
    meas, obs_t, systems, terms = build(HERE / "source")
    tables = HERE / "tables"
    tables.mkdir(exist_ok=True)
    for name, tab in (("measurements", meas), ("observables", obs_t), ("systems", systems), ("uncertainty_terms", terms)):
        tab.write(tables / f"{name}.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
    desc["x_known_issues"] = [f"https://github.com/extragravitation/atlas/issues/{ki['issue']}"
                              for ki in json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]]
    write_datapackage(HERE, desc, {"measurements": ("tables/measurements.ecsv", meas),
                                   "observables": ("tables/observables.ecsv", obs_t),
                                   "systems": ("tables/systems.ecsv", systems),
                                   "uncertainty_terms": ("tables/uncertainty_terms.ecsv", terms)})
    write_checksums(HERE)
    print(f"wrote {len(meas)} measurements, {len(obs_t)} observables, {len(systems)} systems, {len(terms)} uncertainty terms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
