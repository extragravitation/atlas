"""D-051: member coverage relative to the half-light ellipse, from a source's own per-star table.

Frozen with docs/methods/D051_COVERAGE.md. Pure functions; no I/O.

Each member's position is projected onto the tangent plane at the structural centre
(gnomonic projection). It is rotated by the position angle of the major axis (degrees, east
of north) and expressed as the radius of the ellipse through the star, in units of that
ellipse's semi-major axis:

    xi, eta = gnomonic offsets (east, north)
    x_maj   = xi * sin(PA) + eta * cos(PA)
    x_min   = xi * cos(PA) - eta * sin(PA)
    r_ell   = sqrt(x_maj**2 + (x_min / (1 - e))**2)

A star lies beyond the half-light ellipse when r_ell / a_h > 1, where a_h is the semi-major
half-light radius. This is the same contour as the circularised R_h = a_h * sqrt(1 - e), so
the test is identical in either convention.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Structure:
    ra0_deg: float
    dec0_deg: float
    ellipticity: float  # e = 1 - b/a
    pa_deg: float  # position angle of the major axis, east of north
    a_h_arcmin: float  # semi-major half-light radius


def gnomonic(ra_deg: float, dec_deg: float, ra0_deg: float, dec0_deg: float) -> tuple[float, float]:
    """Tangent-plane offsets (xi east, eta north), in degrees."""
    ra, dec, ra0, dec0 = map(math.radians, (ra_deg, dec_deg, ra0_deg, dec0_deg))
    cosc = math.sin(dec0) * math.sin(dec) + math.cos(dec0) * math.cos(dec) * math.cos(ra - ra0)
    xi = math.cos(dec) * math.sin(ra - ra0) / cosc
    eta = (math.cos(dec0) * math.sin(dec) - math.sin(dec0) * math.cos(dec) * math.cos(ra - ra0)) / cosc
    return math.degrees(xi), math.degrees(eta)


def r_over_ah(ra_deg: float, dec_deg: float, s: Structure) -> float:
    """Elliptical radius of a star in units of the semi-major half-light radius."""
    xi, eta = gnomonic(ra_deg, dec_deg, s.ra0_deg, s.dec0_deg)
    pa = math.radians(s.pa_deg)
    x_maj = xi * math.sin(pa) + eta * math.cos(pa)
    x_min = xi * math.cos(pa) - eta * math.sin(pa)
    r_ell_arcmin = 60.0 * math.hypot(x_maj, x_min / (1.0 - s.ellipticity))
    return r_ell_arcmin / s.a_h_arcmin


def summarise(radii: list[float]) -> dict:
    """D-051 item 2: pass if at least one member used lies beyond the half-light ellipse."""
    n_beyond = sum(1 for r in radii if r > 1.0)
    return {
        "n_members": len(radii),
        "n_beyond": n_beyond,
        "fraction_beyond": (n_beyond / len(radii)) if radii else float("nan"),
        "max_r_over_rh": max(radii) if radii else float("nan"),
        "passes": n_beyond >= 1,
    }
