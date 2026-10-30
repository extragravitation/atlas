"""Fetch a package's source files and verify them against sources.json.

Usage: python -m aeg.fetch data/packages/<dataset>/<version>

Files are written to <package>/source/, which is never committed. A file
already present with the right hash is not downloaded again. A hash or
size mismatch is an error: the build stops rather than use an unverified
file.

A source served by a query service (for example a VizieR VOTable export)
stamps each response with the time of the request, so its raw bytes differ
from one download to the next. Such an entry records, besides the raw
`sha256` of the copy used, `content_from` (a marker such as "<RESOURCE")
and `content_sha256`, the hash of the bytes from the marker's first
occurrence to the end. A fresh download is accepted if either hash matches;
the content hash covers the whole catalogue (field definitions and rows).
"""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

USER_AGENT = "extragravitation-atlas-pipeline (+https://extragravitation.org)"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def content_sha256(data: bytes, marker: str) -> str | None:
    i = data.find(marker.encode())
    return None if i < 0 else hashlib.sha256(data[i:]).hexdigest()


def verify(path: Path, entry: dict) -> list[str]:
    problems = []
    if entry.get("content_from") and sha256_of(path) != entry["sha256"]:
        found = content_sha256(path.read_bytes(), entry["content_from"])
        if found != entry["content_sha256"]:
            problems.append(f"{entry['file']}: content sha256 {found}, expected {entry['content_sha256']}")
        return problems
    size = path.stat().st_size
    if size != entry["bytes"]:
        problems.append(f"{entry['file']}: size {size}, expected {entry['bytes']}")
    digest = sha256_of(path)
    if digest != entry["sha256"]:
        problems.append(f"{entry['file']}: sha256 {digest}, expected {entry['sha256']}")
    return problems


def fetch_package(package_dir: Path) -> list[str]:
    spec = json.loads((package_dir / "sources.json").read_text(encoding="utf-8"))
    out_dir = package_dir / "source"
    out_dir.mkdir(exist_ok=True)
    problems: list[str] = []
    for entry in spec["sources"]:
        target = out_dir / entry["file"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_file() and not verify(target, entry):
            print(f"ok (cached)  {entry['file']}")
            continue
        request = urllib.request.Request(entry["url"], headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=120) as response:
            target.write_bytes(response.read())
        found = verify(target, entry)
        if found:
            target.unlink()
            problems += found
        else:
            print(f"ok (fetched) {entry['file']}")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    problems = fetch_package(Path(argv[1]))
    if problems:
        print("Source verification FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
