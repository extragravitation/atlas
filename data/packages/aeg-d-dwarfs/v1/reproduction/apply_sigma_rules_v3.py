"""Apply the frozen dispersion rules to the coded values, version 3 (D-055).

Version 3 adds one step to version 2. Where D-055 names the value to use for a (system,
paper) that the rules could not settle (reading/d055_choices.csv), that value is used and
the paper's other whole-sample values are recorded with the reason "D-055 item N". D-055
item 1 (Hendricks 2014 is an original) is applied in reading/sigma_candidates.csv. Nothing
else changes.

Version 2 docstring follows.

Version 1 (apply_sigma_rules.py) stays as committed, and its result is kept on record:
reading/sigma_selection.csv. Version 2 differs from it in exactly three places, all set by
D-051:
- Coverage (step 3). A value also passes D-038 1A where the source's own per-star member
  table shows at least one member used beyond the half-light ellipse
  (reading/coverage_tables.csv, made by reproduction/coverage_from_tables.py with
  aeg.coverage). A value whose paper releases per-star velocities, but whose table could not
  be reached, is recorded with the reason "coverage not checkable".
- Duplicate printings (step 2). Where several rows are marked as the paper's result, they
  are printings of one estimate. The row printed in a table is used; otherwise the one with
  the most significant digits; a remaining tie is listed for a ruling.
- Lower limits. Recorded and never plotted (unchanged from version 1; now ruled).

Earlier docstring, unchanged in substance:

Usage: python reproduction/apply_sigma_rules.py CODED_CSV OUT_ROWS_CSV OUT_SYSTEMS_CSV

Written and committed before the coding was seen. The steps follow the frozen text in order:

1. Candidates (REPRODUCTION.md, D-036 iii). A candidate is a row with `what = measured`,
   `dimension = los`, `form = global` and `limit` `none` or `upper`.
   Not candidates, each recorded with its reason:
   - quoted values (their source is listed for follow-up);
   - predictions, simulations, gas, assumed values;
   - 3-D values;
   - profile bins (D-038 2D: used under the profile rule, not as a single value);
   - approximate values and ranges;
   - lower limits (no frozen rule; recorded and listed for a ruling).
2. One value per paper (D-038 2B, 2A and its addendum).
   - Whole-sample values are kept; subsets are recorded.
   - Among whole-sample values, a value whose `rotation` is `second_moment`, `none_fitted` or `not_stated`
     is preferred to `about_rotation`. The `about_rotation` value is used only if the paper
     gives no other.
   - If more than one value remains, the one whose `variant` begins with `headline` is used.
     Otherwise the paper is marked `unresolved_within_paper` and listed for a ruling: the
     script never picks by value.
3. Plotting rule D-038 1A (D-042 item 2: plotting rules before precedence). The paper's
   value passes if `coverage = beyond_rh`; otherwise it is an aperture value, recorded and
   not plotted. Upper limits follow the same rule and are plotted as limits.
4. Precedence among the papers whose value passes (D-038 3A, 3B; D-042 items 1 and 2).
   - Originals come before re-analyses. A re-analysis is the default only where no original
     value passes.
   - Then the paper that releases per-star velocities comes first, then the most member
     stars (blank counts as fewest), then the most recent year.
   - A tie on all three is listed for a ruling.
   - Papers of kind `unclear` are listed for a ruling and not used.
   - Every passing value is kept as an alternative.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
_tab = PKG / "reading/coverage_tables.csv"
TABLES = {(r["key"], r["paper"]): r for r in csv.DictReader(open(_tab, encoding="utf-8"))} if _tab.exists() else {}


def sig_digits(x: str) -> int:
    d = "".join(ch for ch in x if ch.isdigit()).lstrip("0")
    return len(d)


def duplicate_printing(head: list) -> list:
    """D-051: several printings of the paper's adopted estimate -> the table printing, else most digits."""
    tab = [r for r in head if "table" in r.get("location", "").lower()]
    pool = tab if len(tab) >= 1 else head
    if len(pool) > 1:
        top = max(sig_digits(r["sigma"]) for r in pool)
        pool = [r for r in pool if sig_digits(r["sigma"]) == top]
    return pool


def kind_of(paper: str, key: str) -> str:
    for r in csv.DictReader(open(PKG / "reading/sigma_candidates.csv", encoding="utf-8")):
        if r["paper"] == paper and r["key"] == key:
            return r["kind_of_source"]
    return "unclear"


def as_int(x: str) -> int:
    try:
        return int(str(x).strip().replace(",", ""))
    except ValueError:
        return -1


def candidate_reason(r: dict) -> str:
    if r["what"] == "quoted":
        return "quoted from another paper"
    if r["what"] != "measured":
        return f"not a measurement ({r['what']})"
    if r["dimension"] != "los":
        return f"not line-of-sight ({r['dimension']})"
    if r["form"] == "profile_bin":
        return "profile bin (D-038 2D)"
    if r["form"] in ("approximate", "range"):
        return f"{r['form']} value"
    if r["limit"] == "lower":
        return "lower limit (no frozen rule)"
    if r["sigma"].strip() == "":
        return "no value printed"
    return ""


def main(coded: str, out_rows: str, out_systems: str) -> int:
    rows = list(csv.DictReader(open(coded, encoding="utf-8")))
    loc = {(v["key"], v["paper"], v["value_id"]): v["location"]
           for v in csv.DictReader(open(PKG / "reading/sigma_values.csv", encoding="utf-8"))}
    for r in rows:
        r["location"] = loc.get((r["key"], r["paper"], r["value_id"]), "")
    for r in rows:
        r["status"], r["reason"] = "", candidate_reason(r)
        if r["reason"]:
            r["status"] = "recorded"
    by_paper: dict[tuple, list] = defaultdict(list)
    for r in rows:
        if not r["status"]:
            by_paper[(r["key"], r["paper"])].append(r)

    chosen: dict[tuple, dict | None] = {}
    flags: dict[str, list] = defaultdict(list)
    choices = {(c["key"], c["paper"]): c for c in csv.DictReader(open(PKG / "reading/d055_choices.csv", encoding="utf-8"))}
    for (key, paper), rs in by_paper.items():
        ch = choices.get((key, paper))
        if ch:
            pick = [r for r in rs if r["value_id"] == ch["value_id"]]
            if len(pick) != 1:
                raise ValueError(f"D-055 choice not found among candidates: {key} {paper} {ch['value_id']}")
            for r in rs:
                if r is not pick[0]:
                    r["status"], r["reason"] = "recorded", f"D-055 item {ch['d055_item']}: {ch['reason']}"
            rs = pick
        whole = [r for r in rs if r["whole_sample"] == "yes"]
        for r in rs:
            if r["whole_sample"] != "yes":
                r["status"], r["reason"] = "recorded", "subset (D-038 2B)"
        pref = [r for r in whole if r["rotation"] in ("second_moment", "none_fitted", "not_stated")] or whole
        for r in whole:
            if r not in pref:
                r["status"], r["reason"] = "recorded", "dispersion about rotation; second moment used (D-038 2A)"
        if len(pref) > 1:
            head = [r for r in pref if r["variant"].strip().lower().startswith("headline")]
            if len(head) > 1:
                head = duplicate_printing(head)
            if len(head) == 1:
                for r in pref:
                    if r is not head[0]:
                        r["status"], r["reason"] = "recorded", "paper's other variant or printing; headline used (D-051 duplicate printing)"
                pref = head
        if len(pref) > 1:
            for r in pref:
                r["status"], r["reason"] = "ruling", "unresolved_within_paper"
            flags[key].append(f"{paper}: several whole-sample values, " + ("printings tie" if any(r["variant"].strip().lower().startswith("headline") for r in pref) else "none marked headline"))
            chosen[(key, paper)] = None
            continue
        if not pref:
            chosen[(key, paper)] = None
            continue
        c = pref[0]
        tab = TABLES.get((key, paper))
        c["coverage_table"] = tab["status"] if tab else ""
        ok = c["coverage"] == "beyond_rh" or (tab is not None and tab["status"] == "checked" and tab["passes"] == "True")
        if not ok:
            if c["velocities_released"] == "yes" and (tab is None or tab["status"] != "checked"):
                why = "aperture: coverage not checkable (table not reached; D-051)"
            else:
                why = f"aperture: coverage {c['coverage']}" + (" and table shows no member beyond R_h" if tab and tab["status"] == "checked" else "") + " (D-038 1A, D-051)"
            c["status"], c["reason"] = "recorded", why
            chosen[(key, paper)] = None
            continue
        c["status"] = "passes"
        chosen[(key, paper)] = c

    systems = []
    keys = sorted({r["key"] for r in rows})
    for key in keys:
        passing = [(p, c) for (k, p), c in chosen.items() if k == key and c is not None]
        unclear = [p for p, c in passing if kind_of(p, key) == "unclear"]
        for p in unclear:
            flags[key].append(f"{p}: kind of source unclear")
        passing = [(p, c) for p, c in passing if kind_of(p, key) != "unclear"]
        orig = [(p, c) for p, c in passing if kind_of(p, key) == "original"]
        pool = orig or passing
        default, how = None, ""
        if pool:
            def rank(pc):
                p, c = pc
                return (c["velocities_released"] == "yes", as_int(c["n_members"]), as_int(c["year"]))
            pool.sort(key=rank, reverse=True)
            if len(pool) > 1 and rank(pool[0]) == rank(pool[1]):
                flags[key].append("precedence tie")
            else:
                default = pool[0]
                how = ("original" if orig else "re-analysis (no original passes)") + (
                    "; only passing value" if len(passing) == 1 else "; precedence D-038 3B")
        for p, c in passing:
            c["status"] = "default" if default and c is default[1] else "alternative"
        lower = [r for r in rows if r["key"] == key and r["reason"] == "lower limit (no frozen rule)"]
        quoted = sorted({r["quoted_from"] for r in rows if r["key"] == key and r["what"] == "quoted" and r.get("quoted_from")})
        d = default[1] if default else None
        systems.append({
            "key": key,
            "default_paper": default[0] if default else "",
            "default_value_id": d["value_id"] if d else "",
            "sigma": d["sigma"] if d else "", "err_minus": d["err_minus"] if d else "", "err_plus": d["err_plus"] if d else "",
            "limit": d["limit"] if d else "", "limit_level": d["limit_level"] if d else "",
            "how": how,
            "n_passing": len(passing),
            "papers_considered": len({p for (k, p) in chosen if k == key}),
            "aperture_only": "yes" if not passing and any(r["key"] == key and r["reason"].startswith("aperture") for r in rows) else "",
            "lower_limits": len(lower),
            "quoted_sources_to_check": "; ".join(quoted),
            "for_ruling": " | ".join(flags.get(key, [])),
        })

    with open(out_rows, "w", newline="", encoding="utf-8") as f:
        names = list(dict.fromkeys(k for r in rows for k in r))
        w = csv.DictWriter(f, fieldnames=names, restval="")
        w.writeheader()
        w.writerows(rows)
    with open(out_systems, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(systems[0]))
        w.writeheader()
        w.writerows(systems)
    n_def = sum(1 for s in systems if s["default_paper"])
    print(f"systems {len(systems)}; with a plotted default {n_def}; aperture only "
          f"{sum(1 for s in systems if s['aperture_only'])}; for ruling {sum(1 for s in systems if s['for_ruling'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
