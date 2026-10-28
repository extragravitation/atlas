"""Convert SPARC mass models into the Atlas data standard (v1.1.0).

Usage: python data/packages/aeg-d-sparc/v1/convert.py

Reads source/ (fetched and hash-verified by `python -m aeg.fetch`), writes
tables/measurements.ecsv and tables/systems.ecsv. Every number comes from
the two SPARC tables; the method is in SOURCE.md.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.table import MaskedColumn, Table

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
DATASET, VERSION, STANDARD = "aeg-d-sparc", "v1", "1.2.0"
ASSIGNED_ON = "2026-10-28"

# Catalogue defaults, read at source: arXiv:1606.09251 (eq. 2, eq. 7) and arXiv:1610.08981 (Table 1).
ML_DISK, ML_BULGE = 0.5, 0.7
HELIUM_FACTOR = 1.33  # already included in Vgas by the source (Table 2, note 2)

KMS2_PER_KPC_TO_MS2 = (1 * u.km / u.s) ** 2 / (1 * u.kpc)
CONV = KMS2_PER_KPC_TO_MS2.to(u.m / u.s**2).value  # (km/s)^2 / kpc -> m/s^2

HUBBLE_TYPES = {0: "S0", 1: "Sa", 2: "Sab", 3: "Sb", 4: "Sbc", 5: "Sc", 6: "Scd",
                7: "Sd", 8: "Sdm", 9: "Sm", 10: "Im", 11: "BCD"}
DISTANCE_METHODS = {
    1: "Hubble flow (H0 = 73 km/s/Mpc, Virgo-centric infall corrected)",
    2: "Tip of the red giant branch",
    3: "Cepheids",
    4: "Ursa Major cluster",
    5: "Supernova light curve",
}


def tokens(path: Path, n: int, numeric_from: tuple[int, int]) -> list[list[str]]:
    """Whitespace-separated data rows with exactly n fields.

    The SPARC files' byte-by-byte headers do not match the data layout of the
    galaxy table as served (see docs/sources/sparc.md), so rows are parsed by
    column order instead. A row is data if it has n fields and fields
    numeric_from.. (as listed) parse as numbers; any other line must be header
    or notes. Field counts are checked so a malformed row cannot slip through.
    """
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
    else:
        c = MaskedColumn([("" if x is None else x) for x in data], name=name, description=description, dtype=str)
    c.meta["ucd"] = ucd
    return c


def build(source_dir: Path) -> tuple[Table, Table, list[dict]]:
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

    system_ids = {g["name"]: f"aeg-s-{i:06d}" for i, g in enumerate(galaxies, start=1)}
    issues = json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    has_bulge = {r["name"] for r in rows if r["Vbul"] != 0.0}

    m = {k: [] for k in [
        "measurement_id", "system_id", "kind", "channel", "method_class", "method", "r_kpc", "r_kind",
        "g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_bar", "g_bar_err_lo", "g_bar_err_hi",
        "g_bar_stars", "g_bar_stars_disk", "g_bar_stars_bulge", "g_bar_gas_cold", "g_bar_gas_hot",
        "stars_status", "gas_cold_status", "gas_hot_status", "assumptions", "adjustable",
        "quality_source", "source_ref", "flags", "known_issues",
        "x_sparc_v_obs", "x_sparc_e_v_obs", "x_sparc_v_gas", "x_sparc_v_disk", "x_sparc_v_bul"]}

    for i, r in enumerate(rows, start=1):
        g = by_name[r["name"]]
        if abs(r["D"] - g["D"]) > 0.0051:
            raise SystemExit(f"{r['name']}: distance differs between tables ({r['D']} vs {g['D']})")
        R = r["R"]
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
        bulge = r["name"] in has_bulge
        assumptions = [f"ml_disk={ML_DISK}"] + ([f"ml_bulge={ML_BULGE}"] if bulge else []) + [
            "distance=source", "inclination=source", f"helium_factor={HELIUM_FACTOR}"]
        adjustable = ["ml_disk"] + (["ml_bulge"] if bulge else []) + ["distance", "inclination"]

        m["measurement_id"].append(f"{DATASET}/{VERSION}/m{i:06d}")
        m["system_id"].append(system_ids[r["name"]])
        m["kind"].append("profile_point")
        m["channel"].append("dynamics")
        m["method_class"].append("kinematic")
        m["method"].append("HI/Halpha rotation curve")
        m["r_kpc"].append(R)
        m["r_kind"].append("3d")
        m["g_obs"].append(g_obs)
        m["g_obs_err_lo"].append(g_obs * rel)
        m["g_obs_err_hi"].append(g_obs * rel)
        m["g_bar"].append(g_bar)
        m["g_bar_err_lo"].append(g_bar_err)
        m["g_bar_err_hi"].append(g_bar_err)
        m["g_bar_stars"].append(stars)
        m["g_bar_stars_disk"].append(disk)
        m["g_bar_stars_bulge"].append(bul if bulge else None)
        m["g_bar_gas_cold"].append(gas)
        m["g_bar_gas_hot"].append(None)
        m["stars_status"].append("measured")
        m["gas_cold_status"].append("measured")
        m["gas_hot_status"].append("absent")
        m["assumptions"].append(";".join(assumptions))
        m["adjustable"].append(";".join(adjustable))
        m["quality_source"].append(f"Q={g['Q']}")
        m["source_ref"].append(f"MassModels_Lelli2016c.mrt:data row {i}")
        mid = f"{DATASET}/{VERSION}/m{i:06d}"
        flags = (["source_quality_low"] if g["Q"] == 3 else []) + sorted({ki["flag"] for ki in issues if mid in ki["measurements"]})
        m["flags"].append(";".join(flags))
        m["known_issues"].append(";".join(f"#{ki['issue']}" for ki in issues if mid in ki["measurements"]))
        m["x_sparc_v_obs"].append(r["Vobs"])
        m["x_sparc_e_v_obs"].append(r["e_Vobs"])
        m["x_sparc_v_gas"].append(r["Vgas"])
        m["x_sparc_v_disk"].append(r["Vdisk"])
        m["x_sparc_v_bul"].append(r["Vbul"])

    acc = u.m / u.s**2
    kms = u.km / u.s
    meas = Table([
        col("measurement_id", m["measurement_id"], ucd="meta.id;meta.main", description="Permanent measurement identifier"),
        col("system_id", m["system_id"], ucd="meta.id", description="Permanent system identifier"),
        col("kind", m["kind"], ucd="meta.code", description="Kind of measurement"),
        col("channel", m["channel"], ucd="meta.code", description="Observational channel"),
        col("method_class", m["method_class"], ucd="meta.code.class", description="Class of method"),
        col("method", m["method"], ucd="meta.note", description="Method as given by the source"),
        col("r_kpc", m["r_kpc"], u.kpc, "phys.size.radius", "Galactocentric radius in the disc plane", "f8"),
        col("r_kind", m["r_kind"], ucd="meta.code", description="Radius type"),
        col("g_obs", m["g_obs"], acc, "phys.acceleration", "Observed acceleration, V_obs^2/R", "f8"),
        col("g_obs_err_lo", m["g_obs_err_lo"], acc, "stat.error;phys.acceleration", "Lower one-sigma bound (velocity, inclination and distance errors)", "f8"),
        col("g_obs_err_hi", m["g_obs_err_hi"], acc, "stat.error;phys.acceleration", "Upper one-sigma bound (velocity, inclination and distance errors)", "f8"),
        col("g_bar", m["g_bar"], acc, "phys.acceleration;meta.modelled", "Newtonian acceleration from detected baryons at catalogue defaults", "f8"),
        col("g_bar_err_lo", m["g_bar_err_lo"], acc, "stat.error;phys.acceleration", "Lower one-sigma bound (10% gas, 25% stellar, per source)", "f8"),
        col("g_bar_err_hi", m["g_bar_err_hi"], acc, "stat.error;phys.acceleration", "Upper one-sigma bound (10% gas, 25% stellar, per source)", "f8"),
        col("g_bar_stars", m["g_bar_stars"], acc, "phys.acceleration;meta.modelled", "Stellar component of g_bar", "f8"),
        col("g_bar_stars_disk", m["g_bar_stars_disk"], acc, "phys.acceleration;meta.modelled", "Stellar disc component of g_bar", "f8"),
        col("g_bar_stars_bulge", m["g_bar_stars_bulge"], acc, "phys.acceleration;meta.modelled", "Bulge component of g_bar; empty where the source has no bulge", "f8"),
        col("g_bar_gas_cold", m["g_bar_gas_cold"], acc, "phys.acceleration;meta.modelled", "Cold gas (atomic hydrogen with helium) component of g_bar; sign kept", "f8"),
        col("g_bar_gas_hot", m["g_bar_gas_hot"], acc, "phys.acceleration;meta.modelled", "Hot gas component of g_bar; not given by the source", "f8"),
        col("stars_status", m["stars_status"], ucd="meta.code", description="Status of the stellar component"),
        col("gas_cold_status", m["gas_cold_status"], ucd="meta.code", description="Status of the cold gas component"),
        col("gas_hot_status", m["gas_hot_status"], ucd="meta.code", description="Status of the hot gas component"),
        col("assumptions", m["assumptions"], ucd="meta.note", description="Named assumptions affecting this row, with catalogue values"),
        col("adjustable", m["adjustable"], ucd="meta.note", description="Assumptions whose sliders can change this row"),
        col("quality_source", m["quality_source"], ucd="meta.code.qual", description="Source's rotation-curve quality flag (1 high, 2 medium, 3 low)"),
        col("source_ref", m["source_ref"], ucd="meta.ref", description="Pointer to the source row"),
        col("flags", m["flags"], ucd="meta.code", description="Atlas flags"),
        col("known_issues", m["known_issues"], ucd="meta.ref", description="Open known issues affecting this row (GitHub issue numbers)"),
        col("x_sparc_v_obs", m["x_sparc_v_obs"], kms, "phys.veloc.rotat", "SPARC Vobs, as published", "f8"),
        col("x_sparc_e_v_obs", m["x_sparc_e_v_obs"], kms, "stat.error;phys.veloc.rotat", "SPARC e_Vobs, as published", "f8"),
        col("x_sparc_v_gas", m["x_sparc_v_gas"], kms, "phys.veloc.rotat;meta.modelled", "SPARC Vgas, as published (includes helium factor 1.33)", "f8"),
        col("x_sparc_v_disk", m["x_sparc_v_disk"], kms, "phys.veloc.rotat;meta.modelled", "SPARC Vdisk, as published (for M/L = 1 at 3.6 micron)", "f8"),
        col("x_sparc_v_bul", m["x_sparc_v_bul"], kms, "phys.veloc.rotat;meta.modelled", "SPARC Vbul, as published (for M/L = 1 at 3.6 micron)", "f8"),
    ])
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    s = {k: [] for k in ["system_id", "name_in_source", "class_in_source", "distance_mpc", "distance_err_mpc",
                         "distance_method", "ra_deg", "dec_deg", "inclination_deg", "inclination_err_deg", "properties"]}
    for g in galaxies:
        s["system_id"].append(system_ids[g["name"]])
        s["name_in_source"].append(g["name"])
        s["class_in_source"].append(f"{HUBBLE_TYPES[g['T']]} (Hubble type T={g['T']})")
        s["distance_mpc"].append(g["D"])
        s["distance_err_mpc"].append(g["e_D"])
        s["distance_method"].append(DISTANCE_METHODS[g["f_D"]])
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
        col("distance_mpc", s["distance_mpc"], u.Mpc, "pos.distance", "Distance as given by SPARC", "f8"),
        col("distance_err_mpc", s["distance_err_mpc"], u.Mpc, "stat.error;pos.distance", "Distance error as given by SPARC", "f8"),
        col("distance_method", s["distance_method"], ucd="meta.code", description="Distance method as given by SPARC"),
        col("ra_deg", s["ra_deg"], u.deg, "pos.eq.ra", "Right ascension (not given by SPARC)", "f8"),
        col("dec_deg", s["dec_deg"], u.deg, "pos.eq.dec", "Declination (not given by SPARC)", "f8"),
        col("inclination_deg", s["inclination_deg"], u.deg, "src.orbital.inclination", "Disc inclination as given by SPARC", "f8"),
        col("inclination_err_deg", s["inclination_err_deg"], u.deg, "stat.error;src.orbital.inclination", "Inclination error as given by SPARC", "f8"),
        col("properties", s["properties"], ucd="meta.note", description="Other source-given properties (JSON; units in key names)"),
    ])
    systems.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    registry = [{"system_id": system_ids[g["name"]], "primary_name": g["name"],
                 "first_dataset": f"{DATASET}/{VERSION}", "assigned_on": ASSIGNED_ON} for g in galaxies]
    return meas, systems, registry


def main() -> int:
    source_dir = HERE / "source"
    meas, systems, registry = build(source_dir)
    tables = HERE / "tables"
    tables.mkdir(exist_ok=True)
    meas.write(tables / "measurements.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    systems.write(tables / "systems.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)

    # Registry: SPARC is the first dataset, so it assigns aeg-s-000001 to aeg-s-000175 in Table 1 order.
    reg_path = REPO / "data/registry/systems.csv"
    existing = list(csv.DictReader(reg_path.open(encoding="utf-8")))
    mine = [r for r in existing if r["first_dataset"] == f"{DATASET}/{VERSION}"]
    if existing and mine != registry:
        raise SystemExit("registry already holds different entries; IDs are never reassigned")
    if not existing:
        with reg_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["system_id", "primary_name", "first_dataset", "assigned_on"], lineterminator="\n")
            w.writeheader()
            w.writerows(registry)
    write_datapackage(meas, systems)
    write_checksums()
    print(f"wrote {len(meas)} measurements, {len(systems)} systems")
    return 0


def _schema(table) -> dict:
    fields = []
    for name in table.colnames:
        c = table[name]
        f = {"name": name, "type": "number" if c.dtype.kind == "f" else "string",
             "description": c.description, "ucd": c.meta.get("ucd")}
        if c.unit is not None:
            f["unit"] = str(c.unit)
        fields.append(f)
    return {"fields": fields, "missingValues": [""]}


def write_datapackage(meas, systems) -> None:
    sources = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))
    dialect = {"delimiter": ",", "commentChar": "#", "header": True}
    descriptor = {
        "name": DATASET,
        "version": VERSION,
        "title": "SPARC rotation curves: observed and baryonic accelerations of 175 disc galaxies",
        "description": "Atlas conversion of the SPARC mass models (Lelli, McGaugh & Schombert 2016) to the Atlas data standard: g_obs and g_bar per radius, with g_bar components kept separate. See SOURCE.md and REPRODUCTION_RESULT.md.",
        "x_standard_version": STANDARD,
        "x_licence_status": "Atlas tables intended CC BY 4.0 under D-004; to be confirmed against the terms of the CDS/VizieR record J/AJ/152/157 (issue #9). Source files are not redistributed.",
        "licenses": [],
        "sources": [{"title": s["role"], "path": s["url"]} for s in sources["sources"]],
        "x_citation": "Lelli, F., McGaugh, S. S. & Schombert, J. M. 2016, AJ 152, 157; plus the rotation-curve source for each galaxy (systems table, rotation_curve_refs).",
        "x_known_issues": [f"https://github.com/extragravitation/atlas/issues/{ki['issue']}"
                           for ki in json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]],
        "resources": [
            {"name": "measurements", "path": "tables/measurements.ecsv", "format": "ecsv", "mediatype": "text/csv",
             "encoding": "utf-8", "dialect": dialect, "schema": _schema(meas)},
            {"name": "systems", "path": "tables/systems.ecsv", "format": "ecsv", "mediatype": "text/csv",
             "encoding": "utf-8", "dialect": dialect, "schema": _schema(systems)},
        ],
    }
    (HERE / "datapackage.json").write_text(json.dumps(descriptor, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_checksums() -> None:
    files = sorted(p for p in HERE.rglob("*") if p.is_file() and p.name != "checksums.sha256"
                   and "source" not in p.relative_to(HERE).parts and "__pycache__" not in p.parts
                   and p.suffix not in {".pyc"})
    lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(HERE).as_posix()}" for p in files]
    (HERE / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
