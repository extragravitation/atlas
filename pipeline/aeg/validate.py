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
KNOWN_STANDARD_VERSIONS = {"1.0.0", "1.1.0", "1.2.0", "1.2.1", "1.3.0"}

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


def check_columns(table, core: set[str], short: str, where: str) -> list[str]:
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
        if name in UNITS:
            if col.unit is None or u.Unit(col.unit) != u.Unit(UNITS[name]):
                problems.append(f"{where}: column {name} unit {col.unit}, expected {UNITS[name]}")
    return problems


def validate(pkg: Path) -> list[str]:
    from astropy.table import Table
    dataset, version = pkg.parent.name, pkg.name
    short = dataset.removeprefix("aeg-d-").replace("-", "_")
    problems: list[str] = []

    meas = Table.read(pkg / "tables/measurements.ecsv", format="ascii.ecsv")
    where = f"{dataset}/{version} measurements"
    if meas.meta.get("standard_version") not in KNOWN_STANDARD_VERSIONS:
        problems.append(f"{where}: unknown standard_version {meas.meta.get('standard_version')!r}")
    for c in REQUIRED_MEAS:
        if c not in meas.colnames:
            problems.append(f"{where}: missing required column {c}")
    problems += check_columns(meas, CORE_MEAS, short, where)

    ids = [str(x) for x in _vals(meas["measurement_id"])]
    for i, mid in enumerate(ids, start=1):
        if mid != f"{dataset}/{version}/m{i:06d}":
            problems.append(f"{where}: row {i} has measurement_id {mid}, expected {dataset}/{version}/m{i:06d}")
            break
    for name, allowed in CLOSED.items():
        if name in meas.colnames:
            bad = {v for v in _vals(meas[name]) if v not in (None, "") and v not in allowed}
            if bad:
                problems.append(f"{where}: {name} has values outside the closed list: {sorted(bad)}")
    if "flags" in meas.colnames:
        bad = {f for v in _vals(meas["flags"]) if v for f in str(v).split(";") if f and f not in FLAGS}
        if bad:
            problems.append(f"{where}: unknown flags {sorted(bad)}")
    for c in ["g_obs_err_lo", "g_obs_err_hi", "g_bar_err_lo", "g_bar_err_hi"]:
        if c in meas.colnames and any(v is not None and v < 0 for v in _vals(meas[c])):
            problems.append(f"{where}: negative values in {c}")
    for c in ["g_obs", "g_bar"]:
        out = [v for v in _vals(meas[c]) if v is not None and not (1e-16 <= abs(v) <= 1e-6)]
        if out:
            problems.append(f"{where}: {len(out)} values of {c} outside 1e-16..1e-6 m/s2 in magnitude")
    if any(v is not None and v <= 0 for v in _vals(meas["g_obs"])):
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
        problems += check_columns(systems, CORE_SYS, short, f"{dataset}/{version} systems")

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
