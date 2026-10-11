import sys, time, random
from radius2 import ecc
from fast import *
n = int(sys.argv[1]); budget = float(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
random.seed(seed)
P = projections(n)
low = [p for p in P if bin(p[1]).count('1') <= 2 and p[1]]   # rank-ish small support
t0 = time.time(); best = 0; tried = 0
while time.time() - t0 < budget:
    a = random.choice(low); c = random.choice(low)
    if a == c or not matched(a, c): continue
    tried += 1
    far, dist, idf = ecc(a, c, n, P, verbose=False)
    if far > best or far >= 4:
        print(f'ecc {far}: a={show(a,n)} c={show(c,n)} (component {len(dist)}, identifiers {len(idf)}) t={time.time()-t0:.0f}s', flush=True)
        if far > best: best = far
print('tried', tried, 'best', best)
