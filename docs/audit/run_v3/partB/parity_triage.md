# Audit v3 Part B, questions 4 to 6: outcome of each finding (D-124, D-125)

This covers the 41 findings under checklist questions 4 to 6 in `reader1/findings.csv` and `reader2/findings.csv`, numbered in file order (reader 1 first). They are not deciding (plan v3 §3.4). Each is resolved by a change or by no change with a reason.

| # | Reader | Finding (short) | Outcome |
|---|---|---|---|
| 1, 28 | R1, R2 | About plain: the analytics note said "now fixed" | change, #252 |
| 2 | R1 | Methods plain: SPARC gas was "hydrogen" only | change, #255 |
| 3 | R1 | GC: the 0.80 coverage cut had no reason | change, #255 (D-036 item 1) |
| 4, 16 | R1 | NGC 2298 and Pal 5: firmer or weaker wording than the source | change, #252 and #255 (the source's words, D-098) |
| 5, 6 | R1 | Dwarf methods: σ citations named other papers' arXiv IDs | change, #248 |
| 7, 22 | R1, R2 | Known issues: each layer pointed to the other | change, #256: plain entries for #222 to #243, used on system pages too |
| 8, 10 | R1 | X-COP and SPARC v3 plain status left out standing failures | change, #246 and #252 |
| 9 | R1 | X-COP v3 plain named version 2 | change, #255 (the v2 page keeps its text, which a frozen test checks) |
| 11 | R1 | Plain licence line stated reuse as settled | change, #252 |
| 12, 23 | R1, R2 | Plain sliders "on the map" | change, #252 (by each slider's scope) |
| 13, 14, 27 | R1, R2 | Not-plotted reasons only in technical shorthand | change, #256 (`reasons_plain.mjs`) |
| 15 | R1 | Map card plain used a share framing | change, #255 |
| 17, 40 | R1, R2 | Hydra II: "Table 1, None" | change, #255 (note beside the text, #232) |
| 18 | R2 | Coverage: the reason for the redshift cut was generic | change, #255 (D-066, D-033 quoted) |
| 19 | R2 | Methods stance plain left out lensing and the layer rules | change, #255 |
| 20 | R2 | Coverage plain shows frozen expert documents | **no change:** the frozen documents are shown as written in both layers, and each has a plain summary above it |
| 21 | R2 | Coverage plain caption: "systems on the map" | change, #255 |
| 24 | R2 | System page: plain heading over verbatim inventory notes | change, #256 |
| 25 | R2 | Dwarf flags verbatim in the plain layer | change, #256 (plain text for all 21 flags) |
| 26 | R2 | Crater called a globular cluster in plain | change, #249 |
| 29 | R2 | About plain left out the search claim | change, #255 |
| 30 | R2 | "Points that match" | change, #252 |
| 31 | R2 | Front page plain "visible matter" against Methods "detected matter" | **no change:** "pull from visible matter" is the ruled plain term (project vocabulary, D-008). Methods' "detected" is the expert sense of the same quantity |
| 32 | R2 | Per-dataset methods: plain is only a summary | change, this PR: a plain version for each section |
| 33, 34 | R2 | Methods counts had no basis (recorded against plotted) | change, #252 |
| 35 | R2 | Methods: X-COP "one-sigma" errors | change, #252 |
| 36 | R2 | Methods: X-COP "non-parametric" | change, #246 |
| 37 | R2 | SPARC error formula attributed to the wrong paper | change, #252 (confirmed on arXiv) |
| 38 | R2 | About: the citation named v0.1 | change, #252 |
| 39 | R2 | Dataset index: "Reproduction: passed" for v3 | change, #252 ("Re-issue test") |
| 41 | R2 | Front page left out part of the v2 audit result | change, #250 (now states audit v3) |

Every finding is resolved: 39 by a change and 2 by no change with a reason (20, 31).
