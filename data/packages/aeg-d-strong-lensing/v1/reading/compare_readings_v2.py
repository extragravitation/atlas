"""Comparison v2 for the A6 input readings.

Written after the v1 output (compare_readings.py) was seen, and before any
adjudication. Disclosed in the adjudication file. v1 is kept as committed, and its
output is kept. v1 keyed stellar-mass rows by the free-text note, and treated a
blank `form` as different from "linear", so rows with equal values went unmatched.
v2 changes only the matching:
- a blank `form` counts as "linear";
- record-level rows (system_id in parentheses) share one key per record;
- `mstar` rows are compared per (system, record) as multisets of
  (value, err_minus, err_plus, form, limit), so the readers' different note wording
  does not matter;
- every other numeric quantity is compared on the value tuple, as in v1.
Usage: python compare_readings_v2.py <a.csv> <b.csv> <out.csv>
"""
import csv
import re
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation

NUMERIC = {"z_l", "z_s", "theta_E", "M_E", "H0", "Om", "mstar", "R_e", "sersic_n", "component_share"}


def norm_id(s):
    s = (s or "").strip()
    if s.startswith("("):
        return "(RECORD)"
    return re.sub(r"[\s_\-−–+]", "", s).upper().replace("SDSSJ", "J")


def num(s):
    s = (s or "").strip().replace("−", "-")
    m = re.match(r"^-?[\d.]+(e-?\d+)?", s)
    try:
        return Decimal(m.group(0)) if m else None
    except InvalidOperation:
        return None


def tup(r):
    return (num(r.get("value")), num(r.get("err_minus")), num(r.get("err_plus")),
            (r.get("form") or "linear").strip() or "linear", (r.get("limit") or "").strip())


def load(p):
    d = defaultdict(list)
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            q = r["quantity"].strip()
            if q in NUMERIC:
                d[(r["scope"].strip(), norm_id(r["system_id"]), r["record"].strip(), q)].append(tup(r))
    return d


def main(a, b, out):
    A, B = load(a), load(b)
    keys = sorted(set(A) | set(B))
    stats = defaultdict(int)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["scope", "system", "record", "quantity", "a", "b", "status"])
        for k in keys:
            va, vb = sorted(A.get(k, []), key=str), sorted(B.get(k, []), key=str)
            if k not in A or k not in B:
                st = "only_a" if k in A else "only_b"
            elif k[3] == "mstar":
                st = "agree" if va == vb else ("a_subset" if set(va) < set(vb) else "b_subset" if set(vb) < set(va) else "differ")
            else:
                st = "agree" if va == vb else "differ"
            stats[st] += 1
            w.writerow([*k, ";".join(map(str, va)), ";".join(map(str, vb)), st])
    print(dict(stats))


if __name__ == "__main__":
    main(*sys.argv[1:4])
