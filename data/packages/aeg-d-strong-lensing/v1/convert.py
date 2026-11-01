"""Convert the A6 strong-lensing inputs into the Atlas data standard 2.0.0.

Usage
    python data/packages/aeg-d-strong-lensing/v1/convert.py
        Real conversion. Skips (exit 0, nothing written) until the gas term is set: the file
        gas_term.json beside this script, written only after JvH rules on the gas default and
        range (D-075 item 1). AEG_REGISTER=1 once, by the maintainer, adds new systems to
        data/registry/systems.csv, as aeg-d-dwarfs/v1 does.
    python .../convert.py --synthetic-gas --inputs SYNTHETIC.csv --out DIR
        Synthetic tests only. Uses a made-up gas term labelled SYNTHETIC, accepts only an input
        file whose every row has a scope beginning "SYNTHETIC", never the real inputs, never
        touches the registry, and writes only into DIR, which must lie outside this package.

Rules applied (nothing beyond them):
    REPRODUCTION.md (frozen, D-065); docs/methods/A6S_PRECEDENCE.md (frozen, D-065);
    D-063, D-064, D-066 and D-075 (rulings on reading/adjudication.md Q1-Q14).

Per system, in projection at the Einstein radius (D-064):
    M_E       printed by the default record; where only theta_E is printed,
              M_E = theta_E^2 c^2 D_s D_l / (4 G D_ls) in the source's cosmology (aeg.lensing)
    R_E       theta_E D_l in the same cosmology (aeg.lensing); R32 prints R_E in kpc and names its
              cosmology only, so the printed R_E is used (D-075 item 4, flag R_E_printed_kpc)
    M*(<R_E)  printed inside R_E; or L(<R_E) x population M/L (D-075 item 3, mstar_from_L_times_ML);
              or total x f(<R_E) from the source's own de Vaucouleurs / Sersic fit
              (aeg.lensing.sersic_projected_fraction; flag mstar_in_RE_from_profile)
    M_gas     the registered gas term (gas_term.json), never derived from the observed side
    g_obs     G M_E / R_E^2,  g_bar = G (M* + M_gas) / R_E^2  (aeg.lensing.projected_acceleration),
              labelled projected (r_kind = projected, x_sl_projection = projected)
    errors    g_obs from the M_E error, g_bar from the stellar-mass error, both at fixed R_E
              (the radius is the coordinate; distance errors are not added, REPRODUCTION.md).

Reported checks (written to checks/, not pass/fail), computed only on a real run:
    formula_check.ecsv   REPRODUCTION.md "Reported" item 1 / A6S_PRECEDENCE §4: M_E from theta_E by
                         the §2.4 formula against the printed M_E, wherever one system has both
                         (R7's printed M_E for R5's models enters when R7 rows are in the inputs).
    profile_step.ecsv    D-075 item 5: the profile step on a record's printed total against the same
                         record's printed mass inside R_E (R13 for SLACS, when its totals and light
                         profile are in the inputs).
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

DATASET, VERSION, STANDARD = "aeg-d-strong-lensing", "v1", "2.0.0"
PID = f"{DATASET}/{VERSION}"
TODAY = "2026-11-01"
INPUTS = HERE / "reading/adjudicated_inputs.csv"
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

# Core flags (data standard 2.0.0 §11); everything else goes to x_sl_flags.
CORE_FLAGS = {"no_uncertainty"}
ASSUMPTIONS = ("sl_gr_lensing;sl_source_cosmology;sl_projected_cylinder;sl_redshifts_spectroscopic;"
               "sl_mstar_population;sl_stellar_imf;sl_mstar_profile;sl_gas_in_RE")

# Proposed registry entries (written into data/assumptions.json only after review; not now).
# p is the slider position. IMF: 0 = Chabrier/Kroupa default, 1 = Salpeter top (A6S_PRECEDENCE §3.2).
# Gas: -1 = registered minimum, 0 = default, +1 = maximum, as a fraction of M*(<R_E) at the default IMF.
PROPOSED_SLIDERS = {
    "sl_stellar_imf": [
        {"column": "g_bar_stars", "formula": "g_bar_stars * (1 + (x_sl_mstar_top_msun / x_sl_mstar_re_msun - 1) * p)"},
        {"column": "g_bar_err_lo", "formula": "g_bar_err_lo * (1 + (x_sl_mstar_top_msun / x_sl_mstar_re_msun - 1) * p)"},
        {"column": "g_bar_err_hi", "formula": "g_bar_err_hi * (1 + (x_sl_mstar_top_msun / x_sl_mstar_re_msun - 1) * p)"},
    ],
    "sl_gas_in_RE": "per component c: g_bar_gas_c = g_bar_stars_default * (f + (f_max - f_min) / 2 * p "
                    "+ (f_max + f_min - 2 f) / 2 * abs(p)), with f, f_min, f_max from x_sl_<c>_frac[_min|_max]",
}

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
# D-075 item 1 (Q14): systems whose sources state gas inside R_E negligible. Kept as quoted source
# assumptions (adjudication.md §5 quotes them); what the gas term does for them is set in gas_term.json.
GAS_SOURCE_NEGLIGIBLE = {
    "ESO 325-G004": "R28 footnote 3; R25 §4",
    "ESO 286-G022": "R25 §4",
    "2MASX J01414232-0735281": "R25 §4",
    "SDSS J1436+4943": "R32 §5",
    "SDSS J1701+3722": "R32 §5",
}


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
        assumption_id   registry id (e.g. "sl_gas_in_RE")
        decision        the decision-log entry that ruled it (D-075 item 1 follow-up)
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
    """Role of one input row under D-075, and the package flags it brings. Unknown status: error."""
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
        return "arcsec"
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
    record_level, systems = {}, {}
    for r in rows:
        if r["system"] == "(record)":
            record_level.setdefault((r["scope"], r["record"]), {})[r["quantity"]] = r
            continue
        s = systems.setdefault((r["scope"], r["system"]), System(r["scope"], r["system"]))
        role, fl = resolve(r)
        s.rows.append({**r, "_role": role})
        s.flags += fl
    return list(systems.values()), record_level


def pick(s: System, q: str, role: str = "default", record: str | None = None) -> list[dict]:
    return [r for r in s.rows if r["quantity"] == q and r["_role"] == role and (record is None or r["record"] == record)]


def one(s: System, q: str, record: str | None = None) -> dict | None:
    xs = pick(s, q, record=record)
    if len(xs) > 1:
        raise ValueError(f"{s.name}: {len(xs)} default rows for {q}")
    return xs[0] if xs else None


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
    h = one(s, "H0", record) or record_level.get((s.scope, record), {}).get("H0")
    om = one(s, "Om", record) or record_level.get((s.scope, record), {}).get("Om")
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
    conv = COSMOLOGY_CONVENTION.get(I.obs_record, "flat_from_omega_lambda")
    I.flags.append(conv)
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
        # Salpeter top: same variant, or the source's printed conversion (D-075 item 5)
        role = "top" if sub is None or sub["quantity"] != "mstar" else "alt_top"
        tops = [r for r in s.rows if r["quantity"] == "mstar" and r["_role"] == role and variant_key(r) == variant_key(ms)]
        if tops:
            I.top, I.top_source = value_with_errors(tops[0])[0], f"{tops[0]['record']} printed Salpeter"
            I.st_rows += (tops[0],)
    elif lap is not None and mlr is not None:  # D-075 item 3 (Q3)
        I.st_record, I.st_rows, I.st_route = lap["record"], (lap, mlr), "L_times_ML"
        l, llo, lhi = value_with_errors(lap)
        u, ulo, uhi = value_with_errors(mlr)
        I.l_ap, I.ml, I.mstar = l, u, l * u
        if llo is not None or ulo is not None:  # relative errors in quadrature (D-075 Q3 (a))
            I.mstar_lo = I.mstar * math.hypot((llo or 0) / l, (ulo or 0) / u)
            I.mstar_hi = I.mstar * math.hypot((lhi or 0) / l, (uhi or 0) / u)
        if ulo is None and uhi is None:
            I.flags.append("no_uncertainty")  # D-075 Q3 (a): e.g. R61 Upsilon_ref has no printed error
        I.flags.append("mstar_from_L_times_ML")
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
        conv_rows = [r for r in s.rows if r["quantity"] in ("chab_to_salp_factor", "imf_alpha_salpeter") and r["_role"] == "default"]
        if conv_rows:
            c = conv_rows[0]
            I.top = I.mstar / num(c["value"]) if c["quantity"] == "chab_to_salp_factor" else I.mstar * num(c["value"])
            I.top_source = f"{c['record']} printed conversion ({c['quantity']} = {c['value']})"
            I.st_rows += (c,)
        else:
            I.flags.append("imf_top_not_read")  # model-paper ratio (D-075 item 5) not yet in the inputs
    return I


def plotting_conditions(s: System, I: Inputs) -> None:
    tk, label, cls, ok, why = classify_kind(s)
    s.kind = (tk, label, cls)
    if not ok:
        s.reasons.append(why)
    ro = sorted({r["status"] for r in s.rows if r["_role"] == "record_only"})
    if ro and ok:
        s.reasons.append("; ".join(ro))
    zl = next((r for r in I.z_rows if r["quantity"] == "z_l"), None)
    zs = next((r for r in I.z_rows if r["quantity"] == "z_s"), None)
    if not (is_spectroscopic(zl) and is_spectroscopic(zs)):
        s.reasons.append("lens and source redshifts not both spectroscopic in the inputs (D-063 item 5)")
    if I.z_l is not None and not I.z_l < Z_CUT:
        s.reasons.append(f"printed z_l = {I.z_l} is not below {Z_CUT} (D-066)")
        s.flags.append("epoch_gap_v1")


# ----------------------------------------------------------------------------- computation
def compute(I: Inputs, gas: GasTerm, source_negligible: bool) -> dict:
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
        frac = 0.0 if source_negligible and gas.source_negligible == "zero" else c.default
        out["gas"][c.name] = (frac, c.minimum, c.maximum, L.projected_acceleration(frac * out["mstar_re"], r))
    out["g_bar"] = out["g_bar_stars"] + sum(v[3] for v in out["gas"].values())
    ks = out["g_bar_stars"] / out["mstar_re"]
    out["g_bar_lo"] = out["mstar_re_lo"] * ks if out["mstar_re_lo"] is not None else None
    out["g_bar_hi"] = out["mstar_re_hi"] * ks if out["mstar_re_hi"] is not None else None
    return out


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
    """§2.4 formula against every printed M_E whose system also has a printed theta_E (any record)."""
    out = []
    for s in systems:
        ths = [r for r in s.rows if r["quantity"] == "theta_E" and r["_role"] in ("default", "alternative")]
        mes = [r for r in s.rows if r["quantity"] == "M_E" and r["_role"] in ("default", "alternative")]
        zl = next((r for r in s.rows if r["quantity"] == "z_l" and r["_role"] == "default"), None)
        zs = next((r for r in s.rows if r["quantity"] == "z_s" and r["_role"] == "default"), None)
        for th in ths:
            h0, om, _ = cosmology(s, record_level, th["record"])
            for me in mes:
                # the same record, or R7's printed M_E for R5's models (REPRODUCTION.md, Observed side)
                same = me["record"] == th["record"] or (me["record"], th["record"]) == ("R7", "R5")
                if not same or None in (h0, om, zl, zs):
                    continue
                comp = L.einstein_mass_msun(num(th["value"]), num(zl["value"]), num(zs["value"]), h0, om)
                printed = value_with_errors(me)[0]
                out.append({"name": s.name, "scope": s.scope, "record_theta": th["record"], "record_m_e": me["record"],
                            "theta_arcsec": num(th["value"]), "z_l": num(zl["value"]), "z_s": num(zs["value"]),
                            "h0": h0, "om": om, "m_e_computed": comp, "m_e_printed": printed, "ratio": comp / printed})
    return out


def profile_step_check(systems: list[System]) -> list[dict]:
    """D-075 item 5: a record's total x f(<R_E) against the same record's printed mass inside R_E."""
    out = []
    for s in systems:
        ms = [r for r in s.rows if r["quantity"] in ("mstar", "mstar_total")]
        tot = [r for r in ms if r["quantity"] == "mstar_total" or re.search(r"\btotal\b", r.get("note", ""))]
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


# ----------------------------------------------------------------------------- conversion
def convert(rows: list[dict], gas: GasTerm, synthetic: bool) -> dict:
    """All rows of all tables, as plain dicts. No file is touched."""
    systems, record_level = group_systems(rows)
    ids = registry([primary_name(s.scope, s.name) for s in systems], synthetic)
    meas, obs, sysrows = [], [], []

    def add_obs(sid, side, q, r, steps, param="", value=None, unit=None):
        v, lo, hi = value_with_errors(r) if value is None else (value, None, None)
        oid = f"{PID}/o{len(obs) + 1:06d}"
        band = re.search(r"\((\w+)\)", r.get("unit", ""))
        obs.append({"observable_id": oid, "system_id": sid, "side": side, "quantity": q, "value": v, "err_lo": lo,
                    "err_hi": hi, "unit": unit or astropy_unit(r),
                    "band": band.group(1) if band and q in ("luminosity", "stellar_ml_population") else "", "limit": "none",
                    "steps": steps, "evidence_tier": tier(r),
                    "source_ref": f"{r['record']}: {r['location']} ({r['url']})", "x_sl_parameter": param or r.get("note", "")[:200],
                    "x_sl_role": r["_role"]})
        return oid

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

    for s in systems:
        sid = ids[primary_name(s.scope, s.name)]
        I = assemble(s, record_level)
        plotting_conditions(s, I)
        where = GAS_SOURCE_NEGLIGIBLE.get(primary_name(s.scope, s.name))
        if where:
            s.gas_statement = f"source states gas inside R_E negligible ({where}; an assumption, not a measurement)"
            s.flags.append("gas_negligible_source_assumption")
        complete = not s.incomplete
        sysrows.append({"system_id": sid, "name_in_source": s.name, "class_in_source": s.kind[2] or "not stated",
                        "taxonomy_kind": s.kind[0], "kind_label": s.kind[1], "host": "",
                        "redshift": I.z_l, "redshift_err": None, "distance_kinematic": "false",
                        "properties": json.dumps({"scope": s.scope, "status": "plotted" if complete and not s.reasons else "recorded",
                                                  "reasons_not_plotted": s.reasons + s.incomplete, "z_s": I.z_s,
                                                  "gas_statement": s.gas_statement or None,
                                                  "flags": sorted(set(s.flags + I.flags))}, ensure_ascii=False, sort_keys=True)})
        if not complete:
            continue
        o_ids, b_ids = [], []
        for r in (I.theta_row, I.m_e_row, I.r_e_row) + I.z_rows:
            if r is not None:
                side, q, steps = QMAP[r["quantity"]]
                o_ids.append(add_obs(sid, side, q, r, steps))
        for r in I.st_rows + I.profile_rows:
            if r["quantity"] in QMAP:
                side, q, steps = QMAP[r["quantity"]]
                b_ids.append(add_obs(sid, side, q, r, steps))
        for r in s.rows:  # alternatives recorded as observables (D-075 items 2, 5; Q1, Q13)
            if r["_role"] in ("alternative", "alt_top") and r["quantity"] in QMAP:
                side, q, steps = QMAP[r["quantity"]]
                add_obs(sid, side, q, r, steps, param=f"alternative: {r.get('note', '')[:180]}")
        c = compute(I, gas, bool(s.gas_statement))
        default_id = f"{PID}/m{len(meas) + 1:06d}"
        meas.append(measurement_row(default_id, sid, s, I, c, gas, o_ids, b_ids, role="default"))
        # alternative measurement rows: one input replaced (stellar mass variant, light profile, lens redshift)
        used = {r["quantity"]: r["record"] for r in (I.st_rows + I.profile_rows + I.z_rows)}
        for r in s.rows:
            # only an alternative from the same record as the default input it replaces (no mixed records)
            if r["_role"] != "alternative" or r["quantity"] not in ("mstar", "R_e", "z_l") or used.get(r["quantity"]) != r["record"]:
                continue
            keep = (list(s.incomplete), list(s.reasons))
            Ia = assemble(s, record_level, sub=r)
            if len(s.incomplete) > len(keep[0]):
                s.incomplete[:], s.reasons[:] = keep
                continue
            s.incomplete[:], s.reasons[:] = keep
            ca = compute(Ia, gas, bool(s.gas_statement))
            mid = f"{PID}/m{len(meas) + 1:06d}"
            meas.append(measurement_row(mid, sid, s, Ia, ca, gas, o_ids, b_ids, role="alternative",
                                        alternative_of=default_id, alt_note=f"{r['quantity']} = {r['value']} ({r['record']}; {r.get('note', '')[:120]})"))
    return {"measurements": meas, "observables": obs, "systems": sysrows,
            "formula_check": formula_check(systems, record_level), "profile_step": profile_step_check(systems),
            "systems_obj": systems}


def measurement_row(mid, sid, s, I, c, gas, o_ids, b_ids, role, alternative_of=None, alt_note=None) -> dict:
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
    adjustable = ";".join(a for a, ok in (("sl_stellar_imf", c["top_re"] is not None), (gas.assumption_id, True)) if ok)
    row = {
        "measurement_id": mid, "system_id": sid, "kind": "system_value", "channel": "lensing", "method_class": "lensing",
        "method": ("projected mass inside the Einstein radius against the projected stellar mass inside the same cylinder, "
                   "both as G M / R_E^2 (D-064); M_E " + I.m_e_source + "; stellar mass " + I.st_route),
        "measured_quantity": "g_obs", "r_kpc": c["r_e"], "r_kind": "projected",
        "g_obs": c["g_obs"], "g_obs_err_lo": c["g_obs_lo"], "g_obs_err_hi": c["g_obs_hi"],
        "g_bar": c["g_bar"], "g_bar_err_lo": c["g_bar_lo"], "g_bar_err_hi": c["g_bar_hi"],
        "g_bar_stars": c["g_bar_stars"],
        "g_bar_gas_cold": c["gas"].get("gas_cold", (None,) * 4)[3], "g_bar_gas_hot": c["gas"].get("gas_hot", (None,) * 4)[3],
        "limit": "none", "stars_status": "measured",
        "gas_cold_status": ("absent" if s.gas_statement and gas.source_negligible == "zero" else "modelled") if "gas_cold" in c["gas"] else "absent",
        "gas_hot_status": ("absent" if s.gas_statement and gas.source_negligible == "zero" else "modelled") if "gas_hot" in c["gas"] else "absent",
        "observed_from": ";".join(o_ids), "baryonic_from": ";".join(b_ids),
        "model_dependence": "total_mass_form" if "model_dependence_half_image_separation" in fl else "none",
        "evidence_tier": max(tier(r) for r in (I.theta_row, I.m_e_row, I.r_e_row) + I.z_rows + I.st_rows + I.profile_rows if r),
        "role": role, "alternative_of": alternative_of, "plotted": "true" if plotted else "false",
        "not_plotted_reason": reason, "assumptions": ASSUMPTIONS.replace("sl_gas_in_RE", gas.assumption_id),
        "adjustable": adjustable, "flags": ";".join(core),
        "source_ref": f"observed {I.obs_record}; stellar {I.st_record}", "notes": note,
        "x_sl_projection": "projected", "x_sl_scope": s.scope,
        "x_sl_flags": " ".join(f for f in fl if f not in CORE_FLAGS),
        "x_sl_theta_e_arcsec": I.theta, "x_sl_z_l": I.z_l, "x_sl_z_s": I.z_s, "x_sl_h0": I.h0, "x_sl_om": I.om,
        "x_sl_m_e_msun": c["m_e"], "x_sl_m_e_source": I.m_e_source,
        "x_sl_r_e_source": "printed" if I.r_e_printed is not None else "computed",
        "x_sl_mstar_route": I.st_route, "x_sl_mstar_msun": I.mstar, "x_sl_l_aperture_lsun": I.l_ap, "x_sl_ml": I.ml,
        "x_sl_r_eff_arcsec": I.r_eff, "x_sl_sersic_n": I.n, "x_sl_profile_fraction": c["f"],
        "x_sl_mstar_re_msun": c["mstar_re"], "x_sl_mstar_top_msun": c["top_re"], "x_sl_mstar_top_source": I.top_source,
        "x_sl_gas_term": f"{gas.assumption_id} ({gas.decision})" + (" SYNTHETIC" if gas.synthetic else ""),
        "x_sl_gas_statement": s.gas_statement,
    }
    for name in ("gas_cold", "gas_hot"):
        g = c["gas"].get(name)
        row[f"x_sl_{name}_frac"], row[f"x_sl_{name}_frac_min"], row[f"x_sl_{name}_frac_max"] = (g[0], g[1], g[2]) if g else (None, None, None)
    return row


def arithmetic_check(meas_rows: list[dict]) -> None:
    """REPRODUCTION.md test 3: recompute every derived column from the stored inputs, to 1e-9."""
    def close(a, b, what, mid):
        if a is None or b is None or abs(a / b - 1) > TOL:
            raise SystemExit(f"arithmetic test 3 failed at {mid}: {what} ({a} vs {b})")
    for r in meas_rows:
        mid = r["measurement_id"]
        if r["x_sl_m_e_source"] == "computed":
            close(L.einstein_mass_msun(r["x_sl_theta_e_arcsec"], r["x_sl_z_l"], r["x_sl_z_s"], r["x_sl_h0"], r["x_sl_om"]),
                  r["x_sl_m_e_msun"], "M_E", mid)
        if r["x_sl_r_e_source"] == "computed":
            close(L.einstein_radius_kpc(r["x_sl_theta_e_arcsec"], r["x_sl_z_l"], r["x_sl_h0"], r["x_sl_om"]), r["r_kpc"], "R_E", mid)
        m = r["x_sl_mstar_msun"]
        if r["x_sl_mstar_route"] == "L_times_ML":
            close(r["x_sl_l_aperture_lsun"] * r["x_sl_ml"], m, "L x M/L", mid)
        if r["x_sl_mstar_route"] == "profile":
            f = L.sersic_projected_fraction(r["x_sl_theta_e_arcsec"], r["x_sl_r_eff_arcsec"], r["x_sl_sersic_n"])
            close(f, r["x_sl_profile_fraction"], "f(<R_E)", mid)
            m = m * f
        close(m, r["x_sl_mstar_re_msun"], "M*(<R_E)", mid)
        close(L.projected_acceleration(r["x_sl_m_e_msun"], r["r_kpc"]), r["g_obs"], "g_obs", mid)
        gs = L.projected_acceleration(m, r["r_kpc"])
        close(gs, r["g_bar_stars"], "g_bar_stars", mid)
        gas = sum(L.projected_acceleration((r[f"x_sl_{c}_frac"] or 0.0) * m, r["r_kpc"]) for c in ("gas_cold", "gas_hot"))
        close(gs + gas, r["g_bar"], "g_bar", mid)


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
    "r_kpc": ("kpc", "phys.size.radius", "Einstein radius R_E (projected)"),
    "g_obs": (ACC, "phys.acceleration", "Observed acceleration in projection, G M_E / R_E^2 (D-064)"),
    "g_obs_err_lo": (ACC, "stat.error;phys.acceleration", "From the M_E error at fixed R_E"),
    "g_obs_err_hi": (ACC, "stat.error;phys.acceleration", "From the M_E error at fixed R_E"),
    "g_bar": (ACC, "phys.acceleration", "Baryonic acceleration in projection, G (M*(<R_E) + M_gas(<R_E)) / R_E^2 (D-064)"),
    "g_bar_err_lo": (ACC, "stat.error;phys.acceleration", "From the stellar-mass error only, at fixed R_E"),
    "g_bar_err_hi": (ACC, "stat.error;phys.acceleration", "From the stellar-mass error only, at fixed R_E"),
    "g_bar_stars": (ACC, "phys.acceleration", "Stars inside the cylinder"),
    "g_bar_gas_cold": (ACC, "phys.acceleration", "Cold gas inside the cylinder (registered gas term)"),
    "g_bar_gas_hot": (ACC, "phys.acceleration", "Hot gas inside the cylinder (registered gas term)"),
    "x_sl_theta_e_arcsec": ("arcsec", "phys.angSize", "Einstein radius (or aperture taken as R_E)"),
    "x_sl_m_e_msun": ("solMass", "phys.mass", "Projected mass inside R_E"),
    "x_sl_mstar_msun": ("solMass", "phys.mass", "Stellar mass as printed (inside R_E or total) or L x M/L"),
    "x_sl_mstar_re_msun": ("solMass", "phys.mass", "Stellar mass inside R_E at the default IMF"),
    "x_sl_mstar_top_msun": ("solMass", "phys.mass", "Salpeter stellar mass inside R_E (IMF slider top); empty where not yet read"),
    "x_sl_l_aperture_lsun": ("solLum", "phys.luminosity", "Luminosity inside R_E (band in observables)"),
    "x_sl_ml": ("solMass / solLum", "phys.composition.massLightRatio", "Population M/L (named IMF)"),
    "x_sl_r_eff_arcsec": ("arcsec", "phys.angSize", "Source's light-profile effective radius"),
    "x_sl_h0": ("km / (Mpc s)", "cosmo.parameter", "Source's H0"),
}


def write_tables(result: dict, out: Path, synthetic: bool) -> None:
    meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
    if synthetic:
        meta["SYNTHETIC"] = "made-up inputs and gas term, for code tests only; not Atlas data"
    (out / "tables").mkdir(parents=True, exist_ok=True)
    (out / "checks").mkdir(parents=True, exist_ok=True)
    for name, spec in (("measurements", MEAS_SPEC), ("observables", {}), ("systems", {})):
        if result[name]:
            _table(result[name], spec, meta).write(out / f"tables/{name}.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
    for name in ("formula_check", "profile_step"):
        rows = result[name]
        if rows:
            t = _table(rows, {}, {**meta, "reported_not_pass_fail": "REPRODUCTION.md 'Reported'; D-075 item 5"})
            t.write(out / f"checks/{name}.ecsv", format="ascii.ecsv", delimiter=",", overwrite=True)
        else:
            (out / f"checks/{name}.txt").write_text(
                f"{name}: no system in the inputs carries both quantities this check compares "
                "(e.g. R7 M_E for R5 models; R13 totals with a light profile).\n", encoding="utf-8")


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
            if inp == INPUTS.resolve():
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
        result = convert(load_inputs(INPUTS), gas, synthetic=False)
        write_tables(result, HERE, synthetic=False)
        from astropy.table import Table
        arithmetic_check(read_back(HERE / "tables/measurements.ecsv"))
        from aeg.package import write_checksums, write_datapackage
        desc = json.loads((HERE / "descriptor.json").read_text(encoding="utf-8"))
        meta = {"dataset": DATASET, "version": VERSION, "standard_version": STANDARD}
        write_datapackage(HERE, desc, {n: (f"tables/{n}.ecsv", _table(result[n], MEAS_SPEC if n == "measurements" else {}, meta))
                                       for n in ("measurements", "observables", "systems")})
        write_checksums(HERE)
        print(f"wrote {len(result['measurements'])} measurements, {len(result['observables'])} observables, "
              f"{len(result['systems'])} systems; test 3 passes")
        return 0
    except Refused as e:
        print(e.code, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
