"""The package follows the Atlas data standard (docs/data-standard.md §7)."""

from pathlib import Path

from aeg.validate import validate

PKG = Path(__file__).resolve().parents[1]


def test_package_follows_the_standard():
    problems = validate(PKG)
    assert problems == [], "\n".join(problems)
