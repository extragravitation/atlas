"""Apply the frozen D-048 kind-basis rule (docs/methods/D048_KIND_BASIS.md) mechanically.

Inputs: reading/kind_coding_mw.csv, reading/kind_coding_m31_field.csv (first coding),
reading/kind_coding_second.csv (20% double coding), the pinned LVDB tables (for
confirmed_star_cluster). Writes reading/kinds.csv and reading/double_coding_agreement.csv.

Rule: A7 if any paper is coded X or LVDB confirmed_star_cluster = 1; otherwise A5 if any
paper gives L, P or G; otherwise A7 ("galaxy label rests on dynamics or metallicity spread
only", or "no stated ground"). Unread papers contribute nothing.
"""

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
R = HERE / "reading"


def codes_of(rows):
    out = {}
    for r in rows:
        cs = {c.strip().upper() for c in (r["codes"] or "").replace(",", ";").split(";") if c.strip()}
        out.setdefault(r["key"], []).append((r["role"], r["ref"], cs))
    return out


def kind(papers, star_cluster_flag):
    allc = set().union(*[c for _, _, c in papers]) if papers else set()
    if "X" in allc or star_cluster_flag:
        return "A7", "a paper disputes the kind or calls it a star cluster" if "X" in allc else "LVDB confirmed_star_cluster = 1"
    if allc & {"L", "P", "G"}:
        return "A5", "label supported by light/structure, population or gas: " + ",".join(sorted(allc & {"L", "P", "G"}))
    if allc & {"D", "M"}:
        return "A7", "galaxy label rests on dynamics or metallicity spread only"
    return "A7", "no stated ground (or no paper read)"


def main() -> int:
    first = []
    for f in ("kind_coding_mw.csv", "kind_coding_m31_field.csv"):
        first += list(csv.DictReader((R / f).open(encoding="utf-8")))
    second = list(csv.DictReader((R / "kind_coding_second.csv").open(encoding="utf-8")))
    lvdb = {}
    for t in ("dwarf_mw", "dwarf_m31", "dwarf_local_field"):
        for r in csv.DictReader((HERE / "source/lvdb" / f"{t}.csv").open(encoding="utf-8")):
            lvdb[r["key"]] = r
    systems = list(csv.DictReader((R / "reading_list.csv").open(encoding="utf-8")))
    c1, c2 = codes_of(first), codes_of(second)
    rows, agree = [], []
    for s in systems:
        k = s["key"]
        flag = str(lvdb.get(k, {}).get("confirmed_star_cluster", "")).strip() in ("1", "1.0")
        kd, why = kind(c1.get(k, []), flag)
        rows.append({"key": k, "name": s["name"], "host": s["host"], "kind": kd, "reason": why,
                     "papers_coded": len(c1.get(k, [])), "unread": sum(1 for _, _, c in c1.get(k, []) if not c)})
        if k in c2:
            kd2, why2 = kind(c2[k], flag)
            agree.append({"key": k, "kind_first": kd, "kind_second": kd2, "agree": kd == kd2,
                          "codes_first": " | ".join(f"{ro}:{','.join(sorted(c))}" for ro, _, c in c1.get(k, [])),
                          "codes_second": " | ".join(f"{ro}:{','.join(sorted(c))}" for ro, _, c in c2[k])})
    for name, data in (("kinds.csv", rows), ("double_coding_agreement.csv", agree)):
        with (R / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
    n5 = sum(r["kind"] == "A5" for r in rows)
    print(f"A5 {n5}, A7 {len(rows) - n5}; double-coded {len(agree)}, kind agreement {sum(a['agree'] for a in agree)}/{len(agree)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
