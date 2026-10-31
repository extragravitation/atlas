"""D-051: member tables for Collins 2013, Kvasova 2024, Spencer 2017 and Cerny 2026 -> source/members/<name>.csv.

Usage (from the package directory): python reproduction/extract_members.py
Written and frozen before any data row of these tables was read. Only the headers were
read: byte-by-byte descriptions, FITS column names, and the distinct values of the
field-name and membership-flag columns.

Each output has columns key, ra_deg, dec_deg plus the source's own membership columns,
which reading/coverage_config.csv uses as the member rule. Positions in sexagesimal are
converted to degrees: RA = 15 (h + m/60 + s/3600); Dec = sign (d + m/60 + s/3600).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_geha2026_v2 import mrt  # noqa: E402  (frozen MRT parser, D-051 v2)

PKG = Path(__file__).resolve().parents[1]
SRC = PKG / "source/members"

COLLINS_FIELDS = {
    "And V": "andromeda_05", "And VI": "andromeda_06", "And IX": "andromeda_09", "And XI": "andromeda_11",
    "And XII": "andromeda_12", "And XIII": "andromeda_13", "And XV": "andromeda_15", "And XVI": "andromeda_16",
    "And XVII": "andromeda_17", "And XVIII": "andromeda_18", "And XIXa": "andromeda_19", "And XIXb": "andromeda_19",
    "And XX": "andromeda_20", "And XXI": "andromeda_21", "And XXII": "andromeda_22", "And XXIIIa": "andromeda_23",
    "And XXIIIb": "andromeda_23", "And XXIV": "andromeda_24", "And XXV": "andromeda_25", "And XXVI": "andromeda_26",
    "And XXVII": "andromeda_27", "And XXVIII": "andromeda_28", "CassII": "cassiopeia_2",
}


def hms(h: str, m: str, s: str) -> float:
    return 15.0 * (float(h) + float(m) / 60.0 + float(s) / 3600.0)


def dms(sign: str, d: str, m: str, s: str) -> float:
    v = float(d) + float(m) / 60.0 + float(s) / 3600.0
    return -v if sign.strip() == "-" else v


def write(name: str, rows: list[dict]) -> None:
    with open(SRC / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def collins2013() -> None:
    rows = []
    for r in mrt(SRC / "collins2013/apj466362t3_mrt.txt"):
        key = COLLINS_FIELDS.get(r["Field"])
        if key is None:
            continue
        # Dec sign: the byte-by-byte description has no sign column; all M31 dSphs here are at positive Dec.
        rows.append({"key": key, "field": r["Field"], "ra_deg": f"{hms(r['RAh'], r['RAm'], r['RAs']):.7f}",
                     "dec_deg": f"{dms('+', r['DEd'], r['DEm'], r['DEs']):.7f}", "Pi": r["Pi"]})
    write("collins2013", rows)


def kvasova2024() -> None:
    rows = []
    for r in mrt(SRC / "kvasova2024/apjad55f0t1_mrt.txt"):
        rows.append({"key": "andromeda_18", "name": r["Name"], "ra_deg": f"{hms(r['RAh'], r['RAm'], r['RAs']):.7f}",
                     "dec_deg": f"{dms(r['DE-'], r['DEd'], r['DEm'], r['DEs']):.7f}", "Mem": r["Mem"]})
    write("kvasova2024", rows)


def spencer2017() -> None:
    rows, seen = [], set()
    for r in mrt(SRC / "spencer2017/apjaa58edt3_mrt.txt"):
        pos = (r["RAdeg"], r["DEdeg"])
        if pos in seen:  # repeat epochs of one star: one row per star
            continue
        seen.add(pos)
        rows.append({"key": "leo_2", "ra_deg": r["RAdeg"], "dec_deg": r["DEdeg"], "Mem": r["Mem?"]})
    write("spencer2017", rows)


def cerny2026() -> None:
    import tarfile

    from astropy.io import fits

    fits_path = SRC / "cerny2026/PublicMemberCatalogs/Draco_II_Members_v1.1.fits"
    if not fits_path.exists():
        with tarfile.open(SRC / "cerny2026/MemberCatalogs_v1.1.tar.gz") as t:
            t.extract("PublicMemberCatalogs/Draco_II_Members_v1.1.fits", SRC / "cerny2026", filter="data")
    rows = []
    with fits.open(SRC / "cerny2026/PublicMemberCatalogs/Draco_II_Members_v1.1.fits") as h:
        for r in h[1].data:
            rows.append({"key": "draco_2", "ra_deg": f"{float(r['Phot_RA']):.7f}", "dec_deg": f"{float(r['Phot_DEC']):.7f}",
                         "inKinematicSample": str(bool(r["inKinematicSample"]))})
    write("cerny2026", rows)


def main() -> int:
    collins2013()
    kvasova2024()
    spencer2017()
    cerny2026()
    return 0


if __name__ == "__main__":
    sys.exit(main())
