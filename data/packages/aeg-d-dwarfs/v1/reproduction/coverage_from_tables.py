"""D-051: member coverage from each source's own per-star table -> reading/coverage_tables.csv.

Usage (from the package directory): python reproduction/coverage_from_tables.py

Inputs, all written before any table is opened (D-051 item 4):
- reading/coverage_config.csv: one row per (key, paper) whose paper releases per-star
  velocities. Columns:
  - `table_file`: the extracted member table, under source/members/;
  - `sha256`: of the original table file the extraction came from;
  - `ra_col`, `dec_col` (degrees, or sexagesimal "hms"/"dms" with `coord_format`);
  - `member_rule`: a Python expression over the table's columns that selects the members
    the source used for the chosen dispersion, as the source states it;
  - `member_rule_quote`, `member_rule_location`: the source's words;
  - `status`: `checked`, or `not reached` with a reason.
- reading/structure_values.csv: the structural original's centre (ra0_deg, dec0_deg),
  ellipticity, position angle and semi-major half-light radius (arcmin), from the two-reader
  structural reading. This is the same R_h the plotted point uses (D-051 item 1).

Output: reading/coverage_tables.csv with key, paper, status, n_members, n_beyond,
fraction_beyond, max_r_over_rh, passes. Every system's numbers are published (D-051 item 2).
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "pipeline"))
from aeg.coverage import Structure, r_over_ah, summarise  # noqa: E402

PKG = Path(__file__).resolve().parents[1]


def sexa(x: str, hours: bool) -> float:
    p = [float(v) for v in x.replace(":", " ").split()]
    sign = -1.0 if x.strip().startswith("-") else 1.0
    deg = abs(p[0]) + p[1] / 60.0 + p[2] / 3600.0
    return sign * deg * (15.0 if hours else 1.0)


def coord(row: dict, col: str, fmt: str, hours: bool) -> float:
    v = row[col]
    return sexa(v, hours) if fmt == "sexagesimal" else float(v)


def main() -> int:
    cfg = list(csv.DictReader(open(PKG / "reading/coverage_config.csv", encoding="utf-8")))
    struct = {r["key"]: r for r in csv.DictReader(open(PKG / "reading/structure_values.csv", encoding="utf-8"))}
    out = []
    for c in cfg:
        rec = {"key": c["key"], "paper": c["paper"], "status": c["status"], "n_members": "", "n_beyond": "",
               "fraction_beyond": "", "max_r_over_rh": "", "passes": ""}
        if c["status"] == "checked":
            st = struct.get(c["key"])
            if not st:
                rec["status"] = "not reached: no structural values"
            else:
                s = Structure(float(st["ra0_deg"]), float(st["dec0_deg"]), float(st["ellipticity"] or 0.0),
                              float(st["pa_deg"] or 0.0), float(st["a_h_arcmin"]))
                rows = list(csv.DictReader(open(PKG / "source/members" / c["table_file"], encoding="utf-8")))
                used = [r for r in rows if eval(c["member_rule"], {"math": math}, dict(r))]  # noqa: S307 - frozen config
                radii = [r_over_ah(coord(r, c["ra_col"], c["coord_format"], True),
                                   coord(r, c["dec_col"], c["coord_format"], False), s) for r in used]
                summ = summarise(radii)
                rec.update({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in summ.items()})
        out.append(rec)
    with open(PKG / "reading/coverage_tables.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} (key, paper) pairs; checked {sum(1 for r in out if r['status'] == 'checked')}; "
          f"pass {sum(1 for r in out if r['passes'] is True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
