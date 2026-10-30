"""D-039 item 1b: M/L by metallicity, piecewise linear, no extrapolation."""

import pytest

from aeg.ml_interp import BEYOND, MLTable


def test_reproduces_table_points_and_interpolates_linearly():
    t = MLTable([-2.0, -1.0, 0.0], [1.8, 2.0, 3.0], [0.1, 0.2, 0.4])
    assert t(-1.0).ml == 2.0 and t(-1.0).err == 0.2 and t(-1.0).flag == ""
    v = t(-0.5)
    assert v.ml == pytest.approx(2.5) and v.err == pytest.approx(0.3) and v.flag == ""


def test_non_monotonic_table_is_followed_exactly():
    t = MLTable([-2.0, -1.5, -1.0], [2.0, 1.9, 2.1])
    assert t(-1.75).ml == pytest.approx(1.95)
    assert t(-1.25).ml == pytest.approx(2.0)


def test_no_extrapolation_outside_the_table():
    t = MLTable([-2.29, 0.22], [1.9, 3.0])
    lo, hi = t(-2.8), t(0.5)
    assert lo.ml == 1.9 and lo.flag == BEYOND
    assert hi.ml == 3.0 and hi.flag == BEYOND
    assert t(-2.29).flag == ""


def test_order_independent_and_duplicates():
    a = MLTable([0.0, -2.0, -1.0], [3.0, 1.8, 2.0])
    b = MLTable([-2.0, -1.0, 0.0, -1.0], [1.8, 2.0, 3.0, 2.0])
    for x in (-1.7, -0.3):
        assert a(x).ml == pytest.approx(b(x).ml)
    with pytest.raises(ValueError):
        MLTable([-1.0, -1.0], [2.0, 2.1])


def test_refusals():
    with pytest.raises(ValueError):
        MLTable([], [])
    with pytest.raises(ValueError):
        MLTable([-1.0, 0.0], [2.0, -1.0])
    with pytest.raises(ValueError):
        MLTable([-1.0, 0.0], [2.0, 3.0])(float("nan"))
