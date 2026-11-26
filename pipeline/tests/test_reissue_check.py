"""The v2 -> v3 re-issue checker (docs/standard-3.0.0-reissue-test.md T1, T2) must catch any change
beyond the version labels. Run on a copy of a real package pair, changed one thing at a time."""

import shutil
from pathlib import Path

import pytest

from aeg.reissue_check import ROOT, t1_tables, t2_code

DS = "aeg-d-kids1000-rar"
SRC = ROOT / "data/packages" / DS


@pytest.fixture
def pair(tmp_path):
    if not (SRC / "v3").is_dir():
        pytest.skip("no v3 package yet")
    base = tmp_path / DS  # named as the dataset, so ruled deviations (keyed by dataset) apply as in the repo
    for v in ("v2", "v3"):
        (base / v / "tables").mkdir(parents=True)
        for f in (SRC / v / "tables").glob("*.ecsv"):
            shutil.copy(f, base / v / "tables" / f.name)
        shutil.copy(SRC / v / "convert.py", base / v / "convert.py")
    return base / "v2", base / "v3"


def test_real_pair_passes(pair):
    assert t1_tables(DS, *pair)[0]
    assert t2_code(*pair)[0]


def test_changed_value_fails(pair):
    f = pair[1] / "tables/measurements.ecsv"
    lines = f.read_text(encoding="utf-8").split("\n")
    i = next(i for i, line in enumerate(lines) if line.startswith(f"{DS}/v3/m000001,"))
    cells = lines[i].split(",")
    j = next(k for k, c in enumerate(cells) if "e-1" in c)
    cells[j] = cells[j].replace("e-1", "1e-1", 1)  # alter one digit string
    lines[i] = ",".join(cells)
    f.write_text("\n".join(lines), encoding="utf-8")
    ok, out = t1_tables(DS, *pair)
    assert not ok and any("measurements.ecsv differs" in o for o in out)


def test_wrong_version_label_fails(pair):
    f = pair[1] / "tables/observables.ecsv"
    f.write_text(f.read_text(encoding="utf-8").replace("{standard_version: 3.0.0}", "{standard_version: 3.0.1}"), encoding="utf-8")
    assert not t1_tables(DS, *pair)[0]


def test_extra_table_fails(pair):
    (pair[1] / "tables/extra.ecsv").write_text("x", encoding="utf-8")
    assert not t1_tables(DS, *pair)[0]


def test_code_change_fails(pair):
    f = pair[1] / "convert.py"
    f.write_text(f.read_text(encoding="utf-8").replace("ISOLATION_LIMIT = 1e-13", "ISOLATION_LIMIT = 2e-13"), encoding="utf-8")
    assert not t2_code(*pair)[0]


def test_header_deviation_only_as_ruled(pair):
    """A ruled T1 header deviation (D-122) is put back exactly; any other header change still fails."""
    f = pair[1] / "tables/measurements.ecsv"
    t = f.read_text(encoding="utf-8")
    assert "assumed hot-gas distribution" in t
    f.write_text(t.replace("assumed hot-gas distribution for the variant", "assumed hot gas for the variant"), encoding="utf-8")
    ok, out = t1_tables(DS, *pair)
    assert not ok
