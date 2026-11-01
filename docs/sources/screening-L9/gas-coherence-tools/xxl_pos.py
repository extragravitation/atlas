"""XLSSC id, RA, Dec (X-ray peak) and z from Umetsu et al. 2020 (arXiv:1909.10524) Table 1, for the 12 pairable XLSSC systems.
Only the id, position and z tokens are captured. python3 -I xxl_pos.py in.txt out.csv"""
import sys, re
ids = '027 054 055 060 061 087 088 091 098 103 104 112'.split()
pat = re.compile(r'\b(0?27|054|055|060|061|087|088|091|098|103|104|112)\s+(\d{1,3}\.\d{3,})\s+([+−-]?\d{1,2}\.\d{3,})\s+(0\.\d{3})')
seen = {}
for l in open(sys.argv[1], encoding='utf-8'):
    m = pat.search(l)
    if m:
        k = '%03d' % int(m.group(1))
        seen.setdefault(k, (m.group(2), m.group(3).replace('−', '-'), m.group(4)))
with open(sys.argv[2], 'w') as f:
    for k in ids:
        if k in seen: f.write(','.join((k,) + seen[k]) + '\n')
print(len(seen), 'of', len(ids))
