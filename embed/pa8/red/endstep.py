import sys, time
sys.argv = ['x', sys.argv[1]]
exec(open('invfam.py').read().split("if __name__ == '__main__':")[0])
# extra goal predicates about b (with y as the chain end): G1(b) = A(b); L1' : eps_y ^ (a v b v c) <= eps_b ; G2 for (a,b,c)
PRED["L1'"] = (2, lambda c, p, u, v, w: [-c.E(c.i['y'], u, v), -c.J3s['abc'](u, v), c.E(c.i['b'], u, v)])
PRED['G2abc'] = (2, lambda c, p, u, v, w: [-c.J3s['abc'](u, v), -c.Tl(c.i['c'], u), -c.Tl(c.i['c'], v), c.E(c.i['c'], u, v)])
PRED['Cmeet'] = (2, lambda c, p, u, v, w: [c.E(c.i['c'], u, v), -c.J(c.i['a'], c.i['c'], u, v), -c.J(c.i['b'], c.i['c'], u, v)])
def run2(H, hyps, goal):
    T, idx = table(H, ('mt', 'a', 'b'))
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in idx if isinstance(k, str)}; c.J3s = {}
        for (_, p) in hyps + [goal]:
            if p not in c.J3s and p in idx: c.J3s[p] = make_J3(pool, cls, E, X, tuple(sorted((idx['a'], idx['c'], idx[p]))), p)
        c.J3s['abc'] = make_J3(pool, cls, E, X, tuple(sorted((idx['a'], idx['b'], idx['c']))), 'abc')
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
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
I12 = ['a_Gamma', 'A', 'M', "G2'", "G2'a", 'N1', 'N2', 'S', 'ac_le_ap', 'cp_le_ap', 'pAC', 'aCP']
end = [('mt','a','c'), ('mt','c','b'), ('comm','y','b'), idf('y')]
t0 = time.time()
for g in [('a_Gamma','b'), ('A','b'), ("L1'",'b'), ('Cmeet','b'), ('G2abc','b'), ('M','b'), ("G2'",'b')]:
    print(f"m={m}: I12(y) + y~b + b|><|c + y id => {g[0]}({g[1]}): {run2(end, [(q, 'y') for q in I12], g)} ({time.time()-t0:.0f}s)", flush=True)
