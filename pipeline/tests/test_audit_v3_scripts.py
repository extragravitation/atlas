"""Tests of the audit v3 comparison and verdict (docs/audit/compare_v3.py), on synthetic readers.

Written before the audit seed exists. Reader values here are made up from the Atlas rows
themselves, so these tests say nothing about the audit's outcome; they check the rules.
"""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("compare_v3", ROOT / "docs/audit/compare_v3.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

STRATUM = "aeg-d-kids1000-rar/v3"
IDS = [f"{STRATUM}/m{n:06d}" for n in range(1, 11)]


def atlas():
    return {r["measurement_id"]: r for r in C.read_ecsv_rows(ROOT / "data/packages" / STRATUM / "tables/measurements.ecsv")}


def write_reader(d: Path, rows: dict, inputs: dict | None = None):
    d.mkdir(parents=True, exist_ok=True)
    with (d / "values.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["measurement_id", "g_obs", "g_bar", "notes"])
        for mid, (go, gb, note) in rows.items():
            w.writerow([mid, go, gb, note])
    with (d / "inputs.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["measurement_id", "input", "value", "unit", "file", "place", "at_locator"])
        for (mid, name), val in (inputs or {}).items():
            w.writerow([mid, name, val, "", "", "", "yes"])


def sample(tmp: Path) -> Path:
    p = tmp / "sample.csv"
    with p.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stratum", "rank", "measurement_id", "key", "status"])
        for i, m in enumerate(IDS, 1):
            w.writerow([STRATUM, i, m, "", "sample"])
    return p


def test_codes(tmp_path):
    A = atlas()
    g = lambda m, f=1.0: (float(A[m]["g_obs"]) * f, float(A[m]["g_bar"]))
    a, b, c = {}, {}, {}
    for m in IDS:
        a[m] = b[m] = (*g(m), "")
    m1, m2, m3, m4, m5, m6, m7, m8 = IDS[:8]
    a[m2] = b[m2] = (*g(m2, 1.05), "")                      # both readers agree, Atlas differs by 0.021 dex
    a[m3] = (*g(m3, 1.05), "")                              # a differs; c sides with b -> agree (2 of 3)
    c[m3] = (*g(m3), "")
    a[m4] = (*g(m4, 1.05), "")                              # a differs; no c yet
    a[m5] = (*g(m5), "method incomplete: step x missing")   # non-blocking: value right
    a[m6] = ("", "", "method incomplete: cannot do step y")  # blocking: no value
    b[m7] = (*g(m7, 1.004), "")                             # within 0.005 dex -> agree
    a[m8] = (*g(m8), "unreadable: column smudged")
    write_reader(tmp_path / "r/a/aeg-d-kids1000-rar", a, {(m1, "ESD_t"): "1.7514 +- 0.1"})
    write_reader(tmp_path / "r/b/aeg-d-kids1000-rar", b, {(m1, "esd t"): "1.7514"})
    write_reader(tmp_path / "r/c/aeg-d-kids1000-rar", c)
    rows = {r["measurement_id"]: r for r in C.compare(tmp_path / "r", sample(tmp_path), ROOT)}
    assert rows[m1]["code"] == "agree"                       # same input name after normalising, same first number
    assert rows[m2]["code"] == "Atlas discrepancy"
    assert rows[m3]["code"] == "agree (2 of 3)"
    assert rows[m4]["code"] == "reader disagreement"
    assert rows[m5]["code"] == "method incomplete" and rows[m5]["method_gap"] == "non-blocking"
    assert rows[m6]["code"] == "method incomplete" and rows[m6]["method_gap"] == "blocking"
    assert rows[m7]["code"] == "agree"
    assert rows[m8]["code"] == "unreadable"


def test_inputs_disagree(tmp_path):
    A = atlas()
    m = IDS[0]
    v = {x: (A[x]["g_obs"], A[x]["g_bar"], "") for x in IDS}
    write_reader(tmp_path / "r/a/aeg-d-kids1000-rar", v, {(m, "bias"): "0.98531"})
    write_reader(tmp_path / "r/b/aeg-d-kids1000-rar", v, {(m, "Bias"): "0.98513"})
    rows = {r["measurement_id"]: r for r in C.compare(tmp_path / "r", sample(tmp_path), ROOT)}
    assert rows[m]["code"] == "reader disagreement" and "bias" in rows[m]["notes"]


def test_bounds_match_the_plan():
    # plan v3 §2.10: n = 220 -> 0 rows 1.35 %, 1 row 2.14 %, 2 rows 2.83 %
    assert [round(100 * C.clopper_pearson_upper(k, 220), 2) for k in range(3)] == [1.35, 2.14, 2.83]


def _run(tmp: Path, n: int, blocking=0, nonblocking=0, prov_fail=0, material=0, pending=0, not_verified=0, review=0):
    rows = []
    for i in range(n):
        gap = "blocking" if i < blocking else "non-blocking" if i < blocking + nonblocking else ""
        code = "method incomplete" if gap else "Atlas discrepancy" if i >= n - material - pending else "agree"
        rows.append({"stratum": "s", "measurement_id": f"m{i}", "code": code, "method_gap": gap})
    with (tmp / "comparison.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with (tmp / "provenance.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["measurement_id", "result"])
        w.writeheader()
        for i in range(n):
            res = "fail" if i < prov_fail else "review" if i < prov_fail + review else "pass"
            w.writerow({"measurement_id": f"m{i}", "result": res})
    with (tmp / "adjudication.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["measurement_id", "outcome", "by", "note"])
        w.writeheader()
        for i in range(n - material - pending, n - pending):
            w.writerow({"measurement_id": f"m{i}", "outcome": "material discrepancy", "by": "Claude", "note": ""})
        for i in range(blocking):
            w.writerow({"measurement_id": f"m{i}", "outcome": "reader error", "by": "Claude", "note": ""})
        for i in range(not_verified):
            w.writerow({"measurement_id": f"m{100 + i}", "outcome": "not verified", "by": "", "note": ""})
    return C.verdict(tmp)


def test_verdicts(tmp_path):
    v = _run(tmp_path, 220)
    assert v["verdict"] == "pass" and v["strict verdict"] == "pass"
    v = _run(tmp_path, 220, blocking=1, material=1, prov_fail=1, nonblocking=3)
    assert v["verdict"] == "pass" and v["strict verdict"] == "not pass"
    v = _run(tmp_path, 220, material=2)
    assert v["verdict"] == "fail"
    v = _run(tmp_path, 220, prov_fail=2)
    assert v["verdict"] == "fail"
    v = _run(tmp_path, 220, pending=1)
    assert v["verdict"].startswith("incomplete") and v["pending adjudication"]
    v = _run(tmp_path, 220, review=1)
    assert v["verdict"].startswith("incomplete")
    v = _run(tmp_path, 220, not_verified=1)
    assert v["verdict"] == "incomplete"
