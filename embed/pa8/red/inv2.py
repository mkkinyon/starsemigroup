"""Clause-language invariant search.  Atoms over two points u != v: E(p,u,v), T(p,u), T(p,v), J(p,q,u,v), p,q in {x,a,c}.
Find clauses of <= K literals valid under (c~x, x id) [S1], valid at chain positions 2 and 3 [S3], and test propagation.
Usage: python3 inv2.py m K"""
import sys, time, itertools, pickle
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
m = int(sys.argv[1]); K = int(sys.argv[2]); DIST = len(sys.argv) > 3 and sys.argv[3] == "distinct"
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
V = ['x', 'a', 'c']
atoms = [('E', p) for p in V] + [('T', p, 'u') for p in V] + [('T', p, 'v') for p in V] + [('J', p, q) for p in V for q in V if p < q]
lits = [(s, a) for a in atoms for s in (1, -1)]
def lit_val(c, u, v, lit):
    s, a = lit
    if a[0] == 'E': x = c.E(c.i[a[1]], u, v)
    elif a[0] == 'T': x = c.Tl(c.i[a[1]], u if a[2] == 'u' else v)
    else: x = c.J(c.i[a[1]], c.i[a[2]], u, v)
    return s * x
def fmt(cl):
    def f(lit):
        s, a = lit
        t = f"E({a[1]})" if a[0] == 'E' else (f"T({a[1]},{a[2]})" if a[0] == 'T' else f"J({a[1]}{a[2]})")
        return t if s > 0 else '~' + t
    return ' | '.join(f(l) for l in cl)
class Ctx: pass
def run(H, hyps, goal):
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        def ctx(ren):
            c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; r = ren or {}
            c.i = {k: idx[r.get(k, k)] for k in V if r.get(k, k) in idx}; return c
        for cl, ren in hyps:
            c = ctx(ren)
            for u in X:
                for v in X:
                    if u != v: cls.append([lit_val(c, u, v, l) for l in cl])
        cl, ren = goal; c = ctx(ren); ors = []
        for u in X:
            for v in X:
                if u != v:
                    w_ = pool.id(('neg', u, v)); ors.append(w_)
                    for l in cl: cls.append([-w_, -lit_val(c, u, v, l)])
        cls.append(ors)
    return solve(T, m, distinct=DIST, verbose=False, symbreak=False, extra=extra) is None
def clauses():
    for k in range(1, K + 1):
        for cl in itertools.combinations(lits, k):
            if len({a for s, a in cl}) < k: continue      # no atom twice
            yield cl
def subsumed(cl, S):
    s = set(cl); return any(set(c2) <= s and len(c2) < len(cl) for c2 in S)
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
base2 = base1 + [('comm','x','y'), idf('y')]
base3 = base2 + [('comm','y','z'), idf('z')]
t0 = time.time(); S1 = []; n = 0
for cl in clauses():
    n += 1
    if subsumed(cl, S1): continue
    if run(base1, [], (cl, None)): S1.append(cl)
print(f"S1: {len(S1)} minimal valid clauses of <= {K} literals under (c~x, x id), {n} tested ({time.time()-t0:.0f}s)", flush=True)
S2 = [cl for cl in S1 if run(base2, [], (cl, {'x': 'y'}))]
print(f"S2: {len(S2)} of these valid at chain position 2 ({time.time()-t0:.0f}s)", flush=True)
S3 = [cl for cl in S2 if run(base3, [], (cl, {'x': 'z'}))]
print(f"S3: {len(S3)} valid at chain position 3 ({time.time()-t0:.0f}s)", flush=True)
for cl in S3: print('   ', fmt(cl))
pickle.dump((S1, S2, S3), open(f'inv2_m{m}_K{K}.pkl', 'wb'))
baseP = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
print("propagation of Q = S3 (for x) to y:", flush=True)
good = []
for cl in S3:
    ok = run(baseP, [(c2, None) for c2 in S3], (cl, {'x': 'y'}))
    print('   ', fmt(cl), 'PROPAGATES' if ok else 'fails', flush=True)
    if ok: good.append(cl)
print(f"{len(good)} of {len(S3)} propagate ({time.time()-t0:.0f}s)")
