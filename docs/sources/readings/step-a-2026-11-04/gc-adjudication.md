# Globular clusters (`aeg-d-gc-baumgardt/v1`): adjudication of the two step A readings

**2026-11-04, Claude.** This compares `gc-reader-A.md` (31 terms, with sub-terms) and `gc-reader-B.md` (41 terms).

**Common ground.** Both readers read the local source copies (all hashes match `sources.json`), plus BH18, B17, Harris 2010, MvdM05, Wolf 2010, K18, L13, L15 and KM09. The e-print hashes agree for every shared source.
- Reader A also read Chantereau 2020, F13, D21, C22 and G22.
- Reader B also read BV21 and BSH20.
- Both were blocked from Harris's bibliography file (`physics.mcmaster.ca`) and did not work around the block.

## Agreement

The two readings agree on every shared term: quotes, sizes, scales, axes moved, and whether v1 carries the term.

**What v1 carries as error:**
- the σ statistical error, in the g_obs bars;
- the population M/L₁ error, in the g_bar bars;
- the IMF range, through the Salpeter column and the slider.

**What v1 records but does not propagate:** the R_h error, and the King W₀ and r₀ errors.

**What v1 carries nothing for:**
- distance;
- integrated magnitude;
- binaries, membership, rotation, tides and crowding;
- the estimator, the deprojection and ellipticity.

The v2 term list is the union. Its groups mirror the dwarf adjudication's, plus the cluster-specific items below.

## Findings settled at source

**F1. Distance moves the axes differently depending on its cause.** Both readers inferred this; Reader B verified it numerically on the source values.
- **What Reader B found:**
  - Harris `M_V,t` = `V_t` − `(m-M)_V` exactly, for all 151 complete rows.
  - `R_Sun` = 10^(((m−M)_V − 3.1 E(B−V) + 5)/5) to within rounding (median 0.2 %).
  - Reader A checked two rows and agrees.
- **What follows:**
  - An error in the horizontal-branch calibration or in V_HB moves R_Sun and L_V together (L ∝ D²). So g_bar is unchanged and g_obs ∝ 1/D.
  - A reddening error moves R_Sun only, so g_obs ∝ 1/D and g_bar ∝ 1/D².
  - An error in V_t moves g_bar only.
- **Consequence for v2.** These are separate rows in the uncertainty-terms table, each with its own registry formula, as §2a rule 5 already allows:
  - the horizontal-branch calibration (Harris 2010 l. 148: zero point ±0.049 mag, slope ±0.033, rms 0.11 mag): dataset scale;
  - the reddening;
  - V_t.
- **The same pattern as the dwarfs:** the stellar g_bar is distance-free whenever the luminosity and the radius scale together.

**F2. Integrated magnitude has a cited independent size.** *Reader B; verified at source.*
- Baumgardt, Sollima & Hilker 2020 (arXiv 2009.09611v1, `paper.tex`, Table "tab:comp", l. 266) gives, for Harris (2010) against their photometry, a scatter σ_V of 0.22, 0.45 and 0.70 mag for V < 8, 8–11 and > 11.
- This is the scatter of the difference between two measurements, not Harris's own error. So it bounds the Harris error from above.
- In v2 it is a system-scale term, status `given_by_other_source`, described exactly that way.
- Reader A reported no stated error for V_t in Harris, which is also correct.

**F3. v1 plots data that its own sources exclude.** *Both readers; verified at source.*
- **NGC 6715 (M54).** B17 (arXiv 1609.08794v1, l. 586–589): "this is most likely due to the fact that the sample includes stars from the Sagittarius dwarf galaxy … We have therefore neglected all data points beyond 200'' in the dynamical analysis of this cluster." v1 uses all its RV bins, including 269″, 410″ and 679″, and plots it.
- **NGC 2298 and Pal 5.** BH18 l. 226–228: their profiles "increase towards the outer parts, which could be due to the ongoing tidal disruption of these clusters … We therefore neglected the outermost data point". v1 plots both with all bins.
- **The same class of issue as the dwarfs' F3.** D-025 sends systems "the source itself describes as tidally disturbed or out of equilibrium" to the exclusion register. Whether that covers a cluster the source treats by dropping bins, rather than the whole system, is a question for the v2 test and a ruling. It gets a known-issue entry; no value is changed here.

**F4. Binaries named by the source.**
- BH18 (l. 230–233) names Pal 13 (about 50 % fall with multi-epoch stars only), Arp 2 and Ter 3 as possibly binary-inflated. Reader A notes these three are already "recorded" for other reasons.
- No v1 binary flag exists, although D-025 asks for one (both readers).

**F5. The error criterion in B17.** *Both readers.*
- B17 sets its "1σ" bounds where the likelihood is 0.5 of its maximum.
- For a Gaussian likelihood, 1σ corresponds to e^(−1/2) ≈ 0.61. So the bounds may be somewhat wider than 1σ.
- The confidence level of the `veldis.html` values is therefore recorded as "stated as 1σ by BH18; criterion as in B17". The difference is not quantified, and nothing is changed.

**F6. Mixed scales inside one error.** e_(M/L)₁ combines a dataset-scale age term (13 ± 2 Gyr for every cluster) with a system-scale [Fe/H] term (±0.2 dex). MvdM05 does not split them. v2 states this in the term's note. It needs no standard change.

**F7. Record locations to correct in the v2 registry.** Both readers found these.
- `assumptions.json` cites KM09 "§2, Table 1 (Q = 0.53–1.00)". In arXiv v1 the Q_pred column is in the table `tab:pred` (§4.1 or §5 by the readers' numbering), not Table 1.
- MvdM05's R_h is in Table 11 (`tab:struc`), while W₀ and r₀ are in Table 10. The registry cites "Table 10" for all three.

**F8. Smaller items.**
- MvdM05 used Harris (1996) for [Fe/H] (behind M/L₁) and for `Dist`, while the Atlas uses Harris (2010). The R_h rescaling corrects the distance part, but M/L₁ keeps the older [Fe/H]. No source states the size.
- Wolf's 4/3 accuracy statement is for King (1962) profiles; v1 uses King (1966).
- Wolf's ⟨σ²⟩ is a whole-system luminosity-weighted average; v1 averages bins covering ≥ 80 % of the light.
- The `veldis.html` "plus updates" values differ slightly from BH18's printed Table 3 (Arp 2's first bin: 1.97 against 2.03).

## What this means for standard 2.4.0

Nothing new beyond the draft. F1's cause-dependent directions are separate uncertainty-terms rows, each with its own registry formula; §2a rule 5 and §7a already allow that.
