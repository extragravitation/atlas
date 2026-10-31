"""D-062 item 2 applied to reading/conversion_inputs.csv (Pegasus IV circularised radius).

Usage (from the package directory), after reproduction/inputs.py:
    python reproduction/inputs_d062.py
Frozen before it was run. Cerny et al. 2023 Table 1 prints the azimuthally averaged r_h =
1.55 (+0.29/-0.24) arcmin (both readings, reading/structure_values_all.csv); the ellipticity is
only an upper limit (< 0.41). The row's printed r_h, convention and R_h are replaced; nothing
else changes. (D-062 item 1, And XII, is applied in convert.py.)
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
P = PKG / "reading/conversion_inputs.csv"


def main() -> int:
    rows = list(csv.DictReader(open(P, encoding="utf-8")))
    hit = 0
    for r in rows:
        if r["key"] == "pegasus_4":
            r.update(rh_printed="1.55", rh_unit="arcmin", rh_convention="circularised", R_h_arcmin="1.55",
                     rh_source="Cerny2023ApJ...942..111C p.7, Table 1 (azimuthally averaged r_h; D-062 item 2)")
            r["flags"] = " ".join(x for x in r["flags"].split() if x != "rh_semimajor_assumed")
            hit += 1
    if hit != 1:
        raise SystemExit("pegasus_4 not found once")
    with open(P, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("D-062 item 2 applied: pegasus_4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
