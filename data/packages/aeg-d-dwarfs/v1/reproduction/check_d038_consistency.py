"""D-038 3A consistency check for A5/A7: originals against Geha et al. 2026 (REPRODUCTION.md,
"Reported, not pass/fail"), by the frozen aeg.repro_dispersion.compare_pair and consistency.

Usage (from the package directory): python reproduction/check_d038_consistency.py
Written and frozen before it was run.

Pairs: every system whose package default (reading/sigma_selection_v3.csv, plotted) is an
original paper (not Geha 2026) and for which Geha et al. 2026 prints a value
(reading/sigma_values.csv, value v1, the paper's whole-sample 2 r_eff value or its 95% upper
limit). Duplicate printings must agree, else the script stops. The original's value is the
package's plotted default, with its printed errors or its upper limit. For And XII (D-062)
the original is treated as an upper limit at 0.0 + its printed upper error, as plotted.
Writes checks/d038_consistency.csv and prints the population outcome.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "pipeline"))
from aeg.repro_dispersion import Value, compare_pair, consistency  # noqa: E402

PKG = Path(__file__).resolve().parents[1]


def f(x):
    try:
        return float(str(x).replace("−", "-"))
    except ValueError:
        return None


def main() -> int:
    sel = {r["key"]: r for r in csv.DictReader(open(PKG / "reading/sigma_selection_v3.csv", encoding="utf-8"))
           if (r["sigma"].strip() or r["limit"].strip()) and not r["default_paper"].startswith("Geha 2026")}
    geha = {}
    for r in csv.DictReader(open(PKG / "reading/sigma_values.csv", encoding="utf-8")):
        if r["paper"].startswith("Geha 2026") and r["value_id"] == "v1":
            geha.setdefault(r["key"], set()).add((r["sigma"].strip(), r["err_minus"].strip(), r["err_plus"].strip(),
                                                  r["limit"].strip()))
    rows, pairs = [], []
    for k in sorted(set(sel) & set(geha)):
        g = geha[k]
        if len(g) != 1:
            raise SystemExit(f"{k}: Geha printings disagree: {g}")
        gs, glo, ghi, glim = next(iter(g))
        G = Value(None, upper_limit=f(gs)) if glim == "upper" else Value(f(gs), f(glo) or 0.0, f(ghi) or 0.0)
        s = sel[k]
        if s["limit"] == "upper":
            O = Value(None, upper_limit=f(s["sigma"]))
        elif f(s["sigma"]) == 0.0:
            O = Value(None, upper_limit=f(s["sigma"]) + f(s["err_plus"]))
        else:
            O = Value(f(s["sigma"]), f(s["err_minus"]) or 0.0, f(s["err_plus"]) or 0.0)
        p = compare_pair(k, O, G)
        pairs.append(p)
        rows.append({"key": k, "original": s["default_paper"], "sigma_original": s["sigma"], "lo_original": s["err_minus"],
                     "hi_original": s["err_plus"], "limit_original": s["limit"], "sigma_geha": gs, "lo_geha": glo,
                     "hi_geha": ghi, "limit_geha": glim, "z": "" if p.z is None else f"{p.z:.3f}",
                     "consistent": "yes" if p.consistent else "no"})
    c = consistency(pairs)
    (PKG / "checks").mkdir(exist_ok=True)
    with open(PKG / "checks/d038_consistency.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"D-038 3A: {len(pairs)} pairs, {c.n_z} with z; |z|>2 fraction {c.frac_beyond_2}; median z {c.median_z}; "
          f"outcome {c.outcome}; per-pair inconsistent: {[p.system for p in pairs if not p.consistent]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
