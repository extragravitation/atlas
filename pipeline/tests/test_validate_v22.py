"""Synthetic tests for the data standard 2.2.0 rules (uncertainty terms, point-scale columns; D-083)."""

from pathlib import Path

from astropy.table import Table

from aeg.validate import validate_v22


def _pkg(tmp: Path, terms_rows, point_hi=None) -> tuple[Path, Table]:
    pkg = tmp / "aeg-d-test" / "v2"
    (pkg / "tables").mkdir(parents=True)
    Table({"system_id": ["aeg-s-000001"], "distance_err_mpc": [0.5]}).write(pkg / "tables/systems.ecsv", format="ascii.ecsv")
    if terms_rows is not None:
        cols = sorted({k for r in terms_rows for k in r})
        Table({c: [r.get(c, "") for r in terms_rows] for c in cols}).write(pkg / "tables/uncertainty_terms.ecsv", format="ascii.ecsv")
    meas = Table({"g_obs_err_hi": [1e-11], "g_obs_err_point_hi": [point_hi if point_hi is not None else 5e-12]})
    return pkg, meas


GOOD = {"term_id": "distance", "scale": "system", "applies_to": "*", "moves": "both", "status": "given",
        "size_column": "distance_err_mpc", "size_kind": "one_sigma", "covariance": "not_applicable"}


def test_good_package_passes(tmp_path):
    pkg, meas = _pkg(tmp_path, [GOOD, {"term_id": "ml", "scale": "dataset", "applies_to": "*", "moves": "g_bar",
                                       "status": "not_given_by_source"}])
    assert validate_v22(pkg, meas) == []


def test_missing_table(tmp_path):
    pkg, meas = _pkg(tmp_path, None)
    assert any("missing" in p for p in validate_v22(pkg, meas))


def test_closed_lists_and_sizes(tmp_path):
    bad = dict(GOOD, scale="galaxy", size_column="no_such_column")
    pkg, meas = _pkg(tmp_path, [bad])
    probs = validate_v22(pkg, meas)
    assert any("closed list" in p for p in probs)
    assert any("size_column" in p for p in probs)


def test_given_without_size(tmp_path):
    t = {k: v for k, v in GOOD.items() if k != "size_column"}
    pkg, meas = _pkg(tmp_path, [t])
    assert any("without a size" in p for p in validate_v22(pkg, meas))


def test_point_error_cannot_exceed_total(tmp_path):
    pkg, meas = _pkg(tmp_path, [GOOD], point_hi=2e-11)
    assert any("exceeds" in p for p in validate_v22(pkg, meas))


def test_unknown_assumption(tmp_path):
    pkg, meas = _pkg(tmp_path, [dict(GOOD, assumption_id="no_such_assumption")])
    assert any("not in the registry" in p for p in validate_v22(pkg, meas))
