"""Invariant search: block-level predicates about (x; a, c) in P(P_m).
Predicates are universal statements over points; each has clause generators for use as hypothesis and as negated goal.
Usage: python3 inv.py m"""
import sys, time, itertools
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
m = int(sys.argv[1])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
# ---- predicate language.  A predicate is (name, body) where body(ctx, u, v) returns a list of literals L such that
# the predicate says: for all u != v (or all u for unary): OR(L).   ctx gives E, Tl, J, idx.
def Pcls(p, q, r):   # blocks of p inside classes of q v r
    return (f"[{p} in {q}v{r}]", lambda c, u, v: [-c.E(c.i[p], u, v), c.J(c.i[q], c.i[r], u, v)])
def PclsT(p, q, r):  # T-blocks of p inside classes of q v r
    return (f"[T({p}) in {q}v{r}]", lambda c, u, v: [-c.E(c.i[p], u, v), -c.Tl(c.i[p], u), c.J(c.i[q], c.i[r], u, v)])
def PclsN(p, q, r):  # N-blocks of p inside classes of q v r
    return (f"[N({p}) in {q}v{r}]", lambda c, u, v: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), c.J(c.i[q], c.i[r], u, v)])
def Pno2T(q, r, s):  # no class of q v r contains two T(s)-blocks
    return (f"[no class of {q}v{r} has two T({s})]", lambda c, u, v: [-c.J(c.i[q], c.i[r], u, v), -c.Tl(c.i[s], u), -c.Tl(c.i[s], v), c.E(c.i[s], u, v)])
def PNin(p, q):      # every N(p)-block meeting supp q lies inside supp q
    return (f"[N({p}) meeting supp {q} inside it]", lambda c, u, v: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), -c.Tl(c.i[q], u), c.Tl(c.i[q], v)])
def PTin(p, q):      # every T(p)-block meeting supp q lies inside supp q
    return (f"[T({p}) meeting supp {q} inside it]", lambda c, u, v: [-c.E(c.i[p], u, v), -c.Tl(c.i[p], u), -c.Tl(c.i[q], u), c.Tl(c.i[q], v)])
def Psupp(p, q):     # supp p subset supp q   (unary: v ignored)
    return (f"[supp {p} <= supp {q}]", lambda c, u, v: [-c.Tl(c.i[p], u), c.Tl(c.i[q], u)])
def Pdisj(p, q):
    return (f"[supp {p} disjoint supp {q}]", lambda c, u, v: [-c.Tl(c.i[p], u), -c.Tl(c.i[q], u)])
def Pmeet(q, r, s, t):  # every class of q v r meeting supp s meets supp t   -- needs existential; handled specially
    return (f"[classes of {q}v{r} meeting supp {s} meet supp {t}]", ('meet', q, r, s, t))
V = ['x', 'a', 'c']
preds = []
for p in V:
    for q in V:
        for r in V:
            if q < r and p not in (q, r): preds += [Pcls(p, q, r), PclsT(p, q, r), PclsN(p, q, r)]
for q in V:
    for r in V:
        if q < r:
            for s in V:
                if s not in (q, r): preds.append(Pno2T(q, r, s))
for p in V:
    for q in V:
        if p != q: preds += [PNin(p, q), PTin(p, q), Psupp(p, q)]
for p in V:
    for q in V:
        if p < q: preds.append(Pdisj(p, q))
for q in V:
    for r in V:
        if q < r:
            for s in V:
                for t in V:
                    if s != t and s not in (q, r) and t not in (q, r): pass
preds += [Pmeet('a','x','x','c'), Pmeet('a','x','x','a'), Pmeet('c','x','x','a'), Pmeet('c','x','x','c'), Pmeet('a','c','c','a'),
          Pmeet('a','x','a','c'), Pmeet('c','x','c','a'), Pmeet('a','x','c','a'), Pmeet('c','x','a','c')]
class Ctx: pass
def run(H, hyps, goal):
    """H: atoms; hyps: list of (pred, ren) assumed; goal: (pred, ren) to refute.  ren maps predicate variable names to table names."""
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        def ctx(ren):
            c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; r = ren or {}
            c.i = {k: idx[r.get(k, k)] for k in V + ['y', 'z', 'b'] if r.get(k, k) in idx}; return c
        for (name, body), ren in hyps:
            c = ctx(ren)
            if isinstance(body, tuple) and body[0] == 'meet':
                _, q, rr, s, t = body
                for u in X:
                    cls.append([-Tl(c.i[s], u)] + [pool.id(('mw', name, u, w)) for w in X])
                    for w in X:
                        a_ = pool.id(('mw', name, u, w)); cls.append([-a_, Tl(c.i[t], w)])
                        if w != u: cls.append([-a_, J(c.i[q], c.i[rr], u, w)])
            else:
                for u in X:
                    for v in X:
                        if u != v: cls.append(body(c, u, v))
        (name, body), ren = goal; c = ctx(ren); ors = []
        if isinstance(body, tuple) and body[0] == 'meet':
            _, q, rr, s, t = body
            for u in X:
                w_ = pool.id(('negm', u)); ors.append(w_)
                cls.append([-w_, Tl(c.i[s], u)])
                for w in X:
                    cls.append([-w_, -Tl(c.i[t], w)] + ([-J(c.i[q], c.i[rr], u, w)] if w != u else []))
        else:
            for u in X:
                for v in X:
                    if u != v:
                        w_ = pool.id(('neg', u, v)); ors.append(w_)
                        for lit in body(c, u, v): cls.append([-w_, -lit])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
base2 = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y')]
base3 = base2 + [('comm','y','z'), idf('z')]
t0 = time.time()
S1 = [P for P in preds if run(base1, [], (P, None))]
print(f"valid for x (c~x, x id): {len(S1)}/{len(preds)} ({time.time()-t0:.0f}s)", flush=True)
for P in S1: print('  ', P[0])
S2 = [P for P in preds if run(base2, [], (P, {'x': 'y'}))]
print(f"valid for y (c~x~y, both id): {len(S2)} ({time.time()-t0:.0f}s)", flush=True)
for P in S2: print('  ', P[0])
S3 = [P for P in S2 if run(base3, [], (P, {'x': 'z'}))]
print(f"valid for z (c~x~y~z, all id): {len(S3)} ({time.time()-t0:.0f}s)", flush=True)
for P in S3: print('  ', P[0])
baseP = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
print("propagation of the conjunction Q = S3 (assumed for x) to y:", flush=True)
for P in S3:
    ok = run(baseP, [(Q, None) for Q in S3], (P, {'x': 'y'}))
    print('  ', P[0], 'PROPAGATES' if ok else 'fails', flush=True)
