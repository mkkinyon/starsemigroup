"""(R'_infty) in the order formulation: x in Comp(c), y~a, theta_x(b)=theta_y(b), b|><|c => a|><|b ?
Also: is there always z in Comp(c) with z~b (reduction to (W_infty))?   Usage: python3 rpinf.py n [budget]"""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
from collections import deque
n = int(sys.argv[1]); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
P = projections(n); random.seed(4)
pairs = [(a, c) for a in P for c in P if matched(a, c)]
if n >= 5: random.shuffle(pairs)
t0 = time.time(); tried = inst = viol = nored = 0
for a, c in pairs:
    if time.time() - t0 > budget: break
    tried += 1
    idf = [v for v in P if theta(v, a) == theta(v, c)]
    dist = {c: 0}; dq = deque([c])
    while dq:
        u = dq.popleft()
        for v in idf:
            if v not in dist and commute(u, v): dist[v] = dist[u] + 1; dq.append(v)
    comp = list(dist)
    Ys = [y for y in P if commute(y, a)]
    Bs = [b for b in P if matched(b, c)]
    for b in Bs:
        tb = {}
        for y in Ys: tb.setdefault(theta(y, b), []).append(y)
        hasz = any(commute(z, b) for z in comp)
        for x in comp:
            r = theta(x, b)
            if r in tb:
                inst += len(tb[r])
                if not matched(a, b):
                    viol += len(tb[r])
                    if viol <= 3: print('VIOLATION a=%s c=%s b=%s x=%s y=%s' % (show(a, n), show(c, n), show(b, n), show(x, n), show(tb[r][0], n)), flush=True)
                if not hasz:
                    nored += len(tb[r])
                    if nored <= 3: print('no z: a=%s c=%s b=%s x=%s y=%s (d(x)=%d)' % (show(a, n), show(c, n), show(b, n), show(x, n), show(tb[r][0], n), dist[x]), flush=True)
print("P_%d: %d pairs, %d instances of (R'_inf), %d violations, %d without z in Comp(c) commuting with b (%.0fs)" % (n, tried, inst, viol, nored, time.time() - t0), flush=True)
