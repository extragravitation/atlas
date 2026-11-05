"""X-COP v2 audit comparison (frozen with docs/audit/AUDIT_PLAN_XCOP_v2.md, D-090 rule 3).

Usage:
  python docs/audit/compare_xcop_v2.py SAMPLE_CSV READER_A_CSV READER_B_CSV [REPO_ROOT]

SAMPLE_CSV is the output of sample_xcop_v2.py; only rows with status "sample"
are compared. Each reader file is a CSV with one row per measurement and the
columns below, in kpc and m s^-2, transcribed from the reader's own return:

  measurement_id, status, r_kpc, g_obs, g_obs_err_lo, g_obs_err_hi,
  g_bar, g_bar_err_lo, g_bar_err_hi

status is "ok", "unreadable" or "method_incomplete". A value the reader
recorded as "not stated" is left blank.

Standard library only. Prints counts, booleans, measurement IDs and field
names only; it never prints a value, so its output can be published as is.

Tolerance (plan section 2.7): |a - b| <= 1e-12 * max(|a|, |b|), on every field
the package row fills. Codes per row, first match wins:
  unreadable           either reader marked the row unreadable
  method incomplete    a reading is missing, marked method_incomplete, or
                       blank on a field the package fills
  reader disagreement  the readers differ from each other on any field
  Atlas discrepancy    the readers agree with each other but not with the package
  agree                otherwise
A sampled ID absent from the package is reported as "absent from package"
(the plan's replacement case, section 2.4).
"""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

STRATUM = "aeg-d-xcop/v2"
REL_TOL = 1e-12
FIELDS = ("r_kpc", "g_obs", "g_obs_err_lo", "g_obs_err_hi", "g_bar", "g_bar_err_lo", "g_bar_err_hi")
CODES = ("agree", "reader disagreement", "Atlas discrepancy", "method incomplete", "unreadable", "absent from package")


def read_csv(path: Path) -> list[dict]:
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if not ln.startswith("#")]
    return list(csv.DictReader(io.StringIO("\n".join(lines))))


def by_id(rows: list[dict], label: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in rows:
        mid = (r.get("measurement_id") or "").strip()
        if mid in out:
            raise SystemExit(f"duplicate measurement_id in {label}: {mid}")
        out[mid] = r
    return out


def num(value: str | None) -> float | None:
    value = (value or "").strip()
    return None if value == "" else float(value)


def close(a: float, b: float) -> bool:
    return abs(a - b) <= REL_TOL * max(abs(a), abs(b))


def code_row(pkg: dict | None, ra: dict | None, rb: dict | None) -> tuple[str, list[str]]:
    if pkg is None:
        return "absent from package", []
    status = [((r or {}).get("status") or "").strip() for r in (ra, rb)]
    if "unreadable" in status:
        return "unreadable", []
    fields = [f for f in FIELDS if num(pkg.get(f)) is not None]
    if ra is None or rb is None or "method_incomplete" in status:
        return "method incomplete", []
    blank = [f for f in fields if num(ra.get(f)) is None or num(rb.get(f)) is None]
    if blank:
        return "method incomplete", blank
    between = [f for f in fields if not close(num(ra[f]), num(rb[f]))]
    if between:
        return "reader disagreement", between
    atlas = [f for f in fields if not (close(num(ra[f]), num(pkg[f])) and close(num(rb[f]), num(pkg[f])))]
    if atlas:
        return "Atlas discrepancy", atlas
    return "agree", []


def compare(sample: Path, reader_a: Path, reader_b: Path, root: Path) -> dict[str, list[tuple[str, list[str]]]]:
    ids = [r["measurement_id"].strip() for r in read_csv(sample) if r.get("status", "").strip() == "sample"]
    pkg = by_id(read_csv(root / "data" / "packages" / STRATUM / "tables" / "measurements.ecsv"), "package")
    ra = by_id(read_csv(reader_a), "reader A")
    rb = by_id(read_csv(reader_b), "reader B")
    result: dict[str, list[tuple[str, list[str]]]] = {c: [] for c in CODES}
    for mid in ids:
        code, fields = code_row(pkg.get(mid), ra.get(mid), rb.get(mid))
        result[code].append((mid, fields))
    return result


def main() -> None:
    if len(sys.argv) not in (4, 5):
        raise SystemExit(__doc__)
    sample, a, b = (Path(p) for p in sys.argv[1:4])
    root = Path(sys.argv[4]) if len(sys.argv) > 4 else Path(__file__).resolve().parents[2]
    result = compare(sample, a, b, root)
    n = sum(len(v) for v in result.values())
    print(f"stratum: {STRATUM}")
    print(f"tolerance_relative: {REL_TOL:g}")
    print(f"rows_compared: {n}")
    for c in CODES:
        print(f"count[{c}]: {len(result[c])}")
    print(f"all_agree: {len(result['agree']) == n and n > 0}")
    for c in CODES:
        for mid, fields in result[c]:
            if c != "agree":
                print(f"{c}: {mid}" + (f" fields={';'.join(fields)}" if fields else ""))


if __name__ == "__main__":
    main()
