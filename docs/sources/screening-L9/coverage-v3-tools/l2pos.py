import sys,re
L=open(sys.argv[1]).read().split('\n')
pos={}
for rng in [(373,429),(438,494),(503,538)]:
    for l in L[rng[0]-1:rng[1]]:
        t=l.split()
        if not t or not re.match(r'^(A\d+b?|S\d+|AWM\d|DC\d+-\d+|Eridanus|MKW\d|Ursa|Virgo)$',t[0]): continue
        m=re.search(r'(\d[\d ]{4,5}\d?\.\d)([-+ ])([\d ]{6})',l)
        if not m: print('NOPOS',t[0],file=sys.stderr); continue
        ra=m.group(1).replace(' ','0').rjust(8,'0'); sg=m.group(2) if m.group(2)!=' ' else '+'; de=m.group(3).replace(' ','0')
        p=f'{ra}{sg}{de}'
        pos.setdefault(t[0],set()).add(p)
for k,v in pos.items(): print(k+','+';'.join(sorted(v)))
