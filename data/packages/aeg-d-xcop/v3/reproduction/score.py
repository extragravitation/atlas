"""Score X-COP v2 against the frozen part B test (REPRODUCTION_PART_B.md items 1-13), once, mechanically.

Usage (locally only; needs the v2 tables, the off-repo source/reading/values.csv and two site builds):
  python data/packages/aeg-d-xcop/v2/reproduction/score.py --dist1 <build 1 dist> --dist2 <build 2 dist> \
      --log <file> [--log <file> ...]

Build 1 = site built with the v2 tables present, after the last edit to any package file; build 2 = site
built as deployed (no v2 tables), checked with the v2 tables moved aside.
The logs are the captured outputs of the converter, validator, formula check, site checks and builds,
searched for every value of values.csv (float64 repr and 6 significant figures; item 12).

CONSENT GATE: prints and writes outcomes, counts, hashes and booleans only, never a row value.
Writes reproduction/result_part_b.json.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

from astropy.table import Table
import numpy as np

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]
PID = "aeg-d-xcop/v2"
FIVE = ["A644", "A1795", "A2029", "A2142", "A2319"]
COUNTS = {"A644": 19, "A1795": 21, "A2029": 22, "A2142": 20, "A2319": 27}
SIDS = {"A644": "aeg-s-000177", "A1795": "aeg-s-000179", "A2029": "aeg-s-000180", "A2142": "aeg-s-000181", "A2319": "aeg-s-000183"}
SEVEN_SIDS = {"A85": "aeg-s-000176", "A1644": "aeg-s-000178", "A2255": "aeg-s-000182", "A3158": "aeg-s-000184",
              "A3266": "aeg-s-000185", "RXC1825": "aeg-s-000186", "ZW1215": "aeg-s-000187"}
A9 = {"A644": "2.04", "A1795": "1.86", "A2029": "2.42", "A2142": "2.27", "A2319": "2.25"}
MMF = {"A644": 0.2241, "A1795": 0.0617, "A2029": 0.1459, "A2142": 0.0852, "A2319": 0.0518}
OBS_STEPS = "events;spectra;projected_t_and_density;deprojected_profiles;hydrostatic_mass;newtonian_g"
BAR_STEPS = "xray;mass;photometry;luminosity;structural_model;newtonian_g"
OBS_REF = ("the source computed g: non-parametric hydrostatic reconstruction evaluated at the radii of the data "
           "(E22 §3.4, l. 263); g_obs = G M_HSE(<r)/r² (l. 453)")
BAR_REF = ("the source computed g, including the central galaxy's dynamical mass-to-light ratio: "
           "G (M_gas + M★,BCG + M★,sat)(<r)/r² (E22 l. 456); ICL excluded (l. 410)")
D092_T = ("The source's g_bar for this cluster could not be rebuilt from the gas and stellar profiles shared with it "
          "(it differs by up to 32 % in the centre; test A2). The values shown are the source's own. The question is with the authors.")
D092_P = ("The published pull from visible matter for this cluster doesn't match the separate files we were given. "
          "We show the published values and have asked the authors.")
A2319_T = ("The Atlas rule that removes systems a source calls out of equilibrium (D-025; D-097 to D-100) applies to "
           "velocity-dispersion measurements only. This cluster's hydrostatic values are therefore plotted, with the "
           "source's own statements shown above (part A §5).")
A2319_P = ("For star clusters and dwarf galaxies, a statement like this from the source takes the system off the map. "
           "That rule is for a different kind of measurement, so this cluster stays on the map, with the source's own words shown.")
HSE_T = ("The source states that its hydrostatic masses are \"mildly biased (<10%) out to R500\" and that \"The HSE "
         "assumption is likely to be a poorer approximation beyond this point\" (Eckert et al. 2022, l. 502). At R200 it "
         "gives \"a mild contribution of nonthermal pressure (10-20%)\" (l. 539).")
HSE_P = "The source says its method is within 10% out to a standard cluster radius, R500, and less reliable beyond it."
VC_T = "X-COP v2 takes g_obs and g_bar as released by Eckert et al. 2022, so its values differ from v1's by ruling (D-090)."
VC_P = "Version 2 uses the values the authors released in 2022, so its numbers differ from version 1."
RULE5 = "Version 2, built from Eckert et al. 2022, is ready and awaiting the authors' confirmation."
EXCL_REASON = "stellar mass not in the source; g_bar bounded below by gas only; recorded under D-090"
EXCL_CITATION = "Eckert et al. 2022, A&A 662, A123 (arXiv 2205.01110v1), l. 103, 114, 402"
D097_WORDING = "describes it as out of equilibrium"
ASSUMPTIONS = "xcop_hse_equilibrium;xcop_spherical;xray_hse_bias=0"


def rows(t: Table) -> list[dict]:
    out = []
    for r in t:
        d = {}
        for c in t.colnames:
            v = r[c]
            if np.ma.is_masked(v):
                d[c] = None
            else:
                v = v.item() if hasattr(v, "item") else v
                d[c] = None if (isinstance(v, str) and v == "") else v
        out.append(d)
    return out


def page_text(p: Path) -> str:
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<script[\s\S]*?</script>", " ", s)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s))


def run(cmd, cwd=ROOT, env=None) -> tuple[int, str]:
    import os
    e = dict(os.environ)
    e["PYTHONPATH"] = str(ROOT / "pipeline")
    if env:
        e.update(env)
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=e)
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist1", required=True)
    ap.add_argument("--dist2", required=True)
    ap.add_argument("--log", action="append", default=[])
    a = ap.parse_args()
    dist1, dist2 = Path(a.dist1), Path(a.dist2)
    res: dict = {"items": {}, "local_only": [2, 4, 5, 11, "12 build 1", "12 log check"], "ci": ["12 build 2", 13, "12 checksum comparison"]}

    frozen = json.loads((ROOT / "data/frozen/xcop-v2-reading.json").read_text(encoding="utf-8"))
    vpath = HERE / "source/reading/values.csv"
    vh = hashlib.sha256(vpath.read_bytes()).hexdigest()
    res["values_csv_sha256_ok"] = vh == frozen["off_repo"]["data/packages/aeg-d-xcop/v2/source/reading/values.csv"]
    V = list(csv.DictReader(vpath.open(encoding="utf-8")))
    M = rows(Table.read(HERE / "tables/measurements.ecsv", format="ascii.ecsv"))
    O = rows(Table.read(HERE / "tables/observables.ecsv", format="ascii.ecsv"))
    S = rows(Table.read(HERE / "tables/systems.ecsv", format="ascii.ecsv"))
    T = rows(Table.read(HERE / "tables/uncertainty_terms.ecsv", format="ascii.ecsv"))
    obs = {o["observable_id"]: o for o in O}
    desc = json.loads((HERE / "datapackage.json").read_text(encoding="utf-8"))
    reg = {x["id"]: x for x in json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))["assumptions"]}
    ki = json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    sysd = {s["system_id"]: s for s in S}
    item = res["items"]

    def put(n, ok, **info):
        item[str(n)] = {"pass": bool(ok), **info}

    # ---- 1. Rows
    exp_sid = [SIDS[c] for c in FIVE for _ in range(COUNTS[c])]
    exp_ref = [f"data_E22.tar.gz:{c}/gbar_gobs_{c}.fits:row {k}" for c in FIVE for k in range(1, COUNTS[c] + 1)]
    ok1 = (len(M) == 109 and [m["system_id"] for m in M] == exp_sid and [m["source_ref"] for m in M] == exp_ref
           and [m["measurement_id"] for m in M] == [f"{PID}/m{i:06d}" for i in range(1, 110)]
           and all(m["kind"] == "profile_point" and m["channel"] == "dynamics" and m["method_class"] == "hydrostatic" for m in M))
    put(1, ok1, rows=len(M), per_cluster={c: sum(1 for m in M if m["system_id"] == SIDS[c]) for c in FIVE})

    # ---- 2. Values (bit for bit against the reader's values.csv)
    order_ok = [(v["cluster"], int(v["row"])) for v in V] == [(c, k) for c in FIVE for k in range(1, COUNTS[c] + 1)]
    n_eq = {"r_kpc": 0, "g_obs": 0, "g_bar": 0}
    for m, v in zip(M, V):
        for col, key in (("r_kpc", "RADIUS"), ("g_obs", "GOBS"), ("g_bar", "GBAR")):
            if isinstance(m[col], float) and m[col] == float(v[key]) and repr(m[col]) == repr(float(v[key])):
                n_eq[col] += 1
    comp_empty = all(m["g_bar_stars"] is None and m["g_bar_gas_cold"] is None and m["g_bar_gas_hot"] is None for m in M)
    status_ok = all(m["stars_status"] == "not_separable" and m["gas_hot_status"] == "not_separable" and m["gas_cold_status"] == "absent"
                    and m["r_kind"] == "3d" for m in M)
    put(2, order_ok and len(V) == 109 and all(x == 109 for x in n_eq.values()) and comp_empty and status_ok,
        values_csv_rows=len(V), equal_bit_for_bit=n_eq, components_empty=comp_empty, statuses=status_ok)

    # ---- 3. Changed values / plotting traceable to the reading
    d096 = list(csv.DictReader((HERE / "reading/d096.csv").open(encoding="utf-8")))
    excl = [r for r in d096 if r["field"] == "excluded" and r["outcome"] not in
            {"none", "no_exclusion_wording", "not_applicable_other_quantity", "not_applicable_other_systems"}]
    not_plotted = [m for m in M if m["plotted"] != "true"]
    put(3, not excl and not not_plotted, reading_exclusions=len(excl), rows_not_plotted=len(not_plotted))

    # ---- 4. Arithmetic
    n4 = 0
    for m in M:
        oo, ob = obs.get(m["observed_from"]), obs.get(m["baryonic_from"])
        if oo and ob and oo["side"] == "observed" and ob["side"] == "baryonic" and oo["value"] == m["g_obs"] and ob["value"] == m["g_bar"]:
            n4 += 1
    put(4, n4 == 109, rows_exact=n4)

    # ---- 5. Error columns and confidence levels
    ef = (HERE / "reading/error_form.md").read_text(encoding="utf-8")
    form = "magnitudes" if "**GOBS_ERR_LO and GOBS_ERR_HI are error magnitudes**" in ef and "**GBAR_ERR is an error magnitude**" in ef else "other"
    n5 = 0
    for m, v in zip(M, V):
        if (m["g_obs_err_lo"] == float(v["GOBS_ERR_LO"]) and m["g_obs_err_hi"] == float(v["GOBS_ERR_HI"])
                and m["g_obs_err_point_lo"] == m["g_obs_err_lo"] and m["g_obs_err_point_hi"] == m["g_obs_err_hi"]
                and m["g_bar_err_lo"] == float(v["GBAR_ERR"]) and m["g_bar_err_hi"] == float(v["GBAR_ERR"])
                and m["g_bar_err_point_lo"] is None and m["g_bar_err_point_hi"] is None):
            n5 += 1
    lev = {r["column"]: r["value"] for r in csv.DictReader((HERE / "reading/err_levels.csv").open(encoding="utf-8"))}
    lev_ok = all(m["err_level"] is None and m["g_bar_err_level"] is None and m["err_level_status"] == lev["err_level_status"] == "not_given_by_source"
                 and m["g_bar_err_level_status"] == lev["g_bar_err_level_status"] == "not_given_by_source" for m in M)
    lev_obs = all(o["err_level"] is None and o["err_level_status"] == "not_given_by_source" for o in O)
    put(5, form == "magnitudes" and n5 == 109 and lev_ok and lev_obs, error_form=form, rows_ok=n5, levels_ok=lev_ok and lev_obs)

    # ---- 6. Extension columns
    props = {r["cluster"].upper(): r for r in csv.DictReader((HERE / "reading/properties.csv").open(encoding="utf-8"))}
    ra = json.loads((HERE / "result_part_a.json").read_text(encoding="utf-8"))["A7"]
    st = Table.read(HERE / "tables/systems.ecsv", format="ascii.ecsv")
    mt = Table.read(HERE / "tables/measurements.ecsv", format="ascii.ecsv")
    sys_cols = ["x_xcop_alpha_nt_r500", "x_xcop_alpha_nt_r500_err_lo", "x_xcop_alpha_nt_r500_err_hi", "x_xcop_alpha_nt_r200",
                "x_xcop_alpha_nt_r200_err_lo", "x_xcop_alpha_nt_r200_err_hi", "x_xcop_centroid_w", "x_xcop_centroid_w_err",
                "x_xcop_mm_gp_ein", "x_xcop_mm_gp_nfw", "x_xcop_mm_ein_nfw", "x_xcop_mass_model_frac", "x_xcop_status"]
    hdr_ok = all(c in st.colnames and st[c].description for c in sys_cols) and all(
        c in mt.colnames and mt[c].description for c in ("x_xcop_centroid_w", "x_xcop_centroid_w_err"))
    au = all("as printed (per cent inferred, not stated)" in st[c].description for c in sys_cols[:6])
    wu = all("10⁻³ (as printed)" in st[c].description for c in sys_cols[6:8])
    nm = {s["name_in_source"].upper(): s for s in S}
    p6 = 0
    for k, s in nm.items():
        p = props[k]
        ok = (s["x_xcop_alpha_nt_r500"] == float(p["alpha_nt_r500"]) and s["x_xcop_alpha_nt_r500_err_lo"] == float(p["alpha_nt_r500_err_lo"])
              and s["x_xcop_alpha_nt_r500_err_hi"] == float(p["alpha_nt_r500_err_hi"]) and s["x_xcop_alpha_nt_r200"] == float(p["alpha_nt_r200"])
              and s["x_xcop_alpha_nt_r200_err_lo"] == float(p["alpha_nt_r200_err_lo"]) and s["x_xcop_alpha_nt_r200_err_hi"] == float(p["alpha_nt_r200_err_hi"])
              and s["x_xcop_centroid_w"] == float(p["w_printed"]) and s["x_xcop_centroid_w_err"] == float(p["w_err_printed"]))
        if k in FIVE:
            r = ra[k]
            ok = ok and s["x_xcop_mm_gp_ein"] == r["GP/EIN"] and s["x_xcop_mm_gp_nfw"] == r["GP/Table1"] and s["x_xcop_mm_ein_nfw"] == r["EIN/Table1"] \
                and s["x_xcop_mass_model_frac"] == MMF[k] and s["x_xcop_status"] == "plotted"
        else:
            ok = ok and s["x_xcop_mm_gp_ein"] is None and s["x_xcop_mm_gp_nfw"] is None and s["x_xcop_mm_ein_nfw"] is None \
                and s["x_xcop_mass_model_frac"] is None and s["x_xcop_status"] == "recorded_not_plotted"
        p6 += ok
    mrow_ok = all(m["x_xcop_centroid_w"] == sysd[m["system_id"]]["x_xcop_centroid_w"]
                  and m["x_xcop_centroid_w_err"] == sysd[m["system_id"]]["x_xcop_centroid_w_err"] for m in M)
    no_rule1 = "x_xcop_r500_rule1_kpc" not in mt.colnames
    put(6, hdr_ok and au and wu and p6 == 12 and mrow_ok and no_rule1, headers=hdr_ok, alpha_unit=au, w_unit=wu,
        systems_ok=p6, rows_centroid=mrow_ok, mass_model_frac_recomputed_equal=all(nm[k]["x_xcop_mass_model_frac"] == MMF[k] for k in FIVE),
        rule1_column_absent=no_rule1)

    # ---- 7. Terms and registry
    five = ";".join(SIDS[c] for c in FIVE)
    four = ";".join(SIDS[c] for c in FIVE if c != "A2319")
    bc = (HERE / "reading/bcg_extra_mass_systems.md").read_text(encoding="utf-8")
    bcg_to = re.search(r"`applies_to` = `([a-z0-9;\-]+)`", bc).group(1)
    E = {  # term: (scale, applies_to, moves, status, size_value, size_kind, size_column, assumption_id)
        "radial_covariance": ("point", "*", "g_obs", "not_given_by_source", None, None, None, None),
        "g_bar_point": ("point", "*", "g_bar", "not_given_by_source", None, None, None, None),
        "np_smoothing": ("point", "*", "g_obs", "not_given_by_source", None, None, None, None),
        "reconstruction_bias": ("dataset", five, "g_obs", "given", 0.05, "upper_bound", None, None),
        "hse_bias": ("dataset", four, "g_obs", "given", 0.10, "upper_bound", None, "xray_hse_bias"),
        "hse_bias_a2319": ("dataset", SIDS["A2319"], "g_obs", "not_given_by_source", None, None, None, "xray_hse_bias"),
        "nonthermal_pressure": ("system", "*", "g_obs", "given_by_other_source", None, "as_released", "x_xcop_alpha_nt_r500", None),
        "gas_inhomogeneity": ("dataset", five, "g_obs", "given", 0.10, "upper_bound", None, None),
        "xmm_calibration": ("dataset", five, "g_obs", "not_given_by_source", None, None, None, None),
        "mass_model_choice": ("system", "*", "g_obs", "given", None, "as_released", "x_xcop_mass_model_frac", None),
        "cosmology": ("dataset", "*", "both", "not_given_by_source", None, None, None, None),
        "gas_density_conversion": ("dataset", five, "g_bar", "not_given_by_source", None, None, None, None),
        "bcg_ml": ("system", "*", "g_bar", "not_given_by_source", None, None, None, None),
        "bcg_ml_extra_mass_model": ("dataset", bcg_to, "g_bar", "given", 0.083, "as_released", None, None),
        "bcg_jam_geometry": ("dataset", five, "g_bar", "given_by_other_source", 0.15, "upper_bound", None, None),
        "bcg_sersic_extrapolation": ("system", "*", "g_bar", "not_given_by_source", None, None, None, None),
        "satellite_cosmic_variance": ("system", "*", "g_bar", "not_given_by_source", None, None, None, None),
        "satellite_flux": ("system", "*", "g_bar", "not_given_by_source", None, None, None, None),
        "satellite_gnfw_smoothing": ("system", "*", "g_bar", "not_given_by_source", None, None, None, None),
        "satellite_projection": ("system", "*", "g_bar", "not_given_by_source", None, None, None, None),
        "satellite_mass_systematic": ("dataset", five, "g_bar", "given_by_other_source", 0.60, "upper_bound", None, None),
        "icl_omitted": ("dataset", five, "g_bar", "given", 0.05, "upper_bound", None, None),
    }
    bad7 = []
    for t in T:
        e = E.get(t["term_id"])
        if not e:
            bad7.append(t["term_id"])
            continue
        got = (t["scale"], t["applies_to"], t["moves"], t["status"], t["size_value"], t["size_kind"], t["size_column"], t["assumption_id"])
        if got != e or t["covariance"] != "not_published" or t["in_error_columns"] is not None or not t["citation"] or not t["note"]:
            bad7.append(t["term_id"])
        if t["status"] in ("given", "given_by_other_source") and not t["size_unit"]:
            bad7.append(t["term_id"] + ":size_unit")
    terms_ok = len(T) == 22 and {t["term_id"] for t in T} == set(E) and not bad7
    hb = reg["xray_hse_bias"]["datasets"].get(PID) or {}
    hb_cols = sorted(e["column"] for e in hb.get("effects", []))
    hb_ok = (hb.get("default") == 0 and hb.get("min") == 0 and hb.get("max") == 0.2 and "l. 502" in (hb.get("default_ref") or "")
             and "l. 502" in (hb.get("range_ref") or "") and "l. 539" in (hb.get("note") or "")
             and hb_cols == sorted(["g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_obs_err_point_lo", "g_obs_err_point_hi"])
             and all(e["formula"] == f"{e['column']} * (1 - p0) / (1 - p)" for e in hb["effects"]))
    new_ok = all(k in reg and PID in reg[k]["datasets"] and not reg[k]["adjustable"] for k in ("xcop_hse_equilibrium", "xcop_spherical")) \
        and "l. 130" in reg["xcop_hse_equilibrium"]["datasets"][PID]["default_ref"] and "l. 38" in reg["xcop_hse_equilibrium"]["datasets"][PID]["default_ref"] \
        and "l. 97" in reg["xcop_spherical"]["datasets"][PID]["default_ref"]
    none_ok = PID not in reg["icl_fraction"]["datasets"] and PID not in reg.get("stars_cluster_modelled", {"datasets": {}})["datasets"]
    rows_ok = all(m["assumptions"] == ASSUMPTIONS and m["adjustable"] == "xray_hse_bias" for m in M)
    put(7, terms_ok and hb_ok and new_ok and none_ok and rows_ok, terms=len(T), term_mismatches=bad7,
        bcg_extra_applies_to_from_reading=bcg_to, xray_hse_bias_v2=hb_ok, new_entries=new_ok, no_icl_or_stars_entries=none_ok, row_assumptions=rows_ok)

    # ---- 8. Tables
    ob_ok = len(O) == 218
    n8 = 0
    for m in M:
        oo, ob = obs.get(m["observed_from"]), obs.get(m["baryonic_from"])
        if not (oo and ob):
            continue
        ok = (oo["quantity"] == ob["quantity"] == "acceleration_released" and oo["unit"] == ob["unit"] == "m / s2"
              and oo["steps"] == OBS_STEPS and ob["steps"] == BAR_STEPS and oo["err_lo"] == m["g_obs_err_lo"] and oo["err_hi"] == m["g_obs_err_hi"]
              and ob["err_lo"] == m["g_bar_err_lo"] and ob["err_hi"] == m["g_bar_err_hi"] and oo["r_kpc"] == ob["r_kpc"] == m["r_kpc"]
              and oo["source_ref"].startswith(m["source_ref"]) and OBS_REF in oo["source_ref"] and BAR_REF in ob["source_ref"]
              and oo["err_level_status"] == ob["err_level_status"] == "not_given_by_source")
        n8 += ok
    t1 = {}
    pat = re.compile(r"^\| ([A-Za-z0-9]+) \| ([0-9.]+) \| ([0-9.]+) \(−([0-9.]+)/\+([0-9.]+)\) \| ([0-9.]+) \(−([0-9.]+)/\+([0-9.]+)\) \| ([0-9.]+) \(−([0-9.]+)/\+([0-9.]+)\) \|$")
    for line in (HERE / "REPRODUCTION.md").read_text(encoding="utf-8").splitlines():
        mm = pat.match(line.strip())
        if mm:
            t1[mm.group(1).upper()] = [float(x) for x in mm.groups()[1:]]
    sys_ok = len(S) == 12 and {s["system_id"] for s in S} == set(SIDS.values()) | set(SEVEN_SIDS.values())
    n8s = 0
    for s in S:
        k = s["name_in_source"].upper()
        p = json.loads(s["properties"])
        v = t1[k]
        n8s += (s["taxonomy_kind"] == "A9" and s["redshift"] == v[0] and p["r500_tot_kpc"] == v[1] and p["m500_tot_1e14_solMass"] == v[4]
                and p["m200_tot_1e14_solMass"] == v[7] and set(p) <= {"r500_tot_kpc", "r500_tot_err_lo_kpc", "r500_tot_err_hi_kpc",
                "m500_tot_1e14_solMass", "m500_tot_err_lo_1e14_solMass", "m500_tot_err_hi_1e14_solMass", "m200_tot_1e14_solMass",
                "m200_tot_err_lo_1e14_solMass", "m200_tot_err_hi_1e14_solMass", "ref"})
    plot_ok = all(m["plotted"] == "true" and m["role"] == "default" and m["not_plotted_reason"] is None for m in M)
    flag_ok = all("no_uncertainty" not in (m["flags"] or "") for m in M)
    put(8, ob_ok and n8 == 109 and sys_ok and n8s == 12 and plot_ok and flag_ok, observables=len(O), rows_with_both_observables_ok=n8,
        systems=len(S), systems_ok=n8s, all_plotted_default=plot_ok, no_uncertainty_flags=sum("no_uncertainty" in (m["flags"] or "") for m in M))

    # ---- 9. Named items (rows; pages in build 1)
    hse = [h for h in sorted(csv.DictReader((HERE / "reading/hse_statements.csv").open(encoding="utf-8")), key=lambda h: int(h["order"]))
           if h["in_a2319_notes"] == "yes"]
    a644 = [m for m in M if m["system_id"] == SIDS["A644"]]
    a644_ok = all(D092_T in (m["notes"] or "") and "reproduction_mismatch" in (m["flags"] or "").split(";")
                  and "#136" in (m["known_issues"] or "").split(";") for m in a644) and len(a644) == 19
    other_flag = any("reproduction_mismatch" in (m["flags"] or "") for m in M if m["system_id"] != SIDS["A644"])
    a2319 = [m for m in M if m["system_id"] == SIDS["A2319"]]

    def in_order(note):
        pos = -1
        for h in hse:
            frag = f"\"{h['quote']}\""
            i = note.find(frag, pos + 1)
            if i < 0 or f"l. {h['line']})" not in note[i:i + len(frag) + 200]:
                return False
            pos = i
        return True
    a2319_ok = len(hse) == 7 and len(a2319) == 27 and all(in_order(m["notes"] or "") for m in a2319)
    proj_ok = all(f"stellar projection: undetermined (part A, A6); stellar normalisation against Ghizzardi et al. 2021: {A9[c]} (part A, A9)"
                  in (m["notes"] or "") for c in FIVE for m in M if m["system_id"] == SIDS[c])
    cen_ok = all(isinstance(m["x_xcop_centroid_w"], float) for m in M)
    kin = {k["issue"]: k for k in ki}
    ki_ok = {124, 129, 136, 178, 179} <= set(kin) and kin[178]["clusters"] == ["A3158"] and kin[178].get("rows") is False \
        and not kin[178]["measurements"] and "03c" in kin[178]["title"] and "D-091" in kin[179]["title"]
    pg = {}
    t644 = page_text(dist1 / f"systems/{SIDS['A644']}/index.html")
    pg["a644_expert"], pg["a644_plain"] = D092_T in t644, D092_P in t644
    t2319 = page_text(dist1 / f"systems/{SIDS['A2319']}/index.html")
    pg["a2319_expert"], pg["a2319_plain"] = A2319_T in t2319, A2319_P in t2319
    pg["a2319_statements_above"] = all(h["quote"] in t2319 for h in hse) and t2319.find(hse[-1]["quote"]) < t2319.find(A2319_T)
    tds = page_text(dist1 / "datasets/aeg-d-xcop/v2/index.html")
    pg["hse_expert"], pg["hse_plain"] = HSE_T in tds, HSE_P in tds
    ex = {}
    for nm_, sid in SEVEN_SIDS.items():
        tx = page_text(dist1 / f"systems/{sid}/index.html")
        ex[nm_] = "Recorded, not plotted" in tx and EXCL_REASON in tx and EXCL_CITATION in tx and D097_WORDING not in tx
    pg["seven_exclusion_pages"] = sum(ex.values())
    put(9, a644_ok and not other_flag and a2319_ok and proj_ok and cen_ok and ki_ok and all(v is True for k, v in pg.items() if k != "seven_exclusion_pages")
        and pg["seven_exclusion_pages"] == 7, a644_rows=a644_ok, flag_only_on_a644=not other_flag, a2319_statements=len(hse),
        a2319_rows=a2319_ok, stellar_projection_notes=proj_ok, centroid_on_rows=cen_ok, known_issues=ki_ok, pages=pg)

    # ---- 10. Descriptor and sources.json
    inv = {c["component"]: c["status"] for c in desc.get("x_baryon_inventory", [])}
    src = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))["sources"]
    arch = {s["file"]: s for s in src}
    arch_ok = all(arch[f]["sha256"] == h and arch[f]["redistributable"] is False and arch[f]["licence"] == "not stated; asked (#19)"
                  and arch[f].get("bytes") and arch[f].get("members_sha256")
                  for f, h in (("data_E22.tar.gz", "ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d"),
                               ("mbar.tar.gz", "0420a7edba60da7f2df6aa4f38cbb21135ab50949d579176a8c893bab712c496")))
    eps = {s["url"].rsplit("/", 1)[-1] for s in src if "arxiv.org/e-print" in s["url"] and s.get("bytes") and s.get("sha256")}
    ep_ok = eps == {"2205.01110v1", "2205.01123v1", "2112.07554v1", "2006.05706v1", "2007.01084v1"}
    d_ok = (desc.get("standard_version") == "2.5.1" and desc.get("x_publication") == "awaiting_authors_consent"
            and desc.get("x_value_change_ruling") == "D-090" and "D-089" in desc.get("x_precedence", "") and "D-090 rule 1" in desc.get("x_precedence", "")
            and desc.get("x_second_reading", {}).get("file") == "SECOND_READING.md" and desc["x_second_reading"].get("frozen") == "data/frozen/xcop-v2-reading.json"
            and inv.get("hot gas") == "measured" and inv.get("central galaxy (BCG) stars") == "measured" and inv.get("satellite galaxy stars") == "measured"
            and inv.get("intracluster light") == "stated_negligible" and "l. 410" in next(c["citation"] for c in desc["x_baryon_inventory"] if c["component"] == "intracluster light")
            and inv.get("cold gas") == "not_addressed" and "one total" in desc.get("x_baryon_inventory_note", ""))
    vc = VC_T in tds and VC_P in tds
    put(10, d_ok and arch_ok and ep_ok and vc, descriptor=d_ok, archives=arch_ok, eprints=ep_ok, value_change_sentences=vc)

    # ---- 11. Second reading, by the listed pairs
    pairs = {
        "values_vs_rows_and_observables": n_eq["r_kpc"] == n_eq["g_obs"] == n_eq["g_bar"] == 109 and n4 == 109,
        "error_form_vs_error_columns": n5 == 109,
        "model_form_vs_model_dependence": "**`model_dependence` = `none`**" in (HERE / "reading/model_form.md").read_text(encoding="utf-8")
                                          and all(m["model_dependence"] == "none" for m in M),
        "err_levels_vs_level_columns": lev_ok,
        "properties_vs_extension_columns": p6 == 12 and mrow_ok,
        "hse_statements_vs_a2319_notes": a2319_ok,
        "bcg_extra_mass_vs_applies_to": next(t["applies_to"] for t in T if t["term_id"] == "bcg_ml_extra_mass_model") == bcg_to == "aeg-s-000177;aeg-s-000183",
        "d096_vs_plotting": not excl and not not_plotted,
    }
    put(11, all(pairs.values()), pairs=pairs)

    # ---- 12. Standard and site, two builds, log check
    b = {}
    rc, _ = run([sys.executable, "-m", "aeg.validate", str(HERE)])
    b["build1_validate"] = rc == 0
    rc, out = run([sys.executable, "-m", "aeg.formula_check"])
    b["build1_formula_check"] = rc == 0 and "formula check passed" in out
    # the v2 entry is exercised: count v2 rows offered xray_hse_bias (3 evaluations each)
    b["build1_formula_check_covers_v2_rows"] = sum(1 for m in M if m["adjustable"] == "xray_hse_bias")
    rc, out = run([sys.executable, "-m", "aeg.site_check", str(dist1)])
    b["build1_site_check_0_errors"] = rc == 0 and out.strip().endswith("0 errors")
    b["build1_v2_pages"] = (dist1 / "datasets/aeg-d-xcop/v2/index.html").is_file()
    rc, out = run(["git", "ls-files", "data/packages/aeg-d-xcop/v2/tables"])
    b["build2_no_v2_table_tracked"] = rc == 0 and out.strip() == ""
    rc, out = run(["git", "check-ignore", "-q", "data/packages/aeg-d-xcop/v2/tables/measurements.ecsv"])
    b["build2_tables_ignored"] = rc == 0
    # Build 2 is checked against the repository as deployed: the v2 tables are moved aside while
    # site_check runs (build-only fix after run 1, which ran it with the tables present; see the result).
    import shutil
    import tempfile
    hold = Path(tempfile.mkdtemp()) / "tables"
    shutil.move(str(HERE / "tables"), str(hold))
    try:
        rc, out = run([sys.executable, "-m", "aeg.site_check", str(dist2)])
    finally:
        shutil.move(str(hold), str(HERE / "tables"))
    b["build2_site_check_0_errors"] = rc == 0 and out.strip().endswith("0 errors")
    t1p = page_text(dist2 / "datasets/aeg-d-xcop/v1/index.html")
    b["build2_v1_current"] = "Superseded by" not in t1p
    b["build2_rule5_sentence"] = RULE5 in t1p
    leak_paths = [p for p in dist2.rglob("*") if p.is_file() and p.suffix in (".html", ".json", ".csv", ".ecsv", ".js", ".txt")
                  and ("aeg-d-xcop/v2" in p.read_text(encoding="utf-8", errors="ignore") and "/m0" in p.read_text(encoding="utf-8", errors="ignore"))]
    b["build2_no_v2_page_point_download"] = not (dist2 / "datasets/aeg-d-xcop/v2").exists() and not (dist2 / "downloads/aeg-d-xcop/v2").exists() \
        and not any(re.search(r"aeg-d-xcop/v2/m\d{6}", p.read_text(encoding="utf-8", errors="ignore")) for p in leak_paths)
    # log check: every value of values.csv, as float64 repr and at 6 significant figures
    needles = set()
    for v in V:
        for k in ("RADIUS", "GBAR", "GBAR_ERR", "GOBS", "GOBS_ERR_LO", "GOBS_ERR_HI"):
            x = float(v[k])
            needles.add(repr(x))
            needles.add(f"{x:.6g}")
            needles.add(f"{x:.5e}")
    hits = 0
    for lp in a.log:
        txt = Path(lp).read_text(encoding="utf-8", errors="ignore")
        hits += sum(1 for nd in needles if nd in txt)
    b["log_files_searched"] = len(a.log)
    b["log_needles"] = len(needles)
    b["log_hits"] = hits
    put(12, all(v is True for k, v in b.items() if isinstance(v, bool)) and hits == 0 and len(a.log) > 0
        and b["build1_formula_check_covers_v2_rows"] == 109, **b)

    # ---- 13. v1 untouched since 5dc4091
    rc, out = run(["git", "diff", "--name-only", "5dc4091", "--", "data/packages/aeg-d-xcop/v1"])
    rc2, out2 = run(["git", "status", "--porcelain", "--", "data/packages/aeg-d-xcop/v1"])
    put(13, rc == 0 and out.strip() == "" and rc2 == 0 and out2.strip() == "", files_changed=len([x for x in out.split() if x]))

    res["pass"] = all(v["pass"] for v in item.values()) and len(item) == 13 and res["values_csv_sha256_ok"]
    (HERE / "reproduction").mkdir(exist_ok=True)
    (HERE / "reproduction/result_part_b.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for k in sorted(item, key=int):
        print(f"item {k}: {'PASS' if item[k]['pass'] else 'FAIL'}")
    print("PART B:", "PASS" if res["pass"] else "FAIL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
