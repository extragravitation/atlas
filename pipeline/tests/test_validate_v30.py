"""Synthetic tests for the data standard 3.0.0 rules (§10 items 19 to 24; D-114).

Each failing case changes one thing in a package that passes, so a pass cannot come from an
unrelated rule."""

import copy
import json
from pathlib import Path

from astropy.table import Table

from aeg.validate import validate_v30

H = "a" * 64
GOOD_SOURCES = {"sources": [
    {"id": "S1", "kind": "data_file", "role": "mass models", "url": "https://example.org/t.mrt", "file": "t.mrt",
     "bytes": 10, "sha256": H, "retrieved": "2026-11-24", "redistributable": False, "evidence_tier": 1,
     "citation": "Author, A. 2016, AJ 152, 157", "identifier": {"doi": "10.0000/x", "ads_bibcode": "2016AJ....152..157L"},
     "licence": {"status": "none_stated", "checked_where": "landing page and README", "checked_on": "2026-11-24"}},
    {"id": "S2", "kind": "archive", "role": "released accelerations", "url": "https://example.org/a.tar.gz",
     "file": "a.tar.gz", "bytes": 20, "sha256": H, "retrieved": "2026-11-24", "redistributable": True, "evidence_tier": 1,
     "citation": "Author, B. 2022, A&A 662, A123", "identifier": {"arxiv": "2205.01110v2"},
     "licence": {"status": "stated", "spdx": "CC-BY-4.0", "checked_where": "archive README", "checked_on": "2026-11-24"},
     "members_sha256": {"A/x.fits": H, "B/x.fits": H}},
    {"id": "S3", "kind": "document", "role": "paper read for M_V", "url": "https://example.org/p.pdf", "file": "p.pdf",
     "bytes": 30, "sha256": H, "retrieved": "2026-11-24", "redistributable": False, "evidence_tier": 1,
     "citation": "Author, C. 2007, ApJ 1, 1", "identifier": {"landing_url": "https://example.org/p"},
     "licence": {"status": "asked", "asked": "https://github.com/extragravitation/atlas/issues/1",
                 "checked_where": "journal page", "checked_on": "2026-11-24"}},
]}
GOOD_RULES = {"rules": [
    {"table": "observables", "match": r"^t\.mrt:data row (?P<row>\d+), column (?P<column>\w+)",
     "sources": ["S1"], "where": {"row": "{row}", "column": "{column}"}},
    {"table": "observables", "match": r"^a\.tar\.gz:(?P<member>[A-Z]/x\.fits):row (?P<row>\d+)",
     "sources": ["S2"], "where": {"member": "{member}", "row": "{row}"}},
    {"table": "measurements", "match": r"^Paper C Table 1", "sources": ["S3"], "where": {"table": "6"},
     "correction": "Table 1"},
]}
GOOD_ISSUES = {"issues": [{"issue": 1, "title": "Locator names Table 1; the values are in Table 6",
                           "url": "https://github.com/extragravitation/atlas/issues/1", "measurements": [],
                           "locators": [r"^Paper C Table 1"]}]}
OBS_REFS = ["t.mrt:data row 1, column Vobs", "t.mrt:data row 2, column SBdisk", "a.tar.gz:A/x.fits:row 3"]
MEAS_REFS = ["Paper C Table 1, row Leo I"]


def _pkg(tmp: Path, sources=None, rules=None, issues=None, desc=None, obs_refs=None, meas_refs=None) -> Path:
    pkg = tmp / "aeg-d-test" / "v3"
    (pkg / "tables").mkdir(parents=True)
    Table({"observable_id": [f"o{i}" for i in range(len(obs_refs or OBS_REFS))],
           "source_ref": obs_refs or OBS_REFS}).write(pkg / "tables/observables.ecsv", format="ascii.ecsv")
    Table({"measurement_id": [f"m{i}" for i in range(len(meas_refs or MEAS_REFS))],
           "source_ref": meas_refs or MEAS_REFS}).write(pkg / "tables/measurements.ecsv", format="ascii.ecsv")
    for name, obj in (("sources.json", sources or GOOD_SOURCES), ("locators.json", rules or GOOD_RULES),
                      ("known_issues.json", issues or GOOD_ISSUES), ("datapackage.json", desc or {"licenses": []})):
        if obj != "absent":
            (pkg / name).write_text(json.dumps(obj), encoding="utf-8")
    return pkg


DEL = object()  # remove the key (None sets it to null)


def _src(changes: dict):
    s = copy.deepcopy(GOOD_SOURCES)
    for (i, key), value in changes.items():
        if value is DEL:
            s["sources"][i].pop(key, None)
        else:
            s["sources"][i][key] = value
    return s


def _probs(tmp, **kw):
    return validate_v30(_pkg(tmp, **kw))


def test_good_package_passes(tmp_path):
    assert _probs(tmp_path) == []


def test_files_required(tmp_path):
    assert any("locators.json missing" in p for p in _probs(tmp_path / "a", rules="absent"))
    assert any("sources.json missing" in p for p in _probs(tmp_path / "b", sources="absent"))


def test_item19_record_fields(tmp_path):
    cases = {
        "id missing": {(0, "id"): DEL},
        "not unique": {(1, "id"): "S1"},
        "kind": {(0, "kind"): "paper"},
        "citation missing": {(0, "citation"): " "},
        "identifier needs": {(0, "identifier"): {}},
        "unknown keys": {(0, "identifier"): {"doi": "10.0/x", "isbn": "1"}},
        "licence must be an object": {(0, "licence"): "CC0"},
        "licence.status": {(0, "licence"): {"status": "open", "checked_where": "x", "checked_on": "2026-11-24"}},
        "licence.checked_on missing": {(0, "licence"): {"status": "none_stated", "checked_where": "x"}},
        "needs spdx or text": {(1, "licence"): {"status": "stated", "checked_where": "x", "checked_on": "d"}},
        "licence.asked": {(2, "licence"): {"status": "asked", "checked_where": "x", "checked_on": "d"}},
    }
    for i, (expect, change) in enumerate(cases.items()):
        probs = _probs(tmp_path / str(i), sources=_src(change))
        assert any(expect in p for p in probs), (expect, probs)


def test_item20_redistribution_needs_stated_licence(tmp_path):
    probs = _probs(tmp_path, sources=_src({(0, "redistributable"): True}))
    assert any("redistributable is true" in p for p in probs)


def test_item21_hash(tmp_path):
    assert any("hex digest" in p for p in _probs(tmp_path / "a", sources=_src({(0, "sha256"): "ABC"})))
    probs = _probs(tmp_path / "b", sources=_src({(0, "sha256"): None}))
    assert any("without unhashed_reason" in p for p in probs)
    assert any("no known_issues.json entry lists source S1" in p for p in probs)
    issues = copy.deepcopy(GOOD_ISSUES)
    issues["issues"].append({"issue": 2, "title": "Paper not retrievable", "url": "u", "measurements": [], "sources": ["S1"]})
    ok = _probs(tmp_path / "c", sources=_src({(0, "sha256"): None, (0, "unhashed_reason"): "paywalled; no arXiv version"}),
                issues=issues)
    assert ok == []


def test_item22_archive_members(tmp_path):
    assert any("needs members_sha256" in p for p in _probs(tmp_path / "a", sources=_src({(1, "members_sha256"): DEL})))
    probs = _probs(tmp_path / "b", obs_refs=OBS_REFS + ["a.tar.gz:C/x.fits:row 1"])
    assert any("member 'C/x.fits'" in p for p in probs)
    probs = _probs(tmp_path / "c", sources=_src({(1, "kind"): "data_file"}))
    assert any("none of its sources is an archive" in p for p in probs)
    # A rule may cite a document beside the archive; the member is checked against the archive only.
    r = copy.deepcopy(GOOD_RULES)
    r["rules"][1]["sources"] = ["S2", "S3"]
    assert _probs(tmp_path / "d", rules=r) == []


def test_item23_rules(tmp_path):
    def rules(i, **change):
        r = copy.deepcopy(GOOD_RULES)
        r["rules"][i].update(change)
        return r
    cases = {
        "not in ['observables', 'measurements']": rules(0, table="systems"),
        "anchored with ^": rules(0, match=r"t\.mrt:data row (?P<row>\d+), column (?P<column>\w+)"),
        "does not compile": rules(0, match="^t.mrt:(unclosed"),
        "not in sources.json": rules(0, sources=["S9"]),
        "at least one source id": rules(0, sources=[]),
        "where needs": rules(0, where={}),
        "where key 'cell'": rules(0, where={"cell": "B2"}),
        "names group 'col'": rules(0, where={"column": "{col}"}),
    }
    for i, (expect, r) in enumerate(cases.items()):
        probs = _probs(tmp_path / str(i), rules=r)
        assert any(expect in p for p in probs), (expect, probs)


def test_item23_every_source_ref_matches_exactly_one_rule(tmp_path):
    probs = _probs(tmp_path / "a", obs_refs=OBS_REFS + ["unknown.txt line 4"])
    assert any("1 source_ref values match no locator rule" in p for p in probs)
    r = copy.deepcopy(GOOD_RULES)
    r["rules"].append({"table": "observables", "match": r"^t\.mrt", "sources": ["S1"], "where": {"table": "2"}})
    assert any("more than one rule" in p for p in _probs(tmp_path / "b", rules=r))
    # A rule only covers its own table.
    probs = _probs(tmp_path / "c", meas_refs=["t.mrt:data row 1, column Vobs"])
    assert any("measurements: 1 source_ref values match no locator rule" in p for p in probs)


def test_item23_correction_needs_known_issue(tmp_path):
    probs = _probs(tmp_path, issues={"issues": []})
    assert any("has a correction but no known_issues.json entry" in p for p in probs)


def test_item24_descriptor(tmp_path):
    probs = _probs(tmp_path / "a", desc={"licenses": [{"name": "CC0-1.0"}]})
    assert any("names its source id in x_source" in p for p in probs)
    probs = _probs(tmp_path / "b", desc={"licenses": [{"name": "CC0-1.0", "x_source": "S9"}]})
    assert any("source 'S9' not in sources.json" in p for p in probs)
    probs = _probs(tmp_path / "c", desc={"licenses": [{"name": "CC0-1.0", "x_source": "S1"}]})
    assert any("whose licence is none_stated" in p for p in probs)
    assert _probs(tmp_path / "d", desc={"licenses": [{"name": "CC-BY-4.0", "x_source": "S2"}]}) == []
