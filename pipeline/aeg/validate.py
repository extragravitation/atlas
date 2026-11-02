"""Validate a data package against the data standard (docs/data-standard.md §7).

Usage: python -m aeg.validate data/packages/<dataset>/<version>

Covers items 4–8, 11 and 12 of §7. Items 1–3 (source hashes, frozen
reproduction file, reproduction tests) are covered by aeg.fetch and the
package's own tests; item 9 by aeg.formula_check; item 10 by aeg.check.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KNOWN_STANDARD_VERSIONS = {"1.0.0", "1.1.0", "1.2.0", "1.2.1", "1.3.0", "2.0.0", "2.1.0", "2.2.0"}

FLAGS = {"no_uncertainty", "beyond_source_range", "inner_resolution_limited", "source_quality_low", "reproduction_mismatch"}
CLOSED = {
    "kind": {"profile_point", "system_value", "population_bin"},
    "channel": {"dynamics", "lensing"},
    "method_class": {"kinematic", "hydrostatic", "lensing"},
    "r_kind": {"3d", "projected"},
    "stars_status": {"measured", "modelled", "absent", "not_separable"},
    "gas_cold_status": {"measured", "modelled", "absent", "not_separable"},
    "gas_hot_status": {"measured", "modelled", "absent", "not_separable"},
}
REQUIRED_MEAS = ["measurement_id", "system_id", "kind", "channel", "method_class", "method", "g_obs", "g_bar",
                 "stars_status", "gas_cold_status", "gas_hot_status", "assumptions", "adjustable", "source_ref"]
CORE_MEAS = set(REQUIRED_MEAS) | {"r_kpc", "r_kind", "g_obs_err_lo", "g_obs_err_hi", "g_bar_err_lo", "g_bar_err_hi",
                                  "g_bar_stars", "g_bar_stars_disk", "g_bar_stars_bulge", "g_bar_gas_cold", "g_bar_gas_hot",
                                  "quality_source", "flags", "known_issues"}
CORE_SYS = {"system_id", "name_in_source", "class_in_source", "distance_mpc", "distance_err_mpc", "distance_method",
            "ra_deg", "dec_deg", "inclination_deg", "inclination_err_deg", "properties"}
UNITS = {
    "r_kpc": "kpc", "distance_mpc": "Mpc", "distance_err_mpc": "Mpc", "ra_deg": "deg", "dec_deg": "deg",
    "inclination_deg": "deg", "inclination_err_deg": "deg",
    **{c: "m / s2" for c in ["g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_bar", "g_bar_err_lo", "g_bar_err_hi",
                              "g_bar_stars", "g_bar_stars_disk", "g_bar_stars_bulge", "g_bar_gas_cold", "g_bar_gas_hot"]},
}


def _vals(col):
    import numpy as np
    out = []
    for v in col:
        if np.ma.is_masked(v):
            out.append(None)
        else:
            out.append(v.item() if hasattr(v, "item") else v)
    return out


def check_columns(table, core: set[str], short: str, where: str, units: dict | None = None) -> list[str]:
    import astropy.units as u
    from astropy.io.votable import ucd as ucdlib
    problems = []
    for name in table.colnames:
        col = table[name]
        if name not in core and not name.startswith(f"x_{short}_"):
            problems.append(f"{where}: column {name!r} is neither core nor a valid extension (x_{short}_...)")
        if not (col.description or "").strip():
            problems.append(f"{where}: column {name} has no description")
        ucd = col.meta.get("ucd") if col.meta else None
        if not ucd:
            problems.append(f"{where}: column {name} has no UCD")
        else:
            try:
                ucdlib.parse_ucd(ucd, check_controlled_vocabulary=True, has_colon=False)
            except ValueError as e:
                problems.append(f"{where}: column {name} UCD {ucd!r} invalid: {e}")
        units_map = UNITS if units is None else units
        if name in units_map:
            if col.unit is None or u.Unit(col.unit) != u.Unit(units_map[name]):
                problems.append(f"{where}: column {name} unit {col.unit}, expected {units_map[name]}")
    return problems


# ------------------------------------------------------------------ 2.0.0
FLAGS_V2 = FLAGS | {"edges_inferred", "value_in_text", "assumed_concentration", "derived_from_delta_g",
                    "metallicity_cut_membership", "fitted_profile", "star_count_weighting"}
CLOSED_V2 = {
    **CLOSED,
    "method_class": {"kinematic", "hydrostatic", "lensing", "ephemeris"},
    "measured_quantity": {"g_obs", "delta_g"},
    "limit": {"none", "upper", "lower"},
    "model_dependence": {"none", "observable_form", "total_mass_form"},
    "role": {"default", "alternative"},
    "not_plotted_reason": {"coverage_below_threshold", "aperture_uncorrected", "central_only",
                           "members_within_half_light", "proper_motion_only", "tier_3", "alternative_value",
                           "limit_only", "epoch_gap", "kinematic_distance", "other"},
}
REQUIRED_MEAS_V2 = [c for c in REQUIRED_MEAS if c != "g_obs"] + [
    "measured_quantity", "limit", "observed_from", "baryonic_from", "model_dependence", "evidence_tier", "role", "plotted"]
CORE_MEAS_V2 = CORE_MEAS | set(REQUIRED_MEAS_V2) | {"delta_g", "delta_g_err_lo", "delta_g_err_hi", "err_level",
                                                    "alternative_of", "not_plotted_reason", "notes"}
# 2.2.0 (D-083): point-scale error columns (§3) and the uncertainty-terms table (§7a).
POINT_ERR_COLS = ["g_obs_err_point_lo", "g_obs_err_point_hi", "g_bar_err_point_lo", "g_bar_err_point_hi"]
CORE_MEAS_V2 = CORE_MEAS_V2 | set(POINT_ERR_COLS)
TERMS_REQUIRED = ["term_id", "scale", "applies_to", "moves", "status"]
TERMS_CORE = set(TERMS_REQUIRED) | {"size_value", "size_lo", "size_hi", "size_unit", "size_column", "size_kind",
                                    "assumption_id", "correlated_with", "covariance", "citation", "locator", "note"}
TERMS_CLOSED = {
    "scale": {"point", "system", "dataset"},
    "moves": {"g_obs", "g_bar", "both"},
    "status": {"given", "given_by_other_source", "not_given_by_source"},
    "size_kind": {"one_sigma", "range", "as_released"},
    "covariance": {"published", "not_published", "not_applicable"},
}
QUANTITIES = {
    "observed": {"v_rot", "sigma_los", "sigma_los_second_moment", "sigma_los_about_rotation", "sigma_pm",
                 "velocity_gradient", "temperature_x", "density_e", "pressure_e", "mass_hse", "delta_sigma", "kappa",
                 "einstein_radius", "binary_sep_proj", "binary_dv_proj", "delta_g_bound", "extra_mass_bound",
                 "perihelion_precession_extra", "distance", "redshift"},
    "baryonic": {"luminosity", "apparent_magnitude", "absolute_magnitude", "surface_brightness", "structural_param",
                 "half_light_radius", "metallicity_feh", "age", "stellar_ml_population", "star_formation_history_ml",
                 "mass_star", "mass_star_counted", "surface_density_hi", "mass_hi", "mass_gas", "mass_gas_limit",
                 "line_flux_co", "known_mass", "distance", "redshift"},
}
LADDER_STEPS = {
    "spectra", "stellar_velocities", "membership", "binary_treatment", "dispersion_global", "dispersion_profile",
    "light_weighting", "half_light_estimator", "integrated_spectra", "aperture_dispersion",
    "aperture_correction_global", "aperture_correction_central", "astrometry", "proper_motions", "dispersion_pm",
    "line_velocities", "velocity_field", "tilted_ring", "inclination", "pressure_correction", "rotation_curve",
    "centripetal", "events", "projected_t_and_density", "deprojected_profiles", "fitted_forms", "hydrostatic_mass",
    "newtonian_g", "shapes", "shear", "excess_surface_density", "deprojection", "image_positions", "lens_model",
    "einstein_radius", "projected_mass", "observations", "ephemeris_fit", "extra_term_fit", "bound", "photometry",
    "luminosity", "structural_model", "stellar_ml", "star_counts", "mass_function", "mass_star_counted",
    "hi_21cm", "co_line", "xray", "surface_density", "mass", "helium_factor",
}
CORE_OBS = {"observable_id", "system_id", "side", "quantity", "value", "err_lo", "err_hi", "unit", "band", "limit",
            "err_level", "r_kpc", "r_kind", "r_in_kpc", "r_out_kpc", "steps", "evidence_tier", "in_text", "source_ref"}
REQUIRED_OBS = ["observable_id", "side", "quantity", "value", "unit", "limit", "steps", "evidence_tier", "source_ref"]
CORE_SYS_V2 = CORE_SYS | {"taxonomy_kind", "kind_label", "host", "distance_kinematic", "distance_ref", "redshift",
                          "redshift_err", "metallicity_feh"}
TAXONOMY_KINDS = {f"A{i}" for i in range(11)}
INVENTORY_STATUS = {"measured", "modelled", "known_unmeasured", "stated_negligible", "absent_limit",
                    "absent_literature_limit", "not_addressed"}
# Quantities added by minor versions of 2.x (docs/data-standard.md §4a), accepted only in packages
# that state that version or a later one.
QUANTITIES_ADDED = {
    "2.1.0": {"observed": {"einstein_mass"}},  # D-076 item 4
}


def quantities_for(standard_version: str) -> dict[str, set[str]]:
    """The closed §4a lists as they stand in the given 2.x version."""
    def key(v):
        return tuple(int(x) for x in v.split("."))
    out = {side: set(q) for side, q in QUANTITIES.items()}
    for v, added in QUANTITIES_ADDED.items():
        if key(str(standard_version)) >= key(v):
            for side, q in added.items():
                out[side] |= q
    return out


UNITS_V2 = {**UNITS, "delta_g": "m / s2", "delta_g_err_lo": "m / s2", "delta_g_err_hi": "m / s2",
            "r_in_kpc": "kpc", "r_out_kpc": "kpc", **{c: "m / s2" for c in POINT_ERR_COLS}}


def _key(v: str) -> tuple:
    try:
        return tuple(int(x) for x in str(v).split("."))
    except ValueError:
        return (0,)


def validate_v22(pkg: Path, meas) -> list[str]:
    """Rules added in standard 2.2.0 (docs/data-standard.md §10 items 11 and 12)."""
    from astropy.table import Table
    dataset, version = pkg.parent.name, pkg.name
    where = f"{dataset}/{version}"
    problems: list[str] = []
    path = pkg / "tables/uncertainty_terms.ecsv"
    if not path.is_file():
        return [f"{where}: tables/uncertainty_terms.ecsv missing (required from 2.2.0)"]
    terms = Table.read(path, format="ascii.ecsv")
    for c in TERMS_REQUIRED:
        if c not in terms.colnames:
            problems.append(f"{where} uncertainty_terms: missing required column {c}")
    if problems:
        return problems
    extra = [c for c in terms.colnames if c not in TERMS_CORE]
    if extra:
        problems.append(f"{where} uncertainty_terms: unknown columns {extra}")
    rows = [dict(zip(terms.colnames, r)) for r in zip(*[_vals(terms[c]) for c in terms.colnames])]
    ids = [r["term_id"] for r in rows]
    if len(ids) != len(set(ids)):
        problems.append(f"{where} uncertainty_terms: term_id not unique")
    for name, allowed in TERMS_CLOSED.items():
        if name in terms.colnames:
            bad = {v for v in _vals(terms[name]) if v not in (None, "") and v not in allowed}
            if bad:
                problems.append(f"{where} uncertainty_terms: {name} has values outside the closed list: {sorted(bad)}")
    systems_ids, sys_cols = set(), set()
    if (pkg / "tables/systems.ecsv").is_file():
        st = Table.read(pkg / "tables/systems.ecsv", format="ascii.ecsv")
        systems_ids, sys_cols = {str(v) for v in _vals(st["system_id"])}, set(st.colnames)
    registry = {a["id"] for a in json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))["assumptions"]}
    for r in rows:
        tid = r["term_id"]
        if r["applies_to"] != "*" and r["applies_to"] not in systems_ids:
            problems.append(f"{where} uncertainty_terms {tid}: applies_to {r['applies_to']!r} is not '*' or a system in the package")
        if r["status"] in ("given", "given_by_other_source"):
            has_size = r.get("size_value") is not None or (r.get("size_lo") is not None and r.get("size_hi") is not None)
            col = r.get("size_column")
            if col:
                has_size = has_size or col in sys_cols
                if col not in sys_cols:
                    problems.append(f"{where} uncertainty_terms {tid}: size_column {col!r} is not a systems column")
            if not has_size:
                problems.append(f"{where} uncertainty_terms {tid}: given term without a size")
        if r.get("assumption_id") and r["assumption_id"] not in registry:
            problems.append(f"{where} uncertainty_terms {tid}: assumption_id {r['assumption_id']!r} not in the registry")
    for side in ("g_obs", "g_bar"):
        for e in ("lo", "hi"):
            pc, tc = f"{side}_err_point_{e}", f"{side}_err_{e}"
            if pc in meas.colnames:
                vals = _vals(meas[pc])
                if any(v is not None and v < 0 for v in vals):
                    problems.append(f"{where} measurements: negative values in {pc}")
                if tc in meas.colnames:
                    over = sum(1 for p, t in zip(vals, _vals(meas[tc])) if p is not None and t is not None and p > t * (1 + 1e-12))
                    if over:
                        problems.append(f"{where} measurements: {over} rows where {pc} exceeds {tc}")
    return problems


def _truthy(v) -> bool:
    return str(v).strip().lower() in {"true", "1", "yes"}


def validate_v2(pkg: Path, meas) -> list[str]:
    """Rules added in standard 2.0.0 (docs/data-standard.md §10)."""
    from astropy.table import Table
    dataset, version = pkg.parent.name, pkg.name
    short = dataset.removeprefix("aeg-d-").replace("-", "_")
    where = f"{dataset}/{version}"
    problems: list[str] = []
    quantities = quantities_for(meas.meta.get("standard_version", "2.0.0"))

    for c in REQUIRED_MEAS_V2:
        if c not in meas.colnames:
            problems.append(f"{where} measurements: missing required column {c}")
    if problems:
        return problems
    rows = [dict(zip(meas.colnames, r)) for r in zip(*[_vals(meas[c]) for c in meas.colnames])]
    for name, allowed in CLOSED_V2.items():
        if name in meas.colnames:
            bad = {v for v in _vals(meas[name]) if v not in (None, "") and v not in allowed}
            if bad:
                problems.append(f"{where} measurements: {name} has values outside the closed list: {sorted(bad)}")

    obs_path = pkg / "tables/observables.ecsv"
    obs_ids: dict[str, str] = {}
    if not obs_path.is_file():
        problems.append(f"{where}: tables/observables.ecsv missing")
    else:
        obs = Table.read(obs_path, format="ascii.ecsv")
        ow = f"{where} observables"
        for c in REQUIRED_OBS:
            if c not in obs.colnames:
                problems.append(f"{ow}: missing required column {c}")
        problems += check_columns(obs, CORE_OBS, short, ow, UNITS_V2)
        if not any(p.startswith(f"{ow}: missing") for p in problems):
            orows = [dict(zip(obs.colnames, r)) for r in zip(*[_vals(obs[c]) for c in obs.colnames])]
            for i, r in enumerate(orows, start=1):
                oid = str(r["observable_id"])
                if oid != f"{dataset}/{version}/o{i:06d}":
                    problems.append(f"{ow}: row {i} has observable_id {oid}, expected {dataset}/{version}/o{i:06d}")
                    break
            for r in orows:
                oid, side = str(r["observable_id"]), r["side"]
                obs_ids[oid] = side
                if side not in quantities:
                    problems.append(f"{ow}: {oid} side {side!r} not in the closed list")
                elif r["quantity"] not in quantities[side]:
                    problems.append(f"{ow}: {oid} quantity {r['quantity']!r} not allowed on the {side} side")
                bad_steps = [s for s in str(r["steps"] or "").split(";") if s and s not in LADDER_STEPS]
                if bad_steps or not r["steps"]:
                    problems.append(f"{ow}: {oid} steps not from the ladders: {bad_steps or 'empty'}")
                if r["limit"] not in ("none", "upper", "lower"):
                    problems.append(f"{ow}: {oid} limit {r['limit']!r} not in the closed list")
                if r["evidence_tier"] not in (1, 2, 3):
                    problems.append(f"{ow}: {oid} evidence_tier must be 1, 2 or 3")

    for r in rows:
        mid = r["measurement_id"]
        for col, side in (("observed_from", "observed"), ("baryonic_from", "baryonic")):
            ids = [x for x in str(r[col] or "").split(";") if x]
            if not ids:
                problems.append(f"{where}: {mid} {col} is empty")
            for x in ids:
                if x not in obs_ids:
                    problems.append(f"{where}: {mid} {col} refers to unknown observable {x}")
                elif obs_ids[x] != side:
                    problems.append(f"{where}: {mid} {col} refers to a {obs_ids[x]}-side observable {x}")
        plotted = _truthy(r["plotted"])
        reason = r.get("not_plotted_reason")
        if plotted and reason:
            problems.append(f"{where}: {mid} is plotted but has a not_plotted_reason")
        if not plotted and not reason:
            problems.append(f"{where}: {mid} is not plotted and has no not_plotted_reason")
        if r["evidence_tier"] not in (1, 2, 3):
            problems.append(f"{where}: {mid} evidence_tier must be 1, 2 or 3")
        elif r["evidence_tier"] == 3 and plotted:
            problems.append(f"{where}: {mid} is tier 3 and must not be plotted (D-035)")
        if r["role"] == "alternative" and "alternative_of" not in r:
            problems.append(f"{where}: {mid} is an alternative without alternative_of")
        mq = r["measured_quantity"]
        if mq == "g_obs" and r.get("g_obs") is None:
            problems.append(f"{where}: {mid} measures g_obs but g_obs is empty")
        if mq == "delta_g" and r.get("delta_g") is None:
            problems.append(f"{where}: {mid} measures delta_g but delta_g is empty")
        if r["limit"] != "none":
            errs = [r.get(f"{mq}_err_lo"), r.get(f"{mq}_err_hi")]
            if any(e is not None for e in errs):
                problems.append(f"{where}: {mid} is a limit but has error values")

    sys_path = pkg / "tables/systems.ecsv"
    if sys_path.is_file():
        systems = Table.read(sys_path, format="ascii.ecsv")
        sw = f"{where} systems"
        for c in ("taxonomy_kind", "kind_label", "distance_kinematic"):
            if c not in systems.colnames:
                problems.append(f"{sw}: missing required column {c}")
        if not any(p.startswith(f"{sw}: missing") for p in problems):
            plotted_systems = {r["system_id"] for r in rows if _truthy(r["plotted"])}
            srows = [dict(zip(systems.colnames, r)) for r in zip(*[_vals(systems[c]) for c in systems.colnames])]
            for r in srows:
                sid = r["system_id"]
                if r["taxonomy_kind"] not in TAXONOMY_KINDS:
                    problems.append(f"{sw}: {sid} taxonomy_kind {r['taxonomy_kind']!r} not A0–A10")
                if not r["kind_label"]:
                    problems.append(f"{sw}: {sid} has no kind_label")
                elif str(r["kind_label"]).startswith("ambiguous") and r["taxonomy_kind"] != "A7":
                    problems.append(f"{sw}: {sid} is labelled ambiguous but not in A7")
                if r.get("distance_mpc") is None and r.get("redshift") is None:
                    problems.append(f"{sw}: {sid} has neither distance_mpc nor redshift")
                if _truthy(r["distance_kinematic"]) and sid in plotted_systems:
                    problems.append(f"{sw}: {sid} has a kinematic distance but plotted rows (D-036 #6)")

    desc_path = pkg / "datapackage.json"
    if desc_path.is_file():
        desc = json.loads(desc_path.read_text(encoding="utf-8"))
        for k in ("x_selection", "x_baryon_inventory", "x_search_log", "x_second_reading"):
            if not desc.get(k):
                problems.append(f"{where} datapackage.json: {k} missing or empty")
        for comp in desc.get("x_baryon_inventory") or []:
            if comp.get("status") not in INVENTORY_STATUS:
                problems.append(f"{where} datapackage.json: baryon component {comp.get('component')!r} "
                                f"status {comp.get('status')!r} not in the closed list")
    else:
        problems.append(f"{where}: datapackage.json missing")
    if not (pkg / "SECOND_READING.md").is_file():
        problems.append(f"{where}: SECOND_READING.md missing")
    return problems


def validate(pkg: Path) -> list[str]:
    from astropy.table import Table
    dataset, version = pkg.parent.name, pkg.name
    short = dataset.removeprefix("aeg-d-").replace("-", "_")
    problems: list[str] = []

    meas = Table.read(pkg / "tables/measurements.ecsv", format="ascii.ecsv")
    where = f"{dataset}/{version} measurements"
    sv = meas.meta.get("standard_version")
    if sv not in KNOWN_STANDARD_VERSIONS:
        problems.append(f"{where}: unknown standard_version {sv!r}")
    v2 = str(sv).startswith("2.")
    for c in (REQUIRED_MEAS_V2 if v2 else REQUIRED_MEAS):
        if c not in meas.colnames:
            problems.append(f"{where}: missing required column {c}")
    problems += check_columns(meas, CORE_MEAS_V2 if v2 else CORE_MEAS, short, where, UNITS_V2 if v2 else None)

    ids = [str(x) for x in _vals(meas["measurement_id"])]
    for i, mid in enumerate(ids, start=1):
        if mid != f"{dataset}/{version}/m{i:06d}":
            problems.append(f"{where}: row {i} has measurement_id {mid}, expected {dataset}/{version}/m{i:06d}")
            break
    for name, allowed in (CLOSED_V2 if v2 else CLOSED).items():
        if name in meas.colnames:
            bad = {v for v in _vals(meas[name]) if v not in (None, "") and v not in allowed}
            if bad:
                problems.append(f"{where}: {name} has values outside the closed list: {sorted(bad)}")
    if "flags" in meas.colnames:
        bad = {f for v in _vals(meas["flags"]) if v for f in str(v).split(";") if f and f not in (FLAGS_V2 if v2 else FLAGS)}
        if bad:
            problems.append(f"{where}: unknown flags {sorted(bad)}")
    for c in ["g_obs_err_lo", "g_obs_err_hi", "g_bar_err_lo", "g_bar_err_hi"]:
        if c in meas.colnames and any(v is not None and v < 0 for v in _vals(meas[c])):
            problems.append(f"{where}: negative values in {c}")
    for c in ["g_obs", "g_bar"]:
        if c not in meas.colnames:
            continue
        out = [v for v in _vals(meas[c]) if v is not None and not (1e-16 <= abs(v) <= 1e-6)]
        if out:
            problems.append(f"{where}: {len(out)} values of {c} outside 1e-16..1e-6 m/s2 in magnitude")
    if "g_obs" in meas.colnames and any(v is not None and v <= 0 for v in _vals(meas["g_obs"])):
        problems.append(f"{where}: g_obs must be positive")

    registry = {r["system_id"] for r in csv.DictReader((ROOT / "data/registry/systems.csv").open(encoding="utf-8"))}
    missing = {s for s in _vals(meas["system_id"]) if s and s not in registry}
    if missing:
        problems.append(f"{where}: {len(missing)} system_id values not in the registry")

    assumptions = {a["id"]: a for a in json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))["assumptions"]}
    used = {t.split("=")[0] for v in _vals(meas["assumptions"]) if v for t in str(v).split(";") if t}
    adjustable = {t for v in _vals(meas["adjustable"]) if v for t in str(v).split(";") if t}
    for a in sorted(used | adjustable):
        if a not in assumptions or f"{dataset}/{version}" not in assumptions[a]["datasets"]:
            problems.append(f"{where}: assumption {a} not in the registry for {dataset}/{version}")
    for a in sorted(adjustable):
        if a in assumptions and not (assumptions[a]["adjustable"] and assumptions[a]["status"] == "confirmed"):
            problems.append(f"{where}: {a} is listed as adjustable but is not a confirmed adjustable assumption")

    sys_path = pkg / "tables/systems.ecsv"
    if sys_path.is_file():
        systems = Table.read(sys_path, format="ascii.ecsv")
        problems += check_columns(systems, CORE_SYS_V2 if v2 else CORE_SYS, short, f"{dataset}/{version} systems")
    if v2:
        problems += validate_v2(pkg, meas)
    if _key(sv) >= (2, 2, 0):
        problems += validate_v22(pkg, meas)

    # checksums.sha256 covers every committed file in the package
    sums = pkg / "checksums.sha256"
    if not sums.is_file():
        problems.append(f"{dataset}/{version}: checksums.sha256 missing")
    else:
        listed = {}
        for line in sums.read_text(encoding="utf-8").splitlines():
            digest, name = line.split(None, 1)
            listed[name.strip()] = digest
        for name, digest in listed.items():
            f = pkg / name
            if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != digest:
                problems.append(f"{dataset}/{version}: checksum mismatch for {name}")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    problems = validate(Path(argv[1]).resolve())
    if problems:
        print("Standard validation FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("Standard validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
