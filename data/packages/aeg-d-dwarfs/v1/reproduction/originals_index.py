"""Build reading/originals.csv: the original papers behind every A5/A7 system's inputs.

Run from the package directory after `python -m aeg.fetch .`:
    python reproduction/originals_index.py [--download DIR]

Step 1 (offline): LVDB v1.1.1 ref_vlos, ref_structure, ref_distance and ref_m_v
for every system in reading/kinds.csv -> reading/originals_list.csv.
Step 2 (network, arxiv.org only): for each reference, the arXiv identifier from
the LVDB bibliography (source/lvdb/lvdb.bib), else an arXiv title search; the
abs page gives the versions, journal-ref and comments; the latest version's PDF
is downloaded and hashed. Records what was found; opens no value.
"""

from __future__ import annotations

import csv
import glob
import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
ROLES = {"ref_vlos": "sigma", "ref_structure": "structure", "ref_distance": "distance", "ref_m_v": "magnitude"}
UA = {"User-Agent": "extragravitation-atlas-pipeline (+https://extragravitation.org)"}
# Found by arXiv title search on 2026-10-30 (absent from the LVDB bibliography); titles checked by hand.
TITLE_SEARCH = {"Hargis2020ApJ...888...31H": "1907.07185", "Munoz2018ApJ...860...66M": "1806.06891", "Vivas2022ApJ...926...78V": "2112.08467"}
NOT_ON_ARXIV = {
    "Monelli2025A&A...700A.201M": "no arXiv version found by title search; version of record via JvH browser",
    "vandeRydt1991AJ....102..130V": "no arXiv version found by title search; version of record via JvH browser",
    "deVaucouleurs1991rc3..book.....D": "catalogue (RC3, book); machine-readable version VizieR VII/155; via JvH browser or a reachable VizieR mirror",
}


def step1() -> list[dict]:
    keys = {r["key"] for r in csv.DictReader(open(PKG / "reading/kinds.csv", encoding="utf-8"))}
    refs: dict[str, dict] = {}
    for f in sorted(glob.glob(str(PKG / "source/lvdb/dwarf_*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            if r["key"] not in keys:
                continue
            for col, role in ROLES.items():
                for x in (r.get(col) or "").split(";"):
                    if x.strip():
                        e = refs.setdefault(x.strip(), {"roles": set(), "systems": set()})
                        e["roles"].add(role)
                        e["systems"].add(r["key"])
    rows = []
    for k in sorted(refs):
        m = re.match(r"^[A-Za-z_\-]+(\d{4}.{15})$", k)
        rows.append({"lvdb_ref": k, "bibcode": m.group(1) if m else "", "roles": ";".join(sorted(refs[k]["roles"])),
                     "n_systems": len(refs[k]["systems"]), "systems": ";".join(sorted(refs[k]["systems"]))})
    with open(PKG / "reading/originals_list.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


def bibliography() -> dict[str, dict]:
    bib = (PKG / "source/lvdb/lvdb.bib").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", bib, re.S):
        body = m.group(2)

        def f(k):
            x = re.search(r"\b" + k + r'\s*=\s*(?:\{(.*?)\}|"(.*?)"|(\w+))\s*,?\s*\n', body, re.S)
            return re.sub(r"\s+", " ", next(g for g in x.groups() if g is not None)).strip("{}") if x else ""

        out[m.group(1).strip()] = {"title": f("title"), "eprint": f("eprint"), "doi": f("doi")}
    return out


def get(url: str) -> bytes:
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(8)
    raise err


def step2(rows: list[dict], download: Path | None) -> None:
    bib = bibliography()
    fields = ["lvdb_ref", "bibcode", "doi", "title", "roles", "n_systems", "systems", "arxiv_id", "arxiv_version",
              "arxiv_version_dates", "arxiv_journal_ref", "arxiv_comments", "arxiv_signals_accepted", "eprint_found_by",
              "pdf_url", "bytes", "sha256", "retrieved", "access_note"]
    out = []
    for r in rows:
        k = r["lvdb_ref"]
        b = bib.get(k, {})
        e = {**r, "doi": b.get("doi", ""), "title": b.get("title", ""), "access_note": NOT_ON_ARXIV.get(k, "")}
        eprint = b.get("eprint") or TITLE_SEARCH.get(k, "")
        if not eprint and "arXiv" in k:
            a = re.search(r"arXiv(\d{4})(\d{5})", k)
            eprint = f"{a.group(1)}.{a.group(2)}"
        e["eprint_found_by"] = "arXiv title search" if k in TITLE_SEARCH else ("LVDB bibliography" if eprint else "")
        if eprint:
            page = get(f"https://arxiv.org/abs/{eprint}").decode()
            vs = [(int(v), html.unescape(re.sub("<[^>]+>", "", d)).strip())
                  for v, d in re.findall(r"<strong>\[v(\d+)\]</strong>\s*(.*?)\s*\(", page)]
            jr = re.search(r'<td class="tablecell jref">(.*?)</td>', page, re.S)
            cm = re.search(r'<td class="tablecell comments mathjax">(.*?)</td>', page, re.S)
            v = max(x[0] for x in vs)
            url = f"https://arxiv.org/pdf/{eprint}v{v}"
            data = get(url)
            if download:
                (download / f"{eprint.replace('/', '_')}v{v}.pdf").write_bytes(data)
            e.update(arxiv_id=eprint, arxiv_version=v, arxiv_version_dates="; ".join(f"v{a} {d}" for a, d in vs),
                     arxiv_journal_ref=html.unescape(jr.group(1)).strip() if jr else "",
                     arxiv_comments=html.unescape(re.sub("<[^>]+>", "", cm.group(1))).strip() if cm else "",
                     pdf_url=url, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), retrieved=time.strftime("%Y-%m-%d"))
            e["arxiv_signals_accepted"] = "yes" if e["arxiv_journal_ref"] or re.search(
                r"accept|published|in press", e["arxiv_comments"], re.I) else "no"
            time.sleep(3)
        out.append(e)
    with open(PKG / "reading/originals.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    rows = step1()
    dl = Path(sys.argv[sys.argv.index("--download") + 1]) if "--download" in sys.argv else None
    step2(rows, dl)
