"""D-051/D-054: structural values for the coverage check, version 3 -> reading/structure_values.csv.

Version 3 differs from version 2 in one step. When the D-052 fit choice is "headline" (the
paper marked its adopted fit on the r_h row only), the fit's profile name is now taken from
that selected r_h row's variant. That name is then used in step 2 to pick the centre of the
same fit. Version 2 left the profile blank in that case, so papers printing a centre per fit
(Richstein 2024: Horologium I, Phoenix II) were wrongly treated as ties.

Version 2 docstring follows.

Usage (from the package directory): python reproduction/structure_for_coverage_v2.py

Version 1 (structure_for_coverage.py) took the centre from the D-052 selection, which
excludes values marked "quoted from" another paper. Under D-054 the centre is the one the
structural original used for its fit, measured or adopted. Version 2 therefore reads the
centre directly from reading/structure_values_all.csv, for the system's structural
original(s) (LVDB ref_structure), in this order:
  1. rows the paper measured, otherwise rows it adopted ("quoted from" in note/variant);
  2. among those, rows of the fit chosen by D-052 (profile name in variant), if any carry one;
  3. rows marked headline, if any;
  4. duplicate printings: table printing, then most significant digits (as D-051/D-052).
Several distinct centres left after these steps count as a tie: the system is then "not
available: centre tie" and its coverage is not checkable. The centre's source (measured or
adopted, with the note naming the cited paper) is written to centre_source.
Ellipticity, PA and r_h are taken as in version 1, from the D-052 selection.
"""

from __future__ import annotations

import csv
import glob
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from structure_for_coverage import coord, lead  # noqa: E402  (frozen version 1 helpers)

PKG = Path(__file__).resolve().parents[1]
PROFILES = {"exponential": r"\bexp(onential)?\b", "plummer": r"plummer", "sersic": r"s[eé]rsic", "king": r"\bking\b"}


def quoted(r: dict) -> bool:
    return "quoted from" in (r.get("note", "") + " " + r.get("variant", "")).lower()


def sig(x: str) -> int:
    return len("".join(ch for ch in x if ch.isdigit()).lstrip("0"))


def pick(rows: list[dict], profile: str) -> tuple[dict | None, str]:
    if not rows:
        return None, "none"
    own = [r for r in rows if not quoted(r)]
    pool, src = (own, "measured") if own else (rows, "adopted")
    if profile:
        rx = PROFILES.get(profile)
        pf = [r for r in pool if rx and re.search(rx, r.get("variant", ""), re.I)]
        pool = pf or pool
    hd = [r for r in pool if r.get("variant", "").strip().lower().startswith("headline")]
    pool = hd or pool
    tab = [r for r in pool if "table" in r.get("location", "").lower()]
    pool = tab or pool
    top = max(sig(r["value"]) for r in pool)
    pool = [r for r in pool if sig(r["value"]) == top]
    if len({r["value"].strip() for r in pool}) > 1:
        return None, "tie"
    return pool[0], src


def main() -> int:
    vals = list(csv.DictReader(open(PKG / "reading/structure_values_all.csv", encoding="utf-8")))
    lv = {}
    for f in sorted(glob.glob(str(PKG / "source/lvdb/dwarf_*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            lv[r["key"]] = r
    out = []
    for r in csv.DictReader(open(PKG / "reading/structure_selection.csv", encoding="utf-8")):
        k = r["key"]
        refs = [x.strip() for x in (lv[k].get("ref_structure") or "").split(";") if x.strip()]
        m = re.search(r"(exponential|plummer|sersic|king)", r.get("profile_choice", ""), re.I)
        profile = m.group(1).lower() if m else ""
        rows = [v for v in vals if v["key"] == k and v["role"] == "structure" and v["paper"] in refs and v["value"].strip()]
        if not profile:
            sel_rh = [v for v in rows if v["quantity"] == "r_h" and v["value"].strip() == r["r_h"].strip()
                      and f"{v['paper']} {v['location']}" == r["r_h_loc"]]
            hits = {p for v in sel_rh for p, rx in PROFILES.items() if re.search(rx, v.get("variant", ""), re.I)}
            profile = hits.pop() if len(hits) == 1 else ""
        ra_r, s1 = pick([v for v in rows if v["quantity"] == "ra0"], profile)
        de_r, s2 = pick([v for v in rows if v["quantity"] == "dec0"], profile)
        ra = coord(ra_r["value"], ra_r["unit"], True) if ra_r else None
        dec = coord(de_r["value"], de_r["unit"], False) if de_r else None
        e = lead(r["ellipticity"]) or 0.0
        pa = lead(r["pa"]) or 0.0
        rh, unit, a = lead(r["r_h"]), r["r_h_unit"], None
        if rh is not None and unit in ("arcmin", "arcsec"):
            rh_arcmin = rh / 60.0 if unit == "arcsec" else rh
            a = rh_arcmin / math.sqrt(1.0 - e) if r["rh_convention"].startswith("circularised") else rh_arcmin
        missing = []
        if ra is None or dec is None:
            missing.append("centre tie" if "tie" in (s1, s2) else "centre")
        if a is None:
            missing.append("angular r_h")
        src = ""
        if ra_r and de_r:
            src = s1 if s1 == s2 else f"ra {s1}, dec {s2}"
            if "adopted" in src:
                src += ": " + (ra_r.get("note", "")[:160])
        out.append({"key": k, "ra0_deg": f"{ra:.6f}" if ra is not None else "", "dec0_deg": f"{dec:.6f}" if dec is not None else "",
                    "ellipticity": f"{e:.4f}", "pa_deg": f"{pa:.2f}", "a_h_arcmin": f"{a:.5f}" if a is not None else "",
                    "rh_convention": r["rh_convention"], "centre_source": src,
                    "status": "ok" if not missing else "not available: " + ", ".join(missing)})
    for name, rows_ in (("structure_values.csv", [r for r in out if r["status"] == "ok"]),
                        ("structure_values_unavailable.csv", [r for r in out if r["status"] != "ok"])):
        with open(PKG / "reading" / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(rows_)
    print(f"{len(out)} systems; complete {sum(1 for r in out if r['status'] == 'ok')}; "
          f"centre adopted {sum(1 for r in out if 'adopted' in r['centre_source'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
