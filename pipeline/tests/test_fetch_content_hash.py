"""aeg.fetch: query-service exports are accepted on their content hash (deviation #19)."""

import hashlib

from aeg import fetch

HEAD1 = b'<VOTABLE>\n Date: 2026-10-30T15:20:37\n<INFO name="request_date" value="2026-10-30T15:20:37"/>\n'
HEAD2 = b'<VOTABLE>\n Date: 2026-10-31T09:00:00\n<INFO name="request_date" value="2026-10-31T09:00:00"/>\n'
BODY = b'<RESOURCE name="x"><TR><TD>1</TD></TR></RESOURCE>\n</VOTABLE>\n'


def entry(raw):
    return {"file": "t.vot", "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "content_from": "<RESOURCE", "content_sha256": hashlib.sha256(BODY).hexdigest()}


def test_new_export_with_same_content_passes(tmp_path):
    p = tmp_path / "t.vot"
    p.write_bytes(HEAD2 + BODY)
    assert fetch.verify(p, entry(HEAD1 + BODY)) == []


def test_changed_content_fails(tmp_path):
    p = tmp_path / "t.vot"
    p.write_bytes(HEAD2 + BODY.replace(b"1", b"2"))
    assert any("content sha256" in x for x in fetch.verify(p, entry(HEAD1 + BODY)))


def test_plain_entries_still_need_exact_bytes(tmp_path):
    p = tmp_path / "f.txt"
    p.write_bytes(b"abc")
    e = {"file": "f.txt", "bytes": 3, "sha256": hashlib.sha256(b"abd").hexdigest()}
    assert fetch.verify(p, e)
