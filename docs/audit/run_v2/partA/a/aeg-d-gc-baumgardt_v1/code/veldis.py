"""Parse Baumgardt veldis.html into bins: (cluster, r, N, sigma, up, low, type, html_line)."""
import re, html
def parse(path):
    lines = open(path, encoding='latin-1').read().split('\n')
    cells = []  # (text, line)
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r'<td[^>]*>(.*?)</td>', ln):
            cells.append((html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).replace('\xa0', ' '), i))
    bins = []; cur = None; k = 0
    # data rows: 7 consecutive cells where the 7th is a type code and 2nd parses as float
    while k + 6 < len(cells):
        grp = cells[k:k+7]
        try:
            float(grp[1][0]); float(grp[3][0])
            ok = re.fullmatch(r'[A-Z0-9]+', grp[6][0].strip()) is not None
        except ValueError:
            ok = False
        if ok:
            name = grp[0][0].strip()
            if name: cur = name
            bins.append(dict(cluster=cur, r=grp[1][0].strip(), N=grp[2][0].strip(), sigma=grp[3][0].strip(),
                             up=grp[4][0].strip(), low=grp[5][0].strip(), type=grp[6][0].strip(), line=grp[1][1]))
            k += 7
        else:
            k += 1
    return bins
if __name__ == '__main__':
    import sys
    b = parse(sys.argv[1])
    print(len(b), len(set(x['cluster'] for x in b)))
    for n in sys.argv[2:]:
        for x in b:
            if x['cluster'] == n: print(x)
