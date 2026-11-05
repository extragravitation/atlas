"""Convert the KiDS-1000 lensing RAR release into the Atlas data standard 2.5.1 (aeg-d-kids1000-rar/v2).

Usage: python data/packages/aeg-d-kids1000-rar/v2/convert.py

The frozen test is REPRODUCTION_REV3.md (re-issued under D-103; it supersedes REPRODUCTION.md). In order:
1. Item 12: every release member used (six data and covariance files and the README) must have the SHA-256
   listed in the frozen reading reading/kids-d096.md. A mismatch stops the conversion.
2. Item 11: the frozen parser reading/scripts/read.py regenerates the second reading from the release, into the
   gitignored source/reading/ folder; the covariance reading (not committed: the release is not
   redistributable) and the committed second-reading CSV must match their frozen hashes. A mismatch stops.
3. The tables are written. Values are computed exactly as v1 (convert.py of v1): g_obs = 4 G ΔΣ / bias.
   Plotting follows item 9 only: the hot-gas variant is an alternative (D-096 rule 3); KiDS-bright rows 1–8
   are recorded, not plotted (D-103; D-096 rule 2). There is no other row-specific rule.

Scoring is separate (reproduction/score.py), after this has run.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path

import astropy.constants as const
import astropy.units as u
import numpy as np
from astropy.table import MaskedColumn, Table

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg.package import write_checksums, write_datapackage  # noqa: E402

DATASET, VERSION, STANDARD = "aeg-d-kids1000-rar", "v2", "2.5.1"
PFX = f"{DATASET}/{VERSION}"
TAR = HERE / "source" / "brouwer2021_rar.tar"
RELEASE = HERE / "source" / "release"
READ_OUT = HERE / "source" / "reading"
FROZEN_READING = ROOT / "data/frozen/kids-v2-reading.json"

# As v1: g_obs = 4 G ΔΣ (paper eq. 7). ΔΣ in M☉/pc² (h = 0.7, physical) -> g in m/s².
FACTOR = (4 * const.G * (1 * u.Msun / u.pc**2)).to(u.m / u.s**2).value
ISOLATION_LIMIT = 1e-13  # m/s²; v1's flag rule (paper §5.2), kept unchanged (REPRODUCTION_REV3.md item 6)
DELTA = np.log10(5e-12 / 1e-15) / 15  # §2.1, l. 174: 15 logarithmic bins

SAMPLES = [
    # (key, ESD file, covariance file, method text, hot gas included?, v1 caveat applies?)
    ("kids_bright", "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt",
     "Weak lensing, stacked isolated KiDS-bright lenses (photometric redshifts)", False, True),
    ("kids_bright_hotgas", "Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt", "Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt",
     "Weak lensing, stacked isolated KiDS-bright lenses; g_bar includes the authors' hot-gas estimate", True, True),
    ("gama", "Fig-4-C1_RAR-GAMA-isolated_Nobins.txt", "Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt",
     "Weak lensing, stacked isolated GAMA lenses (spectroscopic redshifts)", False, False),
]
README = "README.txt"

# Item 9 (D-103): KiDS-bright rows beyond the source's isolation limit; the frozen reading names them.
D103_ROWS = range(1, 9)
D103_NOTE = (
    "D-096 rule 2 (D-103): excluded by the source from its tests of analytical models (l. 748); recorded, not plotted. "
    "The source: \"by only using the seven data points within the isolation criterion limit ($R < 3 \\hMpc$)\" (l. 508); "
    "\"When testing these models, we can only use the ESD profile of isolated KiDS-bright lenses within $R < 0.3 \\hMpc$. "
    "For the mean galaxy mass of the KiDS-bright isolated sample ($\\log[M\\un{gal}/\\hmsun] = 10.69$) this corresponds to a "
    "baryonic acceleration of $g\\un{gal}>7.56\\E{-14} \\mpss$\" (l. 748); \"Here we have removed all data points beyond the "
    "KiDS isolation limit ($R>3 \\hMpc$)\" (l. 821). Reason, as the source states it: photometric-redshift errors admit "
    "non-isolated lenses, so that beyond 0.3 h70⁻¹ Mpc \"the ESD of the isolated sample selected using the offset MICE data "
    "is ∼30% higher than that of the truly isolated MICE galaxies\" (l. 748). Brouwer et al. 2021, RAR_paper_Brouwer_4.tex "
    "(arXiv 2106.11677). The limit is written as both 0.3 and 3 h70⁻¹ Mpc (known issue #169)."
)
POINT_MASS_NOTE = ("Baryons as a point mass at the lens centre (Brouwer et al. 2021 §4.3, l. 405–411; registry "
                   "baryons_point_mass); the SIS deprojection assumes a density profile for the total mass "
                   "(model_dependence = total_mass_form; D-087; K3).")
HOTGAS_NOTE = ("Hot-gas variant: an assumed isothermal hot-gas halo with M_gas = M★ within 100 h70⁻¹ kpc is added to g_bar, "
               "'only a rough order of magnitude estimate' (§5.2, l. 512); gas_hot_status = modelled (D-034), because the gas "
               "is assumed, not detected. An unplotted alternative (D-096 rule 3: the source's 'fiducial estimate' is stars "
               "plus cold gas, §4.3, l. 421). The pairing with the KiDS-bright row of the same bin index is formal: the variant "
               "was binned on its own g_bar, so its bin k holds different lenses. That this file uses the §2.1 bin edges is "
               "the Atlas's inference (REPRODUCTION_REV3.md item 5).")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def frozen_member_hashes() -> dict[str, str]:
    """The seven member hashes listed in the frozen reading reading/kids-d096.md (item 12)."""
    text = (HERE / "reading/kids-d096.md").read_text(encoding="utf-8")
    out = dict(re.findall(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|", text, flags=re.M))
    if len(out) != 7:
        raise SystemExit(f"reading/kids-d096.md: expected 7 member hashes, found {len(out)}")
    return out


def check_and_extract() -> dict[str, bytes]:
    """Item 12: each member used has the frozen hash. Extracts them for the regenerated second reading."""
    want = frozen_member_hashes()
    got: dict[str, bytes] = {}
    with tarfile.open(TAR) as tar:
        for m in tar.getmembers():
            name = Path(m.name).name
            if m.isfile() and name in want:
                if name in got:
                    raise SystemExit(f"item 12: {name} appears twice in the tarball")
                got[name] = tar.extractfile(m).read()
    missing = sorted(set(want) - set(got))
    if missing:
        raise SystemExit(f"item 12 FAIL: members missing from the tarball: {missing}")
    bad = [n for n in want if sha256(got[n]) != want[n]]
    if bad:
        raise SystemExit("item 12 FAIL: hash mismatch for " + ", ".join(f"{n} ({sha256(got[n])})" for n in bad))
    RELEASE.mkdir(parents=True, exist_ok=True)
    for n, b in got.items():
        (RELEASE / n).write_bytes(b)
    print(f"item 12: {len(got)} release members match reading/kids-d096.md")
    return got


def regenerate_reading() -> None:
    """Item 11: regenerate the second reading with the frozen parser and check the frozen hashes."""
    frozen = json.loads(FROZEN_READING.read_text(encoding="utf-8"))
    READ_OUT.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-I", str(HERE / "reading/scripts/read.py"), str(RELEASE), str(READ_OUT)],
                   check=True, capture_output=True, text=True)
    cov_rel = "data/packages/aeg-d-kids1000-rar/v2/source/reading/kids-covariance.csv"
    csv_rel = "data/packages/aeg-d-kids1000-rar/v2/reading/kids-second-reading.csv"
    checks = [(READ_OUT / "kids-covariance.csv", frozen["off_repo"][cov_rel], "covariance reading (off_repo)"),
              (READ_OUT / "kids-second-reading.csv", frozen["files"][csv_rel], "second-reading CSV")]
    for path, expected, what in checks:
        found = sha256(path.read_bytes())
        if found != expected:
            raise SystemExit(f"item 11 FAIL: regenerated {what} has SHA-256 {found}, frozen {expected}")
    print("item 11: regenerated covariance reading and second-reading CSV match their frozen hashes")


def parse(data: bytes) -> list[list[float]]:
    rows = []
    for line in data.decode("ascii").splitlines():
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


def build(members: dict[str, bytes]):
    M: dict[str, list] = {k: [] for k in [
        "measurement_id", "system_id", "kind", "channel", "method_class", "method", "measured_quantity", "r_kpc",
        "r_kind", "g_obs", "g_obs_err_lo", "g_obs_err_hi", "err_level", "err_level_status", "g_bar",
        "g_bar_err_lo", "g_bar_err_hi", "g_bar_basis", "g_bar_bin_lo", "g_bar_bin_hi", "limit",
        "stars_status", "gas_cold_status", "gas_hot_status", "observed_from", "baryonic_from", "model_dependence",
        "evidence_tier", "role", "alternative_of", "plotted", "not_plotted_reason", "assumptions", "adjustable",
        "quality_source", "source_ref", "flags", "notes",
        "x_kids1000_rar_sample", "x_kids1000_rar_esd_t", "x_kids1000_rar_esd_x", "x_kids1000_rar_esd_err",
        "x_kids1000_rar_bias"]}
    O: dict[str, list] = {k: [] for k in [
        "observable_id", "system_id", "side", "quantity", "value", "err_lo", "err_hi", "unit", "limit",
        "err_level", "err_level_status", "steps", "evidence_tier", "source_ref"]}
    cov: dict[str, list] = {k: [] for k in ["measurement_id_i", "measurement_id_j", "quantity", "covariance"]}

    n = no = 0
    kb_ids: list[str] = []
    for key, esd_file, cov_file, method, hotgas, caveat in SAMPLES:
        esd = parse(members[esd_file])
        if len(esd) != 15 or any(len(r) != 8 for r in esd):
            raise SystemExit(f"{esd_file}: expected 15 rows of 8 columns")
        ids = []
        for k, (gbar, esd_t, esd_x, err, bias, _var, _wk2, _w2k2) in enumerate(esd, start=1):
            n += 1
            mid = f"{PFX}/m{n:06d}"
            ids.append(mid)
            if key == "kids_bright":
                kb_ids.append(mid)
            g_obs = FACTOR * esd_t / bias  # as v1, same expression
            g_err = FACTOR * err / bias
            low = caveat and gbar < ISOLATION_LIMIT
            ref = f"brouwer2021_rar.tar:{esd_file}:data row {k}"
            o_obs, o_bar = f"{PFX}/o{no + 1:06d}", f"{PFX}/o{no + 2:06d}"
            no += 2
            # observables (item 8)
            O["observable_id"] += [o_obs, o_bar]
            O["system_id"] += [None, None]
            O["side"] += ["observed", "baryonic"]
            O["quantity"] += ["delta_sigma", "acceleration_released"]
            O["value"] += [esd_t, gbar]
            O["err_lo"] += [err, None]
            O["err_hi"] += [err, None]
            O["unit"] += ["solMass / pc2", "m / s2"]
            O["limit"] += ["none", "none"]
            O["err_level"] += [0.683, None]
            O["err_level_status"] += ["stated", None]
            O["steps"] += ["shapes;shear;excess_surface_density", "photometry"]
            O["evidence_tier"] += [1, 1]
            bar_ref = (f"{ref}, column 1 (g_bar). The released value is the arithmetic midpoint of the source's §2.1 bin {k} "
                       "(l. 174; v2/reading/kids-bins.md), the coordinate at which the lenses were binned on their own g_bar. "
                       "Source steps: per-lens stellar mass (SPS fit) plus cold gas (Boselli et al. 2014 relation), as a point "
                       "mass, binned in g_bar (Brouwer et al. 2021 §2.1, §3.3, §4.3)")
            if hotgas:
                bar_ref += (", plus an assumed isothermal hot-gas halo with M_gas = M★ within 100 h70⁻¹ kpc, "
                            "'only a rough order of magnitude estimate' (§5.2, l. 512)")
            O["source_ref"] += [f"{ref}, column 2 (ESD_t, h70 M☉/pc², before the bias correction; column 5 is the bias) "
                                f"and column 4 (error: 'The 1-sigma error value on ESD_t', README)", bar_ref]
            # measurements
            lo, hi = 10 ** (-15 + (k - 1) * DELTA), 10 ** (-15 + k * DELTA)
            d103 = key == "kids_bright" and k in D103_ROWS
            notes = [POINT_MASS_NOTE]
            if hotgas:
                notes.append(HOTGAS_NOTE)
            if d103:
                notes.append(D103_NOTE)
            if key == "gama":
                notes.append("GAMA is 'still reliable within this region' of low g_bar (Brouwer et al. 2021 §5.2, l. 489).")
            M["measurement_id"].append(mid)
            M["system_id"].append(None)
            M["kind"].append("population_bin")
            M["channel"].append("lensing")
            M["method_class"].append("lensing")
            M["method"].append(method)
            M["measured_quantity"].append("g_obs")
            M["r_kpc"].append(None)
            M["r_kind"].append(None)
            M["g_obs"].append(g_obs)
            M["g_obs_err_lo"].append(g_err)
            M["g_obs_err_hi"].append(g_err)
            M["err_level"].append(0.683)
            M["err_level_status"].append("stated")
            M["g_bar"].append(gbar)
            M["g_bar_err_lo"].append(None)
            M["g_bar_err_hi"].append(None)
            M["g_bar_basis"].append("bin_coordinate")
            M["g_bar_bin_lo"].append(lo)
            M["g_bar_bin_hi"].append(hi)
            M["limit"].append("none")
            M["stars_status"].append("not_separable")
            M["gas_cold_status"].append("not_separable")
            M["gas_hot_status"].append("modelled" if hotgas else "absent")
            M["observed_from"].append(o_obs)
            M["baryonic_from"].append(o_bar)
            M["model_dependence"].append("total_mass_form")
            M["evidence_tier"].append(1)
            if hotgas:
                M["role"].append("alternative")
                M["alternative_of"].append(kb_ids[k - 1])
                M["plotted"].append("false")
                M["not_plotted_reason"].append("alternative_value")
            elif d103:
                M["role"].append("default")
                M["alternative_of"].append(None)
                M["plotted"].append("false")
                M["not_plotted_reason"].append("other")
            else:
                M["role"].append("default")
                M["alternative_of"].append(None)
                M["plotted"].append("true")
                M["not_plotted_reason"].append(None)
            M["assumptions"].append(";".join(["deproj_lensing=sis", "baryons_point_mass"]
                                             + (["hot_gas_halo=authors_estimate"] if hotgas else [])))
            M["adjustable"].append("")
            M["quality_source"].append("isolation not reliable below g_bar ~ 1e-13 m/s2 (authors, section 5.2)" if low else "")
            M["source_ref"].append(ref)
            M["flags"].append("source_quality_low" if low else "")
            M["notes"].append(" ".join(notes))
            M["x_kids1000_rar_sample"].append(key)
            M["x_kids1000_rar_esd_t"].append(esd_t)
            M["x_kids1000_rar_esd_x"].append(esd_x)
            M["x_kids1000_rar_esd_err"].append(err)
            M["x_kids1000_rar_bias"].append(bias)

        gbars = [r[0] for r in esd]

        def index_of(x):
            hits = [i for i, g in enumerate(gbars) if abs(x - g) <= 1e-3 * g]
            if len(hits) != 1:
                raise SystemExit(f"{cov_file}: g_bar {x} matches {len(hits)} ESD rows")
            return hits[0]

        cov_rows = parse(members[cov_file])
        if len(cov_rows) != len(esd) ** 2:
            raise SystemExit(f"{cov_file}: {len(cov_rows)} entries, expected {len(esd) ** 2}")
        for _mm, _mn, gi, gj, c, _corr, b in cov_rows:  # as v1
            cov["measurement_id_i"].append(ids[index_of(gi)])
            cov["measurement_id_j"].append(ids[index_of(gj)])
            cov["quantity"].append("g_obs")
            cov["covariance"].append(FACTOR**2 * c / b)

    acc = u.m / u.s**2
    sd = u.Msun / u.pc**2
    meas = Table([
        col("measurement_id", M["measurement_id"], ucd="meta.id;meta.main", description="Permanent measurement identifier"),
        col("system_id", M["system_id"], ucd="meta.id", description="Empty: population measurement (stacked lenses)"),
        col("kind", M["kind"], ucd="meta.code", description="Kind of measurement"),
        col("channel", M["channel"], ucd="meta.code", description="Observational channel"),
        col("method_class", M["method_class"], ucd="meta.code.class", description="Class of method"),
        col("method", M["method"], ucd="meta.note", description="Method as given by the source. Built in (K6): each lens's photometric or spectroscopic redshift enters ΔΣ through Σ_crit (Brouwer et al. 2021 eq. 3; σ_z/(1+z) = 0.02 for KiDS-bright, §3.1, l. 315); it is not a separate error"),
        col("measured_quantity", M["measured_quantity"], ucd="meta.code", description="The quantity this row measures"),
        col("r_kpc", M["r_kpc"], u.kpc, "phys.size.radius", "Empty: the source bins by g_bar, not radius", True),
        col("r_kind", M["r_kind"], ucd="meta.code", description="Empty: no radius"),
        col("g_obs", M["g_obs"], acc, "phys.acceleration", "Observed acceleration, 4 G ΔΣ / bias (paper eq. 7; README recipe)", True),
        col("g_obs_err_lo", M["g_obs_err_lo"], acc, "stat.error;phys.acceleration", "Point-scale one-sigma error: the released ESD error / bias, times 4G (K1 only). The 0.1 dex the paper adds for the ΔΣ-to-g_obs conversion (K2) is the term esd_to_gobs_conversion, not included here", True),
        col("g_obs_err_hi", M["g_obs_err_hi"], acc, "stat.error;phys.acceleration", "As g_obs_err_lo", True),
        col("err_level", M["err_level"], None, "stat.value", "Confidence level of g_obs_err_*: 0.683, as stated ('The 1-sigma error value on ESD_t', README)", True),
        col("err_level_status", M["err_level_status"], ucd="meta.code", description="stated: the README states one sigma"),
        col("g_bar", M["g_bar"], acc, "phys.acceleration;meta.modelled", "The source's g_bar bin coordinate, as released: the arithmetic midpoint of its §2.1 bin (stars plus cold gas; plus an assumed hot-gas halo for the variant)", True),
        col("g_bar_err_lo", M["g_bar_err_lo"], acc, "stat.error;phys.acceleration", "Empty: g_bar is the bin coordinate, with no point error by construction (g_bar_basis)", True),
        col("g_bar_err_hi", M["g_bar_err_hi"], acc, "stat.error;phys.acceleration", "Empty: as g_bar_err_lo", True),
        col("g_bar_basis", M["g_bar_basis"], ucd="meta.code", description="bin_coordinate: the source binned lenses on their own g_bar (§2.1, l. 174)"),
        col("g_bar_bin_lo", M["g_bar_bin_lo"], acc, "phys.acceleration;stat.min", "Lower edge of the source's g_bar bin k: 10^(−15 + (k−1)Δ), Δ = log10(5e-12/1e-15)/15 (§2.1, l. 174)", True),
        col("g_bar_bin_hi", M["g_bar_bin_hi"], acc, "phys.acceleration;stat.max", "Upper edge of the source's g_bar bin k: 10^(−15 + kΔ)", True),
        col("limit", M["limit"], ucd="meta.code", description="none: every row is a measurement"),
        col("stars_status", M["stars_status"], ucd="meta.code", description="Stars are measured photometrically but included only in total g_bar"),
        col("gas_cold_status", M["gas_cold_status"], ucd="meta.code", description="Cold gas from a scaling relation, included only in total g_bar"),
        col("gas_hot_status", M["gas_hot_status"], ucd="meta.code", description="Hot gas: absent, or modelled (the authors' assumed halo, hot-gas variant only; D-034)"),
        col("observed_from", M["observed_from"], ucd="meta.id", description="Observable behind g_obs (delta_sigma)"),
        col("baryonic_from", M["baryonic_from"], ucd="meta.id", description="Observable behind g_bar (acceleration_released)"),
        col("model_dependence", M["model_dependence"], ucd="meta.code", description="total_mass_form: the SIS deprojection assumes a density profile for the total mass (D-087; K3)"),
        col("evidence_tier", M["evidence_tier"], None, "meta.code.qual", "D-035 evidence tier", True),
        col("role", M["role"], ucd="meta.code", description="default, or alternative (the hot-gas variant, D-096 rule 3)"),
        col("alternative_of", M["alternative_of"], ucd="meta.id", description="For the hot-gas variant: the KiDS-bright row with the same bin index (a formal pairing; see notes)"),
        col("plotted", M["plotted"], ucd="meta.code", description="Whether the row is drawn by default"),
        col("not_plotted_reason", M["not_plotted_reason"], ucd="meta.code", description="alternative_value (hot-gas variant) or other (KiDS-bright rows 1–8: D-103; see notes)"),
        col("assumptions", M["assumptions"], ucd="meta.note", description="Named assumptions affecting this row (registry: deproj_lensing, baryons_point_mass, hot_gas_halo)"),
        col("adjustable", M["adjustable"], ucd="meta.note", description="Assumptions whose sliders can change this row (none)"),
        col("quality_source", M["quality_source"], ucd="meta.code.qual", description="Source's own caveat, where it applies (as v1)"),
        col("source_ref", M["source_ref"], ucd="meta.ref", description="Pointer to the source file and row"),
        col("flags", M["flags"], ucd="meta.code", description="Atlas flags. v1's no_uncertainty (about g_bar, #64) is replaced by g_bar_basis = bin_coordinate"),
        col("notes", M["notes"], ucd="meta.note", description="Notes: assumed baryon forms; the hot-gas variant; the source's own exclusion of KiDS-bright rows 1–8 (D-103)"),
        col("x_kids1000_rar_sample", M["x_kids1000_rar_sample"], ucd="meta.code", description="Lens sample: kids_bright, kids_bright_hotgas or gama"),
        col("x_kids1000_rar_esd_t", M["x_kids1000_rar_esd_t"], sd, "phys.columnDensity;meta.main", "Tangential excess surface density, as released (h70 M_sun/pc^2)", True),
        col("x_kids1000_rar_esd_x", M["x_kids1000_rar_esd_x"], sd, "phys.columnDensity", "Cross excess surface density (null check), as released", True),
        col("x_kids1000_rar_esd_err", M["x_kids1000_rar_esd_err"], sd, "stat.error;phys.columnDensity", "Error on the tangential ESD, as released", True),
        col("x_kids1000_rar_bias", M["x_kids1000_rar_bias"], None, "instr.calib", "Multiplicative calibration (1+K), as released", True),
    ])
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    obs = Table([
        col("observable_id", O["observable_id"], ucd="meta.id;meta.main", description="Permanent observable identifier"),
        col("system_id", O["system_id"], ucd="meta.id", description="Empty: population measurement"),
        col("side", O["side"], ucd="meta.code", description="observed (g_obs side) or baryonic (g_bar side)"),
        col("quantity", O["quantity"], ucd="meta.code", description="Quantity, from the closed list of standard §4a"),
        col("value", O["value"], None, "meta.number", "Value as released, in the row's unit", True),
        col("err_lo", O["err_lo"], None, "stat.error", "Lower error as released, in the row's unit", True),
        col("err_hi", O["err_hi"], None, "stat.error", "Upper error as released, in the row's unit", True),
        col("unit", O["unit"], ucd="meta.unit", description="Unit of value and errors (ΔΣ in h70 M☉/pc², h = 0.7 as the source)"),
        col("limit", O["limit"], ucd="meta.code", description="none"),
        col("err_level", O["err_level"], None, "stat.value", "Confidence level of err_lo/err_hi, as stated", True),
        col("err_level_status", O["err_level_status"], ucd="meta.code", description="stated, where the source states the level"),
        col("steps", O["steps"], ucd="meta.note", description="Steps from the standard's ladders"),
        col("evidence_tier", O["evidence_tier"], None, "meta.code.qual", "D-035 evidence tier", True),
        col("source_ref", O["source_ref"], ucd="meta.ref", description="Source file, row and column, with the source's own steps"),
    ])
    obs.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    covt = Table([
        col("measurement_id_i", cov["measurement_id_i"], ucd="meta.id", description="First measurement of the pair"),
        col("measurement_id_j", cov["measurement_id_j"], ucd="meta.id", description="Second measurement of the pair"),
        col("quantity", cov["quantity"], ucd="meta.code", description="Quantity whose covariance is given"),
        col("covariance", cov["covariance"], acc**2, "stat.covariance;phys.acceleration", "Covariance of g_obs, converted from the released ESD covariance (bias-corrected)", True),
    ])
    covt.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    return meas, obs, covt


TERMS = [
    # term_id, reading, scale, moves, status, size_value, size_unit, size_kind, locator, note, in_error_columns
    ("esd_to_gobs_conversion", "K2", "point", "g_obs", "given", 0.1, "dex", "as_released", "§4.4, l. 438",
     "Added by the paper to every RAR error bar for the ΔΣ-to-g_obs conversion: 'we added 0.1 dex to the error bars of our RAR measurements throughout this work'. The release omits it, and how it combines with the released error (K1) is not stated. All samples.", "no"),
    ("shear_calibration", "K4", "dataset", "g_obs", "not_given_by_source", None, None, None, "§3.1, l. 333–337",
     "The correction μ ≈ 0.014 is applied (the bias column); its uncertainty is not stated. All samples.", None),
    ("source_redshift_calibration", "K5", "dataset", "g_obs", "not_given_by_source", None, None, None, "§3.1, l. 313",
     "'percent-level biases in the mean source redshifts do not significantly impact our analysis', as stated; no size. All samples.", None),
    ("random_subtraction", "K7", "dataset", "g_obs", "not_given_by_source", None, None, None, "§3.1, l. 339",
     "The subtracted random-point profile is described as 'only 1.85 ± 0.75 %' of the signal; a correction applied, not an error on the result. KiDS-bright.", None),
    ("stellar_mass_per_lens_kids", "K8", "dataset", "both", "given", 0.12, "dex", "one_sigma", "§3.3, l. 368",
     "KiDS-bright only (and its hot-gas variant). Per-lens stellar-mass scatter: acts through bin assignment, not as an error on a bin's g_bar, so it also moves g_obs. The source also tested 0.29 dex and states its conclusions do not change.", None),
    ("stellar_mass_per_lens_gama", None, "dataset", "both", "not_given_by_source", None, None, None, "§3.2",
     "GAMA only. GAMA stellar masses are Taylor et al. 2011; this paper states no per-lens scatter for them.", None),
    ("stellar_mass_systematic", "K9", "dataset", "both", "given", 0.2, "dex", "as_released", "§3.3, l. 370; §5.2, l. 491",
     "All samples. The authors re-ran the analysis with log10(M★) ± 0.2 dex, moving lenses between bins, so the effect is not a shift of g_bar (D-021); shown by them as a band.", None),
    ("gama_normalisation", "K10", "dataset", "g_bar", "not_given_by_source", None, None, None, "§3.3, l. 370",
     "KiDS-bright masses were shifted by +0.056 dex to the GAMA mean; the uncertainty of that shift is not stated. KiDS-bright and its hot-gas variant.", None),
    ("cold_gas_relation", "K11", "dataset", "g_bar", "not_given_by_source", None, None, None, "§4.3, l. 409",
     "Boselli et al. 2014 relation; its scatter is not stated in this paper. All samples.", None),
    ("isolation_satellites", "K13", "dataset", "g_obs", "given", 0.30, "fraction of ΔΣ", "as_released", "§5.2, l. 489; App. A, l. 748",
     "One-sided upward: satellites give 'a ∼30% increase in ΔΣ' beyond 0.3 h70⁻¹ Mpc, from the source's MICE test. KiDS-bright rows below about 1e-13 m s⁻² are flagged source_quality_low (as v1); rows 1–8 are recorded, not plotted (D-103). The hot-gas rows' flags follow v1 and may under-flag them (known issue #168).", None),
    ("cosmology_h70", "K15", "dataset", "both", "not_given_by_source", None, None, None, "App. A, l. 746",
     "Distances 'using a flat ΛCDM cosmology, ignoring peculiar velocities'; units carry h70, and the Atlas uses h = 0.7 as the source. All samples.", None),
]


def terms_table():
    cols = {k: [] for k in ["term_id", "scale", "applies_to", "moves", "status", "size_value", "size_unit", "size_kind",
                            "covariance", "citation", "locator", "note", "in_error_columns"]}
    for tid, reading, scale, moves, status, sv, su, sk, loc, note, inerr in TERMS:
        cols["term_id"].append(tid)
        cols["scale"].append(scale)
        cols["applies_to"].append("*")
        cols["moves"].append(moves)
        cols["status"].append(status)
        cols["size_value"].append(sv)
        cols["size_unit"].append(su)
        cols["size_kind"].append(sk)
        cols["covariance"].append("not_published")
        cols["citation"].append("Brouwer et al. 2021, A&A 650, A113 (arXiv 2106.11677)")
        cols["locator"].append(f"{loc}; step A reading {reading}, docs/sources/uncertainty-readings.md §1" if reading
                               else f"{loc}; docs/sources/uncertainty-readings.md §1")
        cols["note"].append(note)
        cols["in_error_columns"].append(inerr)
    t = Table([
        col("term_id", cols["term_id"], ucd="meta.id;meta.main", description="Term identifier"),
        col("scale", cols["scale"], ucd="meta.code", description="point, system or dataset (§2a)"),
        col("applies_to", cols["applies_to"], ucd="meta.id", description="* (all rows); the note names the samples"),
        col("moves", cols["moves"], ucd="meta.code", description="Which side the term moves"),
        col("status", cols["status"], ucd="meta.code", description="given or not_given_by_source"),
        col("size_value", cols["size_value"], None, "stat.error", "Size as stated", True),
        col("size_unit", cols["size_unit"], ucd="meta.unit", description="Unit of size_value"),
        col("size_kind", cols["size_kind"], ucd="meta.code", description="one_sigma or as_released"),
        col("covariance", cols["covariance"], ucd="meta.code", description="not_published (K1's covariance is in tables/covariance.ecsv)"),
        col("citation", cols["citation"], ucd="meta.bib", description="Source"),
        col("locator", cols["locator"], ucd="meta.ref", description="Location in the source and in the step A reading"),
        col("note", cols["note"], ucd="meta.note", description="Note, including the samples the term applies to"),
        col("in_error_columns", cols["in_error_columns"], ucd="meta.code", description="no: the term is not in g_obs_err_* (§7a)"),
    ])
    t.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    return t


def main() -> int:
    members = check_and_extract()
    regenerate_reading()
    meas, obs, covt = build(members)
    terms = terms_table()
    (HERE / "tables").mkdir(exist_ok=True)
    meas.write(HERE / "tables/measurements.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    obs.write(HERE / "tables/observables.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    covt.write(HERE / "tables/covariance.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    terms.write(HERE / "tables/uncertainty_terms.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
    ki = json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    desc["x_known_issues"] = [k["url"] for k in ki]
    write_datapackage(HERE, desc, {"measurements": ("tables/measurements.ecsv", meas),
                                   "observables": ("tables/observables.ecsv", obs),
                                   "covariance": ("tables/covariance.ecsv", covt),
                                   "uncertainty_terms": ("tables/uncertainty_terms.ecsv", terms)})
    write_checksums(HERE)
    plotted = sum(1 for v in meas["plotted"] if v == "true")
    print(f"wrote {len(meas)} measurements ({plotted} plotted), {len(obs)} observables, {len(covt)} covariance entries, "
          f"{len(terms)} terms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
