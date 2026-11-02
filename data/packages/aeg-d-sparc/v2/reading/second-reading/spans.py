import sys, re, collections
f, start = sys.argv[1], int(sys.argv[2])
L = [l.rstrip('\r') for l in open(f,'rb').read().decode('ascii').split('\n')]
data = [l for l in L[start:] if l.strip()]
nt = collections.Counter(len(l.split()) for l in data); print('token counts', nt)
n = max(nt)
spans = [[999,0] for _ in range(n)]
for l in data:
    ms = list(re.finditer(r'\S+', l))
    if len(ms)!=n: print('ODD', repr(l)); continue
    for i,m in enumerate(ms):
        spans[i][0]=min(spans[i][0],m.start()+1); spans[i][1]=max(spans[i][1],m.end())
for i,s in enumerate(spans): print(i, s)
