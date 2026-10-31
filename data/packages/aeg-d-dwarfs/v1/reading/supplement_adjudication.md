# Adjudication log: aeg-d-dwarfs/v1 supplementary reading

Settled against the paper text only (arXiv PDFs listed in sheet.csv); nothing computed. Format: field | key | paper | readers -> final. Reason.

Conventions applied:
1. Where a paper prints both a semi-major a_h and a circularised r_h, code `semi_major_stated` and say "both printed" in `note`. The conversion uses a_h and the ellipticity, per the frozen REPRODUCTION.md.
2. A definition given only by citing another paper (e.g. "following Martin et al. 2008") counts as `not_stated`, unless the paper itself writes out the elliptical radius.
3. (mu) Values compared as printed; where readers differ only in formatting, the paper's table form is adopted.

- rh | fornax_1 | Wang2019 | R1 elliptical_radius_profile, R2 not_stated -> not_stated. Elliptical radius only by citation to Martin et al. (2008) and a figure axis label; not written out (citation convention).
- mu | grus_1 | Cantu2021 | R1 "20.48 (+0.11, −0.22)", R2 "20.48 +0.11 −0.22". Same value, formatting only; Table 5 form adopted.
- mu | leo_6 | Tan2025 | R1 "20.23 (+0.17, see Table 1 for lower error ...)", R2 "20.23 +0.17 −0.12". R1 lower error missing; Table 1 prints −0.12. R2.
- rh | lmc | Choi2018 | R1 elliptical_radius_profile, R2 not_stated -> elliptical_radius_profile (R1). The paper writes out the elliptical radius (Eq. 6) with semi-major scale, so the citation exception applies. Caveat: no r_h printed, only exponential rd, in deprojected disk-plane coordinates.
- rh | pegasus_3 | Richstein2022 | R1 circularised_stated, R2 semi_major_stated -> semi_major_stated. Both printed (ah semi-major and circularised rh); both-printed convention.
- mu | pegasus_4 | Cerny2023 | R1 "19.77 ± 0.03 (stat) ± 0.1 (sys)" (Sec. 5.5 text), R2 "19.77 +0.03 −0.03 ± 0.1" (Table 1). Same value, both printed; Table 1 form adopted.
- mu | phoenix_2 | Richstein2024 | R1 "19.85 (+0.16, −0.17)", R2 "19.85 +0.16 −0.17". Formatting only; Table 2 form adopted. mv_distance_source not in dispute, R1 kept.
- mu | pictor_2 | Pace2025 | R1 "18.26 (+0.04, −0.03) ± 0.1 (sys)", R2 "18.26 +0.04 −0.03 ± 0.1". Formatting only; Table 1 form adopted. The paper is internally inconsistent (text 18.45); both readers note it; value kept from Table 1.
- rh | pisces_2 | Richstein2022 | R1 circularised_stated, R2 semi_major_stated -> semi_major_stated. Both printed; both-printed convention.
- efit | smc | Munoz2018 | R1 no, R2 not_stated -> no (R1). The paper states it did not study the SMC, so it fits no ellipticity; its re is a compiled literature value. Matches how both readers coded other compiled values (e.g. cetus_1 in McConnachie 2012: no).
- efit | andromeda_27 | Richardson2011 | R1 no, R2 yes -> no (R1). For And XXVII the joint ML grid (which fits ϵ with rh) failed; ϵ came from moments and was held fixed while the exponential profile was fitted. R2 quoted the general method, which this system did not use.
- rh | cassiopeia_3 | Rhode2023 | R1 elliptical_radius_profile, R2 not_stated -> not_stated. Elliptical radius defined only by citing Martin et al. (2008) Eq. 4 (citation convention).
- rh | lacerta_1 | Rhode2023 | R1 elliptical_radius_profile, R2 not_stated -> not_stated. Elliptical radius defined only by citing Martin et al. (2008) Eq. 4 (citation convention).
- rh | perseus_1 | Rhode2023 | R1 elliptical_radius_profile, R2 not_stated -> not_stated. Elliptical radius defined only by citing Martin et al. (2008) Eq. 4 (citation convention).
