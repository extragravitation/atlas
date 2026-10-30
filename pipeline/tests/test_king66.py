"""King (1966) model for the D-036 (ii) conversion, version 2 (D-045 item 2).

Synthetic and internal checks only; agreement with published fits
(McLaughlin & van der Marel 2005) is the package's reproduction test.
"""

import math

import pytest

from aeg import dispersion as D
from aeg.king66 import King66, rho_hat, tidal_radius

W0S = (0.5, 2.0, 5.0, 8.0, 12.0)


@pytest.fixture(scope="module")
def models():
    return {w0: King66(w0, 1.0) for w0 in W0S}


def test_density_series_matches_exact_form():
    for w in (1e-3, 2e-3, 5e-3):
        exact = math.exp(w) * math.erf(math.sqrt(w)) - math.sqrt(4 * w / math.pi) * (1 + 2 * w / 3)
        series = 8.0 / (15.0 * math.sqrt(math.pi)) * w ** 2.5
        assert series == pytest.approx(exact, rel=5e-3)  # next term is O(W)
    assert rho_hat(0.0) == 0.0 and rho_hat(-1.0) == 0.0


def test_light_from_gradient_equals_light_from_density(models):
    for m in models.values():
        assert m.quadrature_mass() == pytest.approx(m.poisson_mass(), rel=1e-4)


def test_concentration_rises_with_w0():
    cs = [math.log10(tidal_radius(w)) for w in (0.5, 1, 2, 4, 6, 8, 10, 14, 18)]
    assert all(a < b for a, b in zip(cs, cs[1:]))


def test_grid_convergence(models):
    for w0, m in models.items():
        fine = King66(w0, 1.0, n_per_decade=1600)
        assert m.concentration == pytest.approx(fine.concentration, abs=1e-4)
        assert m.half_light_radius() == pytest.approx(fine.half_light_radius(), rel=1e-3)
        assert m.half_power_radius() == pytest.approx(fine.half_power_radius(), rel=1e-3)


def test_cumulative_fraction_limits_and_monotonic(models):
    for m in models.values():
        assert m.cumulative_fraction(0.0) == 0.0
        assert m.cumulative_fraction(m.r_tidal) == pytest.approx(1.0)
        assert m.cumulative_fraction(10 * m.r_tidal) == 1.0
        rs = [m.r_tidal * f for f in (1e-3, 0.01, 0.05, 0.1, 0.3, 0.6, 0.9)]
        vals = [m.cumulative_fraction(r) for r in rs]
        assert all(0 < a < b <= 1 for a, b in zip(vals, vals[1:]))


def test_cylinder_light_agrees_with_integrated_surface_brightness(models):
    """Independent route: integrate 2 pi R Sigma(R) dR numerically and compare with L_cyl."""
    for w0 in (2.0, 8.0):
        m = models[w0]
        rt = m.r_tidal
        n = 600
        lo = math.log(1e-4)
        rs = [0.0] + [math.exp(lo + (math.log(rt) - lo) * i / n) for i in range(n + 1)]
        sig = [m.surface_density(r, n=1500) for r in rs]
        cum, tot = [0.0], 0.0
        for i in range(1, len(rs)):
            tot += 0.5 * (rs[i - 1] * sig[i - 1] + rs[i] * sig[i]) * (rs[i] - rs[i - 1])
            cum.append(tot)
        for frac in (0.02, 0.1, 0.3, 0.6):
            j = int(frac * n)
            assert cum[j] / tot == pytest.approx(m.cumulative_fraction(rs[j]), abs=2e-3)


def test_half_radii_are_where_they_say(models):
    for m in models.values():
        rh = m.half_light_radius()
        assert m.cumulative_fraction(rh) == pytest.approx(0.5, abs=1e-6)
        rc = m.half_power_radius()
        assert m.surface_density(rc) == pytest.approx(0.5 * m.surface_density(0.0), rel=1e-4)


def test_high_concentration_core_radius_tends_to_scale_radius(models):
    # King's scale radius r0 is defined so that, for concentrated models, the
    # projected density falls to about half its central value near r0.
    assert models[12.0].half_power_radius() == pytest.approx(1.0, abs=0.02)


def test_scaling_with_r0():
    a, b = King66(6.0, 1.0), King66(6.0, 2.5)
    assert b.r_tidal == pytest.approx(2.5 * a.r_tidal)
    assert b.half_light_radius() == pytest.approx(2.5 * a.half_light_radius(), rel=1e-6)
    assert b.cumulative_fraction(2.5) == pytest.approx(a.cumulative_fraction(1.0), rel=1e-9)


def test_from_concentration_inverts():
    for w0 in (1.5, 6.0, 11.0):
        c = math.log10(tidal_radius(w0))
        m = King66.from_concentration(c, 3.0)
        assert m.w0 == pytest.approx(w0, abs=1e-4)
        assert m.concentration == pytest.approx(c, abs=1e-6)
    with pytest.raises(ValueError):
        King66.from_concentration(9.0, 1.0)


def test_refusals():
    with pytest.raises(ValueError):
        King66(6.0, 0.0)
    with pytest.raises(ValueError):
        King66(0.0, 1.0)
    with pytest.raises(ValueError):
        King66(25.0, 1.0)


def test_works_in_the_frozen_conversion(models):
    m = King66(7.0, 1.0)
    # constant sigma returns itself; full coverage when bins span the cluster
    edges = [0.0, 0.5, 2.0, m.r_tidal]
    bins = [D.Bin(edges[i], edges[i + 1], 6.0, 0.3, 0.3) for i in range(3)]
    r = D.light_weighted_dispersion(bins, m)
    assert r.sigma_rms == pytest.approx(6.0)
    assert r.coverage == pytest.approx(1.0, abs=1e-9)
    assert r.plotted
    # an inner-only profile below 80% of the light is recorded, not plotted
    r2 = D.light_weighted_dispersion([D.Bin(0.0, 0.3, 6.0, 0.3, 0.3)], m)
    assert r2.coverage < 0.8 and not r2.plotted
