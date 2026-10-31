"""REPRODUCTION.md test 1: every packaged input number equals the original as printed.

Usage (from the package directory): python reproduction/test1_second_reading.py
Written before the second reading was seen. Inputs: reading/second_reading_{a,b}.csv (the
two halves of the sheet), reading/conversion_inputs.csv and reading/structure_selection.csv.

For each sheet row, the package's printed input values for that block must each be found,
as a number, among the values the second reader recorded for that key, block and paper:
  sigma      sigma; its printed errors (if any); the limit flag for an upper limit
  structure  the printed r_h and the ellipticity
  distance   the printed distance or modulus the package used (each end of a range for Leo I)
  magnitude  the printed m_V,0, or the printed M_V and the modulus or distance used with it
Version 2 (2026-10-31, after the first run, output kept as checks/second_reading_v1.csv) fixes
three defects of this script, none of which changes a package value: (1) a paper modulus stored
as "x +- y" was not parsed, so its expected value was empty; (2) an ellipticity the paper does not
print (package default 0, circular) was still expected; (3) Tucana's r_h is printed in pc (205)
and the package's angle is derived from it, so the printed 205 is what is checked. It also reads
reading/second_reading_{a,b}_followup.csv, targeted re-reads of three rows. Version 2 also (4)
checks an ellipticity printed only as an upper limit (package uses 0) against the printed limit,
and (5) for the modulus behind M_V, accepts the number among the second reader's values for the
same key and paper in any block: test 1 checks transcription; which modulus M_V used is an
interpretation from the adjudicated supplementary reading, and disagreements about it are listed
in SECOND_READING.md.
After D-062 (And XII plotted) four And XII rows were added to the sheet and read by the same
reader (reading/second_reading_a2.csv).
Numbers compare after trimming signs and trailing zeros (float equality). Writes
checks/second_reading.csv (one row per checked number) and prints PASS or FAIL.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]


def f(x):
    import re
    m = re.match(r"\s*[~≃<+]?\s*([-+]?\d+(?:\.\d+)?)", str(x or "").replace("−", "-").replace("–", "-"))
    return float(m.group(1)) if m else None


def expected(r: dict, s: dict, block: str) -> list[tuple[str, float]]:
    k = r["key"]
    if block == "sigma":
        out = [("sigma", f(r["sigma"]))]
        if r["sigma_limit"] != "upper":
            out += [(n, f(r[c])) for n, c in (("err_minus", "sigma_err_minus"), ("err_plus", "sigma_err_plus")) if f(r[c]) is not None]
        return out
    if block == "structure":
        if k == "tucana_1":
            return [("r_h", 205.0), ("ellipticity", 0.48)]
        out = [("r_h", f(r["rh_printed"]))]
        if s["ellipticity"].strip().startswith("<") and k != "bootes_3":
            out.append(("ellipticity_limit", f(s["ellipticity"])))
        elif k == "bootes_3" or s["ellipticity"].strip():
            out.append(("ellipticity", f(r["ellipticity"])))
        return out
    if block == "distance":
        if k == "leo_1":
            return [("distance_modulus", 22.06), ("distance_modulus", 22.25)]
        over = {"leo_4": 151.4, "leo_5": 169.0, "segue_2": 34.4, "tucana_1": 24.74}
        return [("distance", over[k])] if k in over else [("distance", f(s["distance"]))]
    if block == "magnitude":
        over = {"andromeda_06": [-11.5, 24.47], "andromeda_07": [-13.3, 24.41], "phoenix_1": [-9.9, 23.1],
                "leo_t": [-8.0, 23.1], "tucana_5": [-1.1, 55.0], "tucana_1": [-9.55, 24.69], "bootes_3": [-5.8]}
        if k in over:
            return [("magnitude", v) for v in over[k]]
        if s["m_V0_route"].startswith("printed"):
            return [("m_V0", f(s["m_V0"]))]
        out = [("M_V", f(s["M_V"]))]
        if s["mu_paper"].strip():
            out.append(("mv_modulus", f(s["mu_paper"])))
        elif "Munoz" in r["mag_source"]:
            out.append(("mv_distance", f(r["mag_source"].split("D = ")[1].split(" kpc")[0])))
        return out
    return []


def main() -> int:
    read = []
    for h in ("a", "b", "a_followup", "b_followup", "a2"):
        read += list(csv.DictReader(open(PKG / f"reading/second_reading_{h}.csv", encoding="utf-8")))
    inp = {r["key"]: r for r in csv.DictReader(open(PKG / "reading/conversion_inputs.csv", encoding="utf-8"))}
    st = {r["key"]: r for r in csv.DictReader(open(PKG / "reading/structure_selection.csv", encoding="utf-8"))}
    sheet = list(csv.DictReader(open(PKG / "reading/second_reading_sheet.csv", encoding="utf-8")))
    rows, bad = [], 0
    for sh in sheet:
        k, b, p = sh["key"], sh["block"], sh["paper"]
        got = [x for x in read if x["key"] == k and x["block"] == b]
        nums = set()
        for x in got:
            for c in ("value", "err_minus", "err_plus"):
                v = f(x.get(c))
                if v is not None:
                    nums.add(abs(v))
        allp = set()
        for x in read:
            if x["key"] == k and x["paper"].strip() == p.strip():
                for c in ("value", "err_minus", "err_plus"):
                    v = f(x.get(c))
                    if v is not None:
                        allp.add(abs(v))
        for name, v in expected(inp[k], st[k], b):
            pool = nums | allp if name in ("mv_modulus", "mv_distance") else nums
            ok = v is not None and abs(v) in pool
            bad += not ok
            rows.append({"key": k, "block": b, "paper": p, "number": name, "package_value": v, "found": "yes" if ok else "no"})
        if b == "sigma" and inp[k]["sigma_limit"] == "upper":
            ok = any(x.get("limit", "").strip() == "upper" for x in got)
            bad += not ok
            rows.append({"key": k, "block": b, "paper": p, "number": "limit", "package_value": "upper", "found": "yes" if ok else "no"})
    (PKG / "checks").mkdir(exist_ok=True)
    with open(PKG / "checks/second_reading.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"test 1: {len(rows) - bad} of {len(rows)} package numbers found in the second reading: {'PASS' if bad == 0 else 'FAIL'}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
