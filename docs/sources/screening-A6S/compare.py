"""Compare the two independent A6·strong lensing screenings (reader A and reader B).

Usage: python docs/sources/screening-A6S/compare.py
Written and committed before either reading was opened.

Reads reader-{a,b}-block{1,2}.md, takes the decision code of each R row (the first of E, E-pair,
P, X, NS or — in the Decision column), and writes comparison.csv with one row per R number:
r, decision_a, decision_b, agree. Codes are compared as written ("E-pair" differs from "E").
Rows missing from a reading are recorded as "missing". Prints the agreement count.
Disagreements are settled by Claude reading the source for that record, and recorded in
adjudication.md with the reason; neither reading is edited.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODES = ["E-pair", "E", "P", "X", "NS", "—"]


def decisions(reader: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for block in (1, 2):
        path = HERE / f"reader-{reader}-block{block}.md"
        header = None
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if header is None and any(c.lower().startswith("decision") for c in cells):
                header = [c.lower() for c in cells]
                continue
            m = re.match(r"^R(\d+)$", cells[0].replace("*", ""))
            if not m or header is None:
                continue
            cell = cells[header.index(next(h for h in header if h.startswith("decision")))]
            cell = cell.replace("*", "")
            code = next((c for c in CODES if re.match(rf"^{re.escape(c)}\b", cell)), cell[:12] or "blank")
            out[f"R{int(m.group(1))}"] = code
    return out


def main() -> int:
    a, b = decisions("a"), decisions("b")
    keys = sorted(set(a) | set(b) | {f"R{i}" for i in range(1, 60)}, key=lambda k: int(k[1:]))
    rows = [{"r": k, "decision_a": a.get(k, "missing"), "decision_b": b.get(k, "missing")} for k in keys]
    for r in rows:
        r["agree"] = "yes" if r["decision_a"] == r["decision_b"] and r["decision_a"] != "missing" else "no"
    with open(HERE / "comparison.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["r", "decision_a", "decision_b", "agree"])
        w.writeheader()
        w.writerows(rows)
    n = sum(r["agree"] == "yes" for r in rows)
    print(f"{n} of {len(rows)} decisions agree; disagreements: {', '.join(r['r'] for r in rows if r['agree'] == 'no') or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
