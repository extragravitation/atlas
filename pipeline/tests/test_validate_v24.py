"""Synthetic tests for the data standard 2.4.0 rules (D-093)."""

import json
from pathlib import Path

from astropy.table import Table

from aeg.validate import validate_v22, validate_v24


def _pkg(tmp: Path, meas_cols: dict, terms_rows=None, desc=None, obs_cols=None) -> tuple[Path, Table]:
    pkg = tmp / "aeg-d-test" / "v2"
    (pkg / "tables").mkdir(parents=True)
    if terms_rows is not None:
        cols = sorted({k for r in terms_rows for k in r})
        Table({c: [r.get(c, "") for r in terms_rows] for c in cols}).write(pkg / "tables/uncertainty_terms.ecsv", format="ascii.ecsv")
    if obs_cols is not None:
        Table({"observable_id": ["o1"], **obs_cols}).write(pkg / "tables/observables.ecsv", format="ascii.ecsv")
    Table({"system_id": ["aeg-s-000001", "aeg-s-000002"]}).write(pkg / "tables/systems.ecsv", format="ascii.ecsv")
    (pkg / "datapackage.json").write_text(json.dumps(desc or {}), encoding="utf-8")
    meas = Table({"measurement_id": ["m1"], **meas_cols})
    return pkg, meas


BASE = {"g_bar": [1e-11], "g_bar_basis": ["computed"], "err_level_status": ["stated"], "err_level": [0.95]}
KTERM = {"term_id": "conv", "scale": "point", "applies_to": "*", "moves": "g_obs", "status": "given",
         "size_value": 0.1, "in_error_columns": "no"}


def test_new_features_need_240(tmp_path):
    pkg, meas = _pkg(tmp_path, BASE, terms_rows=[dict(KTERM, applies_to="aeg-s-000001;aeg-s-000002", size_kind="upper_bound")],
                     desc={"x_value_change_ruling": "D-090"}, obs_cols={"err_level_status": ["stated"], "err_level": [0.9]})
    probs = validate_v24(pkg, meas, "2.3.0")
    assert len(probs) == 1
    for item in ("g_bar_basis", "err_level_status", "in_error_columns", "list-valued", "upper_bound",
                 "x_value_change_ruling", "observables.err_level_status"):
        assert item in probs[0]


def test_good_240_passes(tmp_path):
    pkg, meas = _pkg(tmp_path, {"g_bar": [1e-11], "err_level_status": ["not_given_by_source"], "g_bar_basis": ["computed"],
                                "g_bar_err_level_status": ["stated"], "g_bar_err_level": [0.683]},
                     terms_rows=[KTERM, {"term_id": "cal", "scale": "dataset", "applies_to": "aeg-s-000001;aeg-s-000002",
                                         "moves": "g_obs", "status": "given", "size_value": 0.05, "size_kind": "upper_bound"}],
                     desc={"x_value_change_ruling": "D-090"},
                     obs_cols={"err_level_status": ["not_given_by_source"], "err_level": [None]})
    assert validate_v24(pkg, meas, "2.4.0") == []
    assert validate_v22(pkg, meas) == []


def test_bin_coordinate_rules(tmp_path):
    pkg, meas = _pkg(tmp_path, {"g_bar": [5e-11], "g_bar_basis": ["bin_coordinate"], "g_bar_bin_lo": [1e-11],
                                "g_bar_bin_hi": [2e-11], "g_bar_err_point_lo": [1e-12]})
    probs = validate_v24(pkg, meas, "2.4.0")
    assert any("outside its bin edges" in p for p in probs)
    assert any("point-scale g_bar errors" in p for p in probs)
    pkg2, meas2 = _pkg(tmp_path / "b", {"g_bar": [1.5e-11], "g_bar_basis": ["computed"], "g_bar_bin_lo": [3e-11], "g_bar_bin_hi": [2e-11]})
    assert any("not bin_coordinate" in p for p in validate_v24(pkg2, meas2, "2.4.0"))
    pkg3, meas3 = _pkg(tmp_path / "c", {"g_bar": [1.5e-11], "g_bar_basis": ["bin_coordinate"], "g_bar_bin_lo": [3e-11], "g_bar_bin_hi": [2e-11]})
    assert any("exceeds" in p for p in validate_v24(pkg3, meas3, "2.4.0"))
    pkg4, meas4 = _pkg(tmp_path / "d", {"g_bar": [1.5e-11], "g_bar_basis": ["bin_coordinate"], "g_bar_bin_lo": [1e-11], "g_bar_bin_hi": [2e-11]})
    assert validate_v24(pkg4, meas4, "2.4.0") == []


def test_levels_and_closed_lists(tmp_path):
    pkg, meas = _pkg(tmp_path, {"g_bar": [1e-11], "err_level_status": ["stated"], "err_level": [None],
                                "g_bar_err_level_status": ["not_given_by_source"], "g_bar_err_level": [0.9],
                                "g_bar_basis": ["guessed"]},
                     obs_cols={"err_level_status": ["maybe"], "err_level": [None]})
    probs = validate_v24(pkg, meas, "2.4.0")
    assert any("err_level_status is stated but err_level is empty" in p for p in probs)
    assert any("g_bar_err_level_status is not_given_by_source" in p for p in probs)
    assert any("measurements: g_bar_basis has values outside" in p for p in probs)
    assert any("observables: err_level_status has values outside" in p for p in probs)


def test_terms_and_ruling(tmp_path):
    pkg, meas = _pkg(tmp_path, {"g_bar": [1e-11]},
                     terms_rows=[dict(KTERM, status="not_given_by_source"), dict(KTERM, term_id="y", scale="system"),
                                 dict(KTERM, term_id="z", in_error_columns="maybe")],
                     desc={"x_value_change_ruling": "D-999"})
    probs = validate_v24(pkg, meas, "2.4.0")
    assert sum("in_error_columns = no requires" in p for p in probs) == 2
    assert any("not yes or no" in p for p in probs)
    assert any("not a decision" in p for p in probs)


def test_ruling_must_be_ruled(tmp_path, monkeypatch):
    import aeg.validate as v
    root = tmp_path / "root"
    (root / "docs").mkdir(parents=True)
    (root / "docs/decisions.md").write_text("## D-200 — Pending\n\n**Ruling: pending.**\n\n## D-201 — Old\n\n**Ruling.** Yes.\n",
                                            encoding="utf-8")
    monkeypatch.setattr(v, "ROOT", root)
    pkg, meas = _pkg(tmp_path, {"g_bar": [1e-11]}, desc={"x_value_change_ruling": "D-200"})
    assert any("has no ruling yet" in p for p in validate_v24(pkg, meas, "2.4.0"))
    pkg2, meas2 = _pkg(tmp_path / "b", {"g_bar": [1e-11]}, desc={"x_value_change_ruling": "D-201"})
    assert validate_v24(pkg2, meas2, "2.4.0") == []
def test_subset_terms(tmp_path):
    term = {"term_id": "cal", "scale": "system", "applies_to": "aeg-s-000001;aeg-s-000002", "moves": "g_obs",
            "status": "not_given_by_source"}
    pkg, meas = _pkg(tmp_path, {"g_bar": [1e-11]}, terms_rows=[term])
    assert any("must have scale = dataset" in p for p in validate_v24(pkg, meas, "2.4.0"))
    pkg2, meas2 = _pkg(tmp_path / "b", {"g_bar": [1e-11]}, terms_rows=[dict(term, scale="dataset", applies_to="aeg-s-000001;aeg-s-999999")])
    assert any("applies_to" in p for p in validate_v22(pkg2, meas2))


def test_size_column_gate(tmp_path):
    term = {"term_id": "r", "scale": "point", "applies_to": "*", "moves": "both", "status": "given",
            "size_column": "r_err"}
    pkg, meas = _pkg(tmp_path, {"g_bar": [1e-11], "r_err": [0.1]}, terms_rows=[term])
    assert any("measurements size_column" in p for p in validate_v24(pkg, meas, "2.3.0"))
    assert validate_v24(pkg, meas, "2.4.0") == []
    pkg2, meas2 = _pkg(tmp_path / "b", {"g_bar": [1e-11], "system_id": ["aeg-s-000001"]},
                       terms_rows=[dict(term, size_column="system_id")])
    assert validate_v24(pkg2, meas2, "2.3.0") == []


def test_old_style_ruling_accepted(tmp_path):
    pkg, meas = _pkg(tmp_path, {"g_bar": [1e-11]}, desc={"x_value_change_ruling": "D-001"})
    assert validate_v24(pkg, meas, "2.4.0") == []
