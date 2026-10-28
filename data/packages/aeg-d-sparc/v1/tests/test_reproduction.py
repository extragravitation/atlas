"""Reproduction test for aeg-d-sparc/v1, implementing REPRODUCTION.md exactly.

REPRODUCTION.md was frozen (and its hash recorded) before this file or
convert.py existed. If this test fails, the package does not ship; the test
is not changed to make it pass.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pytest
from astropy.table import Table

PKG = Path(__file__).resolve().parents[1]
SOURCE = PKG / "source"
TOL_DEX = 0.015


def test_reproduction_file_is_the_frozen_one():
    spec = json.loads((PKG / "sources.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256((PKG / "REPRODUCTION.md").read_bytes()).hexdigest()
    assert digest == spec["reproduction_file"]["sha256"]


@pytest.fixture(scope="module")
def tables():
    return (Table.read(PKG / "tables/measurements.ecsv", format="ascii.ecsv"),
            Table.read(PKG / "tables/systems.ecsv", format="ascii.ecsv"))


def selected(tables):
    meas, systems = tables
    sysinfo = {row["system_id"]: (json.loads(row["properties"])["quality_flag_Q"], float(row["inclination_deg"]))
               for row in systems}
    keep = []
    for row in meas:
        q, inc = sysinfo[row["system_id"]]
        if q == 3 or inc < 30:
            continue
        if not (row["x_sparc_e_v_obs"] / row["x_sparc_v_obs"] < 0.1):
            continue
        keep.append(row)
    return keep


def reference():
    rows = []
    for line in (SOURCE / "RAR.mrt").read_text(encoding="ascii").splitlines():
        try:
            gbar, gobs = float(line[0:6]), float(line[12:18])
            float(line[7:11]); float(line[19:23])
        except (ValueError, IndexError):
            continue
        rows.append((gbar, gobs))
    return rows


def test_1_selection_count(tables):
    assert len(selected(tables)) == 2693


def test_2_point_by_point(tables):
    points = [(math.log10(r["g_bar"]), math.log10(r["g_obs"])) for r in selected(tables)]
    ref = reference()
    assert len(ref) == 2693, f"reference has {len(ref)} data rows"

    # Candidate pairs within tolerance; references sit on a 0.01 dex grid.
    index: dict[tuple[int, int], list[int]] = {}
    for j, (b, o) in enumerate(ref):
        index.setdefault((round(b * 100), round(o * 100)), []).append(j)
    cands = []
    for b, o in points:
        kb, ko = round(b * 100), round(o * 100)
        c = [j for db in (-2, -1, 0, 1, 2) for do in (-2, -1, 0, 1, 2)
             for j in index.get((kb + db, ko + do), [])
             if abs(ref[j][0] - b) <= TOL_DEX and abs(ref[j][1] - o) <= TOL_DEX]
        cands.append(c)
    unmatched_points = [i for i, c in enumerate(cands) if not c]
    assert not unmatched_points, f"{len(unmatched_points)} points have no reference within {TOL_DEX} dex"

    # One-to-one matching (augmenting paths).
    match_ref = [-1] * len(ref)

    def augment(i, seen):
        for j in cands[i]:
            if not seen[j]:
                seen[j] = True
                if match_ref[j] == -1 or augment(match_ref[j], seen):
                    match_ref[j] = i
                    return True
        return False

    import sys
    sys.setrecursionlimit(20000)
    matched = sum(augment(i, [False] * len(ref)) for i in range(len(points)))
    assert matched == len(points) == len(ref)


def test_3_conversion_integrity(tables):
    meas, _ = tables
    assert len(meas) == 3391
    conv = None
    src = []
    for line in (SOURCE / "MassModels_Lelli2016c.mrt").read_text(encoding="ascii").splitlines():
        try:
            float(line[12:18]); R = float(line[19:25])
        except (ValueError, IndexError):
            continue
        src.append((R, float(line[26:32]), float(line[39:45]), float(line[46:52]), float(line[53:59])))
    assert len(src) == 3391
    for row, (R, vobs, vgas, vdisk, vbul) in zip(meas, src):
        assert row["r_kpc"] == pytest.approx(R, abs=1e-9)
        # (km/s)^2/kpc -> m/s^2, derived from this row
        if conv is None:
            conv = row["g_obs"] * R / vobs**2
        v_back = math.sqrt(row["g_obs"] * R / conv)
        assert abs(v_back - vobs) <= 0.01 + 1e-9
        expect = (abs(vgas) * vgas + 0.5 * abs(vdisk) * vdisk + 0.7 * abs(vbul) * vbul) / R * conv
        assert row["g_bar"] == pytest.approx(expect, rel=1e-9, abs=1e-30)
        parts = row["g_bar_stars"] + row["g_bar_gas_cold"]
        assert row["g_bar"] == pytest.approx(parts, rel=1e-9, abs=1e-30)
    # The unit factor itself must be the physical one: (km/s)^2/kpc in m/s^2.
    assert conv == pytest.approx(1e6 / 3.0856775814913673e19, rel=1e-12)
