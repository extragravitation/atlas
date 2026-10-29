import json
from pathlib import Path

from aeg.check import ROOT, check_assumption_registry, check_no_secrets, check_required_files, run


def test_repository_passes_all_checks():
    assert run(ROOT) == []


def test_missing_files_are_reported(tmp_path: Path):
    problems = check_required_files(tmp_path)
    assert "missing required file: LICENSE" in problems


def test_secret_scan_catches_token(tmp_path: Path):
    fake = "ghp_" + "a" * 36
    (tmp_path / "notes.md").write_text(f"token: {fake}\n", encoding="utf-8")
    assert check_no_secrets(tmp_path)


def test_secret_scan_ignores_clean_text(tmp_path: Path):
    (tmp_path / "notes.md").write_text("no secrets here\n", encoding="utf-8")
    assert check_no_secrets(tmp_path) == []


def test_registry_requires_scope_for_adjustable(tmp_path: Path):
    reg = {"assumptions": [{"id": "x", "name_technical": "x", "name_plain": "x", "adjustable": True, "status": "confirmed",
                            "datasets": {"d/v1": {"default": 1, "min": 0, "max": 2, "default_ref": "r", "range_ref": "r", "effects": []}}}]}
    f = tmp_path / "a.json"
    f.write_text(json.dumps(reg), encoding="utf-8")
    assert any("scope" in p for p in check_assumption_registry(f))
    reg["assumptions"][0]["scope"] = "system"
    f.write_text(json.dumps(reg), encoding="utf-8")
    assert check_assumption_registry(f) == []


def test_registry_default_inside_range(tmp_path: Path):
    reg = {"assumptions": [{"id": "x", "name_technical": "x", "name_plain": "x", "adjustable": True, "status": "confirmed", "scope": "dataset",
                            "datasets": {"d/v1": {"default": 3, "min": 0, "max": 2, "default_ref": "r", "range_ref": "r", "effects": []}}}]}
    f = tmp_path / "a.json"
    f.write_text(json.dumps(reg), encoding="utf-8")
    assert any("outside" in p for p in check_assumption_registry(f))
