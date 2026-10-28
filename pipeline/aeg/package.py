"""Helpers shared by package converters: descriptor and checksums."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def schema(table) -> dict:
    fields = []
    for name in table.colnames:
        c = table[name]
        f = {"name": name, "type": "number" if c.dtype.kind == "f" else "string",
             "description": c.description, "ucd": (c.meta or {}).get("ucd")}
        if c.unit is not None:
            f["unit"] = str(c.unit)
        fields.append(f)
    return {"fields": fields, "missingValues": [""]}


def write_datapackage(here: Path, descriptor: dict, tables: dict) -> None:
    """tables: resource name -> (relative path, astropy Table)."""
    dialect = {"delimiter": ",", "commentChar": "#", "header": True}
    descriptor = dict(descriptor)
    descriptor["resources"] = [
        {"name": name, "path": path, "format": "ecsv", "mediatype": "text/csv", "encoding": "utf-8",
         "dialect": dialect, "schema": schema(table)}
        for name, (path, table) in tables.items()
    ]
    (here / "datapackage.json").write_text(json.dumps(descriptor, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_checksums(here: Path) -> None:
    files = sorted(p for p in here.rglob("*") if p.is_file() and p.name != "checksums.sha256"
                   and "source" not in p.relative_to(here).parts and "__pycache__" not in p.parts
                   and p.suffix != ".pyc")
    lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(here).as_posix()}" for p in files]
    (here / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    # python -m aeg.package checksums data/packages/<dataset>/<version>
    import sys
    if len(sys.argv) == 3 and sys.argv[1] == "checksums":
        write_checksums(Path(sys.argv[2]).resolve())
        print("checksums written")
    else:
        print("usage: python -m aeg.package checksums <package dir>")
        sys.exit(2)
