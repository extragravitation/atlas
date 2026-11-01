"""A6 gas adjudication: measurement table and per-phase gas-to-stellar distributions.

Written by the adjudicator (Claude) on 2026-11-01 for `adjudication_gas.md`. Exploratory; no test is
scored here. It touches only the gas-literature galaxies. It computes no lens g_obs, g_bar or ratio
and does not read the lens inputs.

Inputs: the two readings in this folder (values were reconciled first; every value used below
either agrees between readers A and B or was read at source by the adjudicator, see the md).

Choices fixed before any ratio was computed (stated in the md, section 6):
- Lens range (from adjudicated_inputs.csv, ranges only): M*(<R_E) 1.0e10-2.0e11 Msun and total
  M* 3.0e10-1.2e12 Msun. A gas galaxy is "in the lens range" if its stellar mass on the basis
  printed lies in [1.0e10, 1.2e12] for a same-radius mass, or in [3.0e10, 1.2e12] for a total.
- Stellar mass for a gas galaxy: as printed by the gas source; else the source's printed K-band
  luminosity x the source's own printed M*/L_K; else x M*/L_K = 0.82 (printed by C13 Sect. 5.1 and
  N18 Sect. 3.3 for ATLAS3D, citing Bell et al. 2003), flagged `ML_K_assumed`.
- Radius classes: physical (kpc as printed), beam (diameter as printed; radius = half), model.
- Limits are carried as limits. Medians are bracketed: limits set to their value (upper bracket)
  and to zero (lower bracket). No survival-analysis model is used.
- Optional explicit scaling (never a default): for beam rows whose source prints R_e, the stellar
  mass inside the beam radius is total x f(<R_beam) for a de Vaucouleurs profile (n = 4) with the
  frozen `aeg.lensing.sersic_projected_fraction`.

Usage: python -I adjudicate_gas.py <repo_root>
"""
import csv
import os
import re
import statistics
import sys

ROOT = sys.argv[1]
HERE = os.path.join(ROOT, "data/packages/aeg-d-strong-lensing/v1/reading/gas")
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from aeg.lensing import sersic_projected_fraction  # noqa: E402  (frozen, SHA-256 in REPRODUCTION.md)

SAME_LO, TOT_LO, HI = 1.0e10, 3.0e10, 1.2e12
ML_K_ASSUMED = 0.82


def rows(f):
    with open(os.path.join(HERE, f), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


A_N, B_N = rows("reader-a-N.csv"), rows("reader-b-N.csv")


def num(s):
    s = (s or "").replace("−", "-").replace("×", "x").replace(" ", "")
    m = re.match(r"^[<≤]?(-?[\d.]+)(?:x10\^(-?\d+))?", s)
    v = float(m.group(1))
    return v * 10 ** int(m.group(2)) if m.group(2) else v


def mult(u):
    m = re.search(r"10\^(-?\d+)", u or "")
    return 10 ** int(m.group(1)) if m else 1.0


def gas_value(x):
    v = num(x["value"])
    if "log" in (x["unit"] + x["form"]).lower():
        return 10 ** v
    return v * mult(x["unit"])


def is_limit(x):
    return bool(re.search(r"upper|<|≤", (x["limit"] or "") + x["value"][:1]))


def pick(rs, cand, q="gas_mass_in_radius"):
    return [x for x in rs if x["candidate"] == cand and x["quantity"] == q]


out = []  # measurement table


def add(**k):
    out.append(k)


# ---------------- HOT ----------------
# N2 David et al. 2006: Mgas within R_m; L_K in the same aperture (Table 1 note); M*/L_K = 0.8 (N2 Sect. 5).
LK_N2 = {  # Table 1, L_K (Lsun,K) "within the same aperture as that used to extract the X-ray spectrum"; read at source
    "ESO 0428-G014": 3.62e10, "NGC 821": 8.79e10, "NGC 1023": 8.44e10, "NGC 1386": 3.47e10, "NGC 1389": 3.91e10,
    "NGC 2434": 7.38e10, "NGC 2787": 1.46e10, "NGC 3115": 8.95e10, "NGC 3245": 5.92e10, "NGC 3377": 2.75e10,
    "NGC 3379": 7.31e10, "NGC 3608": 5.24e10, "NGC 4251": 6.67e10, "NGC 4435": 2.38e10, "NGC 4459": 7.58e10,
    "NGC 4552": 1.05e11, "NGC 4697": 9.12e10, "NGC 5866": 9.04e10}
for x in pick(B_N, "N2"):
    r = float(x["radius_value"])
    ms = 0.8 * LK_N2[x["galaxy"]]
    add(phase="hot", cand="N2", galaxy=x["galaxy"], radius=f"R_m = {r} kpc", r_kpc=r, rclass="physical",
        gas=gas_value(x), lim=is_limit(x), mstar=ms, mbasis="same aperture: L_K(<R_m) x 0.8 (N2's own M*/L_K)",
        flags="" if r <= 10 else "radius > 10 kpc (outside brief); sensitivity only", use=r <= 10)

# N7 Su et al. 2015: MXgas within 2 r_e (spherical volume of the extraction region); L_K within 2 r_e.
RE_N7 = {"NGC 4472": 7.882, "NGC 4649": 5.453, "NGC 4406": 7.512, "NGC 5846": 6.783, "NGC 5813": 8.614,
         "NGC 4261": 5.539, "NGC 4382": 5.656, "NGC 4374": 4.653, "NGC 3665": 4.876, "NGC 4494": 3.943,
         "NGC 4365": 5.831}  # Table 2 r_e (kpc), read at source
for x in pick(A_N, "N7"):
    lk = float(re.search(r"LK = ([\d.]+) ×10\^10", x["note"]).group(1)) * 1e10
    re_ = RE_N7[x["galaxy"]]
    add(phase="hot", cand="N7", galaxy=x["galaxy"], radius=f"2 r_e = {2*re_:.2f} kpc", r_kpc=2 * re_, rclass="physical",
        gas=gas_value(x), lim=is_limit(x), mstar=ML_K_ASSUMED * lk,
        mbasis="same aperture: L_K(<2 r_e) x 0.82", flags="ML_K_assumed; 2 r_e > typical R_E", use=True)

# ---------------- MOLECULAR ----------------
# N14 O'Sullivan et al. 2015 (a) and 2018 (b): beam FWHM (kpc, diameter); total log M* (SED) printed.
def mstar_note(x):
    m = re.search(r"log M\* = ([\d.]+)", x["note"])
    return 10 ** float(m.group(1))


seen = {}
n14 = pick(B_N, "N14")
a14 = {(x["citation"][:22], x["galaxy"].replace(" ", "")): x for x in pick(A_N, "N14")}
for x in sorted(n14, key=lambda r: "2018" not in r["citation"]):  # 2018 first: later paper wins duplicates
    g = x["galaxy"].replace(" ", "")
    xa = a14.get((x["citation"][:22], g))
    assert xa is not None and abs(mstar_note(xa) / mstar_note(x) - 1) < 1e-9, g  # readers agree on M*
    if g in seen:
        continue
    seen[g] = 1
    d = float(x["radius_value"])
    add(phase="molecular", cand="N14", galaxy=x["galaxy"], radius=f"beam FWHM {d} kpc (radius {d/2:.2f})",
        r_kpc=d / 2, rclass="beam", gas=gas_value(x), lim=is_limit(x), mstar=mstar_note(x),
        mbasis="total (SED fit, as printed)",
        flags="gas in beam / total M* (lower bound on in-beam ratio); group-dominant sample", use=True)

# N13 Davis et al. 2019 (MASSIVE XI): beam diameter (kpc); log L_Ks and R_e printed (Table 1).
for x in pick(B_N, "N13"):
    lk = 10 ** float(re.search(r"log L_Ks = ([\d.]+)", x["note"]).group(1))
    re_ = float(re.search(r"R_e = ([\d.]+) kpc", x["note"]).group(1))
    d = float(x["radius_value"])
    f = sersic_projected_fraction(d / 2, re_, 4.0)
    add(phase="molecular", cand="N13", galaxy=x["galaxy"], radius=f"beam FWHM {d} kpc (radius {d/2:.2f})",
        r_kpc=d / 2, rclass="beam", gas=gas_value(x), lim=is_limit(x), mstar=ML_K_ASSUMED * lk,
        mbasis="total: L_Ks x 0.82", flags=f"ML_K_assumed; optional scaling f(<R_beam; R_e={re_}) = {f:.3f}",
        use=True, f_beam=f)

# ---------------- report ----------------
def fmt(v):
    return f"{v:.3g}"


def dist(sel, key="ratio"):
    det = [r[key] for r in sel if not r["lim"]]
    lim = [r[key] for r in sel if r["lim"]]
    allv = det + lim
    upper = statistics.median(allv) if allv else None
    lower = statistics.median(det + [0.0] * len(lim)) if allv else None
    return dict(n=len(sel), n_det=len(det), n_lim=len(lim),
                det_min=min(det) if det else None, det_max=max(det) if det else None,
                lim_min=min(lim) if lim else None, lim_max=max(lim) if lim else None,
                med_upper=upper, med_lower=lower)


for r in out:
    r["ratio"] = r["gas"] / r["mstar"]
    same = r["mbasis"].startswith("same")
    r["in_range"] = (SAME_LO if same else TOT_LO) <= r["mstar"] <= HI
    if "f_beam" in r:
        r["ratio_scaled"] = r["gas"] / (r["mstar"] * r["f_beam"])

print("| Phase | Cand. | Galaxy | Radius as printed | r (kpc) | Class | M_gas (Msun) | Limit | M* (Msun) | M* basis | Ratio | In lens range | Used | Flags |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in out:
    print(f"| {r['phase']} | {r['cand']} | {r['galaxy']} | {r['radius']} | {r['r_kpc']:.2f} | {r['rclass']} | {fmt(r['gas'])} | "
          f"{'<' if r['lim'] else ''} | {fmt(r['mstar'])} | {r['mbasis']} | {'<' if r['lim'] else ''}{fmt(r['ratio'])} | "
          f"{'yes' if r['in_range'] else 'no'} | {'yes' if r['use'] else 'no'} | {r['flags']} |")
print()
groups = [
    ("hot, N2 (same aperture, M*/L_K 0.8)", lambda r: r["cand"] == "N2"),
    ("hot, N7 (same aperture 2 r_e, M*/L_K 0.82 assumed)", lambda r: r["cand"] == "N7"),
    ("hot, N2 + N7", lambda r: r["phase"] == "hot"),
    ("molecular, N14 (beam / total M*)", lambda r: r["cand"] == "N14"),
    ("molecular, N13 (beam / total M*, M*/L_K 0.82 assumed)", lambda r: r["cand"] == "N13"),
    ("molecular, N14 + N13", lambda r: r["phase"] == "molecular"),
    # sensitivity rows (not defaults)
    ("sens.: hot, radius <= 6.91 kpc (largest lens R_E)", lambda r: r["phase"] == "hot" and r["r_kpc"] <= 6.91),
    ("sens.: hot, M* >= 1e11", lambda r: r["phase"] == "hot" and r["mstar"] >= 1e11),
    ("sens.: molecular, M* >= 1e11", lambda r: r["phase"] == "molecular" and r["mstar"] >= 1e11),
]
print("| Group | N | Detections | Limits | Detected range | Limit range | Median (limits at value) | Median (limits at 0) |")
print("|---|---|---|---|---|---|---|---|")
for name, f in groups:
    sel = [r for r in out if f(r) and r["use"] and r["in_range"]]
    d = dist(sel)
    rng = lambda a, b: "—" if a is None else f"{fmt(a)}–{fmt(b)}"
    print(f"| {name} | {d['n']} | {d['n_det']} | {d['n_lim']} | {rng(d['det_min'], d['det_max'])} | "
          f"{rng(d['lim_min'], d['lim_max'])} | {fmt(d['med_upper'])} | {fmt(d['med_lower'])} |")
sel = [r for r in out if r["cand"] == "N13" and r["in_range"]]
d = dist(sel, "ratio_scaled")
print(f"\nN13 with optional de Vaucouleurs scaling to the beam radius: n={d['n']}, limits {fmt(d['lim_min'])}–{fmt(d['lim_max'])}")
excl = [(r['cand'], r['galaxy'], fmt(r['mstar'])) for r in out if not r['in_range']]
print("Outside lens range:", excl)
s = [r for r in out if r["cand"] == "N2"]
d = dist(s)
print(f"N2 incl. NGC 4552 (10.7 kpc): n={d['n']} median(limits at value)={fmt(d['med_upper'])} max det={fmt(d['det_max'])}")
