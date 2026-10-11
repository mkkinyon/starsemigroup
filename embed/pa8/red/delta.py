"""The counting invariant delta(x) = |eps_x v eps_a| - |eps_x v eps_c| (and delta' with supports) on the
identification graph I(a,c).  Checks: (1) delta, delta' constant on components (proved by hand);
(2) completeness: is Comp(c) = {x in Id : delta(x)=delta(c), delta'(x)=0}?
Usage: python3 delta.py n [budget_seconds]   (n=4 exhaustive; n>=5 random pairs within budget)"""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import projections, join, theta, commute, matched, show
from collections import deque
def comp(a, c, P, idf=None):
    idf = idf or [y for y in P if theta(y, a) == theta(y, c)]
    dist = {c: 0}; dq = deque([c])
    while dq:
        u = dq.popleft()
        for v in idf:
            if v not in dist and commute(u, v):
                dist[v] = dist[u] + 1; dq.append(v)
    return dist, idf

def delta(x, a, c):
    return len(join(x, a)) - len(join(x, c))
def deltap(x, a, c):
    return sum(1 for K in join(x, a) if K & a[1]) - sum(1 for K in join(x, c) if K & c[1])

n = int(sys.argv[1]); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
P = projections(n); random.seed(1)
pairs = [(a, c) for a in P for c in P if a != c and matched(a, c)]
if n >= 5: random.shuffle(pairs)
t0 = time.time(); tried = 0; bad = 0; incomplete = 0; ncomp = []; hist = {}
for a, c in pairs:
    if time.time() - t0 > budget: break
    tried += 1
    dist, idf = comp(a, c, P)
    # all components of Id
    seen = {}; k = 0
    for x in idf:
        if x in seen: continue
        d, _ = comp(a, c, P, idf);
        break
    # cheaper: label components by BFS from each unseen vertex
    label = {}; k = 0
    for x in idf:
        if x in label: continue
        stack = [x]; label[x] = k
        while stack:
            u = stack.pop()
            for v in idf:
                if v not in label and commute(u, v):
                    label[v] = k; stack.append(v)
        k += 1
    ncomp.append(k)
    vals = {}
    for x in idf:
        vals.setdefault(label[x], set()).add((delta(x, a, c), deltap(x, a, c)))
    if any(len(s) > 1 for s in vals.values()):
        bad += 1; print('NOT CONSTANT: a=%s c=%s' % (show(a, n), show(c, n)), flush=True)
    dc = (delta(c, a, c), 0)
    S = {x for x in idf if (delta(x, a, c), deltap(x, a, c)) == dc}
    C = set(dist)
    if S != C:
        incomplete += 1
        if incomplete <= 5:
            extra = [show(x, n) for x in S - C][:4]
            print('incomplete: a=%s c=%s |Comp|=%d |{delta=delta(c)}|=%d  e.g. %s' % (show(a, n), show(c, n), len(C), len(S), extra), flush=True)
    hist[k] = hist.get(k, 0) + 1
print('P_%d: %d pairs, invariants not constant on a component: %d, (delta,delta\') incomplete for Comp(c): %d; #components histogram %s (%.0fs)'
      % (n, tried, bad, incomplete, sorted(hist.items()), time.time() - t0))
