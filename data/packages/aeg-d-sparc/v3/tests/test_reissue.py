"""aeg-d-sparc/v3: the frozen re-issue test (docs/standard-3.0.0-reissue-test.md, T1 to T6; D-114),
and the standard validator. v2's own frozen reproduction test stays in v2/tests; v3's claim is that its
tables equal v2's (T1), so that result carries over."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[3] / "pipeline"))

from aeg.reissue_check import check  # noqa: E402
from aeg.validate import validate  # noqa: E402


def test_reissue_t1_to_t6():
    ok, lines = check("aeg-d-sparc")
    assert ok, "\n".join(lines)


def test_standard_3_0_0():
    assert validate(HERE) == []
