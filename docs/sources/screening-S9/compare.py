"""S9 comparison (stellar masses for clusters, D-068): the two readings matched by record.

Written and committed before either reading was opened. Same method as the A9 compare_v2.py:
rows are matched within each entry (S<n>) by the record's identifier (arXiv id, VizieR path,
Zenodo DOI, GitHub repository or bibcode), so differences in how readers split catalogue rows
do not misalign the comparison. Writes comparison.csv; decisions are not changed.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODES = ["E-pair", "E", "P", "X", "NS", "—"]
ID_PATTERNS = [r"\b\d{4}\.\d{4,5}\b", r"astro-ph/\d{7}", r"J/[A-Za-z+&]+/\d+/[A-Z]?\d+", r"zenodo\.\d+", r"[\w-]+/[\w.-]+(?=\s*\(GitHub|; GitHub)", r"\b\d{4}[A-Za-z&.]{5}[\d.]{4}[A-Za-z.\d]{5}[A-Z.]\b"]


def ids(text: str) -> set[str]:
    out = set()
    for p in ID_PATTERNS:
        out |= {m.group(0).replace("&", "+") for m in re.finditer(p, text)}
    return out


def rows(reader: str) -> list[dict]:
    out = []
    for _ in (1,):
        header = None
        for line in (HERE / f"reader-{reader}.md").read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if header is None and any(c.lower().startswith("decision") for c in cells):
                header = [c.lower() for c in cells]
                continue
            m = re.match(r"^S(\d+)([a-z]?)$", cells[0].replace("*", ""))
            if not m or header is None:
                continue
            dec = cells[next(i for i, h in enumerate(header) if h.startswith("decision"))].replace("*", "")
            code = next((c for c in CODES if re.match(rf"^{re.escape(c)}\b", dec)), dec[:12] or "blank")
            out.append({"row": cells[0].replace("*", ""), "entry": int(m.group(1)), "ids": ids(cells[1]), "code": code})
    return out


def main() -> int:
    A, B = rows("a"), rows("b")
    pairs, usedB = [], set()
    for a in A:
        match = [b for b in B if b["entry"] == a["entry"] and a["ids"] & b["ids"]]
        if match:
            for b in match:
                pairs.append((a["row"], b["row"], a["code"], b["code"]))
                usedB.add(b["row"])
        else:
            pairs.append((a["row"], "unmatched", a["code"], "missing"))
    for b in B:
        if b["row"] not in usedB:
            pairs.append(("unmatched", b["row"], "missing", b["code"]))
    with open(HERE / "comparison.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row_a", "row_b", "decision_a", "decision_b", "agree"])
        for ra, rb, da, db in pairs:
            w.writerow([ra, rb, da, db, "yes" if da == db else "no"])
    n = sum(da == db for _, _, da, db in pairs)
    print(f"{n} of {len(pairs)} matched pairs agree; unmatched rows: A {sum(rb == 'unmatched' for _, rb, _, _ in pairs)}, B {sum(ra == 'unmatched' for ra, _, _, _ in pairs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
