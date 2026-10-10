import sys, time, pickle
sys.argv = ['x', sys.argv[1], '3']
exec(open('inv5.py').read().split("t0 = time.time(); S = []")[0])
exec(open('inv4.py').read().split("def run(H, hyps, goal):")[0].split("class Ctx: pass")[1])   # make_J3
S, new = pickle.load(open('inv5_m4_K3.pkl', 'rb'))
def J3lits(c, u, v, cl):   # cl may contain ('J3', p, q, r) atoms
    out = []
    for s, a in cl:
        if a[0] == 'J3': out.append(s * c.J3s[a[1:]](u, v))
        else: out.append(lit_val(c, u, v, (s, a)))
    return out
def mkctx(pool, cls, E, Tl, J, X, idx, triples):
    c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in V if k in idx}; c.J3s = {}
    for tr in triples: c.J3s[tr] = make_J3(pool, cls, E, X, tuple(idx[p] for p in tr), tr)
    return c
GOAL = ((-1, ('J3', 'a', 'b', 'c')), (-1, ('T','c','u')), (-1, ('T','c','v')), (1, ('E','c')))
GOALa = ((-1, ('J3', 'a', 'b', 'c')), (-1, ('T','a','u')), (-1, ('T','a','v')), (1, ('E','a')))
GOALb = ((-1, ('J3', 'a', 'b', 'c')), (-1, ('T','b','u')), (-1, ('T','b','v')), (1, ('E','b')))
def holds(H, hyps, goal):
    T, idx = table(H, ('mt','a','b'))
    def extra(pool, E, Tl, J, cls, X):
        c = mkctx(pool, cls, E, Tl, J, X, idx, [('a','b','c')])
        for cl in hyps:
            for u in X:
                for v in X:
                    if u != v: cls.append(J3lits(c, u, v, cl))
        ors = []
        for u in X:
            for v in X:
                if u != v:
                    w_ = pool.id(('neg', u, v)); ors.append(w_)
                    for l in J3lits(c, u, v, goal): cls.append([-w_, -l])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
def valid_mt(H, hyps, concl=('a','b')):
    T, idx = table(H, ('mt',) + concl); N = len(T)
    def extra(pool, E, Tl, J, cls, X):
        c = mkctx(pool, cls, E, Tl, J, X, idx, [('a','b','c')])
        for cl in hyps:
            for u in X:
                for v in X:
                    if u != v: cls.append(J3lits(c, u, v, cl))
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
t = time.time()
print(f"m={m}: GOAL (no class of avbvc has two T(c)) under (W_2):", holds(W2, [], GOAL), f"({time.time()-t:.0f}s)", flush=True)
print(f"m={m}: GOALa under (W_2):", holds(W2, [], GOALa), "  GOALb:", holds(W2, [], GOALb), flush=True)
print(f"m={m}: GOAL implied by weak hyps + local clauses:", holds(weak, S, GOAL), flush=True)
print(f"m={m}: weak hyps + GOAL => a|><|b:", valid_mt(weak, [GOAL]), flush=True)
print(f"m={m}: weak hyps + GOAL + local clauses => a|><|b:", valid_mt(weak, S + [GOAL]), flush=True)
print(f"m={m}: weak hyps + GOAL + GOALa + GOALb => a|><|b:", valid_mt(weak, [GOAL, GOALa, GOALb]), flush=True)
