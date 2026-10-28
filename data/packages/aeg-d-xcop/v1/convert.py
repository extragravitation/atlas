"""Convert the X-COP public data release into the Atlas data standard.

Usage: python data/packages/aeg-d-xcop/v1/convert.py

Reads source/allfiles.tar.gz (fetched and hash-verified by aeg.fetch; never
committed) and writes tables/measurements.ecsv and tables/systems.ecsv.
Method in SOURCE.md; reproduction rules in REPRODUCTION.md (frozen before
this file existed); assumption rulings in docs/decisions.md D-005 (X-COP
amendment) and D-022.

Per cluster:
  g_obs        = G M_FORW(<r) / r^2           forward-method hydrostatic mass, <cluster>_hydro_mass.fits
  g_bar_gas_hot= G MGAS(<r) / r^2             gas mass, <cluster>_fgas_profile.fits
  g_bar_stars  = G MSTAR(<r) / r^2            measured: <cluster>_mstar.fits, extension MSTAR_SMOOTHED
                                              modelled: Ettori et al. 2019 prescription (D-022 item 3)
Rows are the hydro file's own radii. Gas and stellar profiles, tabulated on
other grids, are interpolated linearly in log M against log r. No profile is
extrapolated: a radius outside the range of any component used for that
cluster is not converted.
"""

from __future__ import annotations

import io
import json
import math
import os
import sys
import tarfile
from pathlib import Path

import astropy.constants as const
import astropy.units as u
import numpy as np
from astropy.io import fits
from astropy.table import MaskedColumn, Table

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "pipeline"))
from aeg.package import write_checksums, write_datapackage  # noqa: E402

DATASET, VERSION, STANDARD = "aeg-d-xcop", "v1", "1.2.1"
TAR = HERE / "source" / "allfiles.tar.gz"
ROOT = HERE.parents[3]

# G M / r^2 with M in solar masses and r in kpc, in m/s^2.
GCONV = (const.G * u.Msun / u.kpc**2).to(u.m / u.s**2).value

# Ettori et al. 2019 (arXiv:1805.00035) Table 1, backward NFW: redshift, R500 [Mpc], M500 [1e14 Msun],
# R200 [Mpc], M200 [1e14 Msun]. Read at source 2026-10-28. Used for the modelled-star prescription
# (M500, R200) and recorded as system properties. Order = Table 1 order = registry order.
TABLE1 = {
    "A85": (0.0555, 1.235, 5.65, 1.921, 8.50),
    "A644": (0.0704, 1.230, 5.66, 1.847, 7.67),
    "A1644": (0.0473, 1.054, 3.48, 1.778, 6.69),
    "A1795": (0.0622, 1.153, 4.63, 1.755, 6.53),
    "A2029": (0.0773, 1.423, 8.82, 2.173, 12.57),
    "A2142": (0.0909, 1.424, 8.95, 2.224, 13.64),
    "A2255": (0.0809, 1.196, 5.26, 2.033, 10.33),
    "A2319": (0.0557, 1.346, 7.31, 2.040, 10.18),
    "A3158": (0.0597, 1.123, 4.26, 1.766, 6.63),
    "A3266": (0.0589, 1.430, 8.80, 2.325, 15.12),
    "RXC1825": (0.0650, 1.105, 4.08, 1.719, 6.15),
    "ZW1215": (0.0766, 1.358, 7.66, 2.200, 13.03),
}
MEASURED_STARS = {"A85", "A644", "A1795", "A2029", "A2142", "A2319", "ZW1215"}

# D-022 item 3 (Ettori et al. 2019 §5): NFW-shaped stellar profile, c = 2.9 relative to r200
# (Lin et al. 2004), normalised by M*/Mgas(<R500) = 0.39 (M500 / 1e14 Msun)^-0.84 (Gonzalez et al. 2013).
STAR_C200 = 2.9
STAR_NORM, STAR_SLOPE = 0.39, -0.84


def nfw_shape(x):
    return math.log(1 + x) - x / (1 + x)


def loglog(x_new, x, y):
    """Linear interpolation of log y against log x. x_new must lie within [x.min(), x.max()]."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if np.any(np.diff(x) <= 0):
        raise SystemExit("interpolation grid is not strictly increasing")
    if np.any(y <= 0):
        raise SystemExit("cannot interpolate non-positive values in log")
    # Scalar math.log/math.exp, not numpy's vectorised versions: those can differ in the last bit
    # between CPUs, which would make the committed tables depend on the machine that built them.
    lx = [math.log(v) for v in x.tolist()]
    ly = [math.log(v) for v in y.tolist()]
    return math.exp(float(np.interp(math.log(x_new), lx, ly)))


def read_fits(tar: tarfile.TarFile, name: str):
    return fits.open(io.BytesIO(tar.extractfile(name).read()))


def registry_ids() -> dict[str, str]:
    import csv
    rows = list(csv.DictReader((ROOT / "data/registry/systems.csv").open(encoding="utf-8")))
    ids = {r["primary_name"]: r["system_id"] for r in rows if r["first_dataset"] == f"{DATASET}/{VERSION}"}
    missing = [c for c in TABLE1 if c not in ids]
    if missing:
        raise SystemExit(f"clusters not in the registry: {missing}")
    return ids


def col(name, data, unit=None, ucd=None, description="", numeric=False):
    data = list(data)
    if numeric:
        mask = [x is None for x in data]
        arr = np.array([np.nan if x is None else x for x in data], dtype="f8")
        c = MaskedColumn(arr, name=name, mask=mask, unit=unit, description=description)
    else:
        c = MaskedColumn([("" if x is None else x) for x in data], name=name, description=description, dtype=str)
    c.meta["ucd"] = ucd
    return c


def cluster_profiles(tar: tarfile.TarFile, name: str) -> dict:
    """Read one cluster's source profiles, radii in kpc."""
    hydro = read_fits(tar, f"{name}/{name}_hydro_mass.fits")[1]
    fgas = read_fits(tar, f"{name}/{name}_fgas_profile.fits")[1]
    if hydro.header["TUNIT1"].strip() != "kpc" or fgas.header["TUNIT1"].strip() != "R/R500":
        raise SystemExit(f"{name}: unexpected radius units")
    # The gas file's radii are in units of the R500 written in its own header.
    r500_gas = float(fgas.header["R500"])
    out = {
        "r": np.array(hydro.data["RADIUS"], float),
        "m_forw": np.array(hydro.data["M_FORW"], float),
        "em_forw": np.array(hydro.data["EM_FORW"], float),
        "r500_gas_header_kpc": r500_gas,
        "gas_r": np.array(fgas.data["RADIUS"], float) * r500_gas,
        "mgas": np.array(fgas.data["MGAS"], float),
        "mgas_lo": np.array(fgas.data["MGAS_LO"], float),  # one-sigma errors below and above (not bounds)
        "mgas_hi": np.array(fgas.data["MGAS_HI"], float),
    }
    if name in MEASURED_STARS:
        hdul = read_fits(tar, f"{name}/{name}_mstar.fits")
        st = hdul["MSTAR_SMOOTHED"]
        if st.header["TUNIT1"].strip() != "kpc":
            raise SystemExit(f"{name}: unexpected stellar radius unit")
        out["star_r"] = np.array(st.data["RADIUS"], float)
        out["mstar"] = np.array(st.data["MSTAR"], float)
        out["mstar_lo"] = np.array(st.data["MSTAR_LO"], float)  # bounds (total uncertainty), not errors
        out["mstar_hi"] = np.array(st.data["MSTAR_HI"], float)
    return out


def build():
    ids = registry_ids()
    m: dict[str, list] = {k: [] for k in [
        "measurement_id", "system_id", "kind", "channel", "method_class", "method", "r_kpc", "r_kind",
        "g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_bar", "g_bar_err_lo", "g_bar_err_hi",
        "g_bar_stars", "g_bar_gas_hot", "stars_status", "gas_cold_status", "gas_hot_status",
        "assumptions", "adjustable", "source_ref", "flags", "known_issues",
        "x_xcop_m_forw", "x_xcop_m_gas", "x_xcop_m_star",
        "x_xcop_g_bar_gas_err_lo", "x_xcop_g_bar_gas_err_hi", "x_xcop_g_bar_stars_err_lo", "x_xcop_g_bar_stars_err_hi"]}
    s: dict[str, list] = {k: [] for k in ["system_id", "name_in_source", "class_in_source", "properties"]}

    issues = json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    tmp: dict[str, list] = {"name": [], "x": [], "d": []}
    with tarfile.open(TAR) as tar:
        names = set(tar.getnames())
        found = sorted(x for x in names if "/" not in x and x in TABLE1)
        if set(found) != set(TABLE1):
            raise SystemExit(f"archive clusters {found} differ from the expected 12")
        for name, (z, r500, m500, r200, m200) in TABLE1.items():
            has_stars = f"{name}/{name}_mstar.fits" in names
            if has_stars != (name in MEASURED_STARS):
                raise SystemExit(f"{name}: stellar file presence differs from the expected set")
            p = cluster_profiles(tar, name)
            lo, hi = p["gas_r"].min(), p["gas_r"].max()
            if has_stars:
                lo, hi = max(lo, p["star_r"].min()), min(hi, p["star_r"].max())
            # The modelled-star prescription is evaluated for every cluster: it is used for the 5
            # without measured stars, and tested against the 7 with measured stars (D-023).
            mgas500 = loglog(r500 * 1000.0, p["gas_r"], p["mgas"])
            mstar500 = STAR_NORM * (m500) ** STAR_SLOPE * mgas500
            rs = r200 * 1000.0 / STAR_C200
            star_scale = mstar500 / nfw_shape(r500 * 1000.0 / rs)
            sid = ids[name]
            kept = 0
            for k, r in enumerate(p["r"], start=1):
                if not (lo <= r <= hi):
                    continue
                kept += 1
                mf, emf = float(p["m_forw"][k - 1]), float(p["em_forw"][k - 1])
                mg = loglog(r, p["gas_r"], p["mgas"])
                mg_lo = loglog(r, p["gas_r"], p["mgas_lo"])
                mg_hi = loglog(r, p["gas_r"], p["mgas_hi"])
                if has_stars:
                    ms = loglog(r, p["star_r"], p["mstar"])
                    ms_lo = ms - loglog(r, p["star_r"], p["mstar_lo"])
                    ms_hi = loglog(r, p["star_r"], p["mstar_hi"]) - ms
                    if ms_lo < 0 or ms_hi < 0:
                        raise SystemExit(f"{name} r={r}: stellar bounds do not bracket the value")
                else:
                    ms = star_scale * nfw_shape(r / rs)
                    ms_lo = ms_hi = None
                f = GCONV / r**2
                tmp["name"].append(name)
                tmp["x"].append(r / (r500 * 1000.0))
                tmp["d"].append((f * mg + f * star_scale * nfw_shape(r / rs)) / (f * mg + f * ms) - 1)
                gs, gg = f * ms, f * mg
                m["measurement_id"].append(None)  # assigned after the D-023 cut
                m["system_id"].append(sid)
                m["kind"].append("profile_point")
                m["channel"].append("dynamics")
                m["method_class"].append("hydrostatic")
                m["method"].append("X-ray and SZ hydrostatic mass, forward method (no assumed mass profile shape), Ettori et al. 2019")
                m["r_kpc"].append(float(r))
                m["r_kind"].append("3d")
                m["g_obs"].append(f * mf)
                m["g_obs_err_lo"].append(f * emf)
                m["g_obs_err_hi"].append(f * emf)
                m["g_bar"].append(gg + gs)
                gse_lo = None if ms_lo is None else f * ms_lo
                gse_hi = None if ms_hi is None else f * ms_hi
                m["g_bar_err_lo"].append(math.sqrt((f * mg_lo) ** 2 + (gse_lo or 0.0) ** 2))
                m["g_bar_err_hi"].append(math.sqrt((f * mg_hi) ** 2 + (gse_hi or 0.0) ** 2))
                m["g_bar_stars"].append(gs)
                m["g_bar_gas_hot"].append(gg)
                m["stars_status"].append("measured" if has_stars else "modelled")
                m["gas_cold_status"].append("absent")
                m["gas_hot_status"].append("measured")
                if has_stars:
                    m["assumptions"].append("xray_hse_bias=0;icl_fraction=0")
                    m["adjustable"].append("xray_hse_bias;icl_fraction")
                else:
                    m["assumptions"].append("xray_hse_bias=0;stars_cluster_modelled=ettori2019")
                    m["adjustable"].append("xray_hse_bias")
                m["source_ref"].append(f"allfiles.tar.gz:{name}/{name}_hydro_mass.fits:row {k}")
                m["flags"].append(";".join(sorted({ki["flag"] for ki in issues if name in ki["clusters"]})))
                m["known_issues"].append(";".join(f"#{ki['issue']}" for ki in issues if name in ki["clusters"]))
                m["x_xcop_m_forw"].append(mf)
                m["x_xcop_m_gas"].append(mg)
                m["x_xcop_m_star"].append(ms)
                m["x_xcop_g_bar_gas_err_lo"].append(f * mg_lo)
                m["x_xcop_g_bar_gas_err_hi"].append(f * mg_hi)
                m["x_xcop_g_bar_stars_err_lo"].append(gse_lo)
                m["x_xcop_g_bar_stars_err_hi"].append(gse_hi)
            if kept == 0:
                raise SystemExit(f"{name}: no radii within the source ranges")
            s["system_id"].append(sid)
            s["name_in_source"].append(name)
            s["class_in_source"].append("Galaxy cluster (X-COP sample)")
            s["properties"].append(json.dumps({
                "redshift": z, "r500_kpc": r500 * 1000.0, "m500_1e14_solMass": m500,
                "r200_kpc": r200 * 1000.0, "m200_1e14_solMass": m200,
                "r500_mass_ref": "Ettori et al. 2019 Table 1 (backward method, NFW model)",
                "r500_gas_file_header_kpc": p["r500_gas_header_kpc"],
                "stars": "measured (Ghizzardi et al. 2020)" if has_stars else "modelled (Ettori et al. 2019 prescription, D-022)",
            }, separators=(",", ":")))

    # D-023: keep modelled-star rows only inside the range validated on the measured clusters.
    validation = validate_model(tmp)
    keep = [nm in MEASURED_STARS or (validation["x_min"] is not None and validation["x_min"] <= x <= validation["x_max"])
            for nm, x in zip(tmp["name"], tmp["x"])]
    m = {k: [v for v, ok in zip(vals, keep) if ok] for k, vals in m.items()}
    kept_names = [nm for nm, ok in zip(tmp["name"], keep) if ok]
    m["measurement_id"] = [f"{DATASET}/{VERSION}/m{i:06d}" for i in range(1, len(kept_names) + 1)]
    validation["rows"] = {nm: {"kept": kept_names.count(nm), "removed": tmp["name"].count(nm) - kept_names.count(nm)}
                          for nm in TABLE1 if nm not in MEASURED_STARS}
    for ki in issues:
        flagged = [mid for mid, nm in zip(m["measurement_id"], kept_names) if nm in ki["clusters"]]
        if os.environ.get("AEG_UPDATE_KNOWN_ISSUES") == "1":  # maintainer use, before committing
            ki["measurements"] = flagged
            (HERE / "known_issues.json").write_text(json.dumps({"issues": issues}, indent=2) + "\n", encoding="utf-8")
        if flagged != ki["measurements"]:
            raise SystemExit(f"known_issues.json issue #{ki['issue']}: measurement list does not match its clusters")

    acc = u.m / u.s**2
    msun = u.Msun
    meas = Table([
        col("measurement_id", m["measurement_id"], ucd="meta.id;meta.main", description="Permanent measurement identifier"),
        col("system_id", m["system_id"], ucd="meta.id", description="Atlas system identifier"),
        col("kind", m["kind"], ucd="meta.code", description="Kind of measurement"),
        col("channel", m["channel"], ucd="meta.code", description="Observational channel"),
        col("method_class", m["method_class"], ucd="meta.code.class", description="Class of method"),
        col("method", m["method"], ucd="meta.note", description="Method as given by the source"),
        col("r_kpc", m["r_kpc"], u.kpc, "phys.size.radius", "Three-dimensional radius, from the source's hydrostatic-mass grid", True),
        col("r_kind", m["r_kind"], ucd="meta.code", description="Radius is three-dimensional"),
        col("g_obs", m["g_obs"], acc, "phys.acceleration", "Observed acceleration, G M_forward(<r) / r^2", True),
        col("g_obs_err_lo", m["g_obs_err_lo"], acc, "stat.error;phys.acceleration", "One-sigma error, from the source's forward-method mass error", True),
        col("g_obs_err_hi", m["g_obs_err_hi"], acc, "stat.error;phys.acceleration", "One-sigma error, from the source's forward-method mass error", True),
        col("g_bar", m["g_bar"], acc, "phys.acceleration", "Baryonic acceleration, G (M_gas + M_stars)(<r) / r^2", True),
        col("g_bar_err_lo", m["g_bar_err_lo"], acc, "stat.error;phys.acceleration", "Gas and measured-star errors in quadrature; modelled stars carry no error", True),
        col("g_bar_err_hi", m["g_bar_err_hi"], acc, "stat.error;phys.acceleration", "Gas and measured-star errors in quadrature; modelled stars carry no error", True),
        col("g_bar_stars", m["g_bar_stars"], acc, "phys.acceleration", "Stellar component of g_bar (measured or modelled, see stars_status)", True),
        col("g_bar_gas_hot", m["g_bar_gas_hot"], acc, "phys.acceleration", "Hot-gas component of g_bar, from the X-ray gas mass", True),
        col("stars_status", m["stars_status"], ucd="meta.code", description="Stars measured (Ghizzardi et al. 2020) or modelled (D-022)"),
        col("gas_cold_status", m["gas_cold_status"], ucd="meta.code", description="Cold gas not included by the source"),
        col("gas_hot_status", m["gas_hot_status"], ucd="meta.code", description="Hot gas measured from X-ray emission"),
        col("assumptions", m["assumptions"], ucd="meta.note", description="Named assumptions affecting this row"),
        col("adjustable", m["adjustable"], ucd="meta.note", description="Assumptions whose sliders can change this row"),
        col("source_ref", m["source_ref"], ucd="meta.ref", description="Pointer to the source file and row"),
        col("flags", m["flags"], ucd="meta.code", description="Atlas flags"),
        col("known_issues", m["known_issues"], ucd="meta.ref", description="Open known issues affecting this row (GitHub issue numbers)"),
        col("x_xcop_m_forw", m["x_xcop_m_forw"], msun, "phys.mass", "Forward-method hydrostatic mass within r, as released", True),
        col("x_xcop_m_gas", m["x_xcop_m_gas"], msun, "phys.mass", "Gas mass within r, interpolated in log-log from the release", True),
        col("x_xcop_m_star", m["x_xcop_m_star"], msun, "phys.mass", "Stellar mass within r: interpolated from the release, or modelled (D-022)", True),
        col("x_xcop_g_bar_gas_err_lo", m["x_xcop_g_bar_gas_err_lo"], acc, "stat.error;phys.acceleration", "Lower one-sigma error of the gas component", True),
        col("x_xcop_g_bar_gas_err_hi", m["x_xcop_g_bar_gas_err_hi"], acc, "stat.error;phys.acceleration", "Upper one-sigma error of the gas component", True),
        col("x_xcop_g_bar_stars_err_lo", m["x_xcop_g_bar_stars_err_lo"], acc, "stat.error;phys.acceleration", "Lower error of measured stars (total uncertainty as released); empty if modelled", True),
        col("x_xcop_g_bar_stars_err_hi", m["x_xcop_g_bar_stars_err_hi"], acc, "stat.error;phys.acceleration", "Upper error of measured stars (total uncertainty as released); empty if modelled", True),
    ])
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    systems = Table([
        col("system_id", s["system_id"], ucd="meta.id;meta.main", description="Atlas system identifier"),
        col("name_in_source", s["name_in_source"], ucd="meta.id", description="Cluster name as in the X-COP release"),
        col("class_in_source", s["class_in_source"], ucd="src.class", description="Class as the source gives it"),
        col("properties", s["properties"], ucd="meta.note", description="Source-given properties (JSON; units in key names)"),
    ])
    systems.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    return meas, systems, validation


def validate_model(tmp: dict) -> dict:
    """The frozen test of MODEL_TEST.md (D-023), steps 3 to 5."""
    grid = np.exp(np.linspace(math.log(0.025), math.log(1.5), 50))
    per = {}
    for nm in MEASURED_STARS:
        xs = np.array([x for n_, x in zip(tmp["name"], tmp["x"]) if n_ == nm])
        ds = np.array([d for n_, d in zip(tmp["name"], tmp["d"]) if n_ == nm])
        per[nm] = (xs, ds)
    points = []
    for x in grid:
        vals = [abs(float(np.interp(math.log(x), np.log(xs), ds))) for xs, ds in per.values() if xs.min() <= x <= xs.max()]
        D = float(np.median(vals)) if len(vals) >= 5 else None
        points.append({"x": float(x), "n": len(vals), "D": D, "pass": None if D is None else D <= 0.10})
    covered = [pt for pt in points if pt["D"] is not None]
    x_min = x_max = None
    if covered and covered[-1]["pass"]:
        x_max = covered[-1]["x"]
        x_min = x_max
        for pt in reversed(covered):
            if not pt["pass"]:
                break
            x_min = pt["x"]
    return {"points": points, "x_min": x_min, "x_max": x_max}


def main() -> int:
    meas, systems, validation = build()
    (HERE / "tables").mkdir(exist_ok=True)
    meas.write(HERE / "tables/measurements.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    systems.write(HERE / "tables/systems.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    write_datapackage(HERE, {
        "name": DATASET, "version": VERSION,
        "title": "X-COP galaxy clusters: hydrostatic acceleration profiles with gas and stellar masses",
        "description": "Atlas conversion of the X-COP public data release: forward-method hydrostatic masses (Ettori et al. 2019), gas masses (Eckert et al. 2019) and stellar masses (Ghizzardi et al. 2020; modelled for 5 clusters, D-022). See SOURCE.md and REPRODUCTION.md.",
        "x_standard_version": STANDARD,
        "x_licence_status": "No licence stated by the source; Atlas tables intended CC BY 4.0 under D-004, citing the source. Source archive not redistributed.",
        "licenses": [],
        "sources": [{"title": "X-COP public data release", "path": "https://dominiqueeckert.wixsite.com/xcop/data"}],
        "x_citation": "As the X-COP data page requests (read 2026-10-28): thermodynamic profiles, Ghirardini et al. 2018; mass profiles, Ettori et al. 2018 (arXiv:1805.00035; A&A 621, A39); gas mass and gas fraction, Eckert et al. 2018 (arXiv:1805.00034); metal abundance profiles, Ghizzardi et al. 2020 (arXiv:2007.01084; its stellar-mass profiles are used here); A2142, Tchernin et al. 2016; A2319, Ghirardini et al. 2017; RXC 1825, Clavico et al. 2019.",
        "x_known_issues": [ki["url"] for ki in json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]],
        "x_model_test": {"decision": "D-023", "x_min_r_over_r500": validation["x_min"], "x_max_r_over_r500": validation["x_max"],
                         "modelled_rows": validation["rows"]},
        "x_cosmology": "As in the source papers (flat LCDM, H0 = 70 km/s/Mpc, Omega_m = 0.3)",
    }, {"measurements": ("tables/measurements.ecsv", meas), "systems": ("tables/systems.ecsv", systems)})
    write_checksums(HERE)
    (HERE / "source" / "model_test.json").write_text(json.dumps(validation, indent=1), encoding="utf-8")
    print(f"wrote {len(meas)} measurements, {len(systems)} systems; model test range {validation['x_min']} to {validation['x_max']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
