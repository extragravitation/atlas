"""Part B system pages for audit v4 (plan v4 §3.3). Committed before the seed exists.

Usage:  python docs/audit/choose_pages_v4.py SEED_HEX [REPO_ROOT]

For each current dataset (the six v3 packages), ranks its systems by
SHA-256("aeg-audit-v4|page|" + seed + "|" + system_id) ascending and prints ranks 1 and 2:
dataset, rank, system_id, page path. KiDS-1000 has no system pages (population averages);
it is listed with none. Standard library only.
"""
import csv
import hashlib
import io
import sys
from pathlib import Path

PACKAGES = ["aeg-d-sparc/v3", "aeg-d-xcop/v3", "aeg-d-kids1000-rar/v3", "aeg-d-strong-lensing/v3",
            "aeg-d-gc-baumgardt/v3", "aeg-d-dwarfs/v3"]


def main(argv):
    seed = argv[1].lower()
    int(seed, 16)
    root = Path(argv[2]) if len(argv) > 2 else Path(__file__).resolve().parents[2]
    w = csv.writer(sys.stdout, lineterminator="\n")
    w.writerow(["dataset", "rank", "system_id", "page"])
    for p in PACKAGES:
        f = root / "data/packages" / p / "tables/systems.ecsv"
        if not f.exists():
            w.writerow([p, "", "", "(no system pages)"])
            continue
        lines = [ln for ln in f.read_text(encoding="utf-8").splitlines() if not ln.startswith("#")]
        ids = sorted({r["system_id"] for r in csv.DictReader(io.StringIO("\n".join(lines)))})
        ranked = sorted(ids, key=lambda s: hashlib.sha256(f"aeg-audit-v4|page|{seed}|{s}".encode()).hexdigest())
        for i, s in enumerate(ranked[:2], 1):
            w.writerow([p, i, s, f"systems/{s}/"])


if __name__ == "__main__":
    main(sys.argv)
