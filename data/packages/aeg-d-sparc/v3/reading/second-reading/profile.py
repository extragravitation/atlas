import sys
f, start = sys.argv[1], int(sys.argv[2])
L = open(f,'rb').read().decode('ascii').split('\n')
L = [l.rstrip('\r') for l in L]
data = [l for l in L[start:] if l.strip()]
W = max(len(l) for l in data)
occ = ''.join('X' if any(i < len(l) and l[i] != ' ' for l in data) else '.' for i in range(W))
print(len(data), W)
for k in range(0, W, 10): print(f"{k+1:>4}", occ[k:k+10])
print(''.join(str((i+1)//10%10) if (i+1)%10==0 else ' ' for i in range(W)))
print(''.join(str((i+1)%10) for i in range(W)))
print(occ)
