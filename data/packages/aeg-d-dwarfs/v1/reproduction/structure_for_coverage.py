"""D-051 item 1: the structural values the coverage check uses -> reading/structure_values.csv.

Usage (from the package directory): python reproduction/structure_for_coverage.py

Input: reading/structure_selection.csv (D-052, selection v3). For each system:
- centre: ra0, dec0, parsed from degrees or sexagesimal ("hms"/"dms"; separators h m s,
  colon, space, degree, prime and double prime; Unicode minus);
- ellipticity: as selected (blank counts as 0);
- position angle in degrees (blank counts as 0; it has no effect when e = 0);
- semi-major half-light radius in arcmin. Where the selected r_h is circularised,
  a_h = r_h / sqrt(1 - e) (the inverse of REPRODUCTION.md's R_h = a sqrt(1 - e)). Values in
  arcsec are divided by 60. A system with no angular radius, or no centre, is written with
  status "not available" and its coverage is "not checkable".
"""

from __future__ import annotations

import csv
import math
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]


def lead(x: str) -> float | None:
    m = re.match(r"\s*([-+]?\d+(?:\.\d+)?)", (x or "").replace("−", "-"))
    return float(m.group(1)) if m else None


def sexa(x: str, hours: bool) -> float | None:
    t = (x or "").replace("−", "-").strip()
    if not t:
        return None
    neg = t.startswith("-")
    parts = re.findall(r"\d+(?:\.\d+)?", t)
    if len(parts) < 2:
        return None
    vals = [float(p) for p in parts[:3]] + [0.0] * (3 - len(parts[:3]))
    v = vals[0] + vals[1] / 60.0 + vals[2] / 3600.0
    v *= 15.0 if hours else 1.0
    return -v if neg else v


def coord(x: str, unit: str, hours: bool) -> float | None:
    if unit in ("hms", "dms"):
        return sexa(x, hours)
    return lead(x)


def main() -> int:
    out = []
    for r in csv.DictReader(open(PKG / "reading/structure_selection.csv", encoding="utf-8")):
        ra = coord(r["ra0"], r["ra0_unit"], True)
        dec = coord(r["dec0"], r["dec0_unit"], False)
        e = lead(r["ellipticity"]) or 0.0
        pa = lead(r["pa"]) or 0.0
        rh = lead(r["r_h"])
        unit = r["r_h_unit"]
        a = None
        if rh is not None and unit in ("arcmin", "arcsec"):
            rh_arcmin = rh / 60.0 if unit == "arcsec" else rh
            a = rh_arcmin / math.sqrt(1.0 - e) if r["rh_convention"].startswith("circularised") else rh_arcmin
        missing = [n for n, v in (("centre", ra if dec is not None else None), ("angular r_h", a)) if v is None]
        out.append({"key": r["key"], "ra0_deg": f"{ra:.6f}" if ra is not None else "", "dec0_deg": f"{dec:.6f}" if dec is not None else "",
                    "ellipticity": f"{e:.4f}", "pa_deg": f"{pa:.2f}", "a_h_arcmin": f"{a:.5f}" if a is not None else "",
                    "rh_convention": r["rh_convention"], "status": "ok" if not missing else "not available: " + ", ".join(missing)})
    # coverage_from_tables.py reads every row as numbers, so only complete rows go in its input.
    for name, rows in (("structure_values.csv", [r for r in out if r["status"] == "ok"]),
                       ("structure_values_unavailable.csv", [r for r in out if r["status"] != "ok"])):
        with open(PKG / "reading" / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(rows)
    print(f"{len(out)} systems; complete {sum(1 for r in out if r['status'] == 'ok')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
