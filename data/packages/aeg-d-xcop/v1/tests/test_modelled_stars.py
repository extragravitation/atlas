"""Modelled stellar mass for the 5 clusters without measured stars (D-022 item 3).

Not part of the frozen reproduction test: checks that the converter implements
the ruled prescription. Constants are restated here from D-022, independently
of convert.py.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest
from astropy.table import Table

PKG = Path(__file__).resolve().parents[1]
MODELLED = {"A1644", "A2255", "A3158", "A3266", "RXC1825"}


def F(x):
    return math.log(1 + x) - x / (1 + x)


@pytest.fixture(scope="module")
def tables():
    meas = Table.read(PKG / "tables/measurements.ecsv", format="ascii.ecsv")
    systems = Table.read(PKG / "tables/systems.ecsv", format="ascii.ecsv")
    return meas, systems


def test_modelled_profile_follows_d022(tables):
    meas, systems = tables
    for s in systems:
        name = str(s["name_in_source"])
        rows = meas[meas["system_id"] == s["system_id"]]
        if name not in MODELLED:
            assert set(rows["stars_status"]) == {"measured"}
            continue
        assert set(rows["stars_status"]) == {"modelled"}
        props = json.loads(str(s["properties"]))
        r500, r200, m500 = props["r500_kpc"], props["r200_kpc"], props["m500_1e14_solMass"]
        r = np.asarray(rows["r_kpc"], float)
        mgas = np.asarray(rows["x_xcop_m_gas"], float)
        mstar = np.asarray(rows["x_xcop_m_star"], float)
        rs = r200 / 2.9
        # Shape: M*(<r) proportional to F(r / rs).
        shape = mstar / np.array([F(x) for x in r / rs])
        assert np.allclose(shape, shape[0], rtol=1e-12)
        # Normalisation at R500, using the row grid's gas mass interpolated in log-log.
        mgas500 = float(np.exp(np.interp(math.log(r500), np.log(r), np.log(mgas))))
        mstar500 = shape[0] * F(r500 / rs)
        # Row-grid interpolation of the gas mass differs slightly from the source grid's.
        assert abs(mstar500 / mgas500 / (0.39 * m500 ** -0.84) - 1) < 2e-3, name
        assert all(np.ma.is_masked(v) for v in rows["x_xcop_g_bar_stars_err_lo"])
        assert set(rows["adjustable"]) == {"xray_hse_bias"}
