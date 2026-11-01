import sys,re
L=open(sys.argv[1]).read().split('\n')
names=[]
for rng in [(373,429),(438,494),(503,538)]:
    for l in L[rng[0]-1:rng[1]]:
        t=l.split()
        if not t: continue
        if re.match(r'^(A\d+b?|S\d+|AWM\d|DC\d+-\d+|Eridanus|MKW\d|Ursa|Virgo)$',t[0]):
            if t[0] not in names: names.append(t[0])
        else: print('SKIP',l[:30])
print(len(names)); print(' '.join(names))
