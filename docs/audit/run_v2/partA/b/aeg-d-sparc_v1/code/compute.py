#!/usr/bin/env python3
"""Reader B audit of aeg-d-sparc_v1.

Method (packet method/SOURCE.md and methods_page.txt):
  g_obs = Vobs^2 / R
  g_bar = (|Vgas|Vgas + Ud |Vdisk|Vdisk + Ub |Vbul|Vbul) / R
  Ud = 0.5, Ub = 0.7 (catalogue defaults stated in the method)
Outputs in m s^-2; R in kpc, V in km/s (units from the MRT byte description).

Unit conversion: the method states output units but NOT the kpc->m factor.
Used exact unit definitions (not physical constants):
  1 km  = 1000 m (SI prefix)
  1 au  = 149597870700 m (IAU 2012 B2, exact)
  1 pc  = 648000/pi au (IAU 2015 B2, exact); 1 kpc = 1000 pc
"""
import csv, math, hashlib, sys

PKT = "/home/claude/audit_v2/packets/aeg-d-sparc_v1"
OUT = "/home/claude/audit_v2/readers/b/aeg-d-sparc_v1"
SRC = f"{PKT}/sources/MassModels_Lelli2016c.mrt"
FNAME = "MassModels_Lelli2016c.mrt"

UPS_DISK = 0.5
UPS_BUL = 0.7
KM = 1000.0
AU = 149597870700.0
KPC = 1000.0 * 648000.0 / math.pi * AU

# Byte-by-byte description (1-based inclusive byte ranges)
COLS = {"ID": (1, 11), "D": (13, 18), "R": (20, 25), "Vobs": (27, 32),
        "e_Vobs": (34, 38), "Vgas": (40, 45), "Vdisk": (47, 52), "Vbul": (54, 59)}
UNITS = {"ID": "---", "D": "Mpc", "R": "kpc", "Vobs": "km/s", "e_Vobs": "km/s",
         "Vgas": "km/s", "Vdisk": "km/s", "Vbul": "km/s"}

raw = open(SRC, "rb").read()
sha = hashlib.sha256(raw).hexdigest()
assert sha == "9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c", sha
lines = raw.decode("ascii").split("\n")
if lines and lines[-1] == "":
    lines = lines[:-1]
# data begin after the 4th dashed separator line
seps = [i for i, l in enumerate(lines) if l.startswith("-----")]
first = seps[3] + 1  # 0-based index of first data line
data = lines[first:]
print("data rows:", len(data), "first data file line:", first + 1, file=sys.stderr)

def field(line, name):
    a, b = COLS[name]
    return line[a - 1:b].strip()

INC = ("method incomplete: the method states outputs in m s^-2 and radii in kpc but "
       "gives no kpc->m (or km/s->m/s) conversion constant; values computed with exact "
       "unit definitions 1 kpc = 1000*648000/pi au, 1 au = 149597870700 m, 1 km = 1000 m")

vals, inps = [], []
for r in csv.DictReader(open(f"{PKT}/rows.csv")):
    mid, name, ref = r["measurement_id"], r["system_name"], r["source_ref"]
    fn, rest = ref.split(":", 1)
    assert fn == FNAME and rest.startswith("data row "), ref
    n = int(rest[len("data row "):])
    line = data[n - 1]
    fileline = first + n  # 1-based file line
    f = {k: field(line, k) for k in COLS}
    notes = []
    if f["ID"] != name:
        notes.append(f"ID mismatch: source row has {f['ID']} vs rows.csv {name}")
    for k in ("ID", "R", "Vobs", "Vgas", "Vdisk", "Vbul"):
        a, b = COLS[k]
        inps.append([mid, k, f[k], UNITS[k], f"{FNAME}: data row {n} (file line {fileline}), bytes {a}-{b}"])
    R = float(f["R"]) * KPC
    V = {k: float(f[k]) * KM for k in ("Vobs", "Vgas", "Vdisk", "Vbul")}
    if R <= 0:
        vals.append([mid, "", "", "unreadable", "R <= 0"]); continue
    g_obs = V["Vobs"] ** 2 / R
    g_bar = (abs(V["Vgas"]) * V["Vgas"] + UPS_DISK * abs(V["Vdisk"]) * V["Vdisk"]
             + UPS_BUL * abs(V["Vbul"]) * V["Vbul"]) / R
    notes.insert(0, INC)
    notes.append("Ups_disk=0.5, Ups_bul=0.7 (method defaults)")
    if g_bar <= 0:
        notes.append("g_bar <= 0 (negative component term as printed)")
    vals.append([mid, f"{g_obs:.6e}", f"{g_bar:.6e}", "method incomplete", "; ".join(notes)])

with open(f"{OUT}/values.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["measurement_id", "g_obs", "g_bar", "status", "notes"]); w.writerows(vals)
with open(f"{OUT}/inputs.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["measurement_id", "input", "value", "unit", "locator"]); w.writerows(inps)
print(len(vals), "rows;", sum(1 for v in vals if "mismatch" in v[4]), "ID mismatches;",
      sum(1 for v in vals if "g_bar <= 0" in v[4]), "g_bar<=0", file=sys.stderr)
