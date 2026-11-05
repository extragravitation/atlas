"""Reader A audit of aeg-d-sparc_v1.

Method (methods page + SOURCE.md):
  g_obs = Vobs^2 / R
  g_bar = (|Vgas|Vgas + Ups_disk |Vdisk|Vdisk + Ups_bul |Vbul|Vbul) / R
  Ups_disk = 0.50, Ups_bul = 0.70 (stated defaults)
Inputs: R [kpc], V* [km/s] from MassModels_Lelli2016c.mrt (byte columns per its header).

The method states that accelerations are reported in m s^-2 and radii in kpc, but does not
state the kpc -> m conversion constant. Per the brief, that is "method incomplete": values.csv
leaves g_obs/g_bar empty. For information only, this script also writes
  native_values.csv  : g in (km/s)^2/kpc  (needs no unstated constant)
  conditional_SI.csv : g in m s^-2 assuming the IAU 2015 B2 exact parsec
                       (1 pc = 648000/pi au, 1 au = 149597870700 m). Reader's assumption,
                       NOT part of the audit values.
"""
import csv, math, sys, os

PKT = "/home/claude/audit_v2/packets/aeg-d-sparc_v1"
OUT = "/home/claude/audit_v2/readers/a/aeg-d-sparc_v1"
SRC = "MassModels_Lelli2016c.mrt"
UPS_DISK, UPS_BUL = 0.50, 0.70  # stated in method

# byte ranges (1-based inclusive) from the file's own byte-by-byte description
COLS = {"ID": (1, 11), "D": (13, 18), "R": (20, 25), "Vobs": (27, 32), "e_Vobs": (34, 38),
        "Vgas": (40, 45), "Vdisk": (47, 52), "Vbul": (54, 59)}
UNITS = {"D": "Mpc", "R": "kpc", "Vobs": "km/s", "e_Vobs": "km/s", "Vgas": "km/s",
         "Vdisk": "km/s", "Vbul": "km/s"}
USED = ["R", "Vobs", "Vgas", "Vdisk", "Vbul"]

lines = open(os.path.join(PKT, "sources", SRC), encoding="ascii").read().split("\n")
# data begin after the last dashed separator line
last_sep = max(i for i, l in enumerate(lines) if l.startswith("-----"))
data = [l for l in lines[last_sep + 1:] if l.strip()]
data_start_line = last_sep + 2  # 1-based file line number of data row 1
assert len(data) == 3391, len(data)

def field(line, name):
    a, b = COLS[name]
    return line[a - 1:b].strip()

PC_M = 648000 / math.pi * 149597870700.0  # conditional only
KPC_M = 1e3 * PC_M

rows = list(csv.DictReader(open(os.path.join(PKT, "rows.csv"))))
vals, inps, nat, cond = [], [], [], []
for r in rows:
    mid = r["measurement_id"]
    ref = r["source_ref"]
    assert ref.startswith(SRC + ":data row "), ref
    n = int(ref.split("data row ")[1])
    line = data[n - 1]
    fileline = data_start_line + (n - 1)
    gid = field(line, "ID")
    notes = []
    if gid != r["system_name"]:
        vals.append([mid, "", "", "unreadable", f"ID at data row {n} is {gid!r}, not {r['system_name']!r}"])
        continue
    raw = {k: field(line, k) for k in USED}
    for k in USED:
        inps.append([mid, k, raw[k], UNITS[k],
                     f"{SRC} data row {n} (file line {fileline}), bytes {COLS[k][0]}-{COLS[k][1]}, ID={gid}"])
    R, Vobs, Vgas, Vdisk, Vbul = (float(raw[k]) for k in USED)
    gobs_n = Vobs ** 2 / R
    gbar_n = (abs(Vgas) * Vgas + UPS_DISK * abs(Vdisk) * Vdisk + UPS_BUL * abs(Vbul) * Vbul) / R
    note = ("method incomplete: method gives g_obs=Vobs^2/R and g_bar formula with R in kpc and V in km/s, "
            "and reports accelerations in m s^-2, but does not state the kpc-to-metre conversion constant; "
            "inputs read OK; Ups_disk=0.50 Ups_bul=0.70 (stated defaults)")
    if Vgas < 0 or Vdisk < 0 or Vbul < 0:
        note += "; negative component velocity present, signed-square used as in formula"
    vals.append([mid, "", "", "method incomplete", note])
    nat.append([mid, repr(gobs_n), repr(gbar_n)])
    cond.append([mid, f"{gobs_n * 1e6 / KPC_M:.6e}", f"{gbar_n * 1e6 / KPC_M:.6e}"])

def w(name, header, body):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        cw = csv.writer(f); cw.writerow(header); cw.writerows(body)

w("values.csv", ["measurement_id", "g_obs", "g_bar", "status", "notes"], vals)
w("inputs.csv", ["measurement_id", "input", "value", "unit", "locator"], inps)
w("native_values.csv", ["measurement_id", "g_obs_km2_s-2_kpc-1", "g_bar_km2_s-2_kpc-1"], nat)
w("conditional_SI.csv", ["measurement_id", "g_obs_m_s-2_IF_IAU2015_parsec", "g_bar_m_s-2_IF_IAU2015_parsec"], cond)
from collections import Counter
print(Counter(v[3] for v in vals), len(vals), len(inps))
print("negatives:", sum("negative" in v[4] for v in vals))
