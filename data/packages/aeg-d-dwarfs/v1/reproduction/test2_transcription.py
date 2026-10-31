"""REPRODUCTION.md test 2: the package tables, read back, equal the checked inputs.

Usage (from the package directory): python reproduction/test2_transcription.py
For every plotted system, the observables table read back from tables/observables.ecsv must
hold exactly the sigma, its errors, the printed r_h, the ellipticity, the m_V,0 (where used),
the distance and the Upsilon_V of reading/conversion_inputs.csv, whose printed inputs test 1
found in the second reading (checks/second_reading.csv).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from astropy.table import Table

PKG = Path(__file__).resolve().parents[1]


def main() -> int:
    obs = Table.read(PKG / "tables/observables.ecsv", format="ascii.ecsv")
    sysn = {r["system_id"]: r["name_in_source"] for r in Table.read(PKG / "tables/systems.ecsv", format="ascii.ecsv")}
    names = {r["key"]: r["name"] for r in csv.DictReader(open(PKG / "reading/kinds.csv", encoding="utf-8"))}
    got = {}
    for r in obs:
        got.setdefault((sysn[r["system_id"]], r["quantity"]), []).append(r)
    bad, n = [], 0
    for r in csv.DictReader(open(PKG / "reading/conversion_inputs.csv", encoding="utf-8")):
        if r.get("status") != "plotted" or float(r["sigma"]) == 0.0:
            continue
        nm = names[r["key"]]
        checks = [("sigma_los", "value", r["sigma"]), ("half_light_radius", "value", r["rh_printed"]),
                  ("structural_param", "value", r["ellipticity"]), ("distance", "value", r["distance_kpc"]),
                  ("stellar_ml_population", "value", r["upsilon_v"]), ("luminosity", "value", r["L_V"])]
        if r["sigma_limit"] != "upper":
            checks += [("sigma_los", "err_lo", r["sigma_err_minus"]), ("sigma_los", "err_hi", r["sigma_err_plus"])]
        if r.get("m_V0"):
            checks.append(("apparent_magnitude", "value", r["m_V0"]))
        for q, c, v in checks:
            if v in ("", None):
                continue
            n += 1
            rows = got.get((nm, q), [])
            if not any(float(x[c]) == float(v) for x in rows if str(x[c]) not in ("", "--")):
                bad.append((nm, q, c, v))
    print(f"test 2: {n - len(bad)} of {n} values equal: {'PASS' if not bad else 'FAIL'} {bad[:5]}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
