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


def test_check_frozen_detects_changes(tmp_path):
    import hashlib
    import json
    from aeg.check import check_frozen
    (tmp_path / "data/frozen").mkdir(parents=True)
    f = tmp_path / "code.py"
    f.write_text("x = 1\n")
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    (tmp_path / "data/frozen/r.json").write_text(json.dumps({"files": {"code.py": h}}))
    assert check_frozen(tmp_path) == []
    f.write_text("x = 2\n")
    assert check_frozen(tmp_path) == ["data/frozen/r.json: frozen file changed: code.py"]
    f.unlink()
    assert check_frozen(tmp_path) == ["data/frozen/r.json: frozen file missing: code.py"]


def _excluded_repo(tmp_path: Path, body: str) -> Path:
    from aeg.check import EXCLUDED_COLUMNS
    (tmp_path / "data/registry").mkdir(parents=True)
    (tmp_path / "data/packages/aeg-d-x/v2").mkdir(parents=True)
    (tmp_path / "data/registry/systems.csv").write_text("system_id,primary_name,first_dataset,assigned_on\naeg-s-000001,A,aeg-d-x/v1,2026-11-04\n", encoding="utf-8")
    (tmp_path / "data/registry/excluded.csv").write_text(",".join(EXCLUDED_COLUMNS) + "\n" + body, encoding="utf-8")
    return tmp_path


def test_excluded_register_accepts_a_valid_row(tmp_path: Path):
    from aeg.check import check_excluded
    root = _excluded_repo(tmp_path, 'aeg-s-000001,aeg-d-x/v2,"D-097 finding: ""could be due to the ongoing tidal disruption""","Paper, l. 1"\n')
    assert check_excluded(root) == []


def test_excluded_register_catches_bad_rows(tmp_path: Path):
    from aeg.check import check_excluded
    root = _excluded_repo(tmp_path, "aeg-s-999999,aeg-d-x/v9,,cite\naeg-s-999999,aeg-d-x/v9,r,c\n")
    problems = " | ".join(check_excluded(root))
    assert "not in data/registry/systems.csv" in problems
    assert "not found under data/packages" in problems
    assert "empty reason" in problems
    assert "duplicate row" in problems
