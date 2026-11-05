"""Convert aeg-d-dwarfs v1 into v2 under data standard 2.5.1, as the frozen REPRODUCTION.md specifies.

Usage: python data/packages/aeg-d-dwarfs/v2/convert.py

v2 re-issues v1 (D-083, D-084). It starts from v1's own tables, so that every unchanged value is
carried bit for bit, and applies only:
- the D-096 changes recorded in the frozen second reading (reading/resolved.csv, hashed in
  data/frozen/dwarfs-v2-reading.json): Phoenix II (D-096 rule 1; D-098 rule 5) and Fornax (D-101);
- the D-097 classes in that reading (D-098 to D-100, D-102): findings recorded, not plotted;
  possibilities plotted with the quotation;
- the confidence levels, binary-screening classes and R_h, ellipticity and distance errors in that
  reading;
- the 2.4.0/2.5.1 columns and the uncertainty-terms table of REPRODUCTION.md items 5 to 7.

It contains no system-specific rule of its own beyond what the frozen test names. The recomputed
values use v1's frozen formula (v1/convert.py `accelerations`) and, for the coverage of a changed
structure, v1's frozen coverage code (aeg.coverage via v1/reproduction/coverage_from_tables_v2.py's
member rules). It writes the tables, datapackage.json, checksums.sha256 and
reading/conversion_changes.json, and runs REPRODUCTION.md item 4 (arithmetic).
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from astropy.table import MaskedColumn, Table
import astropy.units as u

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
V1 = HERE.parent / "v1"
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg.package import write_checksums, write_datapackage  # noqa: E402
from aeg.coverage import Structure, r_over_ah, summarise  # noqa: E402

DATASET, VERSION, STANDARD = "aeg-d-dwarfs", "v2", "2.5.1"
PID, P1 = f"{DATASET}/{VERSION}", f"{DATASET}/v1"
G = 6.67430e-11
PC = 3.0856775814913673e16
M_SUN = 1.98840987e30

_spec = importlib.util.spec_from_file_location("v1convert", V1 / "convert.py")
v1c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1c)
accelerations = v1c.accelerations  # v1's frozen formula

# REPRODUCTION.md item 5: v1 folded the paper's modulus into the magnitude error for five systems
# (v1/reproduction/inputs_v2.py MAG_OVERRIDE). The M_V error alone (e_minus, e_plus) per system.
MODULUS_FOLDED = {"aeg-s-000347": (0.2, 0.2), "aeg-s-000348": (0.3, 0.3), "aeg-s-000393": (0.4, 0.4),
                  "aeg-s-000390": (None, None), "aeg-s-000402": (0.27, 0.27)}
PHOENIX_II, FORNAX, AND_XII, LEO_T = "aeg-s-000394", "aeg-s-000381", "aeg-s-000352", "aeg-s-000390"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def vals(table):
    out = []
    for i in range(len(table)):
        row = {}
        for c in table.colnames:
            v = table[c][i]
            if np.ma.is_masked(v):
                v = None
            elif isinstance(v, (np.floating,)):
                v = float(v)
            elif isinstance(v, (np.integer,)):
                v = int(v)
            elif isinstance(v, (np.str_, str)):
                v = str(v)
                if v == "":
                    v = None
            row[c] = v
        out.append(row)
    return out


def v2id(x):
    return None if x is None else str(x).replace(P1 + "/", PID + "/")


def col(name, data, unit=None, ucd=None, description="", numeric=False, integer=False):
    return v1c.col(name, data, unit, ucd, description, numeric, integer)


def parse_err(text: str):
    """(err_lo, err_hi) as printed, from the reading's value strings; None where none is printed."""
    t = text.strip()
    if t.lower().startswith("none"):
        return None, None
    inner = re.search(r"\(([^()]*)\)", t)
    for s in ([inner.group(1)] if inner else []) + [t]:
        m = re.search(r"\+([0-9.]+)\s*/\s*-([0-9.]+)", s)
        if m:
            return float(m.group(2)), float(m.group(1))
        m = re.search(r"(?:\+/-|\\pm|±)\s*([0-9.]+)", s)
        if m:
            return float(m.group(1)), float(m.group(1))
    m = re.match(r"^([0-9.]+)\b", t)
    if m:
        return float(m.group(1)), float(m.group(1))
    raise SystemExit(f"cannot parse error {text!r}")


def parse_level(text: str):
    t = text.strip()
    if t.lower().startswith("not stated"):
        return None, "not_given_by_source"
    m = re.match(r"^([0-9.]+)\b", t)
    if m and "stated" in t:
        return float(m.group(1)), "stated"
    raise SystemExit(f"cannot parse level {text!r}")


def squash(s: str) -> str:
    return " ".join((s or "").split())


def main() -> int:
    reading = list(csv.DictReader(open(HERE / "reading/resolved.csv", encoding="utf-8")))
    frozen = json.loads((ROOT / "data/frozen/dwarfs-v2-reading.json").read_text(encoding="utf-8"))
    rel = f"data/packages/{DATASET}/{VERSION}/reading/resolved.csv"
    if frozen["files"][rel] != sha(HERE / "reading/resolved.csv"):
        raise SystemExit("reading/resolved.csv does not match its freeze record")
    if any(r["resolution"] == "awaiting_ruling" for r in reading):
        raise SystemExit("the reading still has rows awaiting a ruling")
    rd = {}
    for r in reading:
        rd.setdefault((r["system_id"], r["field"]), []).append(r)

    def one(sid, field):
        rows = rd.get((sid, field), [])
        if len(rows) != 1:
            raise SystemExit(f"expected one {field} row for {sid}, found {len(rows)}")
        return rows[0]

    m1, o1, s1 = (Table.read(V1 / f"tables/{n}.ecsv", format="ascii.ecsv") for n in ("measurements", "observables", "systems"))
    M, O, S = vals(m1), vals(o1), vals(s1)
    inputs = {r["key"]: r for r in csv.DictReader(open(V1 / "reading/conversion_inputs.csv", encoding="utf-8"))}
    key_of = {s["system_id"]: json.loads(s["properties"])["lvdb_key"] for s in S}
    name_of = {s["system_id"]: s["name_in_source"] for s in S}
    changes = []

    # ---- observables: v1's rows, re-prefixed, with the item 6 errors and the item 5 levels -------------
    for o in O:
        o["observable_id"] = v2id(o["observable_id"])
        o["err_level"], o["err_level_status"] = None, None
    obs_by_id = {o["observable_id"]: o for o in O}

    def new_obs(sid, side, q, value, unit, steps, ref, lo=None, hi=None, band=None, limit="none", param=None,
                level=None, lstatus=None):
        oid = f"{PID}/o{len(O) + 1:06d}"
        o = {"observable_id": oid, "system_id": sid, "side": side, "quantity": q, "value": value, "err_lo": lo,
             "err_hi": hi, "unit": unit, "band": band, "limit": limit, "steps": steps, "evidence_tier": 1,
             "source_ref": ref, "x_dwarfs_parameter": param, "err_level": level, "err_level_status": lstatus}
        O.append(o)
        obs_by_id[oid] = o
        return oid

    # ---- measurements ----------------------------------------------------------------------------------
    for m in M:
        m["measurement_id"] = v2id(m["measurement_id"])
        m["observed_from"] = v2id(m["observed_from"])
        m["baryonic_from"] = ";".join(v2id(x) for x in m["baryonic_from"].split(";"))
        m["alternative_of"] = None
    v1_rows = {m["system_id"]: dict(m) for m in M}  # snapshot, re-prefixed, values untouched

    # item 5 and 6 columns, row by row
    for m in M:
        sid = m["system_id"]
        k = key_of[sid]
        ci = inputs[k]
        # R_h and ellipticity (item 6)
        rh_lo, rh_hi = parse_err(one(sid, "rh_err")["value"])
        if "pc (" in one(sid, "rh_err")["value"]:  # printed in pc: carried to arcmin at the package's own conversion
            fac = float(ci["R_h_arcmin"]) / float(re.search(r"Re = ([0-9.]+)", one(sid, "rh_err")["value"]).group(1))
            rh_lo, rh_hi = rh_lo * fac, rh_hi * fac
        e = float(ci["ellipticity"] or 0.0)
        a = float(ci["rh_printed"])
        Rh = float(ci["R_h_arcmin"])
        used = 1 if ci["rh_convention"].startswith("semi-major") else 0
        expect = a * math.sqrt(1.0 - e) if used else a
        if abs(Rh - expect) > 1e-4 * max(Rh, 1e-9):
            raise SystemExit(f"R_h convention not recognised for {sid}: {ci['rh_convention']!r}, {a}, {e}, {Rh}")
        fac = math.sqrt(1.0 - e) if used else 1.0
        m["x_dwarfs_rh_err_lo_arcmin"] = None if rh_lo is None else rh_lo * fac
        m["x_dwarfs_rh_err_hi_arcmin"] = None if rh_hi is None else rh_hi * fac
        m["x_dwarfs_ellipticity"] = e if used else 0.0
        ee = one(sid, "eps_err")["value"]
        e_lo, e_hi = parse_err(ee)
        m["x_dwarfs_ellipticity_err_lo"], m["x_dwarfs_ellipticity_err_hi"] = (e_lo, e_hi) if used else (None, None)
        m["x_dwarfs_eps_used"] = used
        m["x_dwarfs_rh_semimajor_assumed"] = 1 if "rh_semimajor_assumed" in (ci.get("flags") or "").split() else 0
        d_lo, d_hi = (float(ci["distance_err_minus"]) if ci["distance_err_minus"] else None,
                      float(ci["distance_err_plus"]) if ci["distance_err_plus"] else None)
        m["x_dwarfs_distance_err_lo_kpc"], m["x_dwarfs_distance_err_hi_kpc"] = d_lo, d_hi
        m["x_dwarfs_gbar_stars_distance_exponent"] = -2 if "mv_distance_independent" in (m["x_dwarfs_flags"] or "").split() else 0
        m["_rh"] = (rh_lo, rh_hi, a, ci["rh_unit"])
        m["_eps"] = (e_lo, e_hi)
        # levels (item 5)
        if sid == AND_XII:
            m["err_level"], m["err_level_status"] = None, "not_given_by_source"
        else:
            m["err_level"], m["err_level_status"] = parse_level(one(sid, "sigma_level")["value"])
        m["g_bar_err_level"], m["g_bar_err_level_status"] = parse_level(one(sid, "mag_level")["value"])
        # binary screening (item 9)
        bs = one(sid, "binary_screening")["value"]
        if bs not in ("multi_epoch_stated", "no_multi_epoch_stated", "not_stated"):
            raise SystemExit(f"binary screening {bs!r} for {sid}")
        m["x_dwarfs_binary_screening"] = bs
        if one(sid, "distance_inherited")["value"].startswith("yes"):
            m["x_dwarfs_flags"] = " ".join(filter(None, [m["x_dwarfs_flags"], "distance_inherited"]))
        # D-038 1A (item 9): every v1 row passed it in v1's coding (checked in the result)
        m["assumptions"] = m["assumptions"] + ";dw_member_sample_sigma"
        m["flags"] = ";".join(filter(None, [m["flags"], "star_count_weighting"]))

    # observables: R_h, ellipticity and distance errors (item 6); levels on sigma and magnitude rows (item 5)
    for m in M:
        sid = m["system_id"]
        bar = [obs_by_id[x] for x in m["baryonic_from"].split(";")]
        osig = obs_by_id[m["observed_from"]]
        osig["err_level"], osig["err_level_status"] = m["err_level"], m["err_level_status"]
        for o in bar:
            if o["quantity"] == "half_light_radius":
                lo, hi, _a, _unit = m["_rh"]
                if lo is None:
                    o["source_ref"] = (o["source_ref"] or "") + "; no_uncertainty: no error printed"
                elif "pc (" in one(sid, "rh_err")["value"]:
                    o["err_lo"], o["err_hi"] = m["x_dwarfs_rh_err_lo_arcmin"], m["x_dwarfs_rh_err_hi_arcmin"]
                    o["source_ref"] = (o["source_ref"] or "") + "; error printed in pc (32 pc), converted as the value"
                else:
                    o["err_lo"], o["err_hi"] = lo, hi
            elif o["quantity"] == "structural_param":
                lo, hi = m["_eps"]
                if lo is None:
                    o["source_ref"] = (o["source_ref"] or "") + "; no_uncertainty: no error printed"
                else:
                    o["err_lo"], o["err_hi"] = lo, hi
            elif o["quantity"] == "distance":
                if m["x_dwarfs_distance_err_lo_kpc"] is None:
                    if "no_uncertainty" not in (o["source_ref"] or ""):
                        o["source_ref"] = (o["source_ref"] or "") + "; no_uncertainty: no error printed"
                else:
                    o["err_lo"], o["err_hi"] = m["x_dwarfs_distance_err_lo_kpc"], m["x_dwarfs_distance_err_hi_kpc"]
            elif o["quantity"] == "apparent_magnitude":
                o["err_level"], o["err_level_status"] = m["g_bar_err_level"], m["g_bar_err_level_status"]

    # ---- point-scale g_bar errors (item 5) -------------------------------------------------------------
    def point_errs(m):
        if m["system_id"] in MODULUS_FOLDED:
            em, ep = MODULUS_FOLDED[m["system_id"]]
            g_st = m["g_bar_stars"]
            return (None if ep is None else g_st * (1 - 10 ** (-0.4 * ep)),
                    None if em is None else g_st * (10 ** (0.4 * em) - 1))
        return m["g_bar_err_lo"], m["g_bar_err_hi"]

    for m in M:
        m["g_bar_err_point_lo"], m["g_bar_err_point_hi"] = point_errs(m)

    # ---- D-096 changes from the reading (item 3) --------------------------------------------------------
    by_sid = {m["system_id"]: m for m in M}
    alternatives = []

    def recompute(m, r_inputs):
        a = accelerations(r_inputs)
        m["r_kpc"] = a["r_half_pc"] / 1000.0
        m["g_obs"] = a["g_obs"]
        m["g_bar_stars"], m["g_bar_gas_cold"] = a["g_bar_stars"], a["g_bar_gas"]
        m["g_bar"] = a["g_bar_stars"] + a["g_bar_gas"]
        sig = float(r_inputs["sigma"])
        s_lo, s_hi = float(r_inputs["sigma_err_minus"]), float(r_inputs["sigma_err_plus"])
        m["g_obs_err_lo"] = m["g_obs"] * (1 - ((sig - s_lo) / sig) ** 2)
        m["g_obs_err_hi"] = m["g_obs"] * (((sig + s_hi) / sig) ** 2 - 1)
        mlo, mhi = float(r_inputs["mag_err_minus"]), float(r_inputs["mag_err_plus"])
        m["g_bar_err_hi"] = m["g_bar_stars"] * (10 ** (0.4 * mlo) - 1)
        m["g_bar_err_lo"] = m["g_bar_stars"] * (1 - 10 ** (-0.4 * mhi))
        m["g_bar_err_point_lo"], m["g_bar_err_point_hi"] = point_errs(m)
        m["x_dwarfs_sigma"] = sig
        m["x_dwarfs_sigma_err_lo"], m["x_dwarfs_sigma_err_hi"] = s_lo, s_hi
        m["x_dwarfs_R_h_arcmin"] = float(r_inputs["R_h_arcmin"])

    # Phoenix II: D-096 rule 1 (reading: d096_preferred, role=sigma, ruled; D-098 rule 5)
    pref = [r for r in rd[(PHOENIX_II, "d096_preferred")] if r["resolution"] == "ruled"]
    assert len(pref) == 1 and "11.0" in pref[0]["value"], pref
    m = by_sid[PHOENIX_II]
    ci = dict(inputs[key_of[PHOENIX_II]])
    old = {"sigma": ci["sigma"], "err": (ci["sigma_err_minus"], ci["sigma_err_plus"]), "r_kpc": m["r_kpc"],
           "g_obs": m["g_obs"], "g_bar": m["g_bar"]}
    ci.update(sigma="11.0", sigma_err_minus="5.3", sigma_err_plus="9.4")
    recompute(m, ci)
    o_new = new_obs(PHOENIX_II, "observed", "sigma_los", 11.0, "km / s",
                    "spectra;stellar_velocities;membership;binary_treatment;dispersion_global",
                    "Fritz 2019 A&A 623 A129, Table 4, certain members (arXiv 1805.07350v4 spec_v1_ref1_arx.tex l. 452; "
                    "bold = preferred, caption l. 436); D-096 rule 1 (D-098 rule 5); reading/resolved.csv",
                    5.3, 9.4, param="certain members (the source's preferred value)",
                    level=m["err_level"], lstatus=m["err_level_status"])
    m["observed_from"] = o_new
    m["source_ref"] = m["source_ref"].replace("Fritz 2019 A&A 623 A129", "Fritz 2019 A&A 623 A129 (certain members, Table 4 l. 452)", 1)
    m["notes"] = ("D-096 rule 1: Fritz et al. 2019 mark the certain-members value as preferred (Table 4 caption, l. 436: "
                  "\"We indicate in bold which determination we prefer\"); l. 415: σ \"does not depend significantly on which "
                  "set of members is considered\". The all-members 9.5 km/s is an alternative row.")
    changes.append({"system_id": PHOENIX_II, "name": "Phoenix II", "rule": "D-096 rule 1 (D-098 rule 5)",
                    "reading": "reading/resolved.csv: d096_preferred, role=sigma, resolution=ruled",
                    "quote": "We indicate in bold which determination we prefer (Fritz 2019, l. 436); bold row 11.0 (+9.4/-5.3) km/s (l. 452)",
                    "old": old, "new": {"sigma": "11.0", "err": ("5.3", "9.4"), "r_kpc": m["r_kpc"], "g_obs": m["g_obs"], "g_bar": m["g_bar"]},
                    "plotting": "D-038 1A: v1 coding phoenix_2/v2 has coverage = beyond_rh (Fritz Table 2), so it passes; plotted"})
    alternatives.append((PHOENIX_II, "D-096 rule 1: the all-members value 9.5 (+6.8/−4.4) km/s (Fritz 2019 Table 4 l. 446); "
                                     "the source prefers the certain-members value. v1's default, kept as an alternative."))

    # Fornax: D-101 (D-096 rule 1): Wang 2019 Sérsic fit, the stated best fit
    pref = [r for r in rd[(FORNAX, "d096_preferred")] if r["resolution"] == "ruled"]
    assert len(pref) == 1 and "Sersic" in pref[0]["value"], pref
    m = by_sid[FORNAX]
    ci = dict(inputs[key_of[FORNAX]])
    old = {"rh_printed": ci["rh_printed"], "R_h_arcmin": ci["R_h_arcmin"], "r_kpc": m["r_kpc"], "g_obs": m["g_obs"], "g_bar": m["g_bar"]}
    e = float(ci["ellipticity"])
    ci.update(rh_printed="20.1", R_h_arcmin=f"{20.1 * math.sqrt(1 - e):.6g}")
    recompute(m, ci)
    m["x_dwarfs_rh_err_lo_arcmin"] = m["x_dwarfs_rh_err_hi_arcmin"] = None
    old_rh = [x for x in m["baryonic_from"].split(";") if obs_by_id[x]["quantity"] == "half_light_radius"][0]
    o_new = new_obs(FORNAX, "baryonic", "half_light_radius", 20.1, "arcmin", "photometry;structural_model",
                    "Wang2019ApJ...881..118W Table 1, Sérsic column (arXiv 1809.07801v1 Fornax_main.tex l. 106); the source's "
                    "stated best fit, l. 333 (D-101; D-096 rule 1); no_uncertainty: no error printed",
                    param="as printed (semi-major (assumed, D-052 item 2)); Sérsic fit")
    m["baryonic_from"] = m["baryonic_from"].replace(old_rh, o_new)
    m["source_ref"] = m["source_ref"].replace("different profile models)", "different profile models; Sérsic column, D-101)", 1)
    m["notes"] = ("D-101 (D-096 rule 1): Wang et al. 2019 \"found that Sersic model gives the best fit to the data\" "
                  "(Fornax_main.tex l. 333), so the Sérsic radius 20.1′ is used. The exponential 19.8′ is an alternative row.")
    # coverage of the new structure with v1's frozen member rule (Hendricks 2014) and v1's code
    cfg = [r for f in sorted(V1.glob("reading/coverage_config*.csv")) for r in csv.DictReader(open(f, encoding="utf-8"))
           if r["key"] == key_of[FORNAX] and r["paper"] == inputs[key_of[FORNAX]]["sigma_paper"]]
    st = {r["key"]: r for r in csv.DictReader(open(V1 / "reading/structure_values.csv", encoding="utf-8"))}[key_of[FORNAX]]
    s = Structure(float(st["ra0_deg"]), float(st["dec0_deg"]), float(st["ellipticity"] or 0.0), float(st["pa_deg"] or 0.0), 20.1)
    rows = list(csv.DictReader(open(V1 / "source/members" / cfg[0]["table_file"], encoding="utf-8")))
    used_rows = [r for r in rows if eval(cfg[0]["member_rule"], {"math": math}, dict(r))]  # noqa: S307 - v1's frozen rule
    cov = summarise([r_over_ah(float(r[cfg[0]["ra_col"]]), float(r[cfg[0]["dec_col"]]), s) for r in used_rows])
    if cov.get("passes") is not True:
        m["plotted"], m["not_plotted_reason"] = "false", "coverage_below_threshold"
    changes.append({"system_id": FORNAX, "name": "Fornax", "rule": "D-096 rule 1 (D-101)",
                    "reading": "reading/resolved.csv: d096_preferred and d096_conflict, role=structure, resolution=ruled",
                    "quote": "found that Sersic model gives the best fit to the data while other models seem to fail to capture the complex light profile shape of Fornax (Wang 2019, Fornax_main.tex l. 333)",
                    "old": old, "new": {"rh_printed": "20.1", "R_h_arcmin": ci["R_h_arcmin"], "r_kpc": m["r_kpc"], "g_obs": m["g_obs"], "g_bar": m["g_bar"]},
                    "plotting": f"D-038 1A with D-051 (Hendricks 2014 member table, v1's frozen rule, a_h = 20.1′): {cov}",
                    "coverage": cov})
    alternatives.append((FORNAX, "D-101 (D-096 rule 1): the exponential-profile radius 19.8′ (Wang 2019 Table 1, exponential "
                                 "column); the source states the Sérsic fit is best. v1's default, kept as an alternative."))

    # ---- D-097 classes from the reading (item 8) --------------------------------------------------------
    excluded = []
    counts = {"finding": 0, "possibility": 0, "none": 0}
    stmt_counts = {"finding": 0, "possibility": 0, "neither": 0}
    for r in reading:
        if r["field"] == "d097" and r["value"] in stmt_counts:
            stmt_counts[r["value"]] += 1
    for m in M:
        sid = m["system_id"]
        cls = one(sid, "d097_class")["value"]
        counts[cls] += 1
        if cls == "none":
            continue
        st_rows = [r for r in rd.get((sid, "d097"), []) if r["value"] == cls]
        if not st_rows:
            raise SystemExit(f"{sid}: class {cls} without a {cls} statement")
        text = " | ".join(f"\"{squash(r['quote'])}\" ({r['source']}, {r['location']})" for r in st_rows)
        if cls == "finding":
            m["plotted"], m["not_plotted_reason"] = "false", "other"
            m["notes"] = "; ".join(filter(None, [m["notes"], f"D-097 finding (D-097 to D-100), recorded, not plotted: {text}"]))
            first = st_rows[0]
            excluded.append({"system": sid, "dataset": PID, "reason": f"D-097 finding: {squash(first['quote'])}",
                             "citation": f"{first['source']}, {first['location']}"})
        else:
            m["notes"] = "; ".join(filter(None, [m["notes"], f"D-097 possibility (D-097 to D-100), plotted: {text}"]))

    # ---- alternative rows (D-096), appended (item 1) -----------------------------------------------------
    for sid, note in sorted(alternatives, key=lambda t: list(by_sid).index(t[0])):
        a = dict(v1_rows[sid])
        for k in ("x_dwarfs_rh_err_lo_arcmin", "x_dwarfs_rh_err_hi_arcmin", "x_dwarfs_ellipticity", "x_dwarfs_ellipticity_err_lo",
                  "x_dwarfs_ellipticity_err_hi", "x_dwarfs_eps_used", "x_dwarfs_rh_semimajor_assumed", "x_dwarfs_distance_err_lo_kpc",
                  "x_dwarfs_distance_err_hi_kpc", "x_dwarfs_gbar_stars_distance_exponent", "err_level", "err_level_status",
                  "g_bar_err_level", "g_bar_err_level_status", "x_dwarfs_binary_screening", "assumptions", "flags", "x_dwarfs_flags"):
            a[k] = by_sid[sid][k]
        if sid == FORNAX:  # the alternative keeps the exponential radius and its own printed error (none)
            a["x_dwarfs_rh_err_lo_arcmin"] = a["x_dwarfs_rh_err_hi_arcmin"] = None
        a["g_bar_err_point_lo"], a["g_bar_err_point_hi"] = point_errs(a)
        a["measurement_id"] = f"{PID}/m{len(M) + 1:06d}"
        a["role"], a["alternative_of"] = "alternative", by_sid[sid]["measurement_id"]
        a["plotted"], a["not_plotted_reason"] = "false", "alternative_value"
        a["notes"] = note
        M.append(a)
    for m in M:
        m.pop("_rh", None)
        m.pop("_eps", None)

    # ---- systems (item 2b) ----------------------------------------------------------------------------
    excl_ids = {e["system"] for e in excluded}
    for srow in S:
        sid = srow["system_id"]
        props = json.loads(srow["properties"])
        mrow = by_sid.get(sid)
        if sid in excl_ids:
            props["status"] = "recorded"
            props["reason_not_plotted"] = "D-097 finding (D-097 to D-100): see data/registry/excluded.csv"
        elif mrow is not None and mrow["plotted"] == "false" and props.get("status") == "plotted":
            props["status"] = "recorded"
            props["reason_not_plotted"] = mrow["not_plotted_reason"]
        srow["properties"] = json.dumps(props, ensure_ascii=False, sort_keys=True)

    # ---- write the tables ---------------------------------------------------------------------------
    acc = u.m / u.s ** 2
    meas_cols = list(m1.colnames)
    ins = meas_cols.index("g_bar_err_hi") + 1
    for c in ["g_bar_err_point_lo", "g_bar_err_point_hi"][::-1]:
        meas_cols.insert(ins, c)
    meas_cols.insert(meas_cols.index("role") + 1, "alternative_of")
    meas_cols.insert(meas_cols.index("g_obs_err_hi") + 1, "err_level")
    meas_cols.insert(meas_cols.index("err_level") + 1, "err_level_status")
    meas_cols.insert(meas_cols.index("g_bar_err_point_hi") + 1, "g_bar_err_level")
    meas_cols.insert(meas_cols.index("g_bar_err_level") + 1, "g_bar_err_level_status")
    new_ext = ["x_dwarfs_rh_err_lo_arcmin", "x_dwarfs_rh_err_hi_arcmin", "x_dwarfs_ellipticity", "x_dwarfs_ellipticity_err_lo",
               "x_dwarfs_ellipticity_err_hi", "x_dwarfs_eps_used", "x_dwarfs_rh_semimajor_assumed", "x_dwarfs_distance_err_lo_kpc",
               "x_dwarfs_distance_err_hi_kpc", "x_dwarfs_gbar_stars_distance_exponent", "x_dwarfs_binary_screening"]
    meas_cols += new_ext
    desc1 = {c: (m1[c].description, m1[c].unit, (m1[c].meta or {}).get("ucd"), m1[c].dtype.kind) for c in m1.colnames}
    desc1["g_obs_err_lo"] = ("From the dispersion's printed lower error only. Each pipeline's per-star velocity floors are inside it: the source folds them into its σ error and they cannot be separated (term velocity_error_model)", acc, "stat.error;phys.acceleration", "f")
    desc1["g_obs_err_hi"] = ("From the dispersion's printed upper error only. Each pipeline's per-star velocity floors are inside it: the source folds them into its σ error and they cannot be separated (term velocity_error_model)", acc, "stat.error;phys.acceleration", "f")
    desc1["g_bar_err_lo"] = ("From the magnitude error only (stars), as v1. For five systems v1 folded the paper's distance modulus into it (v1/reproduction/inputs_v2.py MAG_OVERRIDE); g_bar_err_point_lo excludes it", acc, "stat.error;phys.acceleration", "f")
    desc1["g_bar_err_hi"] = ("From the magnitude error only (stars), as v1. For five systems v1 folded the paper's distance modulus into it (v1/reproduction/inputs_v2.py MAG_OVERRIDE); g_bar_err_point_hi excludes it", acc, "stat.error;phys.acceleration", "f")
    desc1.update({
        "g_bar_err_point_lo": ("Point-scale part of g_bar_err_lo: on And VI, And VII, Phoenix and Tucana the M_V error alone (the paper's modulus cancels in m = M_V + μ_paper, REPRODUCTION.md item 5); on Leo T empty (M_V printed without an error, term g_bar_point_leo_t); on every other row equal to g_bar_err_lo", acc, "stat.error;phys.acceleration", "f"),
        "g_bar_err_point_hi": ("Point-scale part of g_bar_err_hi, as g_bar_err_point_lo", acc, "stat.error;phys.acceleration", "f"),
        "alternative_of": ("For an alternative row, the measurement_id of the default it is an alternative to (D-096)", None, "meta.ref", "U"),
        "err_level": ("Confidence level of the σ errors or upper limit, as the σ source states it (frozen second reading, reading/resolved.csv)", None, "stat.confidenceLevel", "f"),
        "err_level_status": ("stated, or not_given_by_source (frozen second reading)", None, "meta.code", "U"),
        "g_bar_err_level": ("Confidence level of the magnitude error, as the magnitude source states it (frozen second reading)", None, "stat.confidenceLevel", "f"),
        "g_bar_err_level_status": ("stated, or not_given_by_source (frozen second reading)", None, "meta.code", "U"),
        "x_dwarfs_rh_err_lo_arcmin": ("Printed lower error of the half-light radius, carried to the circularised R_h with ε fixed (× √(1 − ε) where x_dwarfs_eps_used = 1); empty where none is printed. Size column of term half_light_radius (with _hi)", u.arcmin, "stat.error;phys.angSize", "f"),
        "x_dwarfs_rh_err_hi_arcmin": ("Printed upper error of the half-light radius, as x_dwarfs_rh_err_lo_arcmin. Size column of term half_light_radius", u.arcmin, "stat.error;phys.angSize", "f"),
        "x_dwarfs_ellipticity": ("Ellipticity ε used in R_h = a √(1 − ε); 0 where the radius is printed circularised. Read by the dw_ellipticity and dw_rh_circularised formulas", None, "phys.size.axisRatio", "f"),
        "x_dwarfs_ellipticity_err_lo": ("Printed lower error of ε, where x_dwarfs_eps_used = 1; empty otherwise or where none is printed", None, "stat.error", "f"),
        "x_dwarfs_ellipticity_err_hi": ("Printed upper error of ε, as _lo. Size column of term ellipticity", None, "stat.error", "f"),
        "x_dwarfs_eps_used": ("1 where R_h = a √(1 − ε) is used, else 0. Read by the dw_ellipticity formula", None, "meta.code", "f"),
        "x_dwarfs_rh_semimajor_assumed": ("1 on rows flagged rh_semimajor_assumed (D-052 item 2), else 0. Read by the dw_rh_circularised formula", None, "meta.code", "f"),
        "x_dwarfs_distance_err_lo_kpc": ("Printed lower distance error; empty where none is printed", u.kpc, "stat.error;pos.distance", "f"),
        "x_dwarfs_distance_err_hi_kpc": ("Printed upper distance error, as _lo. Size column of term distance", u.kpc, "stat.error;pos.distance", "f"),
        "x_dwarfs_gbar_stars_distance_exponent": ("Exponent e in g_bar_stars ∝ D^e: −2 on rows flagged mv_distance_independent (Boötes III, D-061 item 2), else 0 (adjudication F1). Read by the dw_distance formula", None, "meta.number", "f"),
        "x_dwarfs_binary_screening": ("Whether the σ source states multi-epoch screening for binaries (D-025): multi_epoch_stated, no_multi_epoch_stated or not_stated (frozen second reading)", None, "meta.code", "U"),
    })
    desc1["assumptions"] = ("Named assumptions affecting this row; dw_member_sample_sigma (D-038 1A) added in v2", None, "meta.note", "U")
    desc1["flags"] = ("Atlas flags; star_count_weighting (D-038 1A) added in v2", None, "meta.code", "U")
    desc1["notes"] = ("Notes, including the D-096 change and any D-097 statement with its quotation (frozen second reading)", None, "meta.note", "U")
    desc1["not_plotted_reason"] = ("Why not plotted (closed list): other = D-097 finding; alternative_value = D-096 alternative", None, "meta.note", "U")

    def build(cols, rows, descs):
        out = []
        for c in cols:
            d, unit, ucd, kind = descs[c]
            data = [r.get(c) for r in rows]
            if kind == "f":
                out.append(col(c, data, unit, ucd, d, numeric=True))
            elif kind in "iu":
                out.append(col(c, data, unit, ucd, d, integer=True))
            else:
                out.append(col(c, data, unit, ucd, d))
        return Table(out)

    meas = build(meas_cols, M, desc1)
    meas.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}

    odesc = {c: (o1[c].description, o1[c].unit, (o1[c].meta or {}).get("ucd"), o1[c].dtype.kind) for c in o1.colnames}
    odesc["err_level"] = ("Confidence level of the errors or limit, as the source states it (sigma and magnitude rows; frozen second reading)", None, "stat.confidenceLevel", "f")
    odesc["err_level_status"] = ("stated, or not_given_by_source; empty where not read", None, "meta.code", "U")
    ocols = list(o1.colnames)
    ocols.insert(ocols.index("err_hi") + 1, "err_level")
    ocols.insert(ocols.index("err_level") + 1, "err_level_status")
    obs_t = build(ocols, O, odesc)
    obs_t.meta = dict(meas.meta)
    sdesc = {c: (s1[c].description, s1[c].unit, (s1[c].meta or {}).get("ucd"), s1[c].dtype.kind) for c in s1.colnames}
    sys_t = build(list(s1.colnames), S, sdesc)
    sys_t.meta = dict(meas.meta)
    terms = build_terms(M, S, inputs, key_of, rd)

    (HERE / "tables").mkdir(exist_ok=True)
    for n, t in (("measurements", meas), ("observables", obs_t), ("systems", sys_t), ("uncertainty_terms", terms)):
        t.write(HERE / f"tables/{n}.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)

    # REPRODUCTION.md item 4: recompute g_obs and g_bar from the stored columns, to 1e-9 (as v1 test 3)
    back = Table.read(HERE / "tables/measurements.ecsv", format="ascii.ecsv")
    for row in back:
        r_m = row["r_kpc"] * 1000.0 * PC
        g1 = 3.0 * (row["x_dwarfs_sigma"] * 1e3) ** 2 / r_m
        g2 = G * (0.5 * row["x_dwarfs_l_v"] * row["x_dwarfs_upsilon_v"] + row["x_dwarfs_m_gas_rh"]) * M_SUN / r_m ** 2
        if abs(g1 / row["g_obs"] - 1) > 1e-9 or abs(g2 / row["g_bar"] - 1) > 1e-9:
            raise SystemExit(f"arithmetic item 4 failed at {row['measurement_id']}")

    # exclusion register (item 8): this dataset's rows, appended
    reg = ROOT / "data/registry/excluded.csv"
    existing = list(csv.DictReader(open(reg, encoding="utf-8")))
    keep = [r for r in existing if r["dataset"] != PID]
    with open(reg, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["system", "dataset", "reason", "citation"], lineterminator="\n")
        w.writeheader()
        w.writerows(keep + excluded)

    (HERE / "reading/conversion_changes.json").write_text(json.dumps(
        {"changes": changes, "excluded": excluded, "d097_system_classes": counts, "d097_statements": stmt_counts},
        indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")

    desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
    write_datapackage(HERE, desc, {"measurements": ("tables/measurements.ecsv", meas),
                                   "observables": ("tables/observables.ecsv", obs_t),
                                   "systems": ("tables/systems.ecsv", sys_t),
                                   "uncertainty_terms": ("tables/uncertainty_terms.ecsv", terms)})
    write_checksums(HERE)
    print(f"wrote {len(meas)} measurements, {len(obs_t)} observables, {len(sys_t)} systems, {len(terms)} terms; "
          f"{len(changes)} D-096 changes; D-097 classes {counts}; item 4 passes")
    return 0


def build_terms(M, S, inputs, key_of, rd):
    """REPRODUCTION.md item 7: exactly the rows of the frozen table."""
    default_rows = [m for m in M if m.get("role") == "default"]
    sids_with_rows = [m["system_id"] for m in default_rows]
    no_rh = [sid for sid in sids_with_rows if rd[(sid, "rh_err")][0]["value"].lower().startswith("none")]
    no_eps = [m["system_id"] for m in default_rows if m["x_dwarfs_eps_used"] == 1 and m["x_dwarfs_ellipticity_err_lo"] is None]
    no_dist = [m["system_id"] for m in default_rows if m["x_dwarfs_distance_err_lo_kpc"] is None]
    savino = [m["system_id"] for m in default_rows if inputs[key_of[m["system_id"]]]["distance_source"].startswith("Savino2022")]
    martin = [m["system_id"] for m in default_rows if "Martin2016" in inputs[key_of[m["system_id"]]]["mag_source"]]
    T = []

    def t(term_id, scale, applies, moves, status, assumption=None, note="", citation=None, locator=None, **size):
        T.append({"term_id": term_id, "scale": scale, "applies_to": applies, "moves": moves, "status": status,
                  "size_value": size.get("size_value"), "size_lo": size.get("size_lo"), "size_hi": size.get("size_hi"),
                  "size_unit": size.get("size_unit"), "size_column": size.get("size_column"), "size_kind": size.get("size_kind"),
                  "assumption_id": assumption, "correlated_with": None, "covariance": "not_published",
                  "citation": citation, "locator": locator, "note": note})

    t("half_light_radius", "point", "*", "both", "given", "dw_rhalf_wolf",
      "§2a rule 7: g_obs ∝ 1/R_h, g_bar ∝ 1/R_h² (stars and gas); left out of both point columns. Two-sided: x_dwarfs_rh_err_lo_arcmin holds the other side (rule 6)",
      "each system's structural original (observables half_light_radius source_ref)", "docs/sources/readings/step-a-2026-11-04/dwarfs-adjudication.md (R_h measurement error)",
      size_column="x_dwarfs_rh_err_hi_arcmin", size_kind="as_released")
    for sid in no_rh:
        t(f"half_light_radius_{sid}", "point", sid, "both", "not_given_by_source", "dw_rhalf_wolf",
          "the structural original prints no R_h error (frozen second reading)", "structural original", "reading/resolved.csv rh_err")
    t("ellipticity", "point", "*", "both", "given", "dw_ellipticity",
      "enters only where x_dwarfs_eps_used = 1. Two-sided: x_dwarfs_ellipticity_err_lo holds the other side (rule 6)",
      "each system's structural original", "adjudication (ellipticity error)", size_column="x_dwarfs_ellipticity_err_hi", size_kind="as_released")
    for sid in no_eps:
        t(f"ellipticity_{sid}", "point", sid, "both", "not_given_by_source", "dw_ellipticity", "the original prints no ε error", "structural original", "reading/resolved.csv eps_err")
    t("ellipticity_radial_variation", "system", "*", "both", "not_given_by_source", "dw_ellipticity",
      "\"Some galaxies show changes in the position angle and/or ellipticity with radius and the current LVDB format does not account for this\" (Pace 2025 §5, l. 699); Sculptor 0.23–0.49 by subsample (Muñoz 2018)",
      "Pace 2025 OJAp 8 142", "§5, l. 699")
    t("rh_convention_profile", "system", "*", "both", "not_given_by_source", "dw_rh_circularised",
      "profile family, and semi-major or circularised convention (flag rh_semimajor_assumed); effect by the dw_rh_circularised formula (D-052 item 2)", "D-052", "item 2")
    t("deprojection_4_3", "dataset", "*", "both", "given", "dw_rhalf_wolf",
      "a parameter term (§2a rule 4). Wolf et al. 2010 Appendix table (l. 1793–1800): Plummer 1.305 to Sérsic n = 8 1.352; \"accurate to better than 2%\" (l. 150–152). 4/3 is the default",
      "Wolf et al. 2010, arXiv 0908.2995", "l. 1793–1800; l. 150–152", size_lo=1.305, size_hi=1.352, size_unit="r½/R_h", size_kind="range")
    t("distance", "system", "*", "both", "given", "dw_distance",
      "g_obs ∝ 1/D; g_bar_stars ∝ D^e with e from x_dwarfs_gbar_stars_distance_exponent (0, or −2 for Boötes III, D-061 item 2); gas ∝ D⁰ (adjudication F1). Two-sided: x_dwarfs_distance_err_lo_kpc holds the other side (rule 6)",
      "each system's distance source (observables distance source_ref)", "adjudication F1", size_column="x_dwarfs_distance_err_hi_kpc", size_kind="as_released")
    for sid in no_dist:
        note = "the distance source prints no error"
        if sid == "aeg-s-000367":
            note += "; Vivas et al. 2022 give a 5.4 kpc dispersion and a ~13 kpc gradient (l. 264–266)"
        t(f"distance_{sid}", "system", sid, "both", "not_given_by_source", "dw_distance", note, "distance source", "conversion inputs: distance errors empty")
    t("distance_calibration_savino", "dataset", ";".join(savino), "both", "given", "dw_distance",
      "Savino §7 (Conclusions), l. 1244: \"Through extensive tests we quantified our typical systematic uncertainties to be ∼3.5%\". Possible overlap: Savino §5 (l. 952) says the quoted intervals \"have been computed to account for our uncertain knowledge of the RR Lyrae metallicity, pulsation parameters, and of the adopted PWZ calibration\"; it does not say whether the 3.5 % overlaps them. Views show the term beside the error bars, never added in",
      "Savino et al. 2022, ApJ 938, 101", "§7 l. 1244; §5 l. 952", size_value=0.035, size_unit="fraction of D", size_kind="as_released")
    t("distance_calibration_other", "dataset", "*", "both", "not_given_by_source", "dw_distance",
      "Carlin et al. 2017's anchor modulus has no error (l. 114); Higgs et al. 2021's TRGB calibration states none (l. 361); Medina et al. 2018 (1802.01581v1, ms.tex, e-print SHA-256 3108c7bf…, l. 266) gives 1.8 % and ~3.6 % for assumed metallicity offsets of ±0.5 and ±1.0 dex, a conditional test, not an error",
      "Carlin 2017; Higgs 2021; Medina 2018", "l. 114; l. 361; l. 266")
    t("velocity_error_model", "dataset", "*", "g_obs", "not_given_by_source", None,
      "per-star floors inside each source's σ error; effect on σ not stated: Geha 2026 k_v 1.4, floor 1.1 km/s (l. 420); Tollerud 2012 2.2 km/s (l. 268); Heiger 2024 1 km/s (l. 109); Kvasova 2024 1.49 km/s (l. 260); Collins 2013 mask offsets (l. 571–573)",
      "Geha 2026; Tollerud 2012; Heiger 2024; Kvasova 2024; Collins 2013", "as in the note")
    t("binaries", "system", "*", "g_obs", "not_given_by_source", None,
      "Wolf l. 1212–1214: \"up to ∼20%\" in σ, only \"in the smallest dSphs\" (citing Minor 2010); rule 5. Screening per row in x_dwarfs_binary_screening (item 9)", "Wolf et al. 2010", "l. 1212–1214")
    t("membership", "system", "*", "g_obs", "not_given_by_source", None,
      "Tollerud's \"few-percent level\" applies to its own systems only (rule 5)", "Tollerud et al. 2012", "")
    t("rotation", "system", "*", "g_obs", "not_given_by_source", None, "Pace 2025 §5", "Pace 2025", "§5")
    t("light_weighting", "dataset", "*", "g_obs", "not_given_by_source", "dw_member_sample_sigma",
      "member-sample σ taken as the light-weighted σ (D-038 1A)", "D-038", "1A")
    t("estimator_normalisation", "dataset", "*", "g_obs", "not_given_by_source", "dw_equilibrium",
      "Wolf's \"±10%\" is a band drawn for the classical dSphs (l. 922–927), not a stated error for these systems (rule 5)", "Wolf et al. 2010", "l. 922–927")
    t("anisotropy_profile", "dataset", "*", "g_obs", "not_given_by_source", "dw_equilibrium",
      "Wolf l. 990–992: \"the errors on M_half increased by roughly 0.05 dex when the (rather extreme) second β(r) form was used\". This is the error of Wolf's own Jeans analysis, so rule 5 gives no size. The estimator-normalisation and anisotropy terms both describe the estimator; no source states their correlation",
      "Wolf et al. 2010", "l. 990–992")
    t("g_bar_point_leo_t", "point", LEO_T, "g_bar", "not_given_by_source", None,
      "de Jong 2008 M_V printed without an error (item 5)", "de Jong et al. 2008", "")
    t("luminosity_function_martin", "dataset", ";".join(martin), "g_bar", "not_given_by_source", None,
      "Martin l. 385: \"A test performed by assuming that And I is instead…\", with ∼0.2 mag brighter for an 8-Gyr population. A one-galaxy test, so rule 5 gives no size. The \"0.29 ± 0.11 magnitudes fainter\" comparison with the literature is quoted too",
      "Martin et al. 2016", "l. 385")
    t("luminosity_function_other", "dataset", "*", "g_bar", "not_given_by_source", None,
      "IMF and population assumed in other sources' luminosity functions: Muñoz 2018 \"assuming a Salpeter initial mass function\" (l. 416)", "Muñoz et al. 2018", "l. 416")
    t("band_transformation", "dataset", "*", "g_bar", "not_given_by_source", None,
      "Muñoz l. 468 (Jordi 2006); Martin l. 379 (Ibata 2007); Richstein; Leo T (D-055 item 7)", "Muñoz 2018; Martin 2016; Richstein", "l. 468; l. 379")
    t("extinction", "system", "*", "g_bar", "not_given_by_source", None, "Martin l. 377; Higgs l. 221–222; Pace App. A l. 800",
      "Martin 2016; Higgs 2021; Pace 2025", "l. 377; l. 221–222; l. 800")
    t("solar_magnitude", "dataset", "*", "g_bar", "not_given_by_source", None,
      "4.85 (McLaughlin & van der Marel 2005); Carlin and Richstein use 4.83", "McLaughlin & van der Marel 2005", "")
    t("stellar_ml", "dataset", "*", "g_bar", "given", "dw_stellar_ml",
      "the D-060 envelope. Two-sided: x_dwarfs_upsilon_v_low holds the other side (rule 6)", "D-060", "",
      size_column="x_dwarfs_upsilon_v_high", size_kind="range")
    t("helium_factor", "dataset", "*", "g_bar", "not_given_by_source", None, "1.33 (Lelli et al. 2016)", "Lelli et al. 2016", "")
    t("gas_inside_rhalf_aeg-s-000390", "system", "aeg-s-000390", "g_bar", "not_given_by_source", "dw_gas_half_total",
      "Leo T: half the total HI mass (flag gas_half_total)", "D-058", "")
    t("gas_inside_rhalf_aeg-s-000393", "system", "aeg-s-000393", "g_bar", "not_given_by_source", "dw_gas_half_total",
      "Phoenix: as above", "D-058", "")
    t("hi_flux", "system", "*", "g_bar", "not_given_by_source", None,
      "Putman 2021's HI mass errors \"are from the distance errors shown\" (MRT Note 4), so they are part of distance and cancel in g_bar. No flux error is stated. Phoenix's \"confusion with Galactic emission\" (Note 22) is quoted",
      "Putman et al. 2021", "MRT Notes 4 and 22")
    t("hi_limit_assumptions", "dataset", "*", "g_bar", "not_given_by_source", None,
      "5σ limits with a fixed 10 km/s width (Putman l. 176) and an assumed central concentration (l. 166); limits enter g_bar as zero",
      "Putman et al. 2021", "l. 176; l. 166")
    t("molecular_ionised_gas", "dataset", "*", "g_bar", "not_given_by_source", None,
      "not_addressed in v1's x_baryon_inventory", "descriptor x_baryon_inventory", "")
    t("heterogeneity", "dataset", "*", "both", "not_given_by_source", None,
      "\"there will be systematics in the LVDB\" (Pace §5)", "Pace 2025", "§5")
    cols = ["term_id", "scale", "applies_to", "moves", "status", "size_value", "size_lo", "size_hi", "size_unit", "size_column",
            "size_kind", "assumption_id", "correlated_with", "covariance", "citation", "locator", "note"]
    num_cols = {"size_value", "size_lo", "size_hi"}
    out = []
    for c in cols:
        data = [r[c] for r in T]
        out.append(col(c, data, None, "meta.note", c, numeric=c in num_cols))
    tt = Table(out)
    tt.meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    return tt


if __name__ == "__main__":
    sys.exit(main())
