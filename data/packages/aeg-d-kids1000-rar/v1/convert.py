"""Convert the KiDS-1000 lensing RAR release into the Atlas data standard.

Usage: python data/packages/aeg-d-kids1000-rar/v1/convert.py

Reads source/brouwer2021_rar.tar (fetched and hash-verified by aeg.fetch) and
writes tables/measurements.ecsv and tables/covariance.ecsv. Method in
SOURCE.md; reproduction rules in REPRODUCTION.md.
"""

from __future__ import annotations

import json
import sys
import tarfile
from pathlib import Path

import astropy.constants as const
import astropy.units as u
import numpy as np
from astropy.table import MaskedColumn, Table

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "pipeline"))
from aeg.package import write_checksums, write_datapackage  # noqa: E402

DATASET, VERSION, STANDARD = "aeg-d-kids1000-rar", "v1", "1.2.1"
TAR = HERE / "source" / "brouwer2021_rar.tar"

# g_obs = 4 G ΔΣ (paper eq. 7). ΔΣ in M☉/pc² (h = 0.7, physical) -> g in m/s².
FACTOR = (4 * const.G * (1 * u.Msun / u.pc**2)).to(u.m / u.s**2).value
ISOLATION_LIMIT = 1e-13  # m/s²; paper §5.2, KiDS-bright only

SAMPLES = [
    # (key, ESD file, covariance file, method text, hot gas included?, source caveat applies?)
    ("kids_bright", "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt",
     "Weak lensing, stacked isolated KiDS-bright lenses (photometric redshifts)", False, True),
    ("kids_bright_hotgas", "Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt", "Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt",
     "Weak lensing, stacked isolated KiDS-bright lenses; g_bar includes the authors' hot-gas estimate", True, True),
    ("gama", "Fig-4-C1_RAR-GAMA-isolated_Nobins.txt", "Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt",
     "Weak lensing, stacked isolated GAMA lenses (spectroscopic redshifts)", False, False),
]


def read_member(tar: tarfile.TarFile, name: str) -> list[list[float]]:
    text = tar.extractfile(name).read().decode("ascii")
    rows = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        rows.append([float(x) for x in line.split()])
    return rows


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


def build():
    m: dict[str, list] = {k: [] for k in [
        "measurement_id", "system_id", "kind", "channel", "method_class", "method", "r_kpc", "r_kind",
        "g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_bar", "g_bar_err_lo", "g_bar_err_hi",
        "stars_status", "gas_cold_status", "gas_hot_status", "assumptions", "adjustable",
        "quality_source", "source_ref", "flags",
        "x_kids1000_rar_sample", "x_kids1000_rar_esd_t", "x_kids1000_rar_esd_x", "x_kids1000_rar_esd_err",
        "x_kids1000_rar_bias"]}
    cov: dict[str, list] = {k: [] for k in ["measurement_id_i", "measurement_id_j", "quantity", "covariance"]}

    with tarfile.open(TAR) as tar:
        n = 0
        for key, esd_file, cov_file, method, hotgas, caveat in SAMPLES:
            esd = read_member(tar, esd_file)
            if not esd or any(len(r) != 8 for r in esd):
                raise SystemExit(f"{esd_file}: expected rows of 8 columns")
            ids = []
            for k, (gbar, esd_t, esd_x, err, bias, _var, _wk2, _w2k2) in enumerate(esd, start=1):
                n += 1
                mid = f"{DATASET}/{VERSION}/m{n:06d}"
                ids.append(mid)
                g_obs = FACTOR * esd_t / bias
                g_err = FACTOR * err / bias
                low = caveat and gbar < ISOLATION_LIMIT
                m["measurement_id"].append(mid)
                m["system_id"].append(None)
                m["kind"].append("population_bin")
                m["channel"].append("lensing")
                m["method_class"].append("lensing")
                m["method"].append(method)
                m["r_kpc"].append(None)
                m["r_kind"].append(None)
                m["g_obs"].append(g_obs)
                m["g_obs_err_lo"].append(g_err)
                m["g_obs_err_hi"].append(g_err)
                m["g_bar"].append(gbar)
                m["g_bar_err_lo"].append(None)
                m["g_bar_err_hi"].append(None)
                m["stars_status"].append("not_separable")
                m["gas_cold_status"].append("not_separable")
                m["gas_hot_status"].append("not_separable" if hotgas else "absent")
                m["assumptions"].append(";".join(["deproj_lensing=sis"] + (["hot_gas_halo=authors_estimate"] if hotgas else [])))
                m["adjustable"].append("")
                m["quality_source"].append("isolation not reliable below g_bar ~ 1e-13 m/s2 (authors, section 5.2)" if low else "")
                m["source_ref"].append(f"brouwer2021_rar.tar:{esd_file}:data row {k}")
                m["flags"].append(";".join((["source_quality_low"] if low else []) + ["no_uncertainty"]))
                m["x_kids1000_rar_sample"].append(key)
                m["x_kids1000_rar_esd_t"].append(esd_t)
                m["x_kids1000_rar_esd_x"].append(esd_x)
                m["x_kids1000_rar_esd_err"].append(err)
                m["x_kids1000_rar_bias"].append(bias)

            # Covariance: rows (min_m, min_n, gbar_i, gbar_j, cov, corr, bias). Match g_bar to ESD rows.
            gbars = [r[0] for r in esd]

            def index_of(x):
                hits = [i for i, g in enumerate(gbars) if abs(x - g) <= 1e-3 * g]
                if len(hits) != 1:
                    raise SystemExit(f"{cov_file}: g_bar {x} matches {len(hits)} ESD rows")
                return hits[0]

            cov_rows = read_member(tar, cov_file)
            if len(cov_rows) != len(esd) ** 2:
                raise SystemExit(f"{cov_file}: {len(cov_rows)} entries, expected {len(esd) ** 2}")
            for _mm, _mn, gi, gj, c, _corr, b in cov_rows:
                cov["measurement_id_i"].append(ids[index_of(gi)])
                cov["measurement_id_j"].append(ids[index_of(gj)])
                cov["quantity"].append("g_obs")
                cov["covariance"].append(FACTOR**2 * c / b)

    acc = u.m / u.s**2
    sd = u.Msun / u.pc**2
    meas = Table([
        col("measurement_id", m["measurement_id"], ucd="meta.id;meta.main", description="Permanent measurement identifier"),
        col("system_id", m["system_id"], ucd="meta.id", description="Empty: population measurement (stacked lenses)"),
        col("kind", m["kind"], ucd="meta.code", description="Kind of measurement"),
        col("channel", m["channel"], ucd="meta.code", description="Observational channel"),
        col("method_class", m["method_class"], ucd="meta.code.class", description="Class of method"),
        col("method", m["method"], ucd="meta.note", description="Method as given by the source"),
        col("r_kpc", m["r_kpc"], u.kpc, "phys.size.radius", "Empty: the source bins by g_bar, not radius", True),
        col("r_kind", m["r_kind"], ucd="meta.code", description="Empty: no radius"),
        col("g_obs", m["g_obs"], acc, "phys.acceleration", "Observed acceleration, 4 G Delta Sigma (bias-corrected)", True),
        col("g_obs_err_lo", m["g_obs_err_lo"], acc, "stat.error;phys.acceleration", "One-sigma error, from the source's ESD error (bias-corrected)", True),
        col("g_obs_err_hi", m["g_obs_err_hi"], acc, "stat.error;phys.acceleration", "One-sigma error, from the source's ESD error (bias-corrected)", True),
        col("g_bar", m["g_bar"], acc, "phys.acceleration;meta.modelled", "Mean baryonic acceleration of the bin (stars plus cold gas; plus hot gas for the hot-gas variant), as given by the source", True),
        col("g_bar_err_lo", m["g_bar_err_lo"], acc, "stat.error;phys.acceleration", "Not given by the source", True),
        col("g_bar_err_hi", m["g_bar_err_hi"], acc, "stat.error;phys.acceleration", "Not given by the source", True),
        col("stars_status", m["stars_status"], ucd="meta.code", description="Stars are measured photometrically but included only in total g_bar"),
        col("gas_cold_status", m["gas_cold_status"], ucd="meta.code", description="Cold gas from a scaling relation, included only in total g_bar"),
        col("gas_hot_status", m["gas_hot_status"], ucd="meta.code", description="Hot gas: absent, or the authors' estimate included in total g_bar"),
        col("assumptions", m["assumptions"], ucd="meta.note", description="Named assumptions affecting this row"),
        col("adjustable", m["adjustable"], ucd="meta.note", description="Assumptions whose sliders can change this row (none)"),
        col("quality_source", m["quality_source"], ucd="meta.code.qual", description="Source's own caveat, where it applies"),
        col("source_ref", m["source_ref"], ucd="meta.ref", description="Pointer to the source file and row"),
        col("flags", m["flags"], ucd="meta.code", description="Atlas flags"),
        col("x_kids1000_rar_sample", m["x_kids1000_rar_sample"], ucd="meta.code", description="Lens sample: kids_bright, kids_bright_hotgas or gama"),
        col("x_kids1000_rar_esd_t", m["x_kids1000_rar_esd_t"], sd, "phys.columnDensity;meta.main", "Tangential excess surface density, as released (h70 M_sun/pc^2)", True),
        col("x_kids1000_rar_esd_x", m["x_kids1000_rar_esd_x"], sd, "phys.columnDensity", "Cross excess surface density (null check), as released", True),
        col("x_kids1000_rar_esd_err", m["x_kids1000_rar_esd_err"], sd, "stat.error;phys.columnDensity", "Error on the tangential ESD, as released", True),
        col("x_kids1000_rar_bias", m["x_kids1000_rar_bias"], None, "instr.calib", "Multiplicative calibration (1+K), as released", True),
    ])
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    covt = Table([
        col("measurement_id_i", cov["measurement_id_i"], ucd="meta.id", description="First measurement of the pair"),
        col("measurement_id_j", cov["measurement_id_j"], ucd="meta.id", description="Second measurement of the pair"),
        col("quantity", cov["quantity"], ucd="meta.code", description="Quantity whose covariance is given"),
        col("covariance", cov["covariance"], acc**2, "stat.covariance;phys.acceleration", "Covariance of g_obs, converted from the released ESD covariance (bias-corrected)", True),
    ])
    covt.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    return meas, covt


def main() -> int:
    meas, covt = build()
    (HERE / "tables").mkdir(exist_ok=True)
    meas.write(HERE / "tables/measurements.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    covt.write(HERE / "tables/covariance.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    write_datapackage(HERE, {
        "name": DATASET, "version": VERSION,
        "title": "KiDS-1000 weak-lensing radial acceleration relation: stacked isolated lenses",
        "description": "Atlas conversion of the released ESD profiles behind Brouwer et al. 2021 Fig. 4 (KiDS-bright, KiDS-bright with hot gas, GAMA). See SOURCE.md and REPRODUCTION.md.",
        "x_standard_version": STANDARD,
        "x_licence_status": "No licence stated by the source; Atlas tables intended CC BY 4.0 under D-004, citing the source. Source file not redistributed.",
        "licenses": [],
        "sources": [{"title": "KiDS science-data release, Brouwer et al. 2021", "path": "https://kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar.tar"}],
        "x_citation": "Brouwer, M. M. et al. 2021, A&A 650, A113, with the KiDS acknowledgement given in that paper.",
        "x_h": 0.7,
    }, {"measurements": ("tables/measurements.ecsv", meas), "covariance": ("tables/covariance.ecsv", covt)})
    write_checksums(HERE)
    print(f"wrote {len(meas)} measurements, {len(covt)} covariance entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
