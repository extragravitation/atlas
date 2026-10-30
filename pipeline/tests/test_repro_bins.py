"""D-045 item 5: reconstructed-binning reproduction check, on synthetic stars."""

import random

import pytest

from aeg.repro_bins import LABEL, PublishedBin, RVStar, check_profile, select
from aeg.repro_dispersion import FAIL, NOT_TESTABLE, PASS, ml_dispersion


def make(n, r0, r1, sigma, rng, e=1.0):
    return [RVStar(r=rng.uniform(r0, r1), v=rng.gauss(0, sigma) + rng.gauss(0, e), e=e, p_member=0.9, p_single=0.9)
            for _ in range(n)]


def published_from(stars, n_per_bin):
    """Bins published by an author who used exactly this rule (must always pass)."""
    s = sorted(stars, key=lambda x: x.r)
    out, k = [], 0
    for n in n_per_bin:
        g = s[k:k + n]; k += n
        ml = ml_dispersion([x.v for x in g], [x.e for x in g])
        out.append(PublishedBin(sum(x.r for x in g) / n, n, ml.sigma, ml.sigma - ml.lo, ml.hi - ml.sigma))
    return out


def test_selection_rules():
    stars = [
        RVStar(1, 0, 1, 0.9, 0.9),     # member
        RVStar(1, 0, 1, 0.5, 0.9),     # p = 0.5 is not > 0.5
        RVStar(1, 0, 1, None, 0.9),    # no probability: not a member
        RVStar(1, 0, 1, 0.9, 0.4),     # binary
        RVStar(1, 0, 1, 0.9, None),    # no single probability: kept
        RVStar(None, 0, 1, 0.9, 0.9),  # no radius: unusable
        RVStar(1, float("nan"), 1, 0.9, 0.9),  # no velocity: unusable
    ]
    sel, unusable = select(stars)
    assert len(sel) == 2 and unusable == 2


def test_author_using_this_rule_always_passes():
    rng = random.Random(3)
    stars = make(30, 0, 10, 8.0, rng) + make(30, 10, 40, 5.0, rng) + make(20, 40, 100, 3.0, rng)
    pub = published_from(stars, [30, 30, 20])
    res = check_profile(stars, pub)
    assert [b.result.outcome for b in res.bins] == [PASS] * 3
    assert all(b.label == LABEL for b in res.bins)
    for b in res.bins:
        assert b.r_mean_rebuilt == pytest.approx(b.published.r_mean)


def test_non_members_and_binaries_do_not_shift_the_bins():
    rng = random.Random(5)
    stars = make(25, 0, 5, 7.0, rng) + make(25, 5, 30, 4.0, rng)
    pub = published_from(stars, [25, 25])
    noise = [RVStar(rng.uniform(0, 30), rng.gauss(0, 60), 1.0, 0.1, 0.9) for _ in range(40)]
    binaries = [RVStar(rng.uniform(0, 30), rng.gauss(0, 30), 1.0, 0.9, 0.2) for _ in range(5)]
    res = check_profile(stars + noise + binaries, pub)
    assert [b.result.outcome for b in res.bins] == [PASS, PASS]


def test_count_mismatch_is_not_testable():
    rng = random.Random(7)
    stars = make(40, 0, 20, 6.0, rng)
    pub = published_from(stars, [20, 20])
    res = check_profile(stars[:-1], pub)
    assert res.n_selected == 39 and res.n_published == 40
    assert all(b.result.outcome == NOT_TESTABLE for b in res.bins)
    assert "membership not reproduced" in res.reason


def test_wrong_published_value_fails():
    rng = random.Random(9)
    stars = make(60, 0, 20, 6.0, rng)
    pub = published_from(stars, [30, 30])
    bad = [pub[0], PublishedBin(pub[1].r_mean, 30, pub[1].sigma * 2, 0.3, 0.3)]
    res = check_profile(stars, bad)
    assert [b.result.outcome for b in res.bins] == [PASS, FAIL]


def test_bins_taken_in_radius_order_whatever_the_input_order():
    rng = random.Random(11)
    stars = make(20, 0, 5, 9.0, rng) + make(20, 5, 50, 2.0, rng)
    pub = published_from(stars, [20, 20])
    a = check_profile(stars, pub)
    b = check_profile(list(reversed(stars)), list(reversed(pub)))
    assert [x.result.recomputed.sigma for x in a.bins] == pytest.approx([x.result.recomputed.sigma for x in b.bins])


def test_tiny_bin_is_not_testable():
    rng = random.Random(13)
    stars = make(12, 0, 20, 5.0, rng)
    pub = published_from(stars, [10, 2][:1]) + [PublishedBin(30.0, 2, 5.0, 1.0, 1.0)]
    res = check_profile(stars, pub)
    assert res.bins[-1].result.outcome == NOT_TESTABLE
