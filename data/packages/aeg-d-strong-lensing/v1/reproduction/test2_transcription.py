"""REPRODUCTION.md test 2: the package tables, read back, equal the values recorded by the readings.

Usage (from the repository root): python data/packages/aeg-d-strong-lensing/v1/reproduction/test2_transcription.py

convert.py's assembly is run again in memory (throw-away system IDs, nothing written) on the adjudicated
reading files. The observables are produced in a fixed order, so row i of tables/observables.ecsv must
hold exactly the side, quantity, unit, value and errors of row i in memory, and its x_strong_lensing_printed
column must equal the adjudicated row's printed value, errors, form and unit. In tables/measurements.ecsv,
the columns that carry transcribed numbers (theta_E, z_l, z_s, H0, Omega_m, printed M_E, printed R_E in kpc,
the stellar mass as printed or L and M/L, R_e and n of the light profile) must equal the adjudicated values.
Equality is exact (ECSV stores the float repr). Writes checks/transcription.csv and prints PASS or FAIL.
Version 2 (2026-11-01, after the first run; output kept as checks/transcription_v1.csv) fixes one defect of
this script: read_back returns an empty string cell as None, so the 191 dimensionless redshift rows (unit "")
were counted as unequal. An empty string and None now compare equal for text columns. No value changed.
"""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
ROOT = PKG.parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
spec = importlib.util.spec_from_file_location("a6convert", PKG / "convert.py")
cv = importlib.util.module_from_spec(spec)
sys.modules["a6convert"] = cv
spec.loader.exec_module(cv)
X = cv.X


def same(a, b) -> bool:
    if a in ("", None) and b in ("", None):  # version 2: an empty text cell reads back as None
        return True
    if a is None or (isinstance(a, float) and math.isnan(a)):
        return b is None or (isinstance(b, float) and math.isnan(b))
    if b is None:
        return False
    return a == b if not isinstance(a, float) else float(a) == float(b)


def main() -> int:
    rows, _, _ = cv.load_real_rows()
    res = cv.convert(rows, cv.load_gas_term(), synthetic=True)
    obs = cv.read_back(PKG / "tables/observables.ecsv")
    meas = cv.read_back(PKG / "tables/measurements.ecsv")
    out, bad = [], 0
    if len(obs) != len(res["observables"]) or len(meas) != len(res["measurements"]):
        print(f"test 2: row counts differ (observables {len(obs)} vs {len(res['observables'])}, "
              f"measurements {len(meas)} vs {len(res['measurements'])}): FAIL")
        return 1
    for i, (t, m, r) in enumerate(zip(obs, res["observables"], res["used_rows"])):
        v, lo, hi = cv.value_with_errors(r)
        printed = f"{r['value']} -{r['err_minus']} +{r['err_plus']} [{r.get('form') or 'linear'}; {r.get('unit', '')}]"
        checks = [("side", t["side"], m["side"]), ("quantity", t["quantity"], m["quantity"]), ("unit", t["unit"], m["unit"]),
                  ("value", t["value"], v), ("err_lo", t["err_lo"], lo), ("err_hi", t["err_hi"], hi),
                  ("printed", t[f"{X}printed"], printed)]
        for name, a, b in checks:
            ok = same(a, b)
            bad += not ok
            out.append({"table": "observables", "row": t["observable_id"], "column": name, "table_value": a,
                        "reading_value": b, "equal": "yes" if ok else "no"})
    cols = ("theta_e_arcsec", "z_l", "z_s", "h0", "om", "m_e_msun", "mstar_msun", "l_aperture_lsun", "ml", "r_eff_arcsec", "sersic_n")
    for t, m in zip(meas, res["measurements"]):
        for c in cols:
            if c == "m_e_msun" and m[f"{X}m_e_source"] != "printed":
                continue
            ok = same(t[f"{X}{c}"], m[f"{X}{c}"])
            bad += not ok
            out.append({"table": "measurements", "row": t["measurement_id"], "column": f"{X}{c}", "table_value": t[f"{X}{c}"],
                        "reading_value": m[f"{X}{c}"], "equal": "yes" if ok else "no"})
        if m[f"{X}r_e_source"] == "printed":
            ok = same(t["r_kpc"], m["r_kpc"])
            bad += not ok
            out.append({"table": "measurements", "row": t["measurement_id"], "column": "r_kpc (printed R_E)",
                        "table_value": t["r_kpc"], "reading_value": m["r_kpc"], "equal": "yes" if ok else "no"})
    with open(PKG / "checks/transcription.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    n = len(out)
    print(f"test 2: {n - bad} of {n} table values equal the adjudicated readings: {'PASS' if not bad else 'FAIL'}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
