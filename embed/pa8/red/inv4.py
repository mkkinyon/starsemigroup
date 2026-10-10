"""Clause-language invariant search with 3-way joins J3 = eps_a v eps_c v eps_x.  Usage: python3 inv4.py m K [distinct]"""
import sys, time, itertools, pickle
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
m = int(sys.argv[1]); K = int(sys.argv[2]); DIST = len(sys.argv) > 3 and sys.argv[3] == "distinct"
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
V = ['x', 'a', 'c']
atoms = [('E', p) for p in V] + [('T', p, 'u') for p in V] + [('T', p, 'v') for p in V] + [('J', p, q) for p in V for q in V if p < q] + [('J3',)]
lits = [(s, a) for a in atoms for s in (1, -1)]
def lit_val(c, u, v, lit):
    s, a = lit
    if a[0] == 'E': x = c.E(c.i[a[1]], u, v)
    elif a[0] == 'T': x = c.Tl(c.i[a[1]], u if a[2] == 'u' else v)
    elif a[0] == 'J': x = c.J(c.i[a[1]], c.i[a[2]], u, v)
    else: x = c.J3(u, v)
    return s * x
def fmt(cl):
    def f(lit):
        s, a = lit
        t = f"E({a[1]})" if a[0] == 'E' else (f"T({a[1]},{a[2]})" if a[0] == 'T' else (f"J({a[1]}{a[2]})" if a[0] == 'J' else "J3(acx)"))
        return t if s > 0 else '~' + t
    return ' | '.join(f(l) for l in cl)
class Ctx: pass
def make_J3(pool, cls, E, X, ps, tag):
    """transitive closure of E(p1)|E(p2)|E(p3): returns J3(x,y)"""
    m_ = len(X)
    def R(i, x, y):
        if x > y: x, y = y, x
        return pool.id(("R3", tag, i, x, y))
    for x in X:
        for y in X:
            if x < y:
                r0 = R(0, x, y); cls.append([-r0] + [E(p, x, y) for p in ps])
                for p in ps: cls.append([r0, -E(p, x, y)])
    L = max(1, (m_ - 1).bit_length())
    for i in range(L):
        for x in X:
            for y in X:
                if x < y:
                    aux = []
                    for u in X:
                        if u in (x, y): continue
                        a = pool.id(("aux3", tag, i, x, y, u))
                        cls.append([-a, R(i, x, u)]); cls.append([-a, R(i, u, y)]); cls.append([a, -R(i, x, u), -R(i, u, y)]); aux.append(a)
                    nxt = R(i + 1, x, y); cls.append([-nxt, R(i, x, y)] + aux); cls.append([nxt, -R(i, x, y)])
                    for a in aux: cls.append([nxt, -a])
    return lambda x, y: R(L, x, y)
def run(H, hyps, goal):
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        cache = {}
        def ctx(ren):
            c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; r = ren or {}
            c.i = {k: idx[r.get(k, k)] for k in V if r.get(k, k) in idx}
            key = tuple(sorted(c.i.values()))
            if key not in cache: cache[key] = make_J3(pool, cls, E, X, key, key)
            c.J3 = cache[key]; return c
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
            if len({a for s, a in cl}) < k: continue
            yield cl
def subsumed(cl, S):
    s = set(cl); return any(set(c2) <= s and len(c2) < len(cl) for c2 in S)
if __name__ == '__main__':
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
    print(f"S2: {len(S2)} valid at chain position 2 ({time.time()-t0:.0f}s)", flush=True)
    S3 = [cl for cl in S2 if run(base3, [], (cl, {'x': 'z'}))]
    print(f"S3: {len(S3)} valid at chain position 3 ({time.time()-t0:.0f}s)", flush=True)
    for cl in S3: print('   ', fmt(cl))
    pickle.dump((S1, S2, S3), open(f'inv4_m{m}_K{K}.pkl', 'wb'))
    baseP = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
    Q = list(S3)
    while True:
        good = [cl for cl in Q if run(baseP, [(c2, None) for c2 in Q], (cl, {'x': 'y'}))]
        print(f"propagation: {len(good)} of {len(Q)} ({time.time()-t0:.0f}s)", flush=True)
        if len(good) == len(Q): break
        Q = good
    pickle.dump(Q, open(f'inv4Q_m{m}_K{K}.pkl', 'wb'))
    print("fixed-point invariant Q:"); [print('   ', fmt(cl)) for cl in Q]
    # closing
    def valid_mt(H, hyps, concl=('a','b')):
        T, idx = table(H, ('mt',) + concl); N = len(T)
        def extra(pool, E, Tl, J, cls, X):
            c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in V}; key = tuple(sorted(c.i.values())); c.J3 = make_J3(pool, cls, E, X, key, key)
            for cl, ren in hyps:
                for u in X:
                    for v in X:
                        if u != v: cls.append([lit_val(c, u, v, l) for l in cl])
        for (q, p) in ((concl[1], concl[0]), (concl[0], concl[1])):
            T2 = [row[:] + [None] for row in T] + [[None] * (N + 1)]
            for i in range(N + 1): T2[i][i] = i
            w = T2[idx[q]][idx[p]]
            if w is not None:
                if w == idx[p]: continue
                if solve(T, m, distinct=[(w, idx[p])], verbose=False, symbreak=False, extra=extra) is not None: return False
                continue
            T2[idx[q]][idx[p]] = N
            if solve(T2, m, distinct=[(N, idx[p])], verbose=False, symbreak=False, extra=extra) is not None: return False
        return True
    P = [('mt','a','c'), ('mt','c','b')]; hy = [(cl, None) for cl in Q]
    print("closing (W): Q(x), x id, x~b, b|><|c => a|><|b:", valid_mt(P + [idf('x'), ('comm','x','b')], hy), flush=True)
    print("closing (R'): Q(x), x id, y~a, th_x(b)=th_y(b) => a|><|b:", valid_mt(P + [idf('x'), ('comm','y','a'), ('eq',('x','b'),('y','b'))], hy), flush=True)
