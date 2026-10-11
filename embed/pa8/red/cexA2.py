import sys, time
sys.argv = ['x', sys.argv[1]]
exec(open('cexA.py').read().split('print(f"m={m}: counterexample')[0])
def cex2(H, hyps, goal, nondeg=True, show=True):
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in idx if isinstance(k, str)}; c.J3s = {}
        for (_, p) in hyps + [goal]:
            if p not in c.J3s: c.J3s[p] = make_J3(pool, cls, E, X, tuple(sorted((idx['a'], idx['c'], idx[p]))), p)
        for name, p in hyps:
            ar, f = PRED[name]
            for u in X:
                for v in X:
                    if u == v: continue
                    for w in (X if ar == 3 else [u]): cls.append(f(c, p, u, v, w))
        name, p = goal; ar, f = PRED[name]; ors = []
        for u in X:
            for v in X:
                if u == v: continue
                for w in (X if ar == 3 else [u]):
                    s = pool.id(('neg', u, v, w)); ors.append(s)
                    for l in f(c, p, u, v, w): cls.append([-s, -l])
        cls.append(ors)
        if nondeg: cls.append([Tl(idx['a'], u) for u in X])     # rank a >= 1
    r = solve(T, m, distinct=True, verbose=False, symbreak=False, extra=extra)
    if r and show:
        for v in ['a','c','y','z']:
            print(f"  {v:2s}", '  '.join(('[' if k=='T' else '(') + ' '.join(map(str,bl)) + (']' if k=='T' else ')') for bl,k in r[idx[v]]))
    return r is None
t = time.time()
print(f"m={m}: nondegenerate (rank a >= 1): I12(y) + y~z + z id => A(z): {cex2(step1, [(q, 'y') for q in I12], ('A', 'z'))} ({time.time()-t:.0f}s)")
