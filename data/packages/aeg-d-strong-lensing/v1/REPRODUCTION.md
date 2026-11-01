# aeg-d-strong-lensing/v1 — reproduction test (draft; frozen on merge, before conversion)

**Status: draft.** Written 2026-10-31. No Einstein radius, Einstein mass, stellar mass, mass-to-light ratio or velocity dispersion value of any A6 lens has been opened. Seen so far:
- the A6 search log and screening readings (metadata and methods);
- the packaging inventory, with column headers, file names, licences and lens counts.

On merge, this file's SHA-256 goes into `sources.json`, and it is not edited after the first conversion run. If a pass/fail test fails, the package does not ship and the failure is published; the test is not changed to pass (operating rule 5).

## Scope

Galaxy-scale strong lenses that are early-type galaxies (cell A6; D-063 item 6). One value per system, in projection, at the Einstein radius (D-064).

The record-level choices are fixed by the frozen precedence rule `docs/methods/A6S_PRECEDENCE.md` (D-065), applied by script to metadata before any value was read:

| Input | SHA-256 |
|---|---|
| `docs/sources/screening-A6S/packaging-inventory.md` (§2 result table) | `4421045d7d78ca5cb79f266b9bfd45db15d7640847a61e5963a41c73a2f4cf2e` |
| `docs/sources/screening-A6S/packaging-tools/a6s_options.csv` | `28a309ee2ecb24ef62c97f85bf270f8d4ef891dd5a05478d821426f2d6158a80` |
| `docs/sources/screening-A6S/packaging-tools/rank_a6s.py` | `1b8e420395768a82cc557053eb098120e8bdd2c691b8f8e1e92c69caf0d80a2e` |
| `docs/methods/A6S_PRECEDENCE.md` | `f103809eadac00dac657061982e963fdfe1e85f46d68188a73953c17dfe9b03d` |

Surveys in v1: every scope row of that table with both an observed-side default and a stellar-mass default:
- SLACS (R5 with R13);
- S4TM (R10);
- SL2S (R20, R22, with redshifts from R21);
- SNELLS (R28 with R26; R61 with R33; R61);
- MNELLS (R27 with R29);
- MaNGA (R32);
- NGC 6505 (R30);
- SuGOHI III (R57);
- CASTLES (R36 with R41);
- KiDS J0233−3447 (R43);
- the Cosmic Horseshoe (R60 with R34);
- J0100+1818 (R47, an A7 system).

Scopes with no stellar-mass default are recorded with that reason: SLACS IX new models, BELLS, BELLS GALLERY, LSD, AGEL, H-ATLAS, Herschel and iPTF16geu. The same applies to COSMOS and Euclid Q1 while they are P.

## Who is plotted (A6S precedence §1; D-066)

All of these must hold; otherwise the system is recorded with the reason.
1. A6 kind: an early-type lens confirmed at source (D-063 item 6). Systems the source calls a group or cluster lens go to A8 or A9; ambiguous ones go to A7.
2. Spectroscopic lens and source redshifts, neither derived with the system's own σ (D-063 items 3 and 5).
3. Printed lens redshift below 0.30 (D-066).
4. An observed side and a stellar mass that refer to the same cylinder (see "Aperture matching").

## Inputs and rules

| Quantity | Rule |
|---|---|
| **Observed side** | The default record's M_E as printed. Where the default prints only θ_E, M_E = θ_E² c² D_s D_l / (4 G D_ls), with the source's own cosmology (§2.4), by the frozen `aeg.lensing.einstein_mass_msun`.<br>**SLACS:** R5 prints θ_E only, so M_E is computed from R5's θ_E. R7's printed M_E for the same models is the reported check below.<br>R_E = θ_E D_l in the same cosmology (`aeg.lensing.einstein_radius_kpc`). An image-separation estimate is used only where it is the default, and is flagged `model_dependence` (D-063 item 2). |
| **Cosmology** | The cosmology stated by the source of each θ_E, read at source and recorded per record (H0, Ω_m, flat). Where a source states none, the system is recorded, not plotted. |
| **Stellar mass inside R_E** | The default record's value as printed, inside R_E. Where the default prints only a total and its own light-profile fit (Sérsic or de Vaucouleurs with R_e), M*(<R_E) = M*_total × f(<R_E), with f from the source's own fit by the frozen `aeg.lensing.sersic_projected_fraction`, flagged `mstar_in_RE_from_profile` (§3.1). Profiles of several components are summed component by component, each with its own printed fraction of light or mass. A multi-Gaussian (MGE) model is evaluated only if a frozen MGE routine exists; until then such a system is recorded with that reason. |
| **IMF and range** | The default is Chabrier or Kroupa as printed. The top of the range is the Salpeter value printed by the same source. Where only one IMF is printed, the top is the same value × the Chabrier-to-Salpeter ratio of the source's population model, read at source in its model paper and registered (§3.2). |
| **Aperture matching** | The two masses must refer to the same cylinder. Where the stellar mass is printed inside another radius R′, it is moved to R_E only by f(<R_E)/f(<R′) from the source's own light-profile fit, flagged. Otherwise the system is recorded, not plotted. The same applies to an observed mass printed inside an aperture other than R_E (e.g. SNELLS R_ap), unless the source states that the aperture equals R_E. |
| **Gas** | §3.4. A system-level statement or limit where the source gives one. Otherwise a cited, quoted literature statement for the kind, read at source before conversion; each system is marked "absent (literature limit for this kind)". The 12 candidates in inventory §4 are judged in the reading step. If none qualifies, the cell returns to JvH before conversion. |
| **g_obs, g_bar** | Projected (D-064): g_obs = G M_E / R_E², g_bar = G M*(<R_E) / R_E² by `aeg.lensing.projected_acceleration`. The points carry the mark and label "projected" and are never merged with 3D values. |
| **Uncertainties** | Printed errors on θ_E or M_E and on the stellar mass are carried. Where a source prints no error, the flag `no_uncertainty` is set. Distance errors are not added (the redshifts are spectroscopic). |
| **Alternatives** | Records named as alternatives in the inventory result table are packaged as alternative observables of the same system, never as defaults. This includes R7's σ-prior stellar masses (D-063 item 3). |

## Reading step (before conversion)

Two independent readers, in separate folders, read every value to be packaged at source, each with a quote and its location, under a brief committed first:
- identifiers, both redshifts and how they were measured, θ_E or M_E with errors, cosmology;
- stellar mass and its aperture, IMF, population model and bands;
- light-profile parameters where §3.1 is needed;
- kind statement, gas statement.

The readers also settle three questions at source, as facts, not rulings:
- whether SNELLS R_ap equals R_E (R61);
- which aperture SuGOHI III's stellar mass refers to (R57);
- whether R26 and R29 print the light profile needed for aperture matching.

Disagreements are settled by Claude at source and logged. A comparison script is committed before the readings are opened.

## Pass/fail tests

1. **Second reading against the sources.** Every packaged number equals the source as printed (or the released file), in both readings.
2. **Transcription.** The package tables, read back, equal the values recorded by the readings.
3. **Arithmetic integrity.** M_E (where computed), R_E, f(<R_E), M*(<R_E), g_obs and g_bar, recomputed from the stored inputs by `aeg.lensing`, agree with the stored values to 10⁻⁹ relative.
4. **Code.** `pipeline/tests/test_lensing.py` passes. These are synthetic tests:
   - distances against the Einstein–de Sitter closed form;
   - the Einstein mass against a hand computation, and its θ² scaling;
   - Sérsic fractions against closed forms for n = ½ and n = 1, the integer-a identity for n = 4, and ½ at R = R_e.

**Pass** means tests 1–4 all hold.

## Reported, not pass/fail

- **§4 formula check.** Where a source prints both θ_E and M_E (e.g. R7 for R5's models; R10; R32), the formula of §2.4 against the printed M_E, as a ratio per system.
- **Overlap.** Systems in more than one survey's default (e.g. SLACS and S4TM): the defaults side by side, with no averaging.
- **Profile step.** Where a source prints both a total stellar mass and the mass inside R_E, the §3.1 fraction against the printed value.

## Code frozen with this file

| File | SHA-256 |
|---|---|
| `pipeline/aeg/lensing.py` | `0755c9390bf114b283d35305c3882bbe46c41303b7a01dc7c376a2a143926ed5` |
| `pipeline/tests/test_lensing.py` | `733262d2a0da9b43f4bb16eefad56b2d9d5ed061b284d34a48745aa6a6bc7cb7` |
