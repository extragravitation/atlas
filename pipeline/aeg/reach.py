"""Re-issue test T7: every address in a 3.0.0 package's sources.json is reachable
(docs/standard-3.0.0-reissue-test.md; D-114).

Usage: python -m aeg.reach <package dir> [<out.json>]

Checks each entry's url, identifier.landing_url and identifier.doi (through https://doi.org/) with a GET
that follows redirects, and records the HTTP status. An address that does not return 200 is listed. T7
fails only if such an entry has sha256 null (then nothing would tie the record to a verifiable file).
Runs in GitHub Actions (.github/workflows/reach.yml): the build workspace cannot reach most hosts.
"""

from __future__ import annotations

import datetime as dt
import json
import time
import sys
import urllib.error
import urllib.request
from pathlib import Path

UA = "AtlasOfExtraGravitation-reachability/1.0 (+https://extragravitation.org; info@extragravitation.org)"


def status(url: str) -> tuple[int | str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Range": "bytes=0-1023"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            r.read(1024)
            code = r.status
            return (200 if code in (200, 206) else code), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception as e:  # noqa: BLE001 - recorded as the result
        return f"{type(e).__name__}: {e}"[:200], url


def run(pkg: Path) -> dict:
    spec = json.loads((pkg / "sources.json").read_text(encoding="utf-8"))
    results = []
    for e in spec["sources"]:
        ident = e.get("identifier") or {}
        addrs = [("url", e.get("url")), ("landing_url", ident.get("landing_url"))]
        if ident.get("doi"):
            addrs.append(("doi", "https://doi.org/" + ident["doi"]))
        for kind, a in addrs:
            if a:
                time.sleep(0.5)  # gentle on the hosts (arXiv, doi.org)
                code, final = status(a)
                results.append({"id": e.get("id"), "field": kind, "address": a, "status": code, "final_url": final,
                                "sha256_present": e.get("sha256") is not None})
    bad = [r for r in results if r["status"] != 200]
    fail = [r for r in bad if not r["sha256_present"]]
    return {"test": "T7, docs/standard-3.0.0-reissue-test.md", "package": f"{pkg.parent.name}/{pkg.name}",
            "checked_on": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "result": "fail" if fail else "pass", "n_addresses": len(results), "not_200": bad, "results": results}


def expand(pkg: Path, compact: dict) -> dict:
    """Rebuild the full T7 record from the compact CI annotation and the package's sources.json."""
    spec = {e.get("id"): e for e in json.loads((pkg / "sources.json").read_text(encoding="utf-8"))["sources"]}
    results = []
    for sid, field, code in compact["rows"]:
        e = spec[sid]
        ident = e.get("identifier") or {}
        addr = {"url": e.get("url"), "landing_url": ident.get("landing_url"),
                "doi": "https://doi.org/" + ident["doi"] if ident.get("doi") else None}[field]
        results.append({"id": sid, "field": field, "address": addr, "status": code, "sha256_present": e.get("sha256") is not None})
    bad = [r for r in results if r["status"] != 200]
    return {"test": "T7, docs/standard-3.0.0-reissue-test.md", "package": compact["package"], "checked_on": compact["checked_on"],
            "result": compact["result"], "n_addresses": len(results), "not_200": bad, "results": results,
            "note": "Expanded from the compact CI annotation; final URLs after redirects are in the run's artifact only."}


def main(argv: list[str]) -> int:
    if len(argv) == 4 and argv[1] == "--expand":
        # python -m aeg.reach --expand <package dir> <compact.json>  -> writes <package>/reproduction/reachability.json
        pkg = Path(argv[2]).resolve()
        out = expand(pkg, json.loads(Path(argv[3]).read_text(encoding="utf-8")))
        (pkg / "reproduction").mkdir(exist_ok=True)
        (pkg / "reproduction/reachability.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{out['package']}: T7 {out['result']}; {out['n_addresses']} addresses, {len(out['not_200'])} not 200")
        return 0 if out["result"] == "pass" else 1
    if len(argv) not in (2, 3):
        print(__doc__)
        return 2
    out = run(Path(argv[1]).resolve())
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    if len(argv) == 3:
        Path(argv[2]).write_text(text, encoding="utf-8")
    print(f"{out['package']}: T7 {out['result']}; {out['n_addresses']} addresses, {len(out['not_200'])} not 200")
    for r in out["not_200"]:
        print(f"  {r['id']} {r['field']} {r['address']}: {r['status']}")
    return 0 if out["result"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
