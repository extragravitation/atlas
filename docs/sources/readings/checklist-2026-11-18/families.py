"""Indicative count of rows per review for candidate route and type families (completeness plan 1.1).

Usage: python3 -I -B families.py
A row counts if it is not `outside`, is used as a test, and its name or how_used matches the family's
regular expression. Keyword matching is coarse: the counts show presence, not exact numbers.
"""
import collections
import csv
import re
from pathlib import Path

ROWS = Path(__file__).resolve().parents[2] / "checklist-reviews.csv"
FAMILIES = {
    "vertical dynamics": r"vertical|oort discrepancy|diskmass|disk ?mass|velocity ellipsoid|flaring|scale height",
    "tidal streams": r"stream",
    "shells": r"shell",
    "direct accelerations": r"pulsar timing|barycentr|aberration|direct (orbital )?acceleration",
    "binary galaxies, satellites as tracers": r"binary galax|galaxy pairs|satellite kinematics|satellites as tracers|"
                                               r"satellite galaxies as tracers|kinematics of bright satellites|tracers of spiral",
    "Local Group timing, local flow": r"timing argument|local group (velocity|mass|dwarf galaxies as tracers)|hubble flow",
    "tidal radii": r"tidal radi|roche|tidal edge|tidal survival|tidal stability",
    "escape velocity": r"escape (speed|velocity)",
    "wide binaries": r"wide binar",
    "open clusters": r"open cluster|pleiades|praesepe",
    "colliding clusters, offsets": r"bullet|collid|offset|train wreck|el gordo",
    "X-ray hydrostatics": r"hydrostatic",
    "galaxy-galaxy weak lensing": r"galaxy-galaxy|weak-lensing rar|weak lensing extension",
    "strong lensing": r"strong lens|einstein (ring|radi)|slacs|castles",
    "galaxy dynamics in clusters": r"virial theorem|velocity dispersion of galaxies in clusters|member redshifts|cluster internal dynamics",
    "polar rings": r"polar ring",
    "tidal dwarfs": r"tidal dwarf|ngc 5291",
    "ultra-diffuse galaxies": r"ultra-diffuse|df2|df4|dragonfly|df44",
    "gravitational redshift in clusters": r"gravitational redshift",
}
READERS = ["FM", "BZ", "BBK", "SAL", "CSZ"]

rows = list(csv.DictReader(ROWS.open(encoding="utf-8")))
print("| Family | " + " | ".join(READERS) + " |\n|:--|" + "--:|" * len(READERS))
for fam, pat in FAMILIES.items():
    c = collections.Counter(
        r["review"] for r in rows
        if r["item_kind"] != "outside" and not r["how_used"].startswith("mentioned")
        and re.search(pat, (r["name"] + " " + r["how_used"]).lower()))
    print(f"| {fam} | " + " | ".join(str(c.get(k, 0)) for k in READERS) + " |")
