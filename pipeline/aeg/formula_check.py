"""Check every slider formula on every measurement (data standard §7 item 9).

Usage: python -m aeg.formula_check

For each package with tables and each assumption listed in a row's
`adjustable` column, evaluates the assumption's effects at its default and
at both ends of its range, in Python and in JavaScript (site/src/formula.mjs,
run with Node), and requires:
  1. Python and JavaScript agree to 1e-12 relative on every value;
  2. at the default, every affected column is unchanged (to 1e-12 relative);
  3. at the range ends, g_obs stays finite and positive, and g_bar finite;
     g_bar <= 0 is allowed only where a signed component is negative
     (reported, since the site cannot place it on a log axis);
  4. every formula parses and names only `p`, `p0`, row columns or
     `system.<column>` columns that exist;
  5. rows that do not list an assumption are never offered it.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

from aeg.formula import apply_assumption, names, parse

ROOT = Path(__file__).resolve().parents[2]
REL_TOL = 1e-12


def _clean(v):
    try:
        import numpy as np
        if np.ma.is_masked(v):
            return None
    except ImportError:
        pass
    if hasattr(v, "item"):
        v = v.item()
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


def close(a, b) -> bool:
    if a is None or b is None or (isinstance(a, float) and math.isnan(a)) or (isinstance(b, float) and math.isnan(b)):
        return (a is None or math.isnan(a)) and (b is None or math.isnan(b))
    return abs(a - b) <= REL_TOL * max(abs(a), abs(b), 1e-300)


def load_package(pkg: Path):
    from astropy.table import Table
    meas = Table.read(pkg / "tables/measurements.ecsv", format="ascii.ecsv")
    systems = Table.read(pkg / "tables/systems.ecsv", format="ascii.ecsv")
    rows = [{k: _clean(r[k]) for k in meas.colnames} for r in meas]
    sysrows = {str(r["system_id"]): {k: _clean(r[k]) for k in systems.colnames} for r in systems}
    return rows, sysrows, set(meas.colnames), set(systems.colnames)


def main() -> int:
    registry = json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))
    problems: list[str] = []
    nonpositive: list[str] = []
    jobs = []
    for pkg in sorted((ROOT / "data/packages").glob("*/*")):
        if not (pkg / "tables/measurements.ecsv").is_file():
            continue
        dataset = f"{pkg.parent.name}/{pkg.name}"
        rows, systems, mcols, scols = load_package(pkg)
        allowed = {"p", "p0"} | mcols | {f"system.{c}" for c in scols}
        defs = {a["id"]: a for a in registry["assumptions"]}
        for a in registry["assumptions"]:
            spec = a["datasets"].get(dataset)
            if not spec:
                continue
            for eff in spec.get("effects", []):
                bad = names(parse(eff["formula"])) - allowed
                if bad:
                    problems.append(f"{dataset} {a['id']} {eff['column']}: unknown names {sorted(bad)}")
                if eff["column"] not in mcols:
                    problems.append(f"{dataset} {a['id']}: effect on unknown column {eff['column']}")
        for row in rows:
            adjustable = [x for x in (row.get("adjustable") or "").split(";") if x]
            for aid in adjustable:
                a = defs.get(aid)
                spec = a and a["datasets"].get(dataset)
                if not a or not spec or not a["adjustable"] or a["status"] != "confirmed":
                    problems.append(f"{row['measurement_id']}: adjustable '{aid}' not a confirmed adjustable assumption for {dataset}")
                    continue
                system = systems[row["system_id"]] if row.get("system_id") else {}
                for p in (spec["min"], spec["default"], spec["max"]):
                    out = apply_assumption(row, system, spec["effects"], p, spec["default"])
                    jobs.append({"row": row, "system": system, "effects": spec["effects"], "p": p,
                                 "p0": spec["default"], "python": {e["column"]: out[e["column"]] for e in spec["effects"]},
                                 "tag": f"{row['measurement_id']} {aid} p={p}"})
                    for e in spec["effects"]:
                        v = out[e["column"]]
                        if p == spec["default"] and not close(v, row.get(e["column"])):
                            problems.append(f"{row['measurement_id']} {aid}: {e['column']} changes at the default ({row.get(e['column'])} -> {v})")
                    if "g_obs" in out and not (isinstance(out["g_obs"], float) and math.isfinite(out["g_obs"]) and out["g_obs"] > 0):
                        problems.append(f"{row['measurement_id']} {aid} p={p}: g_obs = {out['g_obs']}")
                    if "g_bar" in out:
                        gb = out["g_bar"]
                        if not (isinstance(gb, float) and math.isfinite(gb)):
                            problems.append(f"{row['measurement_id']} {aid} p={p}: g_bar = {gb}")
                        elif gb <= 0:
                            # Physical only if some component is negative (signed contributions, e.g. a
                            # central gas depression: arXiv:1606.09251 §III.3). Reported, not an error.
                            comps = [out.get(c) for c in ("g_bar_gas_cold", "g_bar_stars_disk", "g_bar_stars_bulge")]
                            if any(isinstance(c, float) and c < 0 for c in comps):
                                nonpositive.append(f"{row['measurement_id']} {aid} p={p}")
                            else:
                                problems.append(f"{row['measurement_id']} {aid} p={p}: g_bar = {gb} with no negative component")

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
        for col, pv in j["python"].items():
            pv = None if (isinstance(pv, float) and math.isnan(pv)) else pv
            if not close(pv, jr[col]):
                problems.append(f"{j['tag']}: {col} Python {pv} vs JavaScript {jr[col]}")

    print(f"formula check: {len(jobs)} evaluations")
    if nonpositive:
        print(f"note: g_bar <= 0 (net outward baryonic pull, from a negative component) in {len(nonpositive)} slider settings:")
        for n in nonpositive:
            print(f"  - {n}")
    if problems:
        print(f"FAILED ({len(problems)} problems):")
        for p in problems[:50]:
            print(f"  - {p}")
        return 1
    print("formula check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
