"""King (1966) lowered-isothermal model for the D-036 (ii) conversion, version 2 (D-045 item 2).

Adds King (1966) to the structural models of the frozen conversion
(`aeg.dispersion`, D-036), which is not edited: `King66` is a
`StructuralModel` and is passed to `aeg.dispersion.light_weighted_dispersion`
like the others. Standard library only.

The model (King 1966, AJ 71, 64), in the dimensionless form used by
McLaughlin & van der Marel (2005, section 3.1):

    density     rho(W) proportional to  e^W erf(sqrt W) - sqrt(4W/pi) (1 + 2W/3)
    Poisson     (1/x^2) d/dx (x^2 dW/dx) = -9 rho(W) / rho(W0),   x = r / r0
    centre      W(0) = W0, dW/dx(0) = 0;  tidal radius x_t where W = 0
    concentration  c = log10(r_t / r0)

Projected light inside radius R (cylinder), with L(<r) the 3D light inside r:

    L_cyl(R) = L(<R) + int_R^{r_t} 4 pi r^2 rho(r) [1 - sqrt(1 - R^2/r^2)] dr

Surface brightness: Sigma(R) = 2 int_0^{sqrt(r_t^2 - R^2)} rho(sqrt(R^2 + s^2)) ds.

Derived radii, all in the unit of r0: tidal radius, half-light radius
(projected, L_cyl = 0.5), half-power radius (Sigma = Sigma(0) / 2, the "core
radius" R_c of McLaughlin & van der Marel 2005).

Inputs:
- `King66(w0, r0)`: from a source's fitted W0 and scale radius r0.
- `King66.from_concentration(c, r0)`: from a concentration c = log10(r_t/r0)
  and r0 (used for Harris 2010, whose c and r_c are read as log10(r_t/r0)
  and r0: a registered assumption, D-045).

Numerics: the Poisson equation is integrated with fourth-order Runge-Kutta
in u = ln(r/r0), N_PER_DECADE steps per decade from r = 1e-6 r0 (central
series below that) to the tidal radius, found by linear interpolation of the
sign change of W. The 3D light inside r comes from the potential gradient
(-x^2 W'/9); the total is also integrated directly from the density as a
check. Projections use the trapezoidal rule on the same grid (cylinder) or
on a logarithmic grid (surface brightness). Accuracy is set by the tests.
"""

from __future__ import annotations

import bisect
import math
from dataclasses import dataclass, field

from aeg.dispersion import StructuralModel

SPEC_VERSION = "2.0.0"
N_PER_DECADE = 400
W0_MIN, W0_MAX = 0.1, 20.0


def rho_hat(w: float) -> float:
    """Unnormalised King (1966) density as a function of the potential W >= 0."""
    if w <= 0.0:
        return 0.0
    if w < 1e-3:  # series: (8/15) sqrt(1/pi) * 2 W^(5/2) ... keep the exact leading term
        return 8.0 / (15.0 * math.sqrt(math.pi)) * w ** 2.5
    return math.exp(w) * math.erf(math.sqrt(w)) - math.sqrt(4.0 * w / math.pi) * (1.0 + 2.0 * w / 3.0)


X0 = 1e-6          # inner start of the logarithmic grid (units of r0); series below it


def _rhs(u: float, w: float, p: float, rho0: float) -> tuple[float, float]:
    """d/du of (W, p) with x = e^u and p = x^2 dW/dx:  dW/du = p/x,  dp/du = -9 rho x^3."""
    x = math.exp(u)
    return p / x, -9.0 * rho_hat(max(w, 0.0)) / rho0 * x ** 3


def _integrate(w0: float, n_per_decade: int):
    """RK4 in u = ln x from X0 until W <= 0; returns lists x, W, p (p = x^2 dW/dx)."""
    rho0 = rho_hat(w0)
    h = math.log(10.0) / n_per_decade
    u = math.log(X0)
    w, p = w0 - 1.5 * X0 ** 2, -3.0 * X0 ** 3  # central series, rho(W0)/rho0 = 1
    xs, ws, ps = [X0], [w], [p]
    while True:
        k1 = _rhs(u, w, p, rho0)
        k2 = _rhs(u + h / 2, w + h / 2 * k1[0], p + h / 2 * k1[1], rho0)
        k3 = _rhs(u + h / 2, w + h / 2 * k2[0], p + h / 2 * k2[1], rho0)
        k4 = _rhs(u + h, w + h * k3[0], p + h * k3[1], rho0)
        w_new = w + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        p_new = p + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        u += h
        if w_new <= 0.0:
            # tidal radius by linear interpolation in x of the sign change
            x_prev, x_new = xs[-1], math.exp(u)
            xt = x_prev + (x_new - x_prev) * w / (w - w_new)
            pt = p + (p_new - p) * (xt - x_prev) / (x_new - x_prev)
            xs.append(xt); ws.append(0.0); ps.append(pt)
            return xs, ws, ps
        w, p = w_new, p_new
        xs.append(math.exp(u)); ws.append(w); ps.append(p)
        if u > math.log(1e6):
            raise ValueError("no tidal radius found")


def tidal_radius(w0: float, n_per_decade: int | None = None) -> float:
    """x_t = r_t / r0 for central potential W0."""
    if not (W0_MIN <= w0 <= W0_MAX):
        raise ValueError(f"W0 must be in [{W0_MIN}, {W0_MAX}]")
    return _integrate(w0, n_per_decade or N_PER_DECADE)[0][-1]


@dataclass
class King66(StructuralModel):
    w0: float
    r0: float
    name: str = field(default="King 1966", init=False)

    n_per_decade: int = N_PER_DECADE

    def __post_init__(self):
        if not (self.r0 > 0 and math.isfinite(self.r0)):
            raise ValueError("King66 needs r0 > 0")
        if not (W0_MIN <= self.w0 <= W0_MAX):
            raise ValueError(f"W0 must be in [{W0_MIN}, {W0_MAX}]")
        xs, ws, ps = _integrate(self.w0, self.n_per_decade)
        rho0 = rho_hat(self.w0)
        self._x = xs
        self._xt = xs[-1]
        self._rho = [rho_hat(max(w, 0.0)) / rho0 for w in ws]
        self._m3 = [-p / 9.0 for p in ps]   # 3D light inside x, from the potential gradient
        self._total = self._m3[-1]
        # independent check of the light: trapezoid of x^2 rho dx on the same grid
        m = 0.0
        for i in range(1, len(xs)):
            m += 0.5 * (xs[i - 1] ** 2 * self._rho[i - 1] + xs[i] ** 2 * self._rho[i]) * (xs[i] - xs[i - 1])
        self._total_quad = m

    # ---- radii in units of r0 (multiply by r0 for the source's unit)
    @property
    def concentration(self) -> float:
        return math.log10(self._xt)

    @property
    def r_tidal(self) -> float:
        return self._xt * self.r0

    def poisson_mass(self) -> float:
        """Total light from the potential gradient at the tidal radius, -x^2 W'(x_t) / 9."""
        return self._total

    def quadrature_mass(self) -> float:
        """Total light by direct integration of the density (independent of the gradient)."""
        return self._total_quad

    def _index(self, x: float) -> int:
        """Largest i with xs[i] <= x (x inside the grid)."""
        return max(0, bisect.bisect_right(self._x, x) - 1)

    def _interp_rho(self, x: float) -> float:
        if x >= self._xt:
            return 0.0
        if x <= self._x[0]:
            return 1.0
        i = min(self._index(x), len(self._x) - 2)
        t = (x - self._x[i]) / (self._x[i + 1] - self._x[i])
        return self._rho[i] * (1 - t) + self._rho[i + 1] * t

    def _interp_m3(self, x: float) -> float:
        if x <= self._x[0]:
            return x ** 3 / 3.0
        i = min(self._index(x), len(self._x) - 2)
        t = (x - self._x[i]) / (self._x[i + 1] - self._x[i])
        return self._m3[i] * (1 - t) + self._m3[i + 1] * t

    def _cyl(self, xr: float) -> float:
        """Projected light inside cylinder radius xr (units of r0)."""
        if xr <= 0.0:
            return 0.0
        if xr >= self._xt:
            return self._total
        xs, rho = self._x, self._rho

        def g(x, r):
            return x * x * r * (1.0 - math.sqrt(max(0.0, 1.0 - (xr / x) ** 2)))
        k = self._index(xr) + 1
        outer = 0.5 * (g(xr, self._interp_rho(xr)) + g(xs[k], rho[k])) * (xs[k] - xr)
        for i in range(k + 1, len(xs)):
            outer += 0.5 * (g(xs[i - 1], rho[i - 1]) + g(xs[i], rho[i])) * (xs[i] - xs[i - 1])
        return self._interp_m3(xr) + outer

    def cumulative_fraction(self, r: float) -> float:  # L_cyl(<R) / L_total, R in the unit of r0
        if r <= 0.0:
            return 0.0
        return min(1.0, self._cyl(r / self.r0) / self._total)

    def surface_density(self, r: float, n: int = 3000) -> float:
        """Sigma(R) in units of rho(0) r0 (relative values only are used).

        Sigma(R) = 2 int_0^{s_max} rho(sqrt(R^2 + s^2)) ds on a grid of s that is
        logarithmic from 1e-6 r0 to s_max (plus s = 0), so the core is resolved.
        """
        xr = r / self.r0
        if xr >= self._xt:
            return 0.0
        smax = math.sqrt(self._xt ** 2 - xr ** 2)
        lo = math.log(min(1e-6, smax / 10.0))
        pts = [0.0] + [math.exp(lo + (math.log(smax) - lo) * i / n) for i in range(n + 1)]
        vals = [self._interp_rho(math.sqrt(xr * xr + q * q)) for q in pts]
        tot = sum(0.5 * (vals[i - 1] + vals[i]) * (pts[i] - pts[i - 1]) for i in range(1, len(pts)))
        return 2.0 * tot

    def _solve(self, f, target: float) -> float:
        lo, hi = 0.0, self._xt * self.r0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if f(mid) < target:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def half_light_radius(self) -> float:
        """Projected half-light radius, in the unit of r0."""
        return self._solve(self.cumulative_fraction, 0.5)

    def half_power_radius(self) -> float:
        """Radius where the surface brightness falls to half its central value, in the unit of r0."""
        s0 = self.surface_density(0.0)
        return self._solve(lambda r: -self.surface_density(r), -0.5 * s0)

    @classmethod
    def from_concentration(cls, c: float, r0: float) -> "King66":
        """Model with concentration c = log10(r_t / r0); W0 found by bisection (c rises with W0)."""
        lo, hi = W0_MIN, W0_MAX
        c_lo, c_hi = math.log10(tidal_radius(lo)), math.log10(tidal_radius(hi))
        if not (c_lo <= c <= c_hi):
            raise ValueError(f"c = {c} outside the range [{c_lo:.3f}, {c_hi:.3f}] of W0 in [{W0_MIN}, {W0_MAX}]")
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if math.log10(tidal_radius(mid)) < c:
                lo = mid
            else:
                hi = mid
        return cls(0.5 * (lo + hi), r0)
