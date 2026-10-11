import sys, time
sys.argv = ['x', sys.argv[1]]
exec(open('invfam.py').read().split("if __name__ == '__main__':")[0])
I12 = ['a_Gamma', 'A', 'M', "G2'", "G2'a", 'N1', 'N2', 'S', 'ac_le_ap', 'cp_le_ap', 'pAC', 'aCP']
step1 = [('mt','a','c'), idf('y'), ('comm','y','z'), idf('z')]
def cex(H, hyps, goal):
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
    r = solve(T, m, distinct=True, verbose=False, symbreak=False, extra=extra)
    if r:
        for v in ['a','c','y','z']:
            print(f"  {v:2s}", '  '.join(('[' if k=='T' else '(') + ' '.join(map(str,bl)) + (']' if k=='T' else ')') for bl,k in r[idx[v]]))
    else: print('  none')
print(f"m={m}: counterexample to I12(y) + y~z + z id => A(z):"); cex(step1, [(q, 'y') for q in I12], ('A', 'z'))
