"""D-052: select structure, distance and magnitude values per system (docs/methods/D052_STRUCTURE_SELECTION.md).

Usage (from the package directory): python reproduction/select_structure.py
Reads reading/structure_values_all.csv and the LVDB index; writes reading/structure_selection.csv.
Selects only; computes nothing except m_V,0 = M_V + (m-M)_paper (item 5), as the spec says.
"""

from __future__ import annotations

import csv
import glob
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
ORDER = ["exponential", "plummer", "sersic", "king"]
PROFILE_RE = {
    "exponential": re.compile(r"\bexp(onential)?\b", re.I),
    "plummer": re.compile(r"plummer", re.I),
    "sersic": re.compile(r"s[eé]rsic", re.I),
    "king": re.compile(r"\bking\b", re.I),
}


def quoted(r: dict) -> bool:
    return "quoted from" in (r.get("note", "") + " " + r.get("variant", "")).lower()


def headline(r: dict) -> bool:
    return r.get("variant", "").strip().lower().startswith("headline")


def profile_of(r: dict) -> str | None:
    text = r.get("variant", "") + " " + r.get("note", "")
    hits = [p for p, rx in PROFILE_RE.items() if rx.search(text)]
    return hits[0] if len(hits) == 1 else None


def sig(x: str) -> int:
    return len("".join(ch for ch in x if ch.isdigit()).lstrip("0"))


def dedupe(rows: list[dict]) -> tuple[dict | None, str]:
    if not rows:
        return None, "none"
    if len(rows) == 1:
        return rows[0], ""
    tab = [r for r in rows if "table" in r.get("location", "").lower()]
    pool = tab or rows
    top = max(sig(r["value"]) for r in pool)
    pool = [r for r in pool if sig(r["value"]) == top]
    distinct = {(r["value"], r["err_minus"], r["err_plus"]) for r in pool}
    if len(distinct) == 1:
        return pool[0], "duplicate printing resolved"
    return None, "tie between printings"


def by_rule(rows: list[dict], q: str) -> tuple[dict | None, str]:
    """Headline, else abstract-cited, else the sole row; then duplicate printings."""
    rs = [r for r in rows if r["quantity"] == q and r["value"].strip() and not quoted(r)]
    if not rs:
        return None, "not printed"
    h = [r for r in rs if headline(r)]
    if h:
        return dedupe(h)
    a = [r for r in rs if "abstract" in r.get("location", "").lower()]
    if a:
        return dedupe(a)
    if len({(r["value"], r["err_minus"], r["err_plus"]) for r in rs}) == 1 or len(rs) == 1:
        return dedupe(rs)
    return None, "several values, none adopted: for JvH"


def structure(rows: list[dict]) -> dict:
    rs = [r for r in rows if not quoted(r) and r["quantity"] in ("ra0", "dec0", "ellipticity", "pa", "r_h") and r["value"].strip()]
    out, flags = {}, []
    h = [r for r in rs if headline(r)]
    fits = {}
    for r in rs:
        p = profile_of(r)
        if p:
            fits.setdefault(p, []).append(r)
    if h:
        chosen, how = h, "headline"
    else:
        p = next((p for p in ORDER if any(x["quantity"] == "r_h" for x in fits.get(p, []))), None)
        if p:
            chosen, how = fits[p], f"no fit adopted; {p} by fixed order"
        else:
            chosen, how = rs, "single unlabelled fit"
            if len({r["value"] for r in rs if r["quantity"] == "r_h"}) > 1:
                flags.append("several unlabelled r_h values: for JvH")
    # shared centre/shape rows not tied to a fit
    common = [r for r in rs if profile_of(r) is None and not headline(r)]
    for q in ("ra0", "dec0", "ellipticity", "pa", "r_h"):
        cand = [r for r in chosen if r["quantity"] == q] or [r for r in common if r["quantity"] == q]
        if q == "r_h":
            ang = [r for r in cand if r["unit"] in ("arcmin", "arcsec")]
            if ang:
                cand = ang
            elif cand:
                flags.append("physical radius only")
        r, why = dedupe(cand)
        if why == "tie between printings":
            flags.append(f"{q}: tie between printings")
        out[q] = r
    out["profile_choice"] = how
    rh = out.get("r_h")
    conv = ""
    if rh:
        t = (rh.get("note", "") + " " + rh.get("variant", "") + " " + rh.get("quote", "")).lower()
        if re.search(r"circulari[sz]|azimuthal", t):
            conv = "circularised"
        elif re.search(r"semi-?major|major axis", t):
            conv = "semi-major"
        else:
            conv = "semi-major (assumed)"
            flags.append("rh_convention_not_stated")
    out["rh_convention"] = conv
    out["flags"] = flags
    return out


def main() -> int:
    vals = list(csv.DictReader(open(PKG / "reading/structure_values_all.csv", encoding="utf-8")))
    keys = [r["key"] for r in csv.DictReader(open(PKG / "reading/kinds.csv", encoding="utf-8"))]
    lv = {}
    for f in sorted(glob.glob(str(PKG / "source/lvdb/dwarf_*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            lv[r["key"]] = r
    res = []
    for k in keys:
        row = {"key": k}
        flags = []
        refs = {c: [x.strip() for x in (lv[k].get(c) or "").split(";") if x.strip()] for c in ("ref_structure", "ref_distance", "ref_m_v")}
        s_rows = [r for r in vals if r["key"] == k and r["role"] == "structure" and r["paper"] in refs["ref_structure"]]
        st = structure(s_rows) if s_rows else {"flags": ["structure paper not read"]}
        flags += st.get("flags", [])
        for q in ("ra0", "dec0", "ellipticity", "pa", "r_h"):
            r = st.get(q)
            row[q] = r["value"] if r else ""
            row[q + "_err"] = f"{r['err_minus']}/{r['err_plus']}" if r else ""
            row[q + "_unit"] = r["unit"] if r else ""
            row[q + "_loc"] = f"{r['paper']} {r['location']}" if r else ""
        row["profile_choice"] = st.get("profile_choice", "")
        row["rh_convention"] = st.get("rh_convention", "")
        d_rows = [r for r in vals if r["key"] == k and r["role"] == "distance" and r["paper"] in refs["ref_distance"]]
        d, why = by_rule(d_rows, "distance_modulus")
        if d is None and why != "several values, none adopted: for JvH":
            d, why = by_rule(d_rows, "distance")
        meth = [r for r in d_rows if r["quantity"] == "method" and r["value"].strip()]
        mtext = " / ".join(sorted({r["value"] for r in meth}))
        if re.search(r"kinematic|velocity|dynamical", mtext, re.I):
            flags.append("distance method may be kinematic: check (D-036 #6)")
        row.update({"distance": d["value"] if d else "", "distance_err": f"{d['err_minus']}/{d['err_plus']}" if d else "",
                    "distance_unit": d["unit"] if d else "", "distance_quantity": d["quantity"] if d else "",
                    "distance_loc": f"{d['paper']} {d['location']}" if d else "", "distance_method": mtext})
        if d is None:
            flags.append(f"distance: {why}")
        m_rows = [r for r in vals if r["key"] == k and r["role"] == "magnitude" and r["paper"] in refs["ref_m_v"]]
        mv, why = by_rule(m_rows, "M_V")
        mu, why_mu = by_rule(m_rows, "distance_modulus")
        ext, _ = by_rule(m_rows, "extinction")
        row.update({"M_V": mv["value"] if mv else "", "M_V_err": f"{mv['err_minus']}/{mv['err_plus']}" if mv else "",
                    "M_V_loc": f"{mv['paper']} {mv['location']}" if mv else "",
                    "mu_paper": mu["value"] if mu else "", "extinction_note": ext["value"] if ext else ""})
        if mv is None:
            flags.append(f"M_V: {why}")
        if mv and mu:
            try:
                row["m_V0"] = f"{float(mv['value'].replace(chr(8722), '-')) + float(mu['value'].replace(chr(8722), '-')):.4f}"
            except ValueError:
                row["m_V0"] = ""
                flags.append("m_V0 not computable from printed strings")
        else:
            row["m_V0"] = ""
            if mv:
                flags.append("distance basis of M_V differs")
        row["flags"] = " | ".join(flags)
        res.append(row)
    names = list(dict.fromkeys(k for r in res for k in r))
    with open(PKG / "reading/structure_selection.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, restval="")
        w.writeheader()
        w.writerows(res)
    print(f"systems {len(res)}; with r_h {sum(1 for r in res if r['r_h'])}; with distance {sum(1 for r in res if r['distance'])}; "
          f"with M_V {sum(1 for r in res if r['M_V'])}; with m_V0 {sum(1 for r in res if r['m_V0'])}; flagged {sum(1 for r in res if r['flags'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
