"""REPRODUCTION.md test 1: every packaged input number equals both readings, or the adjudicated value
where the readers differed, with the adjudication cited.

Usage (from the repository root): python data/packages/aeg-d-strong-lensing/v1/reproduction/test1_second_reading.py
Written 2026-11-01 after the conversion, before its output was compared with the readings.

Packaged input numbers: every number of every adjudicated row that enters the package tables
(the observables: value and printed errors), plus the numbers that enter only the measurement
columns (H0 and Omega_m of each observed-side record, and the printed Salpeter conversions used
for the IMF top). The rows are taken from convert.py's own assembly, run in memory.

Readings: reader A and reader B (reading/readings/reader-{a,b}-{block1,block2,block3,supplement}.csv);
for SNL-1's R61 L_F814W and Upsilon_ref, which only the adjudicator had read (gas/adjudication_gas.md §1),
the second reading is reading/readings/second-reader-r61-snl1.csv (D-076 item 3).

A number is found in a reading if it appears among the values and errors that reader recorded for
the same record and system (system names compared after removing spaces, dashes, plus signs and the
SDSS prefix, since the readers spelled them differently), either as printed or in base units after
the reader's own unit scaling (1e10, 10^10). The quantity name is not used for matching: the readers
named some quantities differently (adjudication.md §2 "notation"; adjudication_gas.md §1).

Version 2 (2026-11-01, after the first run; its output is kept as checks/second_reading_v1.csv) fixes one
defect of this script: a record-level number (H0, Omega_m, a printed Salpeter conversion) was looked up only
under the readers' "(record)" rows, but reader A filed the printed Salpeter conversions under the systems they
apply to (reader-a-supplement.csv rows "S5 Salpeter conversions"). Version 2 looks a record-level number up
among all of that reader's rows for the record. The first run also found one converter defect, fixed in
convert.py before this run: R26's 2.2 arcsec spectroscopic aperture had been packaged as an alternative
einstein_radius observable (SECOND_READING.md). No other package value changed.

Outcome per number:
  both          found in both readings
  adjudicated   not found in both, and the adjudicated row says it was settled or verified at source;
                the adjudication file cited must name the system (or record, for record-level values)
  FAIL          otherwise
Writes checks/second_reading.csv (one row per number) and prints PASS or FAIL.
"""

from __future__ import annotations

import csv
import importlib.util
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
ROOT = PKG.parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
spec = importlib.util.spec_from_file_location("a6convert", PKG / "convert.py")
cv = importlib.util.module_from_spec(spec)
sys.modules["a6convert"] = cv
spec.loader.exec_module(cv)

READINGS = PKG / "reading/readings"
ADJ = {"inputs": PKG / "reading/adjudication.md", "supplement": PKG / "reading/gas/adjudication_gas.md"}


def norm_sys(s: str) -> str:
    s = (s or "").strip()
    if s.startswith("("):
        return "(RECORD)"
    return re.sub(r"[\s_\-−–+]", "", s).upper().replace("SDSSJ", "J")


def system_key(name: str) -> str:
    return norm_sys(cv.primary_name("", name).replace("SDSS ", ""))


def factor(unit: str) -> float:
    u = (unit or "").replace(" ", "")
    m = re.search(r"1e(\d+)|10\^(\d+)|10\+(\d+)", u)
    return 10.0 ** int(next(g for g in m.groups() if g)) if m else 1.0


def nums_of(cell: str) -> list[float]:
    out = []
    for m in re.finditer(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", str(cell or "").replace("−", "-")):
        try:
            out.append(float(m.group(0)))
        except ValueError:
            pass
    return out


def load_pools() -> dict:
    """reader -> (record, system key) -> set of numbers (as printed and in base units)."""
    pools = {"A": {}, "B": {}, "S": {}}
    for reader, letter in (("A", "a"), ("B", "b")):
        for block in ("block1", "block2", "block3", "supplement"):
            for r in csv.DictReader(open(READINGS / f"reader-{letter}-{block}.csv", encoding="utf-8")):
                key = (r["record"].strip(), norm_sys(r["system_id"]))
                f = factor(r.get("unit", ""))
                for c in ("value", "err_minus", "err_plus"):
                    for v in nums_of(r.get(c)):
                        pools[reader].setdefault(key, set()).update({v, v * f})
    for r in csv.DictReader(open(READINGS / "second-reader-r61-snl1.csv", encoding="utf-8")):
        key = ("R61", system_key("ESO 286-G022"))
        f = factor(r.get("unit", "").replace("10^10", "1e10"))
        for c in ("value", "err"):
            for v in nums_of(r.get(c)):
                pools["S"].setdefault(key, set()).update({v, v * f})
    return pools


def found(pool: dict, record: str, sysname: str, v: float, base: float) -> bool:
    if sysname == "(record)":  # version 2: any row of the reader for this record
        keys = [k for k in pool if k[0] == record]
    else:
        keys = [k for k in pool if k[0] == record and k[1] != "(RECORD)" and
                (system_key(sysname) in k[1] or k[1] in system_key(sysname))]
    vals = set().union(*[pool.get(k, set()) for k in keys]) if keys else set()
    return any(abs(x - v) <= 1e-12 * max(abs(v), 1e-300) or abs(x - base) <= 1e-12 * max(abs(base), 1e-300) for x in vals)


def packaged_rows() -> list[tuple[dict, str]]:
    """(adjudicated row, which file it came from) for every packaged input number's row."""
    inputs = cv.load_inputs(cv.INPUTS)
    sup = cv.load_inputs(cv.SUPPLEMENT)
    rows, _, _ = cv.merge_supplement(inputs, sup)
    res = cv.convert(rows, cv.load_gas_term(), synthetic=True)  # in memory; throw-away IDs; nothing written
    origin = {id(r): "inputs" for r in inputs}
    origin.update({id(r): "supplement" for r in sup})
    out, seen = [], set()

    def add(r):
        k = (r["scope"], r["system"], r["record"], r["quantity"], r["value"], r["err_minus"], r["err_plus"])
        if k in seen:
            return
        seen.add(k)
        src = "supplement" if any(cv._same_row(r, x) for x in sup) and not any(cv._same_row(r, x) for x in inputs) else "inputs"
        out.append((r, src))
    for r in res["used_rows"]:
        add(r)
    _, record_level = cv.group_systems(rows)
    obs_records = {m["source_ref"].split(";")[0].replace("observed ", "").strip() for m in res["measurements"]}
    for s in res["systems_obj"]:
        for r in s.rows:
            if r["quantity"] in ("H0", "Om") and r["record"] in obs_records and r["_role"] == "default":
                add(r)
    for rec in obs_records:
        for q in ("H0", "Om"):
            if q in record_level.get(rec, {}):
                add(record_level[rec][q])
    for m in res["measurements"]:
        t = m[f"{cv.X}mstar_top_source"] or ""
        mm = re.match(r"(R\d+) printed conversion \((\w+) = ", t)
        if mm:
            rec, q = mm.groups()
            add(record_level.get(rec, {}).get(q) or next(r for s in res["systems_obj"] for r in s.rows
                                                         if r["record"] == rec and r["quantity"] == q))
    return out


def main() -> int:
    pools = load_pools()
    adj_text = {k: p.read_text(encoding="utf-8") for k, p in ADJ.items()}
    rows_out, bad = [], 0
    for r, src in packaged_rows():
        f = cv.unit_factor(r.get("unit", "")) if r.get("form") != "log10" else 1.0
        settled = r.get("settled_by", "")
        cites = re.search(r"adjudicat|verified at source|read at source|checked against", settled, re.I)
        name = r["system"] if r["system"] != "(record)" else r["record"]
        short = cv.primary_name("", name).replace("SDSS ", "")
        named = short in adj_text[src] or short.replace("-", "−") in adj_text[src] or r["record"] in adj_text[src]
        is_r61_snl1 = r["record"] == "R61" and "SNL-1" in r["system"] and r["quantity"] in ("L_in_aperture", "ML_stellar_pop")
        for part in ("value", "err_minus", "err_plus"):
            raw = (r.get(part) or "").strip()
            if not raw or cv.num(raw) is None:
                continue
            v = cv.num(raw)
            base = v * f
            a = found(pools["A"], r["record"], r["system"], v, base)
            b = found(pools["B"], r["record"], r["system"], v, base)
            if is_r61_snl1:
                b = found(pools["S"], "R61", r["system"], v, base)
                a = bool(cites)  # the adjudicator's own reading at source (gas/adjudication_gas.md §1)
            if a and b:
                outcome, cite = "both", ""
            elif cites and named:
                outcome = "adjudicated"
                cite = f"{settled} ({ADJ[src].relative_to(PKG)})"
            else:
                outcome, cite = "FAIL", settled
                bad += 1
            rows_out.append({"scope": r["scope"], "system": r["system"], "record": r["record"], "quantity": r["quantity"],
                             "part": part, "value": raw, "unit": r.get("unit", ""), "reader_a": "yes" if a else "no",
                             "reader_b": ("second reader (R61)" if is_r61_snl1 else "yes") if b else "no",
                             "outcome": outcome, "adjudication_cited": cite})
    with open(PKG / "checks/second_reading.csv", "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows_out[0]))
        w.writeheader()
        w.writerows(rows_out)
    n = len(rows_out)
    nb = sum(r["outcome"] == "both" for r in rows_out)
    na = sum(r["outcome"] == "adjudicated" for r in rows_out)
    print(f"test 1: {n - bad} of {n} packaged numbers pass ({nb} in both readings, {na} adjudicated at source with "
          f"the adjudication cited): {'PASS' if not bad else 'FAIL'}")
    for r in [x for x in rows_out if x["outcome"] == "FAIL"][:20]:
        print("  FAIL", r)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
