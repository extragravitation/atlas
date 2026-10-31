"""Synthetic tests of the A5 gas rule (data/packages/aeg-d-dwarfs/v1/reproduction/gas.py). No real values."""

import importlib.util
from pathlib import Path

P = Path(__file__).resolve().parents[2] / "data/packages/aeg-d-dwarfs/v1/reproduction/gas.py"
spec = importlib.util.spec_from_file_location("a5gas", P)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def test_detection_rescaled_helium_half():
    r = g.gas_for_system({"status": "in table", "Dist": "100", "MHI": "1.0E+06", "e_MHI": "1.0E+05", "E_MHI": "", "l_MHI": ""}, 200.0)
    assert r["gas_status"] == "measured"
    assert abs(r["distance_factor"] - 4.0) < 1e-12
    assert abs(r["m_gas_rh"] - 0.5 * 1.33 * 4.0e6) < 1e-6
    assert abs(r["m_gas_rh_err_plus"] - 0.5 * 1.33 * 4.0e5) < 1e-6


def test_limit_absent_but_recorded():
    r = g.gas_for_system({"status": "in table", "Dist": "50", "MHI": "1.0E+04", "e_MHI": "", "E_MHI": "", "l_MHI": "<"}, 25.0)
    assert r["gas_status"] == "absent (measured limit)" and r["m_gas_rh"] == 0.0
    assert abs(r["m_hi_pkg"] - 2500.0) < 1e-9


def test_not_in_table():
    assert g.gas_for_system({"status": "not in Putman 2021"}, 100.0)["gas_status"] == "not addressed"
    assert g.gas_for_system(None, 100.0)["gas_status"] == "not addressed"
