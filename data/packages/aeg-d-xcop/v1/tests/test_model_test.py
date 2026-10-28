"""D-023: the frozen test of the modelled-star prescription (MODEL_TEST.md), recomputed
independently of convert.py from the package tables and the archive's gas files."""

from __future__ import annotations

import hashlib
import io
import json
import math
import tarfile
from pathlib import Path

import astropy.constants as const
import astropy.units as u
import numpy as np
import pytest
from astropy.io import fits
from astropy.table import Table

PKG = Path(__file__).resolve().parents[1]
MEASURED = ["A85", "A644", "A1795", "A2029", "A2142", "A2319", "ZW1215"]
MODELLED = ["A1644", "A2255", "A3158", "A3266", "RXC1825"]
GCONV = (const.G * u.Msun / u.kpc**2).to(u.m / u.s**2).value


def F(x):
    return math.log(1 + x) - x / (1 + x)


@pytest.fixture(scope="module")
def result():
    meas = Table.read(PKG / "tables/measurements.ecsv", format="ascii.ecsv")
    systems = Table.read(PKG / "tables/systems.ecsv", format="ascii.ecsv")
    props = {str(s["name_in_source"]): (str(s["system_id"]), json.loads(str(s["properties"]))) for s in systems}
    curves = {}
    with tarfile.open(PKG / "source/allfiles.tar.gz") as tar:
        for c in MEASURED:
            sid, p = props[c]
            g = fits.open(io.BytesIO(tar.extractfile(f"{c}/{c}_fgas_profile.fits").read()))[1]
            gr = np.asarray(g.data["RADIUS"], float) * float(g.header["R500"])
            mgas500 = math.exp(np.interp(math.log(p["r500_kpc"]), np.log(gr), np.log(np.asarray(g.data["MGAS"], float))))
            rs = p["r200_kpc"] / 2.9
            scale = 0.39 * p["m500_1e14_solMass"] ** -0.84 * mgas500 / F(p["r500_kpc"] / rs)
            rows = meas[meas["system_id"] == sid]
            r = np.asarray(rows["r_kpc"], float)
            gbar_model = np.asarray(rows["g_bar_gas_hot"], float) + GCONV / r**2 * scale * np.array([F(v / rs) for v in r])
            curves[c] = (r / p["r500_kpc"], gbar_model / np.asarray(rows["g_bar"], float) - 1)
    grid = np.geomspace(0.025, 1.5, 50)
    pts = []
    for x in grid:
        vals = [abs(np.interp(math.log(x), np.log(xs), ds)) for xs, ds in curves.values() if xs.min() <= x <= xs.max()]
        pts.append((x, None if len(vals) < 5 else float(np.median(vals))))
    cov = [(x, D) for x, D in pts if D is not None]
    if cov[-1][1] > 0.10:
        return meas, props, None, None
    x_max = x_min = cov[-1][0]
    for x, D in reversed(cov):
        if D > 0.10:
            break
        x_min = x
    return meas, props, x_min, x_max


def test_model_test_file_is_the_frozen_one():
    spec = json.loads((PKG / "sources.json").read_text(encoding="utf-8"))
    assert hashlib.sha256((PKG / "MODEL_TEST.md").read_bytes()).hexdigest() == spec["model_test_file"]["sha256"]


def test_validated_range_matches_the_package(result):
    _, _, x_min, x_max = result
    dp = json.loads((PKG / "datapackage.json").read_text(encoding="utf-8"))["x_model_test"]
    assert x_min is not None
    assert math.isclose(dp["x_min_r_over_r500"], x_min, rel_tol=1e-9)
    assert math.isclose(dp["x_max_r_over_r500"], x_max, rel_tol=1e-9)


def test_modelled_rows_lie_inside_the_range_and_measured_rows_are_uncut(result):
    meas, props, x_min, x_max = result
    for c in MODELLED:
        sid, p = props[c]
        x = np.asarray(meas[meas["system_id"] == sid]["r_kpc"], float) / p["r500_kpc"]
        assert len(x) > 0 and x.min() >= x_min * (1 - 1e-12) and x.max() <= x_max * (1 + 1e-12), c
    # Every row of the hydrostatic grid inside the source ranges is kept for measured clusters:
    # their radii are contiguous on the source grid (source_ref rows consecutive).
    for c in MEASURED:
        sid, _ = props[c]
        k = [int(str(s).rsplit("row ", 1)[1]) for s in meas[meas["system_id"] == sid]["source_ref"]]
        assert k == list(range(k[0], k[0] + len(k))), c
