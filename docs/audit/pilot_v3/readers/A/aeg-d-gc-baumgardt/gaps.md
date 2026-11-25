# Method gaps (independent reader, packet A, aeg-d-gc-baumgardt/v3)

No step was blocked, so neither row is marked "method incomplete". These are the steps I had to infer or guess, even where I am confident of the result.

## Method gaps

1. **Harris row lookup refers to code.** The locator says the row is found "as v1's sources_io.read_harris and norm_name match it". read_harris is not described. I matched the ID column text ("NGC 6712", "NGC 5139") with the §2 norm_name rules.
2. **Harris fixed-width parsing is not described.** mwgc.dat is fixed-width, and the Name column is blank for NGC 6712, so splitting on whitespace is ambiguous. I read R_Sun, V_t and M_V,t by lining the values up under the header labels. Both readings agree.
3. **Start of the King integration.** The method gives W(0)=W0 and dW/dx(0)=0 but starts the integration at x=1e-6. It does not say what values to use at that point. I used the series W = W0 − 1.5x², dW/dx = −3x. The effect is negligible.
4. **Units of the radius in F(R).** F(R) needs R in units of r0, so I took x = R[arcsec]/r0[arcsec]. This is implied ("R is in arcsec, the unit of r0") but not written as a step.
5. **Grid for the 3D light integral.** The trapezoidal grid is unspecified. I used a dense log grid plus adaptive quadrature for the cylinder term. As a cross-check I also ran the stated RK4 scheme (400 steps per decade). The two agree to better than 1e-6 relative in g_obs.
6. **Light normalisation.** "Light follows ρ" is taken to mean that ρ(W) itself is the luminosity density. Normalisation cancels in F.
7. **Precision and rounding are not stated.** The method does not say how many significant figures to report, or whether σ, R_h or L_V are rounded before they are used. I carried full precision throughout and report 7 significant figures.
8. **Parsing veldis.html is not described.** The HTML is malformed (`<tr><tr>`). I treated each `</tr>`-terminated group of seven `<td>` cells as one data row. A blank first cell inherits the cluster name from above.
9. **Candidate tie-breaks were not needed.** RV was the only line-of-sight Type for NGC 6712. For NGC 5139 the only other one was K18, with coverage 0.198, which is below 0.80. So the ordering rules (NStar total, year) were never exercised.

## Locator and provenance issues (not method gaps, but found during the audit)

10. **The veldis locators do not identify bins.** They give `<r> = [value]` as an unfilled placeholder. Each inputs entry therefore cannot be tied to a specific bin. I identified bins by sorted order: 5 RV bins for NGC 6712 and 23 for NGC 5139, which matches the number of sigma_los entries in rows.json.
11. **rows.json lists inputs the method does not use.** It includes (M/L)2 and Harris V_t. I recorded them in inputs.csv but did not use them. It also lists Δσ Up and Low, which only feed the §8 uncertainties; I did not compute those because they were not requested.
12. **The VOTable file hashes do not match sources.json.** The sha256 values in sources.json do not match the two VOTable files in files/. The models file gives fd0b6709… where sources.json says 84647d34…, and the clusters file gives 3a55d995… where sources.json says 282ea6da…. The content hashes (from `<RESOURCE`) do match. The models file header gives request_date 2026-11-25, but sources.json says it was retrieved 2026-10-30. So these are re-exports, and only their header lines differ. sources.json also gives the paths as `mvdm05/…`, but in the packet the files sit directly in files/. The veldis.html and mwgc.dat hashes match.
13. **R_Sun and Dist differ for NGC 5139.** For NGC 5139, Harris R_Sun is 5.2 kpc and the McLaughlin & van der Marel Dist is 5.3 kpc. The §4 step 6 rescaling R_h × R_Sun/Dist handles this as written. I note it only because it affects R_h.
