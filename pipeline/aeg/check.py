"""Repository-wide checks. Run with: python -m aeg.check

Exits non-zero if any check fails. Every pull request runs this.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from aeg.ids import check_registry

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "LICENSE-CONTENT.md",
    "CITATION.cff",
    "CHANGELOG.md",
    "docs/decisions.md",
    "data/registry/systems.csv",
]

# Patterns that look like credentials. Rule 11: nothing of this kind in the repository.
SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),          # GitHub tokens
    re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),                    # AWS access key IDs
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9_-]{32,}"),               # common API key prefix
]

SKIP_DIRS = {".git", "node_modules", "dist", ".venv", "__pycache__", ".pytest_cache"}
TEXT_SUFFIXES = {".md", ".py", ".toml", ".yml", ".yaml", ".json", ".csv", ".cff", ".txt", ".js", ".ts", ".astro", ".html", ".css", ""}


def check_required_files(root: Path) -> list[str]:
    return [f"missing required file: {name}" for name in REQUIRED_FILES if not (root / name).is_file()]


def check_no_secrets(root: Path) -> list[str]:
    problems = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                problems.append(f"possible credential in {path.relative_to(root)} (pattern {pattern.pattern})")
    return problems


def run(root: Path = ROOT) -> list[str]:
    problems = check_required_files(root)
    registry = root / "data/registry/systems.csv"
    if registry.is_file():
        problems += [f"data/registry/systems.csv {p}" for p in check_registry(registry)]
    problems += check_no_secrets(root)
    return problems


def main() -> int:
    problems = run()
    if problems:
        print("Checks FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
