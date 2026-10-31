"""D-057: one [Fe/H] per system for the Upsilon_V interpolation -> reading/feh_values.csv.

Usage (from the package directory): python reproduction/select_feh.py
Inputs: reading/feh_sources.csv (the D-057 original per system), the two independent
readings (reading/feh_reading_{1,2}.csv) and their follow-ups for the originals behind the
Simon 2019 compilation entries (reading/feh_reading_{1,2}_followup.csv, D-053), and the
adjudication reading/feh_adjudication.md, whose rulings are coded in ADJUDICATED below.

Rule: the value the original presents as its headline system [Fe/H] (variant starting
"headline"; quantity feh_mean, feh_median, or "other" for a stacked spectrum), not quoted
from another paper. Both readers must record the same value and errors; otherwise the
system must have an entry in ADJUDICATED. A median or stacked-spectrum headline is used and
flagged. Duplicate printings with different errors: the table printing (D-051).
Systems with kind "none" get no value ("no metallicity original"), except under D-059 item 2:
the headline [Fe/H] printed by the system's dispersion original (reading/feh_d059_sheet.csv,
both readings in reading/feh_reading_{1,2}_d059.csv, which must agree), flagged
feh_from_dispersion_paper (and feh_stacked_spectrum where it comes from a co-added spectrum).
Where that paper prints none, the flag is no_metallicity_value and the system is not plotted.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
R = PKG / "reading"

# key -> (paper, value, err_minus, err_plus, quantity, flags, reason); see feh_adjudication.md
ADJUDICATED = {
    "crater_2": ("Ji2021ApJ...921...32J", "-2.16", "0.04", "0.04", "feh_mean", "",
                 "duplicate printing: table 0.04 over text 0.03 (D-051)"),
    "perseus_1": ("Martin2014ApJ...793L..14M", "-2.0", "0.2", "0.2", "feh_stacked", "feh_stacked_spectrum",
                  "both read -2.0 +-0.2 (12 stars); labelled mean by reader 1, other by reader 2: a stacked-spectrum value"),
    "ugc_04879": ("Kirby2013ApJ...779..102K", "-1.43", "0.02", "0.02", "feh_mean", "",
                  "printed as VV 124; Kirby et al. 2014 abstract: 'VV 124 (UGC 4879)'; both readers read -1.43 +-0.02"),
}
FOLLOWUP = {"carina_1", "fornax_1", "sagittarius_1", "sculptor_1", "sextans_1"}


NSTARS: dict = {}  # star counts are recorded, not compared (both readers' counts kept)


def heads(paths: list[Path]) -> dict:
    d: dict = {}
    for p in paths:
        if not p.exists():
            continue
        for r in csv.DictReader(open(p, encoding="utf-8")):
            if not r["variant"].strip().lower().startswith("headline"):
                continue
            if r["quantity"] not in ("feh_mean", "feh_median", "other") or "quoted from" in r.get("note", "").lower():
                continue
            d.setdefault((r["key"], r["paper"].strip()), set()).add(
                (r["quantity"], r["value"].strip(), r["err_minus"].strip(), r["err_plus"].strip()))
            NSTARS.setdefault((r["key"], r["paper"].strip()), set()).add(r["n_stars"].strip())
    return d


def main() -> int:
    a = heads([R / "feh_reading_1.csv", R / "feh_reading_1_followup.csv"])
    b = heads([R / "feh_reading_2.csv", R / "feh_reading_2_followup.csv"])
    d059 = {r["key"]: r["paper"] for r in csv.DictReader(open(R / "feh_d059_sheet.csv", encoding="utf-8"))}
    d059a, d059b = heads([R / "feh_reading_1_d059.csv"]), heads([R / "feh_reading_2_d059.csv"])
    follow = {r["key"]: r["paper"] for r in csv.DictReader(open(R / "feh_followup_sheet.csv", encoding="utf-8"))}
    out = []
    for s in csv.DictReader(open(R / "feh_sources.csv", encoding="utf-8")):
        k, kind = s["key"], s["kind"]
        paper = follow.get(k, s["paper"])
        row = {"key": k, "kind": kind, "paper": paper, "feh": "", "err_minus": "", "err_plus": "", "quantity": "",
               "n_stars": "", "flags": "", "basis": ""}
        if kind == "none" and k in d059:
            va, vb = d059a.get((k, d059[k]), set()), d059b.get((k, d059[k]), set())
            if va != vb or len(va) > 1:
                raise SystemExit(f"{k}: D-059 readings differ: {va} {vb}")
            if va:
                q, v, em, ep = next(iter(va))
                row.update(paper=d059[k], feh=v, err_minus=em, err_plus=ep, quantity=q,
                           flags="feh_from_dispersion_paper" + (" feh_stacked_spectrum" if d059[k].startswith("Collins2013") else ""),
                           basis="D-059 item 2: dispersion original; both readings agree")
            else:
                row.update(paper=d059[k], flags="no_metallicity_value", basis="D-059 item 2: dispersion original prints no [Fe/H]; not plotted")
        elif kind == "none":
            row["flags"], row["basis"] = "no_metallicity_original", "LVDB gives no metallicity reference"
        elif k in ADJUDICATED:
            p, v, em, ep, q, fl, why = ADJUDICATED[k]
            row.update(paper=p, feh=v, err_minus=em, err_plus=ep, quantity=q, flags=fl, basis="adjudicated: " + why)
        else:
            va, vb = a.get((k, paper), set()), b.get((k, paper), set())
            if len(va) != 1 or va != vb:
                raise SystemExit(f"{k}: readings differ or not single; needs adjudication: {va} {vb}")
            q, v, em, ep = next(iter(va))
            n = ";".join(sorted(x for x in NSTARS.get((k, paper), set()) if x))
            fl = "feh_median" if q == "feh_median" else ""
            if kind == "photometric":
                fl = (fl + " feh_photometric").strip()
            row.update(feh=v, err_minus=em, err_plus=ep, quantity=q, n_stars=n, flags=fl,
                       basis="both readings agree" + ("; original behind Simon 2019 (D-053)" if k in FOLLOWUP else ""))
        out.append(row)
    with open(R / "feh_values.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} systems; with value {sum(1 for r in out if r['feh'])}; "
          f"median {sum('feh_median' in r['flags'] for r in out)}; none {sum(r['kind'] == 'none' for r in out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
