import sys
m_arg = sys.argv[1]; sys.argv = ['x', m_arg]
exec(open('modules.py').read().split("step = ")[0])
step = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
def cex(H, hyps, goal, show=['a','c','x','y']):
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
        cls.append(ors); cls.append([Tl(idx['a'], u) for u in X])
    r = solve(T, m, distinct=True, verbose=False, symbreak=False, extra=extra)
    if r:
        for v in show: print(f"  {v:2s}", '  '.join(('[' if k=='T' else '(') + ' '.join(map(str,bl)) + (']' if k=='T' else ')') for bl,k in r[idx[v]]))
    else: print("  none")
for drop in ['A', 'M', 'Np_cblock']:
    hy = [(q, 'x') for q in ['A', 'M', 'Np_cblock'] if q != drop]
    print(f"m={m}: counterexample to M2 without {drop}(x):"); cex(step, hy, ('A', 'y'))
