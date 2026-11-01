"""Strong-lensing conversions for the A6 strong-lensing cell (D-063, D-064, D-065).

Frozen with `data/packages/aeg-d-a6s/v1/REPRODUCTION.md` before any lensing
table is opened. Standard library only.

1. Distances in a flat Lambda-CDM cosmology given by the source (H0, Omega_m),
   radiation neglected:
       D_C(z) = (c / H0) * int_0^z dz' / E(z'),  E(z) = sqrt(Om (1+z)^3 + 1 - Om)
       D_A(z) = D_C(z) / (1 + z)
       D_A(z1, z2) = (D_C(z2) - D_C(z1)) / (1 + z2)      (flat, z2 > z1)
   The integral uses composite Simpson's rule with N_SIMPSON intervals.

2. Einstein mass from an Einstein radius (A6S precedence §2.4):
       M_E = theta_E^2 c^2 D_s D_l / (4 G D_ls),   R_E = theta_E D_l

3. Projected light inside a cylinder of radius R for a Sersic profile of
   index n and effective (half-light) radius R_e (A6S precedence §3.1):
       f(<R) = P(2n, b_n (R / R_e)^(1/n))
   where P is the regularised lower incomplete gamma function and b_n solves
   P(2n, b_n) = 1/2. De Vaucouleurs is n = 4.

4. Accelerations in projection (D-064): g = G M(<R_E) / R_E^2 for both sides.

Units: SI internally. Masses in solar masses and radii in kpc at the
interface.
"""

from __future__ import annotations

import math

C = 299_792_458.0  # m s^-1 (exact)
G = 6.67430e-11  # m^3 kg^-1 s^-2 (CODATA 2018), as aeg-d-dwarfs/v1
PC = 3.0856775814913673e16  # m (IAU 2015 B2), as aeg-d-dwarfs/v1
KPC = 1e3 * PC
MPC = 1e6 * PC
M_SUN = 1.98840987e30  # kg (IAU 2015 nominal G M_sun / G), as aeg-d-dwarfs/v1
ARCSEC = math.pi / (180.0 * 3600.0)  # rad

N_SIMPSON = 2000  # even


# --- distances ---------------------------------------------------------------

def _e(z: float, om: float) -> float:
    return math.sqrt(om * (1.0 + z) ** 3 + (1.0 - om))


def comoving_distance(z: float, h0: float, om: float) -> float:
    """Line-of-sight comoving distance in metres. h0 in km s^-1 Mpc^-1."""
    if z < 0:
        raise ValueError("z must be >= 0")
    if z == 0:
        return 0.0
    n = N_SIMPSON
    h = z / n
    s = 1.0 / _e(0.0, om) + 1.0 / _e(z, om)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) / _e(i * h, om)
    integral = s * h / 3.0
    hubble_distance = C / (h0 * 1e3 / MPC)  # metres
    return hubble_distance * integral


def angular_diameter_distance(z: float, h0: float, om: float) -> float:
    return comoving_distance(z, h0, om) / (1.0 + z)


def angular_diameter_distance_between(z1: float, z2: float, h0: float, om: float) -> float:
    if not z2 > z1:
        raise ValueError("need z2 > z1")
    return (comoving_distance(z2, h0, om) - comoving_distance(z1, h0, om)) / (1.0 + z2)


# --- Einstein radius and mass ------------------------------------------------

def einstein_radius_kpc(theta_e_arcsec: float, z_l: float, h0: float, om: float) -> float:
    return theta_e_arcsec * ARCSEC * angular_diameter_distance(z_l, h0, om) / KPC


def einstein_mass_msun(theta_e_arcsec: float, z_l: float, z_s: float, h0: float, om: float) -> float:
    """M_E = theta^2 c^2 D_s D_l / (4 G D_ls), in solar masses."""
    if theta_e_arcsec <= 0:
        raise ValueError("theta_E must be > 0")
    th = theta_e_arcsec * ARCSEC
    dl = angular_diameter_distance(z_l, h0, om)
    ds = angular_diameter_distance(z_s, h0, om)
    dls = angular_diameter_distance_between(z_l, z_s, h0, om)
    return th * th * C * C * ds * dl / (4.0 * G * dls) / M_SUN


# --- Sersic enclosed light ---------------------------------------------------

def _gammainc_lower_reg(a: float, x: float) -> float:
    """Regularised lower incomplete gamma P(a, x) (Numerical Recipes 6.2 method)."""
    if x < 0 or a <= 0:
        raise ValueError("need a > 0, x >= 0")
    if x == 0:
        return 0.0
    gln = math.lgamma(a)
    if x < a + 1.0:  # series
        ap, s, d = a, 1.0 / a, 1.0 / a
        for _ in range(10_000):
            ap += 1.0
            d *= x / ap
            s += d
            if abs(d) < abs(s) * 1e-16:
                break
        return s * math.exp(-x + a * math.log(x) - gln)
    # continued fraction for Q, Lentz
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, 10_000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        d = tiny if abs(d) < tiny else d
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-16:
            break
    return 1.0 - math.exp(-x + a * math.log(x) - gln) * h


def sersic_b(n: float) -> float:
    """b_n with P(2n, b_n) = 1/2, by bisection to 1e-14 relative."""
    if n <= 0:
        raise ValueError("n must be > 0")
    lo, hi = 0.0, 2.0 * n + 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _gammainc_lower_reg(2.0 * n, mid) < 0.5:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-14 * max(1.0, mid):
            break
    return 0.5 * (lo + hi)


def sersic_projected_fraction(r: float, r_e: float, n: float) -> float:
    """Fraction of the total light inside a cylinder of radius r."""
    if r < 0 or r_e <= 0:
        raise ValueError("need r >= 0, r_e > 0")
    if r == 0:
        return 0.0
    return _gammainc_lower_reg(2.0 * n, sersic_b(n) * (r / r_e) ** (1.0 / n))


# --- accelerations (D-064) ---------------------------------------------------

def projected_acceleration(mass_msun: float, radius_kpc: float) -> float:
    """g = G M(<R) / R^2 in m s^-2, for a projected (cylinder) mass."""
    if radius_kpc <= 0:
        raise ValueError("radius must be > 0")
    r = radius_kpc * KPC
    return G * mass_msun * M_SUN / (r * r)
