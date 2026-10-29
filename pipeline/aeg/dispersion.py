"""Light-weighted dispersion from a binned line-of-sight profile (D-036 ii).

Decision D-036 (ii): where a source gives a binned line-of-sight dispersion
profile, the Atlas computes

    <sigma^2_los> = sum_i w_i sigma_i^2 / sum_i w_i,

with w_i the light in bin i taken from the source's own surface-brightness
model or a cited structural model, and records the fraction of the system's
light covered by the bins. The value is plotted only if the covered fraction
is at least 0.80 (COVERAGE_THRESHOLD); otherwise it is recorded, not plotted.
D-038 2A: where a source gives the second moment (rotation included), that
column is the input; this module does not care which, the caller passes it.

Specification (frozen with this file; see docs/methods/D036_CONVERSION.md):
- Weights are exact projected light in each annulus, from the closed-form
  cumulative light L(<R) of the structural model. No numerical integration.
- Bins are annuli [r_in, r_out) in the same radial unit and radius
  definition as the structural model. Bins must not overlap. Gaps between
  bins are allowed and are not counted as covered.
- Where the source gives only representative radii (no edges), edges are
  inferred at arithmetic midpoints between adjacent radii; the innermost bin
  starts at 0 and the outermost ends at r_n + (r_n - r_{n-1}) / 2. The
  result carries edges_inferred = True and is shown as such.
- Errors: bins are treated as independent. The lower and upper errors on
  <sigma^2> are propagated in quadrature separately, from sigma_i - lo_i and
  sigma_i + hi_i; the dispersion sigma_rms = sqrt(<sigma^2>) carries the
  corresponding asymmetric errors. Uncertainty in the structural model is not
  propagated (registered as a known limitation).
- A bin given as an upper or lower limit makes the conversion refuse
  (the system is recorded, not converted).
- Supported structural models: Plummer (a), King 1962 (r_c, r_t), Sersic
  (R_e, n; exponential is n = 1). Tabulated surface-brightness profiles are
  not supported by this version.

Only the Python standard library is used, so the result does not depend on
numerical-library versions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Sequence

COVERAGE_THRESHOLD = 0.80
SPEC_VERSION = "1.0.0"


# ---------------------------------------------------------------- models

class StructuralModel:
    """Projected (surface) light profile with closed-form cumulative light."""

    name = "model"

    def cumulative_fraction(self, r: float) -> float:  # L(<R) / L_total
        raise NotImplementedError

    def light_between(self, r_in: float, r_out: float) -> float:
        return self.cumulative_fraction(r_out) - self.cumulative_fraction(r_in)


@dataclass(frozen=True)
class Plummer(StructuralModel):
    """Surface density proportional to (1 + R^2/a^2)^-2; a is the projected half-light radius."""

    a: float
    name = "plummer"

    def __post_init__(self):
        if not self.a > 0:
            raise ValueError("Plummer scale a must be positive")

    def cumulative_fraction(self, r: float) -> float:
        if r <= 0:
            return 0.0
        if math.isinf(r):
            return 1.0
        return r * r / (r * r + self.a * self.a)


@dataclass(frozen=True)
class King62(StructuralModel):
    """King (1962) empirical profile: I(R) = k [(1+x^2)^-1/2 - C]^2, x = R/r_c, C = (1+x_t^2)^-1/2.

    Cumulative light in closed form with u = x^2:
        F(u) = ln(1+u) - 4C sqrt(1+u) + C^2 u,   L(<R) proportional to F(u) - F(0).
    """

    r_c: float
    r_t: float
    name = "king1962"

    def __post_init__(self):
        if not (self.r_c > 0 and self.r_t > self.r_c):
            raise ValueError("King62 needs 0 < r_c < r_t")

    def _f(self, r: float) -> float:
        c = 1.0 / math.sqrt(1.0 + (self.r_t / self.r_c) ** 2)
        u = (r / self.r_c) ** 2
        return math.log1p(u) - 4.0 * c * math.sqrt(1.0 + u) + c * c * u

    def cumulative_fraction(self, r: float) -> float:
        if r <= 0:
            return 0.0
        r = min(r, self.r_t)
        total = self._f(self.r_t) - self._f(0.0)
        return (self._f(r) - self._f(0.0)) / total


def _gammainc_lower_regularized(a: float, x: float) -> float:
    """P(a, x), regularized lower incomplete gamma (series / continued fraction)."""
    if x <= 0:
        return 0.0
    if math.isinf(x):
        return 1.0
    gln = math.lgamma(a)
    if x < a + 1.0:
        ap, s, d = a, 1.0 / a, 1.0 / a
        for _ in range(100000):
            ap += 1.0
            d *= x / ap
            s += d
            if abs(d) < abs(s) * 1e-16:
                break
        return s * math.exp(-x + a * math.log(x) - gln)
    # continued fraction for Q(a, x) (modified Lentz)
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, 100000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-16:
            break
    q = math.exp(-x + a * math.log(x) - gln) * h
    return 1.0 - q


def sersic_b(n: float) -> float:
    """b_n such that R_e encloses half the light: P(2n, b_n) = 1/2 (bisection)."""
    lo, hi = 1e-8, 2.0 * n + 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _gammainc_lower_regularized(2.0 * n, mid) < 0.5:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


@dataclass(frozen=True)
class Sersic(StructuralModel):
    """Sersic (1968) surface brightness with effective radius R_e and index n."""

    r_e: float
    n: float
    name = "sersic"
    _b: float = field(init=False, repr=False, compare=False, default=0.0)

    def __post_init__(self):
        if not (self.r_e > 0 and self.n > 0):
            raise ValueError("Sersic needs R_e > 0 and n > 0")
        object.__setattr__(self, "_b", sersic_b(self.n))

    def cumulative_fraction(self, r: float) -> float:
        if r <= 0:
            return 0.0
        if math.isinf(r):
            return 1.0
        x = self._b * (r / self.r_e) ** (1.0 / self.n)
        return _gammainc_lower_regularized(2.0 * self.n, x)


# ------------------------------------------------------------- conversion

@dataclass(frozen=True)
class Bin:
    r_in: float
    r_out: float
    sigma: float
    err_lo: float
    err_hi: float
    limit: str = "none"  # none | upper | lower


@dataclass(frozen=True)
class Result:
    sigma_rms: float
    err_lo: float
    err_hi: float
    mean_sigma2: float
    coverage: float
    plotted: bool
    edges_inferred: bool
    n_bins: int
    weights: tuple[float, ...]
    model: str
    spec_version: str = SPEC_VERSION


class ConversionRefused(ValueError):
    """The profile cannot be converted under D-036 (ii); the system is recorded only."""


def bins_from_radii(radii: Sequence[float], sigma: Sequence[float],
                    err_lo: Sequence[float], err_hi: Sequence[float],
                    limit: Sequence[str] | None = None) -> list[Bin]:
    """Bins from representative radii only (edges inferred; see module docstring)."""
    n = len(radii)
    if n < 2:
        raise ConversionRefused("edges cannot be inferred from fewer than two radii")
    if any(radii[i] >= radii[i + 1] for i in range(n - 1)) or radii[0] <= 0:
        raise ConversionRefused("radii must be positive and strictly increasing")
    edges = [0.0]
    edges += [0.5 * (radii[i] + radii[i + 1]) for i in range(n - 1)]
    edges.append(radii[-1] + 0.5 * (radii[-1] - radii[-2]))
    lim = list(limit) if limit is not None else ["none"] * n
    return [Bin(edges[i], edges[i + 1], sigma[i], err_lo[i], err_hi[i], lim[i]) for i in range(n)]


def light_weighted_dispersion(bins: Sequence[Bin], model: StructuralModel,
                              edges_inferred: bool = False) -> Result:
    if not bins:
        raise ConversionRefused("no bins")
    bs = sorted(bins, key=lambda b: b.r_in)
    for b in bs:
        if b.limit != "none":
            raise ConversionRefused("a bin is a limit; system recorded, not converted")
        if not (b.r_out > b.r_in >= 0):
            raise ConversionRefused("each bin needs 0 <= r_in < r_out")
        if not (b.sigma >= 0 and b.err_lo >= 0 and b.err_hi >= 0):
            raise ConversionRefused("dispersions and errors must be non-negative")
        if not all(math.isfinite(v) for v in (b.r_in, b.sigma, b.err_lo, b.err_hi)) or math.isnan(b.r_out):
            raise ConversionRefused("non-finite input")
    for a, c in zip(bs, bs[1:]):
        if c.r_in < a.r_out:
            raise ConversionRefused("bins overlap")

    w = [model.light_between(b.r_in, b.r_out) for b in bs]
    wsum = sum(w)
    if not wsum > 0:
        raise ConversionRefused("bins contain no light under the structural model")

    mean_s2 = sum(wi * b.sigma ** 2 for wi, b in zip(w, bs)) / wsum
    # quadrature per side: each bin's contribution to the shift of <sigma^2>
    d_lo = math.sqrt(sum((wi / wsum * (b.sigma ** 2 - max(b.sigma - b.err_lo, 0.0) ** 2)) ** 2
                         for wi, b in zip(w, bs)))
    d_hi = math.sqrt(sum((wi / wsum * ((b.sigma + b.err_hi) ** 2 - b.sigma ** 2)) ** 2
                         for wi, b in zip(w, bs)))
    s = math.sqrt(mean_s2)
    s_lo = math.sqrt(max(mean_s2 - d_lo, 0.0))
    s_hi = math.sqrt(mean_s2 + d_hi)
    coverage = wsum  # weights are fractions of total light
    return Result(
        sigma_rms=s,
        err_lo=s - s_lo,
        err_hi=s_hi - s,
        mean_sigma2=mean_s2,
        coverage=coverage,
        plotted=coverage >= COVERAGE_THRESHOLD,
        edges_inferred=edges_inferred,
        n_bins=len(bs),
        weights=tuple(wi / wsum for wi in w),
        model=model.name,
    )
