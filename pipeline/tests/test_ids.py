from pathlib import Path

import pytest

from aeg.ids import (
    check_registry,
    is_dataset_name,
    is_dataset_version,
    is_measurement_id,
    is_system_id,
)

HEADER = "system_id,primary_name,first_dataset,assigned_on\n"


@pytest.mark.parametrize("value,ok", [
    ("aeg-s-000001", True),
    ("aeg-s-123456", True),
    ("aeg-s-000000", False),
    ("aeg-s-1", False),
    ("aeg-s-0000001", False),
    ("aeg-s-ngc3198", False),
    ("AEG-S-000001", False),
])
def test_system_ids(value, ok):
    assert is_system_id(value) is ok


@pytest.mark.parametrize("value,ok", [
    ("aeg-d-sparc", True),
    ("aeg-d-kids1000-rar", True),
    ("aeg-d-clash-lensing", True),
    ("aeg-d-SPARC", False),
    ("aeg-d-sparc-", False),
    ("aeg-d-", False),
])
def test_dataset_names(value, ok):
    assert is_dataset_name(value) is ok


@pytest.mark.parametrize("value,ok", [
    ("aeg-d-sparc/v1", True),
    ("aeg-d-sparc/v12", True),
    ("aeg-d-sparc/v0", False),
    ("aeg-d-sparc/1", False),
])
def test_dataset_versions(value, ok):
    assert is_dataset_version(value) is ok


@pytest.mark.parametrize("value,ok", [
    ("aeg-d-sparc/v1/m000123", True),
    ("aeg-d-xcop/v2/m000001", True),
    ("aeg-d-sparc/v1/m000000", False),
    ("aeg-d-sparc/v1/m123", False),
    ("aeg-d-sparc/m000123", False),
])
def test_measurement_ids(value, ok):
    assert is_measurement_id(value) is ok


def write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "systems.csv"
    p.write_text(body, encoding="utf-8")
    return p


def test_registry_header_only_is_valid(tmp_path):
    assert check_registry(write(tmp_path, HEADER)) == []


def test_registry_valid_rows(tmp_path):
    body = HEADER + "aeg-s-000001,NGC 3198,aeg-d-sparc/v1,2026-11-02\naeg-s-000002,Abell 383,aeg-d-xcop/v1,2026-11-03\n"
    assert check_registry(write(tmp_path, body)) == []


def test_registry_rejects_gap(tmp_path):
    body = HEADER + "aeg-s-000001,A,aeg-d-sparc/v1,2026-11-02\naeg-s-000003,B,aeg-d-sparc/v1,2026-11-02\n"
    problems = check_registry(write(tmp_path, body))
    assert any("expected aeg-s-000002" in str(p) for p in problems)


def test_registry_rejects_duplicate(tmp_path):
    body = HEADER + "aeg-s-000001,A,aeg-d-sparc/v1,2026-11-02\naeg-s-000001,B,aeg-d-sparc/v1,2026-11-02\n"
    problems = check_registry(write(tmp_path, body))
    assert any("duplicate" in str(p) for p in problems)


def test_registry_rejects_bad_header(tmp_path):
    problems = check_registry(write(tmp_path, "id,name\n"))
    assert problems and "header" in str(problems[0])


def test_registry_rejects_bad_fields(tmp_path):
    body = HEADER + "aeg-s-000001,,sparc,2 Nov 2026\n"
    messages = " ".join(str(p) for p in check_registry(write(tmp_path, body)))
    assert "primary_name is empty" in messages
    assert "not a dataset version" in messages
    assert "not an ISO date" in messages
