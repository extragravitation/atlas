"""D-051 coverage geometry."""

import math

from aeg.coverage import Structure, r_over_ah, summarise

S = Structure(ra0_deg=150.0, dec0_deg=-30.0, ellipticity=0.5, pa_deg=0.0, a_h_arcmin=10.0)


def offset(dra_arcmin_east: float, ddec_arcmin: float):
    # small offsets: east offset scaled by cos(dec)
    return 150.0 + dra_arcmin_east / 60.0 / math.cos(math.radians(-30.0)), -30.0 + ddec_arcmin / 60.0


def test_centre_is_zero():
    assert r_over_ah(150.0, -30.0, S) == 0.0


def test_major_axis_north_for_pa_zero():
    ra, dec = offset(0.0, 10.0)  # 10' north, on the major axis
    assert abs(r_over_ah(ra, dec, S) - 1.0) < 1e-3


def test_minor_axis_east_for_pa_zero():
    ra, dec = offset(5.0, 0.0)  # 5' east = b_h for e = 0.5, on the half-light ellipse
    assert abs(r_over_ah(ra, dec, S) - 1.0) < 1e-3


def test_pa_rotates_axes():
    s90 = Structure(150.0, -30.0, 0.5, 90.0, 10.0)
    ra, dec = offset(10.0, 0.0)  # major axis now east
    assert abs(r_over_ah(ra, dec, s90) - 1.0) < 1e-3


def test_summary_literal_threshold():
    out = summarise([0.2, 0.9, 1.0, 1.01])
    assert out["n_beyond"] == 1 and out["passes"] and out["n_members"] == 4
    assert not summarise([0.5, 1.0])["passes"]
