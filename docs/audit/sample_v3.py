"""Audit sample draw, version 3 (frozen with docs/audit/AUDIT_PLAN_v3.md, D-116).

Usage:  python docs/audit/sample_v3.py SEED_HEX [REPO_ROOT]

Standard library only. Reads the measurement tables of the six v3 packages,
keeps the frame defined in AUDIT_PLAN_v3.md section 2.1, and prints the full
ranking as CSV: stratum, rank, measurement_id, key, status (sample or reserve).
Identical in method to sample_v2.py; only the strata and the key prefix differ.
"""

from __future__ import annotations

import csv
import hashlib
import io
import math
import sys
from pathlib import Path

STRATA = [
    "aeg-d-sparc/v3",
    "aeg-d-xcop/v3",
    "aeg-d-kids1000-rar/v3",
    "aeg-d-strong-lensing/v3",
    "aeg-d-gc-baumgardt/v3",
    "aeg-d-dwarfs/v3",
]
FRACTION = 0.05
MINIMUM = 10
PREFIX = "aeg-audit-v3"


def read_ecsv_rows(path: Path) -> list[dict]:
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if not ln.startswith("#")]
    return list(csv.DictReader(io.StringIO("\n".join(lines))))


def frame(root: Path, stratum: str) -> list[str]:
    rows = read_ecsv_rows(root / "data" / "packages" / stratum / "tables" / "measurements.ecsv")
    ids = []
    for r in rows:
        role = (r.get("role") or "").strip()
        if role in ("", "default"):
            ids.append(r["measurement_id"].strip())
    if len(ids) != len(set(ids)):
        raise SystemExit(f"duplicate measurement_id in {stratum}")
    return sorted(ids)


def sample_size(n: int) -> int:
    return min(n, max(math.ceil(FRACTION * n), MINIMUM))


def key(seed_hex: str, measurement_id: str) -> str:
    return hashlib.sha256(f"{PREFIX}|{seed_hex.lower()}|{measurement_id}".encode("utf-8")).hexdigest()


def draw(seed_hex: str, root: Path) -> list[tuple[str, int, str, str, str]]:
    int(seed_hex, 16)  # must be hexadecimal
    out = []
    for s in STRATA:
        ids = frame(root, s)
        ranked = sorted(ids, key=lambda m: key(seed_hex, m))
        k = sample_size(len(ids))
        for i, m in enumerate(ranked, start=1):
            out.append((s, i, m, key(seed_hex, m), "sample" if i <= k else "reserve"))
    return out


def main() -> None:
    seed = sys.argv[1]
    root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[2]
    w = csv.writer(sys.stdout, lineterminator="\n")
    w.writerow(["stratum", "rank", "measurement_id", "key", "status"])
    for row in draw(seed, root):
        w.writerow(row)


if __name__ == "__main__":
    main()
