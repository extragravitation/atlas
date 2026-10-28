import math

import pytest

from aeg.formula import FormulaError, apply_assumption, evaluate, names, parse


@pytest.mark.parametrize("text,env,expected", [
    ("1 + 2 * 3", {}, 7),
    ("(1 + 2) * 3", {}, 9),
    ("-2^2", {}, -4),
    ("2^3^2", {}, 512),
    ("2^-1", {}, 0.5),
    ("a / b", {"a": 1, "b": 4}, 0.25),
    ("sqrt(a)", {"a": 9}, 3),
    ("abs(-a)", {"a": 2}, 2),
    ("sin(deg2rad(90))", {}, 1),
    ("g_obs * p0 / p", {"g_obs": 2e-10, "p": 2, "p0": 1}, 1e-10),
    ("system.distance_mpc * 2", {"system.distance_mpc": 3.5}, 7),
    ("1.5e-3 * 2", {}, 3e-3),
])
def test_values(text, env, expected):
    assert evaluate(parse(text), env) == pytest.approx(expected, rel=1e-15)


@pytest.mark.parametrize("text,env", [
    ("a + 1", {}),               # missing name
    ("a + 1", {"a": ""}),        # empty cell
    ("sqrt(a)", {"a": -1}),      # outside domain
    ("1 / a", {"a": 0}),         # division by zero
])
def test_nan(text, env):
    assert math.isnan(evaluate(parse(text), env))


@pytest.mark.parametrize("text", ["1 +", "foo(1)", "sqrt", "a ** 2", "(1", "1 2", "a; b", "import os"])
def test_rejects(text):
    with pytest.raises(FormulaError):
        parse(text)


def test_names():
    assert names(parse("g_obs * system.distance_mpc / p")) == {"g_obs", "system.distance_mpc", "p"}


def test_simultaneous_assignment():
    row = {"a": 1.0, "b": 10.0}
    effects = [{"column": "a", "formula": "a * p"}, {"column": "b", "formula": "b + a"}]
    out = apply_assumption(row, {}, effects, p=2, p0=1)
    assert out == {"a": 2.0, "b": 11.0}  # b used the old a
