# aeg-d-dwarfs v3: re-issue under data standard 3.0.0

**Decision:** D-114. **Test:** `docs/standard-3.0.0-reissue-test.md` (T1 to T7), frozen with the standard before this package was built. **Known issue:** #227.

## What changed from v2

- **`sources.json`, 113 entries:**
  - **S1 to S19:** v2's 19 files (the LVDB index, member catalogues, gas table and M/L table) now have `id`, `kind`, `citation`, `identifier` and a structured `licence`. Their addresses and hashes are unchanged.
  - **S20 to S109:** one entry for each of the 90 original papers that a locator names, in the arXiv version the readings record as read (`copy_read`).
    - For 72 of them, a hash was recorded in `v1/reading/originals.csv` or `mcconnachie2012_originals.csv`. Every one was downloaded again on 2026-11-24 and is identical.
    - The other 18 were hashed for the first time on 2026-11-24, from the version the reading records. These include Gregory 2019, Koch 2007, Simon 2011, Kirby 2013, Ou 2024 and Woo et al. 2008, several of the documents the audit found without a hashed record (P3).
  - **S110:** Monelli et al. 2025, read by JvH in the journal PDF. The SHA-256 is as the reading recorded it. The article is open access under CC BY 4.0.
  - **S111:** van de Rydt et al. 1991, read in ADS page scans. It has no arXiv version. At first it had no file, and T7 run 1 failed on it. Under the ruling after that run, JvH downloaded ADS's PDF of the same scans on 2026-11-24 and it was hashed. Before hashing, the recorded values were found on it: M_V = −9.9 ± 0.4 on p. 136 and (m − M)0 = 23.1 ± 0.1 on p. 134 and in the abstract. The hash was recorded after the reading, not when the reading was made.
  - **S112 and S113:** the LaTeX e-prints of Fritz et al. 2019 and Wang et al. 2019, which the locators cite by line. Their hashes equal those in the reading.
- **Documents are verified once, not by CI** (`fetch_in_ci: false`). They were hashed against today's downloads. arXiv and the journals ask automated tools not to bulk-download them, and the conversion never reads them. The reachability job (T7) still checks every address with a small request. The data files S1 to S19 are fetched and hash-checked in CI as before.
- **Citations** are built from the arXiv record of each paper: exact title and authors (the first three, then "et al."). Year and journal come from the ADS bibcode.
- **Licences** were read on 2026-11-24:
  - arXiv records: 65 papers carry the non-exclusive licence to distribute, 13 CC BY 4.0, 10 the "assumed 1991–2003" licence, and 5 CC BY-NC-ND 4.0;
  - LVDB: CC0, from the repository LICENSE;
  - Zenodo member catalogues: CC BY 4.0;
  - VizieR: CDS terms, through the export's `rights_uri`;
  - journal machine-readable tables: none stated in the file headers; the article pages could not be read.
- **`locators.json`, 307 rules:** one per distinct `source_ref`, 241 in observables and 66 in measurements. Each lists its sources and its place. Where the text gives no place, the rule takes it from the reading record and names that record:
  - **σ (25 rules):** places from `v1/reading/sigma_selection_v3.csv` and `sigma_reading_1.csv`, per system.
  - **[Fe/H] (28 rules):** places from `v1/reading/feh_values.csv` and the first-reader [Fe/H] files, per system.
  - **Distance and magnitude references that name a paper but no place (13 rules):** places from the structure, residual and McConnachie readings, each named in the rule. For Saviane et al. 1996, the place of its own TRGB modulus was not recorded, and the rule says so.
  - **"M_V + (m-M) used by the paper" (2 rules):** these name no paper. The paper is the one that gives the system's distance modulus.
  - **Munoz 2018 M_V (18 rules, correction):** the text says Table 1. M_V is in Table 6; Table 1 gives the distance R. This was checked in the arXiv PDF (1806.06891v1). The rules give both tables and quote the text they correct.
- **`known_issues.json`:** the identifiers of issue #156 now read v3. New issue #227 lists the corrections and the unhashed source.
- **`data/registry/excluded.csv`:** v2's eight rows are repeated for v3, unchanged, as the converter writes them.
- **`data/assumptions.json`:** the 11 registry entries for v2 are copied to v3 unchanged.
- **`tests/`:** runs the re-issue test (T1 to T6) and the standard validator.

## What did not change

- **Values and text:** every table equals v2's once the version labels are mapped back (T1).
- **The converter:** `convert.py` differs from v2's in its version line and, by ruling D-115, in line 131 (T2). Line 131 is the key of the frozen-reading check, which now names v2's reading file. Line 132 still compares v3's byte copy against that frozen hash, so the check is unchanged. It still builds from v1's tables and readings, and it rewrites `reading/conversion_changes.json`, whose `aeg-d-dwarfs/v2` labels now read v3.
- **Carried over from v2 and still valid:** `REPRODUCTION.md`, its result, `SECOND_READING.md` and `reading/`.

## Correction added after the run (D-117, issue #232)

All 60 gas inputs carry the source_ref `Putman et al. 2021 Table 1, None`. v1's converter read a column `Galaxy` that `v1/reading/gas_values.csv` does not have; the column is `galaxy_as_printed`. The locator rule now gives the galaxy's row, named by `galaxy_as_printed`, and the columns `l_MHI`, `MHI` and `Dist`. It quotes "None" as the text it corrects. The table text and every value are unchanged. T1 to T6 were re-run after the change and pass; the T4 count is now 19 corrections.

## Test result

T1 to T6: see `reproduction/reissue_check.txt`. T7: run 1 failed (`reproduction/reachability_run1_fail.json`); run 2 passed after the ruled remedy (`reproduction/reachability.json`).
