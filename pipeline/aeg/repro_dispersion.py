"""Reproduction and consistency checks for published velocity dispersions.

D-037 (reproduction check): where a source releases per-star line-of-sight
velocities and publishes a dispersion from them, the Atlas recomputes the
dispersion from the released velocities with the source's own membership
and compares it with the published value. The published value is the one
shown; the recomputed value is never plotted in its place. The result
(pass, fail or not testable, with the numbers) is published for every
system.

D-038 3A (consistency check): for systems with both an original published
dispersion and one from Geha et al. (2026, Keck/DEIMOS Stellar Archive),
the two are compared system by system and as a population; the result is
published whichever way it goes.

Specification (frozen with this file; docs/methods/D037_D038_CHECKS.md):

Reproduction
- Members: the stars the source marks as members. If the source gives
  membership probabilities and states a threshold, that threshold; if it
  gives probabilities without a threshold, p > 0.5. Stars the source flags
  as binaries or velocity variables are excluded, as the source did. If
  the source states a radial selection for its published value, the same
  selection is applied. If membership cannot be reproduced from the release,
  the outcome is NOT_TESTABLE.
- Estimator: maximum likelihood for a Gaussian with per-star errors,
  L = prod_i N(v_i | mu, sigma^2 + e_i^2), mu profiled out; sigma >= 0.
  The 68% interval is where 2 * (ln L_max - ln L_profile(sigma)) <= 1.
  No binary model, no outlier clipping beyond the source's membership,
  no rotation model: this is the dispersion about the sample mean.
- Pass rule: PASS if the recomputed maximum-likelihood value lies inside
  the published 68% interval [sigma_pub - lo, sigma_pub + hi]; otherwise
  FAIL. If the source publishes an upper limit only, PASS if the recomputed
  maximum-likelihood value is at or below the limit. Fewer than 3 members:
  NOT_TESTABLE.
- The comparison is with the published quantity that is a dispersion about
  the sample mean; when the source's published value removes rotation or a
  gradient, or models binaries, that is recorded with the result and the
  test is still run and reported.

Consistency (originals vs Geha et al. 2026)
- Per system: z = (sigma_G - sigma_O) / sqrt(err_G^2 + err_O^2), with each
  err the half-width of the published interval on the side facing the other
  value. The two measurements share raw spectra in many cases, so z is
  approximate; this is stated with the result.
- Upper limits: a pair is consistent if the measured value's lower interval
  bound is at or below the other's limit; two limits are always consistent;
  such pairs get no z.
- Population outcome: CONSISTENT if at most 10% of pairs with a z have
  |z| > 2 and the median z lies in [-0.5, +0.5]; otherwise INCONSISTENT.
  Fewer than 5 pairs with a z: per-system results only, no population
  outcome. No adjustment is made for differing radial selections; each
  source's selection is recorded with the result.

Standard library only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import median
from typing import Sequence

SPEC_VERSION = "1.0.0"
PASS, FAIL, NOT_TESTABLE = "pass", "fail", "not_testable"
CONSISTENT, INCONSISTENT, PER_SYSTEM_ONLY = "consistent", "inconsistent", "per_system_only"


# --------------------------------------------------------------- membership

@dataclass(frozen=True)
class Star:
    v: float                     # line-of-sight velocity
    e: float                     # its 1-sigma error (same unit)
    member: bool | None = None   # source's flag, if given
    p_member: float | None = None
    binary_flag: bool = False    # source flags binary / velocity variable
    r: float | None = None       # projected radius, for a stated radial selection


def select_members(stars: Sequence[Star], p_threshold: float | None = None,
                   r_max: float | None = None) -> list[Star] | None:
    """The source's members, or None if membership cannot be reproduced."""
    out = []
    for s in stars:
        if s.member is not None:
            ok = s.member
        elif s.p_member is not None:
            ok = s.p_member > 0.5 if p_threshold is None else s.p_member >= p_threshold
        else:
            return None
        if not ok or s.binary_flag:
            continue
        if r_max is not None:
            if s.r is None:
                return None
            if s.r > r_max:
                continue
        if not (math.isfinite(s.v) and math.isfinite(s.e) and s.e >= 0):
            return None
        out.append(s)
    return out


# ------------------------------------------------------- likelihood estimator

def _mu_hat(v, e, sigma):
    w = [1.0 / (sigma * sigma + ei * ei) for ei in e]
    return sum(wi * vi for wi, vi in zip(w, v)) / sum(w)


def profile_loglike(v: Sequence[float], e: Sequence[float], sigma: float) -> float:
    if sigma == 0.0 and min(e) == 0.0:
        return -math.inf  # zero variance for an error-free star
    mu = _mu_hat(v, e, sigma)
    ll = 0.0
    for vi, ei in zip(v, e):
        var = sigma * sigma + ei * ei
        ll -= 0.5 * (math.log(2 * math.pi * var) + (vi - mu) ** 2 / var)
    return ll


def _golden_max(f, a, b, tol=1e-10):
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol * max(1.0, abs(b)):
        if fc < fd:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
        else:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
    return 0.5 * (a + b)


def _bisect(f, a, b, tol=1e-10):
    fa = f(a)
    for _ in range(300):
        m = 0.5 * (a + b)
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
        if b - a < tol * max(1.0, abs(b)):
            break
    return 0.5 * (a + b)


@dataclass(frozen=True)
class MLDispersion:
    sigma: float
    lo: float      # lower edge of the 68% interval
    hi: float      # upper edge
    mu: float
    n: int


def ml_dispersion(v: Sequence[float], e: Sequence[float]) -> MLDispersion:
    n = len(v)
    if n < 3:
        raise ValueError("fewer than 3 stars")
    mean = sum(v) / n
    spread = math.sqrt(sum((x - mean) ** 2 for x in v) / (n - 1))
    top = 10.0 * (spread + max(e)) + 1e-9
    f = lambda s: profile_loglike(v, e, s)
    s_hat = _golden_max(f, 0.0, top)
    if f(0.0) >= f(s_hat):
        s_hat = 0.0
    lmax = f(s_hat)
    g = lambda s: 2.0 * (lmax - f(s)) - 1.0
    lo = 0.0 if s_hat == 0.0 or g(0.0) <= 0 else _bisect(g, 0.0, s_hat)
    hi_top = top
    while g(hi_top) <= 0:
        hi_top *= 2
    hi = _bisect(g, s_hat, hi_top)
    return MLDispersion(s_hat, lo, hi, _mu_hat(v, e, s_hat), n)


# ---------------------------------------------------------------- reproduction

@dataclass(frozen=True)
class Published:
    sigma: float | None          # None when only a limit is published
    lo: float = 0.0              # published lower error (sigma - lo is the interval edge)
    hi: float = 0.0
    upper_limit: float | None = None


@dataclass(frozen=True)
class ReproResult:
    outcome: str
    recomputed: MLDispersion | None
    published: Published
    reason: str = ""
    spec_version: str = SPEC_VERSION


def reproduce(stars: Sequence[Star], published: Published, p_threshold: float | None = None,
              r_max: float | None = None) -> ReproResult:
    members = select_members(stars, p_threshold, r_max)
    if members is None:
        return ReproResult(NOT_TESTABLE, None, published, "membership cannot be reproduced from the release")
    if len(members) < 3:
        return ReproResult(NOT_TESTABLE, None, published, "fewer than 3 members")
    ml = ml_dispersion([s.v for s in members], [s.e for s in members])
    if published.sigma is None:
        if published.upper_limit is None:
            return ReproResult(NOT_TESTABLE, ml, published, "no published value or limit")
        ok = ml.sigma <= published.upper_limit
        return ReproResult(PASS if ok else FAIL, ml, published, "published upper limit")
    ok = published.sigma - published.lo <= ml.sigma <= published.sigma + published.hi
    return ReproResult(PASS if ok else FAIL, ml, published)


# ----------------------------------------------------------------- consistency

@dataclass(frozen=True)
class Value:
    sigma: float | None
    lo: float = 0.0
    hi: float = 0.0
    upper_limit: float | None = None


@dataclass(frozen=True)
class PairResult:
    system: str
    consistent: bool
    z: float | None


def compare_pair(system: str, orig: Value, geha: Value) -> PairResult:
    o_lim = orig.sigma is None
    g_lim = geha.sigma is None
    if o_lim and g_lim:
        return PairResult(system, True, None)
    if o_lim or g_lim:
        lim = orig.upper_limit if o_lim else geha.upper_limit
        val = geha if o_lim else orig
        if lim is None:
            raise ValueError(f"{system}: a value is missing")
        return PairResult(system, val.sigma - val.lo <= lim, None)
    if geha.sigma >= orig.sigma:
        eg, eo = geha.lo, orig.hi
    else:
        eg, eo = geha.hi, orig.lo
    denom = math.sqrt(eg * eg + eo * eo)
    if denom == 0:
        z = 0.0 if geha.sigma == orig.sigma else math.copysign(math.inf, geha.sigma - orig.sigma)
    else:
        z = (geha.sigma - orig.sigma) / denom
    return PairResult(system, abs(z) <= 2.0, z)


@dataclass(frozen=True)
class Consistency:
    outcome: str
    pairs: tuple[PairResult, ...]
    n_z: int
    frac_beyond_2: float | None
    median_z: float | None
    spec_version: str = SPEC_VERSION


def consistency(pairs: Sequence[PairResult]) -> Consistency:
    zs = [p.z for p in pairs if p.z is not None]
    if len(zs) < 5:
        return Consistency(PER_SYSTEM_ONLY, tuple(pairs), len(zs), None, None)
    frac = sum(1 for z in zs if abs(z) > 2.0) / len(zs)
    med = median(zs)
    ok = frac <= 0.10 and -0.5 <= med <= 0.5
    return Consistency(CONSISTENT if ok else INCONSISTENT, tuple(pairs), len(zs), frac, med)
