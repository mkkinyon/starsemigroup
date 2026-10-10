"""Evaluators for the quasi-identities of Section 5.8 (order-8 census) on a projection algebra table A[x][y] = theta_y(x).
Each returns a violating assignment or None."""
import itertools

def _basic(A):
    N = len(A); th = lambda p, q: A[q][p]
    mt = lambda p, q: th(p, q) == p and th(q, p) == q
    le = lambda p, q: th(q, p) == p
    comm = lambda p, q: th(p, q) == th(q, p)
    matched = {p: [q for q in range(N) if mt(p, q)] for p in range(N)}
    return N, th, mt, le, comm, matched

def paths(matched, n, mt):
    def rec(prefix):
        if len(prefix) == n + 1: yield prefix; return
        for q in matched[prefix[-1]]: yield from rec(prefix + [q])
    for p0 in matched:
        for P in rec([p0]):
            if not mt(P[0], P[-1]): yield P

def Rprime(A):
    """a~c, b~c, xc=cx, th_x(a)=th_x(c), ya=ay, th_x(b)=th_y(b) => a~b"""
    N, th, mt, le, comm, matched = _basic(A)
    for a, c, b in paths(matched, 2, mt):
        for x in range(N):
            if comm(x, c) and th(x, a) == th(x, c):
                for y in range(N):
                    if comm(y, a) and th(x, b) == th(y, b): return ('Rprime', a, c, b, x, y)
    return None

def V(A):
    """bcb=b, ata<=b, ctc<=a => ata<=btb"""
    N, th, mt, le, comm, matched = _basic(A)
    for b in range(N):
        for c in range(N):
            if th(b, c) != b: continue
            for a in range(N):
                for t in range(N):
                    if le(th(a, t), b) and le(th(c, t), a) and not le(th(a, t), th(b, t)): return ('V', a, b, c, t)
    return None

def _path3(A, name, test):
    N, th, mt, le, comm, matched = _basic(A)
    for P in paths(matched, 3, mt):
        r = test(P, N, th, comm)
        if r is not None: return (name,) + tuple(P) + tuple(r)
    return None

def P1(A):
    """x comm p0,p1; th_p0(x)=th_p2(x); th_x(p1)=th_x(p3) => p0~p3"""
    def test(P, N, th, comm):
        for x in range(N):
            if comm(x, P[0]) and comm(x, P[1]) and th(P[0], x) == th(P[2], x) and th(x, P[1]) == th(x, P[3]): return (x,)
    return _path3(A, 'P1', test)

def P2(A):
    """x comm p0,p2; th_x(p1)=th_x(p2); th_p1(x)=th_p3(x) => p0~p3"""
    def test(P, N, th, comm):
        for x in range(N):
            if comm(x, P[0]) and comm(x, P[2]) and th(x, P[1]) == th(x, P[2]) and th(P[1], x) == th(P[3], x): return (x,)
    return _path3(A, 'P2', test)

def Q(A):
    """x comm p0; th_p1(x)=th_p3(x); y comm p0,p2; th_y(p1)=th_y(p2) => p0~p3"""
    def test(P, N, th, comm):
        xs = [x for x in range(N) if comm(x, P[0]) and th(P[1], x) == th(P[3], x)]
        if not xs: return None
        for y in range(N):
            if comm(y, P[0]) and comm(y, P[2]) and th(y, P[1]) == th(y, P[2]): return (xs[0], y)
    return _path3(A, 'Q', test)

def E6(A):
    """dbd=d, aca=a, ada=a, u<=c, u<=d, bcb=aua => aua=a"""
    N, th, mt, le, comm, matched = _basic(A)
    for a in range(N):
        for c in range(N):
            if th(a, c) != a: continue
            for d in range(N):
                if th(a, d) != a: continue
                for u in range(N):
                    if not (le(u, c) and le(u, d)) or th(a, u) == a: continue
                    for b in range(N):
                        if th(d, b) == d and th(b, c) == th(a, u): return ('E6', a, b, c, d, u)
    return None

def E1(A):
    """z<=b, aba=z, dbd=d, xcx=z, aca=a, bcb=b, e<=x, e<=d, ada=a => aba=a"""
    N, th, mt, le, comm, matched = _basic(A)
    for a in range(N):
        for b in range(N):
            z = th(a, b)
            if z == a or not le(z, b): continue
            for c in range(N):
                if th(a, c) != a or th(b, c) != b: continue
                for d in range(N):
                    if th(a, d) != a or th(d, b) != d: continue
                    for x in range(N):
                        if th(x, c) != z: continue
                        if any(le(e, x) and le(e, d) for e in range(N)): return ('E1', a, b, c, d, x, z)
    return None

ALL = [Rprime, V, P1, P2, Q, E6, E1]

def violated(A):
    for f in ALL:
        r = f(A)
        if r is not None: return r
    return None

if __name__ == "__main__":
    import json, sys, os
    recs = [json.loads(l) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "post8.log"))]
    cands = [r["A"] for r in recs if r["embeds"] is None]
    for i, C in enumerate(cands): print(i, [f(C) for f in ALL])
    sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
    from fourth import table
    print("P7", [f(table()) for f in ALL])
