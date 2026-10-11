import sys
sys.argv = ['x', sys.argv[1]]
exec(open('pairstat.py').read().split("base2 = ")[0])
base2 = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y')]
def cex(H, goal):
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in idx if isinstance(k, str)}; c.J3s = {}
        name, p = goal; ar, f = PRED[name]; ors = []
        for u in X:
            for v in X:
                if u == v: continue
                s = pool.id(('neg', u, v)); ors.append(s)
                for l in f(c, p, u, v, u): cls.append([-s, -l])
        cls.append(ors)
        cls.append([Tl(idx['a'], u) for u in X])
    r = solve(T, m, distinct=True, verbose=False, symbreak=False, extra=extra)
    if r:
        for v in ['a','c','x','y']:
            print(f"  {v:2s}", '  '.join(('[' if k=='T' else '(') + ' '.join(map(str,bl)) + (']' if k=='T' else ')') for bl,k in r[idx[v]]))
cex(base2, ('x_le_ya', 'y'))
