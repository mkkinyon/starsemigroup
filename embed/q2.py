"""Test on P_n:
 Q1: r=prp & r=qrq  ==> pq=qp   (projections)           [James East's condition]
 Q2: pqp=p, qpq=q, qrq=q, rqr=r, rpr=r, prp=p ==> pqr=pr  (triangle flatness)
"""
import sys, itertools, time
from pmon import Pn, projections, is_projection

def run(n):
    P = Pn(n)
    projs = projections(n)
    assert all(is_projection(p, n) for p in projs)
    print(f"P_{n}: {len(projs)} projections")
    # Q1
    t = time.time()
    below = {p: set() for p in projs}          # below[p] = {r : r <= p}
    for p in projs:
        for r in projs:
            if P.prod(p, r, p) == r:
                below[p].add(r)
    bad1 = 0
    for p, q in itertools.combinations(projs, 2):
        if below[p] & below[q]:
            if P.mul(p, q) != P.mul(q, p):
                bad1 += 1
    print(f"  Q1 violations: {bad1}   ({time.time()-t:.1f}s)")
    # Q2: same-D-class relation D(p,q): pqp=p and qpq=q
    t = time.time()
    byrank = {}
    for p in projs:
        byrank.setdefault(P.rank(p), []).append(p)
    nbr = {p: set() for p in projs}
    for k, ps in byrank.items():
        for p, q in itertools.combinations(ps, 2):
            if P.prod(p, q, p) == p and P.prod(q, p, q) == q:
                nbr[p].add(q); nbr[q].add(p)
    bad2 = 0; triangles = 0
    for p in projs:
        for q in nbr[p]:
            for r in nbr[p] & nbr[q]:
                triangles += 1
                if P.prod(p, q, r) != P.mul(p, r):
                    bad2 += 1
                    if bad2 <= 3:
                        print("   non-flat triangle:", p, q, r)
    print(f"  Q2: {triangles} ordered triangles, {bad2} non-flat   ({time.time()-t:.1f}s)")

if __name__ == "__main__":
    for n in range(1, int(sys.argv[1]) + 1):
        run(n)
