"""Write the per-system input tables of the methods pages (D-113 item 2).

Usage:  python docs/methods/datasets/make_input_tables.py

For each default row of a package, list where each input is read: the
observable's source_ref with every printed value removed, and the place the
matching locator rule gives. Values are never written (the methods text must
not carry per-row values: audit plan v3 §2.5). The table replaces the
"<!-- INPUT TABLE -->" marker and anything after it in the methods page.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

from astropy.table import Table

ROOT = Path(__file__).resolve().parents[3]
MARK = "<!-- INPUT TABLE -->"

NUM = r"[−-]?\d+(?:\.\d+)?"


def redact(s: str) -> str:
    s = re.sub(r'\("[^"]*\d[^"]*"[^)]*\)', "(printed value)", s)          # ("µ = 19.62 mag", ...)
    s = re.sub(r'"[^"]*\d[^"]*"', '"[value]"', s)
    s = re.sub(rf"\(?\s*(?:rh|µ|m − M|R_e|Re)\s*=\s*{NUM}[^,;)]*\)?", "[value]", s)
    s = re.sub(rf"{NUM}\s*(?:\+-|±|\+/-)\s*{NUM}(?:\s*(?:pc|kpc|mag))?", "[value]", s)
    s = re.sub(rf"=\s*{NUM}(?:\s*(?:pc|kpc|mag|arcmin))?", "= [value]", s)
    s = re.sub(rf"\(\s*{NUM}\s*(?:pc|kpc)\s*\)", "([value])", s)
    s = re.sub(rf"midpoint of \[value\] to \[value\]", "midpoint of the two printed values", s)
    return s


def where_text(rule: dict | None) -> str:
    if not rule:
        return ""
    w = rule.get("where", {})
    parts = [f"{k}: {v}" for k, v in w.items()]
    return " · ".join(parts)


def rules_for(pkg: Path):
    rules = json.loads((pkg / "locators.json").read_text(encoding="utf-8"))["rules"]
    comp = [(re.compile(r["match"]), r) for r in rules if r["table"] == "observables"]

    def find(ref: str):
        hits = [r for c, r in comp if c.match(ref)]
        return hits[0] if len(hits) == 1 else None
    return find


def dwarfs() -> str:
    pkg = ROOT / "data/packages/aeg-d-dwarfs/v3"
    m = Table.read(pkg / "tables/measurements.ecsv", format="ascii.ecsv")
    o = {r["observable_id"]: r for r in Table.read(pkg / "tables/observables.ecsv", format="ascii.ecsv")}
    s = {r["system_id"]: r for r in Table.read(pkg / "tables/systems.ecsv", format="ascii.ecsv")}
    gas_rows = {r["key"]: r for r in csv.DictReader(open(ROOT / "data/packages/aeg-d-dwarfs/v1/reading/gas_values.csv", encoding="utf-8"))}
    find = rules_for(pkg)
    order = ["sigma_los", "half_light_radius", "distance", "apparent_magnitude", "luminosity", "metallicity_feh"]
    label = {"sigma_los": "σ", "half_light_radius": "r_h and ε", "distance": "Distance", "apparent_magnitude": "m_V,0",
             "luminosity": "Magnitude route (if no m_V,0)", "metallicity_feh": "[Fe/H]"}
    out = []
    rows = sorted((r for r in m if str(r["role"]) == "default"), key=lambda r: str(s[r["system_id"]]["name_in_source"]))
    for r in rows:
        sys_ = s[r["system_id"]]
        props = json.loads(str(sys_["properties"]))
        key = props.get("lvdb_key", "")
        oids = [x for x in (str(r["observed_from"]) + ";" + str(r["baryonic_from"])).split(";") if x in o]
        by_q: dict[str, list] = {}
        for x in oids:
            by_q.setdefault(str(o[x]["quantity"]), []).append(o[x])
        out.append(f"### {sys_['name_in_source']}\n")
        out.append("| Input | Read from | Place (locator) |\n|---|---|---|")
        for q in order:
            for ob in by_q.get(q, []):
                if q == "luminosity" and "apparent_magnitude" in by_q:
                    continue
                ref = redact(str(ob["source_ref"]))
                extra = ""
                if q == "half_light_radius":
                    conv = re.sub(r"^as printed \((.*)\)$", r"\1", str(ob["x_dwarfs_parameter"]))
                    extra = f" Convention: {conv}."
                if q == "sigma_los" and str(ob["limit"]) == "upper":
                    extra = " An upper limit."
                out.append(f"| {label[q]} | {ref}.{extra} | {where_text(find(str(ob['source_ref'])))} |")
        g = gas_rows.get(key, {})
        gs = str(r["x_dwarfs_gas_status"])
        if gs == "not addressed":
            gtxt, gplace = "Not in Putman et al. 2021 Table 1: no gas term", ""
        else:
            gtxt = f"Putman et al. 2021 Table 1, row \"{g.get('galaxy_as_printed', '')}\"; " + (
                "an upper limit: no gas term" if gs.startswith("absent") else "a detection: MHI and Dist")
            gplace = "table 1; row as named"
        out.append(f"| Gas | {gtxt} | {gplace} |")
        out.append(f"| Υ_V | McLaughlin & van der Marel 2005 `clusters`, (M/L)1 interpolated at the [Fe/H] above | |\n")
    return "\n".join(out)


def write(page: Path, table: str) -> None:
    t = page.read_text(encoding="utf-8")
    if MARK not in t:
        raise SystemExit(f"no marker in {page}")
    t = t[: t.index(MARK) + len(MARK)] + "\n\n" + table.rstrip() + "\n"
    page.write_text(t, encoding="utf-8")


def main() -> int:
    write(ROOT / "docs/methods/datasets/aeg-d-dwarfs.md", dwarfs())
    return 0


if __name__ == "__main__":
    sys.exit(main())
