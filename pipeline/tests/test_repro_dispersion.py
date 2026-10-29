"""Synthetic tests for the D-037 reproduction check and the D-038 3A consistency check (frozen with the code)."""

import math
import random

import pytest

from aeg.repro_dispersion import (
    CONSISTENT, FAIL, INCONSISTENT, NOT_TESTABLE, PASS, PER_SYSTEM_ONLY,
    PairResult, Published, Star, Value, compare_pair, consistency, ml_dispersion,
    profile_loglike, reproduce, select_members,
)


def _sample(n, sigma, err, seed, mu=50.0):
    rng = random.Random(seed)
    errs = [err * (0.5 + rng.random()) for _ in range(n)]
    v = [mu + rng.gauss(0, sigma) + rng.gauss(0, e) for e in errs]
    return v, errs


# ------------------------------------------------------------- estimator

def test_ml_matches_sample_sd_when_errors_vanish():
    rng = random.Random(1)
    v = [rng.gauss(0, 5) for _ in range(400)]
    e = [0.0] * 400
    mean = sum(v) / 400
    mle = math.sqrt(sum((x - mean) ** 2 for x in v) / 400)  # ML (biased) estimator
    assert ml_dispersion(v, e).sigma == pytest.approx(mle, rel=1e-6)


def test_ml_recovers_sigma_with_heteroscedastic_errors():
    v, e = _sample(3000, 7.0, 2.0, seed=2)
    r = ml_dispersion(v, e)
    assert r.sigma == pytest.approx(7.0, abs=0.35)
    assert r.lo < r.sigma < r.hi


def test_ml_is_at_maximum_and_interval_is_delta_lnl_half():
    v, e = _sample(80, 4.0, 1.5, seed=3)
    r = ml_dispersion(v, e)
    lmax = profile_loglike(v, e, r.sigma)
    for ds in (-1e-4, 1e-4):
        assert profile_loglike(v, e, r.sigma + ds) <= lmax + 1e-12
    for edge in (r.lo, r.hi):
        assert 2 * (lmax - profile_loglike(v, e, edge)) == pytest.approx(1.0, abs=1e-6)


def test_interval_coverage_is_about_68_percent():
    hits = 0
    trials = 400
    for k in range(trials):
        v, e = _sample(60, 5.0, 2.0, seed=1000 + k)
        r = ml_dispersion(v, e)
        hits += r.lo <= 5.0 <= r.hi
    assert 0.60 <= hits / trials <= 0.76


def test_sigma_zero_when_scatter_is_below_errors():
    # all velocities equal: the maximum is at sigma = 0
    r = ml_dispersion([10.0] * 10, [2.0] * 10)
    assert r.sigma == 0.0 and r.lo == 0.0 and r.hi > 0


def test_ml_needs_three_stars():
    with pytest.raises(ValueError):
        ml_dispersion([1.0, 2.0], [0.1, 0.1])


# ------------------------------------------------------------- membership

def test_membership_flags_binaries_and_probabilities():
    stars = [Star(1, .1, member=True), Star(2, .1, member=False), Star(3, .1, member=True, binary_flag=True)]
    assert [s.v for s in select_members(stars)] == [1]
    probs = [Star(1, .1, p_member=0.9), Star(2, .1, p_member=0.5), Star(3, .1, p_member=0.6)]
    assert [s.v for s in select_members(probs)] == [1, 3]                    # p > 0.5
    assert [s.v for s in select_members(probs, p_threshold=0.6)] == [1, 3]   # p >= stated threshold
    assert [s.v for s in select_members(probs, p_threshold=0.7)] == [1]


def test_membership_not_reproducible():
    assert select_members([Star(1, .1)]) is None                                  # no flag at all
    assert select_members([Star(1, .1, member=True)], r_max=5.0) is None          # radial cut, no radius
    assert [s.v for s in select_members([Star(1, .1, True, r=1), Star(2, .1, True, r=9)], r_max=5)] == [1]


# ----------------------------------------------------------- reproduction

def test_reproduce_pass_and_fail():
    v, e = _sample(200, 6.0, 1.0, seed=5)
    stars = [Star(vi, ei, member=True) for vi, ei in zip(v, e)]
    ml = ml_dispersion(v, e)
    assert reproduce(stars, Published(ml.sigma, 0.3, 0.3)).outcome == PASS
    assert reproduce(stars, Published(ml.sigma + 1.0, 0.3, 0.3)).outcome == FAIL
    # asymmetric published interval is respected
    assert reproduce(stars, Published(ml.sigma - 0.5, 0.1, 0.6)).outcome == PASS
    assert reproduce(stars, Published(ml.sigma - 0.5, 0.6, 0.1)).outcome == FAIL


def test_reproduce_upper_limit_and_untestable():
    v, e = _sample(20, 0.5, 2.0, seed=6)
    stars = [Star(vi, ei, member=True) for vi, ei in zip(v, e)]
    ml = ml_dispersion(v, e)
    assert reproduce(stars, Published(None, upper_limit=ml.sigma + 0.01)).outcome == PASS
    assert reproduce(stars, Published(None, upper_limit=max(ml.sigma - 0.01, 0))).outcome in (FAIL, PASS)
    assert reproduce([Star(1, .1)], Published(5, 1, 1)).outcome == NOT_TESTABLE
    assert reproduce(stars[:2], Published(5, 1, 1)).outcome == NOT_TESTABLE
    assert reproduce(stars, Published(None)).outcome == NOT_TESTABLE


# ------------------------------------------------------------ consistency

def test_pair_z_uses_facing_errors():
    p = compare_pair("A", Value(10, lo=1, hi=3), Value(14, lo=4, hi=1))
    # geha above orig: geha's lower error (4) and orig's upper error (3)
    assert p.z == pytest.approx(4 / 5)
    assert p.consistent
    q = compare_pair("B", Value(10, 1, 1), Value(14, 1, 1))
    assert q.z == pytest.approx(4 / math.sqrt(2)) and not q.consistent


def test_pair_limits():
    assert compare_pair("A", Value(None, upper_limit=3), Value(None, upper_limit=5)).consistent
    assert compare_pair("B", Value(None, upper_limit=3), Value(4, lo=1.5, hi=1)).consistent      # 2.5 <= 3
    assert not compare_pair("C", Value(6, lo=1, hi=1), Value(None, upper_limit=4)).consistent   # 5 > 4
    assert compare_pair("D", Value(None, upper_limit=3), Value(4, 1.5, 1)).z is None


def test_population_outcomes():
    ok = [PairResult(str(i), True, z) for i, z in enumerate([-0.4, 0.1, 0.3, -0.2, 0.0, 0.6, -0.1, 0.2, 1.1, -0.8])]
    assert consistency(ok).outcome == CONSISTENT
    shifted = [PairResult(str(i), True, z + 0.7) for i, z in enumerate([-0.4, 0.1, 0.3, -0.2, 0.0, 0.6, -0.1, 0.2])]
    assert consistency(shifted).outcome == INCONSISTENT          # median outside [-0.5, 0.5]
    wide = [PairResult(str(i), abs(z) <= 2, z) for i, z in enumerate([0, 0.1, -0.1, 2.5, -2.6, 0.2, 0.0, -0.2, 0.1, 0.3])]
    c = consistency(wide)
    assert c.frac_beyond_2 == pytest.approx(0.2) and c.outcome == INCONSISTENT
    few = [PairResult(str(i), True, 0.0) for i in range(4)]
    assert consistency(few).outcome == PER_SYSTEM_ONLY


def test_end_to_end_same_data_reproduces():
    # a source that used this exact estimator on its released members must pass
    for seed in range(20):
        v, e = _sample(50, 3.0, 1.5, seed=200 + seed)
        stars = [Star(vi, ei, member=True) for vi, ei in zip(v, e)] + [Star(500.0, 1.0, member=False)]
        ml = ml_dispersion(v, e)
        r = reproduce(stars, Published(ml.sigma, ml.sigma - ml.lo, ml.hi - ml.sigma))
        assert r.outcome == PASS
        assert r.recomputed.n == 50
