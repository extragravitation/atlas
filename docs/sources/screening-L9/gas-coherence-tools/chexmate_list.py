"""Extract name, X-ray-peak RA/Dec, z and Tier from CHEX-MATE Collaboration 2021 (arXiv:2010.11972) Tables B.1-B.3.
Columns M500, SNR, nH and exposures are skipped and never written. python3 -I chexmate_list.py in.txt out.csv"""
import sys, re
txt = open(sys.argv[1], encoding='utf-8').read()  # whole text: the B tables are split across pages; the row pattern is specific to them
pat = re.compile(r'PSZ2\s+(G\d{3}\.\d{2}[+−-]\d{2}\.\d{2})\s+(\d\d:\d\d:\d\d\.?\d*)\s+([+−-]\d\d:\d\d:\d\d\.?\d*)\s+(\d\.\d+)\s+\S+\s+\S+\s+(12|1|2)\s')
out, seen = [], set()
for l in txt.splitlines():
    for m in pat.finditer(l):
      if m.group(1) not in seen:
        seen.add(m.group(1)); out.append(('PSZ2 ' + m.group(1).replace('−', '-'), m.group(2), m.group(3).replace('−', '-'), m.group(4), m.group(5)))
with open(sys.argv[2], 'w') as f:
    f.write('name,ra_xpeak,dec_xpeak,z,tier\n')
    for r in out: f.write(','.join(r) + '\n')
print(len(out), 'rows;', sum(float(r[3]) < 0.30 for r in out), 'below z=0.30')
