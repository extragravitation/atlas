"""REPRODUCTION.md item 7, "Check": the formula checks on every a6s_* registry entry for aeg-d-strong-lensing/v2.

Usage: python data/packages/aeg-d-strong-lensing/v2/reproduction/check_formulas.py

Runs the checks of pipeline/aeg/formula_check.py on every a6s_* v2 entry with effects, not only those a
row lists in `adjustable`:
  1. every formula parses and names only p, p0, existing row columns or system.<column>;
  2. Python (pipeline/aeg/formula.py) and JavaScript (site/src/formula.mjs, run with Node) agree to a
     relative 1e-12 on every value evaluated here, single entries and every step of the combined runs;
  3. at p = p0, on every row where every column the entry names is filled, every affected column is unchanged
     to a relative 1e-12;
  4. combined (all entries applied in registry order, each at its default unless moved):
     a. all at their defaults: every column unchanged;
     b. only a6s_source_cosmology moved to each stated H0 pair (p = H0_alt / H0_adopted), or only
        a6s_lens_distance moved to ±0.04: g_bar, g_bar_stars, g_bar_gas_cold and g_bar_gas_hot unchanged;
     c. only a6s_theta_e moved (p = 1 ± the row's x_strong_lensing_theta_e_err_frac_hi, or 1 ± 0.02 where empty):
        g_obs unchanged, and g_bar = g_bar_stars + g_bar_gas_cold + g_bar_gas_hot after all entries;
     d. H0 (each pair) or the lens distance (±0.04) moved together with a6s_stellar_imf (0, 1) or a6s_gas_in_RE
        (−1, 1): g_bar equals its value with the slider alone.
Rows where a named column is empty are not evaluated for that entry (for a6s_theta_e: rows without
x_strong_lensing_dlngbar_dlntheta). An effect on a column that is empty in the row (for example g_obs_err_* on
class A rows) is left out, since that column stays empty; the entry is then evaluated on the row only if every
column named by its remaining effects is filled. The counts are written to check_formulas.json beside this script.
Exit status 0 only if every check passes.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
ROOT = PKG.parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg.formula import apply_assumption, names, parse  # noqa: E402
from aeg.formula_check import close, load_package  # noqa: E402

DS = "aeg-d-strong-lensing/v2"
H0_PAIRS = {"cosmology_h0_snells": (70.0, 67.0), "cosmology_h0_j0403": (70.4, 67.8), "cosmology_h0_manga": (67.4, 69.6)}
DIST = (-0.04, 0.04)
BAR = ("g_bar", "g_bar_stars", "g_bar_gas_cold", "g_bar_gas_hot")


def main() -> int:
    registry = json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))
    entries = [(a["id"], a["datasets"][DS]) for a in registry["assumptions"]
               if a["id"].startswith("a6s_") and DS in a["datasets"] and a["datasets"][DS].get("effects")]
    rows, systems, mcols, scols = load_package(PKG)
    allowed = {"p", "p0"} | mcols | {f"system.{c}" for c in scols}
    problems: list[str] = []
    jobs: list[dict] = []
    skipped = {aid: 0 for aid, _ in entries}
    evaluated = {aid: 0 for aid, _ in entries}

    # terms' own pairs must equal the stated sizes in the terms table (adopted = the source's value)
    terms = {t["term_id"]: t for t in __import__("astropy.table", fromlist=["Table"]).Table.read(
        PKG / "tables/uncertainty_terms.ecsv", format="ascii.ecsv")}
    for tid, (adopted, alt) in H0_PAIRS.items():
        lo, hi = float(terms[tid]["size_lo"]), float(terms[tid]["size_hi"])
        if sorted((adopted, alt)) != [lo, hi]:
            problems.append(f"{tid}: pair {adopted}/{alt} differs from the terms table ({lo}, {hi})")

    named = {}
    for aid, e in entries:
        for eff in e["effects"]:
            n = names(parse(eff["formula"]))
            bad = n - allowed
            if bad:
                problems.append(f"{aid} {eff['column']}: unknown names {sorted(bad)}")
            if eff["column"] not in mcols:
                problems.append(f"{aid}: effect on unknown column {eff['column']}")
            named[(aid, eff["column"])] = {x for x in n if x not in ("p", "p0")}

    def empty(row, system, n) -> bool:
        v = system.get(n[7:]) if n.startswith("system.") else row.get(n)
        return v is None or (isinstance(v, float) and math.isnan(v))

    def plan(row, system, aid, e):
        """The effects evaluated on this row: an effect on an empty column is left out (the column stays empty);
        if any remaining effect names an empty column, the entry is not evaluated on this row (None)."""
        effs = [x for x in e["effects"] if not empty(row, system, x["column"])]
        if not effs or any(empty(row, system, n) for x in effs for n in named[(aid, x["column"])]):
            return None
        return effs

    def step(row, system, aid, e, effs, p, tag):
        out = apply_assumption(row, system, effs, p, e["default"])
        jobs.append({"row": row, "system": system, "effects": effs, "p": p, "p0": e["default"],
                     "python": {x["column"]: out[x["column"]] for x in effs}, "tag": tag})
        return out

    def run_all(row, system, moved: dict, tag: str) -> dict:
        cur = dict(row)
        for aid, e in entries:
            effs = plan(cur, system, aid, e)
            if effs is None:
                continue
            cur = step(cur, system, aid, e, effs, moved.get(aid, e["default"]), f"{tag} {aid}")
        return cur

    def filled(row, system, aid) -> bool:
        return plan(row, system, aid, dict(entries)[aid]) is not None

    for row in rows:
        mid = row["measurement_id"]
        system = systems.get(row["system_id"], {})
        # 3. each entry alone at p0
        for aid, e in entries:
            effs = plan(row, system, aid, e)
            if effs is None:
                skipped[aid] += 1
                continue
            evaluated[aid] += 1
            out = step(row, system, aid, e, effs, e["default"], f"{mid} {aid} p0")
            for x in effs:
                if not close(out[x["column"]], row[x["column"]]):
                    problems.append(f"{mid} {aid}: {x['column']} changes at p0 ({row[x['column']]} -> {out[x['column']]})")
        # 4a. all at defaults
        base = run_all(row, system, {}, f"{mid} defaults")
        for c in set().union(*[{x["column"] for x in e["effects"]} for _, e in entries]):
            if not close(base.get(c), row.get(c)):
                problems.append(f"{mid} all defaults: {c} changes ({row.get(c)} -> {base.get(c)})")
        # 4b. H0 or distance alone
        moves = [("a6s_source_cosmology", alt / adopted, tid) for tid, (adopted, alt) in H0_PAIRS.items()]
        moves += [("a6s_lens_distance", p, f"distance {p:+}") for p in DIST]
        for aid, p, label in moves:
            out = run_all(row, system, {aid: p}, f"{mid} {label}")
            for c in BAR:
                if not close(out.get(c), row.get(c)):
                    problems.append(f"{mid} {label}: {c} changes ({row.get(c)} -> {out.get(c)})")
        # 4c. theta_e alone
        if filled(row, system, "a6s_theta_e"):
            f = row.get("x_strong_lensing_theta_e_err_frac_hi") or 0.02
            for p in (1 - f, 1 + f):
                out = run_all(row, system, {"a6s_theta_e": p}, f"{mid} theta {p}")
                if not close(out["g_obs"], row["g_obs"]):
                    problems.append(f"{mid} theta p={p}: g_obs changes")
                total = sum(out.get(c) or 0.0 for c in BAR[1:])
                if not close(out["g_bar"], total):
                    problems.append(f"{mid} theta p={p}: g_bar {out['g_bar']} != components {total}")
        # 4d. H0 or distance with a slider
        for slider, ends in (("a6s_stellar_imf", (0, 1)), ("a6s_gas_in_RE", (-1, 1))):
            if not filled(row, system, slider):
                continue
            for s in ends:
                alone = run_all(row, system, {slider: s}, f"{mid} {slider}={s}")
                for aid, p, label in moves:
                    both = run_all(row, system, {slider: s, aid: p}, f"{mid} {slider}={s} {label}")
                    if not close(both["g_bar"], alone["g_bar"]):
                        problems.append(f"{mid} {slider}={s} with {label}: g_bar {both['g_bar']} != {alone['g_bar']}")

    # 2. Python and JavaScript agree on every value evaluated above
    with tempfile.TemporaryDirectory() as tmp:
        jin, jout = Path(tmp) / "in.json", Path(tmp) / "out.json"
        jin.write_text(json.dumps([{k: j[k] for k in ("row", "system", "effects", "p", "p0")} for j in jobs]), encoding="utf-8")
        script = (
            "import {applyAssumption} from %s;"
            "import {readFileSync, writeFileSync} from 'node:fs';"
            "const jobs = JSON.parse(readFileSync(%s, 'utf8'));"
            "const out = jobs.map(j => { const r = applyAssumption(j.row, j.system, j.effects, j.p, j.p0);"
            " return Object.fromEntries(j.effects.map(e => [e.column, Number.isNaN(r[e.column]) ? null : r[e.column]])); });"
            "writeFileSync(%s, JSON.stringify(out));"
        ) % (json.dumps((ROOT / "site/src/formula.mjs").as_uri()), json.dumps(str(jin)), json.dumps(str(jout)))
        subprocess.run(["node", "--input-type=module", "-e", script], check=True)
        js = json.loads(jout.read_text(encoding="utf-8"))
    for j, jr in zip(jobs, js):
        for c, pv in j["python"].items():
            pv = None if (isinstance(pv, float) and math.isnan(pv)) else pv
            if not close(pv, jr[c]):
                problems.append(f"{j['tag']}: {c} Python {pv} vs JavaScript {jr[c]}")

    result = {"entries": [aid for aid, _ in entries], "rows": len(rows), "evaluations_python_and_js": len(jobs),
              "rows_evaluated_at_p0": evaluated, "rows_not_evaluated_named_column_empty": skipped,
              "problems": len(problems), "result": "pass" if not problems else "fail"}
    (HERE / "check_formulas.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=1))
    for p in problems[:50]:
        print("  -", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
