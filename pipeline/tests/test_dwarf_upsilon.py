"""Synthetic tests of the A5 Upsilon_V rule (D-060). No real values."""

import importlib.util
from pathlib import Path

from aeg.ml_interp import MLTable

P = Path(__file__).resolve().parents[2] / "data/packages/aeg-d-dwarfs/v1/reproduction/upsilon.py"
spec = importlib.util.spec_from_file_location("a5ups", P)
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)

# synthetic model: (M/L)1 = 2 + feh/2 on [-2, 0]; e1 = 0.1; (M/L)2 = 1.6 x (M/L)1; e2 = 0.2
FEH = [-2.0, -1.0, 0.0]
M1 = [1.0, 1.5, 2.0]
TABS = (MLTable(FEH, M1), MLTable(FEH, [m - 0.1 for m in M1]), MLTable(FEH, [1.6 * m + 0.2 for m in M1]))


def test_default_and_envelope():
    r = u.upsilon(-1.0, 0.5, TABS)
    assert abs(r["upsilon_v"] - 1.5) < 1e-12
    assert abs(r["upsilon_v_low"] - (1.25 - 0.1) * 0.90 * 1.3 / 1.6) < 1e-12
    assert abs(r["upsilon_v_high"] - (1.6 * 1.75 + 0.2) * 1.10) < 1e-12
    assert not r["beyond"]


def test_beyond_floor_flagged_not_extrapolated():
    r = u.upsilon(-2.5, 0.1, TABS)
    assert abs(r["upsilon_v"] - 1.0) < 1e-12 and r["beyond"]
    assert abs(r["upsilon_v_low"] - 0.9 * 0.90 * 1.3 / 1.6) < 1e-12


def test_interval_reaching_past_table_flags():
    assert u.upsilon(-1.9, 0.2, TABS)["beyond"]


def test_num_parsing():
    assert u.num("<0.45") == 0.45 and u.num("~0.2") == 0.2 and u.num("−2.16") == -2.16 and u.num("") is None
