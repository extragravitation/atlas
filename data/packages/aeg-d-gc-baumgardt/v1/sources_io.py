"""Readers for the aeg-d-gc-baumgardt/v1 source files (no conversion, no physics).

Each reader returns the values exactly as printed (strings kept alongside
floats where the transcription test needs the printed digits).
"""

from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path

LOS_TYPES = {"RV", "F13", "L13", "L15", "K18", "D21", "C22", "G22"}   # veldis.html legend: line-of-sight
PM_TYPES = {"W15", "C21", "H21", "VB21", "LI22", "T22", "P22"}        # veldis.html legend: proper motions


def norm_name(name: str) -> str:
    """Key for matching cluster names across sources."""
    n = name.upper().replace("MW-", "", 1) if name.upper().startswith("MW-") else name.upper()
    n = re.sub(r"[\s\-_]", "", n)
    n = re.sub(r"^TERZAN(\d+)$", r"TER\1", n)
    aliases = {"2MSGC01": "2MASSGC01", "2MSGC02": "2MASSGC02", "2MS1": "2MASSGC01", "2MS2": "2MASSGC02",
               "DJORG1": "DJOR1", "DJORG2": "DJOR2", "TERZAN1": "TER1", "1636283": "ESO452SC11", "ESOSC06": "ESO280SC06"}
    return aliases.get(n, n)


def _num(s: str):
    s = s.strip()
    if s in ("", "-", "--"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


# ------------------------------------------------------------------ veldis.html

def read_veldis(path: Path) -> list[dict]:
    """Rows of the velocity-dispersion table; the cluster name carries down to its later rows."""
    s = path.read_text(encoding="latin1")
    rows = re.findall(r"<tr[^>]*>(.*?)(?=<tr|</table)", s, re.S | re.I)
    out, current = [], None
    for r in rows:
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                 for c in re.findall(r"<td[^>]*>(.*?)(?=<td|</tr|$)", r, re.S | re.I)]
        if len(cells) != 7:
            continue
        name, rr, n, sig, up, lo, typ = cells
        if name:
            current = name
        out.append({"cluster": current, "r_arcsec": rr, "n_star": n, "sigma": sig, "err_hi": up, "err_lo": lo, "type": typ})
    return out


# --------------------------------------------------------------------- Harris

def _fixed_part(lines: list[str], header_idx: int, labels: list[str]) -> list[dict]:
    """Parse a fixed-width part: each token goes to the label whose right edge is nearest its right edge."""
    head = lines[header_idx]
    ends, pos = [], 0
    for lab in labels:
        i = head.index(lab, pos)
        ends.append(i + len(lab)); pos = i + len(lab)
    out = []
    for line in lines[header_idx + 1:]:
        if not line.strip():
            if out:
                break
            continue
        ident = line[:12].strip()
        rec = {"id": ident, "flags": ""}
        for m in re.finditer(r"\S+", line[12:]):
            tok, end = m.group(0), m.end() + 12
            if tok in ("c", "c:"):
                rec["flags"] = tok
                continue
            j = min(range(len(ends)), key=lambda k: abs(ends[k] - end))
            rec[labels[j]] = (rec.get(labels[j], "") + " " + tok).strip()
        out.append(rec)
    return out


def read_harris(path: Path) -> dict[str, dict]:
    lines = path.read_text(encoding="latin1").splitlines()
    find = lambda pat: next(i for i, l in enumerate(lines) if l.strip().startswith(pat))
    p1 = _fixed_part(lines, find("ID        Name"), ["Name", "RA", "DEC", "L", "B", "R_Sun", "R_gc", "X", "Y", "Z"])
    p2 = _fixed_part(lines, find("ID       [Fe/H]"), ["[Fe/H]", "wt", "E(B-V)", "V_HB", "(m-M)V", "V_t", "M_V,t",
                                                     "U-B", "B-V", "V-R", "V-I", "spt", "ellip"])
    p3 = _fixed_part(lines, find("ID         v_r"), ["v_r", "+/-", "v_LSR", "sig_v", "+/-", "c", "r_c", "r_h",
                                                     "mu_V", "rho_0", "lg(tc)", "lg(th)"])
    out: dict[str, dict] = {}
    for part, tag in ((p1, "I"), (p2, "II"), (p3, "III")):
        for rec in part:
            d = out.setdefault(rec["id"], {"id": rec["id"]})
            for k, v in rec.items():
                if k == "id":
                    continue
                d[f"{tag}:{k}"] = v
    return out


# ------------------------------------------------------------ McLaughlin & vdM

def read_votable(path: Path) -> list[dict]:
    """Rows as {field name: printed string} from a VizieR VOTable (TABLEDATA)."""
    ns = {"v": "http://www.ivoa.net/xml/VOTable/v1.3"}
    root = ET.parse(path).getroot()
    table = root.find(".//v:TABLE", ns)
    names = [f.get("name") for f in table.findall("v:FIELD", ns)]
    rows = []
    for tr in table.findall(".//v:TABLEDATA/v:TR", ns):
        vals = [(td.text or "").strip() for td in tr.findall("v:TD", ns)]
        rows.append(dict(zip(names, vals)))
    return rows


# ------------------------------------------------------------------- RV files

RV_A = ["RA", "DEC", "DCEN", "RV", "E_RV", "NRV", "MJD", "P_Single", "PMEM_RV", "PMEM_PM"]   # 155 files
RV_B = ["RA", "DEC", "DCEN", "RV", "E_RV", "PMEM_RV", "NRV", "MJD", "P_Single"]              # 5 files; P_Mem_PM last


class RVFormatError(ValueError):
    pass


def read_rv(path: Path) -> list[dict]:
    """Per-star rows of a Baumgardt RV file.

    The cluster name runs up to the first token containing a decimal point
    (the right ascension). Then the fixed columns of the file's layout, then
    optional Gaia G and B-R blocks ("x +- e", 3 tokens each); in layout B the
    proper-motion membership probability is the last token.
    """
    lines = path.read_text(encoding="latin1").splitlines()
    layout_b = "P_Mem_PM" in lines[0]
    cols = RV_B if layout_b else RV_A
    out = []
    for k, line in enumerate(lines[2:], start=3):
        toks = line.split()
        if not toks:
            continue
        i = next((j for j, t in enumerate(toks) if "." in t), None)
        if i is None or i == 0:
            raise RVFormatError(f"{path.name}:{k}: cannot find the right ascension")
        rest = toks[i:]
        tail = rest[len(cols):]
        pm_pm = None
        if layout_b and len(tail) in (1, 4, 7):  # P_Mem_PM present (it is blank on a few rows)
            pm_pm, tail = tail[-1], tail[:-1]
        if len(rest) < len(cols) or len(tail) not in (0, 3, 6):
            raise RVFormatError(f"{path.name}:{k}: unexpected number of fields ({len(toks)})")
        rec = {"Cluster": " ".join(toks[:i])}
        rec.update(dict(zip(cols, rest[:len(cols)])))
        if layout_b:
            rec["PMEM_PM"] = pm_pm
        out.append(rec)
    return out
