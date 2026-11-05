"""Audit part B term scan (plan v2 §3.2). Committed before it is run.

Usage:
    python docs/audit/term_scan.py SITE_DIST_DIR OUT_CSV

Lists every occurrence (case-insensitive, whole words) of the frozen term list in all text a
visitor can read in the built site: the visible text of every HTML page (scripts and styles
removed; title, alt, aria-label and title attributes kept), and every README or text file in
the downloads. Each occurrence is written with its page, the matched term and 120 characters of
context on each side, for a reader to classify as allowed or finding. Standard library only.
"""

from __future__ import annotations

import csv
import html
import re
import sys
from pathlib import Path

TERMS = [
    ("dark matter", r"dark\s+matter"),
    ("halo", r"halo(?:e?s)?"),
    ("missing mass", r"missing\s+mass"),
    ("mass discrepancy", r"mass\s+discrepanc(?:y|ies)"),
    ("unseen/invisible/hidden mass or matter", r"(?:unseen|invisible|hidden)\s+(?:mass|matter)"),
    ("MOND", r"MOND"),
    ("Milgrom", r"Milgrom(?:'s|ian)?"),
    ("modified gravity", r"modified\s+gravity"),
    ("modified Newtonian", r"modified\s+Newtonian"),
    ("emergent gravity", r"emergent\s+gravity"),
    ("a0", r"a0|a₀|a_0"),
    ("acceleration scale", r"acceleration\s+scales?"),
    ("NFW", r"NFW"),
    ("Einasto", r"Einasto"),
    ("Burkert", r"Burkert"),
    ("explains", r"explains"),
    ("explained by", r"explained\s+by"),
    ("evidence for", r"evidence\s+for"),
]
PATTERN = re.compile(r"(?<![\w])(" + "|".join(f"(?P<t{i}>{p})" for i, (_, p) in enumerate(TERMS)) + r")(?![\w])", re.I)
ATTRS = re.compile(r'\s(?:alt|title|aria-label)="([^"]*)"', re.I)


def visible_text(raw: str) -> str:
    raw = re.sub(r"<(script|style|svg\s+[^>]*aria-hidden=\"true\")[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    attrs = " ".join(ATTRS.findall(raw))
    m = re.search(r"<title>(.*?)</title>", raw, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape((m.group(1) if m else "") + " " + text + " " + attrs)
    return re.sub(r"\s+", " ", text)


def main(argv):
    dist, out = Path(argv[1]), Path(argv[2])
    rows = []
    files = sorted(p for p in dist.rglob("*") if p.is_file() and p.suffix.lower() in (".html", ".md", ".txt"))
    for p in files:
        raw = p.read_text(encoding="utf-8", errors="replace")
        text = visible_text(raw) if p.suffix.lower() == ".html" else re.sub(r"\s+", " ", raw)
        for m in PATTERN.finditer(text):
            term = next(TERMS[int(k[1:])][0] for k, v in m.groupdict().items() if v)
            rows.append({
                "page": str(p.relative_to(dist)), "term": term, "match": m.group(0),
                "context": text[max(0, m.start() - 120): m.end() + 120],
            })
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["page", "term", "match", "context"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(files)} files scanned, {len(rows)} occurrences")
    for t, _ in TERMS:
        print(f"  {t}: {sum(r['term'] == t for r in rows)}")


if __name__ == "__main__":
    main(sys.argv)
