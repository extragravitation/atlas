"""Convert the A6 strong-lensing inputs into the Atlas data standard 2.1.0.

Usage
    python -m aeg.fetch data/packages/aeg-d-strong-lensing/v1     (first: the released files)
    python data/packages/aeg-d-strong-lensing/v1/convert.py
        Real conversion. Skips (exit 0, nothing written) until the gas term is set: the file
        gas_term.json beside this script, written only after JvH ruled on the gas default and
        range (D-075 item 1; ruled D-076 item 1). AEG_REGISTER=1 once, by the maintainer, adds new
        systems to data/registry/systems.csv, as aeg-d-dwarfs/v1 does.
    python .../convert.py --synthetic-gas --inputs SYNTHETIC.csv --out DIR
        Synthetic tests only. Uses a made-up gas term labelled SYNTHETIC, accepts only an input
        file whose every row has a scope beginning "SYNTHETIC", never the real inputs, never
        touches the registry, and writes only into DIR, which must lie outside this package.

Rules applied (nothing beyond them):
    REPRODUCTION.md (frozen, D-065); docs/methods/A6S_PRECEDENCE.md (frozen, D-065);
    D-063, D-064, D-066, D-075 (rulings on reading/adjudication.md Q1-Q14) and D-076.

Inputs (values transcribed from printed or released tables, read twice and adjudicated):
    reading/adjudicated_inputs.csv       the A6 inputs (adjudication.md)
    reading/adjudicated_supplement.csv   the supplement (gas/adjudication_gas.md §1): R29 cosmology,
                                         SNL-1 via R61 (D-076 item 3; second reading in
                                         reading/readings/second-reader-r61-snl1.csv), R13 totals and
                                         light profiles and R7 M_E (reported checks only), the printed
                                         Salpeter conversions
    gas_term.json                        the ruled gas term (D-076 item 1)
    source/                              the released tier-1 files of sources.json (VizieR, IOP): every
                                         tier-1 number used is found in its system's row of the
                                         released file before anything is written

Per system, in projection at the Einstein radius (D-064):
    M_E       printed by the default record; where only theta_E is printed,
              M_E = theta_E^2 c^2 D_s D_l / (4 G D_ls) in the source's cosmology (aeg.lensing)
    R_E       theta_E D_l in the same cosmology (aeg.lensing); R32 prints R_E in kpc and names its
              cosmology only, so the printed R_E is used (D-075 item 4, flag R_E_printed_kpc)
    M*(<R_E)  printed inside R_E; or L(<R_E) x population M/L (D-075 item 3, mstar_from_L_times_ML);
              or total x f(<R_E) from the source's own de Vaucouleurs / Sersic fit
              (aeg.lensing.sersic_projected_fraction; flag mstar_in_RE_from_profile)
    IMF top   the Salpeter value printed by the same source (SLACS R13 Salpeter-BC03, D-075 item 5;
              SL2S R20's own Salpeter masses, D-076 item 2); else the source's printed conversion
              (R29 alpha = 1.55, R32 alpha ~ 1.65, R30 / 0.61); for S4TM R30's printed FSPS factor
              (Chabrier / 0.61, D-076 item 2, flag salpeter_top_from_other_source_same_model_family);
              else none (flag imf_top_not_read)
    M_gas     the registered gas term (gas_term.json): per component f_c x M*(<R_E) at the default
              IMF, never derived from the observed side
    g_obs     G M_E / R_E^2,  g_bar = G (M* + M_gas) / R_E^2  (aeg.lensing.projected_acceleration),
              labelled projected (r_kind = projected, x_strong_lensing_projection = projected)
    errors    g_obs from the M_E error, g_bar from the stellar-mass error, both at fixed R_E
              (the radius is the coordinate; distance errors are not added, REPRODUCTION.md).

Reported checks (written to checks/, not pass/fail), computed only on a real run:
    formula_check.ecsv   REPRODUCTION.md "Reported" item 1 / A6S_PRECEDENCE §4: M_E from theta_E by
                         the §2.4 formula against the printed M_E, wherever one system has both
                         (R7's printed M_E for R5's models; R10; R28; R29; R30).
    profile_step.ecsv    D-075 item 5: the profile step on R13's printed totals against R13's printed
                         masses inside R_E.
    overlap.csv          systems in more than one survey's default, side by side (none averaged).
    not_tabulated.csv    systems in the reading files that cannot enter the systems table, with why.

Epoch gap (D-066 item 2): every lens read in the scopes at printed z_l >= 0.30 is recorded in the systems
table straight from the two readings (reading/readings/reader-{a,b}-block{1,2,3}.csv; not adjudicated), with
plotted = false, the reason "z_l >= 0.30 (D-066)" and the flag epoch_gap_v1; readers_differ where the two
readings differ (both kept). No measurement or observable rows. See epoch_gap_lenses().
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))
from aeg import lensing as L  # noqa: E402  (frozen; used, never edited)

DATASET, VERSION, STANDARD = "aeg-d-strong-lensing", "v1", "2.1.0"
PID = f"{DATASET}/{VERSION}"
X = "x_strong_lensing_"  # extension-column prefix (data standard §12)
TODAY = "2026-11-01"
INPUTS = HERE / "reading/adjudicated_inputs.csv"
SUPPLEMENT = HERE / "reading/adjudicated_supplement.csv"
GAS_TERM_FILE = HERE / "gas_term.json"
FROZEN = ROOT / "data/frozen/a6s-reproduction.json"
Z_CUT = 0.30  # D-066: printed lens redshift below 0.30 exactly
TOL = 1e-9  # REPRODUCTION.md test 3

REFUSAL = (
    "REFUSED: the gas term inside R_E is not set.\n"
    "D-075 item 1: no A6 point is plotted until the gas term rests on a quoted literature measurement,\n"
    "with a registered default and range ruled by JvH. Write gas_term.json beside convert.py only\n"
    "after that ruling (see GasTerm in convert.py for its fields). Nothing was computed or written."
)

# Core flags (data standard §11); everything else goes to x_strong_lensing_flags.
CORE_FLAGS = {"no_uncertainty"}
IMF_ID = "a6s_stellar_imf"
METHOD_ASSUMPTIONS = ("a6s_gr_lensing", "a6s_source_cosmology", "a6s_projected_cylinder",
                      "a6s_redshifts_spectroscopic", "a6s_mstar_population", IMF_ID, "a6s_mstar_profile")

# Slider effects (registered in data/assumptions.json; checked by aeg.formula_check in Python and JS).
# IMF: p = 0 Chabrier/Kroupa default, p = 1 Salpeter top (A6S_PRECEDENCE §3.2).
_K = f"({X}mstar_top_msun / {X}mstar_re_msun - 1)"
IMF_EFFECTS = [
    {"column": "g_bar_stars", "formula": f"g_bar_stars * (1 + {_K} * p)"},
    {"column": "g_bar_err_lo", "formula": f"g_bar_err_lo * (1 + {_K} * p)"},
    {"column": "g_bar_err_hi", "formula": f"g_bar_err_hi * (1 + {_K} * p)"},
    {"column": "g_bar", "formula": f"g_bar + g_bar_stars * {_K} * p"},
]
# Gas: p = -1 registered minimum, 0 default, +1 maximum, per component as a fraction of M*(<R_E) at the
# default IMF. G M*(<R_E) / R_E^2 at the default IMF is g_obs * M*(<R_E) / M_E (same R_E), so the gas
# does not move with the IMF slider.
_STARS0 = f"g_obs * {X}mstar_re_msun / {X}m_e_msun"


def _gas_frac(c: str) -> str:
    f, lo, hi = f"{X}{c}_frac", f"{X}{c}_frac_min", f"{X}{c}_frac_max"
    return f"({f} + ({hi} - {lo}) / 2 * p + ({hi} + {lo} - 2 * {f}) / 2 * abs(p))"


GAS_EFFECTS = [
    {"column": "g_bar_gas_hot", "formula": f"{_STARS0} * {_gas_frac('gas_hot')}"},
    {"column": "g_bar_gas_cold", "formula": f"{_STARS0} * {_gas_frac('gas_cold')}"},
    {"column": "g_bar", "formula": f"g_bar - g_bar_gas_hot - g_bar_gas_cold + {_STARS0} * "
                                   f"({_gas_frac('gas_hot')} + {_gas_frac('gas_cold')})"},
]

# D-075 item 4 conventions, per record, as read at source (adjudication.md §3b).
COSMOLOGY_CONVENTION = {
    "R30": "flatness_not_stated",      # prints H0 and Omega_m only; taken as flat
    "R32": "cosmology_named_only",     # "Planck Collaboration et al. (2018)", no numbers
    "R26": "cosmology_by_reference",   # adopts R25's (S15) distances
}
# D-075 item 4: R5's stated survey-wide adopted error on theta_E (R5 Table 3; §6.1).
SAMPLE_LEVEL_ERROR = {("R5", "theta_E"): 0.02}
# Redshift measured spectroscopically by the source although the row note does not say the word
# (adjudication.md §2 "MNELLS z_s" and §4 table: R29 measured both redshifts with MUSE).
SPEC_Z_BY_SOURCE = {"R29": "MUSE measurement (adjudication.md §2, §4)"}
# Records that print a fit as de Vaucouleurs (n = 4) in the row note.
DEVAUC = re.compile(r"de Vaucouleurs", re.I)
IMF_WORDS = ("Chabrier", "Kroupa", "Salpeter")
# D-076 item 2: the S4TM Salpeter top is R30's printed FSPS conversion (gas/adjudication_gas.md §6, option S-a):
# R30 §3.1 "rescale these quantities by dividing them with a constant factor of 0.61".
SALPETER_FROM_OTHER_SOURCE = {"R10": "R30"}
# D-075 item 1 (Q14) / D-076 item 1: systems whose sources state gas inside R_E negligible. They take the
# registered gas term; the source statements are kept as quoted source assumptions (adjudication.md §5).
GAS_SOURCE_NEGLIGIBLE = {
    "ESO 325-G004": "R28 footnote 3; R25 §4",
    "ESO 286-G022": "R25 §4",
    "2MASX J01414232-0735281": "R25 §4",
    "SDSS J1436+4943": "R32 §5",
    "SDSS J1701+3722": "R32 §5",
}
# Supplement scope holding R7 rows of lenses outside the SLACS V adjudicated set (record-only, B's Q2).
R7_ONLY_SCOPE = "SLACS (R7 Table 4, not in the SLACS V adjudicated set)"


class Refused(SystemExit):
    """Raised to stop without writing anything."""


# ----------------------------------------------------------------------------- gas term
@dataclass(frozen=True)
class GasComponent:
    name: str  # "gas_cold" or "gas_hot" (data standard §3 columns g_bar_gas_cold, g_bar_gas_hot)
    default: float
    minimum: float
    maximum: float


@dataclass(frozen=True)
class GasTerm:
    """The gas inside R_E, as M_gas,c(<R_E) = f_c x M*(<R_E) at the default IMF, per component.

    Required fields of gas_term.json:
        assumption_id   registry id (e.g. "a6s_gas_in_RE")
        decision        the decision-log entry that ruled it (D-076 item 1)
        form            "fraction_of_mstar_in_RE" (the only form coded; others need new code)
        components      {"gas_cold": {"default", "min", "max"}, "gas_hot": {...}}, at least one
        ref             where the default and range were read (citation and location)
        source_negligible   "zero" or "registered": what the systems whose sources state gas
                        negligible (R28, R25, R32; D-075 item 1) take. No default: it is ruled.
    """
    assumption_id: str
    decision: str
    form: str
    components: tuple[GasComponent, ...]
    ref: str
    source_negligible: str
    synthetic: bool = False


def parse_gas_term(d: dict, synthetic: bool = False) -> GasTerm:
    missing = [k for k in ("assumption_id", "decision", "form", "components", "ref", "source_negligible") if not d.get(k)]
    if missing:
        raise Refused(f"REFUSED: gas term incomplete, missing {missing}. Nothing was written.")
    if d["form"] != "fraction_of_mstar_in_RE":
        raise Refused(f"REFUSED: gas term form {d['form']!r} is not coded (only fraction_of_mstar_in_RE). "
                      "A form that uses M_E or any observed-side quantity is not allowed (D-036 #6).")
    if d["source_negligible"] not in ("zero", "registered"):
        raise Refused("REFUSED: gas term source_negligible must be 'zero' or 'registered'.")
    comps = []
    for name, c in d["components"].items():
        if name not in ("gas_cold", "gas_hot"):
            raise Refused(f"REFUSED: unknown gas component {name!r}")
        lo, de, hi = float(c["min"]), float(c["default"]), float(c["max"])
        if not 0.0 <= lo <= de <= hi:
            raise Refused(f"REFUSED: gas component {name}: need 0 <= min <= default <= max")
        comps.append(GasComponent(name, de, lo, hi))
    if not comps:
        raise Refused("REFUSED: gas term has no components")
    return GasTerm(d["assumption_id"], d["decision"], d["form"], tuple(comps), d["ref"], d["source_negligible"], synthetic)


def load_gas_term(path: Path = None) -> GasTerm | None:
    path = GAS_TERM_FILE if path is None else path
    if not path.is_file():
        return None
    return parse_gas_term(json.loads(path.read_text(encoding="utf-8")))


SYNTHETIC_GAS = {
    "assumption_id": "SYNTHETIC_gas", "decision": "SYNTHETIC (tests only; not a ruling)",
    "form": "fraction_of_mstar_in_RE", "ref": "SYNTHETIC: made-up numbers for code tests",
    "components": {"gas_cold": {"default": 0.01, "min": 0.0, "max": 0.05},
                   "gas_hot": {"default": 0.02, "min": 0.0, "max": 0.10}},
    "source_negligible": "zero",
}


# ----------------------------------------------------------------------------- input rows
def num(x):
    try:
        return float(str(x).replace("−", "-"))
    except (TypeError, ValueError):
        return None


def load_inputs(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _same_row(a: dict, b: dict) -> bool:
    keys = ("scope", "system", "record", "quantity", "value", "err_minus", "err_plus")
    return all((a.get(k) or "").strip() == (b.get(k) or "").strip() for k in keys)


def merge_supplement(rows: list[dict], sup: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """The adjudicated supplement merged into the inputs (gas/adjudication_gas.md §1).

    Returns (merged rows, rows set aside with the reason, rows of systems that cannot be tabulated).
    A supplement row equal to an input row (same scope, system, record, quantity and numbers) is a
    duplicate and is dropped; a row for a value the source does not print is set aside.
    """
    merged, aside, outside = list(rows), [], []
    for r in sup:
        if r["scope"] == R7_ONLY_SCOPE:
            outside.append(r)
            continue
        if r["status"].startswith("not printed"):
            aside.append({**r, "_why": "not printed by the source (kept in the reading file)"})
            continue
        if any(_same_row(r, x) for x in rows):
            aside.append({**r, "_why": "duplicate of an adjudicated_inputs.csv row"})
            continue
        merged.append(r)
    return merged, aside, outside


def imf_of(r: dict) -> str:
    found = [w for w in IMF_WORDS if w in r.get("note", "")]
    return found[0] if len(found) == 1 else ""


def variant_key(r: dict) -> str:
    """The row note with the IMF name removed: pairs a Chabrier/Kroupa value with its Salpeter top."""
    k = r.get("note", "")
    for w in IMF_WORDS:
        k = k.replace(w, "IMF")
    return f"{r['record']}|{k}"


def _r13_role(r: dict) -> str:
    """D-075 item 5 (Q5): Chabrier-BC03 default, Salpeter-BC03 top, Maraston 2005 pair alternative."""
    note = r.get("note", "")
    m05 = "Maraston" in note
    if imf_of(r) == "Salpeter":
        return "alt_top" if m05 else "top"
    return "alternative" if m05 else "default"


def resolve(r: dict) -> tuple[str, list[str]]:
    """Role of one input row under D-075 and D-076, and the package flags it brings. Unknown status: error."""
    s, rec, q = r["status"], r["record"], r["quantity"]
    if s == "default":
        return "default", []
    if s == "default candidate (Q5)" or s in ("range top for BC03 (Q5)", "range top for M05 (Q5)"):
        return _r13_role(r), []
    if s in ("pending Q6", "pending Q7"):  # D-075 item 2: J1538+5817, J0946+1006 -> R13
        return (_r13_role(r) if q == "mstar" else "default"), ["fallback_record"]
    if s == "range top":
        return "top", []
    if s == "default candidate (Q10)":  # D-075 item 5: SL2S CFHT fit
        return "default", []
    if s in ("alternative", "alternative (Q10)", "alternative (Q1)", "alternative (Q13)"):
        return ("alt_top" if q == "mstar" and imf_of(r) == "Salpeter" else "alternative"), []
    if s in ("pending Q2", "pending Q2, Q3"):  # D-075 item 2: J0403-0239 -> R29 matched pair, R27 alternative
        if rec == "R29":
            return "default", ["fallback_record"]
        return "alternative", []
    if s in ("pending Q1", "pending Q3", "pending Q4", "pending Q1, Q3", "pending Q11"):
        return "default", []  # D-075 items 3 and 4, and item 5 (Q11)
    if s == "pending Q1, Q8":
        return "excluded_mge", []  # D-075 item 2: no MGE code in v1
    # supplement (gas/adjudication_gas.md §1)
    if s.startswith("fallback_record candidate"):  # D-076 item 3: R61 is the next-ranked record for SNL-1
        return "default", ["fallback_record"]
    if s.startswith("fallback alternative"):  # R26 (rank 2 after R61) and R25 (rank 3): ranked alternatives
        return "alternative", []
    if s.startswith("profile-step check input") or s.startswith("reported check"):
        return "check", []  # D-075 item 5 and REPRODUCTION.md "Reported": inputs to reported checks only
    if s.startswith("record-only"):
        return "record_only", []
    raise ValueError(f"unknown status {s!r} ({r['system']}, {rec}, {q}); add it to resolve() with its ruling")


def tier(r: dict) -> int:
    """D-035: 1 for released files (VizieR, journal machine-readable tables), 2 for printed tables or text."""
    u = r.get("url", "")
    return 1 if ("vizier" in u or "_mrt" in u or "_ascii" in u) else 2


def astropy_unit(r: dict) -> str:
    u = r.get("unit", "")
    if r["quantity"] in ("theta_E", "aperture", "R_e", "half_separation"):
        return "kpc" if u == "kpc" else "arcsec"
    if r["quantity"] == "R_E_kpc":
        return "kpc"
    if "Msun/Lsun" in u:
        return "solMass / solLum"
    if "Msun" in u:
        return "solMass"
    if "Lsun" in u:
        return "solLum"
    return u


def unit_factor(unit: str) -> float:
    m = re.match(r"\s*(1e\d+)\s", unit or "")
    return float(m.group(1)) if m else 1.0


def value_with_errors(r: dict) -> tuple[float, float | None, float | None]:
    """Linear value and lower/upper errors in base units (Msun, Lsun, arcsec, kpc)."""
    v, lo, hi = num(r["value"]), num(r["err_minus"]), num(r["err_plus"])
    if r.get("form") == "log10":
        x = 10.0 ** v
        return x, (x * (1 - 10.0 ** (-lo)) if lo is not None else None), (x * (10.0 ** hi - 1) if hi is not None else None)
    f = unit_factor(r.get("unit", ""))
    return v * f, (lo * f if lo is not None else None), (hi * f if hi is not None else None)


# ----------------------------------------------------------------------------- assembly
@dataclass
class System:
    scope: str
    name: str
    rows: list = field(default_factory=list)
    flags: list = field(default_factory=list)
    reasons: list = field(default_factory=list)       # plotting conditions not met
    incomplete: list = field(default_factory=list)    # inputs missing for the computation
    kind: tuple = ("A7", "ambiguous: kind not in the inputs", "")
    gas_statement: str = ""


def group_systems(rows: list[dict]) -> tuple[list[System], dict]:
    """Systems with their resolved rows, and the record-level rows by record (one value per quantity)."""
    record_level, systems = {}, {}
    for r in rows:
        if r["system"] == "(record)":
            have = record_level.setdefault(r["record"], {}).get(r["quantity"])
            if have is not None and num(have["value"]) != num(r["value"]):
                raise ValueError(f"record {r['record']} {r['quantity']}: {have['value']} vs {r['value']} in two scopes")
            record_level[r["record"]].setdefault(r["quantity"], r)
            continue
        s = systems.setdefault((r["scope"], r["system"]), System(r["scope"], r["system"]))
        role, fl = resolve(r)
        s.rows.append({**r, "_role": role})
        s.flags += [f for f in fl if f not in s.flags]
    return list(systems.values()), record_level


def pick(s: System, q: str, role: str = "default", record: str | None = None) -> list[dict]:
    return [r for r in s.rows if r["quantity"] == q and r["_role"] == role and (record is None or r["record"] == record)]


def one(s: System, q: str, record: str | None = None) -> dict | None:
    xs = pick(s, q, record=record)
    if len(xs) > 1:
        raise ValueError(f"{s.name}: {len(xs)} default rows for {q}")
    return xs[0] if xs else None


def any_z(s: System, q: str) -> dict | None:
    """The default redshift row, else the first one of any role (for record-only systems)."""
    d = one(s, q)
    if d is not None:
        return d
    return next((r for r in s.rows if r["quantity"] == q and num(r["value"]) is not None), None)


def classify_kind(s: System) -> tuple[str, str, str, bool, str]:
    """(taxonomy_kind, kind_label, class_in_source, plottable, reason) from the source's own label."""
    k = one(s, "kind") or next((r for r in s.rows if r["quantity"] == "kind"), None)
    if k is None:
        notes = " ".join(r.get("note", "") for r in s.rows)
        if "late-type" in notes:
            return "A4", "late-type galaxy", "late-type (row notes)", False, "late-type lens galaxy (D-063 item 6)"
        return "A7", "ambiguous: kind not stated in the inputs", "", False, "kind not established at source"
    v = k["value"].strip()
    if v in ("E", "L", "U"):  # R5 Mph
        if v == "E":
            return "A6", "early-type galaxy", f"Mph = {v}", True, ""
        if v == "L":
            return "A4", "late-type galaxy", f"Mph = {v}", False, "not early-type at source (D-063 item 6)"
        return "A7", "ambiguous: early-type or late-type galaxy", f"Mph = {v}", False, "morphology unclassified at source (D-063 item 6)"
    if re.fullmatch(r"[A-Z]-[A-Z]-[A-Z]", v):  # R10 classification
        ok = v[0] == "E"
        return ("A6" if ok else "A7"), ("early-type galaxy" if ok else "ambiguous: early-type or late-type galaxy"), v, ok, \
            ("" if ok else "not early-type at source (D-063 item 6)")
    if v.startswith("grade"):
        ok = v.startswith("grade A")
        return "A6", "early-type galaxy", v, ok, ("" if ok else f"{v.split(';')[0]}: not a confirmed lens (D-063 item 5)")
    if re.search(r"ellip|E/S0|early-type", v, re.I):
        return "A6", "early-type galaxy", v, True, ""
    return "A7", "ambiguous: kind not settled by the source label", v, False, "kind not settled at source"


def is_spectroscopic(r: dict | None) -> bool:
    if r is None or num(r["value"]) is None:
        return False
    note = r.get("note", "")
    if re.search(r"estimate|z_FP|fundamental-plane", note, re.I):
        return False
    return "spectroscopic" in note or r["record"] in SPEC_Z_BY_SOURCE


def cosmology(s: System, record_level: dict, record: str) -> tuple[float | None, float | None, list[dict]]:
    h = one(s, "H0", record) or record_level.get(record, {}).get("H0")
    om = one(s, "Om", record) or record_level.get(record, {}).get("Om")
    return (num(h["value"]) if h else None), (num(om["value"]) if om else None), [x for x in (h, om) if x]


def aperture_in_note(r: dict) -> float | None:
    m = re.search(r"thetaE = ([0-9.]+)\)|inside ([0-9.]+)″", r.get("note", ""))
    return num(m.group(1) or m.group(2)) if m else None


@dataclass
class Inputs:
    """Everything one measurement row is computed from (the default, or one alternative)."""
    theta: float | None = None
    theta_row: dict | None = None
    z_l: float | None = None
    z_s: float | None = None
    z_rows: tuple = ()
    h0: float | None = None
    om: float | None = None
    cosmo_rows: tuple = ()
    obs_record: str = ""
    m_e: float | None = None
    m_e_lo: float | None = None
    m_e_hi: float | None = None
    m_e_source: str = ""
    m_e_row: dict | None = None
    r_e_printed: float | None = None
    r_e_row: dict | None = None
    st_record: str = ""
    st_rows: tuple = ()
    st_route: str = ""          # printed_in_RE | L_times_ML | profile
    mstar: float | None = None  # as printed (inside R_E, or total)
    mstar_lo: float | None = None
    mstar_hi: float | None = None
    top: float | None = None    # Salpeter value, same aperture as mstar
    top_source: str = ""
    top_rows: tuple = ()
    l_ap: float | None = None
    ml: float | None = None
    r_eff: float | None = None
    n: float | None = None
    profile_rows: tuple = ()
    theta_err: tuple = (None, None)
    flags: list = field(default_factory=list)


def assemble(s: System, record_level: dict, sub: dict | None = None) -> Inputs:
    """Default inputs of a system, with one input replaced by `sub` (an alternative row) if given.
    Missing inputs go to s.incomplete; nothing is guessed."""
    I = Inputs()

    def use(q, record=None):
        if sub is not None and sub["quantity"] == q and (record is None or sub["record"] == record):
            return sub
        return one(s, q, record)

    zl, zs = use("z_l"), use("z_s")
    I.z_l, I.z_s, I.z_rows = (num(zl["value"]) if zl else None), (num(zs["value"]) if zs else None), tuple(x for x in (zl, zs) if x)
    # observed side: printed M_E (or mass inside an aperture taken as R_E, D-075 item 3 / Q1), else theta_E
    me = use("M_E") or use("M_aperture")
    th = None
    if me is not None:
        I.obs_record = me["record"]
        th = use("theta_E", I.obs_record) or (use("aperture", I.obs_record) if me["quantity"] == "M_aperture" else None)
        I.m_e, I.m_e_lo, I.m_e_hi = value_with_errors(me)
        I.m_e_source, I.m_e_row = "printed", me
        if me["quantity"] == "M_aperture":
            I.flags.append("aperture_as_RE_half_image_separation")
    else:
        th = use("theta_E")
        if th is not None:
            I.obs_record = th["record"]
            I.m_e_source = "computed"
    if th is None and me is None:
        s.incomplete.append("no Einstein radius or Einstein mass in the inputs")
        return I
    if th is not None:
        I.theta, I.theta_row = num(th["value"]), th
        if "image half-separation" in th.get("note", "") or me is not None and me["quantity"] == "M_aperture":
            I.flags.append("model_dependence_half_image_separation")
    rk = use("R_E_kpc", I.obs_record)
    if rk is not None:  # D-075 item 4 (Q4): R32 printed R_E in kpc
        I.r_e_printed, I.r_e_row = num(rk["value"]), rk
        I.flags.append("R_E_printed_kpc")
    I.h0, I.om, cr = cosmology(s, record_level, I.obs_record)
    I.cosmo_rows = tuple(cr)
    I.flags.append(COSMOLOGY_CONVENTION.get(I.obs_record, "flat_from_omega_lambda"))
    if I.z_l is None or I.z_s is None:
        s.incomplete.append("lens or source redshift not in the inputs")
    need_cosmo = I.m_e_source == "computed" or I.r_e_printed is None
    if need_cosmo and (I.h0 is None or I.om is None):
        s.incomplete.append(f"cosmology of {I.obs_record} incomplete in the inputs "
                            f"(H0 {'present' if I.h0 is not None else 'missing'}, Omega_m {'present' if I.om is not None else 'missing'})")
    if I.r_e_printed is None and I.theta is None:
        s.incomplete.append("no Einstein radius in the inputs")
    if I.m_e_source == "computed" and I.theta is not None:
        frac = SAMPLE_LEVEL_ERROR.get((I.obs_record, "theta_E"))
        lo, hi = num(th["err_minus"]), num(th["err_plus"])
        if frac is not None and lo is None and hi is None:
            lo = hi = frac * I.theta
            I.flags.append("sample_level_error")
        if lo is None and hi is None:
            I.flags.append("no_uncertainty")
        I.theta_err = (lo, hi)
    if I.m_e_source == "printed" and I.m_e_lo is None and I.m_e_hi is None:
        I.flags.append("no_uncertainty")

    # baryonic side
    ms = use("mstar")
    lap, mlr = use("L_in_aperture"), use("ML_stellar_pop")
    if ms is not None:
        I.st_record, I.st_rows = ms["record"], (ms,)
        I.mstar, I.mstar_lo, I.mstar_hi = value_with_errors(ms)
        note = ms.get("note", "")
        if re.search(r"\btotal\b", note):
            I.st_route = "profile"
        elif re.search(r"inside", note, re.I):
            I.st_route = "printed_in_RE"
            ap = aperture_in_note(ms)
            if ap is not None and I.theta is not None and abs(ap - I.theta) > 1e-12:
                s.reasons.append(f"stellar mass printed inside {ap}″, observed side at {I.theta}″ (one cylinder, REPRODUCTION.md)")
        else:
            s.incomplete.append("aperture of the stellar mass not stated in the inputs")
        # Salpeter top printed by the same source for the same variant (D-075 item 5; D-076 item 2 for SL2S)
        role = "top" if sub is None or sub["quantity"] != "mstar" else "alt_top"
        tops = [r for r in s.rows if r["quantity"] == "mstar" and r["_role"] == role and variant_key(r) == variant_key(ms)]
        if tops:
            I.top, I.top_source, I.top_rows = value_with_errors(tops[0])[0], f"{tops[0]['record']} printed Salpeter", (tops[0],)
    elif lap is not None and mlr is not None:  # D-075 item 3 (Q3)
        I.st_record, I.st_rows, I.st_route = lap["record"], (lap, mlr), "L_times_ML"
        l, llo, lhi = value_with_errors(lap)
        u, ulo, uhi = value_with_errors(mlr)
        I.l_ap, I.ml, I.mstar = l, u, l * u
        if llo is not None or ulo is not None:  # relative errors in quadrature (D-075 Q3 (a))
            I.mstar_lo = I.mstar * math.hypot((llo or 0) / l, (ulo or 0) / u)
            I.mstar_hi = I.mstar * math.hypot((lhi or 0) / l, (uhi or 0) / u)
        if ulo is None and uhi is None:
            I.flags.append("no_uncertainty")  # D-075 Q3 (a); D-076 item 3: R61 Upsilon_ref has no printed error
        I.flags.append("mstar_from_L_times_ML")
        if lap["record"] in COSMOLOGY_CONVENTION and lap["record"] != I.obs_record:
            I.flags.append(COSMOLOGY_CONVENTION[lap["record"]])
        ap = one(s, "aperture", lap["record"])
        if ap is not None and I.theta is not None and abs(num(ap["value"]) - I.theta) > 1e-12:
            s.reasons.append(f"luminosity printed inside {ap['value']}″, observed side at {I.theta}″ (one cylinder)")
        apn = aperture_in_note(lap)
        if apn is not None and I.theta is not None and abs(apn - I.theta) > 1e-12:
            s.reasons.append(f"luminosity printed inside {apn}″, observed side at {I.theta}″ (one cylinder)")
    else:
        mge = [r for r in s.rows if r["_role"] == "excluded_mge"]
        if mge:
            s.incomplete.append("default stellar mass is an MGE (no MGE code in v1); the next-ranked eligible "
                                "stellar-mass record (D-075 item 2, fallback_record) is not in the adjudicated inputs")
        else:
            s.incomplete.append("no eligible stellar mass in the inputs")
    if I.st_route in ("printed_in_RE", "profile") and I.mstar_lo is None and I.mstar_hi is None:
        I.flags.append("no_uncertainty")
    if I.st_route == "profile":
        reff = use("R_e", I.st_record)
        nrow = use("sersic_n", I.st_record)
        if reff is None:
            s.incomplete.append("stellar mass is a total and the source's light-profile R_e is not in the inputs")
        else:
            I.r_eff, I.profile_rows = num(reff["value"]), (reff,) + ((nrow,) if nrow else ())
            if nrow is not None:
                I.n = num(nrow["value"])
            elif DEVAUC.search(reff.get("note", "")):
                I.n = 4.0
            else:
                s.incomplete.append("Sersic index of the source's light profile not in the inputs")
            I.flags.append("mstar_in_RE_from_profile")
            if I.st_record == "R10":  # D-075 item 5 (Q9)
                I.flags.append("profile_differs_from_mass_photometry")
        if I.theta is None:
            s.incomplete.append("profile step needs theta_E")
    if I.top is None and I.mstar is not None:
        conv = [r for r in s.rows if r["quantity"] in ("chab_to_salp_factor", "salpeter_alpha") and r["_role"] == "default"
                and r["record"] == I.st_record]
        rl = record_level.get(I.st_record, {})
        conv = conv or [rl[q] for q in ("chab_to_salp_factor", "salpeter_alpha") if q in rl]
        other = SALPETER_FROM_OTHER_SOURCE.get(I.st_record)
        if not conv and other and "chab_to_salp_factor" in record_level.get(other, {}):
            conv = [record_level[other]["chab_to_salp_factor"]]
            I.flags.append("salpeter_top_from_other_source_same_model_family")  # D-076 item 2
        if conv:
            c = conv[0]
            I.top = I.mstar / num(c["value"]) if c["quantity"] == "chab_to_salp_factor" else I.mstar * num(c["value"])
            I.top_source = f"{c['record']} printed conversion ({c['quantity']} = {c['value']})"
            I.top_rows = (c,)
            if "≈" in c.get("note", "") or "approximate" in c.get("note", ""):
                I.flags.append("salpeter_factor_approx_printed")
        else:
            I.flags.append("imf_top_not_read")
    return I


def plotting_conditions(s: System, I: Inputs) -> None:
    tk, label, cls, ok, why = classify_kind(s)
    s.kind = (tk, label, cls)
    if not ok:
        s.reasons.append(why)
    ro = sorted({r["status"] for r in s.rows if r["_role"] == "record_only"})
    if ro and ok:
        s.reasons.append("; ".join(ro))
    zl = next((r for r in I.z_rows if r["quantity"] == "z_l"), None) or any_z(s, "z_l")
    zs = next((r for r in I.z_rows if r["quantity"] == "z_s"), None) or any_z(s, "z_s")
    if not (is_spectroscopic(zl) and is_spectroscopic(zs)):
        s.reasons.append("lens and source redshifts not both measured spectroscopically in the inputs (D-063 item 5)")
    z = num(zl["value"]) if zl else None
    if z is not None and not z < Z_CUT:
        s.reasons.append(f"printed z_l = {z} is not below {Z_CUT} (D-066)")
        s.flags.append("epoch_gap_v1")


# ----------------------------------------------------------------------------- computation
def compute(I: Inputs, gas: GasTerm) -> dict:
    """Projected masses and accelerations with the frozen aeg.lensing functions."""
    out = {}
    if I.m_e_source == "computed":
        m_e = L.einstein_mass_msun(I.theta, I.z_l, I.z_s, I.h0, I.om)
        lo, hi = I.theta_err
        t = I.theta
        out["m_e"] = m_e
        out["m_e_lo"] = m_e * (1 - ((t - lo) / t) ** 2) if lo is not None else None
        out["m_e_hi"] = m_e * (((t + hi) / t) ** 2 - 1) if hi is not None else None
    else:
        out["m_e"], out["m_e_lo"], out["m_e_hi"] = I.m_e, I.m_e_lo, I.m_e_hi
    out["r_e"] = I.r_e_printed if I.r_e_printed is not None else L.einstein_radius_kpc(I.theta, I.z_l, I.h0, I.om)
    f = L.sersic_projected_fraction(I.theta, I.r_eff, I.n) if I.st_route == "profile" else 1.0
    out["f"] = f if I.st_route == "profile" else None
    out["mstar_re"] = I.mstar * f
    out["mstar_re_lo"] = I.mstar_lo * f if I.mstar_lo is not None else None
    out["mstar_re_hi"] = I.mstar_hi * f if I.mstar_hi is not None else None
    out["top_re"] = I.top * f if I.top is not None else None
    r = out["r_e"]
    out["g_obs"] = L.projected_acceleration(out["m_e"], r)
    k = out["g_obs"] / out["m_e"]
    out["g_obs_lo"] = out["m_e_lo"] * k if out["m_e_lo"] is not None else None
    out["g_obs_hi"] = out["m_e_hi"] * k if out["m_e_hi"] is not None else None
    out["g_bar_stars"] = L.projected_acceleration(out["mstar_re"], r)
    out["gas"] = {}
    for c in gas.components:
        out["gas"][c.name] = (c.default, c.minimum, c.maximum, L.projected_acceleration(c.default * out["mstar_re"], r))
    out["g_bar"] = out["g_bar_stars"] + sum(v[3] for v in out["gas"].values())
    ks = out["g_bar_stars"] / out["mstar_re"]
    out["g_bar_lo"] = out["mstar_re_lo"] * ks if out["mstar_re_lo"] is not None else None
    out["g_bar_hi"] = out["mstar_re_hi"] * ks if out["mstar_re_hi"] is not None else None
    return out


def compute_zero_gas(I: Inputs, gas: GasTerm) -> dict:
    """compute() for a gas term whose source_negligible is 'zero' on a system whose source states it negligible."""
    zero = GasTerm(gas.assumption_id, gas.decision, gas.form,
                   tuple(GasComponent(c.name, 0.0, 0.0, 0.0) for c in gas.components), gas.ref, gas.source_negligible, gas.synthetic)
    return compute(I, zero)


# ----------------------------------------------------------------------------- registry
def primary_name(scope: str, name: str) -> str:
    n = re.sub(r"\s*\(SNL-\d\)$", "", name).strip()
    if re.fullmatch(r"J\d{4}[+-]\d{4}", n):
        n = "SDSS " + n
    return n


def registry(names: list[str], synthetic: bool) -> dict[str, str]:
    """System IDs as aeg-d-dwarfs/v1 assigns them; synthetic runs get throw-away IDs and never touch the file."""
    if synthetic:
        return {n: f"synthetic-{i + 1:06d}" for i, n in enumerate(dict.fromkeys(names))}
    path = ROOT / "data/registry/systems.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    ids = {r["primary_name"]: r["system_id"] for r in rows if r["first_dataset"] == PID}
    missing = [n for n in dict.fromkeys(names) if n not in ids]
    if missing:
        if os.environ.get("AEG_REGISTER") != "1":
            raise SystemExit(f"{len(missing)} systems not in the registry; run once with AEG_REGISTER=1")
        n = max(int(r["system_id"].split("-")[-1]) for r in rows)
        with path.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for name in missing:
                n += 1
                ids[name] = f"aeg-s-{n:06d}"
                w.writerow([ids[name], name, PID, TODAY])
    return ids


# ----------------------------------------------------------------------------- checks
def formula_check(systems: list[System], record_level: dict) -> list[dict]:
    """§2.4 formula against every printed M_E whose system also has a printed theta_E of the same models."""
    out = []
    for s in systems:
        ths = [r for r in s.rows if r["quantity"] == "theta_E" and r["_role"] not in ("excluded_mge",)]
        mes = [r for r in s.rows if r["quantity"] == "M_E" and num(r["value"]) is not None]
        for th in ths:
            zl = next((r for r in s.rows if r["quantity"] == "z_l" and r["record"] == th["record"]
                       and r["_role"] in ("default", "record_only")), None) or any_z(s, "z_l")
            zs = next((r for r in s.rows if r["quantity"] == "z_s" and r["record"] == th["record"]
                       and r["_role"] in ("default", "record_only")), None) or any_z(s, "z_s")
            h0, om, _ = cosmology(s, record_level, th["record"])
            for me in mes:
                # the same record, or R7's printed M_E for R5's models (REPRODUCTION.md, Observed side)
                same = me["record"] == th["record"] or (me["record"], th["record"]) == ("R7", "R5")
                if not same or None in (h0, om, zl, zs) or num(zl["value"]) is None or num(zs["value"]) is None:
                    continue
                comp = L.einstein_mass_msun(num(th["value"]), num(zl["value"]), num(zs["value"]), h0, om)
                printed = value_with_errors(me)[0]
                out.append({"name": s.name, "scope": s.scope, "record_theta": th["record"], "record_m_e": me["record"],
                            "theta_arcsec": num(th["value"]), "z_l": num(zl["value"]), "z_s": num(zs["value"]),
                            "h0": h0, "om": om, "m_e_computed": comp, "m_e_printed": printed, "ratio": comp / printed,
                            "printed_form": me.get("form") or "linear", "printed_value": me["value"]})
    return out


def profile_step_check(systems: list[System]) -> list[dict]:
    """D-075 item 5: a record's total x f(<R_E) against the same record's printed mass inside R_E."""
    out = []
    for s in systems:
        ms = [r for r in s.rows if r["quantity"] in ("mstar", "mstar_total")]
        tot = [r for r in ms if r["quantity"] == "mstar_total" or re.search(r"\btotal\b", r.get("note", ""), re.I)]
        ins = [r for r in ms if r not in tot and re.search(r"inside", r.get("note", ""), re.I)]
        for t in tot:
            for i in ins:
                if t["record"] != i["record"] or imf_of(t) != imf_of(i):
                    continue
                if ("Maraston" in t.get("note", "")) != ("Maraston" in i.get("note", "")):
                    continue
                reff = next((r for r in s.rows if r["quantity"] == "R_e" and r["record"] == t["record"]), None)
                theta = aperture_in_note(i) or next((num(r["value"]) for r in s.rows if r["quantity"] == "theta_E"), None)
                if reff is None or theta is None:
                    continue
                nrow = next((r for r in s.rows if r["quantity"] == "sersic_n" and r["record"] == t["record"]), None)
                n = num(nrow["value"]) if nrow else (4.0 if DEVAUC.search(reff.get("note", "")) else None)
                if n is None:
                    continue
                f = L.sersic_projected_fraction(theta, num(reff["value"]), n)
                comp, printed = value_with_errors(t)[0] * f, value_with_errors(i)[0]
                out.append({"name": s.name, "scope": s.scope, "record": t["record"], "imf": imf_of(t),
                            "theta_arcsec": theta, "r_eff_arcsec": num(reff["value"]), "sersic_n": n, "fraction": f,
                            "mstar_total_msun": value_with_errors(t)[0], "mstar_in_re_computed": comp,
                            "mstar_in_re_printed": printed, "ratio": comp / printed})
    return out


# ----------------------------------------------------------------------------- released files
RELEASED = {  # url (as in the reading files) -> files under source/ (sources.json "file")
    "https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/ApJ/682/964/table4 (and table5)":
        ("vizier/J_ApJ_682_964_table4.tsv", "vizier/J_ApJ_682_964_table5.tsv"),
    "https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/A+A/501/461/lens": ("vizier/J_A+A_501_461_lens.tsv",),
}


def released_files_for(url: str) -> tuple[str, ...]:
    if url in RELEASED:
        return RELEASED[url]
    if "content.cld.iop.org" in url:
        return (f"iop/{url.rsplit('/', 1)[1]}",)
    return ()


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", s).upper().replace("SDSS", "").replace("−", "-")


def released_file_check(rows: list[dict], source_dir: Path) -> list[dict]:
    """Every tier-1 number used is found in its system's row of the released file (value and errors)."""
    out, cache = [], {}
    for r in rows:
        files = released_files_for(r.get("url", ""))
        if not files or r["system"] == "(record)":
            continue
        tokens, missing = set(), []
        for rel in files:
            p = source_dir / rel
            if not p.is_file():
                missing.append(rel)
                continue
            lines = cache.setdefault(rel, p.read_text(encoding="utf-8", errors="replace").splitlines())
            key = _norm(primary_name("", r["system"]))
            for line in lines:
                if line.startswith("#") or key not in _norm(line):
                    continue
                for tok in re.split(r"[\t ]+|\+or-", line):
                    tok = tok.strip()
                    if tok:
                        tokens.add(tok)
        if missing:
            raise Refused(f"REFUSED: released files missing under source/: {missing}. Run python -m aeg.fetch "
                          f"data/packages/{DATASET}/{VERSION} first. Nothing was written.")
        nums = {num(t) for t in tokens if num(t) is not None}
        for part in ("value", "err_minus", "err_plus"):
            v = (r.get(part) or "").strip()
            if not v:
                continue
            ok = (num(v) in nums) if num(v) is not None else (v in tokens)
            out.append({"system": r["system"], "record": r["record"], "quantity": r["quantity"], "part": part,
                        "value": v, "file": ";".join(files), "found": "yes" if ok else "no"})
    return out


# ----------------------------------------------------------------------------- conversion
OBS_STEPS = "image_positions;lens_model;einstein_radius"
MASS_STEPS = "image_positions;lens_model;einstein_radius;projected_mass"
QMAP = {"theta_E": ("observed", "einstein_radius", OBS_STEPS), "aperture": ("observed", "einstein_radius", OBS_STEPS),
        "half_separation": ("observed", "einstein_radius", "image_positions;einstein_radius"),
        "R_E_kpc": ("observed", "einstein_radius", OBS_STEPS),
        "M_E": ("observed", "einstein_mass", MASS_STEPS), "M_aperture": ("observed", "einstein_mass", MASS_STEPS),
        "z_l": ("observed", "redshift", "spectra"), "z_s": ("observed", "redshift", "spectra"),
        "mstar": ("baryonic", "mass_star", "photometry;luminosity;stellar_ml"),
        "L_in_aperture": ("baryonic", "luminosity", "photometry;luminosity"),
        "ML_stellar_pop": ("baryonic", "stellar_ml_population", "stellar_ml"),
        "R_e": ("baryonic", "half_light_radius", "photometry;structural_model"),
        "sersic_n": ("baryonic", "structural_param", "photometry;structural_model")}


def convert(rows: list[dict], gas: GasTerm, synthetic: bool) -> dict:
    """All rows of all tables, as plain dicts. No file is touched."""
    systems, record_level = group_systems(rows)
    not_tabulated = []
    keep = []
    for s in systems:  # data standard §10 item 7: a system needs a redshift (or distance) to be tabulated
        if any_z(s, "z_l") is None:
            not_tabulated.append({"scope": s.scope, "system": s.name,
                                  "reason": "no measured lens redshift in the inputs (data standard §10 item 7)"})
        else:
            keep.append(s)
    real = not any(r["scope"].startswith("SYNTHETIC") for r in rows)
    gap, gap_none, gap_low = epoch_gap_lenses({lens_key(s.name) for s in systems}) if real else ([], [], [])
    if gap_low:  # every lens below the cut must already be in the adjudicated inputs
        raise ValueError(f"lenses below z_l = {Z_CUT} in the readings but not in the inputs: {gap_low}")
    not_tabulated += gap_none
    systems = keep
    ids = registry([primary_name(s.scope, s.name) for s in systems] + [g.name for g in gap], synthetic)
    meas, obs, sysrows, used_rows = [], [], [], []

    def add_obs(sid, side, q, r, steps, param=""):
        v, lo, hi = value_with_errors(r)
        oid = f"{PID}/o{len(obs) + 1:06d}"
        band = re.search(r"\((\w+)\)", r.get("unit", ""))
        obs.append({"observable_id": oid, "system_id": sid, "side": side, "quantity": q, "value": v, "err_lo": lo,
                    "err_hi": hi, "unit": astropy_unit(r),
                    "band": band.group(1) if band and q in ("luminosity", "stellar_ml_population") else "", "limit": "none",
                    "steps": steps, "evidence_tier": tier(r),
                    "source_ref": f"{r['record']}: {r['location']} ({r['url']})", f"{X}parameter": param or r.get("note", "")[:200],
                    f"{X}role": r["_role"], f"{X}printed": f"{r['value']} -{r['err_minus']} +{r['err_plus']} [{r.get('form') or 'linear'}; {r.get('unit', '')}]"})
        used_rows.append(r)
        return oid

    for s in systems:
        sid = ids[primary_name(s.scope, s.name)]
        I = assemble(s, record_level)
        plotting_conditions(s, I)
        where = GAS_SOURCE_NEGLIGIBLE.get(primary_name(s.scope, s.name))
        if where:
            s.gas_statement = (f"source states gas inside R_E negligible ({where}; a source assumption, not a measurement); "
                               f"the registered gas term applies ({gas.decision})" if gas.source_negligible == "registered"
                               else f"source states gas inside R_E negligible ({where}); gas set to zero ({gas.decision})")
            s.flags.append("gas_negligible_source_assumption")
        complete = not s.incomplete
        zrow = any_z(s, "z_l")
        zsrow = any_z(s, "z_s")
        sysrows.append({"system_id": sid, "name_in_source": s.name, "class_in_source": s.kind[2] or "not stated",
                        "taxonomy_kind": s.kind[0], "kind_label": s.kind[1], "host": "",
                        "redshift": num(zrow["value"]), "redshift_err": num(zrow["err_minus"]), "distance_kinematic": "false",
                        "distance_ref": f"lens redshift {zrow['record']}: {zrow['location']}",
                        "properties": json.dumps({"scope": s.scope, "status": "plotted" if complete and not s.reasons else "recorded",
                                                  "plotted": bool(complete and not s.reasons),
                                                  "reasons_not_plotted": s.reasons + s.incomplete,
                                                  "z_s": num(zsrow["value"]) if zsrow else None,
                                                  "gas_statement": s.gas_statement or None,
                                                  "flags": sorted(set(s.flags + I.flags))}, ensure_ascii=False, sort_keys=True)})
        if not complete:
            continue
        o_ids, b_ids = [], []
        for r in (I.theta_row, I.m_e_row, I.r_e_row) + I.z_rows:
            if r is not None:
                side, q, steps = QMAP[r["quantity"]]
                o_ids.append(add_obs(sid, side, q, r, steps))
        for r in I.st_rows + I.top_rows + I.profile_rows:
            if r["quantity"] in QMAP:
                side, q, steps = QMAP[r["quantity"]]
                b_ids.append(add_obs(sid, side, q, r, steps, param=("Salpeter top (IMF slider): " + r.get("note", "")[:170])
                                     if r in I.top_rows else ""))
        for r in s.rows:  # alternatives recorded as observables (D-075 items 2, 5; Q1, Q13)
            # Apertures of stellar-side alternatives (R25, R26 for SNL-1) are luminosity or spectroscopic
            # apertures, not Einstein radii: they stay in the alternative's note, never as einstein_radius.
            if r["quantity"] == "aperture" and r["record"] != I.obs_record:
                continue
            if r["_role"] in ("alternative", "alt_top") and r["quantity"] in QMAP:
                side, q, steps = QMAP[r["quantity"]]
                add_obs(sid, side, q, r, steps, param=f"alternative: {r.get('note', '')[:180]}")
        zero = bool(s.gas_statement) and gas.source_negligible == "zero"
        c = compute_zero_gas(I, gas) if zero else compute(I, gas)
        default_id = f"{PID}/m{len(meas) + 1:06d}"
        meas.append(measurement_row(default_id, sid, s, I, c, gas, o_ids, b_ids, role="default", zero_gas=zero))
        # alternative measurement rows: one input replaced (stellar mass variant, light profile, lens redshift)
        used = {r["quantity"]: r["record"] for r in (I.st_rows + I.profile_rows + I.z_rows)}
        for r in s.rows:
            # only an alternative from the same record as the default input it replaces (no mixed records)
            if r["_role"] != "alternative" or r["quantity"] not in ("mstar", "R_e", "z_l") or used.get(r["quantity"]) != r["record"]:
                continue
            kept = (list(s.incomplete), list(s.reasons))
            Ia = assemble(s, record_level, sub=r)
            if len(s.incomplete) > len(kept[0]):
                s.incomplete[:], s.reasons[:] = kept
                continue
            s.incomplete[:], s.reasons[:] = kept
            ca = compute_zero_gas(Ia, gas) if zero else compute(Ia, gas)
            mid = f"{PID}/m{len(meas) + 1:06d}"
            meas.append(measurement_row(mid, sid, s, Ia, ca, gas, o_ids, b_ids, role="alternative", zero_gas=zero,
                                        alternative_of=default_id,
                                        alt_note=f"{r['quantity']} = {r['value']} ({r['record']}; {r.get('note', '')[:120]})"))
    for g in gap:  # D-066 item 2: recorded in full, flagged epoch_gap_v1; no measurement row
        sysrows.append(gap_system_row(ids[g.name], g))
    return {"measurements": meas, "observables": obs, "systems": sysrows, "used_rows": used_rows, "epoch_gap": gap,
            "formula_check": formula_check(systems, record_level), "profile_step": profile_step_check(systems),
            "overlap": overlap(systems), "not_tabulated": not_tabulated, "systems_obj": systems}


def overlap(systems: list[System]) -> list[dict]:
    """REPRODUCTION.md 'Reported': systems in more than one survey's inputs (by primary name), side by side."""
    by = {}
    for s in systems:
        by.setdefault(primary_name(s.scope, s.name), []).append(s.scope)
    return [{"system": n, "scopes": " | ".join(sc)} for n, sc in sorted(by.items()) if len(sc) > 1]


def measurement_row(mid, sid, s, I, c, gas, o_ids, b_ids, role, zero_gas=False, alternative_of=None, alt_note=None) -> dict:
    fl = list(dict.fromkeys(s.flags + I.flags))
    core = [f for f in fl if f in CORE_FLAGS]
    plotted = role == "default" and not s.reasons
    if role == "alternative":
        reason, note = "alternative_value", f"alternative: {alt_note}"
    elif s.reasons:
        reason = "epoch_gap" if "epoch_gap_v1" in fl and len(s.reasons) == 1 else "other"
        note = "; ".join(s.reasons)
    else:
        reason, note = None, None
    adjustable = ";".join(a for a, ok in ((IMF_ID, c["top_re"] is not None), (gas.assumption_id, not zero_gas)) if ok)
    gas_status = "absent" if zero_gas else "modelled"
    row = {
        "measurement_id": mid, "system_id": sid, "kind": "system_value", "channel": "lensing", "method_class": "lensing",
        "method": ("projected mass inside the Einstein radius against the projected stellar and gas mass inside the same "
                   "cylinder, both as G M / R_E^2 (D-064); M_E " + I.m_e_source + "; stellar mass " + I.st_route),
        "measured_quantity": "g_obs", "r_kpc": c["r_e"], "r_kind": "projected",
        "g_obs": c["g_obs"], "g_obs_err_lo": c["g_obs_lo"], "g_obs_err_hi": c["g_obs_hi"],
        "g_bar": c["g_bar"], "g_bar_err_lo": c["g_bar_lo"], "g_bar_err_hi": c["g_bar_hi"],
        "g_bar_stars": c["g_bar_stars"],
        "g_bar_gas_cold": c["gas"].get("gas_cold", (None,) * 4)[3], "g_bar_gas_hot": c["gas"].get("gas_hot", (None,) * 4)[3],
        "limit": "none", "stars_status": "measured",
        "gas_cold_status": gas_status if "gas_cold" in c["gas"] else "absent",
        "gas_hot_status": gas_status if "gas_hot" in c["gas"] else "absent",
        "observed_from": ";".join(o_ids), "baryonic_from": ";".join(b_ids),
        "model_dependence": "total_mass_form" if "model_dependence_half_image_separation" in fl else "none",
        "evidence_tier": max(tier(r) for r in (I.theta_row, I.m_e_row, I.r_e_row) + I.z_rows + I.st_rows + I.profile_rows if r),
        "role": role, "alternative_of": alternative_of, "plotted": "true" if plotted else "false",
        "not_plotted_reason": reason, "assumptions": ";".join(METHOD_ASSUMPTIONS + (gas.assumption_id,)),
        "adjustable": adjustable, "flags": ";".join(core),
        "source_ref": f"observed {I.obs_record}; stellar {I.st_record}", "notes": note,
        f"{X}projection": "projected", f"{X}scope": s.scope,
        f"{X}flags": " ".join(f for f in fl if f not in CORE_FLAGS),
        f"{X}theta_e_arcsec": I.theta, f"{X}z_l": I.z_l, f"{X}z_s": I.z_s, f"{X}h0": I.h0, f"{X}om": I.om,
        f"{X}m_e_msun": c["m_e"], f"{X}m_e_source": I.m_e_source,
        f"{X}r_e_source": "printed" if I.r_e_printed is not None else "computed",
        f"{X}mstar_route": I.st_route, f"{X}mstar_msun": I.mstar, f"{X}l_aperture_lsun": I.l_ap, f"{X}ml": I.ml,
        f"{X}r_eff_arcsec": I.r_eff, f"{X}sersic_n": I.n, f"{X}profile_fraction": c["f"],
        f"{X}mstar_re_msun": c["mstar_re"], f"{X}mstar_top_msun": c["top_re"], f"{X}mstar_top_source": I.top_source,
        f"{X}gas_term": f"{gas.assumption_id} ({gas.decision})" + (" SYNTHETIC" if gas.synthetic else ""),
        f"{X}gas_statement": s.gas_statement,
    }
    for name in ("gas_cold", "gas_hot"):
        g = c["gas"].get(name)
        row[f"{X}{name}_frac"], row[f"{X}{name}_frac_min"], row[f"{X}{name}_frac_max"] = (g[0], g[1], g[2]) if g else (None, None, None)
    return row


def arithmetic_check(meas_rows: list[dict]) -> int:
    """REPRODUCTION.md test 3: recompute every derived column from the stored inputs, to 1e-9.
    Covers M_E (where computed), R_E, the L x M/L products, f(<R_E), M*(<R_E), the IMF top's scaling,
    g_obs, g_bar_stars, each gas component and g_bar. Returns the number of comparisons."""
    n = 0

    def close(a, b, what, mid):
        nonlocal n
        n += 1
        if a is None or b is None:
            raise SystemExit(f"arithmetic test 3 failed at {mid}: {what} missing ({a} vs {b})")
        if a == b == 0.0:
            return
        if abs(a / b - 1) > TOL:
            raise SystemExit(f"arithmetic test 3 failed at {mid}: {what} ({a} vs {b})")
    for r in meas_rows:
        mid = r["measurement_id"]
        if r[f"{X}m_e_source"] == "computed":
            close(L.einstein_mass_msun(r[f"{X}theta_e_arcsec"], r[f"{X}z_l"], r[f"{X}z_s"], r[f"{X}h0"], r[f"{X}om"]),
                  r[f"{X}m_e_msun"], "M_E", mid)
        if r[f"{X}r_e_source"] == "computed":
            close(L.einstein_radius_kpc(r[f"{X}theta_e_arcsec"], r[f"{X}z_l"], r[f"{X}h0"], r[f"{X}om"]), r["r_kpc"], "R_E", mid)
        m = r[f"{X}mstar_msun"]
        f = 1.0
        if r[f"{X}mstar_route"] == "L_times_ML":
            close(r[f"{X}l_aperture_lsun"] * r[f"{X}ml"], m, "L x M/L", mid)
        if r[f"{X}mstar_route"] == "profile":
            f = L.sersic_projected_fraction(r[f"{X}theta_e_arcsec"], r[f"{X}r_eff_arcsec"], r[f"{X}sersic_n"])
            close(f, r[f"{X}profile_fraction"], "f(<R_E)", mid)
        close(m * f, r[f"{X}mstar_re_msun"], "M*(<R_E)", mid)
        close(L.projected_acceleration(r[f"{X}m_e_msun"], r["r_kpc"]), r["g_obs"], "g_obs", mid)
        gs = L.projected_acceleration(m * f, r["r_kpc"])
        close(gs, r["g_bar_stars"], "g_bar_stars", mid)
        gas = 0.0
        for c in ("gas_cold", "gas_hot"):
            gc = L.projected_acceleration((r[f"{X}{c}_frac"] or 0.0) * m * f, r["r_kpc"])
            if r.get(f"g_bar_{c}") is not None:
                close(gc, r[f"g_bar_{c}"], f"g_bar_{c}", mid)
            gas += gc
        close(gs + gas, r["g_bar"], "g_bar", mid)
    return n


# ----------------------------------------------------------------------------- epoch gap (D-066 item 2)
# The adjudicated inputs hold only the systems below z_l = 0.30. D-066 item 2 records every system at or above
# the cut in full, flagged epoch_gap_v1. These rows come straight from the two independent readings
# (reading/readings/reader-{a,b}-block{1,2,3}.csv); nothing here is adjudicated. A value both readers recorded
# identically is used; where they differ, both are recorded and the system is flagged readers_differ
# (listed in SECOND_READING.md). No measurement or observable row is written for these systems.
READINGS = HERE / "reading/readings"
READING_BLOCKS = ("block1", "block2", "block3")
EPOCH_REASON = "z_l ≥ 0.30 (D-066)"
# Readers' spellings of one lens that the plain normalisation does not join (each checked by eye in the
# two readings: same coordinates or the same name given in the other reader's parenthesis).
LENS_ALIASES = {
    "J010049.18181827.7": "J01001818",      # SDSS J0100+1818 = SDSS J010049.18+181827.7 (both readers say so)
    "COSMICHORSESHOE": "J11481930",         # Cosmic Horseshoe = SDSS J1148+1930 (both readers say so)
    "SL2SJ021760513": "J021737051329",      # SL2SJ02176-0513 (J2000 02:17:37.136 -05:13:29.41)
    "J143607.49494313.2": "J14364943",      # MaNGA J1436+4943 (already in the tables)
    "J170124.01372258.1": "J17013722",      # MaNGA J1701+3722 (already in the tables)
}
LENS_QUANTITIES = {"z_l", "z_s", "kind", "theta_E"}  # a key with none of these is a sample-level row, not a lens
NOT_LENS_SCOPES = {"gas"}  # reader rows about gas statements, not a lens scope
_ESTIMATE = re.compile(r"estimat|z_?FP\b|fundamental-plane", re.I)
# Method classes, in the order searched; the earliest one found in the reader's text is the class.
METHOD_CLASSES = (("not measured", "not measured"), ("not stated", "not stated"), ("tentative", "tentative"),
                  ("estimat", "estimate"), ("derived", "estimate"), ("photometric", "photometric"),
                  ("spectroscop", "spectroscopic"))
_R5_MPH = {"E", "L", "U"}
_R10_CODE = re.compile(r"\b([A-Z]-[A-Z]-[A-Z])\b")


def _norm_id(s: str) -> str:
    return re.sub(r"[\s_\-−–+]", "", s or "").upper().replace("SDSSJ", "J")


def lens_key(system_id: str) -> str:
    """One key per lens: the designation before any parenthesis, normalised; 12-digit J designations keyed on
    the coordinates alone, so the same lens read in SL2S and in SuGOHI is one system."""
    n = _norm_id(system_id.split("(")[0])
    n = LENS_ALIASES.get(n, n)
    m = re.fullmatch(r"[A-Z0-9]*?J(\d{6}\d{6})", n)
    return f"J{m.group(1)}" if m else n


def lens_display_name(system_id: str) -> str:
    base = system_id.split("(")[0].strip().replace("−", "-").replace("–", "-")
    n = _norm_id(base)
    if n == "COSMICHORSESHOE":
        return "SDSS J1148+1930"
    if n.startswith("J010049"):
        return "SDSS J0100+1818"
    if n == "SL2SJ021760513":
        return "SL2SJ021737-051329"
    base = re.sub(r"\s+", "", base)
    base = re.sub(r"^SDSSJ", "J", base)
    return primary_name("", base)


def _first_number(s: str) -> float | None:
    m = re.search(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", (s or "").replace("−", "-"))
    return float(m.group(0)) if m else None


def method_class(text: str) -> str:
    t = (text or "").lower()
    hits = [(t.find(k), v) for k, v in METHOD_CLASSES if k in t]
    return min(hits)[1] if hits else (t.strip() or "")


def _is_estimate(r: dict) -> bool:
    return bool(_ESTIMATE.search(r.get("limit", "") or "") or _ESTIMATE.search(r.get("note", "") or "")
                or "estimate" in (r.get("form", "") or ""))


def load_readings() -> dict:
    """lens key -> scope -> reader ('a'/'b') -> list of reading rows (in file order)."""
    out: dict = {}
    for block in READING_BLOCKS:
        for reader in "ab":
            with open(READINGS / f"reader-{reader}-{block}.csv", encoding="utf-8", newline="") as f:
                for r in csv.DictReader(f):
                    if r["system_id"].strip().startswith("(") or r["scope"].strip() in NOT_LENS_SCOPES:
                        continue
                    k = lens_key(r["system_id"])
                    out.setdefault(k, {}).setdefault(r["scope"].strip(), {}).setdefault(reader, []).append(
                        {**r, "_block": block, "_reader": reader})
    return out


def _reader_view(rows: list[dict]) -> dict:
    """One reader's reading of one lens in one scope."""
    def vals(q, measured_only=False):
        xs = []
        for r in rows:
            if r["quantity"] != q:
                continue
            v = _first_number(r["value"])
            if v is None or (measured_only and _is_estimate(r)):
                continue
            if v not in xs:
                xs.append(v)
        return xs

    def texts(q):
        xs = []
        for r in rows:
            t = re.sub(r"\s+", " ", (r["value"] or "")).strip()
            if r["quantity"] == q and t and t not in xs:
                xs.append(t)
        return xs
    zl_rows = [r for r in rows if r["quantity"] == "z_l" and _first_number(r["value"]) is not None]
    return {
        "z_l": vals("z_l", measured_only=True),
        "z_l_estimates": [v for v in vals("z_l") if v not in vals("z_l", measured_only=True)],
        "z_s": vals("z_s"),
        "z_l_method": sorted({method_class(t) for t in texts("z_l_method")}),
        "z_s_method": sorted({method_class(t) for t in texts("z_s_method")}),
        "z_l_method_text": texts("z_l_method"), "z_s_method_text": texts("z_s_method"),
        "kind_text": texts("kind"),
        "records": sorted({r["record"] for r in rows if r["record"]}),
        "ids": list(dict.fromkeys(r["system_id"].strip() for r in rows)),
        "z_l_rows": zl_rows,
    }


def _kind_code(texts: list[str]) -> str | None:
    """A classification code printed by the source (R5 Mph; R10 class code), if the reader recorded one."""
    bare = [t for t in texts if t in _R5_MPH]
    if len(bare) == 1:
        return bare[0]
    codes = sorted({m.group(1) for t in texts for m in _R10_CODE.finditer(t)})
    return codes[0] if len(codes) == 1 else None


def compare_kind(a: list[str], b: list[str]) -> tuple[str | None, str]:
    """(agreed kind, how): identical recorded texts, or the same printed code; else (None, 'differ')."""
    if a and sorted(a) == sorted(b):
        return " | ".join(a), "identical text"
    ca, cb = _kind_code(a), _kind_code(b)
    if ca and ca == cb:
        return ca, "same printed code"
    return None, "differ"


def _agree(a: list, b: list) -> bool:
    return sorted(a) == sorted(b)


@dataclass
class GapLens:
    key: str
    name: str
    ids: list
    scopes: list
    readings: dict             # scope -> {"a": view, "b": view, ...}
    z_l: float | None = None
    z_s: float | None = None
    z_l_method: str = ""
    z_s_method: str = ""
    kind: tuple = ("A7", "", "")
    flags: list = field(default_factory=list)
    differences: list = field(default_factory=list)   # (scope, quantity, reader A, reader B)
    z_ref: str = ""


def epoch_gap_lenses(tabulated_keys: set) -> tuple[list[GapLens], list[dict], list[dict]]:
    """Lenses read in the scopes but not in the adjudicated inputs.

    Returns (lenses with a printed measured z_l >= 0.30, lenses with no printed measured z_l (not tabulated),
    lenses with a printed z_l below 0.30 that are not in the inputs (reported; expected none))."""
    raw = load_readings()
    gap, none_z, low = [], [], []
    for key, by_scope in raw.items():
        if key in tabulated_keys:
            continue
        if not any(r["quantity"] in LENS_QUANTITIES for d in by_scope.values() for rs in d.values() for r in rs):
            continue
        readings = {sc: {rd: _reader_view(rs) for rd, rs in d.items()} for sc, d in by_scope.items()}
        all_rows = [r for d in by_scope.values() for rs in d.values() for r in rs]
        ids = list(dict.fromkeys(r["system_id"].strip() for r in all_rows))
        first = next(r for r in all_rows)
        name = lens_display_name(first["system_id"])
        measured = sorted({v for d in readings.values() for v in (x for rd in d.values() for x in rd["z_l"])})
        if not measured:
            est = sorted({v for d in readings.values() for rd in d.values() for v in rd["z_l_estimates"]})
            none_z.append({"scope": " | ".join(by_scope), "system": name,
                           "reason": ("lens redshift printed only as an estimate (" + ", ".join(f"{v:g}" for v in est) +
                                      "; fundamental-plane or image-separation), not a measurement (data standard §10 item 7)")
                           if est else "no lens redshift printed (data standard §10 item 7)"})
            continue
        if any(v < Z_CUT for v in measured):
            low.append({"system": name, "scopes": " | ".join(by_scope), "z_l": measured})
            continue
        g = GapLens(key, name, ids, list(by_scope), readings)
        zls, zss, zlm, zsm, kinds = [], [], [], [], []
        for sc, d in readings.items():
            a, b = d.get("a"), d.get("b")
            ea = {"z_l": [], "z_s": [], "z_l_method": [], "z_s_method": [], "kind_text": [], "z_l_estimates": []}
            a, b = a or ea, b or ea
            for q in ("z_l", "z_s", "z_l_method", "z_s_method"):
                if not _agree(a[q], b[q]):
                    g.differences.append((sc, q, a[q], b[q]))
            if a["z_l_estimates"] != b["z_l_estimates"] and (a["z_l_estimates"] or b["z_l_estimates"]):
                g.differences.append((sc, "z_l (estimate, not used)", a["z_l_estimates"], b["z_l_estimates"]))
            kv, how = compare_kind(a["kind_text"], b["kind_text"])
            if kv is None:
                g.differences.append((sc, "kind", a["kind_text"], b["kind_text"]))
            d["kind_agreed"], d["kind_how"] = kv, how
            zls.append(sorted(set(a["z_l"]) | set(b["z_l"])))
            zss.append(sorted(set(a["z_s"]) | set(b["z_s"])))
            zlm.append(sorted(set(a["z_l_method"]) | set(b["z_l_method"])))
            zsm.append(sorted(set(a["z_s_method"]) | set(b["z_s_method"])))
            kinds.append(kv)
        if any(q in ("z_l", "z_s", "z_l_method", "z_s_method", "kind") for _, q, _, _ in g.differences):
            g.flags.append("readers_differ")
        all_zl = sorted({v for x in zls for v in x})
        all_zs = sorted({v for x in zss for v in x})
        if len({tuple(x) for x in zls if x}) > 1 or len({tuple(x) for x in zss if x}) > 1:
            g.flags.append("sources_differ")
        # The redshift column holds the printed value where every reading agrees on one; otherwise the lowest
        # printed value, so that the D-066 test holds for every reading. All readings are in properties.
        g.z_l = all_zl[0]
        g.z_s = all_zs[0] if len(all_zs) == 1 else None
        g.z_l_method = " | ".join(sorted({m for x in zlm for m in x}))
        g.z_s_method = " | ".join(sorted({m for x in zsm for m in x}))
        agreed = [k for k in kinds if k is not None]
        if agreed and len(agreed) == len(kinds) and len(set(agreed)) == 1:
            tk, label, cls, _, _ = classify_kind(System("", "", rows=[{"quantity": "kind", "value": agreed[0],
                                                                       "_role": "default", "note": ""}]))
            g.kind = (tk, label, cls)
        else:
            texts = []
            for sc, d in readings.items():
                for rd in "ab":
                    if rd in d:
                        texts.append(f"reader {rd.upper()} ({sc}): " + (" | ".join(d[rd]["kind_text"]) or "no kind recorded"))
            g.kind = ("A7", "ambiguous: the two readings of the kind differ (not adjudicated; SECOND_READING.md)",
                      "; ".join(texts))
        zr = next(r for d in by_scope.values() for rd in "ab" for r in d.get(rd, [])
                  if r["quantity"] == "z_l" and _first_number(r["value"]) == g.z_l and not _is_estimate(r))
        g.z_ref = f"lens redshift {zr['record']}: {zr['location']} ({zr['url']}), reader {zr['_reader'].upper()}"
        g.flags.insert(0, "epoch_gap_v1")
        gap.append(g)
    gap.sort(key=lambda g: (g.scopes[0], g.name))
    none_z.sort(key=lambda r: (r["scope"], r["system"]))
    return gap, none_z, low


def gap_system_row(sid: str, g: GapLens) -> dict:
    readings = {}
    for sc, d in g.readings.items():
        e = {}
        for rd in "ab":
            v = d.get(rd)
            e[f"reader_{rd}"] = None if v is None else {
                "ids": v["ids"], "records": v["records"], "z_l": v["z_l"], "z_l_estimates": v["z_l_estimates"],
                "z_s": v["z_s"], "z_l_method": v["z_l_method_text"], "z_s_method": v["z_s_method_text"],
                "kind": v["kind_text"]}
        e["kind_agreed"], e["kind_agreed_by"] = d.get("kind_agreed"), d.get("kind_how")
        readings[sc] = e
    props = {"scope": " | ".join(g.scopes), "status": "recorded", "plotted": False,
             "reasons_not_plotted": [EPOCH_REASON], "z_s": g.z_s, "gas_statement": None,
             "flags": g.flags, "identifiers": g.ids, "z_l_method": g.z_l_method, "z_s_method": g.z_s_method,
             "z_l_all_readings": sorted({v for d in g.readings.values() for rd in "ab" if rd in d for v in d[rd]["z_l"]}),
             "z_s_all_readings": sorted({v for d in g.readings.values() for rd in "ab" if rd in d for v in d[rd]["z_s"]}),
             "readers_differ_on": sorted({f"{sc}: {q}" for sc, q, _, _ in g.differences}),
             "readings": readings,
             "note": "recorded from the two independent readings, not adjudicated (D-066 item 2); no measurement row"}
    return {"system_id": sid, "name_in_source": g.name, "class_in_source": g.kind[2] or "not stated",
            "taxonomy_kind": g.kind[0], "kind_label": g.kind[1], "host": "", "redshift": g.z_l, "redshift_err": None,
            "distance_kinematic": "false", "distance_ref": g.z_ref,
            "properties": json.dumps(props, ensure_ascii=False, sort_keys=True)}


# ----------------------------------------------------------------------------- tables
def _table(rows: list[dict], spec: dict, meta: dict):
    import numpy as np
    from astropy.table import MaskedColumn, Table
    cols = []
    keys = list(rows[0].keys()) if rows else list(spec)
    for k in keys:
        unit, ucd, desc = spec.get(k, (None, "meta.note", k))
        data = [r.get(k) for r in rows]
        numeric = any(isinstance(x, float) for x in data) or unit is not None
        if k == "evidence_tier":
            c = MaskedColumn(np.array([int(x) for x in data], dtype="i8"), name=k, description=desc)
        elif numeric:
            c = MaskedColumn(np.array([np.nan if x is None else float(x) for x in data], dtype="f8"),
                             mask=[x is None for x in data], name=k, unit=unit, description=desc)
        else:
            c = MaskedColumn(["" if x is None else str(x) for x in data], name=k, dtype=str, description=desc)
        c.meta["ucd"] = ucd
        cols.append(c)
    t = Table(cols)
    t.meta = dict(meta)
    return t


ACC = "m / s2"
MEAS_SPEC = {
    "measurement_id": (None, "meta.id;meta.main", "Measurement identifier (D-006)"),
    "system_id": (None, "meta.id", "Atlas system identifier (data/registry/systems.csv)"),
    "kind": (None, "meta.code", "system_value: one value per system"),
    "channel": (None, "meta.code", "lensing"),
    "method_class": (None, "meta.code", "lensing"),
    "method": (None, "meta.note", "How g_obs and g_bar were obtained"),
    "measured_quantity": (None, "meta.code", "g_obs"),
    "r_kpc": ("kpc", "phys.size.radius", "Einstein radius R_E (projected)"),
    "r_kind": (None, "meta.code", "projected (D-064): never merged with 3D values"),
    "g_obs": (ACC, "phys.acceleration", "Observed acceleration in projection, G M_E / R_E^2 (D-064)"),
    "g_obs_err_lo": (ACC, "stat.error;phys.acceleration", "From the M_E error at fixed R_E"),
    "g_obs_err_hi": (ACC, "stat.error;phys.acceleration", "From the M_E error at fixed R_E"),
    "g_bar": (ACC, "phys.acceleration", "Baryonic acceleration in projection, G (M*(<R_E) + M_gas(<R_E)) / R_E^2 (D-064)"),
    "g_bar_err_lo": (ACC, "stat.error;phys.acceleration", "From the stellar-mass error only, at fixed R_E"),
    "g_bar_err_hi": (ACC, "stat.error;phys.acceleration", "From the stellar-mass error only, at fixed R_E"),
    "g_bar_stars": (ACC, "phys.acceleration", "Stars inside the cylinder, default IMF"),
    "g_bar_gas_cold": (ACC, "phys.acceleration", "Cold gas inside the cylinder (registered gas term, D-076 item 1)"),
    "g_bar_gas_hot": (ACC, "phys.acceleration", "Hot gas inside the cylinder (registered gas term, D-076 item 1)"),
    "limit": (None, "meta.code", "none"),
    "stars_status": (None, "meta.code", "Stars: measured"),
    "gas_cold_status": (None, "meta.code", "Cold gas: modelled from the registered gas term"),
    "gas_hot_status": (None, "meta.code", "Hot gas: modelled from the registered gas term"),
    "observed_from": (None, "meta.ref", "Observable IDs feeding g_obs"),
    "baryonic_from": (None, "meta.ref", "Observable IDs feeding g_bar (including the IMF top where used)"),
    "model_dependence": (None, "meta.code", "total_mass_form where R_E is half the image separation (D-063 item 2)"),
    "evidence_tier": (None, "meta.code.qual", "Highest (weakest) tier among the inputs (D-035)"),
    "role": (None, "meta.code", "default or alternative"),
    "alternative_of": (None, "meta.id", "Default measurement this row is an alternative to"),
    "plotted": (None, "meta.code", "Plotted in the default view"),
    "not_plotted_reason": (None, "meta.note", "Why not plotted"),
    "assumptions": (None, "meta.note", "Registered assumptions (data/assumptions.json)"),
    "adjustable": (None, "meta.note", "Assumptions with a slider on this row"),
    "flags": (None, "meta.code", "Core flags (data standard §11)"),
    "source_ref": (None, "meta.ref", "Default observed and stellar-mass records (inventory R numbers)"),
    "notes": (None, "meta.note", "Reasons not plotted, or what the alternative replaces"),
    f"{X}projection": (None, "meta.code", "projected (D-064)"),
    f"{X}scope": (None, "meta.note", "Inventory scope (survey)"),
    f"{X}flags": (None, "meta.code", "Package flags (D-075, D-076), space-separated"),
    f"{X}theta_e_arcsec": ("arcsec", "phys.angSize", "Einstein radius (or aperture taken as R_E)"),
    f"{X}z_l": (None, "src.redshift", "Lens redshift used"),
    f"{X}z_s": (None, "src.redshift", "Source redshift used"),
    f"{X}h0": ("km / (Mpc s)", "phys.veloc.expansion", "Source's H0"),
    f"{X}om": (None, "meta.number", "Source's Omega_m (flat)"),
    f"{X}m_e_msun": ("solMass", "phys.mass", "Projected mass inside R_E"),
    f"{X}m_e_source": (None, "meta.code", "printed or computed (A6S_PRECEDENCE §2.4)"),
    f"{X}r_e_source": (None, "meta.code", "printed (kpc, R32) or computed"),
    f"{X}mstar_route": (None, "meta.code", "printed_in_RE, L_times_ML or profile"),
    f"{X}mstar_msun": ("solMass", "phys.mass", "Stellar mass as printed (inside R_E or total) or L x M/L"),
    f"{X}l_aperture_lsun": ("solLum", "phys.luminosity", "Luminosity inside R_E (band in observables)"),
    f"{X}ml": ("solMass / solLum", "phys.composition.massLightRatio", "Population M/L (named IMF)"),
    f"{X}r_eff_arcsec": ("arcsec", "phys.angSize", "Source's light-profile effective radius"),
    f"{X}sersic_n": (None, "meta.number", "Sersic index of the source's light profile (4 = de Vaucouleurs)"),
    f"{X}profile_fraction": (None, "arith.factor", "f(<R_E) from the source's light profile"),
    f"{X}mstar_re_msun": ("solMass", "phys.mass", "Stellar mass inside R_E at the default IMF"),
    f"{X}mstar_top_msun": ("solMass", "phys.mass", "Salpeter stellar mass inside R_E (IMF slider top); empty where not read"),
    f"{X}mstar_top_source": (None, "meta.ref", "Where the Salpeter top comes from"),
    f"{X}gas_term": (None, "meta.ref", "Registered gas term and its ruling"),
    f"{X}gas_statement": (None, "meta.note", "The source's own gas statement, where it makes one"),
    f"{X}gas_cold_frac": (None, "arith.factor", "Cold gas as a fraction of M*(<R_E), default"),
    f"{X}gas_cold_frac_min": (None, "arith.factor", "Cold gas fraction, registered minimum"),
    f"{X}gas_cold_frac_max": (None, "arith.factor", "Cold gas fraction, registered maximum"),
    f"{X}gas_hot_frac": (None, "arith.factor", "Hot gas as a fraction of M*(<R_E), default"),
    f"{X}gas_hot_frac_min": (None, "arith.factor", "Hot gas fraction, registered minimum"),
    f"{X}gas_hot_frac_max": (None, "arith.factor", "Hot gas fraction, registered maximum"),
}
OBS_SPEC = {
    "observable_id": (None, "meta.id;meta.main", "Observable identifier"),
    "system_id": (None, "meta.id", "Atlas system identifier"),
    "side": (None, "meta.code", "observed or baryonic"),
    "quantity": (None, "meta.code", "Data standard 2.1.0 §4a"),
    "value": (None, "meta.number", "Value in the unit of the row (log values converted to linear)"),
    "err_lo": (None, "stat.error", "Lower error, same unit"),
    "err_hi": (None, "stat.error", "Upper error, same unit"),
    "unit": (None, "meta.unit", "Astropy unit string"),
    "band": (None, "instr.bandpass", "Photometric band as the source names it"),
    "limit": (None, "meta.code", "none"),
    "steps": (None, "meta.note", "Ladder steps (data standard §4b)"),
    "evidence_tier": (None, "meta.code.qual", "D-035"),
    "source_ref": (None, "meta.ref", "Record, location and address"),
    f"{X}parameter": (None, "meta.note", "Reading note, or the alternative it is"),
    f"{X}role": (None, "meta.code", "Role of the input row (D-075, D-076)"),
    f"{X}printed": (None, "meta.note", "As printed: value, errors, form and unit"),
}
SYS_SPEC = {
    "system_id": (None, "meta.id;meta.main", "Atlas system identifier"),
    "name_in_source": (None, "meta.id", "Name as printed by the source"),
    "class_in_source": (None, "src.class", "Source's own kind label"),
    "taxonomy_kind": (None, "meta.code", "A0-A10 (D-063 item 6)"),
    "kind_label": (None, "meta.note", "Kind in words"),
    "host": (None, "meta.id", "Host system (none)"),
    "redshift": (None, "src.redshift", "Lens redshift as printed (default record)"),
    "redshift_err": (None, "stat.error;src.redshift", "As printed"),
    "distance_kinematic": (None, "meta.code", "false: spectroscopic redshifts, no kinematic distance"),
    "distance_ref": (None, "meta.ref", "Where the lens redshift was read"),
    "properties": (None, "meta.note", "Scope, status, reasons not plotted, z_s, gas statement, flags (JSON)"),
}


def write_tables(result: dict, out: Path, synthetic: bool) -> dict:
    meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    if synthetic:
        meta["SYNTHETIC"] = "made-up inputs and gas term, for code tests only; not Atlas data"
    (out / "tables").mkdir(parents=True, exist_ok=True)
    (out / "checks").mkdir(parents=True, exist_ok=True)
    tables = {}
    for name, spec in (("measurements", MEAS_SPEC), ("observables", OBS_SPEC), ("systems", SYS_SPEC)):
        if result[name]:
            t = _table(result[name], spec, meta)
            t.write(out / f"tables/{name}.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
            tables[name] = (f"tables/{name}.ecsv", t)
    for name in ("formula_check", "profile_step"):
        rows = result[name]
        if rows:
            t = _table(rows, {}, {**meta, "reported_not_pass_fail": "REPRODUCTION.md 'Reported'; D-075 item 5"})
            t.write(out / f"checks/{name}.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
        else:
            (out / f"checks/{name}.txt").write_text(
                f"{name}: no system in the inputs carries both quantities this check compares "
                "(e.g. R7 M_E for R5 models; R13 totals with a light profile).\n", encoding="utf-8")
    for name, cols in (("overlap", ("system", "scopes")), ("not_tabulated", ("scope", "system", "reason"))):
        with open(out / f"checks/{name}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(cols))
            w.writeheader()
            w.writerows(result[name])
    return tables


def read_back(path: Path) -> list[dict]:
    """Rows of a written ECSV table as plain dicts (masked -> None), for test 3 on the stored values."""
    import numpy as np
    from astropy.table import Table
    t = Table.read(path, format="ascii.ecsv")
    out = []
    for row in t:
        d = {}
        for k in t.colnames:
            v = row[k]
            if v is np.ma.masked:
                d[k] = None
            elif t[k].dtype.kind == "f":
                d[k] = None if math.isnan(float(v)) else float(v)
            elif t[k].dtype.kind in "iu":
                d[k] = int(v)
            else:
                d[k] = str(v) if str(v) != "" else None
        out.append(d)
    return out


def verify_frozen() -> None:
    rec = json.loads(FROZEN.read_text(encoding="utf-8"))
    for rel, h in rec["files"].items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != h:
            raise Refused(f"REFUSED: {rel} does not match its freeze record {FROZEN.name}")


def load_real_rows() -> tuple[list[dict], list[dict], list[dict]]:
    return merge_supplement(load_inputs(INPUTS), load_inputs(SUPPLEMENT))


# ----------------------------------------------------------------------------- entry point
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--synthetic-gas", action="store_true", help="synthetic tests only; writes only into --out")
    ap.add_argument("--inputs", type=Path, help="input CSV (synthetic runs only)")
    ap.add_argument("--out", type=Path, help="output folder (synthetic runs only; outside the package)")
    a = ap.parse_args(argv)
    try:
        if a.synthetic_gas:
            if a.inputs is None or a.out is None:
                raise Refused("REFUSED: --synthetic-gas needs --inputs and --out.")
            inp, out = a.inputs.resolve(), a.out.resolve()
            if inp in (INPUTS.resolve(), SUPPLEMENT.resolve()):
                raise Refused("REFUSED: --synthetic-gas never runs on the real inputs (blinding, D-075 item 1).")
            if out == HERE or HERE in out.parents:
                raise Refused("REFUSED: --synthetic-gas writes nothing into the package folder; choose --out elsewhere.")
            rows = load_inputs(inp)
            if not rows or not all(r["scope"].startswith("SYNTHETIC") for r in rows):
                raise Refused("REFUSED: --synthetic-gas needs every input row's scope to begin with 'SYNTHETIC'.")
            gas = parse_gas_term(SYNTHETIC_GAS, synthetic=True)
            result = convert(rows, gas, synthetic=True)
            arithmetic_check(result["measurements"])
            write_tables(result, out, synthetic=True)
            if result["measurements"]:
                arithmetic_check(read_back(out / "tables/measurements.ecsv"))
            print(f"SYNTHETIC: wrote {len(result['measurements'])} measurements, {len(result['systems'])} systems to {out}")
            return 0
        if a.inputs is not None or a.out is not None:
            raise Refused("REFUSED: --inputs and --out are for --synthetic-gas only.")
        gas = load_gas_term()
        if gas is None:
            # Not a failure: the package is waiting on a ruling (D-075 item 1). Nothing is written,
            # and CI passes so other pull requests are not blocked.
            print("SKIPPED: " + REFUSAL)
            return 0
        verify_frozen()
        if not (HERE / "descriptor.json").is_file():
            raise Refused("REFUSED: descriptor.json is not written yet. Nothing was written.")
        rows, aside, outside = load_real_rows()
        result = convert(rows, gas, synthetic=False)
        released = released_file_check(result["used_rows"], HERE / "source")
        bad = [r for r in released if r["found"] != "yes"]
        if bad:
            raise Refused(f"REFUSED: {len(bad)} tier-1 numbers not found in their released files, e.g. {bad[:3]}. "
                          "Nothing was written.")
        n3 = arithmetic_check(result["measurements"])
        result["not_tabulated"] += [{"scope": r["scope"], "system": r["system"],
                                     "reason": "R7 record-only lens outside the SLACS V adjudicated set: no theta_E, no kind and "
                                               "no redshift row in the inputs; SLACS IX new models have no stellar-mass default "
                                               "(REPRODUCTION.md, Surveys in v1)"} for r in outside]
        tables = write_tables(result, HERE, synthetic=False)
        with open(HERE / "checks/released_files.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["system", "record", "quantity", "part", "value", "file", "found"])
            w.writeheader()
            w.writerows(released)
        n3b = arithmetic_check(read_back(HERE / "tables/measurements.ecsv"))
        from aeg.package import write_checksums, write_datapackage
        desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
        write_datapackage(HERE, desc, tables)
        write_checksums(HERE)
        print(f"wrote {len(result['measurements'])} measurements, {len(result['observables'])} observables, "
              f"{len(result['systems'])} systems; released-file check {len(released)} of {len(released)} numbers found; "
              f"test 3 passes ({n3} comparisons in memory, {n3b} on the stored table)")
        return 0
    except Refused as e:
        print(e.code, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
