"""Repository-wide checks. Run with: python -m aeg.check

Exits non-zero if any check fails. Every pull request runs this.
"""

from __future__ import annotations

import hashlib
import json
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

SKIP_DIRS = {".git", "node_modules", "dist", ".astro", ".venv", "__pycache__", ".pytest_cache"}
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


def check_assumption_registry(path: Path) -> list[str]:
    """data/assumptions.json follows data standard §6 (1.3.0)."""
    import json
    problems = []
    data = json.loads(path.read_text(encoding="utf-8"))
    seen = set()
    for a in data.get("assumptions", []):
        aid = a.get("id", "?")
        if aid in seen:
            problems.append(f"{aid}: duplicate id")
        seen.add(aid)
        for key in ("name_technical", "name_plain", "adjustable", "status", "datasets"):
            if key not in a:
                problems.append(f"{aid}: missing {key}")
        if a.get("status") not in ("draft", "confirmed"):
            problems.append(f"{aid}: status must be draft or confirmed")
        if a.get("adjustable") and a.get("status") == "confirmed":
            if a.get("scope") not in ("dataset", "system"):
                problems.append(f"{aid}: an adjustable assumption needs scope 'dataset' or 'system' (D-014 clarification)")
            for ds, e in a.get("datasets", {}).items():
                for key in ("default", "min", "max", "default_ref", "range_ref", "effects"):
                    if key not in e:
                        problems.append(f"{aid} {ds}: missing {key}")
                if all(k in e for k in ("default", "min", "max")) and not (e["min"] <= e["default"] <= e["max"]):
                    problems.append(f"{aid} {ds}: default outside its range")
                for eff in e.get("effects", []):
                    if not {"column", "formula"} <= set(eff):
                        problems.append(f"{aid} {ds}: an effect needs column and formula")
        elif "scope" in a and a["scope"] not in ("dataset", "system"):
            problems.append(f"{aid}: scope must be 'dataset' or 'system'")
    return problems


def check_frozen(root: Path) -> list[str]:
    """Frozen files must keep the hash recorded when they were frozen.

    Freeze records: data/frozen/*.json ({"files": {path: sha256}}) and the
    protocol documents in data/taxonomy.json. A change to a frozen file needs
    a new version (a new file and a new freeze record), never an edit.
    """
    problems = []
    records = []
    for rec in sorted((root / "data/frozen").glob("*.json")):
        records.append((rec.relative_to(root).as_posix(), json.loads(rec.read_text())["files"]))
    tax = root / "data/taxonomy.json"
    if tax.is_file():
        records.append(("data/taxonomy.json", json.loads(tax.read_text()).get("documents", {})))
    for rec_name, files in records:
        for rel, expected in files.items():
            f = root / rel
            if not f.is_file():
                problems.append(f"{rec_name}: frozen file missing: {rel}")
                continue
            got = hashlib.sha256(f.read_bytes()).hexdigest()
            if got != expected:
                problems.append(f"{rec_name}: frozen file changed: {rel}")
    return problems


def run(root: Path = ROOT) -> list[str]:
    problems = check_required_files(root)
    if (root / "data/assumptions.json").is_file():
        problems += [f"data/assumptions.json {p}" for p in check_assumption_registry(root / "data/assumptions.json")]
    registry = root / "data/registry/systems.csv"
    if registry.is_file():
        problems += [f"data/registry/systems.csv {p}" for p in check_registry(registry)]
    problems += check_no_secrets(root)
    problems += check_frozen(root)
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
