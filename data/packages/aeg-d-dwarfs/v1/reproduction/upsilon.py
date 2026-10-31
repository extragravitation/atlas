"""Stellar mass-to-light ratio Upsilon_V for A5/A7 dwarfs: default and range (D-039, D-059, D-060).

Frozen before it was run on any dwarf. Usage (from the package directory):
    python reproduction/upsilon.py      -> reading/upsilon_v.csv

Model table: McLaughlin & van der Marel 2005 (VizieR J/ApJS/161/304/clusters), Milky Way
clusters only (Cluster starting "MW"), all at log age 10.11 (13 +- 2 Gyr). Columns [Fe/H]
(2 decimals), (M/L)1 = BC03 + Chabrier disk IMF, (M/L)2 = BC03 + Salpeter, with 1-sigma errors
(3 decimals); single-precision VOTable values are rounded to the printed precision.

Per system (reading/feh_values.csv gives [Fe/H]):
  default = (M/L)1 interpolated at [Fe/H] by the frozen aeg.ml_interp.MLTable;
  interval = [Fe/H] -+ s, where s is the intrinsic spread printed by the metallicity original
      (D-060 item 2): spread rows (quantity feh_spread) from that paper, not quoted from
      another, on which both readers agree in value; upper limits are taken at their value;
      several agreed printings -> the largest (the envelope covers every printed variant).
      With no agreed spread, s = the larger [Fe/H] error; with no error printed either, s = 0,
      flagged spread_zero.
  low  = min over the interval of ((M/L)1 - e1), x 0.90 x 0.81  (D-060 item 3)
  high = max over the interval of ((M/L)2 + e2), x 1.10           (D-060 item 4)
  Piecewise-linear tables reach their extremes at the interval ends or at tabulated nodes
  inside it, so both are evaluated there. Any point beyond the table takes the end value and
  the flag beyond_source_range (D-060 item 5).
Systems with no [Fe/H] get no Upsilon_V and the flag no_upsilon (not plotted, D-059).
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "pipeline"))
from aeg.ml_interp import BEYOND, MLTable  # noqa: E402

PKG = Path(__file__).resolve().parents[1]
R = PKG / "reading"
CODE_FACTOR = 0.90      # MvdM05 sec. 3.1: codes agree within ~10% in Upsilon_V
COLOUR_FACTOR = 1.3 / 1.6  # Woo et al. 2008: median Upsilon_V from colours / from SFH
HIGH_FACTOR = 1.10


def num(x: str) -> float | None:
    t = (x or "").strip().replace("−", "-").replace("–", "-").lstrip("~<≤ ")
    m = re.match(r"^-?\d+(\.\d+)?$", t)
    return float(t) if m else None


def model_tables(vot: Path) -> tuple[MLTable, MLTable, MLTable]:
    from astropy.io.votable import parse

    t = parse(str(vot)).get_first_table().to_table(use_names_over_ids=True)
    rows = [r for r in t if str(r["Cluster"]).startswith("MW")]
    if any(round(float(r["logAge"]), 2) != 10.11 for r in rows):
        raise SystemExit("model table: a Milky Way cluster not at log age 10.11")
    feh = [round(float(r["[Fe/H]"]), 2) for r in rows]
    m1 = [round(float(r["(M/L)1"]), 3) for r in rows]
    e1 = [round(float(r["e_(M/L)1"]), 3) for r in rows]
    m2 = [round(float(r["(M/L)2"]), 3) for r in rows]
    e2 = [round(float(r["e_(M/L)2"]), 3) for r in rows]
    default = MLTable(feh, m1)
    low = MLTable(feh, [a - b for a, b in zip(m1, e1)])
    high = MLTable(feh, [a + b for a, b in zip(m2, e2)])
    return default, low, high


def extreme(tab: MLTable, lo: float, hi: float, fn) -> tuple[float, bool]:
    pts = [lo, hi] + [f for f in tab.feh if lo < f < hi]
    vals = [tab(p) for p in pts]
    return fn(v.ml for v in vals), any(v.flag == BEYOND for v in vals)


def upsilon(feh: float, s: float, tabs: tuple[MLTable, MLTable, MLTable]) -> dict:
    d, lo_t, hi_t = tabs
    v = d(feh)
    lo, b1 = extreme(lo_t, feh - s, feh + s, min)
    hi, b2 = extreme(hi_t, feh - s, feh + s, max)
    return {"upsilon_v": v.ml, "upsilon_v_low": lo * CODE_FACTOR * COLOUR_FACTOR, "upsilon_v_high": hi * HIGH_FACTOR,
            "beyond": v.flag == BEYOND or b1 or b2}


def spreads(keys_papers: dict[str, str]) -> dict[str, float]:
    def collect(files: list[str]) -> dict[str, set]:
        d: dict[str, set] = {}
        for f in files:
            p = R / f
            if not p.exists():
                continue
            for r in csv.DictReader(open(p, encoding="utf-8")):
                if r["quantity"] != "feh_spread" or "quoted from" in r.get("note", "").lower():
                    continue
                if keys_papers.get(r["key"]) != r["paper"].strip():
                    continue
                x = num(r["value"])
                if x is not None:
                    d.setdefault(r["key"], set()).add(x)
        return d
    a = collect(["feh_reading_1.csv", "feh_reading_1_followup.csv", "feh_reading_1_d059.csv"])
    b = collect(["feh_reading_2.csv", "feh_reading_2_followup.csv", "feh_reading_2_d059.csv"])
    return {k: max(a[k] & b.get(k, set())) for k in a if a[k] & b.get(k, set())}


def main() -> int:
    tabs = model_tables(PKG / "source/mvdm05/J_ApJS_161_304_clusters.vot")
    fv = list(csv.DictReader(open(R / "feh_values.csv", encoding="utf-8")))
    sp = spreads({r["key"]: r["paper"] for r in fv if r["feh"]})
    out = []
    for r in fv:
        row = {"key": r["key"], "feh": r["feh"], "s": "", "s_basis": "", "upsilon_v": "", "upsilon_v_low": "",
               "upsilon_v_high": "", "flags": r["flags"]}
        feh = num(r["feh"])
        if feh is None:
            row["flags"] = (row["flags"] + " no_upsilon").strip()
            out.append(row)
            continue
        if r["key"] in sp:
            s, basis = sp[r["key"]], "intrinsic spread printed (largest agreed printing)"
        else:
            errs = [x for x in (num(r["err_minus"]), num(r["err_plus"])) if x is not None]
            s, basis = (max(errs), "[Fe/H] error (no spread printed)") if errs else (0.0, "none printed")
        u = upsilon(feh, s, tabs)
        fl = row["flags"]
        if s == 0.0:
            fl += " spread_zero"
        if u["beyond"]:
            fl += " " + BEYOND
        row.update(s=f"{s:g}", s_basis=basis, upsilon_v=f"{u['upsilon_v']:.4f}", upsilon_v_low=f"{u['upsilon_v_low']:.4f}",
                   upsilon_v_high=f"{u['upsilon_v_high']:.4f}", flags=fl.strip())
        out.append(row)
    with open(R / "upsilon_v.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} systems; with Upsilon_V {sum(1 for r in out if r['upsilon_v'])}; "
          f"{BEYOND} {sum(BEYOND in r['flags'] for r in out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
