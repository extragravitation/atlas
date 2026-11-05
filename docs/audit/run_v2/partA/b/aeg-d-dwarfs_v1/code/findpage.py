import sys
t=open(sys.argv[1]).read().split('\f')
for k in sys.argv[2:]:
    print(k, [i+1 for i,p in enumerate(t) if k in p])
