"""Compare the two independent metallicity readings (D-057) and the two Woo 2008 readings.

Usage (from the package directory):
    python reproduction/compare_feh_readings.py feh reading/feh_reading_1.csv reading/feh_reading_2.csv
    python reproduction/compare_feh_readings.py woo reading/woo_reading_1.csv reading/woo_reading_2.csv
Written before either reading was seen. Output: reading/<kind>_comparison.csv.

A printed value is identified by (key, paper, quantity, value) for feh, and by
(key, quantity-like column, value) for woo, with values compared as numbers where both parse,
otherwise as trimmed text. Each value found by one reader only is listed. For feh, the value
each reader marked "headline" is also compared per (key, paper): differing headline sets are
a disagreement even when both readers recorded the same values.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]


def num(x: str) -> str:
    t = (x or "").strip().replace("−", "-").replace("–", "-").replace(" ", "")
    try:
        return repr(float(t))
    except ValueError:
        return t


def load(p: str, kind: str) -> list[dict]:
    return [r for r in csv.DictReader(open(p, encoding="utf-8"))]


def ident(r: dict, kind: str) -> tuple:
    q = (r.get("quantity") or "").strip().lower()
    if kind == "feh":
        return (r["key"], (r.get("paper") or "").strip(), q, num(r.get("value", "")))
    return (r["key"], q, num(r.get("value", "")))


def main(kind: str, a: str, b: str) -> int:
    A, B = load(a, kind), load(b, kind)
    ia = {ident(r, kind): r for r in A}
    ib = {ident(r, kind): r for r in B}
    rows = []
    for k in sorted(set(ia) | set(ib), key=str):
        ra, rb = ia.get(k), ib.get(k)
        status = "both" if ra and rb else ("reader 1 only" if ra else "reader 2 only")
        rows.append({"id": " | ".join(k), "status": status,
                     "variant_1": (ra or {}).get("variant", ""), "variant_2": (rb or {}).get("variant", ""),
                     "location_1": (ra or {}).get("location", ""), "location_2": (rb or {}).get("location", "")})
    if kind == "feh":
        def heads(rs: list[dict]) -> dict:
            d: dict = {}
            for r in rs:
                if (r.get("variant") or "").strip().lower().startswith("headline") and r.get("quantity", "").startswith("feh_m"):
                    d.setdefault((r["key"], r.get("paper", "").strip()), set()).add(num(r["value"]))
            return d
        ha, hb = heads(A), heads(B)
        for k in sorted(set(ha) | set(hb)):
            if ha.get(k) != hb.get(k):
                rows.append({"id": " | ".join(k) + " | headline", "status": "headline differs",
                             "variant_1": ";".join(sorted(ha.get(k, []))), "variant_2": ";".join(sorted(hb.get(k, []))),
                             "location_1": "", "location_2": ""})
    with open(PKG / f"reading/{kind}_comparison.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    c = {s: sum(1 for r in rows if r["status"] == s) for s in ("both", "reader 1 only", "reader 2 only", "headline differs")}
    print(f"{kind}: {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
