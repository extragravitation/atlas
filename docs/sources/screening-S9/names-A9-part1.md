# Screening S9 — cluster names in A9 records, part 1

Scope: cluster names and redshifts only, exactly as printed in each record's sample table. No mass, fraction, concentration, ratio, temperature or other result is recorded here.

Method: arXiv PDFs were downloaded with curl from `https://arxiv.org/pdf/<id>` (the only source host reachable from this session; ar5iv, export.arxiv.org, CDS/VizieR, `dc.g-vo.org` downloads and ADS were refused by the proxy) and converted with `pdftotext -layout`. Names and redshifts were copied from the extracted table text; the XXL table (C18c) was parsed by a script and the row count checked against the stated sample size. One record (C18d) has no arXiv version that could be found; its table was read through the WebFetch tool from the Durham repository copy of the published paper, which returns a model-mediated transcription, not raw text (see C18d).

Conventions: "—" separates name and redshift. Names keep the printed spelling, spacing and minus sign (− U+2212 where the source uses it). Footnote markers printed on a redshift are kept and explained. "Below 0.30" means printed z < 0.30.

Caveats, stated once: pdftotext can drop or merge characters in typeset tables (e.g. spacing inside names). Every list below was read from the extracted text, not from the rendered page image. arXiv versions can differ from the journal version; the version read is given for each record.

| Record | Clusters named | Below z = 0.30 |
|---|---|---|
| C1a 2014ApJ...795..163U | 20 | 5 |
| C1b 2016ApJ...821..116U | 20 | 5 |
| C1c 2015ApJ...801...44Z | 25 | 6 |
| C3a 2014ApJ...794..136D | 25 | 6 |
| C6a 2010MNRAS.404..325R | 20 | 20 |
| C6b 2013ApJ...769L..35O | 0 (list not printed) | — |
| C6c 2016MNRAS.461.3794O | 50 | 50 |
| C7a 2012MNRAS.420.3213O | 27 rows (28 clusters; one field holds two cores) | 1 |
| C7b 2020ApJS..247...12S | 37 | 4 |
| C12d 2007A&A...470..449B | 11 | 11 |
| C12e 2012A&A...546A..79I | 8 (7 new + 1 from Paper I) | 0 |
| C15a 2006ApJ...652..232H | 14 | 7 |
| C18c 2020ApJ...890..148U | 136 | 66 |
| C18d 2019MNRAS.488.1704K | 39 (42 table rows) | 24 |

---

## C1a — Umetsu et al. 2014, ApJ 795, 163 (2014ApJ...795..163U), "CLASH: Weak-lensing shear-and-magnification analysis of 20 galaxy clusters"

- URL read: https://arxiv.org/pdf/1404.1375 (arXiv:1404.1375v3), SHA-256 c39cc608f018fffcb2add764962f7aaae31aeccf9d8bf53e52edb50a6a93d27a
- Table read: Table 1, "Cluster sample", columns Cluster and z_l.

X-ray Selected:
- Abell 383 — 0.187
- Abell 209 — 0.206
- Abell 2261 — 0.224
- RXJ2129.7+0005 — 0.234
- Abell 611 — 0.288
- MS2137-2353 — 0.313
- RXJ2248.7-4431 — 0.348
- MACSJ1115.9+0129 — 0.352
- MACSJ1931.8-2635 — 0.352
- RXJ1532.9+3021 — 0.363
- MACSJ1720.3+3536 — 0.391
- MACSJ0429.6-0253 — 0.399
- MACSJ1206.2-0847 — 0.440
- MACSJ0329.7-0211 — 0.450
- RXJ1347.5-1145 — 0.451
- MACSJ0744.9+3927 — 0.686

High Magnification:
- MACSJ0416.1-2403 — 0.396
- MACSJ1149.5+2223 — 0.544
- MACSJ0717.5+3745 — 0.548
- MACSJ0647.7+7015 — 0.584

Count: 20. Below z = 0.30: 5 (Abell 383, Abell 209, Abell 2261, RXJ2129.7+0005, Abell 611).

## C1b — Umetsu et al. 2016, ApJ 821, 116 (2016ApJ...821..116U), "CLASH: Joint analysis of strong-lensing, weak-lensing shear and magnification data for 20 galaxy clusters"

- URL read: https://arxiv.org/pdf/1507.04385 (arXiv:1507.04385v4), SHA-256 317abf5549022c28774a4393ebab7e11fd590b9699a2d57ee4da3282ae2b21de
- Table read: Table 1, "Properties of the cluster sample", columns Cluster and z_l.

X-ray Selected:
- Abell 383 — 0.187
- Abell 209 — 0.206
- Abell 2261 — 0.224
- RXJ2129.7+0005 — 0.234
- Abell 611 — 0.288
- MS2137-2353 — 0.313
- RXJ2248.7-4431 — 0.348
- MACSJ1115.9+0129 — 0.352
- MACSJ1931.8-2635 — 0.352
- RXJ1532.9+3021 — 0.363
- MACSJ1720.3+3536 — 0.391
- MACSJ0429.6-0253 — 0.399
- MACSJ1206.2-0847 — 0.440
- MACSJ0329.7-0211 — 0.450
- RXJ1347.5-1145 — 0.451
- MACSJ0744.9+3927 — 0.686

High Magnification:
- MACSJ0416.1-2403 — 0.396
- MACSJ1149.5+2223 — 0.544
- MACSJ0717.5+3745 — 0.548
- MACSJ0647.7+7015 — 0.584

Count: 20 (same names and redshifts as C1a). Below z = 0.30: 5.

## C1c — Zitrin et al. 2015, ApJ 801, 44 (2015ApJ...801...44Z), "Hubble Space Telescope combined strong and weak lensing analysis of the CLASH sample"

- URL read: https://arxiv.org/pdf/1411.1414 (arXiv:1411.1414v4), SHA-256 e314fd59cd0e57717f2b7fb9ef42477f108e3faf6147cdff9f03cec2c8d663bc
- What was read: this paper has **no sample table with redshifts**. Its Table 1 ("Summary of Analysis Results") lists abbreviated names only (A209, A383, A611, A1423, A2261, CL1226, M0329, M0416, M0429, M0647, M0717, M0744, M1115, M1149, M1206, M1311, M1423, RXJ1532, M1720, M1931, M2129, MS2137, RXJ1347, RXJ2129, RXJ2248; each with LTM/NFW model suffixes) and no z column; the text says cluster redshifts are mainly taken from Postman et al. (2012). The list below uses the full names printed as the Section 4.x headings and the redshift printed in the first sentence of each section. These in-text redshifts are rounded differently from the CLASH tables (e.g. 0.21, 0.29) and are recorded as printed.

- Abell 209 — 0.21 (§4.1)
- Abell 383 — 0.189 (§4.2)
- Abell 611 — 0.29 (§4.3)
- Abell 1423 — 0.213 (§4.4)
- Abell 2261 — 0.225 (§4.5)
- CL J1226.9+3332 — 0.89 (§4.6)
- MACS J0329.6-0211 — 0.45 (§4.7)
- MACS J0416.1-2403 — 0.40 (§4.8)
- MACS J0429.6-0253 — 0.399 (§4.9)
- MACS J0647.7+7015 — 0.591 (§4.10)
- MACS J0717.5+3745 — 0.546 (§4.11; printed "M0717 (0.546)")
- MACS J0744.8+3927 — 0.698 (§4.12)
- MACS J1115.9+0129 — 0.352 (§4.13)
- MACS J1149.5+2223 — 0.544 (§4.14)
- MACS J1206.2-0847 — 0.44 (§4.15)
- MACS J1311.0-0311 — 0.494 (§4.16)
- MACS J1423.8+2404 — 0.545 (§4.17)
- RXJ1532.9+3021 — no z printed in §4.18 opening (not read elsewhere in this paper)
- MACS J1720.2+3536 — 0.387 (§4.19)
- MACS J1931.8-2635 — 0.352 (§4.20)
- MACS J2129.4-0741 — 0.59 (§4.21)
- MS 2137-2353 — 0.313 (§4.22)
- RXJ1347.5-1145 — 0.45 (§4.23)
- RXJ2129.7+0005 — 0.234 (§4.24)
- RXC J2248.7-4431 — 0.348 (§4.25)

Count: 25. Below z = 0.30: 6 (Abell 209, Abell 383, Abell 611, Abell 1423, Abell 2261, RXJ2129.7+0005). The sample is the same 25 clusters as C3a Table 1.

## C3a — Donahue et al. 2014, ApJ 794, 136 (2014ApJ...794..136D), "CLASH-X: A comparison of lensing and X-ray techniques for measuring the mass profiles of galaxy clusters"

- URL read: https://arxiv.org/pdf/1405.7876 (arXiv:1405.7876v3), SHA-256 b0054d2f5361054253d184dc126c2a924f41b309e42377ef2bddf5c151a3ce7a. Cross-checked against https://ar5iv.arxiv.org/html/1405.7876 via WebFetch (same names and z).
- Table read: Table 1, "CLASH Cluster Data", columns Name and z.

- Abell 209 — 0.206
- Abell 383 — 0.187
- MACSJ0329-02 — 0.450
- MACSJ0429-02 — 0.399
- MACSJ0744+39 — 0.686
- Abell 611 — 0.288
- MACSJ1115+01 — 0.355
- Abell1423 — 0.213
- MACSJ1206-08 — 0.439
- CLJ1226+3332 — 0.890
- MACSJ1311-03 — 0.494
- RXJ1347-1145 — 0.451
- MACSJ1423+24 — 0.545
- MACSJ1532+30 — 0.362
- MACSJ1720+35 — 0.387
- Abell 2261 — 0.224
- MACSJ1931-26 — 0.352
- RXJ2129+0005 — 0.234
- MS2137-2353 — 0.313
- RXCJ2248-4431 — 0.348
- MACSJ0416-24 — 0.397f (footnote f: "Redshift for MACS0416-24 from Postman et al. (2012) is updated by Ebeling et al. (2014).")
- MACSJ0647+70 — 0.584
- MACSJ0717+37 — 0.548
- MACSJ1149+22 — 0.544
- MACSJ2129-07 — 0.570

Count: 25. Below z = 0.30: 6 (Abell 209, Abell 383, Abell 611, Abell1423, Abell 2261, RXJ2129+0005).

## C6a — Richard et al. 2010, MNRAS 404, 325 (2010MNRAS.404..325R), "LoCuSS: First results from strong-lensing analysis of 20 massive galaxy clusters at z = 0.2"

- URL read: https://arxiv.org/pdf/0911.3302 (arXiv:0911.3302v2), SHA-256 b312fd545c0f42975e30e4c184867ee0df75f0cc1e94dd97a97ebe5c1ebfd811. VizieR J/MNRAS/404/325 could not be reached (CDS and dc.g-vo.org refused by the proxy).
- Tables read: Table 1 ("Optical and near-infrared imaging observations of the new strong-lensing LoCuSS clusters") and Table 2 ("Extended sample of 10 previously published spectroscopically-confirmed strong-lensing LoCuSS clusters"), columns Cluster and z. Together they make the 20.

Table 1:
- A 521(a) — 0.2475 (a: also known as RXC J0454.1−1014)
- A 611 — 0.2850
- A 773 — 0.2170
- A 868 — 0.1535
- Z2701(b) — 0.2140 (b: also known as ZwCl 0949.6+5207)
- A 1413 — 0.1427
- A 1835 — 0.2528
- A 2204 — 0.1524
- RX J1720(c) — 0.1640 (c: RX J1720.1+2638)
- RX J2129(d) — 0.2350 (d: RX J2129.6+0005)

Table 2:
- A 68 — 0.2546
- A 383 — 0.1883
- A 963 — 0.2050
- A 1201 — 0.1688
- A 1689 — 0.1832
- A 1703 — 0.2800
- A 2218 — 0.1710
- A 2219 — 0.2281
- A 2390 — 0.2329
- A 2667 — 0.2264

Count: 20. Below z = 0.30: 20.

## C6b — Okabe et al. 2013, ApJ 769, L35 (2013ApJ...769L..35O), "LoCuSS: The mass density profile of massive galaxy clusters at z = 0.2"

- URL read: https://arxiv.org/pdf/1302.2728 (arXiv:1302.2728v2), SHA-256 3e5c799abd257c72d11a255b0fc71f89bd86011cb72ab200ee0802711d160ba0
- What was read: the full text. **The list cannot be read from this record: it does not print the 50 cluster names or redshifts.** Its Table 1 ("Density Profile Models") and Table 2 give only stacked-fit results (not recorded). The text describes "an approximately mass-selected sample of 50 galaxy clusters" drawn from ROSAT All Sky Survey catalogs, and the Fig. 2 caption names one cluster, "ABELL 0141" (no redshift printed with it). The 50 names are printed in C6c Table 1 (below), but this paper does not say so in a table, so they are not attributed to C6b here.

Count: 0 named in a table (1 name in a figure caption). Below z = 0.30: not determinable from this record.

## C6c — Okabe & Smith 2016, MNRAS 461, 3794 (2016MNRAS.461.3794O), "LoCuSS: Weak-lensing mass calibration of galaxy clusters"

- URL read: https://arxiv.org/pdf/1507.04493 (arXiv:1507.04493v2), SHA-256 fada60842c6b7eaafdfca891866e2fb67973460b71e498e42076ee8ed0b7c0e1
- Table read: Table 1, "Cluster sample", columns Name and Redshift.

- ABELL2697 — 0.2320
- ABELL0068 — 0.2546
- ABELL2813 — 0.2924
- ABELL0115 — 0.1971
- ABELL0141 — 0.2300
- ZwCl0104.4+0048 — 0.2540
- ABELL0209 — 0.2060
- ABELL0267 — 0.2300
- ABELL0291 — 0.1960
- ABELL0383 — 0.1883
- ABELL0521 — 0.2475
- ABELL0586 — 0.1710
- ABELL0611 — 0.2880
- ABELL0697 — 0.2820
- ZwCl0857.9+2107 — 0.2347
- ABELL0750 — 0.1630
- ABELL0773 — 0.2170
- ABELL0781 — 0.2984
- ZwCl0949.6+5207 — 0.2140
- ABELL0901 — 0.1634
- ABELL0907 — 0.1669
- ABELL0963 — 0.2050
- ZwCl1021.0+0426 — 0.2906
- ABELL1423 — 0.2130
- ABELL1451 — 0.1992
- RXCJ1212.3-1816 — 0.2690
- ZwCl1231.4+1007 — 0.2290
- ABELL1682 — 0.2260
- ABELL1689 — 0.1832
- ABELL1758N — 0.2800
- ABELL1763 — 0.2279
- ABELL1835 — 0.2528
- ABELL1914 — 0.1712
- ZwCl1454.8+2233 — 0.2578
- ABELL2009 — 0.1530
- ZwCl1459.4+4240 — 0.2897
- RXCJ1504.1-0248 — 0.2153
- ABELL2111 — 0.2290
- ABELL2204 — 0.1524
- ABELL2219 — 0.2281
- RXJ1720.1+2638 — 0.1640
- ABELL2261 — 0.2240
- RXCJ2102.1-2431 — 0.1880
- RXJ2129.6+0005 — 0.2350
- ABELL2390 — 0.2329
- ABELL2485 — 0.2472
- ABELL2537 — 0.2966
- ABELL2552 — 0.2998
- ABELL2631 — 0.2779
- ABELL2645 — 0.2510

Count: 50. Below z = 0.30: 50.

## C7a — Oguri et al. 2012, MNRAS 420, 3213 (2012MNRAS.420.3213O), "Combined strong and weak lensing analysis of 28 clusters from the Sloan Giant Arcs Survey"

- URL read: https://arxiv.org/pdf/1109.2594 (arXiv:1109.2594v2), SHA-256 b93abee8aa266a04cdf819af08c6cb3c74f6330394d06a4584000543e347ee30
- Table read: Table 1, "Cluster sample and summary of Subaru/Suprime-cam imaging observations. The redshifts of the clusters are taken from Bayliss et al. (2011b).", columns Name and z.
- The table has 27 rows for 28 clusters: footnote c on SDSSJ1226+2149 says "This field includes two separate cluster cores, both of which act as strong lenses." The two cores are not given separate rows or redshifts in Table 1.

- SDSSJ0851+3331 — 0.370
- SDSSJ0915+3826 — 0.397
- SDSSJ0957+0509 — 0.448
- SDSSJ1004+4112 — 0.68
- SDSSJ1029+2623 — 0.584
- SDSSJ1038+4849 — 0.430
- SDSSJ1050+0017 — 0.60a
- RCS2J1055+5547 — 0.466
- SDSSJ1110+6459 — 0.659b
- SDSSJ1115+5319 — 0.466
- SDSSJ1138+2754 — 0.451
- SDSSJ1152+3313 — 0.362
- SDSSJ1152+0930 — 0.517
- SDSSJ1209+2640 — 0.561
- SDSSJ1226+2149c — 0.435
- A1703 — 0.277
- SDSSJ1315+5439 — 0.588d
- GHO132029+3155 — 0.308
- SDSSJ1329+2243 — 0.443d
- SDSSJ1343+4155 — 0.418
- SDSSJ1420+3955 — 0.607
- SDSSJ1446+3032 — 0.464
- SDSSJ1456+5702 — 0.484
- SDSSJ1531+3414 — 0.335
- SDSSJ1621+0607 — 0.342
- SDSSJ1632+3500 — 0.49a
- SDSSJ2111−0114 — 0.638

Footnotes: a "Photometric redshifts estimated from the SDSS data, as spectroscopic cluster redshifts are not available for these clusters." b "Based on the spectroscopy of the brightest cluster galaxy at Apache Point Observatory 3.5-meter telescope." c two cores (above). d "Based on the new spectroscopic observation with Gemini/GMOS conducted after the publication of Bayliss et al. (2011b)."

Count: 27 names (28 clusters per the paper). Below z = 0.30: 1 (A1703).

## C7b — Sharon et al. 2020, ApJS 247, 12 (2020ApJS..247...12S; VizieR 2020yCat..22470012S), "Strong lens models for 37 clusters of galaxies from the SDSS Giant Arcs Survey"

- URL read: https://arxiv.org/pdf/1904.05940 (arXiv:1904.05940v1, the only version served; may differ from the journal version), SHA-256 eb4e581c0ff6d2e1d3e1b4fe7c549292b9fef15528ae5b139bf717bfc9c58397. VizieR J/ApJS/247/12 could not be downloaded (CDS and dc.g-vo.org refused by the proxy).
- Table read: Table 3, "Cluster properties", columns Cluster and Redshift (Table 1, "HST-GO-13003 Observations", lists the same 37 names with no redshift). Redshifts are recorded with their printed uncertainty.

- SDSS J0004−0103 — 0.514±0.003
- SDSS J0108+0624 — 0.54778±0.0002
- SDSS J0146−0929 — 0.4469±0.00006
- SDSS J0150+2725 — 0.30619±0.00005
- SDSS J0333−0651 — 0.5729±0.0006
- SDSS J0851+3331 — 0.3689±0.0007
- SDSS J0915+3826 — 0.3961±0.0008
- SDSS J0928+2031 — 0.1920±0.0009
- SDSS J0952+3434 — 0.357±0.003
- SDSS J0957+0509 — 0.448±0.001
- SDSS J1002+2031 — 0.319±0.006
- SDSS J1038+4849 — 0.4308±0.0003
- SDSS J1050+0017 — 0.5931±0.0008
- SDSS J1055+5547 — 0.466±0.003
- SDSS J1110+6459 — 0.656±0.006
- SDSS J1115+1645 — 0.537
- SDSS J1138+2754 — 0.451±0.008
- SDSS J1152+0930 — 0.517±0.009
- SDSS J1152+3313 — 0.3612±0.0007
- SDSS J1156+1911 — 0.54547±0.00013
- SDSS J1207+5254 — 0.275±0.003
- SDSS J1209+2640 — 0.5606±0.0012
- SDSS J1329+2243 — 0.4427±0.0007
- SDSS J1336−0331 — 0.17637±0.00003
- SDSS J1343+4155 — 0.418±0.006
- SDSS J1420+3955 — 0.607±0.006
- SDSS J1439+1208 — 0.42734±0.00013
- SDSS J1456+5702 — 0.484±0.009
- SDSS J1522+2535 — 0.602±0.006
- SDSS J1527+0652 — 0.392±0.005
- SDSS J1531+3414 — 0.335±0.005
- SDSS J1604+2244 — 0.286±0.004
- SDSS J1621+0607 — 0.3429±0.0005
- SDSSJ1632+3500 — 0.466±0.006
- SDSS J1723+3411 — 0.44227±0.00009
- SDSS J2111−0114 — 0.6363±0.0009
- SDSS J2243−0935 — 0.447±0.005

Count: 37. Below z = 0.30: 4 (SDSS J0928+2031, SDSS J1207+5254, SDSS J1336−0331, SDSS J1604+2244).

## C12d — Bardeau et al. 2007, A&A 470, 449 (2007A&A...470..449B), "A lensing survey of X-ray luminous galaxy clusters at redshift z ~ 0.2. II: CFH12k weak lensing analysis and global correlations"

- URL read: https://arxiv.org/pdf/astro-ph/0703395 (arXiv:astro-ph/0703395v2), SHA-256 f6a55a803f0fd487fd499e8f7baa821727b5bade80314e6da59dc9bc6e4aa789
- Table read: Table 1, "Physical properties of the eleven clusters of the sample studied in this paper", columns Cluster and z.

- A 68 — 0.255
- A 209 — 0.206
- A 267 — 0.230
- A 383 — 0.187
- A 963 — 0.206
- A 1689 — 0.184
- A 1763 — 0.228
- A 1835 — 0.253
- A 2218 — 0.171
- A 2219 — 0.228
- A 2390 — 0.233

Count: 11. Below z = 0.30: 11.

## C12e — Israel et al. 2012, A&A 546, A79 (2012A&A...546A..79I), "The 400d Galaxy Cluster Survey weak lensing programme. II: Weak lensing study of seven clusters with MMT/Megacam"

- URL read: https://arxiv.org/pdf/1112.4444 (version stamp not printed in the extracted text), SHA-256 8e076ca015c51f516ca49bf95fa77347cfe6aaff8872e0f377bc35f1071f7438
- Tables read: Table 1 ("Specifications of the data sets for all eight clusters analysed so far ... CL 0030+2618 is the cluster analysed in Paper I") for names; Table 3 ("Additional parameters defining the 'default' cluster models", column (1) z_d) for redshifts.
- Note: the paper's own analysis is of seven clusters; CL 0030+2618 is printed in both tables but was analysed in Paper I.

- CL 0030+2618 — 0.50 (Paper I cluster)
- CL 0159+0030 — 0.39
- CL 0230+1836 — 0.80
- CL 0809+2811 — 0.40
- CL 1357+6232 — 0.53
- CL 1416+4446 — 0.40
- CL 1641+4001 — 0.46
- CL 1701+6414 — 0.45

Count: 8 printed (7 analysed in this paper). Below z = 0.30: 0.

## C15a — Hicks et al. 2006, ApJ 652, 232 (2006ApJ...652..232H), "Multiwavelength mass comparisons of the z~0.3 CNOC cluster sample"

- URL read: https://arxiv.org/pdf/astro-ph/0609334 (arXiv:astro-ph/0609334v3), SHA-256 4e02e6c4c389fbc79fe049bee060caf2d2b211395e39c18d53076398535e887b
- Table read: Table 1, "Cluster Sample", columns Cluster and z.

- Abell 2390 — 0.2279
- MS 0015.9+1609 — 0.5466
- MS 0302.7+1658 — 0.4246
- MS 0440.5+0204 — 0.1965
- MS 0451.5+0250 — 0.2010
- MS 0451.6-0305 — 0.5392
- MS 0839.8+2938 — 0.1928
- MS 0906.5+1110 — 0.1709
- MS 1006.0+1202 — 0.2605
- MS 1008.1-1224 — 0.3062
- MS 1358.4+6245 — 0.3290
- MS 1455.0+2232 — 0.2570
- MS 1512.4+3647 — 0.3726
- MS 1621.5+2640 — 0.4274

Count: 14. Below z = 0.30: 7 (Abell 2390, MS 0440.5+0204, MS 0451.5+0250, MS 0839.8+2938, MS 0906.5+1110, MS 1006.0+1202, MS 1455.0+2232).

## C18c — Umetsu et al., ApJ 890, 148 (bibcode as given in the task: 2021ApJ...890..148U; XXL c–M VizieR record 2021yCat..18900148U), "Weak-lensing analysis of X-ray-selected XXL galaxy groups and clusters with Subaru HSC data"

Note: the bibcode year was not checked against ADS (ADS unreachable); the arXiv PDF read carries the draft date 5 March 2020.

- URL read: https://arxiv.org/pdf/1909.10524 (arXiv:1909.10524v3), SHA-256 685cc4681cbcb0a4c83e17a5404e741d38157b23fd6d3d5ac30a7d71b06dbefe. VizieR J/ApJ/890/148 could not be downloaded (refused by the proxy).
- Table read: Table 2, "Cluster Properties and Weak-lensing Measurements", columns ID and z. Footnote a: "XLSSC cluster identifier (between 1 and 499 or between 500 and 999, for XXL-N or XXL-S, respectively)." The ID is printed as a bare three-digit number; it is recorded as printed (read as XLSSC <ID>). Rows were parsed by script from the extracted text: 136 rows found, no duplicate IDs, z range 0.031–1.033.

- 002 — 0.771
- 003 — 0.836
- 006 — 0.429
- 008 — 0.299
- 009 — 0.328
- 010 — 0.330
- 011 — 0.054
- 013 — 0.308
- 018 — 0.324
- 020 — 0.494
- 021 — 0.085
- 022 — 0.293
- 025 — 0.265
- 027 — 0.295
- 028 — 0.297
- 030 — 0.631
- 032 — 0.803
- 035 — 0.174
- 036 — 0.492
- 038 — 0.584
- 040 — 0.320
- 041 — 0.142
- 044 — 0.263
- 048 — 1.005
- 049 — 0.494
- 050 — 0.140
- 051 — 0.279
- 052 — 0.056
- 054 — 0.054
- 055 — 0.232
- 056 — 0.348
- 057 — 0.153
- 058 — 0.332
- 059 — 0.645
- 060 — 0.139
- 061 — 0.259
- 062 — 0.059
- 064 — 0.874
- 065 — 0.435
- 067 — 0.382
- 071 — 0.833
- 072 — 1.002
- 073 — 1.033
- 075 — 0.211
- 076 — 0.750
- 077 — 0.202
- 078 — 0.953
- 079 — 0.194
- 080 — 0.646
- 082 — 0.427
- 085 — 0.428
- 086 — 0.424
- 087 — 0.141
- 088 — 0.295
- 089 — 0.609
- 090 — 0.141
- 091 — 0.186
- 095 — 0.138
- 096 — 0.520
- 097 — 0.697
- 098 — 0.297
- 099 — 0.391
- 100 — 0.915
- 101 — 0.756
- 102 — 0.969
- 103 — 0.233
- 104 — 0.294
- 105 — 0.432
- 106 — 0.300
- 108 — 0.254
- 110 — 0.445
- 111 — 0.300
- 112 — 0.139
- 114 — 0.234
- 116 — 0.534
- 117 — 0.298
- 121 — 0.317
- 123 — 0.194
- 124 — 0.516
- 127 — 0.315
- 130 — 0.546
- 135 — 0.371
- 137 — 0.290
- 138 — 0.140
- 139 — 0.216
- 140 — 0.294
- 141 — 0.196
- 142 — 0.451
- 144 — 0.447
- 145 — 0.627
- 146 — 0.254
- 147 — 0.031
- 148 — 0.294
- 149 — 0.292
- 150 — 0.292
- 151 — 0.189
- 152 — 0.205
- 153 — 0.880
- 154 — 0.179
- 158 — 0.442
- 159 — 0.614
- 160 — 0.817
- 161 — 0.306
- 162 — 0.138
- 163 — 0.283
- 165 — 0.180
- 166 — 0.158
- 167 — 0.298
- 168 — 0.295
- 169 — 0.498
- 170 — 0.403
- 171 — 0.044
- 172 — 0.426
- 173 — 0.413
- 174 — 0.235
- 176 — 0.141
- 177 — 0.211
- 180 — 0.289
- 181 — 0.371
- 182 — 0.174
- 183 — 0.511
- 184 — 0.811
- 185 — 0.566
- 186 — 0.515
- 187 — 0.447
- 188 — 0.570
- 189 — 0.204
- 190 — 0.070
- 191 — 0.054
- 192 — 0.341
- 193 — 0.203
- 194 — 0.411
- 195 — 0.661
- 198 — 0.356
- 201 — 0.138
- 202 — 0.292

Count: 136. Below z = 0.30: 66.

## C18d — Klein et al. 2019, MNRAS 488, 1704 (2019MNRAS.488.1704K), "Weak lensing measurements of the APEX-SZ galaxy cluster sample"

- URL read: https://durham-repository.worktribe.com/OutputFile/1287225 (Durham repository copy of the published paper; the page states MNRAS 488, 1704–1727 (2019), doi:10.1093/mnras/stz1491). No arXiv version was found by search. VizieR J/MNRAS/488/1704 (table1) exists per https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/MNRAS/488/1704 but the table could not be downloaded (CDS, TAPVizieR and Durham all refused by the proxy for direct download).
- Table read: Table 1, "Cluster data sets: For the clusters analysed in this study, we list the redshift zNED as quoted in NED, ...", columns Cluster and zNED.
- **Verification limit:** this table was read through the WebFetch tool, which returns a model-mediated transcription, not raw text. It was fetched twice with different prompts and both returns agreed row for row. No file hash is available. Spacing such as "RXCJ0437.1 + 0043" is as returned and may be an extraction artefact. This list should be re-read from the PDF or VizieR before it is relied on.
- The table has 42 rows; 3 are continuation rows with a blank name (extra data sets for the cluster above). Their printed z is given in brackets.

- A2744 — 0.307
- RXCJ0019.0−2026 — 0.277
- A2813 — 0.292
- A209 — 0.206
- XLSSC 006 — 0.429
- RXCJ0232.2−4420 — 0.284
- RXCJ0245.4−5302 — 0.302
- A383 — 0.187
- RXCJ0437.1 + 0043 — 0.284
- MS0451.6−0305 — 0.539
- A520 — 0.199
- RXCJ0516.6−5430 — 0.295
- RXCJ0528.9−3927 — 0.284
- RXCJ0532.9−3701 — 0.275
- A3404 — 0.167
- Bullet — 0.297
- A907 — 0.153 [continuation row: 0.153]
- RXCJ1023.6 + 0411 — 0.280
- MS1054.4−0321 — 0.831
- MACSJ1115.8 + 0129 — 0.348 [continuation row: 0.350]
- A1300 — 0.308
- RXCJ1135.6−2019 — 0.305
- RXCJ1206.2−0848 — 0.441
- MACSJ1311.0−0311 — 0.494
- A1689 — 0.183
- RXJ1347−1145 — 0.451 [continuation row: 0.451]
- MACSJ1359.2−1929 — 0.447
- A1835 — 0.253
- RXJ1504 — 0.215
- A2163 — 0.203
- A2204 — 0.152
- RXCJ2014.8−2430 — 0.160
- RXCJ2151.0−0736 — 0.284
- A2390 — 0.228
- MACSJ2214.9−1359 — 0.483
- MACSJ2243.3−0935 — 0.447
- RXCJ2248.7−4431 — 0.348
- A2537 — 0.297
- RXCJ2337.6 + 0016 — 0.278

Count: 39 names (42 rows). Below z = 0.30: 24.

---

Not done here: no cross-matching of names between records, no checks against NED, nothing committed. Scratch files and the downloaded PDFs are in /tmp/claude-0/-home-claude/c0d18c72-c8bb-5ada-a175-e0167606991c/scratchpad/names1/.
