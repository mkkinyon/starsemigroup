"""(R'_inf) instances (x in Comp_ac(c), y~a, theta_x(b)=theta_y(b), b|><|c): is there z in Comp_bc(c) with z~a?
Is y itself in Id(b,c)?  Usage: python3 rpred.py n [budget]"""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
from collections import deque
def compo(a, c, P):
    idf = [v for v in P if theta(v, a) == theta(v, c)]
    dist = {c: 0}; dq = deque([c])
    while dq:
        u = dq.popleft()
        for v in idf:
            if v not in dist and commute(u, v): dist[v] = dist[u] + 1; dq.append(v)
    return list(dist)
n = int(sys.argv[1]); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
P = projections(n); random.seed(6)
pairs = [(a, c) for a in P for c in P if matched(a, c)]
if n >= 5: random.shuffle(pairs)
t0 = time.time(); tried = inst = noz = ynot = 0
cache = {}
for a, c in pairs:
    if time.time() - t0 > budget: break
    tried += 1
    comp = compo(a, c, P)
    Ys = [y for y in P if commute(y, a)]
    for b in P:
        if not matched(b, c): continue
        if (b, c) not in cache: cache[(b, c)] = compo(b, c, P)
        cbc = cache[(b, c)]
        hasz = any(commute(z, a) for z in cbc)
        tb = {}
        for y in Ys: tb.setdefault(theta(y, b), []).append(y)
        for x in comp:
            r = theta(x, b)
            if r not in tb: continue
            for y in tb[r]:
                inst += 1
                if theta(y, c) != r: ynot += 1
                if not hasz:
                    noz += 1
                    if noz <= 3: print('no z: a=%s c=%s b=%s x=%s y=%s' % (show(a, n), show(c, n), show(b, n), show(x, n), show(y, n)), flush=True)
print("P_%d: %d pairs, %d instances; y not in Id(b,c): %d; no z in Comp_bc(c) commuting with a: %d (%.0fs)" % (n, tried, inst, ynot, noz, time.time() - t0), flush=True)
