# Cluster stellar masses (D-068): comparison and adjudication (2026-10-31)

`compare.py` (committed before either reading was opened, matching by record identifier): **44 of 49 matched pairs agree.** Four disagreements were settled from the readers' own notes; the fifth pair is one record that only reader A identified (S13d). Both readers disclose that some unmasked table numbers reached their screens while reading. None were recorded; the disclosures stand in the readings.

| # | A | B | Final | Reason |
|---|---|---|---|---|
| S2b | X | P | **X** | Both readers: the early-type M/L is dynamical, and the spiral share depends on an X-ray temperature relation. Protocol §2: a dynamical M/L is not a baryonic input; scaling relations are excluded (§1.3). |
| S4c | E | P | **X** | Reader B read Table 2: only the stellar fraction (normalised by M500) is printed. Same sample and method as S4b, which is used. |
| S13d | — | NS | **—** | Reader A identified it as a semi-analytic model (Contini & Gu 2021), not observations. |
| S18c | X | P | **X** | Both readers: averages in M500 bins and figures only; no per-cluster values. |

## The readers' questions

- **QS1. Mass-to-light ratio from dynamics** (S3a, S3b, S5, S18b; the BCG part of S12a). **Settled by an existing rule:** protocol §2 says a dynamical M/L is not a baryonic input; it would bring dynamics into g_bar. Coded X. Cost: S3a, S3b and S18b were the only direct measurements of intracluster light in local clusters.
- **QS2. IMF named only in a cited method paper** (S1a, S4a, S4d, S9b, S12a). This applies "named IMF", not a new rule: accepted once the cited paper is read at source and names the IMF, at packaging. Coded P until then.
- **QS3. Per-cluster values neither printed nor released, clusters not named** (S7a, S14b). No cluster can be matched, so X. Recorded as data-request leads (requests are on hold, D-032).
- **QS4. Galaxy-level catalogues and stellar mass functions with no cluster total** (S1b, S1c, S19, S13b, S13f). **Needs a ruling (see below).**
- **QS5. Apertures set by a scaling relation** (r500 or r200 from M–T, L_X–M, SZ or richness). Settled by the draft A9 rule §1 item 6: such radii may be used as radii, flagged. The stellar mass inside them is a direct measurement.
- **QS6.** S14c gives fractions and slopes only: X.

Every decision is in `final.csv`: **E 13, P 11, X 23, — 1.**

## Ruling needed: QS4

May the Atlas build a cluster's stellar mass by summing a published member-galaxy catalogue (or integrating a published stellar mass function)?

- **(a) Recommended: no, not for v1.0.** Summing needs our own membership and completeness corrections: a new analysis, not a reading. That is the line drawn for star clusters and dwarfs, where the Atlas never computes a dispersion from velocities. These records are kept as inputs and leads.
- **(b) Yes, with a frozen, tested summation and completeness method.** It would rest on our own modelling.

## Coverage of the five X-COP clusters with modelled stars (issue #91)

| Cluster | Measured stellar mass found | Status |
|---|---|---|
| A2255 | S4b (Laganá et al. 2011: members inside r500, Salpeter IMF) | **E** |
| A3158 | S1a (OmegaWINGS stellar-mass profiles) | P (IMF via WINGS-SPE, QS2) |
| A3266 | S1a | P (as A3158) |
| A1644 | member-galaxy catalogue only (S1b) | depends on QS4 |
| RXC1825 | none in any record | none |

Ghizzardi et al. 2020 (S12b) confirms that X-COP has no stellar mass for these five.
