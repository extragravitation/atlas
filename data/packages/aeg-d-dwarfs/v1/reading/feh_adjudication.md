# Metallicity (D-057) and Woo et al. 2008 readings: adjudication

Two independent readings under `FEH_READING_BRIEF.md`, compared by `reproduction/compare_feh_readings.py` (committed before either reading was seen), then resolved by `reproduction/select_feh.py` (written after the comparison; disclosed).

## Sheet A: metallicity

- **Raw comparison:** 252 printed values recorded by both readers, 42 by reader 1 only, 32 by reader 2 only, and 2 headline differences (`feh_comparison.csv`).
  - The one-reader values are optional extras: literature values the paper quotes, subsample means, percentiles.
  - Most of the rest differ only in labelling. A printed σ that is an observed standard deviation was labelled `feh_spread` by reader 1 and `other` by reader 2. Neither enters the metallicity used.
- **Headline system value** (the D-057 quantity): for 76 of the 82 systems with an original, both readers recorded the same single value with the same errors. Star counts are recorded but not compared; for Boötes III one reader left the count blank.

Adjudicated:

| System | Ruling |
|---|---|
| Crater II (Ji 2021) | −2.16. The error is printed ±0.04 in the table and ±0.03 in the text; the table printing wins (D-051 duplicate rule): ±0.04. |
| Perseus I (Martin 2014) | −2.0 ± 0.2 (12 stars). Both readers read the same number. It comes from a single stacked spectrum and is the paper's headline, so it is used and flagged `feh_stacked_spectrum`. |
| UGC 4879 (Kirby 2013b) | Printed as "VV 124", −1.43 ± 0.02. Kirby et al. 2014 (already in the record) names the galaxy "VV 124 (UGC 4879)". Reader 1 recorded the value in a row; reader 2 recorded it in a note. Same value. |

**Compilation entries (D-053).** For Carina, Fornax, Sagittarius, Sculptor and Sextans, LVDB's spectroscopic reference is Simon 2019 (ARA&A), a compilation. Simon cites one original per [Fe/H]:
- Fabrizio et al. 2012 for Carina;
- Kirby et al. 2013b (ApJ 779, 102) for Fornax, Sculptor and Sextans;
- Mucciarelli et al. 2017 for Sagittarius.

Both readers read these originals independently (`feh_reading_*_followup.csv`) and agree on every headline value:

| System | Original | [Fe/H] | Stars | Note |
|---|---|---|---|---|
| Fornax | Kirby 2013b | −1.04 ± 0.01 | 672 | |
| Sculptor | Kirby 2013b | −1.68 ± 0.01 | 375 | |
| Sextans | Kirby 2013b | −1.94 ± 0.01 | 123 | |
| Carina | Fabrizio 2012 | −1.80 | 44 | no error printed |
| Sagittarius | Mucciarelli 2017 | −0.52 ± 0.02 | 109 | nucleus only, within 9′, stars with [Fe/H] ≥ −1.0 |

**Compilation differs from its originals.** Simon's numbers are not those printed in the originals: Fornax −1.07, Sculptor −1.73, Sextans −1.97, Sagittarius −0.53. Simon most likely derived them from the originals' data. Under D-053 and D-057 ("originals are the record"), the printed original values are used and the difference is logged here.

Fabrizio 2012 also prints −1.75 ± 0.02 for the same 44 stars in footnote 36; the headline −1.80 is used. Reader 2 recorded it.

**Labels:**
- Four headline values are medians (Lacerta I and Cassiopeia III in Martin 2014; Cetus in Taibi 2018; Tucana in Taibi 2020). They are used and flagged `feh_median`.
- One system's original is photometric. It is flagged `feh_photometric` (D-057 item 2).

**No metallicity original:** 21 systems. Ten of them are plotted dispersions. See D-059.

## Sheet B: Woo et al. 2008

**Values.** The readers agree on every value for the same 29 systems: M*/L_V and log M*. The only differences:
- quantity names, which the brief left free;
- reader 1 attaching the footnote's "typical uncertainty 0.17 dex" to each log M*.

**Further identification.** Woo's "DDO 210" was identified as Aquarius using Kirby et al. 2014 ("Aquarius (DDO 210)"). Both readers then read the row: type Tr, M*/L_V = 0.9, log M* = 6.25. That makes 30 systems.

Woo's "Antlia" is not on the sheet (the sheet has Antlia II and Antlia B), so it was correctly left unmatched.

**Method per galaxy not printed.** Both readers report the same thing. Woo's data set "b" assigns M*/L by morphological type and by which data exist (Table 3, Cases 1–3):
- dI galaxies get an average of colour-based and SFH-based values;
- Case 3 uses type medians;
- the case applied to each galaxy is not printed.

So no Woo value can be confirmed as a per-system star-formation-history value, which is what REPRODUCTION.md's route (a) requires. Proposed ruling: D-059.

## D-059 item 2: [Fe/H] from the dispersion original

Ten plotted systems have no metallicity original. Both readers read their dispersion originals (`feh_d059_sheet.csv`; `feh_reading_*_d059.csv`).

- **Collins 2013 (nine systems):** both readers took the Table 4 co-added-spectrum value as the paper's own result and agree on every value and error. These values are used, flagged `feh_from_dispersion_paper feh_stacked_spectrum`.
  - The paper also prints Table 5 (a compilation of literature values) and figure-panel values. These often differ from Table 4: for And XI, −2.0 ± 0.3 in Table 5 against −1.8 ± 0.1 in Table 4. Both readers recorded them as non-headline.
  - The paper prints no spread for any of these systems.
- **Tollerud 2012 (And XIII):** both readers found no [Fe/H] for the system. And XIII is flagged `no_metallicity_value` and is recorded, not plotted (D-059).
