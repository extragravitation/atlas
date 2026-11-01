import sys,re
L=open(sys.argv[1]).read().split('\n')
out=[]
for i,l in enumerate(L[988:1292],start=989):
    m=re.match(r'^\s*([0-9a-z][0-9a-z]+)\s+(0\.\d{3,4})\b',l)
    if m: out.append((i,m.group(1),m.group(2)))
for o in out: print(*o)
print('N',len(out))
