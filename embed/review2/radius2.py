import sys, time, random
from collections import deque
from fast import *
import blk

def check_fast(n=4):
    P = projections(n); Pb = blk.all_projections(range(n))
    conv = lambda p: (tuple(sorted(sum(1 << x for x in b) for b in p[0])), sum(1 << x for b in p[1] for x in b))
    d = {conv(p): p for p in Pb}
    bad = 0
    for p in P:
        for q in P:
            if theta(p, q) != conv(blk.theta(d[p], d[q])): bad += 1
            if commute(p, q) != blk.commute(d[p], d[q]): bad += 1
    print('fast vs blk mismatches on P_%d:' % n, bad)

def ecc(a, c, n, P, verbose=True):
    t = time.time()
    idf = [y for y in P if theta(y, a) == theta(y, c)]
    dist = {c: 0}; dq = deque([c]); par = {}
    while dq:
        u = dq.popleft()
        for v in idf:
            if v not in dist and commute(u, v):
                dist[v] = dist[u] + 1; par[v] = u; dq.append(v)
    far = max(dist.values())
    if verbose:
        print(f'n={n} a={show(a,n)} c={show(c,n)}: {len(idf)} identifiers, component {len(dist)}, ecc(c)={far} ({time.time()-t:.0f}s)', flush=True)
        v = next(v for v, d in dist.items() if d == far)
        path = [v]
        while path[-1] != c: path.append(par[path[-1]])
        print('   geodesic:', ' ~ '.join(show(u, n) for u in reversed(path)), flush=True)
    return far, dist, idf

if __name__ == '__main__':
    check_fast(4)
    P6 = projections(6)
    ecc(parse('(0 2 3 4)(1)[5]', 6), parse('(0 3)(1)(2)(4)[5]', 6), 6, P6)
    P7 = projections(7)
    for sa, sc in [('(0 2 3 4 5)(1)[6]', '(0 3)(1)(2)(4)(5)[6]'),
                   ('(0 2 3 4 5)(1)[6]', '(0 3)(1)(2)(4 5)[6]'),
                   ('(0 2 3 4 5)(1)[6]', '(0 3 5)(1)(2)(4)[6]'),
                   ('(0 2 3 4)(1)(5)[6]', '(0 3)(1)(2)(4)(5)[6]'),
                   ('(0 2 3 4 5)(1)[6]', '(0 3)(1 5)(2)(4)[6]'),
                   ('(0 2 3 4 5 6)[1]', '(0 3 5)(2)(4)(6)[1]'),
                   ('(0 2 3 4 5 6)[1]', '(0 3)(2 5)(4)(6)[1]'),
                   ('(0 2 3 4)(5 6)[1]', '(0 3)(2)(4 5)(6)[1]'),
                   ]:
        ecc(parse(sa, 7), parse(sc, 7), 7, P7)
