"""Reproduction test for aeg-d-xcop/v1, implementing REPRODUCTION.md exactly.

REPRODUCTION.md was frozen (hash in sources.json) before this file or
convert.py existed. Reference values are parsed from REPRODUCTION.md itself,
not copied from the converter. Failures are handled under D-019; the test is
not changed to make it pass.
"""

from __future__ import annotations

import hashlib
import io
import json
import math
import re
import tarfile
from pathlib import Path

import astropy.constants as const
import astropy.units as u
import numpy as np
import pytest
from astropy.io import fits
from astropy.table import Table

PKG = Path(__file__).resolve().parents[1]
TAR = PKG / "source/allfiles.tar.gz"
TOL = 0.015
INTEGRITY = 1e-9
STARS = {"A85", "A644", "A1795", "A2029", "A2142", "A2319", "ZW1215"}
GCONV = (const.G * u.Msun / u.kpc**2).to(u.m / u.s**2).value


def reference() -> dict[str, dict[str, float]]:
    """Table 1 rows of REPRODUCTION.md: masses in 1e14 Msun, R500 in Mpc."""
    out = {}
    for line in (PKG / "REPRODUCTION.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and re.fullmatch(r"(A\d+|RXC1825|ZW1215)", cells[0]):
            v = [float(c.split("±")[0]) for c in cells[1:]]
            out[cells[0]] = {"m500kpc": v[0], "m1000kpc": v[1], "m1500kpc": v[2], "r500": v[3], "m500": v[4]}
    return out


REF = reference()
CLUSTERS = list(REF)

# Known issue #19 (D-019): checks that fail against the frozen tolerance. They are kept unchanged and
# marked as strict expected failures; any change in this set (a new failure, or one that passes) fails.
KNOWN_FAIL = {
    ("2", "A644", 500), ("2", "A644", 1000), ("2", "A644", 1500), ("2", "A2319", 1000), ("2", "A2319", 1500),
    ("3a", "A644"), ("3a", "A2319"), ("3b", "A644"), ("3b", "A2029"), ("3b", "A2319"),
}
XFAIL = pytest.mark.xfail(strict=True, reason="Known issue #19 (D-019): archive differs from Ettori et al. 2019 Table 1; see REPRODUCTION_RESULT.md")


def cases(test, with_radius=False):
    out = []
    for c in CLUSTERS:
        for r, key in ([(500, "m500kpc"), (1000, "m1000kpc"), (1500, "m1500kpc")] if with_radius else [(None, None)]):
            ident = (test, c, r) if with_radius else (test, c)
            args = (c, r, key) if with_radius else (c,)
            out.append(pytest.param(*args, marks=[XFAIL] if ident in KNOWN_FAIL else [], id="-".join(map(str, ident[1:]))))
    return out


def loglog(x_new, x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(np.exp(np.interp(math.log(x_new), np.log(x), np.log(y))))


@pytest.fixture(scope="module")
def archive():
    with tarfile.open(TAR) as tar:
        names = set(tar.getnames())
        data = {}
        for n in names:
            if n.endswith(("_hydro_mass.fits", "_fgas_profile.fits", "_mstar.fits")):
                data[n] = fits.open(io.BytesIO(tar.extractfile(n).read()))
    return names, data


@pytest.fixture(scope="module")
def meas():
    return Table.read(PKG / "tables/measurements.ecsv", format="ascii.ecsv")


@pytest.fixture(scope="module")
def systems():
    return Table.read(PKG / "tables/systems.ecsv", format="ascii.ecsv")


def test_reproduction_file_is_the_frozen_one():
    spec = json.loads((PKG / "sources.json").read_text(encoding="utf-8"))
    assert hashlib.sha256((PKG / "REPRODUCTION.md").read_bytes()).hexdigest() == spec["reproduction_file"]["sha256"]


def test_reference_parsed_completely():
    assert len(REF) == 12


# 1. Coverage
def test_1_coverage(archive, meas, systems):
    names, _ = archive
    assert sorted(str(x) for x in systems["name_in_source"]) == sorted(CLUSTERS)
    with_stars = {c for c in CLUSTERS if f"{c}/{c}_mstar.fits" in names}
    assert with_stars == STARS
    sid = {str(r["system_id"]): str(r["name_in_source"]) for r in systems}
    status = {}
    for r in meas:
        status.setdefault(sid[str(r["system_id"])], set()).add(str(r["stars_status"]))
    assert {c for c, s in status.items() if s == {"measured"}} == STARS
    assert {c for c, s in status.items() if s == {"modelled"}} == set(CLUSTERS) - STARS


# 2. The archive is the paper's analysis
@pytest.mark.parametrize("cluster,r_kpc,key", cases("2", with_radius=True))
def test_2_archive_nfw_matches_table1(archive, cluster, r_kpc, key):
    h = archive[1][f"{cluster}/{cluster}_hydro_mass.fits"][1].data
    m = loglog(r_kpc, h["RADIUS"], h["M_NFW"]) / 1e14
    assert abs(m / REF[cluster][key] - 1) <= TOL, f"{cluster} M_NFW(<{r_kpc} kpc) = {m:.4f}e14, Table 1 {REF[cluster][key]}e14"


# 3. R500 is consistent
@pytest.mark.parametrize("cluster", cases("3a"))
def test_3a_hydro_mass_at_r500(archive, cluster):
    h = archive[1][f"{cluster}/{cluster}_hydro_mass.fits"][1].data
    m = loglog(REF[cluster]["r500"] * 1000, h["RADIUS"], h["M_NFW"]) / 1e14
    assert abs(m / REF[cluster]["m500"] - 1) <= TOL, f"{cluster} M_NFW(<R500) = {m:.4f}e14, Table 1 M500 {REF[cluster]['m500']}e14"


@pytest.mark.parametrize("cluster", cases("3b"))
def test_3b_gas_file_mass_at_r500(archive, cluster):
    g = archive[1][f"{cluster}/{cluster}_fgas_profile.fits"][1].data
    m = loglog(1.0, g["RADIUS"], g["M_NFW"]) / 1e14
    assert abs(m / REF[cluster]["m500"] - 1) <= TOL, f"{cluster} gas-file M_NFW(R/R500=1) = {m:.4f}e14, Table 1 M500 {REF[cluster]['m500']}e14"


# 4. Conversion integrity, recomputed independently from the archive
def test_4_conversion_integrity(archive, meas, systems):
    _, data = archive
    sid = {str(r["system_id"]): str(r["name_in_source"]) for r in systems}
    bad = []
    for row in meas:
        c = sid[str(row["system_id"])]
        h = data[f"{c}/{c}_hydro_mass.fits"][1]
        g = data[f"{c}/{c}_fgas_profile.fits"][1]
        r = float(row["r_kpc"])
        k = int(str(row["source_ref"]).rsplit("row ", 1)[1]) - 1
        assert float(h.data["RADIUS"][k]) == r
        f = GCONV / r**2
        checks = {
            "g_obs": f * float(h.data["M_FORW"][k]),
            "g_bar_gas_hot": f * loglog(r, np.asarray(g.data["RADIUS"], float) * float(g.header["R500"]), g.data["MGAS"]),
        }
        if c in STARS:
            s = data[f"{c}/{c}_mstar.fits"]["MSTAR_SMOOTHED"].data
            checks["g_bar_stars"] = f * loglog(r, s["RADIUS"], s["MSTAR"])
        for col, expect in checks.items():
            got = float(row[col])
            if abs(got - expect) > INTEGRITY * abs(expect):
                bad.append(f"{row['measurement_id']} {col}: {got} vs {expect}")
    assert not bad, "\n".join(bad[:20])


# Lock (D-019): the flagged rows are exactly every row of the clusters named in known issue #19.
def test_known_mismatch_is_exactly_as_documented(meas, systems):
    issues = json.loads((PKG / "known_issues.json").read_text(encoding="utf-8"))["issues"]
    assert [ki["issue"] for ki in issues] == [19]
    ki = issues[0]
    assert sorted(ki["clusters"]) == sorted({c for _, c, *_ in KNOWN_FAIL})
    sid = {str(r["system_id"]): str(r["name_in_source"]) for r in systems}
    expected = {str(r["measurement_id"]) for r in meas if sid[str(r["system_id"])] in ki["clusters"]}
    flagged = {str(r["measurement_id"]) for r in meas if not np.ma.is_masked(r["flags"]) and "reproduction_mismatch" in str(r["flags"])}
    assert flagged == expected == set(ki["measurements"])
    text = lambda v: "" if np.ma.is_masked(v) else str(v)
    assert all(text(r["known_issues"]) == ("#19" if str(r["measurement_id"]) in expected else "") for r in meas)
