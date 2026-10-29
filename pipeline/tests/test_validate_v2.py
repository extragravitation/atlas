"""Standard 2.0.0 validator rules (docs/data-standard.md §10), on a synthetic package."""

import copy
import csv
import json
from pathlib import Path

import pytest

astropy = pytest.importorskip("astropy")
from astropy.table import Table  # noqa: E402

from aeg import validate as V  # noqa: E402

DS, VER = "aeg-d-synth", "v1"


def _col(t, name, values, ucd, desc="Synthetic test column.", unit=None, dtype=None):
    t[name] = values if dtype is None else __import__("numpy").array(values, dtype=dtype)
    t[name].description = desc
    t[name].meta = {"ucd": ucd}
    if unit:
        t[name].unit = unit


def _write(t, path):
    t.meta["standard_version"] = "2.0.0"
    path.parent.mkdir(parents=True, exist_ok=True)
    t.write(path, format="ascii.ecsv", overwrite=True)


def make_pkg(root: Path, *, meas=None, obs=None, systems=None, desc=None, second=True) -> Path:
    pkg = root / "data/packages" / DS / VER
    m = {
        "measurement_id": [f"{DS}/{VER}/m000001"],
        "system_id": ["aeg-s-900001"],
        "kind": ["system_value"], "channel": ["dynamics"], "method_class": ["kinematic"],
        "method": ["half-light estimator"], "measured_quantity": ["g_obs"],
        "g_obs": [1e-10], "g_bar": [5e-11], "limit": ["none"],
        "stars_status": ["measured"], "gas_cold_status": ["absent"], "gas_hot_status": ["absent"],
        "observed_from": [f"{DS}/{VER}/o000001"], "baryonic_from": [f"{DS}/{VER}/o000002"],
        "model_dependence": ["none"], "evidence_tier": [2], "role": ["default"], "plotted": ["true"],
        "not_plotted_reason": [""], "assumptions": ["stellar_ml=2"], "adjustable": [""], "source_ref": ["Table 1"],
    }
    if meas:
        m.update(meas)
    t = Table()
    ucds = {"measurement_id": "meta.id;meta.main", "system_id": "meta.id", "g_obs": "phys.acceleration",
            "g_bar": "phys.acceleration;meta.modelled", "source_ref": "meta.ref", "evidence_tier": "meta.code.qual",
            "method": "meta.note", "assumptions": "meta.note", "adjustable": "meta.note", "observed_from": "meta.ref",
            "baryonic_from": "meta.ref", "not_plotted_reason": "meta.note", "delta_g": "phys.acceleration"}
    for k, v in m.items():
        _col(t, k, v, ucds.get(k, "meta.code"), unit="m / s2" if k in ("g_obs", "g_bar", "delta_g") else None)
    _write(t, pkg / "tables/measurements.ecsv")

    o = {
        "observable_id": [f"{DS}/{VER}/o000001", f"{DS}/{VER}/o000002"],
        "system_id": ["aeg-s-900001"] * 2,
        "side": ["observed", "baryonic"], "quantity": ["sigma_los", "luminosity"],
        "value": [5.0, 1e5], "unit": ["km / s", "solLum"], "limit": ["none", "none"],
        "steps": ["spectra;stellar_velocities;membership;dispersion_global", "photometry;luminosity"],
        "evidence_tier": [2, 2], "source_ref": ["Table 1", "Table 2"],
    }
    if obs:
        o.update(obs)
    t = Table()
    for k, v in o.items():
        _col(t, k, v, {"observable_id": "meta.id;meta.main", "system_id": "meta.id", "value": "meta.number",
                       "source_ref": "meta.ref", "evidence_tier": "meta.code.qual"}.get(k, "meta.code"))
    _write(t, pkg / "tables/observables.ecsv")

    s = {"system_id": ["aeg-s-900001"], "name_in_source": ["Synth 1"], "class_in_source": ["GC"],
         "taxonomy_kind": ["A3"], "kind_label": ["globular cluster"], "distance_mpc": [0.01],
         "distance_method": ["isochrone"], "distance_kinematic": ["false"], "properties": ["{}"]}
    if systems:
        s.update(systems)
    t = Table()
    for k, v in s.items():
        _col(t, k, v, {"system_id": "meta.id;meta.main", "name_in_source": "meta.id", "class_in_source": "src.class",
                       "distance_mpc": "pos.distance", "properties": "meta.note"}.get(k, "meta.code"),
             unit="Mpc" if k == "distance_mpc" else None)
    _write(t, pkg / "tables/systems.ecsv")

    d = {"name": DS, "standard_version": "2.0.0",
         "x_selection": [{"quantity": "members", "condition": ">=", "value": 10, "citation": "Synthetic"}],
         "x_baryon_inventory": [{"component": "stars", "status": "measured", "citation": "Synthetic"},
                                {"component": "atomic gas", "status": "absent_literature_limit", "citation": "Synthetic"}],
         "x_search_log": "docs/sources/search-log-A3.md#R0", "x_second_reading": {"by": "test", "date": "2026-10-29"}}
    if desc is not None:
        d = desc(copy.deepcopy(d))
    (pkg / "datapackage.json").write_text(json.dumps(d))
    if second:
        (pkg / "SECOND_READING.md").write_text("synthetic\n")
    (pkg / "checksums.sha256").write_text("")
    return pkg


@pytest.fixture
def root(tmp_path, monkeypatch):
    (tmp_path / "data/registry").mkdir(parents=True)
    with (tmp_path / "data/registry/systems.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["system_id", "name", "first_dataset", "assigned"])
        w.writerow(["aeg-s-900001", "Synth 1", f"{DS}/{VER}", "2026-10-29"])
    (tmp_path / "data/assumptions.json").write_text(json.dumps({"assumptions": [
        {"id": "stellar_ml", "datasets": [f"{DS}/{VER}"], "adjustable": False, "status": "draft"}]}))
    monkeypatch.setattr(V, "ROOT", tmp_path)
    return tmp_path


def test_valid_package_passes(root):
    assert V.validate(make_pkg(root)) == []


@pytest.mark.parametrize("kwargs,expect", [
    (dict(meas={"plotted": ["false"]}), "no not_plotted_reason"),
    (dict(meas={"not_plotted_reason": ["coverage_below_threshold"]}), "plotted but has a not_plotted_reason"),
    (dict(meas={"evidence_tier": [3]}), "tier 3 and must not be plotted"),
    (dict(meas={"model_dependence": ["guess"]}), "model_dependence has values outside"),
    (dict(meas={"observed_from": [f"{DS}/{VER}/o000009"]}), "unknown observable"),
    (dict(meas={"observed_from": [f"{DS}/{VER}/o000002"]}), "baryonic-side observable"),
    (dict(obs={"quantity": ["sigma_los", "v_rot"]}), "not allowed on the baryonic side"),
    (dict(obs={"steps": ["spectra;magic", "photometry;luminosity"]}), "steps not from the ladders"),
    (dict(systems={"taxonomy_kind": ["B1"]}), "not A0–A10"),
    (dict(systems={"kind_label": ["ambiguous: dwarf galaxy or star cluster"]}), "labelled ambiguous but not in A7"),
    (dict(systems={"distance_kinematic": ["true"]}), "kinematic distance but plotted rows"),
    (dict(desc=lambda d: {k: v for k, v in d.items() if k != "x_selection"}), "x_selection missing"),
    (dict(desc=lambda d: {**d, "x_baryon_inventory": [{"component": "stars", "status": "assumed"}]}), "not in the closed list"),
    (dict(second=False), "SECOND_READING.md missing"),
])
def test_rule_violations_are_caught(root, kwargs, expect):
    problems = V.validate(make_pkg(root, **kwargs))
    assert any(expect in p for p in problems), problems


def test_limit_without_errors_and_delta_g(root):
    pkg = make_pkg(root, meas={"measured_quantity": ["delta_g"], "delta_g": [1e-13], "limit": ["upper"],
                               "plotted": ["false"], "not_plotted_reason": ["limit_only"]})
    assert V.validate(pkg) == []
    pkg = make_pkg(root, meas={"measured_quantity": ["delta_g"]})
    assert any("measures delta_g but delta_g is empty" in p for p in V.validate(pkg))
