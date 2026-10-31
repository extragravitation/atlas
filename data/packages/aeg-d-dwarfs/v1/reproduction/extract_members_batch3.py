"""D-051: member tables batch 3 -> source/members/<name>.csv.

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
    write("battaglia2011", [{"key": "sextans_1", **pos(r), "e_FeH": r["e_[Fe/H]"].strip(), "E_FeH": r["E_[Fe/H]"].strip()}
                            for r in votable("vizier/J_MNRAS_411_1013")])
    rows = []
    for r in mrt(SRC / "tollerud2012/apj430011t2_mrt.txt"):
        key = next((k for k, m in TOLLERUD_MASKS.items() if r["Mask"] in m), None)
        if key is None:
            continue
        ra = 15.0 * (float(r["RAh"]) + float(r["RAm"]) / 60.0 + float(r["RAs"]) / 3600.0)
        dec = float(r["DEd"]) + float(r["DEm"]) / 60.0 + float(r["DEs"]) / 3600.0
        dec = -dec if r["DE-"].strip() == "-" else dec
        rows.append({"key": key, "ra_deg": f"{ra:.7f}", "dec_deg": f"{dec:.7f}", "Mask": r["Mask"], "Prob": r["Prob"]})
    write("tollerud2012", rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
