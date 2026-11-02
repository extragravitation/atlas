"""aeg-d-sparc/v2 — the frozen reproduction test (REPRODUCTION.md, SHA-256 in sources.json).

Implements tests 1–11 and 13, named by the test numbers of REPRODUCTION.md. Test 12 (validator, site build, site_check, ledger) is the CI
checks job plus test_standard below. v1 is read as it was at commit bf5c9ba.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import pytest
from astropy.table import Table

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[3]
V1 = "data/packages/aeg-d-sparc/v1"
REF = "bf5c9ba"


def git_show(path: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), "show", f"{REF}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def read(text_or_path, from_git=False) -> Table:
    if from_git:
        return Table.read(git_show(text_or_path), format="ascii.ecsv")
    return Table.read(text_or_path, format="ascii.ecsv")


@pytest.fixture(scope="module")
def t():
    return {
        "m1": read(f"{V1}/tables/measurements.ecsv", True),
        "s1": read(f"{V1}/tables/systems.ecsv", True),
        "m2": read(HERE / "tables/measurements.ecsv"),
        "o2": read(HERE / "tables/observables.ecsv"),
        "s2": read(HERE / "tables/systems.ecsv"),
        "u2": read(HERE / "tables/uncertainty_terms.ecsv"),
    }


def vals(col):
    m = np.ma.getmaskarray(col)
    return [None if m[i] else col[i] for i in range(len(col))]


# --- A. values unchanged -----------------------------------------------------------------------

def test_1_2_rows_and_values_bitwise(t):
    m1, m2 = t["m1"], t["m2"]
    assert len(m2) == len(m1) == 3391
    for c in ("system_id", "source_ref"):
        assert list(m2[c]) == list(m1[c]), c
    for c in ("r_kpc", "g_obs", "g_bar", "g_bar_stars", "g_bar_stars_disk", "g_bar_stars_bulge", "g_bar_gas_cold"):
        a, b = vals(m1[c]), vals(m2[c])
        assert all((x is None and y is None) or (x is not None and y is not None and
                   np.float64(x).tobytes() == np.float64(y).tobytes()) for x, y in zip(a, b)), c


def test_3_systems_equal(t):
    s1, s2 = t["s1"], t["s2"]
    assert len(s2) == len(s1) == 175
    for c in s1.colnames:
        assert vals(s1[c]) == vals(s2[c]) or all(
            (x is None and y is None) or x == y or (isinstance(x, float) and math.isnan(x) and math.isnan(y))
            for x, y in zip(vals(s1[c]), vals(s2[c]))), c


# --- B. uncertainties --------------------------------------------------------------------------

def test_4_point_scale_g_obs(t):
    m = t["m2"]
    for r in m:
        expect = r["g_obs"] * 2 * r["x_sparc_e_v_obs"] / r["x_sparc_v_obs"]
        assert r["g_obs_err_point_lo"] == r["g_obs_err_point_hi"]
        assert math.isclose(r["g_obs_err_point_hi"], expect, rel_tol=1e-12, abs_tol=0)


def test_5_decomposition_reproduces_total(t):
    m1, m2, s = t["m1"], t["m2"], t["s2"]
    sys = {r["system_id"]: r for r in s}
    for r1, r2 in zip(m1, m2):
        g = sys[r2["system_id"]]
        di = math.radians(g["inclination_err_deg"])
        inc = math.radians(g["inclination_deg"])
        total2 = (r2["g_obs_err_point_hi"] ** 2 + (r2["g_obs"] * 2 * di / math.tan(inc)) ** 2
                  + (r2["g_obs"] * g["distance_err_mpc"] / g["distance_mpc"]) ** 2)
        assert math.isclose(total2, r1["g_obs_err_hi"] ** 2, rel_tol=1e-9), r2["measurement_id"]


def test_6_g_bar_total(t):
    m1, m2 = t["m1"], t["m2"]
    for c in ("g_bar_err_lo", "g_bar_err_hi"):
        assert vals(m1[c]) == vals(m2[c]), c
    for r in m2:
        if r["g_bar_err_hi"] is np.ma.masked:
            continue
        expect = (0.10 * r["g_bar_gas_cold"]) ** 2 + (0.25 * r["g_bar_stars"]) ** 2
        assert math.isclose(expect, r["g_bar_err_hi"] ** 2, rel_tol=1e-9, abs_tol=1e-60)
    assert np.ma.getmaskarray(m2["g_bar_err_point_lo"]).all() and np.ma.getmaskarray(m2["g_bar_err_point_hi"]).all()
    for c in ("g_obs_err_lo", "g_obs_err_hi", "g_bar_err_lo", "g_bar_err_hi", "g_obs_err_point_lo",
              "g_obs_err_point_hi", "g_bar_err_point_lo", "g_bar_err_point_hi"):
        d = m2[c].description.lower()
        assert "scale" in d or "point-scale" in d, c


EXPECTED_TERMS = {
    "inclination": ("system", "*", "g_obs", "given", "inclination"),
    "distance": ("system", "*", "g_obs", "given", "distance"),
    "hi_flux_calibration": ("system", "*", "g_bar", "given", None),
    "ml_scatter_galaxy": ("system", "*", "g_bar", "given", None),
    "ml_disk": ("dataset", "*", "g_bar", "given", "ml_disk"),
    "ml_bulge": ("dataset", "*", "g_bar", "given", "ml_bulge"),
    "geometry_3d_molecular": ("system", "*", "g_bar", "given", None),
    "g_bar_point": ("point", "*", "g_bar", "not_given_by_source", None),
}


def test_7_uncertainty_terms(t):
    u = t["u2"]
    rows = {r["term_id"]: r for r in u}
    assert set(rows) == set(EXPECTED_TERMS) and len(u) == len(EXPECTED_TERMS)
    for tid, (scale, applies, moves, status, aid) in EXPECTED_TERMS.items():
        r = rows[tid]
        assert (r["scale"], r["applies_to"], r["moves"], r["status"]) == (scale, applies, moves, status), tid
        got_aid = None if r["assumption_id"] in (None, "", np.ma.masked) else r["assumption_id"]
        assert got_aid == aid, tid
        assert r["covariance"] == "not_published", tid
        if status == "given":
            assert r["citation"] and r["locator"], tid
    assert rows["inclination"]["size_column"] == "inclination_err_deg" and rows["inclination"]["size_kind"] == "one_sigma"
    assert rows["distance"]["size_column"] == "distance_err_mpc" and rows["distance"]["size_kind"] == "one_sigma"
    assert rows["hi_flux_calibration"]["size_value"] == 0.10 and rows["hi_flux_calibration"]["size_kind"] == "as_released"
    assert rows["ml_scatter_galaxy"]["size_value"] == 0.25 and rows["ml_scatter_galaxy"]["size_kind"] == "as_released"
    note = rows["ml_scatter_galaxy"]["note"].lower()
    assert "atlas" in note and "within" in note and "between" in note
    assert (rows["ml_disk"]["size_lo"], rows["ml_disk"]["size_hi"], rows["ml_disk"]["size_kind"]) == (0.2, 0.7, "range")
    reg = {a["id"]: a for a in json.loads((REPO / "data/assumptions.json").read_text(encoding="utf-8"))["assumptions"]}
    b = reg["ml_bulge"]["datasets"]["aeg-d-sparc/v2"]
    assert (rows["ml_bulge"]["size_lo"], rows["ml_bulge"]["size_hi"]) == (b["min"], b["max"])
    assert rows["geometry_3d_molecular"]["size_value"] == 0.20 and "small radii" in rows["geometry_3d_molecular"]["locator"]


# --- C. 2.0 structure --------------------------------------------------------------------------

def test_8_observables(t):
    m, o, s = t["m2"], t["o2"], t["s2"]
    obs = {r["observable_id"]: r for r in o}
    assert all(r["evidence_tier"] == 1 for r in o)
    names = {r["system_id"]: r["name_in_source"] for r in s}
    bulge_sys = {r["system_id"] for r in m if r["x_sparc_v_bul"] != 0.0}
    dist = {}
    for r in o:
        if r["quantity"] == "distance":
            assert r["side"] == "observed" and r["unit"] == "Mpc" and r["system_id"] not in dist
            dist[r["system_id"]] = r["observable_id"]
    assert len(dist) == 175
    sys = {r["system_id"]: r for r in s}
    for sid, oid in dist.items():
        assert obs[oid]["value"] == sys[sid]["distance_mpc"] and obs[oid]["err_hi"] == sys[sid]["distance_err_mpc"]
    used = set(dist.values())
    for r in m:
        of = r["observed_from"].split(";")
        assert len(of) == 2 and of[1] == dist[r["system_id"]]
        v = obs[of[0]]
        assert (v["side"], v["quantity"], v["unit"], v["r_kind"]) == ("observed", "v_rot", "km / s", "3d")
        assert v["value"] == r["x_sparc_v_obs"] and v["err_lo"] == v["err_hi"] == r["x_sparc_e_v_obs"] and v["r_kpc"] == r["r_kpc"]
        assert v["steps"] == "rotation_curve"
        bf = [obs[x] for x in r["baryonic_from"].split(";")]
        want = [("v_circ_component", "x_sparc_v_gas", "hi_21cm;surface_density;helium_factor;potential_from_density"),
                ("v_circ_component", "x_sparc_v_disk", "photometry;surface_density;potential_from_density"),
                ("surface_brightness", "x_sparc_sb_disk", "photometry;surface_density")]
        if r["system_id"] in bulge_sys:
            want += [("v_circ_component", "x_sparc_v_bul", "photometry;surface_density;potential_from_density"),
                     ("surface_brightness", "x_sparc_sb_bul", "photometry;surface_density")]
        assert len(bf) == len(want), r["measurement_id"]
        for b, (q, colname, steps) in zip(bf, want):
            assert b["side"] == "baryonic" and b["quantity"] == q and b["steps"] == steps and b["r_kpc"] == r["r_kpc"]
            assert b["value"] == r[colname], (r["measurement_id"], colname)
            assert b["unit"] == ("km / s" if q == "v_circ_component" else "solLum / pc2")
        assert "Υ = 1" in bf[1]["source_ref"]
        used.update(r["observed_from"].split(";") + r["baryonic_from"].split(";"))
    assert used == set(obs), "every observable is used by a measurement"
    assert names  # systems present


def test_9_measurement_columns(t):
    m, s = t["m2"], t["s2"]
    names = {r["system_id"]: r["name_in_source"] for r in s}
    modelled = {"D512-2", "D564-8", "D631-7"}
    for r in m:
        assert (r["measured_quantity"], r["limit"], r["role"], int(r["evidence_tier"])) == ("g_obs", "none", "default", 1)
        assert str(r["plotted"]).lower() == "true"
        gas_modelled = names[r["system_id"]] in modelled
        assert r["model_dependence"] == ("observable_form" if gas_modelled else "none")
        note = "" if r["notes"] is np.ma.masked else str(r["notes"] or "")
        assert ("exponential" in note) == gas_modelled
    flagged = sorted(r["measurement_id"].split("/")[-1] for r in m if "reproduction_mismatch" in str(r["flags"]))
    v1 = sorted(r["measurement_id"].split("/")[-1] for r in t["m1"] if "reproduction_mismatch" in str(r["flags"]))
    assert flagged == v1 and len(flagged) == 4


def test_10_descriptor():
    d = json.loads((HERE / "datapackage.json").read_text(encoding="utf-8"))
    assert d["standard_version"] == "2.3.0"
    assert any("not a statistically complete sample" in e["value"] for e in d["x_selection"])
    inv = {e["component"]: e["status"] for e in d["x_baryon_inventory"]}
    assert inv == {"stars": "measured", "atomic gas": "measured", "helium": "modelled", "molecular gas": "known_unmeasured",
                   "hot gas": "not_addressed", "ionised gas": "not_addressed", "dust": "not_addressed"}
    mol = next(e for e in d["x_baryon_inventory"] if e["component"] == "molecular gas")["citation"]
    assert "minor dynamical component" in mol
    assert "D-005" in d["x_search_log"] and "#48" in d["x_search_log"]
    assert d["x_second_reading"]["file"] == "SECOND_READING.md" and (HERE / "SECOND_READING.md").is_file()


def test_11_second_reading(t):
    m, s = t["m2"], t["s2"]
    rd = list(csv.DictReader((HERE / "reading/second-reading/massmodels.csv").open(encoding="utf-8")))
    gd = list(csv.DictReader((HERE / "reading/second-reading/galaxies.csv").open(encoding="utf-8")))
    assert len(rd) == len(m) and len(gd) == len(s)
    names = {r["system_id"]: r["name_in_source"] for r in s}
    sysd = {r["system_id"]: r for r in s}
    pairs = [("R_kpc", "r_kpc"), ("Vobs", "x_sparc_v_obs"), ("e_Vobs", "x_sparc_e_v_obs"), ("Vgas", "x_sparc_v_gas"),
             ("Vdisk", "x_sparc_v_disk"), ("Vbul", "x_sparc_v_bul"), ("SBdisk", "x_sparc_sb_disk"), ("SBbul", "x_sparc_sb_bul")]
    bad = []
    for a, b in zip(rd, m):
        if a["galaxy"] != names[b["system_id"]]:
            bad.append((b["measurement_id"], "galaxy"))
        for ca, cb in pairs:
            if float(a[ca]) != float(b[cb]):
                bad.append((b["measurement_id"], ca))
        if abs(float(a["D_Mpc"]) - sysd[b["system_id"]]["distance_mpc"]) > 0.0051:
            bad.append((b["measurement_id"], "D"))
    for a, g in zip(gd, s):
        props = json.loads(g["properties"])
        checks = [(a["galaxy"], g["name_in_source"]), (float(a["D_Mpc"]), g["distance_mpc"]), (float(a["e_D"]), g["distance_err_mpc"]),
                  (float(a["Inc"]), g["inclination_deg"]), (float(a["e_Inc"]), g["inclination_err_deg"]), (int(a["Q"]), props["quality_flag_Q"]),
                  (float(a["L36"]), props["luminosity_3p6_1e9_solLum"]), (float(a["MHI"]), props["m_hi_1e9_solMass"]),
                  (float(a["Vflat"]), props["v_flat_km_s"]), (a["Ref"], props["rotation_curve_refs"])]
        for i, (x, y) in enumerate(checks):
            if x != y:
                bad.append((g["system_id"], i))
    assert not bad, bad[:20]


def test_13_v1_untouched():
    listed = git_show(f"{V1}/checksums.sha256")
    for line in listed.splitlines():
        digest, name = line.split(None, 1)
        assert hashlib.sha256((REPO / V1 / name.strip()).read_bytes()).hexdigest() == digest, name


def test_12_standard():
    import sys
    sys.path.insert(0, str(REPO / "pipeline"))
    from aeg.validate import validate
    assert validate(HERE) == []
