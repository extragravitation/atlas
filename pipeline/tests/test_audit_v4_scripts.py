"""Audit plan v4 tools (D-125): frozen hashes, fresh prefix, and the declared input tolerance."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "docs/audit" / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_frozen_hashes_match():
    rec = json.loads((ROOT / "data/frozen/audit-plan-v4.json").read_text())
    for f, h in rec["files"].items():
        assert hashlib.sha256((ROOT / f).read_bytes()).hexdigest() == h, f


def test_sample_is_fresh_and_same_design():
    v3, v4 = load("sample_v3"), load("sample_v4")
    assert v4.PREFIX == "aeg-audit-v4" and v3.PREFIX == "aeg-audit-v3"
    assert (v4.FRACTION, v4.MINIMUM, v4.STRATA) == (v3.FRACTION, v3.MINIMUM, v3.STRATA)
    seed = "00" * 64
    assert v4.key(seed, "x") != v3.key(seed, "x")


def test_input_tolerance_is_relative_1e6_only():
    c = load("compare_v4")
    assert c.same_input("7.93742364e-11", "7.9374236e-11")  # the v3 X-COP artefact
    assert c.same_input("5.50", "5.5")
    assert not c.same_input("5.50", "5.51")
    assert not c.same_input("1.000002", "1.0")
    assert c.same_input("None", "none")
    assert [round(c.clopper_pearson_upper(x, 220) * 100, 2) for x in (0, 1, 2)] == [1.35, 2.14, 2.83]
