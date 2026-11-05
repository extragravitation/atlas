"""X-COP v2 audit sample draw (frozen with docs/audit/AUDIT_PLAN_XCOP_v2.md, D-090 rule 3).

Usage:  python docs/audit/sample_xcop_v2.py SEED_HEX [REPO_ROOT]

Standard library only. Same method as sample_v2.py, for the single stratum
aeg-d-xcop/v2. Prints: stratum, rank, measurement_id, key, status.
"""

from __future__ import annotations

import csv
import hashlib
import io
import math
import sys
from pathlib import Path

STRATUM = "aeg-d-xcop/v2"
FRACTION = 0.05
MINIMUM = 10


def read_ecsv_rows(path: Path) -> list[dict]:
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if not ln.startswith("#")]
    return list(csv.DictReader(io.StringIO("\n".join(lines))))


def frame(root: Path) -> list[str]:
    rows = read_ecsv_rows(root / "data" / "packages" / STRATUM / "tables" / "measurements.ecsv")
    ids = [r["measurement_id"].strip() for r in rows if (r.get("role") or "").strip() in ("", "default")]
    if len(ids) != len(set(ids)):
        raise SystemExit(f"duplicate measurement_id in {STRATUM}")
    return sorted(ids)


def sample_size(n: int) -> int:
    return min(n, max(math.ceil(FRACTION * n), MINIMUM))


def key(seed_hex: str, measurement_id: str) -> str:
    return hashlib.sha256(f"{seed_hex.lower()}|{measurement_id}".encode("utf-8")).hexdigest()


def draw(seed_hex: str, root: Path) -> list[tuple[str, int, str, str, str]]:
    int(seed_hex, 16)  # must be hexadecimal
    ids = frame(root)
    ranked = sorted(ids, key=lambda m: key(seed_hex, m))
    k = sample_size(len(ids))
    return [(STRATUM, i, m, key(seed_hex, m), "sample" if i <= k else "reserve") for i, m in enumerate(ranked, start=1)]


def main() -> None:
    seed = sys.argv[1]
    root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[2]
    w = csv.writer(sys.stdout, lineterminator="\n")
    w.writerow(["stratum", "rank", "measurement_id", "key", "status"])
    for row in draw(seed, root):
        w.writerow(row)


if __name__ == "__main__":
    main()
