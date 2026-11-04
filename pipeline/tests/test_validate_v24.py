"""Synthetic tests for the data standard 2.4.0 rules (D-093)."""

import json
from pathlib import Path

from astropy.table import Table

from aeg.validate import validate_v24


def _pkg(tmp: Path, meas_cols: dict, terms_rows=None, desc=None) -> tuple[Path, Table]:
    pkg = tmp / "aeg-d-test" / "v2"
    (pkg / "tables").mkdir(parents=True)
    if terms_rows is not None:
        cols = sorted({k for r in terms_rows for k in r})
        Table({c: [r.get(c, "") for r in terms_rows] for c in cols}).write(pkg / "tables/uncertainty_terms.ecsv", format="ascii.ecsv")
    (pkg / "datapackage.json").write_text(json.dumps(desc or {}), encoding="utf-8")
    meas = Table({"measurement_id": ["m1"], **meas_cols})
    return pkg, meas


def test_new_columns_need_240(tmp_path):
    pkg, meas = _pkg(tmp_path, {"g_bar_bound": ["lower"], "g_bar_bound_basis": ["gas only"]})
    assert any("need standard 2.4.0" in p for p in validate_v24(pkg, meas, "2.3.0"))


def test_good_240_passes(tmp_path):
    pkg, meas = _pkg(tmp_path, {
        "g_bar": [1e-11], "err_level_status": ["not_given_by_source"],
        "g_bar_bound": ["lower"], "g_bar_bound_basis": ["gas only; stars not given by the source"],
        "g_bar_basis": ["computed"]},
        terms_rows=[{"term_id": "conv", "scale": "point", "applies_to": "*", "moves": "g_obs", "status": "given",
                     "size_value": 0.1, "in_error_columns": "no"}],
        desc={"x_value_change_ruling": "D-090"})
    assert validate_v24(pkg, meas, "2.4.0") == []


def test_bound_rules(tmp_path):
    pkg, meas = _pkg(tmp_path, {"g_bar": [1e-11], "g_bar_bound": ["lower"], "g_bar_bound_basis": [""],
                                "g_bar_err_lo": [1e-12]})
    probs = validate_v24(pkg, meas, "2.4.0")
    assert any("bound_basis is empty" in p for p in probs)
    assert any("bound but has g_bar error" in p for p in probs)


def test_bin_coordinate_and_err_level(tmp_path):
    pkg, meas = _pkg(tmp_path, {"g_bar": [5e-11], "g_bar_basis": ["bin_coordinate"], "g_bar_bin_lo": [1e-11],
                                "g_bar_bin_hi": [2e-11], "g_bar_err_point_lo": [1e-12],
                                "err_level_status": ["not_given_by_source"], "err_level": [0.9]})
    probs = validate_v24(pkg, meas, "2.4.0")
    assert any("outside its bin edges" in p for p in probs)
    assert any("point-scale g_bar errors" in p for p in probs)
    assert any("err_level is set" in p for p in probs)


def test_terms_and_ruling(tmp_path):
    pkg, meas = _pkg(tmp_path, {"g_bar": [1e-11]},
                     terms_rows=[{"term_id": "x", "scale": "point", "applies_to": "*", "moves": "g_obs",
                                  "status": "not_given_by_source", "in_error_columns": "no"}],
                     desc={"x_value_change_ruling": "D-999"})
    probs = validate_v24(pkg, meas, "2.4.0")
    assert any("requires status = given" in p for p in probs)
    assert any("not a decision" in p for p in probs)
