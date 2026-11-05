"""Score aeg-d-kids1000-rar/v2 against its frozen test REPRODUCTION_REV3.md, items 1–11 and 14 (mechanical).

Usage (repository root): PYTHONPATH=pipeline python data/packages/aeg-d-kids1000-rar/v2/reproduction/score.py

Items 12 and 13 are run by convert.py (12), the validator, the site build and aeg.site_check (13); their outcomes
are recorded in REPRODUCTION_RESULT.md. Writes reproduction/score.json.
"""

from __future__ import annotations

import csv
import io
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from astropy.table import Table

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]
V1 = HERE.parent / "v1"
REF = "5dc4091"
P1, P2 = "aeg-d-kids1000-rar/v1/", "aeg-d-kids1000-rar/v2/"
DELTA = math.log10(5e-12 / 1e-15) / 15


def rows(t):
    out = []
    for r in t:
        d = {}
        for c in t.colnames:
            v = r[c]
            d[c] = None if np.ma.is_masked(v) else (v.item() if hasattr(v, "item") else v)
            if isinstance(d[c], str) and d[c] == "":
                d[c] = None
        out.append(d)
    return out


def v1_table(name):
    text = subprocess.run(["git", "show", f"{REF}:data/packages/aeg-d-kids1000-rar/v1/tables/{name}"],
                          cwd=ROOT, check=True, capture_output=True, text=True).stdout
    return Table.read(text, format="ascii.ecsv")


def main() -> int:
    res: dict[str, dict] = {}

    def item(n, ok, detail):
        res[str(n)] = {"outcome": "pass" if ok else "FAIL", "detail": detail}

    m1, m2 = rows(v1_table("measurements.ecsv")), rows(Table.read(HERE / "tables/measurements.ecsv", format="ascii.ecsv"))
    c1, c2 = rows(v1_table("covariance.ecsv")), rows(Table.read(HERE / "tables/covariance.ecsv", format="ascii.ecsv"))
    obs = rows(Table.read(HERE / "tables/observables.ecsv", format="ascii.ecsv"))
    terms = rows(Table.read(HERE / "tables/uncertainty_terms.ecsv", format="ascii.ecsv"))
    desc = json.loads((HERE / "datapackage.json").read_text(encoding="utf-8"))

    # 1
    ok1 = len(m2) == 45 and all(a["x_kids1000_rar_sample"] == b["x_kids1000_rar_sample"] and a["source_ref"] == b["source_ref"]
                                for a, b in zip(m1, m2))
    item(1, ok1, f"{len(m2)} rows; sample and source_ref equal to v1 row by row: {ok1}")

    # 2
    bitcols = ["g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_bar", "x_kids1000_rar_esd_t", "x_kids1000_rar_esd_x",
               "x_kids1000_rar_esd_err", "x_kids1000_rar_bias"]
    allowed = {"flags", "assumptions", "notes", "role", "plotted", "not_plotted_reason", "alternative_of",
               "stars_status", "gas_cold_status", "gas_hot_status"}
    bad_bits = [(i + 1, c) for i, (a, b) in enumerate(zip(m1, m2)) for c in bitcols
                if not (a[c] == b[c] and float(a[c]).hex() == float(b[c]).hex())]
    other = [c for c in m1[0] if c not in bitcols and c not in allowed]
    bad_other = []
    for i, (a, b) in enumerate(zip(m1, m2)):
        for c in other:
            va, vb = a[c], b[c]
            if c == "measurement_id":
                va = va.replace(P1, P2)
            if va != vb:
                bad_other.append((i + 1, c, va, vb))
    changed = sorted({c for c in allowed if c in m1[0] and any(a[c] != b[c] for a, b in zip(m1, m2))})
    item(2, not bad_bits and not bad_other,
         f"bit-for-bit columns {bitcols}: {len(bad_bits)} differences; other v1 columns compared {other}: "
         f"{len(bad_other)} differences {bad_other[:3]}; v1 columns that changed (all allowed): {changed}")

    # 3
    key = lambda r: (r["measurement_id_i"], r["measurement_id_j"], r["quantity"])
    a3 = [(r["measurement_id_i"].replace(P1, P2), r["measurement_id_j"].replace(P1, P2), r["quantity"],
           float(r["covariance"]).hex()) for r in c1]
    b3 = [(r["measurement_id_i"], r["measurement_id_j"], r["quantity"], float(r["covariance"]).hex()) for r in c2]
    item(3, a3 == b3, f"{len(b3)} covariance entries; identical to v1 apart from the prefix: {a3 == b3}")

    # 4
    pointcols = [c for c in m2[0] if "err_point" in c]
    ok4 = all(r["err_level"] == 0.683 and r["err_level_status"] == "stated" for r in m2) and not pointcols
    item(4, ok4, f"err_level 0.683 stated on all rows: {all(r['err_level'] == 0.683 and r['err_level_status'] == 'stated' for r in m2)}; "
                 f"point-scale columns: {pointcols or 'none'}; g_obs errors bit-for-bit v1 (item 2)")

    # 5
    issues5 = []
    for i, r in enumerate(m2):
        k = i % 15 + 1
        lo, hi = 10 ** (-15 + (k - 1) * DELTA), 10 ** (-15 + k * DELTA)
        if r["g_bar_basis"] != "bin_coordinate" or r["g_bar_err_lo"] is not None or r["g_bar_err_hi"] is not None:
            issues5.append((i + 1, "basis/errors"))
        if abs(r["g_bar_bin_lo"] / lo - 1) > 1e-12 or abs(r["g_bar_bin_hi"] / hi - 1) > 1e-12:
            issues5.append((i + 1, "edges"))
        if not (r["g_bar_bin_lo"] <= r["g_bar"] <= r["g_bar_bin_hi"]):
            issues5.append((i + 1, "outside bin"))
        if r["x_kids1000_rar_sample"] == "kids_bright_hotgas" and "§2.1 bin edges is the Atlas's inference" not in (r["notes"] or ""):
            issues5.append((i + 1, "hot-gas edge note"))
    item(5, not issues5, f"45 rows: bin_coordinate, empty g_bar errors, edges to 1e-12, g_bar inside its bin, hot-gas notes; problems: {issues5 or 'none'}")

    # 6
    q1 = [i for i, r in enumerate(m1) if "source_quality_low" in (r["flags"] or "")]
    q2 = [i for i, r in enumerate(m2) if "source_quality_low" in (r["flags"] or "")]
    nu = sum("no_uncertainty" in (r["flags"] or "") for r in m2)
    ki = json.loads((HERE / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    ok6 = q1 == q2 and len(q2) == 16 and nu == 0 and {k["issue"] for k in ki} == {168, 169}
    item(6, ok6, f"no_uncertainty on {nu} rows; source_quality_low on {len(q2)} rows, same as v1: {q1 == q2}; "
                 f"known issues linked: {sorted(k['issue'] for k in ki)} (#168 hot-gas flags, #169 the 0.3/3 Mpc wording)")

    # 7
    spec = {"esd_to_gobs_conversion": ("point", "g_obs", "given", 0.1, "as_released", "no"),
            "shear_calibration": ("dataset", "g_obs", "not_given_by_source", None, None, None),
            "source_redshift_calibration": ("dataset", "g_obs", "not_given_by_source", None, None, None),
            "random_subtraction": ("dataset", "g_obs", "not_given_by_source", None, None, None),
            "stellar_mass_per_lens_kids": ("dataset", "both", "given", 0.12, "one_sigma", None),
            "stellar_mass_per_lens_gama": ("dataset", "both", "not_given_by_source", None, None, None),
            "stellar_mass_systematic": ("dataset", "both", "given", 0.2, "as_released", None),
            "gama_normalisation": ("dataset", "g_bar", "not_given_by_source", None, None, None),
            "cold_gas_relation": ("dataset", "g_bar", "not_given_by_source", None, None, None),
            "isolation_satellites": ("dataset", "g_obs", "given", 0.30, "as_released", None),
            "cosmology_h70": ("dataset", "both", "not_given_by_source", None, None, None)}
    got7 = {t["term_id"]: (t["scale"], t["moves"], t["status"], t["size_value"], t["size_kind"], t["in_error_columns"]) for t in terms}
    cov_ok = all(t["covariance"] == "not_published" and t["applies_to"] == "*" and t["citation"] for t in terms)
    regs = json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))["assumptions"]
    reg_ids = {a["id"] for a in regs if "aeg-d-kids1000-rar/v2" in a["datasets"]}
    asm_ok = all(set(r["assumptions"].split(";")) ==
                 ({"deproj_lensing=sis", "baryons_point_mass"} | ({"hot_gas_halo=authors_estimate"} if r["x_kids1000_rar_sample"] == "kids_bright_hotgas" else set()))
                 for r in m2)
    ok7 = got7 == spec and cov_ok and {"deproj_lensing", "baryons_point_mass", "hot_gas_halo"} <= reg_ids and asm_ok
    item(7, ok7, f"{len(terms)} terms, exactly the table: {got7 == spec}; covariance not_published, citations present: {cov_ok}; "
                 f"registry v2 entries {sorted(reg_ids)}; row assumptions as specified: {asm_ok}")

    # 8
    oid = {o["observable_id"]: o for o in obs}
    issues8 = []
    for r in m2:
        o, b = oid.get(r["observed_from"]), oid.get(r["baryonic_from"])
        if not o or not b:
            issues8.append((r["measurement_id"], "missing")); continue
        if (o["side"], o["quantity"], o["unit"], o["steps"], o["evidence_tier"]) != ("observed", "delta_sigma", "solMass / pc2", "shapes;shear;excess_surface_density", 1):
            issues8.append((r["measurement_id"], "observed row"))
        if not (o["value"] == r["x_kids1000_rar_esd_t"] and o["err_lo"] == o["err_hi"] == r["x_kids1000_rar_esd_err"]):
            issues8.append((r["measurement_id"], "observed values"))
        if (b["side"], b["quantity"], b["unit"], b["steps"], b["evidence_tier"]) != ("baryonic", "acceleration_released", "m / s2", "photometry", 1):
            issues8.append((r["measurement_id"], "baryonic row"))
        if b["value"] != r["g_bar"] or "arithmetic midpoint" not in b["source_ref"] or "point mass" not in b["source_ref"]:
            issues8.append((r["measurement_id"], "baryonic values/ref"))
        if r["x_kids1000_rar_sample"] == "kids_bright_hotgas" and "only a rough order of magnitude estimate" not in b["source_ref"]:
            issues8.append((r["measurement_id"], "hot-gas ref"))
    item(8, not issues8 and len(obs) == 90, f"{len(obs)} observables, two per row; problems: {issues8 or 'none'}")

    # 9
    issues9 = []
    for i, r in enumerate(m2):
        s, k = r["x_kids1000_rar_sample"], i % 15 + 1
        base = (r["measured_quantity"], r["limit"], r["evidence_tier"], r["kind"], r["model_dependence"])
        if base != ("g_obs", "none", 1, "population_bin", "total_mass_form"):
            issues9.append((i + 1, "base"))
        exp_hot = "modelled" if s == "kids_bright_hotgas" else "absent"
        if (r["stars_status"], r["gas_cold_status"], r["gas_hot_status"]) != ("not_separable", "not_separable", exp_hot):
            issues9.append((i + 1, "statuses"))
        if s == "kids_bright_hotgas":
            exp = ("alternative", m2[k - 1]["measurement_id"], "false", "alternative_value")
        elif s == "kids_bright" and k <= 8:
            exp = ("default", None, "false", "other")
            if not all(x in r["notes"] for x in ("(l. 508)", "(l. 748)", "(l. 821)", "∼30% higher",
                                                   "D-096 rule 2 (D-103): excluded by the source from its tests of analytical models (l. 748); recorded, not plotted")):
                issues9.append((i + 1, "D-103 notes"))
        else:
            exp = ("default", None, "true", None)
        if (r["role"], r["alternative_of"], r["plotted"], r["not_plotted_reason"]) != exp:
            issues9.append((i + 1, "role/plotting"))
        if "point mass" not in r["notes"]:
            issues9.append((i + 1, "point-mass note"))
    page = (ROOT / "site/src/pages/datasets/[name]/[version].astro").read_text(encoding="utf-8")
    page_ok = "KiDS-bright bins 1–8" in page and "only a rough order of magnitude estimate" in page
    exc = (ROOT / "data/registry/excluded.csv").read_text(encoding="utf-8")
    item(9, not issues9 and page_ok and "aeg-d-kids1000-rar" not in exc,
         f"measurement columns per row; problems: {issues9 or 'none'}; dataset page states the exclusion and the hot-gas "
         f"variant: {page_ok}; no excluded.csv rows for bins: {'aeg-d-kids1000-rar' not in exc}")

    # 10
    inv = {c["component"]: c["status"] for c in desc.get("x_baryon_inventory", [])}
    ok10 = (desc.get("standard_version") == "2.5.1" and "x_value_change_ruling" not in desc and bool(desc.get("x_selection"))
            and "D-103" in desc.get("x_precedence", "") and inv == {"stars": "measured", "cold gas": "modelled",
            "hot gas": "known_unmeasured", "cool and warm (ionised) gas, dust": "known_unmeasured", "remnants": "not_addressed"}
            and desc.get("x_search_log") and desc.get("x_second_reading") == "SECOND_READING.md")
    item(10, ok10, f"standard 2.5.1; no x_value_change_ruling; x_selection, x_precedence (D-103), x_baryon_inventory {inv}, "
                   f"x_search_log, x_second_reading present: {ok10}")

    # 11
    rd = list(csv.DictReader((HERE / "reading/kids-second-reading.csv").open(encoding="utf-8")))
    name = {"KiDS-bright": "kids_bright", "GAMA": "gama", "KiDS-bright hot-gas variant": "kids_bright_hotgas"}
    by = {(name[r["sample"]], int(r["row_index"])): r for r in rd}
    obs_by = oid
    mism = []
    for i, r in enumerate(m2):
        k, s = i % 15 + 1, r["x_kids1000_rar_sample"]
        x = by[(s, k)]
        o, b = obs_by[r["observed_from"]], obs_by[r["baryonic_from"]]
        pairs = [(o["value"], x["ESD_t"]), (o["err_lo"], x["error"]), (o["err_hi"], x["error"]),
                 (b["value"], x["g_bar"]), (r["g_bar"], x["g_bar"]),
                 (r["x_kids1000_rar_esd_t"], x["ESD_t"]), (r["x_kids1000_rar_esd_x"], x["ESD_x"]),
                 (r["x_kids1000_rar_esd_err"], x["error"]), (r["x_kids1000_rar_bias"], x["bias"])]
        for got, printed in pairs:
            if got != float(printed):
                mism.append((r["measurement_id"], got, printed))
        for got, want in ((r["g_bar_bin_lo"], float(x["bin_lo"])), (r["g_bar_bin_hi"], float(x["bin_hi"]))):
            if abs(got / want - 1) > 1e-12:
                mism.append((r["measurement_id"], "edge", got, want))
    # covariance: regenerated reading (gitignored source/reading/), divided by column 7, times FACTOR², as v1
    import astropy.constants as const
    import astropy.units as u
    FACTOR = (4 * const.G * (1 * u.Msun / u.pc**2)).to(u.m / u.s**2).value
    covr = list(csv.DictReader((HERE / "source/reading/kids-covariance.csv").open(encoding="utf-8")))
    ids = {s: [r["measurement_id"] for r in m2 if r["x_kids1000_rar_sample"] == s] for s in name.values()}
    pkg = {(r["measurement_id_i"], r["measurement_id_j"]): r["covariance"] for r in c2}
    cmis = 0
    for r in covr:
        s = name[r["sample"]]
        want = FACTOR**2 * float(r["covariance"]) / float(r["bias_product"])
        got = pkg[(ids[s][int(r["i"]) - 1], ids[s][int(r["j"]) - 1])]
        if got != want:
            cmis += 1
    plot_ok = all((r["plotted"] == "false") == (r["x_kids1000_rar_sample"] == "kids_bright_hotgas"
                  or (r["x_kids1000_rar_sample"] == "kids_bright" and i % 15 + 1 <= 8)) for i, r in enumerate(m2))
    d096 = (HERE / "reading/kids-d096.md").read_text(encoding="utf-8")
    reading_rows = "Rows 1–8" in d096 and "seven data points" in d096
    item(11, not mism and cmis == 0 and len(covr) == 675 and plot_ok and reading_rows,
         f"{len(m2)} rows × 11 numbers against the frozen reading: {len(mism)} mismatches; covariance {len(covr)} entries "
         f"against the regenerated reading (÷ column 7, × (4G)², as v1): {cmis} mismatches; plotting statuses as the "
         f"reading's two findings (hot-gas variant; KiDS-bright rows 1–8): {plot_ok and reading_rows}")

    # 14
    diff = subprocess.run(["git", "diff", "--quiet", REF, "--", "data/packages/aeg-d-kids1000-rar/v1"], cwd=ROOT)
    untracked = subprocess.run(["git", "status", "--porcelain", "--", "data/packages/aeg-d-kids1000-rar/v1"],
                               cwd=ROOT, capture_output=True, text=True).stdout.strip()
    item(14, diff.returncode == 0 and not untracked, f"git diff {REF} -- v1: {'none' if diff.returncode == 0 else 'DIFFERS'}; "
                                                      f"untracked changes: {untracked or 'none'}")

    out = {"test": "REPRODUCTION_REV3.md", "items": res,
           "counts": {"rows": len(m2), "plotted": sum(r["plotted"] == "true" for r in m2),
                      "d096_rule2_rows": sum(1 for i, r in enumerate(m2) if r["x_kids1000_rar_sample"] == "kids_bright" and i % 15 + 1 <= 8),
                      "d096_rule3_rows": sum(r["x_kids1000_rar_sample"] == "kids_bright_hotgas" for r in m2),
                      "values_changed": len(bad_bits)}}
    (HERE / "reproduction/score.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for k, v in res.items():
        print(k, v["outcome"], "-", v["detail"][:220])
    print(out["counts"])
    return 0 if all(v["outcome"] == "pass" for v in res.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
