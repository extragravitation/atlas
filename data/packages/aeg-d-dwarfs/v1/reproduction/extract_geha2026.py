"""D-051: member table for Geha et al. 2026 (ApJ 999, 140) -> source/members/geha2026.csv.

Usage (from the package directory): python reproduction/extract_geha2026.py
Inputs (fetched by aeg.fetch, hashes in sources.json):
- source/members/geha2026/apjae290dt1_mrt.txt: systems, with Reff (Table 1);
- source/members/geha2026/apjae290dt5_mrt.txt: per-star catalogue (rproj-arc, Pmem-novar).
  Its "Table:" title line repeats Table 4's title; the column notes identify it as the
  per-star catalogue.

Byte ranges come from each file's own "Byte-by-byte Description".

Output columns:
- key, ra_deg, dec_deg, pmem_novar, rproj_arcmin, reff_arcmin;
- r_ell_over_reff: the star's elliptical radius about the structural original's centre,
  ellipticity and PA (reading/structure_values.csv), in units of Table 1's Reff. This is
  the elliptical reading of "within two half-light radii".

Member rule (reading/coverage_config.csv): the paper's own words are "member stars
(P_mem_novar = 1) within two half-light radii". It does not say whether the window is
circular or elliptical. D-051's conservative application ("pass under both readings") is
implemented as members inside BOTH windows: rproj < 2 Reff and r_ell/Reff < 2. A pass on
that set implies a pass under each reading.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "pipeline"))
from aeg.coverage import Structure, r_over_ah  # noqa: E402

PKG = Path(__file__).resolve().parents[1]
SRC = PKG / "source/members/geha2026"
SYSTEM_TO_KEY = {
    "Aqr2": "aquarius_2", "Aqr3": "aquarius_3", "Boo1": "bootes_1", "Boo2": "bootes_2", "Boo3": "bootes_3",
    "CVn1": "canes_venatici_1", "CVn2": "canes_venatici_2", "Col1": "columba_1", "CB": "coma_berenices_1",
    "Dra": "draco_1", "Dra2": "draco_2", "Eri4": "eridanus_4", "For": "fornax_1", "Herc": "hercules_1",
    "Hyd2": "hydra_2", "Leo1": "leo_1", "Leo2": "leo_2", "Leo4": "leo_4", "Leo5": "leo_5", "Leo6": "leo_6",
    "LeoT": "leo_t", "Peg3": "pegasus_3", "Peg4": "pegasus_4", "Pisc2": "pisces_2", "Sgr": "sagittarius_1",
    "Scl": "sculptor_1", "Seg1": "segue_1", "Seg2": "segue_2", "Sext": "sextans_1", "Tri2": "triangulum_2",
    "UMa1": "ursa_major_1", "UMa2": "ursa_major_2", "UMi": "ursa_minor_1", "W1": "willman_1",
}


def mrt(path: Path) -> list[dict]:
    """Parse a CDS/AAS machine-readable table using its own byte-by-byte description."""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    cols, i = [], 0
    while i < len(lines) and not lines[i].startswith("Byte-by-byte"):
        i += 1
    seps = 0
    j = i + 1
    while j < len(lines):
        l = lines[j]
        if re.match(r"^-{20,}", l):
            seps += 1
        else:
            m = re.match(r"^\s*(\d+)-\s*(\d+)\s+\S+\s+\S+\s+(\S+)", l) or re.match(r"^\s*(\d+)\s+\S+\s+\S+\s+(\S+)", l)
            if m and seps == 1:
                if len(m.groups()) == 3:
                    cols.append((int(m.group(1)) - 1, int(m.group(2)), m.group(3)))
                else:
                    cols.append((int(m.group(1)) - 1, int(m.group(1)), m.group(2)))
        j += 1
    # data rows: after the last separator line of the header block
    last = max(k for k, l in enumerate(lines[: j]) if re.match(r"^-{20,}", l))
    out = []
    for l in lines[last + 1:]:
        if not l.strip():
            continue
        out.append({name: l[a:b].strip() for a, b, name in cols})
    return out


def main() -> int:
    t1 = mrt(SRC / "apjae290dt1_mrt.txt")
    reff = {r["System"]: float(r["Reff"]) for r in t1 if r["System"] in SYSTEM_TO_KEY}
    struct = {r["key"]: r for r in csv.DictReader(open(PKG / "reading/structure_values.csv", encoding="utf-8"))}
    stars = mrt(SRC / "apjae290dt5_mrt.txt")
    out = []
    for s in stars:
        key = SYSTEM_TO_KEY.get(s["System"])
        if key is None:
            continue
        st = struct.get(key)
        rell = ""
        if st:
            S = Structure(float(st["ra0_deg"]), float(st["dec0_deg"]), float(st["ellipticity"]), float(st["pa_deg"]), reff[s["System"]])
            rell = f"{r_over_ah(float(s['RAdeg']), float(s['DEdeg']), S):.5f}"
        out.append({"key": key, "ra_deg": s["RAdeg"], "dec_deg": s["DEdeg"], "pmem_novar": s["Pmem-novar"],
                    "rproj_arcmin": s["rproj-arc"], "reff_arcmin": f"{reff[s['System']]}", "r_ell_over_reff": rell})
    (PKG / "source/members").mkdir(parents=True, exist_ok=True)
    with open(PKG / "source/members/geha2026.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} star rows for {len({r['key'] for r in out})} systems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
