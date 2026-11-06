"""Reader A: extract audited rows from data_E22.tar.gz (already verified by SHA-256).

Row numbering: 1-based (FITS binary-table convention; A2319 has NAXIS2=27 and
the packet asks for row 27, which exists only under 1-based counting).
Values: each column is FITS 'E' (big-endian float32). We write repr(float(v)),
i.e. the exact float32 value expanded losslessly to a Python float, plus the
shortest float32 repr (str(np.float32)) for reference.
No unit conversion: header TUNITs are already kpc and m/s^2.
Usage: python3 -I extract.py <reader_dir>
"""
import csv, hashlib, sys
from pathlib import Path
import numpy as np
from astropy.io import fits

base = Path(sys.argv[1])
ex = base / "ex"
rows = list(csv.DictReader(open("/home/claude/audit_xcop/packet/rows.csv")))
COLS = ["RADIUS", "GBAR", "GBAR_ERR", "GOBS", "GOBS_ERR_LO", "GOBS_ERR_HI"]
EXPECT_UNIT = {"RADIUS": "kpc"}  # all others m/s^2

ret_hdr = ["measurement_id", "archive", "file", "file_sha256", "row_1based", "nrows_in_file"]
for c in COLS:
    ret_hdr += [f"{c}_column", f"{c}_header_unit", f"{c}_stored_float32", f"{c}_value", f"{c}_unit_out", f"{c}_conversion"]
ret_hdr += ["status", "notes"]

cmp_hdr = "measurement_id,status,r_kpc,g_obs,g_obs_err_lo,g_obs_err_hi,g_bar,g_bar_err_lo,g_bar_err_hi".split(",")

out_ret, out_cmp = [], []
for r in rows:
    arch, fname, rowspec = r["source_ref"].split(":")
    n = int(rowspec.replace("row", "").strip())
    path = ex / fname
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    with fits.open(path) as h:
        hdu = h[1]
        hdr = hdu.header
        names = hdu.columns.names
        assert names == COLS, names
        units = {hdr[f"TTYPE{i}"].strip(): hdr[f"TUNIT{i}"].strip() for i in range(1, hdr["TFIELDS"] + 1)}
        nrows = hdr["NAXIS2"]
        rec = hdu.data[n - 1]
        rec = {c: np.float32(rec[c]) for c in COLS}
    status = "ok"
    d = {"measurement_id": r["measurement_id"], "archive": arch, "file": fname,
         "file_sha256": sha, "row_1based": n, "nrows_in_file": nrows}
    for c in COLS:
        u = units[c]
        want = EXPECT_UNIT.get(c, "m/s^2")
        if u != want:
            status = "method_incomplete"  # would need a conversion; none expected
        d.update({f"{c}_column": c, f"{c}_header_unit": u,
                  f"{c}_stored_float32": str(rec[c]), f"{c}_value": repr(float(rec[c])),
                  f"{c}_unit_out": "kpc" if c == "RADIUS" else "m s^-2",
                  f"{c}_conversion": "none (header unit already target unit)"})
    lo_ok = rec["GOBS_ERR_LO"] < rec["GOBS"]
    hi_ok = rec["GOBS_ERR_HI"] < rec["GOBS"]
    notes = [
        "Row counted from 1 (FITS convention; A2319 has 27 rows and row 27 is requested).",
        "RADIUS = r in g(r)=GM(<r)/r^2 (paper subsection 'The galaxy cluster radial acceleration relation', label sec:rar); GOBS = GM_HSE(<r)/r^2; GBAR = G(M_gas+M_*,BCG+M_*,sat)(<r)/r^2.",
        "GBAR_ERR: single symmetric uncertainty (a +/- size, not a bound): " + ("value << GBAR." if rec["GBAR_ERR"] < 0.5 * rec["GBAR"] else "CHECK"),
        f"GOBS_ERR_LO / GOBS_ERR_HI: uncertainties (+/- sizes, lower and upper), not bounds: both are smaller than GOBS (LO<GOBS={bool(lo_ok)}, HI<GOBS={bool(hi_ok)}), so neither can be a bound value on GOBS.",
        "Error definition (1-sigma / 68% interval / statistical only): not stated in file header or paper.",
        "Which GOBS reconstruction (nonparametric vs Einasto) the file holds: not stated in file header; paper Fig. caption says data points are NP.",
        "g_bar_err_lo and g_bar_err_hi in compare.csv both = GBAR_ERR (file stores one symmetric error).",
    ]
    d["status"] = status
    d["notes"] = " | ".join(notes)
    out_ret.append(d)
    out_cmp.append({"measurement_id": r["measurement_id"], "status": status,
                    "r_kpc": d["RADIUS_value"], "g_obs": d["GOBS_value"],
                    "g_obs_err_lo": d["GOBS_ERR_LO_value"], "g_obs_err_hi": d["GOBS_ERR_HI_value"],
                    "g_bar": d["GBAR_value"], "g_bar_err_lo": d["GBAR_ERR_value"],
                    "g_bar_err_hi": d["GBAR_ERR_value"]})

with open(base / "return.csv", "w", newline="") as f:
    w = csv.DictWriter(f, ret_hdr); w.writeheader(); w.writerows(out_ret)
with open(base / "compare.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cmp_hdr); w.writeheader(); w.writerows(out_cmp)
print("wrote", len(out_cmp), "rows")
