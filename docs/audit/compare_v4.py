"""Audit v4 comparison and verdict (plan v4 §2.7, §2.8, §2.10, D-125; from compare_v3.py, D-116).

Written and committed before the audit seed exists and before any audit reading is opened
(trigger bed8da2; seed due 2026-11-26T15:04:20Z). Standard library only.

Usage:
    python docs/audit/compare_v4.py compare READINGS_DIR SAMPLE_CSV [REPO_ROOT]
    python docs/audit/compare_v4.py verdict RUN_DIR

READINGS_DIR holds one folder per reader, `a`, `b` and, for the third reader of §2.8, `c`.
Each holds one folder per package (`aeg-d-sparc`, ...) with the reader's out/ files:
    values.csv   measurement_id, g_obs, g_bar, notes                (brief §2.6)
    inputs.csv   measurement_id, input, value, unit, file, place, at_locator

Reading a reader's row (fixed here, before any reading):
- status "method incomplete" if its notes contain "method incomplete" (any case);
  otherwise "unreadable" if they contain "unreadable"; otherwise "ok".
- a value is "given" if it parses as a finite positive number.

Codes per row (§2.7), in this order of precedence:
    missing               a reader (a or b) returned no row
    method incomplete     either reader recorded it
    unreadable            either reader recorded it
    reader disagreement   the readers differ: |Δ log10 g| > 0.005 dex on g_obs or g_bar, or a value
                          not given, or a shared input (same name after normalising: lower case,
                          letters and digits only) differs: compared as the first number in each
                          value where both have one (readers may add errors or notes after the
                          printed value), otherwise as stripped text
    Atlas discrepancy     the readers agree with each other but not with the Atlas (> 0.005 dex)
    agree                 otherwise

Method gaps (§2.8): a "method incomplete" row is blocking if a reader who recorded it gave no
value, or a value more than 0.005 dex from the Atlas on g_obs or g_bar; otherwise non-blocking.

Third reader (§2.8): for a "reader disagreement" row, if reader c has a row, the values that two
of a, b, c agree on (within 0.005 dex on both g) are taken; the row is then coded against the
Atlas as "agree (2 of 3)" or "Atlas discrepancy (2 of 3)". If c has no row yet, or no two agree,
the row is "reader disagreement, unresolved" and goes to Claude's adjudication at source.

Verdict (§2.10), from RUN_DIR/comparison.csv, RUN_DIR/provenance.csv and
RUN_DIR/adjudication.csv (measurement_id, outcome, by, note; outcome one of "material
discrepancy", "reader error", "not verified", "agree", "provenance failure", "provenance
confirmed"; one row per measurement, so a row needing both kinds of adjudication records the
worse outcome):
    decision counts   material discrepancies (adjudication), provenance failures (provenance.csv
                      result "fail"), blocking method gaps (comparison)
    pass              every decision count's 95 % Clopper-Pearson upper bound <= 2.5 %, and no
                      row not verified
    fail              any decision count's upper bound > 2.5 %
    incomplete        no count fails, but some rows are not verified
    strict verdict    pass only if every count, blocking or not, is zero and no row is unverified
A row that is an Atlas discrepancy or unresolved and has no adjudication yet makes the verdict
"incomplete (adjudication pending)": nothing is counted as passed by default.
"""

from __future__ import annotations

import csv
import io
import math
import re
import sys
from pathlib import Path

TOL_DEX = 0.005
THRESHOLD = 0.025
READERS = ("a", "b")


def read_ecsv_rows(path: Path) -> list[dict]:
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if not ln.startswith("#")]
    return list(csv.DictReader(io.StringIO("\n".join(lines))))


def num(x):
    try:
        v = float(str(x).strip().replace("−", "-"))
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def given(x) -> bool:
    v = num(x)
    return v is not None and v > 0


def dex(x, y):
    a, b = num(x), num(y)
    if a is None or b is None or a <= 0 or b <= 0:
        return None
    return abs(math.log10(a) - math.log10(b))


def close(r1: dict, r2: dict) -> bool:
    return all((d := dex(r1.get(q), r2.get(q))) is not None and d <= TOL_DEX for q in ("g_obs", "g_bar"))


def status(row: dict) -> str:
    n = str(row.get("notes", "")).lower()
    if "method incomplete" in n:
        return "method incomplete"
    if "unreadable" in n:
        return "unreadable"
    return "ok"


def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def first_number(x):
    m = re.search(r"[-+−]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", str(x))
    return num(m.group(0)) if m else None


REL_TOL_INPUT = 1e-6  # plan v4 §2.7: binary floats (e.g. FITS float32) printed to different digits are the same value


def same_input(x: str, y: str) -> bool:
    """Equal as numbers if both values start with a number (the printed value; readers may add errors
    or notes after it) and they agree within a relative 1e-6 (plan v4 §2.7); otherwise equal as stripped text."""
    a, b = first_number(x), first_number(y)
    if a is not None and b is not None:
        return a == b or abs(a - b) <= REL_TOL_INPUT * max(abs(a), abs(b))
    return str(x).strip().lower() == str(y).strip().lower()


def load_reader(pdir: Path):
    vals, inps = {}, {}
    for base in (pdir / "out", pdir):
        vp, ip = base / "values.csv", base / "inputs.csv"
        if vp.exists():
            for r in csv.DictReader(vp.open(encoding="utf-8")):
                vals[r["measurement_id"].strip()] = r
            if ip.exists():
                for r in csv.DictReader(ip.open(encoding="utf-8")):
                    inps.setdefault(r["measurement_id"].strip(), {})[norm_name(r.get("input", ""))] = r
            break
    return vals, inps


def clopper_pearson_upper(x: int, n: int, conf: float = 0.95) -> float:
    """One-sided 95 % Clopper-Pearson upper bound: p with P(X <= x | n, p) = 1 - conf.

    This is the bound plan v4 §2.10 states by its numbers (n = 220: 0 rows 1.35 %, 1 row 2.14 %,
    2 rows 2.83 %), and the one D-116 ruled on. (compare.py for v2 used the two-sided interval's
    upper end, which gives 1.66 %, 2.51 % and 3.25 % at n = 220. Under that bound one row would fail the 2.5 % threshold, so the choice matters; the plan's own numbers decide it: one-sided.)"""
    if n == 0 or x >= n:
        return 1.0
    alpha = 1 - conf

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


def code_row(mid: str, atlas: dict, rv: dict) -> dict:
    va = {k: rv[k][0].get(mid) for k in rv}
    ia = {k: rv[k][1].get(mid, {}) for k in rv}
    out = {"code": "", "blocking": "", "notes": []}
    if any(va.get(k) is None for k in READERS):
        out["code"] = "missing"
        out["notes"].append("no row from " + ",".join(k for k in READERS if va.get(k) is None))
        return out
    st = {k: status(va[k]) for k in READERS}
    if "method incomplete" in st.values():
        out["code"] = "method incomplete"
        recorders = [k for k in READERS if st[k] == "method incomplete"]
        block = any(not (given(va[k].get("g_obs")) and given(va[k].get("g_bar"))) or not close(va[k], atlas) for k in recorders)
        out["blocking"] = "blocking" if block else "non-blocking"
        return out
    if "unreadable" in st.values():
        out["code"] = "unreadable"
        return out
    shared = sorted(set(ia["a"]) & set(ia["b"]))
    diff = [n for n in shared if not same_input(ia["a"][n].get("value", ""), ia["b"][n].get("value", ""))]
    if diff:
        out["notes"].append("inputs differ: " + "; ".join(diff))
    agree_ab = close(va["a"], va["b"]) and all(given(va[k].get(q)) for k in READERS for q in ("g_obs", "g_bar"))
    if agree_ab and not diff:
        out["code"] = "agree" if close(va["a"], atlas) else "Atlas discrepancy"
        return out
    # §2.8: third reader
    c = va.get("c")
    if c is None:
        out["code"] = "reader disagreement"
        return out
    pairs = [(x, y) for x, y in (("a", "b"), ("a", "c"), ("b", "c")) if va.get(x) and va.get(y) and close(va[x], va[y])]
    if not pairs:
        out["code"] = "reader disagreement, unresolved"
        out["notes"].append("no two of a, b, c agree")
        return out
    x, _ = pairs[0]
    out["notes"].append("two of three: " + "+".join(pairs[0]))
    out["code"] = "agree (2 of 3)" if close(va[x], atlas) else "Atlas discrepancy (2 of 3)"
    return out


def compare(readings: Path, sample_csv: Path, root: Path) -> list[dict]:
    sample = [r for r in csv.DictReader(sample_csv.open(encoding="utf-8")) if r["status"] == "sample"]
    rows = []
    for stratum in dict.fromkeys(r["stratum"] for r in sample):
        ds = stratum.split("/")[0]
        atlas = {r["measurement_id"]: r for r in read_ecsv_rows(root / "data/packages" / stratum / "tables/measurements.ecsv")}
        rv = {k: load_reader(readings / k / ds) for k in ("a", "b", "c") if (readings / k / ds).exists()}
        for k in READERS:
            rv.setdefault(k, ({}, {}))
        for s in (r for r in sample if r["stratum"] == stratum):
            mid = s["measurement_id"]
            res = code_row(mid, atlas[mid], rv)
            rec = {"stratum": stratum, "measurement_id": mid, "code": res["code"], "method_gap": res["blocking"],
                   "atlas_g_obs": atlas[mid]["g_obs"], "atlas_g_bar": atlas[mid]["g_bar"]}
            for k in ("a", "b", "c"):
                v = rv.get(k, ({}, {}))[0].get(mid) or {}
                rec[f"{k}_g_obs"], rec[f"{k}_g_bar"], rec[f"{k}_status"] = v.get("g_obs", ""), v.get("g_bar", ""), (status(v) if v else "")
            rec["notes"] = " | ".join(res["notes"])
            rows.append(rec)
    return rows


def verdict(run: Path) -> dict:
    comp = list(csv.DictReader((run / "comparison.csv").open(encoding="utf-8")))
    prov = {r["measurement_id"]: r for r in csv.DictReader((run / "provenance.csv").open(encoding="utf-8"))} if (run / "provenance.csv").exists() else {}
    adj = {r["measurement_id"]: r for r in csv.DictReader((run / "adjudication.csv").open(encoding="utf-8"))} if (run / "adjudication.csv").exists() else {}
    n = len(comp)
    # Rows that need Claude's adjudication at source before any count is final (§2.8). A blocking
    # method gap is also read at source: the Atlas may be the one in error there.
    needs = [r["measurement_id"] for r in comp
             if r["code"].startswith(("Atlas discrepancy", "unreadable", "missing", "reader disagreement")) or r["method_gap"] == "blocking"]
    pending = [m for m in needs if m not in adj]
    material = sum(1 for m, a in adj.items() if a["outcome"] == "material discrepancy")
    not_verified = sum(1 for m, a in adj.items() if a["outcome"] == "not verified")
    prov_fail = sum(1 for r in prov.values() if r.get("result") == "fail") + sum(1 for a in adj.values() if a["outcome"] == "provenance failure")
    pending += [m for m, r in prov.items() if r.get("result") == "review" and m not in adj]
    not_verified += sum(1 for m, r in prov.items() if r.get("result") == "not verified" and adj.get(m, {}).get("outcome") != "not verified")
    prov_missing = [r["measurement_id"] for r in comp if r["measurement_id"] not in prov]
    blocking = sum(1 for r in comp if r["method_gap"] == "blocking")
    nonblocking = sum(1 for r in comp if r["method_gap"] == "non-blocking")
    counts = {"material discrepancies": material, "provenance failures": prov_fail, "blocking method gaps": blocking}
    bounds = {k: clopper_pearson_upper(v, n) for k, v in counts.items()}
    if pending or prov_missing:
        v = "incomplete (adjudication or provenance check pending)"
    elif any(b > THRESHOLD for b in bounds.values()):
        v = "fail"
    elif not_verified:
        v = "incomplete"
    else:
        v = "pass"
    strict = "pass" if not pending and not prov_missing and all(c == 0 for c in counts.values()) and nonblocking == 0 and not_verified == 0 else "not pass"
    return {"n": n, "counts": counts, "upper_bounds": bounds, "non-blocking method gaps": nonblocking,
            "not verified": not_verified, "pending adjudication": pending, "provenance not checked": prov_missing,
            "verdict": v, "strict verdict": strict}


def main(argv):
    if argv[1] == "compare":
        rd, sample = Path(argv[2]), Path(argv[3])
        root = Path(argv[4]) if len(argv) > 4 else Path(__file__).resolve().parents[2]
        rows = compare(rd, sample, root)
        with (rd / "comparison.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        codes = sorted({r["code"] for r in rows})
        print("stratum," + ",".join(codes) + ",blocking,non-blocking,n")
        for st in list(dict.fromkeys(r["stratum"] for r in rows)) + ["all"]:
            rr = [r for r in rows if st == "all" or r["stratum"] == st]
            print(st + "," + ",".join(str(sum(r["code"] == c for r in rr)) for c in codes)
                  + f",{sum(r['method_gap'] == 'blocking' for r in rr)},{sum(r['method_gap'] == 'non-blocking' for r in rr)},{len(rr)}")
    elif argv[1] == "verdict":
        import json
        print(json.dumps(verdict(Path(argv[2])), indent=1))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
