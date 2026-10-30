"""Independent second reading of aeg-d-gc-baumgardt/v1.
Hand-written parsers; does not import any package code."""
import csv, re, sys, html
from collections import defaultdict
from astropy.table import Table

PKG = "/home/claude/atlas/data/packages/aeg-d-gc-baumgardt/v1/"
SRC = PKG + "source/"
OUT_MD = PKG + "SECOND_READING.md"
OUT_CSV = PKG + "checks/second_reading.csv"

# ---------------- veldis.html ----------------
def read_veldis():
    td_re = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
    cells = []  # (line_no, raw_inner)
    lines = open(SRC + "veldis.html", encoding="utf-8", errors="replace").read().split("\n")
    for i, ln in enumerate(lines, 1):
        for m in td_re.finditer(ln):
            cells.append((i, m.group(1)))
    rows = []
    k = 0
    cur = None
    while k < len(cells):
        ln, raw = cells[k]
        txt = html.unescape(re.sub(r"<[^>]+>", "", raw)).replace("\xa0", " ")
        if "&nbsp;" in raw and txt.strip() == "":
            k += 1  # separator row between clusters
            cur = None
            continue
        grp = cells[k:k + 7]
        vals = [html.unescape(re.sub(r"<[^>]+>", "", c[1])).strip() for c in grp]
        if vals[0]:
            cur = vals[0]
            nm_raw = vals[0]
        else:
            nm_raw = ""
        if cur is None:
            raise SystemExit(f"row without cluster at line {ln}")
        rows.append(dict(cluster=cur, name_cell=nm_raw, r=vals[1], n=vals[2], sig=vals[3],
                         up=vals[4], low=vals[5], typ=vals[6], line=grp[1][0]))
        k += 7
    return rows

# ---------------- mwgc.dat ----------------
def read_harris():
    lines = open(SRC + "mwgc.dat", encoding="latin-1").read().split("\n")
    parts = {}
    hdr_idx = [i for i, l in enumerate(lines) if re.match(r"^\s+ID\s", l)]
    assert len(hdr_idx) == 3, hdr_idx
    # Part I: R_Sun window = from end of 'B' header column to end of 'R_Sun'
    h1 = lines[hdr_idx[0]]
    a1 = h1.index("R_Sun") - 1; b1 = h1.index("R_Sun") + len("R_Sun")
    h2 = lines[hdr_idx[1]]
    a2 = h2.index("M_V,t") - 1; b2 = h2.index("M_V,t") + len("M_V,t")
    p1, p2 = {}, {}
    for which, (start, end) in enumerate([(hdr_idx[0], hdr_idx[1]), (hdr_idx[1], hdr_idx[2])]):
        for i in range(start + 1, end):
            l = lines[i]
            if l.startswith("_"): break
            if not re.match(r"^ \S", l):
                continue
            cid = l[:12].strip()
            if not cid or "Part" in l:
                continue
            a, b = (a1, b1) if which == 0 else (a2, b2)
            assert l[a-1:a] in (" ", "") and l[b:b+1] in (" ", ""), (i+1, l)
            if which == 0:
                p1.setdefault(cid, (i + 1, l[a1:b1].strip(), l.rstrip()))
            else:
                p2.setdefault(cid, (i + 1, l[a2:b2].strip(), l.rstrip()))
    return p1, p2, (a1, b1, a2, b2)

# ---------------- VOTables (raw XML) ----------------
def read_vot(path):
    txt = open(path, encoding="utf-8").read().split("\n")
    fields = []
    rows = []
    for i, l in enumerate(txt, 1):
        m = re.search(r'<FIELD name="([^"]+)"', l)
        if m:
            fields.append(html.unescape(m.group(1)))
        if l.startswith("<TR>"):
            tds = re.findall(r"<TD>(.*?)</TD>", l)
            assert len(tds) == len(fields), (path, i)
            rows.append((i, dict(zip(fields, tds))))
    return fields, rows

def main():
    V = read_veldis()
    H1, H2, win = read_harris()
    mf, MROWS = read_vot(SRC + "mvdm05/J_ApJS_161_304_models.vot")
    cf, CROWS = read_vot(SRC + "mvdm05/J_ApJS_161_304_clusters.vot")
    print("models fields sample:", [f for f in mf if f in ("W0/gamma", "r0", "Rh", "Dist", "Mod", "E_r0", "e_r0")])
    print("clusters fields sample:", [f for f in cf if "M/L" in f][:4])

    meas = Table.read(PKG + "tables/measurements.ecsv", format="ascii.ecsv")
    obs = Table.read(PKG + "tables/observables.ecsv", format="ascii.ecsv")
    sysT = Table.read(PKG + "tables/systems.ecsv", format="ascii.ecsv")
    O = {r["observable_id"]: r for r in obs}
    S = {r["system_id"]: r["name_in_source"] for r in sysT}

    def val(x):
        return None if (x is None or getattr(x, "mask", False) is True or str(x) == "--") else x

    def fnum(s):
        return float(s) if s not in ("", None) else None

    records = []  # cluster, file, loc, quantity, quoted, pkg, agree
    surprises = []
    arith = []

    def rec(cl, f, loc, q, quoted, pkg, ok):
        records.append(dict(cluster=cl, source_file=f, location=loc, quantity=q, quoted=quoted,
                            package_value=pkg, agree="agree" if ok else "DISAGREE"))

    def same(src_str, pkg):
        if src_str in ("", None):
            return pkg is None
        if pkg is None:
            return False
        return float(src_str) == float(pkg)

    plotted = meas[meas["plotted"] == "true"]
    assert len(plotted) == 64
    vel_by_cl = defaultdict(list)
    for r in V:
        vel_by_cl[r["cluster"]].append(r)

    order = []
    for m in plotted:
        sid = m["system_id"]
        name = str(S[sid]).strip()
        order.append(name)
        assert m["x_gc_baumgardt_dataset"] == "RV"
        # ---- veldis bins
        obs_ids = str(m["observed_from"]).split(";")
        src_rv = [r for r in vel_by_cl.get(name, []) if r["typ"] == "RV"]
        if not vel_by_cl.get(name):
            surprises.append(f"{name}: cluster name not found in veldis.html")
        matched = set()
        for oid in obs_ids:
            o = O[oid]
            assert o["system_id"] == sid
            if o["x_gc_baumgardt_dataset"] != "RV":
                surprises.append(f"{name}: observed_from {oid} has dataset {o['x_gc_baumgardt_dataset']}")
            r_arc = float(o["x_gc_baumgardt_r_arcsec"])
            cand = [r for r in src_rv if float(r["r"]) == r_arc]
            if len(cand) != 1:
                surprises.append(f"{name}: package bin <r>={r_arc} matches {len(cand)} RV rows in veldis.html")
                rec(name, "veldis.html", "-", f"bin <r>={r_arc}", "(no matching RV row)", r_arc, False)
                continue
            r = cand[0]; matched.add(r["line"])
            q = f"{r['name_cell'] or '(blank)'} | {r['r']} | {r['n']} | {r['sig']} | {r['up']} | {r['low']} | {r['typ']}"
            loc = f"veldis.html line {r['line']}"
            tag = f"bin {r['r']}\""
            rec(name, "veldis.html", loc, f"{tag} <r> [arcsec]", q, r_arc, same(r["r"], r_arc))
            rec(name, "veldis.html", loc, f"{tag} NStar", q, val(o["x_gc_baumgardt_n_star"]), same(r["n"], val(o["x_gc_baumgardt_n_star"])))
            rec(name, "veldis.html", loc, f"{tag} sigma [km/s]", q, o["value"], same(r["sig"], o["value"]) and str(o["unit"]) == "km / s")
            rec(name, "veldis.html", loc, f"{tag} dsigma_Up -> err_hi", q, o["err_hi"], same(r["up"], o["err_hi"]))
            rec(name, "veldis.html", loc, f"{tag} dsigma_Low -> err_lo", q, o["err_lo"], same(r["low"], o["err_lo"]))
        for r in src_rv:
            if r["line"] not in matched:
                surprises.append(f"{name}: veldis.html RV bin at line {r['line']} (<r>={r['r']}) is not in observed_from")
        if int(m["x_gc_baumgardt_n_bins"]) != len(obs_ids):
            surprises.append(f"{name}: n_bins={m['x_gc_baumgardt_n_bins']} but observed_from lists {len(obs_ids)}")

        # ---- baryonic
        bar = {}
        for oid in str(m["baryonic_from"]).split(";"):
            o = O[oid]
            p = val(o["x_gc_baumgardt_parameter"])
            bar[str(p)] = o
        hid = re.sub(r"^Ter (\d+)$", r"Terzan \1", name)
        mv_name = "MW-" + hid.replace(" ", "").upper()
        # Harris I
        rs = None
        if hid in H1:
            ln, s, full = H1[hid]; o = bar.get("R_Sun (horizontal branch)")
            pv = None if o is None else o["value"]
            rec(name, "mwgc.dat", f"line {ln} (Part I)", "R_Sun [kpc]", f"{full[:12].strip()} ...{full[win[0]:win[1]+6].rstrip()}  [R_Sun field: '{s}']",
                pv, o is not None and same(s, pv) and str(o["unit"]) == "kpc")
            rs = float(s)
        else:
            surprises.append(f"{name}: not found in mwgc.dat Part I as '{hid}'")
        mvt = None
        if hid in H2:
            ln, s, full = H2[hid]; o = bar.get("M_V,t")
            pv = None if o is None else o["value"]
            rec(name, "mwgc.dat", f"line {ln} (Part II)", "M_V,t [mag]", f"{full[:12].strip()} ...{full[win[2]-6:win[3]+1].rstrip()}  [M_V,t field: '{s}']",
                pv, o is not None and same(s, pv))
            mvt = float(s)
        else:
            surprises.append(f"{name}: not found in mwgc.dat Part II as '{hid}'")
        # MvdM models, King
        mk = [(ln, d) for ln, d in MROWS if d["Cluster"] == mv_name and d["Mod"].strip() == "K"]
        if len(mk) != 1:
            surprises.append(f"{name}: {len(mk)} King rows for {mv_name} in models.vot")
            continue
        ln, d = mk[0]
        loc = f"models.vot line {ln} (recno {d['recno']}, {mv_name}, Mod K)"
        for col, ecol_hi, ecol_lo, pname in [("W0/gamma", "E_W0/gamma", "e_W0/gamma", "W0/gamma"),
                                             ("r0", "E_r0", "e_r0", "r0"),
                                             ("Rh", "E_Rh", "e_Rh", "Rh"),
                                             ("Dist", None, None, "Dist")]:
            o = bar.get(f"McLaughlin & van der Marel 2005 King fit: {pname}")
            pv = None if o is None else o["value"]
            rec(name, "J_ApJS_161_304_models.vot", loc, f"{col}", f"<TD>{d[col]}</TD>", pv, o is not None and same(d[col], pv))
            if ecol_hi and o is not None:
                rec(name, "J_ApJS_161_304_models.vot", loc, f"{ecol_hi} -> err_hi", f"<TD>{d[ecol_hi]}</TD>", val(o["err_hi"]), same(d[ecol_hi], val(o["err_hi"])))
                rec(name, "J_ApJS_161_304_models.vot", loc, f"{ecol_lo} -> err_lo", f"<TD>{d[ecol_lo]}</TD>", val(o["err_lo"]), same(d[ecol_lo], val(o["err_lo"])))
        # clusters
        cr = [(l2, c) for l2, c in CROWS if c["Cluster"] == mv_name]
        if len(cr) != 1:
            surprises.append(f"{name}: {len(cr)} rows in clusters.vot"); continue
        l2, c = cr[0]
        loc2 = f"clusters.vot line {l2} (recno {c['recno']}, {mv_name})"
        o = bar.get("BC03 + Chabrier disk IMF")
        rec(name, "J_ApJS_161_304_clusters.vot", loc2, "(M/L)1", f"<TD>{c['(M/L)1']}</TD>", None if o is None else o["value"], o is not None and same(c["(M/L)1"], o["value"]))
        rec(name, "J_ApJS_161_304_clusters.vot", loc2, "e_(M/L)1 -> err_lo", f"<TD>{c['e_(M/L)1']}</TD>", None if o is None else o["err_lo"], o is not None and same(c["e_(M/L)1"], o["err_lo"]))
        rec(name, "J_ApJS_161_304_clusters.vot", loc2, "e_(M/L)1 -> err_hi", f"<TD>{c['e_(M/L)1']}</TD>", None if o is None else o["err_hi"], o is not None and same(c["e_(M/L)1"], o["err_hi"]))
        if set(bar) - {"R_Sun (horizontal branch)", "M_V,t", "BC03 + Chabrier disk IMF",
                       *[f"McLaughlin & van der Marel 2005 King fit: {p}" for p in ("W0/gamma", "r0", "Rh", "Dist")]}:
            surprises.append(f"{name}: unexpected baryonic parameters {set(bar)}")
        # arithmetic
        if mvt is not None and rs is not None:
            Lv = 10 ** (-0.4 * (mvt - 4.85))
            Rh = 10 ** float(d["Rh"]) * rs / float(d["Dist"])
            ml = float(c["(M/L)1"])
            pl, pr, pm = float(m["x_gc_baumgardt_l_v"]), float(m["x_gc_baumgardt_r_h_pc"]), float(m["x_gc_baumgardt_ml_v"])
            arith.append(dict(cluster=name, Lv=Lv, pLv=pl, okL=abs(pl / Lv - 1) <= 1e-9,
                              Rh=Rh, pRh=pr, okR=abs(pr / Rh - 1) <= 1e-9, ml=ml, pml=pm, okM=(pm == ml),
                              formula=f"10^{d['Rh']} x {rs} / {d['Dist']}"))
    return records, surprises, arith, order

if __name__ == "__main__":
    records, surprises, arith, order = main()
    import pickle
    pickle.dump((records, surprises, arith, order), open(sys.argv[1], "wb"))
    n = len(records); bad = [r for r in records if r["agree"] != "agree"]
    print("checked", n, "disagree", len(bad))
    for b in bad: print(b)
    print("surprises:"); [print(" ", s) for s in surprises]
    print("arith fails:", [a for a in arith if not (a["okL"] and a["okR"] and a["okM"])], len(arith))
