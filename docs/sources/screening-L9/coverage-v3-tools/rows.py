import sys,re
want=set(sys.argv[2].split(','))
cols=[int(c) for c in sys.argv[3].split(',')]
for line in open(sys.argv[1]):
    if not line.startswith('|'): continue
    cells=[c.strip() for c in line.strip().strip('|').split('|')]
    if not cells: continue
    rid=re.sub(r'\*','',cells[0]).strip()
    if rid in want:
        print('=== ',rid)
        for c in cols:
            if c < len(cells): print(f'[{c}]',cells[c])
