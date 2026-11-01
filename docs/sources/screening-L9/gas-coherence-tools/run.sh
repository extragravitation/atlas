#!/bin/sh
# Reproduce gas-coherence-A9.md tables. DL = folder with the arXiv PDFs (pdftotext -layout -> TXT), OUT = output folder.
# Downloads: curl -sSL https://arxiv.org/pdf/<id>; PSZ2: IRSA HFI_PCCS_SZ-union_R2.08.fits.gz (tried, not used for matching).
set -e
T=$(dirname "$0"); REPO=$(cd "$T/../../../.." && pwd); TXT=$1; OUT=$2
python3 -I $REPO/docs/sources/screening-L9/coverage-v3-tools/cov3.py $REPO/docs/sources/screening-S9/coverage-A9-v2.md $REPO/docs/sources/screening-L9/coverage-v3-tools $OUT/cov3.json
python3 -I $T/pairable.py $OUT/cov3.json $OUT/pairable.json
python3 -I $T/chexmate_list.py $TXT/2010.11972.txt $OUT/chexmate.csv
python3 -I $T/xxl_pos.py $TXT/1909.10524.txt $OUT/xxl_pos.csv
python3 -I $T/harvest_pos.py $OUT/positions.csv mulroy19=$TXT/1901.11276.txt martino14=$TXT/1406.6831.txt checs=$TXT/2202.08569.txt \
  clashx=$TXT/1405.7876.txt rines13=$TXT/1209.3786.txt pizzardo21=$TXT/2005.11562.txt cairns=$TXT/astro-ph_0306538.txt \
  umetsu20=$TXT/1909.10524.txt klein19=$TXT/1908.10114.txt li24=$TXT/2411.09735.txt hicks06=$TXT/astro-ph_0609334.txt \
  mulroy14=$TXT/1407.1767.txt okabesmith16=$TXT/1507.04493.txt
python3 -I $T/build.py $OUT/pairable.json $OUT/positions.csv $OUT/chexmate.csv $OUT/xxl_pos.csv $REPO/docs/sources/screening-L9/coverage-v3-tools/L5a.csv $OUT
python3 -I $T/gen_md.py $OUT/gas.json $OUT
