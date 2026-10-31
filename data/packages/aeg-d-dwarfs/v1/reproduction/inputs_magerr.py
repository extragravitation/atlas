"""Printed errors of a printed m_V,0, carried into reading/conversion_inputs.csv.

Usage (from the package directory), after reproduction/inputs_v2.py and inputs_d062.py:
    python reproduction/inputs_magerr.py
Frozen before it was run. The input assembly (inputs.py, inputs_v2.py) took the error of the
magnitude only on the M_V route; where the paper prints m_V,0 itself (route "printed m_V,0"),
its printed error was left out, so g_bar had no magnitude error. This step fills it from the
double-read structure readings (reading/structure_values_all.csv): the row of the same system,
paper and value with quantity m_v; among several, the headline rows, then the table printing
(D-051 duplicate rule). The match must be unique, else the step stops. Nothing else changes.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
P = PKG / "reading/conversion_inputs.csv"


def num(x: str) -> float:
    return float(x.replace("−", "-"))


def main() -> int:
    rows = list(csv.DictReader(open(P, encoding="utf-8")))
    sv = list(csv.DictReader(open(PKG / "reading/structure_values_all.csv", encoding="utf-8")))
    n = 0
    for r in rows:
        if r.get("status") != "plotted" or not r.get("mag_source", "").startswith("printed m_V,0") or r.get("mag_err_minus"):
            continue
        bib = r["mag_source"].split("(", 1)[1].split(" ")[0]
        m = [x for x in sv if x["key"] == r["key"] and x["paper"] == bib and x["quantity"] == "m_v"
             and x["value"].strip() and abs(num(x["value"]) - float(r["m_V0"])) < 1e-9]
        m = [x for x in m if x["variant"].strip().lower().startswith("headline")] or m
        m = [x for x in m if "table" in x["location"].lower()] or m
        if len({(x["err_minus"], x["err_plus"]) for x in m}) != 1:
            raise SystemExit(f"{r['key']}: no unique printed m_V,0 row: {[(x['err_minus'], x['err_plus']) for x in m]}")
        r["mag_err_minus"], r["mag_err_plus"] = m[0]["err_minus"].strip(), m[0]["err_plus"].strip()
        n += 1
    with open(P, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"printed m_V,0 errors carried: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
