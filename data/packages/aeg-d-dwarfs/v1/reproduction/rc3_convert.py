"""D-056: RC3 (VizieR VII/155) values for A5/A7 systems -> reading/rc3_structure_values.csv.

Usage (from the package directory): python reproduction/rc3_convert.py
Input:
- reading/rc3_values.csv: the RC3 row for each system, identified by two readers who agree
  on every field;
- source/members/vizier/VII_155.vot: the catalogue export. The corrected columns BoT and
  B-VoT are read from it by record number.

Output rows use the structure-reading format (key, paper, role, quantity, value, ..., note),
so the D-053 resolution can use them:
- m_v = BoT - (B-V)oT (role magnitude), marked extinction-corrected;
- r_h = 0.5 * 0.1 arcmin * 10**Ae (role structure, circularised);
- ellipticity = 1 - 10**(-R25);
- pa, as printed;
- ra0 and dec0, as printed.
Blank inputs give no row.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
PAPER = "1991rc3..book.....D"


def main() -> int:
    from astropy.io.votable import parse

    t = parse(str(PKG / "source/members/vizier/VII_155.vot")).get_first_table().to_table()
    by_recno = {int(r["recno"]): r for r in t}
    out = []

    def row(key, role, q, value, unit, note):
        out.append({"key": key, "paper": PAPER, "role": role, "copy_read": "VizieR VII/155 (Harvard mirror)", "quantity": q,
                    "value": value, "err_minus": "", "err_plus": "", "unit": unit, "variant": "headline; RC3", "quote": "",
                    "location": f"VizieR VII/155 recno {recno}", "note": note})

    for s in csv.DictReader(open(PKG / "reading/rc3_values.csv", encoding="utf-8")):
        key, recno = s["key"], int(s["recno"])
        r = by_recno[recno]

        def val(c):
            v = r[c]
            return None if getattr(v, "mask", False) or str(v) in ("--", "") else float(v)

        bot, bvot, ae, r25, pa = val("BoT"), val("B-VoT"), val("Ae"), val("R25"), val("PA")
        if bot is not None and bvot is not None:
            row(key, "magnitude", "m_v", f"{bot - bvot:.3f}", "mag",
                "V0 = BoT - (B-V)oT (D-056 item 1); RC3 correction includes Galactic and internal extinction (named assumption)")
        if ae is not None:
            row(key, "structure", "r_h", f"{0.5 * 0.1 * 10 ** ae:.4f}", "arcmin",
                "r_h = 0.5 x 0.1' x 10^Ae (D-056 item 2): circularised (azimuthally averaged)")
        if r25 is not None:
            row(key, "structure", "ellipticity", f"{1 - 10 ** (-r25):.4f}", "",
                "e = 1 - 10^(-R25) from the D25 isophote (D-056 item 3)")
        if pa is not None:
            row(key, "structure", "pa", f"{pa:g}", "deg", "RC3 position angle of the major axis (D25 isophote)")
        row(key, "structure", "ra0", s["RA2000"], "hms", "RC3 position (J2000)")
        row(key, "structure", "dec0", s["DE2000"], "dms", "RC3 position (J2000)")
    with open(PKG / "reading/rc3_structure_values.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} rows for {len({r['key'] for r in out})} systems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
