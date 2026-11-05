"""Convert aeg-d-strong-lensing v1 into v2 under data standard 2.5.1, as the frozen REPRODUCTION.md specifies.

Usage
    python -m aeg.fetch data/packages/aeg-d-strong-lensing/v2     (verifies the sources; not read here)
    python data/packages/aeg-d-strong-lensing/v2/convert.py

v2 re-issues v1 (D-083, D-084) with no value changes (the frozen second reading found no D-096 case). It
starts from v1's own tables, so every unchanged value is carried bit for bit, and applies only what the
frozen test (REPRODUCTION.md, data/frozen/lenses-v2-test.json) names:
- item 2/5: the θ_E error moves from g_obs to g_bar on class A rows (§2a rule 7): g_obs_err_* empty there,
  flag no_uncertainty, the note "θ_E error carried by g_bar ..."; point-scale error columns; confidence
  levels per source and side;
- item 6: the per-row extension columns (θ_E error fractions, the light profile where v1 had none,
  d ln g_bar / d ln θ_E, G M*(<R_E)/R_E² at the source's population, the single-system size columns);
- item 2: new observables for the light profiles v1 did not hold (R5's de Vaucouleurs R_e for SLACS);
- item 7: the uncertainty-terms table, exactly the 44 rows of the frozen table.

Every reading-dependent input (θ_E classes and fractions, profiles, confidence levels, distance and H0
values, baryon-inventory statements) is taken only from the frozen reading files v2/reading/*.csv, whose
hashes are checked against data/frozen/lenses-v2-reading.json before anything is written. Constants that
the frozen test itself states (the single-system sizes of item 6 and the term sizes of item 7) are
cross-checked against the reading where it records them. Computed quantities use v1's frozen code:
aeg.lensing (frozen with v1) and v1/convert.py's arithmetic_check (item 4).

It writes tables/, datapackage.json and checksums.sha256. It does not edit data/assumptions.json (the v2
registry entries were appended once by hand, append-only); it checks that they are there.
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
V1 = HERE.parent / "v1"
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg import lensing as L  # noqa: E402  (frozen with v1; used, never edited)
from aeg.package import write_checksums, write_datapackage  # noqa: E402

_spec = importlib.util.spec_from_file_location("lens_v1_convert", V1 / "convert.py")
v1c = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = v1c  # v1's dataclasses look their module up while it loads
_spec.loader.exec_module(v1c)

DATASET, VERSION, STANDARD = "aeg-d-strong-lensing", "v2", "2.5.1"
PID, P1 = f"{DATASET}/{VERSION}", f"{DATASET}/v1"
X = "x_strong_lensing_"
READ = HERE / "reading"
FROZEN_READING = ROOT / "data/frozen/lenses-v2-reading.json"
FROZEN_TEST = ROOT / "data/frozen/lenses-v2-test.json"
STEP = 1e-4  # item 6: central difference in ln R_E
NEW_ASSUMPTIONS = ("a6s_theta_e", "a6s_lens_distance")  # item 7, added to every row's assumptions

# Constants the frozen test states itself (item 6), keyed by the system the test names.
SINGLE_SYSTEM_SIZES = {
    f"{X}mass_ellipticity_frac": ("aeg-s-000506", 0.03),   # J0403-0239, R29 l. 210; term ellipticity_j0403
    f"{X}los_frac": ("aeg-s-000503", 0.02),                # SNL-0, R28 l. 320-322; term line_of_sight_snl0
    f"{X}neighbour_light_frac": ("aeg-s-000505", 0.015),   # SNL-2, R26 l. 141; term neighbour_light_snl2
}
# item 7: the survey names of the frozen term table, by x_strong_lensing_scope
SURVEY = {"SLACS": ["SLACS V-modelled lenses"], "S4TM": ["S4TM lenses"], "SL2S": ["SL2S III sample"],
          "SNELLS": ["SNL-0 (ESO 325-G004)", "SNL-1 (ESO 286-G022)", "SNL-2"],
          "MaNGA": ["MaNGA J1436+4943", "MaNGA J1701+3722"], "NGC 6505": ["Euclid NGC 6505"],
          "J0403": ["MNELLS J0403-0239"], "SNL-0": ["SNL-0 (ESO 325-G004)"],
          "SNL-1": ["SNL-1 (ESO 286-G022)"], "SNL-2": ["SNL-2"]}

THETA_NOTE_A = "θ_E error carried by g_bar, standard §2a rule 7; term {term}"
NOT_COMPUTED = "θ_E error stated; effect on g_bar not computed"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def vals(table) -> list[dict]:
    out = []
    for row in table:
        d = {}
        for c in table.colnames:
            v = row[c]
            if v is np.ma.masked:
                d[c] = None
            elif table[c].dtype.kind == "f":
                d[c] = None if math.isnan(float(v)) else float(v)
            elif table[c].dtype.kind in "iu":
                d[c] = int(v)
            else:
                d[c] = str(v) if str(v) != "" else None
        out.append(d)
    return out


def v2id(x):
    return None if x is None else str(x).replace(P1 + "/", PID + "/")


def read_csv(name: str) -> list[dict]:
    with open(READ / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_frozen() -> None:
    rec = json.loads(FROZEN_READING.read_text(encoding="utf-8"))
    for rel, h in rec["files"].items():
        if sha(ROOT / rel) != h:
            raise SystemExit(f"REFUSED: {rel} does not match its freeze record {FROZEN_READING.name}")
    rec = json.loads(FROZEN_TEST.read_text(encoding="utf-8"))
    for rel, h in rec["files"].items():
        if sha(ROOT / rel) != h:
            raise SystemExit(f"REFUSED: {rel} does not match its freeze record {FROZEN_TEST.name}")


def check_registry() -> None:
    reg = {a["id"]: a for a in json.loads((ROOT / "data/assumptions.json").read_text(encoding="utf-8"))["assumptions"]}
    v1_ids = [a for a, e in reg.items() if a.startswith("a6s_") and P1 in e["datasets"]]
    missing = [a for a in v1_ids + list(NEW_ASSUMPTIONS) if a not in reg or PID not in reg[a]["datasets"]]
    if missing:
        raise SystemExit(f"REFUSED: data/assumptions.json lacks the {PID} entries of {missing} (item 7)")


def dlngbar_dlntheta(theta: float, r_e: float, n: float) -> float:
    """Item 6: −2 + d ln f(<R_E)/d ln R_E, central difference with step 1e-4 in ln R_E (aeg.lensing, frozen)."""
    up = L.sersic_projected_fraction(theta * math.exp(STEP), r_e, n)
    dn = L.sersic_projected_fraction(theta * math.exp(-STEP), r_e, n)
    return -2.0 + (math.log(up) - math.log(dn)) / (2 * STEP)


def records(source_ref: str) -> tuple[str, str]:
    m = re.fullmatch(r"observed (R\d+); stellar (R\d+)", source_ref)
    if not m:
        raise SystemExit(f"cannot read the records of {source_ref!r}")
    return m.group(1), m.group(2)


def level_of(err_rows: list[dict], source: str, side: str, column_prefix: str) -> tuple[float | None, str]:
    """Item 5: the level and status of a filled error column, from err_levels.csv for that source and side.
    Stated only where every reading row behind the column is `stated` with the same numeric level."""
    rows = [r for r in err_rows if r["source"] == source and r["side"] == side and column_prefix in r["v2_error_column"]]
    if not rows:
        raise SystemExit(f"err_levels.csv has no row for {source} {side} ({column_prefix})")
    levels = set()
    for r in rows:
        if r["level_status"].strip() != "stated":
            return None, "not_given_by_source"
        levels.add(float(r["level"]))
    if len(levels) != 1:
        return None, "not_given_by_source"
    return levels.pop(), "stated"


def main() -> int:
    check_frozen()
    check_registry()
    m1, o1, s1 = (Table.read(V1 / f"tables/{n}.ecsv", format="ascii.ecsv") for n in ("measurements", "observables", "systems"))
    M, O, S = vals(m1), vals(o1), vals(s1)
    obs_by_id = {o["observable_id"]: o for o in O}

    theta = {r["measurement_id_v1"]: r for r in read_csv("theta_class.csv")}
    profiles = read_csv("profiles.csv")
    prof_of = {}
    for p in profiles:
        for mid in p["applies_to_rows"].split(";"):
            prof_of[mid] = p
    err_rows = read_csv("err_levels.csv")
    distance = read_csv("distance.csv")
    inventory = read_csv("baryon_inventory.csv")
    d096 = read_csv("d096.csv")

    # item 3 / rule 1: no D-096 case in the frozen reading, so no value changes
    cases = [r for r in d096 if r["d096_case"].strip().lower() not in ("no", "")]
    if cases:
        raise SystemExit(f"REFUSED: the frozen reading lists D-096 cases {[(r['source'], r['item']) for r in cases]}; "
                         "a value change needs a ruling first (REPRODUCTION.md rule 1)")
    if len(theta) != len(M) or any(m["measurement_id"] not in theta for m in M):
        raise SystemExit("theta_class.csv does not cover v1's rows one to one")
    for m in M:
        t = theta[m["measurement_id"]]
        if t["theta_e_matches_v1"] != "yes" or float(t["theta_e_arcsec"]) != m[f"{X}theta_e_arcsec"]:
            raise SystemExit(f"θ_E of {m['measurement_id']} differs from the reading")

    # ------------------------------------------------------------------ observables (item 2)
    new_obs = []
    profile_obs = {}  # system_id -> new observable id (v2)
    next_n = len(O) + 1
    for p in profiles:
        rows = [m for m in M if m["measurement_id"] in p["applies_to_rows"].split(";")]
        if p["profile_status"] != "printed" or any(m[f"{X}r_eff_arcsec"] is not None for m in rows):
            continue
        if any(theta[m["measurement_id"]]["rule5_class"] != "A" for m in rows):
            continue  # item 2: only for class A rows
        oid = f"{PID}/o{next_n:06d}"
        next_n += 1
        paper = p["paper"].split(" (")[0]
        tex = p["location"].split("/x/")[-1]
        new_obs.append({
            "observable_id": oid, "system_id": p["system_id"], "side": "baryonic", "quantity": "half_light_radius",
            "value": float(p["r_e_arcsec"]), "err_lo": None, "err_hi": None, "unit": "arcsec", "band": None, "limit": "none",
            "steps": "photometry;structural_model", "evidence_tier": 1,
            "source_ref": f"{paper}: {p['table']} (e-print {p['location'].split('/x/')[0]}, {tex.replace(':', ' l. ')}; "
                          f"frozen second reading profiles.csv)",
            f"{X}parameter": f"{p['form']} ({p['n_stated_as']}) fit by {paper}, '{p['r_e_convention']}', {p['band_or_imaging']}; "
                             f"the profile behind M*(<R_E) (v2 item 6)",
            f"{X}role": "profile",
            f"{X}printed": f"{p['r_e_arcsec']} - + [linear; arcsec]",
        })
        profile_obs[p["system_id"]] = oid

    # ------------------------------------------------------------------ measurements
    out = []
    for m in M:
        mid1 = m["measurement_id"]
        t, p = theta[mid1], prof_of.get(mid1)
        cls = t["rule5_class"]
        obs_rec, st_rec = records(m["source_ref"])
        r = {k: v for k, v in m.items()}
        r["measurement_id"] = v2id(m["measurement_id"])
        r["alternative_of"] = v2id(m["alternative_of"])
        r["observed_from"] = ";".join(v2id(x) for x in m["observed_from"].split(";"))
        bf = [v2id(x) for x in m["baryonic_from"].split(";")]
        if m["system_id"] in profile_obs:
            bf.append(profile_obs[m["system_id"]])
        r["baryonic_from"] = ";".join(bf)
        r["assumptions"] = ";".join(m["assumptions"].split(";") + list(NEW_ASSUMPTIONS))
        notes = [m["notes"]] if m["notes"] else []
        flags = [f for f in (m["flags"] or "").split(";") if f]

        # item 5 / rule 5: class A rows carry the θ_E error on g_bar
        lower = t["err_kind"].strip() == "lower_bound"
        frac_lo = frac_hi = None
        if cls == "A":
            r["g_obs_err_lo"] = r["g_obs_err_hi"] = None
            if "no_uncertainty" not in flags:
                flags.append("no_uncertainty")
            notes.append(THETA_NOTE_A.format(term="theta_e_ngc6505" if lower else "theta_e"))
            if lower:
                notes.append(f"θ_E error a lower bound: \"{t['err_quote']}\" ({t['err_location'].split('/x/')[-1].replace(':', ' l. ')})")
            else:
                frac_lo, frac_hi = float(t["theta_e_err_frac_lo"]), float(t["theta_e_err_frac_hi"])
        if cls == "aperture" and m["model_dependence"] == "total_mass_form":
            notes.append(f"model_dependence total_mass_form: the mass is from full lens models evaluated inside R_ap "
                         f"(\"{t['me_def_quote']}\", {t['me_def_location'].split('/x/')[-1].replace(':', ' l. ')}), "
                         "not from the half-image-separation approximation (v2 reading, resolution 2)")
        r["flags"] = ";".join(flags) if flags else None

        # item 6: profile, exponent
        prof_form = prof_re = prof_n = None
        dl = None
        if p is not None and p["profile_status"] == "printed":
            re_, n_ = float(p["r_e_arcsec"]), float(p["n"])
            if m[f"{X}r_eff_arcsec"] is not None:
                if (m[f"{X}r_eff_arcsec"], m[f"{X}sersic_n"]) != (re_, n_):
                    raise SystemExit(f"{mid1}: profiles.csv differs from v1's profile columns")
            else:
                prof_form, prof_re, prof_n = p["form"], re_, n_
            dl = dlngbar_dlntheta(m[f"{X}theta_e_arcsec"], re_, n_)
        elif cls == "A":
            notes.append(NOT_COMPUTED)
        r["notes"] = "; ".join(notes) if notes else None

        # item 5: point columns and levels
        r["g_obs_err_point_lo"], r["g_obs_err_point_hi"] = r["g_obs_err_lo"], r["g_obs_err_hi"]
        r["g_bar_err_point_lo"], r["g_bar_err_point_hi"] = r["g_bar_err_lo"], r["g_bar_err_hi"]
        if any(e["source"] == st_rec and e["side"] == "g_bar" and e["v2_error_column"].startswith("g_bar_err_point")
               for e in err_rows):
            # the L error alone (R32 Table 2), propagated as v1 does (v1/convert.py: M* x hypot(dL/L, dU/U))
            obs = [obs_by_id[x] for x in m["baryonic_from"].split(";")]
            lum = [o for o in obs if o["quantity"] == "luminosity"]
            ml = [o for o in obs if o["quantity"] == "stellar_ml_population"]
            if len(lum) != 1 or len(ml) != 1:
                raise SystemExit(f"{mid1}: expected one luminosity and one M/L observable")
            lo, u = lum[0], ml[0]
            for side, e in (("lo", "err_lo"), ("hi", "err_hi")):
                a, b = (lo[e] or 0.0) / lo["value"], (u[e] or 0.0) / u["value"]
                r[f"g_bar_err_point_{side}"] = m[f"g_bar_err_{side}"] * a / math.hypot(a, b)
        if r["g_obs_err_lo"] is None and r["g_obs_err_hi"] is None:
            r["err_level"], r["err_level_status"] = None, None
        else:
            r["err_level"], r["err_level_status"] = level_of(err_rows, obs_rec, "g_obs", "g_obs_err_lo/hi")
        if r["g_bar_err_lo"] is None and r["g_bar_err_hi"] is None:
            r["g_bar_err_level"], r["g_bar_err_level_status"] = None, None
        else:
            r["g_bar_err_level"], r["g_bar_err_level_status"] = level_of(err_rows, st_rec, "g_bar", "g_bar_err")

        r[f"{X}theta_e_err_frac_lo"], r[f"{X}theta_e_err_frac_hi"] = frac_lo, frac_hi
        r[f"{X}theta_profile_form"], r[f"{X}theta_profile_r_e_arcsec"], r[f"{X}theta_profile_n"] = prof_form, prof_re, prof_n
        r[f"{X}dlngbar_dlntheta"] = dl
        r[f"{X}g_bar_stars_ref"] = m["g_obs"] * m[f"{X}mstar_re_msun"] / m[f"{X}m_e_msun"]
        for c, (sid, v) in SINGLE_SYSTEM_SIZES.items():
            r[c] = v if m["system_id"] == sid else None
        r_eff_err = None
        if m[f"{X}scope"] in SURVEY["SL2S"]:
            mm = re.search(r"imaging for r_eff_sl2s: [^;]*?\((0\.\d+)\)", p["note"])
            if not mm:
                raise SystemExit(f"{mid1}: no R_eff uncertainty in profiles.csv")
            r_eff_err = float(mm.group(1))
        r[f"{X}r_eff_err_frac"] = r_eff_err
        out.append(r)

    # ------------------------------------------------------------------ columns and descriptions
    acc = "m / s2"
    md = {c: (m1[c].description, m1[c].unit, (m1[c].meta or {}).get("ucd"), m1[c].dtype.kind) for c in m1.colnames}
    md["g_obs_err_lo"] = ("From the M_E error at fixed R_E. Empty on class A rows (standard §2a rule 7): there M_E is the mass "
                          "inside the radius of mean convergence 1, so g_obs = π G Σ_cr does not depend on θ_E; the θ_E error is "
                          "carried by g_bar through the term theta_e (or theta_e_ngc6505), and the row has the flag no_uncertainty",
                          m1["g_obs_err_lo"].unit, md["g_obs_err_lo"][2], "f")
    md["g_obs_err_hi"] = ("As g_obs_err_lo", m1["g_obs_err_hi"].unit, md["g_obs_err_hi"][2], "f")
    md["g_bar_err_lo"] = ("From the stellar-mass error only, at fixed R_E; the θ_E error is in the term theta_e (§2a rule 7). "
                          "On the two MaNGA lenses it also contains the shared Υ_ref, a dataset-scale term (upsilon_ref_manga)",
                          m1["g_bar_err_lo"].unit, md["g_bar_err_lo"][2], "f")
    md["g_bar_err_hi"] = ("As g_bar_err_lo", m1["g_bar_err_hi"].unit, md["g_bar_err_hi"][2], "f")
    md["assumptions"] = ("Registered assumptions (data/assumptions.json); a6s_theta_e and a6s_lens_distance added in v2 (item 7)", None, "meta.note", "U")
    md["flags"] = ("Core flags (data standard §11); no_uncertainty added in v2 on class A rows, whose g_obs carries no point error", None, "meta.code", "U")
    md["notes"] = ("Reasons not plotted, or what the alternative replaces; in v2 also the §2a rule 7 note on class A rows, the θ_E "
                   "lower-bound note, 'θ_E error stated; effect on g_bar not computed' where no light profile is printed, and the "
                   "corrected total_mass_form reason", None, "meta.note", "U")
    new = {
        "g_obs_err_point_lo": ("Point-scale g_obs error (§3): one value per lens, so equal to g_obs_err_lo; empty on class A rows", acc, "stat.error;phys.acceleration", "f"),
        "g_obs_err_point_hi": ("As g_obs_err_point_lo", acc, "stat.error;phys.acceleration", "f"),
        "g_bar_err_point_lo": ("Point-scale g_bar error (§3): equal to g_bar_err_lo, except on the two MaNGA lenses, where it is the "
                               "L_Ein error alone (R32), propagated as v1 does, because g_bar_err_lo there also contains the shared "
                               "Υ_ref, a dataset-scale term (upsilon_ref_manga; §2a rules 1 and 6)", acc, "stat.error;phys.acceleration", "f"),
        "g_bar_err_point_hi": ("As g_bar_err_point_lo", acc, "stat.error;phys.acceleration", "f"),
        "err_level": ("Confidence level of g_obs_err_*, as the source states it (frozen reading err_levels.csv); empty where the column is empty", None, "stat.confidenceLevel", "f"),
        "err_level_status": ("stated, or not_given_by_source (a level is never assumed, D-093 rule 1); empty where g_obs_err_* is empty", None, "meta.code", "U"),
        "g_bar_err_level": ("Confidence level of g_bar_err_*, as the source states it (frozen reading err_levels.csv); empty where the column is empty", None, "stat.confidenceLevel", "f"),
        "g_bar_err_level_status": ("stated, or not_given_by_source; empty where g_bar_err_* is empty", None, "meta.code", "U"),
        f"{X}theta_e_err_frac_lo": ("Fractional θ_E error (lower side) on class A rows, as printed (frozen reading theta_class.csv); companion of _hi. "
                                    "Empty outside class A, and on NGC 6505, whose lower bound is the term theta_e_ngc6505", None, "stat.error", "f"),
        f"{X}theta_e_err_frac_hi": ("Fractional θ_E error (upper side), as _lo. Size column of term theta_e (formula a6s_theta_e). Empty: no θ_E "
                                    "error of this kind is given for the row", None, "stat.error", "f"),
        f"{X}theta_profile_form": ("Light-profile form printed by the source (frozen reading profiles.csv), on rows whose v1 profile columns are "
                                   "empty; empty where none is printed or v1 already holds the profile", None, "meta.note", "U"),
        f"{X}theta_profile_r_e_arcsec": ("Effective radius of that profile, as printed; empty as for the form", "arcsec", "phys.angSize", "f"),
        f"{X}theta_profile_n": ("Sérsic index of that profile (4 = de Vaucouleurs); empty as for the form", None, "meta.number", "f"),
        f"{X}dlngbar_dlntheta": ("d ln g_bar / d ln θ_E at fixed redshifts and cosmology = −2 + d ln f(<R_E)/d ln R_E, from the printed profile "
                                 "(v1's columns or the theta_profile columns) by central difference (step 1e-4 in ln R_E) of the frozen "
                                 "aeg.lensing.sersic_projected_fraction. Exponent of the a6s_theta_e formula. Empty where no profile is "
                                 "printed: the θ_E effect on g_bar is not computed (D-104 rule 3)", None, "arith.factor", "f"),
        f"{X}g_bar_stars_ref": ("G M*(<R_E)/R_E² at the source's population, computed as g_obs × mstar_re_msun / m_e_msun. Read by the v2 "
                                "a6s_gas_in_RE formula, so that the gas term does not read g_obs", acc, "phys.acceleration", "f"),
        f"{X}mass_ellipticity_frac": ("Fractional increase of M_E from a small ellipticity, one-sided, upward (R29 l. 210); J0403−0239 only. "
                                      "Size column of term ellipticity_j0403 (in_error_columns = no). Empty: no size given", None, "stat.error", "f"),
        f"{X}los_frac": ("Line-of-sight effect on M_E as a fraction (R28 l. 320–322); SNL-0 only. Size column of term line_of_sight_snl0 "
                         "(in_error_columns = no). Empty: no size given", None, "stat.error", "f"),
        f"{X}neighbour_light_frac": ("Neighbour light as a fraction (R26 l. 141); SNL-2 only. Size column of term neighbour_light_snl2 "
                                     "(in_error_columns = no). Empty: no size given", None, "stat.error", "f"),
        f"{X}r_eff_err_frac": ("Fractional R_e error stated by R20 for the imaging of the row's R_e (0.30 CFHT, 0.10 HST; frozen reading "
                               "profiles.csv); SL2S rows only. Size column of term r_eff_sl2s (in_error_columns = no; effect not computed "
                               "in v2). Empty: no size given", None, "stat.error", "f"),
    }
    md.update(new)
    cols = list(m1.colnames)
    cols.insert(cols.index("g_obs_err_hi") + 1, "g_obs_err_point_lo")
    cols.insert(cols.index("g_obs_err_point_lo") + 1, "g_obs_err_point_hi")
    cols.insert(cols.index("g_bar_err_hi") + 1, "g_bar_err_point_lo")
    cols.insert(cols.index("g_bar_err_point_lo") + 1, "g_bar_err_point_hi")
    at = cols.index("g_bar_err_point_hi") + 1
    cols[at:at] = ["err_level", "err_level_status", "g_bar_err_level", "g_bar_err_level_status"]
    cols += [c for c in new if c not in cols]

    meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    meas = build(cols, out, md, meta)

    od = {c: (o1[c].description, o1[c].unit, (o1[c].meta or {}).get("ucd"), o1[c].dtype.kind) for c in o1.colnames}
    od["quantity"] = ("Data standard 2.5.1 §4a", None, "meta.code", "U")
    od["err_level"] = ("Confidence level of err_lo/err_hi as the source states it; not read for observables in v2 (empty): the "
                       "measurement columns carry the levels (frozen reading err_levels.csv)", None, "stat.confidenceLevel", "f")
    od["err_level_status"] = ("stated or not_given_by_source; empty where not read (all rows in v2)", None, "meta.code", "U")
    ocols = list(o1.colnames)
    ocols.insert(ocols.index("err_hi") + 1, "err_level")
    ocols.insert(ocols.index("err_level") + 1, "err_level_status")
    O2 = []
    for o in O:
        o = dict(o)
        o["observable_id"] = v2id(o["observable_id"])
        o["err_level"] = o["err_level_status"] = None
        O2.append(o)
    for o in new_obs:
        o["err_level"] = o["err_level_status"] = None
        O2.append(o)
    obs_t = build(ocols, O2, od, meta)

    sd = {c: (s1[c].description, s1[c].unit, (s1[c].meta or {}).get("ucd"), s1[c].dtype.kind) for c in s1.colnames}
    sys_t = build(list(s1.colnames), S, sd, meta)

    terms = build_terms(out, S, theta, distance, profiles, meta)

    (HERE / "tables").mkdir(exist_ok=True)
    for n, t in (("measurements", meas), ("observables", obs_t), ("systems", sys_t), ("uncertainty_terms", terms)):
        t.write(HERE / f"tables/{n}.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)

    # item 4 on the stored table: v1's frozen arithmetic, plus the two new computed columns
    back = v1c.read_back(HERE / "tables/measurements.ecsv")
    n4 = v1c.arithmetic_check(back)
    for r in back:
        ref = r["g_obs"] * r[f"{X}mstar_re_msun"] / r[f"{X}m_e_msun"]
        if abs(r[f"{X}g_bar_stars_ref"] / ref - 1) > 1e-12:
            raise SystemExit(f"item 4 failed at {r['measurement_id']}: g_bar_stars_ref")
        if r[f"{X}dlngbar_dlntheta"] is not None:
            re_ = r[f"{X}r_eff_arcsec"] if r[f"{X}r_eff_arcsec"] is not None else r[f"{X}theta_profile_r_e_arcsec"]
            n_ = r[f"{X}sersic_n"] if r[f"{X}sersic_n"] is not None else r[f"{X}theta_profile_n"]
            if abs(dlngbar_dlntheta(r[f"{X}theta_e_arcsec"], re_, n_) / r[f"{X}dlngbar_dlntheta"] - 1) > 1e-6:
                raise SystemExit(f"item 4 failed at {r['measurement_id']}: dlngbar_dlntheta")

    desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
    desc["x_baryon_inventory"] = list(desc["x_baryon_inventory"]) + black_hole_components(inventory)
    write_datapackage(HERE, desc, {"measurements": ("tables/measurements.ecsv", meas),
                                   "observables": ("tables/observables.ecsv", obs_t),
                                   "systems": ("tables/systems.ecsv", sys_t),
                                   "uncertainty_terms": ("tables/uncertainty_terms.ecsv", terms)})
    write_checksums(HERE)
    print(f"wrote {len(meas)} measurements, {len(obs_t)} observables ({len(new_obs)} new), {len(sys_t)} systems, "
          f"{len(terms)} uncertainty terms; item 4 passes ({n4} comparisons by v1's arithmetic_check on the stored table)")
    return 0


def black_hole_components(inv: list[dict]) -> list[dict]:
    """Item 9 (D-104 rule 2): the central black hole as two inventory components, from baryon_inventory.csv."""
    bh = [r for r in inv if r["component"] == "central black hole"]
    neg = [r for r in bh if r["status"] == "stated_negligible"]
    other = [r for r in bh if r["status"] != "stated_negligible"]

    def loc(r):
        return r["location"].split("/x/")[-1].replace(":", " l. ")
    return [
        {"component": "central black hole (SNELLS, MaNGA and NGC 6505 sources)", "status": "stated_negligible",
         "citation": "; ".join(f"{r['source']} ({r['systems']}): \"{r['quote'].strip()}\" ({loc(r)})" for r in neg)
                     + ". Not added to g_bar (D-104 rule 2): every quoted size comes from an M_BH–σ scaling of the lens's own "
                       "velocity dispersion (D-036 #6). R28 sizes it at 2 per cent of M_Ein (l. 693), a larger share of M*(<R_E). "
                       "Frozen v2 reading baryon_inventory.csv"},
        {"component": "central black hole (other sources)", "status": "not_addressed",
         "citation": "Not addressed by " + ", ".join(f"{r['source']} ({r['systems']})" for r in other if r["status"] == "not_addressed")
                     + ". " + " ".join(f"{r['source']} ({r['systems']}): {r['status'].replace('_', ' ')}: \"{r['quote'].strip()}\" "
                                       f"({loc(r)}); {r['note']}." for r in other if r["status"] != "not_addressed")
                     + " R26's black hole is part of its dynamical model, not of a lensing g_bar (v2 reading, resolution 6). "
                       "Frozen v2 reading baryon_inventory.csv"},
    ]


def build(cols: list[str], rows: list[dict], descs: dict, meta: dict) -> Table:
    out = []
    for c in cols:
        d, unit, ucd, kind = descs[c]
        data = [r.get(c) for r in rows]
        if kind == "f":
            col = MaskedColumn(np.array([np.nan if x is None else float(x) for x in data], dtype="f8"),
                               mask=[x is None for x in data], name=c, unit=unit, description=d)
        elif kind in "iu":
            col = MaskedColumn(np.array([int(x) for x in data], dtype="i8"), name=c, description=d)
        else:
            col = MaskedColumn(["" if x is None else str(x) for x in data], name=c, dtype=str, description=d)
        col.meta["ucd"] = ucd
        out.append(col)
    t = Table(out)
    t.meta = dict(meta)
    return t


def build_terms(M: list[dict], S: list[dict], theta: dict, distance: list[dict], profiles: list[dict], meta: dict) -> Table:
    """Item 7: exactly the 44 rows of the frozen table."""
    order = [s["system_id"] for s in S]
    with_rows = [sid for sid in order if any(m["system_id"] == sid for m in M)]

    def sids(*names: str) -> list[str]:
        scopes = [sc for n in names for sc in SURVEY[n]]
        hit = {m["system_id"] for m in M if m[f"{X}scope"] in scopes}
        return [sid for sid in order if sid in hit]

    def lst(*names: str) -> str:
        return ";".join(sids(*names))

    def except_(*names: str) -> str:
        drop = set(sids(*names))
        return ";".join(s for s in with_rows if s not in drop)

    def one(name: str) -> str:
        s = sids(name)
        if len(s) != 1:
            raise SystemExit(f"{name}: expected one system")
        return s[0]

    # cross-checks of the stated sizes against the frozen reading (item 7)
    def dist(source: str, item: str) -> str:
        r = [x for x in distance if x["source"] == source and x["item"] == item]
        if len(r) != 1:
            raise SystemExit(f"distance.csv: no single row {source} {item}")
        return r[0]["value"]
    assert dist("R25", "alternative H0") == "67"
    assert dist("R29", "adopted H0") == "70.4" and dist("P15", "abstract headline H0") == "67.8"
    assert dist("P18", "abstract headline H0") == "67.4" and dist("B14", "abstract headline H0") == "69.6"
    assert dist("R26", "peculiar velocity").startswith("3-4%")
    ngc = [t for t in theta.values() if t["err_kind"].strip() == "lower_bound"]
    lb = {float(t["theta_e_err_frac_hi"]) for t in ngc}
    if len(lb) != 1 or {t["system_id"] for t in ngc} != {one("NGC 6505")}:
        raise SystemExit("theta_class.csv: the lower-bound θ_E rows are not exactly NGC 6505's")
    lb = lb.pop()

    T = []

    def t(term_id, scale, applies, moves, status, assumption=None, citation=None, locator=None, note="", in_err=None, **size):
        T.append({"term_id": term_id, "scale": scale, "applies_to": applies, "moves": moves, "status": status,
                  "size_value": size.get("size_value"), "size_lo": size.get("size_lo"), "size_hi": size.get("size_hi"),
                  "size_unit": size.get("size_unit"), "size_column": size.get("size_column"), "size_kind": size.get("size_kind"),
                  "assumption_id": assumption, "correlated_with": None, "covariance": "not_published",
                  "citation": citation, "locator": locator, "note": note, "in_error_columns": in_err})

    t("theta_e", "point", "*", "g_bar", "given", "a6s_theta_e",
      "R5 (Bolton et al. 2008); R20 (Sonnenfeld et al. 2013a); R32 (Smith et al. 2020); R29 (Collier, Smith & Lucey 2018b)",
      "R5 ms_arxiv.tex l. 972–975; R20 sl2s-rm-pdflatex.tex l. 462, 477–478; R32 main.tex l. 176, l. 261; R29 newlens.tex l. 196",
      "§2a rule 7, class A rows only (rule 5); the column is empty elsewhere, including NGC 6505. Moves g_bar and the coordinate R_E; "
      "g_obs = π G Σ_cr is unchanged. Two-sided: x_strong_lensing_theta_e_err_frac_lo holds the other side. SLACS: R5's adopted "
      "\"2% RMS fractional error\" (ms_arxiv.tex l. 972–975), no level stated (\"RMS\" names a statistic, not a confidence level); "
      "R13 used \"a conservative 5%\" for its lensing masses only (plain.txt l. 1669–1671); R13 does not state that its M* errors "
      "include the θ_E error (v2 reading). R9 0.5 % (ms_v2.tex l. 138) and SL2S's 3 % in this note (F3). SL2S: R20's 68 % intervals "
      "including its 3 % systematic (sl2s-rm-pdflatex.tex l. 462, 477–478). MaNGA: R32 l. 176 and l. 261 (J1701: 10 per cent as "
      "stated; Table 1 prints 1.63 ± 0.16). J0403: ±0.03″ of 1.47″ (R29 l. 196). The a6s_theta_e formula is first order in ln θ_E; "
      "at J1701's 10 % the second-order term is not computed, and where no light profile is printed the effect on g_bar is not "
      "computed (D-104 rule 3)",
      size_column=f"{X}theta_e_err_frac_hi", size_kind="as_released", size_unit="fraction")
    t("theta_e_ngc6505", "point", one("NGC 6505"), "g_bar", "given", "a6s_theta_e", "R30 (O'Riordan et al. 2025)", "ms.tex l. 798; θ_E l. 813",
      "0.001″ of 2.500″. \"should therefore be considered lower-bounds which only account for measurement uncertainty\" (R30 ms.tex "
      "l. 798; θ_E l. 813). The θ_E effect is not computed where no profile is printed (rule 5)",
      size_value=lb, size_kind="lower_bound", size_unit="fraction")
    t("ellipticity_j0403", "point", "*", "g_obs", "given", None, "R29 (Collier, Smith & Lucey 2018b)", "newlens.tex l. 210",
      "One-sided, upward; J0403−0239 only. \"Including a small ellipticity (e ≈ 0.1 as measured from galfit) increases the mass by "
      "3 per cent\" (R29 newlens.tex l. 210); a change in M_E at fixed radius. R29's revised \"∼4 per cent\" total is not used, to "
      "avoid counting the 2 % θ_E part twice", in_err="no",
      size_column=f"{X}mass_ellipticity_frac", size_kind="as_released", size_unit="fraction")
    t("lens_model_profile", "dataset", except_("SNELLS"), "g_bar", "not_given_by_source", "a6s_theta_e",
      "R5; R9; R30", "R5 l. 843–848; R9 l. 398–400; R30 §4.3, l. 798, l. 778",
      "Changes the fitted θ_E, so it moves g_bar and R_E (F1): \"the Einstein radius parameter … becomes somewhat dependent on the "
      "assumed mass model\" for asymmetric images (R5 l. 843–848); slope effects (R9 l. 398–400). NGC 6505: R30 §4.3, where the model "
      "systematic dominates the stated lower bounds but is not sized (l. 798); M_E printed without error (l. 778). Not SNL-0, whose "
      "SIS-against-MFL difference is already in its g_obs error (class B), and not SNL-1 or SNL-2 (apertures)")
    t("sie_axis_convention", "dataset", lst("SLACS", "S4TM"), "g_bar", "not_given_by_source", "a6s_theta_e", "R9 (Shu et al. 2015)", "ms_v2.tex l. 117",
      "Both use the b_SIE intermediate-axis convention (R9 ms_v2.tex l. 117). R9's \"accurate to < 1%\" is the accuracy of Huterer's "
      "conversion relation, not the size of the convention difference")
    t("external_shear", "dataset", lst("S4TM"), "g_bar", "given", "a6s_theta_e", "R9 (Shu et al. 2015); R10 (Shu et al. 2017)", "R9 l. 388; R10 l. 308–309",
      "R9 compares \"the resulted Einstein radii\" with and without shear: \"The overall fractional discrepancy is on the level of 2%\" "
      "(R9 l. 388); \"about 4%\" in mocks. R10 omits shear \"as quantified in Shu15\" (R10 l. 308–309)",
      size_value=0.02, size_kind="as_released", size_unit="fraction")
    t("external_convergence", "dataset", except_("SNL-0"), "g_obs", "not_given_by_source", None, "R9 (Shu et al. 2015)", "l. 386",
      "Changes M_E at a fixed radius: \"no more than a few percent\" (R9 l. 386). SNL-0's is the next row")
    t("line_of_sight_snl0", "point", "*", "g_obs", "given", None, "R28 (Smith & Lucey 2013), citing Taruya et al. 2002", "lensz_arXiv.tex l. 320–322",
      "SNL-0 only. in_error_columns = no (the validator requires point and given for that form; R28 states the size itself, citing "
      "Taruya et al. 2002). \"∼2 per cent for a z = 2 source (Taruya et al. 2002)\" (R28 l. 320–322)", in_err="no",
      size_column=f"{X}los_frac", size_kind="as_released", size_unit="fraction")
    t("lens_light_subtraction", "dataset", lst("S4TM"), "g_bar", "not_given_by_source", "a6s_theta_e", "R10 (Shu et al. 2017)", "l. 290–292",
      "The B-spline foreground subtraction \"could introduce some systematic uncertainties in the lens and source parameters\" (R10 l. 290–292)")
    t("aperture_radius_snl12", "dataset", lst("SNL-1", "SNL-2"), "both", "not_given_by_source", None,
      "R61 (Collier, Smith & Lucey 2018)", "Table 1, l. 151 and l. 155",
      "R_ap against the HST half-separation: 2.38″ and 2.21″ (R61 Table 1, l. 151; the test's \"Table 2\" is Table 1, v2 reading "
      "3.3) against 2.43 ± 0.03″ and 2.30 ± 0.03″ (l. 155); a difference, not an error")
    t("companion_snl2", "point", one("SNL-2"), "g_obs", "not_given_by_source", None, "R61 (Collier, Smith & Lucey 2018)", "l. 317",
      "\"tension between the measured and predicted flux ratios\" (R61 l. 317); SLC15's 8–16 % superseded")
    t("redshift_measurement", "dataset", except_("NGC 6505"), "both", "not_given_by_source", None, "the sources of each row", "",
      "No redshift errors printed except R30 (rows below)")
    t("redshift_lens_ngc6505", "point", one("NGC 6505"), "g_obs", "given", None, "R30 (O'Riordan et al. 2025)", "ms.tex l. 639",
      "z_l (R30 l. 639); effect not computed in v2", size_value=0.00003, size_kind="as_released", size_unit="redshift")
    t("redshift_source_ngc6505", "point", one("NGC 6505"), "g_obs", "given", None, "R30 (O'Riordan et al. 2025)", "ms.tex l. 698",
      "z_s (R30 l. 698); effect not computed in v2", size_value=0.003, size_kind="as_released", size_unit="redshift")
    t("cosmology_h0", "dataset", lst("SLACS", "S4TM", "SL2S", "NGC 6505"), "g_obs", "not_given_by_source", "a6s_source_cosmology",
      "R5; R13; R10; R20; R30", "frozen reading distance.csv",
      "Exact formula a6s_source_cosmology (g_obs ∝ H0 at fixed Ω_m; D-094). These sources test no alternative H0")
    t("cosmology_h0_snells", "dataset", lst("SNELLS"), "g_obs", "given", "a6s_source_cosmology",
      "R25 (Smith, Lucey & Conroy 2015)", "snellsI_arxiv.tex l. 862–863; l. 188",
      "p = 67/70, from the term's own pair (applying D-094/D-104). \"Adopting $H_0$ = 67 … from the Planck cosmology (Planck "
      "Collaboration 2014), rather than … 70 … from WMAP7\" (R25 snellsI_arxiv.tex l. 862–863). R25 adopts 70.4 (l. 188); the pair "
      "is R25's own comparison, 67 against 70 (v2 reading, resolution 5). v1's rows carry 70.4 (WMAP7, R28 and R61), which does "
      "not enter p. In α: \"would yield smaller α by ∼5 per cent\" (l. 863)",
      size_lo=67.0, size_hi=70.0, size_kind="range", size_unit="km s-1 Mpc-1")
    t("cosmology_h0_j0403", "dataset", one("J0403"), "g_obs", "given", "a6s_source_cosmology",
      "R29 (Collier, Smith & Lucey 2018b); Planck Collaboration 2016, A&A 594, A13 (arXiv 1502.01589)", "newlens.tex l. 210, l. 241",
      "p = 67.8/70.4 (applying D-094/D-104). Adopted 70.4 (R29 l. 210). Alternative: \"If we had prescribed the [Planck Collaboration "
      "2016] cosmology\" (l. 241); that paper is A&A 594, A13 (arXiv 1502.01589), whose abstract gives \"H0= (67.8 +/- 0.9) km/s/Mpc\". "
      "In α: \"4 per cent lower, due to the variation in H0\" (l. 241)",
      size_lo=67.8, size_hi=70.4, size_kind="range", size_unit="km s-1 Mpc-1")
    t("cosmology_h0_manga", "dataset", lst("MaNGA"), "g_obs", "given", "a6s_source_cosmology",
      "R32 (Smith et al. 2020); Planck Collaboration 2018 (arXiv 1807.06209); Bennett et al. 2014, ApJ 794, 135 (arXiv 1406.1718)",
      "main.tex l. 100–101, l. 293",
      "p = 69.6/67.4 (applying D-094/D-104). Adopted: \"We adopt the cosmological parameters from\" Planck Collaboration 2018 (R32 "
      "main.tex l. 100–101); arXiv 1807.06209 abstract: \"$H_0 = (67.4\\pm 0.5)$km/s/Mpc\". Alternative: Bennett et al. 2014 (l. 293); "
      "arXiv 1406.1718 abstract: \"69.6+/-0.7 km/s/Mpc\". v1's MaNGA rows have no x_strong_lensing_h0, which does not enter p. In α: "
      "\"would increase α by 3.5 per cent\" (l. 293)",
      size_lo=67.4, size_hi=69.6, size_kind="range", size_unit="km s-1 Mpc-1")
    t("cosmology_omega_m", "dataset", "*", "g_obs", "not_given_by_source", None, "each row's observed-side source", "x_strong_lensing_om",
      "Ω_m as stated per source (x_strong_lensing_om); flags cosmology_named_only, flatness_not_stated as v1")
    for name in ("SNL-0", "SNL-1", "SNL-2"):
        tid = "lens_distance_" + name.lower().replace("-", "")
        note = ("\"an uncertainty corresponding to a 500 km s⁻¹ peculiar velocity (3-4%)\" (R26 snells.tex l. 139), stated for the "
                "lensing M/L, which R26 states is proportional to distance; applied as a shift of ±size_hi in D_l (a6s_lens_distance, "
                "which assumes D_s ≫ D_l). In α: \"up to 5 per cent\" (R25 l. 864)") if name == "SNL-0" else \
               "As SNL-0 (R26 l. 139 covers the three SNELLS lenses of its Table 1)"
        if name == "SNL-0":
            note += ("; R28: \"rescaling the distance assumed for [ESO 325-G004] affects $\\alpha_{\\rm MW}$ linearly\" "
                     "(lensz_arXiv.tex l. 727–730), an α statement (v2 reading)")
        t(tid, "system", one(name), "g_obs", "given", "a6s_lens_distance", "R26 (Newman et al. 2017)", "snells.tex l. 139", note,
          size_lo=0.03, size_hi=0.04, size_kind="as_released", size_unit="fraction of D_l")
    t("lens_distance_ngc6505", "system", one("NGC 6505"), "g_obs", "given", "a6s_lens_distance", "R30 (O'Riordan et al. 2025)", "ms.tex l. 639; l. 790",
      "z 0.04243 (spectroscopic, l. 639) against 0.041 ± 0.001 (cosmological). \"On top of the bulk flow peculiar velocities of "
      "individual galaxies are typically present at the $150\\,\\kms$ level. Combining these two effects results in a cosmological "
      "redshift of $z=0.041\\pm0.001$\" (R30 ms.tex l. 790). R30 does not state which one it uses for distances (v2 reading 3.7). "
      "Effect not computed in v2 (applying D-094/D-104). v1's alternative row (z = 0.041) stays as it is",
      size_lo=0.040, size_hi=0.04243, size_kind="range", size_unit="redshift")
    t("lens_distance_other", "dataset", except_("SNELLS", "NGC 6505"), "g_obs", "not_given_by_source", "a6s_lens_distance",
      "the sources of each row", "frozen reading distance.csv", "No peculiar-velocity or frame effect stated")
    t("aperture_factor_slacs", "dataset", lst("SLACS"), "g_bar", "not_given_by_source", None, "R13 (Grillo et al. 2009)", "plain.txt l. 1701–1705",
      "\"⟨f_ap⟩ = 0.36 ± 0.01\" is a sample mean (R13 l. 1701–1705); \"the stellar mass is traced by the light distribution\"")
    t("r_eff_slacs", "dataset", lst("SLACS"), "g_bar", "given", None, "R5 (Bolton et al. 2008)", "l. 1072–1076",
      "R_e error adopted by R5 (l. 1072–1076); its effect through f(<R_E) is not computed in v2",
      size_value=0.035, size_kind="as_released", size_unit="fraction")
    t("r_eff_sl2s", "point", "*", "g_bar", "given", None, "R20 (Sonnenfeld et al. 2013a)", "sl2s-rm-pdflatex.tex l. 354–359",
      "SL2S rows only: CFHT R_e 0.30, HST R_e 0.10, by the imaging of each row's R_e (the frozen reading records both SL2S lenses with "
      "HST imaging; the CFHT R_e is v1's default, the HST R_e its alternative). R20 l. 354–359; effect not computed in v2",
      in_err="no", size_column=f"{X}r_eff_err_frac", size_kind="as_released", size_unit="fraction")
    t("r_eff_s4tm", "dataset", lst("S4TM"), "g_bar", "not_given_by_source", None, "R10 (Shu et al. 2017)", "l. 386",
      "No R_e error printed (R10 l. 386)")
    t("sps_templates_slacs", "dataset", lst("SLACS"), "g_bar", "not_given_by_source", None, "R13 (Grillo et al. 2009)", "l. 914–916, 1060–1064",
      "solar-metallicity, dust-free templates (R13 l. 914–916, 1060–1064); Maraston pair kept as alternatives")
    t("sps_systematic_s4tm", "dataset", lst("S4TM"), "g_bar", "given", None, "R9 (Shu et al. 2015)", "l. 424–425",
      "\"around 0.5 dex\" between the lower- and upper-bound models (R9 l. 424–425)",
      size_value=0.5, size_kind="as_released", size_unit="dex")
    t("sps_template_sl2s", "dataset", lst("SL2S"), "g_bar", "given", None, "R20 (Sonnenfeld et al. 2013a)", "l. 740",
      "R20 l. 740; bias 0.01 dex", size_value=0.06, size_kind="as_released", size_unit="dex")
    t("luminosity_corrections_manga", "dataset", lst("MaNGA"), "g_bar", "not_given_by_source", None, "R32 (Smith et al. 2020)", "l. 270–272",
      "extinction, band-shift and PSF corrections carry no stated error (R32 l. 270–272; F5)")
    t("upsilon_ref_manga", "dataset", lst("MaNGA"), "g_bar", "given", None, "R32 (Smith et al. 2020)", "main.tex l. 276–277",
      "\"The full range in Υ_ref spanned by these models is 2.41–3.46; our calculations adopt this as the 2σ interval\" (R32 l. 276–277). "
      "One value for both lenses (F4); left out of g_bar_err_point_*",
      size_lo=2.41, size_hi=3.46, size_kind="range", size_unit="solar units (M☉/L☉)")
    t("pop_model_family_j0403", "system", one("J0403"), "g_bar", "not_given_by_source", None, "R29 (Collier, Smith & Lucey 2018b)", "l. 241",
      "Stated only in α, which subtracts a modelled mass, so it is not a g_bar size (D-104 rule 1's reason; applying D-094/D-104). "
      "In α: Maraston models: \"α would increase by 10 per cent\" (R29 l. 241)")
    t("pop_age_j0403", "system", one("J0403"), "g_bar", "not_given_by_source", None, "R29 (Collier, Smith & Lucey 2018b)", "l. 241",
      "As above. In α: 8.5 Gyr: \"α would have increased by 14 per cent\" (R29 l. 241)")
    t("pop_model_family_manga", "dataset", lst("MaNGA"), "g_bar", "not_given_by_source", None, "R32 (Smith et al. 2020)", "l. 293",
      "As above. In α: \"using Maraston models for Υ_ref would increase α by ∼12 per cent\" (R32 l. 293)")
    t("alpha_fe", "dataset", "*", "g_bar", "not_given_by_source", None, "SLC15; SL13", "",
      "SLC15 \"∼4 per cent\" in J-band Υ; SL13 2–3 % in I-band; not for the bands v1 uses")
    t("stellar_imf", "dataset", "*", "g_bar", "given", "a6s_stellar_imf", "v1 slider (D-075 item 5; D-076 item 2)", "",
      "v1's slider, unchanged. Lower end: the printed Chabrier/Kroupa value; upper end in x_strong_lensing_mstar_top_msun",
      size_column=f"{X}mstar_top_msun", size_kind="range", size_unit="solMass")
    t("gas_in_re", "dataset", "*", "g_bar", "given_by_other_source", "a6s_gas_in_RE", "D-076 item 1 (gas_term.json)", "R28 l. 496; R25 l. 769; R32 l. 274",
      "v1's registered term (D-076 item 1); the sources call gas negligible (R28 l. 496; R25 l. 769; R32 l. 274). Hot fraction maximum "
      "in x_strong_lensing_gas_hot_frac_max, cold in x_strong_lensing_gas_cold_frac_max",
      size_column=f"{X}gas_hot_frac_max", size_kind="range", size_unit="fraction of M*(<R_E)")
    t("neighbour_light_snl2", "point", "*", "g_bar", "given", None, "R26 (Newman et al. 2017)", "snells.tex l. 141",
      "SNL-2 only. \"only 1.5%, a minor effect that we neglect\" (R26 l. 141)", in_err="no",
      size_column=f"{X}neighbour_light_frac", size_kind="as_released", size_unit="fraction")
    t("internal_dust_snl1", "point", one("SNL-1"), "g_bar", "not_given_by_source", None, "R61 (Collier, Smith & Lucey 2018)", "l. 313",
      "R61 l. 313")
    t("lensed_source_light", "dataset", "*", "g_bar", "not_given_by_source", None, "R13 (Grillo et al. 2009)", "",
      "\"not affected in any significant way\" (R13)")
    t("solar_magnitude", "dataset", "*", "g_bar", "not_given_by_source", None, "each stellar-side source", "",
      "4.066 (F814W), 4.64 (r, AB), 4.534 and 4.53 (i), as each source states")
    t("aperture_shape", "dataset", "*", "both", "not_given_by_source", None, "R13 (Grillo et al. 2009)", "l. 1646–1651",
      "circular disk for M* against the SIE's elliptical critical curve, \"expressed as in an 'effective' axisymmetric model\" "
      "(R13 l. 1646–1651)")
    if len(T) != 44:
        raise SystemExit(f"item 7: {len(T)} term rows, expected 44")
    cols = ["term_id", "scale", "applies_to", "moves", "status", "size_value", "size_lo", "size_hi", "size_unit", "size_column",
            "size_kind", "assumption_id", "correlated_with", "covariance", "citation", "locator", "note", "in_error_columns"]
    num = {"size_value", "size_lo", "size_hi"}
    descs = {c: (c, None, "meta.note", "f" if c in num else "U") for c in cols}
    return build(cols, T, descs, meta)


if __name__ == "__main__":
    sys.exit(main())
