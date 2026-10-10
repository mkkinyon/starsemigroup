import sys, time, pickle
exec(open('g12.py').read().split("I = [A_y")[0])
def cex(H, hyps, goal):
    T, idx = table(H, ('mt','a','b'))
    def extra(pool, E, Tl, J, cls, X):
        c = mkctx(pool, cls, E, Tl, J, X, idx, TR)
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
    r = solve(T, m, distinct=True, verbose=False, symbreak=False, extra=extra)
    if r:
        for v in ['a','c','b','y']:
            print(f"  {v:2s}", '  '.join(('[' if k=='T' else '(') + ' '.join(map(str,bl)) + (']' if k=='T' else ')') for bl,k in r[idx[v]]))
    else: print('  none')
I = [A_y, M_y, G2p_y, G2pa_y] + Qy
print(f"m={m}: counterexample to weak + I(y) => G1 (all elements distinct):"); cex(weak, I, G1)
