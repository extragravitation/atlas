"""D-053: resolve compilation entries with several originals, version 2.

Version 2 also reads the originals that were not on arXiv:
- reading/scan_structure_values.csv and reading/scan_sigma_values.csv: ADS scans, read by
  two readers;
- reading/rc3_structure_values.csv: RC3, converted under D-056.
Their rows join the candidates' readings. Nothing else changes. Version 1's output is kept
as reading/mcc_resolution_v1.csv.

Spec: docs/methods/D053_COMPILATION_ORIGINALS.md.

Usage (from the package directory): python reproduction/resolve_compilation.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
MCC = "McConnachie2012AJ....144....4M"
MAP = {
    "magnitude (apparent V; source of M_V)": ("structure", ["m_v"]),
    "structure (r_h, ellipticity, PA)": ("structure", ["r_h", "ellipticity", "pa"]),
    "distance": ("structure", ["distance_modulus"]),
    "velocity dispersion (stellar sigma*)": ("sigma", ["sigma"]),
}


def num(x: str) -> float | None:
    m = re.match(r"\s*([-+]?\d+(?:\.\d+)?)", (x or "").replace("−", "-"))
    return float(m.group(1)) if m else None


def decimals(x: str) -> int:
    m = re.match(r"\s*[-+]?\d+(?:\.(\d+))?", (x or "").replace("−", "-"))
    return len(m.group(1)) if m and m.group(1) else 0


def quoted(r: dict) -> bool:
    return "quoted from" in (r.get("note", "") + " " + r.get("variant", "") + " " + r.get("quoted_from", "")).lower() or bool(r.get("quoted_from", "").strip())


def order(r: dict) -> int:
    if r.get("variant", "").strip().lower().startswith("headline"):
        return 0
    if "abstract" in r.get("location", "").lower():
        return 1
    return 2


def year(bib: str) -> int:
    m = re.match(r"(\d{4})", bib or "")
    return int(m.group(1)) if m else 0


def main() -> int:
    mp = list(csv.DictReader(open(PKG / "reading/mcconnachie2012_originals.csv", encoding="utf-8")))
    sv = [r for f in ("mcc_structure_values.csv", "scan_structure_values.csv", "rc3_structure_values.csv")
          for r in csv.DictReader(open(PKG / "reading" / f, encoding="utf-8"))]
    gv = [r for f in ("mcc_sigma_values.csv", "scan_sigma_values.csv")
          for r in csv.DictReader(open(PKG / "reading" / f, encoding="utf-8"))]
    mcc_s = [r for r in csv.DictReader(open(PKG / "reading/structure_values_all.csv", encoding="utf-8")) if r["paper"] == MCC]
    mcc_g = [r for r in csv.DictReader(open(PKG / "reading/sigma_values.csv", encoding="utf-8")) if r["paper"].startswith("McConnachie 2012")]
    groups: dict[tuple, list] = {}
    for r in mp:
        if r["quantity"] in MAP:
            groups.setdefault((r["key"], r["quantity"]), []).append(r)
    out = []
    for (key, cq), cands in sorted(groups.items()):
        kind, qs = MAP[cq]
        for q in qs:
            vals = gv if kind == "sigma" else sv
            vcol = "sigma" if kind == "sigma" else "value"
            printers = []
            for c in cands:
                rows = [r for r in vals if r["key"] == key and r.get("bibcode", r.get("paper", "")) in (c["original_bibcode"], c["original_citation"])
                        or (r["key"] == key and r.get("paper", "") == c["original_bibcode"])]
                rows = [r for r in rows if (kind == "sigma" or r.get("quantity") == q) and (r.get(vcol) or "").strip() and not quoted(r)]
                if rows:
                    printers.append((c, sorted(rows, key=order)))
            ref = [r for r in (mcc_g if kind == "sigma" else mcc_s) if r["key"] == key and (kind == "sigma" or r.get("quantity") == q)]
            mval = next((r[vcol] for r in ref if (r.get(vcol) or "").strip()), "")
            rec = {"key": key, "quantity": q, "candidates": " | ".join(c["original_bibcode"] for c in cands),
                   "printers": " | ".join(c["original_bibcode"] for c, _ in printers), "chosen": "", "how": "", "match_location": "", "flags": ""}
            if not printers:
                rec["how"], rec["flags"] = "no candidate prints it", "unresolved"
            elif len(printers) == 1:
                rec["chosen"], rec["how"] = printers[0][0]["original_bibcode"], "single printer"
            else:
                matches = []
                if mval and num(mval) is not None:
                    d, target = decimals(mval), round(num(mval), decimals(mval))
                    for c, rows in printers:
                        for r in rows:
                            v = num(r[vcol])
                            if v is not None and round(v, d) == target:
                                matches.append((c, r))
                                break
                if len(matches) == 1:
                    c, r = matches[0]
                    rec.update(chosen=c["original_bibcode"], how="value reproduced by the compilation", match_location=r.get("location", ""))
                elif len(matches) > 1:
                    c, r = max(matches, key=lambda m: year(m[0]["original_bibcode"]))
                    rec.update(chosen=c["original_bibcode"], how="several match; most recent", match_location=r.get("location", ""), flags="several_match")
                else:
                    c = max((p[0] for p in printers), key=lambda c: year(c["original_bibcode"]))
                    rec.update(chosen=c["original_bibcode"], how="no match; most recent printer", flags="no_match" if mval else "no_match (compilation value not read)")
            out.append(rec)
    with open(PKG / "reading/mcc_resolution.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(Counter(r["how"] for r in out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
