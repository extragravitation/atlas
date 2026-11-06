"""Reader B: read the 10 audit rows from data_E22.tar.gz (already extracted to ../dl/x).

Run: python3 -I code/read_rows.py   (from /home/claude/audit_xcop/readers/b)
Row numbers in the locator are taken as 1-based (row N -> data[N-1]); see notes.md.
"""
import csv
import hashlib
import sys
from pathlib import Path

from astropy.io import fits

BASE = Path("/home/claude/audit_xcop/readers/b")
ARCHIVE = BASE / "dl" / "data_E22.tar.gz"
EXPECTED_SHA = "ff9ad2129c7bd50f95783c32369643eb87cc9e5ac7a6bfc3eda090e31838953d"
ROWS = Path("/home/claude/audit_xcop/packet/rows.csv")

sha = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
if sha != EXPECTED_SHA:
    sys.exit(f"SHA-256 mismatch: {sha}")

EXPECTED_UNITS = {"RADIUS": "kpc", "GBAR": "m/s^2", "GBAR_ERR": "m/s^2",
                  "GOBS": "m/s^2", "GOBS_ERR_LO": "m/s^2", "GOBS_ERR_HI": "m/s^2"}

ERR_NOTE = ("GOBS_ERR_LO and GOBS_ERR_HI hold uncertainties (+/- sizes), not bounds: "
            "inferred from the values, since GOBS_ERR_HI < GOBS in this row (impossible for an upper bound) "
            "and both error columns are of similar size; neither file nor paper states this, and the "
            "confidence level (e.g. 1 sigma / 68%) is not stated. "
            "GBAR_ERR is a single unsigned column, read as a symmetric uncertainty (+/- size), "
            "confidence level not stated; its value is copied into both g_bar_err_lo and g_bar_err_hi in compare.csv. "
            "Whether GOBS comes from the nonparametric (NP) or Einasto reconstruction: not stated. "
            "No conversion: header units are already kpc and m/s^2.")

ret_rows, cmp_rows = [], []
with ROWS.open() as fh:
    for rec in csv.DictReader(fh):
        mid = rec["measurement_id"]
        arch, member, rowpart = rec["source_ref"].split(":")
        n = int(rowpart.replace("row", "").strip())
        path = BASE / "dl" / "x" / member
        hdul = fits.open(path)
        tab = hdul[1]
        cols = tab.columns
        units = {c.name: c.unit for c in cols}
        assert units == EXPECTED_UNITS, units
        nrows = len(tab.data)
        if not (1 <= n <= nrows):
            cmp_rows.append([mid, "unreadable"] + [""] * 7)
            continue
        r = tab.data[n - 1]
        v = {c.name: repr(float(r[c.name])) for c in cols}
        assert float(r["GOBS_ERR_HI"]) < float(r["GOBS"])
        ret = {"measurement_id": mid, "file": f"{arch}:{member}", "row": n,
               "row_index_0based": n - 1, "file_nrows": nrows}
        for c in cols:
            ret[f"{c.name}_value"] = v[c.name]
            ret[f"{c.name}_unit"] = c.unit
        ret["r_kpc"] = v["RADIUS"]
        ret["conversion"] = "none (header units kpc, m/s^2)"
        ret["notes"] = ERR_NOTE
        ret_rows.append(ret)
        cmp_rows.append([mid, "ok", v["RADIUS"], v["GOBS"], v["GOBS_ERR_LO"], v["GOBS_ERR_HI"],
                         v["GBAR"], v["GBAR_ERR"], v["GBAR_ERR"]])

with (BASE / "return.csv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(ret_rows[0].keys()))
    w.writeheader()
    w.writerows(ret_rows)

with (BASE / "compare.csv").open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["measurement_id", "status", "r_kpc", "g_obs", "g_obs_err_lo", "g_obs_err_hi",
                "g_bar", "g_bar_err_lo", "g_bar_err_hi"])
    w.writerows(cmp_rows)

print("sha ok", sha)
print({s: sum(1 for x in cmp_rows if x[1] == s) for s in ("ok", "unreadable", "method_incomplete")})
