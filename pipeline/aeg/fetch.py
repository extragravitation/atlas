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

Resilience: each address is tried up to ATTEMPTS times with a pause after a
network error or a 5xx response. An entry may list `mirrors`: further
addresses for the same file. They are tried in order only if the main
address fails, and a mirror's file is accepted only if it passes the same
hash check, so a mirror can never change what is used.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

USER_AGENT = "extragravitation-atlas-pipeline (+https://extragravitation.org)"
ATTEMPTS = 3
PAUSE_S = 20.0


def download(url: str, attempts: int | None = None, pause: float | None = None) -> bytes:
    """Bytes at url; retries on network errors and server errors (5xx); other HTTP errors are raised at once."""
    attempts = ATTEMPTS if attempts is None else attempts
    pause = PAUSE_S if pause is None else pause
    last: Exception | None = None
    for i in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=120) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            if e.code < 500:
                raise
            last = e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e
        if i + 1 < attempts:
            time.sleep(pause * (i + 1))
    raise last if last else RuntimeError(f"no response from {url}")


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
        tried: list[str] = []
        for url in [entry["url"], *entry.get("mirrors", [])]:
            try:
                target.write_bytes(download(url))
            except Exception as e:  # noqa: BLE001 - recorded and the next address is tried
                tried.append(f"{url}: {type(e).__name__}: {e}")
                continue
            found = verify(target, entry)
            if not found:
                print(f"ok (fetched) {entry['file']}" + ("" if url == entry["url"] else f" from mirror {url}"))
                break
            target.unlink()
            tried.append(f"{url}: " + "; ".join(found))
        else:
            problems.append(f"{entry['file']}: no address gave a verified file: " + " | ".join(tried))
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
