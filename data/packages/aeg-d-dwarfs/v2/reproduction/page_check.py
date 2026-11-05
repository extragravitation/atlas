"""REPRODUCTION.md item 12, last check: each excluded system's built page contains its excluded.csv quotation exactly.

Usage (repository root, after the site build): python data/packages/aeg-d-dwarfs/v2/reproduction/page_check.py

The page's text is taken by stripping tags and unescaping HTML entities; whitespace runs are collapsed to one
space on both sides (the page wraps text; the register stores one line).
"""

from __future__ import annotations

import csv
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]


def text_of(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<style\b.*?</style>", " ", raw, flags=re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw)).split())


def main() -> int:
    rows = [r for r in csv.DictReader(open(ROOT / "data/registry/excluded.csv", encoding="utf-8")) if r["dataset"] == "aeg-d-dwarfs/v2"]
    res = []
    for r in rows:
        page = ROOT / "site/dist/systems" / r["system"] / "index.html"
        t = text_of(page) if page.is_file() else ""
        res.append({"system": r["system"], "page": str(page.relative_to(ROOT)), "found": " ".join(r["reason"].split()) in t})
    print(json.dumps({"pass": bool(res) and all(x["found"] for x in res), "checked": len(res), "results": res}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
