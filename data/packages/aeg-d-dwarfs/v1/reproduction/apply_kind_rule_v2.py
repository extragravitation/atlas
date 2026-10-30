"""Apply the frozen D-049 kind-basis rule, version 2 (docs/methods/D049_KIND_BASIS_V2.md), mechanically.

Sheets (reading/):
- kind_coding_mw.csv and kind_coding_m31_field.csv: first coding;
- kind_coding_v2_scans.csv: pre-arXiv papers read as ADS scans; replaces a row with the same key and ref;
- kind_coding_v2_agent.csv: structural references for systems with no discovery paper, plus provisional rows re-coded by grounds; replaces a row with the same key and ref, or adds one;
- kind_coding_second.csv: 20% double coding.

Version 2:
- X counts only for "cluster" or "kind undetermined". In the Milky Way coder's sheet, X rows tagged "provisional" in reader_note (and not "open" or "cluster") lose the X and keep their other codes.
- An X is superseded by a strictly later paper (year from the reference key) with L, P or G.
- Then: A7 if an X stands; A5 if any paper gives L, P or G; otherwise A7.

Writes reading/kinds.csv and reading/double_coding_agreement.csv.
"""

import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
R = HERE / "reading"
GOOD = {"L", "P", "G"}


def year(ref: str) -> int:
    m = re.search(r"(1[6-9]\d\d|20\d\d)", ref.split("|")[0])
    return int(m.group(1)) if m else 0


def effective(row: dict, sheet: str) -> set[str]:
    cs = {c.strip().upper() for c in (row["codes"] or "").replace(",", ";").split(";") if c.strip()}
    cs = {c for c in cs if c in {"L", "P", "G", "D", "M", "N", "X"}}
    note = (row.get("reader_note") or "").lower()
    if "X" in cs and sheet == "mw" and "x(provisional)" in note and "x(open)" not in note and "x(cluster)" not in note:
        cs.discard("X")
    return cs


def load(name, sheet):
    p = R / name
    return [(r, sheet) for r in csv.DictReader(p.open(encoding="utf-8"))] if p.is_file() else []


def kind(papers):
    """papers: list of (year, codes)."""
    xs = [y for y, c in papers if "X" in c]
    standing = [y for y in xs if not any(y2 > y and c2 & GOOD for y2, c2 in papers)]
    if standing:
        return "A7", "a paper concludes the kind is undetermined or calls it a star cluster, not superseded on light, population or gas grounds"
    allc = set().union(*[c for _, c in papers]) if papers else set()
    if allc & GOOD:
        return "A5", "label supported by light/structure, population or gas: " + ",".join(sorted(allc & GOOD))
    if allc & {"D", "M"}:
        return "A7", "galaxy label rests on dynamics or metallicity spread only"
    return "A7", "no stated ground (or no paper read)"


def main() -> int:
    first = load("kind_coding_mw.csv", "mw") + load("kind_coding_m31_field.csv", "m31")
    # one entry per (system, paper, role): a scan reading replaces the same paper in the same role;
    # a structural-reference row is added beside any row for the same paper in another role.
    table = {}
    for r, s in first:
        table[(r["key"], r["ref"].split("|")[0], r["role"])] = (r, s)
    for name in ("kind_coding_v2_scans.csv", "kind_coding_v2_agent.csv"):
        for r, s in load(name, "v2"):
            table[(r["key"], r["ref"].split("|")[0], r["role"])] = (r, s)
    per = {}
    for (k, ref, _role), (r, s) in table.items():
        per.setdefault(k, []).append((year(ref), effective(r, s)))
    second = {}
    for r, s in load("kind_coding_second.csv", "second"):
        second.setdefault(r["key"], []).append((year(r["ref"]), effective(r, s), r["ref"].split("|")[0]))
    systems = list(csv.DictReader((R / "reading_list.csv").open(encoding="utf-8")))
    rows, agree = [], []
    for sy in systems:
        k = sy["key"]
        kd, why = kind(per.get(k, []))
        rows.append({"key": k, "name": sy["name"], "host": sy["host"], "kind": kd, "reason": why,
                     "papers": len(per.get(k, [])), "unread": sum(1 for _, c in per.get(k, []) if not c)})
        if k in second:
            # compare on the papers both coders could read (a paper unread by either is left out)
            read2 = {ref for _, c, ref in second[k] if c}
            first_rows = [(ref, year(ref), effective(r, s)) for (kk, ref, role), (r, s) in table.items()
                          if kk == k and role in ("discovery", "vlos")]
            both = {ref for ref, _, c in first_rows if c} & read2
            k1, _ = kind([(y, c) for ref, y, c in first_rows if ref in both])
            k2, _ = kind([(y, c) for y, c, ref in second[k] if ref in both])
            agree.append({"key": k, "papers_both_read": len(both), "kind_first": k1, "kind_second": k2,
                          "agree": (k1 == k2) if both else "not comparable (no paper read by both)"})
    for name, data in (("kinds.csv", rows), ("double_coding_agreement.csv", agree)):
        with (R / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
    n5 = sum(r["kind"] == "A5" for r in rows)
    comp = [a for a in agree if a["agree"] in (True, False)]
    print(f"v2: A5 {n5}, A7 {len(rows) - n5}; double-coded {len(agree)}, comparable {len(comp)}, "
          f"agreement {sum(a['agree'] is True for a in comp)}/{len(comp)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
