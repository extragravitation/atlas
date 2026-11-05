"""Convert the accelerations released with Eckert et al. 2022 into X-COP v2 (data standard 2.5.1).

Usage: python data/packages/aeg-d-xcop/v2/convert.py

Method: the frozen tests REPRODUCTION.md (part A, data/frozen/xcop-v2-part-a.json) and
REPRODUCTION_PART_B.md (part B, data/frozen/xcop-v2-part-b.json), the frozen second reading in
reading/ (data/frozen/xcop-v2-reading.json), and decisions D-087, D-089 to D-092, D-096, D-105.

Inputs:
  - source/data_E22.tar.gz (fetched and hash-verified by aeg.fetch; never committed): the five
    gbar_gobs_<C>.fits files give every value, as released (part B rule 1);
  - the frozen reading files: error form, model form, D-096 outcome, confidence levels, cluster
    properties, hydrostatic statements and the central-galaxy systems come from them and from
    nowhere else. This file has no cluster-specific rule beyond what part B names;
  - result_part_a.json (published): the A7 ratios and A9 ratios;
  - REPRODUCTION.md §2 (frozen): Table 1 of Eckert et al. 2022 as transcribed there.

Writes tables/{measurements,observables,systems,uncertainty_terms}.ecsv, datapackage.json and
checksums.sha256. The tables were held back until publication (D-090 rule 5; part B rule 5) and are
committed since publication under D-106 (2026-11-05).

CONSENT GATE: this script prints counts and hashes only, never a row value, and its error messages
name rows by cluster and row number only (CI logs are public; part B rule 5).
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
import tarfile
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.table import MaskedColumn, Table
import astropy.units as u

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg.package import write_checksums, write_datapackage  # noqa: E402

DATASET, VERSION, STANDARD = "aeg-d-xcop", "v2", "2.5.1"
PID = f"{DATASET}/{VERSION}"
READING = HERE / "reading"
TAR = HERE / "source" / "data_E22.tar.gz"
FIVE = ["A644", "A1795", "A2029", "A2142", "A2319"]          # part A §1 file order
SEVEN = ["A85", "A1644", "A2255", "A3158", "A3266", "RXC1825", "ZW1215"]
EXCL_REASON = "stellar mass not in the source; g_bar bounded below by gas only; recorded under D-090"
EXCL_CITATION = "Eckert et al. 2022, A&A 662, A123 (arXiv 2205.01110v1), l. 103, 114, 402"
D092_T = ("The source's g_bar for this cluster could not be rebuilt from the gas and stellar profiles shared with it "
          "(it differs by up to 32 % in the centre; test A2). The values shown are the source's own. The question is with the authors.")
HSE_PREFIX = "Source statement on hydrostatic validity (part A §5; not an exclusion, part B rule 4)"
OBS_STEPS = "events;spectra;projected_t_and_density;deprojected_profiles;hydrostatic_mass;newtonian_g"
BAR_STEPS = "xray;mass;photometry;luminosity;structural_model;newtonian_g"
OBS_REF = ("the source computed g: non-parametric hydrostatic reconstruction evaluated at the radii of the data "
           "(E22 §3.4, l. 263); g_obs = G M_HSE(<r)/r² (l. 453)")
BAR_REF = ("the source computed g, including the central galaxy's dynamical mass-to-light ratio: "
           "G (M_gas + M★,BCG + M★,sat)(<r)/r² (E22 l. 456); ICL excluded (l. 410)")
METHOD = ("X-ray and SZ hydrostatic g_obs, non-parametric reconstruction, and g_bar from gas, central-galaxy and "
          "satellite masses, both as released by Eckert et al. 2022")
ASSUMPTIONS = "xcop_hse_equilibrium;xcop_spherical;xray_hse_bias=0"
COLS = ["RADIUS", "GBAR", "GBAR_ERR", "GOBS", "GOBS_ERR_LO", "GOBS_ERR_HI"]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fail(msg: str) -> None:
    raise SystemExit(f"convert.py ({PID}): {msg}")


def check_frozen() -> None:
    for rec in ("xcop-v2-part-a.json", "xcop-v2-part-b.json", "xcop-v2-reading.json"):
        d = json.loads((ROOT / "data/frozen" / rec).read_text(encoding="utf-8"))
        for rel, h in d["files"].items():
            if sha((ROOT / rel).read_bytes()) != h:
                fail(f"frozen file changed: {rel}")


def read_archive() -> dict[str, bytes]:
    src = {s["file"]: s for s in json.loads((HERE / "sources.json").read_text(encoding="utf-8"))["sources"]}
    data = TAR.read_bytes()
    if sha(data) != src["data_E22.tar.gz"]["sha256"]:
        fail("source/data_E22.tar.gz does not match sources.json")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for m in tf.getmembers():
            if m.isfile():
                files[m.name.lstrip("./")] = tf.extractfile(m).read()
    want = src["data_E22.tar.gz"]["members_sha256"]
    if set(files) != set(want):
        fail("archive member list differs from sources.json")
    for name, h in want.items():
        if sha(files[name]) != h:
            fail(f"member {name} does not match its recorded hash")
    return files


def gbar_gobs(b: bytes) -> list[dict]:
    with fits.open(io.BytesIO(b)) as h:
        hdu = h[1]
        names = [c.name for c in hdu.columns]
        if names != COLS:
            fail("unexpected gbar_gobs columns")
        units = [(c.unit or "").strip() for c in hdu.columns]
        if units[0] != "kpc" or any(x.replace(" ", "") not in ("m/s^2", "m/s**2", "ms-2") for x in units[1:]):
            fail("unexpected gbar_gobs units")
        # float32 in the file, widened to float64 exactly (the reading's canonical form)
        return [{c: float(np.float64(row[c])) for c in COLS} for row in hdu.data]


def table1() -> dict[str, dict]:
    """Eckert et al. 2022 Table 1 as transcribed in the frozen part A test, §2."""
    out = {}
    num = r"([0-9.]+) \(−([0-9.]+)/\+([0-9.]+)\)"
    pat = re.compile(rf"^\| ([A-Za-z0-9]+) \| ([0-9.]+) \| {num} \| {num} \| {num} \|$")
    for line in (HERE / "REPRODUCTION.md").read_text(encoding="utf-8").splitlines():
        m = pat.match(line.strip())
        if m:
            g = m.groups()
            out[g[0].upper()] = {"name": g[0], "z": float(g[1]),
                                 "r500": [float(x) for x in g[2:5]], "m500": [float(x) for x in g[5:8]],
                                 "m200": [float(x) for x in g[8:11]]}
    if set(out) != set(FIVE + SEVEN):
        fail(f"part A §2 Table 1 parse found {len(out)} clusters, expected 12")
    return out


def registry_ids() -> dict[str, str]:
    rows = list(csv.DictReader((ROOT / "data/registry/systems.csv").open(encoding="utf-8")))
    ids = {r["primary_name"].upper(): r["system_id"] for r in rows if r["first_dataset"] == f"{DATASET}/v1"}
    if set(ids) != set(FIVE + SEVEN):
        fail("registry does not hold the twelve X-COP clusters")
    return ids


def read_reading() -> dict:
    R = {}
    ef = (READING / "error_form.md").read_text(encoding="utf-8")
    R["gobs_form"] = ("magnitudes" if "**GOBS_ERR_LO and GOBS_ERR_HI are error magnitudes**" in ef else
                      "bounds" if "**GOBS_ERR_LO and GOBS_ERR_HI are bounds**" in ef else "undetermined")
    R["gbar_form"] = "magnitudes" if "**GBAR_ERR is an error magnitude**" in ef else "undetermined"
    mf = (READING / "model_form.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*`model_dependence` = `([a-z_]+)`\*\*", mf)
    if not m:
        fail("model_form.md states no model_dependence")
    R["model_dependence"] = m.group(1)
    bc = (READING / "bcg_extra_mass_systems.md").read_text(encoding="utf-8")
    m = re.search(r"`applies_to` = `([a-z0-9;\-]+)`", bc)
    R["bcg_extra_applies_to"] = m.group(1) if m and "**Outcome: decided" in bc else None
    lev = {r["column"]: r for r in csv.DictReader((READING / "err_levels.csv").open(encoding="utf-8"))}
    R["levels"] = {k: (lev[k]["value"] or None) for k in ("err_level", "err_level_status", "g_bar_err_level", "g_bar_err_level_status")}
    R["d096"] = list(csv.DictReader((READING / "d096.csv").open(encoding="utf-8")))
    R["props"] = {r["cluster"].upper(): r for r in csv.DictReader((READING / "properties.csv").open(encoding="utf-8"))}
    R["hse"] = list(csv.DictReader((READING / "hse_statements.csv").open(encoding="utf-8")))
    return R


NON_EXCLUSION = {"none", "no_exclusion_wording", "not_applicable_other_quantity", "not_applicable_other_systems"}
NON_CHANGE = {"none", "no_preference_between_released_values", "benchmark_named_no_alternative_released",
              "column_choice_fixed_by_test", "not_applicable_other_quantity"}


def col(name, data, unit=None, ucd=None, description="", kind="str"):
    data = list(data)
    if kind == "f8" or kind == "i8":
        mask = [x is None for x in data]
        arr = np.array([(0 if kind == "i8" else np.nan) if x is None else x for x in data], dtype=kind)
        c = MaskedColumn(arr, name=name, mask=mask, unit=unit, description=description)
    else:
        c = MaskedColumn([("" if x is None else str(x)) for x in data], name=name, description=description, dtype=str)
    c.meta["ucd"] = ucd
    return c


def main() -> int:
    check_frozen()
    R = read_reading()
    # D-096 (part B rule 1): no change unless the frozen reading names one; this converter implements none.
    for r in R["d096"]:
        if r["field"] == "excluded" and r["outcome"] not in NON_EXCLUSION:
            fail("the reading names an exclusion (rule 1); it goes to JvH before conversion")
        if r["field"] in ("preferred", "fiducial") and r["outcome"] not in NON_CHANGE:
            fail("the reading names a preferred or fiducial change (rule 1); it goes to JvH before conversion")
    if R["model_dependence"] not in ("none", "total_mass_form"):
        fail("model_form.md outcome not in the closed list")
    files = read_archive()
    T1 = table1()
    ids = registry_ids()
    res_a = json.loads((HERE / "result_part_a.json").read_text(encoding="utf-8"))
    issues = json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    lev = R["levels"]
    acc = u.m / u.s ** 2

    # A2319's statements (item 9): every statement marked in_a2319_notes = yes, in file order
    a2319 = [h for h in sorted(R["hse"], key=lambda h: int(h["order"])) if h["in_a2319_notes"] == "yes"]
    a2319_notes = [f"{HSE_PREFIX}: \"{h['quote']}\" ({h['source'].split(',')[0]}, {h['file']} l. {h['line']})" for h in a2319]

    M: list[dict] = []
    O: list[dict] = []
    n = 0
    for name in FIVE:
        member = f"{name}/gbar_gobs_{name}.fits"
        rows = gbar_gobs(files[member])
        sid = ids[name]
        a9 = res_a["A9"][name]["ratio_to_ghizzardi"]
        p = R["props"][name]
        for k, row in enumerate(rows, start=1):
            n += 1
            mid, oo, ob = f"{PID}/m{n:06d}", f"{PID}/o{2 * n - 1:06d}", f"{PID}/o{2 * n:06d}"
            g_obs, g_bar = row["GOBS"], row["GBAR"]
            flags, notes = [], []
            # item 5: error form from the frozen reading
            if R["gobs_form"] == "magnitudes":
                eo_lo, eo_hi = row["GOBS_ERR_LO"], row["GOBS_ERR_HI"]
            elif R["gobs_form"] == "bounds":
                eo_lo, eo_hi = g_obs - row["GOBS_ERR_LO"], row["GOBS_ERR_HI"] - g_obs
            else:
                eo_lo = eo_hi = None
            eb = row["GBAR_ERR"] if R["gbar_form"] == "magnitudes" else None
            if eo_lo is None or eb is None:
                flags.append("no_uncertainty")
            ki = [x for x in issues if name in x.get("clusters", []) and x.get("rows", True)]
            for x in ki:
                if x.get("flag"):
                    flags.append(x["flag"])
            if any(x["issue"] == 136 for x in ki):
                notes.append(D092_T)
            if name == "A2319":
                notes += a2319_notes
            notes.append(f"stellar projection: undetermined (part A, A6); stellar normalisation against Ghizzardi et al. 2021: "
                         f"{a9:.2f} (part A, A9)")
            M.append({
                "measurement_id": mid, "system_id": sid, "kind": "profile_point", "channel": "dynamics",
                "method_class": "hydrostatic", "method": METHOD, "measured_quantity": "g_obs",
                "r_kpc": row["RADIUS"], "r_kind": "3d",
                "g_obs": g_obs, "g_obs_err_lo": eo_lo, "g_obs_err_hi": eo_hi,
                "g_bar": g_bar, "g_bar_err_lo": eb, "g_bar_err_hi": eb,
                "g_bar_stars": None, "g_bar_gas_cold": None, "g_bar_gas_hot": None, "limit": "none",
                "stars_status": "not_separable", "gas_cold_status": "absent", "gas_hot_status": "not_separable",
                "observed_from": oo, "baryonic_from": ob, "model_dependence": R["model_dependence"], "evidence_tier": 1,
                "role": "default", "alternative_of": None, "plotted": "true", "not_plotted_reason": None,
                "assumptions": ASSUMPTIONS, "adjustable": "xray_hse_bias",
                "flags": ";".join(sorted(set(flags))), "known_issues": ";".join(f"#{x['issue']}" for x in ki),
                "source_ref": f"data_E22.tar.gz:{member}:row {k}", "notes": " | ".join(notes),
                "err_level": float(lev["err_level"]) if lev["err_level"] else None, "err_level_status": lev["err_level_status"],
                "g_bar_err_level": float(lev["g_bar_err_level"]) if lev["g_bar_err_level"] else None,
                "g_bar_err_level_status": lev["g_bar_err_level_status"],
                "g_obs_err_point_lo": eo_lo, "g_obs_err_point_hi": eo_hi, "g_bar_err_point_lo": None, "g_bar_err_point_hi": None,
                "x_xcop_centroid_w": float(p["w_printed"]), "x_xcop_centroid_w_err": float(p["w_err_printed"]),
            })
            common = {"system_id": sid, "quantity": "acceleration_released", "unit": "m / s2", "band": None, "limit": "none",
                      "r_kpc": row["RADIUS"], "r_kind": "3d", "evidence_tier": 1}
            O.append({**common, "observable_id": oo, "side": "observed", "value": g_obs, "err_lo": eo_lo, "err_hi": eo_hi,
                      "steps": OBS_STEPS, "source_ref": f"data_E22.tar.gz:{member}:row {k}, GOBS; {OBS_REF}",
                      "err_level": M[-1]["err_level"], "err_level_status": lev["err_level_status"]})
            O.append({**common, "observable_id": ob, "side": "baryonic", "value": g_bar, "err_lo": eb, "err_hi": eb,
                      "steps": BAR_STEPS, "source_ref": f"data_E22.tar.gz:{member}:row {k}, GBAR; {BAR_REF}",
                      "err_level": M[-1]["g_bar_err_level"], "err_level_status": lev["g_bar_err_level_status"]})
    # known issues: measurement lists must match their clusters (as v1)
    for x in issues:
        want = [m["measurement_id"] for m in M if any(ids[c.upper()] == m["system_id"] for c in x.get("clusters", []))] \
            if x.get("rows", True) else []
        if want != x.get("measurements", []):
            fail(f"known_issues.json issue #{x['issue']}: measurement list does not match its clusters")

    mdesc = {
        "measurement_id": ("meta.id;meta.main", "Permanent measurement identifier"),
        "system_id": ("meta.id", "Atlas system identifier"),
        "kind": ("meta.code", "Kind of measurement"), "channel": ("meta.code", "Observational channel"),
        "method_class": ("meta.code.class", "Class of method"), "method": ("meta.note", "Method"),
        "measured_quantity": ("meta.code", "Quantity measured (D-029)"),
        "r_kind": ("meta.code", "Radius is three-dimensional"), "limit": ("meta.code", "Whether g_obs is a limit"),
        "stars_status": ("meta.code", "not_separable: the source's stars are inside the released g_bar total (part B item 2)"),
        "gas_cold_status": ("meta.code", "Cold gas not included by the source (as v1)"),
        "gas_hot_status": ("meta.code", "not_separable: the source's hot gas is inside the released g_bar total (part B item 2)"),
        "observed_from": ("meta.ref", "Observable used on the observed side"),
        "baryonic_from": ("meta.ref", "Observable used on the baryonic side"),
        "model_dependence": ("meta.code", "From reading/model_form.md (D-087; part B rule 3)"),
        "evidence_tier": ("meta.code.qual", "Evidence tier (D-035)"),
        "role": ("meta.code", "Default value for the system, or an alternative"),
        "alternative_of": ("meta.ref", "The default measurement this is an alternative to"),
        "plotted": ("meta.code", "Shown in default views"), "not_plotted_reason": ("meta.note", "Why not plotted (closed list)"),
        "assumptions": ("meta.note", "Named assumptions affecting this row (part B item 7)"),
        "adjustable": ("meta.note", "Assumptions whose sliders can change this row"),
        "flags": ("meta.code", "Atlas flags"), "known_issues": ("meta.ref", "Open known issues affecting this row (GitHub issue numbers)"),
        "source_ref": ("meta.ref", "Source file and row"), "notes": ("meta.note", "Notes (part B item 9)"),
        "err_level_status": ("meta.code", "stated or not_given_by_source (reading/err_levels.csv)"),
        "g_bar_err_level_status": ("meta.code", "stated or not_given_by_source (reading/err_levels.csv)"),
    }
    fdesc = {
        "r_kpc": (u.kpc, "phys.size.radius", "Three-dimensional radius, RADIUS as released"),
        "g_obs": (acc, "phys.acceleration", "Observed acceleration, GOBS as released (the source's non-parametric hydrostatic g_obs)"),
        "g_obs_err_lo": (acc, "stat.error;phys.acceleration", "GOBS_ERR_LO, read as an error magnitude (reading/error_form.md; part B item 5); level not given by the source"),
        "g_obs_err_hi": (acc, "stat.error;phys.acceleration", "GOBS_ERR_HI, read as an error magnitude (reading/error_form.md; part B item 5); level not given by the source"),
        "g_bar": (acc, "phys.acceleration", "Baryonic acceleration, GBAR as released (gas, central galaxy and satellites, as one total)"),
        "g_bar_err_lo": (acc, "stat.error;phys.acceleration", "GBAR_ERR, an error magnitude (reading/error_form.md); mixes point- and system-scale parts"),
        "g_bar_err_hi": (acc, "stat.error;phys.acceleration", "GBAR_ERR, an error magnitude (reading/error_form.md); mixes point- and system-scale parts"),
        "g_bar_stars": (acc, "phys.acceleration", "Empty: the source releases g_bar as a total (part B item 2)"),
        "g_bar_gas_cold": (acc, "phys.acceleration", "Empty: the source releases g_bar as a total (part B item 2)"),
        "g_bar_gas_hot": (acc, "phys.acceleration", "Empty: the source releases g_bar as a total (part B item 2)"),
        "err_level": (None, "stat.value", "Confidence level of g_obs_err_lo/hi; empty: not given by the source (reading/err_levels.csv)"),
        "g_bar_err_level": (None, "stat.value", "Confidence level of g_bar_err_lo/hi; empty: not given by the source (reading/err_levels.csv)"),
        "g_obs_err_point_lo": (acc, "stat.error;phys.acceleration", "Point-scale part of the g_obs error: equal to g_obs_err_lo, the per-radius posterior (part B item 5)"),
        "g_obs_err_point_hi": (acc, "stat.error;phys.acceleration", "Point-scale part of the g_obs error: equal to g_obs_err_hi, the per-radius posterior (part B item 5)"),
        "g_bar_err_point_lo": (acc, "stat.error;phys.acceleration", "Empty: GBAR_ERR mixes point-scale gas errors with the central galaxy's system-scale mass-to-light error; the source gives no point-scale part (term g_bar_point)"),
        "g_bar_err_point_hi": (acc, "stat.error;phys.acceleration", "Empty: GBAR_ERR mixes point-scale gas errors with the central galaxy's system-scale mass-to-light error; the source gives no point-scale part (term g_bar_point)"),
        "x_xcop_centroid_w": (None, "src.morph.param", "Centroid shift w of the cluster, Paper II Table 2 (tab2.tex), as printed in its stated unit of 10⁻³ (as printed); repeated on every row (part A §5); empty never"),
        "x_xcop_centroid_w_err": (None, "stat.error", "Printed ± error of x_xcop_centroid_w, in 10⁻³ (as printed); level not given by the source"),
        "evidence_tier": (None, None, None),
    }
    order = list(M[0].keys())
    mcols = []
    for c in order:
        vals = [m[c] for m in M]
        if c == "evidence_tier":
            mcols.append(col(c, vals, None, mdesc[c][0], mdesc[c][1], "i8"))
        elif c in fdesc:
            un, ucd, de = fdesc[c]
            mcols.append(col(c, vals, un, ucd, de, "f8"))
        else:
            mcols.append(col(c, vals, None, mdesc[c][0], mdesc[c][1]))
    meas = Table(mcols)
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    odesc = {"observable_id": ("meta.id;meta.main", "Permanent observable identifier", None, "str"),
             "system_id": ("meta.id", "Atlas system identifier", None, "str"),
             "side": ("meta.code", "Observed or baryonic side", None, "str"),
             "quantity": ("meta.code", "acceleration_released: the source computed g (D-095)", None, "str"),
             "value": ("meta.number", "Value as released (GOBS or GBAR)", None, "f8"),
             "err_lo": ("stat.error", "Lower error as released (GOBS_ERR_LO or GBAR_ERR), an error magnitude", None, "f8"),
             "err_hi": ("stat.error", "Upper error as released (GOBS_ERR_HI or GBAR_ERR), an error magnitude", None, "f8"),
             "unit": ("meta.unit", "Unit of value", None, "str"), "band": ("instr.bandpass", "Photometric band (none)", None, "str"),
             "limit": ("meta.code", "Whether the value is a limit", None, "str"),
             "r_kpc": ("phys.size.radius", "Three-dimensional radius, RADIUS as released", u.kpc, "f8"),
             "r_kind": ("meta.code", "Radius kind", None, "str"),
             "evidence_tier": ("meta.code.qual", "Evidence tier (D-035)", None, "i8"),
             "steps": ("meta.note", "Processing ladder from data to this quantity (§4b); every step is the source's", None, "str"),
             "source_ref": ("meta.ref", "Source file and row, and what the source computed", None, "str"),
             "err_level": ("stat.value", "Confidence level of err_lo/err_hi; empty: not given by the source (reading/err_levels.csv)", None, "f8"),
             "err_level_status": ("meta.code", "stated or not_given_by_source", None, "str")}
    ocols = ["observable_id", "system_id", "side", "quantity", "value", "err_lo", "err_hi", "unit", "band", "limit",
             "r_kpc", "r_kind", "steps", "evidence_tier", "source_ref", "err_level", "err_level_status"]
    obs_t = Table([col(c, [o[c] for o in O], odesc[c][2], odesc[c][0], odesc[c][1], odesc[c][3]) for c in ocols])
    obs_t.meta = dict(meas.meta)

    # systems: all twelve (part B item 8)
    S = []
    a7 = res_a["A7"]
    for key in ["A85", "A644", "A1644", "A1795", "A2029", "A2142", "A2255", "A2319", "A3158", "A3266", "RXC1825", "ZW1215"]:
        t, p = T1[key], R["props"][key]
        five = key in FIVE
        rat = [a7[key][k] for k in ("GP/EIN", "GP/Table1", "EIN/Table1")] if five else [None, None, None]
        S.append({
            "system_id": ids[key], "name_in_source": t["name"], "class_in_source": "Galaxy cluster (X-COP sample)",
            "taxonomy_kind": "A9", "kind_label": "galaxy cluster", "host": None, "distance_mpc": None,
            "distance_method": None, "distance_kinematic": "false", "distance_ref": None,
            "redshift": t["z"], "redshift_err": None, "metallicity_feh": None,
            "properties": json.dumps({
                "r500_tot_kpc": t["r500"][0], "r500_tot_err_lo_kpc": t["r500"][1], "r500_tot_err_hi_kpc": t["r500"][2],
                "m500_tot_1e14_solMass": t["m500"][0], "m500_tot_err_lo_1e14_solMass": t["m500"][1], "m500_tot_err_hi_1e14_solMass": t["m500"][2],
                "m200_tot_1e14_solMass": t["m200"][0], "m200_tot_err_lo_1e14_solMass": t["m200"][1], "m200_tot_err_hi_1e14_solMass": t["m200"][2],
                "ref": "Eckert et al. 2022 Table 1 (tab:master, l. 324–335; NFW fits, errors as printed), as transcribed in REPRODUCTION.md §2",
            }, ensure_ascii=False, separators=(",", ":")),
            "x_xcop_alpha_nt_r500": float(p["alpha_nt_r500"]), "x_xcop_alpha_nt_r500_err_lo": float(p["alpha_nt_r500_err_lo"]),
            "x_xcop_alpha_nt_r500_err_hi": float(p["alpha_nt_r500_err_hi"]),
            "x_xcop_alpha_nt_r200": float(p["alpha_nt_r200"]), "x_xcop_alpha_nt_r200_err_lo": float(p["alpha_nt_r200_err_lo"]),
            "x_xcop_alpha_nt_r200_err_hi": float(p["alpha_nt_r200_err_hi"]),
            "x_xcop_centroid_w": float(p["w_printed"]), "x_xcop_centroid_w_err": float(p["w_err_printed"]),
            "x_xcop_mm_gp_ein": rat[0], "x_xcop_mm_gp_nfw": rat[1], "x_xcop_mm_ein_nfw": rat[2],
            "x_xcop_mass_model_frac": round(max(abs(r - 1) for r in rat), 4) if five else None,
            "x_xcop_status": "plotted" if five else "recorded_not_plotted",
        })
    units = {R["props"][k]["alpha_unit_status"] for k in R["props"]}
    if units != {"inferred_percent"}:
        fail("alpha unit status is not inferred_percent for every cluster; item 6's other branch is not implemented")
    AU = "as printed (per cent inferred, not stated)"
    sdesc = {
        "system_id": (None, "meta.id;meta.main", "Atlas system identifier", "str"),
        "name_in_source": (None, "meta.id", "Cluster name as in Eckert et al. 2022 Table 1", "str"),
        "class_in_source": (None, "src.class", "Class as the source gives it", "str"),
        "taxonomy_kind": (None, "meta.code", "Taxonomy kind (A0–A10)", "str"),
        "kind_label": (None, "meta.note", "Kind label", "str"),
        "host": (None, "meta.id", "Host (none)", "str"),
        "distance_mpc": (u.Mpc, "pos.distance", "Not given; redshift is given (D-033)", "f8"),
        "distance_method": (None, "meta.note", "Distance method (none)", "str"),
        "distance_kinematic": (None, "meta.code", "Distance derived from kinematics", "str"),
        "distance_ref": (None, "meta.ref", "Distance source (none)", "str"),
        "redshift": (None, "src.redshift", "Redshift, Eckert et al. 2022 Table 1 (part A §2)", "f8"),
        "redshift_err": (None, "stat.error;src.redshift", "Not given", "f8"),
        "metallicity_feh": (None, "phys.abund.Fe", "Not given", "f8"),
        "properties": (None, "meta.note", "Source-given properties only: Table 1's R500,TOT, M500,TOT and M200,TOT (JSON; units in key names)", "str"),
        "x_xcop_alpha_nt_r500": (None, "phys.pressure;arith.ratio", f"Non-thermal pressure fraction at R500, Ettori & Eckert 2022 tab:gamma_beta, last column (the present work, l. 274); unit {AU}; size of term nonthermal_pressure", "f8"),
        "x_xcop_alpha_nt_r500_err_lo": (None, "stat.error", f"Printed lower (subscript) error of x_xcop_alpha_nt_r500, sign as printed (anomalous signs not repaired; reading/resolutions.md); 1 sigma (l. 276); unit {AU}", "f8"),
        "x_xcop_alpha_nt_r500_err_hi": (None, "stat.error", f"Printed upper (superscript) error of x_xcop_alpha_nt_r500, sign as printed; 1 sigma (l. 276); unit {AU}", "f8"),
        "x_xcop_alpha_nt_r200": (None, "phys.pressure;arith.ratio", f"Non-thermal pressure fraction at R200, as x_xcop_alpha_nt_r500; unit {AU}; term nonthermal_pressure", "f8"),
        "x_xcop_alpha_nt_r200_err_lo": (None, "stat.error", f"Printed lower error of x_xcop_alpha_nt_r200, sign as printed (not repaired); unit {AU}", "f8"),
        "x_xcop_alpha_nt_r200_err_hi": (None, "stat.error", f"Printed upper error of x_xcop_alpha_nt_r200, sign as printed; unit {AU}", "f8"),
        "x_xcop_centroid_w": (None, "src.morph.param", "Centroid shift w, Paper II Table 2 (tab2.tex), in 10⁻³ (as printed); continuous, never a label (part A §5)", "f8"),
        "x_xcop_centroid_w_err": (None, "stat.error", "Printed ± error of x_xcop_centroid_w, in 10⁻³ (as printed)", "f8"),
        "x_xcop_mm_gp_ein": (None, "phys.mass;arith.ratio", "Part A A7: non-parametric / Einasto mass at R500 from R3 (result_part_a.json, stored precision); empty for the seven clusters without rows; term mass_model_choice", "f8"),
        "x_xcop_mm_gp_nfw": (None, "phys.mass;arith.ratio", "Part A A7: non-parametric mass at R500 from R3 / Table 1 NFW M500 at Table 1's R500; empty for the seven; term mass_model_choice", "f8"),
        "x_xcop_mm_ein_nfw": (None, "phys.mass;arith.ratio", "Part A A7: Einasto mass at R500 from R3 / Table 1 NFW M500 at Table 1's R500; empty for the seven; term mass_model_choice", "f8"),
        "x_xcop_mass_model_frac": (None, "stat.error;arith.ratio", "Size of term mass_model_choice: round(max |r − 1|, 4) over the three x_xcop_mm_* ratios (part B item 7; D-105 O2); Atlas-computed; empty for the seven", "f8"),
        "x_xcop_status": (None, "meta.code", "Atlas state: plotted (the five with rows) or recorded_not_plotted (the seven without stellar data; part B rule 2)", "str"),
    }
    sys_t = Table([col(c, [s[c] for s in S], sdesc[c][0], sdesc[c][1], sdesc[c][2], sdesc[c][3]) for c in sdesc])
    sys_t.meta = dict(meas.meta)

    terms = build_terms(R, ids)

    # exclusion register (part B rule 2): the seven rows must be present; this script does not write the file
    reg = list(csv.DictReader((ROOT / "data/registry/excluded.csv").open(encoding="utf-8")))
    mine = sorted(r["system"] for r in reg if r["dataset"] == PID)
    if mine != sorted(ids[c] for c in SEVEN) or any(
            r["reason"] != EXCL_REASON or r["citation"] != EXCL_CITATION for r in reg if r["dataset"] == PID):
        fail("data/registry/excluded.csv does not hold the seven rows of part B rule 2 exactly")

    (HERE / "tables").mkdir(exist_ok=True)
    for nm, tab in (("measurements", meas), ("observables", obs_t), ("systems", sys_t), ("uncertainty_terms", terms)):
        tab.write(HERE / f"tables/{nm}.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
    desc["x_known_issues"] = [x["url"] for x in issues]
    write_datapackage(HERE, desc, {"measurements": ("tables/measurements.ecsv", meas),
                                   "observables": ("tables/observables.ecsv", obs_t),
                                   "systems": ("tables/systems.ecsv", sys_t),
                                   "uncertainty_terms": ("tables/uncertainty_terms.ecsv", terms)})
    write_checksums(HERE)
    print(f"{PID}: wrote {len(meas)} measurements ({sum(m['plotted'] == 'true' for m in M)} plotted), {len(obs_t)} observables, "
          f"{len(sys_t)} systems, {len(terms)} terms; no values printed")
    return 0


def build_terms(R, ids) -> Table:
    keys = ["term_id", "scale", "applies_to", "moves", "status", "size_value", "size_lo", "size_hi", "size_unit",
            "size_column", "size_kind", "assumption_id", "correlated_with", "covariance", "citation", "locator", "note",
            "in_error_columns"]
    t = {k: [] for k in keys}
    five = ";".join(ids[c] for c in FIVE)
    four = ";".join(ids[c] for c in FIVE if c != "A2319")

    def term(**kw):
        kw.setdefault("covariance", "not_published")
        for k in keys:
            t[k].append(kw.get(k))

    E22 = "Eckert et al. 2022, A&A 662, A123 (arXiv 2205.01110v1), hydromass.tex"
    PAPER2 = "Eckert et al. 2022b, A&A 666, A41 (arXiv 2205.01123v1), einasto.tex"
    EE22 = "Ettori & Eckert 2022 (arXiv 2112.07554v1), p_nt_b_aa.tex"
    L20 = "Loubser et al. 2020 (arXiv 2006.05706v1), BCG_v3_withoutBold.tex"
    G21 = "Ghizzardi et al. 2021 (arXiv 2007.01084v1), xcop-metallicity.tex"
    PA = "Part A result: REPRODUCTION_RESULT_PART_A.md and result_part_a.json (A7)"
    SAME = "Same programme, not independent."
    bcg_to = R["bcg_extra_applies_to"] or five

    term(term_id="radial_covariance", scale="point", applies_to="*", moves="g_obs", status="not_given_by_source",
         citation=E22, locator="l. 91, 97 (E1, E2)",
         note="The SZ covariance is \"accounted for and propagated\" (E22 l. 91, 97), but no covariance between radii is released")
    term(term_id="g_bar_point", scale="point", applies_to="*", moves="g_bar", status="not_given_by_source",
         citation=E22, locator="l. 111 (E18)",
         note="Part B item 5: GBAR_ERR mixes point-scale gas errors with the central galaxy's mass-to-light error, which is \"constant with radius\"; the source gives no point-scale part")
    term(term_id="np_smoothing", scale="point", applies_to="*", moves="g_obs", status="not_given_by_source",
         citation=E22, locator="l. 235 (E14)",
         note="\"fluctuations on scales smaller than the bin size are suppressed\" (E22 l. 235)")
    term(term_id="reconstruction_bias", scale="dataset", applies_to=five, moves="g_obs", status="given", size_value=0.05,
         size_unit="fraction", size_kind="upper_bound", citation=E22, locator="l. 309, §3.6 (E12)",
         note="\"The nonparametric technique follows the true profile with minimal bias (<5\\%)\" (E22 l. 309), from the source's mock test of its own pipeline (§3.6) on a cluster built to match X-COP's data, which counts as stated for the sample's method (part B item 7; unlike the lens test, where a source's figure from its own models went to the note). NFW \"at most 3\\%\" (l. 309, l. 311) and Einasto \"about 6\\%\" (l. 309)")
    term(term_id="hse_bias", scale="dataset", applies_to=four, moves="g_obs", status="given", size_value=0.10,
         size_unit="fraction", size_kind="upper_bound", assumption_id="xray_hse_bias", citation=E22, locator="l. 502 (E5); l. 539; l. 373",
         note="Valid for r ≤ R500 only. E22 l. 502, two sentences: (1) \"We find similar results in this analysis, as described in Sect. \\ref{sec:fbar}, where we can see that, with the exception of a single system that is known to be strongly biased \\citep[A2319;][]{ghirardini18}, the measured baryon fractions agree with the expectations at $R_{500}$ and slightly exceed the cosmic baryon fraction beyond this point, indicating a mild level of hydrostatic bias.\" (2) \"Since the relative level of nonthermal pressure support is expected to increase with distance to the cluster core \\citep[e.g.,][]{nelson14}, we conclude that our measurements are mildly biased ($<10\\%$) out to $R_{500}$.\" Then: \"The HSE assumption is likely to be a poorer approximation beyond this point.\" Restricting the bound to the four clusters other than A2319 is the Atlas's reading of l. 502: the A2319 exception qualifies the baryon-fraction evidence in sentence (1), and the conclusion in sentence (2) names no exception. Which R500: l. 502 does not define it and the reading found no defining sentence (reading/hse_statements.csv), so Table 1's R500,TOT is used, an inference. Other figures in l. 502: \"X-COP hydrostatic masses are 10-15\\% lower than weak lensing estimates\"; Eckert 2019's \"7\\% at $R_{500}$, 10\\% at $R_{200}$\"; simulations \"$5-30\\%$ at $R_{500}$\". Beyond R500 the source gives \"a mild contribution of nonthermal pressure ($10-20\\%$) at $R_{200}$\" (l. 539), a pressure fraction, not a size. \"although the validity of the HSE assumption at large radii is unclear\" (l. 373; E30). One-sided: hydrostatic g_obs is biased low. Never applied as a correction")
    term(term_id="hse_bias_a2319", scale="dataset", applies_to=ids["A2319"], moves="g_obs", status="not_given_by_source",
         assumption_id="xray_hse_bias", citation=f"{E22}; {PAPER2}", locator="E22 l. 435, l. 502; Paper II l. 80 (E7)",
         note="\"a single system that is known to be strongly biased \\citep[A2319;][]{ghirardini18}\" (E22 l. 502); the statements in reading/hse_statements.csv, on every A2319 row. No size is stated for A2319")
    term(term_id="nonthermal_pressure", scale="system", applies_to="*", moves="g_obs", status="given_by_other_source",
         size_column="x_xcop_alpha_nt_r500", size_unit="as printed (per cent inferred, not stated)", size_kind="as_released",
         citation=EE22, locator="tab:gamma_beta, last column (l. 274); errors l. 276; l. 182; l. 377",
         note="Non-thermal pressure fraction at R500 in x_xcop_alpha_nt_r500; the R200 value in x_xcop_alpha_nt_r200; printed errors in the _err_lo/_err_hi columns, \"at $1 \\sigma$ c.l.\" (l. 276), signs as printed. The unit is as printed: per cent inferred from the magnitudes, not stated (reading/properties.csv). " + SAME + " Computed from the 2019 thermal-only masses (l. 182). Median trend \"$b(0.1 R_{500}) \\approx 0.5 b(R_{500})$\" (l. 377). Overlaps hse_bias; the two are not added. Never applied as a correction (§3c)")
    term(term_id="gas_inhomogeneity", scale="dataset", applies_to=five, moves="g_obs", status="given", size_value=0.10,
         size_unit="fraction", size_kind="upper_bound", citation=E22, locator="l. 504 (E8)",
         note="\"the impact of gas inhomogeneities is small ($<10\\%$)\" (E22 l. 504). Temperature inhomogeneities \"$\\sim10\\%$\" (l. 311, citing other work). Would also move the gas mass, and so g_bar; that effect is not stated")
    term(term_id="xmm_calibration", scale="dataset", applies_to=five, moves="g_obs", status="not_given_by_source",
         citation=E22, locator="l. 311, l. 506 (E9)",
         note="The size is cited from other work: \"effective area calibration (15\\%)\" (E22 l. 311, citing Schellenberger 2015); \"reaches $\\sim20\\%$ for 10 keV plasma\" (l. 506). Conditional and one-sided: \"If the \\emph{Chandra} temperatures are correct, our masses at fixed radii would be underestimated by a similar amount\" (l. 506); \"mostly affects the regions located inside $0.5 R_{500}$\" (l. 506)")
    term(term_id="mass_model_choice", scale="system", applies_to="*", moves="g_obs", status="given",
         size_column="x_xcop_mass_model_frac", size_unit="fraction", size_kind="as_released", citation=f"{PA}; {E22}",
         locator="part A A7 (l. 202 of the part A test); E22 l. 373",
         note="The one Atlas-computed given size (part B item 7; D-105 O2). Per cluster, the largest |ratio − 1| across non-parametric/Einasto (R500 from R3), non-parametric/NFW and Einasto/NFW (NFW = Table 1 M500 at Table 1's R500), from result_part_a.json, in x_xcop_mm_*, rounded to 4 decimals. The max rule was fixed after part A's ratios were published, so it is not blind; all three pairs are forced by part A's frozen text, and the maximum is the conservative envelope over them. An equally conventional alternative, half the spread of the three masses, would give roughly half the size. The NFW pairs compare masses at Table 1's R500 with masses at R500 from R3, so the size partly reflects the R500 definition as well as the model choice, and it is applied as a fractional g_obs size at every radius. E22's sample statement: methods \"within 3\\%\" in median and NFW against NP \"less than 10\\%\" (l. 373). Empty for the seven clusters without rows. Never applied as a correction")
    term(term_id="cosmology", scale="dataset", applies_to="*", moves="both", status="not_given_by_source",
         citation=E22, locator="l. 56; §3.2 item 3 of docs/sources/uncertainty-readings.md",
         note="E22 adopts H0 = 67.8, Ω_m = 0.308 (l. 56); its central-galaxy and satellite sources assume H0 = 73 and 70, and harmonisation is not stated. No alternative is tested by the source; the distance dependence is not computed in v2")
    term(term_id="gas_density_conversion", scale="dataset", applies_to=five, moves="g_bar", status="not_given_by_source",
         citation=E22, locator="§3.1 of docs/sources/uncertainty-readings.md",
         note="The conversion from X-ray emissivity to gas density is not stated")
    term(term_id="bcg_ml", scale="system", applies_to="*", moves="g_bar", status="not_given_by_source",
         citation=E22, locator="l. 111 (E18)",
         note="Dynamical mass-to-light ratio; its error is dominated by the weak-lensing mass and \"constant with radius\" (E22 l. 111). Photometry \"$< 0.25$ mag arcsec$^{-2}$\" and kinematics \"$\\pm4.7$ per cent\" are inputs, not the size of this term")
    term(term_id="bcg_ml_extra_mass_model", scale="dataset", applies_to=bcg_to, moves="g_bar", status="given", size_value=0.083,
         size_unit="fraction", size_kind="as_released", citation=f"{E22}; {L20}", locator="E22 l. 109; reading/bcg_extra_mass_systems.md (E19, reader A)",
         note="Including an extra mass component in the central-galaxy dynamical models lowers the fitted mass-to-light ratio by \"8.3 $\\pm$ 2.9 per cent on average\" (E22 l. 109, which names the component \"a DM mass component\"). The second reading decided which central galaxies this describes (reading/bcg_extra_mass_systems.md)")
    term(term_id="bcg_jam_geometry", scale="dataset", applies_to=five, moves="g_bar", status="given_by_other_source", size_value=0.15,
         size_unit="fraction", size_kind="upper_bound", citation=L20, locator="l. 547 (E20)",
         note="\"changing our cylindrically-aligned JAM models to spherically-aligned JAM models, results in the best-fitting $\\Upsilon_{\\star \\rm DYN}$ parameters changing by up to $\\sim$ 15 per cent\" (Loubser et al. 2020, l. 547). " + SAME)
    term(term_id="bcg_sersic_extrapolation", scale="system", applies_to="*", moves="g_bar", status="not_given_by_source",
         citation=E22, locator="l. 404 (E21)",
         note="Measured \"only within a limited radial range out to $\\sim50$ kpc\", then a Sérsic form (E22 l. 404)")
    term(term_id="satellite_cosmic_variance", scale="system", applies_to="*", moves="g_bar", status="not_given_by_source",
         citation=f"{E22}; {G21}", locator="E22 l. 116; Ghizzardi l. 705 (reader A's E22)",
         note="Estimated with Moster et al. 2011 (E22 l. 116); shown separately by Ghizzardi (l. 705); no size stated in E22")
    term(term_id="satellite_flux", scale="system", applies_to="*", moves="g_bar", status="not_given_by_source",
         citation=G21, locator="l. 712 (E23)", note="Bootstrap of the fluxes (Ghizzardi l. 712); no size stated")
    term(term_id="satellite_gnfw_smoothing", scale="system", applies_to="*", moves="g_bar", status="not_given_by_source",
         citation=E22, locator="l. 408 (E24)",
         note="The profiles are \"quite noisy and not smooth\" and fitted beyond 100 kpc with a gNFW of fixed shape (E22 l. 408); which parameter set is not stated")
    term(term_id="satellite_projection", scale="system", applies_to="*", moves="g_bar", status="not_given_by_source",
         citation=f"{G21}; {PA}", locator="Ghizzardi l. 715; part A A6, A9 (E25); #124",
         note="Whether the satellite profile was deprojected is not stated (#124). Ghizzardi: \"75$\\%$ of the mass obtained integrating along the line of sight lies within the sphere with radius $R_{500}$\" (l. 715). Part A A6: undetermined; A9: 1.86–2.42 against Ghizzardi's spherical masses. Stated on every row's notes")
    term(term_id="satellite_mass_systematic", scale="dataset", applies_to=five, moves="g_bar", status="given_by_other_source",
         size_value=0.60, size_unit="fraction", size_kind="upper_bound", citation=G21, locator="l. 923 (E26, reader A)",
         note="\"Although we lack a clear understanding for the origin of different estimates of $M_{\\rm star}$, our comparison shows that we may be underestimating stellar masses by as much as 60\\%\" (Ghizzardi et al. 2021, l. 923). " + SAME + " Stated for Ghizzardi's own masses; part A A9 shows the shared files hold about twice those masses, so how far the size applies to GBAR is unclear. A Salpeter factor \"$\\sim$ 1.74\" appears only in a commented-out line of the source file (l. 926, not printed) and is not used; reader A's \"factor ∼2\" is its paraphrase. One-sided, upward")
    term(term_id="icl_omitted", scale="dataset", applies_to=five, moves="g_bar", status="given", size_value=0.05,
         size_unit="fraction of the baryon budget", size_kind="upper_bound", citation=E22, locator="l. 410 (E27)",
         note="\"the contribution of ICL to the total baryon budget is expected to be small ($<5\\%$)\" (E22 l. 410). One-sided, upward. Replaces v1's icl_fraction slider in v2 (D-105 O3)")

    desc = {"term_id": ("meta.id", "Term identifier"), "scale": ("meta.code", "point, system or dataset (standard 2.2.0 §2a)"),
            "applies_to": ("meta.id", "System(s), or * for all twelve"), "moves": ("meta.code", "Axes the term moves"),
            "status": ("meta.code", "given, given_by_other_source or not_given_by_source"),
            "size_unit": ("meta.unit", "Unit of the size"),
            "size_column": ("meta.ref", "Systems column holding a per-system size (standard 2.5.1 §12)"),
            "size_kind": ("meta.code", "one_sigma, range, as_released, upper_bound or lower_bound"),
            "assumption_id": ("meta.id", "Registry assumption whose formula moves the values"),
            "correlated_with": ("meta.note", "Correlated terms"), "covariance": ("meta.code", "published, not_published or not_applicable"),
            "citation": ("meta.bib", "Where the size was read"), "locator": ("meta.ref", "Section, table, line or quote"),
            "note": ("meta.note", "What the term is"), "in_error_columns": ("meta.code", "yes or no: whether the term is inside the error columns (empty: not decided, §7a)")}
    cols = []
    for k in keys:
        if k in ("size_value", "size_lo", "size_hi"):
            cols.append(col(k, t[k], None, {"size_value": "stat.error", "size_lo": "stat.min", "size_hi": "stat.max"}[k],
                            {"size_value": "Size as the source states it", "size_lo": "Lower end of a published range",
                             "size_hi": "Upper end of a published range"}[k], "f8"))
        else:
            cols.append(col(k, t[k], ucd=desc[k][0], description=desc[k][1]))
    terms = Table(cols)
    terms.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    return terms


if __name__ == "__main__":
    sys.exit(main())
