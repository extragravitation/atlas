"""Compare the two independent gas readings (part G of GAS_AND_SUPPLEMENT_BRIEF.md v2).

Written after the readings were copied into the repository and before any value
in them was looked at by Claude. Rows are keyed by (candidate, normalised galaxy
name, quantity, radius as printed). Values are compared as printed (decimal
equality, same limit type). Rows in only one reading are listed. The readings
are not changed.
Usage: python compare_gas.py <a.csv> <b.csv> <out.csv>
"""
import csv
import re
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation


def n(s):
    s = (s or "").strip().replace("−", "-").replace("×10^", "e").replace("x10^", "e")
    m = re.match(r"^[<>~≈]?\s*(-?[\d.]+(?:e-?\d+)?)", s)
    try:
        return Decimal(m.group(1)) if m else None
    except InvalidOperation:
        return None


def gid(s):
    return re.sub(r"[\s_\-]", "", (s or "")).upper()


def load(p):
    d = defaultdict(list)
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            k = (r.get("candidate", "").strip(), gid(r.get("galaxy")), r.get("quantity", "").strip(),
                 str(n(r.get("radius_value"))), (r.get("radius_unit") or "").strip())
            d[k].append((n(r.get("value")), (r.get("limit") or "").strip(), (r.get("form") or "linear").strip() or "linear"))
    return d


def main(a, b, out):
    A, B = load(a), load(b)
    st = defaultdict(int)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["candidate", "galaxy", "quantity", "radius", "radius_unit", "a", "b", "status"])
        for k in sorted(set(A) | set(B)):
            va, vb = sorted(A.get(k, []), key=str), sorted(B.get(k, []), key=str)
            s = "only_a" if k not in B else "only_b" if k not in A else ("agree" if va == vb else "differ")
            st[s] += 1
            w.writerow([*k, va, vb, s])
    print(dict(st))


if __name__ == "__main__":
    main(*sys.argv[1:4])
