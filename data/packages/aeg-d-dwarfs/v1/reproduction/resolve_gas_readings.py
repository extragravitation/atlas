"""Putman et al. 2021 Table 1 readings -> reading/gas_values.csv (one row per system).

Usage (from the package directory): python reproduction/resolve_gas_readings.py
Takes the rows on which both readings agree (reading/gas_comparison.csv), then applies the
adjudication in reading/gas_adjudication.md: Cassiopeia II is read from the row
"Andromeda XXX" (both follow-up readings, which must agree field by field). Systems both
readers found absent from the table are written with status "not in Putman 2021".
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_gas_readings import FIELDS  # noqa: E402

COLS = ["key", "status"] + FIELDS


def main() -> int:
    r1 = {r["key"]: r for r in csv.DictReader(open(PKG / "reading/gas_reading_1.csv", encoding="utf-8"))}
    f1 = {r["key"]: r for r in csv.DictReader(open(PKG / "reading/gas_reading_1_followup.csv", encoding="utf-8"))}
    f2 = {r["key"]: r for r in csv.DictReader(open(PKG / "reading/gas_reading_2_followup.csv", encoding="utf-8"))}
    for k in f1:
        bad = [f for f in FIELDS if f1[k][f].strip() != f2[k][f].strip()]
        if bad:
            raise SystemExit(f"follow-up readings disagree for {k}: {bad}")
    out = []
    for c in csv.DictReader(open(PKG / "reading/gas_comparison.csv", encoding="utf-8")):
        k = c["key"]
        if k in f1:
            src, status = f1[k], "in table (adjudicated identification)"
        elif c["agree"] == "yes":
            src, status = r1[k], "in table"
        elif not c["galaxy_as_printed_1"] and c["galaxy_as_printed_2"] in ("", "NOT_IN_TABLE"):
            src, status = {}, "not in Putman 2021"
        else:
            raise SystemExit(f"unresolved disagreement for {k}")
        out.append({"key": k, "status": status, **{f: (src.get(f) or "").strip() for f in FIELDS}})
    with open(PKG / "reading/gas_values.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(out)
    n = {s: sum(1 for r in out if r["status"] == s) for s in {r["status"] for r in out}}
    print(f"{len(out)} systems; {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
