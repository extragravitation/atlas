"""Upsilon_V per the written method (REPRODUCTION.md, row "Upsilon_V", option b):
BC03 + Chabrier disk IMF, (M/L)_1 from McLaughlin & van der Marel 2005 (VizieR J/ApJS/161/304/clusters),
Milky Way globular clusters only, interpolated linearly in [Fe/H]; below the lowest tabulated [Fe/H]
the lowest-[Fe/H] value is used (flag beyond_source_range); no extrapolation.

Values are taken as the printed strings in the VOTable TABLEDATA (not float32-rounded).
Not specified by the method (handled here and recorded in notes.md):
  - above the highest tabulated [Fe/H]: not needed for this packet (all [Fe/H] < 0);
  - duplicate [Fe/H] entries: checked to carry identical (M/L)_1, so collapsed.
"""
import sys
import xml.etree.ElementTree as ET

NS = {"v": "http://www.ivoa.net/xml/VOTable/v1.3"}


def load_table(path):
    tree = ET.parse(path)
    root = tree.getroot()
    # namespace-agnostic search
    fields = [f.attrib["name"] for f in root.iter() if f.tag.endswith("FIELD")]
    rows = []
    for tr in root.iter():
        if not tr.tag.endswith("TR"):
            continue
        tds = [td.text or "" for td in tr if td.tag.endswith("TD")]
        rows.append(dict(zip(fields, tds)))
    return rows


def mw_table(path):
    rows = load_table(path)
    mw = [r for r in rows if r["Cluster"].startswith("MW-")]
    pts = {}
    for r in mw:
        feh = float(r["[Fe/H]"])
        ml = float(r["(M/L)1"])
        if feh in pts and abs(pts[feh][0] - ml) > 0:
            raise ValueError(f"inconsistent (M/L)1 at [Fe/H]={feh}: {pts[feh]} vs {ml}")
        pts.setdefault(feh, (ml, []))[1].append((r["recno"], r["Cluster"], r["[Fe/H]"], r["(M/L)1"], r["logAge"]))
    xs = sorted(pts)
    return xs, pts


def upsilon(feh, xs, pts):
    """Return (Upsilon_V, flag, bracketing rows)."""
    if feh < xs[0]:
        return pts[xs[0]][0], "beyond_source_range", [pts[xs[0]][1][0]]
    if feh > xs[-1]:
        raise ValueError("above highest tabulated [Fe/H]: method does not say")
    for lo, hi in zip(xs[:-1], xs[1:]):
        if lo <= feh <= hi:
            ylo, yhi = pts[lo][0], pts[hi][0]
            if hi == lo:
                return ylo, "", [pts[lo][1][0]]
            y = ylo + (yhi - ylo) * (feh - lo) / (hi - lo)
            return y, "", [pts[lo][1][0], pts[hi][1][0]]
    if feh == xs[-1]:
        return pts[xs[-1]][0], "", [pts[xs[-1]][1][0]]
    raise RuntimeError


if __name__ == "__main__":
    xs, pts = mw_table(sys.argv[1])
    print("MW rows:", sum(len(v[1]) for v in pts.values()), "unique [Fe/H]:", len(xs), "range", xs[0], xs[-1])
    for f in sys.argv[2:]:
        print(f, upsilon(float(f), xs, pts))
