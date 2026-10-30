"""Compare the two independent dispersion readings (reading/SIGMA_READING_BRIEF.md).

Usage: python reproduction/compare_sigma_readings.py READING1_DIR READING2_DIR OUT_CSV

For each (system, paper), the printed numbers are compared as sets: (sigma, err_minus,
err_plus, limit, limit_level) exactly as transcribed (strings, whitespace and a leading
"+" removed). Order and value_id are ignored, because the readers number values
independently. Text fields (estimator, sample, coverage_stated, binaries, gradient) are not
compared here; they are resolved by reading the paper when the rules use them.

Status per (system, paper):
  agree         the same set of numbers;
  disagree      different sets (each reading's numbers are listed);
  only_1/only_2 one reader recorded the pair, the other did not.
"""

from __future__ import annotations

import csv
import glob
import sys
from collections import defaultdict


def norm(x: str) -> str:
    x = (x or "").strip().replace("−", "-").replace(" ", "")
    return x[1:] if x.startswith("+") else x


def load(d: str) -> dict:
    out = defaultdict(list)
    for f in sorted(glob.glob(f"{d}/sheet*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            t = tuple(norm(r.get(c, "")) for c in ("sigma", "err_minus", "err_plus", "limit", "limit_level"))
            out[(r["key"].strip(), r["paper"].strip())].append(t)
    return out


def main(a: str, b: str, out_csv: str) -> int:
    r1, r2 = load(a), load(b)
    rows, counts = [], defaultdict(int)
    for k in sorted(set(r1) | set(r2)):
        s1, s2 = sorted(r1.get(k, [])), sorted(r2.get(k, []))
        st = "only_2" if k not in r1 else "only_1" if k not in r2 else "agree" if s1 == s2 else "disagree"
        counts[st] += 1
        rows.append({"key": k[0], "paper": k[1], "status": st,
                     "reading_1": " | ".join("/".join(t) for t in s1), "reading_2": " | ".join("/".join(t) for t in s2)})
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["key", "paper", "status", "reading_1", "reading_2"])
        w.writeheader()
        w.writerows(rows)
    print(dict(counts))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
