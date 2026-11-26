"""Re-issue test v2 -> v3 under data standard 3.0.0 (docs/standard-3.0.0-reissue-test.md, T1 to T6; D-114).

Usage: python -m aeg.reissue_check <dataset> [<dataset> ...]
       python -m aeg.reissue_check --all      (every dataset that has both v2 and v3)

T7 (addresses reachable) runs separately: python -m aeg.reach.
Exit status 0 only if every test passes for every dataset named.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

from aeg.validate import validate_v30

ROOT = Path(__file__).resolve().parents[2]
PACKAGES = ROOT / "data/packages"
VERSION_LINE = re.compile(r'^DATASET, VERSION, STANDARD = "[^"]+", "v\d+", "[\d.]+"$')
# Ruled deviations from T2: (dataset, the v3 line exactly) -> decision. Each permits one more changed line.
T2_DEVIATIONS = {
    ("aeg-d-dwarfs", '    rel = f"data/packages/{DATASET}/v2/reading/resolved.csv"  # D-115: the v2 freeze record; v3 holds a byte copy'): "D-115",
    ('aeg-d-kids1000-rar', '        col("g_bar", M["g_bar"], acc, "phys.acceleration;meta.modelled", "The source\'s g_bar bin coordinate, as released: the arithmetic midpoint of its §2.1 bin (stars plus cold gas; plus the authors\' assumed hot-gas distribution for the variant)", True),'): "D-122",
    ('aeg-d-kids1000-rar', '        col("gas_hot_status", M["gas_hot_status"], ucd="meta.code", description="Hot gas: absent, or modelled (the authors\' assumed hot-gas distribution, hot-gas variant only; D-034)"),'): "D-122",
    ('aeg-d-xcop', '        "g_obs": (acc, "phys.acceleration", "Observed acceleration, GOBS as released (the source\'s hydrostatic g_obs; the source does not say which of its two methods, nonparametric or Einasto, this column holds; D-119)"),'): "D-122",
}

# Ruled deviations from T1: (dataset, table) -> list of (v3 header text, v2 header text, decision). Only ECSV
# header (#) lines may be listed; N(v3) has each v3 text put back to its v2 text before the hashes are compared.
T1_DEVIATIONS = {
    ("aeg-d-kids1000-rar", "measurements.ecsv"): [
        ("#     \\ the authors' assumed hot-gas distribution for the variant)\"", "#     \\ an assumed hot-gas halo for the variant)\"", "D-122"),
        ("#   description: 'Hot gas: absent, or modelled (the authors'' assumed hot-gas distribution, hot-gas variant only; D-034)'",
         "#   description: 'Hot gas: absent, or modelled (the authors'' assumed halo, hot-gas variant only; D-034)'", "D-122"),
    ],
    ("aeg-d-xcop", "measurements.ecsv"): [
        ("#   description: Observed acceleration, GOBS as released (the source's hydrostatic g_obs; the source does not say which of its two methods,\n#     nonparametric or Einasto, this column holds; D-119)",
         "#   description: Observed acceleration, GOBS as released (the source's non-parametric hydrostatic g_obs)", "D-122"),
    ],
}


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def normalise(text: str, dataset: str, v2_standard: str) -> str:
    """N(file): map the v3 version labels back to v2's (the test's Definitions)."""
    text = text.replace(f"{dataset}/v3/", f"{dataset}/v2/")
    text = text.replace("# - {version: v3}\n", "# - {version: v2}\n")
    return text.replace("# - {standard_version: 3.0.0}\n", f"# - {{standard_version: {v2_standard}}}\n")


def _known_issues_cells(text: str):
    """Rows of an ECSV text as lists of cells, and the index of known_issues (None if absent)."""
    from astropy.io import ascii
    t = ascii.read(text, format="ecsv")
    if "known_issues" not in t.colnames:
        return None, None
    return t, t.colnames.index("known_issues")


def t1_tables(dataset: str, v2: Path, v3: Path) -> tuple[bool, list[str]]:
    out, ok = [], True
    names2 = sorted(p.name for p in (v2 / "tables").glob("*"))
    names3 = sorted(p.name for p in (v3 / "tables").glob("*"))
    if names2 != names3:
        return False, [f"T1 FAIL: table files differ: v2 {names2}, v3 {names3}"]
    for name in names2:
        a = (v2 / "tables" / name).read_text(encoding="utf-8")
        sv2 = re.search(r"^# - \{standard_version: ([\d.]+)\}$", a, flags=re.M)
        n = normalise((v3 / "tables" / name).read_text(encoding="utf-8"), dataset, sv2.group(1) if sv2 else "")
        ruled = []
        for t3, t2_, dec in T1_DEVIATIONS.get((dataset, name), []):
            assert all(x.startswith("#") for x in t3.split("\n") + t2_.split("\n")), "T1 deviations are header lines only"
            if t3 in n:
                n = n.replace(t3, t2_)
                ruled.append(dec)
        if _sha(n.encode()) == _sha(a.encode()):
            if ruled:
                out.append(f"T1 pass with ruled header deviations: {name} identical after N once {len(ruled)} ruled header text(s) "
                           f"are put back ({', '.join(sorted(set(ruled)))}) (sha256 {_sha(a.encode())[:12]}…)")
            else:
                out.append(f"T1 pass: {name} identical after N (sha256 {_sha(a.encode())[:12]}…)")
            continue
        # The one permitted difference: issue numbers added to known_issues cells, none dropped.
        t2, i2 = _known_issues_cells(a)
        t3, _ = _known_issues_cells(n)
        if t2 is not None and t3 is not None and len(t2) == len(t3):
            added, dropped = [], []
            for r2, r3 in zip(t2, t3):
                s2 = {x for x in str(r2["known_issues"] or "").split(";") if x and x != "--"}
                s3 = {x for x in str(r3["known_issues"] or "").split(";") if x and x != "--"}
                dropped += sorted(s2 - s3)
                added += sorted(s3 - s2)
            t3["known_issues"] = t2["known_issues"]
            import io
            buf = io.StringIO()
            t3.write(buf, format="ascii.ecsv", delimiter=",")
            if not dropped and _sha(buf.getvalue().encode()) == _sha(a.encode()):
                out.append(f"T1 pass: {name} identical after N except issue numbers added to known_issues: {sorted(set(added))}")
                continue
            if dropped:
                out.append(f"T1 FAIL: {name}: known_issues drops {sorted(set(dropped))}")
        ok = False
        diff = list(difflib.unified_diff(a.splitlines(), n.splitlines(), "v2", "N(v3)", n=0, lineterm=""))
        out.append(f"T1 FAIL: {name} differs after N; first lines of the diff: " + " | ".join(diff[2:8])[:600])
    return ok, out


def t2_code(v2: Path, v3: Path) -> tuple[bool, list[str]]:
    a = (v2 / "convert.py").read_text(encoding="utf-8").splitlines()
    b = (v3 / "convert.py").read_text(encoding="utf-8").splitlines()
    if len(a) != len(b):
        return False, [f"T2 FAIL: convert.py has {len(a)} lines in v2 and {len(b)} in v3"]
    changed = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    ruled = [(n, y, T2_DEVIATIONS[(v3.parent.name, y)]) for n, x, y in changed if (v3.parent.name, y) in T2_DEVIATIONS]
    changed = [c for c in changed if (v3.parent.name, c[2]) not in T2_DEVIATIONS]
    if ruled and len(changed) == 1 and VERSION_LINE.match(changed[0][2]):
        return True, [f"T2 pass with a ruled deviation: convert.py differs on line {changed[0][0]} (version) and on line "
                      f"{', '.join(str(n) for n, _, _ in ruled)} ({', '.join(d for _, _, d in ruled)}): {ruled[0][1].strip()}"]
    if (len(changed) == 1 and VERSION_LINE.match(changed[0][1]) and VERSION_LINE.match(changed[0][2])
            and '"v3", "3.0.0"' in changed[0][2]):
        return True, [f"T2 pass: convert.py differs only on line {changed[0][0]}: {changed[0][2].strip()}"]
    return False, [f"T2 FAIL: convert.py differs on lines {[c[0] for c in changed]}"]


def t3_t6(v2: Path, v3: Path) -> tuple[bool, list[str]]:
    probs = validate_v30(v3)
    out, ok = [], True
    groups = {"T3": ("sources.json entry", "redistributable", "sha256"), "T4": ("locators.json", "source_ref"),
              "T5": ("archive", "member"), "T6": ("datapackage.json",)}
    for t, keys in groups.items():
        mine = [p for p in probs if any(k in p for k in keys)]
        ok &= not mine
        out += [f"{t} FAIL: {p}" for p in mine] or [f"{t} pass"]
    rest = [p for p in probs if not any(k in p for keys in groups.values() for k in keys)]
    ok &= not rest
    out += [f"T3–T6 FAIL (other): {p}" for p in rest]
    # T3: every v2 entry still present with url, file, bytes and sha256 unchanged.
    e2 = json.loads((v2 / "sources.json").read_text(encoding="utf-8"))["sources"]
    e3 = json.loads((v3 / "sources.json").read_text(encoding="utf-8"))["sources"]
    keyset = {(e.get("url"), e.get("file"), e.get("bytes"), e.get("sha256")) for e in e3}
    lost = [e.get("file") for e in e2 if (e.get("url"), e.get("file"), e.get("bytes"), e.get("sha256")) not in keyset]
    if lost:
        ok = False
        out.append(f"T3 FAIL: v2 entries missing or changed in v3: {lost}")
    nulls = [e["id"] for e in e3 if e.get("sha256") is None]
    out.append(f"T3 count: {len(e3)} entries ({len(e2)} from v2, {len(e3) - len(e2)} new); sha256 null: {nulls or 'none'}")
    loc = json.loads((v3 / "locators.json").read_text(encoding="utf-8"))["rules"]
    out.append(f"T4 count: {len(loc)} rules, {sum('correction' in r for r in loc)} corrections")
    return ok, out


def check(dataset: str) -> tuple[bool, list[str]]:
    v2, v3 = PACKAGES / dataset / "v2", PACKAGES / dataset / "v3"
    if not (v2.is_dir() and v3.is_dir()):
        return False, [f"{dataset}: v2 and v3 are both required"]
    ok, lines = True, []
    for f in (lambda: t1_tables(dataset, v2, v3), lambda: t2_code(v2, v3), lambda: t3_t6(v2, v3)):
        r, out = f()
        ok &= r
        lines += out
    return ok, lines


def main(argv: list[str]) -> int:
    if argv[1:] == ["--all"]:
        names = sorted(p.parent.name for p in PACKAGES.glob("*/v3") if (p.parent / "v2").is_dir())
    else:
        names = argv[1:]
    if not names:
        print(__doc__)
        return 2 if argv[1:] != ["--all"] else 0
    all_ok = True
    for name in names:
        ok, lines = check(name)
        all_ok &= ok
        print(f"== {name}: {'PASS' if ok else 'FAIL'} (T1 to T6)")
        for line in lines:
            print("  " + line)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
