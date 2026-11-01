"""Harvest (name, RA, Dec) from table rows of source texts. Only the name and the coordinate tokens
immediately after it are captured; nothing else on the row is read or written.
python3 -I harvest_pos.py out.csv label=file.txt [label=file.txt ...]"""
import sys, re
NAME = r'(?P<name>(?:Abell|ABELL|ACO|A|ZwCl|Zw|RXC ?J|RX ?J|MKW|NGC|MS|XLSSC|Coma|AWM|PSZ2 ?G|SPT-CL ?J)\s?[0-9][\w.+\-−]*(?:[+\-−][0-9.]+)?)'
DEC = r'(?P<ra>\d{1,3}\.\d{2,})\s+(?P<dec>[+−-]?\s?\d{1,2}\.\d{2,})'
SEX = r'(?P<ras>\d{1,2}[: ]\d\d[: ]\d\d(?:\.\d+)?)\s+(?P<decs>[+−-]\s?\d{1,2}[: ]\d\d[: ]\d\d(?:\.\d+)?)'
pd = re.compile(NAME + r'\s+(?:[A-Za-z][\w+\-]*\s+)?' + DEC)
ps = re.compile(NAME + r'\s+(?:[A-Za-z][\w+\-]*\s+)?(?:[\d.]+\s+)?' + SEX)
def deg_sex(ra, dec):
    r = [float(x) for x in re.split('[: ]', ra.strip())]
    d = dec.replace('−', '-').strip()
    s = -1 if d.startswith('-') else 1
    dd = [float(x) for x in re.split('[: ]', d.lstrip('+-').strip())]
    return 15 * (r[0] + r[1] / 60 + r[2] / 3600), s * (dd[0] + dd[1] / 60 + dd[2] / 3600)
out = open(sys.argv[1], 'w'); out.write('source,name,ra_deg,dec_deg\n'); n = {}
for arg in sys.argv[2:]:
    lab, fn = arg.split('=', 1)
    for l in open(fn, encoding='utf-8'):
        for m in ps.finditer(l):
            try: ra, dec = deg_sex(m.group('ras'), m.group('decs'))
            except Exception: print('skip', lab, repr(m.group('ras')), repr(m.group('decs'))); continue
            out.write(f"{lab},{m.group('name').strip()},{ra:.4f},{dec:.4f}\n"); n[lab] = n.get(lab, 0) + 1
        for m in pd.finditer(l):
            ra = float(m.group('ra')); dec = float(m.group('dec').replace('−', '-').replace(' ', ''))
            if ra <= 360 and abs(dec) <= 90:
                out.write(f"{lab},{m.group('name').strip()},{ra:.4f},{dec:.4f}\n"); n[lab] = n.get(lab, 0) + 1
print(n)
