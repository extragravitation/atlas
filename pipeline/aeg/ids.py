"""Permanent identifiers (decision D-006).

- Systems:      aeg-s-000001   (six digits, sequential, assigned once, never reused)
- Datasets:     aeg-d-<short-name>, versioned /v1, /v2, ...
- Measurements: aeg-d-<short-name>/v<N>/m000001

These formats must never change once anything is published.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

SYSTEM_ID = re.compile(r"^aeg-s-(\d{6})$")
DATASET_NAME = re.compile(r"^aeg-d-[a-z0-9]+(?:-[a-z0-9]+)*$")
DATASET_VERSION = re.compile(r"^(aeg-d-[a-z0-9]+(?:-[a-z0-9]+)*)/v([1-9]\d*)$")
MEASUREMENT_ID = re.compile(r"^(aeg-d-[a-z0-9]+(?:-[a-z0-9]+)*)/v([1-9]\d*)/m(\d{6})$")

REGISTRY_COLUMNS = ["system_id", "primary_name", "first_dataset", "assigned_on"]


def is_system_id(value: str) -> bool:
    return SYSTEM_ID.fullmatch(value) is not None and value != "aeg-s-000000"


def is_dataset_name(value: str) -> bool:
    return DATASET_NAME.fullmatch(value) is not None


def is_dataset_version(value: str) -> bool:
    return DATASET_VERSION.fullmatch(value) is not None


def is_measurement_id(value: str) -> bool:
    m = MEASUREMENT_ID.fullmatch(value)
    return m is not None and m.group(3) != "000000"


@dataclass
class RegistryProblem:
    line: int
    message: str

    def __str__(self) -> str:
        return f"line {self.line}: {self.message}"


def check_registry(path: Path) -> list[RegistryProblem]:
    """Check the system-ID registry.

    Rules: exact header; every ID well formed; IDs unique and strictly
    increasing in file order with no gaps (assigned once, in sequence, never
    reused or removed); primary names present; first_dataset is a dataset
    version; assigned_on is an ISO date.
    """
    problems: list[RegistryProblem] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return [RegistryProblem(1, "registry is empty; it must at least have the header row")]
        if header != REGISTRY_COLUMNS:
            problems.append(RegistryProblem(1, f"header must be {','.join(REGISTRY_COLUMNS)}"))
            return problems

        expected = 1
        seen: set[str] = set()
        for line_no, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                problems.append(RegistryProblem(line_no, "blank row"))
                continue
            if len(row) != len(REGISTRY_COLUMNS):
                problems.append(RegistryProblem(line_no, f"expected {len(REGISTRY_COLUMNS)} columns, found {len(row)}"))
                continue
            system_id, primary_name, first_dataset, assigned_on = row
            m = SYSTEM_ID.fullmatch(system_id)
            if m is None:
                problems.append(RegistryProblem(line_no, f"malformed system ID {system_id!r}"))
                continue
            if system_id in seen:
                problems.append(RegistryProblem(line_no, f"duplicate system ID {system_id}"))
            seen.add(system_id)
            number = int(m.group(1))
            if number != expected:
                problems.append(RegistryProblem(line_no, f"expected aeg-s-{expected:06d}, found {system_id} (IDs are sequential and never removed)"))
            expected = number + 1
            if not primary_name.strip():
                problems.append(RegistryProblem(line_no, "primary_name is empty"))
            if not is_dataset_version(first_dataset):
                problems.append(RegistryProblem(line_no, f"first_dataset {first_dataset!r} is not a dataset version like aeg-d-sparc/v1"))
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", assigned_on) is None:
                problems.append(RegistryProblem(line_no, f"assigned_on {assigned_on!r} is not an ISO date"))
    return problems
