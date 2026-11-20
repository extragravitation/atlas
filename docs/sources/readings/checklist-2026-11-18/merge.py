"""Merge the five readers' item lists (completeness plan 1.1) into one table.

Usage: python3 -I -B merge.py

Writes, in docs/sources/:
- checklist-reviews.csv: every reader row, plus `canonical` (systems only) and `side`;
- checklist-reviews-systems.csv: one row per canonical system, used-as-test and mentioned counts per review.

Systems are given a canonical name by catalogue pattern or by the fixed table below.
Types, routes and `outside` rows keep the readers' own names; merging them is step 1.2.
"""
import csv
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1]  # docs/sources
READERS = ["FM", "BZ", "BBK", "SAL", "CSZ"]
SIDE = {"FM": "MOND-side", "BZ": "MOND-side", "BBK": "DM-side", "SAL": "DM-side", "CSZ": "DM-side"}

# (substring in lower-cased name, canonical names). First match wins; order matters.
NAMED = [
    ("bullet", ["Bullet Cluster (1E 0657-56)"]),
    ("train wreck", ["Abell 520"]), ("abell 520", ["Abell 520"]),
    ("abell 2390", ["Abell 2390"]), ("abell 2218", ["Abell 2218"]),
    ("el gordo", ["El Gordo (ACT-CL J0102-4915)"]),
    ("coma and fornax clusters", ["Coma cluster", "Fornax cluster"]),
    ("coma cluster", ["Coma cluster"]),
    ("fornax galaxy cluster", ["Fornax cluster"]), ("fornax cluster", ["Fornax cluster"]),
    ("fornax", ["Fornax (dwarf spheroidal)"]),
    ("dragonfly 44", ["Dragonfly 44"]), ("df44", ["Dragonfly 44"]),
    ("df2", ["NGC 1052-DF2"]), ("df4", ["NGC 1052-DF4"]),
    ("crater ii", ["Crater II"]), ("antlia ii", ["Antlia II"]),
    ("carina", ["Carina"]), ("draco", ["Draco"]), ("sculptor", ["Sculptor"]), ("sextans", ["Sextans"]),
    ("ursa minor", ["Ursa Minor"]), ("leo ii", ["Leo II"]), ("leo2", ["Leo II"]), ("leo i", ["Leo I"]),
    ("segue 1", ["Segue 1"]), ("segue 2", ["Segue 2"]), ("cetus", ["Cetus"]), ("tucana", ["Tucana"]),
    ("perseus i", ["Perseus I"]),
    ("sagittarius stream", ["Sagittarius stream"]), ("sagittarius tidal stream", ["Sagittarius stream"]),
    ("sagittarius", ["Sagittarius (dwarf spheroidal)"]),
    ("palomar 5", ["Palomar 5"]), ("pal 5", ["Palomar 5"]),
    ("palomar 14", ["Palomar 14"]), ("pal 14", ["Palomar 14"]), ("pal 3", ["Palomar 3"]),
    ("large and small magellanic", ["LMC", "SMC"]), ("magellanic clouds", ["LMC", "SMC"]),
    ("large magellanic", ["LMC"]), ("lmc", ["LMC"]), ("small magellanic", ["SMC"]), ("smc", ["SMC"]),
    ("m31 and m33", ["M31", "M33"]), ("m33", ["M33"]),
    ("m31 satellite", ["M31 satellite system"]), ("andromeda (m31) satellites", ["M31 satellite system"]),
    ("m31", ["M31"]), ("andromeda", ["M31"]),
    ("milky way satellites", ["Milky Way satellite system"]),
    ("centaurus spiral arm", ["Milky Way"]),
    ("milky way", ["Milky Way"]), ("the galaxy", ["Milky Way"]), ("solar neighbourhood", ["Milky Way"]),
    ("local group", ["Local Group"]),
    ("centaurus a group", ["Centaurus A group"]), ("centaurus a", ["Centaurus A (NGC 5128)"]),
    ("m81", ["M81 group"]),
    ("ngc 5291", ["NGC 5291 system"]), ("ngc5291", ["NGC 5291 system"]),
    ("ngc 5557 tidal", ["NGC 5557"]),
    ("holmberg ii", ["Holmberg II"]), ("ho ii", ["Holmberg II"]), ("ho i ", ["Holmberg I"]),
    ("proxima", ["Alpha Centauri system"]),
    ("solar system", ["Solar System"]), ("planets", ["Solar System"]), ("mars", ["Solar System"]),
    ("saturn", ["Solar System"]), ("pioneer", ["Solar System"]), ("voyager", ["Solar System"]),
    ("oort cloud", ["Solar System"]),
    ("q2237", ["Q2237+030"]), ("cl0024", ["Cl 0024+17"]),
]
CAT = re.compile(r"\b(NGC|UGC|IC|DDO|PGC|AGC|ESO|F)\s?-?(\d{2,6}(?:[-+.]\d+|-V\d)?[A-Z]?)\b")


def canonical(name):
    low = name.lower()
    m = re.search(r"read as ([A-Z]+ \d+)", name)
    if m:
        return [m.group(1)]
    if low.startswith("ngc 1052") and "df" not in low:
        return ["NGC 1052"]
    for key, canon in NAMED:
        if key in low:
            return canon
    m = CAT.search(name)
    if m:
        num = m.group(2).lstrip("0") or "0"
        return [f"F{num}" if m.group(1) == "F" else f"{m.group(1)} {num}"]
    return [re.split(r"\s*[(\[:]", name)[0].strip()]


def main():
    rows = []
    for r in READERS:
        with (HERE / f"{r}-items.csv").open(newline="", encoding="utf-8") as f:
            rows += list(csv.DictReader(f))
    fields = list(rows[0].keys())

    merged, systems = [], defaultdict(lambda: {"test": defaultdict(int), "mention": defaultdict(int),
                                                   "scales": set(), "channels": set()})
    for row in rows:
        canons = canonical(row["name"]) if row["item_kind"] == "system" else [""]
        for c in canons:
            merged.append({**row, "canonical": c, "side": SIDE[row["review"]]})
            if c:
                s = systems[c]
                key = "mention" if row["how_used"].startswith("mentioned") else "test"
                s[key][row["review"]] += 1
                s["scales"].add(row["scale"])
                if key == "test":
                    s["channels"].add(row["channel"])

    with (OUT / "checklist-reviews.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["canonical", "side"] + fields)
        w.writeheader()
        w.writerows(sorted(merged, key=lambda x: (x["item_kind"], x["canonical"].lower(), x["review"], int(x["page"] or 0))))

    with (OUT / "checklist-reviews-systems.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["canonical", "used_as_test_by", "mentioned_only_by", "n_reviews_test", "mond_side_test",
                    "dm_side_test", "scales", "channels"])
        for c in sorted(systems, key=str.lower):
            s = systems[c]
            t = sorted(s["test"], key=READERS.index)
            m = sorted(set(s["mention"]) - set(t), key=READERS.index)
            w.writerow([c, ";".join(f"{k}({s['test'][k]})" for k in t), ";".join(m), len(t),
                        sum(SIDE[k] == "MOND-side" for k in t), sum(SIDE[k] == "DM-side" for k in t),
                        ";".join(sorted(s["scales"])), ";".join(sorted(s["channels"]))])
    print(f"{len(merged)} merged rows; {len(systems)} canonical systems")


if __name__ == "__main__":
    main()
