"""Compare the structure/distance/magnitude readings, version 2.

Version 1 (compare_structure_readings.py) compared every row, including the prose
quantities `method`, `band_note` and `profile`, and compared coordinates as printed
strings. Readers wrote these differently ("RR Lyrae, PWZ relation" vs "RR Lyrae,
period-Wesenheit-metallicity relations"; "0h45m39.7s" vs "04539.7"), so 280 of 305 pairs
differed. Version 1 was not changed after it was run. Its output is kept
(reading/structure_comparison_v1.csv).

Version 2 changes two things:
- It compares the numeric quantities only: ra0, dec0, ellipticity, pa, r_h,
  distance_modulus, distance, m_v, M_V, extinction, luminosity.
- It compares coordinates by their digit sequence: the digits and the decimal point,
  ignoring separators and unit symbols.

Prose quantities are checked by the adjudicator only where a rule uses them. The distance
method is checked for every distance used (D-036 #6).

Usage: python reproduction/compare_structure_readings_v2.py READING1_DIR READING2_DIR OUT_CSV
"""

from __future__ import annotations

import csv
import glob
import re
import sys
from collections import defaultdict

NUMERIC = {"ra0", "dec0", "ellipticity", "pa", "r_h", "distance_modulus", "distance", "m_v", "M_V", "extinction", "luminosity"}


def norm(x: str) -> str:
    x = (x or "").strip().replace("−", "-").replace("–", "-").replace(" ", "")
    return x[1:] if x.startswith("+") else x


def coord(x: str) -> str:
    sign = "-" if x.strip().startswith(("-", "−")) else ""
    return sign + re.sub(r"[^0-9.]", "", x)


def load(d: str) -> dict:
    out = defaultdict(list)
    for f in sorted(glob.glob(f"{d}/sheet*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            q = r.get("quantity", "").strip()
            if q not in NUMERIC or not (r.get("value") or "").strip():
                continue
            if q in ("ra0", "dec0"):
                t = (q, coord(r["value"]), coord(r.get("err_minus", "")), coord(r.get("err_plus", "")))
            else:
                t = (q, norm(r["value"]), norm(r.get("err_minus", "")), norm(r.get("err_plus", "")))
            out[(r["key"].strip(), r["paper"].strip(), r["role"].strip())].append(t)
    return out


def main(a: str, b: str, out_csv: str) -> int:
    r1, r2 = load(a), load(b)
    rows, counts = [], defaultdict(int)
    for k in sorted(set(r1) | set(r2)):
        s1, s2 = sorted(set(r1.get(k, []))), sorted(set(r2.get(k, [])))
        st = "only_2" if k not in r1 else "only_1" if k not in r2 else "agree" if s1 == s2 else "disagree"
        counts[st] += 1
        rows.append({"key": k[0], "paper": k[1], "role": k[2], "status": st,
                     "reading_1": " | ".join("/".join(t) for t in s1), "reading_2": " | ".join("/".join(t) for t in s2)})
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["key", "paper", "role", "status", "reading_1", "reading_2"])
        w.writeheader()
        w.writerows(rows)
    print(dict(counts))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
