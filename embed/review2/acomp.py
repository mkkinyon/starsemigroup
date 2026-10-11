"""Is a ever in the component of c in I(a,c)?  (If (W_n) holds for all n, it cannot be, whenever some b ~ a with b|><|c, a not|><| b exists.)
Exhaustive over all matched pairs a != c in P_4, P_5; random in P_6/P_7."""
import sys, time, random
from collections import deque
from fast import *

def comp(a, c, P, idf=None):
    idf = idf or [y for y in P if theta(y, a) == theta(y, c)]
    dist = {c: 0}; dq = deque([c])
    while dq:
        u = dq.popleft()
        for v in idf:
            if v not in dist and commute(u, v):
                dist[v] = dist[u] + 1; dq.append(v)
    return dist, idf

n = int(sys.argv[1]); mode = sys.argv[2]
P = projections(n)
t0 = time.time(); found = 0; tried = 0; maxecc = 0
if mode == 'all':
    pairs = [(a, c) for a in P for c in P if a != c and matched(a, c)]
    print(len(pairs), 'ordered matched pairs a != c in P_%d' % n, flush=True)
else:
    random.seed(int(sys.argv[3])); budget = float(sys.argv[4])
    def gen():
        while True:
            a = random.choice(P); c = random.choice(P)
            if a != c and matched(a, c): yield (a, c)
    pairs = gen()
for a, c in pairs:
    if mode != 'all' and time.time() - t0 > budget: break
    tried += 1
    dist, idf = comp(a, c, P)
    e = max(dist.values()); maxecc = max(maxecc, e)
    if a in dist:
        found += 1
        print('a IN comp(c): a=%s c=%s dist=%d' % (show(a, n), show(c, n), dist[a]), flush=True)
    if mode != 'all' and e >= 5:
        print('ecc %d: a=%s c=%s' % (e, show(a, n), show(c, n)), flush=True)
print('P_%d: tried %d pairs, a in comp(c) in %d cases, max ecc %d (%.0fs)' % (n, tried, found, maxecc, time.time() - t0))
