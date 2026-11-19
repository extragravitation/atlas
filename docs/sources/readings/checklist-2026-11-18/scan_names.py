"""List catalogue-style object names in a review's page range that a reader's CSV does not mention.

Usage: python3 -I scan_names.py <arxiv_id> <READER>

Reads /home/claude/reviews/<arxiv_id>.txt (pdftotext -layout, one form feed per page)
and docs/sources/readings/checklist-2026-11-18/<READER>-items.csv.
Committed with brief.md before any reader starts (completeness plan step 1.1, D-111).
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEXTS = Path("/home/claude/reviews")

RANGES = {
    "1112.3960": [(1, 130)],
    "2110.06936": [(1, 77)],
    "1707.04256": [(1, 42)],
    "1811.08843": [(1, 56)],
    "2406.01705": [(15, 68), (300, 310), (394, 406)],
}

CATALOGUE = re.compile(
    r"\b(?:NGC|UGC|UGCA|IC|DDO|ESO|AGC|PGC|KK|KKH|KKs|WLM|Abell|ACO|MACS\s?J?|RXC?\s?J?|CL|Cl|"
    r"SDSS\s?J|Pal|Palomar|M|Holmberg|Ho|F)\s?-?\s?\d[\dA-Za-z.+\-]*"
)
NAMED = [
    "Milky Way", "Galaxy", "Andromeda", "LMC", "SMC", "Magellanic", "Sagittarius", "Fornax", "Sculptor",
    "Carina", "Draco", "Ursa Minor", "Sextans", "Leo I", "Leo II", "Leo T", "Crater", "Antlia", "Bootes",
    "Boötes", "Segue", "Willman", "Tucana", "Hercules", "Coma Berenices", "Reticulum", "Triangulum", "Eridanus",
    "Bullet", "El Gordo", "Coma", "Virgo", "Perseus", "Centaurus", "Hydra", "Train Wreck", "Musket Ball",
    "Dragonfly", "DF2", "DF4", "DF44", "NGC1052", "Malin", "Cen A", "Centaurus A", "GD-1", "Pal 5",
    "Local Group", "Local Volume", "Solar System", "Sun", "Oort", "Gaia", "Hubble flow", "Kepler",
    "Cassini", "Saturn", "Voyager", "Pioneer", "Pleiades", "Hyades", "Omega Cen", "ω Cen", "47 Tuc",
    "Phoenix", "Pegasus", "Cetus", "Aquarius", "Sag DIG", "Tuc", "Hydrus", "Grus", "Horologium",
    "Kiso", "Arp", "Stephan", "Seyfert", "Hickson", "Shapley", "Ophiuchus", "Norma", "Great Attractor",
    "KBC", "Local Void", "Laniakea", "Abell 520", "A520", "A1689", "A2744", "MACS J0025", "Pandora",
]


def pages_in_range(arxiv_id):
    pages = (TEXTS / f"{arxiv_id}.txt").read_text(errors="ignore").split("\f")
    for lo, hi in RANGES[arxiv_id]:
        for n in range(lo, min(hi, len(pages)) + 1):
            yield n, pages[n - 1]


def norm(s):
    return re.sub(r"[\s\-_.]", "", s).lower()


def main():
    arxiv_id, reader = sys.argv[1], sys.argv[2]
    csv_path = HERE / f"{reader}-items.csv"
    blob = ""
    if csv_path.exists():
        with csv_path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                blob += " " + " ".join(row.values())
    blob_n = norm(blob)

    found = {}
    for n, text in pages_in_range(arxiv_id):
        flat = re.sub(r"\s+", " ", text)
        for m in CATALOGUE.finditer(flat):
            found.setdefault(m.group(0).strip(), set()).add(n)
        for name in NAMED:
            if re.search(r"(?<![A-Za-z])" + re.escape(name) + r"(?![a-z])", flat):
                found.setdefault(name, set()).add(n)

    missing = {k: v for k, v in found.items() if norm(k) not in blob_n}
    print(f"{arxiv_id} {reader}: {len(found)} names found, {len(missing)} not in {csv_path.name}")
    for k in sorted(missing, key=lambda s: s.lower()):
        print(f"  {k}\tpages {','.join(map(str, sorted(missing[k])))}")


if __name__ == "__main__":
    main()
