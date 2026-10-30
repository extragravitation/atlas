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

Resilience: an entry may list `mirrors`, further addresses for the same
file. Every address is tried once, main address first, before any is tried
again; up to ATTEMPTS rounds, with a pause between rounds. A download that
stalls or takes longer than DEADLINE_S is abandoned. A host that failed is
tried last for the rest of the run. A file from any address is used only if
it passes the same hash check, so a mirror can never change what is used.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "extragravitation-atlas-pipeline (+https://extragravitation.org)"
ATTEMPTS = 3
PAUSE_S = 20.0
TIMEOUT_S = 60.0
DEADLINE_S = 240.0

_failed_hosts: set[str] = set()


class Retryable(Exception):
    """A failure that may pass on a later try: network error, stall, or HTTP 5xx."""


def download(url: str) -> bytes:
    """Bytes at url, in one try. Raises Retryable for transient failures; other errors propagate."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    start = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
            chunks = []
            while chunk := response.read(1 << 16):
                chunks.append(chunk)
                if time.monotonic() - start > DEADLINE_S:
                    raise Retryable(f"download took longer than {DEADLINE_S:.0f} s")
            return b"".join(chunks)
    except urllib.error.HTTPError as e:
        if e.code >= 500:
            raise Retryable(f"HTTP {e.code}") from e
        raise
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        raise Retryable(f"{type(e).__name__}: {e}") from e


def _host(url: str) -> str:
    return urllib.parse.urlsplit(url).netloc


def fetch_entry(target: Path, entry: dict) -> str | None:
    """Download a verified copy of entry to target; returns the address used, or None (reasons in entry['_tried'])."""
    addresses = [entry["url"], *entry.get("mirrors", [])]
    addresses.sort(key=lambda u: _host(u) in _failed_hosts)  # stable: order kept within each group
    tried: list[str] = entry.setdefault("_tried", [])
    live = list(addresses)
    for round_ in range(ATTEMPTS):
        if round_:
            time.sleep(PAUSE_S * round_)
        for url in list(live):
            try:
                target.write_bytes(download(url))
            except Retryable as e:
                tried.append(f"{url} (try {round_ + 1}): {e}")
                _failed_hosts.add(_host(url))
                continue
            except Exception as e:  # noqa: BLE001 - permanent for this address; next address
                tried.append(f"{url}: {type(e).__name__}: {e}")
                live.remove(url)
                continue
            found = verify(target, entry)
            if not found:
                return url
            target.unlink()
            tried.append(f"{url}: " + "; ".join(found))
            live.remove(url)  # wrong content does not change on retry
        if not live:
            break
    return None


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
        used = fetch_entry(target, entry)
        if used:
            print(f"ok (fetched) {entry['file']}" + ("" if used == entry["url"] else f" from mirror {used}"))
        else:
            problems.append(f"{entry['file']}: no address gave a verified file: " + " | ".join(entry["_tried"]))
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
