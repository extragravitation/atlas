"""aeg.formula_check withholds row values for unpublished package versions (X-COP v2, D-090 rule 5)."""
import json

from aeg.formula_check import unpublished


def test_published_and_absent(tmp_path):
    assert unpublished(tmp_path) is False
    (tmp_path / "datapackage.json").write_text(json.dumps({"x_publication": "published"}))
    assert unpublished(tmp_path) is False


def test_awaiting_consent(tmp_path):
    (tmp_path / "datapackage.json").write_text(json.dumps({"x_publication": "awaiting_authors_consent"}))
    assert unpublished(tmp_path) is True


def test_descriptor_only(tmp_path):
    (tmp_path / "descriptor.json").write_text(json.dumps({"x_publication": "awaiting_authors_consent"}))
    assert unpublished(tmp_path) is True
