from pathlib import Path

from aeg.check import ROOT, check_no_secrets, check_required_files, run


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
