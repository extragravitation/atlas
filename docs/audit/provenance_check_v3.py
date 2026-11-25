"""Audit v3 provenance check (plan v3 §2.9, D-116).

Written and committed before the audit seed exists and before any audit reading is opened.

Usage:
    python docs/audit/provenance_check_v3.py PACKETS_DIR READINGS_DIR SAMPLE_CSV OUT_CSV [REPO_ROOT]

PACKETS_DIR is the output of build_packets_v3.py (one folder per package, with rows.json,
sources.json and files/). READINGS_DIR holds the readers' folders a/ and b/ as for
compare_v3.py. Writes one row per sampled measurement with the result of each check.

Mechanical part, per row (fixed here, before any reading):
 1 locator    the row's source_ref and the source_ref of every observable it is built from each
              match exactly one rule of the package's locators.json
 2 record     every source those rules name has id, kind, citation, a non-empty identifier, and
              a licence with status, checked_where and checked_on
 3 hash       every such source has a recorded sha256, and its file in the packet verifies as
              aeg.fetch verifies it (size and SHA-256, or the recorded content hash for a
              time-stamped export). A source whose file is not in the packet: "not verified".
 4 place      every place a rule gives that can be checked mechanically exists in the file:
              an HDU number (FITS), an archive member, a PDF page number, a line number of a
              text file or archive member, a numbered row of a FITS or VOTable table. Places
              given in words ("the galaxy's row", "§3.5", "Table 4") are "n/a" here and are
              covered by check 6.
 5 units      every observable the row is built from has a unit that astropy can read (or is
              dimensionless), of the physical type its quantity requires (the map QTYPE below);
              quantities not in the map are "n/a"; and the row's g_obs and g_bar are in m s-2
 Human part:
 6 found      at_locator is read by its first word (yes / no). Readers name inputs freely, so
              inputs are not matched across readers by name. If both readers mark at least one
              input "no", the row is "review" and is adjudicated at source by Claude, quoting the
              source, with this rule fixed now: "provenance failure" if an input the value depends
              on is found by both readers somewhere other than the place the package's record
              gives (its locator, or for an input with no locator, the dataset's methods page),
              unless the rule's correction gives that place; otherwise "provenance confirmed".
              If only one reader marks an input "no", it is listed, not counted. (The dry run on
              the pilot showed why inputs with no locator are not skipped: the X-COP citation
              errors of D-119 were found through such inputs.)
 Late hash (§2.9): for a source in LATE_HASH, checks 3 and 6 pass only if both readers give at
 least one input read from that file (file field contains the file name) with at_locator "yes".

Result per row: "fail" if any check fails; otherwise "review" if check 6 needs adjudication;
otherwise "not verified" if check 3 found a file missing from the packet; otherwise "pass". "n/a" components never count as passes for a
check: a check with only n/a components is reported as n/a.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import re
import sys
import tarfile
from pathlib import Path

ROOT_DEFAULT = Path(__file__).resolve().parents[2]
LATE_HASH = {("aeg-d-dwarfs/v3", "S111")}

# Physical types per observable quantity (astropy physical_type names). Fixed before the readings.
SPEED, LENGTH, ANGLE, MASS = "speed/velocity", "length", "angle", "mass"
QTYPE = {
    "sigma_los": {SPEED}, "velocity": {SPEED}, "v_obs": {SPEED}, "v_gas": {SPEED}, "v_disk": {SPEED}, "v_bul": {SPEED},
    "rotation_velocity": {SPEED},
    "half_light_radius": {ANGLE, LENGTH}, "radius": {LENGTH}, "distance": {LENGTH, "dimensionless"},
    "luminosity": {"dimensionless", "power/radiant flux"}, "apparent_magnitude": {"dimensionless"},
    "metallicity_feh": {"dimensionless"}, "stellar_ml_population": {"dimensionless", "mass/power"},
    "mass_hi": {MASS, "dimensionless"}, "mass_gas_limit": {MASS, "dimensionless"},
    "g_obs": {"acceleration"}, "g_bar": {"acceleration"}, "acceleration": {"acceleration"},
}


def read_ecsv(path: Path):
    from astropy.table import Table
    return Table.read(path, format="ascii.ecsv")


def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def physical_type(unit: str):
    """astropy's physical type name; log(x) units (e.g. log(pc)) take x's type; M/L ratios are "mass/power"."""
    import astropy.units as u
    s = str(unit).strip()
    if s in ("", "--", "None", "dex", "mag", "dimensionless"):
        return "dimensionless"
    m = re.fullmatch(r"(?:log|dex)\((.+)\)", s)
    if m:
        return physical_type(m.group(1))
    try:
        pt = u.Unit(s.replace("Msun", "solMass").replace("Lsun", "solLum"))
        if pt.physical_type == "unknown" and (pt.decompose() / (u.kg / u.W)).decompose().physical_type == "dimensionless":
            return "mass/power"
    except Exception:  # noqa: BLE001
        pass
    try:
        return str(u.Unit(s, parse_strict="raise").physical_type)
    except Exception:  # noqa: BLE001
        try:
            return str(u.Unit(s.replace("Msun", "solMass").replace("Lsun", "solLum")).physical_type)
        except Exception:  # noqa: BLE001
            return None


def ints(v) -> list[int]:
    return [int(x) for x in re.findall(r"\b\d+\b", str(v))] if re.fullmatch(r"[\d,;\s–-]+", str(v).strip()) else []


def open_member(path: Path, member: str) -> bytes | None:
    try:
        with tarfile.open(path) as tf:
            for m in tf.getmembers():
                if m.name.lstrip("./") == member.lstrip("./") or m.name.endswith("/" + member):
                    return tf.extractfile(m).read()
    except tarfile.TarError:
        pass
    return None


def place_checks(rule: dict, files: dict[str, Path]) -> list[tuple[str, str]]:
    """(result, detail) for each mechanically checkable place; [] if none."""
    out = []
    w = rule.get("where", {})
    for sid in rule["sources"]:
        f = files.get(sid)
        if f is None:
            continue
        data = None
        if "member" in w and not re.search(r"[{}\[]", str(w["member"])):
            data = open_member(f, str(w["member"]))
            out.append(("pass" if data is not None else "fail", f"{sid}: member {w['member']} {'present' if data is not None else 'absent'}"))
        target = io.BytesIO(data) if data is not None else f
        name = str(w.get("member", f.name))
        if "hdu" in w and ints(w["hdu"]) and name.endswith((".fits", ".fit", ".fits.gz")):
            from astropy.io import fits
            with fits.open(target) as h:
                k = ints(w["hdu"])[0]
                ok = k < len(h)
                out.append(("pass" if ok else "fail", f"{sid}: HDU {k} of {len(h)}"))
                if ok and "row" in w and ints(w["row"]) and hasattr(h[k], "data") and h[k].data is not None:
                    r = ints(w["row"])[0]
                    out.append(("pass" if 1 <= r <= len(h[k].data) else "fail", f"{sid}: row {r} of {len(h[k].data)}"))
        if "page" in w and ints(w["page"]) and f.suffix.lower() == ".pdf":
            import subprocess
            info = subprocess.run(["pdfinfo", str(f)], capture_output=True, text=True).stdout
            m = re.search(r"Pages:\s+(\d+)", info)
            if m:
                pages = int(m.group(1))
                bad = [p for p in ints(w["page"]) if not 1 <= p <= pages]
                out.append(("fail" if bad else "pass", f"{sid}: pages {ints(w['page'])} of {pages}"))
        if "line" in w and ints(w["line"]):
            text = data if data is not None else None
            if text is None and f.suffix in (".tex", ".txt", ".dat", ".mrt", ".csv", ".html"):
                text = f.read_bytes()
            if text is not None:
                if text[:2] == b"\x1f\x8b":
                    text = gzip.decompress(text)
                n = text.count(b"\n") + 1
                bad = [x for x in ints(w["line"]) if not 1 <= x <= n]
                out.append(("fail" if bad else "pass", f"{sid}: lines {ints(w['line'])[:6]} of {n}"))
    return out


def agg(parts: list[tuple[str, str]]) -> tuple[str, str]:
    rs = [r for r, _ in parts]
    res = "fail" if "fail" in rs else "review" if "review" in rs else "not verified" if "not verified" in rs else "pass" if "pass" in rs else "n/a"
    return res, " | ".join(d for _, d in parts)[:1500]


def reader_inputs(readings: Path, k: str, ds: str) -> dict:
    out: dict = {}
    for base in (readings / k / ds / "out", readings / k / ds):
        p = base / "inputs.csv"
        if p.exists():
            for r in csv.DictReader(p.open(encoding="utf-8")):
                out.setdefault(r["measurement_id"].strip(), []).append(r)
            break
    return out


def main(argv) -> int:
    packets, readings, sample_csv, out_csv = (Path(x) for x in argv[1:5])
    root = Path(argv[5]) if len(argv) > 5 else ROOT_DEFAULT
    sys.path.insert(0, str(root / "pipeline"))
    from aeg import fetch
    sample = [r for r in csv.DictReader(sample_csv.open(encoding="utf-8")) if r["status"] == "sample"]
    rows_out = []
    for stratum in dict.fromkeys(r["stratum"] for r in sample):
        ds = stratum.split("/")[0]
        pkg = root / "data/packages" / stratum
        m = {r["measurement_id"]: r for r in read_ecsv(pkg / "tables/measurements.ecsv")}
        o = {r["observable_id"]: r for r in read_ecsv(pkg / "tables/observables.ecsv")}
        units_meas = {c: str(read_ecsv(pkg / "tables/measurements.ecsv")[c].unit) for c in ("g_obs", "g_bar")}
        rules = json.loads((pkg / "locators.json").read_text(encoding="utf-8"))["rules"]
        src = {e["id"]: e for e in json.loads((pkg / "sources.json").read_text(encoding="utf-8"))["sources"]}
        pdir = packets / ds
        files = {}
        for sid, e in src.items():
            f = pdir / "files" / Path(e.get("file") or sid).name
            if f.exists():
                files[sid] = f
        rin = {k: reader_inputs(readings, k, ds) for k in ("a", "b")}
        for s in (r for r in sample if r["stratum"] == stratum):
            mid = s["measurement_id"]
            row = m[mid]
            refs = [("measurements", str(row["source_ref"]), None)]
            for i in (str(row["observed_from"]) + ";" + str(row["baryonic_from"])).split(";"):
                if i in o:
                    refs.append(("observables", str(o[i]["source_ref"]), o[i]))
            c1, c4, c5, used, rules_hit = [], [], [], set(), []
            for t, ref, ob in refs:
                hit = [r for r in rules if r["table"] == t and re.match(r["match"], ref)]
                c1.append(("pass" if len(hit) == 1 else "fail", f"{t}: {len(hit)} rules"))
                if len(hit) == 1:
                    rules_hit.append(hit[0])
                    used.update(hit[0]["sources"])
                    c4 += place_checks(hit[0], files)
                if ob is not None:
                    want = QTYPE.get(str(ob["quantity"]))
                    if want:
                        pt = physical_type(ob["unit"])
                        ok = pt is not None and pt in want
                        c5.append(("pass" if ok else "fail", f"{ob['quantity']} [{ob['unit']}] is {pt}"))
            gu = all(physical_type(u) == "acceleration" for u in units_meas.values())
            c5.append(("pass" if gu else "fail", f"g units {units_meas}"))
            c2, c3 = [], []
            for sid in sorted(used):
                e = src.get(sid)
                if e is None:
                    c2.append(("fail", f"{sid}: no entry"))
                    continue
                lic = e.get("licence") or {}
                ok2 = all(e.get(k) for k in ("id", "kind", "citation")) and bool(e.get("identifier")) and all(lic.get(k) for k in ("status", "checked_where", "checked_on"))
                c2.append(("pass" if ok2 else "fail", f"{sid}: record {'complete' if ok2 else 'incomplete'}"))
                if not e.get("sha256"):
                    c3.append(("fail", f"{sid}: no recorded hash"))
                elif sid not in files:
                    c3.append(("not verified", f"{sid}: file not in packet"))
                else:
                    err = fetch.verify(files[sid], e)
                    c3.append(("fail" if err else "pass", f"{sid}: {'verifies' if not err else err}"))
            # check 6
            ra = {norm_name(r.get("input", "")): r for r in rin["a"].get(mid, [])}
            rb = {norm_name(r.get("input", "")): r for r in rin["b"].get(mid, [])}
            no = lambda r: re.match(r"\s*(no|n|false)\b", str(r.get("at_locator", "")), re.I) is not None
            yes = lambda r: re.match(r"\s*(yes|y|true)\b", str(r.get("at_locator", "")), re.I) is not None
            has_corr = any("correction" in r for r in rules_hit)
            # Check 6. Readers name inputs freely, so inputs are not matched across readers by name.
            # An input counts only if it is tied to a locator: its normalised name equals, contains or is
            # contained in (3 characters or more) a token of the row's locators: the quantity of an
            # observable the row uses, or a column a matched rule names (templates filled). Inputs with
            # no locator (for example constants or cosmology that the methods text places) are listed only.
            tokens = {norm_name(str(ob["quantity"])) for _, _, ob in refs if ob is not None}
            for t, ref, _ in refs:
                for r in rules_hit:
                    mm = re.match(r["match"], ref) if r["table"] == t else None
                    if not mm:
                        continue
                    g = mm.groupdict()
                    col = re.sub(r"\{(\w+)\}", lambda x: str(g.get(x.group(1), "")), str(r.get("where", {}).get("column", "")))
                    for c in re.split(r"[,;]| and ", col):
                        if len(norm_name(c)) >= 2:
                            tokens.add(norm_name(c))
            tied = lambda n: any(len(x) >= 3 and (x == n or x in n or n in x) for x in tokens) or n in tokens
            c6, review = [], []
            not_at = {}
            for k, rr in (("a", ra), ("b", rb)):
                not_at[k] = sorted(f"{n}{'' if tied(n) else ' (no locator ties to it)'}" for n, r in rr.items() if no(r))
                if any(yes(r) for n, r in rr.items() if tied(n)):
                    c6.append(("pass", f"reader {k}: inputs tied to locators found at them"))
            if not_at["a"] and not_at["b"]:
                c6.append(("review", "both readers mark inputs not at the place given: " + str(not_at)
                           + (" (a correction applies to this row)" if has_corr else "")))
            elif not_at["a"] or not_at["b"]:
                review.append("one reader marks inputs not at the place given: " + str(not_at))
            late = sorted(sid for sid in used if (stratum, sid) in LATE_HASH)
            for sid in late:
                fname = Path(src[sid].get("file") or "").name
                okk = all(any(fname and fname in str(r.get("file", "")) and yes(r) for r in rr.get(mid, [])) for rr in rin.values())
                c3.append(("pass" if okk else "fail", f"{sid}: hashed after reading; {'both readers found the input in it' if okk else 'not confirmed by both readers'}"))
                c6.append(("pass" if okk else "fail", f"{sid}: late hash, both readers {'confirm' if okk else 'do not confirm'}"))
            checks = {"1_locator": agg(c1), "2_record": agg(c2), "3_hash": agg(c3), "4_place": agg(c4), "5_units": agg(c5), "6_found": agg(c6)}
            rs = [v[0] for v in checks.values()]
            result = "fail" if "fail" in rs else "review" if "review" in rs else "not verified" if "not verified" in rs else "pass"
            rec = {"stratum": stratum, "measurement_id": mid, "result": result}
            for k, (r, d) in checks.items():
                rec[k], rec[k + "_detail"] = r, d
            rec["late_hash_sources"] = ";".join(late)
            rec["review"] = " | ".join(review)
            rows_out.append(rec)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0]))
        w.writeheader()
        w.writerows(rows_out)
    from collections import Counter
    print(Counter(r["result"] for r in rows_out))
    for k in ("1_locator", "2_record", "3_hash", "4_place", "5_units", "6_found"):
        print(k, Counter(r[k] for r in rows_out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
