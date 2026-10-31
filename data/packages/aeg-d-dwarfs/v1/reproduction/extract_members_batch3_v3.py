"""D-051: member tables batch 3 -> source/members/<name>.csv. Version 3.

Version 3 parses the Tollerud 2012 MRT by whitespace. The journal file's data rows are
shifted one to two bytes to the right of its own byte-by-byte description (rows are 90-91
characters wide against a declared 89), so byte slicing returned blank coordinates and
version 2 stopped. Every one of the 528 rows has exactly 17 whitespace-separated fields:
Mask, ID, RAh, RAm, RAs, signed DEd, DEm, DEs, T2mag, e_T2mag, M-T2, e_M-T2, RVel,
e_RVel, EW, e_EW, Prob. Nothing else changes from version 2.

Version 1 stopped with KeyError at the Battaglia table: astropy renames the VOTable columns
e_[Fe/H] and E_[Fe/H] to e__Fe_H_ and E__Fe_H_. Version 2 uses the renamed columns.
The four tables written before the stop are written again, unchanged.

Usage (from the package directory): python reproduction/extract_members_batch3.py
Written and frozen before the coverage check ran on these tables.

Sources:
- VizieR VOTables from the Harvard mirror query service (Hendricks 2014, Tolstoy 2025,
  Koch 2007 AJ, Koch 2007 ApJ, Battaglia 2011);
- the Tollerud 2012 ApJ MRT.

Output columns: key, ra_deg, dec_deg, plus the source's own columns that the member rules
in reading/coverage_config_batch3.csv use. Sexagesimal RA/Dec strings ("hh mm ss.s",
"+dd mm ss") are converted to degrees.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_geha2026_v2 import mrt  # noqa: E402  (frozen MRT parser)

PKG = Path(__file__).resolve().parents[1]
SRC = PKG / "source/members"

TOLLERUD_MASKS = {
    "andromeda_01": ("d1_1", "d1_2"), "andromeda_03": ("d3_1", "d3_2", "d3_3"), "andromeda_05": ("d5_1", "d5_2", "d5_3"),
    "andromeda_07": ("d7_1", "d7_2"), "andromeda_09": ("d9_1", "d9_2"), "andromeda_10": ("d10_1", "d10_2"),
    "andromeda_11": ("d11",), "andromeda_12": ("d12",), "andromeda_13": ("d13_1", "d13_2", "d13_3", "d13_4", "d13_5"),
    "andromeda_14": ("A170_1", "A170_2", "d14_3"), "andromeda_15": ("d15_1", "d15_2"), "andromeda_16": ("d16_1", "d16_2"),
    "andromeda_18": ("d18_1",), "andromeda_21": ("d21_1",), "andromeda_22": ("d22_1", "d22_2", "d22_3"),
}


def sexa(x: str, hours: bool) -> float:
    t = x.strip().replace("−", "-")
    neg = t.startswith("-")
    p = [float(v) for v in t.lstrip("+-").replace(":", " ").split()]
    p += [0.0] * (3 - len(p))
    v = p[0] + p[1] / 60.0 + p[2] / 3600.0
    v *= 15.0 if hours else 1.0
    return -v if neg else v


def votable(name: str) -> list[dict]:
    from astropy.io.votable import parse

    t = parse(str(SRC / f"{name}.vot")).get_first_table().to_table()
    rows = []
    for r in t:
        rows.append({c: ("" if (hasattr(r[c], "mask") and r[c] is getattr(r[c], "mask", None)) else str(r[c])).replace("--", "")
                     for c in t.colnames})
    return rows


def write(name: str, rows: list[dict]) -> None:
    with open(SRC / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def pos(r: dict) -> dict:
    if "RA_ICRS" in r:
        return {"ra_deg": r["RA_ICRS"], "dec_deg": r["DE_ICRS"]}
    return {"ra_deg": f"{sexa(r['RAJ2000'], True):.7f}", "dec_deg": f"{sexa(r['DEJ2000'], False):.7f}"}


def main() -> int:
    write("hendricks2014", [{"key": "fornax_1", **pos(r), "H": r["H"].strip()} for r in votable("vizier/J_A_A_572_A82")])
    write("tolstoy2025", [{"key": "sextans_1", **pos(r), "Pmem": r["Pmem"], "Vel": r["Vel"].strip()} for r in votable("vizier/J_A_A_698_A53")])
    write("koch2007aj", [{"key": "leo_2", **pos(r), "RV": r["RV"]} for r in votable("vizier/J_AJ_134_566")])
    write("koch2007apj", [{"key": "leo_1", **pos(r), "HRV": r["HRV"]} for r in votable("vizier/J_ApJ_657_241")])
    write("battaglia2011", [{"key": "sextans_1", **pos(r), "e_FeH": r["e__Fe_H_"].strip(), "E_FeH": r["E__Fe_H_"].strip()}
                            for r in votable("vizier/J_MNRAS_411_1013")])
    rows = []
    lines = (SRC / "tollerud2012/apj430011t2_mrt.txt").read_text(encoding="utf-8").splitlines()
    import re as _re
    end = max(i for i, l in enumerate(lines[:300]) if _re.match(r"^-{20,}", l))
    for l in lines[end + 1:]:
        f = l.split()
        if not f:
            continue
        if len(f) != 17:
            raise ValueError(f"Tollerud row with {len(f)} fields")
        mask, ra_h, ra_m, ra_s, de_d, de_m, de_s, prob = f[0], f[2], f[3], f[4], f[5], f[6], f[7], f[16]
        key = next((k for k, m in TOLLERUD_MASKS.items() if mask in m), None)
        if key is None:
            continue
        ra = 15.0 * (float(ra_h) + float(ra_m) / 60.0 + float(ra_s) / 3600.0)
        dec = abs(float(de_d)) + float(de_m) / 60.0 + float(de_s) / 3600.0
        dec = -dec if de_d.startswith("-") else dec
        rows.append({"key": key, "ra_deg": f"{ra:.7f}", "dec_deg": f"{dec:.7f}", "Mask": mask, "Prob": prob})
    write("tollerud2012", rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
