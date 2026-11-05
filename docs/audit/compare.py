"""Audit comparison (plan v2 §2.7, §2.10). Written and committed before any reading is opened.

Usage:
    python docs/audit/compare.py READINGS_DIR [REPO_ROOT]

READINGS_DIR holds one folder per reader (`a`, `b`). Each holds, per stratum, a folder named
after the package (`aeg-d-sparc_v1`, ...) containing:
    values.csv   measurement_id, g_obs, g_bar, status, notes
                 status is "ok", "method incomplete" or "unreadable"; g in m s^-2
    inputs.csv   measurement_id, input, value, unit, locator

Writes READINGS_DIR/comparison.csv (one row per sampled measurement) and prints the
counts per stratum and code. Standard library only.

Codes (§2.7):
    agree                 both readers agree with each other and with the Atlas
    reader disagreement   the readers differ from each other (accelerations or a shared input)
    Atlas discrepancy     the readers agree with each other but not with the Atlas
    method incomplete     a reader recorded that the written method was not enough
    unreadable            a reader could not read a value
    missing               a reader returned no row for a sampled measurement

Tolerances (§2.7): accelerations |Δ log10 g| <= 0.005 dex; inputs equal at the printed
precision (compared as numbers when both parse, otherwise as stripped text), for inputs that
both readers name identically. Inputs named by only one reader are listed, not compared.
"""

from __future__ import annotations

import csv
import io
import math
import sys
from pathlib import Path

TOL_DEX = 0.005
READERS = ("a", "b")


def read_ecsv_rows(path: Path) -> list[dict]:
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if not ln.startswith("#")]
    return list(csv.DictReader(io.StringIO("\n".join(lines))))


def folder(stratum: str) -> str:
    return stratum.replace("/", "_")


def num(x):
    try:
        v = float(str(x).strip())
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def dex(x, y):
    a, b = num(x), num(y)
    if a is None or b is None or a <= 0 or b <= 0:
        return None
    return abs(math.log10(a) - math.log10(b))


def same_input(x: str, y: str) -> bool:
    a, b = num(x), num(y)
    if a is not None and b is not None:
        return a == b
    return str(x).strip().lower() == str(y).strip().lower()


def load_reader(rdir: Path):
    vals, inps = {}, {}
    vp, ip = rdir / "values.csv", rdir / "inputs.csv"
    if vp.exists():
        for r in csv.DictReader(vp.open(encoding="utf-8")):
            vals[r["measurement_id"].strip()] = r
    if ip.exists():
        for r in csv.DictReader(ip.open(encoding="utf-8")):
            inps.setdefault(r["measurement_id"].strip(), {})[r["input"].strip()] = r.get("value", "")
    return vals, inps


def clopper_pearson_upper(x: int, n: int, conf: float = 0.95) -> float:
    """Upper limit of the two-sided Clopper-Pearson interval: p with P(X <= x | n, p) = (1 - conf)/2."""
    if n == 0:
        return 1.0
    if x >= n:
        return 1.0
    alpha = (1 - conf) / 2

    def cdf(p):
        return sum(math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(x + 1))

    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cdf(mid) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main(argv):
    rd = Path(argv[1])
    root = Path(argv[2]) if len(argv) > 2 else Path(__file__).resolve().parents[2]
    sample = [r for r in csv.DictReader((root / "docs/audit/run_v2/sample.csv").open()) if r["status"] == "sample"]
    strata = sorted({r["stratum"] for r in sample}, key=lambda s: [r["stratum"] for r in sample].index(s))
    out = []
    for st in strata:
        atlas = {r["measurement_id"]: r for r in read_ecsv_rows(root / "data/packages" / st / "tables/measurements.ecsv")}
        rv = {k: load_reader(rd / k / folder(st)) for k in READERS}
        for s in (r for r in sample if r["stratum"] == st):
            mid = s["measurement_id"]
            A = atlas[mid]
            va = {k: rv[k][0].get(mid) for k in READERS}
            ia = {k: rv[k][1].get(mid, {}) for k in READERS}
            notes = []
            if any(v is None for v in va.values()):
                code = "missing"
                notes.append("no row from " + ",".join(k for k in READERS if va[k] is None))
            else:
                st_ = {k: (va[k].get("status") or "ok").strip().lower() for k in READERS}
                if "method incomplete" in st_.values():
                    code = "method incomplete"
                elif "unreadable" in st_.values():
                    code = "unreadable"
                else:
                    d_obs = dex(va["a"]["g_obs"], va["b"]["g_obs"])
                    d_bar = dex(va["a"]["g_bar"], va["b"]["g_bar"])
                    shared = sorted(set(ia["a"]) & set(ia["b"]))
                    diff_inputs = [n for n in shared if not same_input(ia["a"][n], ia["b"][n])]
                    only = sorted(set(ia["a"]) ^ set(ia["b"]))
                    if only:
                        notes.append("inputs named by one reader only: " + "; ".join(only))
                    if d_obs is None or d_bar is None or d_obs > TOL_DEX or d_bar > TOL_DEX or diff_inputs:
                        code = "reader disagreement"
                        if diff_inputs:
                            notes.append("inputs differ: " + "; ".join(diff_inputs))
                    else:
                        ga = {q: dex(va["a"][q], A[q]) for q in ("g_obs", "g_bar")}
                        gb = {q: dex(va["b"][q], A[q]) for q in ("g_obs", "g_bar")}
                        bad = [q for q in ("g_obs", "g_bar") if ga[q] is None or gb[q] is None or ga[q] > TOL_DEX or gb[q] > TOL_DEX]
                        code = "Atlas discrepancy" if bad else "agree"
                        if bad:
                            notes.append("differs from Atlas on " + ",".join(bad))
            out.append({
                "stratum": st, "measurement_id": mid, "code": code,
                "atlas_g_obs": A["g_obs"], "atlas_g_bar": A["g_bar"],
                "a_g_obs": (va["a"] or {}).get("g_obs", ""), "a_g_bar": (va["a"] or {}).get("g_bar", ""),
                "b_g_obs": (va["b"] or {}).get("g_obs", ""), "b_g_bar": (va["b"] or {}).get("g_bar", ""),
                "a_status": (va["a"] or {}).get("status", ""), "b_status": (va["b"] or {}).get("status", ""),
                "notes": " | ".join(notes),
            })
    with (rd / "comparison.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    codes = ["agree", "reader disagreement", "Atlas discrepancy", "method incomplete", "unreadable", "missing"]
    print("stratum," + ",".join(codes) + ",n")
    for st in strata + ["all"]:
        rows = [o for o in out if st == "all" or o["stratum"] == st]
        print(st + "," + ",".join(str(sum(o["code"] == c for o in rows)) for c in codes) + f",{len(rows)}")


if __name__ == "__main__":
    main(sys.argv)
