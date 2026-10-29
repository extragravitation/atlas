"""Checks on the built site (site/dist), independent of the site's own code.

1. Data: every value the browser receives (dist/data/*.json) equals the package table exactly,
   read here with astropy rather than the site's JavaScript parser.
2. Downloads: every ECSV download is byte-identical to the package file; every CSV download holds
   the same values; checksums, datapackage and sources files are byte-identical.
3. Pages: one page per system and per dataset version.
4. Links: every internal link and asset reference in every HTML page resolves to a built file.
5. Reading layers: every technical-layer element has its plain-language twin (D-008).

Usage: python -m aeg.site_check [path/to/dist]
"""

from __future__ import annotations

import csv
import io
import json
import math
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from aeg.formula_check import _clean

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "data/packages"


def same(a, b) -> bool:
    if a is None or b is None:  # an empty ECSV cell: masked in astropy, '' or null in the payload
        return (a is None or a == "") and (b is None or b == "")
    if isinstance(a, float) or isinstance(b, float):
        if isinstance(a, float) and math.isnan(a):
            return False
        return float(a) == float(b)
    return a == b


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs: list[str] = []
        self.ids: set[str] = set()
        self.layers = {"t": 0, "p": 0}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for k in ("href", "src"):
            if a.get(k):
                self.refs.append(a[k])
        if a.get("id"):
            self.ids.add(a["id"])
        if a.get("data-l") in ("t", "p"):
            self.layers[a["data-l"]] += 1


def check_data(dist: Path, errors: list[str]) -> int:
    from astropy.table import Table

    index = json.loads((dist / "data/index.json").read_text())
    n = 0
    for entry in index["datasets"]:
        payload = json.loads((dist / "data" / entry["file"]).read_text())
        name, version = payload["name"], payload["version"]
        pkg = PKG / name / version
        meas = Table.read(pkg / "tables/measurements.ecsv", format="ascii.ecsv")
        if payload["n"] != len(meas):
            errors.append(f"{name}/{version}: payload has {payload['n']} rows, table {len(meas)}")
            continue
        for col, values in payload["columns"].items():
            if col not in meas.colnames:
                errors.append(f"{name}/{version}: payload column {col} not in the table")
                continue
            for i, v in enumerate(values):
                t = _clean(meas[col][i])
                if not same(v, t):
                    errors.append(f"{name}/{version} row {i} {col}: site {v!r} != table {t!r}")
                    break
                n += 1
        sys_path = pkg / "tables/systems.ecsv"
        if payload.get("systems") is not None:
            systems = Table.read(sys_path, format="ascii.ecsv")
            if len(systems) != len(payload["systems"]):
                errors.append(f"{name}/{version}: {len(payload['systems'])} systems in payload, {len(systems)} in table")
            for i, s in enumerate(payload["systems"]):
                for k, v in s.items():
                    if k == "properties":
                        t = json.loads(systems["properties"][i]) if systems["properties"][i] else {}
                        if v != t:
                            errors.append(f"{name}/{version} system {i}: properties differ")
                        continue
                    t = _clean(systems[k][i])
                    if not same(v, t):
                        errors.append(f"{name}/{version} system {i} {k}: site {v!r} != table {t!r}")
                    n += 1
            for s in payload["systems"]:
                if not (dist / "systems" / s["system_id"] / "index.html").is_file():
                    errors.append(f"missing system page for {s['system_id']}")
        if not (dist / "datasets" / name / version / "index.html").is_file():
            errors.append(f"missing dataset page for {name}/{version}")
    return n


def check_downloads(dist: Path, errors: list[str]) -> int:
    from astropy.table import Table

    n = 0
    for pkg in sorted(PKG.glob("*/*/")):
        if not (pkg / "tables/measurements.ecsv").is_file():
            continue
        out = dist / "downloads" / pkg.parent.name / pkg.name
        for f in ("datapackage.json", "checksums.sha256", "sources.json"):
            if (out / f).read_bytes() != (pkg / f).read_bytes():
                errors.append(f"download {out / f} differs from the package file")
            n += 1
        for src in sorted((pkg / "tables").glob("*.ecsv")):
            if (out / src.name).read_bytes() != src.read_bytes():
                errors.append(f"download {out / src.name} differs from {src}")
            t = Table.read(src, format="ascii.ecsv")
            rows = list(csv.reader(io.StringIO((out / (src.stem + ".csv")).read_text())))
            if rows[0] != t.colnames or len(rows) - 1 != len(t):
                errors.append(f"CSV {src.stem}.csv: header or row count differs")
                continue
            for i, r in enumerate(rows[1:]):
                for j, c in enumerate(t.colnames):
                    v = _clean(t[c][i])
                    cell = r[j]
                    if v is None:
                        ok = cell == ""
                    elif isinstance(v, (int, float)) and not isinstance(v, bool):
                        ok = cell != "" and float(cell) == float(v)
                    else:
                        ok = cell == str(v)
                    if not ok:
                        errors.append(f"CSV {pkg.parent.name}/{src.stem} row {i} {c}: {cell!r} != {v!r}")
                        break
            n += 1
    return n


def check_pages(dist: Path, errors: list[str]) -> int:
    pages = sorted(dist.rglob("*.html"))
    parsed = {}
    for p in pages:
        h = Links()
        h.feed(p.read_text())
        parsed[p] = h
        if h.layers["t"] != h.layers["p"]:
            errors.append(f"{p.relative_to(dist)}: {h.layers['t']} technical elements, {h.layers['p']} plain")
    n = 0
    for p, h in parsed.items():
        for ref in h.refs:
            u = urlparse(ref)
            if u.scheme or u.netloc or ref.startswith(("mailto:", "data:", "javascript:")):
                continue
            path, frag = unquote(u.path), u.fragment
            if not path:
                target = p
            else:
                target = (dist / path.lstrip("/")) if path.startswith("/") else (p.parent / path)
                if target.is_dir() or path.endswith("/"):
                    target = target / "index.html"
            if not target.exists():
                errors.append(f"{p.relative_to(dist)}: broken link {ref}")
                continue
            if frag and target.suffix == ".html":
                ids = parsed[target].ids if target in parsed else set()
                if frag not in ids:
                    errors.append(f"{p.relative_to(dist)}: missing anchor {ref}")
            n += 1
    return n


def main(argv: list[str]) -> int:
    dist = Path(argv[0]) if argv else ROOT / "site/dist"
    if not (dist / "index.html").is_file():
        print(f"no built site at {dist}; run the site build first", file=sys.stderr)
        return 2
    errors: list[str] = []
    a = check_data(dist, errors)
    b = check_downloads(dist, errors)
    c = check_pages(dist, errors)
    for e in errors[:200]:
        print("ERROR", e)
    print(f"site check: {a} values compared, {b} download files, {c} internal links; {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
