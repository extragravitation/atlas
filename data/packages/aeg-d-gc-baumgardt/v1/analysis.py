"""aeg-d-gc-baumgardt/v1: conversion under D-025, D-036, D-038, D-039, D-042, D-045, D-046.

Pure computation from the source files; `convert.py` writes the tables.
Everything here follows REPRODUCTION.md (frozen); no tuning.
"""

from __future__ import annotations

import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[3] / "pipeline"))

import astropy.constants as const  # noqa: E402
import astropy.units as u  # noqa: E402

from aeg import dispersion as D  # noqa: E402
from aeg.king66 import King66  # noqa: E402
from sources_io import LOS_TYPES, PM_TYPES, norm_name, read_harris, read_veldis, read_votable  # noqa: E402

SRC = HERE / "source"
M_V_SUN = 4.85            # McLaughlin & van der Marel (2005) §4.2: "M_V,⊙ = +4.85 (Lang 1999)"
WOLF_FACTOR = 4.0 / 3.0   # r½ = 4/3 R_h (Wolf et al. 2010), registered assumption (D-025)
ARCSEC_PER_RAD = 206264.806
YEAR = {"RV": None, "F13": 2013, "L13": 2013, "L15": 2015, "K18": 2018, "D21": 2021, "C22": 2022, "G22": 2022}
A7 = {"CRATER"}           # D-038 4A: classification disputed (Crater / Laevens I)
RECORD_ONLY = {"PAL1": "source structural parameters internally inconsistent (scale radius in pc vs angular "
                       "radius × distance; reproduction test 2, D-046)"}

G = const.G.to_value(u.m ** 3 / (u.kg * u.s ** 2))
M_SUN = const.M_sun.to_value(u.kg)
PC = const.pc.to_value(u.m)


@dataclass
class Candidate:
    dataset: str
    bins: list[dict]
    n_star: int
    result: D.Result | None = None
    refused: str = ""

    @property
    def plotted(self) -> bool:
        return self.result is not None and self.result.plotted


@dataclass
class System:
    name: str
    key: str
    harris: dict | None = None
    king_row: dict | None = None
    pop_row: dict | None = None
    candidates: list[Candidate] = field(default_factory=list)
    pm_bins: list[dict] = field(default_factory=list)
    model: King66 | None = None
    model_source: str = ""
    distance_kpc: float | None = None
    r_h_pc: float | None = None
    r_h_source: str = ""
    l_v: float | None = None
    ml_v: float | None = None
    default: Candidate | None = None
    reasons: list[str] = field(default_factory=list)
    kind: str = "A3"
    g_obs: float | None = None
    g_bar: float | None = None
    r_half_pc: float | None = None


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def load():
    veldis = read_veldis(SRC / "veldis.html")
    harris = {norm_name(k): v for k, v in read_harris(SRC / "mwgc.dat").items()}
    king = {norm_name(r["Cluster"]): r for r in read_votable(SRC / "mvdm05/J_ApJS_161_304_models.vot")
            if r["Cluster"].startswith("MW-") and r["Mod"] == "K"}
    pop = {norm_name(r["Cluster"]): r for r in read_votable(SRC / "mvdm05/J_ApJS_161_304_clusters.vot")
           if r["Cluster"].startswith("MW-")}
    return veldis, harris, king, pop


def harris_core_flag(h: dict) -> str:
    return h.get("III:flags", "")


def build(harris_rc_as_r0: bool = True) -> list[System]:
    veldis, harris, king, pop = load()
    systems: dict[str, System] = {}
    for row in veldis:
        key = norm_name(row["cluster"])
        s = systems.setdefault(key, System(row["cluster"], key, harris.get(key), king.get(key), pop.get(key)))
        if row["type"] in PM_TYPES:
            s.pm_bins.append(row)
            continue
        if row["type"] not in LOS_TYPES:
            raise ValueError(f"unknown profile type {row['type']}")
        c = next((c for c in s.candidates if c.dataset == row["type"]), None)
        if c is None:
            c = Candidate(row["type"], [], 0)
            s.candidates.append(c)
        c.bins.append(row)
        c.n_star += int(row["n_star"]) if row["n_star"].strip() else 0  # IFU datasets give no counts: rank as 0 (D-038 3B)

    for s in systems.values():
        if s.key in A7:
            s.kind = "A7"
            s.reasons.append("classification disputed by sources: A7, ambiguous (D-038 4A)")
        # distance (D-042)
        if s.harris and num(s.harris.get("I:R_Sun")):
            s.distance_kpc = num(s.harris["I:R_Sun"])
        else:
            s.reasons.append("no Harris (2010) horizontal-branch distance (D-042)")
        # structural model (D-045 item 2) and R_h (item 3)
        if s.king_row:
            s.model = King66(float(s.king_row["W0/gamma"]), float(s.king_row["r0"]))  # r0 in arcsec
            s.model_source = "McLaughlin & van der Marel 2005, King (1966) fit"
            if s.distance_kpc:
                s.r_h_pc = 10 ** float(s.king_row["Rh"]) * s.distance_kpc / float(s.king_row["Dist"])
                s.r_h_source = "McLaughlin & van der Marel 2005 R_h, rescaled to the Harris distance"
        elif s.harris and num(s.harris.get("III:c")) and num(s.harris.get("III:r_c")):
            if harris_core_flag(s.harris):
                s.reasons.append(f"Harris c carries a core-collapse flag ('{harris_core_flag(s.harris)}') and there is no "
                                 "McLaughlin & van der Marel fit")
            elif not harris_rc_as_r0:
                s.reasons.append("Harris r_c reading rejected by reproduction test 4; Harris-only clusters recorded")
            else:
                s.model = King66.from_concentration(float(s.harris["III:c"]), float(s.harris["III:r_c"]) * 60.0)
                s.model_source = "Harris 2010 c and r_c, read as log(r_t/r0) and r0 (D-045)"
            if s.distance_kpc and num(s.harris.get("III:r_h")):
                s.r_h_pc = float(s.harris["III:r_h"]) * 60.0 / ARCSEC_PER_RAD * s.distance_kpc * 1000.0
                s.r_h_source = "Harris 2010 r_h at the Harris distance"
        else:
            s.reasons.append("no structural model (no McLaughlin & van der Marel fit; no Harris c and r_c)")
        if s.model and not s.r_h_pc and s.distance_kpc:
            s.reasons.append("no half-light radius")
        # luminosity (D-045 item 4) and M/L (D-039)
        if s.harris and num(s.harris.get("II:M_V,t")) is not None:
            s.l_v = 10 ** (-0.4 * (float(s.harris["II:M_V,t"]) - M_V_SUN))
        else:
            s.reasons.append("no Harris integrated magnitude")
        if s.pop_row and num(s.pop_row.get("(M/L)1")):
            s.ml_v = float(s.pop_row["(M/L)1"])
        else:
            s.reasons.append("no tabulated population M/L_V (metallicity interpolation not yet frozen, D-039)")
        if s.key in RECORD_ONLY:
            s.reasons.append(RECORD_ONLY[s.key])

        # candidates (D-045 item 1; D-036 ii)
        for c in s.candidates:
            bins = sorted(c.bins, key=lambda b: float(b["r_arcsec"]))
            if s.model is None:
                c.refused = "no structural model"
                continue
            try:
                bb = D.bins_from_radii([float(b["r_arcsec"]) for b in bins], [float(b["sigma"]) for b in bins],
                                       [float(b["err_lo"]) for b in bins], [float(b["err_hi"]) for b in bins])
                c.result = D.light_weighted_dispersion(bb, s.model, edges_inferred=True)
            except D.ConversionRefused as e:
                c.refused = str(e)
        # precedence among candidates that pass the plotting rules (D-042, D-038 3B)
        ok = [c for c in s.candidates if c.plotted]
        if ok:
            ok.sort(key=lambda c: (c.dataset != "RV", -c.n_star, -(YEAR[c.dataset] or 0)))
            s.default = ok[0]
        elif s.candidates:
            s.reasons.append("no line-of-sight candidate passes the plotting rules (coverage ≥ 0.80, ≥ 2 bins)")
        else:
            s.reasons.append("no line-of-sight profile (proper motions only, recorded)")

        if s.plotted:
            s.r_half_pc = WOLF_FACTOR * s.r_h_pc
            r = s.r_half_pc * PC
            sig = s.default.result.sigma_rms * 1000.0
            s.g_obs = 3.0 * sig * sig / r
            s.g_bar = G * 0.5 * s.l_v * s.ml_v * M_SUN / (r * r)
    return sorted(systems.values(), key=lambda s: s.key)


def _plotted(self) -> bool:
    return (self.default is not None and not self.reasons and self.kind == "A3" and self.r_h_pc is not None
            and self.l_v is not None and self.ml_v is not None and self.distance_kpc is not None)


System.plotted = property(_plotted)
