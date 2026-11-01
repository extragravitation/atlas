"""Synthetic tests of the A6 strong-lensing conversion (data/packages/aeg-d-strong-lensing/v1/convert.py).

SYNTHETIC: every input value below is made up for code tests. No real lens value is read, and the
real conversion is never run (it refuses without the gas term, which is tested here).
"""

import csv
import importlib.util
import math
import sys
from pathlib import Path

import pytest

from aeg import lensing as L

PKG = Path(__file__).resolve().parents[2] / "data/packages/aeg-d-strong-lensing/v1"
spec = importlib.util.spec_from_file_location("a6convert", PKG / "convert.py")
cv = importlib.util.module_from_spec(spec)
sys.modules["a6convert"] = cv  # dataclasses look the module up while it loads
spec.loader.exec_module(cv)

COLS = ["scope", "system", "record", "quantity", "value", "err_minus", "err_plus", "unit", "form",
        "location", "url", "status", "settled_by", "note"]
SL, S4, MA, SN = "SYNTHETIC SLACS-like", "SYNTHETIC S4TM-like", "SYNTHETIC MaNGA-like", "SYNTHETIC SNELLS-like"
VZ = "https://vizier.example/SYNTHETIC"


def row(scope, system, record, quantity, value, lo="", hi="", unit="", form="linear", status="default", note="", url=VZ):
    return dict(zip(COLS, [scope, system, record, quantity, value, lo, hi, unit, form, "SYNTHETIC", url, status, "SYNTHETIC", note]))


def slacs_like(system, z_l, status_r5="default", q5=("default candidate (Q5)", "range top for BC03 (Q5)",
                                                      "range top for M05 (Q5)")):
    d, top, mtop = q5
    th = "1.0"
    pre = f"inside R_Ein = R5 bSIE (R13 thetaE = {th});"
    return [
        row(SL, system, "R5", "z_l", z_l, status=status_r5, note="spectroscopic (SYNTHETIC)"),
        row(SL, system, "R5", "z_s", "0.6", status=status_r5, note="spectroscopic (SYNTHETIC)"),
        row(SL, system, "R5", "kind", "E", form="", status=status_r5),
        row(SL, system, "R5", "theta_E", th, unit="arcsec", status=status_r5, note="SIE; no per-lens error"),
        row(SL, system, "R13", "mstar", "5", "1", "2", "1e10 Msun", status=d, note=f"{pre} Chabrier, BC03; SYNTHETIC"),
        row(SL, system, "R13", "mstar", "9", "3", "4", "1e10 Msun", status=top, note=f"{pre} Salpeter, BC03; SYNTHETIC"),
        row(SL, system, "R13", "mstar", "4", "1", "1", "1e10 Msun", status=d, note=f"{pre} Kroupa, Maraston 2005; SYNTHETIC"),
        row(SL, system, "R13", "mstar", "6", "2", "2", "1e10 Msun", status=mtop, note=f"{pre} Salpeter, Maraston 2005; SYNTHETIC"),
    ]


def synthetic_rows():
    rows = [
        row(SL, "(record)", "R5", "H0", "70", unit="km s-1 Mpc-1"), row(SL, "(record)", "R5", "Om", "0.3"),
        row(SL, "(record)", "R13", "H0", "70", unit="km s-1 Mpc-1"), row(SL, "(record)", "R13", "Om", "0.3"),
        row(S4, "(record)", "R10", "H0", "70", unit="km s-1 Mpc-1"), row(S4, "(record)", "R10", "Om", "0.274"),
    ]
    rows += slacs_like("SYN-THETA", "0.2")                                    # theta_E only -> M_E computed
    rows += slacs_like("SYN-FALLBACK", "0.15", status_r5="pending Q6", q5=("pending Q6",) * 3)  # D-075 item 2
    rows += slacs_like("SYN-EPOCH", "0.35")                                   # complete inputs, z_l >= 0.30
    rows += [                                                                 # late-type: recorded, not plotted
        row(SL, "SYN-LATE", "R5", "z_l", "0.1", status="record-only (kind)", note="spectroscopic"),
        row(SL, "SYN-LATE", "R5", "z_s", "0.5", status="record-only (kind)", note="spectroscopic"),
        row(SL, "SYN-LATE", "R5", "kind", "L", form="", status="record-only (kind)"),
    ]
    rows += [                                                                 # printed M_E + profile step
        row(S4, "SYN-PRINTED", "R10", "z_l", "0.15", note="spectroscopic"),
        row(S4, "SYN-PRINTED", "R10", "z_s", "0.7", note="spectroscopic"),
        row(S4, "SYN-PRINTED", "R10", "kind", "E-S-A", form=""),
        row(S4, "SYN-PRINTED", "R10", "theta_E", "1.1", unit="arcsec"),
        row(S4, "SYN-PRINTED", "R10", "M_E", "11.0", unit="Msun", form="log10"),
        row(S4, "SYN-PRINTED", "R10", "mstar", "11.3", unit="Msun", form="log10", note="total; Chabrier; SYNTHETIC"),
        row(S4, "SYN-PRINTED", "R10", "R_e", "2.0", unit="arcsec", note="de Vaucouleurs (n = 4) fit; SYNTHETIC"),
    ]
    rows += [                                                                 # L x M/L, printed R_E (kpc), source says gas negligible
        row(MA, "J1436+4943", "R32", "z_l", "0.12", note="spectroscopic"),
        row(MA, "J1436+4943", "R32", "z_s", "1.2", note="spectroscopic"),
        row(MA, "J1436+4943", "R32", "kind", "elliptical", form=""),
        row(MA, "J1436+4943", "R32", "theta_E", "2.0", "0.04", "0.04", "arcsec"),
        row(MA, "J1436+4943", "R32", "R_E_kpc", "4.5", "0.1", "0.1", "kpc", status="pending Q4"),
        row(MA, "J1436+4943", "R32", "M_E", "25", "1", "1", "1e10 Msun"),
        row(MA, "J1436+4943", "R32", "L_in_aperture", "6.0", "0.1", "0.1", "1e10 Lsun (i)", status="pending Q3"),
        row(MA, "J1436+4943", "R32", "ML_stellar_pop", "3.0", "0.3", "0.3", "Msun/Lsun (i)", status="pending Q3", note="Kroupa"),
        row(MA, "J1436+4943", "R32", "cosmology", "named, no numbers", form="", status="pending Q4"),
    ]
    rows += [                                                                 # MGE default: not computable in v1
        row(SN, "SYN-MGE (SNL-1)", "R61", "z_l", "0.03", note="spectroscopic"),
        row(SN, "SYN-MGE (SNL-1)", "R61", "z_s", "0.9", note="spectroscopic"),
        row(SN, "SYN-MGE (SNL-1)", "R61", "kind", "E/S0", form=""),
        row(SN, "SYN-MGE (SNL-1)", "R61", "M_aperture", "9.0", "0.2", "0.2", "1e10 Msun", status="pending Q1"),
        row(SN, "SYN-MGE (SNL-1)", "R61", "aperture", "2.4", unit="arcsec", status="pending Q1"),
        row(SN, "SYN-MGE (SNL-1)", "R61", "H0", "70.4", unit="km s-1 Mpc-1"),
        row(SN, "SYN-MGE (SNL-1)", "R61", "Om", "0.272"),
        row(SN, "SYN-MGE (SNL-1)", "R33", "mstar_profile", "MGE", form="", status="pending Q1, Q8"),
    ]
    return rows


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    return path


@pytest.fixture(scope="module")
def result():
    gas = cv.parse_gas_term(cv.SYNTHETIC_GAS, synthetic=True)
    return cv.convert(synthetic_rows(), gas, synthetic=True)


def by_scope_name(result, name):
    sid = next(s["system_id"] for s in result["systems"] if s["name_in_source"] == name)
    return [m for m in result["measurements"] if m["system_id"] == sid]


def test_theta_only_mass_computed_with_frozen_functions(result):
    (d, alt) = by_scope_name(result, "SYN-THETA")
    m_e = L.einstein_mass_msun(1.0, 0.2, 0.6, 70, 0.3)
    r_e = L.einstein_radius_kpc(1.0, 0.2, 70, 0.3)
    assert d["x_sl_m_e_source"] == "computed" and d["role"] == "default" and d["plotted"] == "true"
    assert d["x_sl_m_e_msun"] == pytest.approx(m_e, rel=1e-12) and d["r_kpc"] == pytest.approx(r_e, rel=1e-12)
    assert d["g_obs"] == pytest.approx(L.projected_acceleration(m_e, r_e), rel=1e-12)
    assert d["g_bar_stars"] == pytest.approx(L.projected_acceleration(5e10, r_e), rel=1e-12)
    assert d["r_kind"] == "projected" and d["x_sl_projection"] == "projected"
    assert "sample_level_error" in d["x_sl_flags"]  # R5's 2% (D-075 item 4)
    assert d["x_sl_mstar_top_msun"] == pytest.approx(9e10)  # Salpeter-BC03 top (D-075 item 5)
    assert "sl_stellar_imf" in d["adjustable"]
    # M05 pair: alternative row, never plotted, pointing at the default
    assert alt["role"] == "alternative" and alt["alternative_of"] == d["measurement_id"]
    assert alt["plotted"] == "false" and alt["not_plotted_reason"] == "alternative_value"
    assert alt["x_sl_mstar_re_msun"] == pytest.approx(4e10) and alt["x_sl_mstar_top_msun"] == pytest.approx(6e10)


def test_synthetic_gas_term_enters_gbar(result):
    (d, _) = by_scope_name(result, "SYN-THETA")
    r_e = d["r_kpc"]
    assert d["g_bar_gas_cold"] == pytest.approx(L.projected_acceleration(0.01 * 5e10, r_e), rel=1e-12)
    assert d["g_bar_gas_hot"] == pytest.approx(L.projected_acceleration(0.02 * 5e10, r_e), rel=1e-12)
    assert d["g_bar"] == pytest.approx(d["g_bar_stars"] + d["g_bar_gas_cold"] + d["g_bar_gas_hot"], rel=1e-12)
    assert d["gas_cold_status"] == "modelled" and "SYNTHETIC" in d["x_sl_gas_term"]


def test_printed_mass_and_profile_step(result):
    (d,) = by_scope_name(result, "SYN-PRINTED")
    f = L.sersic_projected_fraction(1.1, 2.0, 4.0)
    r_e = L.einstein_radius_kpc(1.1, 0.15, 70, 0.274)
    assert d["x_sl_m_e_source"] == "printed" and d["x_sl_m_e_msun"] == pytest.approx(1e11, rel=1e-12)
    assert d["x_sl_profile_fraction"] == pytest.approx(f, rel=1e-12)
    assert d["x_sl_mstar_re_msun"] == pytest.approx(10 ** 11.3 * f, rel=1e-12)
    assert d["g_obs"] == pytest.approx(L.projected_acceleration(1e11, r_e), rel=1e-12)
    for flag in ("mstar_in_RE_from_profile", "profile_differs_from_mass_photometry", "imf_top_not_read"):
        assert flag in d["x_sl_flags"]
    assert "no_uncertainty" in d["flags"] and d["g_obs_err_lo"] is None
    assert d["x_sl_mstar_top_msun"] is None and "sl_stellar_imf" not in d["adjustable"]


def test_l_times_ml_printed_re_and_source_negligible_gas(result):
    (d,) = by_scope_name(result, "J1436+4943")
    m = 6.0e10 * 3.0
    assert d["x_sl_mstar_route"] == "L_times_ML" and d["x_sl_mstar_re_msun"] == pytest.approx(m, rel=1e-12)
    assert d["g_bar_err_lo"] / d["g_bar_stars"] == pytest.approx(math.hypot(0.1 / 6.0, 0.3 / 3.0), rel=1e-12)
    assert d["r_kpc"] == 4.5 and d["x_sl_r_e_source"] == "printed"
    assert d["g_obs"] == pytest.approx(L.projected_acceleration(25e10, 4.5), rel=1e-12)
    for flag in ("mstar_from_L_times_ML", "R_E_printed_kpc", "cosmology_named_only", "gas_negligible_source_assumption"):
        assert flag in d["x_sl_flags"]
    # synthetic gas term says source_negligible = zero
    assert d["g_bar_gas_cold"] == 0.0 and d["gas_cold_status"] == "absent"
    assert d["g_bar"] == pytest.approx(d["g_bar_stars"], rel=1e-15)


def test_fallback_record(result):
    (d, alt) = by_scope_name(result, "SYN-FALLBACK")
    assert d["plotted"] == "true" and "fallback_record" in d["x_sl_flags"]
    assert d["x_sl_mstar_re_msun"] == pytest.approx(5e10)  # Chabrier-BC03 of R13 (D-075 items 2, 5)


def test_not_plotted_cases(result):
    (d, _) = by_scope_name(result, "SYN-EPOCH")
    assert d["plotted"] == "false" and d["not_plotted_reason"] == "epoch_gap" and "epoch_gap_v1" in d["x_sl_flags"]
    assert by_scope_name(result, "SYN-LATE") == [] and by_scope_name(result, "SYN-MGE (SNL-1)") == []
    sysrows = {s["name_in_source"]: s for s in result["systems"]}
    assert sysrows["SYN-LATE"]["taxonomy_kind"] == "A4" and '"recorded"' in sysrows["SYN-LATE"]["properties"]
    assert "not early-type" in sysrows["SYN-LATE"]["properties"]
    assert "MGE" in sysrows["SYN-MGE (SNL-1)"]["properties"] and '"recorded"' in sysrows["SYN-MGE (SNL-1)"]["properties"]


def test_arithmetic_check_passes_and_catches_tampering(result):
    rows = [dict(m) for m in result["measurements"]]
    cv.arithmetic_check(rows)
    rows[0]["g_bar"] *= 1 + 1e-6
    with pytest.raises(SystemExit):
        cv.arithmetic_check(rows)


def test_formula_check_and_profile_step_check():
    gas = cv.parse_gas_term(cv.SYNTHETIC_GAS, synthetic=True)
    res = cv.convert(synthetic_rows(), gas, synthetic=True)
    fc = {r["name"]: r for r in res["formula_check"]}
    assert fc["SYN-PRINTED"]["m_e_computed"] == pytest.approx(L.einstein_mass_msun(1.1, 0.15, 0.7, 70, 0.274), rel=1e-12)
    assert fc["SYN-PRINTED"]["ratio"] == pytest.approx(fc["SYN-PRINTED"]["m_e_computed"] / 1e11, rel=1e-12)
    # D-075 item 5 profile-step check: a record printing a total, a mass inside R_E and its light profile
    pre = "inside R_Ein = R5 bSIE (R13 thetaE = 1.2);"
    rows = [
        row(SL, "SYN-PCHK", "R13", "mstar", "5", status="record-only", unit="1e10 Msun", note=f"{pre} Chabrier, BC03"),
        row(SL, "SYN-PCHK", "R13", "mstar", "12", status="record-only", unit="1e10 Msun", note="total; Chabrier, BC03"),
        row(SL, "SYN-PCHK", "R13", "R_e", "2.5", unit="arcsec", status="record-only", note="de Vaucouleurs"),
    ]
    systems, _ = cv.group_systems(rows)
    (p,) = cv.profile_step_check(systems)
    f = L.sersic_projected_fraction(1.2, 2.5, 4.0)
    assert p["mstar_in_re_computed"] == pytest.approx(12e10 * f, rel=1e-12)
    assert p["ratio"] == pytest.approx(12e10 * f / 5e10, rel=1e-12)


def test_unknown_status_is_an_error():
    with pytest.raises(ValueError):
        cv.resolve(row(SL, "X", "R5", "z_l", "0.1", status="pending Q99"))


def _snapshot():
    return sorted((str(p.relative_to(PKG)), p.stat().st_mtime_ns) for p in PKG.rglob("*") if "__pycache__" not in p.parts)


def test_refuses_without_gas_term(monkeypatch, tmp_path, capsys):
    before = _snapshot()
    monkeypatch.setattr(cv, "GAS_TERM_FILE", tmp_path / "gas_term.json")  # absent

    def boom(*a, **k):
        raise AssertionError("inputs must not be read before the gas term is set")
    monkeypatch.setattr(cv, "load_inputs", boom)
    monkeypatch.setattr(cv, "convert", boom)
    assert cv.main([]) == 0  # skip, not fail: CI is not blocked while the ruling is pending
    assert "SKIPPED: REFUSED: the gas term inside R_E is not set" in capsys.readouterr().out
    assert _snapshot() == before and not (PKG / "tables").exists()


def test_incomplete_gas_term_refused():
    with pytest.raises(cv.Refused):
        cv.parse_gas_term({"assumption_id": "x", "decision": "D-0xx", "form": "fraction_of_mstar_in_RE",
                           "components": {"gas_cold": {"default": 0.1, "min": 0.0, "max": 0.2}}, "ref": "r"})
    with pytest.raises(cv.Refused):  # a form using the observed side is never allowed
        cv.parse_gas_term({**cv.SYNTHETIC_GAS, "form": "fraction_of_M_E"})


def test_synthetic_switch_guards_and_writes_only_outside(tmp_path, capsys):
    before = _snapshot()
    inp = write_csv(tmp_path / "synthetic.csv", synthetic_rows())
    out = tmp_path / "out"
    assert cv.main(["--synthetic-gas", "--inputs", str(cv.INPUTS), "--out", str(out)]) == 3  # real inputs
    assert cv.main(["--synthetic-gas", "--inputs", str(inp), "--out", str(PKG / "tables")]) == 3  # inside package
    bad = write_csv(tmp_path / "bad.csv", [row("SLACS", "X", "R5", "z_l", "0.1")])
    assert cv.main(["--synthetic-gas", "--inputs", str(bad), "--out", str(out)]) == 3  # not labelled synthetic
    assert cv.main(["--inputs", str(inp)]) == 3  # --inputs only with --synthetic-gas
    assert cv.main(["--synthetic-gas", "--inputs", str(inp), "--out", str(out)]) == 0
    assert (out / "tables/measurements.ecsv").is_file() and (out / "checks/formula_check.ecsv").is_file()
    assert "SYNTHETIC" in (out / "tables/measurements.ecsv").read_text(encoding="utf-8")
    assert _snapshot() == before
