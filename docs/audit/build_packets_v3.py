"""Build reader packets for audit plan v3 §2.5 (and the pilot of D-118).

Usage:
  python docs/audit/build_packets_v3.py OUT_DIR MEASUREMENT_ID... [--files DIR] [--brief FILE]

For each measurement row, writes OUT_DIR/<dataset>/ containing, for every row of that dataset given:
  - BRIEF.md: the fixed reader brief (plan §2.6), or the text of --brief;
  - METHOD.md: the dataset's methods page text (docs/methods/datasets/<dataset>.md) as of this commit;
  - rows.json: per row, the measurement identifier, the system's name as the source gives it, and
    every source_ref the row's inputs carry (the row's own and those of the observables it is built
    from), each with the locator rule it matches (where, sources, correction, note; the regular
    expression itself is left out, as it can carry printed values). Printed values are removed from
    all of this text;
  - sources.json: the entries of the package's sources.json those rules name;
  - files/: every file those entries name, checked against its recorded SHA-256. A file is taken
    from --files DIR (by its recorded file name) if present there, otherwise downloaded from its url.
    A file that cannot be got, or whose hash does not match, is listed in MISSING.txt and never
    replaced by another version.

Values of individual rows are never written: no table of the package is copied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

from astropy.table import Table

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "docs/methods/datasets"))
sys.path.insert(0, str(ROOT / "pipeline"))
from make_input_tables import redact  # noqa: E402

VIZIER_MIRRORS = ["vizier.cfa.harvard.edu", "vizier.cds.unistra.fr", "vizier.u-strasbg.fr"]

BRIEF = """You are auditing measurements of a public dataset. From the source files given, read the inputs that the written method needs, exactly as printed, with their units and where you found them (file, and page, table, row, column or line). Then compute the observed acceleration g_obs and the baryonic acceleration g_bar, both in m s⁻², with your own code, following only the written method. Use only the constants stated in the method. If the method does not say how to do a step, do not guess: record "method incomplete" and what was missing. If you cannot read a value, record "unreadable" and why. For every input, also say whether you found it at the place the locator gives; if not, say where you found it. Return values.csv (measurement_id, g_obs, g_bar, notes) and inputs.csv (measurement_id, input, value, unit, file, place, at_locator yes/no). Do not look for or use any other copy of this dataset.
"""


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rule_for(rules, table, ref):
    hit = [r for r in rules if r["table"] == table and re.match(r["match"], ref)]
    if len(hit) != 1:
        raise SystemExit(f"{len(hit)} locator rules match {table} source_ref {ref!r}")
    r = hit[0]
    g = re.match(r["match"], ref).groupdict()
    fill = lambda v: re.sub(r"\{(\w+)\}", lambda x: str(g.get(x.group(1), x.group(0))), str(v))  # the rule's {group} templates
    out = {"sources": r["sources"], "where": {k: redact(fill(v)) for k, v in r.get("where", {}).items()}}
    for k in ("correction", "note"):
        if k in r:
            out[k] = redact(fill(r[k]))
    return out


def get_file(entry: dict, files_dir: Path | None, dest: Path) -> str | None:
    """A copy verified exactly as the pipeline verifies it (aeg.fetch.verify: size and SHA-256, or, for a
    query-service export stamped with its request time, the recorded content hash). Tried in order: the
    --files folder, the entry's local_copies, then its url and mirrors."""
    from aeg import fetch
    if not entry.get("sha256"):
        return f"{entry['id']}: no recorded hash"
    name = Path(entry.get("file") or entry["id"]).name
    target = dest / name
    for c in ([files_dir / name, files_dir / entry.get("file", name)] if files_dir else []) + [ROOT / r for r in entry.get("local_copies", [])]:
        if c.is_file():
            shutil.copyfile(c, target)
            if not fetch.verify(target, entry):
                return None
            target.unlink()
    e = dict(entry)
    if e.get("content_from") and "/viz-bin/" in e.get("url", ""):
        # A VizieR export: the same query at the other VizieR mirrors, accepted only on the recorded content hash.
        q = e["url"].split("/viz-bin/", 1)[1]
        e["mirrors"] = list(e.get("mirrors", [])) + [f"https://{h}/viz-bin/{q}" for h in VIZIER_MIRRORS if h not in e["url"]]
    if fetch.fetch_entry(target, e):
        return None
    target.unlink(missing_ok=True)
    return f"{entry['id']}: no verified copy from the supplied folder, local copies or {entry.get('url', 'its url')}; supply it with --files"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--files")
    ap.add_argument("--brief")
    a = ap.parse_args()
    out = Path(a.out)
    files_dir = Path(a.files) if a.files else None
    brief = Path(a.brief).read_text(encoding="utf-8") if a.brief else BRIEF
    by_pkg: dict[tuple[str, str], list[str]] = {}
    for mid in a.ids:
        ds, ver, _ = mid.split("/")
        by_pkg.setdefault((ds, ver), []).append(mid)
    status = 0
    for (ds, ver), mids in by_pkg.items():
        pkg = ROOT / "data/packages" / ds / ver
        d = out / ds
        (d / "files").mkdir(parents=True, exist_ok=True)
        m = {r["measurement_id"]: r for r in Table.read(pkg / "tables/measurements.ecsv", format="ascii.ecsv")}
        o = {r["observable_id"]: r for r in Table.read(pkg / "tables/observables.ecsv", format="ascii.ecsv")}
        sp = pkg / "tables/systems.ecsv"
        s = {str(r["system_id"]): r for r in Table.read(sp, format="ascii.ecsv")} if sp.exists() else {}
        rules = json.loads((pkg / "locators.json").read_text(encoding="utf-8"))["rules"]
        src = {e["id"]: e for e in json.loads((pkg / "sources.json").read_text(encoding="utf-8"))["sources"]}
        rows, used = [], set()
        for mid in mids:
            r = m[mid]
            refs = [("measurements", str(r["source_ref"]))]
            labels = {}
            for i in (str(r["observed_from"]) + ";" + str(r["baryonic_from"])).split(";"):
                if i in o:
                    ref = str(o[i]["source_ref"])
                    refs.append(("observables", ref))
                    labels.setdefault(ref, set()).add(str(o[i]["quantity"]))
            seen, items = set(), []
            for t, ref in refs:
                if (t, ref) in seen:
                    continue
                seen.add((t, ref))
                lr = rule_for(rules, t, ref)
                used.update(lr["sources"])
                item = {"source_ref": redact(ref), "locator": lr}
                if t == "observables":
                    item["quantity"] = "; ".join(sorted(labels.get(ref, ())))  # what the input is, never its value
                items.append(item)
            rows.append({"measurement_id": mid, "system": str(s[str(r["system_id"])]["name_in_source"]) if str(r["system_id"]) in s else "(population average: no single system)", "inputs": items})
        (d / "BRIEF.md").write_text(brief, encoding="utf-8")
        method = (ROOT / "docs/methods/datasets" / f"{ds}.md").read_text(encoding="utf-8")
        (d / "METHOD.md").write_text(method, encoding="utf-8")
        (d / "rows.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        # Every source of the same reading record as a source used (e.g. the paper that states a record's
        # cosmology next to its data tables), so that what the methods page says to read is in the packet.
        recs = {src[i].get("record") for i in used} - {None, ""}
        used |= {i for i, e in src.items() if e.get("record") in recs}
        ents = [src[i] for i in sorted(used, key=lambda x: int(re.sub(r"\D", "", x) or 0))]
        (d / "sources.json").write_text(json.dumps(ents, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        missing = [x for x in (get_file(e, files_dir, d / "files") for e in ents) if x]
        if missing:
            (d / "MISSING.txt").write_text("\n".join(missing) + "\n", encoding="utf-8")
            status = 1
        print(f"{ds}: {len(mids)} rows, {len(ents)} sources, {len(ents) - len(missing)} files ready, {len(missing)} missing")
        for x in missing:
            print("   ", x)
    return status


if __name__ == "__main__":
    sys.exit(main())
