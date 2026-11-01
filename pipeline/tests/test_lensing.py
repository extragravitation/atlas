"""Synthetic tests for aeg.lensing (frozen with aeg-d-a6s/v1 REPRODUCTION.md)."""

import math

import pytest

from aeg import lensing as L


def test_eds_distances_closed_form():
    # Omega_m = 1: D_A = (2c/H0) (1 - 1/sqrt(1+z)) / (1+z)
    h0 = 70.0
    dh = L.C / (h0 * 1e3 / L.MPC)
    for z in (0.1, 0.5, 2.0):
        exact = 2 * dh * (1 - 1 / math.sqrt(1 + z)) / (1 + z)
        assert L.angular_diameter_distance(z, h0, 1.0) == pytest.approx(exact, rel=1e-10)


def test_low_z_hubble_law():
    h0, z = 70.0, 1e-4
    d = L.angular_diameter_distance(z, h0, 0.3)
    assert d / L.MPC == pytest.approx(L.C / 1e3 * z / h0, rel=1e-3)


def test_einstein_mass_formula_by_hand():
    h0, om, zl, zs, th = 70.0, 0.3, 0.2, 0.6, 1.2
    dl = L.angular_diameter_distance(zl, h0, om)
    ds = L.angular_diameter_distance(zs, h0, om)
    dls = (L.comoving_distance(zs, h0, om) - L.comoving_distance(zl, h0, om)) / (1 + zs)
    t = th * math.pi / 648000
    expect = t * t * L.C**2 * ds * dl / (4 * L.G * dls) / L.M_SUN
    assert L.einstein_mass_msun(th, zl, zs, h0, om) == pytest.approx(expect, rel=1e-12)


def test_einstein_mass_scales_as_theta_squared():
    a = L.einstein_mass_msun(1.0, 0.2, 0.6, 70, 0.3)
    b = L.einstein_mass_msun(2.0, 0.2, 0.6, 70, 0.3)
    assert b / a == pytest.approx(4.0, rel=1e-12)


def test_einstein_mass_rejects_bad_input():
    with pytest.raises(ValueError):
        L.einstein_mass_msun(1.0, 0.6, 0.2, 70, 0.3)
    with pytest.raises(ValueError):
        L.einstein_mass_msun(0.0, 0.2, 0.6, 70, 0.3)


@pytest.mark.parametrize("n", [0.5, 1.0, 2.0, 4.0, 6.0])
def test_half_light_at_re(n):
    assert L.sersic_projected_fraction(1.0, 1.0, n) == pytest.approx(0.5, abs=1e-12)


def test_exponential_closed_form():
    # n = 1: f = 1 - (1 + b x) e^{-b x}
    b = L.sersic_b(1.0)
    for x in (0.2, 1.0, 3.0):
        assert L.sersic_projected_fraction(x, 1.0, 1.0) == pytest.approx(1 - (1 + b * x) * math.exp(-b * x), abs=1e-12)


def test_gaussian_n_half():
    # n = 1/2: f = 1 - exp(-b x^2), b = ln 2
    assert L.sersic_b(0.5) == pytest.approx(math.log(2), rel=1e-12)
    for x in (0.3, 1.5):
        assert L.sersic_projected_fraction(x, 1.0, 0.5) == pytest.approx(1 - math.exp(-math.log(2) * x * x), abs=1e-12)


def test_de_vaucouleurs_b4_and_monotone():
    # independent check: for integer a, P(a, b) = 1 - e^-b sum_{k<a} b^k / k!
    b = L.sersic_b(4.0)
    p8 = 1 - math.exp(-b) * sum(b**k / math.factorial(k) for k in range(8))
    assert p8 == pytest.approx(0.5, abs=1e-12)
    xs = [0.05, 0.1, 0.3, 0.5, 1, 2, 5, 20]
    fs = [L.sersic_projected_fraction(x, 1.0, 4.0) for x in xs]
    assert all(b > a for a, b in zip(fs, fs[1:]))
    assert fs[-1] < 1.0


def test_projected_acceleration():
    g = L.projected_acceleration(1e11, 5.0)
    assert g == pytest.approx(L.G * 1e11 * L.M_SUN / (5 * L.KPC) ** 2, rel=1e-14)
