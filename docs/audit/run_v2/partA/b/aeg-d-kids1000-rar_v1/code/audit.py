#!/usr/bin/env python3
"""Reader B audit of aeg-d-kids1000-rar_v1.

Reads the inputs named by the written method from the source member files and
writes inputs.csv and values.csv.

Strict rule (BRIEF_COMMON.md): constants only from the method text. The method
(SOURCE.md, methods_page.txt) states g_obs = 4 G dSigma and h = 0.7, but gives no
numerical value of G and no conversion from h70 Msun/pc^2 to SI. It also gives
no rule for obtaining g_bar from the released files (stellar and cold-gas
masses are not released). Both g_obs and g_bar are therefore 'method incomplete'
in values.csv.

A supplementary computation using the constants printed in the source README
(not in the method) is written to supplementary_readme_constants.csv for the
coordinator's information only; it is NOT the audit result.

Usage: python3 -I audit.py <packet_dir> <out_dir>
"""
import csv
import os
import re
import sys

packet, out = sys.argv[1], sys.argv[2]
members = os.path.join(packet, "sources", "brouwer2021_rar_members")

rows = list(csv.DictReader(open(os.path.join(packet, "rows.csv"))))
COLS = ["Radius(m/s^2)", "ESD_t(h70*M_sun/pc^2)", "ESD_x(h70*M_sun/pc^2)",
        "error(h70*M_sun/pc^2)", "bias(1+K)", "variance(e_s)", "wk^2", "w^2k^2"]
NEEDED = {  # column -> (input name, unit)
    0: ("Radius", "m/s^2"),
    1: ("ESD_t", "h70*M_sun/pc^2"),
    3: ("error", "h70*M_sun/pc^2"),
    4: ("bias", "1+K (dimensionless)"),
}


def read_data_rows(path):
    """Return list of raw string-token lists for non-comment lines (data row 1 = first)."""
    out_rows = []
    with open(path) as f:
        header = f.readline()
        assert header.startswith("#"), path
        hdr = header.lstrip("#").split()
        assert hdr == COLS, (path, hdr)
        for line in f:
            if line.strip() and not line.startswith("#"):
                toks = line.split()
                assert len(toks) == 8, (path, line)
                out_rows.append(toks)
    return out_rows


inputs_out, values_out, supp_out = [], [], []
# README constants (source, not method) -- supplementary only
G_README = 4.52e-30   # pc^3/(Msun s^2) as printed (README writes unit as pc^2/(Msun*s^2))
PC_M_README = 3.086e16

for r in rows:
    mid = r["measurement_id"]
    m = re.fullmatch(r"brouwer2021_rar\.tar:(.+):data row (\d+)", r["source_ref"])
    assert m, r["source_ref"]
    fname, n = m.group(1), int(m.group(2))
    data = read_data_rows(os.path.join(members, fname))
    toks = data[n - 1]
    loc = f"brouwer2021_rar.tar:{fname}:data row {n} (file line {n + 1}), column "
    for ci, (name, unit) in NEEDED.items():
        inputs_out.append([mid, name, toks[ci], unit, loc + f"{ci + 1} '{COLS[ci]}'"])

    notes = ("g_obs: method states g_obs = 4 G dSigma (SIS deprojection) but gives no value of G "
             "and no conversion of h70*M_sun/pc^2 to kg m^-2 (no M_sun or pc in metres), and does not "
             "say whether ESD_t is divided by the released bias(1+K) before use; "
             "g_bar: method says point mass of stars + cold gas within the radius but those masses are "
             "not released and the method does not say g_bar is to be read from the released "
             "Radius(m/s^2) column")
    if "hotgas" in fname:
        notes += ("; this row is from the 'hotgas' file whose g_bar binning presumably includes hot gas, "
                  "which the method's g_bar definition (stars + cold gas) does not mention")
    values_out.append([mid, "", "", "method incomplete", notes])

    radius, esd, err, bias = (float(toks[i]) for i in (0, 1, 3, 4))
    g_obs_s = 4 * G_README * esd / bias * PC_M_README
    supp_out.append([mid, f"{g_obs_s:.6e}", f"{radius:.6e}",
                     "SUPPLEMENTARY ONLY: README Eq.7 constants (G=4.52e-30, pc/m=3.086e16), "
                     "ESD_t/bias, h70=1 i.e. h=0.7; g_bar = Radius column as printed"])

with open(os.path.join(out, "inputs.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["measurement_id", "input", "value", "unit", "locator"])
    w.writerows(inputs_out)
with open(os.path.join(out, "values.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["measurement_id", "g_obs", "g_bar", "status", "notes"])
    w.writerows(values_out)
with open(os.path.join(out, "supplementary_readme_constants.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["measurement_id", "g_obs_readme", "g_bar_radius_column", "notes"])
    w.writerows(supp_out)
print(len(values_out), "rows")
