"""List the source files a row's inputs need (pilot, D-118). Usage: python needed_sources.py MEASUREMENT_ID..."""
import json, re, sys
from pathlib import Path
from astropy.table import Table
ROOT = Path(__file__).resolve().parents[3]

def need(mid):
    ds, ver, _ = mid.split("/")
    pkg = ROOT / "data/packages" / ds / ver
    m = Table.read(pkg / "tables/measurements.ecsv", format="ascii.ecsv")
    o = {r["observable_id"]: r for r in Table.read(pkg / "tables/observables.ecsv", format="ascii.ecsv")}
    rules = json.loads((pkg / "locators.json").read_text())["rules"]
    src = {s["id"]: s for s in json.loads((pkg / "sources.json").read_text())["sources"]}
    row = [r for r in m if r["measurement_id"] == mid][0]
    refs = [("measurements", str(row["source_ref"]))]
    for i in (str(row["observed_from"]) + ";" + str(row["baryonic_from"])).split(";"):
        if i in o:
            refs.append(("observables", str(o[i]["source_ref"])))
    out = []
    for t, ref in refs:
        hit = [r for r in rules if r["table"] == t and re.match(r["match"], ref)]
        assert len(hit) == 1, (mid, ref, len(hit))
        out.append((t, ref, hit[0]))
    ids = sorted({s for _, _, r in out for s in r["sources"]}, key=lambda x: int(re.sub(r"\D", "", x)))
    return row, out, [src[i] for i in ids]

if __name__ == "__main__":
    for mid in sys.argv[1:]:
        row, out, srcs = need(mid)
        print("==", mid)
        for s in srcs:
            print("  ", s["id"], s["kind"], s.get("sha256", "")[:12] if s.get("sha256") else None, s.get("url", "")[:110], s.get("member", ""))
