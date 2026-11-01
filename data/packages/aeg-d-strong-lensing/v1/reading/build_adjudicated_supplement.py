"""Build adjudicated_supplement.csv from the two part-S readings (GAS_AND_SUPPLEMENT_BRIEF.md v2).

Adjudicator: Claude, 2026-11-01. The readings are not edited. Every value written here either agrees
between readers A and B (checked by this script, which stops on any disagreement) or was read at
source by the adjudicator (rows marked so in `settled_by`). Nothing is computed from lens values:
the script only copies printed numbers. Column format = adjudicated_inputs.csv.

Usage: python -I build_adjudicated_supplement.py   (run from this folder)
"""
import csv
import re

A = list(csv.DictReader(open("readings/reader-a-supplement.csv", encoding="utf-8")))
B = list(csv.DictReader(open("readings/reader-b-supplement.csv", encoding="utf-8")))
I = list(csv.DictReader(open("adjudicated_inputs.csv", encoding="utf-8")))
COLS = ["scope", "system", "record", "quantity", "value", "err_minus", "err_plus", "unit", "form",
        "location", "url", "status", "settled_by", "note"]
out = []


def sid(s):
    return re.sub(r"\s", "", re.sub(r"^SDSS\s*", "", s.replace("−", "-")))


def row(**k):
    out.append({c: k.get(c, "") for c in COLS})


R13_URL = "https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/A+A/501/461/lens"
R7_URL = "https://content.cld.iop.org/journals/0004-637X/705/2/1099/revision1/apj326624t4_ascii.txt"
AGREE = "both readers agree; adjudicator checked against source 2026-11-01"

# ---- 1. R29 cosmology ----
for q, v, u, n in (("H0", "70.4", "km s-1 Mpc-1", "WMAP7 (Komatsu et al. 2011), 'used to calculate the lensing geometry'"),
                   ("Om", "0.272", "", ""),
                   ("OL", "0.728", "", "printed; = 1 - Om, so flat by D-075 item 4 (flag: flat_from_OL); the word 'flat' is not printed")):
    row(scope="MNELLS J0403-0239", system="(record)", record="R29", quantity=q, value=v, unit=u, form="linear",
        location="R29 §4 (Lensing mass and the IMF), para 2, arXiv v1 p.3", url="https://arxiv.org/abs/1803.07082",
        status="default", settled_by="both readers agree",
        note=("'H0 = 70.4 km s−1 Mpc−1 , Ωm = 0.272 and ΩΛ = 0.728'. " + n).strip())

# ---- 2. SNL-1 fallback inputs ----
S = "SNL-1 (ESO 286-G022)"
SYS = "ESO 286-G022 (SNL-1)"
U25, U26, U61 = "https://arxiv.org/abs/1503.02661", "https://arxiv.org/abs/1612.00065", "https://arxiv.org/abs/1709.01931"
# R61: next-ranked eligible stellar-mass record under the frozen ranking (see adjudication_gas.md §2.2).
row(scope=S, system=SYS, record="R61", quantity="L_in_aperture", value="2.52", err_minus="0.04", err_plus="0.04",
    unit="1e10 Lsun (F814W)", form="linear", location="R61 Table 1 'LF814W (≤ Rap)', column SNL-1", url=U61,
    status="fallback_record candidate (D-075 item 2; JvH to confirm rank)",
    settled_by="adjudicator read at source (one reading; outside the part-S brief): needs a second reading",
    note="inside R_ap = 2.38 arcsec (= R25 half-separation); 'extinction and band-shifting corrected'; same aperture as R61's lensing mass")
row(scope=S, system=SYS, record="R61", quantity="ML_stellar_pop", value="2.75", unit="Msun/Lsun (F814W)", form="linear",
    location="R61 §5, SNL-1 paragraph", url=U61, status="fallback_record candidate (D-075 item 2; JvH to confirm rank)",
    settled_by="adjudicator read at source (one reading; outside the part-S brief): needs a second reading",
    note="'combined with the converted Υref of 2.75 (Newman et al. 2017)': R26's Kroupa SPS M/L converted to F814W with ezgal; no error printed: flag no_uncertainty")
row(scope=S, system=SYS, record="R61", quantity="aperture", value="2.38", unit="arcsec", form="linear",
    location="R61 Table 1 'Fiducial aperture, Rap'", url=U61, status="fallback_record candidate (D-075 item 2)",
    settled_by="already adjudicated (adjudicated_inputs.csv, R61 aperture)", note="'SLC15, SINFONI–based'")
# R26
r26 = [("L_in_aperture", "1.62", "0.05", "0.05", "1e10 Lsun (r)", "R26 Table 1 'Lr,Ein' (VizieR J/ApJ/845/157 table1 Lr)",
        "inside θEin = 2.38 arcsec ('Denoted REin by S15'); SDSS r from LDSS-3 imaging; 'distance error not included'; R26 states no cosmology (adopts S15 distances)"),
       ("ML_stellar_pop", "3.93", "0.20", "0.20", "Msun/Lsun (r)", "R26 Table 1 '(M*/Lr)MW' (VizieR (M/Lr)MW)",
        "SPS fit to IMACS spectra with a fixed Kroupa (2001) IMF; IMF-free variants printed, never default (D-063 item 1)"),
       ("aperture", "2.38", "", "", "arcsec", "R26 Table 1 θEin", "luminosity aperture = R25 REin (half the image separation)"),
       ("aperture", "2.2", "", "", "arcsec", "R26 §2.1 (IMACS extraction), last sentence",
        "spectroscopic (M/L) aperture radius; §6.1: 'these radii are matched within ≤ 8%'; flag: ML_aperture_differs (<= 8%)"),
       ("imf", "Kroupa (2001)", "", "", "", "R26 §5", "'(M∗/Lr)MW is inferred from SPS modeling assuming a fiducial Kroupa (2001) IMF'"),
       ("pop_model", "SPS models descended from CvD12 (MIST isochrones, IRTF library)", "", "", "", "R26 §6 para 1",
        "'We use models that are descended from those presented by CvD12'"),
       ("bands", "SDSS r (LDSS-3 imaging); IMACS spectra for M/L", "", "", "", "R26 §2.4, §3", "")]
for q, v, em, ep, u, loc, n in r26:
    row(scope=S, system=SYS, record="R26", quantity=q, value=v, err_minus=em, err_plus=ep, unit=u,
        form="linear" if u else "", location=loc, url=U26, status="fallback alternative (rank 2 after R61)",
        settled_by="both readers agree", note=n)
row(scope=S, system=SYS, record="R26", quantity="mstar", location="R26 Table 1", url=U26, status="not printed",
    settled_by="both readers agree", note="no population stellar mass printed; L x M/L route only (D-075 item 3, flag mstar_from_L_times_ML)")
# R25
r25 = [("L_in_aperture", "4.3", "0.1", "0.1", "1e10 Lsun (J)", "R25 Table 2 'LEin', column SNL-1",
        "2MASS J inside REin = 2.38 arcsec; 'assumes M⊙,J = 3.71 as in Maraston (2005)'"),
       ("ML_stellar_pop", "1.47", "0.12", "0.12", "Msun/Lsun (J)", "R25 Table 3(a) Υref; §4.2",
        "Maraston 2005, Kroupa, ASSUMED age 10 ± 1 Gyr, solar Z (same for all three lenses): an assumed-population M/L (D-063 item 1, carried as an assumption range)"),
       ("ML_stellar_pop", "1.46", "0.18", "0.18", "Msun/Lsun (J)", "R25 Table 3(d) Υref",
        "alternative: ages fitted to 6dF spectra with CvD12 models"),
       ("aperture", "2.38", "", "", "arcsec", "R25 Table 2 REin", "'0.5×image-separation for SNL-1,2'"),
       ("aperture", "1.47", "", "", "kpc", "R25 Table 2 rEin", "same aperture in kpc, R25's cosmology (WMAP7)"),
       ("imf", "Kroupa (2001)", "", "", "", "R25 §4.2", "'here taken as that of Kroupa (2001)'"),
       ("pop_model", "Maraston (2005) [Table 3(a)]; CvD12 [Table 3(d), alternative]", "", "", "", "R25 §4.2; Table 3", ""),
       ("bands", "2MASS J", "", "", "", "R25 §4.1", "'we use J-band photometry from 2MASS (Jarrett et al. 2000)'")]
for q, v, em, ep, u, loc, n in r25:
    row(scope=S, system=SYS, record="R25", quantity=q, value=v, err_minus=em, err_plus=ep, unit=u,
        form="linear" if u and q != "imf" else "", location=loc, url=U25, status="fallback alternative (rank 3)",
        settled_by="both readers agree", note=n)
row(scope=S, system=SYS, record="R25", quantity="mstar", location="R25 Tables 2–3; §4.1–4.2", url=U25, status="not printed",
    settled_by="both readers agree", note="R25 prints L_Ein and Υref, not a stellar mass")

# ---- 3. R13 totals and R_e (z_l < 0.30) ----
bA = {(sid(x["system_id"]), x["quantity"], "Sal" if "Salpeter" in x["note"] else "Cha"): x
      for x in A if x["record"] == "R13" and x["quantity"] in ("mstar", "R_e")}
bB = {(sid(x["system_id"]), x["quantity"], "Sal" if "Sal" in x["location"] else "Cha"): x
      for x in B if x["record"] == "R13" and x["quantity"] in ("mstar", "R_e")}
zB = {sid(x["system_id"]): x["value"] for x in B if x["record"] == "R13" and x["quantity"] == "z_l"}
assert set(bA) == set(bB)
for k in sorted(bA):
    a, b = bA[k], bB[k]
    assert (a["value"], a["err_minus"], a["err_plus"]) == (b["value"], b["err_minus"], b["err_plus"]), k
    s, q, imf = k
    zl = zB[s]
    if q == "mstar":
        row(scope="SLACS V-modelled lenses", system=s, record="R13", quantity="mstar_total", value=a["value"],
            err_minus=a["err_minus"], err_plus=a["err_plus"], unit="1e10 Msun", form="linear",
            location=f"VizieR J/A+A/501/461/lens M{imf if imf == 'Sal' else 'Cha'}BC (e_ lower, E_ upper) = paper Table 4",
            url=R13_URL, status="profile-step check input (D-075 item 5); range top" if imf == "Sal" else "profile-step check input (D-075 item 5)",
            settled_by=AGREE,
            note=f"TOTAL (not inside R_E); {'Salpeter' if imf == 'Sal' else 'Chabrier'}, BC03; SDSS ugriz modelMag SED fit; R13 z_l = {zl}")
    elif imf == "Cha":
        row(scope="SLACS V-modelled lenses", system=s, record="R13", quantity="R_e", value=a["value"], unit="arcsec",
            form="linear", location="VizieR J/A+A/501/461/lens thetae = paper Table 1 θe", url=R13_URL,
            status="profile-step check input (D-075 item 5)", settled_by=AGREE,
            note=f"de Vaucouleurs fit on F814W, printed by R13 citing Bolton et al. 2008a (= R5); R5's own table not opened; R13 z_l = {zl}")

# ---- 4. R7 log M_E (z_l < 0.30) ----
slacs = {sid(x["system"]) for x in I if x["record"] == "R5" and x["quantity"] == "z_l" and float(x["value"]) < 0.30}
bA = {sid(x["system_id"]): x for x in A if x["record"] == "R7" and x["quantity"] == "M_E"}
bB = {sid(x["system_id"]): x for x in B if x["record"] == "R7" and x["quantity"] == "M_E"}
assert set(bA) == set(bB)
for s in sorted(bA):
    a, b = bA[s], bB[s]
    va, vb = a["value"].strip(), b["value"].strip().replace("...", "")
    assert va == vb, s
    zl = re.search(r"z_lens = ([\d.]+)", a["note"]).group(1)
    rE = re.search(r"r_Ein = ([\d.]+) kpc", a["note"])
    inset = s in slacs
    row(scope="SLACS V-modelled lenses" if inset else "SLACS (R7 Table 4, not in the SLACS V adjudicated set)",
        system=s, record="R7", quantity="M_E", value=va, unit="Msun", form="log10",
        location="R7 Table 4 log[M_Ein/M_sun] (IOP ascii apj326624t4); z_lens from Table 3", url=R7_URL,
        status=("not printed ('...')" if not va else
                ("reported check (§4 formula; REPRODUCTION 'Reported, not pass/fail')" if inset else "record-only")),
        settled_by=AGREE + " (IOP ascii SHA-256 7c8a3297…)",
        note=f"no error printed (flag no_uncertainty); R7 z_lens = {zl}" + (f"; r_Ein = {rE.group(1)} kpc (printed)" if rE else ""))
for q, v, n in (("Om", "0.3", ""), ("OL", "0.7", "= 1 - Om: flat by D-075 item 4"),
                ("H0", "70", "printed as 'h = 0.7' (H0 = 100 h km s-1 Mpc-1 is the convention; flag: H0_from_h)")):
    row(scope="SLACS V-modelled lenses", system="(record)", record="R7", quantity=q, value=v,
        unit="km s-1 Mpc-1" if q == "H0" else "", form="linear", location="R7 §1 last para (arXiv:0911.2471v1)",
        url="https://arxiv.org/abs/0911.2471", status="default (for the R7 check)", settled_by="both readers agree",
        note=("'concordance cosmology with Ωm = 0.3 ΩΛ = 0.7 h = 0.7 is assumed'. " + n).strip())

# ---- 5. Salpeter conversions ----
row(scope="MNELLS J0403-0239", system="(record)", record="R29", quantity="salpeter_alpha", value="1.55", form="linear",
    location="R29 §4 para 1 (right column)", url="https://arxiv.org/abs/1803.07082", status="range top factor",
    settled_by="both readers agree",
    note="'a Salpeter IMF (Salpeter 1955), with more low mass stars, has α = 1.55'; relative to Kroupa ('α = 1 by definition'); Conroy et al. 2009 models via ezgal")
row(scope="MaNGA", system="(record)", record="R32", quantity="salpeter_alpha", value="1.65", form="linear",
    location="R32 §5 (Mass-to-light ratios) para 1", url="https://arxiv.org/abs/1911.06338", status="range top factor",
    settled_by="both readers agree; adjudicator read at source",
    note="printed 'α ≈ 1.65' (approximate: flag approx_printed); relative to Kroupa Υref (Conroy, Gunn & White 2009 via EzGal). The other §5 phrase is 'α & 1.6' in pdftotext; not used")
row(scope="Euclid NGC 6505", system="(record)", record="R30", quantity="chab_to_salp_factor", value="0.61", form="linear",
    location="R30 §3.1, Prospector paragraph (end)", url="https://arxiv.org/abs/2502.06505", status="range top factor",
    settled_by="both readers agree; adjudicator read at source",
    note="'rescale these quantities by dividing them with a constant factor of 0.61 and 0.63' (stellar mass, SFR); Salpeter = Chabrier / 0.61; FSPS via Prospector; no citation for the factor")
for rec, mp, url, loc, n in (
        ("R10", "Conroy, Gunn & White 2009 (arXiv:0809.4261v2)", "https://arxiv.org/abs/0809.4261", "whole text",
         "FSPS model paper cited by R9 for R10's masses; reference IMF Kroupa 2001; no Chabrier-to-Salpeter mass ratio printed"),
        ("R10", "Conroy & Gunn 2010 (arXiv:0911.3151v1)", "https://arxiv.org/abs/0911.3151", "whole text",
         "second FSPS paper cited by R9; no 'Salpeter' or 'Chabrier' in the text"),
        ("R20", "Bruzual & Charlot 2003 (arXiv:astro-ph/0309134v1)", "https://arxiv.org/abs/astro-ph/0309134", "§3.1, Fig. 4",
         "IMF effect shown only graphically (Fig. 4); returned-mass fractions at 10 Gyr (31% Salpeter, 48% Chabrier) are not a mass ratio. Not needed: R20 Table 7 prints its own Salpeter masses (already 'range top' in adjudicated_inputs.csv)")):
    row(scope="S4TM lenses" if rec == "R10" else "SL2S III sample", system="(record)", record=rec,
        quantity="chab_to_salp_ratio", value="not printed", location=f"{mp}: {loc}", url=url,
        status="not printed (model paper)", settled_by="both readers agree", note=n)

with open("adjudicated_supplement.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(out)
print(len(out), "rows")
