"""D-052: select structure, distance and magnitude values per system, version 3.

Version 3 differs from version 2 (output kept as reading/structure_selection_v2.csv) only in
how the modulus string is parsed. The supplementary reading records the modulus as printed
with its errors (e.g. "x ± y"), and version 2's float() failed on those, giving 41 cases
"m_V0 not computable from printed strings". Version 3 takes the leading signed number of the
string as the central value. No rule is changed.

Version 2 docstring follows.

Spec: docs/methods/D052_STRUCTURE_SELECTION.md. The rules are unchanged; version 1 stays on
record (reading/structure_selection_v1.csv). Version 2 fixes three defects found on the
first run:
1. The r_h convention is no longer parsed from free text. It is taken from the two-reader
   supplementary reading (reading/supplement_final.csv):
   - semi_major_stated and elliptical_radius_profile count as semi-major;
   - circularised_stated counts as circularised;
   - not_stated with ellipticity fitted counts as semi-major, assumed and flagged
     (D-052 item 2).
   Where a paper prints both a_h and a circularised r_h, the semi-major row is used, as
   REPRODUCTION.md requires (R_h = a sqrt(1 - e)), and the circularised one is a cross-check.
2. Magnitude, following REPRODUCTION.md: use the paper's own extinction-corrected apparent V
   where printed. Otherwise rebuild m_V,0 = M_V + (m-M), using the modulus the paper states
   it used for M_V (supplementary reading). Otherwise flag "distance basis of M_V differs".
3. The modulus behind M_V comes from the supplementary reading, not the role-limited rows.

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


SEMI_RX = re.compile(r"\ba_?\{?h\}?\b|semi-?major|major axis", re.I)
CIRC_RX = re.compile(r"circulari[sz]|azimuthal|geometric mean|sqrt\(1|√\(1", re.I)


def rh_rows_semi(rows: list[dict]) -> list[dict]:
    """Among r_h rows, those the row text marks as semi-major and not as circularised."""
    out = []
    for r in rows:
        t = " ".join(r.get(c, "") for c in ("variant", "note", "quote"))
        if SEMI_RX.search(t) and not CIRC_RX.search(t):
            out.append(r)
    return out


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
    out["flags"] = flags
    return out


def convention(sup: dict, st: dict, s_rows: list[dict], flags: list) -> str:
    if not sup:
        flags.append("no supplementary coding")
        return ""
    d, efit = sup.get("rh_definition", ""), sup.get("ellipticity_fitted", "")
    both = "both printed" in sup.get("note", "").lower()
    if both:
        semi = rh_rows_semi([r for r in s_rows if r["quantity"] == "r_h" and r["value"].strip()
                             and not quoted(r) and r["unit"] in ("arcmin", "arcsec")])
        r, why = dedupe([x for x in semi if headline(x)] or semi)
        if r is not None:
            st["r_h"] = r
            return "semi-major (a_h; circularised value printed too)"
        flags.append("both radii printed but semi-major row not identified: check")
    if d in ("semi_major_stated", "elliptical_radius_profile"):
        return "semi-major"
    if d == "circularised_stated":
        return "circularised"
    if efit == "yes":
        flags.append("rh_convention_not_stated")
        return "semi-major (assumed, D-052 item 2)"
    flags.append("rh convention not stated and ellipticity not fitted")
    return "not stated"


def main() -> int:
    vals = list(csv.DictReader(open(PKG / "reading/structure_values_all.csv", encoding="utf-8")))
    sup = {(r["key"], r["paper"], r["role"]): r for r in csv.DictReader(open(PKG / "reading/supplement_final.csv", encoding="utf-8"))}
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
        s_sup = next((sup.get((k, p, "structure")) for p in refs["ref_structure"] if sup.get((k, p, "structure"))), None)
        conv = convention(s_sup, st, s_rows, flags) if s_rows else ""
        for q in ("ra0", "dec0", "ellipticity", "pa", "r_h"):
            r = st.get(q)
            row[q] = r["value"] if r else ""
            row[q + "_err"] = f"{r['err_minus']}/{r['err_plus']}" if r else ""
            row[q + "_unit"] = r["unit"] if r else ""
            row[q + "_loc"] = f"{r['paper']} {r['location']}" if r else ""
        row["profile_choice"] = st.get("profile_choice", "")
        row["rh_convention"] = conv
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
        m_sup = next((sup.get((k, p, "magnitude")) for p in refs["ref_m_v"] if sup.get((k, p, "magnitude"))), {}) or {}
        mv, why = by_rule(m_rows, "M_V")
        if mv is None:
            mv_any = [r for r in m_rows if r["quantity"] == "M_V" and r["value"].strip()]
            if mv_any:
                mv, why = by_rule([{**r, "note": r["note"].replace("quoted from", "computed with distance from")} for r in mv_any], "M_V")
                if mv is not None:
                    flags.append("M_V row noted as using another paper's distance")
        appv, _ = by_rule(m_rows, "m_v")
        row.update({"M_V": mv["value"] if mv else "", "M_V_err": f"{mv['err_minus']}/{mv['err_plus']}" if mv else "",
                    "M_V_loc": f"{mv['paper']} {mv['location']}" if mv else "",
                    "mu_paper": m_sup.get("mv_distance_modulus", ""), "mv_distance_basis": m_sup.get("mv_distance_basis", ""),
                    "m_V0": "", "m_V0_route": ""})
        if m_sup.get("apparent_v_printed") == "yes" and appv is not None:
            if m_sup.get("apparent_v_extinction_corrected") == "yes":
                row["m_V0"], row["m_V0_route"] = appv["value"], f"printed m_V,0 ({appv['paper']} {appv['location']})"
            else:
                row["m_V0_route"] = "printed apparent V not extinction-corrected: needs extinction"
                flags.append("apparent V not extinction-corrected")
        elif mv is not None and m_sup.get("mv_distance_modulus", "").strip():
            try:
                def f(x: str) -> float:
                    m = re.match(r"\s*([-+]?\d+(?:\.\d+)?)", x.replace(chr(8722), "-"))
                    if not m:
                        raise ValueError(x)
                    return float(m.group(1))
                row["m_V0"] = f"{f(mv['value']) + f(m_sup['mv_distance_modulus']):.4f}"
                row["m_V0_route"] = f"M_V + (m-M) used by the paper ({m_sup.get('mv_distance_basis', '')})"
            except ValueError:
                flags.append("m_V0 not computable from printed strings")
        elif mv is not None:
            flags.append("distance basis of M_V differs")
            row["m_V0_route"] = "M_V only"
        else:
            flags.append(f"M_V: {why}")
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
