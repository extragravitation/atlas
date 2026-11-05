"""Audit reader A, stratum aeg-d-kids1000-rar_v1.

Reads the rows to audit, extracts the printed inputs from the source member
files, and writes inputs.csv and values.csv.

The written method (methods_page.txt, SOURCE.md) gives g_obs = 4 G DeltaSigma
but states no numerical value for G and no pc->m or M_sun->kg conversion, and
does not say which released column holds g_bar. Under the brief, both
accelerations are therefore 'method incomplete' and left empty in values.csv.

A clearly separated SUPPLEMENTARY calculation (not following the written
method; constants taken from the source README, not from the method) is
printed to stdout for the record only. It is not written to values.csv.

Usage: python3 -I audit.py <packet_dir> <out_dir>
"""
import csv
import sys
from pathlib import Path

packet = Path(sys.argv[1])
out = Path(sys.argv[2])
members = packet / "sources" / "brouwer2021_rar_members"

COLS = ["Radius(m/s^2)", "ESD_t(h70*M_sun/pc^2)", "ESD_x(h70*M_sun/pc^2)",
        "error(h70*M_sun/pc^2)", "bias(1+K)", "variance(e_s)", "wk^2", "w^2k^2"]
USE = {  # column label -> unit as printed in header
    "Radius(m/s^2)": "m/s^2",
    "ESD_t(h70*M_sun/pc^2)": "h70*M_sun/pc^2",
    "error(h70*M_sun/pc^2)": "h70*M_sun/pc^2",
    "bias(1+K)": "dimensionless (1+K)",
}


def read_member(name):
    lines = (members / name).read_text().splitlines()
    header = lines[0]
    assert header.startswith("#"), header
    assert header[1:].split() == COLS, header
    data = [ln.split() for ln in lines[1:] if ln.strip() and not ln.startswith("#")]
    for d in data:
        assert len(d) == len(COLS), d
    return data


rows = list(csv.DictReader(open(packet / "rows.csv")))
inputs_out, values_out, supp = [], [], []
for r in rows:
    mid = r["measurement_id"]
    tar, fname, loc = r["source_ref"].split(":")
    assert tar == "brouwer2021_rar.tar"
    n = int(loc.replace("data row", "").strip())
    data = read_member(fname)
    row = data[n - 1]  # data row 1 = first non-comment line
    rec = dict(zip(COLS, row))
    locator = f"brouwer2021_rar.tar:{fname}:data row {n} (sources/brouwer2021_rar_members/{fname}, line {n + 1}), column {{c}}"
    for c, unit in USE.items():
        inputs_out.append([mid, c, rec[c], unit, locator.format(c=c)])

    note = ("method incomplete: g_obs = 4 G DeltaSigma is given but the method states no value of G "
            "and no pc->m / M_sun->kg conversion, and does not say whether DeltaSigma is to be divided by "
            "the released bias(1+K) (bias correction is mentioned only for the uncertainty); "
            "g_bar: the method defines g_bar as stars + cold gas as a point mass but releases no masses or "
            "radii, and does not say that the released Radius(m/s^2) column is g_bar")
    if "hotgas" in fname:
        note += ("; also, this file is the 'hotgas' variant, while the method defines g_bar as stars + cold gas "
                 "only and does not describe a hot-gas term")
    values_out.append([mid, "", "", "method incomplete", note])

    # SUPPLEMENTARY, NOT the written method: README constants
    G = 4.52e-30      # README: G[pc^3/(Msun*s^2)]
    PC_M = 3.086e16   # README: [pc/m]
    esd = float(rec["ESD_t(h70*M_sun/pc^2)"]) / float(rec["bias(1+K)"])
    supp.append((mid, fname, n, 4 * G * esd * PC_M, float(rec["Radius(m/s^2)"])))

with open(out / "inputs.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["measurement_id", "input", "value", "unit", "locator"])
    w.writerows(inputs_out)
with open(out / "values.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["measurement_id", "g_obs", "g_bar", "status", "notes"])
    w.writerows(values_out)

print("SUPPLEMENTARY (README constants; not the written method)")
print("measurement_id,file,data_row,g_obs_readme,radius_column_m_s2")
for s in supp:
    print(f"{s[0]},{s[1]},{s[2]},{s[3]:.4e},{s[4]:.4e}")
