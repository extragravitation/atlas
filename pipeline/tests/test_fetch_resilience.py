"""aeg.fetch: mirrors are tried in order and accepted only by hash; failures are reported, not raised."""

import hashlib
import json

from aeg import fetch


def write_pkg(tmp_path, data: bytes, urls):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    entry = {"file": "f.txt", "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "url": urls[0], "mirrors": urls[1:]}
    (pkg / "sources.json").write_text(json.dumps({"sources": [entry]}))
    return pkg


def test_falls_back_to_a_mirror(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "PAUSE_S", 0.0)
    good = tmp_path / "good.txt"
    good.write_bytes(b"catalogue")
    pkg = write_pkg(tmp_path, b"catalogue", [(tmp_path / "missing.txt").as_uri(), good.as_uri()])
    assert fetch.fetch_package(pkg) == []
    assert (pkg / "source/f.txt").read_bytes() == b"catalogue"


def test_a_mirror_with_other_content_is_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "PAUSE_S", 0.0)
    bad = tmp_path / "bad.txt"
    bad.write_bytes(b"something else")
    pkg = write_pkg(tmp_path, b"catalogue", [(tmp_path / "missing.txt").as_uri(), bad.as_uri()])
    problems = fetch.fetch_package(pkg)
    assert problems and "no address gave a verified file" in problems[0]
    assert not (pkg / "source/f.txt").exists()
