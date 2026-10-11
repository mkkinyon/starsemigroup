"""For instances of (R'_inf) (x in Comp(c), y~a, theta_x(b)=theta_y(b), b|><|c): do delta, delta' of m*=theta_b(x)
equal delta(c), 0 ?  Also test the same for theta_b(y) and for x itself vs. y.   Usage: python3 rpinv.py n [budget]"""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
from collections import deque
def delta(x, a, c): return len(join(x, a)) - len(join(x, c))
def deltap(x, a, c): return sum(1 for K in join(x, a) if K & a[1]) - sum(1 for K in join(x, c) if K & c[1])
n = int(sys.argv[1]); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
P = projections(n); random.seed(5)
pairs = [(a, c) for a in P for c in P if matched(a, c)]
if n >= 5: random.shuffle(pairs)
t0 = time.time(); tried = inst = bad = badp = ybad = 0
for a, c in pairs:
    if time.time() - t0 > budget: break
    tried += 1; dc = delta(c, a, c)
    idf = [v for v in P if theta(v, a) == theta(v, c)]
    dist = {c: 0}; dq = deque([c])
    while dq:
        u = dq.popleft()
        for v in idf:
            if v not in dist and commute(u, v): dist[v] = dist[u] + 1; dq.append(v)
    comp = list(dist)
    Ys = [y for y in P if commute(y, a)]
    for b in P:
        if not matched(b, c): continue
        tb = {}
        for y in Ys: tb.setdefault(theta(y, b), []).append(y)
        for x in comp:
            r = theta(x, b)
            if r not in tb: continue
            inst += 1
            ms = theta(b, x)
            if delta(ms, a, c) != dc:
                bad += 1
                if bad <= 3: print('delta(theta_b(x)) wrong: a=%s c=%s b=%s x=%s y=%s' % (show(a, n), show(c, n), show(b, n), show(x, n), show(tb[r][0], n)))
            elif deltap(ms, a, c) != 0:
                badp += 1
                if badp <= 3: print("delta'(theta_b(x)) wrong: a=%s c=%s b=%s x=%s y=%s" % (show(a, n), show(c, n), show(b, n), show(x, n), show(tb[r][0], n)))
            for y in tb[r]:
                if delta(y, a, c) != dc or deltap(y, a, c) != 0: ybad += 1
print("P_%d: %d pairs, %d instances: delta(theta_b(x)) != delta(c) in %d, delta' != 0 in %d; (delta,delta')(y) wrong in %d (%.0fs)" % (n, tried, inst, bad, badp, ybad, time.time() - t0), flush=True)
