"""Compare the two independent readings of Putman et al. 2021 Table 1 -> reading/gas_comparison.csv.

Usage (from the package directory):
    python reproduction/compare_gas_readings.py reading/gas_reading_1.csv reading/gas_reading_2.csv
Written before either reading was seen. One row per system key; every copied field is
compared as stored text after trimming spaces. A system agrees only if every field agrees.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
FIELDS = ["galaxy_as_printed", "f_Galaxy", "Vel", "Dist", "e_Dist", "E_Dist", "Data", "Method", "sigHI",
          "l_MHI", "MHI", "e_MHI", "E_MHI", "r_Dist"]


def load(p: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in csv.DictReader(open(p, encoding="utf-8")):
        if r["key"] in out:
            raise SystemExit(f"{p}: duplicate key {r['key']}")
        out[r["key"]] = r
    return out


def main(a: str, b: str) -> int:
    A, B = load(a), load(b)
    rows, n_agree = [], 0
    for k in sorted(set(A) | set(B)):
        ra, rb = A.get(k, {}), B.get(k, {})
        diff = [f for f in FIELDS if (ra.get(f) or "").strip() != (rb.get(f) or "").strip()]
        if not ra or not rb:
            diff = ["missing in " + ("1" if not ra else "2")]
        n_agree += not diff
        rows.append({"key": k, "agree": "yes" if not diff else "no", "fields_differing": ";".join(diff),
                     **{f"{f}_1": (ra.get(f) or "").strip() for f in FIELDS},
                     **{f"{f}_2": (rb.get(f) or "").strip() for f in FIELDS}})
    with open(PKG / "reading/gas_comparison.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} systems; agree {n_agree}; disagree {len(rows) - n_agree}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
