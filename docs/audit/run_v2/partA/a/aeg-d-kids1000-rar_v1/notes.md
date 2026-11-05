# Reader A notes: aeg-d-kids1000-rar_v1

## What was read

- Brief: `/home/claude/audit_v2/BRIEF_COMMON.md`.
- Method: `method/methods_page.txt` (KiDS-1000 paragraph and the Uncertainties paragraph), `method/SOURCE.md`, `method/sources.json`.
- Source: the seven members in `sources/brouwer2021_rar_members/`. Their SHA-256 values are recorded below. I used only the three `*_Nobins.txt` files that the locators name, plus `README.txt` to read the column definitions.
- "data row N" is taken as the N-th non-comment line, so it is file line N+1, after the single `#` header line. Every file has 15 data rows with 8 columns, and the header labels were checked in code.
- No arXiv e-print was downloaded. No other copy of the dataset was opened, and no folder outside this packet and this output folder was opened.

## Result: all 10 rows are `method incomplete`

The written method says:
- g_obs = 4 G ΔΣ, a singular-isothermal-sphere deprojection, per SOURCE.md and the methods page.
- g_bar is "stellar mass plus cold gas treated as a point mass", and "stars and cold gas are not separately released."
- Under Uncertainties, the g_obs error is "bias-corrected, as released."
- "Units carry h70; the Atlas takes h = 0.7."

Missing steps:
1. **Constants for g_obs.** The method gives no value of G and no conversion from pc to m or from M_sun to kg. ΔΣ is printed in h70 M_sun pc⁻², so turning 4 G ΔΣ into m s⁻² needs G in matching units or explicit conversions. Neither is in the method. The brief says constants come only from the method, so g_obs cannot be computed.
2. **Bias correction for g_obs.** The method does not say whether ΔΣ for the g_obs value must be divided by the released `bias(1+K)` column. It applies bias correction only to the uncertainty. The README says to always apply it, but the README is a source file, not the method.
3. **Where g_bar comes from.** The method defines g_bar physically: a point mass of stars plus cold gas within the measurement radius. The release contains no stellar masses, gas masses or radii, so that definition cannot be carried out. The method does not say that g_bar should be read from the released first column, `Radius(m/s^2)`. The README describes that column only as "the mean projected distance … in meter-per-second-squared for the RAR data" and does not say it is g_bar. Taking it as g_bar would be a guess under the brief, so g_bar was left empty.
4. **Hot-gas file (m000019, m000021, m000028).** These locators point to `Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt`. The method defines g_bar as stars plus cold gas only and never mentions a hot-gas variant or which baryonic components that file's acceleration axis includes. This is a further gap, and possibly an inconsistency between the method text and the file used.

## SUPPLEMENTARY: not the written method, not in values.csv

This is for the coordinator's information only. It uses the constants printed in the source `README.txt`, not in the method: G = 4.52e-30 pc³ M_sun⁻¹ s⁻², pc/m = 3.086e16, g_obs = 4 G ESD_t/bias [pc/m] (README, "Fig-X_RAR_*"). It also lists the raw first column. If the method had stated these steps, these would be the results. They are deliberately kept out of `values.csv`.

| measurement_id | file | data row | g_obs (README constants) | Radius(m/s^2) column |
|---|---|---|---|---|
| m000034 | Fig-4-C1_RAR-GAMA-isolated_Nobins.txt | 4 | 7.8164e-13 | 7.5922e-15 |
| m000019 | Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt | 4 | 7.0495e-13 | 7.5922e-15 |
| m000028 | Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt | 13 | 1.3781e-11 | 1.2582e-12 |
| m000015 | Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt | 15 | 1.9115e-11 | 3.9169e-12 |
| m000021 | Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt | 6 | 1.7878e-12 | 2.3635e-14 |
| m000007 | Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt | 7 | 3.4969e-12 | 4.1702e-14 |
| m000010 | Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt | 10 | 6.8065e-12 | 2.2906e-13 |
| m000032 | Fig-4-C1_RAR-GAMA-isolated_Nobins.txt | 2 | 7.1919e-13 | 2.4388e-15 |
| m000008 | Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt | 8 | 4.0504e-12 | 7.3580e-14 |
| m000004 | Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt | 4 | 1.4628e-12 | 7.5922e-15 |

## Other observations

- The README labels G as "G[pc^3/(Msun*s^2)] = 4.52e-30 pc^2/(Msun*s^2)". The unit is written two different ways (pc³ and pc²). It is a typo in the source, noted here only.
- The covariance files label the acceleration column `Radius[i](mps2/h70)`, but the Nobins files label it `Radius(m/s^2)` with no h70. The method's "h = 0.7" statement makes h70 = 1 either way, but the labels in the source are inconsistent.
- I recorded the `error` column as an input but did not use it. The task asks for g_obs and g_bar, not their uncertainties.

## Source member SHA-256 values (computed by this reader)

```
343d81c06643e2cc5126490d9f03918ac2708b0cdc4586b1534157c225578a9  Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt
c5fa734affa2e56228f9e78848419a38405775a0cf4c42471ae1c37cdea575ae  Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt
b613425287e1600c3ee866d058ca6ead0649095903debc89f09b100070270d74  Fig-4-C1_RAR-GAMA-isolated_Nobins.txt
963a81504c467feeff8c33043e331ce092f5dab55f0835decd3e8ff419583afc  Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt
5f81078112e1b5cfff24189d1b755db7c48f52d50b179224ed9ab7d8771928fe  Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt
0ae8b6ea736ff4037afaed02552cc389f0f131062c34774bea2542dfab59e6e8  Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt
b3680580696c5dbf5671c700d5e8f90fbfd1dc614fa7e3e07b2f66d1624e8645  README.txt
```

Run with: `python3 -I code/audit.py /home/claude/audit_v2/packets/aeg-d-kids1000-rar_v1 /home/claude/audit_v2/readers/a/aeg-d-kids1000-rar_v1`
