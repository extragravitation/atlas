import pickle, csv, sys, collections, hashlib
D = sys.argv[1]
PKG = "/home/claude/atlas/data/packages/aeg-d-gc-baumgardt/v1/"
rec, sur, ar, order = pickle.load(open(D + "out.pkl", "rb"))

for r in rec:
    if r["quoted"].startswith("(blank)"):
        r["quoted"] = r["quoted"].replace("(blank)", f"(blank; {r['cluster']} block)", 1)

def fmt(v):
    if v is None: return "(missing)"
    f = float(v)
    return repr(int(f)) if f.is_integer() and abs(f) > 5 and "NStar" else repr(f)

with open(PKG + "checks/second_reading.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["cluster", "source_file", "location", "quantity", "quoted", "package_value", "agree"])
    for r in rec:
        w.writerow([r["cluster"], r["source_file"], r["location"], r["quantity"], r["quoted"],
                    "" if r["package_value"] is None else repr(float(r["package_value"])), r["agree"]])

def sha(p):
    return hashlib.sha256(open(PKG + p, "rb").read()).hexdigest()[:16]

n = len(rec); bad = [r for r in rec if r["agree"] != "agree"]
byfile = collections.Counter(r["source_file"] for r in rec)
badfile = collections.Counter(r["source_file"] for r in bad)
nbins = sum(1 for r in rec if r["quantity"].endswith("<r> [arcsec]"))
arith_ok = all(a["okL"] and a["okR"] and a["okM"] for a in ar)
maxL = max(abs(a["pLv"] / a["Lv"] - 1) for a in ar)
maxR = max(abs(a["pRh"] / a["Rh"] - 1) for a in ar)

L = []
L.append("# Second reading: aeg-d-gc-baumgardt v1\n")
L.append("**Reader.** An independent agent session (Claude) with no access to the package's conversion code: "
         "`convert.py`, `analysis.py`, `sources_io.py`, `reproduction/*.py` and the pipeline directory were not imported or read. "
         "All parsers were written from scratch for this reading.  ")
L.append("**Date.** 2026-10-30  ")
L.append("**Scope.** Every input number entering the 64 plotted measurements (`plotted == \"true\"` in `tables/measurements.ecsv`).\n")
L.append("## Method\n")
L.append("- `source/veldis.html`: every `<td>` cell was read with a regular expression, line by line; cells were grouped seven at a time "
         "(Cluster, <r>, NStar, sigma, dsigma_Up, dsigma_Low, Type), skipping the `&nbsp;` separator rows; a blank name cell inherits the "
         "cluster name from the start of its block. Result: 2095 rows, 765 of Type RV, 155 clusters.")
L.append("- `source/mwgc.dat`: the three \"ID\" header lines delimit the parts. In Parts I and II the data lines (starting with a space and a "
         "non-space character) up to the `____` rule were read; the cluster ID is characters 1-12; `R_Sun` and `M_V,t` were cut as fixed-width "
         "fields aligned to their header labels, with an assertion that the character on each side of the field is a space. 157 clusters per part.")
L.append("- `source/mvdm05/*.vot`: raw XML read with regular expressions (FIELD names in order, then one `<TR>` per line). King row = "
         "`Mod == \"K\"` and `Cluster == \"MW-\" + name without spaces, upper case` (\"Ter N\" -> \"MW-TERZANN\", Harris \"Terzan N\").")
L.append("- Package tables were read with `astropy.table.Table.read(..., format=\"ascii.ecsv\")`. For each plotted measurement, each "
         "`observed_from` bin was matched to the source RV row of the same cluster with the same `<r>`; every source RV row of the cluster was "
         "then required to be matched (completeness in both directions). Baryonic inputs were identified by `x_gc_baumgardt_parameter`.")
L.append("- Comparison: `float(source string) == float(package value)` (exact). Units were checked for sigma (km / s) and R_Sun (kpc).")
L.append("- Beyond the brief, the King-fit upper and lower errors (`E_`/`e_` columns, VizieR convention: `E_` = upper, `e_` = lower) were "
         "compared with the package's `err_hi`/`err_lo` for W0/gamma, r0 and Rh; `e_(M/L)1` was compared with both `err_lo` and `err_hi`.")
L.append("- Arithmetic, from this reading's own source values: L_V = 10^(-0.4 (M_V,t - 4.85)); R_h = 10^Rh x R_Sun(Harris) / Dist(MvdM); "
         "compared with `x_gc_baumgardt_l_v`, `x_gc_baumgardt_r_h_pc` (relative tolerance 1e-9) and `x_gc_baumgardt_ml_v` vs (M/L)1 (exact).")
L.append("- Negative control: two values were perturbed in memory (an err_hi of 0.72 -> 0.73, an M_V,t of -6.67 -> -6.68); both were "
         "reported as DISAGREE, so the comparison can fail.")
L.append(f"- Source file SHA-256 (first 16 hex) as read: veldis.html `{sha('source/veldis.html')}`, mwgc.dat `{sha('source/mwgc.dat')}`, "
         f"models.vot `{sha('source/mvdm05/J_ApJS_161_304_models.vot')}`, clusters.vot `{sha('source/mvdm05/J_ApJS_161_304_clusters.vot')}`.\n")
L.append("## Summary\n")
L.append("| Source file | Numbers checked | Agree | Disagree |")
L.append("|---|---:|---:|---:|")
for f in ["veldis.html", "mwgc.dat", "J_ApJS_161_304_models.vot", "J_ApJS_161_304_clusters.vot"]:
    L.append(f"| {f} | {byfile[f]} | {byfile[f]-badfile[f]} | {badfile[f]} |")
L.append(f"| **Total** | **{n}** | **{n-len(bad)}** | **{len(bad)}** |\n")
L.append(f"- Clusters: 64 plotted, all matched by name in all four source files. Dispersion bins: {nbins} (5 numbers each). "
         "Every package bin is in the source; every source RV bin of these 64 clusters is in the package.")
L.append(f"- Of the {n} numbers, 384 are the extra King-fit error columns and 64 are the repeat comparison of e_(M/L)1 with err_hi; "
         f"the numbers named in the brief are {n-448}.")
L.append(f"- Arithmetic: {'PASS' if arith_ok else 'FAIL'} for all 64 (largest relative difference: L_V {maxL:.1e}, R_h {maxR:.1e}; "
         "M/L exact in all 64).")
L.append(f"- Result: **{'PASS' if not bad and not sur and arith_ok else 'FAIL'}**.\n")
L.append("## Per cluster\n")
L.append("Format: quantity | quoted source text | location | package value | result. "
         "Veldis quotes are `Cluster | <r> | NStar | sigma | dsigma_Up | dsigma_Low | Type`; a blank Cluster cell is shown as `(blank; NAME block)`.\n")
A = {a["cluster"]: a for a in ar}
by = collections.defaultdict(list)
for r in rec: by[r["cluster"]].append(r)
for c in order:
    L.append(f"### {c}\n")
    for r in by[c]:
        pv = "(missing)" if r["package_value"] is None else repr(float(r["package_value"]))
        L.append(f"- {r['quantity']} | `{r['quoted']}` | {r['source_file']} {r['location'].replace(r['source_file']+' ','')} | {pv} | {r['agree']}")
    a = A[c]
    L.append(f"- arithmetic L_V = {a['Lv']:.10g} vs {a['pLv']:.10g} | {'agree' if a['okL'] else 'DISAGREE'}; "
             f"R_h = {a['formula']} = {a['Rh']:.10g} pc vs {a['pRh']:.10g} | {'agree' if a['okR'] else 'DISAGREE'}; "
             f"M/L {a['ml']} vs {a['pml']} | {'agree' if a['okM'] else 'DISAGREE'}\n")
L.append("## Disagreements and how resolved\n")
if bad or sur or not arith_ok:
    for r in bad:
        L.append(f"- {r['cluster']} {r['quantity']}: source `{r['quoted']}` vs package {r['package_value']}. Resolution: open, for the maintainer.")
    for s in sur:
        L.append(f"- {s}. Resolution: open, for the maintainer.")
else:
    L.append("None. No number disagreed, no bin was missing in either direction, and all arithmetic checks passed.\n")
L.append("## Observations outside the pass/fail count\n")
L.append("- The introduction of `veldis.html` says the table holds profiles of 156 clusters; this reading finds 155 distinct cluster names "
         "in the table (157 `<b>` elements, two of which are the reference-list headings). This does not affect the 64 plotted clusters.")
open(PKG + "SECOND_READING.md", "w").write("\n".join(L) + "\n")
print(n, len(bad), arith_ok, maxL, maxR)
