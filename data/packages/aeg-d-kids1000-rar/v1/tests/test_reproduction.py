"""Reproduction test for aeg-d-kids1000-rar/v1, implementing REPRODUCTION.md exactly.

REPRODUCTION.md was frozen (hash in sources.json) before this file or
convert.py existed. Failures are handled under D-019; the test is not
changed to make it pass.
"""

from __future__ import annotations

import hashlib
import json
import math
import tarfile
from pathlib import Path

import astropy.constants as const
import astropy.units as u
import pytest
from astropy.table import Table

PKG = Path(__file__).resolve().parents[1]
TAR = PKG / "source/brouwer2021_rar.tar"
FILES = {
    "kids_bright": ("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt"),
    "kids_bright_hotgas": ("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt", "Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt"),
    "gama": ("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt", "Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt"),
}
README_FACTOR = 4 * 4.52e-30 * 3.086e16          # README: 4 G[pc^3/(Msun s^2)] [pc/m]
PKG_FACTOR = (4 * const.G * (1 * u.Msun / u.pc**2)).to(u.m / u.s**2).value


def rows(name):
    with tarfile.open(TAR) as tar:
        text = tar.extractfile(name).read().decode("ascii")
    return [[float(x) for x in l.split()] for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]


@pytest.fixture(scope="module")
def meas():
    return Table.read(PKG / "tables/measurements.ecsv", format="ascii.ecsv")


@pytest.fixture(scope="module")
def cov():
    return Table.read(PKG / "tables/covariance.ecsv", format="ascii.ecsv")


def test_reproduction_file_is_the_frozen_one():
    spec = json.loads((PKG / "sources.json").read_text(encoding="utf-8"))
    assert hashlib.sha256((PKG / "REPRODUCTION.md").read_bytes()).hexdigest() == spec["reproduction_file"]["sha256"]


def test_1_completeness(meas):
    expected = sum(len(rows(esd)) for esd, _ in FILES.values())
    assert len(meas) == expected
    for key, (esd, _) in FILES.items():
        mine = [r for r in meas if r["x_kids1000_rar_sample"] == key]
        assert len(mine) == len(rows(esd))
        assert sorted(str(r["source_ref"]) for r in mine) == sorted(f"brouwer2021_rar.tar:{esd}:data row {k}" for k in range(1, len(rows(esd)) + 1))


def test_2_g_bar(meas):
    for key, (esd, _) in FILES.items():
        mine = [r for r in meas if r["x_kids1000_rar_sample"] == key]
        for r, src in zip(mine, rows(esd)):
            assert r["g_bar"] == pytest.approx(src[0], rel=1e-12)


def test_3_g_obs_against_readme_recipe(meas):
    for key, (esd, _) in FILES.items():
        mine = [r for r in meas if r["x_kids1000_rar_sample"] == key]
        for r, src in zip(mine, rows(esd)):
            g_readme = README_FACTOR * src[1] / src[4]
            e_readme = README_FACTOR * src[3] / src[4]
            assert abs(math.log10(r["g_obs"]) - math.log10(g_readme)) <= 0.001
            assert abs(math.log10(r["g_obs_err_hi"]) - math.log10(e_readme)) <= 0.001
            assert abs(math.log10(r["g_obs_err_lo"]) - math.log10(e_readme)) <= 0.001


def test_4_covariance(meas, cov):
    ids = {}
    for key, (esd, covfile) in FILES.items():
        mine = [str(r["measurement_id"]) for r in meas if r["x_kids1000_rar_sample"] == key]
        gb = [src[0] for src in rows(esd)]
        for mm, mn, gi, gj, c, corr, b in rows(covfile):
            i = mine[min(range(len(gb)), key=lambda k: abs(gb[k] - gi))]
            j = mine[min(range(len(gb)), key=lambda k: abs(gb[k] - gj))]
            ids[(i, j)] = PKG_FACTOR**2 * c / b
    table = {(str(r["measurement_id_i"]), str(r["measurement_id_j"])): r["covariance"] for r in cov}
    assert set(table) == set(ids)
    for k, v in ids.items():
        assert table[k] == pytest.approx(v, rel=1e-9)
        assert table[(k[1], k[0])] == pytest.approx(table[k], rel=1e-9)
        if k[0] == k[1]:
            assert table[k] > 0


def test_5_constants():
    assert abs(PKG_FACTOR / README_FACTOR - 1) <= 0.0025
