"""Raw-text VOTable reader: returns fields and rows of TD strings exactly as printed, with row index (1-based TR order)."""
import re, sys
def read(path):
    s = open(path, encoding='utf-8').read()
    fields = re.findall(r'<FIELD name="([^"]*)"', s)
    rows = []
    for tr in re.findall(r'<TR>(.*?)</TR>', s, re.S):
        tds = re.findall(r'<TD>(.*?)</TD>|<TD/>', tr)
        # re.findall with alternation returns '' for <TD/>
        rows.append(tds)
    return fields, rows
if __name__ == '__main__':
    path, *names = sys.argv[1:]
    f, rows = read(path)
    print(len(f), len(rows))
    for i, r in enumerate(rows, 1):
        d = dict(zip(f, r))
        if any(n == d.get('Cluster','').strip() for n in names):
            print('TR', i, {k: v for k, v in d.items()})
