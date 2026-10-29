"""Synthetic-profile tests for the D-036 (ii) conversion (frozen with the code).

Every expected value below is derived analytically or by an independent
numerical route written here, never from real data.
"""

import math
import random

import pytest

from aeg.dispersion import (
    COVERAGE_THRESHOLD, Bin, ConversionRefused, King62, Plummer, Sersic,
    _gammainc_lower_regularized, bins_from_radii, light_weighted_dispersion, sersic_b,
)


# -------------------------------------------------- independent integrator

def _numeric_fraction(surface, r_in, r_out, r_max, n=200000):
    """Light fraction by midpoint integration of 2*pi*R*I(R) (independent of the closed forms)."""
    def integral(a, b):
        h = (b - a) / n
        return sum(2 * math.pi * (a + (k + 0.5) * h) * surface(a + (k + 0.5) * h) for k in range(n)) * h
    return integral(r_in, r_out) / integral(0.0, r_max)


# ------------------------------------------------------- structural models

def test_plummer_closed_form():
    m = Plummer(a=2.0)
    assert m.cumulative_fraction(2.0) == pytest.approx(0.5, abs=1e-15)
    assert m.cumulative_fraction(4.0) == pytest.approx(0.8, abs=1e-15)
    assert m.cumulative_fraction(0.0) == 0.0
    assert m.cumulative_fraction(math.inf) == 1.0


def test_plummer_against_numeric_integration():
    a = 1.5
    surf = lambda r: (1 + r * r / (a * a)) ** -2
    got = Plummer(a).light_between(0.7, 3.1)
    ref = _numeric_fraction(surf, 0.7, 3.1, 3000.0, n=400000) / 1.0
    # numeric total truncated at 3000 a: missing fraction ~ (a/3000)^2, negligible
    assert got == pytest.approx(ref, rel=2e-4)


def test_king62_against_numeric_integration():
    rc, rt = 0.8, 30.0
    c = (1 + (rt / rc) ** 2) ** -0.5
    surf = lambda r: ((1 + (r / rc) ** 2) ** -0.5 - c) ** 2 if r < rt else 0.0
    m = King62(rc, rt)
    for r_in, r_out in [(0.0, 0.8), (0.8, 5.0), (5.0, 30.0), (2.0, 2.5)]:
        assert m.light_between(r_in, r_out) == pytest.approx(
            _numeric_fraction(surf, r_in, r_out, rt), rel=1e-4, abs=1e-7)
    assert m.cumulative_fraction(rt) == pytest.approx(1.0, abs=1e-15)
    assert m.cumulative_fraction(2 * rt) == pytest.approx(1.0, abs=1e-15)


def test_gammainc_against_closed_forms():
    # P(1, x) = 1 - e^-x ; P(2, x) = 1 - (1 + x) e^-x ; P(0.5, x) = erf(sqrt(x))
    for x in (1e-3, 0.3, 1.0, 2.5, 7.0, 30.0):
        assert _gammainc_lower_regularized(1.0, x) == pytest.approx(1 - math.exp(-x), rel=1e-12, abs=1e-15)
        assert _gammainc_lower_regularized(2.0, x) == pytest.approx(1 - (1 + x) * math.exp(-x), rel=1e-11, abs=1e-15)
        assert _gammainc_lower_regularized(0.5, x) == pytest.approx(math.erf(math.sqrt(x)), rel=1e-11, abs=1e-15)


def test_sersic_half_light_and_exponential():
    for n in (0.5, 1.0, 2.0, 4.0):
        m = Sersic(r_e=3.0, n=n)
        assert m.cumulative_fraction(3.0) == pytest.approx(0.5, abs=1e-10)
    # n = 1 is exponential: L(<R) = 1 - (1 + y) e^-y with y = b_1 R / R_e
    b1 = sersic_b(1.0)
    assert b1 == pytest.approx(1.678346990, rel=1e-8)  # root of P(2, b) = 1/2
    m = Sersic(r_e=1.0, n=1.0)
    for r in (0.2, 1.0, 3.0):
        y = b1 * r
        assert m.cumulative_fraction(r) == pytest.approx(1 - (1 + y) * math.exp(-y), rel=1e-11)


def test_sersic4_against_numeric_integration():
    re_, n = 2.0, 4.0
    b = sersic_b(n)
    surf = lambda r: math.exp(-b * ((r / re_) ** (1 / n) - 1))
    m = Sersic(re_, n)
    got = m.light_between(0.5, 6.0)
    ref = _numeric_fraction(surf, 0.5, 6.0, 4000.0, n=400000)
    assert got == pytest.approx(ref, rel=5e-3)  # truncation of the de Vaucouleurs tail


# --------------------------------------------------------------- conversion

def test_constant_dispersion_returns_itself():
    m = Plummer(1.0)
    bins = [Bin(0.0, 0.5, 7.0, 0.5, 0.5), Bin(0.5, 2.0, 7.0, 0.5, 0.5), Bin(2.0, 5.0, 7.0, 0.5, 0.5)]
    r = light_weighted_dispersion(bins, m)
    assert r.sigma_rms == pytest.approx(7.0, abs=1e-12)


def test_equal_light_bins_average_sigma_squared():
    # Plummer: [0, a] and [a, inf) each hold half the light
    m = Plummer(1.0)
    r = light_weighted_dispersion([Bin(0.0, 1.0, 6.0, 0, 0), Bin(1.0, math.inf, 8.0, 0, 0)], m)
    assert r.mean_sigma2 == pytest.approx((36 + 64) / 2, abs=1e-12)
    assert r.coverage == pytest.approx(1.0, abs=1e-15)
    assert r.weights == pytest.approx((0.5, 0.5), abs=1e-15)


def test_known_weights_three_bins():
    # Plummer fractions: L(<a)=1/2, L(<2a)=4/5, L(<3a)=9/10
    m = Plummer(1.0)
    bins = [Bin(0, 1, 10.0, 0, 0), Bin(1, 2, 6.0, 0, 0), Bin(2, 3, 4.0, 0, 0)]
    r = light_weighted_dispersion(bins, m)
    w = (0.5, 0.3, 0.1)
    expected = sum(wi * s * s for wi, s in zip(w, (10, 6, 4))) / sum(w)
    assert r.mean_sigma2 == pytest.approx(expected, rel=1e-14)
    assert r.coverage == pytest.approx(0.9, abs=1e-14)
    assert r.plotted


def test_coverage_threshold_boundary():
    assert COVERAGE_THRESHOLD == 0.80
    m = Plummer(1.0)
    below = light_weighted_dispersion([Bin(0, 1.99, 5, 0, 0)], m)  # 0.7984...
    above = light_weighted_dispersion([Bin(0, 2.01, 5, 0, 0)], m)  # 0.8016...
    assert below.coverage < 0.8 and not below.plotted
    assert above.coverage > 0.8 and above.plotted


def test_gaps_are_not_covered():
    m = Plummer(1.0)
    r = light_weighted_dispersion([Bin(0, 1, 5, 0, 0), Bin(2, 3, 5, 0, 0)], m)
    assert r.coverage == pytest.approx(0.5 + (0.9 - 0.8), abs=1e-14)


def test_central_only_profile_is_not_plotted():
    m = King62(1.0, 40.0)
    r = light_weighted_dispersion([Bin(0, 0.2, 9, 1, 1), Bin(0.2, 0.5, 8, 1, 1)], m)
    assert r.coverage < 0.2 and not r.plotted


def test_order_of_bins_does_not_matter():
    m = Sersic(2.0, 1.0)
    bins = [Bin(0, 1, 5, .2, .3), Bin(1, 3, 4, .2, .2), Bin(3, 8, 3, .4, .1)]
    a = light_weighted_dispersion(bins, m)
    b = light_weighted_dispersion(list(reversed(bins)), m)
    assert a == b


def test_errors_against_monte_carlo():
    # symmetric errors: analytic propagation vs Monte Carlo of independent Gaussian bins
    m = Plummer(1.0)
    bins = [Bin(0, 1, 9.0, 0.6, 0.6), Bin(1, 2, 7.0, 0.5, 0.5), Bin(2, 6, 5.0, 0.8, 0.8)]
    r = light_weighted_dispersion(bins, m)
    rng = random.Random(20261029)
    w = r.weights
    draws = []
    for _ in range(200000):
        s2 = sum(wi * (b.sigma + rng.gauss(0, b.err_hi)) ** 2 for wi, b in zip(w, bins))
        draws.append(math.sqrt(s2))
    mean = sum(draws) / len(draws)
    sd = math.sqrt(sum((d - mean) ** 2 for d in draws) / (len(draws) - 1))
    half_width = 0.5 * (r.err_lo + r.err_hi)
    assert half_width == pytest.approx(sd, rel=0.05)


def test_asymmetric_errors_are_kept_separate():
    m = Plummer(1.0)
    r = light_weighted_dispersion([Bin(0, 1, 5.0, 0.1, 1.0), Bin(1, 10, 5.0, 0.1, 1.0)], m)
    assert r.err_hi > 5 * r.err_lo


def test_edges_inferred_from_radii():
    bins = bins_from_radii([1.0, 2.0, 4.0], [5, 5, 5], [0, 0, 0], [0, 0, 0])
    assert [(b.r_in, b.r_out) for b in bins] == [(0.0, 1.5), (1.5, 3.0), (3.0, 5.0)]
    r = light_weighted_dispersion(bins, Plummer(1.0), edges_inferred=True)
    assert r.edges_inferred
    assert r.coverage == pytest.approx(25 / 26, abs=1e-14)


@pytest.mark.parametrize("bins,msg", [
    ([Bin(0, 1, 5, 0, 0, "upper")], "limit"),
    ([Bin(0, 2, 5, 0, 0), Bin(1, 3, 5, 0, 0)], "overlap"),
    ([Bin(1, 1, 5, 0, 0)], "r_in < r_out"),
    ([Bin(0, 1, -5, 0, 0)], "non-negative"),
    ([Bin(0, 1, math.nan, 0, 0)], "non-negative"),
    ([], "no bins"),
])
def test_refusals(bins, msg):
    with pytest.raises(ConversionRefused, match=msg):
        light_weighted_dispersion(bins, Plummer(1.0))


def test_model_parameter_validation():
    with pytest.raises(ValueError):
        King62(2.0, 1.0)
    with pytest.raises(ValueError):
        Plummer(0.0)
    with pytest.raises(ValueError):
        Sersic(1.0, 0.0)
    with pytest.raises(ConversionRefused):
        bins_from_radii([1.0], [5], [0], [0])
    with pytest.raises(ConversionRefused):
        bins_from_radii([2.0, 1.0], [5, 5], [0, 0], [0, 0])
