"""(W_infty) at (a,c) in P_m: for every y in Comp(c) (component of c in I(a,c)) and every b ~ y with b|><|c: a|><|b.
This checks all (W_n), n >= 1, at once for the given (a,c).  Exhaustive over matched pairs in P_4, P_5; random in P_6, P_7."""
import sys, time, random
from collections import deque
from fast import *
m = int(sys.argv[1]); mode = sys.argv[2]
P = projections(m)
def comp(a, c, idf):
    dist = {c: 0}; dq = deque([c])
    while dq:
        u = dq.popleft()
        for v in idf:
            if v not in dist and commute(u, v):
                dist[v] = dist[u] + 1; dq.append(v)
    return dist
t0 = time.time(); tried = 0; viol = 0; maxd = 0
if mode == 'all':
    pairs = [(a, c) for a in P for c in P if matched(a, c)]
else:
    random.seed(int(sys.argv[3])); budget = float(sys.argv[4])
    def gen():
        while True:
            a = random.choice(P); c = random.choice(P)
            if matched(a, c): yield (a, c)
    pairs = gen()
for a, c in pairs:
    if mode != 'all' and time.time() - t0 > budget: break
    tried += 1
    idf = [y for y in P if theta(y, a) == theta(y, c)]
    dist = comp(a, c, idf)
    Bc = [b for b in P if matched(b, c) and not matched(a, b)]
    for y, d in dist.items():
        for b in Bc:
            if commute(y, b):
                viol += 1; maxd = max(maxd, d)
                print(f'VIOLATION of (W_{d}): a={show(a,m)} c={show(c,m)} y={show(y,m)} b={show(b,m)}', flush=True)
    if mode != 'all' and tried % 20 == 0: print(f'  ... {tried} pairs, {time.time()-t0:.0f}s', flush=True)
print(f'P_{m}: {tried} matched pairs tested for (W_infty): {viol} violations (max chain length {maxd}); {time.time()-t0:.0f}s')
